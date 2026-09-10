#!/usr/bin/env python3
"""Exact shared-mass inverse reductions; no seed scan or universal no-go."""
from functools import lru_cache
import importlib
from pathlib import Path
import sys
import unittest
import numpy as np
import sympy as s
import closed_inverse as closed


@lru_cache(None)
def reduced_inverse():
    r,g,gr,F,w,X,U=s.symbols("r g gr F w X U",nonzero=True)
    B=1+2*r*g;b=(g+r*gr)/B;p=s.sqrt(B*U);Q=2*X+U;a=g+2/r
    rho=(1-1/B)/r**2+2*b/(B*r)
    pt=(gr+g*g-g*b+(g-b)/r)/B
    P=(2*w*a+3*w*w/(2*F))/B
    Pw=s.diff(P,w)
    Rw=s.diff(P,r)+gr*s.diff(P,g)+w*s.diff(P,F)
    Aw=rho-2*pt+3*w*w/(2*F*F*B)-3*(a-b)*w/(F*B)
    L=2*F*rho+2*w*(g+b)/B+3*w*w/(F*B)
    S=2*F*a*rho+4*w*(r*g-1)/(r*r*B)
    gamma=p*r*S/(2*Q*w)
    W=B*(L-X*r*S/Q)/2
    H=((2/r+w/F)*U-(2*g+w/F)*X)/p
    kappa=2*P/F+H*gamma
    Cj=2*(U-X*r*g)/(p*r)
    M=s.Matrix([[Pw,-w,0],[-3/(F*B),1,-Cj],[2/B,0,2*X*w/p]])
    rhs=s.Matrix([-Rw,-Aw,L])
    L0=lambda expression:s.diff(expression,X)-2*s.diff(expression,U)
    return locals()


