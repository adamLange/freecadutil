#from OCC.Geom import Geom_BSplineSurface, Handle_Geom_BSplineSurface
#from OCC.TColgp import TColgp_Array2OfPnt
#from OCC.TColStd import TColStd_Array1OfReal, TColStd_Array2OfReal, TColStd_Array1OfInteger
from OCC.gp import gp_Vec, gp_Trsf, gp_Pnt
#from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace
import numpy as np
from OCCUtils.edge import Edge

class RibMaker:

    def __init__(self,pointsList,l0,l1,l2):
        """
         pointsList is a list of gp_pnt
         l0, l1, and l2 are TopoDS_Edge

        """
        self.pts = pointsList

        self.l0 = Edge(l0)
        self.l1 = Edge(l1)
        self.l2 = Edge(l2)

        l00 = (self.l0.curve.Value(self.l0.domain()[0])).as_vec()
        l10 = (self.l1.curve.Value(self.l1.domain()[0])).as_vec()
        l20 = (self.l2.curve.Value(self.l2.domain()[0])).as_vec()

        #[[l10-l00],[l20-l00],[unit( (l10-l00) X (l20-l00) )]]
        r1 = l10 - l00
        r2 = l20 - l00 #At this point r2 still needs to be projected to
                       # be perpendicular to r1.
        r3 = gp_Vec(r1.XYZ())
        r3.Cross(r2)
        r3 = r3/r3.Magnitude()
     
        r4 = gp_Vec(r1.XYZ())
        r4.Cross(r3)
        r4 = r4/r4.Magnitude() # unit vector in plane and perpenducular
                               # to r1
        r2 = r4*(r4.Dot(r2)) # This is the r2 you are looking for

        A = np.matrix([[r1.X(),r1.Y(),r1.Z()],
                       [r2.X(),r2.Y(),r2.Z()],
                       [r3.X(),r3.Y(),r3.Z()]
                      ],dtype='float64')
        self.AI = A.I

    def T(self,t):
        """
        Get the transformation matrix, T at parameter t.
        """

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
            [P[2,0],P[2,1],P[2,2],b.Z()],
            [0,     0,     0,     1    ]
          ],dtype='float64')

        """
        trsf = gp_Trsf()
        trsf.SetValues(
            P[0,0],P[0,1],P[0,2],b.X(),
            P[1,0],P[1,1],P[1,2],b.Y(),
            P[2,0],P[2,1],P[2,2],b.Z(),
              1e-6,  1e-6
          )
        return trsf
        """

    def getSection(self,t):
        M = self.T(t)
        trsf_pts = []
        for pnt in self.pts:
            pnt = np.matrix([pnt.X(),pnt.Y(),pnt.Z(),1.0],dtype='float64').T
            trsf_pt = M * pnt
            p = gp_Pnt(trsf_pt[0,0],trsf_pt[1,0],trsf_pt[2,0])
            trsf_pts.append(p)
        return trsf_pts

    def getSections(self,tMin,tMax,numSections):
        sections = []
        for t in np.linspace(tMin,tMax,numSections):
            sections.append(self.getSection(t))
        return sections
