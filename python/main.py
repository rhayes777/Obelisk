#!/usr/bin/env python

import logging

import sys

import audio_controller
from operator import add
import util
import arduino 
import set_light_mode

from time import sleep

##logging.basicConfig(level=logging.DEBUG, filename='main.log')

MAX_DISTANCE = 200
CLOSE_DISTANCE = 100

SAMPLE_SIZE = 5

INPUT_ARRAY_SIZE = 4

NORMALISING_THRESHOLD = 0.01

max_distance_array = INPUT_ARRAY_SIZE * [MAX_DISTANCE]

sample_arrays = []
for n in range(0, SAMPLE_SIZE):
    sample_arrays.append(INPUT_ARRAY_SIZE * [MAX_DISTANCE])

print sample_arrays


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


def play(track_name="evening", default_light_mode=None):
    setup(track_name, default_light_mode)
    logging.info("starting read loop")
    while True:
        loop(default_light_mode)


def setup(track_name, default_light_mode):
    audio_controller.play_track(track_name, INPUT_ARRAY_SIZE)
    global arduino1, arduino2
    arduino1, arduino2 = arduino.get_all()
    if default_light_mode is not None:
        arduino1.set_light_modes([default_light_mode, default_light_mode])
        arduino2.set_light_modes([default_light_mode, default_light_mode])


def get_input_array():
    line1 = arduino1.request_array()
    line2 = arduino2.request_array()

    if line1 and line2:
        line1.extend(line2)
        line = line1

        return util.milliseconds_to_centimeters_array(line)


def loop(default_light_mode):

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

            logging.info("sensor {} at {}".format(n, distance))
            audio_controller.queues[n].put(volume_far)
            volumes[n] = volume_far
        
        if default_light_mode is None:
            arduino1.set_light_modes_by_volumes(volumes[:2])
            arduino2.set_light_modes_by_volumes(volumes[-2:])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        play(sys.argv[1])
    else:
        play()
