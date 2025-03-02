import random
import json
import torch
import os

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Set device for PyTorch
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents file
try:
    with open('intents.json', 'r') as json_data:
        intents = json.load(json_data)
except FileNotFoundError:
    print("Error: 'intents.json' not found. Make sure the file exists.")
    exit()

# Load trained model
FILE = "data.pth"
if not os.path.exists(FILE):
    print(f"Error: '{FILE}' not found. Train the model first.")
    exit()

data = torch.load(FILE, map_location=device)

# Extract model parameters
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

# Initialize model
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

def get_response(msg):
    """Generates a chatbot response based on user input."""
    try:
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
        return "I'm sorry, I didn't understand that."
    
    except Exception as e:
        print(f"Error in chatbot response: {e}")
        return "Something went wrong. Please try again."

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        response = get_response(user_input)
        print(f"{bot_name}: {response}")
