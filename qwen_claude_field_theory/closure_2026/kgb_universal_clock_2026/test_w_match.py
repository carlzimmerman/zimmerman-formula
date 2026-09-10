import importlib
import unittest
import numpy as np


def api():
    try:return importlib.import_module('w_match')
    except ModuleNotFoundError:raise AssertionError('F-gradient common-action matcher missing')


class WMatchTests(unittest.TestCase):
    def test_singular_action_map_not_accepted_as_regular_seed(self):
        m=api()
        row=m.solve((1.05,1.5,.1,.128,1.5),spec=m.s.Spec(eps2=1e-6),max_nfev=1)
        self.assertFalse(row['accepted_initial_root'])

    def test_lower_normalized_jets_independent_of_f_at_fixed_w(self):
        m=api();values=[]
        for f in (.01,.05,.2):
            rows=m.pair(np.log([f,1.5,.15,.128,1.5]))
            values.append(rows[0][1][:3])
        np.testing.assert_allclose(values,[values[1]]*3,rtol=1e-11)

    def test_normalized_curvatures_affine_in_f(self):
        m=api();values=[]
        for f in (.02,.06,.10):
            rows=m.pair(np.log([f,1.5,.15,.128,1.5]))
            values.append(rows[0][1][3:]-rows[1][1][3:])
        np.testing.assert_allclose(values[1],(values[0]+values[2])/2,rtol=2e-10)

    def test_equal_mass_control_and_distinct_mass_rejection(self):
        m=api();theta=np.log([.05,1.5,.1,.128,1.5])
        self.assertLess(np.max(abs(m.residual(theta,m.s.Spec(eps2=1e-6)))),1e-12)
        self.assertGreater(np.linalg.norm(m.residual(theta)),1e-3)


if __name__=='__main__':unittest.main()
