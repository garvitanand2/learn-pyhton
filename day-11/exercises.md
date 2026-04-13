# Day 11 Exercises — Strings

Estimated time: 25–35 minutes

---

## Exercise 1 — Prompt Template Engine

Build a simple template renderer:

```python
def render_template(template: str, **variables) -> str:
    ...
```

Templates use `{{variable_name}}` syntax. Replace each placeholder with
the provided value. If a variable is missing, leave it as `{{variable_name}}`.

```python
template = """
System: You are a {{role}}.
User: {{instruction}}
Context: {{context}}
"""

result = render_template(
    template,
    role="helpful AI assistant",
    instruction="Summarize the following text in 3 bullet points."
    # context is missing → remain as {{context}}
)
print(result)
```

---

## Exercise 2 — Token Counter

Write `count_tokens(text, method="word")`:
- `method="word"` → split on whitespace
- `method="char"` → count characters (excluding spaces)
- `method="sentence"` → split on `.!?`

```python
text = "Large Language Models are transforming AI. They learn from text. Performance improves!"
print(count_tokens(text, "word"))      # ~12
print(count_tokens(text, "char"))      # ~70
print(count_tokens(text, "sentence"))  # 3
```

---

## Exercise 3 — String Cleaner

Write a function `clean_model_output(text)` that:
1. Removes leading/trailing whitespace
2. Removes repeated spaces (collapse to single space)
3. Removes common artifacts: `"[INST]"`, `"[/INST]"`, `"<s>"`, `"</s>"`
4. Removes lines that are purely whitespace
5. Ensures sentences end with proper punctuation

Test with:
```python
raw = """  [INST] Please summarize:   [/INST]
<s>The model   predicted  that     climate  change  is  real.
</s>
   
This is a follow-up sentence
"""
```

---

## Exercise 4 — Regex Patterns Practice

Using the `re` module, write functions to:
1. `extract_emails(text)` — find all email addresses
2. `extract_numbers(text)` — find all numbers (int or float)
3. `mask_pii(text)` — replace email addresses with `[EMAIL]` and phone numbers with `[PHONE]`

```python
text = """
Contact alice@example.com or bob.smith@ai.org.
Call us at 555-123-4567 or +1 (800) 999-0000.
The score was 97.5 and there were 1234 samples.
"""
```

---

## Exercise 5 — N-gram Generator

An n-gram is a contiguous sequence of N tokens. Used in NLP for language modeling.

```python
def ngrams(text: str, n: int) -> list:
    ...

tokens = "the quick brown fox jumps over the lazy dog".split()
print(ngrams(tokens, 2))
# [['the', 'quick'], ['quick', 'brown'], ...]

print(ngrams(tokens, 3))
# [['the', 'quick', 'brown'], ...]
```

Then write a function `ngram_frequency(text, n)` that returns a frequency dict
of all n-grams. Print the top 3 most common bigrams in a paragraph of your choice.

---

## Stretch Challenge — Levenshtein Distance (Edit Distance)

Implement `edit_distance(s1, s2)` — the minimum number of single-character
insertions, deletions, or substitutions to transform s1 into s2.

```python
print(edit_distance("cat", "car"))         # 1 (t → r)
print(edit_distance("kitten", "sitting"))  # 3
print(edit_distance("", "hello"))          # 5
```

Use dynamic programming (2D list). This is used in:
- Spell checkers
- Fuzzy string matching
- DNA sequence alignment
- Typo-tolerant search

What is the time and space complexity?
