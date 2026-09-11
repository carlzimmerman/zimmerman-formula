#!/usr/bin/env python3
"""The radial constraint solver must preserve smooth spherical parity jets."""
import unittest
import numpy as np
import project
from unittest.mock import patch


class ProjectionProfiles(unittest.TestCase):
    def test_regular_even_odd_profiles_and_center_jets(self):
        r=np.linspace(0,1,33)
        b=1+2*r*r+3*r**4+.2*r**6
        u=2*r+3*r**3+.4*r**5
        self.assertTrue(hasattr(project,'radial_profiles'),'regular r-squared interpolation missing')
        bs,qs,us,ws,ds=project.radial_profiles(r,b,b,u,u,np.exp(-r*r))
        x=np.linspace(0,r[3],29)
        np.testing.assert_allclose(bs(x,2),4+36*x*x+6*x**4,atol=2e-10)
        np.testing.assert_allclose(us(x,1),2+9*x*x+2*x**4,atol=2e-10)
        np.testing.assert_allclose(us(x,2),18*x+8*x**3,atol=2e-10)
        for f in (bs,qs,ds):np.testing.assert_allclose(f(-x),f(x),atol=1e-12)
        for f in (us,ws):np.testing.assert_allclose(f(-x),-f(x),atol=1e-12)
        self.assertGreater(min(ds(np.linspace(0,1,301))),0.)

    def test_lapse_and_projection_share_the_regular_center(self):
        import evolve
        self.assertTrue(hasattr(project,'regular_center'),'shared action-derived center data missing')
        system=evolve.Evolution(.02,.3,65,3.,.01,1e-6)
        state=system.initial.copy();state[5]=1e-4*system.r*np.exp(-system.r**2)
        projected=project.project_state(0.,state,system.r,system.model)
        expected=project.regular_center(0.,projected,system.r,system.model)
        captured={};original=evolve.evaluate_center
        def record(values):
            captured.update(values)
            return original(values)
        with patch.object(evolve,'evaluate_center',record):system.fields(0.,state)
        for key,value in expected.items():self.assertAlmostEqual(captured[key],value,places=13)

    def test_radial_error_control_tracks_small_perturbations(self):
        import evolve
        system=evolve.Evolution(.02,.3,65,3.,.01,1e-6)
        original=project.solve_ivp;starts=[]
        def record(fun,span,y0,**kwargs):
            starts.append(np.array(y0))
            return original(fun,span,y0,**kwargs)
        with patch.object(project,'solve_ivp',record):
            project.project_state(0.,system.initial,system.r,system.model)
        self.assertLess(np.max(abs(starts[0])),1e-5)


if __name__=='__main__':unittest.main(verbosity=2)
