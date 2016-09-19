import os
import numpy
from scipy import ndimage, misc, signal

images = []
data_dir = "Data"
for entry in os.listdir(data_dir):
	newfile = ndimage.imread(data_dir + "/" +  entry)
	newfile = misc.imresize(newfile, 3)
	#print(entry)
	#print(newfile)
	#print("_____________________")
	images.append(newfile)
#print(type(images))
images = numpy.array(images)
#print(type(images))
#print(images)

baseline = images[0]
for image in images[1:]:
	print(signal.fftconvolve(baseline,image[::-1, ::-1]))
