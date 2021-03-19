from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastai.vision.all import *
import uvicorn
import asyncio
import aiohttp
import aiofiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


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
    loop = asyncio.get_event_loop()  # get event loop
    tasks = [asyncio.ensure_future(setup_learner())]  # assign some task
    learn = (await asyncio.gather(*tasks))[0]  # get tasks


@app.post("/fastai/predict")
async def machineLearningPrediction(file: bytes = File(...)):
    pred = learn.predict(file)
    return {"result": pred[0]}

@app.post("/opencv/predict")
async def analyze(file: bytes = File(...)):
    pred = learn.predict(file)
    return {"result": pred[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80