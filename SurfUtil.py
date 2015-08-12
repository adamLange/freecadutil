import FreeCAD, FreeCADGui
def getSelectedFaces():
    p = FreeCADGui.Selection.getSelection()
    faces = []
    for part in p:
        faces.extend(part.Shape.Faces)
    return faces
