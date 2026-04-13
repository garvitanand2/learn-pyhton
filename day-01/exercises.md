# Day 1 Exercises — Variables & Data Types

Estimated time: 20–30 minutes

---

## Exercise 1 — AI Model Config

Create variables to describe an AI model configuration.
Store and print the following:
- Model name (string)
- Number of parameters in billions (float)
- Context window size in tokens (int)
- Whether it supports vision (bool)
- Fine-tune checkpoint path (set to None if not fine-tuned)

Expected output (example):
```
Model     : Gemini-Pro
Params    : 7.0B
Context   : 8192 tokens
Vision    : True
Checkpoint: None
```

---

## Exercise 2 — Type Conversion Pipeline

You receive raw data from a config file as strings. Convert them to the correct types:

```python
raw_data = {
    "learning_rate": "0.0003",
    "epochs": "50",
    "model_name": "transformer_v2",
    "use_dropout": "True",
    "dropout_rate": "0.2"
}
```

- Convert `learning_rate` and `dropout_rate` to `float`
- Convert `epochs` to `int`
- Convert `use_dropout` to `bool` (hint: `"True"` as a string is always truthy — think about this!)
- Print each converted value with its type

**Bonus**: What's wrong with `bool("False")`? Fix it correctly.

---

## Exercise 3 — Token Budget Calculator

An LLM has a context window of 4096 tokens.
- System prompt uses 150 tokens
- User message uses 320 tokens
- Model response is allowed the rest

Calculate and print:
1. Tokens used so far (system + user)
2. Tokens remaining for the response
3. Percentage of context window used (as a float, rounded to 2 decimal places)
4. Whether the conversation is under 50% context usage (bool)

---

## Exercise 4 — String Exploration

Given the string:
```python
text = "Large Language Models are transforming the AI industry."
```

Without importing any library, find:
1. Total number of characters (including spaces)
2. Number of words (hint: `.split()`)
3. Whether "AI" appears in the text (bool)
4. The first 5 characters
5. The text in UPPERCASE

---

## Exercise 5 — Identity Puzzle (Interview-Focused)

Predict the output of each line **before** running it. Then verify:

```python
a = 256
b = 256
print(a is b)   # ?

c = 257
d = 257
print(c is d)   # ?

x = None
y = None
print(x is y)   # ?

p = "hello"
q = "hello"
print(p is q)   # ?  (string interning — research this!)
```

Explain in a comment WHY each result is what it is.

---

## Stretch Challenge

Write a short script that:
1. Asks the user (via `input()`) for a confidence score between 0 and 1
2. Converts it to float
3. Prints whether the model is "Confident" (>= 0.8), "Uncertain" (0.5–0.8), or "Not confident" (< 0.5)
4. Prints the confidence as a percentage (e.g. 97.00%)

(You'll need `if/elif/else` which is Day 3 — try it now or revisit after Day 3)
