from PIL import Image
import numpy as np

im = Image.open('icon.png')
im = im.convert('RGBA')

data = np.array(im)   # "data" is a height x width x 4 numpy array
red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
print(data.T)

# Replace white with red... (leaves alpha values alone...)
white_areas = (red == 0) & (blue == 0) & (green == 0)
data[..., :-1][white_areas.T] = (0, 0, 255) # Transpose back needed

im2 = Image.fromarray(data)
im2.show()
im2.save("icon2.png", "png")