#!/usr/bin/env python3
"""u04_ratio_and_pole_scale.py -- lane U task item (3): is G rho_Lambda / a0^2 a pure fixed-point number, and can it be 4?

Setup.  Any RG running with G(k) = g/k^2, Lambda(k) = lambda k^2 (fixed-point form) has
      G(k) rho_Lambda(k) = Lambda(k)/(8 pi) = lambda k^2/(8 pi)        (g cancels identically; u02 part B).
An acceleration scale from the RG must be a0 = c^2 k_X/zeta for some RG scale k_X (the only mass-free acceleration, u03 part A) with a pure number zeta.  Then
      R(X, zeta) := G rho_Lambda/a0^2 = lambda_X zeta^2/(8 pi) ,   and  R = 4  <=>  zeta = zeta_req = sqrt(32 pi/lambda_X).
The candidates for k_X:
   X1  a UV-fixed-point scale (Lambda = lambda*_UV k^2, lambda* scheme dependent; from u01)       -- irrelevant at galactic accelerations, listed for completeness;
   X2  the Einstein-Hilbert IR termination scale k_term where lambda(k) = Lambda/k^2 reaches 1/2 (Reuter-Weyer hep-th/0410119 eq (49): k_term ~ sqrt(Lambda));
       exactly k_term^2 = 2 Lambda for any regulator with P(z) = z + R0(z) >= P(0) = 1 (pole at lambda = min P/2), a normalisation-tied number;
   X3  the cosmological scale k = xi/t of the Bonanno-Reuter fixed-point era, with xi fixed by Bianchi consistency: Lambda t^2 = 8/(3(1+w)^2).
Pre-declared discriminator: a 'hit' = |R/4 - 1| < 5% for some (X, zeta) in the pre-declared natural menu zeta in {1, 2, pi, 2 pi, 4 pi}.  I wrote this menu knowing the target;
the decoy control estimates how often a random target in [2, 8] is 'hit' by the same menu (base rate).  A near-hit is NOT a result unless it beats the decoys.
Controls: pole location vs numerics for several regulators (incl. one with non-monotone P, where lambda_pole != 1/2), rescaled-normalisation mutation, decoy base rate.
Exit 0 iff all pass.
"""
import math
import sys
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.integrate import quad


ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

# --- shapes (copied definitions, R only) ---
def shapes():
    S = {}
    S["exp s=1"] = lambda z: 1.0 if z < 1e-12 else z / math.expm1(z)
    S["exp s=3"] = lambda z: 1.0 if z < 1e-12 else 3 * z / math.expm1(3 * z)
    S["z^2/(e^(z^2)-1)"] = lambda z: 1.0 if z < 1e-12 else z * z / math.expm1(z * z)
    S["optimised"] = lambda z: max(1.0 - z, 0.0)
    S["exp(-z)"] = lambda z: math.exp(-z)
    S["rational 1/(1+z)^2"] = lambda z: 1.0 / (1.0 + z)**2
    return S

print("=" * 100); print("PART A  where does the EH flow terminate?  (Phi's diverge when min_z [z + R0(z)] + w = 0, w = -2 lambda)"); print("=" * 100)
print(f"  {'shape':22s} {'min_z (z+R0)':>14s} {'lambda_pole = min/2':>20s}  monotone P?")
lam_pole = {}
for name, R in shapes().items():
    P = lambda z: z + R(z)
    zs = np.linspace(0, 6, 60001)
    Pv = np.array([P(z) for z in zs])
    m = Pv.min(); mono = bool(np.all(np.diff(Pv) >= -1e-14))
    lam_pole[name] = m / 2
    print(f"  {name:22s} {m:14.6f} {m / 2:20.6f}  {mono}")
mono_names = [n for n in lam_pole if n in ("exp s=1", "z^2/(e^(z^2)-1)", "optimised", "exp(-z)")]
nonmono_names = [n for n in lam_pole if n in ("exp s=3", "rational 1/(1+z)^2")]
check("every regulator with monotone P = z + R0 (the standard admissibility, R0'(0) >= -1) has its pole at lambda = 1/2 exactly", all(abs(lam_pole[n] - 0.5) < 1e-6 for n in mono_names))
check("CONTROL: regulators with non-monotone P (exp s=3 has R0'(0) = -3/2; 1/(1+z)^2) have their pole strictly below 1/2 (0.458, 0.445): the '1/2' is a property of the normalisation R0(0)=1 with monotone P, not of gravity", all(lam_pole[n] < 0.49 for n in nonmono_names))
# numerical divergence check for two shapes: (1-2 lambda) Phi diverges / grows as lambda -> 1/2
def Phi_nm(R, Rp, p, n, w, zmax):
    f = lambda z: z**(n - 1) * (R(z) - z * Rp(z)) / (z + R(z) + w)**p
    v, _ = quad(f, 0, zmax, limit=400, epsabs=1e-12, epsrel=1e-10)
    return v / math.gamma(n)
