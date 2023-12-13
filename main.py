import os
from io import BytesIO

from pack import pack
from bmp import bmp
from axybmp import axybmp

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Listbox
from tkinter import Label
from tkinter import Button
from tkinter import Frame

from PIL import Image, ImageTk


def main():
    root.mainloop()


def openPack():

    # Opening a pack file

    global bmpPack
    global fileName
    
    # Importing the file data
    file = openFile()

    # If the operation was cancelled, set the save button to be disabled
    if file is None:
        saveBtn.configure(state="disabled")
        return

    # Reset the pack file object
    bmpPack = None

    try:
        fileName = os.path.basename(file.name) # Saving the file name for the file save dialog
        bmpPack = pack(file, os.stat(file.name).st_size) # Constructing the pack file object
        saveBtn.configure(state="active") # Save button is enabled
    except:
        messagebox.showerror("Error", "Invalid pack file")
        return

    # Updating the BMP list, image holder and the list box
    updateLists()


def savePack():

    # Saving a pack file

    global fileName

    try:
        data = bmpPack.constructFile() # Building the pack file
    except:
        messagebox.showerror("Error", "Edited file is corrupted")
        return
    
    newFile = saveFile(data, os.path.splitext(fileName)[0], os.path.splitext(fileName)[1], False) # Opening a save file dialog with the file name and the file type
    if newFile is not None:
        fileName = newFile


def updateLists():

    # Updating the BMP list, image holder and the list box

    global bmpPack

    # Clearing everything before stuff is getting updated
    clearLists()
    clearImageHolder()

    try:
        # Going through all of the entries that is in the pack file
        for x in range(len(bmpPack.entries)):

            # Current AxyBMP
            currEntry = bmpPack.entries[x]

            # Creating a BMP object and converting it to a PhotoImage
            currBmp = BytesIO(bmp(rawDataSize = currEntry.size, width = currEntry.width, height = currEntry.height, data = currEntry.data).file)
            currImage = Image.open(currBmp)
            currImage = ImageTk.PhotoImage(currImage)

            # Adding up the image to the image holder list and the list box
            convertedList.append(currImage)
            bmpList.insert(x, currEntry.name[::-1])
    except:
        messagebox.showerror("Error", "Invalid pack file")
        bmpPack = None
        clearLists()
        clearImageHolder()
        return


def clearLists():

    # Clearing both the list box and the BMP list

    if (bmpList.size() > 0):
        bmpList.delete(0, bmpList.size()-1)

    convertedList.clear()


def clearImageHolder():

    # Clearing the image holder

    img.configure(image=None)
    img.image = None


def selectBmp(event):

    # Selecting an entry from the list box

    # If there is an entry selected, a switch is being set to know wether to set the dimensions label and the replace and export buttons
    if len(bmpList.curselection()) > 0:
        switch = "active"
    else:
        switch = "disabled"

    # If the BMP list is not empty and an entry was selected proceed
    if bmpList.size() > 0 and len(bmpList.curselection()) > 0:

        # Updating the image holder
        currImage = convertedList[bmpList.curselection()[0]]
        img.configure(image=currImage)
        img.image = currImage

        # Image width and height for the dimensions label
        imgWidth = bmpPack.entries[bmpList.curselection()[0]].width
        imgHeight = bmpPack.entries[bmpList.curselection()[0]].height

        # If the image width is too big for the window, its being expanded
        if imgWidth >= 110:
            root.wm_geometry(str(600 + imgWidth) + "x350")
        else:
            root.wm_geometry("600x350")

    # Dimensions label
    if switch == "active":
        txt = "Dimensions: " + str(imgWidth) + "x" + str(imgHeight) 
    else:
        txt = ""

    # Reconfiguring the dimensions label and the buttons
    dimensionsText.configure(text=txt)
    exportBtn.configure(state=switch)
    replaceBtn.configure(state=switch)


