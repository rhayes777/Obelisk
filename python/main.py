import logging
import serial
import ast
import audio_controller
from operator import add

# logging.basicConfig(level=logging.INFO)

# http://playground.arduino.cc/Interfacing/Python

UPPER_LIMIT = 5000
MIDDLE_LIMIT = 1000

SAMPLE_SIZE = 5

INPUT_ARRAY_SIZE = 3

sample_arrays = []
for n in range(0, SAMPLE_SIZE):
    sample_arrays.append(INPUT_ARRAY_SIZE * [2*UPPER_LIMIT])
    
print sample_arrays

actions = {str([0, 0, 0]): audio_controller.ACRO_PAD_C,
           str([1, 0, 0]): audio_controller.WAVEDRIFT_PAD_C,
           str([0, 1, 0]): audio_controller.LODE_PAD,
           str([0, 0, 1]): audio_controller.SPACEBEE_PAD,
           str([1, 1, 0]): audio_controller.SPOOKT_PAD_C,
           str([0, 1, 1]): audio_controller.SYTHEX_PAD,
           str([1, 0, 1]): audio_controller.WAVEDRIFT_PAD_C,
           str([1, 1, 1]): audio_controller.ZPLANE_PAD
           }


def loop():
    previous_result_array = None
    audio_controller.loop_next_wav_by_name(audio_controller.ACRO_PAD_C)
    ser = serial.Serial('/dev/cu.usbmodem1411', 9600)

    while True:
        line = ser.readline().strip()
        input_array = ast.literal_eval(line)
        
        sample_arrays.pop(0)
        sample_arrays.append(input_array)

        average_array = INPUT_ARRAY_SIZE * [0]
        
        print average_array
        print sample_arrays
        
        for sample in sample_arrays:
            print average_array
            print sample
            average_array = map(add, average_array, sample)
            
        average_array = map(lambda item: item / SAMPLE_SIZE, average_array)

        logging.debug("average_array = {}".format(average_array))

        result_array = map(lambda result: 1 if result < UPPER_LIMIT else 0, average_array)

        if result_array != previous_result_array:
            previous_result_array = result_array
            audio_controller.loop_next_wav_by_name(actions[str(result_array)])
             
            

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop()
