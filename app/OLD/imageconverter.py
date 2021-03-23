from io import BytesIO
import sys
import base64, re
from PIL import Image
import fastai
from fastai.vision.all import *

path = os.path.join(Path.cwd(),'PythonHttpTrigger')

def base64toimage(baseInput):
    try: 
            base64_data = re.sub('^data:image/.+;base64,', '', baseInput)
            byte_data = base64.b64decode(base64_data)
            image_data = BytesIO(byte_data)

    except:
        pass

    #print(baseInput)
    
    lastImgName = ''
    try:
        img = Image.open(image_data)
        #img
        t = time.time()
        #imagename = 'test' +str(t) + '.png'
        imagename = 'incommingImage.png'
        lastImgName = os.path.join(path,imagename)#'PythonHttpTrigger\\'+'test' +str(t) + '.png'
        img.save(lastImgName)
    except:
        pass
    return lastImgName

def tensor2image(tensors):
    ### Saving plot to PNG #####
    plt.imshow(tensors[1])
    filename = 'predictionPlot.png'
    plotfile = os.path.join(path,filename)
    plt.savefig(plotfile)
    encoded = f'data:image/png;base64,{base64.b64encode(open(plotfile, "rb").read()).decode()}' 
    #'data:image/png;base64,{}'.format(encoded)
    #plotImage =   Image.open('books_read.png')  
    #encoded_string = ""
    #plotBytes  = BytesIO(plotImage)
    #encoded_string = base64.b64encode(plotBytes)
    return encoded