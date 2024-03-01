
## Question 1
For most applications, Why is it necessary to evaluate but go "past" simple evaluation metrics like accuracy, F1, etc.? What things (provide 1 example and justification) can I do to better understand how my model is performing and why it is performing the way it is?

**Your Answer:**
Beyond evaluation metrics such as accuracy/loss, F1, etc, it is an option to incorporate interpretability into models. That is, make them in such a way where they provide understandable intermediate outputs. 

 
## Question 2
As a starting point, I leverage a simpler pre-defined architecture, associated pre-trained weights, which I keep frozen, and a set of dense layers, which are randomly initialized and tuned via the typical model training process (i.e. image classification: VGG13 architecture & weights from being trained on ImageNet). In this case, the results do not meet my minimum qualifications for "good" performance. Name and briefly qualify/justify 2 potential next steps, **assuming I have exhausted all options for performance adjustments related to the dataset.**

**Your Answer:**
The model does not meet your minimum requirements.

Potential next steps:

try data augmentation, which could provide the network more diversity in its patterns included in its convolutional gradients.
Implement transfer learning, use this or a new model to pre-classify the dataset to input to a more general model

Start constraining learning on layers
Try using a different architecture