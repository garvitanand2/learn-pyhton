# Exercise 1 — Loss Metrics Calculator
# Given a list of predicted vs actual values:

# actual    = [3.0, 5.0, 2.5, 7.0, 4.0]
# predicted = [2.8, 5.3, 2.0, 6.5, 4.2]
# Calculate and print:

# MAE — Mean Absolute Error: average of |actual - predicted|
# MSE — Mean Squared Error: average of (actual - predicted)²
# RMSE — Root Mean Squared Error: √MSE (use ** 0.5)

def calculate_errors(actual, predicted):
    n = len(actual)
    mae = sum(abs(a - p) for a, p in zip(actual, predicted)) / n
    mse = sum((a - p) ** 2 for a, p in zip(actual, predicted)) / n
    rmse = mse ** 0.5
    print(f"MAE : {mae:.4f}")
    print(f"MSE : {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")

actual    = [3.0, 5.0, 2.5, 7.0, 4.0]
predicted = [2.8, 5.3, 2.0, 6.5, 4.2]
calculate_errors(actual, predicted)

# Exercise 2 — Batch Partitioner
# Write a script that:
# Sets dataset_size = 5000 and batch_size = 128
# Computes the number of full batches
# Computes the size of the last partial batch (if any)
# Prints a summary table using f-string alignment:
dataset_size = 5000
batch_size = 128
full_batches = dataset_size // batch_size
partial_batch_size = dataset_size % batch_size
print(f"{'Batch Type':<15} {'Batch Size':>10}")
print(f"{'Full Batches':<15} {full_batches:>10}")
print(f"{'Partial Batch':<15} {partial_batch_size:>10}")


# Exercise 3 — Threshold Decision
# A spam classifier returns confidence scores:

# scores = [0.92, 0.45, 0.78, 0.31, 0.88, 0.55]
# For each score, use comparison operators to print whether it's:

# SPAM if score >= 0.75
# UNSURE if 0.50 <= score < 0.75
# NOT SPAM if score < 0.50
scores = [0.92, 0.45, 0.78, 0.31, 0.88, 0.55]
for item in scores:
    if item >= 0.75:
        print(f"Score: {item} - SPAM")
    elif 0.50 <= item < 0.75:
        print(f"Score: {item} - UNSURE")
    else:
        print(f"Score: {item} - NOT SPAM")


print(2 + 3 * 4)        # 14
print((2 + 3) * 4)      # 20
print(2 ** 3 ** 2)      # 512
print(10 - 4 / 2)       # 8
print(10 - 4 // 2)      # 10
print(5 % 3 + 1)        # 3
print(not True or False and True)  # False

# Exercise 5 — AI Training Report Formatter
# Write a function (or just a script) that prints a training summary table for 3 epochs with the following data:

# epoch_data = [
#     {"epoch": 1, "loss": 0.9832, "accuracy": 0.6120},
#     {"epoch": 2, "loss": 0.5421, "accuracy": 0.7845},
#     {"epoch": 3, "loss": 0.2834, "accuracy": 0.9012},
# ]
# Format it as:

# Epoch  |   Loss   | Accuracy
# -------|----------|----------
#   1    |  0.9832  |  61.20%
#   2    |  0.5421  |  78.45%
#   3    |  0.2834  |  90.12%
# Use f-string format specs for alignment and decimal places.

epoch_data = [
    {"epoch": 1, "loss": 0.9832, "accuracy": 0.6120},
    {"epoch": 2, "loss": 0.5421, "accuracy": 0.7845},
    {"epoch": 3, "loss": 0.2834, "accuracy": 0.9012},
]
print(f"{'Epoch':<6} | {'Loss':<8} | {'Accuracy':<9}")
print("-" * 30)
for data in epoch_data:
    epoch = data["epoch"]
    loss = data["loss"]
    accuracy = data["accuracy"] * 100  # convert to percentage
    print(f"{epoch:<6} | {loss:<8.4f} | {accuracy:<9.2f}%")
 