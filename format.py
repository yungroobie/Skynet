import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.misc import imsave
import xml.etree.ElementTree as ET


def to_xml(filename, annots):
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = "train_annotations"
    ET.SubElement(annotation, "filename").text = f'{filename}.jpg'

    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Address Canvassing"
    ET.SubElement(source, "annotations").text = "Address Canvassing"
    ET.SubElement(source, "image").text = "Mapbox"

    image = ET.SubElement(annotation, "size")
    ET.SubElement(image, "width").text = "256"
    ET.SubElement(image, "height").text = "256"
    ET.SubElement(image, "depth").text = "3"

    ET.SubElement(annotation, "segmented").text = "0"
    for box in annots:
        object = ET.SubElement(annotation, "object")
        if int(box[4]) == 0:
            ET.SubElement(object, "name").text = 'residential'
        else:
            ET.SubElement(object, "name").text = 'other'
        bndbox = ET.SubElement(object, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(box[0])
        ET.SubElement(bndbox, "ymin").text = str(box[1])
        ET.SubElement(bndbox, "xmax").text = str(box[2])
        ET.SubElement(bndbox, "ymax").text = str(box[3])

    data = ET.tostring(annotation)
    file = open(f"{filename}.xml", 'wb')
    file.write(data)
    file.close()

data = np.load('data.npz')
X = data['x']
y = data['y']

data = []
for i in range(X.shape[0]):
    # fix class labels
    # 0 for residential, 1 for commercial/other, 2 for images to delete
    y[i, :, 4] = [0 if j <= 9 else 2 if j == 57 else 1 for j in y[i, :, 4]]
    
    temp = [X[i], y[i]]
    data.append(temp)

# Free up some memory
del(X)
del(y)

# Shuffle data
data = np.array(data)
np.random.shuffle(data)

# eliminate bad boxes and zero-padding
for idx, img in enumerate(data):
    adj = np.zeros((1, 5))
    for box in img[1]:
        # Don't add boxes with label of 2
        if box[4] == 2:
            continue
        # check if box is 'proper'
        if (box[0] < box[2]) and (box[1] < box[3]):
            if np.count_nonzero(adj) == 0:
                adj = np.expand_dims(box, 0)
            else:
                adj = np.vstack((adj, box))
    if np.count_nonzero(adj) != 0:
        imsave(f'{idx}.jpg', img[0])
        to_xml(idx, adj)