#!/usr/bin/env python3
"""Independent identities and one frozen-state diagnostic, never a full solution.

Symbolic domain: real coefficients, s0>0, |z|<1; Schur divisions additionally
require nonzero clock Hessian blocks. Numerical input: the preexisting first
exterior state, unchanged P/W/V jets and gamma. No fitted coefficients.
"""
import argparse
import json
from pathlib import Path
import sys

import numpy as np
import sympy as sy
from scipy.optimize import root

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
STATE = BASE / "inhomogeneous_charge_2026/exterior/run_001/result.json"
sys.path.insert(0, str(BASE / "nonlinear_evolution_2026"))
from constitutive import Model


def exact_checks():
    u, z, up, zp, Q, s0 = sy.symbols("u z up zp Q s0", real=True)
    p, p2, w, d, e = sy.symbols("p p2 w d e", real=True)
    r = sy.sqrt(1-z*z)
    v = u-Q*z
    q = (Q-u*z)/r
    S = w-2*Q*Q*d
    P, W = sy.Function("P"), sy.Function("W")
    checks = {}

    def check(name, value):
        residual = sy.simplify(value)
        if residual != 0:
            raise AssertionError((name, residual))
        checks[name] = True

    # Independent quartic truncation before imposing the clock response.
    a, b = sy.symbols("a b")
    eps = sy.symbols("eps")
    zseries = a*eps+b*eps**3
    vv = eps-Q*zseries
    L4 = (-p*eps**2+p2*eps**4/2
          +s0*(w*(1-zseries**2/2-zseries**4/8)
               +d*vv**2*(1+zseries**2/2)+e*vv**4/2))
    a0 = -2*Q*d/S
    c2 = -p+s0*d*w/S
    c4 = p2/2+s0*(e*w**4/2+2*Q**2*d**3*w*(w-Q**2*d))/S**4
    check("quartic_coefficient", sy.expand(L4).coeff(eps, 4).subs(a, a0)-c4)
    check("quadratic_coefficient", sy.expand(L4).coeff(eps, 2).subs(a, a0)-c2)
    check("quartic_independent_of_cubic_clock_response",
          sy.diff(sy.expand(L4).coeff(eps, 4).subs(a, a0), b))

    # Covariant clock current after the one-dimensional static substitution.
    Jx = -w*z/r-2*q*d*v/r**2
    J0 = w/r+2*q*d*z*v/r**2
    check("clock_current_homogeneity_identity", J0+z*Jx-r*w)
    Lz = s0*(-w*z/r+d*r*sy.diff(v*v/r**2, z))
    check("clock_spatial_current_is_Lz_over_s0", Lz/s0-Jx)

    # Direct differentiation of a genuinely three-dimensional invariant.
    # up,zp are either one of the two transverse perturbation components.
    X3 = Q*Q-u*u-up*up
    Y3 = u*u+up*up-Q*Q+(Q-u*z-up*zp)**2/(1-z*z-zp*zp)
    L3 = P(X3)+s0*sy.sqrt(1-z*z-zp*zp)*W(Y3)

    def jets(expression):
        out = expression.subs({up: 0, zp: 0}).doit()
        replacements = {}
        for atom in out.atoms(sy.Subs):
            fn = atom.expr.expr.func if isinstance(atom.expr, sy.Derivative) else None
            if fn == P:
                replacements[atom] = p
            elif fn == W:
                replacements[atom] = d
        out = out.xreplace(replacements)
        out = out.replace(lambda arg: arg.func == W, lambda arg: w)
        return sy.simplify(out)

    Huu = -2*p+2*s0*r*d
    Huz = -2*s0*q*d
    Hzz = s0/r*(2*q*q*d-w)
    check("3d_transverse_uu", jets(sy.diff(L3, up, up))-Huu)
    check("3d_transverse_uz", jets(sy.diff(L3, up, zp))-Huz)
    check("3d_transverse_zz", jets(sy.diff(L3, zp, zp))-Hzz)
    hperp = -2*p+2*s0*r*d*w/(w-2*q*q*d)
    check("3d_transverse_schur", Huu-Huz**2/Hzz-hperp)
    Lu = -2*p*u+2*s0*d*v/r
    # Rotating both gradients differentiates the zero-clock-flux condition.
    check("rotation_clock_ward_identity", Huz*u+Hzz*z-Lz)
    check("rotation_scalar_ward_identity", Huu*u+Huz*z-Lu)
    check("schur_stationarity_identity", hperp*u-(Lu-Huz*Lz/Hzz))

    # Cubic density is a boundary only after restriction, not before variation.
    gam, ux = sy.symbols("gamma ux", real=True)
    chi = sy.Matrix([Q, u, 0, 0])
    dX = sy.Matrix([0, -2*u*ux, 0, 0])
    metric = sy.diag(-1, 1, 1, 1)
    T3 = 2*gam*ux*chi*chi.T+gam*(chi*dX.T+dX*chi.T)-gam*metric*(-2*u*u*ux)
    expected = sy.diag(2*gam*(Q*Q-u*u)*ux, 0, 2*gam*u*u*ux, 2*gam*u*u*ux)
    for i in range(4):
        for j in range(4):
            check("cubic_stress_%d%d" % (i, j), T3[i, j]-expected[i, j])
    check("cubic_1d_boundary", sy.diff(gam*(Q*Q*u-u**3/3), u)*ux-gam*(Q*Q-u*u)*ux)

    # Recompute Einstein trace reversal for a transverse scalar plane wave in
    # the clock rest frame. This is independent of the imported debraider.
    omega, k, qq, bb, M2 = sy.symbols("omega k qq bb M2", real=True)
    covector = sy.Matrix([omega, 0, k, 0])
    vlow = sy.Matrix([qq, bb, 0, 0])
    vup = metric*vlow
    HH = covector*covector.T
    box = sy.trace(metric*HH)
    XX = qq*qq-bb*bb
    dXX = -2*HH*vup
    stress = (2*gam*box*vlow*vlow.T
              +gam*(vlow*dXX.T+dXX*vlow.T)
              -gam*metric*(vup.T*dXX)[0])
    trace_reverse = stress-metric*sy.trace(metric*stress)/2
    feedback = sy.expand(-2*gam*(vup.T*trace_reverse*vup)[0]/M2)
    check("transverse_einstein_gradient_feedback",
          feedback.coeff(k, 2)+2*gam**2*XX**2/M2)
    check("transverse_einstein_kinetic_feedback",
          feedback.coeff(omega, 2)+2*gam**2*XX*(4*qq*qq-XX)/M2)
    check("transverse_einstein_no_mixed_feedback", feedback.coeff(k, 1).coeff(omega, 1))
    return checks


