from fastapi import FastAPI, Request
from fastapi_socketio import SocketManager

from api import OCR
from core.socketIO import socket_app
app = FastAPI()




@app.get("/hello") #specify what http to use
def hello_world(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}
    #return "Hello sohai"   


app.include_router(
    OCR.router,
    prefix='/ocr',
    tags=["ocr"]
)
app.mount('/ws', socket_app)


