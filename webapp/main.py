#Main function for face detection
from webapp.initializer import*
from webapp.classifier_train import*
#import os
from PIL import Image
from resizeimage import resizeimage
import cv2




class Initialize:
    def __init__(self):
        
            
        input_datadir = initializer.input_datadir
        output_datadir = initializer.output_datadir
        self=preprocesses(input_datadir,output_datadir)
        nrof_images_total,nrof_successfully_aligned=self.collect_data()
        print('Total number of images: %d' % nrof_images_total)
        print('Number of successfully aligned images: %d' % nrof_successfully_aligned)




class Train:
    def __init__(self):
        datadir = './pre_img'
        modeldir = './20180402-114759.pb'
        classifier_filename = './class/classifier.pkl'
        print ("Training Start")
        self=training(datadir,modeldir,classifier_filename)
        get_file=self.main_train()
        print('Saved classifier model to file "%s"' % get_file)
        sys.exit("All Done")

def main():
    initialize = Initialize()
    train = Train()


if __name__ == '__main__':
    main()
        
