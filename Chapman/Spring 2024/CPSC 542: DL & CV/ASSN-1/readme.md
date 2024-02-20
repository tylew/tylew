# CPSC 542: Implement a Convolutional Neural Network – Assignment #1
```
Lewis, T.  
tylewis@chapman.edu
ID# 002366930

02/20/24
```

1. ### Identify a vision dataset to work with for classification tasks:

For assignment completion, I used the **[MNIST dataset (link)](https://www.kaggle.com/datasets/hojjatk/mnist-dataset)**. 

The database contains 70,000 BW images of handwritten numeric character depictions: 

![Alt text](mnist_examples.png)

The only Computer Vision exposure I have had prior to this assignment/class is using Euclidean Distance K-nearest neighbors to predict labels from this specific dataset. 

Achieved ~0.9 accuracy using K-Nearest, but Convolutional Neural Network is vastly advantageous. 

2. ### Prove the classification task requires a deep learning solution:

A deep learning solution such as a Convolutional Neural Network (CNN) is suitable for the task of classifying the MNIST dataset.

A CNN, specifically, is able to recognize patterns regardless of their location in the image, crucial to accurately identify patterns exhibited by handwritten characters.

Such classification task may be used to efficiently transcribe scanned documents. This would likely be useful in digitizing historical texts. A Deep Learning solution provides competitive efficiency.

3. ### Results
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