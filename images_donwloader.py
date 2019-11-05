import os, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import cv2
import numpy as np

os.chdir('C:\ISU')

Keyword1_Directory = "Images/Keyword1"
Keyword2_Directory = "Images/Keyword2"
Output_Directory  = "ImageOutput"
Main_Image_Output = "MainOutput"

from google_images_download import google_images_download

def download_images(arguments):

  response = google_images_download.googleimagesdownload()
  absolute_image_paths = response.download(arguments)

KEYWORDS = []

try:
    if not os.path.exists("Images"):
        os.makedirs("Images")
except OSError:
    print ('Error: Creating directory. ' +  "Images")

try:
    if not os.path.exists("ImageOutput"):
        os.makedirs("ImageOutput")
except OSError:
    print ('Error: Creating directory. ' +  "ImageOutput")

try:
    if not os.path.exists("MainOutput"):
        os.makedirs("MainOutput")
except OSError:
    print ('Error: Creating directory. ' +  "MainOutput")

buffer_word = input("Enter the first keyword: ")
KEYWORDS.append(buffer_word)

buffer_word = input("Enter the second keyword: ")
KEYWORDS.append(buffer_word)

print(KEYWORDS)

arguments = {
    "keywords":KEYWORDS[0],
    "limit":9,
    "output_directory":'Images',
    "image_directory":'Keyword1',
    "type":'photo',
    "format":'png',
    "print_urls": False,
}

download_images(arguments)

arguments = {
    "keywords":KEYWORDS[1],
    "limit":1,
    "output_directory":'Images',
    "image_directory":'Keyword2',
    "print_urls": False,
    "type":"photo",
}

download_images(arguments)

for file in os.listdir(Keyword1_Directory):
    img = Image.open(os.path.join(Keyword1_Directory, file))
    img = img.resize((50,50))
    os.path.join(Output_Directory, file)
    img.save(os.path.join(Output_Directory, file))  

f = open("output.txt", "w")

averageR = []
averageG = []
averageB = []

count = 0
averageR = 0
averageG = 0
averageB = 0

for file in os.listdir(Output_Directory):
    img = Image.open(os.path.join(Output_Directory, file))
    img = img.convert('RGB')
    for y in range(0, 50):
        row = ""
        for x in range(0, 50):
      
            RGB = img.getpixel((x,y))
            r, g, b = RGB
            count = count + 1

            averageR += r
            averageG += g
            averageB += b

    averageR = averageR / count
    averageG = averageG / count
    averageB = averageB / count

    print(str(averageR) + ',' + str(averageG) + ',' + str(averageB))

    count = 0
    averageR = 0
    averageG = 0
    averageB = 0

f.close()

for file in os.listdir(Keyword2_Directory):
    img = Image.open(os.path.join(Keyword2_Directory, file))
    width, height = img.size
    img = img.resize((width * 10, height * 10))
    os.path.join(Main_Image_Output, file)
    img.save(os.path.join(Main_Image_Output, file))  

print("done")