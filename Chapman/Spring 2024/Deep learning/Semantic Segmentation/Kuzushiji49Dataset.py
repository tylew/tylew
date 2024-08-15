import os
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import requests

class Kuzushiji49Dataset(Dataset):

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
    def download_file(url, dest_path):
        """
        Downloads a file from the given URL to the specified destination path without using tqdm for progress tracking.
        """
        response = requests.get(url, stream=True)

        if not os.path.exists('./data/k49'):
            os.makedirs('./data/k49')

        with open(dest_path, 'wb') as file:
            for data in response.iter_content(1024):  # Read the data in 1KB chunks
                file.write(data)
                
    def download_dataset(self, data_dir):
        """
        Downloads the dataset files if they are not already in the data_dir.
        """
        urls = [
            'http://codh.rois.ac.jp/kmnist/dataset/k49/k49-train-imgs.npz',
            'http://codh.rois.ac.jp/kmnist/dataset/k49/k49-train-labels.npz',
            'http://codh.rois.ac.jp/kmnist/dataset/k49/k49-test-imgs.npz',
            'http://codh.rois.ac.jp/kmnist/dataset/k49/k49-test-labels.npz'
        ]
        for url in urls:
            filename = url.split('/')[-1]
            filepath = os.path.join(data_dir, filename)
            
            if not os.path.exists(filepath):
                print(f"Downloading {filename}...")
                self.download_file(url, filepath)
            else:
                print('Files already downloaded and verified (KMNIST)')
    
    def load_data(self, data_dir, train):
        """
        Loads data from disk, downloading it if necessary.
        """
        self.download_dataset(data_dir)
        prefix = 'train' if train else 'test'
        images = np.load(os.path.join(data_dir, f'k49-{prefix}-imgs.npz'))['arr_0']
        labels = np.load(os.path.join(data_dir, f'k49-{prefix}-labels.npz'))['arr_0']
        return images, labels

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
