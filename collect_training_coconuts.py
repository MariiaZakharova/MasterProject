#taking the input image, cropping palms from it
from PIL import Image, ImageDraw
import csv
from random import randint
import os

newpath = r'tensorflow/examples/image_retraining/cropping/training_data/coconuts' 
if not os.path.exists(newpath):
	os.makedirs(newpath)

selected_coconuts = open('tensorflow/examples/image_retraining/cropping/Matlab/annotations/selected_coconuts.csv', 'w')
csv_writer1 = csv.writer(selected_coconuts)

leftover_coconuts = open('tensorflow/examples/image_retraining/cropping/Matlab/annotations/leftover_coconuts.csv', 'w')
csv_writer2 = csv.writer(leftover_coconuts)

i = 0
r = 0
ii = Image.open("tensorflow/examples/image_retraining/cropping/coconut.png")

with open('tensorflow/examples/image_retraining/cropping/coords.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter = ',', quotechar = ',')
	for row in spamreader:
		r = randint(0, 20)
		if float(row[1])<9950 and float(row[0])<9760 and float(row[1])>50 and float(row[0])>50 and r==1 and i<35:
			x = float(row[1])
			y = float(row[0])
			print("Image " + str(i) + " " + str(x) + " " + str(y) + "\n")
			new_img = ii.crop(
				(
					x-50, 
					y-50, 
					x+50, 
					y+50
				)
			)
			new_img.save("tensorflow/examples/image_retraining/cropping/training_data/coconuts/coconut" + str(i) + ".jpg")
			csv_writer1.writerow(row)
			i = i+1
		else:
			csv_writer2.writerow(row)
selected_coconuts.close()
leftover_coconuts.close()
