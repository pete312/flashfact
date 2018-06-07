from datetime import datetime, timedelta, time, date
import re
import logging
import helpers 

is1_date = {'fmt':'%Y-%m-%d', 'txt':'ISO1 YYYY-MM-DD'}
is2_date = {'fmt':'%d-%m-%Y',  'txt':'ISO2 YYYY-MM-DD'}
us_date =  {'fmt':'%m-%d-%Y',  'txt':'US MM-DD-YYYY'}

date_formats = (is1_date, is2_date, us_date)
default_format = date_formats[0]

logger = logging.getLogger(__name__)
helpers.setup_logger(logger, stdout=True)

def validate_date_format(sdate, default_format):
    if type(default_format) == str:
        default_format = {'fmt':default_format}

    valid_date = None
    for format in date_formats:
        try:
            valid_date = datetime.strptime(sdate, default_format['fmt'])
            break
        except ValueError:
            pass
            
    return valid_date
    
    
def get_seconds_until_time(target_time):
    '''return float of number of seconds left until the target_time'''

    if not isinstance( target_time, time ):
        raise TypeError("target_time must be datetime.time")
        
    curr_time = datetime.now()
    target_datetime = datetime.combine( datetime.today(), target_time )
    if curr_time > target_datetime:
        target_datetime = target_datetime + timedelta(1)
        
    seconds_left = ( target_datetime - curr_time ).total_seconds()
        
    return seconds_left
    

def str_to_time(timestring, strict=True):
    '''safely convert a string into a time or None if cannot be done'''
    scan_for = '^\s*((\d+):(\d+):(\d+))\s*$'
    if strict:
        scan_for = '^(\d+):(\d+):(\d+)$'
    
    search = re.search(scan_for, timestring)
    if search:
        try:
            return time( *([ int(i) for i in search.groups()]) )
        except ValueError as e:
            logger.error(e)
        
    return None
    
def str_to_date(datestring, delim='-', strict=True):
    '''safely convert a date string into a date or None if cannot be done'''

    scan_for = '^\s*((\d+){delim}(\d+){delim}(\d+))\s*$'.format(delim=delim)
    if strict:
        scan_for = '^(\d+){delim}(\d+){delim}(\d+)$'.format(delim=delim)
    search = re.search(scan_for, datestring)
    if search:
        try:
            return date( *([ int(i) for i in search.groups()]))
        except ValueError as e :
            logger.error(e)
            
            return None
    return None
    

def str_time_to_datetime(timestring, return_future=True):
    '''returns a datetime given a date 
        timestring     time to convert in H:M:S 
        return_future  if True (default) this will return next day's time 
                       if the time given is in the past.
    '''
    
    target_time = str_to_time(timestring)
    target_datetime = datetime.combine( date.today(), target_time ) 
    curr_time = datetime.now()
    
    if curr_time > target_datetime and return_future:
        target_datetime = target_datetime + timedelta(1)

    return target_datetime
    
    
def get_datetime_from_timestring( timestring, format=None ):
    #t = datetime.strptime( timestring , "%H:%M:%S")
    if format:  
        t = datetime.strptime( timestring , format)
    else:
        t = datetime.strptime( timestring , "%H:%M:%S")
    return datetime(*(datetime.now().timetuple()[:3] + (t.hour, t.minute, t.second)))


    
def get_sundays_date(when='last'):
    ''' return today's date '''
    today = datetime.now()
 
    if when == 'last' or when == "":
        sunday = (today - timedelta(today.weekday() + 1)).date()
    else:
        try:
            today = datetime.strptime(when, default_format['fmt'])
        except ValueError:
            print("the date {when} is not a valid date format {date_format}".format(when=when, date_format=default_format['txt']))  
        sunday = (today - timedelta(today.weekday() + 1)).date()

    return sunday
    
    