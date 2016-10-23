import OCC
import OCC.BRepGProp

def getVolumeProps(shape):
  props = OCC.GProp.GProp_GProps()
  OCC.BRepGProp.brepgprop_VolumeProperties(shape,props,0.001)
  return props
