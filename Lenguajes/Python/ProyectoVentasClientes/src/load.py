import pandas as pd
import sqlite3
import os

TRANSFORMED_PATH = "./data/processed/transformed_sales.csv"
DB_PATH = "./db/sales.db"
TABLE_NAME = "sales"

def load_to_sqlite(csv_path, db_path, table_name):
    # Crear carpeta db si no existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Leer datos transformados
    df = pd.read_csv(csv_path)

    # Conectar a SQLite
    conn = sqlite3.connect(db_path)

    # Cargar datos a la tabla
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    # Validación: contar filas
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]

    conn.close()

    print(f"✅ Datos cargados correctamente en '{table_name}'")
    print(f"📊 Filas insertadas: {row_count}")
    print(f"🗄 Base de datos: {db_path}")

if __name__ == "__main__":
    load_to_sqlite(
        TRANSFORMED_PATH,
        DB_PATH,
        TABLE_NAME
    )
