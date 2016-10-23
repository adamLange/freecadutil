import OCC
from OCC.BRepBuilderAPI import *
import OCCUtils
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut

def facesToSolid(block):

  faces = []
  ms = BRepBuilderAPI_Sewing()
  for i in OCCUtils.Topo(block).faces():
    faces.append(i)
    ms.Add(i)
  ms.Perform()
  shape = ms.SewedShape()
  shell = OCCUtils.Topo(shape).shells().next()
  msolid = BRepBuilderAPI_MakeSolid(shell)
  return msolid.Solid()

def clip(partsCompound,tool):

  solids = []
  for i in OCCUtils.Topo(partsCompound).solids():
    mb = BRepAlgoAPI_Cut(i,tool)
    solids.append(mb.Shape())
  return solids
