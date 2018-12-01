from utils.utils import do_nms
from utils.bbox import draw_boxes
from scipy.misc import imsave
import pickle
import numpy as np
import matplotlib.pyplot as plt


old = pickle.load(open('../old.pkl', 'rb'))
new = pickle.load(open('../new.pkl', 'rb'))

for box in old:
    new.append(box)

temp = []
for box in new:
    if box.classes[0] > .35:
        temp.append(box)  
    elif box.classes[1] > .35:
        temp.append(box)

new = temp

def _interval_overlap(interval_a, interval_b):
    x1, x2 = interval_a
    x3, x4 = interval_b

    if x3 < x1:
        if x4 < x1:
            return 0
        else:
            return min(x2,x4) - x1
    else:
        if x2 < x3:
             return 0
        else:
            return min(x2,x4) - x3    

def bbox_iou(box1, box2):
    intersect_w = _interval_overlap([box1.xmin, box1.xmax], [box2.xmin, box2.xmax])
    intersect_h = _interval_overlap([box1.ymin, box1.ymax], [box2.ymin, box2.ymax])  
    
    intersect = intersect_w * intersect_h

    w1, h1 = box1.xmax-box1.xmin, box1.ymax-box1.ymin
    w2, h2 = box2.xmax-box2.xmin, box2.ymax-box2.ymin
    
    union = w1*h1 + w2*h2 - intersect
    
    return float(intersect) / union

def do_nms(boxes, nms_thresh):
    if len(boxes) > 0:
        nb_class = len(boxes[0].classes)
    else:
        return

        
    for c in range(nb_class):
        sorted_indices = np.argsort([-box.classes[c] for box in boxes])

        for i in range(len(sorted_indices)):
            index_i = sorted_indices[i]

            if boxes[index_i].classes[c] == 0: continue

            for j in range(i+1, len(sorted_indices)):
                index_j = sorted_indices[j]

                if bbox_iou(boxes[index_i], boxes[index_j]) >= nms_thresh:
                    boxes[index_j].classes[c] = 0
                    boxes[index_i].classes[c] = 0

do_nms(new, .35)
img = plt.imread("../new.tif")[:, :, [0,1,2]]
img = np.array(img).copy()

out = draw_boxes(img, new, ['residential', 'other'], .35)
imsave('../diff.png', out)

filename = '../diff.pkl'
outfile = open(filename, 'wb')
pickle.dump(new, outfile)
outfile.close()