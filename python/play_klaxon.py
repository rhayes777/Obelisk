#!/usr/bin/env python

import audio_controller
import sys

def play_klaxon(klaxon_name=audio_controller.KLAXON_MIXDOWN_KLAXON1):
    audio_controller.loop_wav_on_new_thread(klaxon_name, no_of_times_to_loop=1)
    
    
if __name__=="__main__":
    if len(sys.argv) > 1:
        play_klaxon(audio_controller.klaxon[int(sys.argv[1])])
    else:
        play_klaxon()
    