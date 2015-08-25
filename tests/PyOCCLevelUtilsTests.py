import unittest
import OCC,OCC.gp

class TestStringMethods(unittest.TestCase):

  def test_upper(self):
      self.assertEqual('foo'.upper(), 'FOO')

  def test_isupper(self):
      self.assertTrue('FOO'.isupper())
      self.assertFalse('Foo'.isupper())

  def test_split(self):
      s = 'hello world'
      self.assertEqual(s.split(), ['hello', 'world'])
      # check that s.split fails when the separator is not a string
      with self.assertRaises(TypeError):
          s.split(2)

  def test_rib_maker_translate(self):

      from OCC.gp import gp_Pnt,gp_Trsf
      from OCCUtils.Construct import points_to_bspline, make_edge
      from PyOCCLevelUtils import RibMaker
      from numpy import matrix
      from numpy.testing import assert_array_max_ulp

      pts = [OCC.gp.gp_Pnt(0,0,0),OCC.gp.gp_Pnt(1,0,0),OCC.gp.gp_Pnt(0,1,0)]
      l0 = make_edge(points_to_bspline([gp_Pnt(0,0,1),gp_Pnt(0,0,10)]))
      l1 = make_edge(points_to_bspline([gp_Pnt(1,0,1),gp_Pnt(1,0,10)]))
      l2 = make_edge(points_to_bspline([gp_Pnt(0,1,1),gp_Pnt(0,1,10)]))

      r = RibMaker(pts,l0,l1,l2)
      M = r.T(1)
      #M_gold = matrix([
      #    [1,0,0,0],
      #    [0,1,0,0],
      #    [0,0,1,9],
      #    [0,0,0,1]
      #  ],dtype='float64')
      #assert_array_max_ulp(M,M_gold)


      M_gold = gp_Trsf()
      M_gold.SetValues(
          1,0,0,0,
          0,1,0,0,
          0,0,1,9,
          1e-8,1e-4)

      flag = True
      for i in range(1,4):
          for j in range(1,5):
              if not (M.Value(i,j) == M_gold.Value(i,j)):
                  flag = False

      self.assertTrue(flag)

      #S = r.getSection(1)
      #S_gold = [OCC.gp.gp_Pnt(0,0,9),OCC.gp.gp_Pnt(1,0,9),OCC.gp.gp_Pnt(0,1,9)]
      #for i in enumerate(S):
      #    self.assertTrue(S[i] == S_gold[i])


  #def test_rib_maker_scale_translate(self):

if __name__ == '__main__':
    unittest.main()
