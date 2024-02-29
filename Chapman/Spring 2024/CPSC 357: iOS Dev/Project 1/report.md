# CPSC 357: Project 1/2

## Author Information
- **Name:** Lewis, T.
- **Email:** tylewis@chapman.edu
- **Date:** 02/29/24

---


This Swift playground includes a variety of functions to demonstrate different programming concepts. I relatively had fun completing this assignment and ended up doing doing 7/8 responses. I have an understanding of this material and look forward to using swift for building an app.

## Functions Implemented
- **Standard Functions**: `isPrime`, `gcd`, `timeToWait`, `verifyParenthesis`, `checkEmail`, `partialSum`, `sumPower`.
- **Closure**: `gcdClosure` is a closure representing a function to calculate the GCD.


## Parameters and Variables
- Parameters are inputs to functions, such as `number` in `isPrime` or `a` and `b` in `gcd`.
- Variables are used within functions to store and manipulate data, such as `a` and `b` within the `gcd` function which are reassigned during the calculation.


## Variables vs. Constants
- **Variables** (`var`): Their values can change. Used for the GCD calculations (`a` and `b` in `gcd` and `gcdClosure`), within loops, and when calculating sums or differences.
- **Constants** (`let`): Their values cannot change once set. Used for function parameters (unless they are explicitly redefined as variables within the function) and temporary storage within loops where reassignment occurs.



# Function Descriptions

### `isPrime(_ number: Int) -> Bool`
- **Purpose**: Determines if a given number is prime.
- **Parameters**: `number` - an integer to check for primality.
- **Logic**: Uses a switch case to handle special cases (2, 3) and a for-loop to check divisibility for other numbers.

### `gcd(_ a: Int, _ b: Int) -> Int`
- **Purpose**: Calculates the greatest common divisor of two numbers.
- **Parameters**: `a`, `b` - integers to find the GCD of.
- **Logic**: Implements the Euclidean algorithm through a while loop.

### `gcdClosure: (Int, Int) -> Int`
- **Purpose**: A closure that calculates the greatest common divisor, similar to the `gcd` function.
- **Parameters**: `a`, `b` - integers to find the GCD of.
- **Logic**: Mirrors the `gcd` function using closure syntax.

### `timeToWait(hr1: Int, min1: Int, hr2: Int, min2: Int) -> String`
- **Purpose**: Calculates the waiting time between two moments.
- **Parameters**: `hr1`, `min1` - the start time; `hr2`, `min2` - the end time.
- **Logic**: Converts times to minutes, finds the difference, and formats the result as a string.

### `verifyParenthesis(expression: String) -> Bool`
- **Purpose**: Checks if parentheses in a string are correctly balanced.
- **Parameters**: `expression` - the string containing parentheses.
- **Logic**: Iterates through the string, tracking the balance of parentheses.

### `checkEmail(_ email: String) -> String`
- **Purpose**: Validates an email address and extracts the username.
- **Parameters**: `email` - the email address to validate.
- **Logic**: Uses regular expressions to verify the email format and extracts the username if valid.

### `partialSum(array1 a1: [Int], array2 a2: [(Int,Int)]) -> [Int]`
- **Purpose**: Calculates the sum of elements within specified ranges of an array.
- **Parameters**: `a1` - the array of integers; `a2` - an array of tuple ranges.
- **Logic**: Iterates through `a2`, summing elements of `a1` within each specified range.

### `sumPower(numberA a: Int, numberB b: Int) -> Int`
- **Purpose**: Calculates the sum of powers from 1 to `b`, each raised to the power of `a`.
- **Parameters**: `a` - the exponent; `b` - the upper limit of the base.
- **Logic**: Uses a for-loop to calculate each power and sums them up.

---


