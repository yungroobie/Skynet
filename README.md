# Skynet
Welcome to Skynet, an automated address canvassing model using satellite imagery.

# 1. Preprocessing and Config file
First, ensure your data has been partitioned into training and validation sets. Then place the images and the corresponding the labels into two separete directories for each set. This should produce four directories: 
```python
    /train_images/ #Directory for training image files
    /train_annotations/ #Directory for training annotation labels
    /val_images/ #Directory for validation image files
    /val_annotations/ #Directory for validation annotation labels
```
These directories should be defined in the ```config.json``` file under their respective fields. 

Any appropriate changes to any other fields should be made at this time. This includes editing the names of the 
class labels, generating anchor boxes with the command ```python gen_anchors.py -c config.json```, and specifying the weights file to be used. 

If the model is being trained for the first time, then ensure the ```backend.h5``` file is in the YOLOv3 directory as those
weights will be used to kick off the training. (This does not need to be specified in the config file) 

# 2. Train the Model
To train the model, run the command:

```python 
python train.py -c config.json
```

Training the model will produce a weights file that contains the model weights for your particular data set. 
This weights file name is designated by the ```saved_weights_name``` field in the config file and can be used
as a checkpoint for restarting training. Training concludes after 5 consecutive epochs did not have an improve in loss. 

# 3. Address Canvassing 
To perform address canvassing on a set of before and after images, run the appropriate canvassing command. For square images, that would be:

```python
python canvassing_square.py
```
Make sure the before and after images are in the root Skynet directory and are named ```old.tif``` and ```new.tif``` respectivly. In the current version, these images will be broken down into tiles to better resemble our training set; this way the model will be able to make accurate predictions. The model will then identify residences in the images and highlight the differences, indicating where new addresses have appeared, and stitch the tiles back together. These differences can be seen in the ```diff.png``` output image.  


# TODO 
+ Finish GUI
+ Canvassing on rectangular images
+ Distiction between if addresses were added or removed

