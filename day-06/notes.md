# Day 6 Notes — Advanced Functions: *args, **kwargs, Recursion

## What & Why

Real-world Python APIs are flexible — they accept varying numbers of arguments
and optional keyword configurations. Understanding `*args` and `**kwargs` lets
you build APIs like the ones you use every day (scikit-learn, PyTorch, LangChain).
Recursion lets you elegantly solve problems with self-similar structure (trees, graphs, nested docs).

---

## *args — Variable Positional Arguments

Collects all extra positional arguments into a **tuple**.

```python
def log(*values):
    for v in values:
        print(v)

log(1, 2, 3)          # works
log("a", "b", "c")   # works
log()                  # works — empty tuple
```

Inside the function, `values` is a plain tuple — iterate it, slice it, index it.

---

## **kwargs — Variable Keyword Arguments

Collects all extra keyword arguments into a **dict**.

```python
def configure(**settings):
    for k, v in settings.items():
        print(f"{k} = {v}")

configure(temperature=0.7, max_tokens=1024, stream=True)
```

Inside the function, `kwargs` is a plain dict.

---

## Combined Signature Order

```python
def f(positional, *args, keyword_only, **kwargs):
    ...
```

The ordering rules:
1. Required positional params
2. `*args`
3. Keyword-only params (after `*`)
4. `**kwargs`

---

## Unpacking Operators

| Operator | What it does |
|----------|--------------|
| `*iterable` | Unpack list/tuple into positional args |
| `**dict` | Unpack dict into keyword args |

```python
args   = (1, 2, 3)
kwargs = {"sep": "-", "end": "\n"}
print(*args, **kwargs)   # 1-2-3
```

### Merging Dicts

```python
base = {"a": 1, "b": 2}
overrides = {"b": 99, "c": 3}
merged = {**base, **overrides}   # {"a": 1, "b": 99, "c": 3}
# Right-side wins for duplicate keys
```

---

## Keyword-Only Arguments

Placing `*` before a parameter forces it to be passed as a keyword:

```python
def call_model(name, *, temperature, max_tokens):
    ...

call_model("gpt-4", temperature=0.7, max_tokens=512)  # OK
call_model("gpt-4", 0.7, 512)  # TypeError!
```

Use keyword-only for safety-critical or configuration parameters.

---

## Recursion

A function that calls itself. Every recursive function needs:
1. **Base case** — the condition that stops recursion
2. **Recursive case** — the step that makes progress toward the base case

```python
def factorial(n):
    if n <= 1:        # base case
        return 1
    return n * factorial(n - 1)   # recursive case
```

### Recursion Trace for `factorial(4)`:
```
factorial(4)
= 4 * factorial(3)
= 4 * 3 * factorial(2)
= 4 * 3 * 2 * factorial(1)
= 4 * 3 * 2 * 1
= 24
```

### Python Recursion Limit

Default limit: **1000 stack frames** (`sys.getrecursionlimit()`).
Deep recursion raises `RecursionError`. For very deep structures, consider
converting recursion to iteration or using `sys.setrecursionlimit()`.

### Memoization

Caching recursive results to avoid recomputation.

```python
memo = {}
def fib(n):
    if n in memo: return memo[n]
    if n <= 1: return n
    memo[n] = fib(n-1) + fib(n-2)
    return memo[n]
```

This converts `O(2^n)` exponential time to `O(n)` linear time.
Python provides `@functools.lru_cache` (Day 22) for automatic memoization.

---

## `setdefault()` and Defensive **kwargs

```python
def call_model(**kwargs):
    kwargs.setdefault("temperature", 0.7)   # only set if key missing
    kwargs.setdefault("max_tokens", 512)
    return make_api_call(**kwargs)
```

---

## Real-World Analogy

`*args` is like a **variadic function in a CLI tool** — you can pass any number
of files to `grep file1 file2 file3 ...`.

`**kwargs` is like a **JSON config object** — you pass a flexible bag of settings
and the system uses what it needs.

Recursion is like a **directory walker** — to process a folder, you process each
file in it, and for each sub-folder, recursively process that folder.

---

## Interview Quick-Fire

1. **What is `*args`?** → Collects extra positional arguments into a tuple inside the function.

2. **What is `**kwargs`?** → Collects extra keyword arguments into a dictionary.

3. **What order must parameters appear?** → Positional, `*args`, keyword-only, `**kwargs`.

4. **What is the difference between `*args` (definition) and `*iterable` (call)?**
   → In a definition, `*args` collects; in a call, `*iterable` unpacks/spreads.

5. **What happens if recursion has no base case?** → Infinite recursion → `RecursionError` when the call stack limit (default 1000) is exceeded.

6. **What is memoization?** → Caching the results of function calls so the same computation isn't repeated. Converts exponential recursive algorithms to linear time.
