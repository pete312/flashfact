#!/bin/env python3

from os.path import join, dirname, abspath, exists
import logging
import unittest 
import helpers

import cta.protocol 
import  model.db
from model.cta import CTAArrival, CTARoute
from state import AppState 

appstate = AppState()  
appstate.datadir = abspath( dirname(__file__) ) # make the tests dir the datadir
appstate.offline = False                        # pull all data from URL sources.

logger = logging.getLogger()
helpers.setup_logger(logger)

def assert_path(filename):
    return exists(filename)


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
        bus_data = cta.protocol.get_bus_stop_activity( 11111111 ) # non existing stop
        self.assertEqual( bus_data, [])
        
        
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
    appstate.offline = False
    route_data = cta.protocol.get_routes()
    return route_data

def get_test_arrival_data(stop_num):    
    try:
        bus_data = cta.protocol.get_bus_stop_activity( stop_num )
        print(bus_data)
    except  IOError:
        print("error: No cached bus data. Please run CTAProtocolTest")
    return bus_data
    

    
    
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
        db.begin_tran()
        self.assertTrue( assert_path(filename) )
        
        # insert a row into this table type
        
        data = get_test_route_data()
        #for row in data:
        #    print(row)
        #    db.insert(CTARoute, row)
        #
        #db.end_tran()
        
        print(db.session.query(CTARoute).filter(CTARoute.stop_id == 1691).all())
        print (db.get_route(1691))
        print (db.get_routes([1691,1672]))
        
        
        #db.insert(CTAArrival, get_test_arrival_data() )
        
        #db.disconnect()
        

if __name__ == "__main__":
    #appstate.offline = False # pull all data from live URL sources.
    #data = cta.protocol.get_routes() # seed the cache
    unittest.main()
    