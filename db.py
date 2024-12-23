import psycopg2
from psycopg2 import sql

# Configuración de la conexión
DB_NAME = "task_manager"
DB_USER = "psqladmin"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    """Devuelve una nueva conexión a la base de datos."""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

try:
    # Prueba de conexión
    connection = get_connection()
    cursor = connection.cursor()

    print("Conexión exitosa a la base de datos")

    # Comprobar la versión de PostgreSQL
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"Versión de PostgreSQL: {db_version}")

    # Crear las tablas
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );
    """
    create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER REFERENCES users(id)
    );
    """
    cursor.execute(create_users_table)
    cursor.execute(create_tasks_table)

    connection.commit()
    print("Tablas creadas exitosamente")

except Exception as e:
    print(f"Error al crear las tablas: {e}")

finally:
    # Cerrar la conexión inicial
    if connection:
        cursor.close()
        connection.close()
        print("Conexión cerrada")
