import sys
import Arduino


arduinos = Arduino.get_all()

def set_light_mode(light_mode="1"):
    for arduino in arduinos:
        arduino.set_light_modes([light_mode, light_mode])
    
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        set_light_mode(sys.argv[1])
    else:
        set_light_mode()