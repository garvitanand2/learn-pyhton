# Day 8 Notes — Lists

## What & Why

A **list** is Python's most versatile built-in data structure:
- **Ordered** — elements have a position (index)
- **Mutable** — can be changed after creation
- **Duplicates allowed** — same value can appear multiple times
- **Heterogeneous** — can hold any mix of types (though avoid this in practice)

In AI/ML, lists hold: tokens, labels, loss curves, prediction scores,
batch samples, layer sizes — almost everything flows through lists.

---

## Key Operations & Time Complexity

| Operation | Method | Time Complexity |
|-----------|--------|-----------------|
| Access by index | `lst[i]` | O(1) |
| Append to end | `lst.append(x)` | O(1) amortized |
| Pop from end | `lst.pop()` | O(1) |
| Insert at index i | `lst.insert(i, x)` | O(n) |
| Remove by value | `lst.remove(x)` | O(n) |
| Search by value | `x in lst` | O(n) |
| Sort | `lst.sort()` | O(n log n) |
| Slice | `lst[a:b]` | O(k) where k = slice size |
| Copy | `lst.copy()` | O(n) |

---

## Slicing

```python
lst[start:stop:step]
```

- `stop` is **exclusive** (not included)
- All three parts are optional
- Negative values count from the end

| Slice | Meaning |
|-------|---------|
| `lst[:]` | full copy |
| `lst[:3]` | first 3 elements |
| `lst[-3:]` | last 3 elements |
| `lst[::2]` | every 2nd element |
| `lst[::-1]` | reversed |

---

## Mutation vs New List

| Method | Modifies original? | Returns |
|--------|--------------------|---------|
| `lst.sort()` | Yes | None |
| `sorted(lst)` | No | New sorted list |
| `lst.reverse()` | Yes | None |
| `reversed(lst)` | No | Iterator |
| `lst.append(x)` | Yes | None |
| `lst + [x]` | No | New list |

---

## The Copy Trap

```python
a = [1, 2, 3]
b = a            # b is NOT a copy — same list object

b.append(4)
print(a)   # [1, 2, 3, 4] ← a was also modified!

# Fix:
b = a.copy()   # or a[:] or list(a)
```

For lists containing mutable objects (nested lists, dicts), use `copy.deepcopy()`.

---

## Sorting with Keys

```python
# Sort strings by length
words.sort(key=len)

# Sort dicts by a field
models.sort(key=lambda m: m["accuracy"], reverse=True)

# Stable sort: maintains relative order of equal elements
```

Python's `sort()` uses **Timsort** — O(n log n) worst case, O(n) for nearly-sorted data.

---

## `list()` Constructor

Converts any iterable to a list:
```python
list(range(5))         # [0, 1, 2, 3, 4]
list("hello")          # ['h', 'e', 'l', 'l', 'o']
list({"a": 1, "b": 2}) # ['a', 'b']  ← only keys!
```

---

## Real-World Analogy

A list is like a **dataset CSV file**:
- Each row/sample is an element
- You can slice to get a subset (train/val/test split)
- You sort to rank models
- You append new data when it arrives
- You never want to accidentally mutate the original

---

## Interview Quick-Fire

1. **What is the difference between `list.sort()` and `sorted(list)`?**
   → `.sort()` modifies in place and returns `None`; `sorted()` returns a new sorted list without modifying the original.

2. **What is the time complexity of `x in my_list`?**
   → O(n) — Python scans linearly. For fast lookups, use a `set` (O(1)).

3. **What does `a = b` do when b is a list?**
   → Creates a second reference to the same list. Modifying via `a` also changes `b`. Use `.copy()` or `[:]` for a shallow copy.

4. **What is the difference between `append` and `extend`?**
   → `append(x)` adds `x` as a single element; `extend(iterable)` adds each element of the iterable individually.

5. **How do you reverse a list without modifying the original?**
   → `lst[::-1]` (slice) or `list(reversed(lst))`.
