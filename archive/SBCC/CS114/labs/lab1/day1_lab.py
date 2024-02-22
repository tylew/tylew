""" 
    For each problem, complete the function so that it satisfies the description in the docstring.
    Many of the problems can be solved in 1 line of code using built-in functionality.
    https://docs.python.org/3/library/functions.html
    https://docs.python.org/3/tutorial/controlflow.html
    https://docs.python.org/3/tutorial/introduction.html#lists
    https://docs.python.org/3/tutorial/introduction.html#strings
    https://docs.python.org/3/tutorial/datastructures.html
    https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions

    You can run unit tests for the problems by running:
    python -m unittest day1_tester.py

    If all your functions are correct, you should see:
        Ran 20 tests in 0.001s
        OK

    The first 2 have been solved for you.
"""


from typing import Any, Union


def problem_1():
    """Assigns a variable to the value 4 and prints it.

    Args:
        None

    Returns:
        None
    """
    x = 4
    print(x)


def problem_2(x : int) -> int:
    """Adds 5 to the input and returns it.

    Args:
        x (int): The number to add 5 to.

    Returns:
        int: The input plus 5.
    """
    return x + 5


def problem_3(str1 : str, str2 : str) -> None:
    """Takes two strings and prints them one after another, on separate lines, using 2 print statements.

    Args:
        text1 (str): The first string
        text2 (str): The second string

    Returns:
        None
    """

    print(str1)
    print(str2)


def problem_4(x : int) -> bool:
    """Checks if a number is even or odd.
    For example

    Args:
        x (int): The number to check.

    Returns:
        bool: True if the number is even, False if the number is odd.
    """
    return x % 2 == 0


def problem_5(x : int) -> bool:
    """Checks if a number is divisible by 3.

    Args:
        x (int): The number to check.

    Returns:
        bool: True if the number is divisible by 3, False otherwise.
    """

    return x % 3 == 0


def problem_6(x : int) -> bool:
    """Checks if a number is divisible by 3 or 5.

    Args:
        x (int): The number to check.

    Returns:
        bool: True if the number is divisible by 3 or 5, False otherwise.
    """
    return x % 3 == 0 or x % 5 == 0

    
# The built-in functionality helps makes this and other problems easier. Check out the max() method: https://docs.python.org/3/library/functions.html
def problem_7(x : int, y : int) -> int:
    """Returns the larger of two numbers.

    Args:
        x (int): The first number.
        y (int): The second number.

    Returns:
        int: The larger of x and y.
    """

    return max(x,y)


def problem_8(x : int, y : int, z : int) -> int:
    """Returns the smallest of three numbers.

    Args:
        x (int): The first number.
        y (int): The second number.
        z (int): The third number.

    Returns:
        int: The smallest of x, y, and z.
    """

    return min(x,y,z)


# List resources:   
#  https://docs.python.org/3/tutorial/introduction.html#lists
#  https://docs.python.org/3/tutorial/datastructures.html
def problem_9(lst : list) -> Any:
    """Returns the 3rd element of the list.
    
    Args:
        lst (list): The list.
    
    Returns:
        Any: The 3rd element of the list.
    """

    return lst[2]


def problem_10(lst : list) -> Any:
    """Returns the smallest element of the list.
    
    Args:
        lst (list): The list.
    
    Returns:
        Any: The smallest element of the list.
    """
    s = lst[0]
    for item in lst:
        if item < s:
            s = item

    return s



def problem_11(lst : list) -> int:
    """Returns the length of a list.

    Args:
        lst (list): The list.

    Returns:
        int: The length of the list.
    """

    return len(lst)


def problem_12(lst : list, x : Any) -> Union[int, None]:
    """Returns the position (the index) of the first element in the list that has value x.
    If the list does not contain x, return None.

    Args:
        lst (list): The list.
        x (Any): The value to search for.

    Returns:
        Union[int, None]: The index of the value x, or None.
    """

    for idx, item in enumerate(lst):
        if item == x:
            return idx
    
    return None




def problem_13(lst : list) -> int:
    """Returns the 3rd and 5th elements of the list added together. 
    If the list is too short, return 0.

    Args:
        lst (list): The list.

    Returns:
        int: The sum of the 3rd and 5th elements of the list.
    """
    if len(lst) >= 4:
        return lst[2] + lst[4]
    
    return 0


