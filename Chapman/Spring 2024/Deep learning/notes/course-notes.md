<script
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
  type="text/javascript">
</script>

TWIMLAI podcast
'this week in ml & ai'

For quiz 2:
Explain-ability of transfer learning 


- Temporal
- Spacial

Limitations:
- models aren't always 'plug-n-play'
- models will form a bias around their training data


Attention is all you need introduced the transformer, an encoder/decoder architecture. 

## Auto Encoder
Output should be as close as possible to input


Check using 'reconstruction-error' -- some loss function

U-Nets used for segmentation in 2D

### Vision
- Sensors (eyes) gather information about surroundings
  - depth
  - color
- Forming ideas of surroundings
  - Classification

NN's:
- Layers
  - Nodes
  - Activation functions
- Flexibility
  - non-linear relationships
- Loss function
  - representation of error, want to minimize
- Other sets of parameters

For next week review:
- Gradient descent
- Back prop
- Convocational NN intro slides

#

Convolution layer 
Cross-Correlation
Feature detection in space

Backpropogation:
1. Initialization of network
2. Forward pass
3. Calculate error/loss
4. Backward pass (backpropogation of error)
5. Repeat 2-4 until converge/epochs

# Mar 7

IOU
-> Overlap area/Total area 
$$\frac{TP}{TP + FP + FN}$$

Softmax -> proxy for certainty 

Q: why might want to propogate certainty forward?

A: Make sure using high-certainty information to make decisions.

A2: low-certainty will also indicate changes must be made to model. 

## 
aleatoric - data/measurement related

epistemic - model related

Does the performance of my model match the certainty it is returning?

