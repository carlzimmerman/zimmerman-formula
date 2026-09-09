#!/usr/bin/env python3
import unittest
import mpmath as mp
import ic11_clock_pressure as pressure


class CombinedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps=60

    def model(self):
        return __import__("ic12_combined_transition")

    def test_new_pressure_branch_initial_conditions(self):
        model=self.model()
        for S in (mp.mpf('.1'),mp.mpf('.2')):
            bg=pressure.state(S)
            point=[-3*mp.exp(-mp.mpf(1)/6)*bg['H'],S+bg['w'],bg['u']]
            actual=model.at_point(point)
            self.assertLess(mp.norm(actual['gradient'][1:3,:]),mp.mpf('1e-45'))
            self.assertLess(abs(actual['physical_H']-bg['physical_H']),mp.mpf('1e-43'))

    def test_combined_switch_jets_match_raw_hamiltonian(self):
        model=self.model()
        xi,u=mp.mpf('.23'),mp.mpf('.63')
        point=[-3*mp.mpf('1.17')/mp.exp((4-3*u)*xi),xi,u]
        bg=model.at_point(point)
        for i in range(3):
            self.assertLess(abs(bg['gradient'][i]-mp.diff(model.raw_density,tuple(point),tuple(int(k==i) for k in range(3)))),mp.mpf('1e-42'))
            for j in range(3):
                self.assertLess(abs(bg['hessian'][i,j]-mp.diff(model.raw_density,tuple(point),tuple(int(k==i)+int(k==j) for k in range(3)))),mp.mpf('1e-39'))

    def test_actual_continuation_and_UV_identity(self):
        model=self.model()
        states,failure=model.continuation()
        self.assertIsNone(failure)
        self.assertEqual(len(states),501)
        self.assertTrue(any(bg['eta']<mp.mpf('.999') for bg in states))
        for bg in states:
            self.assertLess(mp.norm(bg['gradient'][1:3,:]),mp.mpf('1e-40'))
            self.assertLess(abs(bg['scalar_UV_kinetic']-bg['scalar_UV_identity']),mp.mpf('1e-40'))
            self.assertLess(abs(bg['tensor_speed_squared']-1),mp.mpf('1e-45'))
        for bg in states[::100]:
            self.assertLess(mp.norm(bg['preservation_residual']),mp.mpf('1e-40'))
            self.assertEqual(bg['dirac_rank'],4)
        self.assertGreater(states[200]['scalar_UV_kinetic'],0)
        self.assertLess(states[220]['scalar_UV_kinetic'],0)
        bg=states[220]
        mixing=bg['hessian'][1:3,0]/2
        Q=bg['auxiliary']+mp.mpf('1e16')*bg['G']
        finite=bg['scalar_UV_kinetic']-(mixing.T*(Q**-1)*mixing)[0]
        self.assertLess(finite,0)


if __name__=='__main__':
    unittest.main()
