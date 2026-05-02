from database.connection import get_connection, return_connection


# Trae todos los empleados con su email y rol por JOIN a usuarios y roles
def get_all() -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT e.id, e.usuario_id, e.dpi, e.nombre, e.telefono, e.cargo,
                       e.fecha_contrato::text, e.estado,
                       u.email, r.nombre AS rol_nombre
                FROM empleados e
                INNER JOIN usuarios u ON e.usuario_id = u.id
                INNER JOIN roles r    ON u.rol_id     = r.id
                ORDER BY e.nombre
            """)
            cols = [desc[0] for desc in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        return_connection(conn)


# Busca un empleado por ID con su email y rol, retorna None si no existe
def get_by_id(empleado_id: int) -> dict | None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT e.id, e.usuario_id, e.dpi, e.nombre, e.telefono, e.cargo,
                       e.fecha_contrato::text, e.estado,
                       u.email, r.nombre AS rol_nombre
                FROM empleados e
                INNER JOIN usuarios u ON e.usuario_id = u.id
                INNER JOIN roles r    ON u.rol_id     = r.id
                WHERE e.id = %s
            """, (empleado_id,))
            row = cur.fetchone()
            if row is None:
                return None
            cols = [desc[0] for desc in cur.description]
            return dict(zip(cols, row))
    finally:
        return_connection(conn)


# Crea el usuario y el empleado en una sola transacción
def create(email: str, password_hash: str, rol_id: int, dpi: str, nombre: str, telefono: str, cargo: str, fecha_contrato: str) -> dict:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO usuarios (email, password_hash, rol_id) VALUES (%s, %s, %s) RETURNING id",
                (email, password_hash, rol_id),
            )
            usuario_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO empleados (usuario_id, dpi, nombre, telefono, cargo, fecha_contrato)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (usuario_id, dpi, nombre, telefono, cargo, fecha_contrato))
            empleado_id = cur.fetchone()[0]
            conn.commit()
        return get_by_id(empleado_id)
    except Exception:
        conn.rollback()
        raise
    finally:
        return_connection(conn)


# Actualiza solo los campos recibidos y retorna el empleado actualizado
def update(empleado_id: int, campos: dict) -> dict | None:
    if not campos:
        return get_by_id(empleado_id)

    sets = ", ".join(f"{k} = %s" for k in campos)
    valores = list(campos.values()) + [empleado_id]

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE empleados SET {sets} WHERE id = %s", valores)
            conn.commit()
            if cur.rowcount == 0:
                return None
        return get_by_id(empleado_id)
    finally:
        return_connection(conn)


# Elimina un empleado por ID; lanza ValueError si tiene ventas o compras registradas
def delete(empleado_id: int) -> bool:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM empleados WHERE id = %s", (empleado_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        if "foreign key" in str(e).lower() or "violates" in str(e).lower():
            raise ValueError("No se puede eliminar: el empleado tiene ventas o compras registradas")
        raise
    finally:
        return_connection(conn)
