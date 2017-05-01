#taking the image with black squares, cropping background images, that contain less than 0.05 black pixels
from PIL import Image
import csv
from random import randint
import os

newpath = r'tensorflow/examples/image_retraining/cropping/training_data/background' 
if not os.path.exists(newpath):
	os.makedirs(newpath)

selected_background = open('tensorflow/examples/image_retraining/cropping/Matlab/annotations/selected_background.csv', 'w')
csv_writer = csv.writer(selected_background)

i = 0
im = Image.open("tensorflow/examples/image_retraining/cropping/Matlab/annotation_black_white_on_color.png")

while i < 35:
	x = randint(50, 9950)
	y = randint(50, 9760)
	new_img = im.crop(
		(
			x-50, 
			y-50, 
			x+50, 
			y+50
		)
	)
	black = 0
	for pixel in new_img.getdata():
		if pixel == (0, 0, 0):
			black += 1
	#print(black)
	allp = len(new_img.getdata())
	per = black/allp
	#print(per)
	if per<0.05:
		print("Image " + str(i) + " " + str(x) + " " + str(y) + "\n")
		new_img.save("tensorflow/examples/image_retraining/cropping/training_data/background/background" + str(i) + ".jpg")
		csv_writer.writerow([str(y),str(x)])
		i = i+1

selected_background.close()
