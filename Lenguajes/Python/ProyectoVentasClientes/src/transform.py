import pandas as pd
import os

RAW_PROCESSED_PATH = "./data/processed/fact_sales.csv"
TRANSFORMED_PATH = "./data/processed/transformed_sales.csv"

def clean_column_names(cols):
    cleaned = (
        cols
        .str.strip()
        .str.lower()
        .str.replace(r"[()/%]", "", regex=True)
        .str.replace(" ", "_")
    )
    print("Original columns:")
    print(list(cols))
    print("\nCleaned columns:")
    print(list(cleaned))
    return cleaned

def transform_data(df):
    # Normalizar nombres de columnas
    df.columns = clean_column_names(df.columns)

    print("\nColumnas finales en DataFrame:")
    print(df.columns.tolist())

    # Fecha
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['dayofweek'] = df['date'].dt.day_name()

    # Ajuste nombres de columnas según extract.py
    quantity_col = 'quantity_sold_kg' if 'quantity_sold_kg' in df.columns else 'quantity_sold_kilo'
    price_col = 'unit_selling_price' if 'unit_selling_price' in df.columns else 'unit_selling_price_rmbkg'

    # Cálculo de ventas
    if quantity_col in df.columns and price_col in df.columns:
        df['total_sale'] = df[quantity_col] * df[price_col]

        # Filtros SOLO si existen columnas
        df = df[df[quantity_col] > 0]
        df = df[df[price_col] >= 0]
    else:
        raise Exception("❌ Columnas clave no encontradas para cálculo de ventas")

    # Eliminar duplicados
    df = df.drop_duplicates()

    return df

if __name__ == "__main__":
    df = pd.read_csv(RAW_PROCESSED_PATH, low_memory=False)
    df_transformed = transform_data(df)

    os.makedirs(os.path.dirname(TRANSFORMED_PATH), exist_ok=True)
    df_transformed.to_csv(TRANSFORMED_PATH, index=False)

    print(f"\n✅ Datos transformados guardados en {TRANSFORMED_PATH}")
