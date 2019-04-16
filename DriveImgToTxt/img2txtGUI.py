from __future__ import print_function
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
import os
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload
import ntpath
import datetime
import io
import shutil

window = tk.Tk()
inputFiles = []
exportList = []
exportListOfNames = []
destinationFolder = ""
driveFileId = ""



# function to close the window
def quit():
    window.destroy()

# fuction to browse filesystem for pdfs and picture files
def browseFiles():
    inputFolderPath = filedialog.askdirectory(title = "Select Folder")
    
    enteredFilesEntry.insert(0, inputFolderPath)
    print(inputFolderPath)
    for filename in os.listdir(inputFolderPath):
        inputFiles.append(inputFolderPath+"/"+filename)
        print("Adding: ", filename)
    print("Files Found: ", inputFiles)
    

def browseDestination():
    destinationSelected =  filedialog.askdirectory(title = "Select Folder")
    destinationFolderEntry.insert(0, destinationSelected)
    global destinationFolder
    destinationFolder = destinationSelected
    

# process the images by first uploading them to google drive
def processFiles():

    # set up google drive api usage
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    


    # create a folder for the images to uploaded to
    file_metadata = {
        'name': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata, fields='id').execute()
    print ('Folder ID: ', file.get('id'))
    driveFileId = file.get('id')


    # upload the files to that folder
    
    
    for pic in inputFiles:
        
        file_metadata = {
            'name': ntpath.basename(pic),
            'parents': [driveFileId],
            'mimeType': 'application/vnd.google-apps.document'
        }

        media = MediaFileUpload(pic,
                            mimetype='image/jpeg',
                            resumable=True)
        file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        exportList.append(file.get('id'))
        exportListOfNames.append(ntpath.basename(pic))

    print(exportList)
    





def exportFiles():

    # set up google drive api usage
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    
    print("DESTINATION FOLDER: ", destinationFolder)
    for export, exportName in zip(exportList, exportListOfNames):
        # Now download the files(export as plaintext)
        print ('Fetching File ID: ', exportName, ".txt...")
        
        file_id = export
        request = service.files().export_media(fileId=file_id, mimeType='text/plain')
        
        print(export)
        print("Placing Files: ",os.getcwd())
        fh = io.FileIO((destinationFolder+"/"+exportName+".txt"), 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%.", int(status.progress() * 100))

        



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

    # Process Button
    processBtn = tk.Button(window, text ="Process", command = processFiles )
    processBtn.pack()
    processBtn.place(height=30, width=70, rely=.85, relx=.67)

    # Export to text Button
    processBtn = tk.Button(window, text ="Export", command = exportFiles )
    processBtn.pack()
    processBtn.place(height=30, width=70, rely=.85, relx=.47)

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
