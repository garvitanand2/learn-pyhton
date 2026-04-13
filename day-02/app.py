# =============================================================
# Day 2: Operators & Input/Output
# Goal: Understand how Python computes and communicates.
#       In AI pipelines, you constantly evaluate conditions,
#       transform data, and format outputs.
# =============================================================

# --- 1. ARITHMETIC OPERATORS ----------------------------------
# What: Math operations on numbers
# AI use: Loss calculations, normalization, scaling data

true_value  = 10.0
pred_value  = 7.5

# Basic operations
diff        = true_value - pred_value            # subtraction
abs_error   = abs(diff)                          # absolute error
sq_error    = diff ** 2                          # exponentiation → squared error
print(f"Absolute Error : {abs_error}")
print(f"Squared Error  : {sq_error}")

# Mean Squared Error for a batch
errors = [1.2, 0.5, 2.1, 0.8, 1.5]
mse    = sum(e ** 2 for e in errors) / len(errors)
print(f"MSE            : {round(mse, 4)}")

# Floor division and modulo (very useful for batching)
dataset_size = 1000
batch_size   = 32
num_batches  = dataset_size // batch_size   # floor division: 31
remainder    = dataset_size %  batch_size   # modulo: 8 leftover samples
print(f"\nDataset: {dataset_size} | Batch: {batch_size}")
print(f"Full batches : {num_batches}")
print(f"Leftover samples : {remainder}")

# Division always returns float in Python 3
print(f"\n10 / 3  = {10 / 3}")    # 3.3333...
print(f"10 // 3 = {10 // 3}")    # 3   (integer floor division)
print(f"10 % 3  = {10 % 3}")     # 1   (remainder)
print(f"2 ** 8  = {2 ** 8}")     # 256 (exponentiation)

# --- 2. AUGMENTED ASSIGNMENT OPERATORS ------------------------
# Shorthand: x += 1  is the same as  x = x + 1

total_loss = 0.0
batch_losses = [0.45, 0.32, 0.28, 0.41, 0.35]
for loss in batch_losses:
    total_loss += loss          # accumulate loss over batches

avg_loss = total_loss / len(batch_losses)
print(f"\nAverage batch loss: {round(avg_loss, 4)}")

step = 0
step += 1        # increment training step
step *= 2        # double it
step -= 1        # subtract
print(f"Step after operations: {step}")   # (0+1)*2-1 = 1

# --- 3. COMPARISON OPERATORS ----------------------------------
# What: Compare two values, always returns bool (True/False)
# AI use: Checking thresholds, validation conditions

confidence    = 0.87
threshold     = 0.80
max_tokens    = 4096
tokens_used   = 3500

print(f"\nconfidence >= threshold : {confidence >= threshold}")  # True
print(f"tokens_used < max_tokens: {tokens_used < max_tokens}")  # True
print(f"confidence == 0.87      : {confidence == 0.87}")        # True
print(f"confidence != threshold : {confidence != threshold}")   # True

# Chained comparisons — Pythonic and readable
score = 78
print(f"Score 60-90? {60 <= score <= 90}")   # True — Python allows chaining!

# --- 4. LOGICAL OPERATORS -------------------------------------
# What: Combine boolean conditions
# and → both must be True
# or  → at least one must be True
# not → inverts the boolean

is_trained    = True
above_threshold = confidence >= threshold

if is_trained and above_threshold:
    print("\nModel is ready to deploy.")

use_cache  = False
use_api    = True
if use_cache or use_api:
    print("Data source available.")

debug_mode = False
if not debug_mode:
    print("Running in production mode.")

# Short-circuit evaluation (important for performance and safety)
# `and` stops at first False, `or` stops at first True
result = None
fallback = "default_output"
output = result or fallback     # result is None (falsy), so uses fallback
print(f"\nOutput: {output}")    # "default_output"

# --- 5. BITWISE OPERATORS (brief — used in hashing/encoding) --
flags = 0b1010   # binary: 8 + 2 = 10
mask  = 0b1100   # binary: 8 + 4 = 12
print(f"\nAND: {flags & mask}")    # 0b1000 = 8
print(f"OR : {flags | mask}")     # 0b1110 = 14
print(f"XOR: {flags ^ mask}")     # 0b0110 = 6
print(f"NOT: {~flags}")           # -(flags+1) = -11 in Python

# --- 6. INPUT / OUTPUT ----------------------------------------
# input() always returns a STRING — you must convert!

print("\n--- Input / Output Demo ---")
print("Simulating user input (hardcoded for demo):")

# In real usage: name = input("Enter your name: ")
name = "Alex"   # simulating input
print(f"Hello, {name}! Welcome to the AI track.")

# Simulating numeric input
raw_lr = "0.001"    # simulating: lr = input("Learning rate: ")
lr = float(raw_lr)
print(f"Learning rate set to: {lr}")

# --- 7. PRINT FORMATTING --------------------------------------

# sep and end arguments
print("Model", "Version", "Loss", sep=" | ")        # custom separator
print("Training", end="... ")                         # no newline
print("Done!")

# Padding and alignment (useful for tabular reports)
print(f"\n{'Metric':<15} {'Value':>10}")
print(f"{'Loss':<15} {0.2435:>10.4f}")
print(f"{'Accuracy':<15} {0.9712:>10.4f}")
print(f"{'F1-Score':<15} {0.9543:>10.4f}")

# Format spec: {value:<width.precisionf}
#   <  = left-align
#   >  = right-align
#   ^  = center
#   .4f = 4 decimal places float

# --- 8. OPERATOR PRECEDENCE -----------------------------------
# PEMDAS / BODMAS — same as math
# P: Parentheses   E: Exponents   MD: Mul/Div   AS: Add/Sub

result = 2 + 3 * 4      # 14, not 20 (multiplication first)
result = (2 + 3) * 4    # 20 (parentheses first)
result = 2 ** 3 ** 2    # 512 (right-associative: 3**2=9, 2**9=512)
print(f"\nPrecedence result: {result}")

# Use parentheses generously in AI formulas for clarity
relu_output = max(0, 0.3 * 10 - 2)  # max(0, 1) = 1
print(f"ReLU output: {relu_output}")

# --- SUMMARY --------------------------------------------------
print("\n--- Day 2 Complete ---")
print("Operators and I/O — the building blocks of all computation.")
