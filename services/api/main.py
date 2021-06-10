from fastapi import FastAPI, UploadFile,File, Response
from fastapi.responses import FileResponse
from typing import Optional
import cv2
import pytesseract
import numpy as np
import shutil
import base64
from PIL import Image
from io import BytesIO

app = FastAPI()

@app.get("/") #specify what http to use
def hello_world():
    return "Hello World 123"

def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image

@app.post("/ocr")
async def ocr(file: UploadFile=File(...)):
    print("receiveddd d")
    print(type(file),'file type')
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    # print(type(file.file))
    img = read_imagefile(await file.read())
    # print(type(img))
    output =  image_processing(img)
    return output

def image_processing(img):
    img = np.array(img)
    try:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
    except:
        img =  cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gray = cv2.bitwise_not(img_bin)

    kernel = np.ones((2, 1), np.uint8)
    img = cv2.erode(gray, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    # cv2.imshow('ab',img)
    # cv2.waitKey(0)
    out_below = pytesseract.image_to_string(img)
    print("OUTPUT:", out_below)
    return out_below