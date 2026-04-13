# Day 22 Notes — Decorators

## What Is a Decorator?

A decorator is a **higher-order function** — a function that accepts a function and returns a (usually enhanced) function.

```python
def my_decorator(fn):         # accepts function
    def wrapper(*args, **kwargs):
        print("Before")
        result = fn(*args, **kwargs)  # call original
        print("After")
        return result
    return wrapper            # returns new function

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Before
# Hello!
# After
```

`@my_decorator` above a function is *syntactic sugar* for:
```python
say_hello = my_decorator(say_hello)
```

---

## Always Use `@functools.wraps`

Without it, your wrapper replaces the original function's identity:

```python
import functools

def my_decorator(fn):
    @functools.wraps(fn)  # ← copies __name__, __doc__, __annotations__
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper
```

---

## Decorator with Arguments — Three Layers

```python
def retry(max_attempts=3):      # Layer 1: decorator factory (takes args)
    def decorator(fn):          # Layer 2: actual decorator (takes function)
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):  # Layer 3: wrapper (called at runtime)
            for i in range(max_attempts):
                try:
                    return fn(*args, **kwargs)
                except Exception:
                    if i == max_attempts - 1:
                        raise
        return wrapper
    return decorator

@retry(max_attempts=5)
def my_function(): ...
```

---

## Common Decorator Patterns

### Timer
```python
def timer(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        print(f"{fn.__name__} took {(time.perf_counter()-start)*1000:.2f}ms")
        return result
    return wrapper
```

### Validator
```python
def validate_not_empty(fn):
    @functools.wraps(fn)
    def wrapper(text, *args, **kwargs):
        if not text or not text.strip():
            raise ValueError("Input cannot be empty")
        return fn(text, *args, **kwargs)
    return wrapper
```

### Memoize (Manual)
```python
def memoize(fn):
    cache = {}
    @functools.wraps(fn)
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper
```

### Deprecation Warning
```python
def deprecated(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"{fn.__name__} is deprecated",
            DeprecationWarning, stacklevel=2
        )
        return fn(*args, **kwargs)
    return wrapper
```

---

## Stacking Decorators

When stacking, **decorators apply bottom-up**, but **execute outer-first at runtime**:

```python
@A   # applied second; outermost wrapper → runs first
@B   # applied first; innermost wrapper → runs second
def f(): ...

# Equivalent to:
f = A(B(f))
```

---

## `functools.lru_cache`

```python
from functools import lru_cache

@lru_cache(maxsize=256)    # cache up to 256 unique call signatures
def embed_text(text: str) -> list[float]:
    # ... expensive embedding computation
    return [0.1, 0.2, ...]

embed_text("hello")   # computed and cached
embed_text("hello")   # ← served from cache instantly

embed_text.cache_info()    # CacheInfo(hits=1, misses=1, maxsize=256, currsize=1)
embed_text.cache_clear()   # remove all cached values
```

**Important:** Only works with **hashable** arguments (strings, ints, tuples — NOT lists/dicts).

---

## Framework Examples

```python
# Flask
@app.route("/predict", methods=["POST"])
def predict(): ...

# pytest
@pytest.mark.parametrize("input,expected", [...])
def test_classifier(input, expected): ...

# PyTorch
@torch.no_grad()
def evaluate(model, data): ...

# Pydantic / FastAPI
@validator("learning_rate")
def check_lr(cls, v):
    assert 0 < v < 1, "LR out of range"
    return v
```

---

## Quick-Fire Interview Questions

1. **What does a decorator do?**  
   Takes a function, wraps it to add behavior, returns the enhanced version.

2. **Why use `@functools.wraps`?**  
   Preserves `__name__`, `__doc__`, and type annotations of the original function.

3. **How do you write a decorator that accepts arguments?**  
   Add an outer factory layer: `def decorator_factory(arg): def decorator(fn): def wrapper(...): ...`

4. **What's the order of execution with stacked decorators?**  
   Applied bottom-up; the outermost decorator's wrapper runs first at call time.

5. **When would you use `lru_cache`?**  
   For pure functions (same input always gives same output) that are called repeatedly with the same arguments — e.g., tokenization, embedding lookup, Fibonacci.
