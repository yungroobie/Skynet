import numpy as np
import matplotlib.pyplot as plt
import cv2

data = np.load('data.npz')
X = data['x']
y = data['y']

datas = []
for i in range(X.shape[0]):
    # fix class labels
    y[i, :, 4] = [0 if j <= 9 else 1 for j in y[i, :, 4]]
    
    temp = [X[i] / np.float16(255.), y[i]]
    datas.append(temp)

datas = np.array(datas)
np.random.shuffle(datas)

del(X)
del(y)

# eliminate bad boxes and zero-padding
for idx, img in enumerate(datas):
    adj = np.array([])
    for box in img[1]:
        if np.count_nonzero(box) != 0:
            if box[0] < box[2] and box[1] < box[3]:
                if adj.size == 0:
                    adj = box
                else:
                    adj = np.vstack((adj, box,))
    datas[idx][1] = adj

np.save('formatted_data.npy', datas)