import tkinter as tk
from PIL import Image, ImageTk
import os


settingsPath = list(os.path.dirname(os.path.abspath(__file__))) #This turns all the backslashes in the path into foreward slashes
for x in range(len(settingsPath)):
    if settingsPath[x] == "\\":
        settingsPath[x] = "/"
settingsPath = ''.join(settingsPath) + "/Setup.txt"
setupFile = open(settingsPath, "r")
s = setupFile.readlines()

imgNum = int(s[3].rstrip()) #The rstrip removes newlines that are attached to everything
imagePath = s[7].rstrip()
prefix = s[11].rstrip()
suffix = s[15].rstrip()
fileExtension = s[19].rstrip()
horizontalRes = int(s[23].rstrip())
verticalRes = int(s[27].rstrip())
renameTo = s[31].rstrip()



imagePath = list(imagePath) #This bit ensures that the file path will work whether or not there is a / at the end of the path, so "C:/ExamplePath/Photos/"
if imagePath[len(imagePath)-1] == "/":
    imagePath.pop()
for x in range(len(imagePath)): #This corrects for backslashes used in the image folder path
    if imagePath[x] == "\\":
        imagePath[x] = "/"
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

print(fullPath)
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