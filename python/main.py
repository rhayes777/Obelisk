import logging
import serial
import ast
import audio_controller
from operator import add
import util

# logging.basicConfig(level=logging.INFO)

# http://playground.arduino.cc/Interfacing/Python

MAX_DISTANCE = 300
CLOSE_DISTANCE = 100
TIME_DISTANCE_CONVERSION_FACTOR = 58.138

SAMPLE_SIZE = 100

INPUT_ARRAY_SIZE = 2

NORMALISING_THRESHOLD = 0.1

max_distance_array = INPUT_ARRAY_SIZE * [MAX_DISTANCE]

sample_arrays = []
for n in range(0, SAMPLE_SIZE):
    sample_arrays.append(INPUT_ARRAY_SIZE * [MAX_DISTANCE])

print sample_arrays

audio_samples = [
    audio_controller.A_FAR_Master,
    audio_controller.A_NEAR_Master,
    audio_controller.B_FAR_Master,
    audio_controller.B_NEAR_Master,
    audio_controller.C_FAR_Master,
    audio_controller.C_NEAR_Master,
    audio_controller.D_FAR_Master,
    audio_controller.D_NEAR_Master
]

last_sample_array = None
should_normalise = True


def milliseconds_to_meters(value):
    return value / TIME_DISTANCE_CONVERSION_FACTOR


def milliseconds_to_meters_array(array):
    return map(lambda value: milliseconds_to_meters(value), array)


def normalise(new_sample_array):
    global last_sample_array
    global should_normalise
    global max_distance_array

    if last_sample_array is not None:
        test_array = [abs(new_sample - last_sample) < NORMALISING_THRESHOLD for new_sample, last_sample in
                      zip(new_sample_array, last_sample_array)]
        print test_array
        if not False in test_array:
            for n in range(0, len(new_sample_array)):
                if new_sample_array[n] < MAX_DISTANCE:
                    max_distance_array[n] = new_sample_array[n]

            should_normalise = False

    last_sample_array = new_sample_array
    logging.info("normalised")


def loop():
    ser = serial.Serial(util.get_arduino_port(), 9600)

    for n in range(0, 2 * INPUT_ARRAY_SIZE):
        print "Playing {}".format(audio_samples[n])
        audio_controller.loop_wav_on_new_thread(audio_samples[n])

    while True:
        line = ser.readline().strip()
        input_array = milliseconds_to_meters_array(ast.literal_eval(line))

        if should_normalise:
            logging.info("normalising")
            normalise(input_array)
            continue

        sample_arrays.pop(0)
        sample_arrays.append(input_array)

        average_array = INPUT_ARRAY_SIZE * [0]

        for sample in sample_arrays:
            average_array = map(add, average_array, sample)

        average_array = map(lambda value: value / SAMPLE_SIZE, average_array)

        logging.debug("average_array = {}".format(average_array))

        for n in range(0, INPUT_ARRAY_SIZE):
            max_distance = max_distance_array[n]
            distance = average_array[n]
            if distance < 0:
                distance = 0
            if distance > max_distance:
                distance = max_distance
            volume_far = 1 - distance / max_distance
            volume_near = 0
            if distance < CLOSE_DISTANCE:
                volume_near = 1 - distance / CLOSE_DISTANCE
            logging.info("sensor {} at {}".format(n, distance))
            audio_controller.queues[2 * n].put(volume_near)
            audio_controller.queues[2 * n + 1].put(volume_far)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop()
# audio_controller.loop_wav_on_new_thread("A_FAR_Master_converted.wav")
