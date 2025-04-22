from flask import Flask
from cooperandthearm import CooperAndTheArm
from flask_socketio import SocketIO
import asyncio
#from routes import define_routes
#from sockets import define_sockets
#from updates import define_updates


async def main():

    arm = CooperAndTheArm("COM4")
    await arm.connect()

    app = Flask(__name__)
    socketio = SocketIO(app)

    #define_routes(app, arm)
    #define_sockets(socketio, arm)
    #define_updates(socketio, arm)

    socketio.run(app)
    

if __name__ == "__main__":
    asyncio.run(main())