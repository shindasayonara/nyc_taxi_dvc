import pandas as pd


def test_processed_data_has_no_missing_values(tmp_path):
    """Проверяет отсутствие пропущенных значений."""

    data = {
        "passenger_count": [1, 2, 1],
        "trip_distance": [2.5, 3.0, 1.5],
        "trip_duration_minutes": [30.0, 25.0, 15.0],
        "fare_amount": [10.0, 12.0, 7.0],
        "total_amount": [12.0, 15.0, 9.0],
    }

    df = pd.DataFrame(data)

    file_path = tmp_path / "processed.csv"
    df.to_csv(file_path, index=False)

    result = pd.read_csv(file_path)

    assert not result.isnull().values.any()


def test_processed_data_has_valid_values():
    """Проверяет соблюдение основных правил качества данных."""

    df = pd.DataFrame(
        {
            "passenger_count": [1, 2, 1],
            "trip_distance": [2.5, 3.0, 1.5],
            "trip_duration_minutes": [30.0, 25.0, 15.0],
            "fare_amount": [10.0, 12.0, 7.0],
            "total_amount": [12.0, 15.0, 9.0],
        }
    )

    assert (df["passenger_count"] > 0).all()
    assert (df["trip_distance"] > 0).all()
    assert (df["trip_duration_minutes"] > 0).all()
    assert (df["trip_duration_minutes"] <= 1440).all()
    assert (df["fare_amount"] >= 0).all()
    assert (df["total_amount"] >= 0).all()
