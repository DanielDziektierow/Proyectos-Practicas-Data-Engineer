import sqlite3
import pandas as pd
import os

DB_PATH = "./db/sales.db"
OUTPUT_PATH = "./data/processed/sql_outputs"

QUERIES = {
    "total_sales": """
        SELECT 
            ROUND(SUM(total_sale), 2) AS total_sales_rmb
        FROM sales;
    """,

    "sales_by_category": """
        SELECT 
            category_name,
            ROUND(SUM(total_sale), 2) AS total_sales
        FROM sales
        GROUP BY category_name
        ORDER BY total_sales DESC;
    """,

    "top_products": """
        SELECT 
            item_name,
            ROUND(SUM(total_sale), 2) AS revenue
        FROM sales
        GROUP BY item_name
        ORDER BY revenue DESC
        LIMIT 10;
    """,

    "monthly_sales": """
        SELECT
            year,
            month,
            ROUND(SUM(total_sale), 2) AS total_sales
        FROM sales
        GROUP BY year, month
        ORDER BY year, month;
    """,

    "discount_impact": """
        SELECT
            discount_yesno,
            COUNT(*) AS transactions,
            ROUND(SUM(total_sale), 2) AS total_sales
        FROM sales
        GROUP BY discount_yesno;
    """
}

def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    for name, query in QUERIES.items():
        print(f"\n▶ Ejecutando query: {name}")
        df = run_query(query)

        print(df)

        output_file = os.path.join(OUTPUT_PATH, f"{name}.csv")
        df.to_csv(output_file, index=False)

        print(f"💾 Resultado guardado en {output_file}")

if __name__ == "__main__":
    main()
