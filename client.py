import asyncio
import socketio
# I tested this code as it is in Mac OS
from pynput.keyboard import Key, Controller
import subprocess
from kivy.app import App
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        return Button(text='Hello World')

TestApp().run()

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection established')

@sio.event
async def my_message(data):
    print('message received with ', data)
    await sio.emit('my response', {'response': 'my response'})

@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('http://byteus.me:8000',
        namespaces="/ws",socketio_path ="ws/socket.io",
        transports ="websocket",
        headers={"USERNAME":"kenny","DEVICENAME":"laptop","ISPHONE":"false"})
    await sio.wait()
    print('connected to server')


@sio.on('sendtext',namespace="/ws")
def receivetext(text):
    paste(text)

def paste(text):
    cmd='echo '+text.strip()+'|clip'
    subprocess.check_call(cmd, shell=True)
    
    keyboard = Controller()

    keyboard.press(Key.ctrl.value) #this would be for your key combination
    # keyboard.press(Key.cmd.value)
    keyboard.press('v')
    keyboard.release('v')
    keyboard.release(Key.ctrl.value) #this would be for your key combination
    # keyboard.release(Key.cmd.value)


if __name__ == '__main__':
    asyncio.run(main())