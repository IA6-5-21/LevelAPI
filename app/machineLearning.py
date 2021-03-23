from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastai.vision.all import *
import uvicorn
import asyncio
import aiohttp
import aiofiles

from io import BytesIO
import sys
import base64, re
from PIL import Image
#Fastai start
path = Path(__file__).parent
# REPLACE THIS WITH YOUR URL
export_url = "https://www.dropbox.com/s/9p1omxq9d275r8e/export.pkl?dl=1"
export_file_name = 'export.pkl'


def label_func(fn): 

  return path/'Maske'/f'{fn.stem}_P.png'


async def download_file(url, dest):
    if dest.exists():
        return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                f = await aiofiles.open(dest, mode='wb')
                await f.write(await response.read())
                await f.close()


async def setup_learner():
    await download_file(export_url, path / export_file_name)
    try:
        
        learn = load_learner(path/export_file_name)
        learn.dls.device = 'cpu'
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

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
#### LEvelchecks
def checkLevel(prediction):
    coffe = 0
    notCoffee = 0
    total=0
    lines = prediction[1]
    for i in range(0,200):
        for j in range(0,200 ):
            if(lines[i][j]==255):
                coffe=coffe+1
            elif(lines[i][j]==127):
                notCoffee = notCoffee+1
            total=total+1
    if coffe != 0 and coffe != 0.0:
        levelEstimate =  round((coffe/(coffe + notCoffee))*100,1)
    else:
        levelEstimate = 'NullLevel'
    print(f"the level is: {levelEstimate}%")
    print(f"Coffee: {coffe}")
    print(f"Not Coffee: {notCoffee}")
    print(f"Total: {total}")
    return levelEstimate


learn = None
#Fastai slutt