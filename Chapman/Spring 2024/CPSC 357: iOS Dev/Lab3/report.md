# Functions, classes/inheritance, optionals, guards

### Functions.playground
- Functions in Swift are self-contained blocks of code that perform a specific task, defined using the func keyword.
- Swift functions support parameter names for both internal code use and external callers, enhancing code readability.
- Functions can return a value, indicated by an arrow (->) followed by the return type.
- Variadic parameters allow for receiving zero or more values of a specified type, enabling flexibility in function arguments.
- Functions can be nested within other functions to encapsulate related functionality.
### Classes and Inheritance.playground
- Classes in Swift are reference types that allow for the creation of complex data models with properties and methods.
- Inheritance enables a class to inherit properties, methods, and other characteristics from another class.
- Swift supports method overriding, allowing a subclass to provide a custom implementation of a method defined in its superclass.
- Initializers in classes ensure that all stored properties of an instance are properly set up before use.
- Swift classes can have deinitializers (deinit), which are called automatically when an instance of the class is deallocated.
### Optionals.playground
- Optionals in Swift are types that can hold either a value or nil, indicating the absence of a value.
- Forced unwrapping (!) accesses the value of an optional directly but causes a runtime error if the optional is nil.
- Optional binding (if let or guard let) safely unwraps optionals, providing a way to handle nil values gracefully.
- Optional chaining allows for the calling of methods, properties, and subscripts on an optional that might currently be nil.
- The nil-coalescing operator (??) provides a default value for an optional if it contains nil.
###  Guard.playground
- The `guard` statement is used for early exit from a function or loop, improving readability by handling error cases first.
- Unlike `if` statements, `guard` ensures that variables and constants created in its condition are available in the subsequent code.
- `guard` is often used for unwrapping optionals and ensuring conditions are met before proceeding with the execution of the following code.
- Using `guard` can reduce the nesting of if statements, making code clearer and more linear.
- `guard` must always exit the current scope when its condition is not met, typically with a return, break, continue, or throw statement.