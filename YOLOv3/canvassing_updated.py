import matplotlib.pyplot as plt
from scipy.misc import imsave
import os
import numpy as np



img = plt.imread("7_old.tif")[:, :, [0,1,2]]
t = 5
e = 100
n = img.shape[0]
tileSpace = n/t
extraTileSpace = ((t-1)*(2*e))/t
finalTileSize = int(tileSpace + extraTileSpace)

print(img.shape)
for i in range(t):
	for j in range(t):
		startx = ((i*tileSpace) - i * (2*e)) + (i*extraTileSpace)
		endx = startx + tileSpace + extraTileSpace
		starty = ((j*tileSpace) - j * (2*e)) + (j*extraTileSpace)
		endy = starty + tileSpace + extraTileSpace
		temp = img[int(round(startx)):int(round(endx)), int(round(starty)):int(round(endy))]
		imsave(f"tiles/{i}_{j}.jpg", temp)
os.system("python predict.py -c config.json -i tiles/")
os.system("mv output/*.jpg tiles/")
out = np.zeros((5000, 5000, 3), dtype=np.uint16)
os.chdir("tiles")
for image in os.listdir():
	temp = plt.imread(image)
	row, col = map(int, image.split('.')[0].split('_'))
	startx = ((row*tileSpace) - row * (2*e)) + (row*extraTileSpace)
	endx = startx + tileSpace + extraTileSpace
	starty = ((col*tileSpace) - col * (2*e)) + (col*extraTileSpace)
	endy = starty + tileSpace + extraTileSpace
	out[int(round(startx)):int(round(endx)), int(round(starty)):int(round(endy))] = temp

imsave('../output.png', out)
os.system("rm *")
os.system("mv ../output/*.pkl .")
