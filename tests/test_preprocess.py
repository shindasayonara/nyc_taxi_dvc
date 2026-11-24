import pandas as pd

from src.preprocess import preprocess_data


def test_preprocess_removes_invalid_rows(tmp_path):
    """
    Проверяет, что предобработка удаляет некорректные поездки
    и сохраняет только корректные записи.
    """

    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "tpep_pickup_datetime": [
            "2016-03-01 10:00:00",
            "2016-03-01 11:00:00",
            "2016-03-01 12:00:00",
            "2016-03-01 13:00:00",
            "2016-03-01 14:00:00",
            "2016-03-01 15:00:00",
        ],
        "tpep_dropoff_datetime": [
            "2016-03-01 10:30:00",  # Корректная поездка
            "2016-03-01 11:30:00",  # Некорректный пассажир
            "2016-03-01 12:30:00",  # Нулевая дистанция
            "2016-03-01 12:00:00",  # Нулевая длительность
            "2016-03-02 15:00:00",  # Длительность больше 24 часов
            "2016-03-01 15:30:00",  # Отрицательная стоимость
        ],
        "passenger_count": [1, 0, 1, 1, 1, 1],
        "trip_distance": [2.5, 2.0, 0.0, 1.5, 5.0, 3.0],
        "fare_amount": [10.0, 8.0, 7.0, 6.0, 20.0, -5.0],
        "total_amount": [12.0, 10.0, 9.0, 8.0, 25.0, 0.0],
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    preprocess_data(
        input_path=str(input_file),
        output_path=str(output_file),
    )

    assert output_file.exists()

    result = pd.read_csv(output_file)

    assert len(result) == 1
    assert result.iloc[0]["passenger_count"] == 1
    assert result.iloc[0]["trip_distance"] == 2.5
    assert result.iloc[0]["trip_duration_minutes"] == 30.0
