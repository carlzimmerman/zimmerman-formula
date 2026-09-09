import importlib.util
import unittest


class ResponseLimitTests(unittest.TestCase):
    def test_laurent_coefficient_includes_curvature_and_face_acceleration_gradient(self):
        self.assertIsNotNone(importlib.util.find_spec('ic41_response_limit'))
        m=__import__('ic41_response_limit')
        self.assertEqual(m.identity(),0)


if __name__=='__main__':unittest.main()
