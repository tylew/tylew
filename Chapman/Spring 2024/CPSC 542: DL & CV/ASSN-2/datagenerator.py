import matplotlib.pyplot as plt
import numpy as np

import torch
from torch.utils.data import TensorDataset

from CIFAR10Dataset import CIFAR10Dataset
from Kuzushiji49Dataset import Kuzushiji49Dataset

def display_and_save_images(images_tensor, segm_maps_tensor, filename):
    # Create a plot with 5 rows and 3 columns
    fig, axes = plt.subplots(5, 3, figsize=(10, 15))

    # Loop over each row and plot the test image, ground truth segmentation map, and predicted segmentation map
    for i in range(5):
        axes[i, 0].imshow(images_tensor[i].cpu().numpy().transpose(1, 2, 0))  # Test image
        axes[i, 0].set_title('Test Image')
        axes[i, 1].imshow(segm_maps_tensor[i].cpu().numpy(), cmap='gray')  # Segmentation map
        axes[i, 1].set_title('Segmentation Map')

    # Hide remaining axes
    for j in range(2, 3):
        for i in range(5):
            axes[i, j].axis('off')

    # Adjust layout
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig(filename)
    plt.show()


def split_data(X, ratio=0.60):
    num_samples = X.shape[0]
    ind_split = int(ratio*num_samples)
    permutation = np.random.permutation(num_samples)
    return X[permutation[:ind_split]], X[permutation[ind_split:]]

class Datagen():
    """
    Object to sample the data that we can segment. The sample function combines data
    from MNIST and CIFAR and overlaps them
    """
    def __init__(self):
        
        direc_cifar = CIFAR10Dataset('./data/cifar')
        direc_mnist = Kuzushiji49Dataset('./data/k49')
        ## Unpack the data
        X_cifar, y_cifar = direc_cifar.images, direc_cifar.labels
        X_mnist, y_mnist = direc_mnist.images, direc_mnist.labels

        self.data = {'mnist':{'train':None, 'val':None}, 'cifar':{'train':None, 'val':None}}

        self.data['mnist']['train'], self.data['mnist']['test'] = split_data(X_mnist)
        self.data['cifar']['train'], self.data['cifar']['test'] = split_data(X_cifar)

    def sample(self, batch_size, dataset = 'train'):
        """
        Samples a batch of data. It randomly inserts the MNIST images into cifar images
        :param batch_size:
        :param norm: indicate wether to normalize the data or not
        :return:
        """
        assert dataset in ['train', 'test']
        idx_cifar = np.random.choice(self.data['cifar'][dataset].shape[0], batch_size)
        idx_mnist = np.random.choice(self.data['mnist'][dataset].shape[0], batch_size)
        im_cifar = self.data['cifar'][dataset][idx_cifar]
        im_mnist = self.data['mnist'][dataset][idx_mnist][:, ::2, ::2]
        size_mnist = 14

        # mnist_mask = np.greater(im_mnist, 0.3, dtype = np.float32)
        mnist_mask = np.greater(im_mnist, 0.3).astype(np.float32)
        im_mnist = im_mnist * mnist_mask

        width_start = np.random.randint(0,32-size_mnist,size=(batch_size))
        height_start = np.random.randint(0,32-size_mnist,size=(batch_size))
        
        # expand dimentions of mnist character
        mnist_batch = np.repeat(np.expand_dims((im_mnist), 3), 3, 3)
        
        # define base seg map return variable
        segm_maps = np.zeros((batch_size, 32, 32)).astype(np.float32)

        for i in range(batch_size):
            im_cifar[i, width_start[i]:width_start[i]+size_mnist, height_start[i]:height_start[i]+size_mnist] += mnist_batch[i]
            segm_maps[i, width_start[i]:width_start[i]+size_mnist, height_start[i]:height_start[i]+size_mnist] += mnist_mask[i]
        im_cifar = np.clip(im_cifar, 0.0, 1.0)
        im_cifar = np.transpose(im_cifar, (0,3,1,2)).astype(np.float32)

        images_tensor = torch.tensor(im_cifar, dtype=torch.float32)
        segm_maps_tensor = torch.tensor(segm_maps, dtype=torch.float32)

        return TensorDataset(images_tensor, segm_maps_tensor)


# main for testing and generating examples
if __name__ == "__main__":
    dg = Datagen()
    dataset = dg.sample(32)
    display_and_save_images(dataset.tensors[0], dataset.tensors[1], "images_and_segmaps.png")
    