from PIL import Image, ImageDraw
import csv
from random import randint
import os

os.system("bazel build tensorflow/examples/label_image:label_image")

import time
start_time = time.time()

newpath = r'tensorflow/examples/image_retraining/cropping/classification2/background2' 
if not os.path.exists(newpath):
	os.makedirs(newpath)

newpath = r'tensorflow/examples/image_retraining/cropping/classification2/coconut2' 
if not os.path.exists(newpath):
	os.makedirs(newpath)

newpath = r'tensorflow/examples/image_retraining/cropping/Matlab/detection_files' 
if not os.path.exists(newpath):
	os.makedirs(newpath)

# A file containing the coordinates of each patch and classification scores for a 'coconut' and a 'background' classes
classification_coconuts_background = open('tensorflow/examples/image_retraining/cropping/Matlab/annotations/classification_coconuts_background2.csv', 'w')
csv_writer_classification_coconuts_background = csv.writer(classification_coconuts_background)

coconut_model_binary = open('tensorflow/examples/image_retraining/cropping/Matlab/detection_files/coconut_model_binary2.txt', 'w')
coconut_model_grayscale_coconuts = open('tensorflow/examples/image_retraining/cropping/Matlab/detection_files/coconut_model_grayscale_coconuts2.txt', 'w')
coconut_model_grayscale_background = open('tensorflow/examples/image_retraining/cropping/Matlab/detection_files/coconut_model_grayscale_background2.txt', 'w')

i = 0
number_of_coconuts = 0
str_for_model = " "

# Classification for coconut training data

with open('tensorflow/examples/image_retraining/cropping/Matlab/annotations/selected_coconuts.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter = ',', quotechar = ',')
	for row in spamreader:
		x = float(row[1])
		y = float(row[0])
		print(str(i) + ": " + str(x) + " " + str(y) + "\n")
		new_img = Image.open("tensorflow/examples/image_retraining/cropping/training_data/coconuts/coconut" + str(i) + ".jpg")
		os.system("bazel-bin/tensorflow/examples/label_image/label_image --graph=tensorflow/examples/label_image/data/tensorflow_inception_graph.pb --labels=tensorflow/examples/label_image/data/imagenet_comp_graph_label_strings.txt --output_layer=final_result --image=tensorflow/examples/image_retraining/cropping/training_data/coconuts/coconut" + str(i) + ".jpg")
		with open('tensorflow/examples/image_retraining/cropping/class_info.csv', newline='') as csvfile:
			spamreader2 = csv.reader(csvfile, delimiter = ',', quotechar = ',')
			for row in spamreader2:
				class_label = row[0]
				score_coconuts = float(row[1])
				score_background = float(row[2])
		print("class: " + class_label + "\n")
		if class_label == "coconuts":
			new_img.save("tensorflow/examples/image_retraining/cropping/classification2/coconut2/img" + str(i) + ".jpg")
			str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + "1" + "\n"
			coconut_model_binary.write(str_for_model)
			number_of_coconuts = number_of_coconuts+1
		else:
			new_img.save("tensorflow/examples/image_retraining/cropping/classification2/background2/img" + str(i) + ".jpg")
			str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + "0" + "\n"
			coconut_model_binary.write(str_for_model)

		csv_writer_classification_coconuts_background.writerow([str(y),str(x),str(score_coconuts),str(score_background)])

		str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + str(score_coconuts) + "\n"
		coconut_model_grayscale_coconuts.write(str_for_model)

		str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + str(score_background) + "\n"
		coconut_model_grayscale_background.write(str_for_model)		
		i = i+1

# Classification for background training data

i = 0
str_for_model = " "

with open('tensorflow/examples/image_retraining/cropping/Matlab/annotations/selected_background.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter = ',', quotechar = ',')
	for row in spamreader:
		x = float(row[1])
		y = float(row[0])
		print(str(i) + ": " + str(x) + " " + str(y) + "\n")
		new_img = Image.open("tensorflow/examples/image_retraining/cropping/training_data/background/background" + str(i) + ".jpg")
		os.system("bazel-bin/tensorflow/examples/label_image/label_image --graph=tensorflow/examples/label_image/data/tensorflow_inception_graph.pb --labels=tensorflow/examples/label_image/data/imagenet_comp_graph_label_strings.txt --output_layer=final_result --image=tensorflow/examples/image_retraining/cropping/training_data/background/background" + str(i) + ".jpg")
		with open('tensorflow/examples/image_retraining/cropping/class_info.csv', newline='') as csvfile:
			spamreader2 = csv.reader(csvfile, delimiter = ',', quotechar = ',')
			for row in spamreader2:
				class_label = row[0]
				score_coconuts = float(row[1])
				score_background = float(row[2])
		print("class: " + class_label + "\n")
		if class_label == "coconuts":
			new_img.save("tensorflow/examples/image_retraining/cropping/classification2/coconut2/img" + str(i) + ".jpg")
			str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + "1" + "\n"
			coconut_model_binary.write(str_for_model)
			number_of_coconuts = number_of_coconuts+1
		else:
			new_img.save("tensorflow/examples/image_retraining/cropping/classification2/background2/img" + str(i) + ".jpg")
			str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + "0" + "\n"
			coconut_model_binary.write(str_for_model)

		csv_writer_classification_coconuts_background.writerow([str(y),str(x),str(score_coconuts),str(score_background)])

		str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + str(score_coconuts) + "\n"
		coconut_model_grayscale_coconuts.write(str_for_model)

		str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + str(score_background) + "\n"
		coconut_model_grayscale_background.write(str_for_model)		
		i = i+1


classification_coconuts_background.close()
coconut_model_binary.close()
coconut_model_grayscale_coconuts.close()
coconut_model_grayscale_background.close()

print("\nNumber of coconut trees in the image: " + str(number_of_coconuts))

print("--- %s seconds ---" % (time.time() - start_time))
