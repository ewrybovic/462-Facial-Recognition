import socket
from threading import Thread
from FaceNet import FaceNet
from ClientThread import ClientThread
import time

class FaceNetServer():
    def __init__(self, ip, port, ftp_port, debug):
        self.ip = ip
        self.port = port
        self.ftp_port = ftp_port
        self.debug = debug
        self.shutdown = False
        self.threads = []
        self.model = None

    # Parse the command that the user sent to the server
    def parseCommand(self, command):
        if command == "exit":
            print("Server: Shutdown starting")
            self.shutdown = True
            self.startShutdown()
        elif command == "recomp":
            print("Server: Recompiling model")
            self.model = self.compileModel()
            self.sendModelToThreads()
        else:
            print("Server: Unknown Command")

    # Shutdown function that will close all child threads
    def startShutdown(self):
        for thread in self.threads:
            print("Server: killing thread " + str(thread.ident))
            thread.shutdown = True

    def waitForConnections(self):
        # Start the server
        print("Starting Server", self.ip + ":", self.port)
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpsock.bind((self.ip, self.port))

        # Adding a timeout to the server so the while conditional can be checked
        tcpsock.settimeout(1)
        print("Server: Waiting for connections...")

        while not self.shutdown:
            try:
                tcpsock.listen(5)
                (client_conn, (client_ip, client_port)) = tcpsock.accept()
                print("Server: Connection from", (client_ip, client_port))
                # FCHANGE
                newThread = ClientThread(client_ip, client_port, self.ftp_port, client_conn, self.model, self.debug)
                newThread.start()
                self.threads.append(newThread)

            # Adding a timeout will throw an exception but this doesn't matter
            except:
                pass

    # Sends the new model over to each client thread opened
    def sendModelToThreads(self):
        for thread in self.threads:
            thread.model = self.model

    # Compiles the model if debug is not true
    def compileModel(self):
        # Compile the model
        if not self.debug:
            print('Server: Compiling model please wait.')
            model = FaceNet()
            model.start()

            # Wait for the model to finish before starting the server 
            while not model.isDone:
                time.sleep(5)
                print("Server: Model is still compiling")

            return model

    # Recompile the model when an unknown user gives their name
    def recompileOnNewImage(self):
        
        # continually check each thread to see if we need to recompile the model
        while not self.shutdown:
            for thread in self.threads:
                
                # recompile will be set to true after a new user's image is placed in  the images folder
                if thread.recompile == True:
                    print("Server: New user, recompiling model")
                    thread.recompile = False
                    
                    self.model = self.compileModel()
                    self.sendModelToThreads()
                    
                    print("Server: Done recompiling")
            
            # only check threads every couple of seconds instead of constantly
            time.sleep(5)

    # Function that kicks off the server
    def start(self):
        # Compile the model
        self.model = self.compileModel()

        # Create a thread that just runs the waitForConnections function
        connectionThread = Thread(target=self.waitForConnections)
        connectionThread.start()
        
        # create a thread for recompiling, runs the recompileOnNewImage function
        recompileThread = Thread(target = self.recompileOnNewImage)
        recompileThread.start()

        # While the serer is not shutting down 
        while not self.shutdown:
            self.parseCommand(str(input("Server: Waiting for command...\n")))

        # Stop the connection thread
        connectionThread.join()

if __name__ == "__main__":
    TCP_IP = "localhost"
    TCP_PORT = 5000
    TCP_FTP_PORT = 3000
    DEBUG_MODE = False # change back to false once done testing
    server = FaceNetServer(TCP_IP, TCP_PORT, TCP_FTP_PORT,DEBUG_MODE)
server.start()