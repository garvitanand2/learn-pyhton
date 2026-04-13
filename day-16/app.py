# Day 16: File Handling
# Focus: Reading, writing, and managing files — the foundation
#         of every data pipeline and model training workflow.

# ============================================================
# WHAT: Python can read and write files on disk using open()
#       or the modern pathlib.Path interface.
# WHY:  AI pipelines load datasets from disk, save checkpoints,
#       write logs, export results, and read config files.
# ============================================================

import os
import json
import csv
import io
from pathlib import Path

# ============================================================
# 1. Writing a Text File
# ============================================================
print("=== 1. Writing Text Files ===")

# "w" mode: write (creates or overwrites)
# "a" mode: append (adds to existing file)
# Always use `with` — it automatically closes the file

log_path = Path("training_log.txt")

with open(log_path, "w") as f:
    f.write("=== Training Log ===\n")
    f.write("Epoch 1 | Loss: 0.8432 | Acc: 0.6100\n")
    f.write("Epoch 2 | Loss: 0.5217 | Acc: 0.7840\n")
    f.write("Epoch 3 | Loss: 0.3891 | Acc: 0.8560\n")

print(f"Wrote to: {log_path}")

# Append more lines
with open(log_path, "a") as f:
    f.write("Epoch 4 | Loss: 0.2934 | Acc: 0.8900\n")

# ============================================================
# 2. Reading a Text File
# ============================================================
print("\n=== 2. Reading Text Files ===")

# Read entire file as string
with open(log_path, "r") as f:
    content = f.read()
print("Full content:")
print(content)

# Read line by line (memory efficient for large files!)
print("Line by line:")
with open(log_path, "r") as f:
    for line in f:
        line = line.strip()  # remove \n
        if line and "Epoch" in line:
            parts = line.split("|")
            epoch = parts[0].strip()
            loss = parts[1].strip()
            print(f"  {epoch} — {loss}")

# readlines() → list of strings
with open(log_path, "r") as f:
    lines = f.readlines()
print(f"\nTotal lines: {len(lines)}")

# ============================================================
# 3. JSON Files (Most important for AI config & data)
# ============================================================
print("\n=== 3. JSON Files ===")

# Model configuration
model_config = {
    "model_name": "bert-base-uncased",
    "hidden_size": 768,
    "num_attention_heads": 12,
    "num_hidden_layers": 12,
    "max_position_embeddings": 512,
    "vocab_size": 30522,
    "dropout": 0.1,
}

config_path = Path("model_config.json")

# Write JSON
with open(config_path, "w") as f:
    json.dump(model_config, f, indent=4)
print(f"Saved config to: {config_path}")

# Read JSON
with open(config_path, "r") as f:
    loaded_config = json.load(f)
print(f"Loaded model: {loaded_config['model_name']}")
print(f"Hidden size:  {loaded_config['hidden_size']}")

# json.dumps / json.loads for strings (no file)
json_string = json.dumps(model_config, indent=2)
print(f"\nJSON string (first 50 chars): {json_string[:50]}...")
parsed = json.loads(json_string)
print(f"Parsed type: {type(parsed)}")

# ============================================================
# 4. CSV Files
# ============================================================
print("\n=== 4. CSV Files ===")

dataset_path = Path("dataset.csv")

# Write CSV
rows = [
    ["id", "text", "label"],
    [1, "The model performed well", "positive"],
    [2, "Training loss diverged", "negative"],
    [3, "Benchmark results are average", "neutral"],
    [4, "State of the art results!", "positive"],
    [5, "Out of memory error", "negative"],
]

with open(dataset_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
print(f"Saved dataset to: {dataset_path}")

# Read CSV with DictReader (row as dict — easier to use!)
print("\nReading CSV:")
with open(dataset_path, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        label = row["label"]
        text = row["text"][:30]
        print(f"  [{label.upper():<10}] {text}")

# ============================================================
# 5. pathlib — Cleaner File Operations
# ============================================================
print("\n=== 5. pathlib Path Methods ===")

# Write and read with pathlib (simpler!)
data_file = Path("quick_data.json")
data = {"samples": 1000, "classes": ["positive", "negative", "neutral"]}
data_file.write_text(json.dumps(data, indent=2))
print(f"Wrote: {data_file}")

loaded = json.loads(data_file.read_text())
print(f"Loaded classes: {loaded['classes']}")

# ============================================================
# 6. Working with File Paths
# ============================================================
print("\n=== 6. File Path Utilities ===")

p = Path("logs/experiment_001/metrics.json")
print(f"Name:      {p.name}")
print(f"Stem:      {p.stem}")
print(f"Extension: {p.suffix}")
print(f"Parent:    {p.parent}")
print(f"Parts:     {p.parts}")

# Check if file exists before reading
if config_path.exists():
    print(f"\n✓ Config file exists ({config_path.stat().st_size} bytes)")
else:
    print("\n✗ Config file not found")

# ============================================================
# 7. Common Patterns in AI Projects
# ============================================================
print("\n=== 7. Real-World Patterns ===")

def load_jsonl(file_path: str) -> list:
    """Load a JSONL file (one JSON object per line).
    Common format for large ML datasets (e.g., The Pile, OASST)."""
    records = []
    path = Path(file_path)
    if not path.exists():
        return records
    with open(path, "r") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  Skip line {line_num}: {e}")
    return records

def save_results(results: list, output_path: str) -> None:
    """Save experiment results as JSONL."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for record in results:
            f.write(json.dumps(record) + "\n")
    print(f"Saved {len(results)} records to {path}")

# Simulate saving results
results = [
    {"id": 1, "pred": "positive", "confidence": 0.92},
    {"id": 2, "pred": "negative", "confidence": 0.87},
    {"id": 3, "pred": "neutral",  "confidence": 0.71},
]
save_results(results, "outputs/run_001.jsonl")

# ============================================================
# 8. Cleanup Demo Files
# ============================================================
for cleanup_path in [log_path, config_path, dataset_path, data_file]:
    if cleanup_path.exists():
        cleanup_path.unlink()  # delete file
print("\nCleaned up demo files.")
print("Day 16 complete! File I/O is the foundation of every data pipeline.")
