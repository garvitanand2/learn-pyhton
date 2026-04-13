# Day 12 Notes — List Comprehensions

## What & Why

**Comprehensions** are concise, readable expressions for building new collections
by transforming or filtering existing ones. They replace multi-line for loops
with a single, expressive line.

They are **faster** than equivalent loops because CPython optimizes them at the
bytecode level (the loop variable assignment happens internally, not via SETATTR).

---

## The Four Comprehension Types

### 1. List Comprehension → produces a list
```python
[expression for item in iterable if condition]
```

### 2. Dict Comprehension → produces a dict
```python
{key_expr: val_expr for item in iterable if condition}
```

### 3. Set Comprehension → produces a set
```python
{expression for item in iterable if condition}
```

### 4. Generator Expression → lazy, produces one item at a time
```python
(expression for item in iterable if condition)
```

---

## Reading Comprehensions (Mental Model)

Read left-to-right like English:

```python
[x ** 2 for x in range(10) if x % 2 == 0]
```

→ "Give me `x squared` for each `x` in `range(10)` if `x is even`"

---

## Filter vs Transform vs Both

```python
# Filter only (no transformation)
passing = [s for s in scores if s >= 0.60]

# Transform only (no filter)
doubled = [s * 2 for s in scores]

# Both
norm_high = [round(s, 4) for s in scores if s >= 0.80]
```

---

## Nested Comprehensions

```python
# Nested loop → flatten
flat = [x for row in matrix for x in row]

# Order: outer loop first, inner loop second (reads left to right)
# for row in matrix:
#     for x in row:
#         flat.append(x)
```

---

## Ternary in Expression Position

```python
# if/else in the expression (not the filter)
labels = ["pass" if s >= 0.6 else "fail" for s in scores]
```

Note the difference in position:
- `[x for x in data if condition]` ← filter (items excluded if condition False)
- `[x if condition else y for x in data]` ← transform (all items kept, value differs)

---

## Generator Expressions

Use `()` instead of `[]` for lazy evaluation:

```python
total = sum(x ** 2 for x in range(1_000_000))   # O(1) memory
any(s > 0.9 for s in scores)                     # stops at first True
all(s >= 0.0 for s in scores)                    # stops at first False
```

**When to use generators vs lists**:
| Use list `[]` | Use generator `()` |
|---------------|-------------------|
| Need random access (`result[i]`) | Iterate once |
| Need `len()` | Feed to `sum()`, `any()`, `all()` |
| Reuse result multiple times | Large dataset (memory matters) |

---

## Walrus Operator `:=` (Python 3.8+)

Assigns a value AND uses it in the same expression:

```python
results = [(text, n) for text in corpus if (n := len(text)) > 100]
```

Without `:=`, you'd compute `len(text)` twice (once in `if`, once to use).

---

## Performance Comparison

```python
# Slowest: string concatenation
result = ""
for word in words:
    result += word + " "

# Faster: join
result = " ".join(word for word in words)

# Memory-efficient: use generator inside join
result = " ".join(clean(w) for w in words if valid(w))
```

---

## Real-World Analogy

A comprehension is like a **SQL SELECT with WHERE**:

```sql
SELECT UPPER(name) AS name, accuracy * 100 AS pct
FROM models
WHERE accuracy >= 0.9;
```

In Python:
```python
[(m["name"].upper(), m["accuracy"] * 100)
 for m in models
 if m["accuracy"] >= 0.9]
```

---

## Interview Quick-Fire

1. **What is the difference between `[]` and `()` comprehension syntax?**
   → `[]` creates a list (eager, all in memory). `()` creates a generator (lazy, one at a time).

2. **When would you prefer a generator over a list comprehension?**
   → When the result is large (memory), used only once (iteration), or fed to `sum()`/`any()`/`all()`.

3. **What is the walrus operator?**
   → `:=` (Python 3.8+) assigns a value during an expression. Avoids computing the same thing twice in a comprehension filter + use.

4. **Are comprehensions always faster than loops?**
   → For typical cases yes (CPython optimizes them). For very complex expressions with many side effects, profiling is needed.

5. **What's wrong with `[x for x in range(10**9)]`?**
   → It tries to build a list with 1 billion elements in RAM — likely crashes. Use `(x for x in range(10**9))` instead.
