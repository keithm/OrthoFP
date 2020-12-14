import os
import math
import numpy as np

class FlightPlan():

    def __init__(self,flightplan_file):
        self.flightplan_file = flightplan_file
        self.departure={}
        self.arrival={}
        self.waypoints=[]
        self.coords=[]
        self.read_flight_plan()


    def read_flight_plan(self):
        try:
            f=open(self.flightplan_file,'r')
            for line in f.readlines():
                line=line.strip()
                if not line: continue
                if line[0]=='#': continue
                if (line.count(' ') == 5):
                    (wptype, wpid, via, alt, lat, lon)=line.split()
                    self.waypoints.append({'wpid': wpid, 'alt': alt, 'lat': float(lat), 'lon': float(lon)})
            f.close()
        except:
            print("FP error: Could not read flight plan file " + self.flightplan_file)
            return 0

    def getCoords(self, pad=0):
        for coords in range(0,len(self.waypoints)-1):
            x_coords=np.array([self.waypoints[coords]['lon'],self.waypoints[coords+1]['lon']])
            y_coords=np.array([self.waypoints[coords]['lat'],self.waypoints[coords+1]['lat']])
            # test for vertical line
            if x_coords[0] != x_coords[-1]:
                for p in range(-pad, pad+1):
                    coefficients = np.polyfit(x_coords, y_coords+p, 1)
                    polynomial = np.poly1d(coefficients)
                    x_axis = np.arange(x_coords[0],x_coords[-1],1)
                    y_axis = polynomial(x_axis)
                    self.coords.extend(list(zip(np.floor(y_axis).astype(int), np.floor(x_axis).astype(int))))
            else:
                # vertical line
                for y in range(math.floor(y_coords[0]), math.floor(y_coords[1])):
                    for x in range(math.floor(x_coords[0]-pad),math.floor(x_coords[0]+pad+1)):
                        self.coords.extend(y,x)
        # Grids around airports with width = pad*2
        for coords in [(self.waypoints[0]['lon'],self.waypoints[0]['lat']),(self.waypoints[-1]['lon'],self.waypoints[-1]['lat'])]:
            x_axis = np.linspace(coords[0]-pad,coords[0]+pad,pad*2+1)
            y_axis = np.linspace(coords[1]-pad,coords[1]+pad,pad*2+1)
            x_coords, y_coords = np.meshgrid(x_axis, y_axis)
            self.coords.extend(list(zip(np.floor(y_coords.ravel()).astype(int),np.floor(x_coords.ravel()).astype(int))))
        self.coords = list(dict.fromkeys(self.coords))
        self.coords.sort(key=lambda tup: tup[1])
        return self.coords


            



