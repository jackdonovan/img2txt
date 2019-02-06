import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

window = tk.Tk()
inputFiles = []
destinationFolder = ""



# function to close the window
def quit():
    window.destroy()

# fuction to browse filesystem for pdfs and picture files
def browseFiles():
    filenameSelected =  filedialog.askopenfilename(initialdir = "/",title = "Select input file",filetypes = (("jpeg files","*.jpg"),("PDF files","*.pdf")))
    enteredFilesEntry.insert(0,filenameSelected+", ")
    inputFiles.append(filenameSelected)
    print(inputFiles)

def browseDestination():
    destinationSelected =  filedialog.askdirectory(title = "Select Folder")
    destinationFolderEntry.insert(0, destinationSelected)
    destinationFolder = destinationSelected

# Use this fuction to make widgets within the window
def makeWidgets():

    # Title Label
    titleFont = font.Font(family = 'Arial', size=12, weight='bold')
    lblTitle = tk.Label(window, text="Image To Text Converter", font=titleFont)
    lblTitle.pack() 
    lblTitle.place(height=20, width=190, rely=.05, relx=.02)

    # close button
    closeBtn = tk.Button(window, text ="Close", command = quit )
    closeBtn.pack()
    closeBtn.place(height=30, width=70, rely=.85, relx=.82)

    # Browse for file button
    browseButton = tk.Button(window, text = "Browse for\n Input Files", command = browseFiles)
    browseButton.pack()
    browseButton.place(height = 40, width=110, rely = .3, relx = .02)

    # Browse for destination button
    browseDestinationButton = tk.Button(window, text = "Browse \n Destination Folder", command = browseDestination)
    browseDestinationButton.pack()
    browseDestinationButton.place(height = 40, width=110, rely = .5, relx = .02)

    # Label for selected files
    lblSelectedFiles = tk.Label(window, text="Selected Files:")
    lblSelectedFiles.pack() 
    lblSelectedFiles.place(height=20, width=72, rely=.3, relx=.25)

    # Label for Destination folder
    lblSelectedFiles = tk.Label(window, text="Selected Destination Folder:")
    lblSelectedFiles.pack() 
    lblSelectedFiles.place(height=20, width=145, rely=.5, relx=.25)

# initialize all the window properties
window.title("Image To Text")
window.geometry("500x300")

# Make input file text box
enteredFilesEntry = tk.Entry(window)
enteredFilesEntry.pack()
enteredFilesEntry.place(height=20, width = 320, rely = .38, relx=.25)

# Make destination folder text box
destinationFolderEntry = tk.Entry(window)
destinationFolderEntry.pack()
destinationFolderEntry.place(height=20, width = 320, rely = .58, relx=.25)


makeWidgets()
window.mainloop()