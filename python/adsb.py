import pandas
import numpy as np
from math import *
import PlaneFxns as PF
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

header = ['MSG',
          'Transmission Type',
          'System-generated SessionID',
          'System-generated AircraftID',
          'HexIdent',
          'System-generated Flight ID',
          'Date message generated',
          'Time message generated',
          'Date message logged', 
          'Time message logged',
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
#NOAO
lat0 =  np.radians(32.233)
lon0 =  np.radians(-110.948)
alt0 = 2643 * 0.3048
#Cerro Pachon
lat0 =  np.radians(-30.2517)#        -30.677*radcon
lon0 =  np.radians(-70.7382)#                            -70.928*radcon
alt0 = 2715

# 30deg circle                                                                                    
r = 1
q = np.radians(np.linspace(0,360)) # array of degrees for plotting                                 
dis = r * cos(np.radians(30))      # radial distance to airplanes in sky at 30                     
h = r * sin(np.radians(30))        # high to airplanes in skay at 30                               
h = np.linspace(h, h, len(q))      # array of heights for plotting                                 
X = dis * np.sin(q)                # X value of radial distance                                 
Y = dis * np.cos(q)                # Y value of radial distance                           

### Import data ###                                                                                
data = PF.dat2pan('../outback290715.csv')
#data = PF.dat2pan('./out_collect.csv')                                                            
hid ="#" + pandas.Series(data.HexIdent)

### Plotting ###

fig = plt.figure()
plt.scatter(data.Long, data.Lat, color= hid)
plt.plot(np.degrees(lon0), np.degrees(lat0), '*', color = 'red') # Antenna Location
plt.xlabel('Longitude')
plt.ylabel('Latitude')
#plt.xlim(-74,-70)
#plt.ylim(-32,-29)
plt.title('Geographic Coords 2D')
#plt.savefig('GeoCoords2D.pdf',bbox_inches='tight')

fig = plt.figure()
plt.plot(X,Y)
plt.scatter(-data.y, data.x, color = hid)
plt.plot(0, 0, '*', color = 'red')
plt.xlim(-r, r)
plt.ylim(-r, r)
plt.xlabel('W - E')
plt.ylabel('S - N')
plt.title('Local Horizon 2D')
#plt.savefig('LocalHorizon2D.pdf',bbox_inches='tight')

fig = plt.figure()
ax2 = fig.add_subplot(111, projection = '3d') # 3d spatial                                         
ax2.scatter(data.Long, data.Lat, data.Altitude, c = hid, linewidth = 0.1)
ax2.scatter(np.degrees(lon0), np.degrees(lat0), alt0, color = 'red')
ax2.set_zlim(0)
ax2.view_init(5,-80)
ax2.set_xlabel('Longitude')
ax2.set_ylabel('Latitude')
ax2.set_zlabel('Elevation (m)')
ax2.set_title('Geographic Coords 3D')

fig = plt.figure()
ax3 = fig.add_subplot(111, projection = '3d') # 3d sphere   
ax3.plot(X,Y,h)
ax3.scatter(data.x, data.y, data.z, c = hid, linewidth = 0.1)
ax3.set_xlim(-r,r)
ax3.set_ylim(-r,r)
ax3.set_zlim(0,1)
ax3.view_init(30,-160)
ax3.set_xlabel('E - W')
ax3.set_ylabel('N - S')
ax3.set_zlabel('z')
ax3.set_title('Local Horizon 3D')

### Plane Stats ###                                                                                     
Hour = PF.PlaneperHour(data)
data['Hour'] = Hour
Nightdata = (data[data.Hour < 6], data[data.Hour >= 18])
Nightdata = pandas.concat(Nightdata)
Daydata = data[data.Hour >= 6]
Daydata = Daydata[Daydata.Hour <18]

# Night v Day                                                                                           
binnum = 60
cmaptype = plt.cm.Greys

fig = plt.figure()
plt.hist2d(-Daydata.y,Daydata.x,bins=(binnum,binnum),norm = mpl.colors.LogNorm(), cmap=cmaptype)
plt.colorbar()
#plt.title('Day Frequency')
plt.xlim(-1,1)
plt.ylim(-1,1)
plt.plot(X,Y)
#plt.savefig('DayFreq2DHist.png',bbox_inches='tight')

fig = plt.figure()
plt.hist2d(-Nightdata.y,Nightdata.x,bins=(binnum, binnum),norm = mpl.colors.LogNorm(), cmap=cmaptype)
plt.colorbar()
#plt.title('Night Frequency')
plt.xlim(-1,1)
plt.ylim(-1,1)
plt.plot(X,Y)
#plt.savefig('NightFreq2DHist.pdf',bbox_inches='tight')

# 2d hist of sky    
fig = plt.figure()
plt.hist2d(-data.y,data.x,bins=(binnum,binnum),norm = mpl.colors.LogNorm(), cmap=cmaptype)
plt.xlabel('E - W')
plt.ylabel('S - N')
#plt.title('2D Histogram of Total Received Signals')
plt.xlim(-1,1)
plt.ylim(-1,1)
plt.plot(0,0,'*',color='red')
plt.colorbar()
plt.plot(X,Y)
#plt.savefig('TotSign2DHist.pdf',bbox_inches='tight')

# Planes above altitude degree night/day (sanity check)                                                                          
binnum = 24                                                                                     
Data10      = PF.PlaneperSlice(10,90,data)                                                         
Daydata10   = PF.PlaneperSlice(10,90,Daydata) 
Nightdata10 = PF.PlaneperSlice(10,90,Nightdata) 
Hour10      = PF.PlaneperHour(Data10)
DayHour10   = PF.PlaneperHour(Daydata10)
NightHour10 = PF.PlaneperHour(Nightdata10)

fig = plt.figure()
ax0 = fig.add_subplot(131)
ax1 = fig.add_subplot(132)
ax2 = fig.add_subplot(133)
ax0.hist(Hour10,bins=binnum)
ax1.hist(DayHour10,bins=12)
ax2.hist(NightHour10,bins=24)
ax0.set_xlim(0,23)
ax1.set_xlim(0,23)
ax2.set_xlim(0,23)
fig.subplots_adjust(wspace = 0.5)
#plt.savefig('DayvNightHist.pdf',bbox_inches='tight')

# Planes above altitude degree                                                                          
testdeg = (10,30,45,60)                                                                           
for i in testdeg:                                                                                 
    Datatest = PF.PlaneperSlice(i,90,data)                                                        
    Hourtest = PF.PlaneperHour(Datatest)                                                         
    fig = plt.figure()                                                                            
    plt.hist(Hourtest,log="True",bins=24)                                                          
    plt.title("Planes Above "+ str(i)+ " Degrees")                                                 
    plt.ylabel("Number of Received Signals")                                                       
    plt.xlabel("Hour")                                                                    
    plt.xlim(0,23) 
    plt.ylim(1,50000)
    #plt.savefig('PlanesAbove'+str(i)+".pdf",bbox_inches='tight')

# alt/az plot of signals

fig = plt.figure()
plt.scatter(np.degrees(data.Az),np.degrees(data.Al),color=hid)
plt.xlim(-180,180)
plt.ylim(0,90)
plt.xlabel('Azimuth (degrees)')
plt.ylabel('Altitude (degrees)')
#plt.title('Raw Alt/Az with HexIds')
#plt.savefig('AltAzwHID.pdf',bbox_inches='tight')

# 2d hist of sky alt/az                                                                           

fig = plt.figure()
plt.hist2d(np.degrees(data.Az),np.degrees(data.Al),bins=(73,19),norm = mpl.colors.LogNorm(), cmap=cmaptype)
plt.xlabel('Azimuth (degrees)')
plt.ylabel('Altitude (degrees)')
#plt.title('2D Histogram of Total Received Signals (Alt/Az)')
plt.xlim(-180,180)
plt.ylim(0,90)
plt.plot(0,0,'*',color='red')
plt.colorbar()
#plt.savefig('TotSignAltAz2DHist.pdf',bbox_inches='tight')
