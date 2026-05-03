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

def AI_model_configuration():
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

AI_model_configuration();

# Exercise 2: Type Conversion
# You receive raw data from a config file as strings. Convert them to the correct types:

# raw_data = {
#     "learning_rate": "0.0003",
#     "epochs": "50",
#     "model_name": "transformer_v2",
#     "use_dropout": "True",
#     "dropout_rate": "0.2"
# }
# Convert learning_rate and dropout_rate to float
# Convert epochs to int
# Convert use_dropout to bool (hint: "True" as a string is always truthy — think about this!)
# Print each converted value with its type
# Bonus: What's wrong with bool("False")? Fix it correctly.
raw_data = {
    "learning_rate": "0.0003",
    "epochs": "50",
    "model_name": "transformer_v2",
    "use_dropout": "True",
    "dropout_rate": "0.2"
}
print(f"Original learning_rate: {raw_data['learning_rate']} (type: {type(raw_data['learning_rate'])})");
print(f"Original epochs: {raw_data['epochs']} (type: {type(raw_data['epochs'])})");
print(f"Original use_dropout: {raw_data['use_dropout']} (type: {type(raw_data['use_dropout'])})");
print(f"Original dropout_rate: {raw_data['dropout_rate']} (type: {type(raw_data['dropout_rate'])})");
learning_rate = float(raw_data["learning_rate"]);
epochs = int(raw_data["epochs"]);
use_dropout = raw_data["use_dropout"] == "True"; # This will correctly convert "True" to True and "False" to False
dropout_rate = float(raw_data["dropout_rate"]);
print(f"Converted learning_rate: {learning_rate} (type: {type(learning_rate)})");
print(f"Converted epochs: {epochs} (type: {type(epochs)})");
print(f"Converted use_dropout: {use_dropout} (type: {type(use_dropout)})");
print(f"Converted dropout_rate: {dropout_rate} (type: {type(dropout_rate)})");


# Exercise 3 — Token Budget Calculator
# An LLM has a context window of 4096 tokens.

# System prompt uses 150 tokens
# User message uses 320 tokens
# Model response is allowed the rest
# Calculate and print:

# Tokens used so far (system + user)
# Tokens remaining for the response
# Percentage of context window used (as a float, rounded to 2 decimal places)
# Whether the conversation is under 50% context usage (bool)

context_window = 4096;
system_prompt_tokens = 150;
user_message_tokens = 320;
tokens_used = system_prompt_tokens + user_message_tokens;
tokens_remaining = context_window - tokens_used;
percentage_used = (tokens_used / context_window) * 100;
under_50_percent = percentage_used < 50;
print(f"Tokens used so far: {tokens_used}");
print(f"Tokens remaining for the response: {tokens_remaining}");
print(f"Percentage of context window used: {percentage_used}%");
print(f"Is the conversation under 50% context usage? {under_50_percent}");


# Exercise 4 — String Exploration
# Given the string:

# text = "Large Language Models are transforming the AI industry."
# Without importing any library, find:

# Total number of characters (including spaces)
# Number of words (hint: .split())
# Whether "AI" appears in the text (bool)
# The first 5 characters
# The text in UPPERCASE

text = "Large Language Models are transforming the AI industry."
total_characters = len(text);
words = text.split(" ");
number_of_words = len(words);
contains_AI = "AI" in text;
first_five_characters = text[:5];
uppercase_text = text.upper();
print(f"Total number of characters: {total_characters}");
print(f"Words: {words}");
print(f"Number of words: {number_of_words}");
print(f"Does 'AI' appear in the text? {contains_AI}");
print(f"First 5 characters: '{first_five_characters}'");        
print(f"Text in UPPERCASE: '{uppercase_text}'");


# Exercise 5 — Identity Puzzle (Interview-Focused)
# Predict the output of each line before running it. Then verify:

# a = 256
# b = 256
# print(a is b)   # ?

# c = 257
# d = 257
# print(c is d)   # ?

# x = None
# y = None
# print(x is y)   # ?

# p = "hello"
# q = "hello"
# print(p is q)   # ?  (string interning — research this!)
# Explain in a comment WHY each result is what it is.


a = 256
b = 256
print(a is b)   # True, because small integers (from -5 to 256) are cached by Python and point to the same memory location.

c = 257
d = 257
print(c is d)   # False, because integers outside the range of -5 to 256 are not cached, so c and d point to different memory locations.

x = None
y = None
print(x is y)   # True, because None is a singleton in Python, meaning there is only one instance of None in memory, so x and y point to the same location.

p = "hello"
q = "hello"
print(p is q)   # True, because strings that are identical and are valid identifiers are interned by Python, meaning they point to the same memory location.