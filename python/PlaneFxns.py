#!/usr/bin/python

######################################

def dat2pan(filename):
    import pandas
    import numpy as np
    from math import *
    header = ['MSG',
                        'Transmission Type',
                        'System-generated SessionID',
                        'System-generated AircraftID',
                        'HexIdent',
                        'System-generated Flight ID',
                        'DateMessagGenerated',
                        'TimeMessageGenerated',
                        'DateMessageLogged',
                        'TimeMessageLogged',
                        'Callsign',
                        'Altitude',
                        'GroundSpeed',
                        'Track',
                        'Lat',
                        'Long',
                        'VerticalRate',
                        'Squawk',
                        'Alert',
                        'Emergency',
                        'SPI',
                        'IsOnGround',
                        ]
    ### Constants ###
    radcon = pi/180
    R = 6.371e6    # Radius of the Earth (m)
    # NOAO
    lat0 =   32.233*radcon
    lon0 = -110.948*radcon
    alt0 = 2643 * 0.3048
    # Cerro Pachon
    lat0 =  -30.677*radcon
    lon0 =  -70.928*radcon
    alt0 = 2715
    ### Data ###
    alldata = pandas.read_csv(filename,names=header)
    data = alldata[alldata.Lat.notnull()]
    Lat = np.radians(pandas.Series(data.Lat))
    Lon = np.radians(pandas.Series(data.Long))
    Alt = pandas.Series(data.Altitude)
    ### Converting geographical coords to horizontal ###
    dLat = Lat - lat0
    dLon = Lon - lon0
    dAlt = Alt - alt0
    a = np.sin(dLat/2)**2 + cos(lat0) * np.cos(Lat) * np.sin(dLon/2)**2
    d = R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    Al = np.arctan2(Alt, d)
    north = np.sin(dLon) * np.cos(Lat)
    east  = cos(lat0) * np.sin(Lat) - sin(lat0) * np.cos(Lat) * np.cos(dLon)
    Az = np.arctan2(north, east)
    ### 3D coords ###
    r = 1
    x = r * np.cos(Al) * np.cos(Az)
    y = r *-np.cos(Al) * np.sin(Az)
    z = r * np.sin(Al)
    data['Al'] = Al; data['Az'] = Az; data['x'] = x;data['y'] = y; data['z'] = z;
    return data

######################################

def PlaneperSlice(minDeg,maxDeg,inputdata):
    import numpy as np
    Slicedata = inputdata[inputdata.Al >= np.radians(minDeg)]; Slicedata = Slicedata[Slicedata.Al <= np.radians(maxDeg)]
    return Slicedata

######################################

def PlaneperHour(inputdata2):
    Time = inputdata2.TimeMessageLogged
    Hour = [elem[:2] for elem in Time]
    Hour = [float(i) for i in Hour]
    return Hour
