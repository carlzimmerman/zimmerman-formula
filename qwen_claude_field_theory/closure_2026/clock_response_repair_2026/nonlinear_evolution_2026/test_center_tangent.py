#!/usr/bin/env python3
"""A regular mixed derivative must agree with the center action equation."""
import unittest
import numpy as np
from evolve import Evolution,derivatives
from project import project_state,regular_center,radial_profiles,match_odd_center_rate


class CenterTangency(unittest.TestCase):
    def test_origin_closure_keeps_manufactured_gradient_accuracy(self):
        errors=[];adjustments=[]
        for n in (33,65,129):
            r=np.linspace(0,1,n);potential=np.exp(-r*r)
            raw=derivatives(potential,r[1])[0]
            corrected=match_odd_center_rate(r,raw,-2.)
            exact=-2*r*np.exp(-r*r)
            np.testing.assert_array_equal(corrected[2:],raw[2:])
            self.assertEqual(corrected[0],0.)
            errors.append(max(abs(corrected[:-2]-exact[:-2])))
            adjustments.append(abs(corrected[1]-raw[1]))
        self.assertLess(errors[1],errors[0]/8)
        self.assertLess(errors[2],errors[1]/8)
        self.assertLess(adjustments[1],adjustments[0]/16)
        self.assertLess(adjustments[2],adjustments[1]/16)

    def test_clock_gradient_rate_preserves_action_center_jet(self):
        system=Evolution(.02,.3,129,3.,.01,1e-6)
        state=system.initial.copy();r=system.r
        state[4]+=1e-6*np.exp(-(r/.3)**2)
        state[5]=1e-5*r*np.exp(-(r/.3)**2)
        state=project_state(0.,state,r,system.model)
        f=system.fields(0.,state);rate,_=system.rhs(0.,state)
        center=regular_center(0.,state,r,system.model)
        target=f['rate'][0,3]*center['Q_c']+f['N'][0]*center['Q2']
        actual=radial_profiles(r,rate[1],rate[4],rate[5],rate[6],rate[7])[2](0.,1)
        self.assertLess(abs(actual-target),1e-10)


if __name__=='__main__':unittest.main(verbosity=2)
