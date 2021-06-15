#azure
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from core import ImageProcessing
from array import array
from fastapi import APIRouter, UploadFile,File, Response
from fastapi.responses import FileResponse
from typing import Optional
import os
import sys
import time
import shutil
import base64
from PIL import Image
from core import Config
from io import BytesIO



router = APIRouter()
computervision_client = ComputerVisionClient(Config.AZURE_OCR_ENDPOINT, CognitiveServicesCredentials(Config.AZURE_OCR_KEY))


@router.post("")
async def ocr(file: UploadFile=File(...)):
    print(type(file),'file type')
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"

    imgstream = BytesIO(await file.read())  # convert to byte stream
    read_response = computervision_client.read_in_stream(imgstream, raw=True)
    # Get the operation location (URL with ID as last appendage)
    read_operation_location = read_response.headers["Operation-Location"]
    # Take the ID off and use to get results
    operation_id = read_operation_location.split("/")[-1]
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower () not in ['notstarted', 'running']:
            break
        print ('Waiting for result...') 

    ans=[]
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)
                ans.append(line.text)
                #print(line.bounding_box)
    return ans

