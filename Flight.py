from opensky_api import OpenSkyApi
import pandas as pd 
import numpy as np 

class Flight() :
    
    def __init__(self) :
        
        self.column = ['baro_altitude',    'callsign'  ,   'geo_altitude',    'heading', 'icao24',    'last_contact',    'latitude',    'longitude',    'on_ground',    'origin_country',    'position_source',    'sensors',    'spi',    'squawk',    'time_position',    'velocity',     'vertical_rate']
        self.data =  pd.DataFrame(columns=self.column)
         # API
        self.api = OpenSkyApi("yassineatmk","bjproject")
    
    # Lon , Lat Converter To X and Y    
    def converter(self,lon,lat):
        
        k = 6378137
        x= lon * (k * np.pi/180.0)
        y= np.log(np.tan((90 + lat) * np.pi/360.0)) * k
        
        return x,y
    
    # Flights Data Farame Loader ( API :  opensky-network.org )  
    def update_data(self , near = False , lon = 0 , lat = 0) :
        self.data = self.data[0:0]
        baro_altitude = []
        callsign = []
        geo_altitude = []
        heading = []
        icao24 = []
        last_contact = []
        latitude = []
        longitude = []
        on_ground = []
        origin_country = []
        position_source = []
        sensors = []
        spi = []
        squawk = []
        time_position = []
        velocity = []
        vertical_rate = []
        
        try :
           
            # bbox = (min latitude, max latitude, min longitude, max longitude)
            if near :
                states = self.api.get_states( bbox=( lat - 2    ,   lat + 2    ,  lon - 2    ,   lon + 2  ))
            else :
                states = self.api.get_states( )

            for s in states.states:
                baro_altitude.append(s.baro_altitude)
                callsign.append(s.callsign)
                geo_altitude.append(s.geo_altitude)
                heading.append(s.heading)
                icao24.append(s.icao24)
                last_contact.append(s.last_contact)
                latitude.append(s.latitude)
                longitude.append(s.longitude)
                on_ground.append(s.on_ground)
                origin_country.append(s.origin_country)
                position_source.append(s.position_source)
                sensors.append(s.sensors)
                spi.append(s.spi)
                squawk.append(s.squawk)
                time_position.append(s.time_position)
                velocity.append(s.velocity)
                vertical_rate.append(s.vertical_rate)
                
            self.data["baro_altitude"] = baro_altitude
            self.data["callsign"] = callsign
            self.data["geo_altitude"] = geo_altitude
            self.data["heading"] = heading
            self.data["icao24"] = icao24
            self.data["last_contact"] = last_contact
            self.data["latitude"] = latitude
            self.data["longitude"] = longitude
            self.data["on_ground"] = on_ground
            self.data["origin_country"] = origin_country
            self.data["position_source"] = position_source
            self.data["sensors"] = sensors
            self.data["spi"] = spi
            self.data["squawk"] = squawk
            self.data["time_position"] = time_position
            self.data["velocity"] = velocity
            self.data["vertical_rate"] = vertical_rate
            self.data['rot_angle'] = self.data['heading']*-1
            self.data['url']= 'https://upload.wikimedia.org/wikipedia/commons/1/17/Plane_icon_nose_up.svg'
            
            self.data["x"] , self.data["y"] = self.converter( self.data["longitude"] ,self.data["latitude"]) 

            self.data = self.data.fillna('No Data')
            
            print( "Flights Updated" )
        except :         
            print("Time Out APi : opensky-network.org , Please Wait")

        
        
    # Destroy Object
    def __del__(self):
        print("Flight Destroyed")  

# Main function
def main() :

    f = Flight()
    f.update_data()
    print(f.data) 
    print("Done !!")
    
# call the main ( Stand alone mode)
if __name__ == "__main__" :
    main()

        
