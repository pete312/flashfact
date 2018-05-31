#!/bin/env python3

# unit tests for flashfact

from os.path import join, dirname, abspath, exists
import logging
import unittest 
from time import sleep
from datetime import datetime, timedelta
import time

# app libs for testing
import helpers

import cta.protocol 
import  model.db
from model.cta import CTAArrival, CTARoute
from state import AppState 

appstate = AppState()  
appstate.datadir = abspath( dirname(__file__) ) # make the tests dir the datadir
appstate.offline = False                        # pull all data from URL sources.

logger = logging.getLogger()
helpers.setup_logger(logger, stdout=True)


import dtime

def assert_path(filename):
    return exists(filename)
    
class TestDTime(unittest.TestCase):
    def test_time_conversions(self):
        now = datetime.now()
        dt_5_seconds = now + timedelta(0,5)
        td_5_seconds = dt_5_seconds - now
        float_5_seconds = td_5_seconds.total_seconds()
        
        # make sure the 5 second assumption is correct
        self.assertEqual( float_5_seconds , 5.0 )
        
        # check datetime mode input of get_seconds_until
        test_result = dtime.get_seconds_until(dt_5_seconds, now)
        self.assertEqual( test_result , 5.0 )
        
        # check string mode input of get_seconds_until 
        
        # For elegance reasons get_seconds_until does not support sub second 
        # timestamps in string mode. Only in datestamp mode.
        # But datetime.now() has microseconds and it will be unlikely to pass any 
        # assertEqual() test without removing microseconds from the datetime.now()
        # So, round the datetime variable "now" to the last second by removing 
        # the microseconds portion.
        now = datetime(*now.timetuple()[:6]) 
        
        timestring = dt_5_seconds.strftime("%Y-%m-%d %H:%M:%S")
        test_result = dtime.get_seconds_until(timestring, now)
        self.assertEqual( test_result , 5.0 )

        badtimestring = dt_5_seconds.strftime("%Y-%m-%d %H:%M")
        self.assertRaises(ValueError,  dtime.get_seconds_until, (badtimestring, now) )
        self.assertRaises(ValueError,  dtime.get_seconds_until, (None, now) )
        
       

class CTAProtocolTest(unittest.TestCase):

        
    def test_fcache(self):
        testfile = appstate.datadir +  '/1'
        fakefile =  appstate.datadir +  '/not_exists'
        cta.protocol.fcache(testfile, [1,2,3], pickle=True)
        
        data = cta.protocol.fcache(testfile, pickle=True)
        self.assertEqual( data, [1,2,3]) 
        
        self.assertRaises(OSError, cta.protocol.fcache, (fakefile)) 
        
    def test_load_rotues(self):
        
        data_live = cta.protocol.get_routes() # seed the routes
        appstate.offline = True
        data_cached = cta.protocol.get_routes()
        self.assertEqual(data_live, data_cached)
        
       
        
    def test_bus_stop_activity(self):
        # must return set of bus due time data
        
        data = {'name': 'Western & Birchwood Terminal', 'id': '1691', 'rtpiFeedName': None}
        stop_num = int( data['id'] )
        appstate.offline = False
        bus_data = cta.protocol.get_bus_stop_activity( stop_num )
        
        self.assertTrue( bus_data != None ) # have data
        
        appstate.offline = True
        self.assertRaises(IOError ,cta.protocol.get_bus_stop_activity, ( 11111111 )) 
        appstate.offline = False
        
        
        self.assertRaises(ValueError ,cta.protocol.get_bus_stop_activity, ( 11111111 )) 
        #bus_data = cta.protocol.get_bus_stop_activity( 11111111 ) # non existing stop
        #self.assertEqual( bus_data, [])
        
        
    def run_test():
        dbfile = appstate.datadir + "test.db"
        c = DB(dbfile)
        Session = sessionmaker(c.engine)
        Base.metadata.create_all(c.engine) # in the event there is no db file at all.
        EventData.__table__.drop(c.engine) 
        Base.metadata.create_all(c.engine) # now we have clean start
        d = c.get_load_dfx("04-15-2018")
        block = []

        conn = Session()
        for row in d:
            r1 = c.insert(row)
            print(r1)
            conn.add(c.insert(row))
        
        conn.commit()
        
        conn.query()
        
def get_test_route_data():
    route_data = cta.protocol.get_routes()
    return route_data

def get_test_arrival_data(stop_num):    
    try:
        bus_data = cta.protocol.get_bus_stop_activity( stop_num )
        
    except  IOError:
        print("error: No cached bus data. Please run CTAProtocolTest")
    return bus_data
    
    
    

import threading
def test_timed(*a, **ka):
    print('starting test_timed at {now} called with :'.format(now=datetime.now()))
    print(a)
    print(ka)
    #print("threads",  [(i.is_alive(),i.getName(), i.interval) for i in threading.enumerate() if i.getName() != 'MainThread'] )
    
    ka['checkin'].append(datetime.now())
    # ka will have checkin arg removed as this makes it untestable
    ka['checkin'].append( str(a) + ',' + str({i:v for i,v in ka.items() if i != 'checkin'}) )
    
class MiscTest(unittest.TestCase):
    def test_timed_callback(self):
        # check if the timer works as expected.
        now = datetime.now()
        checkin =  [now]
        args = (1,2,3)
        kwargs = dict(this='that', checkin=checkin)
        t1 = helpers.new_timed_callback(test_timed, seconds=1.2, args=args, kwargs=kwargs )
        sleep(3)
        duration = (checkin[1] - checkin[0]).total_seconds()
        self.assertTrue( duration > 1.2 and duration < 1.25, "unexpected duration %s" % duration)
        # test arg passing
        # kwargs will have checkin arg removed
        expected = '{0},{1}'.format(str(args), str({i:v for i,v in kwargs.items() if i != 'checkin'})) 
        self.assertEqual(checkin[2],  expected )
        
        # now check it doesnt run.
        now = datetime.now()
        checkin = [now]
      
        self.assertEqual(len(checkin), 1)
        kwargs = dict(this='that', checkin=checkin)
        t2 = helpers.new_timed_callback(test_timed, seconds=0.5, args=args, kwargs=kwargs, no_start=True )
        
        self.assertEqual(len(checkin), 1)
        sleep(1)
        self.assertEqual(len(checkin), 1)
        t2.start()
        sleep(1)
        duration = (checkin[1] - checkin[0]).total_seconds()
        self.assertTrue( duration > 1.5 and duration < 1.75, "unexpected duration %s" % duration)
    
class DBModelTest(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_all(self):    
        filename = 't.db'
        
        try:
            os.remove(filename)
        except:
            pass
            
        db = model.db.DB("ctatest")
        db.sqlite(filename) # select method as sqlite with filename
        db.create()
        self.assertTrue( assert_path(filename) )
        
        # insert a row into this table type
        
        data = get_test_route_data()
        if not data:
            raise IOError("no cached data. Please run the CTAProtocolTest to populate cache.")

        #db.merge_route_data( data )
        
        #logger.info(db.session.query(CTARoute).filter_by(route_number = '49B').all() )
        #logger.info(db.session.query(CTARoute).filter(CTARoute.stop_id == 1691).all())
        #logger.info(db.get_route(1691))
        #logger.info(db.get_routes([1691,1672]))
        
        appstate.offline = False
        data = get_test_arrival_data(1691)
        
        db.merge_arrival_data( data )
        
        
        
        

if __name__ == "__main__":
    #appstate.offline = False # pull all data from live URL sources.
    #data = cta.protocol.get_routes() # seed the cache
    unittest.main()
    