<<<<<<< Updated upstream
=======
# import torch
# from torchvision import datasets, transforms

# class CIFAR10:
#     def __init__(self, data_dir, train=True, transform=None):
#         self.classes = [f'Class {i}' for i in range(10)]

#         # Use the provided transform or default to ToTensor()
#         if transform is None:
#             self.transform = transforms.ToTensor()
#         else:
#             self.transform = transform

#         # Load the dataset
#         self.imagesset = self.load_data(data_dir, train)

#     def load_data(self, dir, train):
#         # Use the transform assigned in __init__
#         dataset = datasets.CIFAR10(root=dir, train=train, download=True, transform=self.transform)
#         return dataset
'''
# Usage example
data_dir = './data'
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

cifar10_loader = CIFAR10(data_dir=data_dir, train=True, transform=transform)
'''
>>>>>>> Stashed changes
import pickle
import os
from os.path import join, exists
import numpy as np
import torch
<<<<<<< Updated upstream
from torch.utils.data import Dataset
from torchvision import datasets
from PIL import Image
=======
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, transforms
from PIL import Image
import requests
>>>>>>> Stashed changes

class CIFAR10Dataset(Dataset):

    def __init__(self, data_dir, train=True, transform=None):
        """
        Initializes the dataset for Kuzushiji-49.
        :param data_dir: Directory where the dataset is/will be stored.
        :param train: Boolean indicating if the dataset is for training or testing.
        :param transform: Transformations to apply to the images.
        """
        self.classes = [f'Class {i}' for i in range(49)]
        self.transform = transform
        self.images, self.labels = self.load_data(data_dir, train)

    @staticmethod
    def unpickle(file):
        """
        unpickles cifar batches from the encoded files. Code from
        https://www.cs.toronto.edu/~kriz/cifar.html
        :param file:
        :return:
        """
        with open(file, 'rb') as fo:
            dict = pickle.load(fo, encoding='bytes')
        return dict
                
    def download_dataset(self, data_dir):
        """
        Downloads the dataset files if they are not already in the data_dir.
        """
        datasets.CIFAR10(root=data_dir, train=True, download=True, transform=self.transform)
        datasets.CIFAR10(root=data_dir, train=False, download=True, transform=self.transform)
    
    def load_data(self, data_dir, train):
        """
        the data comes in batches. So this function concatenates the data from the batches
        :param direc: directory where the batches are located
        :return:
        """

        self.download_dataset(data_dir)

        data_dir += '/cifar-10-batches-py'

        assert exists(data_dir), "directory does not exist"
        images,labels = [], []
        for filename in os.listdir(data_dir):
            if filename[:5] == 'data_' or filename[:5] == 'test_':
                data = self.unpickle(join(data_dir, filename))
                images.append(data[b'data'].reshape((10000,3,32,32)))
                labels += data[b'labels']
        assert images, "No data was found in '%s'. Are you sure the CIFAR10 data is there?"%data_dir

        # images = np.concatenate(images, 0)
        # images = np.transpose(images, (0,2,3,1)).astype(np.float32)
        images = np.concatenate(images, 0)
        images = np.transpose(images, (0,2,3,1)).astype(np.float32)
        images /= 255.0  # Normalize to [0, 1]
<<<<<<< Updated upstream
        
=======
>>>>>>> Stashed changes
        return images,labels

    def __len__(self):
        """
        Returns the size of the dataset.
        """
        return len(self.labels)

    def __getitem__(self, idx):
        """
        Returns a sample from the dataset at the specified index.
        """
        image = Image.fromarray(self.images[idx])
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label
