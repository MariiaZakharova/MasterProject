import csv

coconut_model_0_00 = open('tensorflow/examples/image_retraining/cropping/Matlab/detection_files/coconut_model_0_15.txt', 'w')

i = 0
r = 0

with open('tensorflow/examples/image_retraining/cropping/Matlab/annotations/classification_coconuts_background_0_15.csv', 'r') as detections_file:
	spamreader = csv.reader(detections_file, delimiter = ',', quotechar = ',')
	for row in spamreader:
		x = int(row[1])
		y = int(row[0])
		score = float(row[2])
		print("Image " + str(i) + " " + str(x) + " " + str(y) + " " + str(score) + "\n")
		str_for_model = "1," + str(x) + "," + str(y) + ",100,100," + str(score) + "\n"
		coconut_model_0_00.write(str_for_model)
		i = i+1

coconut_model_0_00.close()
detections_file.close()
