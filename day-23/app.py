# Day 23: Context Managers
# Focus: Guaranteed resource management with `with` statements

# ============================================================
# WHAT: A context manager controls setup and teardown around
#       a block of code. `with` ensures teardown runs even
#       if an exception occurs.
# WHY:  File handles, database connections, GPU memory,
#       temporary directories, and model inference locks all
#       need guaranteed cleanup. This is how Python does it.
# ============================================================

import time
import os
import json
from pathlib import Path
from contextlib import contextmanager, suppress

# ============================================================
# 1. Why Context Managers Exist
# ============================================================
print("=== 1. The Problem ===")

# Without context manager — resource leak if exception occurs:
# f = open("file.txt")
# data = f.read()      # ← what if this crashes?
# f.close()            # ← this never runs!

# With context manager:
# with open("file.txt") as f:
#     data = f.read()  # ← exception or not, file always closes

# ============================================================
# 2. The Protocol: __enter__ and __exit__
# ============================================================
print("\n=== 2. __enter__ and __exit__ ===")

class Timer:
    """Context manager that measures block execution time.
    
    Usage:
        with Timer("training epoch"):
            train_one_epoch(model, data)
    """

    def __init__(self, label: str = "block"):
        self.label = label
        self.elapsed: float = 0.0

    def __enter__(self):
        """Called at the start of `with` block.
        The return value is assigned to the `as` variable."""
        self._start = time.perf_counter()
        print(f"  [{self.label}] Starting...")
        return self          # `as timer` in `with Timer() as timer:`

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called at the end of `with` block (always).
        
        exc_type, exc_val, exc_tb: exception info (None if no exception).
        Return True to suppress the exception; False/None to propagate it.
        """
        self.elapsed = time.perf_counter() - self._start
        status = "✓ OK" if exc_type is None else f"✗ {exc_type.__name__}"
        print(f"  [{self.label}] {status} — {self.elapsed*1000:.3f}ms")
        return False  # don't suppress exceptions


# Normal usage
with Timer("data preprocessing") as t:
    total = sum(i**2 for i in range(100_000))
print(f"  Elapsed: {t.elapsed*1000:.3f}ms")

# Exception occurs — __exit__ still runs
print()
try:
    with Timer("failing block"):
        x = 1 / 0
except ZeroDivisionError:
    print("  Exception was propagated (not suppressed)")

# ============================================================
# 3. @contextmanager Decorator — Cleaner Syntax
# ============================================================
print("\n=== 3. @contextmanager ===")

# Using a generator with @contextmanager is often simpler
# than writing a full class.

@contextmanager
def timer_ctx(label: str = "block"):
    """Same as Timer class but as a generator-based context manager."""
    start = time.perf_counter()
    print(f"  [{label}] Starting...")
    try:
        yield  # execution pauses here; the `with` block runs
    finally:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  [{label}] Done — {elapsed:.3f}ms")

with timer_ctx("tokenization"):
    tokens = [word for sentence in ["hello world", "foo bar"] * 10_000
              for word in sentence.split()]

print(f"  Token count: {len(tokens)}")

# ============================================================
# 4. Managing Temporary Files
# ============================================================
print("\n=== 4. Temporary Resources ===")

@contextmanager
def temp_json_file(data: dict, suffix: str = ".json"):
    """Creates a temp JSON file, yields its path, deletes after."""
    import tempfile
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, delete=False
        ) as tmp:
            json.dump(data, tmp, indent=2)
            tmp_path = Path(tmp.name)
        print(f"  Temp file created: {tmp_path.name}")
        yield tmp_path
    finally:
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()
            print(f"  Temp file deleted: {tmp_path.name}")

config = {"model": "bert", "lr": 3e-5}
with temp_json_file(config) as path:
    loaded = json.loads(path.read_text())
    print(f"  Loaded from temp file: {loaded}")

print(f"  File exists after `with`: {path.exists()}")

# ============================================================
# 5. Mock Object Patch (Testing Pattern)
# ============================================================
print("\n=== 5. Model Inference Context ===")

class ModelInference:
    """Simulates switching model to eval mode for inference.
    (Like torch.no_grad() and model.eval())"""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.training = True
        self.grad_enabled = True

    def __enter__(self) -> "ModelInference":
        self.training = False
        self.grad_enabled = False
        print(f"  [{self.model_name}] Switched to EVAL mode (grad disabled)")
        return self

    def __exit__(self, *args) -> None:
        self.training = True
        self.grad_enabled = True
        print(f"  [{self.model_name}] Restored to TRAIN mode")

    def predict(self, text: str) -> str:
        assert not self.training, "Call predict only in inference context!"
        return f"[prediction for: '{text}']"


model = ModelInference("bert-classifier")
print(f"  Before: training={model.training}")

with model as m:
    result = m.predict("some input text")
    print(f"  Result: {result}")
    print(f"  During: training={model.training}")

print(f"  After:  training={model.training}")

# ============================================================
# 6. contextlib.suppress — Ignore Specific Exceptions
# ============================================================
print("\n=== 6. suppress ===")

# Remove a file if it exists — old way:
try:
    os.remove("nonexistent_file.txt")
except FileNotFoundError:
    pass

# Clean way with suppress:
with suppress(FileNotFoundError):
    os.remove("nonexistent_file.txt")
    print("  This never prints (exception suppressed)")

print("  Continued normally after suppress")

# ============================================================
# 7. Stacking Context Managers
# ============================================================
print("\n=== 7. Stacking Context Managers ===")

@contextmanager
def log_context(name: str):
    print(f"  START {name}")
    yield
    print(f"  END   {name}")

# Multiple with statements (Python 3.10+ single line)
with log_context("outer") as _:
    with log_context("inner") as _:
        print("  → Doing work here")

# Or in one line (equivalent):
with log_context("A"), log_context("B"):
    print("  → Both contexts active simultaneously")

print("\nDay 23 complete! Context managers = clean, safe resource management.")
