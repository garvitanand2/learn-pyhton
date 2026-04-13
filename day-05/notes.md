# Day 5 Notes — Functions (Basics)

## What & Why

A **function** is a named, reusable block of code that takes inputs (parameters),
does some work, and optionally returns an output.

In AI engineering:
- Every preprocessing step is a function
- Every model call is wrapped in a function
- Every evaluation metric is a function
- Functions compose into pipelines

The key principle: **one function = one responsibility**

---

## Anatomy of a Function

```python
def function_name(param1, param2, param3=default) -> return_type:
    """Docstring: what this function does."""
    # body
    return result
```

| Part | Purpose |
|------|---------|
| `def` | keyword to define a function |
| `function_name` | snake_case by convention |
| `param1, param2` | inputs (positional) |
| `param3=default` | optional parameter with fallback |
| `-> return_type` | type hint for return value (optional but good practice) |
| `"""..."""` | docstring |
| `return` | sends a value back to the caller |

---

## Parameters vs Arguments

- **Parameter**: the variable in the function definition → `def greet(name):`
- **Argument**: the actual value passed when calling → `greet("Alice")`

---

## Default Parameters

```python
def create_prompt(task, style="formal", max_length=500):
    ...

create_prompt("summarize")            # uses defaults
create_prompt("summarize", max_length=200)  # partial override
```

**Critical rule**: Default values are evaluated **once** at definition time.
**Never use mutable defaults** like lists or dicts:

```python
# BUG — shared mutable default:
def add_token(text, tokens=[]):
    tokens.append(text)
    return tokens

# FIX — use None and create new list inside:
def add_token(text, tokens=None):
    if tokens is None:
        tokens = []
    tokens.append(text)
    return tokens
```

---

## Multiple Return Values

Python functions can return multiple values — they're packed into a tuple.

```python
def get_stats(values):
    return min(values), max(values), sum(values) / len(values)

lo, hi, mean = get_stats([1, 5, 3, 7])   # destructuring
```

---

## Scope — LEGB Rule

Python resolves names in this order:

1. **L**ocal — inside the current function
2. **E**nclosing — inside any wrapping function (closures)
3. **G**lobal — module-level names
4. **B**uilt-in — Python's built-in names (`len`, `print`, `range`, etc.)

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)    # "local"
    inner()

outer()
print(x)    # "global"
```

**Best practice**: Avoid `global` keyword — it creates tight coupling.
Use function arguments and return values instead.

---

## Pure Functions vs Side Effects

| Pure Function | Side Effect |
|---------------|-------------|
| Depends only on inputs | Modifies state outside itself |
| Always same output for same input | May produce different results |
| Easier to test | Harder to reason about |

Prefer pure functions in data pipelines — they're predictable and testable.

---

## First-Class Functions

Functions are **objects** in Python — you can:
- Assign to a variable: `fn = my_function`
- Pass as an argument: `apply(fn, data)`
- Return from a function: `return fn`
- Store in a list: `pipeline = [step1, step2, step3]`

This is the basis of functional pipelines in Python.

---

## Real-World Analogy

A function is like a **pipeline stage** in a data processing system:
- Input: raw data → Output: transformed data
- Each stage does one thing well
- Stages compose to form the full pipeline
- Good stages are **stateless** (pure functions)

---

## Interview Quick-Fire

1. **What is the difference between a parameter and an argument?**
   → Parameter is in the definition; argument is the value passed during the call.

2. **Why should you avoid mutable default arguments?**
   → The default is created once at function definition time. All calls share the same object, causing unexpected state accumulation.

3. **What does `return` without a value return?**
   → `None`.

4. **What is the LEGB rule?**
   → Python looks up names in: Local → Enclosing → Global → Built-in scope.

5. **What is a pure function?**
   → A function with no side effects that always returns the same output for the same input. Easy to test, cache, and parallelize.
