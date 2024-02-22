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








// Variables and Constants
var variableName = "Hello, world!" // Variable: Mutable
let constantName = 100 // Constant: Immutable

// Data Types
let integer: Int = 10
let floatingPoint: Float = 3.14
let doublePrecision: Double = 3.14159265359
let boolean: Bool = true
let string: String = "Hello, Swift!"


let array: [String] = ["Apple", "Banana", "Cherry"]
let dictionary: [String: Int] = ["Apple": 1, "Banana": 2]

// Control Flow

// If Statement
if boolean {
    // Code to execute if boolean is true
} else {
    // Code to execute if boolean is false
}

// Switch Statement
let someValue = 5
switch someValue {
case 1...4:
    print("Between 1 and 4")
case 5:
    print("Exactly 5")
default:
    print("Something else")
}

// For-In Loop
for item in array {
    print(item)
}

// While Loop
var count = 5
while count > 0 {
    print(count)
    count -= 1
}

// Functions
func greet(name: String) -> String {
    return "Hello, \(name)!"
}
print(greet(name: "Swift"))

// Optionals
var optionalString: String? = "An optional string"
// Optional Binding
if let string = optionalString {
    print(string)
}
// Force Unwrapping
print(optionalString!)

// Enums
enum CompassPoint {
    case north, south, east, west
}
var direction = CompassPoint.west

// Structs
struct Point {
    var x: Int
    var y: Int
}
let point = Point(x: 10, y: 20)

// Classes
class Vehicle {
    var currentSpeed = 0.0
    func description() -> String {
        return "traveling at \(currentSpeed) miles per hour"
    }
}
let someVehicle = Vehicle()

// Error Handling
enum PrinterError: Error {
    case outOfPaper, noToner, onFire
}
func send(job: Int, toPrinter printerName: String) throws -> String {
    if printerName == "Never Has Toner" {
        throw PrinterError.noToner
    }
    return "Job sent"
}

// Protocols
protocol Identifiable {
    var id: String { get set }
}
struct User: Identifiable {
    var id: String
}

// Extensions
extension Int {
    func squared() -> Int {
        return self * self
    }
}
let number = 7
print(number.squared())


// Closures
// A simple closure that takes no parameters and returns no value
let simpleClosure = {
    print("This is a simple closure.")
}
simpleClosure()

// A closure that takes parameters and returns a value
let multiplyClosure: (Int, Int) -> Int = { $0 * $1 }
print(multiplyClosure(3, 4))

// Using trailing closure syntax
let numbers = [1, 2, 3, 4, 5]
let squaredNumbers = numbers.map { $0 * $0 }
print(squaredNumbers)

// Guard Statement
// A function using guard to early exit if a condition isn't met
func greet(person: [String: String]) {
    guard let name = person["name"] else {
        print("Name missing")
        return
    }
    print("Hello \(name)!")
}
greet(person: ["name": "John"])

// Tuples
// Defining a tuple
let http404Error = (404, "Not Found")
// Accessing elements of a tuple
print("The status code is \(http404Error.0)")
print("The status message is \(http404Error.1)")

// Decomposing tuples
let (statusCode, statusMessage) = http404Error
print("The status code is \(statusCode)")
print("The status message is \(statusMessage)")

// Named elements in tuples for readability
let http200Status = (statusCode: 200, description: "OK")
print("The code is \(http200Status.statusCode) and the status is \(http200Status.description)")



class Product {
    var name: String
    var price: Double

    // Constructor (Initializer)
    init(name: String, price: Double) {
        self.name = name
        self.price = price
    }
    
    // Destructor (Deinitializer)
    deinit {
        print("\(name) is being deinitialized")
    }
    
    // Method to describe the product
    func describe() {
        print("Product: \(name), Price: \(price)")
    }
    
    // Operator Overloading
    static func + (left: Product, right: Product) -> Product {
        let combinedName = "\(left.name) & \(right.name) Bundle"
        let combinedPrice = left.price + right.price
        return Product(name: combinedName, price: combinedPrice)
    }
}

// Example usage
let product1 = Product(name: "Laptop", price: 1200.00)
let product2 = Product(name: "Mouse", price: 40.00)

// Combining products
let bundledProduct = product1 + product2
bundledProduct.describe()
