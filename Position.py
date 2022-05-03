import numpy as np 
import requests 
import pandas as pd
import os


class Position () :
    
    def __init__(self) :
        # API
        self.token  = "cd0246f867819d"
        self.api = f"https://ipinfo.io?token={self.token}"
        self.res =  None 
        
        #  Map Location Initialization
        self.start_lon_min  ,    self.start_lat_min =    -14   ,   29
        self.start_lon_max  ,    self.start_lat_max =   -4    ,   34 
        
        self.x_start_range , self.y_start_range = None , None
        self.start_range()
        
        
        #  My Location Variables
        self.lon , self.lat = None , None 
        
        # Data Holder   
        self.column = ['latitude' ,'longitude'  ,'x' ,'y'  ,'rot_angle' ,'city', 'region', 'origin_country',"callsign",  "velocity","baro_altitude","url"]
        self.data = pd.DataFrame(columns = self.column)
        
    def request(self) :
        self.res = requests.get(self.api).json()
    
    # Lon , Lat Converter To X and Y 
    def converter(self, lon , lat):
        
        k = 6378137
        x= lon * (k * np.pi/180.0)
        y= np.log(np.tan((90 + lat) * np.pi/360.0)) * k
        
        return x,y
    
    # Map Location Initialization After converting ( Lon , Lat ) to ( X , Y ) 
    def start_range(self): 
           
        xy_min = self.converter(self.start_lon_min,self.start_lat_min)
        
        xy_max = self.converter(self.start_lon_max,self.start_lat_max)
        
        self.x_start_range , self.y_start_range = ([xy_min[0],xy_max[0]] , [xy_min[1],xy_max[1]])
     
    
    # My Location Initializer ( Latitude , Longitude) ( API :  ipinfo.io )
    def coordination(self) :
        
        self.request()
        temp = self.res["loc"].split(",")  
        self.lat , self.lon   =  float(temp[0]) , float(temp[1])
    
    # My Location Data Farame Loader ( API :  ipinfo.io )
    def update_data(self) :
        
        self.data = self.data[0:0]
        self.request()

        self.data['city']  =   [ self.res["city"]  ] 
        self.data['region']  =  [self.res["region"]]   
        self.data['origin_country']  = [  self.res["country"]]
        self.data['rot_angle']  = [0]  
        lat,lon =  self.res ["loc"].split(",")
        self.lat , self.lon  = float( lat ) , float( lon )
        self.data['latitude']  = [ float(lat )]  
        self.data['longitude']  = [float(lon )]  
        
        self.data['callsign']  = ["Our Plane"]   
        self.data['velocity']  =   ["+∞"]  
        self.data['baro_altitude']  = ["+∞"]    
        
        self.data["x"] , self.data["y"] = self.converter(self.data['longitude'] , self.data['latitude']   )
        
        # https://upload.wikimedia.org/wikipedia/commons/d/d1/Google_Maps_pin.svg
        # url =  os.path.join(os.path.dirname(__file__), 'static', 'position_icon.png')
        # url =  "/app/static/position_icon.png"
        # self.data['url']  = ["./assets/position_icon.svg" ]  
        self.data['url']  = ["https://upload.wikimedia.org/wikipedia/commons/d/d1/Google_Maps_pin.svg" ]  

        self.data = self.data.fillna('No Data')
        
        print( "Location Updated" )
    
    # Destroy Object
    def __del__(self):
        print("Position Destroyed")  

# Main function
def main() :
    p = Position()
    p.update_data()
    print(p.data)
    p.coordination()
    print(p.lon , p.lat)
    print("Done !!")
    
    
# call the main ( Stand alone mode)
if __name__ == "__main__" :
    main()


    