import torch
from torch.utils.data import random_split
from torch.utils.data import DataLoader
from torch.optim import Adam
from torch import nn
import numpy as np
import time
import matplotlib.pyplot as plt

from datagenerator import Datagen
from model import Model

# define hyperparameters 
INIT_LR = 1e-3
DROPOUT = .2
BATCH_SIZE = 64
EPOCHS = 10
TRAIN_COUNT = 50000
TRAIN_SPLIT = 0.75
TEST_COUNT = 5000

# set the device we will be using to train the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Print the selected device
print("Selected PyTorch device:", device)

# load datasets train/validation
dataGenerator = Datagen()
trainData = dataGenerator.sample(batch_size=TRAIN_COUNT, dataset='train')
testData = dataGenerator.sample(batch_size=TEST_COUNT, dataset='test')

# Calculate the number of samples for training and validation
numTrainSamples = int(len(trainData) * TRAIN_SPLIT)
numValSamples = len(trainData) - numTrainSamples

# Apply random_split 
trainDataSplit, valDataSplit = random_split(
        trainData, 
        [numTrainSamples, numValSamples], 
        generator=torch.Generator().manual_seed(42)
    )

# Initialize the train, validation, and test data loaders
trainDataLoader = DataLoader(trainDataSplit, batch_size=BATCH_SIZE, shuffle=True)
valDataLoader = DataLoader(valDataSplit, batch_size=BATCH_SIZE, shuffle=False)
testDataLoader = DataLoader(testData, batch_size=BATCH_SIZE, shuffle=False)



print("[INFO] Data setup complete.")


# initilize model
model = Model(inChannels=3,dropout=DROPOUT).to(device)

# initialize optimizer and loss function
opt = Adam(model.parameters(), lr=INIT_LR)
lossFn = nn.CrossEntropyLoss()

# begin training loop
startTime = time.time()

# Initialize the TRAIN_HISTORY dictionary
TRAIN_HISTORY = {
    "train_loss": [],
    "val_loss": [],
    "mIoU": [] 
}


# loop over epochs
for e in range(0, EPOCHS):
    # set the model in training mode
    model.train()
    # initialize the total training and validation loss
    totalTrainLoss = 0
    totalValLoss = 0
    # initialize the total intersection and union for mIoU calculation
    total_intersection = 0
    total_union = 0
    
    # loop over the training set
    for (x, y) in trainDataLoader:

        # print(x.shape)
        # print(y.shape)
        # send the input to the device
        (x, y) = (x.to(device), y.to(device))
        # perform a forward pass and calculate the training loss
        pred = model(x)
        loss = lossFn(pred, y)
        # zero out the gradients, perform the backpropagation step,
        # and update the weights
        opt.zero_grad()
        loss.backward()
        opt.step()
        # add the loss to the total training loss so far
        totalTrainLoss += loss.item()
        
        # Calculate Intersection over Union for mIoU
        intersection = torch.logical_and(pred > 0.5, y > 0.5).sum().item()
        union = torch.logical_or(pred > 0.5, y > 0.5).sum().item()
        total_intersection += intersection
        total_union += union

    # switch off autograd for evaluation
    with torch.no_grad():
        # set the model in evaluation mode
        model.eval()
        # loop over the validation set
        for (x, y) in valDataLoader:
            # send the input to the device
            (x, y) = (x.to(device), y.to(device))
            # make the predictions and calculate the validation loss
            pred = model(x)
            totalValLoss += lossFn(pred, y).item()

    # calculate the average training and validation loss
    avgTrainLoss = totalTrainLoss / len(trainDataLoader)
    avgValLoss = totalValLoss / len(valDataLoader)
    # calculate the Mean Intersection over Union (mIoU)
    mIoU = total_intersection / total_union
    # update training history
    TRAIN_HISTORY["train_loss"].append(avgTrainLoss)
    TRAIN_HISTORY["val_loss"].append(avgValLoss)
    TRAIN_HISTORY["mIoU"].append(mIoU)
    # print the model training and validation information
    print("[INFO] EPOCH: {}/{}".format(e + 1, EPOCHS))
    print("Train loss: {:.6f}, Validation loss: {:.6f}".format(
        avgTrainLoss, avgValLoss))
    print("Mean Intersection over Union (mIoU): {:.4f}".format(mIoU))
    print()

