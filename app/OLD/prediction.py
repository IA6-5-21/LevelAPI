import os
from io import BytesIO
#import fastai
# from fastai.vision import *
from azure.storage.blob import BlobClient

from fastai.vision.all import *


def InitLearner(blobFile):
    
    blob_data = BytesIO(blobFile)
    #print(ImgName)

    dls=SegmentationDataLoaders.from_label_func(
        path = path,  fnames = get_image_files(os.path.join(path,"Images")),
        label_func = label_function,
        codes=np.loadtxt(Path(os.path.join(path,'codes.txt')),dtype=str),
        bs=1,num_workers = 0,
        item_tfms=Resize(200)
    )

    learn = unet_learner(dls,resnet34, metrics = acc_camvid )

    ##Load .pkl
    #learn = load_learner(os.path.join(path,'models','LevelFinderV1.pkl'),cpu=True)#'C:/Users/Christian/source/repos/pythonAzureFunction/PythonHttpTrigger/LevelFinderV1')
    #learn = load_learner(os.path.join(path,'models','No_transform_LevelFinderV1.pkl'),cpu=True)
    ##Load .pth
    learn.load(blob_data)#'No_transform_LevelFinderV3')
    #learn.load('LevelFinderV3')
    return learn


def label_function(fn): 
   return os.path.join(path,'Maske',f'{fn.stem}_P.png')
# def label_function(fn): 
#   return path+'\\Maske\\'+f'{fn.stem}_P.png'

  ## Level check method
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
#### Custom metrics #####
def acc_camvid(input, target):
    target = target.squeeze(1)
    #mask = target != void_code
    return (input.argmax(dim=1)==target).float().mean()

##########################

def RunPrediction(ImgName):

    #pred_class, pred_idx, outputs = learn.predict(lastImgName)#os.path.join(path,"Images",'0.jpg'))
    outputs = alearner.predict(ImgName)#os.path.join(path,"Images",'0.jpg'))
    # for i in outputs[0]:
    #     print(i)
    
    #print(pred_class)
    #print(pred_idx)
    #print(outputs[0])
    

    newTensor =  outputs
    return newTensor    

#### code here
path = os.path.join(Path.cwd(),'PythonHttpTrigger')

blob_client = BlobClient.from_blob_url("https://pythonfunctiontesting.blob.core.windows.net/4298b4ec-b6c6-47dc-97f2-658d6b2dc2d1/No_transform_LevelFinderV3.pth?sp=r&st=2021-03-02T21:29:42Z&se=2021-03-03T05:29:42Z&sv=2020-02-10&sr=b&sig=hvm5267oMRa7%2FXtTfif1ZGJKWG%2FGkmpZuvnciS11n9E%3D")
download_stream = blob_client.download_blob()

alearner = InitLearner(download_stream.readall())# fileName)