def exportBmp():

    # Exporting a BMP

    # If there's nothing selected or a pack wasn't imported, return
    if len(bmpList.curselection()) <= 0  or len(convertedList) <= 0 :
        messagebox.showerror("Error", "No file selected or pack was not imported")
        return

    # Gets the currently selected image from the BMP list
    entryNum = bmpList.curselection()[0]
    currImage = convertedList[entryNum]

    # Converts the data to a BytesIO so it can be saved
    data = BytesIO()
    currImage = ImageTk.getimage(currImage)
    currImage.save(data, format="BMP")

    # Opens up a save dialog
    saveFile(data.getvalue(), bmpPack.entries[entryNum].name[::-1] + ".bmp")


def replaceBmp():

    # Replacing a bmp

    # Getting the currently selected BMP file
    replacedIndex = bmpList.curselection()[0]
    replacedAxyFile = bmpPack.entries[replacedIndex]

    # Opens up a save dialog
    bmpFile = openFile(True)

    # If the dialog was cancelled, return
    if bmpFile is None:
        return

    try:
        # Constructs the file as an AxyBMP
        bmpData = bmp(file = bmpFile)
        rawBmp = axybmp(bmpFile = bmpData, name = replacedAxyFile.name)
    except:
        messagebox.showerror("Error", "Invalid file")
        return

    # Shows a warning message to the user if the dimensions don't match
    if rawBmp.width != replacedAxyFile.width or rawBmp.height != replacedAxyFile.height:
        response = messagebox.askquestion("Info","WARNING:\nThe dimensions of the image that you are trying to import do not match the image that you are trying to replace.\nDo you want to continue?")
        if response == "no":
            return

    # Updating the data and the lists
    replacedAxyFile.width = rawBmp.width
    replacedAxyFile.height = rawBmp.height
    replacedAxyFile.data = rawBmp.data
    replacedAxyFile.totalSize = rawBmp.totalSize
    replacedAxyFile.size = rawBmp.size
    replacedAxyFile.file = rawBmp.constructFile()
    updateLists()
    

def openFile(isBmp = False):

    # Opening a file and returning it's data

    if isBmp:
        fileTypes = ("BMP Files","*.bmp")
    else:
        fileTypes = ("All Files","*.*")

    try:
        file = filedialog.askopenfile(mode="rb", filetypes = [fileTypes])
    except IOError as e:
        messagebox.showerror("Error", e)
        return None

    return file


def saveFile(data, fileName, fileType = "bmp", img = True):

    # Saving a file and returning it's data

    noExtension = False
    if not img:
        try:
            fileType = fileType.split(".")[1]
        except:
            noExtension = True

    if not noExtension:
        file = filedialog.asksaveasfile(initialfile = fileName, defaultextension = "." + fileType, filetypes = [(fileType.upper() + " Files","*." + fileType),("All Files","*.*")], mode = "wb")
    else:
        file = filedialog.asksaveasfile(initialfile = fileName, filetypes = [("All Files","*.*")], mode = "wb")

    if file is None:
        return None

    try:
        file.write(data)
    except IOError as e:
        messagebox.showerror("Error", e)
        return None

    return os.path.basename(file.name)


fileName = ""

bmpPack = None

convertedList = []


# UI stuff

root = tk.Tk()

icon = ImageTk.PhotoImage(file = "icon.ico")

root.title("AxyTool - v0.1")
root.iconphoto(False, icon)
root.geometry("600x350")
root.resizable(False, False)



frm = Frame(root)
frm.grid()
frm.pack(fill=tk.BOTH, expand=True)

img = Label(borderwidth=0)
img.place(x=490, y=160)


bmpList = Listbox(height=15, width=25)
bmpList.place(x=10, y=55)

openBtn = Button(frm, text="Open file", command=openPack, width=10)
openBtn.place(x=10, y=10)

quitBtn = Button(frm, text="Quit", command=root.destroy, width=10)
quitBtn.place(x=250,y=10)

saveBtn = Button(frm, text="Save file", command=savePack, state="disabled", width=10)
saveBtn.place(x=490,y=10)

replaceBtn = Button(frm, text="Replace", command=replaceBmp, state="disabled", width=10)
replaceBtn.place(x=250, y=90)

dimensionsText = Label()
dimensionsText.place(x=250, y=160)



exportBtn = Button(frm, text="Export", command=exportBmp, state="disabled", width=10)
exportBtn.place(x=250, y=290)



bmpList.bind('<<ListboxSelect>>', selectBmp)
main()