import asyncio
import functools
import logging
import re
import requests
from functools import wraps
from threading import RLock
import aiohttp
from time import sleep

_LOGGER = logging.getLogger(__name__)
ZONEMAP = {1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h"}

class Mhub(object):
    """
    HDAnywhere MHUB interface
    """

    def power_status(self):
        """
        Get the structure representing the status of the zone
        :return: status of the zone or None
        """
        raise NotImplemented()
    
    def set_power(self, power: bool):
        """
        Turn zone on or off
        :param power: True to turn on, False to turn off
        """
        raise NotImplemented()
    
    def zone_status(self, zone: int):
        """
        Get the structure representing the status of the zone
        :param zone: zone 1..8
        :return: status of the zone or None
        """
        raise NotImplemented()

    def set_zone_source(self, zone: int, source: int):
        """
        Set source for zone
        :param zone: Zone 1-8
        :param source: integer from 1-8
        """
        raise NotImplemented()

    def set_all_zone_source(self, source: int):
        """
        Set source for all zones
        :param source: integer from 1-8
        """
        raise NotImplemented()


def get_mhub(url):
    """
    Return synchronous version of HDAnywhere MHUB
    :param port_url: serial port, i.e. '/dev/ttyUSB0'
    :return: synchronous implementation of Blackbird interface
    """
    lock = RLock()

    def synchronized(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper

    class MhubSync(Mhub):
        def __init__(self, url):
            """
            Initialize the client.
            """
            self.host = url + '/api/'

        def _process_request(self, request):
            """
            Send data to socket
            :param request: request that is sent to the blackbird
            :param skip: number of bytes to skip for end of transmission decoding
            :return: ascii string returned by blackbird
            """
            _LOGGER.debug('Sending "%s"', request)
            
            response = requests.get(url = self.host + request)

            return response.json()
        
        @synchronized
        def power_status(self):
            json = self._process_request('data/0')
            return json['data']['power']
    
        @synchronized
        def set_power(self, power: bool):
            if power:
                self._process_request('power/1')
            else:
                self._process_request('power/0')
        
        @synchronized
        def zone_status(self, zone: int):
            # Returns status of a zone
            json = self._process_request('data/200/z' + str(zone))
            return json['data']['zone']['video_input']
    
        @synchronized
        def set_zone_source(self, zone: int, source: int):
            zone_letter = ZONEMAP.get(zone)
            control_zone = 'control/switch/' + str(zone_letter) + '/' + str(source)
            self._process_request(control_zone)
    
        @synchronized
        def set_all_zone_source(self, source: int):
            for zone in ZONEMAP: 
                self.set_zone_source(zone, source)
                sleep(1)

    return MhubSync(url)