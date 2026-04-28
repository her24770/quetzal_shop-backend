from database.connection import get_connection, return_connection


# Trae todos los proveedores ordenados alfabéticamente
def get_all() -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, nombre, telefono, email, direccion
                FROM proveedores
                ORDER BY nombre
            """)
            cols = [desc[0] for desc in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        return_connection(conn)


# Busca un proveedor por ID, retorna None si no existe
def get_by_id(proveedor_id: int) -> dict | None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, nombre, telefono, email, direccion
                FROM proveedores
                WHERE id = %s
            """, (proveedor_id,))
            row = cur.fetchone()
            if row is None:
                return None
            cols = [desc[0] for desc in cur.description]
            return dict(zip(cols, row))
    finally:
        return_connection(conn)


# Trae todos los productos asociados a un proveedor con su precio de costo
def get_productos(proveedor_id: int) -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.id, p.nombre, p.descripcion, p.precio,
                       pp.precio_costo, c.nombre AS categoria
                FROM producto_proveedor pp
                INNER JOIN productos p   ON pp.producto_id  = p.id
                INNER JOIN categorias c  ON p.categoria_id  = c.id
                WHERE pp.proveedor_id = %s
                ORDER BY p.nombre
            """, (proveedor_id,))
            cols = [desc[0] for desc in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        return_connection(conn)


# Inserta un proveedor y retorna el registro creado
def create(nombre: str, telefono: str, email: str, direccion: str) -> dict:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO proveedores (nombre, telefono, email, direccion)
                VALUES (%s, %s, %s, %s)
                RETURNING id, nombre, telefono, email, direccion
            """, (nombre, telefono, email, direccion))
            conn.commit()
            cols = [desc[0] for desc in cur.description]
            return dict(zip(cols, cur.fetchone()))
    finally:
        return_connection(conn)


# Actualiza solo los campos recibidos y retorna el proveedor actualizado
def update(proveedor_id: int, campos: dict) -> dict | None:
    if not campos:
        return get_by_id(proveedor_id)

    sets = ", ".join(f"{k} = %s" for k in campos)
    valores = list(campos.values()) + [proveedor_id]

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE proveedores SET {sets} WHERE id = %s", valores)
            conn.commit()
            if cur.rowcount == 0:
                return None
        return get_by_id(proveedor_id)
    finally:
        return_connection(conn)


# Elimina un proveedor por ID; lanza ValueError si tiene compras o productos asociados
def delete(proveedor_id: int) -> bool:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM proveedores WHERE id = %s", (proveedor_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        if "foreign key" in str(e).lower() or "violates" in str(e).lower():
            raise ValueError("No se puede eliminar: el proveedor tiene compras o productos asociados")
        raise
    finally:
        return_connection(conn)
