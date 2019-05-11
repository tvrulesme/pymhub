import unittest

import serial
from time import sleep

from pymhub import (get_mhub)
import asyncio

class TestBlackbird(unittest.TestCase):
    def setUp(self):
        self.responses = {}
        self.mhub = get_mhub('http://192.168.0.44')

    def test_zone_status(self):
        #power_status
        status = self.mhub.power_status();
        self.assertIsNotNone(status, 'Status is None')
        
        #set_power
        self.mhub.set_power(not status)
        newstatus = self.mhub.power_status();
        self.assertNotEqual(status, newstatus, 'Status Unchanged')
        
        
        
        #zone_status
        zoneinput = int(self.mhub.zone_status(1));
        self.assertGreaterEqual(zoneinput, 1, 'Bad input found')
        switchInput = zoneinput - 1
        if switchInput < 1:
            switchInput = zoneinput + 1
            
        self.mhub.set_zone_source(1,switchInput)
        sleep(2)
        
        #set_zone_source
        changed_zone = int(self.mhub.zone_status(1));
        
        self.assertNotEqual(zoneinput, changed_zone, 'Status Unchanged')
        
        self.mhub.set_zone_source(1,zoneinput)
        
        self.mhub.set_power(True)
        sleep(2)
        self.mhub.set_all_zone_source(2)
            
        print(self.mhub.zone_status(1))


if __name__ == '__main__':
   unittest.main()
