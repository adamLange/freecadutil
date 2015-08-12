import Involute
import numpy as np

align = -10.0*np.pi/180.0
center = FreeCAD.Vector(-0.44,25.82,0)
# 14.5 deg contact angle
db = 0.645 * 25.4

def drawInv(db,center,alignmentAngle):
    x,y = Involute.involutePts(db/2.0,align,np.pi/180.0*20.0,25)
    for i in range(len(x)):
        v = FreeCAD.Vector(x[i],y[i],0) + center
        Part.show(Part.Point(x[i],y[i]).toShape())
