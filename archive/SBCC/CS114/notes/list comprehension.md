### List comprehension

```
new_list = [ (new_item) for (item) in (itterator) if (conditional) ]
```

able to use to create other itterables such as `dictionary` and `generator`

 `Generators` use `()` instead of `[]` and calculates as it goes, such as:

 ```
 list = [1,2,3,4,5]

 gen = ( x**2 for x in list if x%2 == 0 )

# retrieves next value
 next(gen) #-> 4
 next(gen) #-> 16

 # OR:

 gen = iter(list)

 next(gen) #-> 1
 next(gen) #-> 2 ...
 
 # print remaining values
 list(gen) #-> [3,4,5]
 ```

### Arrays in python

#### usage:
```
import array

int_array = ('i', [1,2,3,4])
```

`Array` can only store specific primitive data types