class SharedPreservation(unittest.TestCase):
    def zero(self,e):self.assertEqual(s.factor(e),0)

    def test_closed_inverse_solves_original_three_rows(self):
        d=reduced_inverse()
        for residual in d["M"]*s.Matrix([d["W"],d["kappa"],d["gamma"]])-d["rhs"]:
            self.zero(residual)
        self.zero(d["M"].det()-4*d["w"]*d["Q"]/(d["B"]*d["p"]*d["r"]))

    def test_geometry_source_collapses_to_linear_F_and_w(self):
        d=reduced_inverse()
        self.zero(d["S"]-(d["Aw"]*d["w"]+d["Rw"]+d["a"]*d["L"]))
        self.zero(s.diff(d["S"],d["F"],2))
        self.zero(s.diff(d["S"],d["w"],2))
        self.zero(s.diff(d["S"],d["F"],d["w"]))

    def test_pressure_chain_and_L0_identities(self):
        d=reduced_inverse();L0=d["L0"]
        self.zero(L0(d["P"]))
        L1P=s.diff(d["P"],d["F"])+(s.diff(d["P"],d["r"])+d["gr"]*s.diff(d["P"],d["g"])+d["W"]*s.diff(d["P"],d["w"]))/d["w"]
        self.zero(L1P-d["kappa"])
        self.zero(L0(d["gamma"])+d["gamma"]/d["U"])
        Rrad=d["a"]+3*d["w"]/(2*d["F"])
        self.zero(L0(d["kappa"])+2*d["gamma"]*Rrad/d["p"])
        self.zero(L0(d["W"])+d["B"]*d["w"]*d["gamma"]/d["p"])

    def test_signed_H_matching_quadratic_and_jacobian(self):
        d=reduced_inverse();v=s.symbols("v",positive=True)
        alpha=2/d["r"]+d["w"]/d["F"]
        eta=2*d["g"]+d["w"]/d["F"]
        numerator=alpha*d["U"]-eta*d["X"]
        self.zero(d["H"]*d["p"]-numerator)
        self.zero(numerator.subs(d["U"],v*v)-(alpha*v*v-eta*d["X"]))
        self.zero(s.diff(d["H"],d["U"])-(alpha*d["U"]+eta*d["X"])/(2*d["p"]*d["U"]))
        self.zero(s.diff(d["gamma"],d["U"])-d["gamma"]*(2*d["X"]-d["U"])/(2*d["U"]*d["Q"]))

    def test_first_and_next_action_jet_preservation(self):
        f,j,jprime,dk,A,B,A0,A1,B0,B1=s.symbols("f j jprime dk A B A0 A1 B0 B1")
        E=A+f*B
        N=A0+f*(A1+B0)+f*f*B1
        variables=(f,j,dk,A,B)
        flow=(j,jprime,E,A0+f*A1,B0+f*B1)
        D=lambda expression:sum(s.diff(expression,var)*vel for var,vel in zip(variables,flow))
        self.zero(D(f*dk)-(j*dk+f*E))
        self.zero(D(E)-(N+j*B))
        self.zero(D(D(f*dk))-(jprime*dk+2*j*E+f*(N+j*B)))
        self.zero(s.diff(D(f*dk),j)-dk)
        # The same arbitrary difference dk represents Δkappa or Δgamma.

    def test_first_determinant_tangency_identity(self):
        A,B,C,D,f,j,A0,A1,B0,B1,C0,C1,D0,D1=s.symbols("A B C D f j A0 A1 B0 B1 C0 C1 D0 D1")
        E1=A+f*B;E2=C+f*D;T=A*D-C*B
        variables=(A,B,C,D,f)
        flow=(A0+f*A1,B0+f*B1,C0+f*C1,D0+f*D1,j)
        derivative=lambda e:sum(s.diff(e,var)*vel for var,vel in zip(variables,flow))
        N1=A0+f*(A1+B0)+f*f*B1
        N2=C0+f*(C1+D0)+f*f*D1
        self.zero(derivative(T)-(N1*D-N2*B+E1*(D0+f*D1)-E2*(B0+f*B1)))
        self.zero(s.diff(derivative(T),j))

    def test_pivot_solvability_and_degenerate_control(self):
        N1,N2,B,D,j=s.symbols("N1 N2 B D j",nonzero=True)
        chosen=-N1/B
        self.zero((N1+j*B).subs(j,chosen))
        self.zero((N2+j*D).subs(j,chosen)-(N2*B-N1*D)/B)
        self.zero((N1+j*B).subs(B,0)-N1)
        self.zero((N2+j*D).subs(D,0)-N2)

    def test_H_coordinates_preserve_same_lower_constraints(self):
        P,F,Gamma,H1,H2,k1,k2,P1,P2,H,Gamma1,Gamma2=s.symbols("P F Gamma H1 H2 k1 k2 P1 P2 H Gamma1 Gamma2")
        self.zero((2*P/F+H1*Gamma)-(2*P/F+H2*Gamma)-Gamma*(H1-H2))
        # On common lower H and Gamma, differentiated kappa gaps triangularize.
        P1x,P2x,G1x,G2x,H1x,H2x,f,commonPx=s.symbols("P1x P2x G1x G2x H1x H2x f commonPx")
        difference=2*(P1-P2)/F+H1*Gamma1-H2*Gamma2
        variables=(F,P1,P2,H1,H2,Gamma1,Gamma2)
        flow=(f,P1x,P2x,H1x,H2x,G1x,G2x)
        derivative=sum(s.diff(difference,var)*vel for var,vel in zip(variables,flow))
        lower={P1:P,P2:P,H1:H,H2:H,Gamma1:Gamma,Gamma2:Gamma,P1x:commonPx,P2x:commonPx}
        self.zero(derivative.subs(lower)-H*(G1x-G2x)-Gamma*(H1x-H2x))

    def test_scaled_lower_map_extends_smoothly_to_zero_epsilon(self):
        eps,y,A,e,lam,F,w,X,u=s.symbols("eps y A e lam F w X u",positive=True)
        B=1/(1-2*eps*y/A)
        Pbar=s.cancel((2*w*(y*B+2*A/eps)+3*w*w/(2*F))*eps/B)
        Hbar=(2*A*u+eps*w*u/F-X*(2*y*B+w/F))/s.sqrt(B*u)
        S2=8*F*A*y*y*e/lam*(eps*y*B+2*A)+4*w*(eps*y*B/A-1)*A*A/B
        Gbar=s.sqrt(B*u)*S2/(2*A*(2*X+eps*u)*w)
        D=4*F*y*y*e/lam
        target=(4*A*w,(2*A*u-X*(2*y+w/F))/s.sqrt(u),A*s.sqrt(u)/X*(D/w-1))
        for out,expected in zip((Pbar,Hbar,Gbar),target):
            self.zero(out.subs(eps,0)-expected)

    def test_exact_nonzero_limiting_lower_jacobian(self):
        y,w,u,F,X,A,Ap,D,Dp,e=s.symbols("y w u F X A Ap D Dp e",nonzero=True)
        out=s.Matrix([4*A*w,(2*A*u-X*(2*y+w/F))/s.sqrt(u),A*s.sqrt(u)/X*(D/w-1)])
        Dy=lambda q:s.diff(q,y)+Ap*s.diff(q,A)+Dp*s.diff(q,D)
        J=s.Matrix.hstack(out.applyfunc(Dy),out.diff(w),out.diff(u))
        at=s.factor(J.det().subs({y:1,w:-F,u:X/A,Ap:1/(2*A),D:4*F*e,Dp:4*F*e*(1-e)}))
        reduced=s.factor(at.subs(A*A,1-e))
        polynomial=12*e**3-32*e*e+28*e+3
        self.zero(reduced+2*A*polynomial/X)
        self.zero(polynomial-(3+4*e*(2+2*(1-e)+3*(1-e)**2)))

    def test_closed_helper_matches_actual_inverse_and_complex_step(self):
        source_dir=Path(__file__).resolve().parents[2]/"kgb_nonaffine_clock_2026"
        sys.path.insert(0,str(source_dir))
        source=importlib.import_module("nonaffine_inverse")
        cases=[(1e-6,.1,.525,.05,.25,1.5,-1e5),
               (2e-6,1.,.7,-.04,.75,.5,0.),
               (4e-6,2.,.9,.08,1.25,2.,2e4)]
        for eps,y,F,f,bscale,dscale,j in cases:
            X=.5;a=closed.geometry(eps,y);U=bscale*X*a['r']*a['g']
            w=f*(-dscale*a['g'])
            new=closed.coefficients(eps,y,X,U,w,F,f,j)
            old=source.coefficients(eps,y,X,U,w/f,j0=j,F0=F,f0=f,X0=X)
            keys=('P','PX','GX','z','zr')
            np.testing.assert_allclose([new[k] for k in keys],[old[k] for k in keys],rtol=2e-9,atol=1e-12)
            point=np.array([y,X,U,w,F,f])
            flow=closed.flow_X(eps,y,X,U,w,F,f,j)
            direction=np.array([flow['y'],1.,flow['U'],flow['w'],flow['F'],flow['f']])
            h=1e-25
            varied=closed.coefficients(eps,*(point+1j*h*direction),j=j)
            # Differentiating the closed helper along the true X-flow includes
            # F_X=f and f_X=j; compare to the original physical-jet derivative.
            _,pxx,gxx=source.action_curvatures(eps,y,X,U,w/f,j0=j,F0=F,f0=f,X0=X)
            np.testing.assert_allclose(np.imag([varied['PX'],varied['GX']])/h,[pxx,gxx],rtol=2e-8,atol=1e-10)


if __name__=="__main__":unittest.main(verbosity=2)
