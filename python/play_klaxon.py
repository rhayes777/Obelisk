#!/usr/bin/env python

import arduino
import audio_controller
import sys
from time import sleep
import time


arduino1, arduino2 = arduino.get_all()

FLASHING_PERIOD = 60


def play_moment(moment):
    arduino1.set_light_modes(moment[:2])
    arduino2.set_light_modes(moment[-2:])


def play_klaxon(klaxon_name=None):
    if klaxon_name is None:
        klaxon_name = audio_controller.klaxon[int(round(volume * 3))]
    audio_controller.loop_wav_on_new_thread(klaxon_name, no_of_times_to_loop=1)
    
    pattern = [[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]]
    
    moment_no = 0 
    while True:
        play_moment(pattern[moment_no])
        moment_no += 1
        if moment_no > len(pattern) - 1:
            moment_no = 0
        sleep(0.25)
            
            
    
    
if __name__=="__main__":
    if len(sys.argv) > 1:
        play_klaxon(audio_controller.klaxon[int(sys.argv[1])])
    else:
        play_klaxon()
    