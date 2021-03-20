import base64
from io import BytesIO
import cv2
from PIL import Image
import numpy as np

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
