import mysql.connector
from mysql.connector import pooling

# Configura la connexió a MariaDB
db_config = {
    'host': 'mariadb',
    'user': 'popview',
    'password': 'pirineus',
    'database': 'pop_view',
    'collation': 'utf8mb4_general_ci'
}

# Pool de connexions
db_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)

def get_db_connection():
    return db_pool.get_connection()

# Estructura SQL de la base de dades
CREATE_TABLES = {
    "usuari": """
        CREATE TABLE IF NOT EXISTS usuari (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(255) NOT NULL,
            imatge TEXT,
            edat INT NOT NULL,
            correu VARCHAR(255) UNIQUE NOT NULL,
            contrasenya VARCHAR(255) NOT NULL
        )
    """,
    "llista": """
        CREATE TABLE IF NOT EXISTS llista (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titol VARCHAR(255) NOT NULL,
            descripcio TEXT,
            privada BOOLEAN NOT NULL
        )
    """,
    "titol": """
        CREATE TABLE IF NOT EXISTS titol (
            id INT AUTO_INCREMENT PRIMARY KEY,
            imatge TEXT,
            nom VARCHAR(255) NOT NULL,
            descripcio TEXT,
            plataformes VARCHAR(255) NOT NULL,
            es_peli BOOLEAN NOT NULL,
            rating FLOAT NOT NULL,
            comentaris TEXT
        )
    """,
    "usuari_llista": """
        CREATE TABLE IF NOT EXISTS usuari_llista (
            usuari_id INT,
            llista_id INT,
            PRIMARY KEY (usuari_id, llista_id),
            FOREIGN KEY (usuari_id) REFERENCES usuari(id) ON DELETE CASCADE,
            FOREIGN KEY (llista_id) REFERENCES llista(id) ON DELETE CASCADE
        )
    """,
    "llista_titol": """
        CREATE TABLE IF NOT EXISTS llista_titol (
            llista_id INT,
            titol_id INT,
            PRIMARY KEY (llista_id, titol_id),
            FOREIGN KEY (llista_id) REFERENCES llista(id) ON DELETE CASCADE,
            FOREIGN KEY (titol_id) REFERENCES titol(id) ON DELETE CASCADE
        )
    """,
    "usuari_titol": """
        CREATE TABLE IF NOT EXISTS usuari_titol (
            usuari_id INT,
            titol_id INT,
            PRIMARY KEY (usuari_id, titol_id),
            FOREIGN KEY (usuari_id) REFERENCES usuari(id) ON DELETE CASCADE,
            FOREIGN KEY (titol_id) REFERENCES titol(id) ON DELETE CASCADE
        )
    """
}

def create_tables():
    db = get_db_connection()
    cursor = db.cursor()
    for table_name, create_stmt in CREATE_TABLES.items():
        cursor.execute(create_stmt)
    db.commit()
    cursor.close()
    db.close()

if __name__ == "__main__":
    create_tables()
