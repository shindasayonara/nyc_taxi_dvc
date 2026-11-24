import pandas as pd

# =============================================================
# Структура обработанного датасета
# =============================================================

EXPECTED_COLUMNS = [
    "VendorID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "pickup_longitude",
    "pickup_latitude",
    "RatecodeID",
    "store_and_fwd_flag",
    "dropoff_longitude",
    "dropoff_latitude",
    "payment_type",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
    "trip_duration_minutes",
]


# =============================================================
# Столбцы для проверки пропущенных значений
# =============================================================

REQUIRED_NON_NULL_COLUMNS = [
    "passenger_count",
    "trip_distance",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "trip_duration_minutes",
    "fare_amount",
    "total_amount",
]


# =============================================================
# Проверка качества данных
# =============================================================


def validate_dataframe(df: pd.DataFrame) -> list[str]:
    """
    Проверяет DataFrame на соответствие правилам качества
    данных из лабораторной работы №2.

    Проверяются:
    1. Структура датасета.
    2. Отсутствие пропущенных значений.
    3. Шесть числовых ограничений.

    Возвращает список обнаруженных нарушений.
    Если список пустой, все проверки пройдены.
    """

    errors = []

    # ---------------------------------------------------------
    # 1. Проверка структуры датасета
    # ---------------------------------------------------------

    actual_columns = set(df.columns)
    expected_columns = set(EXPECTED_COLUMNS)

    missing_columns = expected_columns - actual_columns
    extra_columns = actual_columns - expected_columns

    if missing_columns:
        errors.append(f"Отсутствуют обязательные столбцы: {sorted(missing_columns)}")

    if extra_columns:
        errors.append(f"Обнаружены лишние столбцы: {sorted(extra_columns)}")

    # ---------------------------------------------------------
    # 2. Проверка пропущенных значений
    # ---------------------------------------------------------

    for column in REQUIRED_NON_NULL_COLUMNS:
        if column not in df.columns:
            continue

        missing_count = int(df[column].isna().sum())

        if missing_count > 0:
            errors.append(
                f"Столбец '{column}': обнаружено пропущенных значений: {missing_count}"
            )

    # ---------------------------------------------------------
    # 3. Проверка числовых ограничений
    # ---------------------------------------------------------

    rules = [
        (
            "passenger_count",
            "значения должны быть >= 1",
            lambda values: values >= 1,
        ),
        (
            "trip_distance",
            "значения должны быть > 0",
            lambda values: values > 0,
        ),
        (
            "trip_duration_minutes",
            "значения должны быть > 0",
            lambda values: values > 0,
        ),
        (
            "trip_duration_minutes",
            "значения должны быть <= 1440",
            lambda values: values <= 1440,
        ),
        (
            "fare_amount",
            "значения должны быть >= 0",
            lambda values: values >= 0,
        ),
        (
            "total_amount",
            "значения должны быть >= 0",
            lambda values: values >= 0,
        ),
    ]

    for column, description, condition in rules:
        if column not in df.columns:
            continue

        values = pd.to_numeric(df[column], errors="coerce")
        valid_mask = condition(values)

        invalid_count = int((~valid_mask).sum())

        if invalid_count > 0:
            errors.append(
                f"Столбец '{column}': {description}; нарушений: {invalid_count}"
            )

    return errors
