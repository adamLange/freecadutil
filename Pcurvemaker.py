import OCC.BOPTools
import OCC.BRepBuilderAPI


def faceFromWireFace(W,F):
    """
        W: a wire on the face
        F: a face
        return: a face

        The wire W need not have pcurves on the face.  The pcurves will be 
        calculated in this function.  The resulting face is constructed 
        by using the surface of the input face F, and is bounded by the 
        input wire W.
    """
    # get all edges of the input wire
    inputEdges = []
    exp = OCC.TopExp.TopExp_Explorer(W,OCC.TopAbs.TopAbs_EDGE)
    while exp.More():
        inputEdges.append(OCC.TopoDS.topods.Edge(exp.Current()))
        exp.Next()

    # check for the existance of pcurves of edges, if non existant, make them
    #pcurves = []
    outputEdges = []
    for edge in inputEdges:
        aC = OCC.Geom2d.Handle_Geom2d_Curve()
        pcurves.append(OCC.BOPTools.BOPTools_AlgoTools2D_HasCurveOnSurface(edge,F,aC))
        new,start,finish,tolerance = OCC.BOPTools.BOPTools_AlgoTools2D_HasCurveOnSurface(edge,F,aC)
        outputEdges.append(OCC.BRepBuilderAPI.BRepBuilderAPI_MakeEdge())
    return pcurves
