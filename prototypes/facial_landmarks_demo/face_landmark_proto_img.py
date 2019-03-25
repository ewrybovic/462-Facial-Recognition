from imutils import face_utils
import dlib
import cv2
import math

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
class FacialLandmarks:

	def __init__(self): # debug mode show everything else only rectangle 
		self.landmarkFile = "shape_predictor_68_face_landmarks.dat"
		self.faceDetector = dlib.get_frontal_face_detector()
		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor(self.landmarkFile)
		# Should not get land marks in constructor
		#self.landmarks = self.get_facial_landmarks()

		self.landmarks = None
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
		if (landmark == "hello"):
			pass


	# Gets the height and width of the face
	# Returns in list [img, height, width]
	def get_height_width(self, img, recalc_landmarks = False, draw_on_image = False):
		# Get landmarks if none exists or if user wants to recalc image
		if self.landmarks == None or calc_landmarks:
			self.get_facial_landmarks(img)

		# Get facial features
		top = self.landmarks[27]
		bot = self.landmarks[8]
		left = self.landmarks[0]
		right = self.landmarks[16]

		# Calculate hight and width
		height = self.calculateDistance(top[0], top[1], bot[0], bot[1])
		width = self.calculateDistance(left[0], left[1], right[0], right[1])

		if draw_on_image:
			if type(img) == str:
				img = cv2.imread(img)

			cv2.line(img, (bot[0], bot[1]), (top[0], top[1]), (255, 0, 0), 2)
			cv2.line(img, (right[0], right[1]), (left[0], left[1]), (255, 0, 0), 2)
			cv2.putText(img, "height: " + str(height), (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)
			cv2.putText(img, "width: " + str(width), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)
			return (img, height, width)
		else:
			return (height, width)

 
if __name__ == "__main__":
	fl = FacialLandmarks()
	img, _, _ = fl.get_height_width(str(dir_name + image_names[0]), draw_on_image=True)
	cv2.imshow("Out", img)
	cv2.waitKey(0)