Ropt = lambda z: max(1 - z, 0.0); Roptp = lambda z: -1.0 if z < 1 else 0.0
vals = [Phi_nm(Ropt, Roptp, 2, 2, -2 * (0.5 - d), 1.0) for d in (1e-1, 1e-2, 1e-3)]
print(f"  optimised cutoff Phi^2_2(-2 lambda) at lambda = 1/2 - (0.1, 0.01, 0.001): {[f'{v:.3f}' for v in vals]}  (exact 1/(2(2 delta)^2))")
check("optimised cutoff: Phi^2_2 blows up like 1/(1-2 lambda)^2 as lambda -> 1/2", abs(vals[2] / (1 / (2 * (2e-3)**2)) - 1) < 1e-6)
# normalisation mutation: R0(0) = a moves the pole to a/2  (equivalent to rescaling k -> k sqrt(a), i.e. to changing zeta)
a = 1.7
Rm = lambda z: a * math.exp(-z / a)          # monotone P = z + a exp(-z/a), R(0) = a
zs = np.linspace(0, 6, 6001)
m = min(z + Rm(z) for z in zs)
check("MUTATION: R0(0) = a = 1.7 puts the pole at lambda = a/2 = 0.85: the number 1/2 is a normalisation convention (k -> sqrt(a) k), degenerate with zeta", abs(m / 2 - a / 2) < 1e-6)
print("  Consequence: k_term^2 = 2 Lambda holds in the convention R_k(0) = k^2; in another convention k_term^2 = 2 Lambda/a.  Only the product (convention) x zeta below is meaningful.")

print(); print("=" * 100); print("PART B  R(X, zeta) = G rho_Lambda / a0^2 with a0 = c^2 k_X/zeta"); print("=" * 100)
# lambda* values from u01 (the printed table); re-derive quickly here from the optimised closed form and a few numbers copied from u01's output
import re, subprocess
out = open(__file__.rsplit('/', 1)[0] + "/u01_eh_fixed_points.out").read()
rows = re.findall(r"^\s{2}(\S.*?\S)\s{2,}([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+-2.0000", out, flags=re.M)
lam_uv = {r[0]: float(r[2]) for r in rows}
print(f"  UV-fixed-point lambda* read from u01_eh_fixed_points.out ({len(lam_uv)} shapes): {dict((k, round(v, 4)) for k, v in lam_uv.items())}")
check("u01 output parsed: 9 shapes", len(lam_uv) == 9)
lam_uv["Litim alpha->inf (u01 part 6)"] = 0.25
Ls = np.array(list(lam_uv.values()))

def R_of(lam_X, zeta): return lam_X * zeta**2 / (8 * math.pi)
menu = [1.0, 2.0, math.pi, 2 * math.pi, 4 * math.pi]
print(f"\n  X1 (UV fixed point, scheme spread lambda* in [{Ls.min():.3f}, {Ls.max():.3f}]):  R = lambda* zeta^2/(8 pi)")
print(f"     {'zeta':>8s} {'R min':>10s} {'R max':>10s}")
for z in menu:
    print(f"     {z:8.4f} {R_of(Ls.min(), z):10.4f} {R_of(Ls.max(), z):10.4f}")
zr1 = np.sqrt(32 * math.pi / Ls)
print(f"     zeta_req = sqrt(32 pi/lambda*) in [{zr1.min():.2f}, {zr1.max():.2f}]")
# X2: pole scale, Lambda = k_term^2/2 => lambda_X = 1/2
lamX2 = 0.5
print(f"\n  X2 (EH termination scale, Lambda = k_term^2/2):  R = zeta^2/(16 pi)")
for z in menu:
    print(f"     zeta = {z:8.4f}:  R = {R_of(lamX2, z):8.4f}")
zr2 = math.sqrt(32 * math.pi / lamX2)
print(f"     zeta_req = sqrt(64 pi) = 8 sqrt(pi) = {zr2:.4f}")
check("X2: zeta_req = 8 sqrt(pi) = 14.18", abs(zr2 - 8 * math.sqrt(math.pi)) < 1e-12)
# X3: cosmic time. a0 = c^2/(zeta t); Lambda t^2 = 8/3 (w=0) -> lambda_X = Lambda t^2 = 8/3 with k -> 1/t
lamX3 = 8.0 / 3.0
print(f"\n  X3 (Bonanno-Reuter fixed-point era, w = 0, k -> 1/t, Lambda t^2 = 8/3):  R = (8/3) zeta^2/(8 pi) = zeta^2/(3 pi)")
for z in menu:
    print(f"     zeta = {z:8.4f}:  R = {R_of(lamX3, z):8.4f}")
