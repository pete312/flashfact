#!/bin/env python3

import unittest 
import cta.protocol
import logging
import helpers


logger = logging.getLogger()
helpers.setup_logger(logger)

class TestCTA(unittest.TestCase):
    def test_1(self):
        cta.protocol.fcache('/tmp/1', [1,2,3], pickle=True)
        
        
    def test_2(self):
        data = cta.protocol.fcache('/tmp/1', pickle=True)
        self.assertEqual( data, [1,2,3]) 


if __name__ == "__main__":
    unittest.main()