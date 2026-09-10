#!/usr/bin/env python3
"""Exact non-affine inverse algebra; no numerical or full-DOF certificate."""
from functools import lru_cache
import importlib.util
from pathlib import Path
import unittest

import sympy as s


@lru_cache(None)
def system():
    r,g,gr,F,f,j,X,p,z=s.symbols("r g gr F f j X p z",nonzero=True)
    B=1+2*r*g;Br=2*g+2*r*gr;b=Br/(2*B);U=p*p/B;Q=2*X+U
    a=g+2/r;K=3*f*f/(2*F)
    DX=lambda expression:f*s.diff(expression,F)+j*s.diff(expression,f)
    Kx=DX(K)
    P=(2*f*z*a+K*z*z)/B
    Pz=s.diff(P,z)
    R0=s.diff(P,r)+gr*s.diff(P,g)+z*DX(P)
    rho=(1-1/B)/r**2+Br/(B*B*r)
    pt=(gr+g*g-g*b+(g-b)/r)/B
    Cj=2*X*(U/X-r*g)/(p*r)
    Achi=f*(rho-2*pt)-Kx*z*z/B-2*K*(g-b+2/r)*z/B
    Lbase=2*F*rho+P-2*j*z*z/B+K*z*z/B-2*f*(2/r-b)*z/B
    M=s.Matrix([[Pz,-z,0],[-2*K/B,1,-Cj],[2*f/B,0,2*X*z/p]])
    rhs=s.Matrix([-R0,-Achi,Lbase])
    determinant=4*f*z*Q/(B*p*r)
    return locals()


