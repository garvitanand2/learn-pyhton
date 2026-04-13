# Day 12 Exercises — List Comprehensions

Estimated time: 25–35 minutes

---

## Exercise 1 — Data Pipeline One-Liners

Convert each of the following loops into a comprehension:

**a)** Square all odd numbers from 1 to 20:
```python
# Loop version:
result = []
for n in range(1, 21):
    if n % 2 != 0:
        result.append(n ** 2)
```

**b)** Extract words longer than 4 characters from a sentence, lowercased:
```python
sentence = "Large Language Models are Transforming Natural Language Processing"
```

**c)** Build a dict of `{model_name: cost_in_cents}` (multiply cost by 100):
```python
models = [("gpt-4", 0.03), ("bert", 0.001), ("llama", 0.0009)]
```

**d)** Flatten this list of lists:
```python
batches = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
```

---

## Exercise 2 — Score Bucketing

Given a list of scores, create a new list where each score is replaced
by its tier: `"A" (>=90)`, `"B" (>=75)`, `"C" (>=60)`, `"F" (<60)`.

```python
scores = [92, 68, 45, 88, 76, 55, 100, 61, 72, 30]
# Expected: ['A', 'C', 'F', 'A', 'B', 'F', 'A', 'C', 'C', 'F']
```

Use a ternary in the comprehension expression.

---

## Exercise 3 — Matrix Comprehensions

Using only comprehensions (no NumPy):

1. Create the identity matrix of size n×n:
   ```python
   identity(3)
   # [[1, 0, 0],
   #  [0, 1, 0],
   #  [0, 0, 1]]
   ```

2. Multiply two matrices (matrix multiplication, not element-wise):
   ```python
   A = [[1, 2], [3, 4]]
   B = [[5, 6], [7, 8]]
   matmul(A, B)
   # [[19, 22], [43, 50]]
   ```

---

## Exercise 4 — Generator Efficiency Comparison

Write two versions of a function that computes the sum of squares of all
even numbers from 1 to N:

1. Using a list comprehension (stores all values)
2. Using a generator expression (lazy)

For N = 10,000,000:
- Measure time with `time.time()`
- Measure memory with `sys.getsizeof()`
- Print the comparison

Which is better? When would you pick each?

---

## Exercise 5 — Text Preprocessing Pipeline

Build a complete text preprocessing pipeline using comprehensions:

```python
documents = [
    "  Hello, World! This is AI.  ",
    "NATURAL language PROCESSING uses ML.",
    "stop words: the a an is are",
    "  99 problems   but   code   ain't   one  ",
]

stop_words = {"the", "a", "an", "is", "are", "but", "this"}
```

Using comprehensions, produce for each document:
1. A cleaned string (stripped, lowercased)
2. A list of tokens (split, strip punctuation)
3. A list of tokens with stop words removed
4. The final string re-joined

All in a single pipeline expression if possible.

---

## Stretch Challenge — Sieve of Eratosthenes

Generate all prime numbers up to N using the sieve algorithm, using
comprehensions where possible:

```python
def primes_up_to(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            # mark multiples using a comprehension assignment trick
            ...
    return [i for i in range(2, n + 1) if sieve[i]]

print(primes_up_to(50))
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

This is used in hash functions and cryptography — foundational to secure AI systems.
