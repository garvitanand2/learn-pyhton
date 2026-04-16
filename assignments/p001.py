# Create variables to describe an AI model configuration. Store and print the following:

# Model name (string)
# Number of parameters in billions (float)
# Context window size in tokens (int)
# Whether it supports vision (bool)
# Fine-tune checkpoint path (set to None if not fine-tuned)
# Expected output (example):

# Sample Output:
# Model     : Gemini-Pro
# Params    : 7.0B
# Context   : 8192 tokens
# Vision    : True
# Checkpoint: None


model_name = "Gemini-Pro";
params = 7.0; # in billions
context_window_size = 8192; # in tokens
supports_vision = True;
fine_tune_checkpoint_path = None;

print(f"Model     : {model_name}");
print(f"Params    : {params}B");
print(f"Context   : {context_window_size} tokens");
print(f"Vision    : {supports_vision}");
print(f"Checkpoint: {fine_tune_checkpoint_path}");
