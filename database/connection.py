import psycopg2
from psycopg2 import pool
from config import settings

# Pool de conexiones (evita crear una conexión nueva en cada request)
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD
)

def get_connection():
    """Obtiene una conexión del pool"""
    return connection_pool.getconn()

def return_connection(conn):
    """Devuelve una conexión al pool"""
    connection_pool.putconn(conn)

def close_all_connections():
    """Cierra todas las conexiones del pool (útil en shutdown)"""
    connection_pool.closeall()
