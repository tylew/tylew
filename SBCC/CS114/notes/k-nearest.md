We want an algorithm that can classify images of black and white numbers 0-9

## Template matching

We could check how close each template is to the image we are processing

One way we could go about doing this is treat the images as a flattened 2d grid and compate it to that of the template

```
distance(input, 0_template) -> 0.4
distance(input, 1_template) -> 0.1

-> most likely a '1' because least difference between input and test
```

Template matching is not robust with messy and different writing styles. Shifts as well cause problems

## Machine learning (K-Nearest Neighbors)

1. get a dataset of thousands of labeled images (MNIST dataset)
2. Given an input, find the 5 closest images from the dataset
    - By converting images to vectors and computing the distance() between them and the input (method above)
3. Take most common match