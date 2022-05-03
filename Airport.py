import numpy as np 
import pandas as pd
import os
import sys


class Airport () :
    
    def __init__(self) :
        self.data = None
    
    # Lon , Lat Converter To X and Y 
    def converter(self, lon , lat):
        
        k = 6378137
        x= lon * (k * np.pi/180.0)
        y= np.log(np.tan((90 + lat) * np.pi/360.0)) * k
        
        return x,y
    
    #  Airport Data Frame Loader
    def update_data(self , near = False , lon = 0, lat = 0) :
        self.data = pd.read_csv(self.resource_path("assets\\airports.csv"))
        np.seterr(divide = 'ignore')
        self.data["x"] , self.data["y"] = self.converter(self.data["longitude_deg"] ,self.data["latitude_deg"])
        
        self.data['url'] = "https://upload.wikimedia.org/wikipedia/commons/6/65/OOjs_UI_icon_mapPin-progressive.svg"
        
        self.data["d"] = np.NaN
        
        if near :
            x,y = self.converter(lon,lat)
            self.data = self.data[ self.data["latitude_deg"].between(lat - 1 , lat + 1) ] 
            self.data = self.data[  self.data["longitude_deg"].between(lon - 1 , lon + 1 )]
            self.data["d"] = np.sqrt( (self.data["x"]-lon)**2 + (self.data["y"]-lat)**2)
            self.data = self.data[self.data.d == self.data.d.min()]
        else :
            self.data = self.data[self.data["type"] == "large_airport"]
        
        self.data['rot_angle'] = 0
        self.data = self.data.fillna('No Data')
        
        print( "Airport Updated" )
    
    
    def resource_path(self , relative_path):
                # """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
    # Destroy Object
    def __del__(self):
        print("Airplane Destroyed")  
    
# Main function
def main() :

    a = Airport()
    a.update_data(True , -9 , 30)
    print(a.data)
    a.update_data()
    print(a.data)
    print("Done !!")
    
# call the main ( Stand alone mode)
if __name__ == "__main__" :
    main()

        
    