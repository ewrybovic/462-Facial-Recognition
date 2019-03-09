from tkinter import *
import cv2
import PIL
from PIL import Image, ImageTk
import FileTransferClient
import numpy as np
from time import sleep
from threading import Thread

IMAGE_PADDING_X = 10
IMAGE_PADDING_Y_UP = 50
IMAGE_PADDING_Y_DOWN = 25

IMAGE_SIZE = 96

# Network Ports  FCHANGE
TCP_IP = "localhost"
TCP_SERVER_PORT = 5000
TCP_FTP_PORT    = 3000

# The boolean to dictate if the GUI takes an image
isCaptureImage = False
didTakeImage = False
isConnected = False
Shutdown = False
sendImageThread = FileTransferClient.FileTransferClient(TCP_IP, TCP_SERVER_PORT, 1024, "savedImage.jpg")

# Create a thread to send the image
def thread_image_function():

	global isConnected
	global Shutdown
	global sendImageThread
    
	while not isConnected and not Shutdown:	
		isConnected = sendImageThread.makeConnection()
		if isConnected == False:
			sleep(0.5)
		print("Trying to reconnect")
	print("Broke out of the while loop")

# variables for writing images
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCorner = (10, 700)
fontScale = 1
fontColor = (255, 255, 255)
lineType = 2

# Create the face cascade variable for detecting faces
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Set the width and the height of the frame
width, height = 1280, 720
width, height = 640, 480 #delete

# Create the video capture and set the widht and height
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Make the root of Tkinter
root = Tk()

# Closing function, also closes FCHANGE
def close():
    global Shutdown
    Shutdown = True
    sendImageThread.closeSocket()
    root.quit()

# binf the escape key to quit the GUI
root.bind('<Escape>', lambda e: close())

# Creates the image widget in the form of a label lol
imageBox = Label(root)
imageBox.pack()

# When the button is pressed capture the image
def captureImage():
    global isCaptureImage
    isCaptureImage = True

# Button to capture the image
captureButton = Button(root, text="Capture", command=captureImage)
captureButton.pack(side=RIGHT, padx=5, pady=5)

# Create the menubar
menubar = Menu(root)

# Create the submenu
fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label = "Capture Image", command = captureImage)
fileMenu.add_command(label = "Check Connection to server")
fileMenu.add_command(label = "Quit", command = close)

# Add submenu to the menu bar
menubar.add_cascade(label = "File", menu = fileMenu)

# Add the emnubar to the root
root.config(menu = menubar)

# handle exit through GUI X FCHANGE
root.protocol("WM_DELETE_WINDOW", close)

# Returns the image of only the face
def getROI(frame, x1, y1, x2, y2):
    height, width, _ = frame.shape
    return frame[max(0, y1):min(height, y2), max(0, x1):min(width, x2)]

# function to send the new user's id to the server
# runs after the user types in their name
def send_name():
    # get the name from the entry box the user typed in
    user_name = name_entry.get()
    sendImageThread.id = user_name
    
    # send this name/id to the server
    sendImageThread.send_name_to_server(user_name)
    
    entry_box.destroy()

# bring up a text box to have the new user enter their name
def enter_user_name():
    # create a new window where the name will be entered
    global entry_box
    entry_box = Toplevel(root)
    entry_box.wm_title("New User")
    
    Label(entry_box, text = "Enter your name").grid(row = 0)
    global name_entry
    name_entry = Entry(entry_box)
    name_entry.grid(row = 0, column = 1)
    
    # id will be changed later, when the user enters their name
    sendImageThread.id = ""
    
    # create a button labeled enter; when pressed the window will close, and send the name to the server
    Button(entry_box, text = "Enter", command = send_name).grid(row = 3, column = 1, sticky = W, pady = 3)
  

def show_frame():
    global isCaptureImage, isConnected, didTakeImage, sendImageThread, face_cascade, fontColor
    imageText = ""
    foundFace = False
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Detect if a face is in the frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    # Move the frame to a new variable to remove the blue border
    displayFrame = cv2.copyMakeBorder(frame, 0,0,0,0, cv2.BORDER_REPLICATE)

    # Loop over the faces found and draw a rectangle
    for (x, y, w, h) in faces:
        foundFace = True
        x1 = x - IMAGE_PADDING_X
        y1 = y - IMAGE_PADDING_Y_UP
        x2 = x + w + IMAGE_PADDING_X
        y2 = y + h + IMAGE_PADDING_Y_DOWN
        cv2.rectangle(displayFrame, (x1, y1), (x2, y2), (255, 0, 0), lineType)

    # Take a picture if the button has been pressed
    if isCaptureImage and isConnected:
        print("Taking picture")
        imageText = "Status: taking picture"

        # Check if there was a face in the frame before saving image
        if foundFace:
            faceFrame = getROI(frame, x1, y1, x2, y2)
            faceFrame = cv2.resize(faceFrame, (IMAGE_SIZE, IMAGE_SIZE))
            cv2.imwrite("savedImage.jpg", faceFrame)
        else:
            cv2.imwrite("savedImage.jpg", frame)
        isCaptureImage = False
        didTakeImage = True

        # Start the thread and send the image
        if not sendImageThread.isDone:
            sendImageThread = FileTransferClient.FileTransferClient(TCP_IP, TCP_SERVER_PORT, 1024, "savedImage.jpg")
            sendImageThread.openSocket()
            sendImageThread.start()
        else:
            sendImageThread.start()

    # If there is no connection to the server notify the user
    elif not isConnected:
        if isCaptureImage:
            imageText = "Status: Cannot take picture unless connected to server"
        else:
            imageText = "Status: No Connection to server"
    else:
        if sendImageThread.isAlive():
            imageText = "Status: Sending image to server"
        else:
            if sendImageThread.id != "None" and sendImageThread.id != "":
                imageText = "Status: Your name is " + sendImageThread.id
            elif sendImageThread.id == "None":
                # id is none, have user enter their name, save in id
                imageText = "Status: New user"
                enter_user_name()
            elif didTakeImage:
                imageText = "Status: Image sent to server"
            else:
                imageText = "Status: idle" 

    # Change the color of the image for Tkinter
    displayFrame = cv2.cvtColor(displayFrame, cv2.COLOR_BGR2RGBA)

    # Write the status to the image
    cv2.putText(displayFrame, imageText, bottomLeftCorner, font, fontScale, fontColor, lineType)
    img = Image.fromarray(displayFrame)

    # Creates a Tkinter compatible image
    imgtk = ImageTk.PhotoImage(image = img)
    imageBox.imgtk = imgtk
    imageBox.configure(image = imgtk)
    
    # Calls this function after a given interval
    imageBox.after(int(1000/60), show_frame)

# Start thread for connecting thread function
thread = Thread(target = thread_image_function)
thread.start()

# Call show frame to start the loop
show_frame()
root.mainloop()
