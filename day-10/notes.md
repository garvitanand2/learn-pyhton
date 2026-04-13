# Day 10 Notes — Dictionaries (Deep Dive)

## What & Why

A **dictionary** is Python's hash map — it maps **keys** to **values** with:
- O(1) average lookup, insert, delete
- Ordered by insertion (Python 3.7+)
- Keys must be hashable (str, int, tuple — NOT list or dict)
- Values can be anything

Dicts are everywhere in AI: API responses, configs, feature maps,
inference results, word-to-index mappings, accumulating stats.

---

## Access Patterns

| Pattern | Code | Behavior |
|---------|------|----------|
| Hard access | `d["key"]` | KeyError if missing |
| Safe access | `d.get("key")` | Returns None if missing |
| Safe with default | `d.get("key", default)` | Returns default if missing |
| Set if missing | `d.setdefault("key", val)` | Sets only if key absent |

**Rule**: Use `.get()` in production code. Only use `d["key"]` when you're
sure the key exists or want to fail fast on a programming error.

---

## Important Methods

| Method | Returns | Side effect |
|--------|---------|-------------|
| `d.keys()` | view of keys | — |
| `d.values()` | view of values | — |
| `d.items()` | view of (k, v) pairs | — |
| `d.get(k, default)` | value or default | — |
| `d.pop(k)` | value | removes key |
| `d.popitem()` | last (k, v) pair | removes it |
| `d.update(other)` | None | merges other into d |
| `d.setdefault(k, v)` | value | sets if missing |
| `d.copy()` | shallow copy | — |
| `d.clear()` | None | empties dict |

---

## Dict Comprehension

```python
{key_expr: val_expr for item in iterable if condition}
```

Examples:
```python
# Invert a mapping
idx_to_word = {v: k for k, v in word_to_idx.items()}

# Filter
high_conf = {k: v for k, v in results.items() if v >= 0.9}

# Transform values
pct = {k: v * 100 for k, v in metrics.items()}

# Build from two lists
mapping = {k: v for k, v in zip(keys, values)}
```

---

## `collections.defaultdict`

Automatically creates a default value for missing keys:

```python
from collections import defaultdict

freq = defaultdict(int)    # default: 0
freq["new_word"] += 1      # no KeyError

groups = defaultdict(list)
groups["cat"].append("img1.jpg")   # no KeyError
```

Common default factories: `int`, `list`, `set`, `dict`, `float`

---

## `collections.Counter`

A dict subclass optimized for counting:

```python
from collections import Counter

freq = Counter(["a", "b", "a", "c", "a"])
freq.most_common(2)   # [("a", 3), ("b", 1)]
freq["x"]             # 0, not KeyError
freq + Counter(...)   # merge counts
```

---

## Merging Dicts

| Method | Python version | Notes |
|--------|---------------|-------|
| `{**a, **b}` | 3.5+ | Creates new dict; b wins |
| `a.update(b)` | all | Mutates a; b wins |
| `a \| b` | 3.9+ | Creates new dict; b wins |
| `a \|= b` | 3.9+ | In-place update; b wins |

---

## Dict vs List

| Situation | Use |
|-----------|-----|
| Access by position | list |
| Access by name | dict |
| Counting occurrences | Counter or defaultdict(int) |
| Grouping items | defaultdict(list) |
| Config/settings | dict |
| Cache (key → result) | dict |

---

## Views vs Copies

`d.keys()`, `d.values()`, `d.items()` return **views** — they reflect
changes to the dict in real time. To get a static snapshot: `list(d.keys())`.

---

## Real-World Analogy

A dict is like a **JSON config file** or a **database row** accessed by column name.
Every time you call an LLM API, you're building a dict and sending it:

```python
payload = {
    "model": "gpt-4",
    "messages": [...],
    "temperature": 0.7
}
response = requests.post(url, json=payload)
```

---

## Interview Quick-Fire

1. **What is the time complexity of dict lookup?** → O(1) average, O(n) worst case (hash collision, very rare with Python's hash table).

2. **Why can't you use a list as a dict key?** → Lists are mutable (unhashable). Dict keys must have a stable hash value.

3. **What's the difference between `d["key"]` and `d.get("key")`?** → `d["key"]` raises `KeyError` if missing; `.get()` returns None (or a default).

4. **Are Python dicts ordered?** → Yes, since Python 3.7 — insertion order is guaranteed.

5. **What is `defaultdict` and when would you use it?** → A dict subclass that auto-creates default values for missing keys, eliminating "check then set" boilerplate. Use for frequency counting, grouping, and graph adjacency lists.
