#!/usr/bin/env python3
"""eq03_footing_lambda.py -- the two a0 footings as ONE parameter, and what the z=0 and z=2.5 data each measure.

The record carries two footings: a0 = kappa c sqrt(G rho_Lambda) (canonical, flat in z) and a0 = kappa c sqrt(G rho_total)
(alternative, tracks cH(z), rising). Both are kappa = 1/2. Write the density a0 'sees' as

        rho_seen(z) = rho_Lambda + lambda * rho_m(z),        rho_m(z) = rho_m0 (1+z)^3,        0 <= lambda <= 1,

so lambda = 0 is the canonical footing and lambda = 1 the alternative one (radiation and curvature neglected, stated
in E1). Then
        a0(z)^2 = kappa^2 (3/8pi) (c H0)^2 [Om_L + lambda Om_m (1+z)^3]
        a0(z)/a0(0) = sqrt[(Om_L + lambda Om_m (1+z)^3) / (Om_L + lambda Om_m)] .
z=0 fixes the PRODUCT kappa^2 (Om_L + lambda Om_m); the z=2.5 rise fixes lambda ALONE (kappa cancels), so the pair
measures both. Nothing here is a claim that a0 sees matter; lambda is the knob that turns the record's two-way fork into
a number a measurement can bound.
Exit 0 = every identity/control held; the numbers in E3-E5 are recomputed here from the committed likelihood result.
"""
import math
import sys
import sympy as sp

ok = []
def check(c, m):
    ok.append(bool(c)); print(f"  [{'OK' if c else 'FAIL'}] {m}")

c = 2.99792458e8
H0 = 67.4e3 / 3.0856775814913673e22
OmL, Omm = 0.685, 0.315                     # the footing scripts' values (Om_L + Om_m = 1, flat, radiation neglected)
Zf = math.sqrt(32 * math.pi / 3)

# ---- E1: exact limits ----------------------------------------------------------------------------------------
lam, z, OL, Om, kap, H = sp.symbols('lambda z Omega_L Omega_m kappa H0', positive=True)
R2 = (OL + lam * Om * (1 + z)**3) / (OL + lam * Om)
check(sp.simplify(R2.subs(lam, 0) - 1) == 0, "E1a  lambda = 0  ->  a0(z)/a0(0) = 1 exactly (canonical footing, flat)")
check(sp.simplify(R2.subs({lam: 1, Om: 1 - OL}) - (OL + (1 - OL) * (1 + z)**3)) == 0,
      "E1b  lambda = 1 (flat) -> a0(z)/a0(0)^2 = Om_L + Om_m (1+z)^3 = E(z)^2 exactly (alternative footing, tracks cH(z))")
a0_0 = kap * sp.sqrt(sp.Rational(3, 8) / sp.pi) * H * (OL + lam * Om)**sp.Rational(1, 2)
check(sp.simplify((a0_0.subs({lam: 1, Om: 1 - OL, kap: sp.Rational(1, 2)}) - H / (2 * sp.sqrt(sp.Rational(8, 3) * sp.pi)))) == 0,
      "E1c  lambda = 1, kappa = 1/2: a0(0) = c H0 / Z  (Z = 2 sqrt(8 pi/3)), the alt footing")
Ez_cert = math.sqrt(0.6862 + 0.3138 * 3.5**3)
check(3.7595 < Ez_cert < 3.7615, f"E1d  cross-check vs the ChainCert-certified E(2.5) in (3.76, 3.761) at Om_m = 0.3138: recomputed {Ez_cert:.4f}")

# ---- E2: sensitivity of the z = 2.5 rise ----------------------------------------------------------------------
def dex(lam_, zz=2.5):
    return 0.5 * math.log10((OmL + lam_ * Omm * (1 + zz)**3) / (OmL + lam_ * Omm))
print("\n  E2  a0(2.5)/a0(0) as a function of lambda (rise in dex; LCDM-native emergent scale is +0.33 dex, flat law 0.00)")
print(f"      {'lambda':>8}{'a0(2.5)/a0(0)':>16}{'dex':>8}")
for l in (0, 0.005, 0.01, 0.03, 0.05, 0.1, 0.3, 0.5, 0.7, 1.0):
    print(f"      {l:>8.3f}{10**dex(l):>16.3f}{dex(l):>8.3f}")
check(abs(dex(1.0) - math.log10(3.767)) < 2e-3, "E2a  lambda = 1: rise = E(2.5) = 3.77x, +0.576 dex")
lam_for = lambda target: next(l / 10000 for l in range(0, 10001) if dex(l / 10000) >= target)
l013, l033 = lam_for(0.13), lam_for(0.33)
print(f"      a matter admixture of only lambda = {l013:.3f} already raises a0(2.5) by 0.13 dex (one object's precision);")
print(f"      lambda = {l033:.3f} raises it by the LCDM-native +0.33 dex.")
check(l013 < 0.05, f"E2b  the flat-law test is a test of lambda < ~{l013:.3f}: a small admixture of rho_m is a large rise at z = 2.5")