print("[INFO] Completed training.")

# measure how long training took
endTime = time.time()
print("[INFO] total time taken to train the model: {:.2f}s".format(
	endTime - startTime))


def evaluate_and_visualize_performance(model, testDataLoader, TRAIN_HISTORY, device, lossFn):
    """
    Evaluates the model on the test set, prints the final model segmentation metrics,
    saves a plot of the training performance over epochs, and also saves a plot with
    the 3 best and 3 worst accurate predictions.
    """
    model.eval()  # Set the model to evaluation mode.
    test_losses = []
    predictions_details = []

    with torch.no_grad():
        for x_test, y_test in testDataLoader:
            x_test, y_test = x_test.to(device), y_test.to(device)
            pred_test = model(x_test)
            loss = lossFn(pred_test, y_test)
            test_losses.append(loss.item())

            # Loop through the batch of predictions
            for i in range(len(x_test)):
                # Extract individual predictions and their corresponding truth
                individual_pred = pred_test[i]
                individual_truth = y_test[i]
                individual_image = x_test[i]

                # Calculate a simple accuracy metric per prediction
                # Here we use IoU as an example; adapt it based on your model's specifics
                intersection = torch.logical_and(individual_pred > 0.5, individual_truth > 0.5).float().sum()
                union = torch.logical_or(individual_pred > 0.5, individual_truth > 0.5).float().sum()
                iou = (intersection / union).item() if union > 0 else 0

                predictions_details.append((iou, individual_image.cpu().numpy(), individual_truth.cpu().numpy(), individual_pred.cpu().numpy()))

    # Sort predictions by IoU score.
    predictions_details.sort(key=lambda x: x[0], reverse=True)

    # Select the 3 best and 3 worst predictions.
    best_predictions = predictions_details[:3]
    worst_predictions = predictions_details[-3:]

    # Visualize the best and worst predictions.
    fig, axes = plt.subplots(6, 3, figsize=(15, 25))
    for idx, (iou, img, gt, pred) in enumerate(best_predictions + worst_predictions):
        if idx < 3:
            title_prefix = 'Best'
        else:
            title_prefix = 'Worst'

        ax_img = axes[idx, 0]
        ax_gt = axes[idx, 1]
        ax_pred = axes[idx, 2]

        # Since pred is already a numpy array, directly use it for plotting
        pred_np = pred.squeeze()  # Assuming single-channel output, squeeze it

        ax_img.imshow(img.transpose(1, 2, 0))  # Adjust if your image requires different handling
        ax_img.set_title(f"{title_prefix} {idx%3+1} - Image")
        ax_img.axis('off')

        ax_gt.imshow(gt.squeeze(), cmap='gray')
        ax_gt.set_title(f"{title_prefix} {idx%3+1} - Ground Truth")
        ax_gt.axis('off')

        ax_pred.imshow(pred_np, cmap='gray', vmin=0, vmax=1)  # Ensure proper scaling
        ax_pred.set_title(f"{title_prefix} {idx%3+1} - Prediction")
        ax_pred.axis('off')

    plt.tight_layout()
    plt.savefig('best_worst_predictions_plot.png')
    plt.show()


    # Plot and save training performance.
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(TRAIN_HISTORY['train_loss'], label='Train Loss')
    plt.plot(TRAIN_HISTORY['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss Over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(TRAIN_HISTORY['mIoU'], label='mIoU')
    plt.title('Mean IoU Over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('mIoU')
    plt.legend()

    plt.tight_layout()
    plt.savefig('training_performance_and_accuracy_plot.png')

    plt.show()

# Call the function after training is complete.
evaluate_and_visualize_performance(model, testDataLoader, TRAIN_HISTORY, device, lossFn)


# Print the table header
print("{:<10} | {:<12} | {:<12} | {:<5}".format("Epoch", "Train Loss", "Validation Loss", "mIoU"))

# Print each row of the table
for epoch in range(len(TRAIN_HISTORY["train_loss"])):
    print("{:<10} | {:<12.6f} | {:<12.6f} | {:<5.4f}".format(epoch + 1, 
        TRAIN_HISTORY["train_loss"][epoch], 
        TRAIN_HISTORY["val_loss"][epoch], 
        TRAIN_HISTORY["mIoU"][epoch])
    )