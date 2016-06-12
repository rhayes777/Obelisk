import serial
import subprocess
from os import system
import ast

# http://playground.arduino.cc/Interfacing/Python

def loop():
    ser = serial.Serial('/dev/cu.usbmodem1411', 9600)
    while True:
        line = ser.readline().strip()
        print line
        arr = ast.literal_eval(line)
        
        for val in arr:
            print val
#         print type(line)
#         if "First" in line:
#             
#         if "Second" in line:
            
    
def bash_command(string):
    print string
    system(string)

if __name__ == "__main__":
    loop()