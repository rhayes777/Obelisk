import main
from play_klaxon import play_klaxon
import set_light_mode
from datetime import datetime
import logging


MUSIC_OFF = 0
LIGHTS_OFF = 7
MORNING = 11
AFTERNOON = 14
EVENING = 17
NIGHT = 21


class Action(object):
    
    def __init__(self, start_hour, end_hour):
        self.start_hour = start_hour
        self.end_hour = end_hour
        
    def is_time_within_range(self, time):
        return time.hour > self.start_hour and time.hour < self.end_hour
        
    def start(self):
        print "Action class is abstract. function 'start' should be overridden"
        assert False
        
        
class LightsOnAction(Action):
    
    def __init__(self):
        super(LightsOnAction, self).__init__(MUSIC_OFF, LIGHTS_OFF)
        
    def start(self):
        set_light_mode.set_light_mode(set_light_mode.ON)
        
        
class LightsOffAction(Action):
    
    def __init__(self):
        super(LightsOffAction, self).__init__(LIGHTS_OFF, MORNING)
        
    def start(self):
        set_light_mode.set_light_mode(set_light_mode.OFF)
        

class MorningAction(Action):
    
    def __init__(self):
        super(MorningAction, self).__init__(MORNING, AFTERNOON)
        
    def start(self):
        play_klaxon()
        main.play("morning", default_light_mode=set_light_mode.OFF)
        

class AfternoonAction(Action):
    
    def __init__(self):
        super(AfternoonAction, self).__init__(AFTERNOON, EVENING)
        
    def start(self):
        play_klaxon()
        main.play("afternoon", default_light_mode=set_light_mode.OFF)
        
        
class EveningAction(Action):
    
    def __init__(self):
        super(EveningAction, self).__init__(EVENING, NIGHT)
        
    def start(self):
        play_klaxon()
        main.play("evening")
        
        
class NightAction(Action):
    
    def __init__(self):
        super(NightAction, self).__init__(NIGHT, MUSIC_OFF)
        
    def start(self):
        play_klaxon()
        main.play("night")


actions = [LightsOnAction(), LightsOffAction(), MorningAction(), AfternoonAction(), EveningAction(), NightAction()]


def take_action():
    now = datetime.now()
    for action in actions:
        if action.is_time_within_range(now):
            action.start()
            break
            
            
if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    take_action()