# =============================================================
# Day 4: Loops — for & while
# Goal: Iterate over data. In AI, you loop over datasets,
#       training steps, tokens, and results constantly.
# =============================================================

# --- 1. FOR LOOP — iterating over a sequence -----------------
# What: Executes a block for each item in an iterable
# AI use: Processing rows in a dataset, tokens in a prompt

tokens = ["The", "model", "predicted", "correctly"]
for token in tokens:
    print(token, end=" ")
print()  # newline

# Iterating over indices (when you need position)
for i, token in enumerate(tokens):
    print(f"[{i}] {token}")

# range() — generates integers on-demand (memory efficient)
print("\nEpoch progress:")
for epoch in range(1, 6):           # 1, 2, 3, 4, 5
    print(f"  Epoch {epoch}/5 completed")

# range(start, stop, step)
print("\nLearning rate decay schedule:")
for step in range(0, 1001, 200):    # 0, 200, 400, 600, 800, 1000
    lr = 0.01 * (0.9 ** (step / 200))
    print(f"  Step {step:4d} | LR: {lr:.6f}")

# --- 2. WHILE LOOP — condition-based repetition ---------------
# What: Repeats as long as a condition is True
# AI use: Training until convergence, retrying API calls

loss = 1.0
epoch = 0
learning_rate = 0.1
target_loss = 0.1

print("\nSimulated training loop:")
while loss > target_loss:
    loss *= (1 - learning_rate)    # simulated loss decay
    epoch += 1
    print(f"  Epoch {epoch:2d} | Loss: {loss:.4f}")
    if epoch >= 50:                # safety guard against infinite loops
        print("  Max epochs reached — stopping.")
        break

# --- 3. BREAK & CONTINUE --------------------------------------
# break    → exits the loop entirely
# continue → skips current iteration, move to next

print("\nFiltering dataset tokens:")
vocab = ["hello", "", "world", None, "AI", "", "model"]
clean_tokens = []
for word in vocab:
    if not word:           # skip empty strings and None (falsy)
        continue
    if word == "STOP":     # stop processing if stop token found
        break
    clean_tokens.append(word)

print(f"Clean tokens: {clean_tokens}")

# Finding first model above threshold (break on success)
models = [
    {"name": "v1", "accuracy": 0.72},
    {"name": "v2", "accuracy": 0.81},
    {"name": "v3", "accuracy": 0.95},
    {"name": "v4", "accuracy": 0.98},
]
print("\nSearching for best model:")
for model in models:
    if model["accuracy"] >= 0.90:
        print(f"Found deployable model: {model['name']} ({model['accuracy']:.0%})")
        break
else:
    # for-else: executes if loop completed WITHOUT hitting break
    print("No model meets the deployment threshold.")

# --- 4. NESTED LOOPS ------------------------------------------
# AI use: Iterating over a grid of hyperparameters

print("\nHyperparameter search:")
learning_rates = [0.01, 0.001, 0.0001]
batch_sizes    = [32, 64, 128]

for lr in learning_rates:
    for bs in batch_sizes:
        # Simulate a training run
        simulated_acc = round(0.5 + 0.1 * (1/lr) ** 0.1 * (bs / 100) ** 0.2, 4)
        print(f"  LR={lr} | BS={bs:3d} → Acc={simulated_acc}")

# --- 5. ITERATING OVER DICTIONARIES --------------------------
config = {
    "model":          "llama-3",
    "learning_rate":  0.0003,
    "batch_size":     32,
    "max_tokens":     4096,
    "use_fp16":       True,
}

print("\nModel Config:")
for key, value in config.items():
    print(f"  {key:<20}: {value}")

# Just keys
print("\nConfig keys:", list(config.keys()))

# Just values
print("Config values:", list(config.values()))

# --- 6. ZIP — iterating two sequences together ---------------
inputs  = ["cat", "dog", "bird", "fish"]
labels  = [0, 1, 2, 3]
scores  = [0.95, 0.88, 0.72, 0.91]

print("\nInference results:")
for text, label, score in zip(inputs, labels, scores):
    print(f"  '{text}' → class {label} | confidence: {score:.2f}")

# --- 7. ELSE CLAUSE ON LOOPS ----------------------------------
# The else block runs ONLY if the loop completed without break

search_term = "transformer"
corpus = ["neural networks", "deep learning", "convolutional nets"]

for doc in corpus:
    if search_term in doc:
        print(f"\nFound '{search_term}' in: '{doc}'")
        break
else:
    print(f"\n'{search_term}' not found in corpus.")

# --- 8. COMPREHENSIONS PREVIEW (deep dive Day 12) ------------
# One-liner loops for building lists — very common in data pipelines

squared_errors = [e ** 2 for e in [0.2, -0.3, 0.5, -0.1]]
print(f"\nSquared errors: {squared_errors}")

high_conf = [s for s in scores if s >= 0.90]
print(f"High-confidence scores: {high_conf}")

# --- 9. PRACTICAL EXAMPLE: Tokenizer Word Counter ------------
def count_word_frequencies(text: str) -> dict:
    """Count how often each word appears — like a basic tokenizer."""
    frequencies = {}
    words = text.lower().split()
    for word in words:
        # clean punctuation from end of word
        word = word.strip(".,!?;:")
        if word:
            frequencies[word] = frequencies.get(word, 0) + 1
    return dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True))

corpus_text = """
Transformers use attention mechanisms. Attention is the core of transformers.
Transformers changed how we process language and vision tasks.
"""

freq = count_word_frequencies(corpus_text)
print("\nWord Frequencies:")
for word, count in list(freq.items())[:8]:
    bar = "█" * count
    print(f"  {word:<15} {bar} ({count})")

# --- SUMMARY --------------------------------------------------
print("\n--- Day 4 Complete ---")
print("Loops = iteration over data = the engine of every data pipeline.")
