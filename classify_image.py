# import the necessary packages
from keras.applications import ResNet50
from keras.applications import InceptionV3
from keras.applications import Xception # TensorFlow ONLY
from keras.applications import VGG16
from keras.applications import VGG19
from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import numpy as np
import argparse, os

def is_image(f):
	if len(f.split(".")) > 1:
		return f.split(".")[1] in ["jpg", "jpeg", "png", "gif"]
	return False
	
def get_directory_files(directory):
	files_array = []
	for path, subdirs, files in os.walk(directory):
		for filename in files:
			f = os.path.join(path, filename)
			if is_image(f):
				files_array.append(f)
	return files_array

def get_img_info(directory):
	dictionary = {}
	dictionary["Files"] = {}
	dictionary["Keyword"] = {}
	files = get_directory_files(directory)
	for f in files: 
		f_result = img_classify(f)
		dictionary["Files"][f] = f_result
		for rank_result in f_result: 
			rank, label, prediction = rank_result
			if prediction > 50: 
				if label not in dictionary["Keyword"]:
					dictionary["Keyword"][label] = []
				dictionary["Keyword"][label].append((f, prediction))
	return dictionary

def img_classify(image, model='vgg16'):
	# define a dictionary that maps model names to their classes
	# inside Keras
	MODELS = {
		"vgg16": VGG16, 
		"vgg19": VGG19, 
		"inception": InceptionV3, 
		"xception": Xception, 
		"resnet": ResNet50
	}

	if model not in MODELS.keys(): 
		raise AssertionError("The --model command line argument should"
			"be a key in the `MODELS` directory")

	# initialize the input image shape (224x224 pixels) along with
	# the pre-processing function (this might need to be changed
	# based on which model we use to classify our image)
	inputShape = (224, 224)
	preprocess = imagenet_utils.preprocess_input

	# if we are using the InceptionV3 or Xception networks, then we
	# need to set the input shape to (299x299) [rather than (224x224)]
	# and use a different image processing function
	if model in ("inception", "xception"):
		inputShape = (299, 299)
		preprocess = preprocess_input


	# load our the network weights from disk (NOTE: if this is the
	# first time you are running this script for a given network, the
	# weights will need to be downloaded first -- depending on which
	# network you are using, the weights can be 90-575MB, so be
	# patient; the weights will be cached and subsequent runs of this
	# script will be *much* faster)
	print("[INFO] loading {}...".format(model))
	Network = MODELS[model]
	model = Network(weights="imagenet")

	# load the input image using the Keras helper utility while ensuring
	# the image is resized to `inputShape`, the required input dimensions
	# for the ImageNet pre-trained network
	print("[INFO] loading and pre-processing image...")
	image = load_img(image, target_size=inputShape)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = preprocess(image)

	# classify the image
	print("[INFO] classifying the image with '{}'...".format(model))
	preds = model.predict(image)
	P = imagenet_utils.decode_predictions(preds)

	# loop over the predictions and display the rank-5 
	# predictions + probabilities to our terminal
	format_string = lambda x: " ".join(x.split("_"))
	array = []
	for (i, (imagenetID, label, prob)) in enumerate(P[0]):
		array.append([i + 1, format_string(label), round(prob * 100, 2)])
	return array
