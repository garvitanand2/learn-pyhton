# # Day 4 Exercises — Loops

# Estimated time: 25–35 minutes

# ## Exercise 1 — Training Epoch Simulator

# Simulate a training loop that:
# 1. Starts with `loss = 2.0` and `accuracy = 0.0`
# 2. Each epoch, loss decreases by 15% and accuracy increases by 8% (capped at 1.0)
# 3. Loop runs until `loss < 0.15` OR `accuracy >= 0.95` OR `epoch > 100`
# 4. Print a status line per epoch:
# ```
# Epoch  1 | Loss: 1.7000 | Accuracy: 8.00%
# Epoch  2 | Loss: 1.4450 | Accuracy: 15.68%
# ...
# ```
# 5. After the loop, print WHY it stopped (loss threshold / accuracy threshold / max epochs)

loss = 2.0;
accuracy = 0.0;
epoch = 0;
while loss >= 0.15 and accuracy < 0.95 and epoch <= 100:
    epoch += 1;
    loss *= 0.85; # Decrease loss by 15%
    accuracy = min(accuracy + 0.08, 1.0); # Increase accuracy by 8%, capped at 1.0
    print(f"Epoch {epoch:3d} | Loss: {loss:.4f} | Accuracy: {accuracy*100:.2f}%");  
if loss < 0.15:
    print("Stopped because loss threshold was reached.");
elif accuracy >= 0.95:
    print("Stopped because accuracy threshold was reached.");
else:
    print("Stopped because maximum epochs were reached.");

# ## Exercise 2 — Batch Generator

# Write a function `create_batches(data, batch_size)` that:
# 1. Takes a list and a batch size
# 2. Returns a list of batches (each batch is a sub-list)
# 3. The last batch may be smaller than `batch_size`

# ```python
# data = list(range(1, 11))   # [1, 2, ..., 10]
# batches = create_batches(data, 3)
# # Expected: [[1,2,3], [4,5,6], [7,8,9], [10]]
# ```

# Use only a `for` loop and `range()` with a step — no slicing tricks yet (or try both!).

def create_batches(data, batch_size):
    batches = [];
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]; # Slicing to create a batch
        batches.append(batch);
    return batches;

# ## Exercise 3 — Vocabulary Builder

# Given a list of sentences, build a vocabulary dictionary:
# - Keys: unique words (lowercased, stripped of punctuation)
# - Values: number of times the word appears across all sentences

# ```python
# corpus = [
#     "The cat sat on the mat.",
#     "The cat ate the rat.",
#     "The rat sat on a mat.",
# ]
# ```


# Print the top 5 most frequent words with a bar chart (use `"█" * count`).

corpus = [
    "The cat sat on the mat.",
    "The cat ate the rat.",
    "The rat sat on a mat.",
];
vocab = {};
for sentence in corpus:
    words = sentence.lower().replace(".", "").split(); # Lowercase, remove punctuation, split into words
    for word in words:
        vocab[word] = vocab.get(word, 0) + 1; # Increment word count
# Sort vocabulary by frequency
sorted_vocab = sorted(vocab.items(), key=lambda item: item[1], reverse=True);
print("Top 5 most frequent words:");
for word, count in sorted_vocab[:5]:
    print(f"{word}: {count} {'█' * count}");    

# ## Exercise 4 — Duplicate Detector

# Given a list of user IDs, find all duplicates and print them (without using sets — use only loops and conditionals to understand the process, then optimize with a set).

# ```python
# user_ids = [101, 203, 101, 450, 203, 789, 101, 999]
# ```

# Expected output:
# ```
# Duplicates found: [101, 203]
# ```

# **Bonus**: Re-implement using a `set` and compare the approach.
user_ids = [101, 203, 101, 450, 203, 789, 101, 999];
duplicates = [];
for i in range(len(user_ids)):
    for j in range(i + 1, len(user_ids)):
        if user_ids[i] == user_ids[j] and user_ids[i] not in duplicates:
            duplicates.append(user_ids[i]);
print(f"Duplicates found: {duplicates}");


# ## Exercise 5 — Nested Loop: Confusion Matrix Printer

# Given a list of true labels and predicted labels:

# ```python
# true_labels = [0, 1, 2, 0, 1, 2, 0, 1, 2]
# pred_labels = [0, 2, 2, 0, 0, 2, 1, 1, 2]
# num_classes = 3
# ```

# Build and print a 3×3 confusion matrix using nested loops.

# Expected:
# ```
# Confusion Matrix:
#      Pred 0  Pred 1  Pred 2
# True 0   2       1       0
# True 1   1       1       1
# True 2   0       0       2
# ```

true_labels = [0, 1, 2, 0, 1, 2, 0, 1, 2];
pred_labels = [0, 2, 2, 0, 0, 2, 1, 1, 2];
num_classes = 3;
# Initialize confusion matrix with zeros
confusion_matrix = [[0 for _ in range(num_classes)] for _ in range(num_classes)];
# Populate confusion matrix
for t, p in zip(true_labels, pred_labels):
    confusion_matrix[t][p] += 1;
# Print confusion matrix
print("Confusion Matrix:");
print("      Pred 0  Pred 1  Pred 2");
for i in range(num_classes):
    print(f"True {i}   {confusion_matrix[i][0]:<7} {confusion_matrix[i][1]:<7} {confusion_matrix[i][2]:<7}");           


# Given a long text (paste any paragraph), write a script that:
# 1. Counts word frequencies
# 2. Removes common stop words: `["the", "a", "an", "is", "are", "was", "of", "in", "to", "and"]`
# 3. Prints the top 10 remaining words sorted by frequency
# 4. Also prints the total unique word count

# Use `for` loops, `dict.get()`, and `sorted()` with a `key` argument.


paragraph = """Your long text goes here. You can paste any paragraph you like, and the script will count word frequencies, remove common stop words, and print the top 10 remaining words along with the total unique word count."""
stop_words = ["the", "a", "an", "is", "are", "was", "of", "in", "to", "and"];
word_freq = {};
for word in paragraph.lower().replace(".", "").split():
    if word not in stop_words:
        word_freq[word] = word_freq.get(word, 0) + 1;
# Sort by frequency
sorted_words = sorted(word_freq.items(), key=lambda item: item[1], reverse=True);
print("Top 10 words:");
for word, freq in sorted_words[:10]:
    print(f"{word}: {freq}");
print(f"Total unique words (excluding stop words): {len(word_freq)}");