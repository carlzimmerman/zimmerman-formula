"""Controls for the pressure-enabled inverse; no prescribed candidate PASS."""
import importlib.util
from pathlib import Path
import unittest


class PressureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=Path(__file__).with_name('shared_pressure.py')
        cls.present=path.exists()
        if cls.present:
            spec=importlib.util.spec_from_file_location('pressure',path)
            cls.model=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.model)

    def setUp(self):
        self.assertTrue(self.present,'pressure inverse not implemented')

    def test_einstein_pressure_and_density_elimination(self):
        a=self.model.symbolic_reduction()
        self.assertTrue(all(x==0 for x in a['Einstein_residuals']))

    def test_radial_current_and_density_are_both_solved(self):
        a=self.model.symbolic_reduction()
        self.assertTrue(all(x==0 for x in a['scalar_residuals']))

    def test_schwarzschild_zero_density_control(self):
        self.assertEqual(self.model.symbolic_reduction()['Schwarzschild_density'],0)

    def test_local_reconstructed_stress_is_independently_checked(self):
        a=self.model.local('1e-6',1.0,0.0,0.15,1e6)
        self.assertLess(a['relative_stress_error'],1e-7)
        self.assertLess(a['relative_current_error'],1e-7)

    def test_high_acceleration_cancellation_control(self):
        path=Path(__file__).with_name('precision_check.py')
        self.assertTrue(path.exists(),'high-precision independent control missing')
        spec=importlib.util.spec_from_file_location('precision',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        a=module.check('1e-6','20','-15.610882545637942','.2795108412451867','10000')
        self.assertLess(float(a['relative_stress_error']),1e-35)

    def test_free_second_derivative_has_action_derived_health_invariant(self):
        path=Path(__file__).with_name('jet_window.py')
        self.assertTrue(path.exists(),'general kinetic-curvature window missing')
        spec=importlib.util.spec_from_file_location('jet_window',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        a=module.derive()
        self.assertTrue(all(x==0 for x in a['slope_residuals']))
        self.assertEqual(a['invariant_derivative'],0)
        self.assertIn('regular_slope_residuals',a)
        self.assertTrue(all(x==0 for x in a['regular_slope_residuals']))

    def test_jet_window_accepts_canonical_cone_and_rejects_negative_invariant(self):
        path=Path(__file__).with_name('jet_steering.py')
        self.assertTrue(path.exists(),'constructive health-window solver missing')
        spec=importlib.util.spec_from_file_location('steering',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        self.assertTrue(module.window(4.,0.,-1.,1.)['exists'])
        self.assertFalse(module.window(-1.,0.,-1.,1.)['exists'])

    def test_regular_chart_crosses_zero_kinetic_slope(self):
        path=Path(__file__).with_name('regular_clock.py')
        self.assertTrue(path.exists(),'regular P_X=0 chart missing')
        spec=importlib.util.spec_from_file_location('regular',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        g=self.model.geometry(1e-6,1.,0.,.1,1.)
        W=g['r']*g['g'];z=W/(2e-6*(2+W))
        a=module.local(1e-6,1.,0.,z,0.,-1.)
        self.assertTrue(a['finite'])
        self.assertLess(abs(a['PX']),1e-8)
        self.assertLess(a['relative_stress_error'],1e-7)

    def test_constructed_jet_is_healthy_in_high_precision(self):
        def get(name):
            spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'))
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            return module
        steering=get('jet_steering');precision=get('precision_check')
        choice=steering.choose(1e-6,20.,0.,.5,0.,1.)
        self.assertIsNotNone(choice['selected'])
        self.assertIn('pressure',__import__('inspect').signature(precision.check).parameters)
        a=precision.check('1e-6','20','0','.5','1',pressure='0',pxx=str(choice['PXX']))
        self.assertLess(float(a['relative_stress_error']),1e-35)
        self.assertTrue(a['healthy'])


if __name__=='__main__':unittest.main()
