
# SQLAlchemy ORM interface
# Pete Moore 5/11/18

from sqlalchemy import create_engine
from sqlalchemy import Integer, String, DateTime, Time,  Date
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect, select
from datetime import datetime

class DatabaseNotReady(Exception):
    pass
    
class EndWithoutBeginTran(Exception):
    pass
    
class NoBeginTran(Exception):
    pass


from model.cta import CTARoute, CTAArrival, Base

#Base = declarative_base()

# ORM connection reference. http://docs.sqlalchemy.org/en/latest/core/engines.html


class DB:

   
    def __init__(self, dbname):
        #Cmd.__init__(self)
        self.engine = None
        self.database = dbname
        self._c = None
        self.ready = False
        self.session = None
        
    def begin_tran(self):
        self.session = Session(self.engine)
        
    def end_tran(self):
        if not self.session:
            raise ErrorEndTranWithoutBeginTran()
        self.session.commit()
        self.session = None

    def sqlite(self, dbname):
        self.engine = create_engine("sqlite:///{name}".format(name=dbname))
        self.Session = sessionmaker(self.engine)
        self.ready = True
        
    def create(self):
        if not self.ready: 
            raise DatabaseNotReady()
        Base.metadata.create_all(self.engine)
        
    def connect(self):
        if not self.ready or self.engine:
            raise DatabaseNotReady()
        self.engine.connect()
        
    def do_recreatedb(self, s):
        ans = input("Are you sure you want to destroy and recreate the %s DB? " % self.name)
        if ans.lower().startswith("y"):
            EventData.__table__.drop(self.engine)
            self.createdb("")
            
            
    def get_tables(self,s):
        if s != "":
            self.name = s
            self.engine = create_engine("sqlite:///{name}".format(name=self.name))
        inspector = inspect(self.engine)
        
        for i in inspector.get_table_names():
            print(i)
            for ii in inspector.get_columns(i):
                print("\t",ii)
               
  
        
    # def do_set_date_format(self, s='YYYY-MM-DD'):
        # while 1:
            # try:
                # ans = int(input(("1. MM-DD-YYYY\n"
                         # "2. DD-MM-YYYY\n"
                         # "3. YYYY-MM-DD\n")))
            # except ValueError as e:
                # print("select a number")
                
            # if not [i for i in (1,2,3,) if i == ans]:
                # print("select one of the formats provided")
        
    def insert_cta_route(self, row, session):
        d = CTARoute()
        #print(row)
        d.route_number  = row['route_number']
        d.stop_name     = row['stop_name']
        d.stop_id       = row['stop_id']
        d.direction     = row['direction']
        
        session.add(d)
       
       
        
    def insert(self, table, data):
    
        if not self.session:
            raise NoBeginTran("insert without begin_tran")
            
        print(table, type(table), CTARoute)
        if table == CTARoute:
            
            if type(data) == dict: 
                self.insert_cta_route(data, self.session)
            else:
                for row in data:
                    print("row ins", row)
                    self.insert_cta_route(row, session)
        
        # insert data from d which is a table of values from self.get_load_dfx('mm-dd-yyyy')
        # year = ' ' + str(datetime.now().year)
        # date = datetime.strptime( d['Date'] + year, '%d-%b %a %Y' ).date()
        # #time = datetime.strptime( d['GMT'] , '%H:%M' ).time()
        # evd = EventData()
        # evd.ev_date         = date
        # evd.ev_time         = d['GMT'] 
        # evd.currency        = d['Currency']
        # evd.event_text      = d['Event']
        # evd.previous        = d['Previous']
        # evd.forcast         = d['Forecast']
        
        # if session:
            # print("adding ", evd )
            # session.add(evd)
        # return evd
        
        
    def get_route(self, stop_id):
        results = self.session.query(CTARoute).filter_by(stop_id=stop_id).all()
        
        return results
            
    def get_routes(self, stop_ids):
        results = self.session.query(CTARoute).filter(CTARoute.stop_id.in_([1672,1691])).all()
        return results
        
       
        
        
    def do_exit(self, s):
        return True
        
    def do_quit(self, s):
        return True