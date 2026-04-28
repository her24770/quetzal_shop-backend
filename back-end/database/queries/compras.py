from database.connection import get_connection, return_connection


# Trae el listado de compras con el nombre del empleado
def get_all() -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.fecha::text, c.total, c.numero_factura,
                       e.nombre AS empleado
                FROM compras c
                INNER JOIN empleados e ON c.empleado_id = e.id
                ORDER BY c.fecha DESC
            """)
            cols = [desc[0] for desc in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        return_connection(conn)


# Trae una compra completa con todos sus items por JOINs
def get_by_id(compra_id: int) -> dict | None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Datos de la compra
            cur.execute("""
                SELECT c.id, c.empleado_id, e.nombre AS empleado_nombre,
                       c.fecha::text, c.total, c.numero_factura
                FROM compras c
                INNER JOIN empleados e ON c.empleado_id = e.id
                WHERE c.id = %s
            """, (compra_id,))
            row = cur.fetchone()
            if row is None:
                return None
            cols = [desc[0] for desc in cur.description]
            compra = dict(zip(cols, row))

            # Items de la compra
            cur.execute("""
                SELECT ic.producto_id, p.nombre AS producto_nombre,
                       ic.proveedor_id, pr.nombre AS proveedor_nombre,
                       ic.cantidad, ic.precio_costo_historico, ic.subtotal
                FROM items_compra ic
                INNER JOIN productos  p  ON ic.producto_id  = p.id
                INNER JOIN proveedores pr ON ic.proveedor_id = pr.id
                WHERE ic.compra_id = %s
            """, (compra_id,))
            cols_items = [desc[0] for desc in cur.description]
            compra["items"] = [dict(zip(cols_items, r)) for r in cur.fetchall()]

            return compra
    finally:
        return_connection(conn)


# Registra una compra completa en una sola transacción:
# 1. Inserta la compra y sus items con el precio de costo recibido
# 2. Suma el stock de cada producto recibido
# Si cualquier paso falla, hace rollback y no queda nada a medias
def crear(empleado_id: int, numero_factura: str, items: list) -> dict:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Validar que cada producto y proveedor existan y calcular total
            items_procesados = []
            total = 0.0
            for item in items:
                cur.execute("SELECT id FROM productos WHERE id = %s", (item["producto_id"],))
                if cur.fetchone() is None:
                    raise ValueError(f"Producto {item['producto_id']} no encontrado")

                cur.execute("SELECT id FROM proveedores WHERE id = %s", (item["proveedor_id"],))
                if cur.fetchone() is None:
                    raise ValueError(f"Proveedor {item['proveedor_id']} no encontrado")

                subtotal = item["precio_costo"] * item["cantidad"]
                total += subtotal
                items_procesados.append({
                    "producto_id":  item["producto_id"],
                    "proveedor_id": item["proveedor_id"],
                    "cantidad":     item["cantidad"],
                    "precio_costo": item["precio_costo"],
                    "subtotal":     subtotal,
                })

            # Insertar la compra
            cur.execute("""
                INSERT INTO compras (empleado_id, numero_factura, total)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (empleado_id, numero_factura, total))
            compra_id = cur.fetchone()[0]

            # Insertar cada item y sumar stock
            for item in items_procesados:
                cur.execute("""
                    INSERT INTO items_compra (compra_id, producto_id, proveedor_id, cantidad, precio_costo_historico, subtotal)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (compra_id, item["producto_id"], item["proveedor_id"], item["cantidad"], item["precio_costo"], item["subtotal"]))

                cur.execute("""
                    UPDATE productos SET stock = stock + %s WHERE id = %s
                """, (item["cantidad"], item["producto_id"]))

            conn.commit()

        return get_by_id(compra_id)

    except Exception:
        # Si algo falla, deshacer todos los cambios de esta transacción
        conn.rollback()
        raise
    finally:
        return_connection(conn)
