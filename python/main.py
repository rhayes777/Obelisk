import serial
import ast
import pyaudio
import sys
import wave
from threading import Thread
from time import sleep
import numpy
import struct

# http://playground.arduino.cc/Interfacing/Python

FADE_LENGTH = 500
CHUNK_SIZE = 1024

actions = [([0, 0, 0], "Acro_Pad_C_converted.wav"),
           ([1, 0, 0], "Deepkord_Pad_C_converted.wav"),
           ([0, 1, 0], "Lode_Pad_converted.wav"),
           ([0, 0, 1], "Spacebee_Pad_converted.wav"),
           ([1, 1, 0], "Spooky_Pad_C_converted.wav"),
           ([0, 1, 1], "Synthex_Pad_converted.wav"),
           ([1, 0, 1], "Wavedrift_Pad_C_converted.wav"),
           ([1, 1, 1], "Zplane_Pad_converted.wav")]


class AudioLoop:
    def __init__(self, loop_name, volume=1):
        self.loop_name = loop_name
        self.wf = wave.open(loop_name, 'rb')
        self.stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                             channels=self.wf.getnchannels(),
                             rate=self.wf.getframerate(),
                             output=True)
        self.data = self.wf.readframes(CHUNK_SIZE)
        self.volume = volume
        self.is_playing_continuously = False
        self.is_fading_in = False
        self.is_fading_out = False

    def play_continuously(self):
        self.is_playing_continuously = True
        while self.is_playing_continuously:
            if self.is_fading_in:
                self.volume += 0.1
            if self.is_fading_out:
                self.volume -= 0.1
            if self.volume < 0:
                if self.is_fading_out:
                    self.stop()
            if self.volume > 1:
                self.is_fading_in = False
                self.volume = 1
            arr = self.volume * numpy.fromstring(self.data, numpy.int16)
            data = struct.pack('h' * len(arr), *arr)
            self.stream.write(data)
            data = self.wf.readframes(CHUNK_SIZE)
            if data == '':  # If file is over then rewind.
                self.wf.rewind()
                self.data = self.wf.readframes(CHUNK_SIZE)

    def stop(self):
        # Stop stream.
        self.is_playing_continuously = False
        self.stream.stop_stream()
        self.stream.close()

    def fade_in(self):
        self.is_fading_in = True
        self.is_fading_out = False

    def fade_out(self):
        self.is_fading_in = False
        self.is_fading_out = True


# Instantiate PyAudio.
p = pyaudio.PyAudio()
should_play = False
is_sample_finished = True
current_loop = AudioLoop("Acro_Pad_C_converted.wav")


def loop():
    global current_loop
    loop_wav_on_new_thread("Acro_Pad_C_converted.wav")
    ser = serial.Serial('/dev/cu.usbmodem1411', 9600)

    while True:
        line = ser.readline().strip()
        print line
        arr = ast.literal_eval(line)

        for action in actions:
            if arr == action[0]:
                print "next loop changed"
                next_loop = AudioLoop(action[1], 1)
                Thread(target=next_loop.play_continuously).start()
                next_loop.fade_in()
                current_loop.fade_out()
                current_loop = next_loop
                print next_loop.loop_name


def loop_wav(wav_filename, chunk_size=CHUNK_SIZE):
    global is_sample_finished
    try:
        print 'Trying to play file ' + wav_filename
        wf = wave.open(wav_filename, 'rb')
    except IOError as ioe:
        sys.stderr.write('IOError on file ' + wav_filename + '\n' + \
                         str(ioe) + '. Skipping.\n')
        return
    except EOFError as eofe:
        sys.stderr.write('EOFError on file ' + wav_filename + '\n' + \
                         str(eofe) + '. Skipping.\n')
        return

    # print "framerate = {}".format(wf.getframerate())
    # print "sampwidth = {}".format(wf.getsampwidth())
    # print "nchannels = {}".format(wf.getnchannels())

    # Open stream.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    is_sample_finished = False

    # PLAYBACK LOOP
    data = wf.readframes(CHUNK_SIZE)
    while should_play:
        arr = numpy.fromstring(data, numpy.int16)
        data = struct.pack('h' * len(arr), *arr)
        stream.write(data)
        data = wf.readframes(CHUNK_SIZE)
        if data == '':  # If file is over then rewind.
            wf.rewind()
            data = wf.readframes(CHUNK_SIZE)

    is_sample_finished = True

    # Stop stream.
    stream.stop_stream()
    stream.close()


def loop_wav_on_new_thread(name):
    global should_play
    should_play = False
    while not is_sample_finished:
        sleep(0.01)
    should_play = True

    t = Thread(target=loop_wav, args=(name,))
    t.start()


if __name__ == "__main__":
    loop()
