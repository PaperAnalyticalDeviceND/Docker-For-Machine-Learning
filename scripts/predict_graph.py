#####################################################
# Tensorflow prediction for PADs using Caffenet CNN #
# @author Chris Sweet <csweet1@nd.edu>              #
# @version 1.0 11/15/18                             #
#####################################################

#~Load libraries~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# We need tensorflow and numpy for training the CNN,
# matplotlib for plotting, os.path and PIL for loading images,
# and random to partition the data into test and training sets
import tensorflow as tf
import numpy as np
#from matplotlib import pyplot as plt
import math
from os.path import dirname, abspath
from os.path import join
import os.path
import PIL
import random
#import urllib.request
from PIL import Image, ImageEnhance, ImageStat
import sys
import getopt
import copy

#~get inlines~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#inline parameter?
optlist, args = getopt.getopt(sys.argv[1:], 'i:n:dr:')

#image to analyzed
image_location = '/var/www/html/joomla/images/padimages/processed//Acetaminophen-12LanePADKenya2015-1-58861.processed.png'
nnet_file = 'tensor_100_9.nnet'
debug_print = False
randpart = ''

for o, a in optlist:
    if o == '-i':
        image_location = a
    elif o == '-n':
        nnet_file = a
    elif o == '-r':
        randpart = a
    elif o == '-d':
        debug_print = True
    else:
        print('Unhandled option: ', o)
        sys.exit(-2)

if debug_print:
    print("Image location", image_location)
    print("Network definition file location", nnet_file)

#~Read network definition file~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#open and read file
with open(nnet_file) as fin:
    content = fin.readlines()

fin.close()

#strip spaces
content = [x.strip() for x in content]

#parse contents of definition file
drugs = ""
exclude = ""
model_checkpoint = ""
type = ""

for line in content:
    if 'DRUGS' in line:
        drugs = line[6:].split(',')
    elif 'LANES' in line:
        exclude = line[6:]
    elif 'WEIGHTS' in line:
        model_checkpoint = line[8:]
    elif 'TYPE' in line:
        type = line[5:]

#test for Tensorflow
if type != "tensorflow":
    print('Not tensorflow network!')
    sys.exit(-2)

if debug_print:
    print("Type", type)
    print("Drugs", drugs, len(drugs))
    print("Exclude", exclude)
    print("Model", model_checkpoint)

#~variables~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
classes = len(drugs) #9 #Amoxicillin rerun,Acetaminophen,Ciprofloxacin,Ceftriaxone,Metformin,Ampicillin,Azithromycin,Cefuroxime Axetil,Levofloxacin

#~Identification~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#location of the weights/biases and architecture for the CNN (saved above)
#model_for_identification = model_checkpoint

#called to identify subject in image
def identify(image):
    #reshape the image to an (1, 154587) vector
    image = np.mat(np.asarray(image).flatten())
    #create session
    with tf.Session() as sess:
        #load in the saved weights
        saver = tf.train.import_meta_graph(model_checkpoint+'.meta')
        saver.restore(sess, model_checkpoint)#tf.train.latest_checkpoint('tf_checkpoints/', model_for_identification+'.index'))

        #get graph to extract tensors
        graph = tf.get_default_graph()
        pred = graph.get_tensor_by_name("pred:0")
        output = graph.get_tensor_by_name("output:0")
        X = graph.get_tensor_by_name("X:0")
        keep_prob = graph.get_tensor_by_name("keep_prob:0")

        #saver.restore(sess, model_for_identification)

        #find the prediction
        result = sess.run(pred, feed_dict={X: image, keep_prob: 1.})
        #we can look at the softmax output as well
        prob_array = sess.run(output, feed_dict={X: image, keep_prob: 1.})
        #print("result",result,"prob",prob_array)

        #return result (add 1 as indexed from 1 not 0)
        return result[0], prob_array


#load drug names, now loaded in nnet file
#f = open('drug_names.txt')
#firstline = f.readline()
#drugs = firstline.split(',')

#get it
#urllib.request.urlretrieve( 'https://pad.crc.nd.edu/images/padimages/processed//Acetaminophen-12LanePADKenya2015-1-58861.processed.png', 'test.jpg')
#Load png file using the PIL library
img = PIL.Image.open(image_location)

#check image rectified
width, height = img.size
if width != 730 or (height != 1220 and height != 1250):
    print("Image not rectified "+str(width)+", "+str(height))
    sys.exit(-3)

#crop out active area
img = img.crop((71, 359, 71+636, 359+490))
#lanes split
lane = []

#exclude these lanes, now loaded from nnet file
#exclude = "AJ"

#loop over lanes
for i in range(0,12):
    if chr(65+i) not in exclude:
        lane.append(img.crop((53*i, 0, 53*(i+1), 490)))

#reconstruct
imgout = Image.new("RGB", (53 * len(lane), 490))

#loop over lanes
for i in range(0,len(lane)):
    imgout.paste(lane[i], (53*i, 0, 53*(i+1), 490))

#resize
imgout = imgout.resize((227,227), Image.ANTIALIAS)

#show it
#imgplot = plt.imshow(imgout)

#catagorize
predicted_drug, predicted_prob = identify(imgout)

#output to emulate caffe classifier
if randpart != '':
    #find the highest probability
    temppred = copy.deepcopy(predicted_prob[0])
    pClass1 = temppred.argmax()

    temppred[pClass1] = -1
    pClass2 = temppred.argmax()

    temppred[pClass2] = -1
    pClass3 = temppred.argmax()

    f = open('nnet/nn'+randpart+'.csv',"w+")

    #save to temp file
    f.write(drugs[pClass1]+','+str(predicted_prob[0][pClass1])+','+str(pClass1)+','+drugs[pClass2]+','+str(predicted_prob[0][pClass2])+','+str(pClass2)+','+drugs[pClass3]+','+str(predicted_prob[0][pClass3])+','+str(pClass3)+',\r\n')

    f.close()


#~Print outout~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print(drugs[predicted_drug])
print(predicted_prob[0][predicted_drug])

#~End~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
