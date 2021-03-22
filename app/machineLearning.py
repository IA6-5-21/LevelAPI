from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastai.vision.all import *
import uvicorn
import asyncio
import aiohttp
import aiofiles

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

learn = None
#Fastai slutt