import socketio    
from db.db_temp import db

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*' )    
socket_app = socketio.ASGIApp(sio)    

@sio.on("chat",namespace="/ws")
def chat(sid,msg):
    print(msg)

@sio.on("myInfo",namespace="/ws")
def online(sid,username,device_name,isPhone):
    #sio.enter_room(sid, username)
    db[username][device_name]=sid  #store sid and device_name
    update_devices_status()

@sio.event(namespace="/ws")
async def disconnect(sid):
    # db[username][device_name]=sid  #store sid and device_name
    print('disconnected', sid)
    environ= sio.get_environ(sid,namespace="/ws")
    username=environ["HTTP_USERNAME"]
    if(environ["HTTP_ISPHONE"]):
        sio.leave_room(sid,username,namespace="/ws")
    else:
        db[username].pop(environ["HTTP_DEVICENAME"])
    await update_devices_status(username)

@sio.event(namespace="/ws")
async def connect(sid, environ):
    username=environ["HTTP_USERNAME"]
    if(environ["HTTP_ISPHONE"]):
        sio.enter_room(sid, username,namespace="/ws")  # put all mobile devices into room
    else:
        db[username][environ["HTTP_DEVICENAME"]]=sid  #store the computer sid
    await update_devices_status(username)


async def update_devices_status(username):
    devices=[device for device,W in db[username].items()]
    await sio.emit('online_devices', devices , room=username,namespace="/ws")
