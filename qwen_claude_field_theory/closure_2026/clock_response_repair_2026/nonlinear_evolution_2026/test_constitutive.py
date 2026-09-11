#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import unittest
import numpy as np

HERE=Path(__file__).resolve().parent


class ConstitutiveTests(unittest.TestCase):
    def test_full_jets_recover_fixed_slice_and_vary_off_branch(self):
        path=HERE/"constitutive.py"
        self.assertTrue(path.exists(),"off-branch constitutive evaluator is absent")
        spec=importlib.util.spec_from_file_location("evolution_constitutive",path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        oldspec=importlib.util.spec_from_file_location("old_initial_background",HERE.parent/"nonlinear_infall_2026/background.py")
        old=importlib.util.module_from_spec(oldspec);oldspec.loader.exec_module(old)
        model=module.Model(.03,gamma=1e-6)
        prior=old.background()
        jets=model.jets(0.,prior["q"]**2,0.)
        for new,previous in dict(P="P",P_X="PX",P_XX="PXX",P_t="Pt",P_Xt="PXt",
                                 P_tt="Ptt",W="W0",W_Y="WY",W_t="Wt",V_t="Vt",V_tt="Vtt").items():
            np.testing.assert_allclose(jets[new],prior[previous],rtol=2e-10,atol=2e-12)
        x=prior["q"]**2*.98;y=.003;dt=1e-5
        middle=model.jets(.01,x,y)
        left=model.jets(.01-dt,x,y);right=model.jets(.01+dt,x,y)
        for value,derivative in (("P","P_t"),("P_X","P_Xt"),("W","W_t"),("W_YY","W_YYt")):
            np.testing.assert_allclose((right[value]-left[value])/(2*dt),middle[derivative],rtol=2e-6,atol=2e-8)
        self.assertNotAlmostEqual(float(middle["P"]),0.,places=6)


if __name__=="__main__":unittest.main(verbosity=2)
