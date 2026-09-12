"""Geometry and dimensional normalization, independent of desired dispersion."""
import importlib.util
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent


class StudyTests(unittest.TestCase):
    def module(self):
        p=HERE/'study.py'
        self.assertTrue(p.exists(),'The data-to-field calculation is missing')
        s=importlib.util.spec_from_file_location('df2_study',p)
        m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
        return m

    def test_distance_changes_host_geometry_not_a0(self):
        m=self.module()
        close=m.geometry(17.6,17.6)
        far=m.geometry(17.6,21.3)
        self.assertLess(close['separation_kpc'],71.)
        self.assertGreater(far['separation_kpc'],3700.)
        self.assertEqual(close['a0_m_s2'],far['a0_m_s2'])
        self.assertGreater(close['external_over_a0']/far['external_over_a0'],40)

    def test_fixed_photometry_distance_scaling(self):
        m=self.module()
        a,b=m.geometry(17.6,21.3),m.geometry(20.,21.3)
        self.assertAlmostEqual(a['eta']/b['eta'],1.,places=12)
        self.assertAlmostEqual(a['stellar_mass_Msun']/b['stellar_mass_Msun'],(.88)**2,places=12)


if __name__=='__main__':unittest.main()
