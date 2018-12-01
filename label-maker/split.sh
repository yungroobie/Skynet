#! /bin/bash
rm -rf train
rm -rf val
rm -rf annots
rm -rf val_annots

python format.py

mkdir train
mkdir val
mkdir annots
mkdir val_annots

mv `ls *.jpg | tail -800` val
mv *.jpg train
mv `ls *.xml | tail -800` val_annots
mv *.xml annots