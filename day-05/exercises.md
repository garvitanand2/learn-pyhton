# Day 5 Exercises — Functions (Basics)

Estimated time: 25–35 minutes

---

## Exercise 1 — Metric Suite

Write three separate functions (each as a pure function):

1. `compute_mae(actual, predicted)` → Mean Absolute Error
2. `compute_mse(actual, predicted)` → Mean Squared Error
3. `compute_rmse(actual, predicted)` → RMSE (reuse `compute_mse`)

Then write a fourth function `compute_all_metrics(actual, predicted)` that calls
all three and returns a dictionary:

```python
{"mae": 0.35, "mse": 0.18, "rmse": 0.42}
```

Test with:
```python
actual    = [3.0, 5.0, 2.5, 7.0, 4.0]
predicted = [2.8, 5.3, 2.0, 6.5, 4.2]
```

---

## Exercise 2 — Configurable Tokenizer

Write a function `tokenize(text, lowercase=True, remove_punct=True, split_on=" ")`:
- If `lowercase` is True, convert text to lowercase
- If `remove_punct` is True, strip punctuation from each token
- Split on the given character

Return a list of non-empty tokens.

Test:
```python
tokenize("Hello, World! How are YOU?")
# ['hello', 'world', 'how', 'are', 'you']

tokenize("Hello, World!", lowercase=False, remove_punct=False)
# ['Hello,', 'World!']
```

---

## Exercise 3 — Pipeline Builder

Create a function `build_pipeline(steps)` that takes a list of functions
and returns a new function that applies them in sequence:

```python
def build_pipeline(steps):
    ...

def lowercase(text): return text.lower()
def strip_spaces(text): return text.strip()
def remove_exclamation(text): return text.replace("!", "")

pipeline = build_pipeline([lowercase, strip_spaces, remove_exclamation])
result = pipeline("  HELLO WORLD!  ")
print(result)   # "hello world"
```

This is the **functional pipeline pattern** — core to many AI frameworks.

---

## Exercise 4 — Scope Puzzle

Look at this code — predict the output before running it:

```python
x = 10
y = 20

def outer():
    x = 100
    def inner():
        y = 200
        print(f"inner: x={x}, y={y}")
    inner()
    print(f"outer: x={x}, y={y}")

outer()
print(f"global: x={x}, y={y}")
```

Write down your predictions. Then run it and explain each output.

**Bonus**: Modify `inner()` to use `nonlocal x` and predict the new output.

---

## Exercise 5 — Mutable Default Bug Hunter

Consider this buggy function:

```python
def collect_predictions(text, results=[]):
    results.append(text)
    return results

r1 = collect_predictions("cat")
r2 = collect_predictions("dog")
print(r1)   # What do you expect? What actually happens?
print(r2)
```

1. Run the code and observe the bug
2. Explain WHY it happens
3. Fix it correctly

---

## Stretch Challenge — Recursive Factorial + Memoization

1. Write `factorial(n)` recursively
2. Add a manual cache using a dictionary to avoid recomputing values:

```python
cache = {}

def factorial(n, cache=None):
    if cache is None:
        cache = {}
    ...
```

3. Time both versions for n=30 using `time.time()` and compare.
4. **Note**: Python's built-in `functools.lru_cache` does this automatically
   — you'll learn that on Day 22.
