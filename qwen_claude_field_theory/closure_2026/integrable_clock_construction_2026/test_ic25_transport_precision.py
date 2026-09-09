"""Independent precision check for the nonautonomous propagator."""
import importlib.util
import unittest


class PrecisionTests(unittest.TestCase):
    def test_arbitrary_precision_transport_retains_volume(self):
        self.assertIsNotNone(importlib.util.find_spec('ic25_transport_precision'),'Precision cross-check missing')
        import ic25_transport_precision as m
        h=m.base.evolve(.005,profile='charge')
        coarse=m.propagate(h,1,4);fine=m.propagate(h,1,8)
        self.assertLess(float(fine['relative_volume_error']),1e-30)
        self.assertLess(abs(float(coarse['singular_values'][0]/fine['singular_values'][0])-1),1e-3)


if __name__=='__main__':unittest.main()
