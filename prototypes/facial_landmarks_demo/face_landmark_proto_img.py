from imutils import face_utils
import dlib
import cv2

#GLOBAL
dir_name = 'images/'
image_names = ['obama.jpg', 'two_people.jpg']

# p = our pre-treined model directory, on my case, it's on the same script's diretory.
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

# change to 0 for obama picture
image_file = dir_name + image_names[0]
# open image
imgg = cv2.imread(image_file)
# Converting the image to gray scale
gray = cv2.cvtColor(imgg, cv2.COLOR_BGR2GRAY)
	
# Get faces into webcam's image
rects = detector(imgg, 0)
# For each detected face, find the landmark.
for (i, rect) in enumerate(rects):
	# Make the prediction and transfom it to numpy array
	shape = predictor(imgg, rect)
	shape = face_utils.shape_to_np(shape)

	# Draw on our image, all the finded cordinate points (x,y) 
	for (x, y) in shape:
		cv2.circle(imgg, (x, y), 2, (0, 255, 0), -1)
	print("Image %s x, y array: " %(i))
	print(shape)

# Show the image, uncomment line 36-38 and comment out 39 for resizing 
#cv2.namedWindow("image", cv2.WINDOW_NORMAL)
#img_resize = cv2.resize(imgg, (960, 1266))
#cv2.imshow("image", img_resize)
cv2.imshow("image", imgg)
cv2.waitKey(0)
cv2.destroyAllWindows()