import serial
import subprocess
from os import system

# http://playground.arduino.cc/Interfacing/Python

def loop():
    ser = serial.Serial('/dev/cu.usbmodem1411', 9600)
    while True:
        line = ser.readline()
        print line
#         print type(line)
#         if "First" in line:
#             
#         if "Second" in line:
            
    
def bash_command(string):
    print string
    system(string)

if __name__ == "__main__":
    loop()