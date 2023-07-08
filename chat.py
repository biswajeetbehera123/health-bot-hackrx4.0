import random
import json

import torch

from Tokenization_and_stemming import tokenize, stem, bag_of_words
from NN_model1 import NeuralNet

FILE = "data.pth"
data = torch.load(FILE)    

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

with open('intents.json', 'r') as f:
    intents = json.load(f)

device = torch.device('cpu')
model = NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "San"


def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
       for intent in intents['intents']:
           if tag == intent['tag']:
               return f"{bot_name}: {random.choice(intent['responses'])}"
    else:
        return f"{bot_name}: Please consult with our consultants. Click at the Help button above to book an appointment."


if __name__ == "__main__":
    print("How can I help you? type 'quit' to exit")
    while True:
        sentence=input("You: ")
        if sentence == "quit":
            break
        
        final_response = get_response((sentence))
        print(final_response)
    
   

