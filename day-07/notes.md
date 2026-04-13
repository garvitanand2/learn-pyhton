# Day 7 Notes — Week 1 Mini Project Reflection

## Project: ModelMatcher CLI

### What You Built

A command-line tool that:
1. Accepts a task description from the user
2. Filters registered AI models by task, cost, and speed preferences
3. Displays formatted model cards with cost estimates
4. Tracks session history
5. Loops until the user quits

---

## Week 1 Concepts Applied

| Concept       | Where Used                                               |
|---------------|----------------------------------------------------------|
| Variables     | `token_count`, `max_cost`, `session_history`             |
| Data types    | `str`, `float`, `int`, `bool`, `list`, `dict`, `None`    |
| Operators     | Cost calculation, comparisons, `not in`, `index.isdigit()`|
| Conditionals  | Command routing, filter validation, guard clauses        |
| Loops         | Main `while` loop, model search loop, `enumerate()`      |
| Functions     | Each feature is a function with single responsibility    |
| *args/**kwargs| (Used indirectly via `sort(key=lambda...)`; build on Day 22)|
| Docstrings    | Every function documented                                |
| f-strings     | All output formatting                                    |

---

## Architecture Patterns Learned

### Separation of Concerns

The project is split into clear layers:
- **Data layer** — `MODEL_REGISTRY` (the data)
- **Logic layer** — `match_models()`, `estimate_cost()` (pure functions)
- **Presentation layer** — `display_model_card()`, `print_banner()` (UI)
- **Controller** — `run_cli()` (orchestrates everything)

This is the same pattern used in production AI systems.

### Guard Clauses

```python
if not validate_task(task_input):
    print("Invalid task")
    continue     # skip the rest of the loop body
```

Checks bad input early → keeps the happy path flat and readable.

### Data-Driven Design

The logic (`match_models`) doesn't care about specific model names.
Add a new model to `MODEL_REGISTRY` → it automatically appears in searches.
**This is the right way to build configurable systems.**

---

## Code Quality Checklist

- [ ] Functions have single responsibility
- [ ] No magic numbers (use named constants)
- [ ] Input validated before use
- [ ] Docstrings on all functions
- [ ] Consistent naming: `snake_case` for functions/variables, `UPPER_CASE` for constants
- [ ] No deep nesting (max 2–3 levels)
- [ ] `if __name__ == "__main__":` for entry point

---

## Possible Extensions

1. **Persistence** — save session history to a JSON file (Day 16 topic)
2. **Error handling** — handle invalid inputs more robustly (Day 17)
3. **OOP refactor** — make `Model` a class (Day 18)
4. **CLI framework** — use `argparse` instead of raw `input()` (Day 28)
5. **Config file** — load `MODEL_REGISTRY` from a JSON/YAML file (Day 25)

---

## Interview Reflection

**Q: How would you design a model routing system?**

This project is a simplified version. In production:
1. A request comes in with task type and constraints
2. A registry maps capabilities to models
3. A router applies business rules (cost, speed, context length)
4. The cheapest/fastest suitable model is selected
5. Fallback logic handles unavailability

This is exactly how orchestration layers in LLM applications work.
