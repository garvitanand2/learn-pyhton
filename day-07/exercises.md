# Day 7 Exercises — Week 1 Mini Project Extensions

Estimated time: 45–60 minutes (mini project day — go deeper!)

---

## Exercise 1 — Add a Comparison Mode

Extend `ModelMatcher` with a `compare` command:
- Ask the user for two model names
- Display their cards side by side
- Print which one wins on: cost, speed, max context
- Print a recommendation with a reason

Hint: Look up both models by name from `MODEL_REGISTRY` using a loop.

---

## Exercise 2 — Cost Calculator

Add a `calculate` command that:
1. Asks for a model name
2. Asks for: number of input tokens, number of output tokens
   (output tokens typically cost 2× input for some models — add a `cost_multiplier` field)
3. Calculates total cost for a conversation
4. Tells how many such conversations you can have for $1, $10, $100

---

## Exercise 3 — Add Input Validation Layer

Improve the current `run_cli()` to handle all input errors gracefully:
- Non-numeric input where a number is expected
- Empty input for required fields
- Cost value outside `[0.0, 1.0]` range
- Token count above 200,000

None of these should crash the program — they should print a helpful message
and ask again. Research Python's `try/except` briefly (preview of Day 17).

---

## Exercise 4 — Statistics Summary

Add a `stats` command that processes `session_history` and prints:
- Total searches made
- Most common task searched
- Average results per search
- Most recommended model

Use only loops, dictionaries, and the functions you already know.

---

## Exercise 5 — Filter by Provider

Add a `--provider` filter option in the search flow:
- Ask: "Filter by provider? (openai/anthropic/meta/mistral/Enter to skip)"
- Only show models from that provider
- Update `match_models()` to accept a `provider` keyword argument

---

## Stretch Challenge — Rebuild as a "Score-Based" Ranker

Instead of binary match (model supports task or not), give each model a **score**:

```python
def score_model(model, task, token_count, budget=None):
    score = 0

    # Task match
    if task in model["strengths"]:
        score += 50

    # Token fit
    if token_count <= model["max_tokens"]:
        score += 20

    # Budget fit
    if budget and model["cost_per_1k"] <= budget:
        score += 20

    # Speed bonus
    speed_bonus = {"fast": 10, "medium": 5, "slow": 0}
    score += speed_bonus.get(model["speed"], 0)

    return score
```

Sort all models by score descending and display the top 3 with their scores.

This is exactly how **retrieval ranking** and **recommendation systems** work.
