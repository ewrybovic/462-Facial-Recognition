from imutils import face_utils
import dlib
import cv2
import math
import numpy as np

# Calculated the distance between two points
def calculateDistance(x1, y1, x2, y2):
    return format(math.sqrt((x2 - x1)**2 + (y2-y1)**2), '.2f')

# Function for finding the height and width ratios of a face
# top is point 27, bottom is point 8, left is point 0, right is point 16
def findWidthAndHeight(top, bottom, left, right):
    height = calculateDistance(top[0], top[1], bottom[0], bottom[1])
    width = calculateDistance(left[0], left[1], right[0], right[1])
    return (width, height)

# sample code from https://towardsdatascience.com/facial-mapping-landmarks-with-dlib-python-160abcf7d672
 
# let's go code an faces detector(HOG) and after detect the 
# landmarks on this detected face

# p = our pre-treined model directory, on my case, it's on the same script's diretory.
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

cap = cv2.VideoCapture(0)
 
while True:
    # Getting out image by webcam 
    _, image = cap.read()
    # Converting the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    # Get faces into webcam's image
    rects = detector(gray, 0)
    
    # For each detected face, find the landmark.
    for (i, rect) in enumerate(rects):
        # Make the prediction and transfom it to numpy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
    
        # Draw on our image, all the finded cordinate points (x,y) 
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

        # GEtting the landmarks for width and height of face
        (left_x,left_y) = shape[0]
        cv2.circle(image, (left_x,left_y), 2, (0, 0, 255), -1)

        (right_x,right_y) = shape[16]
        cv2.circle(image, (right_x,right_y), 2, (0, 0, 255), -1)

        (top_x, top_y) = shape[27]
        cv2.circle(image, (top_x, top_y), 2, (0,0,255), -1)

        (bot_x, bot_y) = shape[8]
        cv2.circle(image, (bot_x, bot_y), 2, (0,0,255), -1)

        # Draw a line to connect them
        cv2.line(image, (bot_x,bot_y),(top_x,top_y), (255,0,0), 2)
        cv2.line(image, (left_x,left_y),(right_x,right_y), (255,0,0), 2)

        (face_width, face_height) = findWidthAndHeight(shape[27], shape[8], shape[0], shape[16])
        cv2.putText(image, "height: " + str(face_height), (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)
        cv2.putText(image, "width: " + str(face_width), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)

    
    # Show the image
    cv2.imshow("Output", image)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()