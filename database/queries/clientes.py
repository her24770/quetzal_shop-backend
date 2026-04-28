from database.connection import get_connection, return_connection


# Trae todos los clientes ordenados alfabéticamente
def get_all() -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, nombre, nit, telefono, direccion
                FROM clientes
                ORDER BY nombre
            """)
            cols = [desc[0] for desc in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        return_connection(conn)


# Busca un cliente por ID, retorna None si no existe
def get_by_id(cliente_id: int) -> dict | None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, nombre, nit, telefono, direccion
                FROM clientes
                WHERE id = %s
            """, (cliente_id,))
            row = cur.fetchone()
            if row is None:
                return None
            cols = [desc[0] for desc in cur.description]
            return dict(zip(cols, row))
    finally:
        return_connection(conn)


# Busca un cliente por NIT, útil para identificarlo rápido en caja
def get_by_nit(nit: str) -> dict | None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, nombre, nit, telefono, direccion
                FROM clientes
                WHERE nit = %s
            """, (nit,))
            row = cur.fetchone()
            if row is None:
                return None
            cols = [desc[0] for desc in cur.description]
            return dict(zip(cols, row))
    finally:
        return_connection(conn)


# Inserta un cliente y retorna el registro creado
def create(nombre: str, nit: str, telefono: str, direccion: str) -> dict:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO clientes (nombre, nit, telefono, direccion)
                VALUES (%s, %s, %s, %s)
                RETURNING id, nombre, nit, telefono, direccion
            """, (nombre, nit, telefono, direccion))
            conn.commit()
            cols = [desc[0] for desc in cur.description]
            return dict(zip(cols, cur.fetchone()))
    finally:
        return_connection(conn)


# Actualiza solo los campos recibidos y retorna el cliente actualizado
def update(cliente_id: int, campos: dict) -> dict | None:
    if not campos:
        return get_by_id(cliente_id)

    sets = ", ".join(f"{k} = %s" for k in campos)
    valores = list(campos.values()) + [cliente_id]

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE clientes SET {sets} WHERE id = %s", valores)
            conn.commit()
            if cur.rowcount == 0:
                return None
        return get_by_id(cliente_id)
    finally:
        return_connection(conn)


# Elimina un cliente por ID, retorna True si se eliminó algo
def delete(cliente_id: int) -> bool:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
            conn.commit()
            return cur.rowcount > 0
    finally:
        return_connection(conn)
