import argparse
import os

import pandas as pd


def preprocess_data(input_path: str, output_path: str) -> None:
    """
    Загружает исходный датасет NYC Yellow Taxi,
    выполняет предобработку и сохраняет очищенный набор данных.
    """

    print("=" * 60)
    print("ЗАПУСК ПРЕДОБРАБОТКИ ДАННЫХ")
    print("=" * 60)

    print(f"\nИсходный файл: {input_path}")

    df = pd.read_csv(input_path)
    rows_before = len(df)

    print(f"Количество строк до обработки: {rows_before:,}".replace(",", " "))

    df["tpep_pickup_datetime"] = pd.to_datetime(
        df["tpep_pickup_datetime"], errors="coerce"
    )
    df["tpep_dropoff_datetime"] = pd.to_datetime(
        df["tpep_dropoff_datetime"], errors="coerce"
    )

    df["trip_duration_minutes"] = (
        df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60

    mask_passenger = df["passenger_count"] > 0
    mask_distance = df["trip_distance"] > 0
    mask_duration_positive = df["trip_duration_minutes"] > 0
    mask_duration_max = df["trip_duration_minutes"] <= 1440
    mask_fare = df["fare_amount"] >= 0
    mask_total = df["total_amount"] >= 0

    clean_mask = (
        mask_passenger
        & mask_distance
        & mask_duration_positive
        & mask_duration_max
        & mask_fare
        & mask_total
    )

    df_clean = df.loc[clean_mask].copy()

    rows_after = len(df_clean)
    rows_removed = rows_before - rows_after
    removed_percent = rows_removed / rows_before * 100 if rows_before else 0

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    df_clean.to_csv(output_path, index=False)

    print("\nРЕЗУЛЬТАТ ОБРАБОТКИ")
    print("-" * 60)
    print(f"Строк до обработки:    {rows_before:,}".replace(",", " "))
    print(f"Строк после обработки: {rows_after:,}".replace(",", " "))
    print(f"Удалено строк:         {rows_removed:,}".replace(",", " "))
    print(f"Удалено:               {removed_percent:.4f}%")
    print(f"\nРезультат сохранён: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Предобработка NYC Yellow Taxi Dataset"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Путь к исходному CSV-файлу",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Путь для сохранения очищенного CSV-файла",
    )

    args = parser.parse_args()

    preprocess_data(
        input_path=args.input,
        output_path=args.output,
    )
