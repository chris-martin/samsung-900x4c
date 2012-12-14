#!/usr/bin/python

import re
from subprocess import Popen, PIPE
from sys import argv

def run(*args):
    pipe = Popen(args, stdout=PIPE)
    return pipe.communicate()[0]

def mix(action, item = "Master"):
    run("amixer", "set", item, action)

def sound_off():
    mix(action = "mute")

def sound_on():
    for item in ["Master", "Headphone", "Speaker"]:
        mix(action = "unmute", item = item)

def sound_status():
    return re.findall(
        "\[([^\]]+)\]$", 
        run("amixer", "get", "Master")
    )[0].strip()

def print_sound_status():
    print(sound_status())

def sound_toggle():
    s = sound_status()
    { "on": sound_off, "off": sound_on }[s]()

def sound_up():
    sound_on()
    mix(action = "5+")

def sound_down():
    mix(action = "5-")

functions = { 
    "up": sound_up,  
    "down": sound_down,
    "off": sound_off, 
    "on": sound_on,
    "toggle": sound_toggle,
    "status": print_sound_status,
}

if __name__ == "__main__":
    arg = None
    if len(argv) == 2:
        arg = argv[1]
    if arg not in functions:
        arg = None
    if arg:
        functions[argv[1]]()
    else:
        print("Usage: sound [up|down|off|on|toggle|status]")

