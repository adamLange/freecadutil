import OCCUtils
from OCC.TColgp import TColgp_Array1OfPnt
from OCC.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger
from OCC.Geom import Geom_BSplineCurve
import numpy as np

def wire_to_bspline(wire,degree=2,startMult=3,endMult=3):
  if wire.Closed():
    periodic = True
  else:
    periodic = False

  topoWire = OCCUtils.Topo(wire)
  n_u = topoWire.number_of_vertices()
  Poles = TColgp_Array1OfPnt(1,n_u)
  Weights = TColStd_Array1OfReal(1,n_u)

  i = 1
  for vert in topoWire.vertices():
    Poles.SetValue(i,OCCUtils.Common.vertex2pnt(vert))
    Weights.SetValue(i,1.0)
    i+=1

  if not periodic:
    n_increasing = (n_u + degree + 1) - (startMult-1) - (endMult-1)

  else:
    n_increasing = n_u + 1

  knots = []
  knots.extend(np.linspace(0,1.0,n_increasing).tolist())

  Knots = TColStd_Array1OfReal(1,len(knots))
  for n,i in enumerate(knots):
    Knots.SetValue(n+1,i)

  l = [startMult]
  m = [1]*(len(knots)-2)
  r = [endMult]

  m.extend(r)
  l.extend(m)
  mults = l 

  Mults = TColStd_Array1OfInteger(1,len(mults))
  for n,i in enumerate(mults):
    Mults.SetValue(n+1,i)

  """
Geom_BSplineCurve::Geom_BSplineCurve 	(
 	const TColgp_Array1OfPnt &  	Poles,
	const TColStd_Array1OfReal &  	Weights,
	const TColStd_Array1OfReal &  	Knots,
	const TColStd_Array1OfInteger &  	Multiplicities,
	const Standard_Integer  	Degree,
	const Standard_Boolean  	Periodic = Standard_False,
	const Standard_Boolean  	CheckRational = Standard_True 
	) 	
  """
  curve = Geom_BSplineCurve(Poles,Weights,Knots,Mults,degree,periodic)
  return curve
