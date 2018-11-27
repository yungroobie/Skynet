import matplotlib.pyplot as plt
from scipy.misc import imsave
import os
import numpy as np

img = plt.imread("terrace.tif")[:, :, [0,1,2]]
t = 5
e = 100
n = img.shape[0]
tileSpace = n/t
extraTileSpace = ((t-1)*(2*e))/t
finalTileSize = int(tileSpace + extraTileSpace)

print(img.shape)
os.chdir("test")
for i in range(t):
	for j in range(t):
		startx = ((i*tileSpace) - i * (2*e)) + (i*extraTileSpace)
		endx = startx + tileSpace + extraTileSpace
		starty = ((j*tileSpace) - j * (2*e)) + (j*extraTileSpace)
		endy = starty + tileSpace + extraTileSpace
		temp = img[int(round(startx)):int(round(endx)), int(round(starty)):int(round(endy))]
		imsave(f"{i}_{j}.jpg", temp)
out = np.zeros((5000, 5000, 3), dtype=np.uint16)
for image in os.listdir():
	temp = plt.imread(image)
	row, col = map(int, image.split('.')[0].split('_'))
	startx = ((row*tileSpace) - row * (2*e)) + (row*extraTileSpace)
	endx = startx + tileSpace + extraTileSpace
	starty = ((col*tileSpace) - col * (2*e)) + (col*extraTileSpace)
	endy = starty + tileSpace + extraTileSpace
	out[int(round(startx)):int(round(endx)), int(round(starty)):int(round(endy))] = temp

plt.imshow(out)
#plt.imshow(img)
plt.show()