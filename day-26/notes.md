# Day 26 Notes — Virtual Environments & Dependency Management

## Why Virtual Environments?

```
System Python
├── numpy 1.24 (Project A needs this)
└── numpy 2.0  (Project B needs this)
        ↑
   CONFLICT — can't have both!

With virtual environments:
.venv-project-a/
└── numpy 1.24

.venv-project-b/
└── numpy 2.0

No conflict — each project has its own isolated environment.
```

---

## Creating and Using a Virtual Environment

```bash
# Create (one time per project)
python -m venv .venv           # standard name: .venv

# Activate
source .venv/bin/activate      # Mac/Linux
.\.venv\Scripts\activate       # Windows PowerShell

# Your prompt changes: (.venv) user@machine:~/project$

# Install packages
pip install torch transformers fastapi

# Deactivate
deactivate
```

---

## `requirements.txt` — Pinned Dependencies

```bash
# Generate after installing everything you need:
pip freeze > requirements.txt

# Recreate environment identically on any machine:
pip install -r requirements.txt
```

```
# requirements.txt (exact versions for reproducibility)
torch==2.1.0
transformers==4.36.0
numpy==1.26.2
```

**Tip:** Maintain two files:
- `requirements.txt` — production (exact pinned versions)
- `requirements-dev.txt` — development tools (pytest, black, ruff)

---

## `pyproject.toml` — Modern Package Config

The modern standard (replaces setup.py):

```toml
[project]
name = "my-package"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "torch>=2.0",          # lower-bound only (flexible)
    "transformers>=4.30",
]

[project.optional-dependencies]
dev = ["pytest", "black", "ruff"]
gpu = ["torch[cuda12]"]

# Install all dev deps:
# pip install -e ".[dev]"
```

---

## Version Specifiers

| Specifier | Meaning |
|-----------|---------|
| `==1.2.3` | Exactly 1.2.3 |
| `>=1.2.3` | 1.2.3 or higher |
| `~=1.2.3` | Compatible: >=1.2.3, <1.3 |
| `!=1.2.3` | Anything except 1.2.3 |
| `>=1.2,<2.0` | Range |

---

## Environment Variables & Secrets

**Never hardcode secrets in source code.** Use environment variables.

```bash
# Set in shell:
export OPENAI_API_KEY="sk-..."

# Load in Python:
import os
api_key = os.environ.get("OPENAI_API_KEY")
```

**With `python-dotenv`:**
```python
# pip install python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()   # reads .env file → sets environment variables
api_key = os.getenv("OPENAI_API_KEY")
```

**.env file example:**
```
OPENAI_API_KEY=sk-project-abc123
ENVIRONMENT=development
DATABASE_URL=sqlite:///./dev.db
```

**Always add `.env` to `.gitignore`!**

---

## Project Structure Best Practice

```
my-ai-project/
├── .venv/              ← never commit
├── .env                ← never commit (add to .gitignore)
├── .env.example        ← commit (template, empty values)
├── .gitignore
├── pyproject.toml      ← package config
├── requirements.txt    ← pinned production deps
├── requirements-dev.txt ← dev tools
├── README.md
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── config.py
│       ├── models.py
│       └── utils.py
├── tests/
│   └── test_models.py
└── notebooks/
    └── exploration.ipynb
```

---

## conda vs venv

| Feature | `venv` | `conda` |
|---------|--------|---------|
| Install | Built into Python | Separate install |
| Package manager | `pip` | `conda` + `pip` |
| Speed | Fast | Slower |
| Binary deps | Manual | Handles C deps |
| Best for | Pure Python projects | Scientific computing, CUDA |
| Env file | requirements.txt | environment.yml |

For AI/ML work: both are acceptable. Most production systems use `venv + pip`.

---

## Checking What's Installed

```python
import importlib.metadata as meta

# Get installed packages
for dist in meta.distributions():
    print(dist.name, dist.version)

# Check specific package
try:
    version = meta.version("transformers")
    print(f"transformers: {version}")
except meta.PackageNotFoundError:
    print("transformers not installed")
```

---

## Quick-Fire Interview Questions

1. **Why use virtual environments?**  
   Isolates project dependencies to avoid version conflicts between projects.

2. **What does `pip freeze > requirements.txt` do?**  
   Outputs all currently installed packages with exact versions to `requirements.txt`.

3. **Why shouldn't you commit `.env` files?**  
   They contain secrets (API keys, database credentials) that must not be in version control.

4. **What's the difference between `requirements.txt` and `pyproject.toml`?**  
   `requirements.txt` lists exact pinned versions for deployment; `pyproject.toml` defines flexible version ranges for library distribution.

5. **How do you share your environment setup with a teammate?**  
   Commit `requirements.txt` or `pyproject.toml`; they run `pip install -r requirements.txt` after activating their own venv.
