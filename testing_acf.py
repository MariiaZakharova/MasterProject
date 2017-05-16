from PIL import Image, ImageDraw
import csv
from random import randint
import os

import numpy as np
import tensorflow as tf
from io import BytesIO

#os.system("bazel build tensorflow/examples/image_retraining:retrain")
#os.system("bazel-bin/tensorflow/examples/image_retraining/retrain --image_dir tensorflow/examples/image_retraining/cropping/training_data --output_graph tensorflow/examples/label_image/data/tensorflow_inception_graph.pb --output_labels tensorflow/examples/label_image/data/imagenet_comp_graph_label_strings.txt --bottleneck_dir tensorflow/examples/label_image/data/bottleneck")

#os.system("python tensorflow/examples/image_retraining/retrain.py --image_dir tensorflow/examples/image_retraining/cropping/training_data --output_graph tensorflow/examples/label_image/data/tensorflow_inception_graph.pb --output_labels tensorflow/examples/label_image/data/imagenet_comp_graph_label_strings.txt --bottleneck_dir tensorflow/examples/label_image/data/bottleneck --summaries_dir tensorflow/examples/label_image/data/retrain_logs")

import time
start_time = time.time()

newpath = r'tensorflow/examples/image_retraining/cropping/Matlab/detection_files' 
if not os.path.exists(newpath):
	os.makedirs(newpath)

# Getting paths to the graph and class label of the retrained network
modelFullPath = 'tensorflow/examples/label_image/data/tensorflow_inception_graph.pb'
labelsFullPath = 'tensorflow/examples/label_image/data/imagenet_comp_graph_label_strings.txt'

# 2 functions taken from https://github.com/eldor4do/TensorFlow-Examples/blob/master/retraining-example.py and modified

# Calculate time for loading the model
start_time2 = time.time()

# Function for creating a graph
def create_graph():
	# Creates graph from saved graph_def.pb and returns a saver.
	with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		_ = tf.import_graph_def(graph_def, name='')

# Create graph from saved GraphDef
create_graph()
softmax_tensor = tf.Session().graph.get_tensor_by_name('final_result:0')

print("--- %s seconds for loading the model ---" % (time.time() - start_time2))


# Calculate time for loading the labels
start_time2 = time.time()

# Load the labels
f = open(labelsFullPath, 'rb')
lines = f.readlines()
labels = [str(w).replace("\n", "") for w in lines]

print("--- %s seconds for loading the labels ---" % (time.time() - start_time2))

# Function for classifying an image
def run_inference_on_image(image_patch):
	answer = None
#	global largest_score
	global score_coconut
	global score_background
#	global largest_label 

#	largest_score = 0

	with tf.Session() as sess:


		# Calculate time for saving an image patch to a buffer
		start_time2 = time.time()

		imageBuf = BytesIO()
		image_patch.save(imageBuf, format = "JPEG")
		image_patch = imageBuf.getvalue()

		print("--- %s seconds for saving an image patch to a buffer ---" % (time.time() - start_time2))


		# Calculate time for getting predictions for an image patch
		start_time2 = time.time()

		# Feed the image_patch as an input to the graph and get first prediction
		predictions = sess.run(softmax_tensor, \
			{'DecodeJpeg/contents:0': image_patch})
		predictions = np.squeeze(predictions)

		print("--- %s seconds for getting predictions for an image patch ---" % (time.time() - start_time2))

		
		# Calculate time for sorting the predictions
		start_time2 = time.time()

		# Sort to show labels of prediction in order of confidence
		top_k = predictions.argsort()[-len(predictions):][::-1]

		for node_id in top_k:
			human_string = labels[node_id]
			score = predictions[node_id]

#			if score > largest_score:
#				largest_score = score
#				largest_label = human_string

			if "coconut" in human_string:
				score_coconut = score

			if "background" in human_string:
				score_background = score


			print('%s (score = %.5f)' % (human_string, score))

		print("--- %s seconds for sorting the predictions ---" % (time.time() - start_time2))
		
		answer = labels[top_k[0]]
		sess.close()
	return answer


# A file containing the coordinates of each patch and classification scores for a 'coconut' and a 'background' classes
classification_coconuts_background = open('tensorflow/examples/image_retraining/cropping/Matlab/annotations/classification_coconuts_background.csv', 'w')
csv_writer_classification_coconuts_background = csv.writer(classification_coconuts_background)

# An input image with black rectangles on the places of the training samples
ii = Image.open("tensorflow/examples/image_retraining/cropping/Matlab/marked_black_coconuts_background.png")

i = 0
number_of_coconuts = 0
str_for_model = " "


with open('tensorflow/examples/image_retraining/cropping/MatlabEval/detections/output_detections_0_15.txt', 'r') as detections_file:
	for line in detections_file:
		elements = line.split(",")
		x = int(elements[1])
		y = int(elements[2])

		# Calculate time needed to process one image patch
		start_time_for_image_patch = time.time()

		print(str(i) + ": " + str(x) + " " + str(y) + "\n")
		new_img = ii.crop(
			(
				x-50, 
				y-50, 
				x+50, 
				y+50
			)
		)

		run_inference_on_image(new_img)	

		csv_writer_classification_coconuts_background.writerow([str(y),str(x),str(score_coconut),str(score_background)])
		print(str(y),str(x),str(score_coconut),str(score_background))
	
		i = i+1
		print("--- %s seconds needed to process one image patch ---" % (time.time() - start_time_for_image_patch))



classification_coconuts_background.close()

print("--- %s seconds for the whole classification process ---" % (time.time() - start_time))
