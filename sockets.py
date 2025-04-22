from flask import Flask
from cooperandthearm import CooperAndTheArm, Component
from cooperandthearm.command import Command
from cooperandthearm.instruction import SetSpeed, SetAngle, Instruction, GetAngle
from flask_socketio import SocketIO
from util import component_from_str, instruction_from_set_option
import asyncio
from threading import Thread, Event

movement_thread: Thread | None = None
movement_active: Event = Event()

async def arm_motion(component: Component, direction: int, arm: CooperAndTheArm):
    STEP = 100

    global movement_active

    while True:
        angle = (await arm.dispatch(Command(component, GetAngle())))[0]
        new_angle = max(min(angle + (STEP * direction), 1000), -1000)
        await arm.dispatch(Command(component, SetAngle(new_angle)))
        await asyncio.sleep(0.01)

        if not movement_active.is_set():
            break
        
def define_sockets(socketio: SocketIO, arm: CooperAndTheArm):

    print("Defining sockets...")

    @socketio.on("begin_motion")
    def on_begin_motion(data):
        if not ("component" in data and "direction" in data):
            return
        
        component = component_from_str(data.get('component', ''))
        direction = int(data.get('direction', 0))

        if data and direction:
            direction = 1 if direction > 0 else -1

            global movement_thread, movement_active

            if not movement_active.is_set():
                movement_active.set()
                movement_thread = Thread(target=asyncio.run, args=(arm_motion(component, direction, arm),))
                movement_thread.start()


    @socketio.on("stop_motion")
    def on_stop_motion(data):

        global movement_thread, movement_active
        
        print(movement_thread, movement_active)

        movement_active.clear()
        if movement_thread is not None:
            movement_thread.join()
            movement_thread = None
        

        

    @socketio.on("set")
    def on_set(data):

        print("DATA:", data)

        if not ("value" in data and "component" in data and "option" in data):
            return 

        value: int = int(data['value'])
        component: str = data['component']
        option: str = data['option']

        if value is None or component is None or option is None:
            return
        
        comp = component_from_str(component)

        if comp is None:
            return

        instruction = instruction_from_set_option(option, value)
        
        if instruction is None:
            return
        
        command = Command(comp, instruction)

        asyncio.run(arm.dispatch(command))