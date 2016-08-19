import main
from play_klaxon import play_klaxon
import set_light_mode
from datetime import datetime


MUSIC_OFF = 0
LIGHTS_OFF = 7
MORNING = 11
AFTERNOON = 14
EVENING = 17
NIGHT = 21


class Action:
    
    def __init__(self, start_hour, end_hour):
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.functions = functions
        
        
    def is_time_within_range(self, time):
        if time.hour > self.start_hour and time.hour < self.end_hour:
            return time.minute > self.start_minute and time.minute < self.end_minute
        return False
        
    def start(self):
        print "Action class is abstract. function 'start' should be overridden"
        assert False
        
        
class LightsOnAction(Action):
    
    def __init__(self):
        super(Action, self).__init__(MUSIC_OFF, LIGHTS_OFF)
        
    def start(self):
        set_light_mode.set_light_mode(set_light_mode.ON)
        
        
class LightsOffAction(Action):
    
    def __init__(self):
        super(Action, self).__init__(LIGHTS_OFF, MORNING)
        
    def start(self):
        set_light_mode.set_light_mode(set_light_mode.OFF)
        

class MorningAction(Action):
    
    def __init__(self):
        super(Action, self).__init__(MORNING, AFTERNOON)
        
    def start(self):
        play_klaxon()
        main.play("morning")
        

class AfternoonAction(Action):
    
    def __init__(self):
        super(Action, self).__init__(AFTERNOON, EVENING)
        
    def start(self):
        play_klaxon()
        main.play("afternoon", should_use_lights=False)
        
        
class EveningAction(Action):
    
    def __init__(self):
        super(Action, self).__init__(EVENING, NIGHT)
        
    def start(self):
        play_klaxon()
        main.play("evening", should_use_lights=True)
        
        
class NightAction(Action):
    
    def __init__(self):
        super(Action, self).__init__(NIGHT, MUSIC_OFF)
        
    def start(self):
        play_klaxon()
        main.play("night", should_use_lights=True)


actions = [LightsOnAction(), LightsOffAction(), MorningAction(), AfternoonAction(), EveningAction(), NightAction()]


def take_action():
    now = datetime.now()
    for action in actions:
        if action.is_time_within_range(now):
            action.start()
            break
            
            
if __name__=="__main__":
    take_action()