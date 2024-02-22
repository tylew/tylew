import math
import time
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

class ShakespeareDataset(Dataset):
    def __init__(self, data: str):
        """
        Our dataset has two attributes which we initialize here:
        - self.data:
        We convert the dataset (a giant string) into a list of ASCII
        characters.
        For example, "Thou art bloop" becomes [84, 104, 111, 117, 32, 97, 114,
        116, 32, 98, 108, 111, 111, 112]
        - self.seq_length:
        The length of the input sequence we will feed into the model.
        This is analogous to the context window in LLMs / GPT-type models.
        This is used by __getitem__ to return a sequence of 32 characters + a
        33rd character as the target for training.
        """
        self.data = torch.tensor([ord(c) for c in data])
        self.seq_length = 32

    def __len__(self):
        """
        Returns the number of sequences available from our dataset.
        Since we're not using padding, the number of sequences is smaller than the
        length of the dataset.
        """
        return len(self.data) - self.seq_length

    def __getitem__(self, idx):
        """
        Returns a single sequence (32 characters) as the input and the next
        character (the 33rd character) as the target.
        """
        seq = self.data[idx:idx + self.seq_length]
        target = self.data[idx + self.seq_length]
        return seq, target

class Trainer():
    def __init__(self, shakespeare_data: str):
        """
        Our Trainer has one attribute:
        - self.dataloader:
        We use the dataloader to iterate over the dataset in batches.
        First, we create an instance of our Shakespeare Dataset using the
        class defined above.
        Then we can pass in the DataSet to a DataLoader.
        """
        dataset = ShakespeareDataset(shakespeare_data)
        self.dataloader = DataLoader(dataset, batch_size=256, shuffle=True)

    def train(self, model: nn.Module):
        """
        Use the dataloader to iterate over the dataset in batches.
        Pass each batch to the model, retrieve the output, and compute the loss.
        Use the loss to update the model parameters.
        Previously we subtracted out the gradient by hand,
        but you can use AdamW to perform a more efficient version of gradient
        descent for you.
        """
        # TODO: Implement this method
        # raise NotImplementedError("Implement me!")
    
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

        t = time.time()
        for i, batch in enumerate(self.dataloader):
            inputs, targets = batch
            inputs = inputs.to(device)
            targets = targets.to(device)

            optimizer.zero_grad()

            output = model(inputs)
            loss = F.cross_entropy(output,targets)

            optimizer.step()
            if i % 100 == 0:
                print(f'Batch: {i}, Loss: {loss.item()}, Time: {time.time() - t:.4f}')
                t = time.time()


class SmallLanguageModel(nn.Module):
    def __init__(self):
        """
        You should define the layers of your neural network here in __init__.
        In the forward method, you should define how the input is processed by
        these layers to return the output.
        Your init method should begin with super().__init__().
        """
        super(SmallLanguageModel, self).__init__()
        self.embeddings = nn.Embedding(128, 300)
        self.nonlinearity = nn.ReLU()

        self.linear1 = nn.Linear(300 * 32, 500)
        self.norm1 = nn.LayerNorm(500)
        self.classifier = nn.Linear(500,128)
    

    def forward(self, x: torch.Tensor):
        """
        This method defines how the input is processed by the layers to return the
        output.
        x is an input tensor of shape (batch_size, sequence_length)
        Your output should have shape (batch_size, 128), where each batch entry
        lists a probability for each of the 128 possible characters
        Note that you can essentially ignore the batch dimension, since PyTorch
        layers automatically handle it. No need to write for-loops.
        """
        x = self.embeddings(x)
        # x = x.sum(dim=1)
        x = x.reshape(x.shape[0],x.shape[1] * x.shape[2])
        x = self.linear1(x)
        x = self.nonlinearity(x)
        x = self.norm1(x)
        x = self.classifier(x)

        
        return x

