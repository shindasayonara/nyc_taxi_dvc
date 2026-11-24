import argparse
from collections import Counter
from pathlib import Path

import pandas as pd

from src.data_quality import validate_dataframe


def validate_csv(input_path: str, chunksize: int = 100_000) -> bool:
    """
    Проверяет CSV-файл частями, не загружая весь датасет
    в оперативную память.

    Возвращает True, если все проверки пройдены.
    """

    file_path = Path(input_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    if chunksize <= 0:
        raise ValueError("Размер порции должен быть больше нуля.")

    print("=" * 65)
    print("ПРОВЕРКА КАЧЕСТВА ДАННЫХ")
    print("=" * 65)

    print(f"\nФайл: {file_path}")
    print(f"Размер порции: {chunksize:,} строк".replace(",", " "))

    # ---------------------------------------------------------
    # 1. Проверка структуры CSV
    # ---------------------------------------------------------

    print("\n1. Проверка структуры датасета...")

    header = pd.read_csv(file_path, nrows=0)

    schema_errors = validate_dataframe(pd.DataFrame(columns=header.columns))

    if schema_errors:
        print("Обнаружены нарушения структуры:")
        for error in schema_errors:
            print(f"  - {error}")
    else:
        print("Структура датасета соответствует требованиям.")

    # ---------------------------------------------------------
    # 2. Проверка данных частями
    # ---------------------------------------------------------

    print("\n2. Проверка содержимого CSV...")

    total_rows = 0
    total_chunks = 0

    # Здесь будут накапливаться счётчики нарушений.
    violations = Counter()

    for chunk in pd.read_csv(file_path, chunksize=chunksize):
        total_chunks += 1
        total_rows += len(chunk)

        errors = validate_dataframe(chunk)

        for error in errors:
            # Структура уже проверена по заголовку CSV.
            if (
                "Отсутствуют обязательные столбцы" in error
                or "Обнаружены лишние столбцы" in error
            ):
                continue

            # Подсчёт пропущенных значений.
            if "пропущенных значений:" in error:
                message, count = error.rsplit(": ", 1)
                violations[message] += int(count)

            # Подсчёт нарушений числовых ограничений.
            elif "; нарушений:" in error:
                message, count = error.rsplit("; нарушений: ", 1)
                violations[message] += int(count)

    # ---------------------------------------------------------
    # 3. Вывод результатов
    # ---------------------------------------------------------

    print("\n" + "=" * 65)
    print("РЕЗУЛЬТАТЫ ПРОВЕРКИ")
    print("=" * 65)

    print(f"\nОбработано строк: {total_rows:,}".replace(",", " "))
    print(f"Обработано порций: {total_chunks}")

    if violations:
        print("\nОбнаруженные нарушения:")

        for message, count in sorted(violations.items()):
            print(f"  - {message}: {count:,}".replace(",", " "))
    else:
        print("\nНарушений качества данных не обнаружено.")

    has_errors = bool(schema_errors or violations)

    print("\n" + "-" * 65)

    if has_errors:
        print("ИТОГ: ПРОВЕРКА НЕ ПРОЙДЕНА")
    else:
        print("ИТОГ: ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ")

    print("=" * 65)

    return not has_errors


def main():
    parser = argparse.ArgumentParser(
        description="Проверка качества обработанного NYC Taxi Dataset"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Путь к проверяемому CSV-файлу",
    )

    parser.add_argument(
        "--chunksize",
        type=int,
        default=100_000,
        help="Количество строк в одной порции (по умолчанию 100000)",
    )

    args = parser.parse_args()

    is_valid = validate_csv(
        input_path=args.input,
        chunksize=args.chunksize,
    )

    return 0 if is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
