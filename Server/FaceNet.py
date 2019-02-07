import numpy as np
import time
import tensorflow as tf
from fr_utils import *
from inception_blocks_v2 import *
from keras import backend as K
from threading import Thread
import FaceNetFunctions
    
# Starts the FaceNet model, compiles it in a thread to help with conjestion
class FaceNet(Thread):

    def __init__(self):
    	# TODO: Need to change the image size
        self.image_size = 96
        self.isDone = False
        Thread.__init__(self)
        # Set the format of keras so a 100 x 100 RGB image has shap(3, 100, 100)
        K.set_image_data_format("channels_first")
    
    # Function that will run asynchronously, creates the FaceNet model
    def run(self):
        # Create and compile the model
        self.FRmodel = faceRecoModel(input_shape=(3, self.image_size, self.image_size))
        self.FRmodel.compile(optimizer='adam', loss=FaceNetFunctions.triplet_loss, metrics=['accuracy'])
        load_weights_from_FaceNet(self.FRmodel)
        
        # Prepare the database of faces
        self.database = FaceNetFunctions.prepare_database(self.FRmodel)
        self.isDone = True

    def findIdentity(self, image):
        return FaceNetFunctions.find_identity(image, self.database, self.FRmodel)


if __name__=='__main__':

    test_image = cv2.imread('images/Evan.jpg')

    print('compiling model')
    model = FaceNet()
    model.start()
    num = 0
    # Check if the model is done compiling before continuing
    while True:
        if not model.isDone:
            print('not done yet')
            num += 1
            time.sleep(10)
        else:
            break
    print('model finished')
    print('Testing identity')
    print(model.findIdentity(test_image))

    