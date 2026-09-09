"""Independent controls for the proposed projector/constitutive construction."""
import unittest
import numpy as np
import sympy as s
from construct import canonical_constraints, derive


class ConstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = derive()

    def test_dirac_engine_on_regular_and_auxiliary_systems(self):
        q, u, v, w = s.symbols('q u v w')
        free = canonical_constraints((v*v-q*q)/2, [q], [v])
        auxiliary = canonical_constraints((v*v-q*q-u*u)/2+u*q/3, [q,u], [v,w])
        self.assertEqual(free['dof'], auxiliary['dof'])
        self.assertEqual(auxiliary['poisson_rank'], 2)
        self.assertEqual(free['poisson_rank'], 0)

    def test_projectors_at_rotated_wavevectors(self):
        rng = np.random.default_rng(2909)
        for _ in range(20):
            kh = rng.normal(size=3); kh /= np.linalg.norm(kh)
            e1 = np.cross(kh, [0.,1.,0.]); e1 /= np.linalg.norm(e1)
            e2 = np.cross(kh,e1)
            PT = np.eye(3)-np.outer(kh,kh)
            Ktt = np.outer(e1,e1)-np.outer(e2,e2)
            Kv = -(np.outer(kh,e1)+np.outer(e1,kh))/2
            Ks = -np.eye(3)+.3*np.outer(kh,kh)
            self.assertLess(np.linalg.norm(PT@Ktt@kh), 1e-14)
            self.assertLess(abs(np.trace(PT@Ktt)), 1e-14)
            self.assertLess(np.linalg.norm(PT@Ks@kh), 1e-14)
            self.assertLess(abs(np.trace(PT@Kv)), 1e-14)
            self.assertAlmostEqual(np.linalg.norm(PT@Kv@kh)**2, .25)

    def test_constitutive_hessian_by_directional_difference(self):
        C = 5/3
        def f(g):
            y = np.linalg.norm(g)
            G = y*y+2*(1+y)*np.exp(-y)-2
            return 2*y*y-C*G
        for y in (.1,1.,2.,8.):
            bg = np.array([0.,0.,y])
            for direction in (np.array([1.,0.,0.]), np.array([0.,0.,1.])):
                h = 1e-3
                # Fourth-order independent finite difference for d²f/2.
                numeric = (-f(bg+2*h*direction)+16*f(bg+h*direction)-30*f(bg)
                           +16*f(bg-h*direction)-f(bg-2*h*direction))/(24*h*h)
                expected = 2-C*(1-np.exp(-y)+y*np.exp(-y)*direction[2]**2)
                self.assertAlmostEqual(numeric, expected, places=7)

    def test_retaining_bare_G_equals_measured_G_changes_health(self):
        # C=2 forces Gbare=Gmeasured and gives a negative longitudinal
        # acceleration Hessian at y=2. The chosen renormalization repairs it.
        mu_l = 1+np.exp(-2)
        self.assertLess(2-2*mu_l, 0)
        self.assertGreater(2-(5/3)*mu_l, 0)

    def test_new_operator_has_no_vector_velocity(self):
        result = self.result['transverse_repair']['vector_constraint_count']
        self.assertEqual(result['velocity_rank'], 0)
        self.assertEqual(result['dof'], 0)

    def test_missing_gates_remain_open(self):
        self.assertIn('FULL_THEORY_OPEN', self.result['status'])
        self.assertIn('causal response with clock and matter retained', self.result['open'])
        self.assertEqual(self.result['zero_field']['cs2_limit'], '0')


if __name__ == '__main__':
    unittest.main()
