import socket
from threading import Thread
from socketserver import ThreadingMixIn
from FaceNet import FaceNet
import time
import cv2


TCP_IP = "localhost"
TCP_PORT = 5000
BUFFER_SIZE = 1024
#Buffer_SIZE = 4096

class ClientThread(Thread):
    # Constructor for the class
    def __init__(self, ip, port, sock, model):
        Thread.__init__(self)
        self.model = model
        self.ip = ip
        self.port = port
        self.sock = sock
        print("New thread started for "+ ip + ":", str(port))

    # Closes the socket
    def closeSocket(self):
        print("%s: Closing Socket" %self.ip)
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
        id = self.model.findIdentity(face)
        print("%s: The id of client is " %self.ip, id)

        # Send the id back to the client
        self.sock.send(str.encode(id))

    # Overall structure for the server
    def run(self):
        while True:
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
        print("%s: Stopping Thread" %self.ip)

if __name__ == '__main__':
    print('Compiling model please wait.')

    # Create the model and compile it
    model = FaceNet()
    model.start()

    # Wait for the model to finish before starting the server 
    while not model.isDone:
        time.sleep(5)
        print("Model is still compiling")

    # Start the server
    print("Starting Server", TCP_IP + ":", TCP_PORT)
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    #threads = []

    while True:
        print("Waiting for connections...")
        tcpsock.listen(5)
        (conn, (ip, port)) = tcpsock.accept()
        print("Connection from", (ip, port))
        newThread = ClientThread(ip, port, conn, model)
        newThread.start()
        #threads.append(newThread)

    #for thread in threads:
    #    thread.join()