/*:
 ## Controlling the Display
 
 The `backgroundColor` property of `PixelDisplay` controls the display color.
 
 - callout(Experiment): Try changing the background color of the display.
 */
//display.backgroundColor = .cyan
/*:
 Notice that any of the pixels you've already set don't change color.
 
- callout(Experiment): Add a few pixels and change the background color again.
 */
display.backgroundColor = .green
display.setPixel(x: 0, y: 0, color: .blue)
display.setPixel(x: 1, y: 3, color: .yellow)
display.setPixel(x: 5, y: 2, color: .red )
let color = Color(red: 100/255.0, green: 50/255.0, blue: 200/255.0, alpha: 1)
display.setPixel(x: 7, y: 7, color: color)
/*:
 Notice that you don't see the first background color at all. That's because all the operations execute quickly when your code runs.
 
 On the next page, put some pixels in a row.

[Previous](@previous)  |  page 3 of 13  |  [Next: Lines](@next)
 */
