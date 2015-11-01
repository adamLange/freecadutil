from OCC.Geom import Geom_BSplineSurface, Handle_Geom_BSplineSurface
from OCC.TColgp import TColgp_Array2OfPnt
from OCC.TColStd import TColStd_Array1OfReal, TColStd_Array2OfReal, TColStd_Array1OfInteger
from OCC.gp import gp_Vec, gp_Trsf, gp_Pnt
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace
import numpy as np
from OCCUtils.edge import Edge
import OCCUtils


class NurbsSurfaceBase:

    def __init__(self,**kwargs):
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

    def toPyOCC(self,dbg=False):
        poles,n_u,n_v = self.getPoles()

        Poles = TColgp_Array2OfPnt(1,n_u,1,n_v)
        for n,i in enumerate(poles):
            iu = n%n_u
            iv = n/n_u
            Poles.SetValue(iu+1,iv+1,i)
        
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

    def TopoDS_Face(self):
        surf = self.toPyOCC()
        hsurf = Handle_Geom_BSplineSurface(surf)
        facemaker = BRepBuilderAPI_MakeFace()
        facemaker.Init(hsurf,True,0.001)
        return facemaker.Face()

class RibMaker(NurbsSurfaceBase):

    def __init__(self,pointsList,l0,l1,l2,**kwargs):
        """
         pointsList is a list of gp_pnt
         l0, l1, and l2 are TopoDS_Edge

        """
        NurbsSurfaceBase.__init__(self,**kwargs)

        self.pts = pointsList

        self.l0 = Edge(l0)
        self.l1 = Edge(l1)
        self.l2 = Edge(l2)

        self.a = (self.l0.curve.Value(0)).as_vec()

        r1, r2, r3 = self.getRVecs(0)

        A = np.matrix([[r1.X(),r1.Y(),r1.Z()],
                       [r2.X(),r2.Y(),r2.Z()],
                       [r3.X(),r3.Y(),r3.Z()]
                      ],dtype='float64')
        self.AI = A.I

    def getRVecs(self,t):

        l0t = (self.l0.curve.Value(t)).as_vec()

        l1t = (self.l1.curve.Value(t)).as_vec()

        l2t = (self.l2.curve.Value(t)).as_vec()

        r1 = l1t - l0t
        r2 = l2t - l0t
        r3 = gp_Vec(r1.XYZ())
        r3.Cross(r2)
        r3 = r3/r3.Magnitude()

        r4 = gp_Vec(r1.XYZ())
        r4.Cross(r3)
        r4 = r4/r4.Magnitude() # unit vector in plane and perpenducular
                               # to r1
        r2 = r4*(r4.Dot(r2)) # This is the r2 you are looking for

        return r1, r2, r3

    def T(self,t):
        """
        Get the transformation matrix, T at parameter t.
        """

        r1,r2,r3 = self.getRVecs(t)

        B = np.matrix([[r1.X(),r1.Y(),r1.Z()],
                       [r2.X(),r2.Y(),r2.Z()],
                       [r3.X(),r3.Y(),r3.Z()]
                      ],dtype='float64')

        return self.AI*B

    def getSection(self,t):
        M = self.T(t)
        trsf_pts = []
        b = (self.l0.curve.Value(t)).as_vec()
        for pnt in self.pts:
            pnt = pnt.as_vec() - self.a
            pnt = np.matrix([pnt.X(),pnt.Y(),pnt.Z()],dtype='float64').T
            trsf_pt = (pnt.T * M).T
            p = gp_Pnt((gp_Vec(trsf_pt[0,0],trsf_pt[1,0],trsf_pt[2,0]) + b).XYZ())
            trsf_pts.append(p)
        return trsf_pts

    def getSections(self,tMin,tMax,numSections):
        sections = []
        for t in np.linspace(tMin,tMax,numSections):
            sections.append(self.getSection(t))
        return sections

    def getPoles(self):
        poles = []
        sections = self.getSections(0,1.0,10)
        n_u = len(sections[0])
        n_v = len(sections)
        for row in sections:
            poles.extend(row)
        return (poles,n_u,n_v)

from OCC.Geom import Geom_Plane
from OCC.GeomAPI import GeomAPI_IntCS
class RibMakerL0Normal(RibMaker):

    def getRVecs(self,t):

        p0 = gp_Pnt()
        vec = gp_Vec()
        self.l0.curve.D1(t,p0,vec)
        plane = Geom_Plane( p0, vec.as_dir() )
        intcs1 = GeomAPI_IntCS(self.l1.curve.GetHandle(),plane.GetHandle())
        intcs2 = GeomAPI_IntCS(self.l2.curve.GetHandle(),plane.GetHandle())
        
        u1, v1, w1 = intcs1.Parameters(1)
        u2, v2, w2 = intcs2.Parameters(1)

        p1 = self.l1.curve.Value(w1)
        p2 = self.l2.curve.Value(w2)

        r1 = p1.as_vec() - p0.as_vec()
        r2 = p2.as_vec() - p0.as_vec()
        r3 = gp_Vec(r1.XYZ())
        r3.Cross(r2)
        r3 = r3/r3.Magnitude()

        r4 = gp_Vec(r1.XYZ())
        r4.Cross(r3)
        r4 = r4/r4.Magnitude()

        r2 = r4*(r4.Dot(r2))

        return r1, r2 ,r3

