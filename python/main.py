import serial
import subprocess
from os import system

# http://playground.arduino.cc/Interfacing/Python

def loop():
    ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
    while True:
        line = ser.readline()
        print line
        if "detected" in line:
            bash_command("python /Users/richardhayes/Desktop/OtherWork/HueScripts/light_control.py random")
        if "ended" in line:
            bash_command("python /Users/richardhayes/Desktop/OtherWork/HueScripts/light_control.py random")
    
def bash_command(string):
    print string
    system(string)

if __name__ == "__main__":
    loop()