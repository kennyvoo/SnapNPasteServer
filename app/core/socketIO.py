import socketio
from starlette.middleware import cors    
from db.db_temp import db

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[], cors_credentials=True)    
socket_app = socketio.ASGIApp(sio)    

@sio.on("chat",namespace="/ws")
def chat(sid,msg):
    print(msg)

@sio.on("transfer",namespace="/ws")
async def transfer(sid,device_name,data,mode):
    environ= sio.get_environ(sid,namespace="/ws")
    username=environ["HTTP_USERNAME"]
    target_sid=db[username][device_name]

    if mode=="text":
        await sio.emit('sendtext', data ,to=target_sid,namespace="/ws")
    elif mode=="picture":
        await sio.emit('sendpic', data ,to=target_sid,namespace="/ws")
    else:  #pdf
        await sio.emit('sendPDF', data ,to=target_sid,namespace="/ws")
    

@sio.event(namespace="/ws")
async def disconnect(sid):
    # db[username][device_name]=sid  #store sid and device_name
    print('disconnected', sid)
    environ= sio.get_environ(sid,namespace="/ws")
    #print(environ)
    username=environ["HTTP_USERNAME"]
    if(environ["HTTP_ISPHONE"]=="true"):
        sio.leave_room(sid,username,namespace="/ws")
    else:
        del db[username][environ["HTTP_DEVICENAME"]]
        #db[username].pop(environ["HTTP_DEVICENAME"])
    await update_devices_status(username)


@sio.event(namespace="/ws")
async def connect(sid, environ):
    # print(environ)
    username=environ["HTTP_USERNAME"]
    print('connected', sid)
    
    if(environ["HTTP_ISPHONE"]=="true"):
        sio.enter_room(sid, username,namespace="/ws")  # put all mobile devices into room
    else:
        db[username][environ["HTTP_DEVICENAME"]]=sid  #store the computer sid
    await update_devices_status(username)



async def update_devices_status(username):

    devices=[device for device,W in db[username].items()]
    print(username)
    print(db[username])
    print(devices)
    await sio.emit('online_devices', devices , room=username,namespace="/ws")
