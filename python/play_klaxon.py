#!/usr/bin/env python

import arduino
import audio_controller
import sys
from time import sleep
import time
from random import randint


arduino1, arduino2 = arduino.get_all()

FLASHING_PERIOD = 60

patterns = [[
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
            ],
            [
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
            ],
            [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 0, 1],
            [0, 0, 1, 1],
            [1, 0, 1, 1],
            [0, 1, 1, 1],
            [1, 1, 1, 1]
            ]]


def play_moment(moment):
    arduino1.set_light_modes(moment[:2])
    arduino2.set_light_modes(moment[-2:])


def play_klaxon(klaxon_name=None):
    if klaxon_name is None:
        klaxon_name = audio_controller.klaxon[randint(0,3)]
    audio_controller.loop_wav_on_new_thread(klaxon_name, no_of_times_to_loop=1)
    
    pattern = patterns[randint(0, len(patterns) - 1)]
    
    moment_no = 0 
    start = time.time()
    seconds_elapsed = 0
    while seconds_elapsed < FLASHING_PERIOD:
        play_moment(pattern[moment_no])
        moment_no += 1
        if moment_no > len(pattern) - 1:
            moment_no = 0
        sleep(0.25)
        seconds_elapsed = time.time() - start
    
    arduino1.ser.close()    
    arduino2.ser.close()

    
if __name__=="__main__":
    if len(sys.argv) > 1:
        play_klaxon(audio_controller.klaxon[int(sys.argv[1])])
    else:
        play_klaxon()
    