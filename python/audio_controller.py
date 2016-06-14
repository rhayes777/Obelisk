import logging
import pyaudio
import sys
import wave
from threading import Thread
from time import sleep

logging.basicConfig(level=logging.INFO)

# http://playground.arduino.cc/Interfacing/Python

ACRO_PAD_C = "Acro_Pad_C.wav"
DEEPKORD_PAD_C = "Deepkord_Pad_C.wav"
LODE_PAD = "Lode_Pad.wav"
SPACEBEE_PAD = "Spacebee_Pad_converted.wav"
SPOOKT_PAD_C = "Spooky_Pad_C.wav"
SYTHEX_PAD = "Synthex_Pad.wav"
WAVEDRIFT_PAD_C = "Wavedrift_Pad_C.wav"
ZPLANE_PAD = "Zplane_Pad.wav"


# Instantiate PyAudio.
p = pyaudio.PyAudio()
should_play = True
is_sample_finished = True


CHUNK_SIZE = 1024


def loop_wav(wav_filename, chunk_size=CHUNK_SIZE):
    global is_sample_finished

    try:
        logging.info('Trying to play file ' + wav_filename)
        wf = wave.open("samples/" + wav_filename, 'rb')
    except IOError as ioe:
        sys.stderr.write('IOError on file ' + wav_filename + '\n' + \
                         str(ioe) + '. Skipping.\n')
        return
    except EOFError as eofe:
        sys.stderr.write('EOFError on file ' + wav_filename + '\n' + \
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

    is_sample_finished = False
    
    logging.debug("getting data")

    # PLAYBACK LOOP
    data = wf.readframes(CHUNK_SIZE)
    while should_play:
        logging.debug("playing")
        stream.write(data)
        logging.debug("data written")
        data = wf.readframes(CHUNK_SIZE)
        logging.debug("data read")
        if data == '':  # If file is over then rewind.
            logging.debug("rewinding")
            wf.rewind()
            data = wf.readframes(CHUNK_SIZE)
        
    logging.debug("sample finished")

    is_sample_finished = True

    # Stop stream.
    logging.debug("stopping stream")
    stream.stop_stream()
    logging.debug("closing stream")
    stream.close()


def loop_next_wav_by_name(name):
    global should_play
    should_play = False
    while not is_sample_finished:
        sleep(0.01)
    should_play = True

    t = Thread(target=loop_wav, args=(name,))
    t.start()
