import matplotlib.pyplot as plt
import numpy as np
import os
from os.path import join, exists

from CIFAR10Dataset import CIFAR10Dataset
from Kuzushiji49Dataset import Kuzushiji49Dataset

def generate_plot(X, fn = 'plot.png'):
    """
    Generic function to plot the images in a grid
    of num_plot x num_plot
    :param X:
    :return:
    """
    print(f'generating plot {fn}')
    plt.figure()
    num_plot = 5
    f, ax = plt.subplots(num_plot, num_plot)
    for i in range(num_plot):
        for j in range(num_plot):
            idx = np.random.randint(0, X.shape[0])
            ax[i,j].imshow(X[idx])
            # ax[i, j].imshow(X[idx], cmap='gray', interpolation='none')
            ax[i,j].get_xaxis().set_visible(False)
            ax[i,j].get_yaxis().set_visible(False)
    f.subplots_adjust(hspace=0.1)  #No horizontal space between subplots
    f.subplots_adjust(wspace=0)

    plt.savefig(fn, dpi=300)  # Save as PNG with high resolution
    plt.close()

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


        # print(len(X_cifar))

    def sample(self, batch_size, norm=True, dataset='train'):
        """
        Samples a batch of data by randomly inserting MNIST images into CIFAR images.
        :param batch_size: The number of samples in the batch.
        :param norm: Indicates whether to normalize the data or not.
        :param dataset: Specifies the dataset partition to use ('train' or 'test').
        :return: A tuple of (modified CIFAR images, segmentation maps).
        """
        assert dataset in ['train', 'test']
        
        # Randomly select indices for CIFAR and MNIST images
        idx_cifar = np.random.choice(self.data['cifar'][dataset].shape[0], batch_size, replace=False)
        idx_mnist = np.random.choice(self.data['mnist'][dataset].shape[0], batch_size, replace=False)
        
        # Extract the selected CIFAR and MNIST images
        im_cifar = self.data['cifar'][dataset][idx_cifar]
        im_mnist = self.data['mnist'][dataset][idx_mnist][:, ::2, ::2]
        
        # generate_plot(im_mnist, fn='fff.png')
        size_mnist = 14  # Size of the MNIST images
        
        # Create a mask for MNIST images where the pixel value is greater than a threshold
        mnist_mask = np.greater(im_mnist, 0.3).astype(np.float32)
        
        # Apply the mask to MNIST images
        im_mnist = im_mnist * mnist_mask
        
        # Random positions where MNIST images will be inserted in CIFAR images
        width_start = np.random.randint(0, 32 - size_mnist, size=batch_size)
        height_start = np.random.randint(0, 32 - size_mnist, size=batch_size)
        
        # Initialize segmentation maps
        segm_maps = np.zeros((batch_size, 32, 32, 3), dtype=np.float32)

        for i in range(batch_size):
            # Position for MNIST image to be inserted
            h_pos, w_pos = height_start[i], width_start[i]

            # Create an overlay image that is initially zeros (black)
            overlay_img = np.zeros((32, 32, 3), dtype=np.float32)
            
            # Place the MNIST image within the overlay image at the specified position
            overlay_img[h_pos:h_pos+size_mnist, w_pos:w_pos+size_mnist, :] = np.repeat(im_mnist[i][:, :, np.newaxis], 3, axis=2)
            
            # Update segmentation map
            segm_maps[i] = overlay_img

            # Overlay the MNIST image onto the CIFAR image
            # This adds the overlay if the pixel value in MNIST is greater than 0 (using the mask)
            im_cifar[i] = np.where(overlay_img > 0, [.2, .2, .2], im_cifar[i])
        
        if norm:
            im_cifar = (im_cifar-130.)/70.

        generate_plot(im_cifar)
        generate_plot(segm_maps, fn='segm.png')

        return im_cifar, segm_maps




if __name__ == "__main__":
    dg = Datagen()
    data, segm_maps = dg.sample(32)
    # generate_plot(data)
    