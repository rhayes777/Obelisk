import logging
import serial
import ast
import audio_controller
from operator import add

logging.basicConfig(level=logging.INFO)

# http://playground.arduino.cc/Interfacing/Python

UPPER_LIMIT = 2000
MIDDLE_LIMIT = 1000

SAMPLE_SIZE = 10

ACRO_PAD_C = "Acro_Pad_C.wav"
DEEPKORD_PAD_C = "Deepkord_Pad_C.wav"
LODE_PAD = "Lode_Pad.wav"
SPACEBEE_PAD = "Spacebee_Pad_converted.wav"
SPOOKT_PAD_C = "Spooky_Pad_C.wav"
SYTHEX_PAD = "Synthex_Pad.wav"
WAVEDRIFT_PAD_C = "Wavedrift_Pad_C.wav"
ZPLANE_PAD = "Zplane_Pad.wav"

actions = {[0, 0, 0]: audio_controller.ACRO_PAD_C,
           [1, 0, 0]: audio_controller.DEEPKORD_PAD_C,
           [0, 1, 0]: audio_controller.LODE_PAD,
           [0, 0, 1]: audio_controller.SPACEBEE_PAD,
           [1, 1, 0]: audio_controller.SPOOKT_PAD_C,
           [0, 1, 1]: audio_controller.SYTHEX_PAD,
           [1, 0, 1]: audio_controller.WAVEDRIFT_PAD_C,
           [1, 1, 1]: audio_controller.ZPLANE_PAD
           }


def loop():
    previous_result_array = None
    audio_controller.loop_next_wav_by_name(audio_controller.ACRO_PAD_C)
    ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
    while True:
        line = ser.readline().strip()
        logging.debug(line)
        input_array = ast.literal_eval(line)

        current_sample = 0
        sample_array = len(input_array) * [0]
        while current_sample < SAMPLE_SIZE:
            sample_array = map(add, sample_array, input_array)

        average_array = map(lambda total: total / SAMPLE_SIZE, sample_array)
        result_array = map(lambda result: 1 if result < UPPER_LIMIT else 0, average_array)

        if result_array != previous_result_array:
            audio_controller.loop_next_wav_by_name(actions[result_array])


if __name__ == "__main__":
    loop()
