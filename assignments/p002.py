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

learning_rate = float(raw_data["learning_rate"])
epochs = int(raw_data["epochs"])
model_name = raw_data["model_name"]
use_dropout = raw_data["use_dropout"] == "True"  # This will correctly convert "True" to True and "False" to False
dropout_rate = float(raw_data["dropout_rate"])

print(f"Learning Rate: {learning_rate} (type: {type(learning_rate)})")
print(f"Epochs       : {epochs} (type: {type(epochs)})")
print(f"Model Name   : {model_name} (type: {type(model_name)})")
print(f"Use Dropout  : {use_dropout} (type: {type(use_dropout)})")
print(f"Dropout Rate : {dropout_rate} (type: {type(dropout_rate)})")
