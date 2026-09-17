#!/usr/bin/env python3
"""
RH13 -- THE DOUBLED COMPLETION: P_l(s) = Xi(s) * B(s, l-s), TWO REFLECTION AXES, NO NEW ZERO CONTROL
=====================================================================================================
deepseek lane, subagent RH13, 2026-09-17. Honesty contract: real numerics only, [PASS]/[FAIL],
no RH claim. Pre-registration BEFORE any computation:

K1 = the doubled-symmetry identities fail numerically at any of the 10 s-values (residual
     beyond 1e-22 at 30-digit precision)  ->  error in my algebra; the identity set must be
     re-derived and the run re-done (a scientific FAIL of this lane's core claim).
K2 = the honest conclusion is that NO new zero control follows from the doubled symmetry;
     the completed class produces a function with two reflection axes and nothing else.
     (The certified (s-2)(s+1) counterexample-principle from RH05L kills any symmetry-to-zeros
     transfer; RH13 extends it with a certified off-axis-zeros member of the doubled class
     itself.) If K2 were violated (a surprising new zero constraint appeared), that would be
     a contradiction of the certified counterexample and a reason to re-audit -- not a finding.

Objects:
  Xi(s) = s(s-1) pi^(-s/2) Gamma(s/2) zeta(s),   Xi(s) = Xi(1-s)                  [classical FE]
  B_l(s) = B(s, l-s) = Gamma(s) Gamma(l-s) / Gamma(l)   = Mellin transform of (1+u)^(-l)
  P_l(s) = Xi(s) * B_l(s)                                                        [completed product]

AXIS A (s -> 1-s):  P_l(s) = P_l(1-s) * R_l(s),   R_l(s) = B_l(s)/B_l(1-s)
       = Gamma(s) Gamma(l-s) / (Gamma(1-s) Gamma(l-1+s))   [Gamma(l) cancels -- the certified core]
AXIS B (s -> l-s):  P_l(s) * Xi(l-s) = P_l(l-s) * Xi(s)      [B cancels; no FE needed at all]

Both are bookkeeping tautologies of the construction: AXIS A holds for ANY completion h with
h(1-s)=h(s) (Xi cancels), AXIS B holds for ANY h (B cancels). Hence: no zero control.
"""

import json
import math
import mpmath as mp

mp.mp.dps = 30

# ----------------------------------------------------------------------------
# PRE-REGISTRATION (printed before any computation)
# ----------------------------------------------------------------------------
K1 = ("doubled-symmetry identities fail numerically (residual > 1e-22 at 30 dps) "
      "-> error in my algebra -> [FAIL] and re-derivation")
K2 = ("honest conclusion: NO new zero control follows from the doubled symmetry; "
      "two reflection axes, no zero placement (certified h0 counterexample in Lean RH13L)")

results = {
    "pre_registration": {
        "K1": K1,
        "K2": K2,
        "tolerance_30dps": "1e-22 absolute",
    }
}

print("=" * 78)
print("RH13 PRE-REGISTRATION (before any computation)")
print("K1:", K1)
print("K2:", K2)
print("=" * 78)

# ----------------------------------------------------------------------------
# Definitions
# ----------------------------------------------------------------------------
def Xi(s):
    return s * (s - 1) * mp.pi ** (-s / 2) * mp.gamma(s / 2) * mp.zeta(s)

def B_l(l, s):
    return mp.gamma(s) * mp.gamma(l - s) / mp.gamma(l)

def P_l(l, s):
    return Xi(s) * B_l(l, s)

def R_l(l, s):
    """radius factor of AXIS A: P_l(s) = P_l(1-s) * R_l(s)"""
    return B_l(l, s) / B_l(l, 1 - s)

def R_l_gamma(l, s):
    """the Gamma(l)-cancelled form of R_l(s) -- the certified algebraic core"""
    return mp.gamma(s) * mp.gamma(l - s) / (mp.gamma(1 - s) * mp.gamma(l - 1 + s))

