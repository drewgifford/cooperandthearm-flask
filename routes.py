from flask import render_template, Flask
from cooperandthearm import CooperAndTheArm
from cooperandthearm.command import Command
from util import COMPONENTS
from cooperandthearm.instruction import GetAngle, GetSpeed
from dispatcher import ArmDispatcher
import asyncio

def define_routes(app: Flask, dispatcher: ArmDispatcher):


    @app.route("/")
    def index():
        return render_template("index.html")
    
    @app.get("/read")
    async def read():
        data = {}
        for component in COMPONENTS:
            angle, speed = await dispatcher.dispatch(component, GetAngle()), Command(component, GetSpeed())

            data[component.name.lower()] = {
                'angle': angle,
                'speed': speed
            }

        return data