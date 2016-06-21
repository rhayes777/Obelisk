import logging
import serial
import ast
import audio_controller
from operator import add

# logging.basicConfig(level=logging.INFO)

# http://playground.arduino.cc/Interfacing/Python

UPPER_LIMIT = 5000
MIDDLE_LIMIT = 1000

SAMPLE_SIZE = 1

INPUT_ARRAY_SIZE = 3

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

    current_sample = 0
    sample_array = INPUT_ARRAY_SIZE * [0]
    min_array = INPUT_ARRAY_SIZE * [10 * UPPER_LIMIT]

    while True:
        line = ser.readline().strip()
        input_array = ast.literal_eval(line)
#         logging.debug("input_array = {}".format(input_array))



        if current_sample < SAMPLE_SIZE:
            sample_array = map(add, sample_array, input_array)
#             for n in range(0, INPUT_ARRAY_SIZE):
#                 if sample_array[n] < min_array[n]:
#                     min_array[n] = sample_array[n]
            current_sample += 1
            print sample_array
        else:

            average_array = map(lambda total: total / SAMPLE_SIZE, sample_array)

            logging.debug("average_array = {}".format(average_array))

            result_array = map(lambda result: 1 if result < UPPER_LIMIT else 0, min_array)

            if result_array != previous_result_array:
                previous_result_array = result_array
                audio_controller.loop_next_wav_by_name(actions[str(result_array)])
                
            current_sample = 0
            sample_array = INPUT_ARRAY_SIZE * [0]
            min_array = INPUT_ARRAY_SIZE * [10 * UPPER_LIMIT]   
            

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop()
