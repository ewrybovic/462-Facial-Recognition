from imutils import face_utils
import dlib
import cv2

#GLOBAL
dir_name = 'images/'
image_names = ['obama.jpg', 'two_people.jpg']

'''
Facial landmark coord
Points
1-17 are face/jawline
 - 1-9 is left half
 - 9- 17 is right half
18-22 is left eyebrow
23-27 is right eyebrow
28-31 is nose
 - 32-36 is lower part of nose
37-42 is left eye
43-48 is right eye 
49 - 60 is outer lip outline
 - 61-68 is inner lip outline
'''

#have a draw frame function, draw the rect, the shapes features
# have the x, y coord top corner bottom corner, found face is a boolean
class facialLandmarks:

	def __init__(self): # debug mode show everything else only rectangle 
		self.landmarkFile = "shape_predictor_68_face_landmarks.dat"
		self.faceDetector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor(self.landmarkFile)
		self.landmarks = self.get_facial_landmarks()
		self.facial_landmarks_list = ["face_outline", "l_eyebrow", "r_eyebrow", "nose", "l_eye", "r_eye", "mouth"]
	
	def get_facial_landmarks(self):
		# change to 0 for obama picture
		image_file = dir_name + image_names[0]
		# open image
		img = cv2.imread(image_file)
		# Converting the image to gray scale
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			
		# Get faces into webcam's image
		rects = detector(img, 0)
		# For each detected face, find the landmark.
		for (i, rect) in enumerate(rects):
			# Make the prediction and transfom it to numpy array
			landmarks = predictor(img, rect)
			landmarks = face_utils.shape_to_np(landmarks)

			# Draw on our image, all the finded cordinate points (x,y) 
			""" for (x, y) in landmarks:
				cv2.circle(img, (x, y), 2, (0, 255, 0), -1)
			print("Image %s x, y array: " %(i))
			print(landmarks) """

		# Show the image, uncomment line 36-38 and comment out 39 for resizing 
		#cv2.namedWindow("image", cv2.WINDOW_NORMAL)
		#img_resize = cv2.resize(img, (960, 1266))
		#cv2.imshow("image", img_resize)
		""" cv2.imshow("image", img)
		cv2.waitKey(0)
		cv2.destroyAllWindows() """

		return landmarks
	
	def get_specific_facial_Landmark(self, landmark):
		if (landmark == "hello"):
			pass
 

print(fl.getFacialLandmarks(str(dir_name + image_names[1])))