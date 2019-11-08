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

def create_folders(folder_name):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    except OSError:
        print ('Error: Creating directory. ' +  folder_name)

KEYWORDS = []

create_folders("Images")
create_folders("ImageOutput")
create_folders("MainOutput")

buffer_word = input("Enter the first keyword: ")
KEYWORDS.append(buffer_word)

buffer_word = input("Enter the second keyword: ")
KEYWORDS.append(buffer_word)

print(KEYWORDS)

arguments = {
    "keywords":KEYWORDS[0],
    "limit":1,
    "output_directory":'Images',
    "image_directory":'Keyword1',
    "type":'photo',
    "format":'jpg',
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
    "format":'jpg',
}

download_images(arguments)

for file in os.listdir(Keyword1_Directory):
    img = Image.open(os.path.join(Keyword1_Directory, file))
    img = img.resize((50,50))
    os.path.join(Output_Directory, file)
    img.save(os.path.join(Output_Directory, file))  

def rgb_scan(directory, multiplierx, multipliery):
    count = 0
    averageR = 0
    averageG = 0
    averageB = 0

    for file in os.listdir(directory):
        img = Image.open(os.path.join(directory, file))
        img = img.convert('RGB')
        for y in range(0, multipliery):
            for x in range(0, multiplierx):
        
                RGB = img.getpixel((x,y))
                r, g, b = RGB
                count = count + 1

                averageR += r
                averageG += g
                averageB += b

        averageR = averageR / count
        averageG = averageG / count
        averageB = averageB / count

        print(str(int(averageR)) + ',' + str(int(averageG)) + ',' + str(int(averageB)))

        count = 0
        averageR = 0
        averageG = 0
        averageB = 0

rgb_scan(Output_Directory,50,50)

##########################################

count = 0
averageR = 0
averageG = 0
averageB = 0

f = open("values.txt", "w")

for file in os.listdir(Keyword2_Directory):
    img = Image.open(os.path.join(Keyword2_Directory, file))
    img = img.convert('RGB')
    width, height = img.size
    width = 5 * round(width/5) 
    height = 5 * round(height/5) 
    print(width, height)
    img = img.resize((width, height))
    rgbr = [[0 for x in range((int(width/5)))] for y in range(int((height/5)))]
    rgbb = [[0 for x in range((int(width/5)))] for y in range(int((height/5)))]
    rgbg = [[0 for x in range((int(width/5)))] for y in range(int((height/5)))]
    for y in range(0, height):
        for x in range(0, width):

            RGB = img.getpixel((x,y))
            r, g, b = RGB
            count = count + 1

            averageR += r
            averageG += g
            averageB += b

            if x % 5 == 0:
                rgbr[int(y / 5)][int(x / 5)] = (averageR / 5)
                rgbg[int(y / 5)][int(x / 5)] = (averageG / 5)
                rgbb[int(y / 5)][int(x / 5)] = (averageB / 5)
                averageR = 0
                averageG = 0
                averageB = 0

    f.write(str(rgbr[0][0]) + " " + str(rgbg[0][0]) + " " + str(rgbb[0][0]))    

f.close()



##########################################

if False:

    for file in os.listdir(Keyword2_Directory):
        img = Image.open(os.path.join(Keyword2_Directory, file))
        width, height = img.size
        img = img.resize((width * 10, height * 10))
        os.path.join(Main_Image_Output, file)
        img.save(os.path.join(Main_Image_Output, file))  
        os.remove(os.path.join(Keyword2_Directory, file))

#os.remove(Keyword1_Directory)
#os.remove(Keyword2_Directory)
#os.remove(Output_Directory)
#os.remove(Main_Image_Output)

print("done")