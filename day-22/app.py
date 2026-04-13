# Day 22: Decorators
# Focus: Augmenting functions without modifying them

# ============================================================
# WHAT: A decorator is a function that takes another function
#       and returns an enhanced version of it.
# WHY:  ML frameworks use decorators everywhere: @torch.no_grad(),
#       @property, @classmethod, @app.route(), @pytest.mark.
#       They let you add cross-cutting concerns (timing, logging,
#       caching, validation) without cluttering core logic.
# ============================================================

import time
import functools
import warnings
from datetime import datetime

# ============================================================
# 1. Functions are First-Class Objects
# ============================================================
print("=== 1. Functions as Objects ===")

def greet(name): return f"Hello, {name}!"

# A function can be passed as an argument
def apply_twice(fn, value):
    return fn(fn(value))

print(apply_twice(str.upper, "hello"))  # "HELLO" (already upper)
print(apply_twice(lambda x: x + 1, 5)) # 7

# A function can be returned from another function
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier   # returns the function, not the result!

double = make_multiplier(2)
triple = make_multiplier(3)
print(f"double(5) = {double(5)}")
print(f"triple(5) = {triple(5)}")

# ============================================================
# 2. The Decorator Pattern (Manual)
# ============================================================
print("\n=== 2. Manual Decorator ===")

def timer_wrapper(fn):
    """Wraps fn to print how long it takes to run."""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [{fn.__name__}] took {elapsed*1000:.3f}ms")
        return result
    return wrapper

def slow_tokenize(text):
    time.sleep(0.01)  # simulate slow work
    return text.split()

# Without syntax sugar (manual decoration):
slow_tokenize = timer_wrapper(slow_tokenize)
tokens = slow_tokenize("hello world test")
print(f"  Tokens: {tokens}")

# ============================================================
# 3. The @ Syntax (Decorator Syntax)
# ============================================================
print("\n=== 3. @ Decorator Syntax ===")

# `@timer_wrapper` above `def` is exactly equivalent to:
# `fn = timer_wrapper(fn)` after the definition

@timer_wrapper
def batch_normalize(values: list[float]) -> list[float]:
    total = sum(values)
    return [v / total for v in values if total > 0]

result = batch_normalize([0.1, 0.3, 0.4, 0.2])
print(f"  Normalized: {result}")

# ============================================================
# 4. functools.wraps — Preserve Metadata
# ============================================================
print("\n=== 4. functools.wraps ===")

# Problem: custom wrappers hide original function's name/docstring
def bad_timer(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper

@bad_timer
def my_function():
    """This is my function's docstring."""
    pass

print(f"Without wraps: {my_function.__name__}")    # "wrapper" — WRONG!
print(f"Without wraps: {my_function.__doc__}")     # None — WRONG!

# Fix: use @functools.wraps
def good_timer(fn):
    @functools.wraps(fn)   # ← copies name, doc, annotations from fn
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        print(f"  [{fn.__name__}] {(time.perf_counter()-start)*1000:.3f}ms")
        return result
    return wrapper

@good_timer
def my_function():
    """This is my function's docstring."""
    pass

print(f"With wraps: {my_function.__name__}")    # "my_function" ✓
print(f"With wraps: {my_function.__doc__}")     # correct docstring ✓

# ============================================================
# 5. Decorators with Arguments
# ============================================================
print("\n=== 5. Decorators with Arguments ===")

# For arguments, wrap the decorator in another function:
def retry(max_attempts: int = 3, delay: float = 0.1):
    """Decorator factory: retries a function on failure."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"  Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise RuntimeError(f"Failed after {max_attempts} attempts") from last_exception
        return wrapper
    return decorator

import random
random.seed(42)

@retry(max_attempts=4, delay=0.05)
def flaky_api_call(endpoint: str) -> dict:
    """Simulates an API call that fails 60% of the time."""
    if random.random() < 0.6:
        raise ConnectionError(f"API timeout for {endpoint}")
    return {"status": 200, "data": "success"}

result = flaky_api_call("/predict")
print(f"  Final result: {result}")

# ============================================================
# 6. Useful Built-in Decorators
# ============================================================
print("\n=== 6. Built-in Decorators ===")

# @functools.lru_cache — memoize expensive computations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_compute(n: int) -> int:
    """Fibonacci — exponential without cache, linear with it."""
    if n <= 1: return n
    return expensive_compute(n - 1) + expensive_compute(n - 2)

start = time.perf_counter()
fib_40 = expensive_compute(40)
elapsed_first = time.perf_counter() - start

start = time.perf_counter()
fib_40_again = expensive_compute(40)
elapsed_cached = time.perf_counter() - start

print(f"  fib(40) = {fib_40}")
print(f"  First call:  {elapsed_first*1000:.3f}ms")
print(f"  Cached call: {elapsed_cached*1000:.6f}ms")
print(f"  Cache info: {expensive_compute.cache_info()}")

# ============================================================
# 7. Stacking Decorators
# ============================================================
print("\n=== 7. Stacking Decorators ===")

def validate_input(fn):
    @functools.wraps(fn)
    def wrapper(text: str, *args, **kwargs):
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"Invalid input to {fn.__name__}: {text!r}")
        return fn(text, *args, **kwargs)
    return wrapper

def log_call(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"  → Calling {fn.__name__}({args[0]!r})")
        result = fn(*args, **kwargs)
        print(f"  ← {fn.__name__} returned {result!r}")
        return result
    return wrapper

# Stacking: applied bottom-up, then outer → inner at runtime
@log_call        # applied second
@validate_input  # applied first
def classify(text: str) -> str:
    return "positive" if "good" in text.lower() else "negative"

classify("good performance")
try:
    classify("")
except ValueError as e:
    print(f"  Caught: {e}")

print("\nDay 22 complete! Decorators are the foundation of Python frameworks.")
