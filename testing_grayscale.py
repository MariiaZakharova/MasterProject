from PIL import Image, ImageDraw
import csv
from random import randint
import os

os.system("bazel build tensorflow/examples/image_retraining:retrain")
os.system("bazel-bin/tensorflow/examples/image_retraining/retrain --image_dir ~/Envs/tf/tensorflow-master/tensorflow/examples/image_retraining/cropping/training_data --output_graph ~/Envs/tf/tensorflow-master/tensorflow/examples/label_image/data/tensorflow_inception_graph.pb --output_labels ~/Envs/tf/tensorflow-master/tensorflow/examples/label_image/data/imagenet_comp_graph_label_strings.txt --bottleneck_dir ~/Envs/tf/tensorflow-master/tensorflow/examples/label_image/data/bottleneck")
os.system("bazel build tensorflow/examples/label_image:label_image")

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

classification_coconuts = open('tensorflow/examples/image_retraining/cropping/Matlab/annotations/classification_coconuts.csv', 'w')
csv_writer1 = csv.writer(classification_coconuts)

classification_background = open('tensorflow/examples/image_retraining/cropping/Matlab/annotations/classification_background.csv', 'w')
csv_writer2 = csv.writer(classification_background)

classification_all = open('tensorflow/examples/image_retraining/cropping/Matlab/annotations/classification_all.csv', 'w')
csv_writer3 = csv.writer(classification_all)

coconut_model1 = open('tensorflow/examples/image_retraining/cropping/Matlab/detection_files/coconut_model1.txt', 'w')
coconut_model2 = open('tensorflow/examples/image_retraining/cropping/Matlab/detection_files/coconut_model2.txt', 'w')

ii = Image.open("tensorflow/examples/image_retraining/cropping/Matlab/marked_black_coconuts_background.png")

i = 0
number_of_coconuts = 0
str_for_model = " "

for y in range(50, 9760, 100):
#x=9000
#while i<1:
	for x in range(50, 10050, 100):
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
		f = open('class_info.txt', 'r')
		class_label = f.readline()
		score = f.readline()
		f.close()
		print("class: " + class_label + "\n")
		if class_label == "coconuts\n":
			new_img.save("tensorflow/examples/image_retraining/cropping/classification/coconut/img" + str(i) + ".jpg")
			csv_writer1.writerow([str(y),str(x)])
			str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + "1" + "\n"
			coconut_model1.write(str_for_model)
			number_of_coconuts = number_of_coconuts+1
		else:
			new_img.save("tensorflow/examples/image_retraining/cropping/classification/background/img" + str(i) + ".jpg")
			csv_writer2.writerow([str(y),str(x)])
			str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + "0" + "\n"
			coconut_model1.write(str_for_model)

		csv_writer3.writerow([str(y),str(x),score])
		str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + score + "\n"
		coconut_model2.write(str_for_model)		
		i = i+1

classification_coconuts.close()
classification_background.close()
classification_all.close()
coconut_model1.close()
coconut_model2.close()

print("\nNumber of coconut trees in the image: " + str(number_of_coconuts))

print("--- %s seconds ---" % (time.time() - start_time))
