#!/bin/env python3

import unittest 
import cta.protocol
import logging
import helpers
from os.path import join, dirname, abspath

from state import AppState 

appstate = AppState()  
appstate.datadir = abspath( dirname(__file__) ) # make the tests dir the datadir
appstate.offline = False                        # pull all data from URL sources.

logger = logging.getLogger()
helpers.setup_logger(logger)



class TestCTA(unittest.TestCase):

        
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
        
        
        #self.assertTrue
        
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

if __name__ == "__main__":
    #appstate.offline = False # pull all data from live URL sources.
    #data = cta.protocol.get_routes() # seed the cache
    unittest.main()
    