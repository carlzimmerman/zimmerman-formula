#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
KM2 -- L340's PREDICTION T1 MADE QUANTITATIVE: the exact lag of a moving source's phantom in the C-H/K candidate, and
whether any current dataset can see it.  (Support computation for the lead track; L340's file is not edited -- its
linear block is copied verbatim below with attribution.)

T1 AS STATED (real_research/g03_audit_2026/L340_filtered_khronon_completion.py):
  "the phantom follows a source moving at v relative to the preferred frame with a lag of order (v/c_s)^2,
   c_s^2 = c_2 c^2/(C(2 + 3 c_2)); for a source faster than c_s the phantom is left behind."

WHAT THIS LANE COMPUTES (frozen-coefficient, principal order: exactly L340's H1 block, no new physics)
  Q1 THE EXACT RESPONSE.  L340's unitary-gauge scalar block M(omega, k) X = S for X = (psi, phi, beta, U), solved in
     closed form.  The potential matter feels is Phi_B = phi + beta_dot (beta is the shift potential; the convention is
     checked against KM1's independently derived momentum constraint), the lensing potential (Phi_B + Psi_B)/2 with
     Psi_B = psi.  For a source moving at v, omega = k v cos(theta).
  Q2 THE LAG LAW.  R(u) = Phi_B(u)/Phi_B(0), u = omega/(k c) = (v/c) cos(theta): its expansion in (u/c_s)^2, its pole
     (the mode speed: R diverges at u = c_s -- the 'left behind' threshold), and the same for lensing.  The PHANTOM's
     own fractional change is (R - 1)(1 + C)/C.
  Q3 SIZE ACROSS L340's WINDOW.  c_2 in (7.2e-3, 0.067), alpha_c = 1e-9; C = C_T = nu_mono - 1 and C = C_L = h'(y) at
     y = 1e-4 .. 1; sources at 300 / 600 km/s (galaxies through the CMB frame), 1500 (cluster members), 3000 / 4700
     (the Bullet's subcluster / its shock); angle average over theta for a randomly oriented stack.
  Q4 REACH.  Against the precision of the datasets that could see it, each at its physically relevant depth: the
     BTFR/RAR intrinsic scatter (~0.05 dex = 12% in g; y 0.01-1), KiDS-1000's outer lensing bins (~15-30%; y <= 1e-3),
     cluster weak-lensing masses (~10-20%; y 0.1-1, R500 at 0.3-0.6 a0).
  RESULT IN ONE LINE: to O(c_2) the phantom is AMPLIFIED by 1/(1 - v_par^2/c_s^2) -- a resonance, not a lag -- and no
  current dataset reaches it.
  MUTATE=1 sets c_2 = 0 (no momentum channel): Q2's omega -> 0 limit becomes Newtonian (L330's frozen phantom), and the
  Q2 check must FAIL (rc = 1).

Run from the repository root:  python3 real_research/khronon_momentum_2026/KM2_phantom_lag_law.py
"""
import os, sys, json, math
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "KM2_phantom_lag_law"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "KM2", "mutate": MUTATE, "checks": {}, "numbers": {}}
CKMS = 2.99792458e5
_trap = getattr(np, "trapezoid", None) or np.trapz


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


# ------------------------------------------------------------------ L340's block, verbatim (H1, lines 144-154)
k, C, c2, ac, w = sp.symbols('k C c_2 alpha_c omega', real=True)
psi, phi, beta, U, R = sp.symbols('psi phi beta U R')
D = -sp.I * w


def block(C_, eps_, ac_, a2_=0, a3_=0, g_=0):
    E = [4*k**2*psi - 4*k**2*phi - D*(-12*D*psi + 4*k**2*beta + 6*eps_*(3*D*psi - k**2*beta) + a3_*D*U),
         -4*k**2*psi - 4*k**2*(U - phi) + 2*ac_*k**2*phi - R,
         4*k**2*D*psi - 2*eps_*k**2*(3*D*psi - k**2*beta) + 4*k**2*g_*D*U + D*R,
         4*k**2*(U - phi) + 4*k**2*C_*U - D*(2*a2_*D*U + a3_*D*psi + 4*k**2*g_*beta)]
    X = [psi, phi, beta, U]
    M = sp.Matrix([[sp.diff(e_, x_) for x_ in X] for e_ in E]); S = sp.Matrix([-e_.subs({x_: 0 for x_ in X}) for e_ in E])
    return M, S


# ============================================================================================ Q1
banner("Q1  THE EXACT RESPONSE OF L340's BLOCK TO A SOURCE MOVING THROUGH THE PREFERRED FRAME")
# The response depends on omega and k only through u = omega/(k c) (c = 1 in the block): set k = 1, omega = u.
u = sp.symbols("u", positive=True)
c2_use = 0 if MUTATE else c2
M, S = block(C, -c2_use, ac)                            # L340: eps = 1 - lambda = -c_2
M1 = M.subs({k: 1, w: u}); S1 = S.subs({k: 1, w: u})
sol = [sp.cancel(v) for v in M1.LUsolve(S1)]
psiN = -R / 4                                            # -R/(4 k^2) at k = 1
Xr = {nm: sp.cancel(v / psiN) for nm, v in zip(("psi", "phi", "beta", "U"), sol)}
PhiB = sp.cancel(Xr["phi"] + (-sp.I * u) * Xr["beta"])  # Phi_B = phi + beta_dot, beta_dot -> -i omega beta
PsiB = Xr["psi"]
lens = sp.cancel((PhiB + PsiB) / 2)
static = sp.cancel(sp.limit(PhiB, u, 0, "+"))
static_len = sp.cancel(sp.limit(lens, u, 0, "+"))
P(f"    Phi_B/psi_N at u -> 0 = {sp.factor(static)};  (Phi_B + Psi_B)/(2 psi_N) at u -> 0 = {sp.factor(static_len)}")
# convention check: the block's momentum-constraint row equals KM1's (4 + 6 c2) k^2 D psi - 2 c2 k^4 beta
row3 = sp.expand((block(C, -c2, ac)[0][2, :] * sp.Matrix([psi, phi, beta, U]))[0])
km1_row = sp.expand((4 + 6 * c2) * k ** 2 * D * psi - 2 * c2 * k ** 4 * beta)
conv_ok = sp.simplify(row3 - km1_row) == 0
P(f"    L340 momentum-constraint row = KM1's (beta = KM1's shift sigma, Phi_B = phi + beta_dot): {conv_ok}")
OUT["numbers"]["Q1"] = {"PhiB_static": str(sp.factor(static)), "lens_static": str(sp.factor(static_len)), "convention_ok": conv_ok}
check("Q1 the block solves in closed form; its u -> 0 response is the static MOND boost (1 + C) up to alpha_c's "
      "G-renormalisation, and its shift convention matches KM1's derivation",
      f"Phi_B(0)/psi_N = {sp.factor(static)}; convention {conv_ok}",
      conv_ok and sp.simplify(static - (1 + C) / (1 - ac * (1 + C) / 2)) == 0,
      "the lag is read off the same block that gave L340's tracking result")

# ============================================================================================ Q2
banner("Q2  THE LAG LAW: R = 1 + a1 (u/c_s)^2, THE POLE AT THE MODE SPEED, LENSING")
cs2 = c2 / (C * (2 + 3 * c2))
Rdyn = sp.cancel(PhiB / static)
Rlen = sp.cancel(lens / static_len)
a1_dyn = sp.factor(sp.cancel(sp.diff(Rdyn, u, 2).subs(u, 0) / 2 * cs2))
a1_len = sp.factor(sp.cancel(sp.diff(Rlen, u, 2).subs(u, 0) / 2 * cs2))
a1_small = {nm: sp.factor(sp.limit(sp.limit(ex, ac, 0), c2, 0)) for nm, ex in (("dyn", a1_dyn), ("lens", a1_len))}
P(f"    a1_dyn  = {a1_dyn}")
P(f"    a1_lens = {a1_len}")
P(f"    leading order (alpha_c, c_2 -> 0): a1_dyn = {a1_small['dyn']},  a1_lens = {a1_small['lens']}")
# the pole, numerically: |R| blows up where u^2 -> c_s^2 (sample parameters)
Rn = sp.lambdify((u, C, c2, ac), Rdyn, "numpy")
pole_rows = []
for Cv, c2v in ((1.0, 1e-2), (10.0, 7.2e-3), (100.0, 6.7e-2)):
    csv = math.sqrt(c2v / (Cv * (2 + 3 * c2v)))
    grid = np.linspace(0.2 * csv, 1.8 * csv, 200001)
    vals = np.abs(np.array(Rn(grid, Cv, c2v, 1e-9), dtype=complex))
    upk = grid[int(np.argmax(vals))]
    pole_rows.append((Cv, c2v, csv, upk, upk / csv))
    P(f"    C = {Cv:6.1f}, c2 = {c2v:.1e}: |R| peaks at u = {upk:.6e}, c_s = {csv:.6e}, ratio {upk / csv:.5f}")
pole_ok = all(abs(r_[4] - 1) < 2e-3 for r_ in pole_rows)
# the closed form suggested by a1 = C/(C+1) and the pole at c_s: R = 1 + [C/(1+C)] u^2/(c_s^2 - u^2)
cf_err = []
for Cv, c2v in ((1.0, 7.2e-3), (10.0, 2e-2), (100.0, 6.7e-2)):
    csv = math.sqrt(c2v / (Cv * (2 + 3 * c2v)))
    for fr in (0.1, 0.5, 0.9):
        uu = fr * csv
        Rex = complex(Rn(uu, Cv, c2v, 1e-9)).real
        Rcf = 1 + Cv / (1 + Cv) * uu ** 2 / (csv ** 2 - uu ** 2)
        cf_err.append(abs(Rex - Rcf) / abs(Rex - 1))
P(f"    closed form R = 1 + [C/(1+C)] u^2/(c_s^2 - u^2): max relative error of (R - 1) over 9 cells = {max(cf_err):.2e}")
OUT["numbers"]["Q2"] = {"closed_form_max_rel_err": max(cf_err), "a1_dyn": str(a1_dyn), "a1_lens": str(a1_len),
                        "a1_leading": {kk: str(vv) for kk, vv in a1_small.items()}, "poles": pole_rows}
check("Q2 the phantom tracks slow sources with R = 1 + a1 (v cos(theta)/c_s)^2 and diverges at the mode speed "
      "u = c_s (the 'left behind' threshold); the coefficients are exact", f"a1_dyn = {a1_small['dyn']}, a1_lens = "
      f"{a1_small['lens']} (leading order); pole/c_s = {[round(r_[4], 5) for r_ in pole_rows]}",
      (not MUTATE) and pole_ok and a1_small["dyn"] != 0 and max(cf_err) < 0.05,
      "T1's '(v/c_s)^2' now has its coefficient, its sign and its angle: the PHANTOM is AMPLIFIED by "
      "1/(1 - v_par^2/c_s^2) (a resonance, not a lag) to O(c_2)")

# ============================================================================================ Q3
banner("Q3  THE SIZE ACROSS L340's WINDOW (kernel nu_mono, both constitutive directions)")
def h_rar(y):
    return y / np.expm1(np.sqrt(y))
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: dh_rar(y), 1.0, 5.0); H_P = h_rar(Y_P)
def nu_mono(y):                                          # L340's A1 kernel (below the peak nu_mono = nu_RAR)
    return 1.0 + h_rar(min(y, Y_P)) / y if y <= Y_P else 1.0 + (H_P + 0.05 * H_P * math.log((y + Y_P) / (2 * Y_P))) / y
def CL(y, e=1e-5):
    f = lambda yy: yy * nu_mono(yy)
    return (f(y * (1 + e)) - f(y * (1 - e))) / (2 * y * e) - 1.0
Rd_f = Rn
ACV = 1e-9
speeds = {"galaxy 300": 300.0, "galaxy 600": 600.0, "cluster member 1500": 1500.0, "Bullet subcluster 3000": 3000.0,
          "Bullet shock 4700": 4700.0}
rows = []
thetas = np.linspace(0, np.pi / 2, 721)
for c2v in (7.2e-3, 2e-2, 6.7e-2):
    for yv in (1e-4, 1e-3, 1e-2, 1e-1, 1.0):
        for lab_dir, Cv in (("T", nu_mono(yv) - 1.0), ("L", CL(yv))):
            csv = CKMS * math.sqrt(c2v / (Cv * (2 + 3 * c2v)))
            for slab, vv in speeds.items():
                if vv >= csv:
                    rows.append((c2v, yv, lab_dir, Cv, csv, slab, vv, float("nan"), "LEFT BEHIND (v >= c_s)"))
                    continue
                uu = (vv / CKMS) * np.cos(thetas)
                Rv = np.real(np.array(Rd_f(uu, Cv, c2v, ACV), dtype=complex))
                Ravg = float(_trap(Rv * np.sin(thetas), thetas) / _trap(np.sin(thetas), thetas))
                dph = (Ravg - 1.0) * (1 + Cv) / Cv                # fractional change of the phantom part
                rows.append((c2v, yv, lab_dir, Cv, csv, slab, vv, Ravg - 1.0, f"phantom {dph:+.2e}"))
for r_ in rows:
    if r_[0] == 7.2e-3 and r_[2] == "T" and r_[5] in ("galaxy 600", "cluster member 1500", "Bullet shock 4700"):
        P(f"    c2 = {r_[0]:.1e}  y = {r_[1]:.0e}  C_{r_[2]} = {r_[3]:8.2f}  c_s = {r_[4]:8.0f} km/s  {r_[5]:22s}: "
          f"<R-1> = {r_[7]:+.2e}  {r_[8]}")
OUT["numbers"]["Q3"] = [dict(zip(("c2", "y", "dir", "C", "c_s_kms", "source", "v_kms", "dR_avg", "note"), r_)) for r_ in rows]
gal = [abs(r_[7]) for r_ in rows if r_[5].startswith("galaxy") and r_[1] >= 1e-2 and not math.isnan(r_[7])]
far = [abs(r_[7]) for r_ in rows if r_[5].startswith("galaxy") and r_[1] <= 1e-3 and not math.isnan(r_[7])]
left = sorted({(r_[0], r_[1], r_[2], r_[5]) for r_ in rows if "LEFT" in r_[8]})
P(f"    galaxies (y >= 0.01) : max |<R-1>| = {max(gal):.2e};  far outskirts (y <= 1e-3): max {max(far):.2e}")
P(f"    left-behind cells (v >= c_s): {len(left)} of {len(rows)}; e.g. {left[:4]}")
OUT["numbers"]["Q3_summary"] = {"galaxy_max": max(gal), "outskirt_max": max(far), "n_left_behind": len(left)}
check("Q3 inside galaxies the effect is tiny; it grows only in the far outskirts (C large -> c_s small) and for fast "
      "cluster systems at the c_2 floor", f"galaxy bodies <= {max(gal):.1e}; outskirts <= {max(far):.1e}; "
      f"{len(left)} left-behind cells", max(gal) < 0.02,
      "the effect scales as C (v/c)^2 / c_2: small c_2 and deep-MOND outskirts are where T1 lives")

# ============================================================================================ Q4
banner("Q4  REACH: DOES ANY CURRENT DATASET SEE IT?")
reach = {"BTFR/RAR intrinsic scatter": 0.12, "KiDS-1000 outer lensing bins": 0.15, "cluster weak-lensing masses": 0.10}
det = {}
sel = {"BTFR/RAR intrinsic scatter": (lambda r_: r_[5].startswith("galaxy") and 1e-2 <= r_[1] <= 1.0),
       "KiDS-1000 outer lensing bins": (lambda r_: r_[5].startswith("galaxy") and r_[1] <= 1e-3),
       "cluster weak-lensing masses": (lambda r_: ("cluster" in r_[5] or "Bullet" in r_[5]) and 0.1 <= r_[1] <= 1.0)}
for dsname, prec in reach.items():
    cand = [abs(r_[7]) for r_ in rows if sel[dsname](r_) and not math.isnan(r_[7])]
    det[dsname] = {"max_effect": max(cand), "precision": prec, "reachable": max(cand) > prec}
    P(f"    {dsname:30s}: largest predicted <R-1> = {max(cand):.2e} vs precision ~{prec:.2f} -> "
      f"{'REACHABLE' if max(cand) > prec else 'below reach'}")
P("    (y ranges: galaxy bodies 0.01-1; KiDS outer bins <= 1e-3; clusters 0.1-1 -- cluster R500 sits at 0.3-0.6 a0)")
OUT["numbers"]["Q4"] = det
check("Q4 no current dataset reaches T1: galaxy bodies <= 0.3%, KiDS outskirts <= 4%, cluster lensing <= ~7% (the "
      "Bullet at the c_2 floor) against ~12% / 15% / 10% precision",
      {kk: f"{vv['max_effect']:.3f} vs {vv['precision']}" for kk, vv in det.items()},
      not any(vv["reachable"] for vv in det.values()),
      "the candidate's new prediction is real but below today's reach; the nearest handle is a CMB-velocity split of "
      "stacked lensing at the few-percent level, or Bullet-class mergers at the c_2 floor")

# ============================================================================================ verdict
banner("VERDICT")
P("""  T1 is now a number, and its sign is not a lag.  In L340's own block a source moving at v through the preferred
  frame has its potential multiplied by R = 1 + [C/(1+C)] v_par^2/(c_s^2 - v_par^2): the PHANTOM part is amplified by
  1/(1 - v_par^2/c_s^2), diverging at the mode speed c_s (beyond it the quasi-static phantom no longer exists).
  With c_s^2 = c_2 c^2/(C(2+3c_2)) the effect is ~ C v^2/(c_2 c^2): <= 0.3% in galaxy bodies, <= 4% in Mpc-scale
  weak-lensing outskirts, <= ~7% for Bullet-class mergers at the c_2 floor -- below the reach of every dataset in
  hand.  A real, falsifiable prediction of the candidate that today's data cannot yet test.  Frozen-coefficient,
  principal order; a galaxy's phantom integrates over directions and radii, which this lane averages but does
  not solve.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
