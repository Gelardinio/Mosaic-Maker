#Gerald Liu ISU
#November 24, 2019
#Program that constructs mosaics give 2 keywords

#Import modules
import images_downloader
from google_images_download import google_images_download
import tkinter as tk
import os, sys
import cv2
from PIL import Image, ImageTk
Image.MAX_IMAGE_PIXELS = None
import numpy as np
import shutil


#Downloads images off google images based on a list of arguments
def download_images(arguments):
  response = google_images_download.googleimagesdownload()
  absolute_image_paths = response.download(arguments)

#Creates folders for image placement
def create_folders(folder_name):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    except OSError:
        print ('Error: Creating directory. ' +  folder_name)

#Converts RGB values into hex format
def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb  

#Code for the take photo button to take photos
def runPrg(): 
    try:
        package=e1.get()
        images_downloader.KEYWORDS.append(package)
        package=e2.get()
        images_downloader.KEYWORDS.append(package)
    except:
        global photoTaken
        photoTaken = True
    master.destroy()

#Closes program window
def close_window(): 
    master.destroy()
    sys.exit()

#Takes picture for the user
def take_picture():
    cam = cv2.VideoCapture(0)
    retval, frame = cam.read()
    if retval != True:
        raise ValueError("Can't read frame")

    cv2.imwrite('Images/Keyword2/userphoto.png', frame)
    #cv2.imshow("img1", frame)
    cv2.waitKey()
    e2.destroy()

#Main Interface
def makeMain():
    global master
    master = tk.Tk()
    master.title("Mosaic Maker")

    #Creates window
    master.minsize(500, 200)
   
    imageLoc = 'reference.PNG'

    #Make new window
    canvas = tk.Canvas(master, width=500, height=200, highlightthickness=0)
    
    canvas.pack()

    #Positions background image
    img = ImageTk.PhotoImage(Image.open(imageLoc).resize((500, 200), Image.ANTIALIAS))
    canvas.background = img  
    bg = canvas.create_image(0, 0, anchor=tk.NW, image=img)

    #Different button placements
    canvas.create_text(120,20, text="First Keyword", font=("Courier", 20))
    canvas.create_text(120,55, text="Second Keyword", font=("Courier", 20))

    quitButton = tk.Button(master, text="Quit",font=("Courier", 20), command = close_window)
    quitButton.configure(background=_from_rgb((160, 163, 161))) 
    quitButton.place(x=10, y= 140)

    runButton = tk.Button(master, text="Run",font=("Courier", 20), command = runPrg)
    runButton.configure(background=_from_rgb((4, 135, 6)))
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