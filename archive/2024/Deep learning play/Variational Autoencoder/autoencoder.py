# %% [markdown]
# Below is an implementation of an autoencoder written in PyTorch. We apply it to the MNIST dataset.

# %%
import torch
torch.manual_seed(0)
import torch.nn as nn
import torch.nn.functional as F
import torch.utils
import torch.distributions
import torchvision
import numpy as np
import matplotlib.pyplot as plt 

# %%
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# %%
class Encoder(nn.Module):
    def __init__(self, latent_dims):
        super(Encoder, self).__init__()
        self.linear1 = nn.Linear(784, 512)
        self.linear2 = nn.Linear(512, latent_dims)

    def forward(self, x):
        x = torch.flatten(x, start_dim=1)
        x = self.linear1(x)
        x = F.relu(x)
        x = self.linear2(x)
        return x

# %%
class Decoder(nn.Module):
    def __init__(self, latent_dims):
        super(Decoder, self).__init__()
        self.linear1 = nn.Linear(latent_dims, 512)
        self.linear2 = nn.Linear(512, 784)

    def forward(self, z):
        z = self.linear1(z)
        z = F.relu(z)
        z = self.linear2(z)
        z = torch.sigmoid(z)
        return z.reshape((-1, 1, 28, 28))

# %%
class Autoencoder(nn.Module):
    def __init__(self, latent_dims):
        super(Autoencoder, self).__init__()
        self.encoder = Encoder(latent_dims)
        self.decoder = Decoder(latent_dims)

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)

# %%
def train(autoencoder, data, epochs=20):
    opt = torch.optim.Adam(autoencoder.parameters())
    for epoch in range(epochs):
        for x, y in data:
            x = x.to(device) # GPU
            opt.zero_grad()
            x_hat = autoencoder(x)
            loss = ((x - x_hat)**2).sum()
            loss.backward()
            opt.step()
    return autoencoder

# %%
latent_dims = 2
autoencoder = Autoencoder(latent_dims).to(device) # GPU

data = torch.utils.data.DataLoader(
        torchvision.datasets.MNIST('./data',
               transform=torchvision.transforms.ToTensor(),
               download=True),
        batch_size=128,
        shuffle=True)

autoencoder = train(autoencoder, data)

# %%
def plot_latent(autoencoder, data, num_batches=100, save_path='latent_plot.png'):
    plt.figure(figsize=(10, 8))  # Optional: specify figure size
    for i, (x, y) in enumerate(data):
        z = autoencoder.encoder(x.to(device))
        z = z.to('cpu').detach().numpy()
        plt.scatter(z[:, 0], z[:, 1], c=y, cmap='tab10')
        if i >= num_batches:
            plt.colorbar()
            plt.savefig(save_path)  # Save the figure
            plt.close()  # Close the figure to free memory
            break

# %%
plot_latent(autoencoder, data)

# %%
def plot_reconstructed(autoencoder, r0=(-5, 10), r1=(-10, 5), n=12, save_path='reconstruction_plot.png'):
    w = 28
    img = np.zeros((n*w, n*w))
    for i, y in enumerate(np.linspace(*r1, n)):
        for j, x in enumerate(np.linspace(*r0, n)):
            z = torch.Tensor([[x, y]]).to(device)
            x_hat = autoencoder.decoder(z)
            x_hat = x_hat.reshape(28, 28).to('cpu').detach().numpy()
            img[(n-1-i)*w:(n-1-i+1)*w, j*w:(j+1)*w] = x_hat
    plt.figure(figsize=(10, 8))  # Optional: specify figure size
    plt.imshow(img, extent=[*r0, *r1])
    plt.savefig(save_path)  # Save the figure
    plt.close()  # Close the figure to free memory


# %%
plot_reconstructed(autoencoder)


