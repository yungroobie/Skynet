import matplotlib.pyplot as plt
from scipy.misc import imsave
import os
import numpy as np

img = plt.imread("0_old.tif")[:, :, [0,1,2]]
print(img.shape)
os.chdir("test")
for i in range(5):
	for j in range(5):
		temp = img[i*1000:(i+1)*1000, j*1000:(j+1)*1000]
		imsave(f"{i}_{j}.jpg", temp)
os.chdir('test')
out = np.zeros((5000, 5000, 3), dtype=np.uint16)
for img in os.listdir():
	temp = plt.imread(img)
	row, col = map(int, img.split('.')[0].split('_'))
	out[row*1000:(row+1)*1000, col*1000:(col+1)*1000] = temp

plt.imshow(out)
plt.show()