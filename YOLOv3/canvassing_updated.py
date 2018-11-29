import matplotlib.pyplot as plt
from scipy.misc import imsave
import os
import numpy as np
import pickle
from utils.utils import do_nms
from utils.bbox import draw_boxes

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

os.chdir("tiles")
os.system("rm *")
os.system("mv ../output/*.pkl .")

boxes = []
for tile in os.listdir():
	row, col = map(int, tile.split('.')[0].split('_'))
	tile_boxes = pickle.load(open(tile, 'rb'))
	# adjust boxes
	for box in tile_boxes:
		box.xmin = box.xmin + finalTileSize * row
		box.xmax = box.xmax + finalTileSize * row
		box.ymin = box.ymin + finalTileSize * col
		box.ymax = box.ymax + finalTileSize * col

		boxes.append()

do_nms(boxes, .35)
out = draw_boxes(img, boxes, ['other', 'residential'], 0.35)


imsave('../output.png', out)