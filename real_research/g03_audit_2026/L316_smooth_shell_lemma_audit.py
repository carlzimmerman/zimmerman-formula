#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L316 -- AUDIT OF THE "SMOOTH-SHELL LEMMA": deepseek's g03_verdict (09-15) does not close G03.

THE CLAIM AUDITED (deepseek_push/g03_verdict.md): "an isotropic local screen -- Helmholtz or Gaussian, single or
double, 0.005-0.1 pc -- preserves the l=2 moment of the mu-transition shell ... the transition shell's l=2 moment
is the Cassini quadrupole; nothing local and isotropic can remove it", hence every G03 candidate fails Cassini
(>= 6.18x) and "the force-law class is closed WITH PROOF".  That verdict contradicts the lead track's G02
(qwen_claude_field_theory/closure_2026/g02_filtered_efe.py, 14/14 + the 09-04 correction): the T-B double
filter (QUMOND parent, output filter on the PHANTOM) survives Cassini statically for xi >= 0.02-0.03 pc.
Both cannot be right.  This lane finds which half of the lemma is true.

  A1 THE TRUE HALF: isotropic smoothing preserves the EXTERIOR l=2 moment int rho_2 r^4 dr EXACTLY (r^2 Y_2 is
     a harmonic polynomial; its average over any radial kernel is itself).  Verified numerically with the
     exact l=2-projected Gaussian kernel (it is also the kernel's normalisation check).
  A2 THE FALSE HALF: the Cassini quadrupole at Saturn is NOT that moment.  Saturn sits deep INSIDE the phantom
     shell (r_Saturn / r_M ~ 3e-4), so it feels the INTERIOR tidal coefficient int rho_2 r^-1 dr, whose weight
     r^-3 Y_2 is singular at the Sun.  Once xi >~ r_M the smoothing ball covers the singularity and the
     coefficient is suppressed.  Computed on a phantom-like l=2 shell centred on r_M vs xi/r_M.
  A3 WHERE THE SUPPRESSION REACHES THE CEILING: the bare kernel is 6.44x (canonical) / 7.63x (alt) above the
     Park ceiling (L243); the xi/r_M at which the toy shell's interior coefficient falls by that factor, in pc,
     against G02's committed floors 0.02/0.03 pc.  (A toy shell, so an order-of-magnitude cross-check of G02,
     not a replacement for it.)
  A4 THE AQUAL-DIVERGENCE CAVEAT (sympy): a filter (1 - xi^2 lap) applied to div[mu grad Phi] acts on the
     SOURCE, whose vacuum value is zero.  With a point Sun it replaces the Sun by a Yukawa cloud
     e^{-r/xi}/(4 pi xi^2 r): the enclosed mass at Saturn is ~(r/xi)^2/2 ~ 1e-6.  That is not T-B, whose output
     filter acts on the phantom only.
  MUTATE=1 uses the exterior weight r^2 in place of the interior r^-3 in A2: the "suppression" then disappears
     and A2 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/g03_audit_2026/L316_smooth_shell_lemma_audit.py
