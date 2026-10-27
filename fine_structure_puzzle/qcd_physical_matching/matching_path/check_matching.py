#!/usr/bin/env python3
"""Small exact matching audit plus an independent Ewald shape sum.

No hadron inputs, measured charge, or cosmological data are used.
"""
import argparse
import json
import math
import platform
import sys
from itertools import product
from pathlib import Path

import mpmath as mp
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    checks = []

    def exact(name, lhs, rhs=0):
        residual = s.factor(s.together(lhs - rhs))
        assert residual == 0, (name, residual)
        checks.append({"name": name, "kind": "exact", "residual": str(residual)})

    # These symbolic quantities are derivatives, not assumed evaluated QCD data.
    ma, ml, fa, fl, alpha, c1, charge, L = s.symbols(
        "M_alpha M_ell f_alpha f_ell alpha c1 Q L", nonzero=True
    )
    k = c1 * charge**2 / 2
    dl = -k * alpha / (L * ml)
    exact("finite-volume proton constraint at first order", ml * dl + k * alpha / L)
    induced = s.expand(fl * dl)
    exact("retuned flat baseline coefficient", induced, -k * alpha * fl / (L * ml))
    fintr = s.symbols("Delta_intrinsic")
    fixed_reference = fintr + fl * dl
    same_theory = fixed_reference - fl * dl
    exact("same-theory subtraction cancels retuned flat baseline", same_theory, fintr)
    exact("zero charge removes retuning term", induced.subs(charge, 0))

    b, bs, cp, cs, scale = s.symbols("B sum_x_dB C_p sum_x_dC Lambda", nonzero=True)
    f_l = scale**4 * (4 * b - bs)
    m_l = scale * (cp - cs)
    exact("alpha Lambda cubed over L coefficient", induced.subs({fl: f_l, ml: m_l}),
          -k * alpha * scale**3 * (4*b-bs) / (L*(cp-cs)))
    v_l = s.symbols("v_ell")
    exact("independent cosmological retuning cancels baseline", (fl+v_l).subs(v_l, -fl))
    exact("cosmological tangent shifts apparent coefficient", -k*alpha*(fl+v_l)/(L*ml)-induced,
          -k*alpha*v_l/(L*ml))

    # Two independent quark running-mass conversions, with strong/charge
    # matching already absorbed into derivatives of S and M in these coordinates.
    p0, p1, p2, u1a, u2a, u1l, u2l = s.symbols("p0 p1 p2 u1a u2a u1l u2l")
    ma_hat = ma + p1*u1a + p2*u2a
    ml_hat = p0 + p1*u1l + p2*u2l
    ell_dot = -ma_hat / ml_hat
    z1_dot = u1a + u1l*ell_dot
    z2_dot = u2a + u2l*ell_dot
    exact("full running-mass retuning preserves proton", ma+p0*ell_dot+p1*z1_dot+p2*z2_dot)
    exact("first invariant quark mass is held", z1_dot-u1a-u1l*ell_dot)
    exact("second invariant quark mass is held", z2_dot-u2a-u2l*ell_dot)
    I, O0, O1, O2 = s.symbols("I O0 O1 O2")
    K_running = I + ell_dot*O0 + z1_dot*O1 + z2_dot*O2
    I_hat = I + u1a*O1 + u2a*O2
    O_ell = O0 + u1l*O1 + u2l*O2
    exact("operator insertion equals matched-coordinate expression", K_running,
          I_hat - ma_hat/ml_hat*O_ell)

    # RG operator normalization and Feynman-Hellmann checks.
    beta, g, G2, gamma, S_mass, theta, M, sigma = s.symbols(
        "beta g G2 gamma S_mass Theta M sigma", nonzero=True
    )
    gauge_action = G2/(4*g*g)
    exact("RG strong-scale gauge derivative", -beta*s.diff(gauge_action, g), beta*G2/(2*g**3))
    exact("trace minus canonical mass has anomalous mass term",
          beta*G2/(2*g)+(1+gamma)*S_mass-S_mass,
          beta*G2/(2*g)+gamma*S_mass)
    exact("connected proton trace minus sigma normalization", (2*M*M-2*M*sigma)/(2*M), M-sigma)
    aa, al = s.symbols("A_alpha A_ell")
    exact("fixed proton ratio response", (aa-ma/ml*al)/M**3,
          aa/M**3 - ma*al/(ml*M**3))
    pa, P, ha, Qmass = s.symbols("p_alpha P h_alpha Q_mass")
    exact("prior constrained logarithmic formula",
          ha-3*pa+(Qmass-3*P)*pa/(1-P), ha-(3-Qmass)*pa/(1-P))

    # A formal local counterterm cannot create a fixed-theory linear H term.
    H, b0, b2, b4 = s.symbols("H b0 b2 b4")
    def D(expr):
        return H*s.diff(expr, H)
    def Pdiff(expr):
        return D(D(D(expr))-6*D(expr)+8*expr)
    exact("sphere projection annihilates local vacuum/curvature terms", Pdiff(b0+b2*H**2+b4*H**4))
    exact("sphere projection retains path-induced baseline linear term", Pdiff(H), 3*H)
    exact("sphere metric operation on fixed-coupling linear density", H-D(H)/4, s.Rational(3,4)*H)

    # Ewald identity derived in RAW_DERIVATION.md; eta=pi.
    # erfc(x) <= exp(-x^2)/(sqrt(pi)*x) bounds the omitted real-space sum.
    def shape(dps, N):
        with mp.workdps(dps):
            total = mp.mpf(-3)
            for x, y, z in product(range(-N, N+1), repeat=3):
                n2 = x*x+y*y+z*z
                if n2:
                    r = mp.sqrt(n2)
                    total += mp.exp(-mp.pi*n2)/(mp.pi*n2) + mp.erfc(mp.sqrt(mp.pi)*r)/r
            a = N+1
            theta_bound = 1+2*mp.exp(-mp.pi)/(1-mp.exp(-3*mp.pi))
            trunc_bound = (12*theta_bound**2/(mp.pi*a*a) * mp.exp(-mp.pi*a*a)
                           /(1-mp.exp(-mp.pi*(2*a+1))))
            return total, trunc_bound, mp.nstr(total, dps-5), mp.nstr(trunc_bound, 8)
    shape_rows = []
    vals = []
    for dps, N in [(40, 3), (60, 4)]:
        val, bound, valstr, boundstr = shape(dps, N)
        vals.append((val,bound))
        shape_rows.append({"decimal_precision": dps, "cube_N": N, "c1": valstr,
                           "analytic_truncation_bound": boundstr,
                           "roundoff_certified": False})
    with mp.workdps(60):
        # The tolerance includes a deliberately loose allowance for finite
        # arithmetic; only the exponential tail bound is analytic.
        assert abs(vals[0][0]-vals[1][0]) < vals[0][1]+mp.mpf("1e-35")
        assert abs(vals[1][0]-mp.mpf("-2.83729")) < mp.mpf("0.00001")
    checks.extend([
        {"name":"Ewald cutoff and precision comparison", "kind":"numerical", "passed":True},
        {"name":"primary-source c1 rounded benchmark", "kind":"numerical", "passed":True},
    ])
    result = {
        "assertion_tested":"First-order matching algebra, operator retuning, subtraction cancellation, RG and sphere normalization; Ewald c1 on two declared finite cubes.",
        "software":{"python":platform.python_version(),"sympy":s.__version__,"mpmath":mp.__version__},
        "checks": checks, "check_count":len(checks), "shape_constant":shape_rows,
        "induced_coefficient":"-alpha Q^2 c1/2 * f_ell/M_ell",
        "interpretation":"Exact cancellation of the retuned flat-baseline contribution under same-theory flat subtraction. No physical QCD vacuum matrix element evaluated.",
    }
    Path(args.output).write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"check_count":len(checks),"shape_constant":shape_rows}))


if __name__ == "__main__":
    main()
