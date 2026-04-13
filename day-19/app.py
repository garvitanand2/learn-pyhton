# Day 19: OOP Advanced — Inheritance & Polymorphism
# Focus: Building class hierarchies for extensible AI systems

# ============================================================
# WHAT: Inheritance lets a class *extend* another class,
#       inheriting all its attributes and methods while
#       adding or overriding behavior.
# WHY:  PyTorch's nn.Module, sklearn's BaseEstimator, and
#       every major ML framework is built on inheritance.
#       Understanding it means you can read framework source
#       code and build your own extensions.
# ============================================================

# ============================================================
# 1. Single Inheritance
# ============================================================
print("=== 1. Single Inheritance ===")

class BaseModel:
    """Abstract base for all model types."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.is_trained = False

    def train(self, data: list) -> None:
        """Default training logic (can be overridden)."""
        print(f"  [{self.model_name}] Training on {len(data)} samples...")
        self.is_trained = True

    def predict(self, text: str) -> str:
        """Must be implemented by subclasses."""
        raise NotImplementedError(
            f"{type(self).__name__} must implement predict()"
        )

    def save(self, path: str) -> None:
        import json
        checkpoint = {"model_name": self.model_name, "is_trained": self.is_trained}
        print(f"  Saved checkpoint to {path}")

    def __repr__(self) -> str:
        status = "trained" if self.is_trained else "untrained"
        return f"{type(self).__name__}(name={self.model_name!r}, status={status})"


class SentimentClassifier(BaseModel):
    """Classifies text as positive / negative / neutral."""

    def __init__(self, model_name: str, threshold: float = 0.5):
        super().__init__(model_name)   # ← always call super().__init__()
        self.threshold = threshold    # new attribute specific to this class
        self._word_scores: dict[str, float] = {}

    def train(self, data: list) -> None:
        """Override: custom training logic."""
        super().train(data)           # still runs BaseModel.train()

        # Build simple word scoring
        positive_words = {"great", "excellent", "fantastic", "best", "love", "perfect"}
        negative_words = {"bad", "poor", "terrible", "awful", "worst", "hate"}
        for word in positive_words:
            self._word_scores[word] = 1.0
        for word in negative_words:
            self._word_scores[word] = -1.0
        print(f"  [{self.model_name}] Built vocab of {len(self._word_scores)} words")

    def predict(self, text: str) -> str:
        """Override: sentiment prediction."""
        words = text.lower().split()
        score = sum(self._word_scores.get(w, 0) for w in words)
        if score > self.threshold:
            return "positive"
        elif score < -self.threshold:
            return "negative"
        else:
            return "neutral"


# Usage
train_data = ["great results", "bad performance", "neutral baseline"]
clf = SentimentClassifier("lexicon-v1", threshold=0.3)
clf.train(train_data)

test_cases = ["great and fantastic", "terrible and awful", "average baseline"]
for text in test_cases:
    print(f"  '{text}' → {clf.predict(text)}")

# ============================================================
# 2. Polymorphism — Same interface, different behaviors
# ============================================================
print("\n=== 2. Polymorphism ===")

class KeywordClassifier(BaseModel):
    """Rule-based classifier using keyword matching."""

    def __init__(self, rules: dict[str, list[str]]):
        super().__init__("keyword-clf")
        self.rules = rules  # {"positive": ["good", "great"], ...}

    def predict(self, text: str) -> str:
        text_lower = text.lower()
        for label, keywords in self.rules.items():
            if any(kw in text_lower for kw in keywords):
                return label
        return "neutral"

class ZeroShotClassifier(BaseModel):
    """Simulates a zero-shot model (no training needed)."""

    def __init__(self):
        super().__init__("zero-shot-sim")
        self.is_trained = True  # zero-shot doesn't need training

    def predict(self, text: str) -> str:
        # Simulate: return label based on string length (demo only)
        length = len(text.split())
        return "positive" if length > 5 else "negative"


# All models share the same interface — this is polymorphism
rules = {"positive": ["great", "excellent"], "negative": ["bad", "poor"]}
models: list[BaseModel] = [
    clf,                            # SentimentClassifier
    KeywordClassifier(rules),       # KeywordClassifier
    ZeroShotClassifier(),           # ZeroShotClassifier
]

test_text = "great and excellent performance"
print(f"  Test: '{test_text}'")
for model in models:
    print(f"  {type(model).__name__:<25} → {model.predict(test_text)}")

# ============================================================
# 3. super() — Calling Parent Methods
# ============================================================
print("\n=== 3. super() ===")

class PreprocessingModel(SentimentClassifier):
    """Adds preprocessing before prediction."""

    def __init__(self, model_name: str):
        super().__init__(model_name)  # calls SentimentClassifier.__init__
        self.preprocessing_steps = []

    def add_preprocessing(self, fn) -> "PreprocessingModel":
        """Adds a preprocessing function. Returns self for chaining."""
        self.preprocessing_steps.append(fn)
        return self

    def predict(self, text: str) -> str:
        # Apply preprocessing first
        for step in self.preprocessing_steps:
            text = step(text)
        return super().predict(text)  # calls SentimentClassifier.predict


# Build preprocessing pipeline
model = PreprocessingModel("sentiment-preprocessed")
model.train(train_data)
model.add_preprocessing(str.lower).add_preprocessing(str.strip)

print(f"  Prediction: {model.predict('  GREAT Performance  ')}")

# ============================================================
# 4. Mixins — Composing Behavior
# ============================================================
print("\n=== 4. Mixins ===")

class LoggingMixin:
    """Adds logging capability to any class."""

    def log(self, message: str, level: str = "INFO") -> None:
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"  [{ts}] [{level}] [{type(self).__name__}] {message}")

class SerializableMixin:
    """Adds JSON serialization to any class."""

    def to_dict(self) -> dict:
        """Override in concrete classes."""
        raise NotImplementedError

    def to_json(self) -> str:
        import json
        return json.dumps(self.to_dict(), indent=2)


class RobustClassifier(BaseModel, LoggingMixin, SerializableMixin):
    """Classifier with logging and serialization built in."""

    def __init__(self, model_name: str):
        super().__init__(model_name)

    def predict(self, text: str) -> str:
        self.log(f"Predicting for input: '{text[:30]}'")
        label = "positive" if "good" in text else "negative"
        self.log(f"Result: {label}")
        return label

    def to_dict(self) -> dict:
        return {"model_name": self.model_name, "is_trained": self.is_trained}


rc = RobustClassifier("robust-v1")
result = rc.predict("good model performance")
print(f"  JSON: {rc.to_json()}")

# ============================================================
# 5. isinstance() and issubclass()
# ============================================================
print("\n=== 5. isinstance / issubclass ===")

print(f"clf is BaseModel:         {isinstance(clf, BaseModel)}")
print(f"clf is SentimentClf:      {isinstance(clf, SentimentClassifier)}")
print(f"SentimentCLF -> BaseModel:{issubclass(SentimentClassifier, BaseModel)}")
print(f"str is int subclass:      {issubclass(str, int)}")

print("\nDay 19 complete! Inheritance enables scalable, extensible AI systems.")
