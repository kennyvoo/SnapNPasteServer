#azure
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from core import ImageProcessing
from array import array
from fastapi import APIRouter, UploadFile,File, Response,Depends
from fastapi.responses import FileResponse
from typing import Optional
import os
import base64
from PIL import Image
from core import Config
from io import BytesIO
from .auth import fastapi_users
from db.base_class import User
router = APIRouter()

computervision_client = ComputerVisionClient(Config.AZURE_OCR_ENDPOINT, CognitiveServicesCredentials(Config.AZURE_OCR_KEY))

@router.post("/ocr/document_detection")
async def document_detection(file: UploadFile=File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    #imgstream = BytesIO(await file.read())  # convert to byte stream
    response=ImageProcessing.document_finder(await file.read())
    print(response)
    return response

@router.post("/ocr/warped_image")
async def warped_image(file: UploadFile=File(...),points:list=[]):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    #imgstream = BytesIO(await file.read())  # convert to byte stream
    response=ImageProcessing.warped_image(await file.read(),points)
    print(response)
    return response




@router.post("/ocr/azure")
async def ocr(file: UploadFile=File(...)): #,User= Depends(fastapi_users.current_user(active=True, verified=True)
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
    if read_result.status.lower () == "failed":
        return "OCR fail to return "
    else:
         print("successful :)")
    ans=[]
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)
                ans.append(line.text)
                #print(line.bounding_box)
    print("-----------------COMPLETED--------------")
    return ans


@router.post("/ocr/azurefull")
async def ocr(file: UploadFile=File(...)): #,User= Depends(fastapi_users.current_user(active=True, verified=True)
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
                ans.append({"text":line.text,"bb":line.bounding_box})
                #print(line.bounding_box)
    print(ans)
    return ans


@router.post("/ocr")
async def detect_document(file: UploadFile=File(...)):
    """Detects document features in an image."""
    from google.cloud import vision

    import io
    import base64

    client = vision.ImageAnnotatorClient()

    print(type(file),'file type')
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    #image_content = base64.b64encode(await file.read())  # convert to byte stream
    #print(type(image_content))
    image = vision.Image(content=await file.read())

    response = client.document_text_detection(image=image)
    print(response)
    # with open('outputfile.json', 'wb') as outf:
    #     outf.write(response.context)
    print(str(response.full_text_annotation.text))
    ans=[]
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            #print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                # print('Paragraph confidence: {}'.format(paragraph.confidence))
                para=""
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    para+=word_text+" "
                    # print('Word text: {} (confidence: {})'.format(word_text, word.confidence))

                    # for symbol in word.symbols:
                    #     print('\tSymbol: {} (confidence: {})'.format(
                    #         symbol.text, symbol.confidence))
                tempbb=[]
                for vertex in paragraph.bounding_box.vertices:
                    tempbb.append(vertex.x)
                    tempbb.append(vertex.y)
            
                ans.append({"text":para,"bb":tempbb})
                #ans.append({"text":para,"bb":paragraph.bounding_box})
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
        return "Server Error"
    return ans