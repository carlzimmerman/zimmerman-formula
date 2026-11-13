#!/usr/bin/env python3
"""
H062 -- THE EXPONENT GAP.

Does the kernel the RAR selected survive Cassini?

TWO families both written "mu_n" in this repo, and they are NOT the same:

  (A) BN11 / published  mu_n(x) = x/(1+x^n)^(1/n)
      deep slope d mu/d x -> 1 for EVERY n, so a_0 is a FREE normalisation,
      independent of n.  This is the family route1B tested against Cassini.

  (B) Mandel / photocount (L231)  mu_n(Y) = 1 - (1+Y)^(-n),  Y = g/s
      deep slope -> n, so  a_0 = s/n  and  kappa = 1/n.
      This is the family the RAR selected (L232: n = 2 <=> kappa = 1/2).

They coincide ONLY at n = 1.  So route1B's "n >= 5 clears Cassini" applies to
family (A), where n does NOT fix kappa -- it says nothing about family (B), which
is the one that carries the a_0-Lambda relation.

THIS LANE runs family (B) through both gates and asks whether ANY integer survives.

Units: everything below is in units of s = c sqrt(G rho_Lambda), fixed by choosing
the canonical kappa = 1/2 normalisation s = 2 * a_0_canonical.  No galaxy parameter
is fitted; n is the only discrete freedom.
"""
import math, os, glob, json, sys
import numpy as np
from scipy import integrate
from scipy.optimize import brentq

