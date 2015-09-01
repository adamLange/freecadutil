import unittest
import OCC,OCC.gp

class TestStringMethods(unittest.TestCase):

  def test_rib_maker_scale_translate(self):

      from OCC.gp import gp_Pnt,gp_Trsf
      from OCCUtils.Construct import points_to_bspline, make_edge
      from PyOCCLevelUtils import RibMaker
      from numpy import matrix
      from numpy.testing import assert_array_max_ulp

      pts = [OCC.gp.gp_Pnt(5,0,0),OCC.gp.gp_Pnt(6,0,0),OCC.gp.gp_Pnt(5,1,0)]
      l0 = make_edge(points_to_bspline([gp_Pnt(5,0,1),gp_Pnt(5,0,10)]))
      l1 = make_edge(points_to_bspline([gp_Pnt(6,0,1),gp_Pnt(6,0,10)]))
      l2 = make_edge(points_to_bspline([gp_Pnt(5,1,1),gp_Pnt(5,2,10)]))

      r = RibMaker(pts,l0,l1,l2)
      M = r.T(1)

      M_gold = matrix(
        [
          [1,0,0],
          [0,2,0],
          [0,0,1]
        ],dtype='float64')

      assert_array_max_ulp(M,M_gold)

      """
      M_gold = gp_Trsf()
      M_gold.SetValues(
          1,0,0,0,
          0,2,0,0,
          0,0,1,9,
          1e-8,1e-4)

      flag = True
      for i in range(1,4):
          for j in range(1,5):
              if not (M.Value(i,j) == M_gold.Value(i,j)):
                  flag = False

      self.assertTrue(flag)
      """

      # check one section
      S = r.getSection(1)
      S_gold = [OCC.gp.gp_Pnt(5,0,9),OCC.gp.gp_Pnt(6,0,9),OCC.gp.gp_Pnt(5,2,9)]
      for i in range(len(S)):
          self.assertTrue(S[i] == S_gold[i])

      # check several sections
      Z = r.getSections(0,1.0,3)
      Z_gold = [
          [gp_Pnt(5,0,0),gp_Pnt(6,0,0),gp_Pnt(5,1,0)],
          [gp_Pnt(5,0,4.5),gp_Pnt(6,0,4.5),gp_Pnt(5,1.5,4.5)],
          [gp_Pnt(5,0,9.0),gp_Pnt(6,0,9.0),gp_Pnt(5,2,9.0)]
        ]

      for i in range(len(Z)):
          for j in range(len(Z[i])):
              self.assertTrue(Z[i][j] == Z_gold[i][j])

  def test_RibMakerL0Perpendicular(self):

      from OCC.gp import gp_Pnt,gp_Trsf
      from OCCUtils.Construct import points_to_bspline, make_edge
      from PyOCCLevelUtils import RibMakerL0Perpendicular
      from numpy import matrix
      from numpy.testing import assert_array_max_ulp

      pts = [OCC.gp.gp_Pnt(5,0,0),OCC.gp.gp_Pnt(6,0,0),OCC.gp.gp_Pnt(5,1,0)]
      l0 = make_edge(points_to_bspline([gp_Pnt(5,0,1),gp_Pnt(5,0,10)]))
      l1 = make_edge(points_to_bspline([gp_Pnt(6,0,1),gp_Pnt(6,0,20)]))
      l2 = make_edge(points_to_bspline([gp_Pnt(5,1,1),gp_Pnt(5,2,10)]))

      r = RibMakerL0Perpendicular(pts,l0,l1,l2)
      M = r.T(1)

      M_gold = matrix(
        [
          [1,0,0],
          [0,2,0],
          [0,0,1]
        ],dtype='float64')

      assert_array_max_ulp(M,M_gold)

      # check one section
      S = r.getSection(1)
      S_gold = [OCC.gp.gp_Pnt(5,0,9),OCC.gp.gp_Pnt(6,0,9),OCC.gp.gp_Pnt(5,2,9)]
      for i in range(len(S)):
          self.assertTrue(S[i] == S_gold[i])

      # check several sections
      Z = r.getSections(0,1.0,3)
      Z_gold = [
          [gp_Pnt(5,0,0),gp_Pnt(6,0,0),gp_Pnt(5,1,0)],
          [gp_Pnt(5,0,4.5),gp_Pnt(6,0,4.5),gp_Pnt(5,1.5,4.5)],
          [gp_Pnt(5,0,9.0),gp_Pnt(6,0,9.0),gp_Pnt(5,2,9.0)]
        ]

      for i in range(len(Z)):
          for j in range(len(Z[i])):
              self.assertTrue(Z[i][j] == Z_gold[i][j])
  """
  def test_RibMakerTranslatePlane(self):

      from OCC.gp import gp_Pnt,gp_Trsf
      from OCCUtils.Construct import points_to_bspline, make_edge
      from PyOCCLevelUtils import RibMaker
      from numpy import matrix
      from numpy.testing import assert_array_max_ulp

      pts = [OCC.gp.gp_Pnt(5,0,0),OCC.gp.gp_Pnt(6,0,0),OCC.gp.gp_Pnt(5,1,0)]
      l0 = make_edge(points_to_bspline([gp_Pnt(5,0,1),gp_Pnt(5,0,10)]))
      l1 = make_edge(points_to_bspline([gp_Pnt(6,0,1),gp_Pnt(6,0,20)]))
      l2 = make_edge(points_to_bspline([gp_Pnt(5,1,1),gp_Pnt(5,2,10)]))

      r = RibMakerL0Perpendicular(pts,l0,l1,l2)
      M = r.T(1)

      M_gold = matrix(
        [
          [1,0,0],
          [0,2,0],
          [0,0,1]
        ],dtype='float64')

      assert_array_max_ulp(M,M_gold)

      # check one section
      S = r.getSection(1)
      S_gold = [OCC.gp.gp_Pnt(5,0,9),OCC.gp.gp_Pnt(6,0,9),OCC.gp.gp_Pnt(5,2,9)]
      for i in range(len(S)):
          self.assertTrue(S[i] == S_gold[i])

      # check several sections
      Z = r.getSections(0,1.0,3)
      Z_gold = [
          [gp_Pnt(5,0,0),gp_Pnt(6,0,0),gp_Pnt(5,1,0)],
          [gp_Pnt(5,0,4.5),gp_Pnt(6,0,4.5),gp_Pnt(5,1.5,4.5)],
          [gp_Pnt(5,0,9.0),gp_Pnt(6,0,9.0),gp_Pnt(5,2,9.0)]
        ]

      for i in range(len(Z)):
          for j in range(len(Z[i])):
              self.assertTrue(Z[i][j] == Z_gold[i][j])
    """

if __name__ == '__main__':
    unittest.main()
