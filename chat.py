
# import random
# import json
# import torch
# from model import NeuralNet
# from nltk_utils import bag_of_words, tokenize

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# # Load intents data
# with open('intents.json', 'r') as f:
#     intents = json.load(f)

# FILE = "data.pth"
# # Load model data with weights_only set to True
# data = torch.load(FILE, weights_only=True)

# # Print keys to debug
# print("Keys in loaded data:", data.keys())

# # Check if the necessary keys are present
# if not all(key in data for key in ["input_size", "hidden_size", "output_size", "all_words", "tags", "model_state"]):
#     raise KeyError("One or more required keys are missing from the data.pth file.")


# model_state = data["model_state"]
# input_size = data["input_size"]

# output_size = data["output_size"]
# hidden_size = data["hidden_size"]
# all_words = data["all_words"]
# tags = data["tags"]


# # Initialize the model
# model = NeuralNet(input_size, hidden_size, output_size)
# model.load_state_dict(model_state)
# model.eval()

# # Implement our chatbot
# bot_name = "BOT"

# def get_response(msg):
#     # Tokenize the input sentence
#     sentence = tokenize(msg)
#     X = bag_of_words(sentence, all_words)
#     # Reshape the input
#     X = X.reshape(1, X.shape[0])
#     X = torch.from_numpy(X).to(device)  # Move input to the correct device
#     output = model(X)
#     _, predicted = torch.max(output, dim=1)
#     tag = tags[predicted.item()]
    
#     # Calculate probabilities using softmax
#     probs = torch.softmax(output, dim=1)
#     prob = probs[0][predicted.item()]
    
#     if prob.item() > 0.75:
#         # Check if the tag matches
#         for intent in intents["intents"]:
#             if tag == intent["tag"]:
#                 # Possible response
#                 return random.choice(intent['responses'])
            
#     return "I do not understand..."


# if __name__=="__main__":
#     print("Let's chat : type 'quit' to exit")
#     while True:
#         sentence = input("You: ")
#         if sentence == "quit":
#             break

#         resp = get_response(sentence)
#         print(resp)


import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return "I do not understand..."


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)
