import OCC
import Part
import FreeCADGui, FreeCAD
import OCCUtils, OCCUtils.face, OCCUtils.vertex

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
  shape = OCCUtils.Common.vertex2pnt(shape)
  shape = shape.as_vec()
  return shape

def selectionToWire():
  shape = selectionToTopoDSShape()
  shape = OCCUtils.Topo(shape)
  shape = shape.wires().next()
  return shape

def show(TopoDSShape):
  Part.show(Part.__fromPythonOCC__(TopoDSShape))

def showBSplineSurfacePoles(bspline):
  from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
  for v in range(bspline.NbVPoles()):
    for u in range(bspline.NbUPoles()):
      pole = bspline.Pole(u+1,v+1)
      mv = BRepBuilderAPI_MakeVertex(pole)
      shapeobj = FreeCAD.ActiveDocument.addObject("Part::Feature","pole_{}_{}".format(u+1,v+1))
      shapeobj.Shape = Part.__fromPythonOCC__(mv.Vertex())
  FreeCAD.ActiveDocument.recompute()

def showBSplineCurvePoles(bspline):
  from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
  for u in range(bspline.NbPoles()):
      pole = bspline.Pole(u+1)
      mv = BRepBuilderAPI_MakeVertex(pole)
      shapeobj = FreeCAD.ActiveDocument.addObject("Part::Feature","pole_{}".format(u+1))
      shapeobj.Shape = Part.__fromPythonOCC__(mv.Vertex())
  FreeCAD.ActiveDocument.recompute()

def retrieveBSplineCurvePoles(bspline):
  for u in range(bspline.NbPoles()):
    pnt = Part.__toPythonOCC__(FreeCAD.ActiveDocument.getObjectsByLabel('pole_{}'.format(u+1))[0].Shape)
    pnt = OCCUtils.Topo(pnt).vertices().next()
    pnt = OCCUtils.vertex.vertex2pnt(pnt)
    bspline.SetPole(u+1,pnt)

def showPoint(point):
  from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
  mv = BRepBuilderAPI_MakeVertex(point)
  show(mv.Vertex())
