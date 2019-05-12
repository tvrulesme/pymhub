# pymhub
Python3 interface implementation for HDAnywhere HDBaseT Matrix

## Notes
This is for use with [Home-Assistant](http://home-assistant.io)

## Usage
```python
from pymhub import get_mhub

# Connect via IP
mhub = get_mhub('http://192.168.0.44')

# Valid zones are 1-8
zone_status = mhub.zone_status(1)

# Turn off mhub #1
hub.set_power(False)

# Set source 5 for zone #1
mhub.set_zone_source(1,5)

# Set all zones to source 2
mhub.set_all_zone_source(2)

```
