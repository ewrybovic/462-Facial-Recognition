How to run:

 - Make sure all of the libraries are downloaded from the requirements.txt
 - Also only python 3.6.6 will work for this project as that was the last build that tensorflow worked with when making this project
 - Start the facenetserver.py by running the command "python facenetserver.py"
 - Wait for the facenet model to compile, there will be a message on the server saying it is waiting for connections
 - Once the server is up, run stream.py with "python stream.py"
 - If the status message says "idle" then the client is connected to the server
 - Press the capture button to send an image to the server
 - If the server does not recognize you then it will ask for your name
 - Wait a few moments for the server to recompile the model
 - Once it is done, send another image and the server should say your name...hopefully
 - In the file menu, you can access some other functionality
 - to exit press teh escape key
 - To turn off the server, type exit and press enter. It will go through the shut off process