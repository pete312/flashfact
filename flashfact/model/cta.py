

from sqlalchemy import create_engine
from sqlalchemy import Integer, String, DateTime, Time,  Date
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect, select

Base = declarative_base()


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



## <route>
##     <id>49B</id>
##     <stops>
##         <stop>
##             <name>Leland & Western (Brown Line)</name><id>1375</id><rtpiFeedName/>
##         </stop>
##         <stop>
##             <name>Western & Albion</name><id>1680</id>
##             <rtpiFeedName/>
##         </stop>
##         <stop>
##             <name>Western & Albion</name><id>1702</id>
##             <rtpiFeedName/>
##         </stop>
##     </stops>
## </route>



class CTARoute(Base):
    __tablename__ = 'cta_route'
    
    id  = Column(Integer, primary_key=True)
    route_number    = Column(String())
    stop_name       = Column(String())
    stop_id         = Column(Integer())
    direction       = Column(String())
    
    def __repr__(self):
        return "CTARoute <id> [{0}] route_number [{1}]  stop_id [{3}] direction [{4}] stop_name [{2}]".format(
            self.id,
            self.route_number,
            self.stop_name,
            self.stop_id,
            self.direction
            )
            
    def __str__(self):
        return self.__repr__()
    

class CTAArrival(Base):
    __tablename__ = 'cta_bus_arrival'

    id                  = Column(Integer, primary_key=True)
    eta                 = Column(Integer())
    unit                = Column(String())
    mode                = Column(String())
    final_destination   = Column(String())
    next_bus_minutes    = Column(Integer())
    vehicle_no          = Column(Integer())
    route_number        = Column(String())
    route_d_unknown     = Column(String())
    
    
    def __str__(self):
        return "CTAArrival <id [{0}] eta [{1}] unit [{2}] final_destination [{3}] next_bus_minutes [{4}] vehicle_no [{5}] route_number [{6}] unknown [{7}] > ".format(         
                 self.id, 
                 self.eta, 
                 self.unit,
                 self.mode,
                 self.final_destination,
                 self.next_bus_minutes,
                 self.vehicle_no,
                 self.route_number,
                 route_d_unknown)

