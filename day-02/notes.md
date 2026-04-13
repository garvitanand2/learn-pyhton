# Day 2 Notes — Operators & Input/Output

## What & Why

**Operators** are the verbs of programming — they tell Python *what to do* with values.
**Input/Output (I/O)** is how your program talks to the outside world (users, files, APIs).

In AI engineering:
- Arithmetic operators → compute loss, normalize data, batch indices
- Comparison operators → check thresholds, validate conditions
- Logical operators → combine conditions in control flow

---

## Arithmetic Operators

| Operator | Name             | Example          | Result |
|----------|------------------|------------------|--------|
| `+`      | Addition          | `3 + 2`          | `5`    |
| `-`      | Subtraction       | `10 - 3.5`       | `6.5`  |
| `*`      | Multiplication    | `4 * 2`          | `8`    |
| `/`      | True division     | `7 / 2`          | `3.5`  |
| `//`     | Floor division    | `7 // 2`         | `3`    |
| `%`      | Modulo (remainder)| `7 % 2`          | `1`    |
| `**`     | Exponentiation    | `2 ** 10`        | `1024` |

> In Python 3, `/` always returns `float`. Use `//` for integer division.

### Critical AI Pattern: Batching with `//` and `%`
```python
num_batches = dataset_size // batch_size   # how many full batches
leftover    = dataset_size % batch_size    # samples in the last partial batch
```

---

## Augmented Assignment

Shorthand operators that modify a variable in place:

```python
x += 1   # x = x + 1
x -= 1   # x = x - 1
x *= 2   # x = x * 2
x /= 2   # x = x / 2
x //= 2  # x = x // 2
x **= 2  # x = x ** 2
x %= 3   # x = x % 3
```

Use `+=` constantly when accumulating losses, counts, totals.

---

## Comparison Operators

Always return `True` or `False`.

| Operator | Meaning                |
|----------|------------------------|
| `==`     | equal to               |
| `!=`     | not equal to           |
| `<`      | less than              |
| `>`      | greater than           |
| `<=`     | less than or equal     |
| `>=`     | greater than or equal  |

### Chained Comparisons (Pythonic)
```python
if 0.0 <= confidence <= 1.0:   # valid probability range
    print("Valid confidence score")
```

---

## Logical Operators

| Operator | Meaning         | Short-circuit rule         |
|----------|-----------------|----------------------------|
| `and`    | both True       | stops at first `False`     |
| `or`     | at least one True | stops at first `True`    |
| `not`    | inverts bool    | —                          |

### Short-Circuit Evaluation
```python
# Safe: doesn't call expensive_fn() if flag is False
if flag and expensive_function():
    ...

# Fallback pattern (very common in Python)
result = compute() or default_value
```

---

## Operator Precedence (High → Low)

1. `()` — Parentheses
2. `**` — Exponentiation (right-associative!)
3. `+x`, `-x`, `~x` — Unary
4. `*`, `/`, `//`, `%`
5. `+`, `-`
6. `<<`, `>>`
7. `&`, `^`, `|`
8. `==`, `!=`, `<`, `>`, `<=`, `>=`
9. `not`
10. `and`
11. `or`

> When in doubt, use parentheses. They make intent clear and prevent bugs.

---

## Input / Output

### `input()` — always returns a string
```python
name  = input("Name: ")          # str
lr    = float(input("LR: "))     # must cast to float
steps = int(input("Steps: "))    # must cast to int
```

### `print()` — flexible output
```python
print("a", "b", "c", sep=", ")    # a, b, c
print("loading", end="...")        # no newline at end

# f-string with format spec
print(f"{value:.4f}")    # 4 decimal places
print(f"{name:<20}")     # left-align in 20-char field
print(f"{value:>10.2f}") # right-align, 2 decimal places
```

---

## Real-World Analogy

Think of operators as the **mathematical machinery** inside a training loop:
- `+`, `-` → accumulate and adjust losses
- `//`, `%` → chop a dataset into mini-batches
- `==`, `>=` → decide whether to stop training (early stopping)
- `and`, `or` → combine multiple conditions before acting

---

## Interview Quick-Fire

1. **`/` vs `//`?** → `/` always returns float; `//` returns the floor of the quotient (int if both operands are int).
2. **What is short-circuit evaluation?** → `and` stops evaluating at the first `False`; `or` stops at the first `True`. Used for safety and performance.
3. **Operator precedence for `2 ** 3 ** 2`?** → `512`. Exponentiation is right-associative: evaluated as `2 ** (3 ** 2)` = `2 ** 9` = `512`.
4. **How do you safely get a fallback value?** → `result = value or default` — works because `None`, `0`, `""`, `[]` are falsy.
5. **What does `input()` return?** → Always a `str`. You must explicitly cast it.
