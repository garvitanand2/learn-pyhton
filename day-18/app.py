# Day 18: OOP Basics
# Focus: Modeling real-world AI components as Python objects

# ============================================================
# WHAT: Object-Oriented Programming (OOP) lets you bundle
#       data (attributes) and behavior (methods) together
#       into a *class*. An *instance* is one concrete object
#       built from that blueprint.
# WHY:  Every ML framework uses OOP:
#       torch.nn.Module, sklearn.BaseEstimator, tf.keras.Layer.
#       Learning OOP lets you read, extend, and build them.
# ============================================================

# ============================================================
# 1. Defining a Class
# ============================================================
print("=== 1. Basic Class ===")

class ModelConfig:
    """Stores hyperparameters for a ML model.
    
    Analogy: A class is like a blueprint for a house.
    Each instance (object) is a house built from that blueprint.
    Each house can have different colors (attribute values).
    """

    # Class attribute: shared by ALL instances
    framework = "PyTorch"

    def __init__(self, model_name: str, learning_rate: float = 1e-4,
                 batch_size: int = 32, max_epochs: int = 10):
        """Constructor — called when you create an instance.
        
        `self` is a reference to the specific instance being created.
        It MUST be the first parameter of every instance method.
        """
        # Instance attributes: unique to each instance
        self.model_name = model_name
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.max_epochs = max_epochs

    def describe(self) -> str:
        """Returns a human-readable summary of this config."""
        return (
            f"Model: {self.model_name}\n"
            f"LR: {self.learning_rate} | Batch: {self.batch_size}"
            f" | Epochs: {self.max_epochs}"
        )

    def total_steps(self, dataset_size: int) -> int:
        """Calculates total training steps."""
        steps_per_epoch = -(-dataset_size // self.batch_size)  # ceiling division
        return steps_per_epoch * self.max_epochs


# Create instances
bert_cfg = ModelConfig("bert-base-uncased", learning_rate=2e-5, max_epochs=5)
gpt_cfg  = ModelConfig("gpt-2", learning_rate=5e-5, batch_size=16, max_epochs=3)

print(bert_cfg.describe())
print(f"\nGPT-2 total steps (10k dataset): {gpt_cfg.total_steps(10_000)}")
print(f"\nClass attribute: {ModelConfig.framework}")  # access on class
print(f"Instance access: {bert_cfg.framework}")        # also works

# ============================================================
# 2. Instance, Class, and Static Methods
# ============================================================
print("\n=== 2. Method Types ===")

class Tokenizer:
    """Simple whitespace tokenizer with vocabulary."""

    special_tokens = ["<PAD>", "<UNK>", "<BOS>", "<EOS>"]

    def __init__(self, vocab: dict | None = None):
        self.vocab = vocab or {}
        self.inverse_vocab = {v: k for k, v in self.vocab.items()}

    def encode(self, text: str) -> list[int]:
        """Instance method: accesses self."""
        tokens = text.lower().split()
        return [self.vocab.get(t, 0) for t in tokens]  # 0 = <UNK>

    @classmethod
    def from_corpus(cls, corpus: list[str]) -> "Tokenizer":
        """Class method: creates instance from data.
        
        Convention: cls (not self) refers to the class itself.
        Used as alternative constructors.
        """
        all_words = set()
        for text in corpus:
            all_words.update(text.lower().split())
        vocab = {word: idx + 4 for idx, word in enumerate(sorted(all_words))}
        # Reserve 0-3 for special tokens
        for i, tok in enumerate(cls.special_tokens):
            vocab[tok] = i
        return cls(vocab)

    @staticmethod
    def clean_text(text: str) -> str:
        """Static method: utility that doesn't need self or cls.
        
        No access to instance or class state.
        Use when the function is related to the class conceptually
        but doesn't need to access any class/instance data.
        """
        import re
        return re.sub(r"[^\w\s]", "", text.lower()).strip()


corpus = ["the cat sat on the mat", "the dog ran fast", "cats and dogs"]
tokenizer = Tokenizer.from_corpus(corpus)
print(f"Vocab size: {len(tokenizer.vocab)}")
print(f"Encode 'the cat': {tokenizer.encode('the cat')}")
print(f"Clean: '{Tokenizer.clean_text('Hello, World!!')}'")

# ============================================================
# 3. Properties — Controlled Attribute Access
# ============================================================
print("\n=== 3. Properties ===")

class TrainingRun:
    """Manages a single model training run."""

    def __init__(self, run_id: str, epochs: int = 10):
        self._run_id = run_id
        self._epochs = epochs
        self._metrics: list[dict] = []

    @property
    def run_id(self) -> str:
        """Read-only property (no setter defined)."""
        return self._run_id

    @property
    def epochs(self) -> int:
        return self._epochs

    @epochs.setter
    def epochs(self, value: int):
        """Setter with validation."""
        if not isinstance(value, int) or value < 1:
            raise ValueError(f"epochs must be a positive int, got {value!r}")
        self._epochs = value

    @property
    def best_loss(self) -> float | None:
        """Computed property — no stored value."""
        if not self._metrics:
            return None
        return min(m["loss"] for m in self._metrics)

    def log_epoch(self, loss: float, accuracy: float) -> None:
        self._metrics.append({
            "epoch": len(self._metrics) + 1,
            "loss": loss,
            "accuracy": accuracy,
        })

    def __repr__(self) -> str:
        return f"TrainingRun(run_id={self._run_id!r}, epochs={self._epochs})"


run = TrainingRun("run_001", epochs=5)
run.log_epoch(0.842, 0.61)
run.log_epoch(0.523, 0.77)
run.log_epoch(0.391, 0.85)

print(repr(run))
print(f"Best loss: {run.best_loss:.3f}")

try:
    run.run_id = "overwrite"  # should fail — no setter
except AttributeError as e:
    print(f"Read-only property: {e}")

run.epochs = 10  # valid setter
print(f"Updated epochs: {run.epochs}")

# ============================================================
# 4. Magic Methods (__str__, __len__, __eq__)
# ============================================================
print("\n=== 4. Magic / Dunder Methods ===")

class Dataset:
    """Represents a labeled text dataset."""

    def __init__(self, name: str, records: list[dict]):
        self.name = name
        self._records = records

    def __len__(self) -> int:
        """Called by len(dataset)."""
        return len(self._records)

    def __getitem__(self, index: int) -> dict:
        """Called by dataset[0]."""
        return self._records[index]

    def __repr__(self) -> str:
        """Unambiguous representation for devs."""
        return f"Dataset(name={self.name!r}, size={len(self)})"

    def __str__(self) -> str:
        """Human-readable representation."""
        return f"[{self.name}] — {len(self)} samples"

    def __contains__(self, text: str) -> bool:
        """Called by 'word' in dataset."""
        return any(r["text"] == text for r in self._records)


records = [
    {"id": 1, "text": "great model", "label": "positive"},
    {"id": 2, "text": "bad results", "label": "negative"},
    {"id": 3, "text": "average performance", "label": "neutral"},
]
ds = Dataset("SentimentV1", records)

print(repr(ds))
print(str(ds))
print(f"Length: {len(ds)}")
print(f"First item: {ds[0]}")
print(f"'great model' in ds: {'great model' in ds}")
print(f"'missing' in ds: {'missing' in ds}")

print("\nDay 18 complete! Classes are the building blocks of every ML framework.")
