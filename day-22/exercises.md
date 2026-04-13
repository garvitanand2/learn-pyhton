# Day 22 Exercises — Decorators

Estimated time: 45–60 minutes

---

## Exercise 1 — Timing Decorator Suite

Write these three timing decorators:

1. `@timer` — prints `"fn_name took X.XXXms"`
2. `@timer_stats(n=10)` — runs the function `n` times and prints min/max/avg time
3. `@threshold_warning(max_ms=100)` — prints a `⚠️ SLOW CALL` warning if function exceeds threshold

Test all three with functions that simulate different workloads using `time.sleep()`.

---

## Exercise 2 — Input Validation Decorator

Write `@validate(**type_map)` that validates argument types at runtime:

```python
@validate(text=str, max_tokens=int, temperature=float)
def generate(text: str, max_tokens: int = 100, temperature: float = 0.7):
    return f"Generated from: {text}"

generate("hello", 50, 0.9)   # OK
generate(123, 50, 0.9)        # raises TypeError: expected str for 'text'
generate("hello", "bad", 0.9) # raises TypeError: expected int for 'max_tokens'
```

Use `functools.wraps` and `inspect.signature` to match positional args to parameter names.  
(Hint: `inspect.signature(fn).parameters` gives you parameter names in order.)

---

## Exercise 3 — Rate Limiter

Write `@rate_limit(calls_per_second=5)` that:
1. Tracks timestamps of the last N calls (use `collections.deque`)
2. If calls exceed the rate, sleeps until the oldest call is 1 second old
3. Prints `"Rate limited: waiting X.XXs"` when throttling

Test by calling a function 10 times in rapid succession and verifying it slows down.

---

## Exercise 4 — Caching Decorator with TTL

Write `@cache_with_ttl(max_size=100, ttl_seconds=60)` that:
1. Caches results like `lru_cache`
2. Each cached entry expires after `ttl_seconds`
3. Expired entries are recomputed on next call
4. Has a `cache_info()` method: `{"hits": N, "misses": M, "expired": K, "size": S}`

Test by mocking time with a `time_provider` parameter (or use `time.sleep` with short TTL).

---

## Exercise 5 — `@trace` Decorator for Debugging

Write `@trace` that:
1. Before calling: print `"CALL fn_name(args, kwargs)"`
2. After calling: print `"RETURN fn_name → <result>"`
3. On exception: print `"ERROR fn_name → ExceptionType: message"` and re-raises

Then write `@conditional_trace(enabled=True)` — only traces if `enabled=True`.

This pattern is used in ML libraries to trace execution graphs.

---

## Stretch Challenge — Class Decorator

A decorator can also be a **class** (by implementing `__call__`):

```python
class Retry:
    def __init__(self, fn):
        functools.update_wrapper(self, fn)  # equivalent to @wraps
        self.fn = fn
        self.attempt_counts: dict[str, int] = {}
    
    def __call__(self, *args, **kwargs):
        ...  # retry logic
    
    def stats(self):
        return self.attempt_counts
```

Implement `Retry` as a class decorator that:
1. Retries up to 3 times on any exception
2. Tracks per-function call attempt counts (accessible via `.stats()`)
3. Exposes the decorated function's metadata via `functools.update_wrapper`
