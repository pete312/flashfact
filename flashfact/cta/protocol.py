
from dtime import *
import state
import logging
import pickle as _pickle
import os.path
import xml.etree.ElementTree as ET
import requests

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

_ROUTE_URL = 'http://www.ctabustracker.com/bustime/map/getStopsForRouteDirection.jsp?route=49B&direction={direction}'


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
    stop_activity = 'http://www.ctabustracker.com/bustime/eta/getStopPredictionsETA.jsp?stop={stop}'.format(stop=int(stop_number))
    results = []
    cache_file = '/tmp/cta_stop_activity_%s.dat' % stop_number
    if appstate.offline:
        stop_activity = cache(cache_file)
    else:
        tracker = requests.get(stop_activity)
        ET.format()
    
    return results


def get_routes():
    if appstate.offline:
        return fcache('/tmp/bustracker.routes.dat','rb', pickle=True)
    routes = {'Northbound':[], 'Southbound':[]}
    route_xml = requests.get(_ROUTE_URL.format(direction='Southbound')).text
    root = ET.fromstring(route_xml)
    for c in root.iter('stop'):
        route  = {i.tag:i.text for i in c}
        routes['Southbound'].append(route)
        #route['direction'] = 'Southbound'
        #routes[route['name']] = route
            
    route_xml = requests.get(_ROUTE_URL.format(direction='Northbound')).text
    root = ET.fromstring(route_xml)
    for c in root.iter('stop'):
        route  = {i.tag:i.text for i in c}
        #route['direction'] = 'Northbound'
        routes['Northbound'].append(route)
        #routes[route['name']] = route
    f = open('/tmp/bustracker.routes.dat','wb')
    fcache('/tmp/bustracker.routes.dat', routes, pickle=True)
    
    return routes

