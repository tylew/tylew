import urllib
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
from final import SmallLanguageModel, Trainer

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

if not torch.cuda.is_available():
    print("WARNING: A GPU was not detected. Running on CPU only.")
    print("TRAINING MAY BE SLOW.")
    print("If you're in a notebook, go to Runtime -> Change runtime type -> Hardware accelerator -> GPU")
    print("If you're running this locally, make sure you have a Nvidia GPU and that PyTorch is installed with GPU support.")
    print("Run the following command:\n pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    print()

def sample(model, length):
    # Text samples your model will be used to complete.
    inputs = ["I must inquire for that which is",
              "There is truth to be had in the ",
              "Here be dragons, here be wisdom,",
              "The world is a stage, and we are",
              "I like cats, I think they are go"]
    
    # Convert the input to a tensor of ascii values
    input = torch.tensor([[ord(c) for c in line] for line in inputs]).to(device)
    output = []

    for i in range(length):
        output = model(input[:, -32:])
        output = output.squeeze(0)

        # Sample the next character. Softmax converts the output to a probability distribution.
        probs = F.softmax(output, dim=-1)
        out_tokens = []

        for i in range(len(probs)):
            # We use multinomial to sample from this distribution.
            out_tokens.append(torch.multinomial(probs[i], 1))

        out_tokens = torch.stack(out_tokens)
        input.data = torch.cat([input.data, out_tokens], dim=1)

    # Convert the output to a string for printing. The if-else is to clean up garbled text a bit.
    return [''.join([chr(c) if 32 <= c <= 126 or c == 10 else "?" for c in s]) for s in input]

# Download the tiny shakespeare dataset
url = 'https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt'
urllib.request.urlretrieve(url, 'input.txt')

# Load the dataset
with open('input.txt', 'r') as f:
    text = f.read()

print("Initializing the model, using the student's model definition...")
model = SmallLanguageModel().to(device)
print("Model loaded successfully")
trainer = Trainer(shakespeare_data=text)
print("Trainer loaded successfully")

# Train the model
for epoch in range(30):
    print("Sampling some text completions from the model. I've written a function that generates text completions for you, one token at a time, using your model.")
    print("A randomly initialized model, or a model that hasn't learned anything, will produce gibberish.")
    generated_sentences = sample(model, 256)
    
    for i, sentence in enumerate(generated_sentences):
        model.eval() # Put the model into evaluation mode in case there's dropout layers.
        print("-" * 80)
        print(f"Completion {i+1}:")
        print(sentence)
        print("=" * 80)
    
    print("Training the model for an epoch, using the student's trainer. This may take some time.")
    model.train() # Put the model back into training mode in case dropout is being used.
    trainer.train(model)
    print("=" * 80)
