from tkinter import messagebox
from tkinter import filedialog
from PIL import Image
import pytesseract as pyt
from pdf2image import convert_from_path
from tkinter import *
import shutil
import os
import csv
from dateutil.parser import parse
from datetime import datetime

pyt.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

homedir = os.getcwd()
receiptsdir = os.path.join(homedir,"receipts")
stores = list()
with open("stores.csv", "r") as storesCSV:
    csv_reader = csv.reader(storesCSV)
    for i in csv_reader:
        stores.append(i)

def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy = fuzzy)
        return True
    except ValueError:
        return False

def selectFile():
    global filepath
    filepath = filedialog.askopenfilenames()
    filenumLabel.config(text="you have selected " + str(len(filepath)) + " file(s)")
    
def submitFile():
    for i in filepath:
        datekey = ""
        namekey = ""
        print(i)
        image = convert_from_path(i)
        namekey = currentstoresItems.get(currentstoresItems.curselection())[0]
        for line in (pyt.image_to_string((image[0]))).split():   
            if "/" in line:
                if is_date(line) == True:
                    try:
                        datekey = datetime.strptime(line, "%m/%d/%y")
                        datekey = datekey.strftime("%B %d, %Y")
                    except ValueError:
                        pass
                    try:
                        datekey = datetime.strptime(line, "%m/%d/%Y")
                        datekey = datekey.strftime("%B %d, %Y")
                    except ValueError:
                        pass
            elif "-" in line:
                if is_date(line) == True:
                    try:
                        datekey = datetime.strptime(line, "%m-%d-%y")
                        datekey = datekey.strftime("%B %d, %Y")
                    except ValueError:
                        pass
                    try:
                        datekey = datetime.strptime(line, "%m-%d-%Y")
                        datekey = datekey.strftime("%B %d, %Y")
                    except ValueError:
                        pass
            else:
                pass

        print("This is the datekey: " + datekey)
        if datekey != "":
            rename = namekey + " " + datekey + ".pdf"
            rename = os.path.join(os.path.dirname(i),rename)
            os.rename(i,rename)
        else:
            rename = i
            print("Could not locate date")
        shutil.move(rename,os.path.join(receiptsdir,namekey))
        

    filenumLabel.config(text="")
def addStore():
    if addStoreEntry.get() != "":
        if os.path.exists(addStoreEntry.get()) == True:
            if os.path.isdir(addStoreEntry.get()) == True:
                messagebox.showerror(message="Directory already exists")
        else:
            with open("stores.csv", "a",newline="") as storesCSV:
                csv_writer = csv.writer(storesCSV)
                csv_writer.writerow([addStoreEntry.get()])
                
                if os.path.basename(os.getcwd()) != "receipts":
                    os.chdir("receipts")
                else:
                    pass
            os.mkdir(addStoreEntry.get())
        os.chdir(homedir)
        currentstoresItems.delete(0, END)
        with open("stores.csv", "r") as storesCSV:
            csv_reader = csv.reader(storesCSV)
            for i in csv_reader:
                currentstoresItems.insert(END, i)
        addStoreEntry.delete(0,END)
    else:
        pass


root = Tk()
Title = Label(root,text="Receipt Organizer", font=("Helvetica 20"))
Title.pack(padx=25,pady=5)

selectButton = Button(root,text="Select File",command=selectFile)
selectButton.pack()

filenumLabel = Label(root,text=" ")
filenumLabel.pack()

submitButton = Button(root, text="Submit",command=submitFile)
submitButton.pack()

currentStores = Label(root,text="Current Stores",font="bold")
currentStores.pack(pady=(15,0))


currentstoresItems = Listbox(root,height=10)
currentstoresItems.pack(pady=(0,10))

with open("stores.csv", "r") as storesCSV:
    csv_reader = csv.reader(storesCSV)
    for i in csv_reader:
        currentstoresItems.insert(END, i)


addStoreEntry = Entry(root)
addStoreEntry.pack(pady=(10,5))

addstoreButton = Button(root, text="Add Store", command=addStore)
addstoreButton.pack(pady=(0,10))

root.mainloop()
