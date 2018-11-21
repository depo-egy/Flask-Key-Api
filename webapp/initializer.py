from webapp.packages.preprocess_test import preprocesses
from PIL import Image
from resizeimage import resizeimage
import os
import cv2
import sys
input_datadir = './trained_img'
output_datadir = './pre_img'
obj=preprocesses(input_datadir,output_datadir)

nrof_images_total,nrof_successfully_aligned=obj.collect_data()


print(type(nrof_images_total))
print('Total number of images: %d' % nrof_images_total)
print('Number of successfully aligned images: %d' % nrof_successfully_aligned)
