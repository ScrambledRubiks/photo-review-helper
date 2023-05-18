import tkinter as tk
from PIL import Image, ImageTk
import os

#Edit the variables below for your photos:
imgNum = 1 #Number the images start at, mine started at 1
imagePath = "C:/ExamplePath/Photos" #Full path of the folder the images are in, folders and file names cannot have spaces, AND MAKE SURE YOU ARE USING FOREWARD SLASHES!!
prefix = "photo" #Prefix to every image number(as in the "photo" in photo1), leave blank if there is none
suffix = "" #Suffix to every image (as in the "photo" in 1photo), leave blank if there is none
fileExtension = "jpg" #The file extension of all of your photos
horizontalRes = 1600 #Horizontal resolution for the photos' display, make sure this is a whole number!
verticalRes = 900 #Vertical resolution for the photos' display, make sure this is a whole number!
renameTo = "_GOOD" #The suffix that pressing m will add to the file name
#Once these are done you're all set!

imagePath = list(imagePath) #This bit ensures that the file path will work whether or not there is a / at the end of the path, so "C:/ExamplePath/Photos/"
if imagePath[len(imagePath)-1] == "/":
    imagePath.pop()
imagePath = ''.join(imagePath)


fullPath = "{}/{}{}{}.{}".format(imagePath, prefix,  str(imgNum), suffix, fileExtension) #Creates the full path for each photo

win = tk.Tk()
win.title("Photo Review Helper")
win.geometry("1600x900")
path = list(os.path.dirname(os.path.abspath(__file__))) #This stuff just gets the filepath for the icon
for x in range(len(path)):
    if path[x] == "\\":
        path[x] = "/"
path = ''.join(path)
icon = tk.PhotoImage(file=f"{path}/ScrambledRubiks-Emblem.png")
win.iconphoto(True,icon)

image1 = Image.open(fullPath) #These prepare the images for proper display
image1 = image1.resize((int(2544/2), int(1696/2)), Image.LANCZOS) 
ph = ImageTk.PhotoImage(image1)

label1 = tk.Label(image=ph)
label1.image = image1

def key_pressed(event): #This is everything that happens when you hit a key
    global imgNum
    global image1
    global fullPath
    global label1
    global ph
    global imagePath
    global prefix
    global suffix
    global fileExtension
    global horizontalRes
    global verticalRes
    if event.char == ",": #Handling going down the photo list
        imgNum -= 1
        fullPath = "{}/{}{}{}.{}".format(imagePath, prefix,  str(imgNum), suffix, fileExtension)
        image1 = Image.open(fullPath)
        image1 = image1.resize((horizontalRes, verticalRes), Image.LANCZOS)
        ph = ImageTk.PhotoImage(image1)
            
        label1.configure(image=ph)
        label1.image = ph
    elif event.char == ".": #Handling going up the photo list
        imgNum += 1 
        print(imgNum)
        fullPath = "{}/{}{}{}.{}".format(imagePath, prefix,  str(imgNum), suffix, fileExtension)
        image1 = Image.open(fullPath)
        image1 = image1.resize((int(2544/2), int(1696/2)), Image.LANCZOS)
        ph = ImageTk.PhotoImage(image1)
            
        label1.configure(image=ph)
        label1.image = ph

    elif event.char == "m": #Handling marking the photos
        pathNoFileExtension = "{}/{}{}{}".format(imagePath, prefix,  str(imgNum), suffix) #This is to keep the file extension from being renamed like "photo1.jpg_GOOD"
        name = pathNoFileExtension + renameTo + "." + fileExtension
        os.rename(fullPath, name)


#Position image
label1.place(x=0, y=0)
win.bind("<Key>",key_pressed)
win.mainloop()