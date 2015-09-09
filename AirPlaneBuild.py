import FreeCAD

def buildVerticalStabilizer():
    from PyOCCLevelUtils import RibMakerTranslatePlane
    import OCCUtils
    import Part
    from BSplineSketch import InteractiveBSplineCurve

    sectionSketch = FreeCAD.ActiveDocument.getObjectsByLabel('wingRoot008')[0]
    leadingEdge= FreeCAD.ActiveDocument.getObjectsByLabel('leadingEdge')[0]
    trailingEdge= FreeCAD.ActiveDocument.getObjectsByLabel('trailingEdge')[0]
    widthEdge= FreeCAD.ActiveDocument.getObjectsByLabel('widthEdge')[0]

    leadingEdge = OCCUtils.Topo(Part.__toPythonOCC__(leadingEdge.Shape)).edges().next()
    trailingEdge = OCCUtils.Topo(Part.__toPythonOCC__(trailingEdge.Shape)).edges().next()
    widthEdge = OCCUtils.Topo(Part.__toPythonOCC__(widthEdge.Shape)).edges().next()

    sectionICurve = InteractiveBSplineCurve(sectionSketch)
    pointsList = sectionICurve.getPolesAs_gp_Pnt()
    
    rm = RibMakerTranslatePlane(pointsList,leadingEdge,trailingEdge,widthEdge)

    #rm.uPeriodic = True
    #rm.UStartMultiplicity = 1
    #rm.UEndMultiplicity = 1
   
    return rm.TopoDS_Face()

def buildFoil(foilLabel,sectionSketchLabel,leadingEdgeSketchLabel,trailingEdgeSketchLabel,widthEdgeSketchLabel):
    
    from PyOCCLevelUtils import RibMakerTranslatePlane
    import OCCUtils
    import Part
    from BSplineSketch import InteractiveBSplineCurve

    sps = FreeCAD.ActiveDocument.getObjectsByLabel(sectionSketchLabel)[0]
    sectionPoints = InteractiveBSplineCurve(sps).getPolesAs_gp_Pnt()

    leadingEdgeSketch = FreeCAD.ActiveDocument.getObjectsByLabel(leadingEdgeSketchLabel)[0]
    trailingEdgeSketch = FreeCAD.ActiveDocument.getObjectsByLabel(trailingEdgeSketchLabel)[0]
    widthEdgeSketch = FreeCAD.ActiveDocument.getObjectsByLabel(widthEdgeSketchLabel)[0]

    leadingEdge = OCCUtils.Topo(Part.__toPythonOCC__(InteractiveBSplineCurve(leadingEdgeSketch).getShape())).edges().next()
    trailingEdge = OCCUtils.Topo(Part.__toPythonOCC__(InteractiveBSplineCurve(trailingEdgeSketch).getShape())).edges().next()
    widthEdge = OCCUtils.Topo(Part.__toPythonOCC__(InteractiveBSplineCurve(widthEdgeSketch).getShape())).edges().next()

    rm = RibMakerTranslatePlane(sectionPoints,leadingEdge,trailingEdge,widthEdge)
    shapeobj = FreeCAD.ActiveDocument.addObject("Part::Feature",foilLabel)
    shapeobj.Shape = Part.__fromPythonOCC__(rm.TopoDS_Face())
    FreeCAD.ActiveDocument.recompute()

