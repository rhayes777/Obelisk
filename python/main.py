import logging
import serial
import ast
import audio_controller
from operator import add
import util

# logging.basicConfig(level=logging.INFO)

# http://playground.arduino.cc/Interfacing/Python

MAX_DISTANCE = 200
CLOSE_DISTANCE = 100
TIME_DISTANCE_CONVERSION_FACTOR = 58.138

SAMPLE_SIZE = 100

INPUT_ARRAY_SIZE = 3

sample_arrays = []
for n in range(0, SAMPLE_SIZE):
    sample_arrays.append(INPUT_ARRAY_SIZE * [MAX_DISTANCE])
    
print sample_arrays

           
audio_samples = [
                    audio_controller.A_FAR_Master,
                    audio_controller.A_NEAR_Master,
                    audio_controller.B_FAR_Master,
                    audio_controller.B_NEAR_Master,
                    audio_controller.C_FAR_Master,
                    audio_controller.C_NEAR_Master,
                    audio_controller.D_FAR_Master,
                    audio_controller.D_NEAR_Master
                    ]


def loop():
    previous_result_array = INPUT_ARRAY_SIZE * [0]
    ser = serial.Serial(util.get_arduino_port(), 9600)
    
    for n in range(0, 2 * INPUT_ARRAY_SIZE):
        print "Playing {}".format(audio_samples[n])
        audio_controller.loop_wav_on_new_thread(audio_samples[n])

    while True:
        line = ser.readline().strip()
        input_array = ast.literal_eval(line)
        print input_array
        
        sample_arrays.pop(0)
        sample_arrays.append(input_array)

        average_array = INPUT_ARRAY_SIZE * [0]
        
        for sample in sample_arrays:
            average_array = map(add, average_array, sample)
            
        average_array = map(lambda value: value / (SAMPLE_SIZE * TIME_DISTANCE_CONVERSION_FACTOR) , average_array)

        logging.debug("average_array = {}".format(average_array))

        for n in range(0, INPUT_ARRAY_SIZE):
            distance = average_array[n]
            if distance < 0:
                distance = 0
            if distance > MAX_DISTANCE:
                distance = MAX_DISTANCE
            volume_far = 1 - distance / MAX_DISTANCE
            volume_near = 0
            if distance < CLOSE_DISTANCE:
                volume_near = 1 - distance / CLOSE_DISTANCE
            print "sensor {} at {}".format(n, distance)
            audio_controller.queues[n].put(volume_near)
            audio_controller.queues[n + INPUT_ARRAY_SIZE].put(volume_far)

             
            
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop()
