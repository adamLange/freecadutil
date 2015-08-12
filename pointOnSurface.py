import Part
def pointAt(shape,u,v):
    v = shape.Shape.valueAt(u,v)
    shape.Document.addObject("Part::Feature","pointOn").Shape = Part.Point(v).toShape()
