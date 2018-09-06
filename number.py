import cv2 as cv
import imutils
import io
from transform import four_point_transform
import numpy as np
from google.cloud import storage
from google.cloud import vision
from google.protobuf import json_format

def denoising(path):
	img = cv.imread('/home/pi/Project_ocr/IMAGE SERVER FILES/Results/gray_image.png')
	b,g,r = cv.split(img)           # get b,g,r
	rgb_img = cv.merge([r,g,b])     # switch it to rgb

	# Denoising
	dst = cv.fastNlMeansDenoising(img,None,10,7,21) #For RGB-cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)

	b,g,r = cv.split(dst)           # get b,g,r
	rgb_dst = cv.merge([r,g,b])     # switch it to rgb
	cv.imwrite('/home/pi/Project_ocr/IMAGE SERVER FILES/Results/denoising.png',rgb_dst)
	return rgb_dst


def conv_grayscale(path):
	image = cv.imread('/home/pi/Project_ocr/IMAGE SERVER FILES/Results/final.jpg')
	gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
	cv.imwrite('/home/pi/Project_ocr/IMAGE SERVER FILES/Results/gray_image.png',gray_image)
	return denoising('/home/pi/Project_ocr/IMAGE SERVER FILES/Results/gray_image.png')
	
	
	  
def increse_contrast(path):
	img = cv.imread(path)

	lab= cv.cvtColor(img, cv.COLOR_BGR2LAB)

	l, a, b = cv.split(lab)

	clahe = cv.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
	cl = clahe.apply(l)

	limg = cv.merge((cl,a,b))

	final = cv.cvtColor(limg, cv.COLOR_LAB2BGR)
	cv.imwrite('/home/pi/Project_ocr/IMAGE SERVER FILES/Results/final.jpg',final)
	return conv_grayscale('/home/pi/Project_ocr/IMAGE SERVER FILES/Results/final.jpg')
	
def detect_document(path):
	"""Detects document features in an image."""
	client = vision.ImageAnnotatorClient()

	# [START vision_python_migration_document_text_detection]
	with io.open(path, 'rb') as image_file:
		content = image_file.read()

	image = vision.types.Image(content=content)

	response = client.document_text_detection(image=image)
	stri=''
	sav=0
	count=0
	for page in response.full_text_annotation.pages:
		for block in page.blocks:
			for paragraph in block.paragraphs:
				for word in paragraph.words:
					word_text = ''.join([symbol.text for symbol in word.symbols])
					#print('Word text: {} (confidence: {})'.format(word_text, word.confidence))
					stri+=word_text
					sav=sav+word.confidence
					count=count+1
					#print(stri)
	if count==0:
		return (None,None)
	return (stri,abs(sav/count))
					

def transform_exe(frame,fname):
	image = cv.imread(frame)
        image = imutils.rotate(image,180)
	pt=[(393,761),(3039,624),(2995,2310),(409,2310)]
	pt=str(pt)
	pts = np.array(eval(pt), dtype = "float32")
	 
	# apply the four point tranform to obtain a "birds eye view" of
	# the image
	warped = four_point_transform(image, pts)
	cv.imwrite('/home/pi/Project_ocr/IMAGE SERVER FILES/Results/warped.jpg',warped)
	cv.imwrite('/home/pi/CAPTUREiD iMAGES/'+fname,warped)
	cont=increse_contrast("/home/pi/Project_ocr/IMAGE SERVER FILES/Results/warped.jpg")
	cv.imwrite('/home/pi/Project_ocr/IMAGE SERVER FILES/Results/gimp.png',cont)
	return detect_document('/home/pi/Project_ocr/IMAGE SERVER FILES/Results/gimp.png')
 
			

			
					


