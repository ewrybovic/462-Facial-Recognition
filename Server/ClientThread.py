import socket
import cv2
from threading import Thread
from sys import platform
import os
import sqlite3
from BackgroundCleaner import *

# Import the FacialLandmarks file from parent directory, kinda hacky
import sys
sys.path.append("../")
from Common.FacialLandmarks import FacialLandmarks

BUFFER_SIZE = 1024

class ClientThread(Thread):
    # Constructor for the class
    def __init__(self, ip, port, ftp_port,sock, model, debug):
        Thread.__init__(self)
        self.database_flag = 0
        self.database_name = ""
        self.model = model
        self.ip = ip
        self.port = port
        self.sock = sock
        self.debug = debug
        self.didDisconnect = False
        self.shutdown = False
        self.recompile = False
        self.useBackgroundRemover = False
        self.ftp_port = ftp_port
        self.faceLandmarks = FacialLandmarks(fromClient=False)
        	
        print(ip +": New thread started for "+ ip + ":", str(port))
        
    #fuction used to add user to database or is used to lookup an already existing user
    def database_fuct(self, id_, flag):
        conn = sqlite3.connect('FacRecDatabase.db')
        c = conn.cursor()   
 
        if id_ == "":
            pass
        elif self.database_flag:     
           
            lookup = (id_,)
            for row in c.execute('SELECT * FROM FaceRecInfo ORDER BY name'):
               print (row)
            
            print (c.fetchone())
            
        else:
            name = (id_,)
            c.execute('''INSERT INTO FaceRecInfo VALUES (?, 'Youtube.com')''', name)
            conn.commit()
            for row in c.execute('SELECT * FROM FaceRecInfo ORDER BY name'):
               print (row)
        conn.close()   
	

    # Closes the socket
    def closeSocket(self):
        print("%s: Closing Socket" %self.ip)
        print("%s: Closing Socket!!!" %self.ip)
        self.didDisconnect = True
        self.sock.close()
        self.database_fuct(self.database_name, self.database_flag)
        
    # Read the data that comes from the client
    def readData(self):
        ftpSock = self.getFTPConnection() #FCHANGE
        filename = "%s.jpg" %self.ip
        with open(filename, 'wb') as f:
            print("%s: File opened" %self.ip)
            while True:
                data = ftpSock.recv(BUFFER_SIZE)                
                if not data or data == b'1':
                    f.close()
                    print("%s: Data received, closing file" %self.ip)
                    break
                
                #write data to file
                f.write(data)
        print("%s: Closed Server FTP connection (%s, %s)" %(self.ip, str(self.ip), str(self.ftp_port)))
        ftpSock.close()
    
        try:
            # Get the height and width of the face in the frame
            self.faceLandmarks.get_height_width(filename)
        except Exception as e:
            print("Error: ", e)
        
        # remove image background after image is received but before it moves into the facial recognition model
        if self.useBackgroundRemover:
            # run the clean background function and save the image, then run the find identity function
            file = CleanBackground(cv2.imread(filename), debug=False)
            cv2.imwrite(filename, file)
            self.findIdentity(filename)
        else:
            self.findIdentity(filename)

    # Runs the model to find the identity of the person
    def findIdentity(self, filename):
        print("%s: Finding ID" %self.ip)
        face = cv2.imread(filename)
        if not self.debug:
            # using id_ because id is a built in function
            id_ = self.model.findIdentity(face)
            print("%s: The id of client is " %self.ip, id_)

            if (id_ == None):
                id_ = "None"
            else:
                
                self.database_flag = 1
                self.database_name = id_           			
        else:
            print("%s: Debug mode enabled" %self.ip)
            id_ = "Debug"
        # Send the id back to the client
        self.sock.send(id_.encode())

    def getFTPConnection(self):
        #make a socket and listn, then return the socket
        ftpTransSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ftpTransSock.bind(('', self.ftp_port))
        print("%s: Listening for FTP connection on port: %s" %(self.ip, self.ftp_port))
        while True:
            ftpTransSock.listen()
            ftpConnSock, addr = ftpTransSock.accept()
            break
        print("%s: FTP connection from (%s)" %(self.ip, str(addr)))
        return ftpConnSock
      
    
    # receive the name from the client, and rename the image
    def set_name(self):
        new_name = self.sock.recv(BUFFER_SIZE)
        new_name = str(new_name, 'utf-8')
        
        # next change image file name to match the new id
        # and move the file into the images folder
        
        # the locations where the image is, and where it will be moved to
        if platform == 'linux' or platform == 'linux2':
            old_path = os.getcwd() + "/" + self.ip + ".jpg"
            new_path = os.getcwd() + "/images/" + new_name + ".jpg"
        elif platform == 'win32':
            old_path = os.getcwd() + "\\" + self.ip + ".jpg"
            new_path = os.getcwd() + "\\images\\" + new_name + ".jpg"
            
        # moves the image into the images folder, and names it 'new_id'.jpg
        os.rename(old_path, new_path)
        print("%s: The id of client is now " %self.ip, new_name)
        
        self.database_flag = 0
        self.database_name = new_name
        
        # will let the server know it needs to recompile so the new user can be recognized
        self.recompile = True

    # Overall structure for the server
    def run(self):
        self.sock.settimeout(1)
        while not self.shutdown:
            try:
                command = self.sock.recv(BUFFER_SIZE)
                if command == b'status':
                    print("%s: Client asked for status" %self.ip)
                    self.sock.send(b'1')
                elif command == b"send image":
                    self.sock.send(b'1')
                    self.readData()
                elif command == b"set new user name":
                    self.set_name()
                elif command == b"":
                    self.closeSocket()
                    break
                else:
                    print("%s: Unknown Command of:" %self.ip, command)
                    self.closeSocket()
                    
                    break
            except:
                pass
        print("%s: Stopping Thread" %self.ip)
