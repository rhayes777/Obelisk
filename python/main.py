import serial
from os import system
import ast
import pyaudio
import sys
import wave
from threading import Thread
from time import sleep

# http://playground.arduino.cc/Interfacing/Python

actions = [([0, 0, 0], "Acro_Pad_C_converted.wav"),
           ([1, 0, 0], "Deepkord_Pad_C_converted.wav"),
           ([0, 1, 0], "Lode_Pad_converted.wav"),
           ([0, 0, 1], "Spacebee_Pad_converted.wav"),
           ([1, 1, 0], "Spooky_Pad_C_converted.wav"),
           ([0, 1, 1], "Synthex_Pad_converted.wav"),
           ([1, 0, 1], "Wavedrift_Pad_C_converted.wav"),
           ([1, 1, 1], "Zplane_Pad_converted.wav")]

# Instantiate PyAudio.
p = pyaudio.PyAudio()
should_play = False
is_sample_finished = True


def loop():
    loop_wav_on_new_thread("Acro_Pad_C_converted.wav")
    ser = serial.Serial('/dev/cu.usbmodem1411', 9600)
    while True:
        line = ser.readline().strip()
        print line
        arr = ast.literal_eval(line)

        for action in actions:
            if arr == action[0]:
                loop_wav_on_new_thread(action[1])


CHUNK_SIZE = 1024


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


    # Open stream.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    is_sample_finished = False

    # PLAYBACK LOOP
    data = wf.readframes(CHUNK_SIZE)
    while should_play:
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

