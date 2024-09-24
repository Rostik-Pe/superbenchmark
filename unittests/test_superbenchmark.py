import json
from datetime import datetime
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from superbenchmark_app import app, BenchmarkResult, HTTPException

client = TestClient(app)


def test_get_average_results_success():
    test_data = _load_test_data()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "average_token_count": 15.0,
        "average_time_to_first_token": 61.67,
        "average_time_per_output_token": 25.0,
        "average_total_generation_time": 441.67
    }

    with patch("superbenchmark_app._get_benchmark_results", return_value=test_data), \
            patch("fastapi.testclient.TestClient.get", return_value=mock_response):
        response = client.get("/results/average")
        assert response.status_code == 200
        assert response.json() == {
            "average_token_count": 15.0,
            "average_time_to_first_token": 61.67,
            "average_time_per_output_token": 25.0,
            "average_total_generation_time": 441.67
        }


def test_get_average_results_in_time_window_success():
    test_data = _load_test_data()
    relevant_data = [r for r in test_data if datetime(2023, 9, 1) <= r.timestamp <= datetime(2023, 9, 2)]
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "average_token_count": 15.0,
        "average_time_to_first_token": 62.5,
        "average_time_per_output_token": 25.0,
        "average_total_generation_time": 437.5
    }

    with patch("superbenchmark_app._get_benchmark_results", return_value=relevant_data), \
            patch("fastapi.testclient.TestClient.get", return_value=mock_response):
        start_time = datetime(2023, 9, 1)
        end_time = datetime(2023, 9, 2)
        response = client.get(f"/results/average/{start_time.isoformat()}/{end_time.isoformat()}")
        assert response.status_code == 200
        assert response.json() == {
            "average_token_count": 15.0,
            "average_time_to_first_token": 62.5,
            "average_time_per_output_token": 25.0,
            "average_total_generation_time": 437.5
        }


def test_get_average_results_no_data():
    with patch("superbenchmark_app._get_benchmark_results",
               side_effect=HTTPException(status_code=404, detail="No benchmark results found.")):
        response = client.get("/results/average")
        assert response.status_code == 404
        assert response.json() == {"detail": "No benchmark results found."}


def test_get_average_results_in_time_window_no_data():
    with patch("superbenchmark_app._get_benchmark_results", return_value=[]):
        start_time = datetime(2023, 9, 3)
        end_time = datetime(2023, 9, 4)
        response = client.get(f"/results/average/{start_time.isoformat()}/{end_time.isoformat()}")
        assert response.status_code == 404
        assert response.json() == {"detail": "No benchmark results found within the specified time window."}


def _load_test_data() -> list[BenchmarkResult]:
    with open("test_db.json") as f:
        data = json.load(f)
        return [BenchmarkResult(**result) for result in data["benchmarking_results"]]
