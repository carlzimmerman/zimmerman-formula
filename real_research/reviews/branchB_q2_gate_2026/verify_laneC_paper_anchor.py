#!/usr/bin/env python3
"""
PUBLISHED-VALUE PIN: Desmond, Hees & Famaey 2024 (arXiv:2401.04796v2), Fig. 1 caption gives
q(1)=0.094, q(1.5)=0.159, q(2)=0.221 for the RAR IF nu_RAR(y) = (1-exp(-sqrt(y)))^-1,
computed from their eq (12):
   q = (3/2) Int_0^inf dv Int_{-1}^1 dxi (nu-1) [eN(3xi-5xi^3) + v^2(1-3xi^2)]
with nu at sqrt(eN^2+v^4+2 eN v^2 xi), eN nu(eN) = etilde.  NO sqrt-denominator.
Test the lane/committed transcription (WITH /sqrt(D)) and the faithful form (WITHOUT) against
these published values. Also rerun the committed baseline's own validation function.
"""
import numpy as np
from scipy import integrate
from scipy.optimize import brentq

def nu_rar(y): return 1.0/(1.0 - np.exp(-np.sqrt(y)))

def q_generic(etilde, nu, with_sqrtD, vmax=200.0):
    eN = brentq(lambda x: x*nu(x) - etilde, 1e-9, 1e4)
    def ig(xi, v):
        D = eN*eN + v**4 + 2*eN*v*v*xi
        if D <= 0: return 0.0
        w = (nu(np.sqrt(D)) - 1.0)*(eN*(3*xi - 5*xi**3) + v*v*(1 - 3*xi*xi))
        return w/np.sqrt(D) if with_sqrtD else w
    val,_ = integrate.dblquad(ig, 0.0, vmax, lambda v: -1.0, lambda v: 1.0,
                              epsabs=1e-11, epsrel=1e-9)
    return 1.5*val, eN

print("nu_RAR, published q anchors (Desmond+2024 Fig 1 caption):")
print(f"  {'etilde':>7}{'published':>11}{'no-sqrtD |q|':>14}{'with-sqrtD |q|':>15}")
pub = {1.0: 0.094, 1.5: 0.159, 2.0: 0.221}
for et, qp in pub.items():
    qa,_ = q_generic(et, nu_rar, with_sqrtD=False)
    qb,_ = q_generic(et, nu_rar, with_sqrtD=True)
    print(f"  {et:>7.1f}{qp:>11.3f}{abs(qa):>14.4f}{abs(qb):>15.4f}")

# committed baseline's own validation (imports its function directly)
import sys
sys.path.insert(0, "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/reviews")
import importlib.util
spec = importlib.util.spec_from_file_location(
    "aest_full", "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/reviews/aest_cassini_quadrupole_full.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print("\ncommitted baseline aest_cassini_quadrupole_full.validate_q_against_simple():")
for et, q, Q2 in mod.validate_q_against_simple():
    print(f"  etilde={et:.3f}: q={q:+.4f}  Q2={Q2:+.3e}  (lane cross-check printed the same? compare)")
print("\nEXIT 0")