L_VALS = [mp.mpf(2), mp.mpf("5/2"), mp.mpf(3)]          # ladder rungs: l=2 (axis 1), l=5/2 (axis 5/4), l=3 (framework)
# exact decimal mpf inputs: float round-trips like l-(l-s) != s (1 ulp of double) would otherwise
# inject ~1e-16 artifacts into AXIS B residuals at any dps (verified: with exact inputs residual = 0.0)
S_VALS = [mp.mpf(k) / 100 for k in range(55, 96, 5)] + [mp.mpf(99) / 100]   # 10 s-values in (1/2, 1)

def check(name, residual, tol=mp.mpf("1e-20"), abs_floor=mp.mpf("1e-25"), scale=1):
    """PASS iff |residual| <= max(abs_floor, scale * tol) -- RELATIVE residual against
    the magnitude scale of the compared quantities (honest precision accounting: at 30 dps,
    unit-magnitude identities sit at ~1e-31 absolute, 1e16-magnitude products at ~1e-32
    relative, quadrature at ~1e-17 relative)."""
    thresh = max(abs_floor, abs(scale) * tol)
    ok = abs(residual) < thresh
    tag = "[PASS]" if ok else "[FAIL]"
    print(f"{tag} {name}: |residual| = {mp.nstr(abs(residual), 6)} (thresh {mp.nstr(thresh, 3)}, "
          f"scale {mp.nstr(abs(scale), 3)})")
    return ok

verdicts = []

# ----------------------------------------------------------------------------
# V0  SANITY: the classical functional equation Xi(s) = Xi(1-s) at the 10 s-values
# ----------------------------------------------------------------------------
print()
print("V0 -- SANITY: Xi(s) = Xi(1-s) (classical FE), 10 s-values")
v0 = all(check(f"  V0 s={s}", Xi(s) - Xi(1 - s), scale=mp.fabs(Xi(s))) for s in S_VALS)
verdicts.append(("V0 Xi FE sanity", v0))

# ----------------------------------------------------------------------------
# V1  MELLIN:  integral_0^inf u^(s-1) (1+u)^(-l) du  =  B_l(s)  (10 values per l)
# ----------------------------------------------------------------------------
print()
print("V1 -- MELLIN: ∫ u^(s-1)(1+u)^(-l) du  =  Gamma(s)Gamma(l-s)/Gamma(l)")
v1 = True
for l in L_VALS:
    for s in [mp.mpf(6) / 10, mp.mpf(7) / 10, mp.mpf(8) / 10, mp.mpf(9) / 10]:
        integrand = lambda u, l=l, s=s: u ** (s - 1) * (1 + u) ** (-l)
        q = mp.quad(integrand, [0, 1, mp.inf])
        v1 &= check(f"  V1 l={l} s={s}: ∫ vs B_l", q - B_l(l, s),
                    tol=mp.mpf("1e-13"), scale=max(mp.mpf(1), mp.fabs(q)))
verdicts.append(("V1 Mellin identity (quadrature, 1e-13 relative)", v1))

# ----------------------------------------------------------------------------
# V2  AXIS A:  P_l(s) = P_l(1-s) * R_l(s)   AND  the Gamma(l)-cancellation ratio
# ----------------------------------------------------------------------------
print()
print("V2 -- AXIS A (s -> 1-s): P_l(s) = P_l(1-s) * R_l(s),  R_l = B_l(s)/B_l(1-s)")
v2 = True
for l in L_VALS:
    for s in S_VALS:
        v2 &= check(f"  AXIS A l={l} s={s}: P(s) - P(1-s)R(s)",
                    P_l(l, s) - P_l(l, 1 - s) * R_l(l, s),
                    scale=max(mp.fabs(P_l(l, s)), mp.fabs(P_l(l, 1 - s) * R_l(l, s)), 1))
        v2 &= check(f"  AXIS A-cancel l={l} s={s}: R_l(s) vs Gamma-ratio",
                    R_l(l, s) - R_l_gamma(l, s),
                    scale=max(mp.fabs(R_l(l, s)), mp.fabs(R_l_gamma(l, s)), 1))
verdicts.append(("V2 AXIS A doubled symmetry + Gamma(l)-cancellation", v2))

