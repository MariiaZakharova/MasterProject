from PIL import Image, ImageDraw
import csv
from random import randint
import os

import numpy as np
import tensorflow as tf
from io import BytesIO

#os.system("bazel build tensorflow/examples/image_retraining:retrain")
#os.system("bazel-bin/tensorflow/examples/image_retraining/retrain --image_dir tensorflow/examples/image_retraining/cropping/training_data --output_graph tensorflow/examples/label_image/data/tensorflow_inception_graph.pb --output_labels tensorflow/examples/label_image/data/imagenet_comp_graph_label_strings.txt --bottleneck_dir tensorflow/examples/label_image/data/bottleneck")

import time
start_time = time.time()

newpath = r'tensorflow/examples/image_retraining/cropping/Matlab/detection_files' 
if not os.path.exists(newpath):
	os.makedirs(newpath)

# Getting paths to the graph and class label of the retrained network
imagePath = 'tensorflow/examples/image_retraining/cropping/test2.jpg'
modelFullPath = 'tensorflow/examples/label_image/data/tensorflow_inception_graph.pb'
labelsFullPath = 'tensorflow/examples/label_image/data/imagenet_comp_graph_label_strings.txt'

# 2 functions taken from https://github.com/eldor4do/TensorFlow-Examples/blob/master/retraining-example.py and modified

# Function for creating a graph
def create_graph():
	# Creates graph from saved graph_def.pb and returns a saver.
	with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		_ = tf.import_graph_def(graph_def, name='')

# Create graph from saved GraphDef
create_graph()

# Load the labels
f = open(labelsFullPath, 'rb')
lines = f.readlines()
labels = [str(w).replace("\n", "") for w in lines]

# Function for classifying an image
def run_inference_on_image(image_patch):
	answer = None
	global largest_score
	global score_coconut
	global score_background
	global largest_label 

	largest_score = 0

	with tf.Session() as sess:

		imageBuf = BytesIO()
		image_patch.save(imageBuf, format = "JPEG")
		image_patch = imageBuf.getvalue()

		# Feed the image_patch as an input to the graph and get first prediction
		softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
		predictions = sess.run(softmax_tensor, \
			{'DecodeJpeg/contents:0': image_patch})
		predictions = np.squeeze(predictions)

		# Sort to show labels of prediction in order of confidence
		top_k = predictions.argsort()[-len(predictions):][::-1]

		for node_id in top_k:
			human_string = labels[node_id]
			score = predictions[node_id]
			if score > largest_score:
				largest_score = score
				largest_label = human_string

			if "coconut" in human_string:
				score_coconut = score

			if "background" in human_string:
				score_background = score


			print('%s (score = %.5f)' % (human_string, score))

		answer = labels[top_k[0]]
		sess.close()
	return answer


# A file containing the coordinates of each patch and classification scores for a 'coconut' and a 'background' classes
classification_coconuts_background = open('tensorflow/examples/image_retraining/cropping/Matlab/annotations/classification_coconuts_background.csv', 'w')
csv_writer_classification_coconuts_background = csv.writer(classification_coconuts_background)

#coconut_model_binary = open('tensorflow/examples/image_retraining/cropping/Matlab/detection_files/coconut_model_binary.txt', 'w')
#coconut_model_grayscale_coconuts = open('tensorflow/examples/image_retraining/cropping/Matlab/detection_files/coconut_model_grayscale_coconuts.txt', 'w')
#coconut_model_grayscale_background = open('tensorflow/examples/image_retraining/cropping/Matlab/detection_files/coconut_model_grayscale_background.txt', 'w')

# An input image with black rectangles on the places of the training samples
ii = Image.open("tensorflow/examples/image_retraining/cropping/Matlab/marked_black_coconuts_background.png")

i = 0
number_of_coconuts = 0
str_for_model = " "

for y in range(50, 9960, 20):
#x=9000
#while i<1:
	for x in range(50, 9960, 20):
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

		print("class: " + largest_label + "\n")
#		if "coconut" in largest_label:
#			new_img.save("tensorflow/examples/image_retraining/cropping/classification/coconut/img" + str(i) + ".jpg")
#			str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + "1" + "\n"
#			coconut_model_binary.write(str_for_model)
#			number_of_coconuts = number_of_coconuts+1
#		else:
#			new_img.save("tensorflow/examples/image_retraining/cropping/classification/background/img" + str(i) + ".jpg")
#			str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + "0" + "\n"
#			coconut_model_binary.write(str_for_model)

		csv_writer_classification_coconuts_background.writerow([str(y),str(x),str(score_coconut),str(score_background)])
		print(str(y),str(x),str(score_coconut),str(score_background))
#		str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + str(score_coconut) + "\n"
#		coconut_model_grayscale_coconuts.write(str_for_model)

#		str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + str(score_background) + "\n"
#		coconut_model_grayscale_background.write(str_for_model)		
		i = i+1



classification_coconuts_background.close()
#coconut_model_binary.close()
#coconut_model_grayscale_coconuts.close()
#coconut_model_grayscale_background.close()

#print("\nNumber of coconut trees in the image: " + str(number_of_coconuts))

print("--- %s seconds ---" % (time.time() - start_time))
