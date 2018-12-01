import matplotlib.pyplot as plt
from scipy.misc import imsave
import os
import numpy as np
import pickle
from utils.utils import do_nms
from utils.bbox import draw_boxes


for file in ['old', 'new']:

	img = plt.imread(f"{file}.tif")[:, :, [0,1,2]]
	img = np.array(img).copy()
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

	os.system("rm tiles/*")
	os.system("mv output/*.pkl tiles/")

	boxes = []
	for tile in os.listdir("tiles"):
		row, col = map(int, tile.split('.')[0].split('_'))
		tile_boxes = pickle.load(open(f'tiles/{tile}', 'rb'))
		# adjust boxes
		for box in tile_boxes:
			box.xmin = box.xmin + col * (finalTileSize - 2*e)
			box.xmax = box.xmax + col * (finalTileSize - 2*e)
			box.ymin = box.ymin + row * (finalTileSize - 2*e)
			box.ymax = box.ymax + row * (finalTileSize - 2*e)

			boxes.append(box)

	do_nms(boxes, .35)

	filename = f'{file}.pkl'
	outfile = open(filename, 'wb')
	pickle.dump(boxes, outfile)
	outfile.close()

	out = draw_boxes(img, boxes, ['other', 'residential'], 0.35)
	imsave(f'{file}.png', out)

os.system("python diff.py")
os.system("rm old.pkl new.pkl tiles/* output/*")