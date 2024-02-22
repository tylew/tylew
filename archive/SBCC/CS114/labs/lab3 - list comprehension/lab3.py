# Lab 3: Lists and arrays
# Complete the functions below

# Use list comprehensions when asked.

# Some resources:
# https://docs.python.org/3/tutorial/datastructures.html
# https://docs.python.org/3/library/array.html
# https://www.w3schools.com/python/python_lists_comprehension.asp



# Problem 1 has been solved for you.
def problem_01(x : int) -> list:
    """Use a list comprehension to create a list of all EVEN numbers from 1 to x (inclusive). 

    Do this in one line by returning the list comprehension.
    
    Args:
        x (int): The upper bound of the range

    Returns:
        list: A list of all numbers from 1 to x (inclusive)

    Example: 
        problem_01(5) -> [1, 2, 3, 4, 5]
    """
    return [i for i in range(1, x + 1) if i % 2 == 0]



def problem_02(x : int) -> list:
    """Use a list comprehension to create a list of all numbers divisible by 3 from 1 to x (inclusive). 

    Do this in one line by returning the list comprehension.

    Args:
        x (int): The upper bound of the range

    Returns:
        list: A list of all EVEN numbers from 1 to x (inclusive)

    Example:
        problem_02(16) -> [3, 6, 9, 12, 15]
    """

    return [y for y in range(1,x+1) if y % 3 == 0]



def problem_03(x : int) -> list:
    """Use a list comprehension to create a list of all numbers from 1 to x (inclusive) SQUARED.
    Remember that the output is on the leftmost side of the list comprehension, and you can do stuff to it like squaring it.

    Do this in one line by returning the list comprehension.
    
    Args:
        x (int): The upper bound of the range

    Returns:
        list: A list of all numbers from 1 to x (inclusive) SQUARED

    Example:
        problem_03(5) -> [1, 4, 9, 16, 25]
    
    """

    return [(y * y) for y in range(1,x+1)]



def problem_04(colors : list, sizes : list) -> list[tuple]:
    """Given a list of shirt sizes and a list of shirt colors, return a list of all possible combinations of color and size, as tuples.
    We saw this in the slides.

    Possible shirt colors may include "red", "blue", and "green".
    Possible shirt sizes may include "XXS", "XS", "S", "M", "L", "XL", "XXL".

    Use a list comprehension.
    Do this in one line by returning the list comprehension.
    
    Args:
        colors (list): A list of colors
        sizes (list): A list of sizes

    Returns:
        list: A list of all possible shirt combinations as tuples

    Example:
        problem_04(["red", "blue"], ["S", "M"]) -> [("red", "S"), ("red", "M"), ("blue", "S"), ("blue", "M")]
    """

    return [
        (l, t) 
        for l in colors 
        for t in sizes
        ]



def problem_05(colors : list, sizes : list) -> list[tuple]:
    """Given a list of shirt sizes and a list of shirt colors, return a list of all possible combinations of color and size, as tuples.
    We saw this in the slides, but this time there's a twist.

    OUR STORE IS OUT OF MEDIUM SHIRTS, so we don't want any medium shirts in our list.
    Do not include combinations with medium shirts such as ("red", "M")

    Remember that you can use if-statements in list comprehensions and they appear on the rightmost side.
    Only outputs that pass the if-statement will be included in the list comprehension.

    Possible shirt colors may include "red", "blue", and "green".
    Possible shirt sizes may include "XXS", "XS", "S", "M", "L", "XL", "XXL".

    Use a list comprehension.
    Do this in one line by returning the list comprehension.
    
    Args:
        colors (list): A list of colors
        sizes (list): A list of sizes

    Returns:
        list: A list of all possible shirt combinations as tuples EXCLUDING any combinations with medium shirts.

    Example:
        problem_04(["red", "blue", "green"], ["S", "M", "L"]) -> [("red", "S"), ("red", "L"), ("blue", "S"), ("blue", "L"), ("green", "S"), ("green", "L")]
    """

    return [(l, t,) for l in colors for t in sizes if t.lower() != 'm']



def problem_06(colors : list, 
              sizes : list, 
              out_of_stock_colors : set,
              out_of_stock_sizes : set
            ) -> list[tuple]:
    """Given a list of shirt sizes and a list of colors, return a list of all possible shirt configurations.
    
    Do not include combinations with colors that appear in out_of_stock_colors.
    Do not include combinations with sizes that appear in out_of_stock_sizes.
    
    Use a list comprehension. 
    You can check if a color or size is in an out_of_stock set using the "in" keyword.
    You can add an if-statement to the rightmost side of a list comprehension.

    Args:
        colors (list): A list of colors
        sizes (list): A list of sizes
        out_of_stock_colors (set): A set of colors that are out of stock
        out_of_stock_sizes (set): A set of sizes that are out of stock

    Returns:
        list: A list of all possible shirt combinations as tuples EXCLUDING any combinations with out of stock colors or sizes.

    Example:
        problem_05(["red", "blue", "green"], ["S", "M", "L"], {"red", "blue"}, {"M"}) -> [("green", "S"), ("green", "L")]
    """

    return [(c,s,) for c in colors if c not in out_of_stock_colors for s in sizes if s not in out_of_stock_sizes]
    


def problem_07(vector1 : list, vector2 : list) -> list:
    """
    Given two vectors, return a new vector that is the sum of the two vectors, as shown on the slides.

    The sum of two vectors is the sum of the corresponding elements of the vectors.

    For example:
    [1, 2, 3] + [4, 5, 6] = [5, 7, 9]

    Use a list comprehension.
    Do this in one line by returning the list comprehension.

    Args:
        vector1 (list): A list of numbers
        vector2 (list): A list of numbers

    Returns:
        list: A list of numbers that is the sum of the two vectors

    Example:
        problem_06([1, 2, 3], [4, 5, 6]) -> [5, 7, 9]
    """

    return [x+y for (x,y) in zip(vector1,vector2)]



