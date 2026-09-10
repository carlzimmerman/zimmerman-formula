import unittest
import mpmath as mp
import constant_f as c


class ConstantFTests(unittest.TestCase):
    def test_exact_geometry_and_clock_compatibility(self):
        self.assertTrue(all(value==0 for value in c.symbolic_checks()))

    def test_actual_on_shell_and_regular_field_map(self):
        with mp.workdps(60):
            out=c.evaluate('1e-6','.1','.5','.525')
            for key in ('physical_metric_error','physical_current_error','EF_metric_error','EF_current_error','clock_U_derivative_error','P_derivative_error'):
                self.assertLess(out[key],mp.mpf('1e-35'),key)
            self.assertEqual(out['Dfield'],mp.mpf('1.05'))
            self.assertEqual(out['Dcoord'],1)
            self.assertLess(out['kinetic'],0)
            self.assertGreater(out['angular'],0)
            self.assertFalse(out['strict_EF_scalar_cone'])

    def test_curvatures_are_total_action_derivatives(self):
        with mp.workdps(60):
            a=c.state('1e-6','.1','.5','.525');jet=c.jets(a)
            for index,key in ((3,'PX'),(4,'GX')):
                # Independent partial derivatives combined along the radial flow.
                direct=(mp.diff(lambda yy:c.state(a['eps'],yy,a['X'],a['F'])[key],a['y'])/a['ry']
                    +a['z']*mp.diff(lambda xx:c.state(a['eps'],a['y'],xx,a['F'])[key],a['X']))/a['z']
                self.assertLess(abs(jet[index]-direct)/max(abs(direct),1),mp.mpf('1e-40'))


if __name__=='__main__':unittest.main()
