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

  def test_rib_maker_scale_translate(self):

      from OCC.gp import gp_Pnt
      from OCCUtils.Construct import points_to_bspline, make_edge
      from PyOCCLevelUtils import RibMaker
      from numpy import matrix
      #from numpy.testing import assert_array_almost_equal_nulp
      from numpy.testing import assert_array_max_ulp

      pts = [OCC.gp.gp_Pnt(0,0,0),OCC.gp.gp_Pnt(1,0,0),OCC.gp.gp_Pnt(0,1,0)]
      l0 = make_edge(points_to_bspline([gp_Pnt(0,0,0),gp_Pnt(0,0,10)]))
      l1 = make_edge(points_to_bspline([gp_Pnt(1,0,0),gp_Pnt(1,0,10)]))
      l2 = make_edge(points_to_bspline([gp_Pnt(0,1,0),gp_Pnt(0,1,10)]))


      r = RibMaker(pts,l0,l1,l2)
      M = r.T(1)
      M_gold = matrix([
          [1,0,0, 0],
          [0,1,0, 0],
          [0,0,0,10],
          [0,0,0, 1]
        ],dtype='float64')
      #assert_array_almost_equal_nulp(M,M_gold)
      assert_array_max_ulp(M,M_gold)

if __name__ == '__main__':
    unittest.main()
