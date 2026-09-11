"""Independent finite-difference checks of unchanged off-trajectory P jets."""
import importlib.util
from pathlib import Path
import unittest


class TransferJets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parent.parent / 'nonlinear_evolution_2026' / 'constitutive.py'
        spec = importlib.util.spec_from_file_location('_transfer_constitutive', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.models = [module.Model(.15, gamma=g) for g in (0., 1e-6)]

    def evaluator(self):
        self.assertIsNotNone(importlib.util.find_spec('transfer_jets'),
                             'missing extra derivatives of the frozen constitutive action')
        from transfer_jets import extra_jets
        return extra_jets

    def points(self):
        for model in self.models:
            for tau, factor in ((.03, .94), (.09, 1.02)):
                yield model, tau, factor * model.background(tau)['q']**2

    @staticmethod
    def derivative(function, center, step=2e-4):
        return (function(center-2*step)-8*function(center-step)
                +8*function(center+step)-function(center+2*step))/(12*step)

    def close(self, actual, expected, tolerance=2e-7):
        self.assertAlmostEqual(actual, expected,
                               delta=2e-10+tolerance*abs(expected))

    def test_lower_derivatives_match_original_action(self):
        evaluate = self.evaluator()
        for model, tau, X in self.points():
            with self.subTest(gamma=model.gamma, tau=tau, X=X):
                got = evaluate(model, tau, X, include_lower=True)
                original = model.jets(tau, X, 0.)
                for key in ('P', 'P_X', 'P_XX', 'P_t', 'P_Xt', 'P_tt'):
                    self.close(got[key], float(original[key]), 2e-12)

    def test_high_derivatives_against_original_finite_differences(self):
        evaluate = self.evaluator()
        for model, tau, X in self.points():
            with self.subTest(gamma=model.gamma, tau=tau, X=X):
                got = evaluate(model, tau, X)
                self.assertEqual(set(got), {'P_XXX', 'P_XXt', 'P_Xtt'})
                self.assertTrue(all(isinstance(value, float) for value in got.values()))
                self.close(got['P_XXX'], self.derivative(
                    lambda x: float(model.jets(tau, x, 0.)['P_XX']), X))
                self.close(got['P_XXt'], self.derivative(
                    lambda t: float(model.jets(t, X, 0.)['P_XX']), tau))
                self.close(got['P_Xtt'], self.derivative(
                    lambda t: float(model.jets(t, X, 0.)['P_Xt']), tau))
                self.close(got['P_Xtt'], self.derivative(
                    lambda x: float(model.jets(tau, x, 0.)['P_tt']), X))

    def test_physical_time_chain_includes_clock_and_field_motion(self):
        evaluate = self.evaluator()
        for model, tau, X in self.points():
            for sbar, qdot in ((.73, -.06), (1.4, .04)):
                with self.subTest(gamma=model.gamma, tau=tau, sbar=sbar, qdot=qdot):
                    q = X**.5
                    got = evaluate(model, tau, X)
                    expected = self.derivative(lambda t: float(model.jets(
                        tau+sbar*t, (q+qdot*t)**2, 0.)['P_Xt']), 0.)
                    self.close(sbar*got['P_Xtt']+2*q*qdot*got['P_XXt'], expected)

    def test_logarithm_boundary_is_rejected(self):
        evaluate = self.evaluator()
        model = self.models[0]
        bg = model.background(.03)
        with self.assertRaises(ValueError):
            evaluate(model, .03, 1.01*bg['U']/(2*bg['d']))


if __name__ == '__main__':
    unittest.main()
