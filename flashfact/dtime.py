from datetime import datetime, timedelta

is1_date = {'fmt':'%Y-%m-%d', 'txt':'ISO1 YYYY-MM-DD'}
is2_date = {'fmt':'%d-%m-%Y',  'txt':'ISO2 YYYY-MM-DD'}
us_date =  {'fmt':'%m-%d-%Y',  'txt':'US MM-DD-YYYY'}

date_formats = (is1_date, is2_date, us_date)
default_format = date_formats[0]

date_format = is1_date



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
            
    print(valid_date)
    return valid_date
    
    
    
def stime_2datetime(timestring):
    t = datetime.strptime(timestring, "%H:%M:%S")
    return datetime(*(datetime.now().timetuple()[:3] + (t.hour, t.minute, t.second)))
    


    
def get_sundays_date(when='last'):
    # get today's date
    today = datetime.now()
 
    if when == 'last' or when == "":
        sunday = (today - timedelta(today.weekday() + 1))
        #sunday = (today - timedelta(today.weekday() + 1)).timetuple()[:3]
    else:
        try:
            today = datetime.strptime(when, default_format['fmt'])
        except ValueError:
            print("the date {when} is not a valid date format {date_format}".format(when=when, date_format=default_format['txt']))  
        sunday = (today - timedelta(today.weekday() + 1)) 
        print ("sunday = {sunday}, today = {today}".format(sunday=sunday,today=today))
    return sunday