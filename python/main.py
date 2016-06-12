import serial
from os import system
import ast
import pyaudio
import sys
import wave
from threading import Thread

# http://playground.arduino.cc/Interfacing/Python

actions = [([0, 0, 0], "Roland-GR-1-12-String-Guitar-C4.wav"), 
([1, 0, 0], "Alesis-S4-Plus-Piccolo-C5.wav"), 
([0, 1, 0], "Casio-CZ-5000-Human-Voice-C4.wav"), 
([0, 0, 1], "Casio-CZ-5000-Synth-Bass-C1.wav"), 
([1, 1, 0], "Crash-Cymbal-1.wav"), 
([0, 1, 1], "Cuica-1.wav"),
([1, 0, 1], "E-Mu-Proteus-2-Tubular-Bell-C5.wav"), 
([1, 1, 1], "Alesis-S4-Plus-Calliope-C4.wav")]

# Instantiate PyAudio.
p = pyaudio.PyAudio()


def loop():
    ser = serial.Serial('/dev/cu.usbmodem1411', 9600)
    while True:
        line = ser.readline().strip()
        print line
        arr = ast.literal_eval(line)
        
        for action in actions:
            if arr == action[0]:

                t = Thread(target=play_wav, args=(action[1],))
                t.start()
                t.join()
                print "thread finished...exiting"

#                 play_wav(action[1])

CHUNK_SIZE = 1024


def play_wav(wav_filename, chunk_size=CHUNK_SIZE):

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

    data = wf.readframes(chunk_size)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Stop stream.
    stream.stop_stream()
    stream.close()

    # # Close PyAudio.
    # p.terminate()
    
    
def bash_command(string):
    print string
    system(string)

if __name__ == "__main__":
    loop()
#     play_wav("Roland-GR-1-12-String-Guitar-C4.wav")