# Day 30 Exercises — Extend SentimentFlow

## Exercise 1: Add a new PipelineStep — DuplicateFilter
Add a `DuplicateFilter` step that skips records whose `cleaned_text` has already been seen in the current run. Insert it after `TextCleaner` in the pipeline.

```python
class DuplicateFilter(PipelineStep):
    def __init__(self, config: PipelineConfig):
        super().__init__(config)
        self._seen: set[str] = set()

    def _process(self, record: TextRecord) -> TextRecord:
        if record.cleaned_text in self._seen:
            record.skipped = True
            record.skip_reason = "duplicate text"
        else:
            self._seen.add(record.cleaned_text)
        return record

# Test:
dedupe_filter = DuplicateFilter(config)
texts = ["Great model", "Great model", "Terrible results", "Great model"]
records = [TextRecord(i+1, t) for i, t in enumerate(texts)]
cleaned = [TextCleaner(config)._process(r) for r in records]
filtered = [dedupe_filter.process(r) for r in cleaned]
print("Skipped:", [r.record_id for r in filtered if r.skipped])  # [2, 4]
```

---

## Exercise 2: Config from JSON File
Write a `config.json` file, load it with `PipelineConfig.from_json()`, and run the pipeline with it.

```json
{
  "min_token_count": 3,
  "max_token_count": 100,
  "output_path": "exercise_output.jsonl",
  "batch_size": 32,
  "verbose": true
}
```

```python
from pathlib import Path
import json

# YOUR TASK:
# 1. Write config.json to a temp file
# 2. Load it with PipelineConfig.from_json()
# 3. Run the pipeline with DEMO_TEXTS
# 4. Print the first 3 results

config_data = {
    "min_token_count": 3,
    "max_token_count": 100,
    "output_path": "exercise_output.jsonl",
    "batch_size": 32,
    "verbose": True,
}
config_path = Path("temp_config.json")
config_path.write_text(json.dumps(config_data))

config = PipelineConfig.from_json(str(config_path))
records, stats = run_pipeline(DEMO_TEXTS, config)
for r in records[:3]:
    print(r.record_id, r.label, r.score)

config_path.unlink()  # cleanup
```

---

## Exercise 3: Add Confidence Bands to the Report
Modify `print_report()` to also print the percentage of records in each confidence band: low (<0.4), medium (0.4–0.7), high (>0.7).

```python
def print_confidence_bands(records: list[TextRecord]) -> None:
    processed = [r for r in records if not r.skipped]
    bands = {"low (<0.4)": 0, "medium (0.4-0.7)": 0, "high (>0.7)": 0}
    for r in processed:
        if r.score < 0.4:
            bands["low (<0.4)"] += 1
        elif r.score <= 0.7:
            bands["medium (0.4-0.7)"] += 1
        else:
            bands["high (>0.7)"] += 1
    print("\n  Confidence Bands:")
    total = len(processed) or 1
    for band, count in bands.items():
        print(f"    {band:<20} {count:>4} ({count/total*100:.1f}%)")

# Call it inside or after print_report:
records, stats = run_pipeline(DEMO_TEXTS, PipelineConfig())
print_confidence_bands(records)
```

---

## Exercise 4: Write Tests for Two Pipeline Steps
Using `pytest`, write at least 5 tests covering `TextCleaner` and `Tokenizer` step behavior.

```python
import pytest
from dataclasses import dataclass

# (import or paste the relevant classes from app.py)

@pytest.fixture
def config():
    return PipelineConfig(min_token_count=2)

@pytest.fixture
def cleaner(config):
    return TextCleaner(config)

@pytest.fixture
def tokenizer(config):
    return Tokenizer(config)

def test_cleaner_removes_punctuation(cleaner):
    r = TextRecord(1, "Hello, World! This is great.")
    result = cleaner.process(r)
    assert "," not in result.cleaned_text
    assert "!" not in result.cleaned_text

def test_cleaner_skips_empty_text(cleaner):
    r = TextRecord(1, "   ")
    result = cleaner.process(r)
    assert result.skipped
    assert result.skip_reason == "empty after cleaning"

def test_tokenizer_lowercases(tokenizer, config):
    r = TextRecord(1, "HELLO WORLD")
    r.cleaned_text = "HELLO WORLD"
    result = tokenizer.process(r)
    assert all(t == t.lower() for t in result.tokens)

def test_tokenizer_skips_short_text(tokenizer, config):
    r = TextRecord(1, "hi")
    r.cleaned_text = "hi"
    result = tokenizer.process(r)
    assert result.skipped  # 1 token < min_token_count=2

def test_tokenizer_truncates_long_text(config):
    long_config = PipelineConfig(min_token_count=1, max_token_count=3)
    tok = Tokenizer(long_config)
    tokens_text = " ".join(["word"] * 10)
    r = TextRecord(1, tokens_text)
    r.cleaned_text = tokens_text
    result = tok.process(r)
    assert len(result.tokens) == 3
```

---

## Exercise 5: Stream from a Real File
Write a 10-line text file and run the full pipeline on it using `stream_from_file()`.

```python
from pathlib import Path

# Create a sample input file
sample_texts = [
    "This Python course is absolutely excellent and highly recommended.",
    "The pace is too slow and the examples are confusing.",
    "Good balance of theory and practical exercises.",
    "I learned more in 30 days than in months of tutorials.",
    "Some days feel rushed and lack sufficient depth.",
    "The final project ties everything together beautifully.",
    "Documentation could be clearer for beginners.",
    "Highly satisfied with the progress I made this month.",
    "A few exercises have bugs that need fixing.",
    "Overall an outstanding learning experience.",
]

input_path = Path("sample_input.txt")
input_path.write_text("\n".join(sample_texts), encoding="utf-8")

# YOUR TASK: use stream_from_file instead of stream_from_list
config = PipelineConfig(min_token_count=3, output_path="file_stream_results.jsonl")
steps = [TextCleaner(config), Tokenizer(config), FeatureExtractor(config), SentimentLabeler(config)]
pipeline = Pipeline(steps, config)
source = stream_from_file(input_path)
results = pipeline.run(source)
print_report(results, pipeline.step_stats)

# Cleanup
input_path.unlink()
Path("file_stream_results.jsonl").unlink(missing_ok=True)
```

---

## Stretch Challenge: Add a CLI Summary Flag
Add a `--summary-only` flag to the argparse CLI that runs the pipeline but prints the report without saving any output file. Modify `main()` to support this.

```python
# In argparse setup, add:
parser.add_argument("--summary-only", action="store_true",
                    help="Print report but do not save JSONL output")

# In main(), after running the pipeline:
if args.summary_only:
    print_report(records, step_stats)
    print("  (--summary-only: no file saved)")
else:
    print_report(records, step_stats)
    count = save_jsonl(records, output_path)
    print(f"\n  Results saved: {output_path} ({count} records)")
```
