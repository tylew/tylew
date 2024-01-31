import torch
from lab8 import *

def test_problem1():
    assert torch.equal(problem1(torch.tensor([[1, 2, 3], [4, 5, 6]])), torch.tensor([1, 2, 3]))
    assert torch.equal(problem1(torch.tensor([[7, 8], [9, 10]])), torch.tensor([7, 8]))
    assert torch.equal(problem1(torch.tensor([[11]])), torch.tensor([11]))
    assert torch.equal(problem1(torch.arange(12).view(3, 4)), torch.tensor([0, 1, 2, 3]))
    assert torch.equal(problem1(torch.zeros(2, 5)), torch.zeros(5))

def test_problem2():
    assert torch.equal(problem2(torch.tensor([[1, 2, 3], [4, 5, 6]])), torch.tensor([1, 4]))
    assert torch.equal(problem2(torch.tensor([[7, 8], [9, 10]])), torch.tensor([7, 9]))
    assert torch.equal(problem2(torch.tensor([[11], [12]])), torch.tensor([11, 12]))
    assert torch.equal(problem2(torch.arange(12).view(3, 4)), torch.tensor([0, 4, 8]))
    assert torch.equal(problem2(torch.ones(5, 2)), torch.ones(5))

def test_problem3():
    assert torch.equal(problem3(torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]])), torch.tensor([[4, 5, 6], [7, 8, 9]]))
    assert torch.equal(problem3(torch.arange(16).view(4, 4)), torch.tensor([[8, 9, 10, 11], [12, 13, 14, 15]]))
    assert torch.equal(problem3(torch.ones(5, 3)), torch.ones(2, 3))
    assert torch.equal(problem3(torch.zeros(4, 2)), torch.zeros(2, 2))
    assert torch.equal(problem3(torch.arange(6).view(3, 2)), torch.tensor([[2, 3], [4, 5]]))

def test_problem4():
    assert torch.equal(problem4(torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]])), torch.tensor([[1, 3], [7, 9]]))
    assert torch.equal(problem4(torch.ones(6, 6)), torch.ones(3, 3))
    assert torch.equal(problem4(torch.zeros(4, 4)), torch.zeros(2, 2))
    assert torch.equal(problem4(torch.arange(25).view(5, 5)), torch.tensor([[0, 2, 4], [10, 12, 14], [20, 22, 24]]))
    assert torch.equal(problem4(torch.arange(16).view(4, 4)), torch.tensor([[0, 2], [8, 10]]))

def test_problem5():
    assert torch.equal(problem5(torch.tensor([[1, 2, 3], [4, 5, 6]])), torch.tensor([6, 15]))
    assert torch.equal(problem5(torch.tensor([[7, 8], [9, 10], [11, 12]])), torch.tensor([15, 19, 23]))
    assert torch.equal(problem5(torch.tensor([[13]])), torch.tensor([13]))
    assert torch.equal(problem5(torch.arange(12).view(3, 4)), torch.tensor([6, 22, 38]))
    assert torch.equal(problem5(torch.zeros(4, 5)), torch.zeros(4))

def test_problem6():
    assert torch.equal(problem6(torch.tensor([[1, 2, 3], [4, 5, 6]])), torch.tensor([5, 7, 9]))
    assert torch.equal(problem6(torch.tensor([[7, 8], [9, 10], [11, 12]])), torch.tensor([27, 30]))
    assert torch.equal(problem6(torch.tensor([[13], [14], [15]])), torch.tensor([42]))
    assert torch.equal(problem6(torch.arange(12).view(3, 4)), torch.tensor([12, 15, 18, 21]))
    assert torch.equal(problem6(torch.ones(5, 2)), torch.tensor([5, 5]))

def test_problem7():
    assert torch.equal(problem7(torch.tensor([1, 2, 3, 4, 5, 6])), torch.tensor([[1, 2, 3], [4, 5, 6]]))
    assert torch.equal(problem7(torch.tensor([7, 8, 9, 10, 11, 12])), torch.tensor([[7, 8, 9], [10, 11, 12]]))
    assert torch.equal(problem7(torch.tensor([13, 14, 15, 16, 17, 18])), torch.tensor([[13, 14, 15], [16, 17, 18]]))
    assert torch.equal(problem7(torch.arange(9)), torch.tensor([[0, 1, 2], [3, 4, 5], [6, 7, 8]]))
    assert torch.equal(problem7(torch.ones(6)), torch.tensor([[1, 1, 1], [1, 1, 1]]))

def test_problem8():
    assert problem8(torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]])) == 15
    assert problem8(torch.tensor([[2, 0], [0, 2]])) == 4
    assert problem8(torch.tensor([[10]])) == 10
    assert problem8(torch.arange(4).view(2, 2)) == 3
    assert problem8(torch.tensor([[1, 2, 3], [4, 5, 6]])) == 6

def test_problem9():
    assert torch.equal(
        problem9(torch.tensor([[1, 2, 3], [4, 5, 6]]), torch.tensor([[1, 2], [3, 4], [5, 6]])),
        torch.tensor([[22, 28], [49, 64]])
    )
    assert torch.equal(
        problem9(torch.tensor([[1, 0], [0, 1]]), torch.tensor([[1, 2], [3, 4]])),
        torch.tensor([[1, 2], [3, 4]])
    )
    assert torch.equal(
        problem9(torch.tensor([[2, 3], [0, 1]]), torch.tensor([[1, 2], [3, 1]])),
        torch.tensor([[11, 7], [3, 1]])
    )
    assert torch.equal(
        problem9(torch.ones(2, 3, dtype=torch.int64), torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]])),
        torch.tensor([[12, 15, 18], [12, 15, 18]])
    )
    assert torch.equal(
        problem9(torch.eye(3, dtype=torch.int64), torch.tensor([[0, 1, 2], [3, 4, 5], [6, 7, 8]])),
        torch.tensor([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    )

def get_mnist_data():
    import torchvision
    mnist_dataset = torchvision.datasets.MNIST(root="./MNIST", train=True, download=True, transform=torchvision.transforms.ToTensor())
    image, target = mnist_dataset[0]
    return image, target

def test_problem10():
    image, label = get_mnist_data()
    image = image.view(-1)
    target = torch.nn.functional.one_hot(torch.tensor(label), num_classes=10).float()
    function = problem10(image, target)
    loss = torch.norm((image @ function) - target)
    print(f"Your loss value: {loss}")
    assert loss < 1

def test_problem11():
    image, label = get_mnist_data()
    image = image[0]
    target = torch.nn.functional.one_hot(torch.tensor(label), num_classes=10).float()
    function = problem11(image, target)
    patches = torch.nn.functional.pad(image, (1, 1, 1, 1), mode='constant', value=0).unfold(0, 6, 6).unfold(1, 6, 6).contiguous().view(-1, 36)
    out = patches @ function
    loss = torch.norm(out.sum(dim=0) - target)
    print(f"Your loss value: {loss}")
    assert loss < 1

if __name__ == "__main__":
    test_problem1()
    test_problem2()
    test_problem3()
    test_problem4()
    test_problem5()
    test_problem6()
    test_problem7()
    test_problem8()
    test_problem9()
    test_problem10()
    test_problem11()
    print("All tests passed!")
