
from dtime import *
import state
import logging
import pickle as _pickle
import os.path
import xml.etree.ElementTree as ET
import requests
from random import random
logger = logging.getLogger(__name__)

appstate = state.AppState()


## from 
## http://www.ctabustracker.com/bustime/eta/getStopPredictionsETA.jsp?stop=1702

## <pre>
##     <pt>9</pt>
##     <pu> MINUTES</pu>
##     <mode>1</mode>
##     <consist/>
##     <cars/>
##     <fd> Western Brown Line</fd>
##     <zone/>
##     <scheduled>false</scheduled>
##     <nextbusminutes>0</nextbusminutes>
##     <nextbusonroutetime>1:38 PM</nextbusonroutetime>
##     <v>1855</v>
##     <rn>49B</rn>
##     <rd>49B</rd>
## </pre>

## from 
## http://www.ctabustracker.com/bustime/map/getStopsForRouteDirection.jsp?route=49B&direction=Southbound

## <route>
##     <id>49B</id>
##     <stops>
##         <stop>
##             <name>Leland & Western (Brown Line)</name>
##             <id>1375</id>
##             <rtpiFeedName/>
##         </stop>
##         <stop>
##             <name>Western & Albion</name>
##             <id>1680</id>
##             <rtpiFeedName/>
##         </stop>
##         <stop>
##             <name>Western & Albion</name>
##             <id>1702</id>
##             <rtpiFeedName/>
##         </stop>
##     </stops>
## </route>

_ROUTE_URL = 'http://www.ctabustracker.com/bustime/map/getStopsForRouteDirection.jsp?route={route}&direction={direction}'


def fcache(filename, data=None, pickle=False):
    '''
        file cache function:
            filename  place to save data or load data from
            data      if present, then save this data. if not, return filename content.
            pickle    pickle the data object before saving or loading
        
    '''
    if data:
        # save 
        logger.info("caching state to " + filename)
        with open(filename, 'wb') as f:
            if pickle: 
                _pickle.dump(data,f)
            else:
                f.write(data)
    else:
        # load
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                if pickle:  
                    data = _pickle.load(f)
                else:
                    data = f.read()
        else:
            raise IOError("no such file " + filename)
        return data

def get_bus_stop_activity(stop_number):
    stop_activity = 'http://www.ctabustracker.com/bustime/eta/getStopPredictionsETA.jsp?stop={stop}&key={randkey}'.format(stop=int(stop_number), randkey=random())
    results = []
    cache_file = '/tmp/cta_stop_activity_%s.dat' % stop_number
    logger.info("cache file is " + cache_file)
    
    # Trying to make sense of the CTA tags. Tags named val_* are of little use.
    tag_conversion = {  'v': 'vehicle',
                        'nextbusonroutetime' : 'eta',
                        'pt' : 'minutes',
                        'rn' : 'route_number',
                        'fd' : 'final_destination',
                        'pu' : 'val_pu',   
                        # tag <nextbusminutes> does not appear to change and 
                        # looks like the tag <pt> is showing this value anyway
                        'nextbusminutes' : 'next_bus_minutes',
                        # <pu> tag possibly means prediction unit 
                        # because its mostly set to value of MINUTES, but it changes 
                        # to val of APPROACHING when <pt> tag value is '&nbsp;' which
                        # seems inconsistent (I convert <pt> to 0 for consistency).  
                        # So perhaps its function is simply a display message field.
                        'rd' : 'val_rd',
                        'mode':'val_mode',
                        'consist':'val_consist',
                        'cars':'val_cars',
                        'zone':'val_zone',
                        'scheduled':'val_scheduled'
                        }
    
    if appstate.offline:
        results = fcache(cache_file, pickle=True)
        return results
    else:
        
        logger.info("get arrival data from " + stop_activity)
        tracking = requests.get(stop_activity)
        if tracking.status_code == 200:
            root = ET.fromstring(tracking.text)
        else:
            raise IOError("no such file "+ root.dump())
            
        if root.find('noPredictionMessage') is not None:
            raise ValueError("no stop found for %s" % stop_number)
        
        for row in root: 
            d = {tag_conversion[i.tag]:str(i.text).strip() for i in row}
            d['stop_id'] = stop_number
            
            if d['minutes'] == '&nbsp;': # remove this annoying value
                d['minutes'] = 0
            logger.info("arrival time vehicle {vehicle} at stop {stop_id} - {minutes} {val_pu} {eta} onward to {final_destination}".format(**d))
            results.append(d)
    
    return results


def get_routes():
    
    # consider returning cache results
    if appstate.offline:
        routes = fcache('/tmp/bustracker.routes.dat','rb', pickle=True)
        if routes:
            return routes
        
    routes = []
    route_xml = requests.get(_ROUTE_URL.format(route='49B', direction='Southbound')).text
    root = ET.fromstring(route_xml)
    route_number = root.find('id').text
    tag_conversion = {  'name': 'stop_name',
                        'id' : 'stop_id',
                        'rtpiFeedName' :'rtpiFeedName',
                        }
    for c in root.iter('stop'):
        route  = {tag_conversion[i.tag]:i.text for i in c}
        route['route_number'] = route_number
        route['direction'] = 'Southbound'
        routes.append(route)
      
            
    route_xml = requests.get(_ROUTE_URL.format(route='49B', direction='Northbound')).text
    root = ET.fromstring(route_xml)
    route_number = root.find('id').text
    for c in root.iter('stop'):
        route  = {tag_conversion[i.tag]:i.text for i in c}
        route['route_number'] = route_number
        route['direction'] = 'Northbound'
        routes.append(route)

    fcache('/tmp/bustracker.routes.dat', routes, pickle=True)
    
    return routes

