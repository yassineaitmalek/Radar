# Yassine ATMK

# needed libraries

# pip intall bokeh
# pip install numpy
# pip install pandas
# pip install opensky_api


from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure
from bokeh.models import HoverTool,LabelSet,ColumnDataSource
from bokeh.models.widgets import Button 
from bokeh.layouts import row
from bokeh.events import ButtonClick , DoubleTap
from bokeh.tile_providers import get_provider,CARTODBPOSITRON



from Position import Position
from Airport import Airport
from Flight import Flight


class Radar():
    
    def __init__(self,mode):
        
        # The Server 
        self.apps = {'/': Application(FunctionHandler( self.track ))}
        self.server = Server(self.apps , port=8080)
        
        # API Objects
        self.position = Position()
        self.airport = Airport()
        self.flight = Flight()
        
        self.running = False
        
        #  Modes  Booleans 
        self.my_location = False 
        self.near_airport = False
        self.near_flight = False
        self.airports = False
        self.flights = False
        
        #  Mode String
        self.mode = mode
     
        
                         
        #  Data Sources for the graph and Hovers
        
        # flight data source & hover
        self.flight_source = ColumnDataSource({
                                            'baro_altitude' : [] ,'callsign' : [] ,'geo_altitude' : [] ,'heading' : [] ,
                                            'icao24' : [] ,'last_contact' : [] ,'latitude' : [] ,'longitude' : [] ,'on_ground' : [] ,
                                            'origin_country' : [] ,'position_source' : [] ,'sensors' : [] ,'spi' : [] ,'squawk' : [] ,'time_position' : [] ,
                                            'velocity' : [] ,'vertical_rate' : [] ,'rot_angle' : [] ,'url' : [] ,'x' : [] ,'y' : [] 
                                        })
        self.flight_hover = HoverTool()
    
        
        # position data source & hover
        self.position_source = ColumnDataSource({
                                            'latitude' : [] ,'longitude' : [] ,'x' : [] ,'y' : [] ,'rot_angle' : [] ,
                                            'city': [], 'region': [], 'origin_country': [] ,'callsign':[],  "velocity":[],"baro_altitude":[],"url":[]
                                        })
        self.position_hover = HoverTool()

        # airport data source & hover
        self.airport_source = ColumnDataSource({
                                            'id':[],'ident':[],'type':[],'name':[],'latitude_deg':[],'longitude_deg':[],'elevation_ft':[],'continent':[],
                                            'iso_country':[],'iso_region':[],'municipality':[],'scheduled_service':[],'gps_code':[],'iata_code':[],'local_code':[],
                                            'home_link':[],'wikipedia_link':[],'keywords':[],'x':[],'y':[],'url':[],'d':[],"rot_angle":[],"d" :[]
                                        })
        self.airport_hover = HoverTool()
        
        # distance data source & hover
        self.distance_source = ColumnDataSource(data=dict(x=[], y=[],dist=[])) 
        self.distance_hover = HoverTool()
        self.coordList = []
        
        # empty map
        self.plan   =   figure(
                        x_range = self.position.x_start_range   ,   y_range = self.position.y_start_range   ,x_axis_type = 'mercator' ,
                        y_axis_type = 'mercator'  ,     sizing_mode = 'scale_width' ,   plot_height = 270 
                      )
        
        # map Action listner
        self.plan.on_event(DoubleTap, self.draw_line_listener)
        
        # Map Type
        self.tile_prov   =  get_provider(CARTODBPOSITRON)
        self.plan.add_tile(self.tile_prov,level='image')
      
        # Buttons
        self.width = 175
        self.allflights_bt  = Button(label = "ALL FLIGLHTS",button_type = "success", max_width = self.width)
        self.allflights_bt.on_event(ButtonClick, self.allflights_listener)

        self.allairports_bt  = Button(label = "ALL AIRPORTS",button_type = "success", max_width = self.width)
        self.allairports_bt.on_event(ButtonClick, self.allairports_listener)

        self.my_location_bt  = Button(label = "MY LOCATION",button_type = "success", max_width = self.width)
        self.my_location_bt.on_event(ButtonClick, self.my_location_listener)
            
        # self.stop_bt  = Button(label = "STOP",button_type = "danger", max_width = self.width)
        # self.stop_bt.on_event(ButtonClick, self.stop_listener)
        
        self.map_bt  = Button(label = "MAP",button_type = "warning", max_width = self.width)
        self.map_bt.on_event(ButtonClick, self.map_listener)
        
        self.nearfl_bt  = Button(label = "NEAR FLIGHTS",button_type = "success", max_width = self.width)
        self.nearfl_bt.on_event(ButtonClick, self.nearflights_listener)
        
        self.nearap_bt  = Button(label = "NEAR AIRPORT",button_type = "success" , max_width = self.width)
        self.nearap_bt.on_event(ButtonClick, self.nearairport_listener)
        
        self.nearflap_bt  = Button(label = "NEAR FLIGHTS & AIRPORT",button_type = "success" , max_width = (self.width + 30))
        self.nearflap_bt.on_event(ButtonClick, self.near_flights_aiport_listener)
        
        self.clearline_bt  = Button(label = "CLEAR LINES",button_type = "default" , max_width = self.width)
        self.clearline_bt.on_event(ButtonClick, self.clearline_listener)
        
    
        
    
    # Data sources cleaner : Flight , Airport , Position
    def clear_data(self) :
        self.position_source.data = {k: [] for k in self.position_source.data}
        self.airport_source.data = {k: [] for k in self.airport_source.data}
        self.flight_source.data = {k: [] for k in self.flight_source.data}
        
    # Data source cleaner :  Distance   
    def clearline_listener(self,event) :
        self.coordList = []
        self.distance_source.data = {k: [] for k in self.distance_source.data}
    
    # Listeners 
    def draw_line_listener(self,event) :
        if len(self.coordList) >= 1 :
            d = ( ((event.x - self.coordList[-1][0])**(2) + (event.y - self.coordList[-1][1])**(2))**(0.5) ) / 1000
            Coords  =   [event.x , event.y , d]
            
        
        else :
             Coords  =   [event.x , event.y , 0]
             
        self.coordList.append(Coords)
        if ( len(self.coordList) > 1 ) and (self.coordList[0][2] == 0 ) :
            self.coordList[0][2] = self.coordList[1][2]
  
        self.distance_source.data = dict(x=[i[0] for i in self.coordList], y=[i[1] for i in self.coordList] ,dist=[i[2] for i in self.coordList] )
      
      
    def allflights_listener(self,event):
        self.clear_data()
        self.mode = "flights"
        self.modes()
    

    def nearflights_listener(self,event):
        
        self.clear_data()
        self.mode = "near_flights"
        self.modes()
        

    def stop_listener(self,event):
        self.clear_data()
        print('Mode : STOP')
        self.stop()
        
           
    def allairports_listener(self,event):
        self.clear_data()
        self.mode = "airports"
        self.modes()


    def nearairport_listener(self,event):   
        self.clear_data()
        self.mode = "near_airport"
        self.modes()
  
    
    def my_location_listener(self ,event ) :  
        self.clear_data()
        self.mode = "my_location"
        self.modes()
      
      
    def near_flights_aiport_listener(self ,event ) :   
        self.clear_data()
        self.mode = "near_flights_aiport"
        self.modes()
    
    
    def map_listener(self ,event ) :
        self.clear_data()
        self.mode = "map"
        self.modes()
    
   
    # Mode Initializer
    def modes(self) :
        
        if self.mode == "my_location" : 
            self.my_location = True
            self.near_airport = False
            self.airports = False
            self.near_flight = False
            self.flights = False
            print("Mode : MY LOCATION") 
            
        elif self.mode == "near_airport" : 
            self.my_location = True
            self.near_airport = True
            self.airports = False
            self.near_flight = False
            self.flights = False
            print("Mode : NEAR AIRPORT") 
            
        elif self.mode == "near_flights" : 
            self.my_location = True
            self.near_flight = True
            self.near_airport = False
            self.airports = False
            self.flights = False
            print("Mode : NEAR FLIGHTS ") 
            
        elif self.mode == "airports" :
            self.airports = True
            self.my_location = False
            self.near_airport = False
            self.near_flight = False
            self.flights = False
            print("Mode : ALL AIRPORTS") 
            
        elif self.mode == "flights":
            self.flights = True
            self.airports = False
            self.my_location = False
            self.near_airport = False
            self.near_flight = False
            print("Mode : ALL FLIGHTS ") 
            
        elif self.mode == "near_flights_aiport" :
            self.my_location = True
            self.near_airport = True
            self.near_flight = True
            self.flights = False
            self.airports = False
            print("Mode : NEAR FLIGHTS & AIRPORT") 
            
        elif self.mode == "map" : 
            self.flights = False
            self.airports = False
            self.my_location = False
            self.near_airport = False
            self.near_flight = False
            print("Mode : MAP") 
        
        else :
            raise Exception("Service Type Does Not Exist")
        


    #  Update Data and ReLoad
    def update(self):
        
        if self.my_location :
            
            self.position.update_data() 
            n_roll_1 = len(self.position.data.index)
            self.position_source.stream(self.position.data.to_dict(orient='list') , n_roll_1)
            
            
        if self.near_flight or self.flights :
            if self.near_flight :
                self.flight.update_data(True , self.position.lon , self.position.lat)
            else :
                self.flight.update_data()
            
            n_roll_2 = len(self.flight.data.index)
            self.flight_source.stream(self.flight.data.to_dict(orient='list'),n_roll_2)
        
        
        if self.near_airport or self.airports :
            
            if self.airports :
                self.airport.update_data()
            if self.near_airport : 
               self.airport.update_data(True , self.position.lon , self.position.lat)
                
            n_roll_3=len(self.airport.data.index)
            self.airport_source.stream(self.airport.data.to_dict(orient='list'),n_roll_3)
            
    
    
    # The main CallBack 
    def track(self,doc):
        
        # Calling Update every 10s
        doc.add_periodic_callback( self.update   , 10000) 
        
        # img_url ==> show icons as imgs
        # circle  ==> Draw litle points on the map in the imgs because hover does not support image_url
        # lable   ==>  the name that appears on top of each point on the map
        
        #  Position
        self.plan.image_url(
                        url="url"   , x='x' ,   y='y'   ,   source=self.position_source  ,   anchor='center',
                        angle_units='deg'   ,   angle='rot_angle'   ,   h_units='screen'    ,   w_units='screen'    ,   w=30    ,h=30
                        
                    )
        pme = self.plan.circle('x','y',source=self.position_source,fill_color='red',hover_color='red',size=5,fill_alpha=0.8,line_width=0) #
        
        labelsme = LabelSet(
                        x='x'   , y='y' , text='callsign'   ,   level='glyph' ,   x_offset=5 ,    y_offset=5,    
                        
                        source=self.position_source  ,   render_mode='canvas',     background_fill_color='white',  text_font_size="8pt"
                    )
        self.position_hover.renderers = [pme]
        self.position_hover.tooltips = [
                            ('Call sign','@callsign')       ,   ('Origin Country','@origin_country'),
                            ('velocity(m/s)','@velocity')   ,   ('Altitude(m)','@baro_altitude')
                            ]
    
        
        self.plan.add_layout(labelsme)
        self.plan.add_tools(self.position_hover)
        
        # Airport
        self.plan.image_url(
                    url="url"   , x='x' ,   y='y'   ,   source=self.airport_source  ,   anchor='center',
                    angle_units='deg'   ,   angle='rot_angle'   ,   h_units='screen'    ,   w_units='screen'    ,   w=30    ,h=30
                    
                )
        pap = self.plan.circle('x','y',source=self.airport_source,fill_color='blue',hover_color='blue',size=5,fill_alpha=0.8,line_width=0)
        
        labelsap = LabelSet(
                        x='x'   , y='y' , text='name'   ,   level='glyph' ,   x_offset=5 ,    y_offset=5,    
                        
                        source=self.airport_source  ,   render_mode='canvas',     background_fill_color='white',  text_font_size="8pt"
                    )
        
        self.airport_hover.renderers = [pap]
        self.airport_hover.tooltips = [
                            ('Name','@name')       ,   ('Country','@iso_country'),
                                ('Municipality','@municipality'),('Type','@type')   
                            ]
    
        
        self.plan.add_layout(labelsap)
        self.plan.add_tools(self.airport_hover)
        
    
        # Flight
        self.plan.image_url(
                        url="url"   , x='x' ,   y='y'   ,   source=self.flight_source  ,   anchor='center',
                        angle_units='deg'   ,   angle='rot_angle'   ,   h_units='screen'    ,   w_units='screen'    ,   w=30    ,h=30
                        
                    )
        pfl = self.plan.circle('x','y',source=self.flight_source,fill_color='black',hover_color='black',size=5,fill_alpha=0.8,line_width=0)
    
        labelsfl = LabelSet(
                                x='x'   , y='y' , text='callsign'   ,   level='glyph' ,   x_offset=5 ,    y_offset=5,    
                                
                                source=self.flight_source  ,   render_mode='canvas',     background_fill_color='white',  text_font_size="8pt"
                            )
        
        self.flight_hover.renderers = [pfl]
        self.flight_hover.tooltips = [
                            ('Call sign','@callsign')       ,   ('Origin Country','@origin_country'),
                            ('velocity(m/s)','@velocity')   ,   ('Altitude(m)','@baro_altitude')
                            ]
    
        
        self.plan.add_layout(labelsfl)
        self.plan.add_tools(self.flight_hover)
    
        # Distance
        pl = self.plan.line('x','y',source=self.distance_source,line_width=6, line_alpha=0.6)
        self.distance_hover.renderers = [pl]
        self.distance_hover.tooltips = [
                            ("Distance in KM " , ("@dist"))
                            
                            ]
        self.plan.add_tools(self.distance_hover)
        
        
        # the Title and  Content of the WebPage   
        doc.title ='Radar'
        doc.add_root(self.plan)
        doc.add_root(   
                        row  (      
                                self.allflights_bt , self.allairports_bt , self.my_location_bt , self.nearfl_bt , self.nearap_bt , 
                                self.nearflap_bt , self.clearline_bt , self.map_bt 
                                
                              )   
                    )
        
        
        
            
     
    #  Starting The Server   
    def start(self):
        
        print("Server Started")
        print("http://localhost:"+str(self.server.port))
        self.running = True
           
        # service Mode Initialization
        self.modes()
        # open Browser to localhost:port
        self.server.show("/")
        # starting the loop
        self.server._loop.start()
        
        
    # Stopping the Server
    def stop(self) :
     
        self.server.unlisten()
        # stopping the loop
        self.server._loop.stop()
        
        self.running = False
        print("Server Stoped")
        
        
    # Destroy Object
    def __del__(self):
        print("Radar Destroyed")  

# Main function
def main() :
    
    r = Radar("map")
    r.start()
    del r
    print("END .....")
    
# call the main ( Stand alone mode)
if __name__ == "__main__" :
    main()

