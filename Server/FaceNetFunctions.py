import numpy as np
import tensorflow as tf
import glob
import os
from fr_utils import *
from inception_blocks_v2 import *

# Activation function for the FaceNet model to calculate loss
def triplet_loss(y_true, y_pred, alpha = 0.3):
    # anchor and positive image are from the same person and negative is from someone else
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]

    # Calculate the distance from the achor to the positive and negative images(euclidean distance)
    positive_distance = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)), axis=-1)
    negative_distance = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)), axis=-1)

    # Loss is the distance between the two images, but add alpha so loss != 0
    basic_loss = tf.add(tf.subtract(positive_distance, negative_distance), alpha)

    # Gets the max of the array and do a reduce su
    loss = tf.reduce_sum(tf.maximum(basic_loss, 0.0))

    return loss

# Function for determining the identity
def who_is_it(image, database, model):
	# from fr_utils.py
	encoding = img_to_encoding(image, model)

	min_distance = 100
	identity = None

	#Loop over the dictionary of names and encodings
	for (name, enc) in database.items():
		dist = np.linalg.norm(enc - encoding)
		print("distance for %s is %s" %(name, dist))

		# change to what I want
		if dist > 0.8:
			continue
		else:
			return name

# Prepares the images to be processed by the FaceNet
def prepare_database(model):
    database = {}

    # get every image in the directory
    for file in glob.glob("images/*"):
        # split the image and get the name of the person
        identity = os.path.splitext(os.path.basename(file))[0]
        # from fr_utils.py
        database[identity] = img_path_to_encoding(file, model)

    return database

# Takes a frame to find the person in it
def find_identity(frame, database, model):
	height, width, channels = frame.shape
	return who_is_it(frame, database, model)