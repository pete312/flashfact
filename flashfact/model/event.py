from argparse import ArgumentParser

from state import State


def get_options():
    parser = ArgumentParser(description='CMD Option Demo.', epilog="")
    parser.add_argument('--testmode', action='store_true', default=False, help='no menu. Just run the test')

    return parser.parse_args()


Base = declarative_base()

class EventData():
    event_types = (DailyFXData, CTAData)
    
    
    
    

class DB(Cmd):
    def __init__(self, name):
        Cmd.__init__(self)
        self.engine = None
        self.name = name
        self._c = None
        if name != "":
           self.engine = create_engine("sqlite:///{name}".format(name=self.name))
           self.Session = sessionmaker(self.engine)

    def do_createdb(self, s):
        if s != "":
            self.name = s
            self.engine = create_engine("sqlite:///{name}".format(name=self.name))
        Base.metadata.create_all(self.engine)
        
    def do_recreatedb(self, s):
        ans = input("Are you sure you want to destroy and recreate the %s DB? " % self.name)
        if ans.lower().startswith("y"):
            EventData.__table__.drop(self.engine)
            self.createdb("")
            
            
    def do_tables(self,s):
        if s != "":
            self.name = s
            self.engine = create_engine("sqlite:///{name}".format(name=self.name))
        inspector = inspect(self.engine)
        
        for i in inspector.get_table_names():
            print(i)
            for ii in inspector.get_columns(i):
                print("\t",ii)
                
    def do_showevents(self, s):
        if s == "":
            s = '01-02-2000 12-26-2038' # all records 
        
        sdate , stime = s.split(" ")
        # to do build query and return results.
        session = self.Session()
        
        for row in session.query(EventData):
            print(row)
        print("done")
        
        
    def do_load_dfx(self, s, show=True, use_cached=True):
        
        date_fmt = us_date['fmt']
    
        if s == "" :
        
            date = get_sundays_date()
            print("Error: date required in mm-dd-yyyy format")
            return
        
        #date = datetime.strptime(s, date_fmt)
        #date = date.strftime(date_fmt)
        date = get_sundays_date(s)
        
        data = get_dailyfx_data(date, use_cached=use_cached)
        data = process_daily_fx_data(data)
        if show:
            print(data)
        
        session = self.Session()
        for row in data:
            print ("inserting ", row)
            self.insert(row, session)
        self._c = data # save this data for the get wrapper if needed
        
        
    def get_load_dfx(self, date):
        # return a table of rows from DailyFX with a date arg of mm-dd-yyyy
        self.do_load_dfx(date, show=False)
        return self._c
        
    def do_set_date_format(self, s='YYYY-MM-DD'):
        while 1:
            try:
                ans = int(input(("1. MM-DD-YYYY\n"
                         "2. DD-MM-YYYY\n"
                         "3. YYYY-MM-DD\n")))
            except ValueError as e:
                print("select a number")
                
            if not [i for i in (1,2,3,) if i == ans]:
                print("select one of the formats provided")
        
        
    def insert2(self, d):
        q = 'insert into event_data values (?,?,?,?,?,?) where ev_date = ? and event_text'
        
    def insert(self, d, session=None):
        # insert data from d which is a table of values from self.get_load_dfx('mm-dd-yyyy')
        year = ' ' + str(datetime.now().year)
        date = datetime.strptime( d['Date'] + year, '%d-%b %a %Y' ).date()
        #time = datetime.strptime( d['GMT'] , '%H:%M' ).time()
        evd = EventData()
        evd.ev_date         = date
        evd.ev_time         = d['GMT'] 
        evd.currency        = d['Currency']
        evd.event_text      = d['Event']
        evd.previous        = d['Previous']
        evd.forcast         = d['Forecast']
        
        if session:
            print("adding ", evd )
            session.add(evd)
        return evd
        
        
        
    def do_exit(self, s):
        return True
        
    def do_quit(self, s):
        return True
        

def run_test():
    # do whatever test is needed in dev

    c = DB('econdata.db')
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
    
def debug_here():
    import pdb
    from readline import parse_and_bind
    import rlcompleter
    parse_and_bind("tab: complete")
    pdb.set_trace()
        
if __name__ == "__main__": 
    
    args = get_options()
    if args.testmode:
        run_test()
    else:

        c = DB('econdata.db')
        
        c.cmdloop()
            
    