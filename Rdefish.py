# You should replace these 3 lines with the output in calibration step

import cv2
assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'
import imutils
from number import transform_exe
import numpy as np
import re
import os
import glob
import sys
import time

#**House warming**DIM=(2592, 1944)
#K=np.array([[1296.362306990352, 0.0, 1473.832773002673], [0.0, 1300.4231696636355, 1406.8315980526995], [0.0, 0.0, 1.0]])
#D=np.array([[-0.03424083879891268], [0.032424581500647406], [-0.026989753296597918], [0.006958292392107039]])

#dot world
DIM=(3280, 2464)
K=np.array([[1629.0410564926335, 0.0, 1722.2789176387014], [0.0, 1630.2284745441577, 820.3114158477711], [0.0, 0.0, 1.0]])
D=np.array([[0.004592385780279527], [-0.07056727309628642], [0.10373344044130645], [-0.05913477899531448]])

Raw_image_path = '/home/pi/Project_ocr/IMAGE SERVER FILES/images/fisheye/'

img_destination_path = '/home/pi/CAPTUREiD iMAGES/'



def undistort():
  if os.listdir(Raw_image_path):
    print("Directory is not empty")   
    time.sleep(5)
    count = 0;
    print "defishing starts..."
    os.chdir(Raw_image_path)
    images = glob.glob('*.jpg')
    
    for fname in images:
      print "processing : "+fname
      completeName= Raw_image_path+fname
      print "Compltnme :"+completeName
      img = cv2.imread(completeName)
      h,w = img.shape[:2]
  
      map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
      #fname = "df"+fname
      undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
      count=count+1;
      path=img_destination_path+fname
      print(path)
      cv2.imwrite(path,undistorted_img)
      #****************************************************************
      g=(stri,confin)=transform_exe(path,fname)
      print(g)

if __name__ == '__main__':
     while(1):
        undistort()