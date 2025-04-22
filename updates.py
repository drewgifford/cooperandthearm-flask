from cooperandthearm import CooperAndTheArm, Command, GetAngle, GetSpeed
from flask_socketio import SocketIO
import asyncio
import threading
from util import COMPONENTS

async def update_thread(socketio: SocketIO, arm: CooperAndTheArm):
    """
    Update clients with the latest arm angle and speed.
    """
    print("Starting update thread...")

    last_packet = None

    while True:

        data = {}

        for component in COMPONENTS:

            speed, angle = await arm.dispatch(
                Command(component, GetSpeed()),
                Command(component, GetAngle())
            )

            data[component.name.lower()] = {
                "angle": angle,
                "speed": speed
            }

        if data != last_packet:
            socketio.emit("update", data)
            last_packet = data

        await asyncio.sleep(0.1)


def define_updates(socketio: SocketIO, arm: CooperAndTheArm) -> threading.Thread:

    update_thread_instance = threading.Thread(target=asyncio.run, args=(update_thread(socketio, arm),))
    update_thread_instance.daemon = True
    update_thread_instance.start()

    return update_thread_instance
