from flask import render_template, Flask
from cooperandthearm import CooperAndTheArm
from cooperandthearm.command import Command
from util import COMPONENTS
from cooperandthearm.instruction import GetAngle, GetSpeed
import asyncio

def define_routes(app: Flask, arm: CooperAndTheArm):

    print("Defining routes...")

    @app.route("/")
    def index():
        return render_template("index.html")