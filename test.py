from PIL import Image
import numpy as np

orig_color = (254,200,94)
replacement_color = (0,0,0)
img = Image.open("icon.png").convert('RGB')
data = np.array(img)
data[(data == orig_color).all(axis = -1)] = replacement_color
img2 = Image.fromarray(data, mode='RGB')
img2.show()