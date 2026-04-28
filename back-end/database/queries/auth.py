from database.connection import get_connection, return_connection

# funcion para extraccion de data según el email
def get_user_by_email(email: str) -> dict | None:
    """
    Busca un usuario por email y trae su rol y datos de empleado.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    u.id AS user_id,
                    u.email,
                    u.password_hash,
                    u.rol_id,
                    r.nombre AS rol_nombre,
                    e.id AS empleado_id,
                    e.nombre AS nombre_empleado
                FROM usuarios u
                INNER JOIN roles r ON u.rol_id     = r.id
                LEFT  JOIN empleados e ON e.usuario_id = u.id
                WHERE u.email = %s
            """, (email,))

            row = cur.fetchone()
            if row is None:
                return None

            # Convertir la tupla en dict usando los nombres de columna
            cols = [desc[0] for desc in cur.description]
            return dict(zip(cols, row))
    finally:
        return_connection(conn)
