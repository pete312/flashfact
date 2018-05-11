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





class CTAData():
    id  = Column(Integer, primary_key=True)
    vehicle_no = Column(Integer)
    
    def __str__(self):
        return "DailyFXData <id [{0}] date [{1}] time [{2}] currency [{3}] event [{4}]> ".format( self.id, 
                 self.ev_date, 
                 self.ev_time,
                 self.currency,
                 self.event_text,
                 self.previous,
                 self.forcast)

