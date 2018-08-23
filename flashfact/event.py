import threading
import queue
from time import sleep

import timefunc

class Event(threading.Thread):
    def __init__(self, event_td=None, seconds_left=None, callback=None ):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        if seconds_left:
            self.seconds_left = seconds_left
        elif event_td:
            self.seconds_left = (event_td - datetime.datetime.now()).total_seconds()
            
            
        print( "event in", self.seconds_left, "seconds")
        
    def run(self):
        
        while 1:
            t = threading.Timer(2, self.process, {'results':self.queue})
            t.start()
            if self._stop:
                break
            sleep(1)
        
    def stop(self):
        self._stop = True
    
    def add_timed_event(self, delay, callback, reoccur=False, *args, **kwargs):
        threading.Timer( delay, callback, args, kwargs) 
    
    def process(self, *args, **kwargs):
        kwargs['results'].push("my result")
        print("processing..", args, kwargs)
        
        

    
class Scheduler(threading.Thread):

    def __init__(self, event_td=None, seconds_left=None, callback=None, mainantance_period=5, debug=False ):
        threading.Thread.__init__(self)
        self.schedules = []
        self.history = []
        self._maint_period = mainantance_period
        self.debug = True
        
        self._maint()
        
        
    def run(self):
        while 1:
            sleep(1)
            for s in schedules:
                print(s.threadName)
    
    # TODO: change maint from timer based to event based.
    def _maint(self):
        '''clean up events that have executed'''
        if self.debug:
            for i in self.schedules:
                print("event ", i )
        done = [i for i in self.schedules if not i.is_alive() ]
        self.schedules = [i for i in self.schedules if i.is_alive() ]
        self.history += done 

        t = threading.Timer(self._maint_period, self._maint)
        t.name = 'maint'
        t.start()
        
        
    def add_schedule(self, when, what, *args, **kwargs):
            
        t = threading.Timer(when, what, args, kwargs)
        if self.debug:
            print("adding timer ", t, when )
        if 'thread_name' in kwargs:
            t.name = kwargs['thread_name']
        else:
            t.name = t.name + "_event"
        t.start()
        self.schedules.append(t) 
        
    def enumerate(self):
        return self.schedules
        
    def add_event(self, event):
        if not isinstance(event, Event):
            raise TypeError("require a ")
        
        
    def show_schedule(self):
        for i in self.schedules:
            print("event waiting  ", i.name, i.ident)
        for i in self.history:
            print("event executed ", i.name, i.ident)
                        
        
            
            