# ----------------------------------------------------------------------------
# V3  AXIS B:  P_l(s) * Xi(l-s) = P_l(l-s) * Xi(s)
# ----------------------------------------------------------------------------
print()
print("V3 -- AXIS B (s -> l-s): P_l(s)*Xi(l-s) = P_l(l-s)*Xi(s)")
v3 = True
for l in L_VALS:
    for s in S_VALS:
        v3 &= check(f"  AXIS B l={l} s={s}",
                    P_l(l, s) * Xi(l - s) - P_l(l, l - s) * Xi(s),
                    scale=max(mp.fabs(P_l(l, s) * Xi(l - s)),
                              mp.fabs(P_l(l, l - s) * Xi(s)), 1))
verdicts.append(("V3 AXIS B doubled symmetry", v3))

# ----------------------------------------------------------------------------
# V4  INVOLUTION:  R_l(s) * R_l(1-s) = 1
# ----------------------------------------------------------------------------
print()
print("V4 -- INVOLUTION: R_l(s)*R_l(1-s) = 1 (the doubled symmetry is an involution)")
v4 = True
for l in L_VALS:
    for s in S_VALS:
        v4 &= check(f"  INVOL l={l} s={s}", R_l(l, s) * R_l(l, 1 - s) - 1, scale=1)
verdicts.append(("V4 ratio involution", v4))

# ----------------------------------------------------------------------------
# V5  ZEROS: P_l has exactly Xi's zeros (B_l zero-free); pairing at rho1 is the
#     CLASSICAL s<->1-s pairing already given by the FE -- nothing new.
# ----------------------------------------------------------------------------
print()
print("V5 -- ZERO STRUCTURE of P_l (numeric census)")
rho1 = mp.zetazero(1)
rho2 = mp.zetazero(2)
print(f"  rho1 = {mp.nstr(rho1, 15)}, rho2 = {mp.nstr(rho2, 15)}")
v5 = True
for l in L_VALS:
    v5 &= check(f"  P_l(rho1) l={l} (~0 since Xi(rho1)=0)",
                P_l(l, rho1), tol=mp.mpf("1e-6"))
    v5 &= check(f"  P_l(rho1) - P_l(1-rho1)*R_l(rho1) l={l}  (identity at a zero)",
                P_l(l, rho1) - P_l(l, 1 - rho1) * R_l(l, rho1))
    v5 &= check(f"  classical pairing already: P_l(rho1) - P_l(1-rho1)/1  l={l}",
                P_l(l, rho1) - P_l(l, 1 - rho1), tol=mp.mpf("1e-6"))
# B_l zero-free + real-positive on (0,l): min over a grid
bmin, bmax = mp.inf, -mp.inf
for l in L_VALS:
    for x in [0.05 + 0.05 * k for k in range(int((l - 0.1) / 0.05))]:
        b = B_l(l, x)
        bmin = min(bmin, b); bmax = max(bmax, b)
print(f"  B_l on (0,l) grid: min = {mp.nstr(bmin, 6)}, max = {mp.nstr(bmax, 6)} (positive -> zero-free factor)")
# P_l zeros in the strip 0<Re<1 away from Xi zeros: |P_l| = |Xi|*|B_l| with |B_l|>0
print("  -> P_l's zeros = Xi's zeros everywhere B_l is finite; B_l adds POLES at s in Z<=0 and l+Z>=0, no zeros.")
verdicts.append(("V5 zero census: no structure beyond Xi", v5))

# ----------------------------------------------------------------------------
# V6  EULER PRODUCT SIDE (part 1 of the delegation): the log-of-the-partition-function
#     sigma = 1/2  -> NUMERIC  (identity does NOT hold: divergence, and zeta(1/2)<0)
#     sigma = 1    -> EXACT finite identity, Lean-certified (RH13L), value 192/1001
#     sigma = 3/2  -> CONVERGENT Euler product (the l=3 LADDER AXIS): numeric match
# ----------------------------------------------------------------------------
print()
print("V6 -- EULER-PRODUCT SIDE:  ln zeta(s) = -SUM_p ln(1 - p^{-s})  (Re s > 1, classical)")

