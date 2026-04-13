# Day 26 Exercises — Virtual Environments & Dependency Management

Estimated time: 30–45 minutes

---

## Exercise 1 — Environment Inspector

Write a script `inspect_env.py` that prints a formatted report about the current Python environment:

```
=== Python Environment Report ===
Python:          3.11.6
Executable:      /Users/you/.venv/bin/python3
In Virtual Env:  YES
Venv Path:       /Users/you/project/.venv

=== Installed Packages (20 found) ===
Package          Version    License (if available)
----------------------------------------------
fastapi          0.109.0
numpy            1.26.2
...
```

Use: `sys`, `os`, `importlib.metadata`

---

## Exercise 2 — Requirements Validator

Write `validate_requirements(req_file: str)` that:
1. Reads a `requirements.txt` file
2. For each frozen requirement (`package==version`):
   - Check if it's currently installed
   - If installed: compare versions (match / mismatch)
   - If not installed: mark as missing
3. Returns `{"ok": [...], "mismatch": [...], "missing": [...]}`
4. Prints a color-coded or ASCII summary

---

## Exercise 3 — Dependency Tree

Write a function `show_deps(package_name: str)` using `importlib.metadata` that:
1. Gets the package's metadata
2. Shows its `Requires-Dist` (direct dependencies)
3. Shows each dependency's version that is currently installed
4. For each dependency, shows its `Requires-Dist` one level deep (like `pip show`)

```
transformers 4.36.0
├── huggingface-hub >=0.19.3 → installed: 0.20.1
├── numpy >=1.17 → installed: 1.26.2
├── tokenizers >=0.14 → installed: 0.15.0
│   └── huggingface-hub >=0.16.4 → installed: 0.20.1
└── ...
```

---

## Exercise 4 — `.env` File Manager

Write an `EnvManager` class that:
1. `load(path=".env")` — reads `.env` file and stores key-value pairs
2. `get(key, default=None)` — gets a value
3. `require(*keys)` — raises `RuntimeError` if any key is missing
4. `generate_example(path)` — writes a `.env.example` with keys but empty values
5. `validate_schema(schema)` — where schema is `{key: type}`:
   - Validates types (cast each value to its type)
   - Returns dict of typed values
   - Raises `EnvValidationError` with all issues at once (not just the first)

---

## Exercise 5 — Package Compatibility Checker

Write `check_compatibility(package_a, package_b)` that:
1. Gets the installed version of both packages
2. Gets `Requires-Dist` of each
3. Checks if either package requires a version of the other that conflicts

For example:
```python
check_compatibility("transformers", "tokenizers")
# Output:
# transformers 4.36.0 requires tokenizers>=0.14
# tokenizers 0.15.0 is installed ✓ (compatible)
```

---

## Stretch Challenge — Project Bootstrapper

Write a `bootstrap_project(project_name, template="ml")` function that:
1. Creates the standard project directory structure
2. Writes a starter `pyproject.toml` with common dependencies
3. Writes a `.env.example` with common AI project env vars
4. Writes a `.gitignore` with Python/AI patterns
5. Writes a `README.md` with project name and basic setup instructions

Templates:
- `"ml"` → torch, transformers, datasets deps
- `"api"` → fastapi, uvicorn, pydantic deps
- `"data"` → pandas, numpy, matplotlib deps

Run it and verify the directory structure was created correctly.
