from fastapi import FastAPI, Request,Depends
from fastapi_socketio import SocketManager
from fastapi.responses import FileResponse

from api import OCR,auth
from core.socketIO import socket_app
from db.db import database


app = FastAPI()


@app.get("/") #specify what http to use
def hello_world(request: Request):
    # client_host = request.client.host
    # return {"client_host": client_host}
    return "Hey Jude"   

@app.get("/hanming") #specify what http to use
def dwdw(request: Request):
    #client_host = request.client.host
    #return {"client_host": client_host}
    #return "Hello sohai""   
    return FileResponse("../hanming.jpeg")



app.include_router(
    OCR.router,
    prefix='/ocr',
    tags=["ocr"],
)
app.include_router(
    auth.router,
    prefix='',
    tags=["auth"],
)

app.mount('/ws', socket_app)



@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()