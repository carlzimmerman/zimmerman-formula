#!/usr/bin/env python3
"""Bounded static clock elimination of the unchanged constitutive action.

This freezes the metric and all explicit clock-dependent coefficients. It is
not an Einstein solution, a time evolution, or a hyperbolicity certificate.
"""
import argparse
import ast
from functools import lru_cache
import json
from pathlib import Path
import sys

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
STATE = BASE / "inhomogeneous_charge_2026/exterior/run_001/result.json"
sys.path.insert(0, str(BASE / "nonlinear_evolution_2026"))
from constitutive import Model


class StaticClock:
    def __init__(self):
        self.state = json.loads(STATE.read_text())["rows"][0]
        self.Q = self.state["physical_Q"]
        self.s = self.state["clock_rate"]
        self.tau = self.state["tau"]
        self.model = Model(0.01, gamma=self.state["gamma"])
        self.bg = self.model.background(self.tau)
        self.j0 = self.model.jets(self.tau, self.Q**2, 0.0)
        b = self.bg
        self.C = b["U"] - 2*b["d"]*b["ell"] - 2*self.model.gamma*b["q"]**2*b["qdot"]
        self.k = 2*b["d"]*np.sqrt(b["ell"])
        W, W1, W2, P1, P2 = (self.j0[x] for x in ("W", "W_Y", "W_YY", "P_X", "P_XX"))
        self.F = W - 2*self.Q**2*W1
        self.A = -2*self.Q*W1/self.F
        r = 1-self.Q*self.A
        self.B = (-W*self.A**3/2 + W1*(self.A*r*r-self.Q*self.A**2*r)
                  - 2*self.Q*W2*r**3)/self.F
        self.c2 = -P1 + self.s*W1*W/self.F
        self.c4 = P2/2+self.s*(-W*self.A**4/8+W1*self.A**2*r*r/2+W2*r**4/2)
        self.L0 = self.j0["P"]+self.s*W

    def evaluate(self, u, z):
        """Chain-rule derivatives of the invariant P(X)+s0 sqrt(1-z²)W(Y)."""
        if abs(z) >= 1:
            raise ValueError("clock gradient is not timelike")
        Q, s0 = self.Q, self.s
        D = 1-z*z
        r = np.sqrt(D)
        v = u-Q*z
        X, Y = Q*Q-u*u, v*v/D
        j = self.model.jets(self.tau, X, Y)
        W, W1, W2 = j["W"], j["W_Y"], j["W_YY"]
        Yu, Yz = 2*v/D, -2*Q*v/D+2*z*v*v/D**2
        Yuu = 2/D
        Yuz = -2*Q/D+4*z*v/D**2
        Yzz = 2*Q*Q/D-8*Q*z*v/D**2+2*v*v/D**2+8*z*z*v*v/D**3
        rz, rzz = -z/r, -1/r**3
        L = j["P"]+s0*r*W
        Lu = -2*u*j["P_X"]+s0*r*W1*Yu
        Lz = s0*(rz*W+r*W1*Yz)
        Luu = -2*j["P_X"]+4*u*u*j["P_XX"]+s0*r*(W2*Yu*Yu+W1*Yuu)
        Luz = s0*(rz*W1*Yu+r*(W2*Yz*Yu+W1*Yuz))
        Lzz = s0*(rzz*W+2*rz*W1*Yz+r*(W2*Yz*Yz+W1*Yzz))
        qclock=(Q-u*z)/r
        Tclock=W-2*qclock*qclock*W1
        transverse_clock=-s0*Tclock/r
        transverse_schur=-2*j["P_X"]+2*s0*r*W1*W/Tclock
        return dict(u=float(u), z=float(z), X=float(X), Y=float(Y), L=float(L),
                    Lu=float(Lu), Lz=float(Lz), Luu=float(Luu), Luz=float(Luz),
                    Lzz=float(Lzz), schur=float(Luu-Luz*Luz/Lzz),
                    transverse_clock=float(transverse_clock),
                    transverse_schur=float(transverse_schur),
                    P_log_numerator=float(j["domain_denominator"]),
                    P_log_denominator=float(self.bg["U"]-2*self.bg["d"]*self.bg["q"]**2),
                    W_sqrt_argument=float(1+Y/self.bg["ell"]),
                    clock_timelike_margin=float(D))

    def radical(self, u, z):
        """Independent exact square-root reduction, without constitutive jets."""
        ell, Q = self.bg["ell"], self.Q
        D, a = 1-z*z, Q*Q-ell
        T = ell+u*u-2*Q*u*z+a*z*z
        E = -self.C*z/np.sqrt(D)+self.k*(a*z-Q*u)/np.sqrt(T)
        E_z = -self.C/D**1.5+self.k*ell*(a-u*u)/T**1.5
        return dict(clock_lagrangian=float(self.s*(self.C*np.sqrt(D)+self.k*np.sqrt(T))),
                    Lz=float(self.s*E), Lzz=float(self.s*E_z))

    def solve(self, u):
        if u == 0:
            return 0.0
        if u < 0:
            return -self.solve(-u)
        # The README proves uniqueness and nondegeneracy on this interval for
        # these positive coefficients; this is not an arbitrary root switch.
        return float(brentq(lambda z: self.radical(u, z)["Lz"], -1+1e-12, 0,
                            xtol=5e-16, rtol=4*np.finfo(float).eps))

    def row(self, u):
        return self.evaluate(u, self.solve(u))

    def high_precision_root(self, key, u0):
        """80 digits applied to rounded model inputs, not interval certification."""
        mp.mp.dps = 80
        m = lambda x: mp.mpf(str(float(x)))
        Q, s0, ell = map(m, (self.Q, self.s, self.bg["ell"]))
        U, d, qb, H, gam = map(m, (self.bg["U"], self.bg["d"], self.bg["q"], self.bg["H"], self.model.gamma))
        # Reconstruct dependent coefficients at high precision from the same
        # rounded primitive model data, rather than rounding C and k again.
        C=U-2*d*ell-2*gam*qb*qb*m(self.bg["qdot"])
        k=2*d*mp.sqrt(ell)
        def lag(u, z):
            X = Q*Q-u*u
            P = -U*mp.log((U-2*d*X)/(U-2*d*qb*qb))/2+3*gam*qb*H*(X-qb*qb)
            return P+s0*(C*mp.sqrt(1-z*z)+k*mp.sqrt(ell*(1-z*z)+(u-Q*z)**2))
        def flux(u, z):
            return mp.diff(lambda zz: lag(u, zz), z)
        def target(u, z):
            if key == "Lu":
                return mp.diff(lambda uu: lag(uu, z), u)
            Luu = mp.diff(lambda uu: lag(uu, z), u, 2)
            Luz = mp.diff(lambda uu: flux(uu, z), u)
            Lzz = mp.diff(lambda zz: flux(u, zz), z)
            return Luu-Luz*Luz/Lzz
        u, z = mp.findroot((flux, target), (m(u0), m(self.solve(u0))), tol=mp.mpf("1e-65"))
        result=dict(u=str(u), z=str(z), clock_residual=str(flux(u,z)),
                    target_residual=str(target(u,z)),
                    Lzz=str(mp.diff(lambda zz: flux(u,zz),z)),
                    scope="80-digit differentiation of the exact reduced radicals with rounded model inputs; not an interval certificate")
        if key == "Lu":
            rr=mp.sqrt(1-z*z)
            qc=(Q-u*z)/rr
            sc=s0*rr
            Y=(u-Q*z)**2/(1-z*z)
            X=Q*Q-u*u
            denominator=U-2*d*X
            p=U*d/denominator+3*gam*qb*H
            pxx=2*U*d*d/denominator**2
            W=C+k*mp.sqrt(ell+Y)
            WY=k/(2*mp.sqrt(ell+Y))
            WYY=-k/(4*(ell+Y)**mp.mpf("1.5"))
            T=W-2*qc*qc*WY
            K0=2*p+4*qc*qc*pxx
            G0=2*p-2*sc*WY*W/T
            t=2*gam*gam*X
            dK=t*(4*qc*qc-X)
            dG=-t*X
            K,G=K0+dK,G0+dG
            # Evaluate the existing helper unchanged. Extracting its function
            # avoids importing unrelated cosmological evolution modules.
            helper=BASE/"finite_gradient_metric_2026/cubic/cubic_debraiding.py"
            nodes=[n for n in ast.parse(helper.read_text()).body
                   if isinstance(n,ast.FunctionDef) and n.name in ("corrected","derive")]
            namespace={"np":np,"sy":sp,"lru_cache":lru_cache}
            exec(compile(ast.Module(body=nodes,type_ignores=[]),str(helper),"exec"),namespace)
            symbolic_checks=namespace["derive"]()["checks"]
            jf={key:float(value) for key,value in zip(("PX","PXX","W","WY","WYY"),(p,pxx,W,WY,WYY))}
            direct=namespace["corrected"](jf,float(qc),float(sc),float(Y),0.0,
                gamma=float(gam),M2=1.0,hessian_cov=np.zeros((4,4)))
            no_feedback=namespace["corrected"](jf,float(qc),float(sc),float(Y),0.0,
                gamma=0.0,M2=1.0,hessian_cov=np.zeros((4,4)))
            result["conditional_affine_transverse_principal"]=dict(
                scope="Conditional local affine chi Hessian=0, full cubic Einstein debraiding in clock-rest frame, transverse wavevector; not an on-shell cosmological or localized solution.",
                gamma_zero_control="Disables only explicit cubic metric feedback at the same finite-gamma constitutive jets; does not change or refit the action.",
                Q_clock=str(qc),s_clock=str(sc),X=str(X),Y=str(Y),
                lorentz_invariant_X_residual=str(qc*qc-Y-X),
                jets={key:str(value) for key,value in zip(("PX","PXX","W","WY","WYY"),(p,pxx,W,WY,WYY))},
                transverse_clock_F=str(T),K_without_metric_feedback=str(K0),
                G_without_metric_feedback_evaluated=str(G0),
                deltaK_metric=str(dK),deltaG_metric=str(dG),
                K_with_metric_feedback=str(K),G_with_metric_feedback=str(G),
                mixed_coefficient="0 (transverse wavevector and affine Hessian)",
                quarter_discriminant=str(K*G),speed_squared=str(G/K),imaginary_speed=str(mp.sqrt(-G/K)),
                nonaffine_positive_gradient_gate=dict(
                    frame="Clock rest frame with spatial chi gradient along x; H_ab=nabla_a nabla_b chi in that orthonormal frame.",
                    y_wave_B_H="-H_00+H_xx+H_zz",
                    z_wave_B_H="-H_00+H_xx+H_yy",
                    formula="At the same stationary constitutive jets: G_perp=4*gamma*B_H-2*gamma^2*X^2/M2.",
                    positive_G_iff_for_gamma_positive="2*M2*B_H > gamma*X^2",
                    B_H_threshold_at_M2_1=str(gam*X*X/2),
                    interpretation="A required Hessian threshold for positive diagonal transverse G, not an assigned Hessian or a coefficient change. Both transverse directions must be checked. Mixed principal terms and kinetic signs also matter; no full hyperbolicity conclusion follows from this inequality alone."),
                existing_corrected_helper_float=direct,
                existing_covariant_symbolic_checks=symbolic_checks,
                existing_corrected_without_feedback_float=no_feedback,
                float_gradient_error_against_high_precision=str(m(direct["gradient"])-G),
                interpretation="The exact stationary reduced gradient has transverse G0 numerically zero to high precision. The nonzero negative gamma-squared metric correction makes the conditional affine transverse discriminant negative; it does not certify an instability of an unsolved non-affine background.")
        return result


