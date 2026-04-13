# Day 1 Notes — Variables & Data Types

## What & Why

Every program (and every AI system) boils down to **data flowing through logic**.
Before you can build a pipeline, train a model, or process text, you need to store
values. That's what **variables** are for.

Python is **dynamically typed** — you don't declare a type; Python infers it at
runtime. This makes code fast to write, but you must understand types to avoid
silent bugs in data pipelines.

---

## Core Data Types

| Type    | Example                | AI / ML use case                        |
|---------|------------------------|-----------------------------------------|
| `int`   | `batch_size = 32`      | counts, indices, layer sizes, epochs    |
| `float` | `lr = 0.001`           | learning rates, probabilities, loss     |
| `bool`  | `is_training = True`   | flags, conditions, switches             |
| `str`   | `label = "cat"`        | prompts, labels, dataset paths          |
| `None`  | `result = None`        | unset outputs, optional config fields   |

---

## How It Works

Python stores each value as an **object** in memory. A variable is just a
**name tag** (reference) pointing to that object.

```
batch_size = 32
```

Memory: `batch_size` ──→ [object: int, value: 32]

When you do `a = b`, you're creating a second name pointing to the **same object**,
not copying it. This matters for mutable types (lists, dicts) — covered in Week 2.

---

## Floating-Point Precision

```python
0.1 + 0.2  # → 0.30000000000000004
```

This is **not a Python bug** — it's how IEEE 754 binary floating-point works.
In AI/ML, always use `round()`, `math.isclose()`, or NumPy for comparisons
involving floats.

---

## Type Conversion (Casting)

| From → To    | Function       | Example                      |
|--------------|----------------|------------------------------|
| str → float  | `float(x)`     | `float("0.85")` → `0.85`     |
| str → int    | `int(x)`       | `int("512")` → `512`         |
| int → str    | `str(x)`       | `str(512)` → `"512"`         |
| float → int  | `int(x)`       | `int(0.97)` → `0` (truncate) |
| anything → bool | `bool(x)`  | `bool(0)` → `False`          |

> **Falsy values**: `0`, `0.0`, `""`, `[]`, `{}`, `None` → all evaluate to `False`
> **Truthy values**: everything else → evaluates to `True`

---

## f-Strings (Python 3.6+)

The modern, preferred way to embed values in strings:

```python
model = "GPT"
version = 4
print(f"Running {model}-{version}")         # Running GPT-4
print(f"Remaining: {4096 - tokens_used}")   # expressions work too
```

Older styles (avoid in new code):
- `"Hello " + name`  — concatenation (messy, slow)
- `"Hello %s" % name` — C-style (legacy)
- `"Hello {}".format(name)` — verbose but still common

---

## Identity vs Equality

| Operator | Checks              | Use when                        |
|----------|---------------------|---------------------------------|
| `==`     | value is the same   | comparing data values            |
| `is`     | same object in RAM  | checking `None`, singletons      |

```python
# Always use `is` (not ==) to check for None
if result is None:
    print("No output yet")
```

---

## Constants Convention

Python has no built-in constant keyword. By convention, use `SCREAMING_SNAKE_CASE`
for values that should not change:

```python
MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.7
```

---

## Real-World Analogy

Think of your Python script as an **AI pipeline config file**:
- `int` → the knobs you turn (epochs, batch size)
- `float` → the precise settings (learning rate, threshold)
- `str` → the labels and instructions (prompts, class names)
- `bool` → the on/off switches (training mode, debug flag)
- `None` → a slot not yet filled (model output waiting to be computed)

---

## Interview Quick-Fire

1. **What is Python's type system?** → Dynamic typing — types are checked at runtime,
   not compile time. Every variable is a reference to an object.

2. **Difference between `is` and `==`?** → `==` checks value equality; `is` checks
   object identity (same memory address).

3. **Why does `0.1 + 0.2 != 0.3`?** → IEEE 754 floating-point representation
   cannot represent 0.1 or 0.2 exactly in binary.

4. **What are falsy values?** → `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None`, `False`.

5. **What is `None`?** → A singleton object of type `NoneType` representing the
   absence of a value. There is only one `None` object in a Python process.
