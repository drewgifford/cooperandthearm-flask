from flask import Flask
from cooperandthearm import CooperAndTheArm, Component
from cooperandthearm.command import Command
from cooperandthearm.instruction import SetSpeed, SetAngle, Instruction, GetAngle
from flask_socketio import SocketIO
from dispatcher import ArmDispatcher
import asyncio

movement_task: asyncio.Task = None
movement_active = asyncio.Event()

def component_from_str(component: str) -> Component:
    if component == "base":
        return Component.BASE
    elif component == "shoulder":
        return Component.SHOULDER
    elif component == "elbow":
        return Component.ELBOW
    elif component == "claw":
        return Component.CLAW
    
    return None

def instruction_from_set_option(set_option: str, value: int) -> Instruction | None:
    if set_option == "angle":
        return SetAngle(value)
    elif set_option == "speed":
        return SetSpeed(value)
    
    return None
        
def define_sockets(socketio: SocketIO, dispatcher: ArmDispatcher):

    def arm_motion(component: Component, direction: int):
        STEP = 100
        while movement_active.is_set():
            angle = (dispatcher.dispatch_sync(Command(component, GetAngle())))[0]
            new_angle = max(min(angle + (STEP * direction), 1000), -1000)
            dispatcher.dispatch_sync(Command(component, SetAngle(new_angle)))
            await asyncio.sleep(0.01)


    @socketio.on("begin_motion")
    def on_begin_motion(data):
        if not ("component" in data and "direction" in data):
            return
        
        component = component_from_str(data.get('component', ''))
        direction = int(data.get('direction', 0))

        if data and direction:
            direction = 1 if direction > 0 else -1

            if not movement_active.is_set():
                movement_active.set()

                arm_motion(component, direction)


    @socketio.on("stop_motion")
    def on_stop_motion(data):
        movement_active.clear()

    @socketio.on("set")
    async def on_set(data):

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

        await dispatcher.dispatch(command)
