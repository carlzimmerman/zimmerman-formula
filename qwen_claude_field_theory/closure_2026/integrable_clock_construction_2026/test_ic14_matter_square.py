"""Check implicit jets, matter mixing, and the local construction's exclusions."""
import importlib.util
import unittest
import mpmath as mp
import ic11_clock_pressure as vacuum


class MatterSquareTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 50

    def model(self):
        self.assertIsNotNone(importlib.util.find_spec('ic14_matter_square'))
        return __import__('ic14_matter_square')

    def test_implicit_jets_match_five_point_branch_differences(self):
        model = self.model()
        X = mp.exp(-mp.mpf('.2'))/2
        h = mp.mpf('1e-5')
        def branch(x, key):
            v = vacuum.state(-mp.log(2*x)/2)
            return v['P'] if key == 'FXX' else mp.exp(2*v['w'])
        jets = model.branch_jets('.1')
        for key in ('FXX', 'z0XX'):
            f = lambda x: branch(x, key)
            numerical = (-f(X+2*h)+16*f(X+h)-30*f(X)+16*f(X-h)-f(X-2*h))/(12*h*h)
            self.assertLess(abs(numerical-jets[key]), mp.mpf('1e-11'))

    def test_vacuum_pressure_and_matter_cones(self):
        model = self.model()
        for S in ('.03', '.05', '.1', '.2'):
            zero = model.state(S, 0)
            self.assertLess(abs(zero['pressure']-vacuum.state(S)['P']), mp.mpf('1e-40'))
            for Y in ('.0001', '.01', '.1'):
                bg = model.state(S, Y)
                self.assertGreater(min(bg['kinetic_eigenvalues']), 0)
                self.assertGreater(min(bg['cone_margin_eigenvalues']), 0)
                self.assertLess(bg['Lww'], 0)
                self.assertLess(abs(bg['constraint']), mp.mpf('1e-40'))

    def test_effective_hessian_matches_raw_velocity_schur(self):
        model = self.model()
        bg = model.state('.1', '.01')
        point = (mp.sqrt(2*bg['X']), mp.sqrt(2*bg['Y']), bg['z'])
        def density(v1, v2, z):
            return model.raw(-mp.log(v1), z, v2*v2/2)
        H = mp.matrix(3)
        for i in range(3):
            for j in range(3):
                H[i,j] = mp.diff(density, point, tuple(int(k == i)+int(k == j) for k in range(3)))
        self.assertLess(mp.norm(bg['K']-(H[:2,:2]-H[:2,2:3]*H[2:3,:2]/H[2,2])), mp.mpf('1e-30'))

    def test_scan_is_bounded_and_does_not_certify_an_interval(self):
        model = self.model()
        scan = model.scan(101)
        self.assertEqual(scan['samples'], 101)
        self.assertGreater(scan['minimum_z0XX'], 0)
        self.assertGreater(scan['minimum_cone_determinant_at_Y_zero'], 0)
        self.assertFalse(scan['interval_certified'])

    def test_chart_and_plateau_are_recomputed(self):
        model = self.model()
        self.assertTrue(model.state('.1', '.01')['inside_eta_one'])
        distant = model.state('.1', 100)
        self.assertFalse(distant['inside_original_chart'])
        self.assertFalse(distant['admissible'])
        for S in ('.03', '.1', '.2'):
            boundary = model.plateau_boundary(S)
            self.assertGreater(boundary['Y'], 0)
            self.assertLess(abs(boundary['activation_r']**2-boundary['boundary_r_squared']), mp.mpf('1e-35'))

    def test_invalid_inputs_and_symbolic_identities(self):
        model = self.model()
        for args in ((0, 0), ('.1', -1), ('.1', 0, 0)):
            with self.assertRaises(ValueError):
                model.state(*args)
        self.assertTrue(all(v == 0 for v in model.identities().values()))

    def test_boosted_quartic_recovers_aligned_cones_and_solves_principal_matrix(self):
        model = self.model()
        self.assertTrue(hasattr(model, 'boosted_characteristics'))
        bg = model.state('.1', '.0001')
        aligned = sorted([-mp.sqrt(c) for c in bg['speeds_squared']]+[mp.sqrt(c) for c in bg['speeds_squared']])
        roots = model.boosted_characteristics('.1', '.0001', 0)['roots']
        self.assertLess(max(abs(a-b) for a,b in zip(aligned,roots)), mp.mpf('1e-35'))
        for boost in ('.5', '.9'):
            result = model.boosted_characteristics('.1', '.0001', boost)
            self.assertLess(result['maximum_principal_residual'], mp.mpf('1e-35'))
            self.assertFalse(result['physical_activation_checked'])


if __name__ == '__main__':
    unittest.main()
