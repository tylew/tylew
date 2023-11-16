from seekPixel import seekPixel

# F(pix) = rotation degrees
eq = lambda x: (float(x) - 154.3) / -1.64
seekPixel.setSeekOperation(eq)

# Find motor pos. for pixel #43
print(seekPixel.getMotorPosition(43))