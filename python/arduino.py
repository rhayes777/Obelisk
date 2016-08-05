import serial
import ast
import logging
import time
import math

MEASUREMENT_PAUSE = 0.1  # s

# logging.basicConfig(level=logging.DEBUG)

class Arduino:
    
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(port, 9600)
        self.write("-1")
        self.light_modes = [0, 0]
        
    def write(self, message):
        self.ser.write(message)
        
    def read(self):
        bytes_to_read = self.in_waiting()
        result = self.ser.read(bytes_to_read)
        if "[" in result:
            while not "]" in result:
                next = self.ser.read(self.in_waiting())
                if len(next):
                    result += next
            return result
        return None
        
    def read_array(self):
        string = self.read()
        if not string:
            return None
        arr = string.split("\n")
        string = arr[0]
        if "[" in string and "]" in string:
##            print string
            try:
                arr = ast.literal_eval(string)
                if isinstance(arr, list):
                    return arr 
            except Exception as e:
                print e
        return None
        
    def read_next_array(self):
        array = None
        while not array:
            array = self.read_array()
        return array
        
    def in_waiting(self):
        return self.ser.inWaiting()
        
    def request_array(self):
        logging.debug("requesting from port {}".format(self.port))
        array = None
        while not array:
            self.write("-1")
            time.sleep(MEASUREMENT_PAUSE)
            array = self.read_array()
        return array
        
    def set_light_modes(self, light_modes):
        self.light_modes = light_modes
        to_write = "".join(str(light_mode) for light_mode in self.light_modes) 
        self.write(to_write)
        logging.debug("Writing light modes {} to {}".format(to_write, self.port))
        
    def set_light_modes_by_volumes(self, volumes):
        self.set_light_modes(map(lambda volume: int(round(volume * 9)), volumes))
        
