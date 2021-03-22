from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastai.vision.all import *
#import traditional as trad
import uvicorn
import asyncio
import aiohttp
import aiofiles
from fastapi.middleware.cors import CORSMiddleware
from machineLearning import *
from pydantic import BaseModel 

class Item(BaseModel): 
    image: str 
    name: str

app = FastAPI()



origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Setup the learner on server start"""
    global learn
    '''Receive model from onedrive'''
    '''commented out to increase loading speed when not predicting during development''' 
    #loop = asyncio.get_event_loop()  # get event loop
    #tasks = [asyncio.ensure_future(setup_learner())]  # assign some task
    #learn = (await asyncio.gather(*tasks))[0]  # get tasks




@app.get("/fastai/predict",response_class=HTMLResponse)
async def wrongPage():
    '''GET for browser entry to /fastai/predict, giving link to coffeeefinder webpage'''
    #pred = learn.predict(file)
    print("GET test")
    return """
    <html>
        <head>
            <title>Wrong place!</title>
        </head>
        <body>
            <h1>Wrong page, please goto Coffeefinder webpage@ <a href="http://localhost:3000/">localhost:3000</a>!</h1>
        </body>
    </html>
    """
    

@app.post("/fastai/predict")
async def machineLearningPrediction(item:Item):
    #pred = learn.predict(file)
    '''ReturnTEST; sending recieved image back to sender (coffeefinder webpage)'''
    return {"name": "Hello worlD!", "image":item.image}

'''Commented out during development of machinelearning module'''
# @app.post("/opencv/predict")
# async def analyze(file: bytes = File(...)):
#     pred = learn.predict(file)
#     return {"result": pred[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)