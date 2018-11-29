import matplotlib.pyplot as plt
from scipy.misc import imsave
import os
import numpy as np

img = plt.imread("5356c.tif")[:, :, [0,1,2]]
t = 5
e = 100
m = img.shape[0]
n = img.shape[1]
tileSpaceRight = n/t
tileSpaceDown = m/t
extraTileSpace = ((t-1)*(2*e))/t
#finalTileSize = int(tileSpace + extraTileSpace)

print(img.shape)
os.chdir("test")
for i in range(t):
	for j in range(t):
		startx = ((i*tileSpaceRight) - i * (2*e)) + (i*extraTileSpace)
		print(round(startx))
		endx = startx + tileSpaceRight + extraTileSpace
		print(round(endx))
		starty = ((j*tileSpaceDown) - j * (2*e)) + (j*extraTileSpace)
		print(round(starty))
		endy = starty + tileSpaceDown + extraTileSpace
		print(round(endy))
		temp = img[int(round(starty)):int(round(endy)), int(round(startx)):int(round(endx))]
		print(temp.shape)
		imsave(f"{i}_{j}.jpg", temp)
#Replace with image size
out = np.zeros((8600, 13100, 3), dtype=np.uint16)
for image in os.listdir():
	temp = plt.imread(image)
	row, col = map(int, image.split('.')[0].split('_'))
	startx = ((row*tileSpaceRight) - row * (2*e)) + (row*extraTileSpace)
	endx = startx + tileSpaceRight + extraTileSpace
	starty = ((col*tileSpaceDown) - col * (2*e)) + (col*extraTileSpace)
	endy = starty + tileSpaceDown + extraTileSpace
	out[int(round(starty)):int(round(endy)), int(round(startx)):int(round(endx))] = temp

plt.imshow(out)
#plt.imshow(img)
plt.show()