import torch

# Function to return the first row of a 2D tensor
def problem1(t: torch.Tensor) -> torch.Tensor:
    return t[0]

# Function to return the first column of a 2D tensor
def problem2(t: torch.Tensor) -> torch.Tensor:
    return t[:, 0]

# Function to return the last 2 rows of a 2D tensor
def problem3(t: torch.Tensor) -> torch.Tensor:
    return t[-2:]

# Function to return every other row and column of a 2D tensor
def problem4(t: torch.Tensor) -> torch.Tensor:
    return t[::2, ::2]

# Function to return the sum of each row of a 2D tensor
def problem5(t: torch.Tensor) -> torch.Tensor:
    return t.sum(dim=1)

# Function to return the sum of each column of a 2D tensor
def problem6(t: torch.Tensor) -> torch.Tensor:
    return t.sum(dim=0)

# Function to split a 1D tensor into non-overlapping chunks of size 3
def problem7(t: torch.Tensor) -> torch.Tensor:
    return t.view(-1, 3)

# Function to return the sum of diagonal elements of a 2D tensor
def problem8(t: torch.Tensor) -> torch.Tensor:
    return t.trace()

# Function to perform matrix multiplication of two 2D tensors
def problem9(tensor1: torch.Tensor, tensor2: torch.Tensor) -> torch.Tensor:
    return torch.mm(tensor1, tensor2)

# Function to train a function to approximate a target from an image
def problem10(image: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    # Initialize the function tensor with random values
    function = torch.randn(784, 10, requires_grad=True)

    # Set up optimization parameters
    learning_rate = 0.01
    num_iterations = 1000

    # Training loop
    for _ in range(num_iterations):
        # Forward pass
        output = image @ function

        # Calculate the loss (Euclidean distance)
        loss = torch.norm(output - target)

        # Backpropagation to compute gradients
        loss.backward()

        # Update the function tensor using gradient descent
        with torch.no_grad():
            function -= learning_rate * function.grad
            function.grad.zero_()  # Reset gradients

    return function

# Function to train a function to approximate a target from an image with patches
def problem11(image: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    function = torch.randn(36, 10, requires_grad=True)
    learning_rate = 0.1
    iterations = 1000
    
    for _ in range(iterations):
        patches = torch.nn.functional.unfold(image.unsqueeze(0).unsqueeze(0), 6)
        patches = patches.view(-1, 36)
        output = torch.mm(patches, function)
        loss = torch.norm(output.sum(dim=0) - target)
        loss.backward()
        with torch.no_grad():
            function -= learning_rate * function.grad
            function.grad.zero_()
    
    return function
