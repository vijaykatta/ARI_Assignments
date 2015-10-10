# -*- coding: utf-8 -*-
"""
Created on Thu Oct 08 21:06:38 2015

@author: Vijay Katta/Student No: 15202724
Modified Date: Fri Oct 9 11:35 2015

"""
import sqlite3;
import pandas as pd;
import numpy as np;

conn = sqlite3.connect('c:\\sqlite\\renewable.db')

df_p = pd.read_sql_query('select long,lat from ports',conn)
df_l = pd.read_sql_query('select long,lat,production from location',conn)


# Distance by the Haversine formula
# https://en.wikipedia.org/wiki/Haversine_formula
def dist_from_coordinates(lat1, lon1, lat2, lon2):
    R = 6371 # Earth's radius in KM

    # convert to radians
    d_lat = np.radians(lat2-lat1)
    d_lon = np.radians(lon2-lon1)

    r_lat1 = np.radians(lat1)
    r_lat2 = np.radians(lat2)

    # argument under the root
    a = np.sin(d_lat/2.) **2 + np.cos(r_lat1) * np.cos(r_lat2) * np.sin(d_lon/2.)**2

    haversine = 2 * R * np.arcsin(np.sqrt(a))

    return haversine

#declare a list to store cost of port
totalcostofport = [0,0,0]

#Outer loop for each port
for i in df_p.index:
    #Inner loop - for each location
    for j in df_l.index:
        #call function to calculate distance
        distance = dist_from_coordinates(df_p.iat[i,0], df_p.iat[i,1],df_l.iat[j,0], df_l.iat[j,1])
        #calculate the cost of each location to port
        cost = distance * df_l.iat[j,2]
        #add the cost of all locations for each port
        totalcostofport[i] += cost
        
#get the index of least value of cost from the list totalcostofport
bestportindex= totalcostofport.index(min(totalcostofport))   
     
#print the co-ordinates of the port with least transportation cost
print 'Port with least/minimal transportation cost is @  (longitude,latitude) : %f,%f' %(df_p.iat[bestportindex,0],df_p.iat[bestportindex,1])


