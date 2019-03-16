import socket
from threading import Thread
import sys
import time

# Class for a file tansfer client will send an image to a server in a new thread
class FileTransferClient(Thread):
    # Constructor for the class
    def __init__(self, ip, port, ftp_port,buffersize, filename, isSimulated = False):
        #TCP_IP = "192.168.1.173"
        #TCP_PORT = 5000
        #BUFFER_SIZE = 4096
        Thread.__init__(self)
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.TCP_FTP_PORT = ftp_port
        self.BUFFER_SIZE = buffersize
        self.filename = filename
        self.isSimulated = isSimulated
        self.isDone = False
        self.id = ""

    def openSocket(self):
        print("Opening Socket")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.TCP_IP, self.TCP_PORT))

    # Closes the socket
    def closeSocket(self):
        print("Closing Socket")
        self.sock.close()

    # Make the connection with the server
    def makeConnection(self):
        if self.isSimulated:
            return True

        # Try to open the socket and ping the server
        try:
            self.openSocket()
            self.sock.send(b"status")
            status = self.sock.recv(self.BUFFER_SIZE)
            
            # Check on status, don;t technically need this
            if status == b'1':
                print('Connection is good')
                return True
            else:
                print("Connection not good")
                return False
        except:
            print("Could not connect to server") 
            return False

    # Kills the thread
    def closeThread(self):
        self.closeSocket()
        print("Closing Socket")
        #sys.exit()
    
    # function to set up socket to let clinet connect to ftp port
    def establishFTPConnection(self):
        ftpPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ftpPort.connect((self.TCP_IP, self.TCP_FTP_PORT))
        print("%s: FTP connection established to (%s, %s)" %(self.TCP_IP, str(self.TCP_IP), str(self.TCP_FTP_PORT)))
        return ftpPort

    # send a new user name to the server, used in send_name() function in stream.py
    def send_name_to_server(self, user_name):
        self.sock.send(b"set new user name")
        time.sleep(0.5)
        self.sock.send(user_name.encode())
        self.closeThread()

    # Send the image file to the server
    def run(self):
        if self.isSimulated:
            return

        # Send the send image command
        self.sock.send(b"send image") 
        isReady = self.sock.recv(self.BUFFER_SIZE)
        if isReady != b'1':
            print("Bad connection to server")
            self.closeSocket()
            return
        #FCHANGE
        imgTransSock = self.establishFTPConnection()
        print("Sending file")
        f = open(self.filename, 'rb')
        while True:
            print("Opening file to send")
            data = f.read(self.BUFFER_SIZE)

            # Keep reading the file until it is empty
            while (data):
                imgTransSock.send(data) #FCHANG send through ftp port

                # Only read small chunks of data can change this
                data = f.read(self.BUFFER_SIZE)
            if not data:
                print("No more data. Closing file")
                f.close()
                time.sleep(0.5)
                # Tell the sever the file has been fully transfered
                self.sock.send(b'1')
                #self.closeSocket()
                break
        print("%s: Closing client FTP connection to (%s, %s)" %(self.TCP_IP, str(self.TCP_IP), str(self.TCP_FTP_PORT)))
        imgTransSock.close()
        # Get the id of the image sent
        self.id = str(self.sock.recv(self.BUFFER_SIZE), 'utf-8')
        print("Your id is: ", id)
        
        if (self.id != "None" and self.id != ""):
            print("Your id is: ", self.id)
            self.closeThread()

        # need to keep the thread open until closing the window
        # self.closeThread()
