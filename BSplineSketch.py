import Part
import numpy as np

from OCC.Geom import Geom_BSplineSurface, Handle_Geom_BSplineSurface
from OCC.TColgp import TColgp_Array2OfPnt
from OCC.TColStd import TColStd_Array1OfReal, TColStd_Array2OfReal, TColStd_Array1OfInteger
from OCC.gp import gp_Pnt, gp_Vec
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace

class InteractiveBSplineCurve:

    def __init__(self,sketch,**kwargs):
        self.sketch = sketch
        if "weights" in kwargs:
            self.weights = kwargs['weights']
        else:
            self.weights = False
        if "periodic" in kwargs:
            self.periodic = kwargs['periodic']
        else:
            self.periodic = False

    def getShape(self):
        points = []
        points.append(self.sketch.Geometry[0].StartPoint)
        for line in self.sketch.Geometry:
            points.append(line.EndPoint)

        bs = Part.BSplineCurve()

        if self.weights:
            weights = self.weights
        else:
            weights = [1.0]*len(points)

        bs.buildFromPolesMultsKnots(points,weights=weights,periodic=self.periodic)
        shape = bs.toShape()
        shape.Placement = self.sketch.Placement
        return shape

    def getPoles(self):
        points = []
        points.append(self.sketch.Geometry[0].StartPoint)
        for line in self.sketch.Geometry:
            points.append(line.EndPoint)
        return points

class InteractiveBSplineSurface:

    def __init__(self,sketchList,**kwargs):
        self.sketchList = sketchList
        self.uDegree = 2
        self.vDegree = 2
        self.uPeriodic = False
        self.vPeriodic = False
        self.uStartMultiplicity = 3
        self.vStartMultiplicity = 3
        self.uEndMultiplicity = 3
        self.vEndMultiplicity = 3

    def getPoles(self):
        poles = []
        poleSequence = []
        for sketch in self.sketchList:
            points = []
            geo = []
            for G in sketch.Geometry:
                if not G.Construction:
                    geo.append(G)
            vec = sketch.Placement.multVec(geo[0].StartPoint)
            points.append(vec)
            poleSequence.append(vec)
            for line in geo:
                vec = sketch.Placement.multVec(line.EndPoint)
                points.append(vec)
                poleSequence.append(vec)
            poles.append(points)
          
        n_u = len(poles[0])
        n_v = len(poles)
        return (poleSequence,n_u,n_v)

    def getShape(self):
        surf = Part.BSplineSurface()
        poles, n_u, n_v = self.getPoles()
        surf.buildFromPolesMultsKnots(poles,[1]*(n_u+1),[1]*(n_v+1))
        return surf

    def toPyOCC(self,dbg=False):
        poles,n_u,n_v = self.getPoles()

        Poles = TColgp_Array2OfPnt(1,n_u,1,n_v)
        for n,i in enumerate(poles):
            iu = n%n_u
            iv = n/n_u
            Poles.SetValue(iu+1,iv+1,gp_Pnt(i.x,i.y,i.z))
        
        weights = [1]*(n_u*n_v)
        Weights = TColStd_Array2OfReal(1,n_u,1,n_v)
        for n,i in enumerate(weights):
            iu = n%n_u
            iv = n/n_u
            Weights.SetValue(iu+1,iv+1,i)

        if not self.uPeriodic:
            n_increasing = (n_u + self.uDegree + 1) - (self.uStartMultiplicity-1) - (self.uEndMultiplicity-1)

        else:
            n_increasing = n_u + 1

        uknots = []
        uknots.extend(np.linspace(0,1.0,n_increasing).tolist())

        UKnots = TColStd_Array1OfReal(1,len(uknots))
        for n,i in enumerate(uknots):
            UKnots.SetValue(n+1,i)

        l = [self.uStartMultiplicity]
        m = [1]*(len(uknots)-2)
        r = [self.uEndMultiplicity]

        m.extend(r)
        l.extend(m)
        uMults = l

        UMults = TColStd_Array1OfInteger(1,len(uMults))
        for n,i in enumerate(uMults):
            UMults.SetValue(n+1,i)

        if not self.vPeriodic:
            n_increasing = (n_v + self.vDegree + 1) - (self.vStartMultiplicity-1) - (self.vEndMultiplicity-1)

        else:
            n_increasing = n_v + 1

        vknots = []
        vknots.extend(np.linspace(0,1.0,n_increasing).tolist())

        VKnots = TColStd_Array1OfReal(1,len(vknots))
        for n,i in enumerate(vknots):
            VKnots.SetValue(n+1,i)

        l = [self.vStartMultiplicity]
        m = [1]*(len(vknots)-2)
        r = [self.vEndMultiplicity]

        m.extend(r)
        l.extend(m)
        vMults = l

        VMults = TColStd_Array1OfInteger(1,len(vMults))
        for n,i in enumerate(vMults):
            VMults.SetValue(n+1,i)

        if dbg:
            return {'poles':poles,'weights':weights,'uknots':uknots,'vknots':vknots,'umults':uMults,'vmults':vMults,'udegree':self.uDegree,'vdegree':self.vDegree}
        #return (Poles,Weights,UKnots,VKnots,UMults,VMults,self.UDegree,self.vDegree,UPeriodic,VPeriodic)
        return Geom_BSplineSurface(Poles,Weights,UKnots,VKnots,UMults,VMults,self.uDegree,self.vDegree,self.uPeriodic,self.vPeriodic)

    def toFreeCADShape(self):
        surf = self.toPyOCC()
        hsurf = Handle_Geom_BSplineSurface(surf)
        facemaker = BRepBuilderAPI_MakeFace()
        facemaker.Init(hsurf,True,0.001)
        return Part.__fromPythonOCC__(facemaker.Face())

