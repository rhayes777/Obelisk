#!/usr/bin/env python

import logging

import audio_controller
from operator import add
import util
from arduino import Arduino

# logging.basicConfig(level=logging.INFO)

# http://playground.arduino.cc/Interfacing/Python

MAX_DISTANCE = 300
CLOSE_DISTANCE = 100
TIME_DISTANCE_CONVERSION_FACTOR = 58.138

SAMPLE_SIZE = 5

INPUT_ARRAY_SIZE = 4

NORMALISING_THRESHOLD = 0.01

test_array = INPUT_ARRAY_SIZE * [False]

max_distance_array = INPUT_ARRAY_SIZE * [MAX_DISTANCE]

sample_arrays = []
for n in range(0, SAMPLE_SIZE):
    sample_arrays.append(INPUT_ARRAY_SIZE * [MAX_DISTANCE])

print sample_arrays

# audio_samples = [
#     audio_controller.A_FAR_Master,
#     audio_controller.A_NEAR_Master,
#     audio_controller.B_FAR_Master,
#     audio_controller.B_NEAR_Master,
#     audio_controller.C_FAR_Master,
#     audio_controller.C_NEAR_Master,
#     audio_controller.D_FAR_Master,
#     audio_controller.D_NEAR_Master
# ]

audio_samples = [
    audio_controller.TRACK2_1A,
    audio_controller.TRACK2_1B,
    audio_controller.TRACK2_2A,
    audio_controller.TRACK2_2B,
    audio_controller.TRACK2_3A,
    audio_controller.TRACK2_3B,
    audio_controller.TRACK2_4A,
    audio_controller.TRACK2_4B
]

# audio_samples = [
#     audio_controller.TRACK2_1A_2,
#     audio_controller.TRACK2_1B_2,
#     audio_controller.TRACK2_2A_2,
#     audio_controller.TRACK2_2B_2,
#     audio_controller.TRACK2_3A_2,
#     audio_controller.TRACK2_3B_2,
#     audio_controller.TRACK2_4A_2,
#     audio_controller.TRACK2_4B_2
# ]

last_sample_array = None
should_normalise = True


def milliseconds_to_meters(value):
    return value / TIME_DISTANCE_CONVERSION_FACTOR


def milliseconds_to_meters_array(array):
    return map(lambda value: milliseconds_to_meters(value), array)


def normalise(new_sample_array):
    global last_sample_array
    global should_normalise
    global max_distance_array
    global test_array

    if last_sample_array is not None:
        for n in range(0, INPUT_ARRAY_SIZE):
            if not test_array[n]:
                if abs(new_sample_array[n] - last_sample_array[n]) < NORMALISING_THRESHOLD or (new_sample_array[n] > MAX_DISTANCE and last_sample_array[n] > MAX_DISTANCE):
                    test_array[n] = True
                    if new_sample_array[n] < MAX_DISTANCE:
                        max_distance_array[n] = new_sample_array[n]
                    
        print test_array
        if not False in test_array:
            should_normalise = False

    last_sample_array = new_sample_array


def loop():
    ports = util.get_arduino_ports()
    arduino1 = Arduino(ports[0])
    arduino2 = Arduino(ports[1])

    for n in range(0, 2 * INPUT_ARRAY_SIZE):
        print "Playing {}".format(audio_samples[n])
        audio_controller.loop_wav_on_new_thread(audio_samples[n], INPUT_ARRAY_SIZE)
        

    print "starting read loop"
    while True:
        
        line1 = arduino1.request_array()
        line2 = arduino2.request_array()

        if line1 and line2:
            line1.extend(line2)
            line = line1
    
            input_array = milliseconds_to_meters_array(line)
    
            if should_normalise:
                logging.info("normalising")
                normalise(input_array)
                continue
    
            sample_arrays.pop(0)
            sample_arrays.append(input_array)
    
            average_array = INPUT_ARRAY_SIZE * [0]
    
            for sample in sample_arrays:
                average_array = map(add, average_array, sample)
    
            average_array = map(lambda value: value / SAMPLE_SIZE, average_array)
    
            logging.debug("average_array = {}".format(average_array))
            
            volumes = INPUT_ARRAY_SIZE * [0]
    
            for n in range(0, INPUT_ARRAY_SIZE):
                max_distance = max_distance_array[n]
                distance = average_array[n]
                if distance < 0:
                    distance = 0
                if distance > max_distance:
                    distance = max_distance
                volume_far = 1 - distance / max_distance
                volume_near = 0
                if distance < CLOSE_DISTANCE:
                    volume_near = 1 - distance / CLOSE_DISTANCE
                logging.info("sensor {} at {}".format(n, distance))
                audio_controller.queues[2 * n].put(volume_far)
                audio_controller.queues[2 * n + 1].put(volume_far)
                volumes[n] = volume_far
            
            arduino1.set_light_modes_by_volumes(volumes[:2])
            arduino2.set_light_modes_by_volumes(volumes[-2:])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop()
# audio_controller.loop_wav_on_new_thread("A_FAR_Master_converted.wav")