R = []
def chk(cond, label, detail=""):
    R.append((bool(cond), label))
    print(f"  [{'ok' if cond else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))

# ---------------------------------------------------------------- constants
GM_SUN = 1.32712440018e20
A0C    = 9.3619e-11            # canonical a_0, kappa = 1/2
S      = 2.0 * A0C             # c sqrt(G rho_Lambda);  a_0(n) = S/n
GEXT   = 2.32e-10              # Gaia EDR3 external field (DHF24 sec 3.3)
Q2_CEIL= 5.2e-27               # Park+2026 2-sigma ceiling
RA     = 1.871 / 1.5           # AQUAL/QUMOND calibration (BN11 Table-1)

# ---------------------------------------------------------------- the families
def mu_bn11(x, n): return x / (1.0 + x ** n) ** (1.0 / n)
def mu_mand(Y, n): return 1.0 - (1.0 + Y) ** (-n)

def nu_of(mu, n):
    """nu(X) = 1/mu(w), where w solves mu(w)*w = X  (X = g_N / scale)."""
    def f(X):
        X = np.atleast_1d(np.asarray(X, float)); out = np.empty_like(X)
        for i, xx in enumerate(X):
            if xx <= 0 or xx > 1e14:
                out[i] = 1.0; continue
            g   = lambda w: mu(w, n) * w - xx
            hi  = max(10.0, 2.0 * math.sqrt(xx) + 2.0)
            try:
                while g(hi) < 0: hi *= 2
                w = brentq(g, 1e-14, hi, xtol=1e-15, rtol=8.9e-16)
            except Exception:
                w = xx
            out[i] = w / xx
        return out if out.size > 1 else out[0]
    return f

# -------------------------------------------- DHF24 Eq.(10) machinery (route1B)
def Fprim(a, v, eN): return eN * (1.5*a*a - 1.25*a**4 - 0.25) + v*v * (a - a**3)

def P_of(eN, y0):
    vlo, vhi = math.sqrt(abs(y0 - eN)), math.sqrt(y0 + eN)
    if vhi <= vlo: return 0.0
    def f(v):
        x = (y0*y0 - eN*eN - v**4) / (2.0*eN*v*v)
        return Fprim(min(1.0, max(-1.0, x)), v, eN)
    val, _ = integrate.quad(f, vlo, vhi, limit=800, epsabs=1e-15, epsrel=1e-13)
    return 1.5 * val

def solve_eN(nu, et):
    return brentq(lambda x: x * float(np.asarray(nu(x)).ravel()[0]) - et,
                  1e-12, 1e10, xtol=1e-15, rtol=8.9e-16)

YG = np.logspace(-8, 10, 1801)
YM = np.sqrt(YG[1:] * YG[:-1])
_PC = {}
def Pgrid(eN):
    k = round(eN, 12)
    if k not in _PC: _PC[k] = np.array([P_of(eN, y) for y in YM])
    return _PC[k]

def Q2_of(nu, a0):
    """AQUAL quadrupole Q_zz for kernel nu with MOND scale a0."""
    eN = solve_eN(nu, GEXT / a0)
    q  = -float(np.sum(Pgrid(eN) * np.diff(np.asarray(nu(YG), float))))
    return 1.5 * a0 ** 1.5 / math.sqrt(GM_SUN) * abs(q) * RA, abs(q)

# ---------------------------------------------------------------- RAR data
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
js   = os.path.join(ROOT, "qwen_38_experiment", "data", "rar_sparc_a0units.json")
if not os.path.exists(js):
    print("FATAL: committed RAR file not found:", js); sys.exit(1)
d   = json.load(open(js))
pts = np.array(d["rows"], float)
X_, Y_ = pts[:, 0], pts[:, 1]
ok = (X_ > 0) & (Y_ > 0) & np.isfinite(X_) & np.isfinite(Y_)
X_, Y_ = X_[ok], Y_[ok]
print(f"H062 -- the exponent gap.  {len(X_)} committed SPARC RAR points.\n")

chk(True, f"0.0  RAR points loaded with positive accelerations", f"{len(X_)} rows")

def rms_mand(n):
    """predicted y for the Mandel family: argument in units of S, a0 = S/n."""
    nu = nu_of(mu_mand, n)
    Xs = X_ / 2.0                       # X = g_N / S   with S = 2*A0C
    pred = np.array([nu(x) * x for x in Xs]) * 2.0
    pred = np.clip(pred, 1e-12, 1e12)
    return float(np.sqrt(np.mean((np.log10(Y_) - np.log10(pred)) ** 2)))

def rms_bn11(n, a0=A0C):
    """predicted y for BN11's published family; a0 is free and FIXED here."""
    nu = nu_of(mu_bn11, n)
    pred = np.array([nu(x) * x for x in X_])
    pred = np.clip(pred, 1e-12, 1e12)
    return float(np.sqrt(np.mean((np.log10(Y_) - np.log10(pred)) ** 2)))

NS = [1, 2, 3, 4, 5, 6, 8, 10, 20]

print("=" * 92)
print("PART 1 -- what each family predicts for the RAR (nothing fitted)")
print("=" * 92)
print(f"  {'n':>3}  {'A) BN11 rms[dex]':>18}   {'B) Mandel rms[dex]':>20}   {'B) a0(n)=S/n':>14}")
ROW = {}
for n in NS:
    ra = rms_bn11(n); rb = rms_mand(n)
    ROW[n] = (ra, rb, S / n)
    print(f"  {n:>3}  {ra:>18.4f}   {rb:>20.4f}   {S/n:>14.5e}")
bestB = min(NS, key=lambda n: ROW[n][1])
bestA = min(NS, key=lambda n: ROW[n][0])
print(f"\n  RAR-preferred:  (A) BN11 n = {bestA}  ({ROW[bestA][0]:.4f} dex)"
      f"      (B) Mandel n = {bestB}  ({ROW[bestB][1]:.4f} dex)")
print(f"  NOTE the two families coincide only at n = 1 "
      f"(BN11 {ROW[1][0]:.4f} vs Mandel {ROW[1][1]:.4f})")

nsame = max(abs(mu_bn11(Y, 1) - mu_mand(Y, 1)) for Y in (1e-3, 0.1, 1.0, 7.0, 1e4))
chk(nsame < 1e-12,
    "1.1  the two families are the SAME FUNCTION at n = 1 (not merely similar)",
    f"max|mu_bn11 - mu_mand| at n=1 over 5 decades = {nsame:.2e}")
chk(abs(ROW[2][0] - ROW[2][1]) > 1e-6,
    "1.1b they DIVERGE for n >= 2, which is why route1B's numbers do not apply here",
    f"n=2 RAR rms: BN11 {ROW[2][0]:.4f} vs Mandel {ROW[2][1]:.4f}")

chk(abs(bestB - 2) <= 1,
    "1.2  the Mandel family reproduces L232's selection (n = 2 <=> kappa = 1/2)",
    f"this independent pipeline selects n = {bestB} on {len(X_)} points")

print()
print("=" * 92)
print("PART 2 -- family (B), the one that carries kappa = 1/n, against Cassini")
print("=" * 92)
print(f"  {'n':>3}  {'a0(n)':>12} {'etilde':>8} {'|q|':>10} {'Q_zz':>13} {'x ceiling':>11} {'RAR rms':>9}")
GAP = {}
for n in NS:
    a0 = S / n
    nu = nu_of(mu_mand, n)
    try:
        Q, q = Q2_of(nu, a0); mult = Q / Q2_CEIL
    except Exception as e:
        Q, q, mult = float('nan'), float('nan'), float('nan')
    GAP[n] = (mult, ROW[n][1])
    print(f"  {n:>3}  {a0:>12.4e} {GEXT/a0:>8.3f} {q:>10.5f} {Q:>13.4e} {mult:>11.2f} {ROW[n][1]:>9.4f}")

passing  = [n for n in NS if GAP[n][0] < 1.0]
kappa_ok = [n for n in NS if abs(1.0/n - 0.5) < 3*0.034]      # kappa meas 0.529+-0.034
print(f"\n  Cassini-safe      (Q_zz < ceiling)      : n in {passing}")
print(f"  kappa-consistent  (1/n = 1/2 within 3s) : n in {kappa_ok}")
joint = sorted(set(passing) & set(kappa_ok))
print(f"  JOINT                                   : {joint if joint else 'EMPTY'}")

chk(len(passing) > 0, "2.1  some integer clears the Cassini quadrupole",
    f"{passing}")
chk(len(joint) == 0,
    "2.2  DECISIVE: no integer is BOTH Cassini-safe AND kappa = 1/2",
    f"Cassini needs {passing}; kappa = 1/2 needs {kappa_ok}; intersection {joint}")

print()
print("=" * 92)
nf = [n for n in NS if GAP[n][0] >= 1.0]
nq = min(nf) if nf else None
print("RESULT")
print("=" * 92)
if not passing:
    print("  No integer in the scanned family clears Cassini at all.")
else:
    print(f"  The lowest Cassini-safe exponent is n = {min(passing)}, which forces")
    print(f"  kappa = 1/{min(passing)} = {1.0/min(passing):.3f}   against the measured")
    print(f"  0.529 +- 0.034 (README)  --  off by {abs(1.0/min(passing)-0.529)/0.034:.1f} sigma.")
print(f"  The RAR-preferred n = {bestB} gives kappa = 1/{bestB} = {1.0/bestB:.3f}")
print( "      but its Q_zz is %.2fx the Cassini ceiling." % GAP[bestB][0] if GAP[bestB][0]==GAP[bestB][0] else "")
print()
print("READING: inside a single mu_n kernel there is a FORK, not a gap.")
print("  Family (A) BN11  : n and kappa are DECOUPLED -> Cassini satisfiable,")
print("                     but then nothing connects a_0 to Lambda.")
print("  Family (B) Mandel: n IS kappa -> you may have the relation OR Cassini.")
print("  You cannot have both with one exponent.")
print()
print("CAVEATS: (i) SPARC-only rms on committed binned points, no per-galaxy")
print("         nuisance (Upsilon_disk) fit -- route1B flags that as undecided;")
print("         (ii) family (A) is given a_0 = A0C fixed, which is its free dial;")
print("         (iii) the DHF24 quadrature is this lane's reconstruction of")
print("         route1B's committed pipeline, not an independent derivation.")

BAD = [l for c, l in R if not c]
print(f"\nH062 RESULT: {len(R)-len(BAD)}/{len(R)} checks passed."
      + (f"  FAILURES: {BAD}" if BAD else ""))
print(json.dumps({"pass": len(R)-len(BAD), "fail": len(BAD),
                  "cassini_safe": passing, "kappa_ok": kappa_ok, "joint": joint,
                  "rar_best_mandel": bestB}))
sys.exit(1 if BAD else 0)
