#!/usr/bin/env python

import logging

import sys

import audio_controller
from operator import add
import util
from arduino import Arduino

logging.basicConfig(level=logging.DEBUG, filename='main.log')

# http://playground.arduino.cc/Interfacing/Python

MAX_DISTANCE = 300
CLOSE_DISTANCE = 100
TIME_DISTANCE_CONVERSION_FACTOR = 58.138

SAMPLE_SIZE = 5

INPUT_ARRAY_SIZE = 4

NORMALISING_THRESHOLD = 0.01

max_distance_array = INPUT_ARRAY_SIZE * [MAX_DISTANCE]

sample_arrays = []
for n in range(0, SAMPLE_SIZE):
    sample_arrays.append(INPUT_ARRAY_SIZE * [MAX_DISTANCE])

print sample_arrays

afternoon = [
    audio_controller.A_FAR_Master,
    audio_controller.A_NEAR_Master,
    audio_controller.B_FAR_Master,
    audio_controller.B_NEAR_Master,
    audio_controller.C_FAR_Master,
    audio_controller.C_NEAR_Master,
    audio_controller.D_FAR_Master,
    audio_controller.D_NEAR_Master
]

evening = [
    audio_controller.TRACK2_1A,
    audio_controller.TRACK2_1B,
    audio_controller.TRACK2_2A,
    audio_controller.TRACK2_2B,
    audio_controller.TRACK2_3A,
    audio_controller.TRACK2_3B,
    audio_controller.TRACK2_4A,
    audio_controller.TRACK2_4B
]

track_dict = {"afternoon": afternoon,
              "evening": evening}


def milliseconds_to_centimeters(value):
    return value / TIME_DISTANCE_CONVERSION_FACTOR


def milliseconds_to_centimeters_array(array):
    return map(lambda value: milliseconds_to_centimeters(value), array)


def normalise():
    last_sample_array = None
    should_normalise = True
    global max_distance_array
    test_array = INPUT_ARRAY_SIZE * [False]

    while should_normalise:
        new_sample_array = get_input_array()

        if last_sample_array is not None:
            for n in range(0, INPUT_ARRAY_SIZE):
                if not test_array[n]:
                    if abs(new_sample_array[n] - last_sample_array[n]) < NORMALISING_THRESHOLD or (
                                    new_sample_array[n] > MAX_DISTANCE and last_sample_array[n] > MAX_DISTANCE):
                        test_array[n] = True
                        if new_sample_array[n] < MAX_DISTANCE:
                            max_distance_array[n] = new_sample_array[n]

            print test_array
            if not False in test_array:
                should_normalise = False

        last_sample_array = new_sample_array


arduino1 = None
arduino2 = None


def play(track_name="evening"):
    setup(track_name)
    print "starting read loop"
    while True:
        loop()


def setup(track_name):
    audio_samples = track_dict[track_name]

    for n in range(0, 2 * INPUT_ARRAY_SIZE):
        print "Playing {}".format(audio_samples[n])
        audio_controller.loop_wav_on_new_thread(audio_samples[n], INPUT_ARRAY_SIZE)
        
    global arduino1, arduino2
    ports = util.get_arduino_ports()
    arduino1 = Arduino(ports[0])
    arduino2 = Arduino(ports[1])
    
    normalise()


def get_input_array():
    line1 = arduino1.request_array()
    line2 = arduino2.request_array()

    if line1 and line2:
        line1.extend(line2)
        line = line1

        return milliseconds_to_centimeters_array(line)


def loop():

    input_array = get_input_array()
    if input_array:

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
            audio_controller.queues[2 * n].put(volume_near)
            audio_controller.queues[2 * n + 1].put(volume_far)
            volumes[n] = volume_far

        arduino1.set_light_modes_by_volumes(volumes[:2])
        arduino2.set_light_modes_by_volumes(volumes[-2:])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) > 1:
        play(sys.argv[1])
    else:
        play()
