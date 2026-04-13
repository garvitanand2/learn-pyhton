# =============================================================
# Day 5: Functions — Basics
# Goal: Package reusable logic into named blocks.
#       In AI systems, functions ARE the pipeline — every
#       transformation, validation, and computation is a function.
# =============================================================

# --- 1. DEFINING AND CALLING A FUNCTION -----------------------
# What: A named, reusable block of code
# Why:  DRY (Don't Repeat Yourself), testable, modular

def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

message = greet("AI Engineer")
print(message)    # Hello, AI Engineer!

# --- 2. PARAMETERS & RETURN VALUES ----------------------------

def compute_mae(actual: list, predicted: list) -> float:
    """Compute Mean Absolute Error between two lists of numbers."""
    if len(actual) != len(predicted):
        raise ValueError("Lists must be the same length")

    total_error = 0.0
    for a, p in zip(actual, predicted):
        total_error += abs(a - p)

    return total_error / len(actual)

actuals    = [3.0, 5.0, 2.5, 7.0]
preds      = [2.8, 5.3, 2.0, 6.5]
mae        = compute_mae(actuals, preds)
print(f"\nMAE: {mae:.4f}")

# --- 3. DEFAULT PARAMETER VALUES ------------------------------
# What: Parameters with a pre-set fallback value
# Why:  Makes functions flexible without requiring all arguments

def create_model_config(
    model_name: str,
    temperature: float = 0.7,       # default
    max_tokens: int = 1024,         # default
    top_p: float = 1.0              # default
) -> dict:
    """Build a model configuration dictionary."""
    return {
        "model":       model_name,
        "temperature": temperature,
        "max_tokens":  max_tokens,
        "top_p":       top_p
    }

# Using defaults
config_1 = create_model_config("gpt-3.5-turbo")
print(f"\nConfig 1: {config_1}")

# Overriding some defaults
config_2 = create_model_config("gpt-4", temperature=0.2, max_tokens=2048)
print(f"Config 2: {config_2}")

# --- 4. MULTIPLE RETURN VALUES --------------------------------
# Python returns a tuple — destructure it on the caller side

def normalize(values: list) -> tuple:
    """Normalize a list to [0, 1] range. Returns (normalized, min, max)."""
    min_val = min(values)
    max_val = max(values)
    rng     = max_val - min_val

    if rng == 0:
        return [0.0] * len(values), min_val, max_val

    normalized = [(v - min_val) / rng for v in values]
    return normalized, min_val, max_val

raw_scores    = [10, 25, 30, 5, 20, 15]
norm, lo, hi  = normalize(raw_scores)   # destructure tuple
print(f"\nNormalized: {[round(x, 2) for x in norm]}")
print(f"Range: [{lo}, {hi}]")

# --- 5. DOCSTRINGS --------------------------------------------
# What: A string right after def — documents the function
# Why:  Enables help(), IDE tooltips, auto-generated docs

def tokenize(text: str, lowercase: bool = True) -> list:
    """
    Tokenize a string into words.

    Args:
        text (str): Input text to tokenize.
        lowercase (bool): If True, convert tokens to lowercase. Default True.

    Returns:
        list: A list of string tokens.

    Example:
        >>> tokenize("Hello World")
        ['hello', 'world']
    """
    if lowercase:
        text = text.lower()
    return text.split()

tokens = tokenize("Large Language Models Are Powerful")
print(f"\nTokens: {tokens}")
print(help(tokenize))   # prints the docstring

# --- 6. FUNCTION AS A VALUE (First-Class Functions) -----------
# In Python, functions are objects — you can pass them around

def apply_twice(func, value):
    """Apply a function to a value, then apply it again to the result."""
    return func(func(value))

def double(x):
    return x * 2

result = apply_twice(double, 3)   # double(double(3)) = double(6) = 12
print(f"\napply_twice(double, 3) = {result}")

# Passing different functions to the same pipeline step
def square(x):
    return x ** 2

print(f"apply_twice(square, 2) = {apply_twice(square, 2)}")  # square(4) = 16

# --- 7. VARIABLE SCOPE ----------------------------------------
# Local  → exists only inside the function
# Global → exists in the module level
# LEGB rule: Local → Enclosing → Global → Built-in

counter = 0    # global

def increment():
    """Increment the global counter."""
    global counter    # declare we're modifying the global
    counter += 1

increment()
increment()
print(f"\nCounter: {counter}")   # 2

# Best practice: AVOID global state. Use return values instead.
def increment_pure(n: int) -> int:
    """Pure function — no side effects."""
    return n + 1

c = 0
c = increment_pure(c)
c = increment_pure(c)
print(f"Pure counter: {c}")   # 2

# --- 8. PRACTICAL EXAMPLE: Text Preprocessing Pipeline -------

def to_lowercase(text: str) -> str:
    return text.lower()

def remove_punctuation(text: str) -> str:
    import string
    return text.translate(str.maketrans("", "", string.punctuation))

def strip_whitespace(text: str) -> str:
    return " ".join(text.split())

def preprocess(text: str, steps: list = None) -> str:
    """
    Apply a list of preprocessing functions to text in sequence.
    This is a functional pipeline pattern — a building block of NLP.
    """
    if steps is None:
        steps = [to_lowercase, remove_punctuation, strip_whitespace]

    for step in steps:
        text = step(text)    # each step transforms the output of the previous
    return text

raw_text = "  Hello, World!  This is   an AI  model.  "
clean    = preprocess(raw_text)
print(f"\nRaw   : '{raw_text}'")
print(f"Clean : '{clean}'")

# --- SUMMARY --------------------------------------------------
print("\n--- Day 5 Complete ---")
print("Functions = the building blocks of every AI system.")