"""
import os, sys, json, math
import numpy as np
import sympy as sp
from scipy.special import ive
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L316_smooth_shell_lemma_audit"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L316", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 104); P(t); P("=" * 104)


P(__doc__)
GM_SUN, PC, AU = 1.32712440018e20, 3.0856775814913673e16, 1.495978707e11
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
R_M = {k: math.sqrt(GM_SUN / v) for k, v in A0.items()}
BARE = {"canonical": 6.44, "alt": 7.63}                 # L243 |Q2|/ceiling of the bare kernel
G02_FLOOR_PC = {"gaussian": (0.02, 0.03), "helmholtz": 0.03}


def K2(a, r, xi):
    """l=2 projection of the normalised 3D Gaussian kernel of width xi (per unit r^2 dr)."""
    x = a * r / xi**2
    if x < 1e-8:
        return 0.0
    i2_scaled = math.sqrt(math.pi / (2 * x)) * ive(2.5, x)          # i_2(x) e^{-x}
    return 4 * math.pi / ((2 * math.pi)**1.5 * xi**3) * math.exp(-(a - r)**2 / (2 * xi**2)) * i2_scaled


def smoothed_weight(a, xi, power):
    """[K * (r^power Y_2)](a)/Y_2 = int K2(a,r) r^power r^2 dr."""
    f = lambda r: K2(a, r, xi) * r**power * r**2
    lo, hi = max(1e-9, a - 12 * xi), a + 12 * xi
    val, _ = quad(f, lo, hi, limit=400, epsabs=0, epsrel=1e-9)
    return val


# a phantom-like l=2 shell: log-normal in r around r_M (width 0.5 in ln r); units of r_M
def shell(a):
    return math.exp(-(math.log(a))**2 / (2 * 0.5**2))


AGRID = np.geomspace(0.05, 20, 700)

# ============================================================================================ A1
banner("A1  THE TRUE HALF: the exterior l=2 moment is preserved exactly by isotropic smoothing")
ext = []
for xi in (0.3, 1.0, 3.0):
    num = np.trapz([shell(a) * a**2 * smoothed_weight(a, xi, 2) for a in AGRID], AGRID)
    den = np.trapz([shell(a) * a**2 * a**2 for a in AGRID], AGRID)
    ext.append((xi, num / den))
    P(f"    xi/r_M = {xi:3.1f}: smoothed/unsmoothed exterior moment = {num/den:.6f}")
OUT["numbers"]["exterior_ratio"] = ext
check("A1 isotropic Gaussian smoothing preserves int rho_2 r^4 dr to < 1e-3 at every xi (r^2 Y_2 is harmonic)",
      [round(v, 6) for _, v in ext], all(abs(v - 1) < 1e-3 for _, v in ext),
      "this is the half of the smooth-shell lemma that is TRUE -- and it also validates the l=2 kernel")

# ============================================================================================ A2
banner("A2  THE FALSE HALF: the interior tidal coefficient (what Saturn feels) IS suppressed once xi >~ r_M")
pw = 2 if MUTATE else -3
XIS = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]
den = np.trapz([shell(a) * a**2 * a**pw for a in AGRID], AGRID)
supp = []
for xi in XIS:
    num = np.trapz([shell(a) * a**2 * smoothed_weight(a, xi, pw) for a in AGRID], AGRID)
    supp.append((xi, num / den))
    P(f"    xi/r_M = {xi:4.2f}: interior coefficient ratio = {num/den:.4f}")
OUT["numbers"]["interior_ratio"] = supp
r_small = dict(supp)[0.05]; r_big = dict(supp)[3.0]
check("A2 the interior l=2 tidal coefficient is unchanged for xi << r_M and suppressed by > 10x at xi = 3 r_M",
      f"ratio {r_small:.4f} at xi = 0.05 r_M; {r_big:.4f} at xi = 3 r_M",
      abs(r_small - 1) < 0.02 and r_big < 0.1,
      "the lemma conflates the exterior moment (preserved) with the interior coefficient (not preserved): "
      "Saturn is at 3e-4 r_M, deep inside the shell, and feels the latter")

# ============================================================================================ A3
banner("A3  WHERE THE TOY SUPPRESSION REACHES THE CEILING, in pc, against G02's committed floors")
xs = np.array([s[0] for s in supp]); rs = np.array([s[1] for s in supp])
floors = {}
for fk in ("canonical", "alt"):
    target = 1.0 / BARE[fk]
    ok_idx = np.where(rs <= target)[0]
    if len(ok_idx) == 0:
        floors[fk] = None
        continue
    j = ok_idx[0]
    x_cross = float(np.exp(np.interp(math.log(target), [math.log(rs[j]), math.log(rs[j - 1])],
                                     [math.log(xs[j]), math.log(xs[j - 1])])))
    floors[fk] = dict(xi_over_rM=x_cross, xi_pc=x_cross * R_M[fk] / PC, r_M_pc=R_M[fk] / PC)
    P(f"    {fk:9s}: bare {BARE[fk]}x -> needs ratio {target:.3f}; toy shell reaches it at xi = {x_cross:.2f} r_M "
      f"= {x_cross * R_M[fk] / PC:.3f} pc (r_M = {R_M[fk] / PC:.4f} pc); G02 committed floor 0.02-0.03 pc")
OUT["numbers"]["toy_floor"] = floors
okA3 = all(v is not None and 0.005 < v["xi_pc"] < 0.3 for v in floors.values())
check("A3 the toy shell's ceiling-crossing screen length lands at O(r_M) ~ 0.01-0.1 pc on both footings, the same "
      "order as G02's committed floors (0.02/0.03 pc)",
      {k: (round(v["xi_pc"], 4) if v else None) for k, v in floors.items()}, okA3,
      "an order-of-magnitude cross-check: the mechanism G02 used is real; deepseek's null at xi <= 0.1 pc is "
      "not a property of isotropic screens", load_bearing=False)

# ============================================================================================ A4
banner("A4  THE AQUAL-DIVERGENCE CAVEAT: a filter on div[mu grad Phi] acts on the source, not on the phantom")
r, xi = sp.symbols("r xi", positive=True)
Gx = sp.exp(-r / xi) / (4 * sp.pi * xi**2 * r)
helm = sp.simplify(Gx - xi**2 * sp.diff(r**2 * sp.diff(Gx, r), r) / r**2)
norm = sp.simplify(sp.integrate(4 * sp.pi * r**2 * Gx, (r, 0, sp.oo)))
frac = {}
for xpc in (0.02, 0.03, 0.1):
    q = 9.58 * AU / (xpc * PC)
    frac[xpc] = 1 - (1 + q) * math.exp(-q)
OUT["numbers"]["saturn_enclosed_fraction"] = frac
check("A4 (1 - xi^2 lap) G = 0 for r > 0 with int G = 1: filtering the AQUAL divergence replaces a point Sun by a "
      "Yukawa cloud; enclosed at Saturn: " + ", ".join(f"{k} pc -> {v:.1e}" for k, v in frac.items()),
      f"residual {helm}; normalisation {norm}", helm == 0 and norm == 1 and max(frac.values()) < 1e-4,
      "so a divergence filter is either this (Newton destroyed at Saturn) or, with the Sun imposed as an inner "
      "boundary condition as in g03_candidate1_gates.py, it acts only through boundary rows -- in neither case "
      "is it T-B, whose output filter acts on the phantom (QUMOND form)")

# ============================================================================================ verdict
banner("VERDICT")
P("""  The smooth-shell lemma is true of the EXTERIOR l=2 moment and false of the INTERIOR tidal coefficient, which
  is what Saturn measures.  Isotropic smoothing on a scale >~ r_M suppresses the Cassini quadrupole, at the order
  of G02's committed floors.  deepseek's g03_verdict therefore does not close G03 and should not be cited as a
  proof that the force-law class fails Cassini; G02's static T-B survival stands, and G03 remains astra's open
  lane (the C-H action exists; its causal feasibility is OPEN with one adverse electrovacuum-cylinder result).""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
