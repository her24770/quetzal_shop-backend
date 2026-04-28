from database.connection import get_connection, return_connection


# Trae todas las categorías ordenadas alfabéticamente
def get_all() -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre, descripcion FROM categorias ORDER BY nombre")
            cols = [desc[0] for desc in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        return_connection(conn)


# Busca una categoría por su ID, retorna None si no existe
def get_by_id(categoria_id: int) -> dict | None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, nombre, descripcion FROM categorias WHERE id = %s",
                (categoria_id,)
            )
            row = cur.fetchone()
            if row is None:
                return None
            cols = [desc[0] for desc in cur.description]
            return dict(zip(cols, row))
    finally:
        return_connection(conn)


# Inserta una nueva categoría y retorna el registro creado
def create(nombre: str, descripcion: str) -> dict:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s) RETURNING id, nombre, descripcion",
                (nombre, descripcion)
            )
            conn.commit()
            cols = [desc[0] for desc in cur.description]
            return dict(zip(cols, cur.fetchone()))
    finally:
        return_connection(conn)


# Elimina una categoría por ID, retorna True si se eliminó algo
def delete(categoria_id: int) -> bool:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM categorias WHERE id = %s", (categoria_id,))
            conn.commit()
            return cur.rowcount > 0
    finally:
        return_connection(conn)
