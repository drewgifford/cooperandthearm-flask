from cooperandthearm import BASE, SHOULDER, ELBOW, CLAW, Component, SetAngle, SetSpeed
from cooperandthearm.instruction import Instruction

COMPONENTS = [BASE, SHOULDER]

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