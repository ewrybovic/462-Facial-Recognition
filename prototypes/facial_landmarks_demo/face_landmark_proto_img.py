
from imutils import face_utils
import dlib
import cv2
import math
import enum

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
# enum in python, gives you the start/stop  for the features in self.landmarks, chnage enums to single int 
class facialLandmarkType(enum.Enum):
		#basic
		jawline = (1,17)
		leftEyebrow = (18, 22)
		rightEyeBrow = (23, 27)
		nose = (28, 31)
		leftEye = (37, 42)
		rightEye = (43, 48)
		mouth = (49, 68)
		# specific
		top = 27
		bot = 8
		left = 0
		right = 16

#have a draw frame function, draw the rect, the shapes features
# have the x, y coord top corner bottom corner, found face is a boolean
class FacialLandmarks:

	def __init__(self): # debug mode show everything else only rectangle 
		self.landmarkFile = "shape_predictor_68_face_landmarks.dat"
		self.faceDetector = dlib.get_frontal_face_detector()
		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor(self.landmarkFile)
		# Should not get land marks in constructor
		#self.landmarks = self.get_facial_landmarks()
		self.height = 0
		self.width = 0
		self.top = [0,0]
		self.bot = [0,0]
		self.right = [0,0]
		self.left = [0,0]

		self.landmarks = []
		self.facial_landmarks_list = ["face_outline", "l_eyebrow", "r_eyebrow", "nose", "l_eye", "r_eye", "mouth"]
	
	def get_facial_landmarks(self, img):
		# change to 0 for obama picture
		#image_file = dir_name + image_names[0]
		# Check if image is a string and open if so
		if type(img) == str:
			img = cv2.imread(img)

		# Converting the image to gray scale
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			
		# Get faces into webcam's image
		rects = self.detector(img, 0)
		# For each detected face, find the landmark.
		for (i, rect) in enumerate(rects):
			# Make the prediction and transfom it to numpy array
			pred = self.predictor(img, rect) # Having one variable for two different data types is slow in python
			self.landmarks = face_utils.shape_to_np(pred)

			# Only get the first face
			break

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

		return self.landmarks


	# Calculate the distance between two points
	def calculateDistance(self, x1, y1, x2, y2):
	    return format(math.sqrt((x2 - x1)**2 + (y2-y1)**2), '.2f')

	
	def get_specific_facial_Landmark(self, landmark):
		if (landmark == facialLandmarkType.top):
			return self.landmarks[27]
		if (landmark == facialLandmarkType.bot):
			return self.landmarks[8]
		if (landmark == facialLandmarkType.left):
			return self.landmarks[0]
		if (landmark == facialLandmarkType.right):
			return self.landmarks[16]
		#---
		if (landmark == facialLandmarkType.jawline):
			return self.landmarks[0:16]
		if (landmark == facialLandmarkType.leftEyebrow):
			return self.landmarks[17:21]
		if (landmark == facialLandmarkType.rightEyeBrow):
			return self.landmarks[22:26]
		if (landmark == facialLandmarkType.nose):
			return self.landmarks[27:30]
		if (landmark == facialLandmarkType.leftEye):
			return self.landmarks[36:41]
		if (landmark == facialLandmarkType.rightEye):
			return self.landmarks[42:47]
		if (landmark == facialLandmarkType.mouth):
			return self.landmarks[48:67]
	
	def drawFaceFrame(self):
		# get top, bot, left, right landmarks and draw a bo around it 
		pass

	def drawLandmarks(self, imgDraw, img):
		for (x, y) in self.landmarks:
			imgDraw.circle(img, (x, y), 2, (0, 255, 0), -1)

	# Draws width and hieght on image
	def draw_on_image(self, img):
		if len(self.landmarks) == 0:
			return None

		if type(img) == str:
				img = cv2.imread(img)

		cv2.line(img, (self.bot[0], self.bot[1]), (self.top[0], self.top[1]), (255, 0, 0), 2)
		cv2.line(img, (self.right[0], self.right[1]), (self.left[0], self.left[1]), (255, 0, 0), 2)
		cv2.putText(img, "height: " + str(self.height), (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)
		cv2.putText(img, "width: " + str(self.width), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)

		return img

	# Gets the height and width of the face
	# Returns in list [img, height, width]
	def get_height_width(self, img, recalc_landmarks = False):
		# Get landmarks if none exists or if user wants to recalc image
		if len(self.landmarks) == 0 or recalc_landmarks:
			self.get_facial_landmarks(img)

		# If the landmarks is still 0, then there wasn't a face
		if len(self.landmarks) != 0:
			# Get facial features
			self.top = self.landmarks[27]
			self.bot = self.landmarks[8]
			self.left = self.landmarks[0]
			self.right = self.landmarks[16]

			# Calculate hight and width
			self.height = self.calculateDistance(self.top[0], self.top[1], self.bot[0], self.bot[1])
			print(self.height)
			self.width = self.calculateDistance(self.left[0], self.left[1], self.right[0], self.right[1])
			print(self.width)


	def drawLandmarks(self, imgDraw, img):
		for (x, y) in self.landmarks:
			imgDraw.circle(img, (x, y), 2, (0, 255, 0), -1)
 
if __name__ == "__main__":
	fl = FacialLandmarks()
	fl.get_height_width(str(dir_name + image_names[0]), recalc_landmarks = True)
	img = fl.draw_on_image(str(dir_name + image_names[0]))
	cv2.imshow("Out", img)
	cv2.waitKey(0)