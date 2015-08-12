import Part
import FreeCAD
from FreeCAD import Vector as V
import numpy as np


def involutePoints(rb,theta,phiMax,nPts=100):
    phi = np.linspace(0.0,phiMax,nPts)
    l = rb*phi
    x = rb*np.cos(phi+theta)-l*np.cos(180.0-phi-theta)
    y = rb*np.sin(phi+theta)+l*np.sin(180.0-phi-theta)
    return x,y

align = -11.0*np.pi/180.0
center = V(-0.44,25.82,0)
# 14.5 deg contact angle
db = (2.0/3.0)*25.4*np.cos(14.5*np.pi/180.0)

def drawInvToFreeCAD(db,center,alignmentAngle):
    x,y = involutePoints(db/2.0,alignmentAngle,np.pi/180.0*30.0,25)
    for i in range(len(x)):
        v = V(x[i],y[i],0) + center
        Part.show(Part.Point(v).toShape())

def drawMyInv():
    for i in np.linspace(0,np.pi*2.0,9):
        drawInvToFreeCAD(db,center,align+i)

def drawGearset():
    pressureAngle = 14.5*np.pi/180.0
    normal = V(0.0,0.0,1.0)
    pitch = 12.0 # teeth per inch

    pinionCenter = V(-4.875*25.4,0,107.0)
    pinionPitchRadius = 25.4*2/3.0
    pinionNTeeth = 8.0
    pinionAddendumRadius = pinionPitchRadius + (1 / pitch)*25.4
    pinionDedendumRadius = pinionPitchRadius - (1.25 / pitch)*25.4
    pinionBaseRadius = pinionPitchRadius * np.cos(pressureAngle)

    gearCenter = V(0,0,107.0)
    gearPitchRadius = (4.875 - pinionPitchRadius/25.4)*25.4
    gearNTeeth = 109.0
    gearAddendumRadius = gearPitchRadius + (1/pitch)*25.4
    gearDedendumRadius = gearPitchRadius - (1.25/pitch)*25.4
    gearBaseRadius = gearPitchRadius * np.cos(pressureAngle)

    d = FreeCAD.activeDocument()
    d.addObject("Part::Feature","pinionPitchCircle").Shape = (Part.Circle(pinionCenter,normal,pinionPitchRadius).toShape())
    d.addObject("Part::Feature","pinionAddendumCircle").Shape = (Part.Circle(pinionCenter,normal,pinionAddendumRadius).toShape())
    d.addObject("Part::Feature","pinionDedendumCircle").Shape = (Part.Circle(pinionCenter,normal,pinionDedendumRadius).toShape())

    d.addObject("Part::Feature","gearPitchCircle").Shape = (Part.Circle(gearCenter,normal,gearPitchRadius).toShape())
    d.addObject("Part::Feature","gearAddendumCircle").Shape = (Part.Circle(gearCenter,normal,gearAddendumRadius).toShape())
    d.addObject("Part::Feature","gearDedendumCircle").Shape = (Part.Circle(gearCenter,normal,gearDedendumRadius).toShape())


    #for i in np.linspace(0,np.pi*2.0-np.pi*2.0/8.0,8):
        
