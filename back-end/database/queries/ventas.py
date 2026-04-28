from database.connection import get_connection, return_connection


# Trae el listado de ventas usando la vista v_ventas_completo
def get_all() -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, fecha::text, total, descuento,
                       cliente, nit, empleado, metodo_pago
                FROM v_ventas_completo
                ORDER BY fecha DESC
            """)
            cols = [desc[0] for desc in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        return_connection(conn)


# Trae una venta completa con todos sus items por JOINs
def get_by_id(venta_id: int) -> dict | None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Datos de la venta
            cur.execute("""
                SELECT v.id, v.cliente_id, cl.nombre AS cliente_nombre,
                       v.empleado_id, e.nombre AS empleado_nombre,
                       v.metodo_pago_id, mp.metodo AS metodo_pago,
                       v.fecha::text, v.total, v.descuento
                FROM ventas v
                INNER JOIN clientes cl      ON v.cliente_id     = cl.id
                INNER JOIN empleados e      ON v.empleado_id    = e.id
                INNER JOIN metodos_pago mp  ON v.metodo_pago_id = mp.id
                WHERE v.id = %s
            """, (venta_id,))
            row = cur.fetchone()
            if row is None:
                return None
            cols = [desc[0] for desc in cur.description]
            venta = dict(zip(cols, row))

            # Items de la venta
            cur.execute("""
                SELECT iv.producto_id, p.nombre AS producto_nombre,
                       iv.cantidad, iv.precio_unitario_historico, iv.subtotal
                FROM items_venta iv
                INNER JOIN productos p ON iv.producto_id = p.id
                WHERE iv.venta_id = %s
            """, (venta_id,))
            cols_items = [desc[0] for desc in cur.description]
            venta["items"] = [dict(zip(cols_items, r)) for r in cur.fetchall()]

            return venta
    finally:
        return_connection(conn)


# Registra una venta completa en una sola transacción:
# 1. Obtiene el precio actual de cada producto
# 2. Inserta la venta y sus items
# 3. Descuenta el stock de cada producto
# Si cualquier paso falla, hace rollback y no queda nada a medias
def crear(cliente_id: int, empleado_id: int, metodo_pago_id: int, descuento: float, items: list) -> dict:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Obtener precio actual de cada producto y calcular totales
            items_procesados = []
            total = 0.0
            for item in items:
                cur.execute("SELECT precio, stock FROM productos WHERE id = %s", (item["producto_id"],))
                producto = cur.fetchone()
                if producto is None:
                    raise ValueError(f"Producto {item['producto_id']} no encontrado")
                precio, stock = producto
                if stock < item["cantidad"]:
                    raise ValueError(f"Stock insuficiente para producto {item['producto_id']}")
                subtotal = float(precio) * item["cantidad"]
                total += subtotal
                items_procesados.append({
                    "producto_id": item["producto_id"],
                    "cantidad":    item["cantidad"],
                    "precio":      float(precio),
                    "subtotal":    subtotal,
                })

            total_final = total - descuento

            # Insertar la venta
            cur.execute("""
                INSERT INTO ventas (cliente_id, empleado_id, metodo_pago_id, total, descuento)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (cliente_id, empleado_id, metodo_pago_id, total_final, descuento))
            venta_id = cur.fetchone()[0]

            # Insertar cada item y descontar stock
            for item in items_procesados:
                cur.execute("""
                    INSERT INTO items_venta (venta_id, producto_id, cantidad, precio_unitario_historico, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (venta_id, item["producto_id"], item["cantidad"], item["precio"], item["subtotal"]))

                cur.execute("""
                    UPDATE productos SET stock = stock - %s WHERE id = %s
                """, (item["cantidad"], item["producto_id"]))

            conn.commit()

        return get_by_id(venta_id)

    except Exception:
        # Si algo falla, deshacer todos los cambios de esta transacción
        conn.rollback()
        raise
    finally:
        return_connection(conn)
