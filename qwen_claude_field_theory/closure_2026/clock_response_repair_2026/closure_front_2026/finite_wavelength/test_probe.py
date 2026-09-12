"""Controls that detect wrong matter-source signs or missing constraint terms."""
import importlib.util
from pathlib import Path
import unittest
import sympy as s


class ProbeTests(unittest.TestCase):
    def test_conserved_source_variation(self):
        path = Path(__file__).with_name('probe.py')
        self.assertTrue(path.exists(), 'conserved matter probe not implemented')
        spec = importlib.util.spec_from_file_location('probe', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        result, ctx = mod.derive()
        self.assertTrue(all(result['checks'].values()))
        self.assertEqual(ctx['source_lapse_derivative'], -ctx['rho'])
        # Removing the imposed source must remove both canonical driving terms.
        self.assertEqual(s.simplify(ctx['F'].subs(ctx['rho'], 0)), 0)
        self.assertEqual(s.simplify(ctx['S'].subs(ctx['rho'], 0)), 0)
        # These symbols must affect the Hamiltonian driver: no free-system rerun.
        self.assertNotEqual(s.diff(ctx['F'], ctx['rho']), 0)
        self.assertNotEqual(s.diff(ctx['S'], ctx['rho']), 0)


if __name__ == '__main__':
    unittest.main()
