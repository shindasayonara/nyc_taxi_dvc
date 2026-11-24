import argparse

from preprocess import preprocess_data


def run_pipeline(input_path: str, output_path: str) -> None:
    """
    Запускает полный конвейер предобработки данных.
    """

    print("=" * 60)
    print("КОНВЕЙЕР ОБРАБОТКИ NYC YELLOW TAXI")
    print("=" * 60)

    preprocess_data(
        input_path=input_path,
        output_path=output_path,
    )

    print("\nКонвейер обработки завершён успешно.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Конвейер обработки NYC Yellow Taxi Dataset"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Путь к исходному CSV-файлу",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Путь для сохранения обработанного CSV-файла",
    )

    args = parser.parse_args()

    run_pipeline(
        input_path=args.input,
        output_path=args.output,
    )
