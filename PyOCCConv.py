import OCC
import Part
import FreeCADGui
import OCCUtils, OCCUtils.face

def sel2Topo():
  topo = selectionToTopoDSShape()
  topo = OCCUtils.Topo(topo)
  return topo

def selectionToTopoDSShape():
  selection = FreeCADGui.Selection.getSelection()[0]
  return Part.__toPythonOCC__(selection.Shape)

def selectionToTopoDSFace():
  shape = selectionToTopoDSShape()
  shape = OCCUtils.Topo(shape)
  shape = shape.faces().next()
  return shape

def selectionToVec():
  shape = selectionToTopoDSShape()
  shape = OCCUtils.Topo(shape)
  shape = shape.vertices().next()
  shape = OCCUtils.vertex.vertex2pnt(shape)
  shape = shape.as_vec()
  return shape

def selectionToWire():
  shape = selectionToTopoDSShape()
  shape = OCCUtils.Topo(shape)
  shape = shape.wires().next()
  return shape

def show(TopoDSShape):
  Part.show(Part.__fromPythonOCC__(TopoDSShape))
