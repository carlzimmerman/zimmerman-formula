"""Regression controls: legitimate mesh-pair rows must not collide."""
import unittest
from verify_late import comparison_key

class Controls(unittest.TestCase):
 def test_two_mesh_pairs_at_same_time_are_distinct(self):
  a=dict(galaxy='Draco',t=.5,footing='canonical',beta=0,left_ne=4096,right_ne=8192);b=dict(a,left_ne=8192,right_ne=16384)
  self.assertEqual(len({comparison_key(a),comparison_key(b)}),2)
 def test_duplicate_pair_is_the_same(self):
  a=dict(galaxy='Sextans',t=1.,footing='alt',beta=-.5,left_ne=8192,right_ne=16384)
  self.assertEqual(comparison_key(a),comparison_key(dict(a)))
 def test_source_footing_is_part_of_identity(self):
  a=dict(galaxy='Draco',t=.5,footing='canonical',beta=0,left_ne=4096,right_ne=8192)
  self.assertNotEqual(comparison_key(a),comparison_key(dict(a,footing='alt')))

if __name__=='__main__':unittest.main()
