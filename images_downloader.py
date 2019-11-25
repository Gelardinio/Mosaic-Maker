# Import modules
import functions
from google_images_download import google_images_download
import tkinter as tk
import os, sys
import cv2
from PIL import Image, ImageTk
Image.MAX_IMAGE_PIXELS = None
import numpy as np
import shutil

#Directory where files are located 
os.chdir('E:/ISU_FINAL') #Edit based on where files will be placed

KEYWORDS = []

#Image density specification
density = 2

#Declare directories
Keyword1_Directory = "Images/Keyword1"
Keyword2_Directory = "Images/Keyword2"
Output_Directory  = "ImageOutput"
Main_Image_Output = "MainOutput"


#Create folders 
functions.create_folders("Images")
functions.create_folders("Images/Keyword2")
functions.create_folders("Images/Keyword1")
functions.create_folders("ImageOutput")
functions.create_folders("MainOutput")

photoTaken = False

#Run main menu function
functions.makeMain()

print(KEYWORDS)

count = 0

#Create new window
master = tk.Tk()

imageLoc = 'reference.PNG'

canvas = tk.Canvas(master, width=600, height=200, highlightthickness=0)

canvas.pack()

master.minsize(600, 20)
master.title("Mosaic Maker")

img = ImageTk.PhotoImage(Image.open(imageLoc).resize((600, 600), Image.ANTIALIAS))
canvas.background = img  # Keep a reference in case this code is put in a function.
bg = canvas.create_image(0, 0, anchor=tk.NW, image=img)

canvas.create_text(280,30, text="Processing... Your image will show up shortly", font=("Courier", 15))
canvas.create_text(220,60, text="This window will close in 5 seconds", font=("Courier", 15))

master.after(5000, master.destroy)

master.mainloop()

#Declare image download arguments
arguments = {
    "keywords":KEYWORDS[0],
    "limit":100,
    "output_directory":'Images',
    "image_directory":'Keyword1',
    "type":'photo',
    "format":'jpg',
    "print_urls": False,
}

while count < 1: 
    functions.download_images(arguments)
    for file in os.listdir(Keyword1_Directory):
        img = Image.open(os.path.join(Keyword1_Directory, file))
        count = count + 1

#Declare image download arguments
if photoTaken == False:
    arguments = {
        "keywords":KEYWORDS[1],
        "limit":1,
        "output_directory":'Images',
        "image_directory":'Keyword2',
        "print_urls": False,
        "type":"photo",
        "format":'jpg',
    }

    count = 0

    #Check that images are downloaded
    while count < 1: 
        functions.download_images(arguments)
        for file in os.listdir(Keyword2_Directory):
            img = Image.open(os.path.join(Keyword2_Directory, file))
            count = count + 1

#Resize images
for file in os.listdir(Keyword1_Directory):
    try:
        img = Image.open(os.path.join(Keyword1_Directory, file))
        img = img.resize((50,50))
        os.path.join(Output_Directory, file)
        img.save(os.path.join(Output_Directory, file))  
    except:
        print("Error")


count = 0
arr_count = 0
averageR = 0
averageG = 0
averageB = 0

arr_R = []
arr_G = []
arr_B = []

#Scan and store input images RGB values
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

    arr_count = arr_count + 1

    count = 0
    averageR = 0
    averageG = 0
    averageB = 0

count = 0
averageR = 0
averageG = 0
averageB = 0

#Scan output image RGV values based in chunks
for file in os.listdir(Keyword2_Directory):
    img = Image.open(os.path.join(Keyword2_Directory, file))
    img = img.convert('RGB')
    width, height = img.size
    width = density * round(width/density) 
    height = density * round(height/density) 
    print(width, height)
    img = img.resize((width, height))
    rgbr = [[0 for x in range((int(width/density)))] for y in range(int((height/density)))]
    rgbb = [[0 for x in range((int(width/density)))] for y in range(int((height/density)))]
    rgbg = [[0 for x in range((int(width/density)))] for y in range(int((height/density)))]
    for y in range(0, height):
        for x in range(0, width):

            RGB = img.getpixel((x,y))
            r, g, b = RGB
            count = count + 1

            averageR += r
            averageG += g
            averageB += b

            if x % density == 0:
                rgbr[int(y / density)][int(x / density)] = (averageR / density)
                rgbg[int(y / density)][int(x / density)] = (averageG / density)
                rgbb[int(y / density)][int(x / density)] = (averageB / density)
                averageR = 0
                averageG = 0
                averageB = 0


images = []

#Add resized image to images array
for file in os.listdir(Output_Directory):
    img2 = Image.open(os.path.join(Output_Directory, file))
    images.append(img2)

#Create mosaic
for file in os.listdir(Keyword2_Directory):
    img = Image.open(os.path.join(Keyword2_Directory, file))
    img = img.convert('RGB')
    width, height = img.size
    width = density * round(width/density) 
    height = density * round(height/density) 
    total_diff = []
    x_offset = 0
    y_offset = 0

    #Create a new image of specified dimensions
    img2 = Image.new('RGB', (int(width * (50 / density)), int(height * (50 / density))))

    #Append images based on RGB value comparissons
    for y in range(0, (int(height / density))):  
        x_offset = 0
        for x in range(0, (int(width / density))): 
            index_total = 0
            difference_total = (abs((rgbr[y][x] - arr_R[0])) + abs((rgbg[y][x] - arr_G[0])) + abs((rgbb[y][x] - arr_B[0])))
            for i in range(0, len(arr_R)):
                if (abs((rgbr[y][x] - arr_R[i])) + abs((rgbg[y][x] - arr_G[i])) + abs((rgbb[y][x] - arr_B[i]))) < difference_total: 
                    difference_total = (abs((rgbr[y][x] - arr_R[i])) + abs((rgbg[y][x] - arr_G[i])) + abs((rgbb[y][x] - arr_B[i])))
                    index_total = i

            img2.paste(images[index_total], (x_offset, y_offset))
            x_offset = x_offset + 50
        y_offset = y_offset + 50 
    img2.save('Output.jpg')

#Show user the processed final image
master = tk.Tk()
img = Image.open("Output.jpg")
img = img.resize((800,700))
img.save("Outputref.jpg")
master.title("Output")
img2 = ImageTk.PhotoImage(Image.open("Outputref.jpg"))
panel = tk.Label(master, image = img2)
panel.pack(side = "bottom", fill = "both", expand = "yes")
master.mainloop()

shutil.rmtree(Keyword2_Directory)

#Main loop
if __name__ == "__main__":
    main()
