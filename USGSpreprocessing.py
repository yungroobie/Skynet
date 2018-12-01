import os
import zipfile
import fnmatch
import shutil

# File paths -------------------------------------------------------------------
# path to directory of zipped files from USGS
source = "C:\\Users\\Brian\\Desktop\\USGS"
# path to new directory containing images to label
dest = "C:\\Users\\Brian\\Desktop\\images"

# Unzip USGS files ------------------------------------------------------------
os.chdir(source)
for file in os.listdir():
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall()

# Recursively search for images and save paths --------------------------------
images = []
for root, dirs, files in os.walk(source+"\\VA"):
    for name in files:
        if fnmatch.fnmatch(name, '*.tif'):
            images.append(os.path.join(root, name))

# Move images into new directory ----------------------------------------------
os.mkdir(dest)
for image in images:
    shutil.move(image, dest)

# Rename files to make relationships clear ------------------------------------

os.chdir(dest)
files = os.listdir()
for i in range(0, len(files), 2):
    os.rename(files[i], f"{i}_new.tif")
    os.rename(files[i+1], f"{i}_old.tif")
