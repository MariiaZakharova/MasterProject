from PIL import Image, ImageDraw
import csv
from random import randint
import os

os.system("bazel build --config=opt --config=cuda tensorflow/examples/image_retraining:retrain")
os.system("bazel-bin/tensorflow/examples/image_retraining/retrain --image_dir tensorflow/examples/image_retraining/cropping/training_data --output_graph tensorflow/examples/label_image/data/tensorflow_inception_graph.pb --output_labels tensorflow/examples/label_image/data/imagenet_comp_graph_label_strings.txt --bottleneck_dir tensorflow/examples/label_image/data/bottleneck")
os.system("bazel build --config=opt --config=cuda tensorflow/examples/label_image:label_image")

import time
start_time = time.time()

newpath = r'tensorflow/examples/image_retraining/cropping/testing_data' 
if not os.path.exists(newpath):
	os.makedirs(newpath)

newpath = r'tensorflow/examples/image_retraining/cropping/classification/background' 
if not os.path.exists(newpath):
	os.makedirs(newpath)

newpath = r'tensorflow/examples/image_retraining/cropping/classification/coconut' 
if not os.path.exists(newpath):
	os.makedirs(newpath)

newpath = r'tensorflow/examples/image_retraining/cropping/Matlab/detection_files' 
if not os.path.exists(newpath):
	os.makedirs(newpath)

# A file containing the coordinates of each patch and classification scores for a 'coconut' and a 'background' classes
classification_coconuts_background = open('tensorflow/examples/image_retraining/cropping/Matlab/annotations/classification_coconuts_background.csv', 'w')
csv_writer_classification_coconuts_background = csv.writer(classification_coconuts_background)

coconut_model_binary = open('tensorflow/examples/image_retraining/cropping/Matlab/detection_files/coconut_model_binary.txt', 'w')
coconut_model_grayscale_coconuts = open('tensorflow/examples/image_retraining/cropping/Matlab/detection_files/coconut_model_grayscale_coconuts.txt', 'w')
coconut_model_grayscale_background = open('tensorflow/examples/image_retraining/cropping/Matlab/detection_files/coconut_model_grayscale_background.txt', 'w')

# An input image with black rectangles on the places of the training samples
ii = Image.open("tensorflow/examples/image_retraining/cropping/Matlab/marked_black_coconuts_background.png")

i = 0
number_of_coconuts = 0
str_for_model = " "

for y in range(50, 9950, 20):
#x=9000
#while i<1:
	for x in range(50, 9950, 20):
		print(str(i) + ": " + str(x) + " " + str(y) + "\n")
		new_img = ii.crop(
			(
				x-50, 
				y-50, 
				x+50, 
				y+50
			)
		)
		new_img.save("tensorflow/examples/image_retraining/cropping/testing_data/img" + str(i) + ".jpg")
		os.system("bazel-bin/tensorflow/examples/label_image/label_image --graph=tensorflow/examples/label_image/data/tensorflow_inception_graph.pb --labels=tensorflow/examples/label_image/data/imagenet_comp_graph_label_strings.txt --output_layer=final_result --image=tensorflow/examples/image_retraining/cropping/testing_data/img" + str(i) + ".jpg")
		f = open('tensorflow/examples/image_retraining/cropping/class_info.txt', 'r')
		class_label = f.readline()
		score_coconuts = f.readline()
		score_background = f.readline()
		f.close()
		print("class: " + class_label + "\n")
		if class_label == "coconuts\n":
			new_img.save("tensorflow/examples/image_retraining/cropping/classification/coconut/img" + str(i) + ".jpg")
			str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + "1" + "\n"
			coconut_model_binary.write(str_for_model)
			number_of_coconuts = number_of_coconuts+1
		else:
			new_img.save("tensorflow/examples/image_retraining/cropping/classification/background/img" + str(i) + ".jpg")
			str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + "0" + "\n"
			coconut_model_binary.write(str_for_model)

		csv_writer_classification_coconuts_background.writerow([str(y),str(x),str(score_coconuts),str(score_background)])

		str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + score_coconuts + "\n"
		coconut_model_grayscale_coconuts.write(str_for_model)

		str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + score_background + "\n"
		coconut_model_grayscale_background.write(str_for_model)		
		i = i+1

classification_coconuts_background.close()
coconut_model_binary.close()
coconut_model_grayscale_coconuts.close()
coconut_model_grayscale_background.close()

print("\nNumber of coconut trees in the image: " + str(number_of_coconuts))

print("--- %s seconds ---" % (time.time() - start_time))
