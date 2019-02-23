import socket
import cv2
from threading import Thread

BUFFER_SIZE = 1024

class ClientThread(Thread):
    # Constructor for the class
    def __init__(self, ip, port, sock, model, debug):
        Thread.__init__(self)
        self.model = model
        self.ip = ip
        self.port = port
        self.sock = sock
        self.debug = debug
        self.didDisconnect = False
        self.shutdown = False
        print(ip +": New thread started for "+ ip + ":", str(port))

    # Closes the socket
    def closeSocket(self):
        print("%s: Closing Socket" %self.ip)
        self.didDisconnect = True
        self.sock.close()

    # Read the data that comes from the client
    def readData(self):
        filename = "%s.jpg" %self.ip
        with open(filename, 'wb') as f:
            print("%s: File opened" %self.ip)
            while True:
                data = self.sock.recv(BUFFER_SIZE)
                if not data or data == b'1':
                    f.close()
                    print("%s: Data received, closing file" %self.ip)
                    break
                
                #write data to file
                f.write(data)
        print("%s: Successfully closed file" %self.ip)
        self.findIdentity(filename)

    # Runs the model to find the identity of the person
    def findIdentity(self, filename):
        print("%s: Finding ID" %self.ip)
        face = cv2.imread(filename)
        if not self.debug:
            id = self.model.findIdentity(face)
            print("%s: The id of client is " %self.ip, id)

            if (id == None):
                id = "None"
        else:
            print("%s: Debug mode enabled" %self.ip)
            id = "Debug"
        # Send the id back to the client
        self.sock.send(str.encode(id))

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