class RibMaker:

    def __init__(self,pointsList,l0,l1,l2):
        """
          l0, l1, and l2 are TopoDS_Edge

        """

        self.profileSketch = profileSketch

        self.l0 = Edge(l0)
        self.l1 = Edge(l1)
        self.l2 = Edge(l2)

        #l1(0)
        l10 = (self.l1.curve.Value(self.l1.domain()[0])).as_vec()

        #l0(0)
        l00 = (self.l0.curve.Value(self.l0.domain()[0])).as_vec()

        #l2(0)
        l20 = (self.l2.curve.Value(self.l2.domain()[0])).as_vec()

        #[[l10-l00],[l20-l00],[unit( (l10-l00) X (l20-l00) )]]
        r1 = l10 - l00
        r2 = l20 - l00
        r3 = gp_Vec()
        r3 = (l10-l00).Cross(l20-l00)
        r3 = r3/r3.Magnitude()
        A = np.matrix([[r1.X(),r1.Y(),r1.Z()],
                       [r2.X(),r2.Y(),r2.Z()],
                       [r3.X(),r3.Y(),r3.Z()]
                      ],dtype='float64')
        self.AI = AI

    def T(self,t):
        """
        Get the transformation matrix, T at parameter t.
        """

        l0t = (self.l0.curve.Value(t)).as_vec()

        l1t = (self.l1.curve.Value(t)).as_vec()

        l2t = (self.l2.curve.Value(t)).as_vec()

        r1 = l1t - l0t
        r2 = l2t - l0t
        r3 = gp_Vec()
        r3 = (l1t-l0t).Cross(l2t-l0t)
        r3 = r3/r3.Magnitude()

        B = np.matrix([[r1.X(),r1.Y(),r1.Z()],
                       [r2.X(),r2.Y(),r2.Z()],
                       [r3.X(),r3.Y(),r3.Z()]
                      ],dtype='float64')

        P = self.AI*B
        b = (self.l0.curve.Value(t)).as_vec() - (self.l0.curve.Value(0)).as_vec()

        #|    P    | b |
        #| ------- | - |
        #| 0 ... 0 | 1 |

        return np.matrix([
            [P[0,0],P[0,1],P[0,2],b.X()],
            [P[1,0],P[1,1],P[1,2],b.Y()],
            [P[2,0],P[2,1],P[2,1],b.Z()],
            [0,     0,     0,     1    ]
          ],dtype='float64')

    #def getSection(self,t):


    #def getSections(self,tMin,tMax,numSections):
