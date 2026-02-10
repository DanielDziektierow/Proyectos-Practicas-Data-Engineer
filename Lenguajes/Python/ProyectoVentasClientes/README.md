# Ejecutar desde la raíz del proyecto:
# C:/Python311/python.exe src/extract.py

import os
import pandas as pd

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed")

# =========================
# LOADERS
# =========================
def load_csv(filename, encoding="utf-8"):
    filepath = os.path.join(RAW_DATA_PATH, filename)
    return pd.read_csv(
        filepath,
        dtype={"Item Code": str},
        encoding=encoding
    )

# =========================
# CLEANERS
# =========================
def clean_products(df):
    df = df.drop_duplicates()
    df["Category Name"] = df["Category Name"].str.replace("Â", "", regex=False)
    return df

def clean_sales(df):
    df = df.drop_duplicates()

    df.columns = [
        "date",
        "time",
        "item_code",
        "quantity_sold_kg",
        "unit_selling_price",
        "sale_or_return",
        "discount"
    ]

    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df["quantity_sold_kg"] = pd.to_numeric(df["quantity_sold_kg"], errors="coerce")
    df["unit_selling_price"] = pd.to_numeric(df["unit_selling_price"], errors="coerce")

    return df

def clean_wholesale(df):
    df = df.drop_duplicates()
    df.columns = ["date", "item_code", "wholesale_price"]
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df["wholesale_price"] = pd.to_numeric(df["wholesale_price"], errors="coerce")
    return df

def clean_loss(df):
    df = df.drop_duplicates()
    df.columns = ["item_code", "item_name", "loss_rate"]
    df["loss_rate"] = pd.to_numeric(df["loss_rate"], errors="coerce")
    return df

# =========================
# BUILD FACT TABLE
# =========================
def build_fact_table(products, sales, wholesale, loss):
    df = sales.merge(
        products,
        left_on="item_code",
        right_on="Item Code",
        how="left"
    )

    df = df.merge(
        loss,
        left_on=["item_code", "Item Name"],
        right_on=["item_code", "item_name"],
        how="left"
    )

    df = df.merge(
        wholesale,
        on=["item_code", "date"],
        how="left"
    )

    # Manejo controlado de nulos
    df["loss_rate"] = df["loss_rate"].fillna(0)

    return df

# =========================
# MAIN
# =========================
def main():
    print("📂 Archivos en data/raw:")
    print(os.listdir(RAW_DATA_PATH))

    products = clean_products(load_csv("annex1.csv", encoding="latin1"))
    sales = clean_sales(load_csv("annex2.csv"))
    wholesale = clean_wholesale(load_csv("annex3.csv"))
    loss = clean_loss(load_csv("annex4.csv"))

    fact_sales = build_fact_table(products, sales, wholesale, loss)

    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    output_path = os.path.join(PROCESSED_DATA_PATH, "fact_sales.csv")
    fact_sales.to_csv(output_path, index=False)

    print("✅ ETL finalizado correctamente")
    print(f"📄 Archivo generado: {output_path}")
    print(f"📊 Filas totales: {len(fact_sales)}")

if __name__ == "__main__":
    main()
