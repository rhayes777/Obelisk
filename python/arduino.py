import serial
import ast

class Arduino:
    
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600)
        self.write("1")
        
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
        string = string.split("\n")[0]
        if "[" in string and "]" in string:
            return ast.literal_eval(string)
        return None
        
    def read_next_array(self):
        array = None
        while not array:
            array = self.read_array()
        return array
        
    def in_waiting(self):
        return self.ser.inWaiting()
        
    def has_waiting(self):
        return self.in_waiting() > 0
        
    def request_array(self):
        array = None
        while not array: 
           self.write("1")
           array = self.read_array()
        return array