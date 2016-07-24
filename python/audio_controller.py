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


# Instantiate PyAudio.
p = pyaudio.PyAudio()
should_play = True
is_sample_tapering = True

queues = []


CHUNK_SIZE = 1024

# logging.basicConfig(level=logging.DEBUG)

class Loop:
    
    def __init__(self, wav_filename, chunk_size=CHUNK_SIZE, volume=1):
        self.wav_filename = wav_filename
        self.chunk_size=chunk_size
        self.volume = volume
        self.queue = Queue()

    def start(self):
    
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
        
        while should_play:
            if not self.queue.empty():
                self.volume = self.queue.get()
                
            arr = self.volume * numpy.fromstring(data, numpy.int16) 
            data = struct.pack('h'*len(arr), *arr)
    
            stream.write(data)
    
            data = wf.readframes(self.chunk_size)
    
            if data == '':  # If file is over then rewind.
    
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


def loop_wav_on_new_thread(name):
    t = Thread(target=loop_wav, args=(name,))
    t.start()
    
def loop_wav(name):
    loop = Loop(name)
    print "appending queue to queues"
    queues.append(loop.queue)
    print "new size = {}".format(len(queues))
    loop.start()
    print "loop started"

