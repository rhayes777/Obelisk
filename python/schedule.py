import main
from play_klaxon import play_klaxon
from datetime import datetime
from time import sleep
import logging
import arduino


MUSIC_OFF_LOW = 0
MUSIC_OFF_HIGH = 24
LIGHTS_OFF = 7
MORNING = 11
AFTERNOON = 14
EVENING = 17
NIGHT = 21


class Action(object):
    
    def __init__(self, start_hour, end_hour):
        self.start_hour = start_hour
        self.end_hour = end_hour
        
    def is_time_within_range(self, hour):
        return hour >= self.start_hour and hour < self.end_hour
        
    def start(self):
        print "Action class is abstract. function 'start' should be overridden"
        assert False
        
        
class LightsOnAction(Action):
    
    def __init__(self):
        super(LightsOnAction, self).__init__(MUSIC_OFF_LOW, LIGHTS_OFF)
        
    def start(self):
        logging.info("starting LightsOnAction")
        arduino1, arduino2 = arduino.get_all()
        sleep(0.1)
        arduino1.set_light_modes([1, 1])
        arduino2.set_light_modes([1, 1])
        
        
class LightsOffAction(Action):
    
    def __init__(self):
        super(LightsOffAction, self).__init__(LIGHTS_OFF, MORNING)
        
    def start(self):
        logging.info("starting LightsOffAction")
        arduino1, arduino2 = arduino.get_all()
        sleep(0.1)
        arduino1.set_light_modes([0, 0])
        arduino2.set_light_modes([0, 0])
        

class MorningAction(Action):
    
    def __init__(self):
        super(MorningAction, self).__init__(MORNING, AFTERNOON)
        
    def start(self):
        logging.info("starting MorningAction")
        play_klaxon()
        main.play("morning", default_light_mode=arduino.OFF)
        

class AfternoonAction(Action):
    
    def __init__(self):
        super(AfternoonAction, self).__init__(AFTERNOON, EVENING)
        
    def start(self):
        logging.info("starting AfternoonAction")
        play_klaxon()
        main.play("afternoon", default_light_mode=arduino.OFF)
        
        
class EveningAction(Action):
    
    def __init__(self):
        super(EveningAction, self).__init__(EVENING, NIGHT)
        
    def start(self):
        logging.info("starting EveningAction")
        play_klaxon()
        main.play("evening")
        
        
class NightAction(Action):
    
    def __init__(self):
        super(NightAction, self).__init__(NIGHT, MUSIC_OFF_HIGH)
        
    def start(self):
        logging.info("starting NightAction")
        play_klaxon()
        main.play("night")


actions = [LightsOnAction(), LightsOffAction(), MorningAction(), AfternoonAction(), EveningAction(), NightAction()]


def take_action():
    logging.info('take_action')
    now = datetime.now()
    hour = now.hour
    for action in actions:
        if action.is_time_within_range(hour):
            action.start()
            break
            
            
if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    take_action()
