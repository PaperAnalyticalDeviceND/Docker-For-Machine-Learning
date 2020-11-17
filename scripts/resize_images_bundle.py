from PIL import Image
import os, sys
from PIL import Image, ImageEnhance, ImageStat
import math

# function to return average brightness of an image
# Source: http://stackoverflow.com/questions/3490727/what-are-some-methods-to-analyze-image-brightness-using-python
def brightness(im):
    stat = ImageStat.Stat(im)
    r,g,b = stat.mean
    #return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))   #this is a way of averaging the r g b values to derive "human-visible" brightness
    return math.sqrt(0.577*(r**2) + 0.577*(g**2) + 0.577*(b**2))

#defining the path to check for images
paths = ["msh_tanzania_data/test/", "msh_tanzania_data/training/", "msh_tanzania_data/catagorize/"]

#path for resized pictures
#path2 = "/home/swallen2/Tensorflow_caffenet/TestingImages/ImageResized/"

#defining the resize function to resize images in folder
def resize(path):
    dirs = os.listdir(path)

    #looping over all the pictures in specified folder
    for pic in dirs:
        if os.path.isfile(path+pic):
            try:
                #Load an image from the hard drive
                original = Image.open(path+pic)

                #fix brightness
                bright = brightness(original)

                #massage image
                imgbright = ImageEnhance.Brightness(original)
                original = imgbright.enhance(165.6/bright)

                #Find initial size
                #print ("The size of the Image is: ")
                #print(original.format, original.size, original.mode)

                #Resizing the image to be 227 pixels width (keeping ratio).
                #basewidth = 227
                #wpercent = (basewidth / float(original.size[0]))
                #hsize = int((float(original.size[1]) * float(wpercent)))
                #im2 = original.resize((basewidth, hsize), Image.ANTIALIAS)

                #for square images
                size = (227, 227)
                im2 = original.resize((size), Image.ANTIALIAS)

                #giving ability to generate new image name/folder to save
                f, e = os.path.splitext(path+pic)

                #print f
                im2.save(f + ".png")

                #Check sizing
                #print ("The size of the resized Image is: ")
                #print(im2.format, im2.size, im2.mode)

            except:
                print ("Unable to load image:" + pic)

#call
for path in paths:
    resize(path)
