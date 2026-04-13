# =============================================================
# Day 1: Python Setup, Variables & Data Types
# Goal: Think like a data engineer — every value has a type,
#       and knowing types prevents bugs in AI pipelines.
# =============================================================

# --- 1. INTEGERS -----------------------------------------------
# What: Whole numbers — no decimal point
# AI use: batch sizes, token counts, layer depths, epochs

batch_size = 32          # how many samples per training step
num_epochs = 100         # how many full passes over the dataset
num_layers = 4           # depth of a neural network

print(f"batch_size  = {batch_size}  | type: {type(batch_size)}")
print(f"num_epochs  = {num_epochs} | type: {type(num_epochs)}")

# --- 2. FLOATS -------------------------------------------------
# What: Numbers with a decimal point (IEEE 754 double precision)
# AI use: learning rates, loss values, probabilities, thresholds

learning_rate   = 0.001   # small → slow learning; large → unstable
loss_value      = 0.2435  # how wrong the model's prediction was
confidence      = 0.97    # probability assigned by a classifier

print(f"\nlearning_rate = {learning_rate} | type: {type(learning_rate)}")
print(f"loss_value    = {loss_value}  | type: {type(loss_value)}")

# Floating-point precision warning (important for AI engineers!)
a = 0.1 + 0.2
print(f"\n0.1 + 0.2 = {a}")               # 0.30000000000000004  ← not 0.3!
print(f"Round fix: {round(a, 2)}")        # 0.3  ← use round() when comparing

# --- 3. BOOLEANS -----------------------------------------------
# What: True or False — stored as 1 / 0 under the hood
# AI use: flags for training mode, GPU availability, dropout

is_training     = True
use_gpu         = False
dropout_enabled = True

print(f"\nis_training     = {is_training}  | type: {type(is_training)}")
print(f"int(True)  = {int(True)}")        # 1
print(f"int(False) = {int(False)}")       # 0

# --- 4. STRINGS ------------------------------------------------
# What: Sequence of characters (immutable)
# AI use: prompts, labels, model names, dataset paths

model_name      = "llama-3"
task_label      = "text-classification"
dataset_path    = "/data/train.csv"
prompt_template = "Summarize the following text:\n{text}"

print(f"\nmodel_name  = {model_name}  | type: {type(model_name)}")
print(f"Length of model_name: {len(model_name)} chars")

# Multi-line string (great for prompt templates)
system_prompt = """
You are a helpful AI assistant.
Answer concisely and accurately.
"""
print(f"System prompt:\n{system_prompt}")

# --- 5. NONETYPE -----------------------------------------------
# What: Represents "no value" / "not yet set"
# AI use: uninitialized model outputs, optional config values

model_output   = None
cached_result  = None

print(f"model_output = {model_output} | type: {type(model_output)}")
print(f"Is None? {model_output is None}")   # always check with `is`, not `==`

# --- 6. TYPE CONVERSION (CASTING) ------------------------------
# AI pipeline data often arrives as strings — must convert!

raw_threshold  = "0.85"           # came from a config file as string
threshold      = float(raw_threshold)
print(f"\nConverted threshold: {threshold} | type: {type(threshold)}")

token_count    = 512
report_label   = "Token count: " + str(token_count)  # int → str for concat
print(report_label)

confidence_pct = int(confidence * 100)  # float → int (truncates, no rounding)
print(f"Confidence: {confidence_pct}%")

# --- 7. MULTIPLE ASSIGNMENT ------------------------------------
x, y, z = 10, 20, 30            # unpack values in one line
print(f"\nx={x}, y={y}, z={z}")

# Pythonic swap — no temp variable needed
x, y = y, x
print(f"After swap: x={x}, y={y}")

# --- 8. CONSTANTS (Convention: SCREAMING_SNAKE_CASE) ----------
MAX_TOKENS          = 4096
DEFAULT_TEMPERATURE = 0.7
API_VERSION         = "v1"

print(f"\nMAX_TOKENS          = {MAX_TOKENS}")
print(f"DEFAULT_TEMPERATURE = {DEFAULT_TEMPERATURE}")

# --- 9. F-STRINGS (modern, fast, readable) --------------------
model   = "GPT"
version = 4
params  = "1.8T"
print(f"\nRunning {model}-{version} with {params} parameters")

# Expression inside f-string
tokens_used = 1024
print(f"Tokens remaining: {MAX_TOKENS - tokens_used}")

# --- 10. IDENTITY vs EQUALITY ----------------------------------
# `==`  checks VALUE equality
# `is`  checks if two names point to the SAME object in memory

a = [1, 2, 3]
b = [1, 2, 3]
print(f"\na == b : {a == b}")   # True  — same values
print(f"a is b : {a is b}")   # False — different objects

# Python caches small ints (-5 to 256) — a quirk to know for interviews
p = 200
q = 200
print(f"p is q (small int 200): {p is q}")   # True — cached

r = 1000
s = 1000
print(f"r is s (large int 1000): {r is s}")  # False — not cached

# --- 11. CHECKING TYPES ----------------------------------------
print(f"\ntype checks:")
print(f"isinstance(batch_size, int)   : {isinstance(batch_size, int)}")
print(f"isinstance(learning_rate, float): {isinstance(learning_rate, float)}")
print(f"isinstance(model_name, str)   : {isinstance(model_name, str)}")
print(f"isinstance(model_output, type(None)): {isinstance(model_output, type(None))}")

# --- SUMMARY ---------------------------------------------------
print("\n--- Day 1 Complete ---")
print("You now understand Python's core data types.")
print("Next: operators and input/output (Day 2)")
