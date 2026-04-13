# Day 24 Notes — Lambda, Map, Filter, Reduce

## Lambda — When to Use (and When Not To)

```python
# Good — short, inline, obvious
items.sort(key=lambda x: x["score"])
filtered = filter(lambda x: x > 0, values)
squared = map(lambda x: x**2, data)

# Bad — complex logic, assign to variable
normalize = lambda x, min_v, max_v: (x - min_v) / (max_v - min_v) if max_v > min_v else 0
# → Use def instead! Named functions are more readable and debuggable.
```

**Rule:** If a lambda is more than one expression, or gets assigned to a variable name, write a `def` instead.

---

## map() — Lazy Transformation

```python
# Always lazy — returns iterator, not list
result = map(fn, iterable)        # not computed yet
result = map(fn, iter1, iter2)    # zip-like behavior

# Materialize:
list(map(str.upper, ["a", "b"]))  # ["A", "B"]
set(map(len, ["hi", "hello"]))    # {2, 5}
dict(map(lambda x: (x, x**2), range(5)))  # {0: 0, 1: 1, ...}
```

---

## filter() — Lazy Selection

```python
# Returns iterator of elements where fn(x) is truthy
evens = filter(lambda x: x % 2 == 0, range(10))

# filter(None, iterable) — removes falsy values
truthy = list(filter(None, [0, 1, "", "hello", None, [], [1]]))
# → [1, "hello", [1]]
```

---

## reduce() — Accumulate to Single Value

```python
from functools import reduce

reduce(fn, [a, b, c, d])
# Step 1: acc = fn(a, b)
# Step 2: acc = fn(acc, c)
# Step 3: acc = fn(acc, d)
# Return: acc

# With initial value:
reduce(fn, iterable, initial_value)
```

Common uses:
```python
import operator
reduce(operator.add, [1, 2, 3, 4])    # 10
reduce(operator.mul, [1, 2, 3, 4])    # 24
reduce(lambda a, b: a | b, [{"x"}, {"y"}, {"z"}])  # {"x", "y", "z"}
reduce(lambda best, x: x if x > best else best, values)  # max()
```

---

## functools.partial

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube   = partial(power, exponent=3)

square(4)   # 16
cube(4)     # 64

# Useful for customizing behavior passed to map/filter:
normalize_100 = partial(scale, factor=100)
scaled = list(map(normalize_100, raw_values))
```

---

## map/filter/reduce vs Comprehensions

| Operation | Comprehension | Functional |
|-----------|--------------|------------|
| Transform | `[f(x) for x in data]` | `list(map(f, data))` |
| Filter | `[x for x in data if pred(x)]` | `list(filter(pred, data))` |
| Both | `[f(x) for x in data if pred(x)]` | `list(map(f, filter(pred, data)))` |
| Reduce | loop + accumulate | `reduce(fn, data)` |

**Prefer comprehensions** for readability.  
**Use map/filter with named functions** for functional pipeline style.  
**Use generators** (`(x for x in ...)`) for memory efficiency in pipelines.

---

## operator Module — Replace Lambdas

```python
import operator

# Instead of: sorted(items, key=lambda x: x["score"])
from operator import itemgetter
sorted(items, key=itemgetter("score"))

# Instead of: lambda x, y: x * y
operator.mul(3, 4)   # 12

# Instead of: lambda x: x.name
from operator import attrgetter
sorted(objects, key=attrgetter("name"))
```

---

## Function Composition

```python
from functools import reduce

def pipe(*fns):
    """Apply functions left to right: pipe(f, g)(x) = g(f(x))"""
    return lambda x: reduce(lambda v, fn: fn(v), fns, x)

preprocess = pipe(
    str.strip,
    str.lower,
    lambda s: re.sub(r"[^\w\s]", "", s),
    str.split,
)

preprocess("  Hello, World!  ")  # ["hello", "world"]
```

---

## Quick-Fire Interview Questions

1. **What's the difference between `map()` and a list comprehension?**  
   Both transform, but `map()` is lazy and takes a function object; comprehensions are more readable and support complex expressions.

2. **What does `filter(None, iterable)` do?**  
   Returns only truthy elements (removes `0`, `""`, `None`, `[]`, etc.).

3. **What does `reduce(fn, [a,b,c])` compute?**  
   `fn(fn(a, b), c)` — folds left with binary function.

4. **What is `partial()`?**  
   Creates a new function by pre-filling some arguments of an existing function.

5. **When should you use `lambda` vs `def`?**  
   `lambda` for short, inline, single-expression operations (sorting keys, callbacks). Use `def` when the function is multi-line, complex, or will be reused.
