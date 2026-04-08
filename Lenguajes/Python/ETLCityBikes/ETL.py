import requests
import pandas as pd
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

URL = os.getenv("API_URL")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "output/data.csv")

def get_data(url):
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.json()


def transform_data(data):
    stations = data.get("network", {}).get("stations", [])
    
    rows = []
    for s in stations:
        rows.append({
            "name": s["name"],
            "free_bikes": s["free_bikes"],
            "empty_slots": s["empty_slots"],
            "lat": s["latitude"],
            "lon": s["longitude"]
        })

    df = pd.DataFrame(rows)

    df["total_slots"] = df["free_bikes"] + df["empty_slots"]
    df["occupancy"] = df["free_bikes"] / df["total_slots"]
    df["occupancy"] = df["occupancy"].fillna(0)

    return df


def load_data(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


def main():
    try:
        logging.info("Inicio del proceso ETL")

        data = get_data(URL)
        df = transform_data(data)

        logging.info(f"Estaciones procesadas: {len(df)}")

        load_data(df, OUTPUT_PATH)

        logging.info("Archivo generado correctamente")

    except requests.exceptions.Timeout:
        logging.error("La API tardó demasiado")
    except requests.exceptions.HTTPError:
        logging.exception("Error HTTP")
    except Exception:
        logging.exception("Error general")


if __name__ == "__main__":
    main()