def problem_08(vector1 : list, vector2 : list, vector3 : list) -> list:
    """Given three vectors, return a new vector that is the sum of the three vectors.
    
    zip can take three lists as arguments. It works the same way as shown on the slides, but the tuples it produces will have three elements.
    You can also do it without zip.
    
    Use a list comprehension.
    Do this in one line by returning the list comprehension.

    Args:
        vector1 (list): A list of numbers
        vector2 (list): A list of numbers
        vector3 (list): A list of numbers

    Returns:
        list: A list of numbers that is the sum of the three vectors

    Example:
        problem_06([1, 2, 3], 
                  [4, 5, 6],
                  [7, 8, 9]) -> [12, 15, 18]
    """

    return [x+y+z for (x,y,z) in zip(vector1,vector2,vector3)]



def problem_09(vector : list) -> int:
    """Given a vector:
    1. Square each number in the vector. 
    2. Sum the elements of the squared vector together into one number. 
    3. Return this number.

    This is known as the "squared euclidean norm" of the vector. It's the length (magnitude) of the vector, but squared.

    For example:
    [1, 2, 3] squared is [1, 4, 9]

    Summing over the squared vector gives us 1 + 4 + 9 = 14. We return 14.
    
    Use a list comprehension to square the vector, then add the elements together.
    You can add the elements of a list together by passing it to sum().
    
    Args:
        vector (list): A list of numbers
    
    Returns:
        int: The sum of the elements of the squared vector
        
    Example:
        problem_09([1, 2, 3]) -> 14
    """

    return sum(v**2 for v in vector)



def problem_10(vector1 : list, vector2 : list) -> int:
    """Given two vectors:
    1. Multiply the vectors together element-wise. 
    2. Sum the elements of the resulting vector together into one number.
    3. Return this number.

    This is known as the "dot product" of the two vectors.

    Multiplying two vectors element-wise means to multiply vector1[0] with vector2[0], vector1[1] with vector2[1], and so on.
    Similar to what we did when we added two vectors, but with multiplication instead of addition.

    For example:
    [1, 2, 3] * [4, 5, 6] = [4, 10, 18]

    Summing the result gives us 4 + 10 + 18 = 32.

    Use a list comprehension to multiply the vectors together element-wise, then add the elements together.

    Args:
        vector1 (list): A list of numbers
        vector2 (list): A list of numbers

    Returns:
        int: The sum of the elements of the new vector

    Example:
        problem_10([1, 2, 3], [4, 5, 6]) -> 32
    """

    return sum(v*v2 for (v, v2) in zip(vector1,vector2))




######## EXTRA CREDIT ########

import array

def problem_11_extra(
        matrix : array.array, 
        vector : array.array, 
        M : int, 
        N : int
    ) -> array.array:
    """Implement matrix-vector multiplication using arrays. 
    
    Do NOT use lists or list comprehensions.
    
    The code isn't too long once you know how to do it, but it can be tricky to figure out.

    The matrix will be an array of type float of size M*N (M rows, N columns).
    The vector will an array of type float of size N
    The output should a newly allocated array of type float and size M.

    You can imagine a matrix as M rows of size N vectors.

    We go through each row in the matrix and dot product our input vector (size N) with the row vector (also size N) from the matrix.
    The result of one dot-product between two vectors is a single number (a scalar).
    When we do this for every one of the M rows in the matrix, the result is an array of M numbers - the output vector of size M.

    Unlike in NumPy, Python arrays do not support multi-dimensional indexing. E.G. matrix[0][0] will not work.
    The matrix is given in ROW-MAJOR ORDER. This means that the first N values represent the first row, the next N values represent the second row, and so on.
    https://en.wikipedia.org/wiki/Row-_and_column-major_order
    (row-major order is how they're represented under-the-hood in NumPy, too)

    Args:
        matrix (array.array): An array of type float, of size M*N, representing a matrix in row-major order.
        vector (array.array): An array of type float, of size N.

    Returns:
        array.array: A newly allocated array of type float and size M.

    Example:
        matrix = array.array('f', [1, 2, 3, 4, 5, 6])
        vector = array.array('f', [1, 2, 3])
        m = 2
        n = 3
        problem_11(vector, matrix, m, n) -> array.array('f', [14, 32])

        How?
        1*1 + 2*2 + 3*3 = 14 -> This is the dot-product of our input vector with the first row in the matrix.
        1*4 + 2*5 + 3*6 = 32 -> This is the dot-product of our input vector with the second row in the matrix.
    """

    arr = array.array('f', [0.0] * M)  # Initialize the array with zeros

    for x in range(M):
        sum = 0.0  # Reset sum for each row
        for y in range(N):
            sum += matrix[x * N + y] * vector[y]  # Calculate dot product
        arr[x] = sum  # Store the result in the array

    return arr


def problem_12_extra(
        matrix : array.array, 
        vector : array.array, 
        M : int, 
        N : int
    ) -> array.array:
    """Repeat problem 11, but this time do it in one line with a list comprehension.

    You can nest list comprehensions. 
    For example:
        [[i * j for j in [1, 2, 3]] for i in [4, 5, 6]] -> [[4, 8, 12], [5, 10, 15], [6, 12, 18]]

    You can pass a list comprehension to array.array() to create an array from a list comprehension. 
    For example:
        return array.array('f', [vector[i] * 2 for i in range(N)])

    (This negates the performance benefits of working with arrays, it's just an interesting challenge)
    """

    return array.array('f', [sum(matrix[x * N + y] * vector[y] for y in range(N)) for x in range(M)])