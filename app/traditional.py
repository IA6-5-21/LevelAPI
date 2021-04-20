import base64
from io import BytesIO
import cv2
from PIL import Image
import numpy as np
#from matplotlib import pyplot as plt
import imutils
import sys
import os
import numpy 

def base64toCvImage(base64Input):
    """Method for converting from base64image to
    a picture that cv2 can show and use.
    Mostly code from the old function christina wrote
    in the AzureFunctionPython repo"""
    try:
        base64Data = base64Input.partition(",")[2]
        byteData = base64.b64decode(base64Data+"===")#The equals are extra padding(?)
        imageData = BytesIO(byteData)
        pilImg = Image.open(imageData)
        npImage = np.array(pilImg)
        cvImage = cv2.cvtColor(npImage, cv2.COLOR_RGBA2BGRA)
        return cvImage
    except Exception as ex:
        print(ex)
        return None

def model(cvImage):
    levelPercent = 0
    container_gray = cv2.split(cvImage)[0]
    container_gray = cv2.GaussianBlur(container_gray, (7, 7), 0) # blur image
    (T, container_threshold) = cv2.threshold(container_gray, 50, 255, cv2.THRESH_BINARY_INV)# manual threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    container_open = cv2.morphologyEx(container_threshold, cv2.MORPH_OPEN, kernel) # apply opening operation
    contours = cv2.findContours(container_open.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# find all contours
    contours = imutils.grab_contours(contours)
    
    areas = [cv2.contourArea(contour) for contour in contours]   # sort contours by area
    (contours, areas) = zip(*sorted(zip(contours, areas), key=lambda a:a[1]))
    #container_clone = cvImage.copy()
    # draw bounding box, calculate aspect and display decision
    cv2.drawContours(container_threshold,contours,-1,(255,0,0),2)
    (x, y, w, h) = cv2.boundingRect(contours[-1])
    cv2.rectangle(container_threshold, (x, y), (x + w, y + h), (0, 0, 255), 2)


    containerHeightInPixels = int(w/0.420) #Change this value to width/Hight of container to find correct ratio
    levelPercent = round((h/containerHeightInPixels)*100,1)

    backtorgb = cv2.cvtColor(container_threshold,cv2.COLOR_GRAY2RGB)
    cv2.rectangle(backtorgb, (x, y), (x + w, y + h), (0, 0, 255), 4)
    cv2.putText(backtorgb, f"{levelPercent}%", (x + 10, y + 60), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 5)

    noegreier, buffer = cv2.imencode('.png',backtorgb)
    base64string = toBase64(buffer)
    # cv2.putText(container_clone, f"{levelPercent}%", (x + 10, y + 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
    #cv2.namedWindow("output4", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions                    
    #cv2.imshow("output4", container_clone)                            # Show image
    #cv2.waitKey(0)
    print(levelPercent)
    return {"name":"opencv","level":levelPercent,"image":base64string}

def predict(base64Image):
    cvImage = base64toCvImage(base64Image)
    level = model(cvImage)
    return level
def toBase64(image):
    encoded = f'data:image/png;base64,{base64.b64encode(image).decode()}'
    return encoded
    #base64string=base64.b64encode(buffer)
    #base64string="data:image/png;base64,"+base64string