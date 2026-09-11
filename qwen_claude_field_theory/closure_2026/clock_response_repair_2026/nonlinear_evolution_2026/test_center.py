#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import unittest
import numpy as np

from constitutive import Model


class CenterTests(unittest.TestCase):
    def test_regular_center_recovers_initial_action_accelerations(self):
        path=Path(__file__).resolve().parent/"center.py"
        self.assertTrue(path.exists(),"regular origin action limit missing")
        spec=importlib.util.spec_from_file_location("center",path)
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        model=Model(.01);b=model.background(0);q,H=b["q"],b["H"]
        v=model.jets(0,q*q,0)
        v.update(a_c=1.,A2=.02/3,b2=0.,K_c=H,Q_c=q,Q2=0.,u1=0.,rho=.02,
                 constraint_addition=1.)
        mat,rhs=m.evaluate_center(v)
        N=.9973;hd,qd,nrr=np.linalg.solve(mat,rhs@np.array([N,1.]))
        J=2*q*v["P_X"]-6*v["gamma"]*H*q*q
        ea=N*.02/3-2*nrr+N*q*J+v["W"]+2*hd+2*v["gamma"]*q*q*qd
        self.assertLess(abs(ea),1e-11)
        B=2*v["P_X"]+4*q*q*v["P_XX"]-12*v["gamma"]*H*q
        chi=B*qd-6*v["gamma"]*q*q*hd+3*N*H*J+2*q*v["P_Xt"]+6*v["gamma"]*q*q*nrr
        self.assertLess(abs(chi),1e-11)


if __name__=="__main__":unittest.main(verbosity=2)