# ---- E3: what the z = 0 amplitude says about lambda, for a given kappa ------------------------------------------
a0_hat, sig = 1.0766e-10, 0.0544             # committed SPARC profile likelihood (Upsilon free per galaxy), galaxy-clustered sigma
def Om_eff_from(a0v, kv):
    return (a0v / (c * H0))**2 * (8 * math.pi / 3) / kv**2
print("\n  E3  z = 0 amplitude -> Omega_eff = Om_L + lambda Om_m, then lambda, for a given kappa (SPARC a0 = 1.0766e-10, 5.44%):")
print(f"      {'kappa':<16}{'Om_eff':>8}{'+-':>7}{'lambda_hat':>12}{'+-':>7}{'0 excluded at':>15}{'1 excluded at':>15}")
kM = math.sqrt(2 / (3 * math.pi))
res = {}
for nm, kv in (("1/2", 0.5), ("sqrt(2/3pi)", kM)):
    Oe = Om_eff_from(a0_hat, kv); sO = 2 * sig * Oe
    lh = (Oe - OmL) / Omm; sl = sO / Omm
    res[nm] = (lh, sl)
    print(f"      {nm:<16}{Oe:>8.4f}{sO:>7.4f}{lh:>12.3f}{sl:>7.3f}{lh/sl:>13.2f} s{(1-lh)/sl:>13.2f} s")
check(abs(res["1/2"][0] - 0.70) < 0.02 and abs(res["1/2"][1] - 0.31) < 0.02, "E3a  kappa = 1/2: lambda_hat = 0.70 +- 0.31 (recomputed)")
print("      Read: at kappa = 1/2 the z = 0 amplitude puts lambda at 0.70 +- 0.31, which is 2.2 sigma above the flat law's 0 and 1.0 sigma")
print("      below the alternative footing's 1. That is the same 2.4 sigma 'pull toward the alternative footing' the record already")
print("      states, now as a bound on lambda. At kappa = sqrt(2/3pi) the fit wants Om_eff = 1.07 (> 1), i.e. lambda >= 1.")

# ---- E4: the pair (z = 0, z = 2.5) fixes kappa AND lambda -------------------------------------------------------
print("\n  E4  combined: a z = 2.5 rise D (dex) gives lambda; then kappa follows from the z = 0 amplitude.")
print(f"      {'D measured':>10}{'lambda':>9}{'kappa':>9}")
def lam_from_D(D):
    lo, hi = 0.0, 1.0
    if dex(hi) < D: return float('nan')
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        (lo, hi) = (mid, hi) if dex(mid) < D else (lo, mid)
    return 0.5 * (lo + hi)
for D in (0.0, 0.05, 0.13, 0.33, 0.576):
    l = lam_from_D(D)
    Oe = OmL + l * Omm
    kv = (a0_hat / (c * H0)) * math.sqrt(8 * math.pi / 3) / math.sqrt(Oe)
    print(f"      {D:>10.3f}{l:>9.3f}{kv:>9.4f}")
print("      (kappa = a0(0)/(cH0) sqrt(8pi/3)/sqrt(Om_eff); at D = 0 kappa = 0.575, at D = 0.576 kappa = 0.476.)")


# ---- E4b: the rise inverts in CLOSED FORM (certified in Lean: ChainCert/Footing.lean, foot_lambda_of_rise / foot_rise_of_lambda) ------
#      R^2 = rho  <=>  lambda = Om_L (rho - 1) / (Om_m (u - rho)),   u = (1+z)^3,  rho = 10^(2 D)
print("\n  E4b closed-form inverse lambda(D) = Om_L (10^(2D) - 1) / (Om_m ((1+z)^3 - 10^(2D))) against the bisection above:")
u25 = 3.5 ** 3
worst = 0.0
for D in (0.0, 0.05, 0.13, 0.33, 0.5, 0.576):
    rho = 10 ** (2 * D)
    lam_cf = OmL * (rho - 1) / (Omm * (u25 - rho))
    lam_bis = lam_from_D(D)
    if not math.isnan(lam_bis):
        worst = max(worst, abs(lam_cf - lam_bis))
    print(f"      D = {D:5.3f}   closed form {lam_cf:.6f}   bisection {lam_bis:.6f}")
check(worst < 1e-9, f"E4b  the closed-form inverse agrees with the bisection to {worst:.1e} at every D with a solution in [0,1]")
check(abs(OmL * (10 ** 0.26 - 1) / (Omm * (u25 - 10 ** 0.26)) - 0.0434) < 5e-4, "E4c  lambda = 0.043 gives +0.13 dex at z = 2.5, from the closed form alone")

# ---- E5: control -- a wrong evolution law must fail the E(z) cross-check ------------------------------------------
wrong = math.sqrt((OmL + 1.0 * Omm * (1 + 2.5)**2) / 1.0)      # (1+z)^2 instead of (1+z)^3
check(abs(wrong - Ez_cert) > 0.5, f"C1   control: a mutated matter scaling (1+z)^2 gives {wrong:.3f}, far from the certified E(2.5) = {Ez_cert:.3f}: the cross-check would catch it")
print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
