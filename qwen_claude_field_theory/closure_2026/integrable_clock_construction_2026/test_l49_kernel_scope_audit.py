import importlib.util
import unittest


class KernelScopeTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('l49_kernel_scope_audit'))
        return __import__('l49_kernel_scope_audit')

    def test_inverse_solves_requested_equation_without_assigned_acceleration(self):
        m=self.module()
        import math
        for gN in (.001,.1,1.,10.,100.):
            y=m.exponential_inverse(gN)
            self.assertLess(abs(y*(-math.expm1(-y))-gN),1e-11*max(1,gN))

    def test_current_l49_kernel_is_checked_against_the_requested_law(self):
        out=self.module().audit()
        self.assertLess(out['max_exact_equation_residual'],1e-10)
        self.assertGreater(out['max_l49_equation_residual'],.1)


if __name__=='__main__':unittest.main()
