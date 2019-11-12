import tkinter as tk
import os, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import numpy as np

os.chdir('C:\ISU')

if False: 
    master = tk.Tk()
    master.title("ISU")
    tk.Label(master, text="First Keyword").grid(row=0)
    tk.Label(master, text="Second Keyword").grid(row=1)

    e1 = tk.Entry(master)
    e2 = tk.Entry(master)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    master.mainloop()
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


count = 0
arr_count = 0
averageR = 0
averageG = 0
averageB = 0

arr_R = []
arr_G = []
arr_B = []

for file in os.listdir(Output_Directory):
    
    img = Image.open(os.path.join(Output_Directory, file))
    img = img.convert('RGB')
    for y in range(0, 50):
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

    arr_R.append(averageR)
    arr_G.append(averageG)
    arr_B.append(averageB)

    print(str(int(arr_R[arr_count])) + ',' + str(int(arr_G[arr_count])) + ',' + str(int(arr_B[arr_count])))

    arr_count = arr_count + 1

    count = 0
    averageR = 0
    averageG = 0
    averageB = 0

count = 0
averageR = 0
averageG = 0
averageB = 0

f = open("values.txt", "w")

for file in os.listdir(Keyword2_Directory):
    img = Image.open(os.path.join(Keyword2_Directory, file))
    img = img.convert('RGB')
    width, height = img.size
    width = 3 * round(width/3) 
    height = 3 * round(height/3) 
    print(width, height)
    img = img.resize((width, height))
    rgbr = [[0 for x in range((int(width/3)))] for y in range(int((height/3)))]
    rgbb = [[0 for x in range((int(width/3)))] for y in range(int((height/3)))]
    rgbg = [[0 for x in range((int(width/3)))] for y in range(int((height/3)))]
    for y in range(0, height):
        for x in range(0, width):

            RGB = img.getpixel((x,y))
            r, g, b = RGB
            count = count + 1

            averageR += r
            averageG += g
            averageB += b

            if x % 3 == 0:
                rgbr[int(y / 3)][int(x / 3)] = (averageR / 3)
                rgbg[int(y / 3)][int(x / 3)] = (averageG / 3)
                rgbb[int(y / 3)][int(x / 3)] = (averageB / 3)
                averageR = 0
                averageG = 0
                averageB = 0

    f.write(str(rgbr[0][0]) + " " + str(rgbg[0][0]) + " " + str(rgbb[0][0]))    

f.close()
images = []

for file in os.listdir(Output_Directory):
    img2 = Image.open(os.path.join(Output_Directory, file))
    images.append(img2)

for file in os.listdir(Keyword2_Directory):
    img = Image.open(os.path.join(Keyword2_Directory, file))
    img = img.convert('RGB')
    width, height = img.size
    width = 3 * round(width/3) 
    height = 3 * round(height/3) 
    total_diff = []
    x_offset = 0
    y_offset = 0

    img2 = Image.new('RGB', ((width * 16), (height * 16)))

    for y in range(0, (int(height / 3))):  
        x_offset = 0
        for x in range(0, (int(width / 3))): 
            index_total = 0
            difference_total = (abs((rgbr[y][x] - arr_R[0])) + abs((rgbg[y][x] - arr_G[0])) + abs((rgbb[y][x] - arr_B[0])))
            for i in range(0, len(arr_R)):
                if (abs((rgbr[y][x] - arr_R[i])) + abs((rgbg[y][x] - arr_G[i])) + abs((rgbb[y][x] - arr_B[i]))) < difference_total: 
                    difference_total = (abs((rgbr[y][x] - arr_R[i])) + abs((rgbg[y][x] - arr_G[i])) + abs((rgbb[y][x] - arr_B[i])))
                    index_total = i

            img2.paste(images[index_total], (x_offset, y_offset))
            x_offset = x_offset + 50
                
        print(str(int(difference_total)))
        y_offset = y_offset + 50 
    img2.save('firsttest.jpg')
        


#os.remove(Keyword1_Directory)
#os.remove(Keyword2_Directory)
#os.remove(Output_Directory)
#os.remove(Main_Image_Output)


print("done")