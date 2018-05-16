
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

import logging
import pdb

class DatabaseNotReady(Exception):
    pass
    
class EndWithoutBeginTran(Exception):
    pass
    
class NoBeginTran(Exception):
    pass
    
class BeginTranInProgress(Exception):
    pass


from model.cta import CTARoute, CTAArrival, Base

logger = logging.getLogger(__name__)

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
        
        
    def new_session(self):
        return Session(self.engine)
        
    def begin_tran(self):
        if self.session:
            raise BeginTranInProgress()
        self.session = Session(self.engine)
        return self.session
        
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
            print("-- ", i)
            for ii in inspector.get_columns(i):
                print("--\t",ii)
               
  
        
    def insert_cta_route(self, row, session):
       
        logger.info("inserting row {0}".format( row ))
        
        d = CTARoute()
        d.route_number  = row['route_number']
        d.stop_name     = row['stop_name']
        d.stop_id       = row['stop_id']
        d.direction     = row['direction']
        
        session.add(d)
       
       
    def insert_cta_arrival(self, row):
    
        logger.info( "insert {0}".format(row) ) 
        
        d = CTAArrival()
        d.vehicle           = row['vehicle']
        d.route_number      = row['route_number']
        d.stop_id           = row['stop_id']
        d.minutes           = row['minutes']
        d.val_pu            = row['val_pu']
        d.eta               = row['eta']
        d.final_destination = row['final_destination']
        d.next_bus_minutes  = row['next_bus_minutes' ]
        d.val_mode          = row['val_mode']
        d.val_rd            = row['val_rd'] 
        logger.info("created CTAArrival %s" % d)
        return d
       
        
    def insert(self, table, data, session):
        
        session = self.begin_tran()
        
        if table == CTARoute:
            if type(data) == dict: 
                self.insert_cta_route(data, session)
            else:
                for row in data:
                    self.insert_cta_route(row, session)
        elif table == CTAArrival:
            if type(data) == dict: 
                d = self.insert_cta_arrival(row)
                session.add(d)
            else:
                for row in data:
                    d = self.insert_cta_arrival(row)
                    session.add(d)
        else:
            return
       
        self.end_tran()
        
   
    def merge_route_data(self, route_data):
        
        session = self.new_session()
        
        existing_data = session.query(CTARoute).order_by('route_number','stop_id')
        
        # index the route_data
        rdx = {"{route}_{stop}".format(route=i['route_number'], stop=i['stop_id']) :i for i in route_data}
        visited = []
        to_add = rdx.copy()
        for d in existing_data:
            key = "{route}_{stop}".format(route=d.route_number, stop=d.stop_id) 
            print("row id", d.id, key, end=' ' )
            if key in visited:
                logger.warning("duplicate data {0}".format(d))
            elif key in rdx:
                # update the data
                del to_add[key]
            else:
                logger.info("db has extra row {0}".format(d))
                #self.insert(CTARoute, rdx[key], session)
                
            visited.append(key)
        if to_add:
            logger.info("adding missing routes.")
            self.insert(CTARoute, to_add.values(), session)
            
        session.commit()

        
    def merge_arrival_data(self, arrival_data):
    
        session = self.new_session()
        existing_data = session.query(CTAArrival).order_by('vehicle')
        
        # index the arrival_data
        adx = {"{vehicle}".format(**d):d for d in arrival_data}
        
        visited = []
        to_add = adx.copy()

        for d in existing_data:
            key = "{vehicle}".format( vehicle=d.vehicle )
            if key in visited:
                logger.warn('duplicate entry {0}'.format(d))
            elif key in adx:
                logger.info("update route {route_number} {vehicle} {minutes} -> {um} {val_pu} {eta} -> {ueta} going to {final_destination}".format(route_number=d.route_number, eta=d.eta, val_pu=d.val_pu, minutes=d.minutes, vehicle=d.vehicle,final_destination=d.final_destination,um=adx[key]['minutes'], ueta=adx[key]['eta']))
                d.eta = adx[key]['eta']
                d.minutes = adx[key]['minutes']
                del to_add[key]
            else:
                logger.info("db has extra row {0}".format(d))
            
            visited.append(key)

        if to_add:
            # whatever is in this list needs to be added to database
            logger.info("adding missing arrivals {0}".format( to_add.values() ))
            self.insert(CTAArrival, list(to_add.values()), session=session)

      
        session.commit()
        
        
    def get_route(self, stop_id):
        results = self.session.query(CTARoute).filter_by(stop_id=stop_id).all()
        
        return results
            
    def get_routes(self, stop_ids):
        results = self.session.query(CTARoute).filter(CTARoute.stop_id.in_(stop_ids)).all()
        return results
        
       

    def do_exit(self, s):
        return True
        
    def do_quit(self, s):
        return True