# Day 26: Virtual Environments & Dependency Management
# Focus: Reproducible, isolated Python environments

# ============================================================
# WHAT: A virtual environment is an isolated Python installation
#       with its own packages, separate from the system Python.
# WHY:  Project A needs numpy 1.24, Project B needs numpy 2.0.
#       Without isolation, they'd conflict. Every professional
#       Python project uses virtual environments. This is
#       table stakes for AI engineering.
# ============================================================

# This file demonstrates virtual environment concepts
# and dependency management patterns through runnable code.

import sys
import os
import subprocess
from pathlib import Path

# ============================================================
# 1. Inspect the Current Environment
# ============================================================
print("=== 1. Current Environment Info ===")

print(f"Python executable: {sys.executable}")
print(f"Python version:    {sys.version.split()[0]}")
print(f"Platform:          {sys.platform}")

# Is this a virtual environment?
in_venv = (
    hasattr(sys, "real_prefix") or                     # virtualenv
    (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)  # venv
)
print(f"In virtual env:    {in_venv}")
if in_venv:
    print(f"Venv path:         {sys.prefix}")

# ============================================================
# 2. Listing Installed Packages (programmatically)
# ============================================================
print("\n=== 2. Installed Packages ===")

try:
    import importlib.metadata as meta
    installed = [(d.name, d.version) for d in meta.distributions()]
    installed.sort(key=lambda x: x[0].lower())
    print(f"Total packages: {len(installed)}")
    print("Sample (first 10):")
    for name, version in installed[:10]:
        print(f"  {name:<30} {version}")
except Exception as e:
    print(f"  Could not list packages: {e}")

# ============================================================
# 3. What a requirements.txt Looks Like
# ============================================================
print("\n=== 3. requirements.txt ===")

requirements_content = """
# requirements.txt — pin exact versions for reproducibility

# Core ML
torch==2.1.0
transformers==4.36.0
datasets==2.15.0
accelerate==0.25.0

# Data science
numpy==1.26.2
pandas==2.1.4
scikit-learn==1.3.2

# NLP utilities
sentencepiece==0.1.99
tokenizers==0.15.0

# API and serving
fastapi==0.109.0
uvicorn==0.25.0
pydantic==2.5.3

# Development
pytest==7.4.3
pytest-cov==4.1.0
black==23.12.1
ruff==0.1.9
pre-commit==3.6.0

# Utilities
python-dotenv==1.0.0
tqdm==4.66.1
loguru==0.7.2
"""

print(requirements_content)

# ============================================================
# 4. pyproject.toml (Modern Standard)
# ============================================================
print("\n=== 4. pyproject.toml ===")

pyproject_content = """
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "my-nlp-project"
version = "0.1.0"
description = "NLP classification service"
requires-python = ">=3.11"
dependencies = [
    "torch>=2.0.0",
    "transformers>=4.30.0",
    "fastapi>=0.100.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "ruff>=0.1.0",
]
gpu = [
    "torch[cuda12]>=2.0.0",
]

[tool.black]
line-length = 88
target-version = ["py311"]

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]
"""

print(pyproject_content)

# ============================================================
# 5. .env File Pattern (Secrets Management)
# ============================================================
print("\n=== 5. Environment Variables & .env ===")

# .env file (NEVER commit this to git):
dotenv_example = """
# .env — local secrets (add to .gitignore!)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=ant-...
DATABASE_URL=postgresql://user:pass@localhost/mydb
ENVIRONMENT=development
LOG_LEVEL=DEBUG
"""

# .env.example (SAFE to commit — template without values):
dotenv_example_safe = """
# .env.example — copy to .env and fill in your values
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
DATABASE_URL=
ENVIRONMENT=development
LOG_LEVEL=INFO
"""

print("Contents of .env.example:")
print(dotenv_example_safe)

# Load env vars safely in code:
def get_env(key: str, default: str | None = None, required: bool = False) -> str | None:
    """Safely get environment variable."""
    value = os.environ.get(key, default)
    if required and value is None:
        raise RuntimeError(
            f"Required environment variable '{key}' is not set.\n"
            f"Check your .env file."
        )
    return value

api_key = get_env("OPENAI_API_KEY", default="demo-key")
log_level = get_env("LOG_LEVEL", default="INFO")
print(f"API key set: {bool(api_key)}")
print(f"Log level:   {log_level}")

# ============================================================
# 6. Key Shell Commands (Reference)
# ============================================================
print("\n=== 6. Key Shell Commands Reference ===")

commands = {
    "Create venv": "python -m venv .venv",
    "Activate (Mac/Linux)": "source .venv/bin/activate",
    "Activate (Windows)": ".venv\\Scripts\\activate",
    "Deactivate": "deactivate",
    "Install package": "pip install requests",
    "Install dev deps": "pip install -e '.[dev]'",
    "Freeze dependencies": "pip freeze > requirements.txt",
    "Install from file": "pip install -r requirements.txt",
    "Show package info": "pip show transformers",
    "List packages": "pip list",
    "Outdated packages": "pip list --outdated",
    "Uninstall package": "pip uninstall package-name",
    "Create locked env": "pip-compile pyproject.toml",
}

for action, cmd in commands.items():
    print(f"  {action:<25}  {cmd}")

# ============================================================
# 7. .gitignore for Python Projects
# ============================================================
print("\n=== 7. .gitignore Essentials ===")

gitignore = """
# .gitignore for a Python AI project

# Virtual environments
.venv/
venv/
env/

# Compiled Python
__pycache__/
*.py[cod]
*.pyo

# Distribution / packaging
build/
dist/
*.egg-info/

# Secrets (NEVER commit!)
.env
*.key
secrets/

# Model artifacts (usually too large for git)
checkpoints/
*.pt
*.pkl
*.bin
*.safetensors

# Data (usually too large for git)
data/
datasets/

# Outputs and logs
outputs/
logs/
*.log
runs/
mlruns/

# Jupyter
.ipynb_checkpoints/

# IDE
.vscode/
.idea/
"""

print(gitignore)
print("Day 26 complete! Reproducible environments are professional engineering standards.")