def run(points=2001, umax=0.01):
    if points<101 or not 0.002<=umax<=0.01:
        raise ValueError("Contract requires points>=101 and 0.002<=umax<=0.01")
    obj = StaticClock()
    if not all(x>0 for x in (obj.s,obj.F,obj.C,obj.Q,obj.bg["d"],obj.bg["ell"],obj.Q**2-obj.bg["ell"])):
        raise AssertionError("The documented branch proof hypotheses changed")
    grid = np.linspace(0, umax, points)
    rows = [obj.row(float(u)) for u in grid]
    radical_errors = {key: max(abs(row[key]-obj.radical(row["u"],row["z"])[key]) for row in rows)
                      for key in ("Lz", "Lzz")}
    roots = {}
    for key in ("schur", "Lu"):
        brackets = [(a["u"], b["u"]) for a,b in zip(rows[:-1],rows[1:]) if a[key]*b[key]<0]
        found = []
        for lo, hi in brackets:
            u = brentq(lambda x: obj.row(x)[key], lo, hi, xtol=5e-16)
            found.append(dict(bracket=[lo,hi], exact=row_to_summary(obj.row(u)),
                              high_precision=obj.high_precision_root(key,u)))
        roots[key] = found
        if len(found)!=1:
            raise AssertionError("Expected one sampled positive sign change for "+key+"; inspect changed output")
    gate=roots["Lu"][0]["high_precision"]["conditional_affine_transverse_principal"]
    if not (abs(mp.mpf(gate["G_without_metric_feedback_evaluated"]))<mp.mpf("1e-60")
            and mp.mpf(gate["K_with_metric_feedback"])>0
            and mp.mpf(gate["quarter_discriminant"])<0):
        raise AssertionError("Conditional affine transverse gate changed")
    errors = []
    for u in (0.0001,0.0002,0.0004,0.0008,0.001,0.0015,0.002,0.005,0.01):
        r = obj.row(u)
        zs = obj.A*u+obj.B*u**3
        ds = obj.c2*u*u+obj.c4*u**4
        exact_delta = r["L"]-obj.L0
        gs = 2*obj.c2*u+4*obj.c4*u**3
        hs = 2*obj.c2+12*obj.c4*u*u
        errors.append(dict(u=u, exact_z=r["z"], cubic_z=zs, z_absolute_error=abs(zs-r["z"]),
                           exact_action_delta=exact_delta, quartic_action_delta=ds,
                           action_delta_absolute_error=abs(ds-exact_delta),
                           exact_gradient=r["Lu"], cubic_gradient=gs,
                           gradient_absolute_error=abs(gs-r["Lu"]), exact_schur=r["schur"],
                           quadratic_schur=hs, schur_absolute_error=abs(hs-r["schur"])))
    W, W1, W2, P1, P2 = (float(obj.j0[x]) for x in ("W", "W_Y", "W_YY", "P_X", "P_XX"))
    coefficients = dict(F=obj.F,A=obj.A,B=obj.B,r=1-obj.Q*obj.A,c2=obj.c2,c4=obj.c4,
                        bare_c2=-P1+obj.s*W1,bare_c4=(P2+obj.s*W2)/2,
                        bare_PXX_plus_sWYY=P2+obj.s*W2,
                        schur_at_origin=2*obj.c2,Lzz_at_origin=-obj.s*obj.F,
                        quartic_schur_root=np.sqrt(-obj.c2/(6*obj.c4)),
                        quartic_stationary_root=np.sqrt(-obj.c2/(2*obj.c4)))
    return dict(scope="frozen-metric frozen-explicit-coefficient static 1D zero-clock-flux diagnostic",
                source=dict(path=str(STATE.relative_to(BASE)),index=0,tau=obj.tau,
                            Q=obj.Q,s0=obj.s,gamma=obj.model.gamma,reference_qbar=obj.bg["q"],
                            jets=dict(PX=P1,PXX=P2,W=W,WY=W1,WYY=W2)),
                coefficients=coefficients,
                branch_certificate_hypotheses=dict(C=obj.C,d=obj.bg["d"],ell=obj.bg["ell"],
                    Q_squared_minus_ell=obj.Q**2-obj.bg["ell"],F=obj.F,
                    assertion="For u>=0 and -1<z<=0, Lzz<=-s0*F<0; flux changes sign at endpoints, so a unique nondegenerate root exists."),
                bounded_scan=dict(u_min=0,u_max=umax,points=points,reflection="z(-u)=-z(u)",
                    max_abs_clock_residual=max(abs(x["Lz"]) for x in rows),
                    max_abs_z=max(abs(x["z"]) for x in rows),
                    min_abs_clock_block=min(abs(x["Lzz"]) for x in rows),
                    min_P_log_numerator=min(x["P_log_numerator"] for x in rows),
                    P_log_denominator=rows[0]["P_log_denominator"],
                    min_W_sqrt_argument=min(x["W_sqrt_argument"] for x in rows),
                    min_clock_timelike_margin=min(x["clock_timelike_margin"] for x in rows),
                    min_X=min(x["X"] for x in rows),
                    schur_min=min(x["schur"] for x in rows),schur_max=max(x["schur"] for x in rows),
                    independent_radical_max_absolute_errors=radical_errors),
                located_sign_changes=roots,series_errors=errors,
                non_claims=["No solution of the coupled Einstein-scalar-clock constraints or nonlinear field equations.",
                    "Explicit tau coefficient derivatives, nonstatic terms and curved-background terms were frozen away.",
                    "The constant-gamma cubic is a boundary term only after this flat static 1D restriction; its metric variation is not zero.",
                    "Zero integrated clock flux is a branch choice, not a global zero-mode or boundary-condition theorem.",
                    "A static Schur sign change is not a nonlinear hyperbolicity or stability certificate.",
                    "The scan and high precision controls are numerical, not interval-certified or exhaustive root counts."])


def row_to_summary(row):
    return {k:row[k] for k in ("u","z","Lu","Lz","schur","Lzz",
                              "transverse_clock","transverse_schur","X","Y")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--points", type=int, default=2001)
    parser.add_argument("--umax", type=float, default=0.01)
    parser.add_argument("--run-tests", action="store_true")
    args = parser.parse_args()
    test_result=None
    if args.run_tests:
        import unittest
        suite=unittest.defaultTestLoader.discover(str(HERE),pattern="test_clock_response.py")
        test_result=unittest.TextTestRunner(verbosity=2).run(suite)
        if not test_result.wasSuccessful():
            sys.exit(1)
    result = run(args.points,args.umax)
    if test_result is not None:
        result["unit_tests"]=dict(tests_run=test_result.testsRun,failures=len(test_result.failures),
                                  errors=len(test_result.errors),successful=test_result.wasSuccessful())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(dict(coefficients=result["coefficients"],
                         bounded_scan=result["bounded_scan"],
                         located_sign_changes=result["located_sign_changes"]),indent=2))
