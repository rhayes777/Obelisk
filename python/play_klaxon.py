#!/usr/bin/env python

import audio_controller

def play_klaxon(klaxon_name):
    audio_controller.loop_wav_on_new_thread(klaxon_name, no_of_loops_required=1)
    
    
if __name__=="__main__":
    play_klaxon(audio_controller.KLAXON_MIXDOWN_KLAXON1)