#!/usr/bin/env python3
"""Frozen FSP-010 all-photon-scale Dirac reconstruction control.

No QCD numerical inference. The mass integral is performed analytically
before independent radial/Feynman-parameter numerical quadrature.
"""
import json
from pathlib import Path
import sys

import mpmath as mp
import sympy as sp

BASE = Path("fine_structure_puzzle/qcd_hard_vacuum/hard_bridge")
INPUTS = json.loads((BASE / "INPUTS.json").read_text())
DEST = Path(sys.argv[1])
CHECKS = []


def check(name, value, target=0, tol=None):
    tol = mp.mpf(INPUTS["relative_tolerance"]) if tol is None else mp.mpf(tol)
    err = abs(value - target)
    ok = err <= tol * max(mp.mpf(1), abs(target))
    CHECKS.append({"name": name, "passed": bool(ok), "absolute_error": mp.nstr(err, 35)})
    if not ok:
        raise AssertionError("%s: %s versus %s" % (name, mp.nstr(value, 40), mp.nstr(target, 40)))


def serialize(value):
    if isinstance(value, dict):
        return {str(k): serialize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [serialize(v) for v in value]
    if isinstance(value, mp.mpf):
        return mp.nstr(value, 65)
    return value


def symbolic_checks():
    s, t, L, r = sp.symbols("s t L r", positive=True)
    for n in INPUTS["derivative_orders"]:
        kernel = n * s ** (n - 1) * t / (t + s) ** (n + 1)
        assert sp.simplify(sp.diff((s / (t + s)) ** n, s) - kernel) == 0
        CHECKS.append({"name": "exact kernel primitive n=%d" % n, "passed": True})
    rat = (-sp.Rational(1, 3) + r + r**2 - r**3 / 3) / (1 - r + r**2)
    assert sp.simplify(rat - (sp.Rational(2, 3) - r / 3 + (2*r - 1)/(r*r-r+1))) == 0
    CHECKS.append({"name": "exact UV density-difference rational identity", "passed": True})


def functions():
    pi2 = mp.pi**2
    a = 3 / (16*pi2)

    def weight(v):
        r = mp.exp(-2*v)
        return mp.mpf(3)/4 + r/2 - r*r/4

    def qrad(integrand, scale):
        # v=asinh(z) removes the radial logarithmic UV range. All v>0
        # are included; breakpoints resolve the photon transition scale.
        vstar = mp.asinh(mp.sqrt(scale)/2)
        pts = sorted(set([mp.mpf(0), mp.mpf(1), vstar, vstar+1, vstar+4]))
        return mp.quad(integrand, pts + [mp.inf])

    def f(s):
        return mp.quad(lambda x: -(1+x)*mp.log(x*x+(1-x)*s)-x,
                       [0, mp.mpf('0.5'), mp.mpf('0.9'), 1]) / (8*pi2)

    def fder(k, s):
        return ((-1)**k * mp.factorial(k-1)/(8*pi2)
                * mp.quad(lambda x: (1+x)*(1-x)**k/(x*x+(1-x)*s)**k,
                          [0, mp.mpf('0.5'), mp.mpf('0.9'), 1]))

    def hfp(n, s):
        return (-1)**n * s**(n-1) * fder(n, s)/mp.factorial(n-1)

    def hrad(n, s):
        return n*s**(n-1)/(2*pi2) * qrad(
            lambda v: weight(v)*(4*mp.sinh(v)**2)/(4*mp.sinh(v)**2+s)**(n+1), s)

    def irad(n, L):
        return qrad(lambda v: weight(v)*(L/(4*mp.sinh(v)**2+L))**n, L)/(2*pi2)

    def jfp(n, L):
        def integrand(x):
            c = x*x/(1-x)
            y = L/(L+c)
            return (1+x)*(mp.log1p(L/c)-sum(y**k/k for k in range(1,n))-mp.log1p(L))
        return mp.quad(integrand, [0, mp.mpf('0.5'), mp.mpf('0.9'), 1])/(8*pi2)

    return a, f, fder, hfp, hrad, irad, jfp


def run_precision(dps):
    mp.mp.dps = dps
    a, f, fder, hfp, hrad, irad, jfp = functions()
    B = mp.mpf('2.5')/(16*mp.pi**2)
    fzero = 4/(16*mp.pi**2)
    check("zero photon MSbar value dps=%d" % dps, f(0), fzero)
    derivatives = []
    reconstructions = []
    for n in INPUTS["derivative_orders"]:
        for ss in INPUTS["photon_s"]:
            s = mp.mpf(ss)
            fp, radial = hfp(n, s), hrad(n, s)
            check("independent derivative n=%d s=%s dps=%d" % (n, ss, dps), radial, fp)
            derivatives.append({"n": n, "s": s, "feynman_parameter": fp, "radial": radial})
        H = sum(mp.mpf(1)/k for k in range(1,n))
        for ls in INPUTS["upper_mass_squared_L"]:
            L = mp.mpf(ls)
            raw_radial = irad(n,L)
            jj = raw_radial-a*mp.log1p(L)
            independent_j = jfp(n,L)
            check("all momentum mass-integral n=%d L=%s dps=%d" % (n,ls,dps), jj, independent_j)
            endpoint = f(L) + sum((-L)**k/mp.factorial(k)*fder(k,L) for k in range(1,n))
            exact_reconstruction = raw_radial+endpoint
            check("finite endpoint reconstruction n=%d L=%s dps=%d" % (n,ls,dps), exact_reconstruction, fzero)
            reconstructions.append({"n": n, "L": L, "subtracted_integral": jj,
                                    "independent_subtracted_integral": independent_j,
                                    "matched_finite_endpoint": endpoint,
                                    "exact_reconstructed_fzero": exact_reconstruction,
                                    "asymptotic_boundary_reconstruction": B+a*H+jj,
                                    "asymptotic_boundary_error": B+a*H+jj-fzero})

    # Independent smooth rational all-momentum density-difference check.
    K = a*mp.quad(lambda r: (-mp.mpf(1)/3+r+r*r-r**3/3)/(1-r+r*r), [0,1])
    check("infinite all-momentum density difference dps=%d" % dps, K, a/2)
    check("n1 infinite matched reconstruction dps=%d" % dps, B+K, fzero)
    for n in INPUTS["derivative_orders"]:
        H = sum(mp.mpf(1)/k for k in range(1,n))
        # This logarithmic x-integral is obtained by exact all-s integration
        # of the Feynman-parameter derivative, not from f(0).
        allscale = mp.quad(lambda x: (1+x)*(mp.log((1-x)/(x*x))-H),
                          [0, mp.mpf('0.5'), mp.mpf('0.9'),1])/(8*mp.pi**2)
        check("infinite all-scale integral n=%d dps=%d" % (n,dps), allscale, a*(mp.mpf('0.5')-H))
        check("infinite matched reconstruction n=%d dps=%d" % (n,dps), B+a*H+allscale, fzero)
    boundaries = [{"s":mp.mpf(ss), "extracted_B":f(mp.mpf(ss))+a*mp.log(mp.mpf(ss)),
                   "error":f(mp.mpf(ss))+a*mp.log(mp.mpf(ss))-B}
                  for ss in INPUTS["upper_mass_squared_L"]]
    return {"dps":dps,"a":a,"B":B,"fzero":fzero,"K":K,
            "J1_infinity":a/2,"J3_infinity":-a,
            "missing_B_error_if_B_omitted":-B,
            "missing_harmonic_error_n3":-mp.mpf('1.5')*a,
            "derivatives":derivatives,"reconstructions":reconstructions,"boundaries":boundaries}


symbolic_checks()
results = [run_precision(dps) for dps in INPUTS["precision_digits"]]
lo, hi = results
for key in ["a","B","fzero","K"]:
    check("cross precision %s" % key,lo[key],hi[key],INPUTS["cross_precision_tolerance"])
for row_lo,row_hi in zip(lo["reconstructions"],hi["reconstructions"]):
    check("cross precision reconstruction n=%d L=%s" % (row_hi["n"],row_hi["L"]),
          row_lo["subtracted_integral"],row_hi["subtracted_integral"],INPUTS["cross_precision_tolerance"])
out={"assertion_tested":"All-scale photon-mass kernel normalization and matched finite/infinite endpoint reconstruction in the elementary Dirac control",
     "claim_scope":"Finite numerical control plus separately proved conditional integral theorem; no numerical QCD claim",
     "results":results,"checks":CHECKS,"passed_checks":sum(c["passed"] for c in CHECKS)}
DEST.write_text(json.dumps(serialize(out),indent=2)+"\n")
print(json.dumps({"passed_checks":out["passed_checks"],"precisions":INPUTS["precision_digits"],
                  "a":mp.nstr(hi["a"],18),"B":mp.nstr(hi["B"],18),"fzero":mp.nstr(hi["fzero"],18)}))
