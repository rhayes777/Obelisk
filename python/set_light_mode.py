import sys
import arduino


ON = 1
OFF = 0

arduinos = arduino.get_all()

def set_light_mode(light_mode=ON):
    light_mode = str(light_mode)
    for arduino in arduinos:
        arduino.set_light_modes([light_mode, light_mode])
    
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        set_light_mode(sys.argv[1])
    else:
        set_light_mode()