1. With respect to max pooling layers:
   1. Is there any direct computations needed on the max pooling layers during the backwards pass?
No

    2. How might propagation of max pooling information further backwards in the network be handled?

The output from each pooling region is utilized to represent the entirety of that region when it is propagated back to the preceding layer.

2. Compare the back-propagation process differences for a dense (traditional feed-forward) layer and a convolutional layer.

Dense layer is 1D, CNN is 2d