def problem_14(lst : list) -> int:
    """Returns the sum of all even-indexed elements in the list (indices 0, 2, 4, etc).
    For example, if the list is [1, 2, 3, 4, 5], the sum would be 1 + 3 + 5 = 9.
    If the list is empty, return 0.

    Args:
        lst (list): The list.

    Returns:
        int: The sum of all the even-indexed elements in the list.
    """
    ret = 0
    for idx, item in enumerate(lst):
        if idx % 2 == 0:
            ret += item

    return ret





def problem_15(lst : list) -> int:
    """Returns the sum of every 3rd element in the list.
    For example, if the list is [1, 2, 3, 4, 5, 6], the sum would be 3 + 6 = 9.
    If the list is too short, return 0.

    Args:
        lst (list): The list.

    Returns:
        int: The sum of every 3rd element in the list.
    """
    ret = 0
    for idx, item in enumerate(lst):
        if (idx + 1) % 3 == 0:
            ret += item

    return ret


def problem_16(x : int) -> int:
    """Returns the sum of all the numbers from 0 to x, inclusive.
    For example, if x is 5, the sum would be 0 + 1 + 2 + 3 + 4 + 5 = 15.

    Args:
        x (int): The number to sum up to.

    Returns:
        int: The sum of all the numbers from 0 to x, inclusive.
    """
    ret = 0
    for i in range(x+1):
        ret += i

    return ret



def problem_17(x : int) -> int:
    """Returns the sum of all the numbers from 0 to x, inclusive, that are divisible by 3 or 5.
    For example, if x is 10, the sum would be 0 + 3 + 5 + 6 + 9 + 10 = 33.

    Args:
        x (int): The number to sum up to.

    Returns:
        int: The sum of all the numbers from 0 to x, inclusive, that are divisible by 3 or 5.
    """
    ret = 0
    for i in range(x+1):
        if i % 3 == 0 or i % 5 == 0:
            ret += i

    return ret


def problem_18(s : str) -> int:
    """Returns the number of vowels in the string.
    For example, if the string is "Hello World", the result would be 3.

    Args:
        s (str): The string.

    Returns:
        int: The number of vowels in the string.
    """
    ret = 0
    for letter in s:
        if letter.lower() in ['a','e','i','o','u']:
            ret += 1

    return ret

# These last few problems are the types of things I might expect to see as an easier / warmup question in a coding interview (they can get much harder).
def problem_19(s : str) -> str:
    """Returns a new string with all the vowels in s removed.
    For example, if the string is "Hello World", the result would be "Hll Wrld".

    Args:
        s (str): The string.

    Returns:
        str: The string with all the vowels removed.
    """
    ret = ''
    for letter in s:
        if letter.lower() not in ['a','e','i','o','u']:
            ret += letter

    return ret


def problem_20(s1 : str, s2 : str) -> str:
    """Returns s1 interleaved with s2. Start with the first character of s1.
    For example, if s1 is "Hello" and s2 is "World", the result would be "HWeolrllod".

    Args:
        s1 (str): The first string.
        s2 (str): The second string.

    Returns:
        str: The string with s1 interleaved with s2.
    """
    ret = ''
    for i in range(max(len(s1), len(s2))):
        if i < len(s1):
            ret += s1[i]
        if i < len(s2):
            ret += s2[i]

    return ret

def problem_21(a : int, b : int, c : int, d : int) -> str:
    """
    Given four side lengths. Determine if the 4 sides can be arranged into a square, a rectangle, or neither.

    Yes squares are rectangles, but for this problem, if the sides can be arranged into a square, return "square".

    For example, if the side lengths are 2, 2, 2, 2, return the string "square".
    If the side lengths are 1, 2, 1, 2, return the string "rectangle".'
    If the side lengths are 4, 3, 3, 4, return the string "rectangle".
    If the side lengths are 1, 5, 3, 3, return the string "neither".
    
    If a side length is 0 or negative, return "neither".

    Args:
        a (int): The first side length.
        b (int): The second side length.
        c (int): The third side length.
        d (int): The fourth side length.

    Returns:
        str: "square", "rectangle", or "neither".
    """
    # Check for invalid side lengths
    if a <= 0 or b <= 0 or c <= 0 or d <= 0:
        return "neither"

    # Sort the sides to make comparison easier
    sides = sorted([a, b, c, d])

    # Check for square: All four sides equal
    if sides[0] == sides[1] == sides[2] == sides[3]:
        return "square"
    # Check for rectangle: Opposite sides equal
    elif sides[0] == sides[1] and sides[2] == sides[3]:
        return "rectangle"
    else:
        return "neither"