class NonaffineVariation(unittest.TestCase):
    def assert_zero(self, expression):
        self.assertEqual(s.factor(expression),0)

    def test_full_current_density_and_radial_rows(self):
        d=system();zprime,px,gx=s.symbols("zprime px gx")
        Echi=d["f"]*(d["rho"]-2*d["pt"])-d["Kx"]*d["z"]**2/d["B"]-2*d["K"]*(zprime+(d["g"]-d["b"]+2/d["r"])*d["z"])/d["B"]
        direct=s.Matrix([
            d["Pz"]*zprime+d["R0"]-px*d["z"],
            px+Echi-d["Cj"]*gx,
            2*(d["f"]*zprime+(d["j"]-d["K"]/2)*d["z"]**2+(2/d["r"]-d["b"])*d["f"]*d["z"])/d["B"]+2*d["X"]*gx*d["z"]/d["p"]-d["P"]-2*d["F"]*d["rho"]])
        for residual in direct-(d["M"]*s.Matrix([zprime,px,gx])-d["rhs"]):
            self.assert_zero(residual)
        self.assert_zero(d["Kx"]-3*d["f"]*d["j"]/d["F"]+3*d["f"]**3/(2*d["F"]**2))

    def test_determinant_has_no_conformal_invertibility_factor(self):
        d=system()
        self.assert_zero(d["M"].det()-d["determinant"])
        # Static inverse can be regular where the X-dependent conformal map is not.
        self.assert_zero(d["M"].det().subs(d["F"],d["X"]*d["f"])-d["determinant"])

    def test_j_control_is_only_a_first_column_shift(self):
        d=system();control=s.Matrix([-d["z"]**2/d["f"],0,0])
        for residual in d["rhs"].diff(d["j"])-d["M"]*control:
            self.assert_zero(residual)
        self.assertEqual(d["M"].diff(d["j"]),s.zeros(3))

    def test_F_gradient_coordinates_remove_j(self):
        d=system();w,wp,kap,gam=s.symbols("w wp kap gam")
        replacement={d["z"]:w/d["f"]}
        P=s.factor(d["P"].subs(replacement))
        Pw=s.diff(P,w)
        Rw=s.diff(P,d["r"])+d["gr"]*s.diff(P,d["g"])+w*s.diff(P,d["F"])
        A=d["rho"]-2*d["pt"]+3*w*w/(2*d["F"]**2*d["B"])-3*(d["g"]-d["b"]+2/d["r"])*w/(d["F"]*d["B"])
        L=2*d["F"]*d["rho"]+P+3*w*w/(2*d["F"]*d["B"])-2*(2/d["r"]-d["b"])*w/d["B"]
        Mw=s.Matrix([[Pw,-w,0],[-3/(d["F"]*d["B"]),1,-d["Cj"]],[2/d["B"],0,2*d["X"]*w/d["p"]]])
        rhsw=s.Matrix([-Rw,-A,L])
        oldv=s.Matrix([(wp-d["j"]*w*w/d["f"]**2)/d["f"],d["f"]*kap,d["f"]*gam])
        rows=s.diag(1,1/d["f"],1)*(d["M"].subs(replacement)*oldv-d["rhs"].subs(replacement))
        for residual in rows-(Mw*s.Matrix([wp,kap,gam])-rhsw):
            self.assert_zero(residual)
        self.assert_zero(Mw.det()-4*w*d["Q"]/(d["B"]*d["p"]*d["r"]))
        self.assertFalse(any(expression.has(d["f"],d["j"]) for expression in list(Mw)+list(rhsw)))

    def test_angular_equation_remains_dependent(self):
        d=system();zprime,px,gx=s.symbols("zprime px gx")
        ang=2*d["F"]*d["pt"]-d["P"]-gx*d["p"]*d["z"]/d["B"]+2*(d["f"]*zprime+d["j"]*d["z"]**2+(d["g"]-d["b"]+1/d["r"])*d["f"]*d["z"])/d["B"]-d["K"]*d["z"]**2/d["B"]
        weights=s.Matrix([[d["r"]/2,d["r"]*d["z"]/2,-d["r"]*d["g"]/2]])
        self.assert_zero(ang-(weights*(d["M"]*s.Matrix([zprime,px,gx])-d["rhs"]))[0])

    def test_zero_gradient_and_pressure_fold(self):
        d=system();at_zero={d["z"]:0}
        self.assert_zero(d["P"].subs(at_zero))
        self.assert_zero(d["R0"].subs(at_zero))
        self.assert_zero(d["Pz"].subs(at_zero)-2*d["f"]*d["a"]/d["B"])
        self.assert_zero(d["Lbase"].subs(at_zero)-2*d["F"]*d["rho"])
        fold=-2*d["F"]*d["a"]/(3*d["f"])
        self.assert_zero(d["Pz"].subs(d["z"],fold))
        self.assert_zero(d["M"].det().subs(d["z"],fold)+8*d["F"]*d["a"]*d["Q"]/(3*d["B"]*d["p"]*d["r"]))

    def test_total_action_curvature_control(self):
        F,f,j,z,zr0,X,U,r,g,gr=s.symbols("F f j z zr0 X U r g gr",nonzero=True)
        k=s.Function("k")(F,f*z,X,U,r,g)
        variables=(F,f,X,U,r,g,z)
        direction=(f*z,j*z,z,-2*g*(2*X+U)-2*z,1,gr,zr0-j*z*z/f)
        PX=f*k
        PXX=sum(s.diff(PX,var)*vel for var,vel in zip(variables,direction))/z
        self.assert_zero(s.diff(PXX,j)-PX/f)
        # k is an arbitrary smooth solved function, so the same identity applies
        # independently to G_X/f; no equation for k was substituted here.

    def test_matched_mass_curvatures_cancel_common_j(self):
        j,f,PX,GX,p1,p2,g1,g2=s.symbols("j f PX GX p1 p2 g1 g2",nonzero=True)
        self.assert_zero((p1+j*PX/f)-(p2+j*PX/f)-(p1-p2))
        self.assert_zero((g1+j*GX/f)-(g2+j*GX/f)-(g1-g2))

    def test_light_quadratic_interpolation_and_isotropic_policy(self):
        I,R,beta,d,delta,t=s.symbols("I R beta d delta t",real=True)
        K=I-delta;T=-beta*delta
        q=K+T-2*d*t+(R-T)*t*t
        self.assert_zero(q-((1-t)*q.subs(t,0)+t*q.subs(t,1)-(R-T)*t*(1-t)))
        isotropic_delta=-R/beta
        self.assert_zero(q.subs({delta:isotropic_delta,t:1})-(I+R*(1+1/beta)-2*d))

    def test_dimensionful_target_is_a_conditional_normalization(self):
        a0,c,R,Gb,M,y,mu=s.symbols("a0 c R Gb M y mu",nonzero=True)
        r=a0*R/c**2;eps2=Gb*M*a0/c**4
        # This is a change-of-units identity, not derivation of epsilon from
        # an interior source or proof that Gb equals measured Newton's G.
        self.assert_zero((r*r*y*mu-eps2)*c**4/(a0*R*R)-(a0*y*mu-Gb*M/(R*R)))

    def test_Einstein_frame_action_curvature_control(self):
        X,F,f,j,P,PX,GX,PXX0,GXX0=s.symbols("X F f j P PX GX PXX0 GXX0",nonzero=True)
        C=2*F;C1=2*f;C2=2*j;D=C-X*C1
        PXX=PXX0+j*PX/f;GXX=GXX0+j*GX/f
        Pt1=(PX-2*C1*P/C)/D
        Gt1=C*GX/D
        Pt2=C*C*(PXX-2*C2*P/C-2*C1*PX/C+2*C1*C1*P/C**2)/D**2+C*C*X*C2*(PX-2*C1*P/C)/D**3
        Gt2=C*C*(C1*GX+C*GXX)/D**2+C**3*X*C2*GX/D**3
        alpha=2*C**3/(C1*D**2)
        self.assert_zero(s.diff(Pt2,j)-alpha*Pt1)
        self.assert_zero(s.diff(Gt2,j)-alpha*Gt1)
        x=s.symbols("x",real=True);c=s.Function("C")(x)
        self.assert_zero(s.diff(x/c,x)-(c-x*s.diff(c,x))/c**2)

    def test_Einstein_frame_enthalpy_and_beta_from_physical_jets(self):
        C,C1,X,GX,z,p,B,Darea=s.symbols("C C1 X GX z p B Darea",positive=True)
        Dfield=C-X*C1
        chi=X/C;Gchi=C*GX/Dfield;chir=Dfield*z/C**2
        self.assert_zero(2*chi*Gchi*chir/p-2*X*GX*z/(C*C*p))
        pE=p/(s.sqrt(C)*Darea);BE=B/Darea**2
        self.assert_zero(pE*pE/(2*BE*chi)-p*p/(2*B*X))
        d=system()
        weights=s.Matrix([[d["f"]*d["r"]/(2*d["F"]),
            1+d["f"]*d["r"]*d["z"]/(2*d["F"]),
            d["f"]*(1-d["g"]*d["r"])/(2*d["F"])]])
        mapped_current=s.Matrix([[0,1,-d["Cj"]-d["f"]*d["z"]*(d["U"]-d["X"])/(d["F"]*d["p"])]])
        for residual in weights*d["M"]-mapped_current:self.assert_zero(residual)
        self.assert_zero((weights*d["rhs"])[0]-2*d["f"]*d["P"]/d["F"])

    def test_primary_unitary_kinetic_degeneracy_and_shift(self):
        F,f,A,K,V,G=s.symbols("F f A K V G",nonzero=True)
        L=-2*F*K*K/3-2*f*A*K*V-3*f*f*A*A*V*V/(2*F)
        self.assert_zero(L+2*F*(K+3*f*A*V/(2*F))**2/3)
        Hess=s.hessian(L,(K,V))
        null=s.Matrix([-3*f*A/(2*F),1])
        for residual in Hess*null:self.assert_zero(residual)
        self.assert_zero(Hess.det())
        pi=s.Rational(3,2)*s.diff(L,K);pstar=s.diff(L,V)
        self.assert_zero(F*pstar-f*A*pi)
        # Boundary convention: ADM F R boundary removed; -G box(phi) not
        # integrated by parts. Its highest-velocity term is G(V+A*K).
        full=L+G*(V+A*K)
        pi_full=s.Rational(3,2)*s.diff(full,K);p_full=s.diff(full,V)
        self.assert_zero(F*(p_full-G)-f*A*(pi_full-s.Rational(3,2)*G*A))
        self.assertEqual(s.hessian(full,(K,V)),Hess)

    def test_correlated_KGB_principal_pencil_has_no_radial_control(self):
        path=Path(__file__).resolve().parents[2]/"ticking_kgb_inverse_2026"/"kgb_inverse.py"
        spec=importlib.util.spec_from_file_location("audited_kgb_principal",path)
        model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
        a=model.principal_template()
        B,p,v,g,r=s.symbols("B p v g r",positive=True)
        h,GX,P=s.symbols("h GX P",real=True)
        X=(v*v-p*p/B)/2
        PX=2*GX*(p*p/(B*r)-X*g)/p
        H=s.Matrix([[-g*p/B,v*g/s.sqrt(B),0,0],[v*g/s.sqrt(B),h,0,0],[0,0,p/(B*r),0],[0,0,0,p/(B*r)]])
        subs={a["G1"]:GX,a["P1"]:PX,a["P"]:P}
        subs.update(dict(zip(a["v"],[-v,p/s.sqrt(B),0,0])))
        subs.update({a["H"][i,j]:H[i,j] for i in range(4) for j in range(i,4)})
        slope=(PX*a["M"].diff(a["P2"])+GX*a["M"].diff(a["G2"])).subs(subs,simultaneous=True)
        stress=a["T"].subs(subs,simultaneous=True)
        beta=p*p/(2*B*X);E=stress[0,0]+P
        target=s.diag(E,0,beta*E,beta*E)
        for residual in slope-target:self.assert_zero(residual)


if __name__=="__main__":
    unittest.main(verbosity=2)
