#!/usr/bin/env python3
"""Exact inverse identities and bounded independent 3x3-coordinate checks."""
from functools import lru_cache
from pathlib import Path
import sys
import unittest
import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import conformal_inverse as source


@lru_cache(None)
def system():
    r,g,gr,F,f,X,p,z=s.symbols("r g gr F f X p z",nonzero=True)
    B=1+2*r*g; Br=2*g+2*r*gr; b=Br/(2*B); U=p*p/B
    K=3*f*f/(2*F);Kx=-3*f**3/(2*F**2);a=g+2/r
    pressure=(2*f*z*a+K*z*z)/B
    Pz=s.diff(pressure,z)
    R0=f*s.diff(pressure,F)*z+s.diff(pressure,r)+s.diff(pressure,g)*gr
    rho=(1-1/B)/r**2+Br/(B*B*r)
    pt=(gr+g*g-g*b+(g-b)/r)/B
    Cj=2*X*(U/X-r*g)/(p*r)
    Achi=f*(rho-2*pt)-Kx*z*z/B-2*K*(g-b+2/r)*z/B
    Lbase=2*F*rho+pressure-2*f*(2/r-b)*z/B+K*z*z/B
    M=s.Matrix([[Pz,-z,0],[-2*K/B,1,-Cj],[2*f/B,0,2*X*z/p]])
    rhs=s.Matrix([-R0,-Achi,Lbase])
    slope=z/Pz
    M2=s.Matrix([[1-2*K*slope/B,-Cj],[2*f*slope/B,2*X*z/p]])
    determinant=4*f*z*(2*X+U)/(B*p*r)
    angular_coeff=s.Matrix([[2*f/B,0,-p*z/B]])
    angular_const=2*F*pt-pressure+2*f*(g-b+1/r)*z/B-K*z*z/B
    numeric=s.lambdify((r,g,gr,F,f,X,p,z),(M,rhs,pressure),"numpy",cse=True)
    return locals()


def independent_gradient_solution(eps,y,X,U,z,sigma):
    """Construct the unsimplified 3x3 from the independently varied equations."""
    a=source.metric(eps,y)
    M,rhs,P=system()["numeric"](a["r"],a["g"],a["gr"],(1+sigma*X)/2,
                                sigma/2,X,np.sqrt(a["B"]*U),z)
    zr,px,gx=np.linalg.solve(M,np.asarray(rhs).reshape(3))
    return zr,px,gx,P,a


class ConformalInverseStructure(unittest.TestCase):
    def test_three_by_three_determinant(self):
        d=system()
        self.assertEqual(s.factor(d["M"].det()-d["determinant"]),0)

    def test_two_by_two_determinant_and_pressure_fold(self):
        d=system()
        root=d["a"]+3*d["f"]*d["z"]/(2*d["F"])
        expected=2*d["z"]*(2*d["X"]+d["U"])/(d["p"]*d["r"]*root)
        self.assertEqual(s.factor(d["M2"].det()-expected),0)
        self.assertEqual(s.factor(d["Pz"]*d["M2"].det()-d["M"].det()),0)
        self.assertEqual(s.factor(root**2-d["a"]**2-3*d["B"]*d["pressure"]/(2*d["F"])),0)
        fold=-2*d["F"]*d["a"]/(3*d["f"])
        self.assertEqual(s.factor(d["Pz"].subs(d["z"],fold)),0)
        atfold=s.factor(d["M"].det().subs(d["z"],fold))
        target=-8*d["F"]*d["a"]*(2*d["X"]+d["U"])/(3*d["B"]*d["p"]*d["r"])
        self.assertEqual(s.factor(atfold-target),0)

    def test_angular_residual_is_an_exact_linear_combination(self):
        d=system()
        weights=s.Matrix([[d["r"]/2,d["r"]*d["z"]/2,-d["r"]*d["g"]/2]])
        self.assertTrue(all(s.factor(v)==0 for v in weights*d["M"]-d["angular_coeff"]))
        self.assertEqual(s.factor((weights*d["rhs"])[0]+d["angular_const"]),0)

    def test_zero_gradient_requires_zero_target_density(self):
        d=system()
        atzero={d["z"]:0}
        self.assertEqual(d["pressure"].subs(atzero),0)
        self.assertEqual(d["R0"].subs(atzero),0)
        self.assertEqual(s.factor(d["Pz"].subs(atzero)-2*d["f"]*d["a"]/d["B"]),0)
        self.assertEqual(s.factor(d["Lbase"].subs(atzero)-2*d["F"]*d["rho"]),0)
        # Once radial preservation forces z'=0, the density row is 0=2F rho.
        self.assertEqual(d["M"][2,2].subs(atzero),0)

    def test_exact_exponential_target_density_reduction(self):
        r,y,e=s.symbols("r y e",nonzero=True)
        mu=1-e;lam=mu+y*e
        yr=-2*y*mu/(r*lam)
        B=1/(1-2*r*y);Br=2*(y+r*yr)*B*B
        geometric=(1-1/B)/r**2+Br/(B*B*r)
        target=4*y*y*e/(r*lam)
        self.assertEqual(s.factor(geometric-target),0)
        # e=exp(-y); positivity for finite positive r,y is proved in Lean.

    def test_zero_pressure_other_branch_is_not_zero_gradient(self):
        d=system()
        other=-4*d["F"]*d["a"]/(3*d["f"])
        self.assertEqual(s.factor(d["pressure"].subs(d["z"],other)),0)
        self.assertEqual(s.factor(d["M"].det().subs(d["z"],other)
                         +16*d["F"]*d["a"]*(2*d["X"]+d["U"])/(3*d["B"]*d["p"]*d["r"])),0)

    def test_root_inverse_and_curvatures_in_independent_gradient_coordinates(self):
        cases=[(1e-6,.1,.1,.25,1.),(1e-6,1.,.001,.75,.5),(1e-6,2.,.1,1.25,1.5)]
        for eps,y,sigma,b,dscale in cases:
            X,U,P=source.initial(eps,y,sigma,b,dscale)
            old,pxx,gxx=source.action_curvatures(eps,y,X,U,P,sigma)
            zr,px,gx,pressure,a=independent_gradient_solution(eps,y,X,U,old["z"],sigma)
            np.testing.assert_allclose([zr,px,gx,pressure],[old["zr"],old["PX"],old["GX"],P],rtol=2e-9,atol=1e-15)
            point=np.array([y,X,U,old["z"]])
            tangent=np.array([1/a["ry"],old["z"],-2*a["g"]*(2*X+U)-2*old["z"],zr])
            h=1e-25
            perturbed=independent_gradient_solution(eps,*(point+1j*h*tangent),sigma)
            independent=np.imag(perturbed[1:3])/h/old["z"]
            np.testing.assert_allclose(independent,[pxx,gxx],rtol=2e-8,atol=1e-12)
            # Real central difference in the independent gradient chart.
            dr=1e-6*a["r"]
            plus=independent_gradient_solution(eps,*(point+dr*tangent),sigma)
            minus=independent_gradient_solution(eps,*(point-dr*tangent),sigma)
            finite=(np.array(plus[1:3])-np.array(minus[1:3]))/(2*dr*old["z"])
            np.testing.assert_allclose(finite,[pxx,gxx],rtol=3e-5,atol=1e-9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
