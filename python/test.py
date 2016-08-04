import audio_controller
from time import sleep

def wobble_sample():
    audio_controller.loop_wav_on_new_thread(audio_controller.TRACK2_1B, no_of_queues_required=1)
    sleep(1)
    queue = audio_controller.queues[0]
    while True:
        volume = 0
        while volume < 1:
            sleep(0.1)
            print "queueing {}".format(volume)
            queue.put(volume)
            volume += 0.1
        while volume > 0:
            sleep(0.1)
            print "queueing {}".format(volume)
            queue.put(volume)
            volume -= 0.1
    
    
if __name__ == "__main__":
    wobble_sample()