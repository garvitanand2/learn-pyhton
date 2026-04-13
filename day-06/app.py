# =============================================================
# Day 6: Advanced Functions — *args, **kwargs, Recursion
# Goal: Write flexible, composable functions.
#       AI frameworks (like LangChain, PyTorch) use these
#       patterns extensively in their APIs.
# =============================================================

# --- 1. *args — VARIABLE POSITIONAL ARGUMENTS ----------------
# What: Collects all extra positional args into a TUPLE
# Why:  When you don't know how many inputs a function will receive

def combine_texts(*texts: str) -> str:
    """Combine any number of text segments into one string."""
    return " ".join(texts)

result = combine_texts("Large", "Language", "Models", "are", "powerful")
print(result)   # Large Language Models are powerful

def log_metrics(*values: float) -> dict:
    """Compute stats over any number of metric values."""
    return {
        "count":  len(values),
        "min":    min(values),
        "max":    max(values),
        "mean":   sum(values) / len(values),
    }

stats = log_metrics(0.82, 0.91, 0.78, 0.95, 0.87)
print(f"\nMetric stats: {stats}")

# --- 2. **kwargs — VARIABLE KEYWORD ARGUMENTS ----------------
# What: Collects extra keyword arguments into a DICT
# Why:  Flexible configuration, forward-compatible APIs

def create_request(**kwargs) -> dict:
    """Build an API request payload from keyword arguments."""
    return kwargs

req = create_request(
    model="gpt-4",
    temperature=0.7,
    max_tokens=1024,
    stream=True,
    user="alice"
)
print(f"\nRequest payload: {req}")

# Forwarding kwargs to another function (very common pattern)
def safe_model_call(model_fn, **kwargs):
    """Wrapper that adds safety defaults before calling the model."""
    kwargs.setdefault("max_tokens", 512)    # set if not provided
    kwargs.setdefault("temperature", 0.5)
    return model_fn(**kwargs)               # unpack dict as keyword args

def mock_model(**kwargs):
    return f"Called with: {kwargs}"

output = safe_model_call(mock_model, model="gpt-4", max_tokens=2048)
print(f"\n{output}")

# --- 3. COMBINING *args AND **kwargs -------------------------
# Full signature: (required, *args, **kwargs) — order matters!

def pipeline_step(step_name: str, *inputs, **config) -> str:
    """
    A generic pipeline step that accepts:
    - step_name: required positional
    - *inputs: any number of input data items
    - **config: any configuration parameters
    """
    input_count = len(inputs)
    config_str  = ", ".join(f"{k}={v}" for k, v in config.items())
    return f"[{step_name}] processing {input_count} inputs | config: {config_str}"

msg = pipeline_step(
    "tokenizer",
    "Hello world", "Goodbye world",   # *inputs
    lowercase=True, max_len=512        # **kwargs
)
print(f"\n{msg}")

# --- 4. UNPACKING OPERATORS (* and **) -----------------------
# The reverse: spread a list/dict into separate arguments

def compute_loss(y_true, y_pred, loss_type="mse"):
    err = y_true - y_pred
    return err ** 2 if loss_type == "mse" else abs(err)

# Unpack a tuple into positional args
args_tuple = (10.0, 7.5)
loss = compute_loss(*args_tuple, loss_type="mse")   # 10.0, 7.5
print(f"\nLoss: {loss}")

# Unpack a dict into keyword args
config_dict = {"y_true": 10.0, "y_pred": 7.5, "loss_type": "mae"}
loss = compute_loss(**config_dict)
print(f"Loss (dict unpack): {loss}")

# Merging dicts with ** (Python 3.9+ has | operator too)
defaults  = {"temperature": 0.7, "top_p": 1.0, "max_tokens": 512}
overrides = {"temperature": 0.2, "max_tokens": 2048}
final_cfg = {**defaults, **overrides}   # overrides win
print(f"\nMerged config: {final_cfg}")

# --- 5. RECURSION ---------------------------------------------
# What: A function that calls itself to solve a smaller sub-problem
# AI use: Tree traversal (AST, knowledge graphs), divide-and-conquer

def factorial(n: int) -> int:
    """Compute n! recursively."""
    if n <= 1:          # base case — stops the recursion
        return 1
    return n * factorial(n - 1)   # recursive case

print(f"\n5! = {factorial(5)}")    # 120
print(f"10! = {factorial(10)}")   # 3628800

# Fibonacci — classic recursion (naive, exponential time)
def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"\nFibonacci(10) = {fibonacci(10)}")   # 55

# Memoized Fibonacci (O(n) time) — preview of lru_cache (Day 22)
def fibonacci_memo(n: int, memo: dict = None) -> int:
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]

print(f"Fibonacci_memo(35) = {fibonacci_memo(35)}")   # fast!

# --- 6. RECURSION FOR TREE/NESTED DATA -----------------------
# JSON / nested dicts are tree structures — recursion is natural here

def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """
    Flatten a nested dictionary into dot-notation keys.
    
    Example:
        {"model": {"name": "gpt-4", "config": {"lr": 0.001}}}
        → {"model.name": "gpt-4", "model.config.lr": 0.001}
    """
    items = {}
    for key, value in d.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.update(flatten_dict(value, new_key, sep))   # RECURSE
        else:
            items[new_key] = value
    return items

nested = {
    "model": {
        "name": "llama-3",
        "training": {
            "lr": 0.001,
            "epochs": 50,
            "batch_size": 32
        }
    },
    "eval": {
        "metric": "f1",
        "threshold": 0.8
    }
}

flat = flatten_dict(nested)
print("\nFlattened config:")
for k, v in flat.items():
    print(f"  {k}: {v}")

# --- 7. KEYWORD-ONLY ARGUMENTS (after *) ---------------------
# Force callers to use keyword syntax for important args

def train_model(model_name: str, *, learning_rate: float, epochs: int) -> str:
    """* forces lr and epochs to be keyword-only."""
    return f"Training {model_name}: lr={learning_rate}, epochs={epochs}"

# Must use keywords:
result = train_model("transformer", learning_rate=0.001, epochs=100)
print(f"\n{result}")

# This would raise TypeError:
# train_model("transformer", 0.001, 100)   ← wrong!

# --- SUMMARY --------------------------------------------------
print("\n--- Day 6 Complete ---")
print("Advanced functions: *args, **kwargs, recursion — the backbone of flexible APIs.")
