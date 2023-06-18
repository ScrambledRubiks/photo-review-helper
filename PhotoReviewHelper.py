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

imagePath = s[3].rstrip()
fileExtension = s[7].rstrip()
horizontalRes = int(s[11].rstrip())
verticalRes = int(s[15].rstrip())
renameTo = s[18].rstrip()





imagePath = list(imagePath) #This bit ensures that the file path will work whether or not there is a / at the end of the path, so "C:/ExamplePath/Photos/"
if imagePath[len(imagePath)-1] == "/":
    imagePath.pop()
for x in range(len(imagePath)): #This corrects for backslashes used in the image folder path
    if imagePath[x] == "\\":
        imagePath[x] = "/"
imagePath = ''.join(imagePath)


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

file_path = []

def get_image_files(image_folder): #ChatGPT helped with this stuff
    global file_path
    image_files = []
    for file_name in os.listdir(image_folder):
        if file_name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            file_path = os.path.join(image_folder, file_name)
            image_files.append(file_path)
    image_files.sort(key=os.path.getmtime)  # Sort files by modification time
    return image_files

image_folder = imagePath
image_files = get_image_files(image_folder)
current_index = 0

image1 = Image.open(image_files[0]) #These prepare the images for proper display
image1 = image1.resize((horizontalRes, verticalRes), Image.LANCZOS) 
ph = ImageTk.PhotoImage(image1)

label1 = tk.Label(image=ph)
label1.image = image1




def show_image(image_path):
    image = Image.open(image_path)
    image = image.resize((horizontalRes, verticalRes), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    label1.configure(image=photo)
    label1.image = photo
    label1.place(x=0, y=0) 


def key_pressed(event):
    global current_index
    global file_path
    global renameTo
    
    if event.char == ",":
        current_index -= 1
    elif event.char == ".":
        current_index += 1
    elif event.char == "m": #Handling marking the photos
        current_index = max(0, min(current_index, len(image_files) - 1))
        
        file_path = image_files[current_index]  # Update the file_path with the current image
        
        path2 = list(os.path.splitext(file_path)[0])
        for x in range(len(path2)):
            if path2[x] == "\\":
                path2[x] = "/"
        path2 = ''.join(path2)
        
        name = path2 + renameTo + "." + fileExtension
        os.rename(file_path, name)
    
    current_index = max(0, min(current_index, len(image_files) - 1))
    show_image(image_files[current_index])
    print(current_index)



#Position image
label1.place(x=0, y=0)
win.bind("<Key>",key_pressed)
win.mainloop()