def numerical_check():
    state = json.loads(STATE.read_text())["rows"][0]
    Q, s0, tau = (state[k] for k in ("physical_Q", "clock_rate", "tau"))
    model = Model(.01, gamma=state["gamma"])
    bg = model.background(tau)
    # Independently reconstruct the exact scalar density and differentiate it.
    u, z = sy.symbols("u z", real=True)
    X = Q*Q-u*u
    Y = (u-Q*z)**2/(1-z*z)
    U, d, ell, qb, Hb = (bg[k] for k in ("U", "d", "ell", "q", "H"))
    P = -U*sy.log((U-2*d*X)/(U-2*d*qb*qb))/2+3*model.gamma*qb*Hb*(X-qb*qb)
    W = U+2*d*ell*(sy.sqrt(1+Y/ell)-1)-2*model.gamma*qb*qb*bg["qdot"]
    L = P+s0*sy.sqrt(1-z*z)*W
    grad = sy.lambdify((u,z), (sy.diff(L,u), sy.diff(L,z)), "numpy", cse=True)
    hess = sy.lambdify((u,z), sy.hessian(L,(u,z)), "numpy", cse=True)
    solved = root(lambda x: grad(*x), [.0015, -.017], jac=lambda x: hess(*x), tol=1e-11)
    if not solved.success or max(abs(np.asarray(grad(*solved.x))))>1e-12:
        raise AssertionError("Independent stationary root failed: "+solved.message)
    uu, zz = map(float, solved.x)

    def row(uu, zz):
        rr = np.sqrt(1-zz*zz)
        vv = uu-Q*zz
        qq = (Q-uu*zz)/rr
        jj = model.jets(tau, Q*Q-uu*uu, vv*vv/(rr*rr))
        ww, dd, pp = (float(jj[k]) for k in ("W", "W_Y", "P_X"))
        Huu = -2*pp+2*s0*rr*dd
        Huz = -2*s0*qq*dd
        Hzz = s0/rr*(2*qq*qq*dd-ww)
        Jx = -ww*zz/rr-2*qq*dd*vv/(rr*rr)
        J0 = ww/rr+2*qq*dd*zz*vv/(rr*rr)
        Jx_tau = -jj["W_t"]*zz/rr-2*qq*jj["W_Yt"]*vv/(rr*rr)
        J0_tau = jj["W_t"]/rr+2*qq*jj["W_Yt"]*zz*vv/(rr*rr)
        source = jj["P_t"]-jj["V_t"]+s0*rr*jj["W_t"]-s0*J0_tau
        source_identity = jj["P_t"]-jj["V_t"]+s0*zz*Jx_tau
        lu, lz = map(float, grad(uu, zz))
        HH = np.asarray(hess(uu, zz),dtype=float)
        hh = Huu-Huz**2/Hzz
        XX = Q*Q-uu*uu
        K0 = 2*pp+4*qq*qq*jj["P_XX"]
        deltaK = 2*model.gamma**2*XX*(4*qq*qq-XX)
        deltaG = -2*model.gamma**2*XX**2
        identity_error = hh*uu-(lu-Huz*lz/Hzz)
        assert abs(source-source_identity)<1e-14
        assert abs(identity_error)<1e-14
        return dict(u=uu,z=zz,q_parallel=qq,X=Q*Q-uu*uu,Y=vv*vv/(rr*rr),
                    Lu=lu,Lz=lz,transverse_raw_hessian=[[Huu,Huz],[Huz,Hzz]],
                    transverse_clock_block=Hzz,transverse_schur=hh,
                    transverse_ward_residual=identity_error,
                    longitudinal_schur=float(HH[0,0]-HH[0,1]**2/HH[1,1]),
                    clock_rest_affine_principal=dict(K0=float(K0),G0=-hh,
                        deltaK=float(deltaK),deltaG=float(deltaG),
                        corrected_K=float(K0+deltaK),corrected_G=float(-hh+deltaG),
                        corrected_c_squared=float((-hh+deltaG)/(K0+deltaK)),
                        scope="Clock rest frame, wavevector transverse to spatial chi gradient, vanishing background covariant chi Hessian, M2=1; no on-shell background claim"),
                    clock_J0=J0,clock_Jx=Jx,clock_Jx_tau=float(Jx_tau),
                    P_tau_minus_V_tau=float(jj["P_t"]-jj["V_t"]),
                    static_time_current_source=float(source),
                    static_source_identity_residual=float(source-source_identity))

    origin, stationary = row(0.,0.), row(uu,zz)
    assert abs(stationary["transverse_schur"])<1e-12
    assert abs(stationary["transverse_clock_block"])>1e-5
    assert stationary["longitudinal_schur"]<0
    return dict(source_path=str(STATE.relative_to(BASE)),source_index=0,
                Q=Q,s0=s0,tau=tau,gamma=model.gamma,
                physical_H=state.get("H"),reference_H=Hb,
                origin=origin,stationary=stationary,
                scope="One double-precision nonzero stationary root of the frozen static density. No interval root certificate, full background, dynamical stability, or Einstein constraint solve.")


def run():
    return dict(exact_checks=exact_checks(),numerical=numerical_check(),
                verdict="correct only after a stated restriction",
                conclusion="The static clock elimination has the stated quartic, but every regular O(3)-covariant nonzero stationary gradient has two zero transverse static Schur eigenvalues.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
