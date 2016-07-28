import logging
import pyaudio
import sys
import wave
from threading import Thread
from time import sleep
import numpy
import struct
from Queue import Queue

# http://playground.arduino.cc/Interfacing/Python

ACRO_PAD_C = "Acro_Pad_C.wav"
ORION_PAD = "Orion_Pad.wav"
LODE_PAD = "Lode_Pad.wav"
SPACEBEE_PAD = "Spacebee_Pad.wav"
SPOOKT_PAD_C = "Spooky_Pad_C.wav"
SYTHEX_PAD = "Synthex_Pad.wav"
WAVEDRIFT_PAD_C = "Wavedrift_Pad_C.wav"
ZPLANE_PAD = "Zplane_Pad.wav"

A_FAR_Master  = "A_FAR_Master.wav"
A_NEAR_Master = "A_NEAR_Master.wav"
B_FAR_Master  = "B_FAR_Master.wav"
B_NEAR_Master = "B_NEAR_Master.wav"
C_FAR_Master  = "C_FAR_Master.wav"
C_NEAR_Master = "C_NEAR_Master.wav"
D_FAR_Master  = "D_FAR_Master.wav"
D_NEAR_Master = "D_NEAR_Master.wav"

TRACK2_1A = "TRACK2_1A.wav"
TRACK2_1B = "TRACK2_1B.wav"
TRACK2_2A = "TRACK2_2A.wav"
TRACK2_2B = "TRACK2_2B.wav"
TRACK2_3A = "TRACK2_3A.wav"
TRACK2_3B = "TRACK2_3B.wav"
TRACK2_4A = "TRACK2_4A.wav"
TRACK2_4B = "TRACK2_4B.wav"

TRACK2_1A_2 = "TRACK2_1A_2.wav"
TRACK2_1B_2 = "TRACK2_1B_2.wav"
TRACK2_2A_2 = "TRACK2_2A_2.wav"
TRACK2_2B_2 = "TRACK2_2B_2.wav"
TRACK2_3A_2 = "TRACK2_3A_2.wav"
TRACK2_3B_2 = "TRACK2_3B_2.wav"
TRACK2_4A_2 = "TRACK2_4A_2.wav"
TRACK2_4B_2 = "TRACK2_4B_2.wav"

KLAXON_MIXDOWN_KLAXON1 = "KLAXON_MIXDOWN_KLAXON1.wav"
KLAXON_MIXDOWN_KLAXON2 = "KLAXON_MIXDOWN_KLAXON2.wav"
KLAXON_MIXDOWN_KLAXON3 = "KLAXON_MIXDOWN_KLAXON3.wav"
KLAXON_MIXDOWN_KLAXON4 = "KLAXON_MIXDOWN_KLAXON4.wav"


# Instantiate PyAudio.
p = pyaudio.PyAudio()
should_play = True
is_sample_tapering = True

queues = []

number_of_ready_loops = 0

CHUNK_SIZE = 1024
VOLUME_DECAY_RATE = 0.15

# logging.basicConfig(level=logging.DEBUG)

class Loop:
    
    def __init__(self, wav_filename, no_of_loops_required, chunk_size=CHUNK_SIZE, volume=1, number_of_times_to_loop=-1):
        self.number_of_times_to_loop = number_of_times_to_loop
        self.wav_filename = wav_filename
        self.chunk_size=chunk_size
        self.volume = volume
        self.no_of_loops_required = no_of_loops_required
        self.queue = Queue()

    def start(self):
        
        global should_play
        global number_of_ready_loops
        
        should_play = True
    
        try:
            self.log('Trying to play file ' + self.wav_filename)
            wf = wave.open("samples/" + self.wav_filename, 'rb')
        except IOError as ioe:
            sys.stderr.write('IOError on file ' + self.wav_filename + '\n' + \
                             str(ioe) + '. Skipping.\n')
            return
        except EOFError as eofe:
            sys.stderr.write('EOFError on file ' + self.wav_filename + '\n' + \
                             str(eofe) + '. Skipping.\n')
            return
    
        self.log("framerate = {}".format(wf.getframerate()))
        self.log("sampwidth = {}".format(wf.getsampwidth()))
        self.log("nchannels = {}".format(wf.getnchannels()))
        
        self.log("opening stream")
    
        # Open stream.
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        self.log("getting data")
        
        data = wf.readframes(self.chunk_size)
        self.log("data got")
        
        loop_number = 0
        
        number_of_ready_loops += 1
        while number_of_ready_loops < self.no_of_loops_required:
            pass
        
        while should_play:
            if not self.queue.empty():
                new_volume = self.queue.get()
                if new_volume >= self.volume:
                    self.volume = new_volume
                else:
                    self.volume -= VOLUME_DECAY_RATE
                    if self.volume < 0:
                        self.volume = 0
                
            arr = self.volume * numpy.fromstring(data, numpy.int16) 
            data = struct.pack('h'*len(arr), *arr)
    
            stream.write(data)
    
            data = wf.readframes(self.chunk_size)
    
            if data == '':  # If file is over then rewind.
                if self.number_of_times_to_loop > 0:
                    loop_number += 1
                    if loop_number == self.number_of_times_to_loop:
                        should_play = False
                    print loop_number
                wf.rewind()
                data = wf.readframes(self.chunk_size)
        
                    
        self.log("sample finished")
    
        # Stop stream.
        self.log("stopping stream")
        stream.stop_stream()
        self.log("closing stream")
        stream.close()
        
    def log(self, message):
        logging.debug("{}: {}".format(self.wav_filename, message))    


def loop_wav_on_new_thread(name, no_of_queues_required=0, no_of_times_to_loop=-1):
    t = Thread(target=loop_wav, args=(name, no_of_queues_required, no_of_times_to_loop, ))
    t.start()
    
def loop_wav(name, no_of_queues_required, no_of_times_to_loop):
    loop = Loop(name, no_of_queues_required, number_of_times_to_loop=no_of_times_to_loop)
    if no_of_queues_required:
        print "appending queue to queues"
        queues.append(loop.queue)
        print "new size = {}".format(len(queues))
    print "starting loop..."
    loop.start()
    

