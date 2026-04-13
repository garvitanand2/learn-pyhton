# Day 9 Notes — Tuples & Sets

## Tuples

### What & Why

A **tuple** is an **ordered, immutable** sequence. Once created, it cannot
be modified. This immutability makes tuples:
- **Hashable** — can be used as dictionary keys or set elements
- **Safe** — passed around without risk of accidental mutation
- **Slightly faster** — than lists for iteration/storage
- **Semantically meaningful** — signals "this data is fixed"

```python
# Tuple: items are related, fixed set, positional meaning
model_info = ("gpt-4", "openai", 128000)   # name, provider, max_tokens

# List: items are individual, may grow/change
batch_losses = [0.92, 0.81, 0.74]
```

---

### Singleton Tuple

```python
t = (42,)   # ← trailing comma makes it a tuple
x = (42)    # ← this is just an int in parentheses!

print(type(t))   # <class 'tuple'>
print(type(x))   # <class 'int'>
```

---

### Unpacking

```python
name, accuracy = ("BERT", 0.92)        # basic
first, *rest   = (1, 2, 3, 4, 5)       # extended: rest = [2, 3, 4, 5]
a, b = b, a                             # swap
```

**Extended unpacking** (`*`) captures the "rest" as a list.

---

### `namedtuple`

A subclass of tuple where fields have names — like a lightweight data class:

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3.0, 4.0)
print(p.x, p.y)   # 3.0 4.0
print(p[0])       # 3.0 — still indexable
```

Use when you want the readability of attribute access without full OOP (Day 18).

---

## Sets

### What & Why

A **set** is an **unordered collection of unique, hashable elements**.
Built on a hash table — same as dict keys — giving O(1) average-case operations.

| Operation          | List O(?) | Set O(?) |
|--------------------|-----------|----------|
| Membership (`in`)  | O(n)      | O(1)     |
| Add element        | O(1)      | O(1)     |
| Remove element     | O(n)      | O(1)     |

When you have millions of tokens and need to check if each one is in a
vocabulary, a `set` is 1000× faster than a `list`.

---

### Set Algebra

```python
A | B    # union: all elements from both
A & B    # intersection: elements in both
A - B    # difference: in A but not in B
A ^ B    # symmetric difference: in one but not both
```

Also available as methods: `.union()`, `.intersection()`, `.difference()`, `.symmetric_difference()`.

---

### Mutable vs Frozen Sets

| Type | Mutable | Hashable (usable as dict key) |
|------|---------|-------------------------------|
| `set` | Yes | No |
| `frozenset` | No | Yes |

```python
immutable_vocab = frozenset(["cat", "dog", "bird"])
cache = {immutable_vocab: "vocab v1"}   # frozenset as dict key — valid!
```

---

### Common Mistakes

```python
# Empty set:
s = set()   # ✓ CORRECT
s = {}      # ✗ WRONG — this is an empty dict!

# Non-hashable elements:
s = {[1, 2], [3, 4]}   # TypeError: unhashable type 'list'
s = {(1, 2), (3, 4)}   # ✓ Tuples are hashable
```

---

## When to Use What

| Situation | Use |
|-----------|-----|
| Ordered, changeable data | `list` |
| Fixed record, return multiple values | `tuple` |
| Fast membership test, deduplication | `set` |
| Set algebra (union/intersection) | `set` |
| Immutable set (dict key, element of set) | `frozenset` |

---

## Real-World Analogy

- **Tuple** → A database **row** (fixed schema, positional fields, immutable record)
- **Set** → A **whitelist/blacklist** — add items, check membership instantly, no duplicates

---

## Interview Quick-Fire

1. **Why can't you use a list as a dict key?** → Lists are mutable (unhashable). Dict keys must be hashable (their hash value can't change). Tuples are immutable, so they're hashable.

2. **What is the time complexity of `x in my_set`?** → O(1) average case (hash table lookup). Worst case O(n) due to hash collisions, but this is extremely rare.

3. **`set()` vs `{}`?** → `{}` creates an empty **dict**. Use `set()` for an empty set.

4. **What does `A ^ B` return for sets?** → Symmetric difference: elements in A or B but **not in both**. Useful for finding what changed between two versions.

5. **Can a set contain another set?** → No. Elements must be hashable. Use `frozenset` as an element of a set.
