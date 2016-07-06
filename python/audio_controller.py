import logging
import pyaudio
import sys
import wave
from threading import Thread
from time import sleep
import numpy
import struct

# http://playground.arduino.cc/Interfacing/Python

ACRO_PAD_C = "Acro_Pad_C.wav"
ORION_PAD = "Orion_Pad.wav"
LODE_PAD = "Lode_Pad.wav"
SPACEBEE_PAD = "Spacebee_Pad.wav"
SPOOKT_PAD_C = "Spooky_Pad_C.wav"
SYTHEX_PAD = "Synthex_Pad.wav"
WAVEDRIFT_PAD_C = "Wavedrift_Pad_C.wav"
ZPLANE_PAD = "Zplane_Pad.wav"


# Instantiate PyAudio.
p = pyaudio.PyAudio()
should_play = True
is_sample_tapering = True


CHUNK_SIZE = 1024

class loop:
    
    def __init__(self, wav_filename, chunk_size=CHUNK_SIZE, volume=0.0):
        self.wav_filename = wav_filename
        self.chunk_size=chunk_size
        self.volume = volume
        self.queue = Queue()

    def start():
    
        try:
            logging.info('Trying to play file ' + self.wav_filename)
            wf = wave.open("samples/" + self.wav_filename, 'rb')
        except IOError as ioe:
            sys.stderr.write('IOError on file ' + self.wav_filename + '\n' + \
                             str(ioe) + '. Skipping.\n')
            return
        except EOFError as eofe:
            sys.stderr.write('EOFError on file ' + self.wav_filename + '\n' + \
                             str(eofe) + '. Skipping.\n')
            return
    
        logging.debug("framerate = {}".format(wf.getframerate()))
        logging.debug("sampwidth = {}".format(wf.getsampwidth()))
        logging.debug("nchannels = {}".format(wf.getnchannels()))
        
        logging.debug("opening stream")
    
        # Open stream.
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        logging.debug("getting data")
        
        data = wf.readframes(self.chunk_size)
            
        
        while should_play:
            arr = self.volume * numpy.fromstring(data, numpy.int16) 
            data = struct.pack('h'*len(arr), *arr)
    
            stream.write(data)
    
            data = wf.readframes(self.chunk_size)
    
            if data == '':  # If file is over then rewind.
    
                wf.rewind()
                data = wf.readframes(chunk_size)
        
                    
        logging.debug("sample finished")
    
        # Stop stream.
        logging.debug("stopping stream")
        stream.stop_stream()
        logging.debug("closing stream")
        stream.close()


def loop_wav_on_new_thread(name):
    t = Thread(target=loop_wav, args=(name,))
    t.start()
    
def loop_wav(name):
    loop = loop(name)
    loop.start()
