# Day 17 Exercises — Exception Handling

Estimated time: 45–60 minutes

---

## Exercise 1 — Validate Model Configuration

Write a function `validate_config(config: dict)` that raises specific exceptions:

1. `KeyError` (or custom `MissingFieldError`) if required keys are absent  
   Required: `"model_name"`, `"learning_rate"`, `"batch_size"`, `"max_epochs"`
2. `TypeError` if any value is the wrong type  
   - `model_name` → str; `learning_rate` → float; `batch_size` → int; `max_epochs` → int
3. `ValueError` for out-of-range values  
   - `learning_rate`: 1e-6 to 0.1  
   - `batch_size`: 1 to 2048  
   - `max_epochs`: 1 to 1000

Validate these configs and print clear error messages:
```python
configs = [
    {"model_name": "bert", "learning_rate": 3e-5, "batch_size": 32, "max_epochs": 10},
    {"model_name": "bert", "learning_rate": 5.0, "batch_size": 32, "max_epochs": 10},  # bad lr
    {"model_name": 123, "learning_rate": 3e-5, "batch_size": 32, "max_epochs": 10},    # bad type
    {"learning_rate": 3e-5},   # missing keys
]
```

---

## Exercise 2 — Safe JSON Loader

Write `safe_load_json(path: str, default=None)` that:
1. Returns `default` if file doesn't exist (don't crash)
2. Returns `default` if JSON is malformed (log a warning)
3. Returns `default` if file is empty
4. Returns the parsed dict on success

Test it with 3 cases: valid path, nonexistent path, and a path to a text file with invalid JSON.

---

## Exercise 3 — Custom Exception Hierarchy

Create this hierarchy for a data pipeline:

```
PipelineError (base)
├── StageError(stage_name: str)
│   ├── InputValidationError(field: str, reason: str)
│   └── TransformError(transform_name: str, detail: str)
└── OutputError(output_path: str)
```

Each exception should:
- Store relevant attributes
- Have a clear `__str__` message

Write a `run_pipeline(data)` function that raises different exceptions based on `data` content, and demonstrate catching them at different levels.

---

## Exercise 4 — Retry Decorator

Write a `retry(max_attempts=3, delay=0.1)` function (not yet a decorator, just a wrapper) that:

1. Tries calling a function up to `max_attempts` times
2. Waits `delay` seconds between attempts (use `time.sleep`)
3. On final failure, re-raises the last exception
4. Logs each attempt: `"Attempt 1/3 failed: <error>"`

Test it with a function that randomly fails 70% of the time using `random.random()`.

---

## Exercise 5 — Safe Batch Labeler

Build a robust batch processor:

```python
def batch_label(records: list, labeler_fn) -> dict:
    """
    Returns:
    {
        "success": [processed records],
        "failed": [{"index": i, "record": ..., "error": "..."}],
        "success_rate": float
    }
    """
```

Test with a labeler that:
- Raises `ValueError` for records where `text` is under 3 chars
- Raises `KeyError` for records missing the `"text"` key
- Otherwise returns `{"text": ..., "label": "ok"}`

---

## Stretch Challenge — Context-Aware Error Logger

Build an `ErrorLogger` class that:
1. Accepts a `log_file` path in `__init__`
2. Has a method `log(error: Exception, context: dict)` that writes to the file: timestamp, error type, message, and context as JSON
3. Has a `get_summary()` method that reads the log and returns `{error_type: count}` dict
4. Handles file-write failures gracefully (falls back to printing)

Simulate 20 random errors from a list of error types and show the summary.
