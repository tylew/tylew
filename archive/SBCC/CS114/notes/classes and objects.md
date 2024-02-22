## Classes and objects

Kinda like a dictionary
```
class MyClass:
    sally = 100
    bob = 95
    joe = 85
```

Can do more than a dictionary, `functions` & `methods` can be defined under class

```
class MyClass:
    ...

    def print_scores():
        print(MyClass.sally, ...)

    # Modifier
    def reset_scores(self):
        sally = 0
        ...
```

`dictionary` only stores and retrieves, whereas `class` can be programmed to do things.

`objects` can be created to make an "instance" of a class

```
classroom = MyClass()
classrom.sally = 50

print(classroom.sally) # -> 50
print(MyClass.sally)   # -> 100

# also:

classroom.reset_grades() == MyClass.reset_grades(classroom)
```

when dealing with objects, methods always have a `self` argument 


- A fucntion that belogs to a class is called a `method`
- Often contains a `self` refrence

`dunder methods` allow for object customization
- "double under" aka. anything that follows this syntax: __ [modifier] __

type() and dir()
- type() -> returns type of class 
- dir() -> lists all attributes that belong