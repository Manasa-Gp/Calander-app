
from datetime import datetime;

class Event:
    def __init__(self,title,start_time,end_time):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
    def eventOverlap(self,other_event):
        if other_event.start_time >= self.end_time: # event 2 starts when event 1 ends
            return False
        elif other_event.end_time <= self.start_time:  # event 2 ends before event 1 starts 
            return False
        return True
    def to_dict(self):
         return {
        "title": self.title,
        "start_time": self.start_time.strftime("%m-%d-%Y %I:%M %p"),
        "end_time": self.end_time.strftime("%m-%d-%Y %I:%M %p")
            }
    @staticmethod
    def from_dict(event):
        return Event(
            event["title"],
            datetime.strptime(event["start_time"], "%m-%d-%Y %I:%M %p"),
            datetime.strptime(event["end_time"], "%m-%d-%Y %I:%M %p")
        )