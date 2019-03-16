import cv2
import numpy as np

# Global Variables
DEBUG = True
BLUR = 21
CANNY_THRESH_1 = 10
CANNY_THRESH_2 = 200
MASK_DILATE_ITER = 10
MASK_ERODE_ITER = 10
MASK_COLOR = (0.0, 0.0, 0)

# Detects edges in an image and removes noise from the background using Opening
def edgeDetection(img, DEBUG=False, ERODE_IMAGE=True):
	img = cv2.GaussianBlur(img, (1,1), 0)
	if DEBUG:
		cv2.imshow('Blur',img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	# Find edges in the image
	edges = cv2.Canny(img, CANNY_THRESH_1, CANNY_THRESH_2)
	if DEBUG:
		cv2.imshow('canny',edges)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	# Dilate makes the lines generated by the edges to be bigger
	edges = cv2.dilate(edges, None)
	if DEBUG:
		cv2.imshow('dilate',edges)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	if ERODE_IMAGE:
		# Erode makes the lines smaller
		edges = cv2.erode(edges, None)
		if DEBUG:
			cv2.imshow('erode',edges)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

	return edges

# Creates a mask of the iamge
def createMask(edges, DEBUG=False, ERODE_MASK=False):
	# Find contours in the edges, sort by the area
	contour_info = []

	# Find the contours in the image
	_, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

	# add all of the contours into the list
	for c in contours:
		contour_info.append((
			c,
			cv2.isContourConvex(c),
			cv2.contourArea(c)
		))

	# Sort the list
	contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
	max_contour = contour_info[0]

	# create an empty mask then draw a polygon of the max contour
	mask = np.zeros(edges.shape)
	cv2.fillConvexPoly(mask, max_contour[0], (255))

	if DEBUG:
		cv2.imshow('mask',mask)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	# Smooth and blur mask
	if ERODE_MASK:
		mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
		if DEBUG:
			cv2.imshow('mDilate',mask)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
		if DEBUG:
			cv2.imshow('mErode',mask)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

	# BLur mask to get rid of artifacts
	mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
	if DEBUG:
		cv2.imshow('mGaus',mask)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	return mask

# Blends the make and image together
def blendMaskAndImage(img, mask):
	# Create a 3-channel np array
	mask_stack = np.dstack([mask]*3)

	# before blending convert int value to float
	mask_stack = mask_stack.astype('float32') / 255.0
	img = img.astype('float32') / 255.0

	#blend then convert to int
	masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR)
	masked = (masked * 255).astype('uint8')
	return masked

# Function to call to remove the background of an image
def CleanBackground(img, debug=True, erode_mask=False, erode_image=True):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	edges = edgeDetection(gray, DEBUG=debug, ERODE_IMAGE=erode_image)
	mask = createMask(edges, DEBUG=debug, ERODE_MASK=erode_mask)
	return blendMaskAndImage(img, mask)

if __name__ == '__main__':
	img = CleanBackground(cv2.imread('Evan.jpg'))
	cv2.imshow('output', img)
	cv2.waitKey()


