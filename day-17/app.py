# Day 17: Exception Handling
# Focus: Building robust Python that doesn't crash in production

# ============================================================
# WHAT: Exceptions are errors that occur at runtime. Python
#       lets you *catch* them with try/except blocks so your
#       program can recover gracefully.
# WHY:  AI pipelines deal with dirty data, missing files,
#       network failures, and bad user input. Robust error
#       handling is what separates production code from scripts.
# ============================================================

# ============================================================
# 1. Basic try / except
# ============================================================
print("=== 1. Basic try/except ===")

# Without handling — crashes the program:
# result = 1 / 0   # ZeroDivisionError

# With handling:
try:
    result = 1 / 0
except ZeroDivisionError:
    print("Division by zero caught!")
    result = 0

print(f"Result: {result}")

# Bad string → int conversion
user_input = "abc"
try:
    value = int(user_input)
except ValueError as e:
    print(f"ValueError: {e}")
    value = 0
print(f"Parsed value: {value}")

# ============================================================
# 2. Catching Multiple Exception Types
# ============================================================
print("\n=== 2. Multiple Exceptions ===")

def safe_divide(a, b):
    """Divides two numbers with comprehensive error handling."""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print(f"  Error: Cannot divide {a} by zero")
        return None
    except TypeError as e:
        print(f"  Error: Invalid types — {e}")
        return None

print(safe_divide(10, 2))     # 5.0
print(safe_divide(10, 0))     # None
print(safe_divide("10", 2))   # None

# Catch multiple exceptions in one line
def parse_config_value(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

print(parse_config_value("42"))    # 42
print(parse_config_value("bad"))   # None
print(parse_config_value(None))    # None

# ============================================================
# 3. else and finally
# ============================================================
print("\n=== 3. else + finally ===")

def load_config(filename: str) -> dict:
    """
    try   → attempt the operation
    except → handle known error cases
    else  → runs ONLY if no exception occurred
    finally → ALWAYS runs (cleanup code goes here)
    """
    import json
    from pathlib import Path

    file_path = Path(filename)
    result = {}

    try:
        with open(file_path, "r") as f:
            result = json.load(f)
    except FileNotFoundError:
        print(f"  Config file not found: {filename}")
    except json.JSONDecodeError as e:
        print(f"  Invalid JSON in {filename}: {e}")
    else:
        print(f"  Config loaded successfully: {len(result)} keys")
    finally:
        print(f"  [load_config finished for: {filename}]")

    return result

# Test with non-existent file
config1 = load_config("nonexistent.json")
print(f"  Result: {config1}")

# ============================================================
# 4. Raising Exceptions
# ============================================================
print("\n=== 4. Raising Exceptions ===")

def validate_batch_size(batch_size: int) -> int:
    """Validates batch size for a training run."""
    if not isinstance(batch_size, int):
        raise TypeError(f"batch_size must be int, got {type(batch_size).__name__}")
    if batch_size <= 0:
        raise ValueError(f"batch_size must be positive, got {batch_size}")
    if batch_size > 2048:
        raise ValueError(f"batch_size too large: {batch_size} (max: 2048)")
    return batch_size

for value in [32, -1, 0, "64", 4096]:
    try:
        result = validate_batch_size(value)
        print(f"  validate_batch_size({value!r}) = {result} ✓")
    except (TypeError, ValueError) as e:
        print(f"  validate_batch_size({value!r}) → {type(e).__name__}: {e}")

# ============================================================
# 5. Custom Exceptions
# ============================================================
print("\n=== 5. Custom Exceptions ===")

class ModelError(Exception):
    """Base class for model-related errors."""
    pass

class ModelNotFoundError(ModelError):
    """Raised when a model checkpoint doesn't exist."""
    def __init__(self, model_name: str, path: str):
        self.model_name = model_name
        self.path = path
        super().__init__(f"Model '{model_name}' not found at: {path}")

class InvalidInputError(ModelError):
    """Raised when input data fails validation."""
    def __init__(self, field: str, expected: str, got: str):
        self.field = field
        super().__init__(
            f"Invalid '{field}': expected {expected}, got {got}"
        )

# Using custom exceptions
def load_model(model_name: str, checkpoint_dir: str = "checkpoints"):
    from pathlib import Path
    path = Path(checkpoint_dir) / f"{model_name}.pt"
    if not path.exists():
        raise ModelNotFoundError(model_name, str(path))
    return f"<Model {model_name}>"

def process_input(data: dict):
    if not isinstance(data.get("text"), str):
        raise InvalidInputError("text", "str", type(data.get("text")).__name__)
    return data["text"].strip()

# Test custom exceptions
for test in ["bert", "gpt4"]:
    try:
        model = load_model(test)
        print(f"  Loaded: {model}")
    except ModelNotFoundError as e:
        print(f"  {type(e).__name__}: {e}")

for test_data in [{"text": "Hello!"}, {"text": 42}, {}]:
    try:
        result = process_input(test_data)
        print(f"  Processed: '{result}'")
    except InvalidInputError as e:
        print(f"  {type(e).__name__}: {e}")

# ============================================================
# 6. Exception Chaining — raise from
# ============================================================
print("\n=== 6. Exception Chaining ===")

def fetch_dataset(path: str) -> list:
    """Demonstrates exception chaining for better debugging."""
    from pathlib import Path
    try:
        import json
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError as original_error:
        raise RuntimeError(
            f"Dataset pipeline failed: could not open '{path}'"
        ) from original_error

try:
    data = fetch_dataset("missing_dataset.json")
except RuntimeError as e:
    print(f"  RuntimeError: {e}")
    if e.__cause__:
        print(f"  Caused by: {type(e.__cause__).__name__}: {e.__cause__}")

# ============================================================
# 7. Production Pattern — Defensive Data Loader
# ============================================================
print("\n=== 7. Production: Defensive Data Loader ===")

def safe_batch_process(records: list, processor_fn) -> tuple:
    """
    Processes records safely, collecting errors instead of crashing.
    Returns: (successful_results, error_log)
    """
    results = []
    errors = []

    for i, record in enumerate(records):
        try:
            result = processor_fn(record)
            results.append(result)
        except Exception as e:
            errors.append({
                "index": i,
                "record": record,
                "error_type": type(e).__name__,
                "error_msg": str(e),
            })

    return results, errors

# Simulate processor that sometimes fails
def extract_score(record: dict) -> float:
    score = record["score"]
    if not isinstance(score, (int, float)):
        raise TypeError(f"Score must be numeric, got {type(score).__name__}")
    return float(score)

sample_records = [
    {"id": 1, "score": 0.92},
    {"id": 2, "score": "high"},     # bad data
    {"id": 3, "score": 0.78},
    {"id": 4},                       # missing key
    {"id": 5, "score": 0.65},
]

scores, errs = safe_batch_process(sample_records, extract_score)
print(f"  Processed successfully: {len(scores)} records")
print(f"  Scores: {scores}")
print(f"  Errors ({len(errs)}):")
for err in errs:
    print(f"    Record #{err['index']}: {err['error_type']}: {err['error_msg']}")

print("\nDay 17 complete! Robust exceptions = production-ready code.")
