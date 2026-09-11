"""Behavior tests: incorrect source sign/elimination/current must fail."""
import importlib.util
from pathlib import Path
import unittest


class SourceVariationTests(unittest.TestCase):
    def test_sourced_action_is_implemented(self):
        path = Path(__file__).with_name('source.py')
        self.assertTrue(path.exists(), 'missing action-derived baryon source implementation')
        spec = importlib.util.spec_from_file_location('source_gate', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        facts, _ = module.derive()
        for name, result in facts['checks'].items():
            with self.subTest(name=name):
                self.assertTrue(result)
        # A deleted source must fail the test; the zero-source regression alone
        # cannot distinguish a sourced model from the previous vacuum code.
        self.assertTrue(facts['source_is_nonzero'])
        self.assertTrue(facts['wrong_source_sign_rejected'])


if __name__ == '__main__':
    unittest.main()
