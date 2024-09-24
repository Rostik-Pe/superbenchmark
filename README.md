# SuperBenchmark

SuperBenchmark is a FastAPI application designed to manage and query benchmarking results for a Large Language Model (
LLM).

## Features

- **GET /results/average**: Returns the average performance statistics across all benchmarking results.
- **GET /results/average/{start_time}/{end_time}**: Returns the average performance statistics for benchmarking results
  within a specified time window.

## Data Model

The `BenchmarkResult` data model represents a single benchmarking result:

```python
class BenchmarkResult(BaseModel):
    request_id: str
    prompt_text: str
    generated_text: str
    token_count: int
    time_to_first_token: int
    time_per_output_token: int
    total_generation_time: int
    timestamp: datetime
```

## Installation

1. Clone the repository:

```
git clone https://github.com/
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Set the `SUPERBENCHMARK_DEBUG` environment variable to `"True"` to run the application in debug mode, which allows
   access to the `test_database.json` file.
2. Run the FastAPI application:

```
python superbenchmark_app.py
```

3. The application will be available at `http://localhost:8000`.

## Contributing

If you have any suggestions or find any issues, feel free to create a new issue or submit a pull request.

## License

This project is licensed under my LICENSE.