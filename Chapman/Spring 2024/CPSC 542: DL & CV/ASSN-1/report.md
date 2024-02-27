# CPSC 542: Implement a Convolutional Neural Network – Assignment #1
```
Lewis, T.  
tylewis@chapman.edu
ID# 002366930

02/27/24
```

1. ### Identify a vision dataset to work with for classification tasks:

For assignment completion, I used the **[MNIST dataset (link)](https://www.kaggle.com/datasets/hojjatk/mnist-dataset)**. 

The database contains 70,000 greyscale 28x28px images of handwritten numeric character depictions: 

![Alt text](mnist_examples.png)

The computer vision exposure I have had prior to this assignment/course is using Euclidean Distance K-nearest neighbors to predict labels from this specific dataset. 


2. ### Prove the classification task requires a deep learning solution:

K-Nearest yielded a ~0.9 accuracy, but Convolutional Neural Network (CNN) is vastly advantageous and suitable for the task of classifying the MNIST dataset.

A Deep Learning solution will greatly improve the accuracy of patterns being recognized by the model. A CNN, specifically, provides competitive efficiency in the task of classifying, and is able to recognize patterns regardless of their location in the image, beneficial to accurately identify patterns exhibited by handwritten characters.

Such classification task may be used to transcribe scanned documents. This would be useful as a transfer-layer in a model digitizing documents such as historical texts. 

1. ### Results

***** ***Implement results section*** ******

---

Report - Data
Describes the data and its features. This should include findings from EDA.

Report - Methods (Preprocessing)
Describes preprocessing and augmentation steps to input data into model

Report - Methods (Model)
Describes the model and parameters used

Report - Results
Includes description of the results/metrics/ validation

Report - Plots/Figures
A figure to show the model performance

Report - Discussion/Results
Discusses the performance metrics with respect to the problem. How changing parameters changed performance, future works, etc. Evaluate if this is a good model. Include what was learned from the assignment