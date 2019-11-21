import tkinter as tk
import os, sys
import cv2
from PIL import Image, ImageTk
Image.MAX_IMAGE_PIXELS = None
import numpy as np
import shutil

os.chdir('C:\ISU')

KEYWORDS = []

isRun = False

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

create_folders("Images")
create_folders("ImageOutput")
create_folders("MainOutput")

photoTaken = False

def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb   

def runPrg(): 
    package=e1.get()
    KEYWORDS.append(package)
    try:
        package=e2.get()
        KEYWORDS.append(package)
    except:
        global photoTaken
        photoTaken = True

    master.destroy()

def close_window(): 
    print(isRun)

def take_picture():
    cam = cv2.VideoCapture(0)
    retval, frame = cam.read()
    if retval != True:
        raise ValueError("Can't read frame")

    cv2.imwrite('Images/Keyword2/userphoto.png', frame)
    #cv2.imshow("img1", frame)
    cv2.waitKey()
    e2.destroy()
    
def makeMain():
    global master
    master = tk.Tk()
    master.title("Mosaic Maker")

    master.minsize(500, 200)
   
    imageLoc = 'background.jpeg'

    canvas = tk.Canvas(master, width=500, height=200)
    
    canvas.pack()

    img = ImageTk.PhotoImage(Image.open(imageLoc).resize((500, 200), Image.ANTIALIAS))
    canvas.background = img  # Keep a reference in case this code is put in a function.
    bg = canvas.create_image(0, 0, anchor=tk.NW, image=img)

    canvas.create_text(120,20, text="First Keyword", font=("Courier", 20))
    canvas.create_text(120,55, text="Second Keyword", font=("Courier", 20))

    quitButton = tk.Button(master, text="Quit",font=("Courier", 20), command = close_window)
    quitButton.configure(background= _from_rgb((160, 163, 161))) 
    quitButton.place(x=10, y= 140)

    runButton = tk.Button(master, text="Run",font=("Courier", 20), command = runPrg)
    runButton.configure(background=_from_rgb((101, 145, 87)))
    runButton.place(x=320, y=140)
    runButton.config(width = 10, height = 1)

    vidButton = tk.Button(master, text="Take a picture",font=("Courier", 15), command = take_picture)
    vidButton.configure(background=_from_rgb((245, 158, 66)))
    vidButton.place(x=10, y=90)


    global e1
    e1 = tk.Entry(master,width=20, font=("Courier", 15), background=_from_rgb((48, 189, 240)))
    e1.place(x = 240, y = 9)
    global e2
    e2 = tk.Entry(master,width=20, font=("Courier", 15), background=_from_rgb((48, 189, 240)))
    e2.place(x = 240, y = 42)

    master.mainloop()

makeMain()
print(KEYWORDS)

count = 0

master = tk.Tk()
master.title("Mosaic Maker")

master.configure(background=_from_rgb((105, 162, 176)))

master.minsize(500, 200)

Label1 = tk.Label(master, text="Processing", font=("Courier", 20), background=_from_rgb((105, 162, 176)))
Label1.place(x = 150, y = 30)

master.after(3000, master.destroy())
master.mainloop()


arguments = {
    "keywords":KEYWORDS[0],
    "limit":1,
    "output_directory":'Images',
    "image_directory":'Keyword1',
    "type":'photo',
    "format":'jpg',
    "print_urls": False,
}

while count < 1: 
    download_images(arguments)
    for file in os.listdir(Keyword1_Directory):
        img = Image.open(os.path.join(Keyword1_Directory, file))
        count = count + 1

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

    while count < 1: 
        download_images(arguments)
        for file in os.listdir(Keyword2_Directory):
            img = Image.open(os.path.join(Keyword2_Directory, file))
            count = count + 1


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

master = tk.Tk()
img = Image.open("firsttest.jpg")
img = img.resize((800,700))
img.save("firsttest2.jpg")
master.title("Output")
img2 = ImageTk.PhotoImage(Image.open("firsttest2.jpg"))
panel = tk.Label(master, image = img2)
panel.pack(side = "bottom", fill = "both", expand = "yes")
master.mainloop()

shutil.rmtree(Keyword2_Directory)

#os.remove(Keyword1_Directory)
#os.remove(Keyword2_Directory)
#os.remove(Output_Directory)
#os.remove(Main_Image_Output)


print("done")

