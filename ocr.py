# -*- coding: utf-8 -*-
"""OCR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N3owZRFLrSLNVSFy6Eh37zDNTChwKqn2
"""

#Import drive
from google.colab import drive
drive.mount('/content/gdrive')

# Commented out IPython magic to ensure Python compatibility.
#Move to the directory having current notebook
# %cd gdrive/My\ Drive/Colab\ Notebooks/OCR

#Install Tesseract and ISR
!sudo apt install tesseract-ocr
!pip install pytesseract
!pip install ISR

# Commented out IPython magic to ensure Python compatibility.
#Import important libraries
import pytesseract
from pytesseract import Output
import cv2
from google.colab.patches import cv2_imshow
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import re
import os
import imutils
import glob
from PIL import Image

# Create two folders named as "LR_images" and "SR_images"
# Put all the low resolution images in LR_images folder and then use GANS to 
# convert it into High Resolution
# Put all converted images into SR_images folder

#import GANs model
from ISR.models import RRDN     

#load the pretrained weights - (Trained on DIV2K dataset)
model = RRDN(weights='gans')   

files = [img for img in glob.glob("LR_images/*.jpg")]
d=1
for im in files:
  img = Image.open(im)
  sr_img = model.predict(np.array(img))
  Image.fromarray(sr_img).save("SR_images/%d.jpg"%d)
  d+=1

# Regular expression and validation of aadhar no.
def regex(text):
  uid = set()
  newlist = []
  for xx in text.split('\n'):
    newlist.append(xx)
  newlist = list(filter(lambda x: len(x) > 12, newlist))
  for no in newlist:
    if re.match("^[0-9 ]+$", no):
      uid.add(no)
  if(len(list(uid))>=1):
    # Validating using Verhoeff algorithm
    if(validate(list(uid)[0])):
      print(list(uid)[0])
      print('\n')
      return 1
    else:
      print('Invalid Aadhar no.')
      print('\n')
      return 1
  else:
    return None

# Sharpen the image
def sharp(img):
  kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
  img = cv2.filter2D(img, -1, kernel)
  return img

# To validate aadhaar Num
def validate(aadhaarNum):

        aadhaarNum = aadhaarNum.split(" ")
        y = ""
        for i in aadhaarNum:
          y = y + i

        mult = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5], [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
            [3, 4, 0, 1, 2, 8, 9, 5, 6, 7], [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
            [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3], [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]

        perm = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4], [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
            [8, 9, 1, 6, 0, 4, 3, 5, 2, 7], [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]


        try:
            i = len(y)
            j = 0
            x = 0

            while i > 0:
                i -= 1
                x = mult[x][perm[(j % 8)][int(y[i])]]
                j += 1
            if x == 0:
                return 1 
            else:
                return 0 

        except ValueError:
            return 0 
        except IndexError:
            return 0

# Extraction of aadhar card from different images
# LOGIC:- For each image extract aadhar card no. if not found 
#         sharpen the image and then found, if not found again
#         rotate the image by 90 degree and repeat the same process.

####################### CHECK WITH LOW RESOLUTION IMAGES ######################
'''
filenames = [img for img in glob.glob("LR_images/*")]
for img in filenames:
    im = cv2.imread(img)
    cv2_imshow(im)
    config = ('-l eng --oem 3 --psm 11')
    text = pytesseract.image_to_string(im, config=config)
    if(regex(text)):
      continue
    else:
      img = sharp(im)
      text = pytesseract.image_to_string(img, config=config)
      if(regex(text)): continue
      im = imutils.rotate(im, 90)
      text = pytesseract.image_to_string(im, config=config)
      if(regex(text)):
        continue
      else:
        img = sharp(im)
        text = pytesseract.image_to_string(img, config=config)
        if(regex(text)): continue
        im = imutils.rotate(im, 90)
        text = pytesseract.image_to_string(im, config=config)
        if(regex(text)):
          continue
        else:
          img = sharp(im)
          text = pytesseract.image_to_string(img, config=config)
          if(regex(text)): continue
          im = imutils.rotate(im, 90)
          text = pytesseract.image_to_string(im, config=config)
          if(regex(text)):
            continue
          else:
            img = sharp(im)
            text = pytesseract.image_to_string(img, config=config)
            if(regex(text)): continue
            print('None')
            print('\n')
'''
####################### CHECK WITH SUPER RESOLUTION IMAGES ####################
# Use it if aadhar number not extracted using low resolution images.

filenames = [img for img in glob.glob("SR_images/*.jpg")]
for img in filenames:
    im = cv2.imread(img)
    cv2_imshow(im)
    config = ('-l eng --oem 3 --psm 11')
    text = pytesseract.image_to_string(im, config=config)
    if(regex(text)):
      continue
    else:
      img = sharp(im)
      text = pytesseract.image_to_string(img, config=config)
      if(regex(text)): continue
      im = imutils.rotate(im, 90)
      text = pytesseract.image_to_string(im, config=config)
      if(regex(text)):
        continue
      else:
        img = sharp(im)
        text = pytesseract.image_to_string(img, config=config)
        if(regex(text)): continue
        im = imutils.rotate(im, 90)
        text = pytesseract.image_to_string(im, config=config)
        if(regex(text)):
          continue
        else:
          img = sharp(im)
          text = pytesseract.image_to_string(img, config=config)
          if(regex(text)): continue
          im = imutils.rotate(im, 90)
          text = pytesseract.image_to_string(im, config=config)
          if(regex(text)):
            continue
          else:
            img = sharp(im)
            text = pytesseract.image_to_string(img, config=config)
            if(regex(text)): continue
            print('None')
            print('\n')

