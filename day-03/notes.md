# Day 3 Notes — Conditional Statements

## What & Why

Conditionals let your program **make decisions** — executing different code
based on the state of data. Every AI system is full of branching logic:
"Is confidence above threshold?" "Is this a valid task type?" "Did the API return an error?"

---

## if / elif / else

```python
if condition_1:
    # runs if condition_1 is True
elif condition_2:
    # runs if condition_1 is False AND condition_2 is True
elif condition_3:
    # can have as many elif as needed
else:
    # runs if no condition above was True
```

Rules:
- Only **one block** executes — the first matching one
- `else` is optional
- `elif` is short for "else if"

---

## Truthiness (Automatic Boolean Evaluation)

Python evaluates most values as `True` or `False` in an `if` context — no explicit comparison needed.

| Value                  | Truthiness |
|------------------------|------------|
| `0`, `0.0`, `0j`       | False      |
| `""`, `[]`, `{}`, `()` | False      |
| `None`                 | False      |
| `False`                | False      |
| Everything else        | True       |

```python
# Avoid:  if len(my_list) > 0:
# Prefer: if my_list:

# Avoid:  if result == None:
# Prefer: if result is None:   (None is a singleton)
```

---

## Ternary Operator (Conditional Expression)

```python
label = "Pass" if score >= 0.70 else "Fail"
```

One-liner — great for simple assignments, bad for complex logic.
**Never nest ternaries more than once** — readability drops sharply.

---

## `in` Membership Operator

```python
if task in ["classification", "summarization"]:
    ...

if token in stop_tokens:
    break

if key in my_dict:
    value = my_dict[key]
```

Works on: `str`, `list`, `tuple`, `set`, `dict` (checks **keys**).
For sets and dicts, `in` is **O(1)** — constant time. For lists, it's **O(n)**.

---

## `any()` and `all()`

Cleaner alternatives to writing `or`/`and` chains over iterables:

```python
# True if ANY element satisfies the condition
any(score >= 0.90 for score in scores)

# True if ALL elements satisfy the condition
all(score >= 0.70 for score in scores)
```

Use these to write expressive, readable validation logic.

---

## `match` Statement (Python 3.10+)

Structural pattern matching — more powerful than simple `if/elif` for
routing and dispatch logic.

```python
match response_type:
    case "text":
        handle_text()
    case "error":
        handle_error()
    case _:            # default/wildcard
        handle_unknown()
```

Supports **guards** (extra conditions), **OR patterns** (`case 400 | 401`),
and complex structural matching on objects.

---

## Guard Clauses Pattern (Early Return)

Instead of deep nesting, use early returns to handle edge cases first:

```python
# Nested (hard to read):
def process(data):
    if data is not None:
        if len(data) > 0:
            if is_valid(data):
                return compute(data)

# Guard-clause style (clean):
def process(data):
    if data is None:
        return None
    if len(data) == 0:
        return []
    if not is_valid(data):
        raise ValueError("Invalid data")
    return compute(data)
```

---

## Real-World Analogy

Think of conditionals as **routing rules** in a microservices system:
- If the request is a classification task → send to BERT
- If the token count is > 8k → upgrade to GPT-4
- If confidence < 0.5 → flag for human review
- Otherwise → proceed with default model

Your code IS the decision-making logic of the system.

---

## Interview Quick-Fire

1. **What is truthy/falsy in Python?** → Values that evaluate to True/False in boolean context. Falsy: `0`, `""`, `[]`, `{}`, `None`, `False`.
2. **Difference between `if x == None` and `if x is None`?** → Always use `is None`. `None` is a singleton; `is` checks identity. `==` calls `__eq__` which could be overridden.
3. **What is short-circuit evaluation in logical operators?** → `and` stops at first falsy value; `or` stops at first truthy value. The remaining expressions are NOT evaluated.
4. **When would you use `match` over `if/elif`?** → When dispatching on a fixed set of cases (command routing, response types, state machines). More readable and extensible than long elif chains.
5. **What does `any([])` return?** → `False`. What does `all([])` return? → `True` (vacuously true, no conditions to violate).
