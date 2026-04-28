from database.connection import get_connection, return_connection


# Trae todos los métodos de pago disponibles
def get_all() -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, metodo FROM metodos_pago ORDER BY id")
            cols = [desc[0] for desc in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        return_connection(conn)
