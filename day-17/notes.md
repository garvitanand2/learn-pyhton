# Day 17 Notes — Exception Handling

## The Exception Hierarchy

```
BaseException
├── SystemExit           ← sys.exit()
├── KeyboardInterrupt    ← Ctrl+C
└── Exception            ← All normal exceptions inherit from here
    ├── TypeError        ← Wrong type ("abc" + 1)
    ├── ValueError       ← Right type, wrong value (int("abc"))
    ├── NameError        ← Undefined variable name
    ├── AttributeError   ← Wrong attribute (None.strip())
    ├── KeyError         ← Missing dict key (d["missing"])
    ├── IndexError       ← List out of bounds (l[99])
    ├── FileNotFoundError ← open("missing.txt")
    ├── ZeroDivisionError ← 1 / 0
    ├── ImportError      ← import non_existent_module
    ├── StopIteration    ← Iterator exhausted
    └── RuntimeError     ← Generic runtime error
```

---

## Full try/except/else/finally Structure

```python
try:
    # Code that might fail
    result = risky_operation()
except SpecificError as e:
    # Runs only if SpecificError was raised
    handle_specific(e)
except (AnotherError, ThirdError) as e:
    # Catch multiple exceptions in one handler
    handle_either(e)
except Exception as e:
    # Catch-all for unexpected exceptions
    log_error(e)
else:
    # Runs ONLY if NO exception occurred
    use_result(result)
finally:
    # ALWAYS runs — cleanup, closing resources
    cleanup()
```

### When to use each block

| Block | When to use |
|-------|-------------|
| `except SpecificError` | Preferred — be precise about what you handle |
| `except Exception` | Logging + re-raise; avoid silencing errors |
| `else` | Code that should only run on success |
| `finally` | Resource cleanup (closing files, connections) |

---

## Raising Exceptions

```python
# Raise built-in exception
raise ValueError("Temperature must be between 0 and 1")

# Raise with context
raise TypeError(f"Expected str, got {type(x).__name__}")

# Re-raise current exception (inside except block)
try:
    risky()
except Exception:
    log("Unexpected error")
    raise          # re-raises the same exception

# Chain exceptions (preserve cause)
try:
    load_file()
except FileNotFoundError as e:
    raise RuntimeError("Pipeline failed") from e
```

---

## Custom Exceptions — Best Practice

```python
# 1. Create a base exception for your domain
class AppError(Exception):
    """Base class for all application errors."""
    pass

# 2. Specific exceptions inherit from it
class ConfigError(AppError):
    """Invalid configuration."""
    pass

class DataError(AppError):
    """Data format or content error."""
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"Field '{field}': {message}")

# 3. Catch at different granularities
try:
    process()
except DataError as e:
    handle_data_error(e)
except AppError as e:
    handle_any_app_error(e)
except Exception as e:
    handle_unexpected(e)
```

**Why custom exceptions?**
- Makes code self-documenting ("why did it fail?")
- Allows callers to catch specific errors precisely
- Can carry structured data (field names, codes, context)

---

## Common Pitfalls

### 1. Bare `except:` — Never do this
```python
# BAD — catches KeyboardInterrupt too!
try:
    run()
except:
    pass

# GOOD — at minimum catch Exception
try:
    run()
except Exception as e:
    log(e)
```

### 2. Silent swallowing
```python
# BAD — errors disappear silently
try:
    parse_data(x)
except Exception:
    pass

# GOOD — at least log
try:
    parse_data(x)
except Exception as e:
    logger.warning(f"parse_data failed: {e}")
```

### 3. Too broad catches
```python
# BAD — catches ValueError from unrelated code
try:
    x = int(user_input)
    y = process(x)
    z = format_output(y)
except ValueError:
    print("Bad input")  # which line caused it?

# GOOD — narrow the try block
try:
    x = int(user_input)
except ValueError:
    print("Bad input: expected a number")
    return
```

---

## AI / Production Patterns

### Retry with backoff
```python
import time

def call_api_with_retry(fn, max_retries=3, delay=1.0):
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2  # exponential backoff
```

### Safe batch processor pattern
```python
def process_batch(items, fn):
    results, errors = [], []
    for i, item in enumerate(items):
        try:
            results.append(fn(item))
        except Exception as e:
            errors.append({"index": i, "error": str(e)})
    return results, errors
```

---

## Quick-Fire Interview Questions

1. **What's the difference between `except Exception` and `except:`?**  
   Bare `except:` catches everything including `SystemExit` and `KeyboardInterrupt`; `except Exception` is standard.

2. **When does the `else` block run?**  
   Only if the `try` block completes without raising any exception.

3. **When does `finally` run?**  
   Always — even if exception occurred, `return` executed, or `continue`/`break` triggered.

4. **What does `raise ... from ...` do?**  
   Chains exceptions; the original exception becomes `__cause__` of the new one.

5. **What's the benefit of custom exception classes?**  
   Callers can catch specific failure modes precisely, and exceptions can carry structured context data.
