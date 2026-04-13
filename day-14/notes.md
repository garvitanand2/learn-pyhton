# Day 14 Notes — Week 2 Mini Project Reflection

## Project: DataSight Dataset Profiler

### What You Built

A data analysis pipeline that:
1. Profiles a text classification dataset
2. Computes label distribution and class balance score
3. Calculates text length statistics
4. Builds vocabulary and per-label token frequencies
5. Detects data quality issues (duplicates, short texts, missing labels)
6. Produces a stratified train/val/test split
7. Prints a structured profiling report

---

## Week 2 Concepts Applied

| Concept | Where Used |
|---------|-----------|
| Lists | Dataset storage, token lists, split results |
| Tuples | `Counter.most_common()` returns `[(word, count), ...]` |
| Sets | `set(all_tokens)` for unique vocabulary |
| Dicts | Profile results, issue records, split output |
| `Counter` | Token frequencies, label counts, source counts |
| `defaultdict` | Grouping records by label |
| List comprehensions | Tokenization, filtering, stat extraction |
| Dict comprehensions | Per-label top tokens |
| Nested structures | `profile` dict with nested `text_stats`, `vocabulary` |
| String methods | `.lower()`, `.split()`, `.strip()` in tokenizer |
| Regex | `re.sub()` for cleaning, `re.findall()` for sentence count |

---

## Key Engineering Patterns

### Single Responsibility Functions

Each function does ONE thing:
- `tokenize()` → str → list of clean tokens
- `compute_text_stats()` → str → stats dict
- `profile_dataset()` → list → complete profile dict
- `detect_issues()` → list → list of issue dicts
- `print_report()` → profile, issues, splits → None (side effect)

### Data-Driven Output

The report is generated from the `profile` dict — not hardcoded strings.
Change the dataset → the report automatically reflects the change.

### Pure vs Impure Functions

- `profile_dataset()`, `detect_issues()`, `split_dataset()` → pure (no side effects)
- `print_report()` → impure (side effect: prints to stdout)
- Keeping impure functions at the "edges" makes the core logic testable.

---

## Possible Extensions

- **Day 16** (File Handling): Save the profile to `report.json`
- **Day 17** (Exceptions): Handle missing fields, wrong types
- **Day 18** (OOP): `DataSight` class with state
- **Day 29** (Testing): Write pytest tests for `profile_dataset`

---

## Interview Reflection

**Q: You have a large text dataset. How would you quickly profile it before training?**

Key things to check:
1. **Class balance** — imbalanced classes hurt model performance
2. **Text length distribution** — min/max/avg tokens determines context window needs
3. **Vocabulary coverage** — OOV rate on test set
4. **Data quality** — duplicates, mislabeled examples, empty strings
5. **Source distribution** — if data comes from multiple sources, check for domain shift

This is exactly what `DataSight` does.
