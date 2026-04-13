# =============================================================
# Day 3: Conditional Statements
# Goal: Control your program's flow based on data.
#       AI systems constantly make decisions — classify,
#       route, threshold, filter. Conditionals are the core.
# =============================================================

# --- 1. BASIC IF / ELIF / ELSE --------------------------------
# What: Execute different code blocks based on a condition
# Why:  Route data, apply rules, make decisions in pipelines

confidence = 0.87

if confidence >= 0.90:
    label = "HIGH CONFIDENCE"
elif confidence >= 0.70:
    label = "MEDIUM CONFIDENCE"
elif confidence >= 0.50:
    label = "LOW CONFIDENCE"
else:
    label = "BELOW THRESHOLD — REJECT"

print(f"Confidence {confidence:.2f} → {label}")

# --- 2. NESTED CONDITIONALS -----------------------------------
# Use sparingly — deep nesting hurts readability

is_trained       = True
accuracy         = 0.94
deployment_ready = False

if is_trained:
    if accuracy >= 0.90:
        if not deployment_ready:
            print("\nModel trained and accurate — ready to deploy after final check.")
        else:
            print("\nModel is already deployed.")
    else:
        print("\nModel trained but accuracy too low.")
else:
    print("\nModel not yet trained.")

# Better practice: flatten with `and`
if is_trained and accuracy >= 0.90 and not deployment_ready:
    print("Flat check: ready to deploy.")

# --- 3. TERNARY OPERATOR (Conditional Expression) -------------
# What: One-liner if/else
# Syntax: value_if_true if condition else value_if_false

score  = 0.73
status = "Pass" if score >= 0.70 else "Fail"
print(f"\nScore {score} → {status}")

# Nested ternary (use with caution — readability drops)
tier = "Gold" if score >= 0.90 else ("Silver" if score >= 0.70 else "Bronze")
print(f"Tier: {tier}")

# --- 4. TRUTHINESS & FALSY CHECKS ----------------------------
# Python's `if` doesn't need `== True` — anything is truthy/falsy

model_output = ""         # empty string — falsy
cached_result = None      # None — falsy
error_list = []           # empty list — falsy
ready_flag = 1            # non-zero int — truthy

# Anti-pattern (verbose):
if model_output == "":
    print("\nNo output (verbose check)")

# Pythonic:
if not model_output:
    print("No output (Pythonic check)")

if cached_result is None:
    print("Cache miss — fetching fresh data")

if not error_list:
    print("No errors found")

if ready_flag:
    print("System ready")

# --- 5. `in` OPERATOR -----------------------------------------
# What: Checks membership — works on strings, lists, dicts, sets
# AI use: Check if class label is valid, if token exists, etc.

VALID_TASKS  = ["classification", "summarization", "translation", "qa"]
STOP_TOKENS  = ["<|endoftext|>", "</s>", "[EOS]"]
model_labels = {"cat": 0, "dog": 1, "bird": 2}

task = "summarization"
token = "</s>"
label = "cat"

print(f"\nTask valid: {task in VALID_TASKS}")             # True
print(f"Stop token: {token in STOP_TOKENS}")             # True
print(f"Label known: {label in model_labels}")           # True (checks keys)
print(f"Label unknown: {'fish' not in model_labels}")    # True

# String membership
sentence = "The transformer architecture changed AI forever."
print(f"'transformer' in sentence: {'transformer' in sentence}")

# --- 6. MATCH STATEMENT (Python 3.10+) -----------------------
# What: Structural pattern matching — like switch/case but more powerful
# AI use: Route model tasks, handle response types

response_type = "error"

match response_type:
    case "text":
        action = "display text response"
    case "image":
        action = "render image output"
    case "code":
        action = "syntax-highlight code block"
    case "error":
        action = "log error and retry"
    case _:
        action = "unknown response type — skip"  # default case

print(f"\nMatch result: {action}")

# Match with conditions (guards)
http_status = 404

match http_status:
    case 200:
        msg = "OK"
    case 400 | 401 | 403:
        msg = "Client error"
    case 404:
        msg = "Not found"
    case code if 500 <= code < 600:
        msg = f"Server error {code}"
    case _:
        msg = "Unknown status"

print(f"HTTP {http_status}: {msg}")

# --- 7. CONDITIONAL WITH `any()` / `all()` -------------------
# Very Pythonic — avoid manual loops when checking a list of conditions

scores     = [0.82, 0.91, 0.76, 0.88]
thresholds = [0.80, 0.80, 0.80, 0.80]

all_pass = all(s >= t for s, t in zip(scores, thresholds))
any_fail = any(s < t  for s, t in zip(scores, thresholds))

print(f"\nAll models pass threshold: {all_pass}")
print(f"Any model failed threshold: {any_fail}")

# --- 8. PRACTICAL EXAMPLE: Routing a Model Request -----------

def route_request(task_type: str, token_count: int) -> str:
    """Route an AI request to the appropriate model tier."""
    if task_type not in VALID_TASKS:
        return f"Error: Unknown task '{task_type}'"

    if token_count > 32000:
        return "Route to: GPT-4-128k (long context)"
    elif token_count > 8000:
        return "Route to: GPT-4 (standard)"
    elif task_type == "classification":
        return "Route to: BERT (efficient classifier)"
    else:
        return "Route to: GPT-3.5-Turbo (default)"

print("\n--- Request Routing ---")
print(route_request("summarization", 12000))
print(route_request("classification", 256))
print(route_request("translation", 5000))
print(route_request("invalid_task", 100))

# --- SUMMARY --------------------------------------------------
print("\n--- Day 3 Complete ---")
print("Conditionals = decision-making = the logic layer of AI pipelines.")
