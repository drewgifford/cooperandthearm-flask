from flask import Flask
from cooperandthearm import CooperAndTheArm
from flask_socketio import SocketIO
import asyncio
from routes import define_routes
from sockets import define_sockets
from updates import define_updates

socketio: SocketIO = None

async def main():

    arm = CooperAndTheArm("/dev/cu.usbserial-14230")
    await arm.connect()

    app = Flask(__name__)
    socketio = SocketIO(app, async_mode="threading")
    
    define_routes(app, arm)
    define_sockets(socketio, arm)
    define_updates(socketio, arm)

    socketio.run(app)

if __name__ == "__main__":
    asyncio.run(main())