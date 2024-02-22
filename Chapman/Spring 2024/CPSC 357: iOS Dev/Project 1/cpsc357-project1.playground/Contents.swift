import UIKit

func isPrime(number: Int) -> Bool
{
    switch number {
        case 2, 3:
            return true // 2 and 3 are prime numbers
        case let n where n < 2 || n % 2 == 0:
            return false // Numbers less than 2 and even numbers are not prime
        default:
            // Check for factors from 3 up to the square root of `number`.
            // Increment by 2 to skip even numbers.
            for i in stride(from: 3, through: Int(Double(number).squareRoot()), by: 2) {
                if number % i == 0 {
                    return false // Found a factor, so `number` is not prime
                }
            }
            return true // No factors found, so `number` is prime
    }
}

isPrime(number: 10)
isPrime(number: 79)




func gcd(numberA a: Int, numberB b: Int) -> Int
{
    var a = a
    var b = b
    while b != 0 {
        let temp = b
        b = a % b
        a = temp
    }
    return a
}

let gcdResult = gcd(numberA: 15, numberB: 100)
print(gcdResult)




func timeToWait(hr1: Int, min1: Int, hr2: Int, min2: Int)
{
    let temp1 = hr1 * 60 + min1
    let temp2 = hr2 * 60 + min2
    
    let difference = temp2-temp1
    let diffHr = difference / 60 // Integer division automatically truncates towards zero
    let diffMin = difference % 60
}

// Used llm for line 47
// original operation: Double(difference / Int(60)).rounded(.towardZero)
timeToWait(hr1: 2, min1: 15, hr2: 3, min2: 15)



// Algorithm adapted from stack exchange explanation
func verifyParenthesis(expression: String) -> Bool {
    var count = 0
    for char in expression {
        if char == "(" {
            count += 1
        } else if char == ")" {
            count -= 1
        }
        
        // If count becomes negative, there's a closing parenthesis without an opening one
        if count < 0 {
            return false
        }
    }
    
    // If count is not zero, there are unmatched parentheses
    return count == 0
}

print(verifyParenthesis(expression: "()()")) // true
print(verifyParenthesis(expression: "(()))")) // false
print(verifyParenthesis(expression: ")(")) // false



import Foundation

func checkEmail(_ email: String) -> String {
    // Regular expression to match a basic email pattern
    let usernameRegex = "[A-Za-z0-9._]+"
    let domainRegex = "[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"
    let emailRegex = "^\(usernameRegex)@\(domainRegex)$"
//    let emailRegex = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
    
    let emailTest = NSPredicate(format:"SELF MATCHES %@", emailRegex)
    let isValid = emailTest.evaluate(with: email)
    
    if isValid {
        let userName = email.components(separatedBy: "@").first!
        return "Thanks for the email \(userName)"
    } else {
        return "Provide a valid email"
    }
}

// Testing the function with the given examples
print(checkEmail("cibrian@chapman.edu"))
print(checkEmail("hipjasif@gmail.com")) // "Thanks for the email hipjasif"
print(checkEmail("thisisnot an email")) // "Provide a valid email"
print(checkEmail("cibrien.edu"))





func partialSum(array1 a1: [Int], array2 a2: [(Int,Int)]) -> [Int]
{
    var sumArray: [Int] = []
    for item in a2
    {
        var localSum: Int = 0
        for i in item.0 ... item.1
        {
            localSum += a1[i]
        }
        sumArray.append(localSum)
    }
    return sumArray
}

partialSum(array1: [3,6,4,15,30], array2:[(1,3),(0,4)])



func sumPower(numberA a: Int, numberB b: Int) -> Int
{
    var final: Int = 0
    for i in 1 ... b {
        let power = Int(pow(Double(i), Double(a))) // Correct exponentiation
        final += power
    }
    return final
}

//    1^2+2^2+3^2+4^2+5^2
sumPower(numberA: 2, numberB: 5)



