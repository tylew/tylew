/*:
 ## Pixels
 
 All the pages in this playground have a `display` instance whose type is `PixelDisplay`. The properties and methods of `PixelDisplay` provide the interface to your low-resolution graphics display.
 
 The display on this page has 64 pixels in an 8-by-8 grid. Pixel coordinates are zero-indexed, just like arrays.
 
 The `setPixel(x:y:color)` method addresses an individual pixel at the specified x and y location. The `Color` type has several predefined values, as shown below.
 */
display.setPixel(x: 0, y: 0, color: .blue)
display.setPixel(x: 1, y: 3, color: .yellow)
display.setPixel(x: 5, y: 2, color: .red )
let color = Color(red: 100/255.0, green: 50/255.0, blue: 200/255.0, alpha: 1)
display.setPixel(x: 7, y: 7, color: color)
//: - callout(Experiment): Uncomment the following line. After the `color:` parameter label, type a period; then select a color from the autocompletion options.

/*:
 But you can also create any color you want. The `Color` type has three initializers. You can use autocompletion to discover them.
 
 - callout(Experiment): Uncomment the following line. Position the insertion point after `Color(`, and press escape to see all the initializers. Select an initializer to create a custom color. Try using other initializers for additional pixels.
 */

//let color = Color(red: 100/255.0, green: 50/255.0, blue: 200/255.0, alpha: 1)
//display.setPixel(x: 7, y: 7, color: color)
 
//: - callout(Exercise): Try creating a simple graphic by placing pixels of different colors on the display.

//: Next, take control of the entire display.

//: [Previous](@previous)  |  page 2 of 13  |  [Next: Controlling the Display](@next)
