import Part
def sketchToPoints(sketch):
    geo = sketch.Geometry
    points = []
    document = sketch.Document
    for shape in geo:
        points.append(shape.StartPoint)
        points.append(shape.EndPoint)
    #for i in range(len(points)):
    poles = []
    for i in [4,7,9,13,17,18,19,15,11,5]:
        poles.append(points[i])
    bs = Part.BSplineCurve()
    bs.buildFromPolesMultsKnots(poles,periodic=True)
    shape = bs.toShape()
    shape.Placement = sketch.Placement
    document.addObject("Part::Feature","foilSection").Shape = shape
