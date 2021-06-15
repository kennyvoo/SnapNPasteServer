import cv2
from PIL import Image
import numpy as np
from io import BytesIO

def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image

