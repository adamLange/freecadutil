import OCC
import OCC.BRepGProp

def getVolumeProps(shape,density):
  props = OCC.GProp.GProp_GProps()
  OCC.BRepGProp.brepgprop_VolumeProperties(shape,props,0.001)
  props1 = OCC.GProp.GProp_GProps()
  props1.Add(props,density)
  return props1

def printVolumeProps(props,v0=OCC.gp.gp_Vec(0,0,0)):
  v_cm = (props.CentreOfMass().as_vec() - v0)*1e-3

  m = props.MatrixOfInertia()

  I11 = m.Value(1,1)*1e-6
  I12 = m.Value(1,2)*1e-6
  I13 = m.Value(1,3)*1e-6

  I21 = m.Value(2,1)*1e-6
  I22 = m.Value(2,2)*1e-6
  I23 = m.Value(2,3)*1e-6

  I31 = m.Value(3,1)*1e-6
  I32 = m.Value(3,2)*1e-6
  I33 = m.Value(3,3)*1e-6

  s = ''
  s += "mass = {} [kg]\n".format(props.Mass())
  s += "centre of mass = {},{},{} [m]\n".format(v_cm.X(),v_cm.Y(),v_cm.Z())
  s += "matrix of inertia [kg m^2] = \n{}, {}, {},\n{}, {}, {},\n{}, {}, {}\n".format(I11,I12,I13,I21,I22,I23,I31,I32,I33)

  print(s)

def getSurfaceProps(shape):
  props = OCC.GProp.GProp_GProps()
  OCC.BRepGProp.brepgprop_SurfaceProperties(shape,props)
  return props
