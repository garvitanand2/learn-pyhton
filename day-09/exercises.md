# Day 9 Exercises — Tuples & Sets

Estimated time: 25–35 minutes

---

## Exercise 1 — Coordinate System

Represent 2D points as tuples. Write functions:
1. `distance(p1, p2)` — Euclidean distance between two 2D points
2. `midpoint(p1, p2)` — midpoint tuple
3. `translate(point, dx, dy)` — return new point shifted by (dx, dy)
4. `scale(point, factor)` — multiply both coordinates by factor

Since tuples are immutable, all functions should return **new tuples**.

```python
p1 = (0.0, 0.0)
p2 = (3.0, 4.0)
print(distance(p1, p2))    # 5.0
print(midpoint(p1, p2))    # (1.5, 2.0)
print(translate(p2, 1, -1)) # (4.0, 3.0)
```

---

## Exercise 2 — Vocabulary Coverage Analysis

You have a training vocabulary and a test corpus. Using sets:

```python
train_vocab = {
    "the", "quick", "brown", "fox", "jumps", "over",
    "lazy", "dog", "a", "cat", "sat", "on", "mat"
}

test_sentences = [
    "the quick fox ran fast",
    "a cat jumped over the fence",
    "the brown dog sat quietly",
    "machine learning transforms data",
]
```

For each sentence:
1. Tokenize into a set of words
2. Find OOV (out-of-vocabulary) words: in test but not train
3. Compute coverage: % of test words that are in vocab

Print a summary table.

---

## Exercise 3 — Named Tuple Data Class

Create a `namedtuple` called `ModelBenchmark` with fields:
`name`, `task`, `accuracy`, `latency_ms`, `cost_per_1k`

Create 5 benchmark records. Then:
1. Find the model with the highest accuracy
2. Find the fastest model (lowest latency)
3. Find the cheapest model (lowest cost)
4. Find models that score >= 0.85 accuracy AND <= 100ms latency

(Practice indexing into named fields vs positional)

---

## Exercise 4 — Set Operations on User Tags

A recommendation system tags users with interests:

```python
users = {
    "alice": {"ml", "python", "data", "nlp"},
    "bob":   {"python", "web", "api", "docker"},
    "carol": {"ml", "statistics", "r", "data"},
    "dave":  {"nlp", "transformers", "ml", "python"},
}
```

Write functions to:
1. `common_interests(u1, u2)` — interests shared by two users
2. `unique_to_user(user, others)` — interests only this user has
3. `recommend_users(target_user, all_users)` — return other users sorted by number of shared interests
4. Find all unique tags across ALL users

---

## Exercise 5 — Deduplication with Order Preservation

Implement `unique_ordered(items)` using a **set for O(1) lookups** but preserving insertion order:

```python
predictions = ["cat", "dog", "cat", "bird", "dog", "cat", "fish"]
print(unique_ordered(predictions))
# ['cat', 'dog', 'bird', 'fish']
```

Compare this approach to using `list(set(predictions))` — what's different?

---

## Stretch Challenge — Intersection of Multiple Sets

Given N sets, find elements that appear in **at least K** of them:

```python
tag_sets = [
    {"ml", "python", "nlp"},
    {"ml", "data", "python"},
    {"nlp", "transformers", "ml"},
    {"python", "api", "data"},
]

print(appears_in_at_least(tag_sets, k=3))
# {"ml", "python"}  ← appear in 3+ sets
```

This is used in ensemble learning and voting classifiers.
