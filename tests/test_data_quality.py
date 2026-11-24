import pandas as pd
import pytest

from src.data_quality import EXPECTED_COLUMNS, validate_dataframe


@pytest.fixture
def valid_dataframe():
    """
    Создаёт корректный DataFrame со всеми 20 ожидаемыми столбцами.
    """

    data = {
        "VendorID": [1, 2, 1],
        "tpep_pickup_datetime": [
            "2016-03-01 10:00:00",
            "2016-03-01 11:00:00",
            "2016-03-01 12:00:00",
        ],
        "tpep_dropoff_datetime": [
            "2016-03-01 10:30:00",
            "2016-03-01 11:25:00",
            "2016-03-01 12:15:00",
        ],
        "passenger_count": [1, 2, 1],
        "trip_distance": [2.5, 3.0, 1.5],
        "pickup_longitude": [-73.98, -73.99, -73.97],
        "pickup_latitude": [40.75, 40.76, 40.74],
        "RatecodeID": [1, 1, 1],
        "store_and_fwd_flag": ["N", "N", "N"],
        "dropoff_longitude": [-73.95, -73.96, -73.94],
        "dropoff_latitude": [40.78, 40.77, 40.76],
        "payment_type": [1, 2, 1],
        "fare_amount": [10.0, 12.0, 7.0],
        "extra": [0.5, 0.5, 0.0],
        "mta_tax": [0.5, 0.5, 0.5],
        "tip_amount": [2.0, 1.0, 1.5],
        "tolls_amount": [0.0, 0.0, 0.0],
        "improvement_surcharge": [0.3, 0.3, 0.3],
        "total_amount": [13.3, 14.3, 9.3],
        "trip_duration_minutes": [30.0, 25.0, 15.0],
    }

    return pd.DataFrame(data, columns=EXPECTED_COLUMNS)


def test_valid_dataframe_passes_all_checks(valid_dataframe):
    """Корректный DataFrame должен пройти все проверки."""

    errors = validate_dataframe(valid_dataframe)

    assert errors == []


def test_missing_column_is_detected(valid_dataframe):
    """Проверяет обнаружение отсутствующего столбца."""

    df = valid_dataframe.drop(columns=["VendorID"])

    errors = validate_dataframe(df)

    assert any("Отсутствуют обязательные столбцы" in error for error in errors)


def test_extra_column_is_detected(valid_dataframe):
    """Проверяет обнаружение лишнего столбца."""

    df = valid_dataframe.copy()
    df["unexpected_column"] = [1, 2, 3]

    errors = validate_dataframe(df)

    assert any("Обнаружены лишние столбцы" in error for error in errors)


def test_missing_values_are_detected(valid_dataframe):
    """Проверяет обнаружение пропущенных значений."""

    df = valid_dataframe.copy()
    df.loc[0, "passenger_count"] = None

    errors = validate_dataframe(df)

    assert any(
        "passenger_count" in error and "пропущенных значений" in error
        for error in errors
    )


@pytest.mark.parametrize(
    "column, invalid_value, expected_message",
    [
        ("passenger_count", 0, "значения должны быть >= 1"),
        ("trip_distance", 0, "значения должны быть > 0"),
        ("trip_duration_minutes", 0, "значения должны быть > 0"),
        ("trip_duration_minutes", 1441, "значения должны быть <= 1440"),
        ("fare_amount", -1, "значения должны быть >= 0"),
        ("total_amount", -1, "значения должны быть >= 0"),
    ],
)
def test_numeric_rules_are_enforced(
    valid_dataframe,
    column,
    invalid_value,
    expected_message,
):
    """Проверяет соблюдение каждого числового ограничения."""

    df = valid_dataframe.copy()
    df.loc[0, column] = invalid_value

    errors = validate_dataframe(df)

    assert any(column in error and expected_message in error for error in errors)
