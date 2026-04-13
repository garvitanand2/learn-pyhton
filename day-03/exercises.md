# Day 3 Exercises — Conditional Statements

Estimated time: 20–30 minutes

---

## Exercise 1 — Model Confidence Router

Given a confidence score, classify the model's output into one of four tiers:

| Range          | Tier           | Action                          |
|----------------|----------------|---------------------------------|
| >= 0.95        | "CERTAIN"      | Auto-approve and publish        |
| 0.80 – 0.94    | "CONFIDENT"    | Approve with logging            |
| 0.60 – 0.79    | "UNCERTAIN"    | Flag for human review           |
| < 0.60         | "UNCONFIDENT"  | Reject and request re-inference |

Test with scores: `0.97`, `0.82`, `0.65`, `0.42`

---

## Exercise 2 — Token Budget Guard

Write a function `check_token_budget(prompt_tokens, max_tokens)` that:
1. Raises a printed warning if `prompt_tokens` uses more than 80% of the budget
2. Raises a printed error if `prompt_tokens >= max_tokens`
3. Returns `"OK"` if within safe limits

Use guard-clause style (early checks at the top, happy path at the end).

Test with:
- `check_token_budget(3400, 4096)` → warning
- `check_token_budget(4096, 4096)` → error
- `check_token_budget(1000, 4096)` → OK

---

## Exercise 3 — Multi-Condition Validator

A dataset entry is valid only if ALL of the following are true:
- `text` is a non-empty string
- `label` is in `["positive", "negative", "neutral"]`
- `confidence` is between 0.0 and 1.0 (inclusive)
- `word_count` is a positive integer

Write a validator that checks each condition individually and prints which ones fail.

Test data:
```python
entry_1 = {"text": "Great product!", "label": "positive", "confidence": 0.95, "word_count": 2}
entry_2 = {"text": "", "label": "happy", "confidence": 1.2, "word_count": -1}
```

---

## Exercise 4 — FizzBuzz (AI Edition)

For numbers 1 to 30:
- Print "Batch" if divisible by 3 (batch processing step)
- Print "Epoch" if divisible by 5 (epoch completed)
- Print "Checkpoint" if divisible by both 3 and 5 (save checkpoint!)
- Otherwise print the number

Hint: Check the combined condition FIRST.

---

## Exercise 5 — Request Router with `match`

(Requires Python 3.10+)

Build a `route_model_request(task, token_count)` function using `match`:

Tasks and their model mappings:
- `"embedding"`: always use `"text-embedding-ada-002"`
- `"chat"` with token_count > 16000: use `"gpt-4-32k"`
- `"chat"` otherwise: use `"gpt-3.5-turbo"`
- `"image"`: use `"dall-e-3"`
- `"transcription"`: use `"whisper-1"`
- any other task: return `"Error: unknown task"`

Test:
```python
print(route_model_request("chat", 5000))       # gpt-3.5-turbo
print(route_model_request("chat", 20000))      # gpt-4-32k
print(route_model_request("image", 0))         # dall-e-3
print(route_model_request("translate", 100))   # Error: unknown task
```

---

## Stretch Challenge — Grade Classifier with `any()` / `all()`

A student needs to pass ALL of the following tests to be certified in the AI track:
- Python basics score >= 70
- Data structures score >= 75
- OOP score >= 70
- Algorithms score >= 65

```python
students = [
    {"name": "Alice", "scores": {"python": 85, "ds": 78, "oop": 72, "algo": 68}},
    {"name": "Bob",   "scores": {"python": 65, "ds": 80, "oop": 75, "algo": 70}},
    {"name": "Carol", "scores": {"python": 92, "ds": 88, "oop": 85, "algo": 79}},
]
```

For each student, print:
- Whether they are CERTIFIED (all passing)
- Which subjects they failed (if any)

Use `all()` for the pass check and a comprehension to find failing subjects.