class RibMakerTranslatePlane(RibMaker):


    def __init__(self,pointsList,l0,l1,l2,**kwargs):

        NurbsSurfaceBase.__init__(self,**kwargs)

        self.pts = pointsList

        self.l0 = Edge(l0)
        self.l1 = Edge(l1)
        self.l2 = Edge(l2)

        self.a = (self.l0.curve.Value(0)).as_vec()

        p0 = self.l0.curve.Value(0).as_vec()
        p1 = self.l1.curve.Value(0).as_vec()
        p2 = self.l2.curve.Value(0).as_vec()

        r1 = p1 - p0
        r2 = p2 - p0
        r3 = gp_Vec(r2.XYZ())
        r3.Cross(r1)
        r3 = r3/r3.Magnitude()

        r4 = gp_Vec(r1.XYZ())
        r4.Cross(r3)
        r4 = r4/r4.Magnitude()

        r2 = r4*(r4.Dot(r2))

        self.planeNormal = r3.as_dir()

        A = np.matrix([[r1.X(),r1.Y(),r1.Z()],
                       [r2.X(),r2.Y(),r2.Z()],
                       [r3.X(),r3.Y(),r3.Z()]
                      ],dtype='float64')
        self.AI = A.I

    def getRVecs(self,t):

        p0 = self.l0.curve.Value(t)

        plane = Geom_Plane(p0, self.planeNormal)

        intcs1 = GeomAPI_IntCS(self.l1.curve.GetHandle(),plane.GetHandle())
        intcs2 = GeomAPI_IntCS(self.l2.curve.GetHandle(),plane.GetHandle())
        
        u1, v1, w1 = intcs1.Parameters(1)
        u2, v2, w2 = intcs2.Parameters(1)

        p1 = self.l1.curve.Value(w1)
        p2 = self.l2.curve.Value(w2)

        r1 = p1.as_vec() - p0.as_vec()
        r2 = p2.as_vec() - p0.as_vec()
        r3 = gp_Vec(r2.XYZ())
        r3.Cross(r1)
        r3 = r3/r3.Magnitude()

        r4 = gp_Vec(r1.XYZ())
        r4.Cross(r3)
        r4 = r4/r4.Magnitude()

        r2 = r4*(r4.Dot(r2))

        return r1, r2 ,r3

class SectionProjectionSurface(NurbsSurfaceBase):
    
    from OCC.BRepProj import BRepProj_Projection
    from OCC.BRepIntCurveSurface import BRepIntCurveSurface_Inter
    from OCC.gp import gp_Lin,gp_Dir,gp_Vec
    import pdb

    def __init__(self,point,rootWire,face1,face2,**kwargs):
        """
        @param point gp_Pnt
        @param rootWire TopoDS_Wire
        @param face1 TopoDS_Face
        @param face2 TopoDS_Face
        """

        #NurbsSurfaceBase.__init__(self)
        self.basePoint = point
        self.rootWire = rootWire
        self.face1 = face1
        self.face2 = face2

        self.uDegree = 2
        self.vDegree = 1
        self.uPeriodic = True
        self.vPeriodic = False
        self.uStartMultiplicity = 1
        self.vStartMultiplicity = 2
        self.uEndMultiplicity = 1
        self.vEndMultiplicity = 2

    def getPoles(self):
        poles = []
        poleSequence = []
        rootPoleSequence = []
        tipPoleSequence = []

        rootOp = self.BRepProj_Projection(self.rootWire,self.face1,self.basePoint)
        rootSectionWire = rootOp.Current()

        rootBSpline = OCCUtils.edge.Edge(OCCUtils.Topo(rootSectionWire).edges().next())._adaptor.BSpline().GetObject()

        inter = self.BRepIntCurveSurface_Inter()

        for i in range(rootBSpline.NbPoles()):
            currentRootPole = rootBSpline.Pole(i+1)
            rootPoleSequence.append(currentRootPole)

            vec = self.gp_Vec(self.basePoint,currentRootPole)
            direction = self.gp_Dir(vec)
            line = self.gp_Lin(self.basePoint,direction)
            inter.Init(self.face2,line,1e-6)

            tipPoleSequence.append(inter.Pnt())

        poleSequence.extend(rootPoleSequence)
        poleSequence.extend(tipPoleSequence)

        self.pdb.set_trace()
        n_u = rootBSpline.NbPoles()
        n_v = 2
        return (poleSequence,n_u,n_v)
"""

TODO make classes inhereting from RibMaker that

A. has a plane which is always parallel to the plane defined by l0(0) l1(0) l2(0)
B. has a plane which is always perpendicular to l0(t)
C. has a plane which revolves around l0
-  For A B and C, a handy oce class will be GeomAPI_IntCS

"""
