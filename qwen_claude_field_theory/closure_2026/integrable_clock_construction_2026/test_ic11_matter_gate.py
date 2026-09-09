"""Catch omitted matter mixing and incorrect fixed-velocity auxiliary elimination."""
import importlib.util
import unittest
import mpmath as mp
import ic10_local_clock as original


class MatterGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 50

    def model(self):
        self.assertIsNotNone(importlib.util.find_spec('ic11_matter_gate'))
        return __import__('ic11_matter_gate')

    def test_vacuum_reshape_preserves_pressure_and_eliminated_kinetic(self):
        model = self.model()
        for S in map(mp.mpf, ['.03', '.1', '.2']):
            left, right = model.state(S, 0, 0), model.state(S, 0, '.01')
            self.assertLess(abs(left['w']-right['w']), mp.mpf('1e-38'))
            self.assertLess(abs(left['pressure']-right['pressure']), mp.mpf('1e-38'))
            self.assertLess(abs(left['K'][0,0]-right['K'][0,0]), mp.mpf('1e-36'))
            self.assertLess(abs(left['K'][1,1]-left['D'][1,1]), mp.mpf('1e-38'))
            self.assertGreater(left['Lww'], 0)
            self.assertLess(right['Lww'], 0)

    def test_matrix_matches_independent_velocity_hessian_schur(self):
        model = self.model()
        bg = model.state('.1', '.01', '.01')
        X, Y, w = bg['X'], bg['Y'], bg['w']
        point = (mp.sqrt(2*X), mp.sqrt(2*Y), w)
        def velocity_density(v1, v2, aux):
            return model.raw(-mp.log(v1), aux, v2*v2/2, mp.mpf('.01'))
        H = mp.matrix(3)
        for i in range(3):
            for j in range(3):
                order = tuple(int(k==i)+int(k==j) for k in range(3))
                H[i,j] = mp.diff(velocity_density, point, order)
        self.assertLess(mp.norm(bg['K']-(H[:2,:2]-H[:2,2:3]*H[2:3,:2]/H[2,2])),mp.mpf('1e-33'))

    def test_ordinary_matter_changes_the_auxiliary_root(self):
        model = self.model()
        vacuum, matter = model.state('.1',0,'.01'), model.state('.1','.01','.01')
        self.assertGreater(abs(vacuum['w']-matter['w']),mp.mpf('1e-9'))
        self.assertLess(abs(matter['constraint']),mp.mpf('1e-35'))

    def test_rejects_invalid_clock_chart_and_matter_density(self):
        model = self.model()
        with self.assertRaises(ValueError):model.state(-1,0,0)
        with self.assertRaises(ValueError):model.state('.1',-1,0)

    def test_balanced_auxiliary_curvature_repairs_the_mixed_cone(self):
        model = self.model()
        for S in ['.03','.05','.1','.2']:
            bg = model.state(S,'.0001','balanced')
            self.assertTrue(bg['inside_eta_one'])
            self.assertLess(bg['Lww'],0)
            self.assertGreater(min(bg['kinetic_eigenvalues']),0)
            self.assertGreater(min(bg['cone_margin_eigenvalues']),0)
            self.assertTrue(bg['healthy_causal'])

    def test_balanced_vacuum_has_the_same_clock_pressure(self):
        model = self.model()
        for S in ['.03','.1','.2']:
            first,second=model.state(S,0,0),model.state(S,0,'balanced')
            self.assertLess(abs(first['pressure']-second['pressure']),mp.mpf('1e-35'))
            self.assertLess(abs(first['K'][0,0]-second['K'][0,0]),mp.mpf('1e-33'))

    def test_balanced_finite_matter_fold_is_not_a_regular_elimination(self):
        model=self.model()
        self.assertTrue(hasattr(model,'fold'))
        result=model.fold('.1')
        self.assertGreater(result['Y'],0)
        self.assertLess(result['Y'],mp.mpf('.01'))
        self.assertLess(abs(result['constraint']),mp.mpf('1e-32'))
        self.assertLess(abs(result['Lww']),mp.mpf('1e-30'))

    def test_velocity_fold_does_not_imply_fixed_momentum_rank_loss(self):
        model=self.model()
        result=model.fold('.1')
        self.assertIn('canonical_auxiliary_bracket',result)
        self.assertGreater(abs(mp.det(result['canonical_auxiliary_bracket'])),mp.mpf('1e-8'))
        values=mp.eigsy(result['reduced_momentum_hessian'],eigvals_only=True)
        self.assertLess(abs(values[0]),mp.mpf('1e-30'))
        self.assertGreater(values[1],0)


if __name__ == '__main__':
    unittest.main()