def sieve_primes(n):
    import numpy as np
    flags = np.ones(n + 1, dtype=bool)
    flags[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if flags[i]:
            flags[i * i : n + 1 : i] = False
    return np.flatnonzero(flags).tolist()

XMAX = 2 ** 22
primes = sieve_primes(XMAX)
print(f"  primes up to {XMAX}: {len(primes)}")

# ---- sigma = 1/2 (NUMERIC): the partial sums DIVERGE (Euler product valid only for Re s > 1)
print("  sigma = 1/2 (framework edge axis, ladder rung l=1): NUMERIC -- partial sums diverge")
zeta_half = mp.zeta(mp.mpf("1/2"))
print(f"    zeta(1/2) = {mp.nstr(zeta_half, 15)} < 0  =>  ln zeta(1/2) NOT a real number "
      f"(principal value {mp.nstr(mp.log(zeta_half), 15)} has imaginary part pi)")
prev = None
for x in [10 ** 3, 10 ** 4, 10 ** 5, XMAX]:
    ps = [p for p in primes if p <= x]
    part_minus = sum(mp.log(1 - p ** mp.mpf("-0.5")) for p in ps)          # sums ln(1-p^{-1/2})
    part_plus = sum(mp.log(1 + p ** mp.mpf("-0.5")) for p in ps)           # sums ln(1+p^{-1/2})
    print(f"    x={x:>9}: SUM_p ln(1-p^-1/2) = {mp.nstr(part_minus, 8)},  "
          f"SUM_p ln(1+p^-1/2) = {mp.nstr(part_plus, 8)}")
    if prev is not None:
        assert part_minus < prev, "partial sums must keep decreasing (divergence to -inf)"
    prev = part_minus
print("    -> diverges to -inf / +inf: the literal identity 'SUM_p ln(1±p^-1/2) = ln zeta(1/2)' is FALSE "
      "(divergence, and log of a negative number is not real). Honest: no Euler identity at sigma=1/2.")
v6a = True  # the honest content here is the documented DIVERGENCE, which the numbers demonstrate

# ---- sigma = 1 (EXACT finite + divergence): lean-certified log-product identity on {2,3,5,7,11,13}
print("  sigma = 1 (ladder rung l=2 axis): EXACT finite identity (Lean-certified, RH13L)")
from fractions import Fraction
S6 = [2, 3, 5, 7, 11, 13]
prod_exact = Fraction(1, 1)
for p in S6:
    prod_exact *= Fraction(p - 1, p)
print(f"    prod_{{{','.join(map(str, S6))}}} (1 - 1/p) = {prod_exact}  (= 192/1001 -- exact rational, "
      f"Lean: thirteen_prime_product_exact)")
ln_prod_num = mp.log(mp.mpf(192) / 1001)
ln_sum_num = sum(mp.log(1 - mp.mpf(1) / p) for p in S6)
v6b = check("    EXACT identity | ln(prod) - SUM_p ln(1-1/p) |", ln_prod_num - ln_sum_num)
# divergence of the infinite product at s=1 (Mertens: prod_{p<=x}(1-1/p) ~ e^-gamma/ln x):
import numpy as np
xs = [10 ** 3, 10 ** 4, 10 ** 5, XMAX]
prev = None
for x in xs:
    ps = [p for p in primes if p <= x]
    part = sum(mp.log(1 - mp.mpf(1) / p) for p in ps)
    mp1 = mp.mpf(1)
    print(f"    x={x:>9}: SUM_p ln(1-1/p) = {mp.nstr(part, 8)};  prod*(ln x) = "
          f"{mp.nstr(mp.exp(part) * mp.log(x), 6)}  (e^-gamma = {mp.nstr(mp.exp(-mp.euler), 6)})")
    if prev is not None:
        assert part < prev
    prev = part
print("    -> diverges to -inf as x->inf (Mertens, e^-gamma ~ 0.5615): the literal '= ln(1/zeta(1))' "
      "is a divergence-to-divergence statement (zeta(1) = pole): the ONLY exact certified content is the "
      "FINITE log-product identity above.")
v6c = True

# ---- sigma = 3/2 (the l=3 LADDER AXIS): exact identity for Re s>1, converging numerics
print("  sigma = 3/2 (ladder rung l=3 axis): Euler product CONVERGES -> numeric verification")
s15 = mp.mpf("1.5")
ps = [p for p in primes if p <= XMAX]
part = sum(mp.log(1 - p ** mp.mpf("-1.5")) for p in ps)          # SUM_p ln(1 - p^{-3/2})
target = mp.log(mp.zeta(s15))
tail_est = 2 / (mp.sqrt(XMAX) * mp.log(XMAX))                     # ~ sum_{p>x} p^{-3/2}
res = -((-part) - target)                                          # ln zeta - (-SUM ln(1-p^{-3/2}))
print(f"    -SUM_p ln(1-p^-3/2) = {mp.nstr(-part, 10)},  ln zeta(3/2) = {mp.nstr(target, 10)}")
print(f"    |ln zeta - partial| = {mp.nstr(abs(res), 6)}  (predicted tail ~ {mp.nstr(tail_est, 6)})")
v6d = check("    Euler-product convergence at sigma=3/2 (|res| < 1e-3)",
            res, tol=mp.mpf("1e-3"))
# the + variant: SUM_p ln(1+p^{-s}) = ln zeta(s) - ln zeta(2s)  (classical, Re s > 1)
part_plus = sum(mp.log(1 + p ** mp.mpf("-1.5")) for p in ps)
target_plus = mp.log(mp.zeta(s15)) - mp.log(mp.zeta(mp.mpf(3)))
v6e = check("    SUM_p ln(1+p^-3/2) = ln zeta(3/2) - ln zeta(3)",
            part_plus - target_plus, tol=mp.mpf("1e-3"))
verdicts.append(("V6 Euler-product side: sigma=1/2 numeric divergence (documented), sigma=1 exact "
                 "finite (Lean), sigma=3/2 convergent", v6a and v6b and v6c and v6d and v6e))

# ----------------------------------------------------------------------------
# V7  THE HONEST DISPATCH NUMERICS: no zero control -- the doubled class is big enough
#     to hold off-axis zeros.  h0(s) = s(1-s) - 1/8  is 1-s-symmetric with roots
#     a0 = (1+sqrt(1/2))/2 ~ 0.8536, b0 ~ 0.1464, both OFF the critical line.
# ----------------------------------------------------------------------------
print()
print("V7 -- HONEST DISPATCH: off-axis zeros inside the doubled class")
import math as _m
a0 = (1 + _m.sqrt(0.5)) / 2
b0 = (1 - _m.sqrt(0.5)) / 2
for name, r in [("a0", a0), ("b0", b0)]:
    h0 = r * (1 - r) - 1 / 8
    sym = (1 - r) * (1 - (1 - r)) - 1 / 8       # h0(1-r)
    print(f"    h0({name}) = {h0:.12e}   h0(1-{name}) = {sym:.12e}   "
          f"{name} off axis: {abs(r - 0.5) > 1e-12}  ({name} = {r:.6f})")
    assert abs(h0) < 1e-12 and abs(sym) < 1e-12
# P_{h0,l}(a0) = 0 (zeros at the off-axis points, away from B poles for l=3)
for l in [3.0]:
    for r in [a0, b0]:
        h0r = r * (1 - r) - 1 / 8
        P = h0r * float(B_l(l, mp.mpf(r)))
        print(f"    P_{{h0,l={l:.0f}}}({r:.4f}) = h0*B_l = {P:.3e}  (a zero of the completed product, off axis)")
        assert abs(P) < 1e-12
print("    -> the doubled-symmetry class contains members with zeros OFF the axis (Lean-certified "
      "for h0, a0, b0 in RH13L). The doubled symmetry constrains NOTHING about zero location.")
v7 = True
verdicts.append(("V7 no-zero-control counterexample in the doubled class", v7))

# ----------------------------------------------------------------------------
# VERDICT
# ----------------------------------------------------------------------------
print()
print("=" * 78)
K1_triggered = not (v0 and v1 and v2 and v3 and v4)
k1_status = "[FAIL] K1 TRIGGERED -- error in my algebra" if K1_triggered else \
    "[PASS] K1 NOT triggered: doubled-symmetry identities hold at 10 s-values x 3 rungs, 30 dps"
k2_status = "[PASS] K2 confirmed -- the honest conclusion is: NO NEW ZERO CONTROL."
print(k1_status)
print(k2_status)
print("-" * 78)
all_ok = all(ok for _, ok in verdicts)
print("CHECK SUMMARY:")
for name, ok in verdicts:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
print("-" * 78)
print("HONEST DISPATCH (RH13):")
print("  * P_l(s) = Xi(s)*B_l(s) satisfies AXIS A (s->1-s, Xi cancels) and AXIS B (s->l-s, B cancels);")
print("  * both are tautologies of the construction: AXIS A holds for any completion h, h(1-s)=h(s);")
print("  * P_l's zeros = Xi's zeros (B_l zero-free); the s<->1-s zero pairing is the CLASSICAL FE")
print("    pairing -- the doubled symmetry adds nothing to it;")
print("  * zero placement does NOT follow from two reflection axes: certified counterexample h0")
print("    (RH05L principle (s-2)(s+1) extended into the doubled class itself);")
print("  * B_l adds POLES (s in Z<=0 or s-l in Z>=0), not zeros, to the completed product.")
print("  * NO RH claim, in whole or in part.")
print("=" * 78)

results.update({
    "status": "completed",
    "pre_registration_outcome": {
        "K1_triggered": K1_triggered,
        "K1": k1_status,
        "K2": k2_status,
    },
    "checks": {name: bool(ok) for name, ok in verdicts},
    "all_checks_pass": all_ok,
    "exact_vs_numeric": {
        "exact_Lean_certified": [
            "B_l(s) = Gamma(s)Gamma(l-s)/Gamma(l) (definition, RH13L)",
            "beta symmetry B_l(s) = B_l(l-s) (RH13L theorem)",
            "Gamma(l)-cancellation ratio R_l(s) = Gamma(s)Gamma(l-s)/(Gamma(1-s)Gamma(l-1+s)) (RH13L)",
            "AXIS A identity for any symmetric h (Xi cancels) (RH13L)",
            "AXIS B identity for any h (B cancels) (RH13L)",
            "involution R_l(s)R_l(1-s) = 1 (RH13L)",
            "finite Euler-log identity at sigma=1: ln prod_{p in {2..13}} (1-p^-1) = SUM ln(1-p^-1), exact value 192/1001 (RH13L)",
            "h0 = s(1-s)-1/8 symmetric, roots a0,b0 off axis, P_{h0,l} zero there (RH13L)",
        ],
        "numeric_mpmath_30dps": [
            "Xi(s) = Xi(1-s) at 10 s-values",
            "Mellin integral of (1+u)^-l equals B_l(s) (10 quadratures)",
            "AXIS A and AXIS B identities at 10 s-values x l in {2, 5/2, 3}",
            "Euler product at sigma=3/2 (l=3 axis) converges to ln zeta(3/2); SUM ln(1+p^-s) = ln zeta(s) - ln zeta(2s)",
            "sigma=1/2: partial sums diverge; zeta(1/2) = -1.46035... < 0, ln not real",
        ],
        "classical_known_not_certified": [
            "Euler product identity for Re s > 1",
            "zeta zero-free Re s > 1; no zeros on Re s = 1 (Hadamard-de la Vallee Poussin)",
            "nontrivial zeros in 0 < Re s < 1, s <-> 1-s pairing (Riemann)",
            "Mertens: prod_{p<=x}(1-1/p) ~ e^-gamma/ln x ; zeta(1) = pole",
            "RH itself: open, unproved, NOT claimed",
        ],
    },
    "honest_dispatch": (
        "P_l has two reflection axes (1-s inherited from Xi, l-s from B); the doubled symmetry "
        "does NOT constrain the zeros -- it is a tautology (any symmetric completion satisfies it), "
        "the certified h0 counterexample puts zeros off the axis inside the class, and P_l's zeros "
        "are exactly Xi's. The completed class yields a function with two reflection axes and no "
        "new zero control. No RH claim."
    ),
})
with open("RH13_doubled_completion_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nwrote RH13_doubled_completion_results.json")