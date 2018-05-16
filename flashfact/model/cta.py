

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
    
    #id                  = Column(Integer, primary_key=True)
    #eta                 = Column(String())
    #unit                = Column(String())
    #mode                = Column(String())
    #final_destination   = Column(String())
    #next_bus_minutes    = Column(String())
    #next_bus_time       = Column(String())
    #vehicle_no          = Column(String())
    #route_number        = Column(String())
    #route_d_unknown     = Column(String())

    id                  = Column(Integer, primary_key=True)
    vehicle             = Column(Integer())
    stop_id             = Column(Integer())
    eta                 = Column(Integer())
    minutes             = Column(Integer())
    next_bus_minutes    = Column(Integer())
    final_destination   = Column(String())
    val_mode            = Column(String())
    route_number        = Column(String())
    val_pu              = Column(String())
    val_rd              = Column(String())
    
    
    def __str__(self):
        return "CTAArrival <id [{id}] vehicle [{vehicle}] route_number [{route_number}] stop_id [{stop_id}] minutes [{minutes}] val_pu [{val_pu}] eta [{eta}] final_destination [{final_destination}] next_bus_minutes [{next_bus_minutes}] val_mode [{val_mode}] val_rd [{val_rd}] > ".format(         
                  id                =self.id, 
                  vehicle           =self.vehicle,
                  route_number      =self.route_number,
                  stop_id=          self.stop_id,
                  minutes           =self.minutes,
                  val_pu            =self.val_pu,
                  eta               =self.eta, 
                  final_destination =self.final_destination,
                  next_bus_minutes  =self.next_bus_minutes,
                  val_mode          =self.val_mode,
                  val_rd            =self.val_rd)

        return "CTAArrival <id [{id}] eta [{eta}] unit [{unit}] final_destination [{final_destination}] next_bus_minutes [{next_bus_minutes}] next_bus_time [{next_bus_time}] mode [{mode}] vehicle_no [{vehicle_no}] route_number [{route_number}] unknown [{route_d_unknown}] > ".format(         
                  id=self.id, 
                  eta=self.eta, 
                  unit=self.unit,
                  mode=self.mode,
                  final_destination=self.final_destination,
                  next_bus_minutes=self.next_bus_minutes,
                  vehicle_no=self.vehicle_no,
                  route_number=self.route_number,
                  route_d_unknown=self.route_d_unknown,
                  next_bus_time=self.next_bus_minutes)

