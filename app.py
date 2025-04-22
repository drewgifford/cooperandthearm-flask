from flask import Flask, render_template
from cooperandthearm import CooperAndTheArm
from flask_socketio import SocketIO
import asyncio
import os
from routes import define_routes
from sockets import define_sockets
from dispatcher import ArmDispatcher

from serial.tools import list_ports

app: Flask
arm: CooperAndTheArm

PORT = "/dev/cu.usbserial-14130"


async def main():

    # TODO: Add CooperAndTheArm
    arm = CooperAndTheArm(PORT)
    await arm.connect()

    app = Flask(__name__)
    socketio = SocketIO(app, async_mode="eventlet")
    dispatcher = ArmDispatcher(arm)

    await dispatcher.start()

    define_routes(app, dispatcher)
    define_sockets(socketio, dispatcher)

    socketio.run(app)

if __name__ == "__main__":
    asyncio.run(main())