zr3 = math.sqrt(32 * math.pi / lamX3)
print(f"     zeta_req = sqrt(12 pi) = {zr3:.4f}   (2 pi = {2 * math.pi:.4f}; ratio {zr3 / (2 * math.pi):.4f})")
check("X3: zeta_req = sqrt(12 pi) = 6.14", abs(zr3 - math.sqrt(12 * math.pi)) < 1e-12)
print("     NB: a0 = c^2/(2 pi t) with the cosmic time t (Milgrom's 2 pi applied to 1/t, not to H = 4/(3t)) gives R = 4 pi/3 = 4.19, 4.7% above 4.  Reported as a near-miss, not a result (see decoys).")

print(); print("=" * 100); print("PART C  pre-declared menu hit test and decoy base rate"); print("=" * 100)
Xs = {f"UV {k}": v for k, v in lam_uv.items()}; Xs["X2 pole"] = lamX2; Xs["X3 cosmic"] = lamX3
def hits(target, tol=0.05):
    h = []
    for name, lam in Xs.items():
        for z in menu:
            if abs(R_of(lam, z) / target - 1) < tol:
                h.append((name, z))
    return h
h4 = hits(4.0)
print(f"  hits of the true target R = 4 within 5%: {h4}")
rng = np.random.default_rng(20260929)
targets = np.exp(rng.uniform(math.log(2.0), math.log(8.0), 20000))
frac = np.mean([len(hits(T)) > 0 for T in targets[:4000]])
print(f"  base rate: fraction of decoy targets in [2, 8] (log-uniform) hit within 5% by the same menu: {frac:.3f}")
check("the menu can express 4 within 5% (X3 with zeta = 2 pi, 4.7%): reported honestly as a near-miss", any(n == "X3 cosmic" and abs(z - 2 * math.pi) < 1e-9 for n, z in h4))
check("but the base rate of random targets being 'hit' by the same menu is >= 20% (uninformative)", frac >= 0.20)
# exact-4 requirement never met by a natural zeta:
exact = [(n, z) for n, lam in Xs.items() for z in menu if abs(R_of(lam, z) - 4.0) < 1e-9]
check("NO (X, zeta) in the menu gives exactly R = 4", len(exact) == 0)

print(); print("=" * 100); print("PART D  what the RG lane would have to supply, in one line"); print("=" * 100)
print("  G rho_Lambda = 4 a0^2  <=>  zeta^2 lambda_X = 32 pi.   Required: X2: zeta = 8 sqrt(pi); X3: zeta = sqrt(12 pi); X1: zeta in [16.7, 25.6] (scheme dependent).")
print("  Every RG paper leaves the cutoff-identification constant free (xi, kappa, zeta); where Bianchi consistency fixes it (X3) the fixed quantity is Lambda t^2, not an acceleration.")


print(); print("=" * 100); print("PART E  a warning against a decoy: the '32 pi^2' in the Shapiro-Sola-Stefancic running of rho_Lambda"); print("=" * 100)
import sympy as sp
nu0 = sp.Rational(1, 1) / (12 * sp.pi)          # SSS eq (3.9): |nu| = nu_0 = 1/(12 pi), sigma = +-1, M = M_P
C1_over_MP2 = 3 * nu0 / (8 * sp.pi)              # SSS (3.7): C1 = 3 nu M_P^2/(8 pi);  rho_Lambda(H) = C0 + C1 H^2
print("  SSS: rho_Lambda(H) = C0 + C1 H^2, C1 G = 3 nu/(8 pi); with their 'conservative' nu_0 = 1/(12 pi):  C1 G =", sp.simplify(C1_over_MP2))
check("3 nu_0/(8 pi) = 1/(32 pi^2)  (the standard one-loop factor 1/(2 (4 pi)^2), NOT the puzzle's 32 pi^2)", sp.simplify(C1_over_MP2 - 1 / (32 * sp.pi**2)) == 0)
print(f"  It would give G rho_Lambda^run = H^2/(32 pi^2) => 'a0' = (1/2) sqrt(.) = H/(8 sqrt(2) pi) = {1/(8*math.sqrt(2)*math.pi):.4f} H, vs needed ~0.12-0.17 H: no relation.  nu is free (nu ~ 1e-6 in their galaxy section vs 1e-2 in cosmology).")
check("that 'a0' is >3x below the framework's a0/(cH) = 0.14 (0.028 vs 0.145 at Omega_L = 0.7)", 1 / (8 * math.sqrt(2) * math.pi) < 0.145 / 3)

print()
fails = ok.count(False)
print(f"RESULT: {ok.count(True)} checks passed, {fails} failed")
sys.exit(1 if fails else 0)
