#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG117 -- door 2 of the ten doors: Verlinde's emergent gravity mapped onto the CFG44 target.

Criteria FROZEN in ../CFG117_FROZEN_CRITERIA.md (committed before any script or number); the shared gates G1-G5 are in
../closure_map/TEN_DOORS_GATES_2026-09-29.md.  The menu of doors was written knowing the target.

THE MODEL.  Verlinde 2016 (arXiv:1611.02269; SciPost Phys. 2, 016 (2017)) gives the apparent dark mass of a spherical baryon
distribution,
        M_D^2(r) = (a_V r^2 / G) d(M_B(r) r)/dr ,        a_V = c H / 6
(eq. 4.49 at d = 4, Sigma_D^2 = (a_0/8 pi G) Sigma_B/(d-1); a_M = a_0/6, eq. 1.7; a_0 = c H_0, eq. 1.2).  H is carried both ways
(declared): H0 = 67.4 km/s/Mpc (Verlinde's text) and H_Lambda = H0 sqrt(Omega_Lambda), Omega_Lambda = 0.685.

THE TARGET.  CFG44 (Bcommon.target_fields, imported read-only):  C(r) = rho_c r^3 g_tot = (a0/4 pi) M_b(<r).
Verlinde's candidate:  rho_D = M_D'/(4 pi r^2),  g_tot = G (M_B + M_D)/r^2,  so  C_V = G M_D' (M_B + M_D) / (4 pi r).
G1 is scored with a0 = a_V (the shape, not the normalisation): x = r/r_M, r_M = sqrt(G M_b/a_V), x in [0.1, 30]; a point mass and
CFG44's exponential spheres at M_b = 1e9, 1e10, 1e11, 1e12 Msun with h = 2, 3, 4, 5 kpc (CFG44/CFG50's pairing); the same
constants at every mass.

CHECKS (frozen)
  C1 CONTROL   point mass, analytic: Verlinde gives M_D = M x, so C_V/C_T = (1 + x)/x at every x; reproduced to 1e-9 (1.033 at x = 30).
  C2 CONTROL   Bcommon's exponential-sphere target reproduces CFG44's committed C(r) = (a0/4 pi) M_b(<r), with the closed form
               M_b(<r) = M P(3, r/h), to 1e-9.
  H1 HEADLINE  G1 holds: C_V/C_T lies in [0.9, 1.1] over x in [0.1, 30] for every mass, both geometries (and both H choices).
REPORTED
  R1  the ratio curves: values at x = 0.1, 1, 3, 10, 30; the largest deviation; the x range within 10%; the split of the ratio into a
      density ratio rho_D/rho_c and a field ratio g_V/g_T (their product is the ratio).
  R2  the normalisation: a_V/a0 for both H choices and both footings; kappa_V = sqrt(8 pi/3)/6 (H_Lambda) and
      kappa_V' = kappa_V/sqrt(Omega_Lambda) (H0) against the fitted windows 0.465 +- 0.076 (BTFR) and 0.55 +- 0.17 (distance-free).
  R3  the gates G2-G5 as statements from the literature (arXiv abstract pages and HTML renderings read; nothing downloaded).

MUTATE=1 (frozen): Verlinde's M_D is replaced by the target's own cold mass -- for the point mass exactly M (sqrt(1 + x^2) - 1), the
frozen formula; for the exponential spheres the target's own cold mass w/G from Bcommon (the frozen formula is its point-mass case;
the README discloses this reading, and the literal formula's numbers are printed in the MUTATE run).  H1 must then pass.  C1 and C2
test the Verlinde and the target code paths and are not touched by the MUTATE.

Units kpc, km/s, Msun (Bcommon's).  kappa = 1/2 and Omega_c h^2 stay FITTED; nothing is fitted or scanned here.
"""
import os
import sys
import math

sys.dont_write_bytecode = True                                        # write nothing outside this lane (no __pycache__)
import numpy as np
from scipy.special import gammainc
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
CAMPAIGN = os.path.dirname(HERE)
sys.path.insert(0, CAMPAIGN)
sys.path.insert(0, os.path.join(CAMPAIGN, "CFG44_fluid_target"))
import CFG7_common as C7                                                          # Report; C7.C4 = CFG4_common (FP0's footings)
from Bcommon import G, KPC_M, C_KMS, exp_sphere, point_mass, target_fields       # the CFG44 target, read-only

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG117_verlinde", MUTATE)
P = R.P
C4 = C7.C4

# ------------------------------------------------------------------------------------------------ declared constants (frozen file)
H0 = 67.4                                                            # km/s/Mpc, Planck18 (declared)
OMEGA_L = 0.685                                                      # Planck18 (declared)
H_CHOICES = (("H0", H0), ("H_Lambda", H0 * math.sqrt(OMEGA_L)))
A0_FOOT_SI = {"canonical": float(C4.A0["canonical"]), "alt": float(C4.A0["alt"])}   # FP0: rho_Lambda 9.3603e-11, rho_total 1.1312e-10
MASSES = ((1e9, 2.0), (1e10, 3.0), (1e11, 4.0), (1e12, 5.0))        # (M_b [Msun], h [kpc]): CFG44/CFG50's pairing
GEOMS = ("point", "expsphere")
KAPPA_WINDOWS = (("BTFR", 0.465, 0.076), ("distance-free", 0.55, 0.17))   # the fitted kappa windows (CFG0 F3), rho_Lambda footing
X_LO, X_HI, N_G1 = 0.1, 30.0, 3001                                  # the G1 range and its nodes (log-uniform)
X_REPORT = (0.1, 1.0, 3.0, 10.0, 30.0)
TOL_G1, TOL_CTRL = 0.10, 1e-9
SI = 1e6 / KPC_M                                                     # (km/s)^2/kpc -> m/s^2

# the grid: N_G1 log-uniform nodes on [0.1, 30] (both ends exact), continued inward with the same step so the target's ODE starts at
# <= 1e-3 r_M, CFG44's default depth (the start's offset has decayed by (1e-2)^5 in w^2 by x = 0.1)
DLOG = math.log10(X_HI / X_LO) / (N_G1 - 1)
K_DEEP = int(math.ceil(math.log10(X_LO / 1e-3) / DLOG))
X_START = X_LO * 10.0 ** (-K_DEEP * DLOG)
N_ALL = N_G1 + K_DEEP


def a_V(H):
    """Verlinde's a_V = c H / 6 in (km/s)^2/kpc, H in km/s/Mpc."""
    return C_KMS * H / 1e3 / 6.0


def baryons(geom, M, h):
    """Bcommon's profile (for the target) and the closed forms M_B, dM_B/dr, d2M_B/dr2 of the same baryons (for Verlinde's side)."""
    if geom == "point":
        return (point_mass(M), lambda r: np.full_like(r, M), lambda r: np.zeros_like(r), lambda r: np.zeros_like(r))
    s = lambda r: r / h
    return (exp_sphere(M, h),
            lambda r: M * gammainc(3.0, s(r)),                                        # M P(3, s): CFG44's closed form
            lambda r: M * s(r) ** 2 * np.exp(-s(r)) / (2.0 * h),                      # 4 pi r^2 rho_b, rho_b = M e^{-s}/(8 pi h^3)
            lambda r: M * (2.0 * s(r) - s(r) ** 2) * np.exp(-s(r)) / (2.0 * h * h))


def verlinde_MD(r, aV, MB, dMB, d2MB):
    """M_D and dM_D/dr from M_D^2 = (a_V/G) Q, Q = r^2 d(M_B r)/dr = r^2 (M_B + r M_B')."""
    Q = r ** 2 * (MB(r) + r * dMB(r))
    dQ = 2.0 * r * MB(r) + 4.0 * r ** 2 * dMB(r) + r ** 3 * d2MB(r)
    MD = np.sqrt(aV * Q / G)
    return MD, (aV / G) * dQ / (2.0 * MD)


def C_of(r, MBr, MD, dMD):
    """C = rho_D r^3 g_tot with rho_D = M_D'/(4 pi r^2) and g_tot = G (M_B + M_D)/r^2."""
    return G * dMD * (MBr + MD) / (4.0 * math.pi * r)


def within_intervals(x, ratio, sp, tol=TOL_G1):
    """the sub-ranges of [x_0, x_-1] where |ratio - 1| <= tol (ends refined on the spline)."""
    lx = np.log(x)
    ok = np.abs(ratio - 1.0) <= tol
    out, i, n = [], 0, len(x)

    def edge(la, lb, r_out):
        bound = 1.0 + tol if r_out > 1.0 + tol else 1.0 - tol
        return math.exp(brentq(lambda l: float(sp(l)) - bound, la, lb, xtol=1e-14))

    while i < n:
        if not ok[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and ok[j + 1]:
            j += 1
        a = float(x[i]) if i == 0 else edge(lx[i - 1], lx[i], ratio[i - 1])
        b = float(x[j]) if j == n - 1 else edge(lx[j], lx[j + 1], ratio[j + 1])
        out.append([a, b])
        i = j + 1
    return out


def summarise(x, ratio, dens, gfr):
    lx = np.log(x)
    sp, spd, spg = CubicSpline(lx, ratio), CubicSpline(lx, dens), CubicSpline(lx, gfr)
    dev = np.abs(ratio - 1.0)
    i = int(np.argmax(dev))
    xs = np.geomspace(X_LO, X_HI, 31)
    return dict(at={f"{v:g}": float(sp(math.log(v))) for v in X_REPORT},
                split={f"{v:g}": [float(spd(math.log(v))), float(spg(math.log(v)))] for v in X_REPORT},
                max_dev=float(dev[i]), x_max_dev=float(x[i]), ratio_at_max_dev=float(ratio[i]),
                ratio_min=float(ratio.min()), x_ratio_min=float(x[int(np.argmin(ratio))]), ratio_max=float(ratio.max()),
                within10=within_intervals(x, ratio, sp), pass_G1=bool(dev.max() <= TOL_G1),
                curve=dict(x=xs.tolist(), ratio=sp(np.log(xs)).tolist()))


def run_case(geom, M, h, H):
    aV = a_V(H)
    prof, MB, dMB, d2MB = baryons(geom, M, h)
    rM = math.sqrt(G * M / aV)
    f = target_fields(prof, r0=X_START * rM, r1=X_HI * rM, n=N_ALL, a0=aV)            # the CFG44 target with a0 = a_V
    k = slice(K_DEEP, None)
    r = f["r"][k]
    x = r / rM
    assert abs(x[0] / X_LO - 1) < 1e-12 and abs(x[-1] / X_HI - 1) < 1e-12 and len(x) == N_G1
    rho_T, g_T, w_T, uN = f["rho"][k], f["g"][k], f["w"][k], f["uN"][k]
    CT = rho_T * r ** 3 * g_T                                                           # the target's C(r) from Bcommon
    MBr = MB(r)
    cand = {}
    MD, dMD = verlinde_MD(r, aV, MB, dMB, d2MB)                                         # Verlinde
    cand["verlinde"] = (MD, dMD)
    sq = np.sqrt(1.0 + x * x)
    if geom == "point":                                                                 # the target's own cold mass (MUTATE)
        cand["target_cold"] = (M * (sq - 1.0), M * x / (rM * sq))
    else:
        cand["target_cold"] = (w_T / G, 4.0 * math.pi * r ** 2 * rho_T)
    cand["literal_pm"] = (M * (sq - 1.0), M * x / (rM * sq))                            # the frozen formula taken literally
    out = dict(aV=aV, rM=rM, x=x, r=r, CT=CT, MBr=MBr, uN=uN, rho_T=rho_T, g_T=g_T, prof=prof, dMB=dMB)
    for key, (md, dmd) in cand.items():
        ratio = C_of(r, MBr, md, dmd) / CT
        dens = dmd / (4.0 * math.pi * r ** 2 * rho_T)                                   # rho_candidate / rho_c
        gfr = G * (MBr + md) / (g_T * r ** 2)                                           # g_candidate / g_T
        out[key] = dict(ratio=ratio, dens=dens, gfr=gfr)
    # Verlinde's own onset criterion (eq. 1.3): dark phenomena where Sigma = M_B(<r)/(4 pi r^2) < a_0/(8 pi G), a_0 = c H = 6 a_V
    Sig = MBr / (4.0 * math.pi * r ** 2)
    above = Sig >= 6.0 * aV / (8.0 * math.pi * G)
    out["sigma_above_x"] = [float(x[above].min()), float(x[above].max())] if above.any() else None
    return out


# =============================================================================================================== run
P("CFG117 -- door 2: Verlinde's emergent gravity mapped onto the CFG44 target" + ("   [MUTATE=1]" if MUTATE else ""))
P(f"  declared: H0 = {H0} km/s/Mpc, Omega_Lambda = {OMEGA_L}; footings (FP0): canonical {A0_FOOT_SI['canonical']:.6e}, alt {A0_FOOT_SI['alt']:.6e} m/s^2")
for hn, H in H_CHOICES:
    P(f"  a_V = c H/6 with {hn:8s} = {H:8.4f} km/s/Mpc:  {a_V(H):9.3f} (km/s)^2/kpc = {a_V(H) * SI:.5e} m/s^2")
P(f"  grid: {N_G1} log-uniform nodes on x in [{X_LO}, {X_HI}] (step {DLOG:.3e} dex), the target's ODE started at x = {X_START:.4e} ({K_DEEP} extra nodes)")
if MUTATE:
    P("\n  *** MUTATE=1: M_D is replaced by the target's own cold mass (point mass: M(sqrt(1+x^2) - 1); exponential spheres: Bcommon's w/G).")
    P("      H1 must pass.  C1 and C2 keep testing the Verlinde and target code paths. ***")

CASES = {}
for hn, H in H_CHOICES:
    for geom in GEOMS:
        for M, h in MASSES:
            CASES[(geom, M, hn)] = run_case(geom, M, h, H)
EVAL = "target_cold" if MUTATE else "verlinde"

# ------------------------------------------------------------------------------------------------ C1
R.banner("C1  CONTROL: point mass, Verlinde's M_D = M x, so C_V/C_T = (1 + x)/x (the Verlinde code path, untouched by the MUTATE)")
c1 = 0.0
for (geom, M, hn), c in CASES.items():
    if geom != "point":
        continue
    x = c["x"]
    c1 = max(c1, float(np.max(np.abs(c["verlinde"]["ratio"] / ((1.0 + x) / x) - 1.0))))
    MDv = verlinde_MD(c["r"], c["aV"], lambda r: np.full_like(r, M), lambda r: np.zeros_like(r), lambda r: np.zeros_like(r))[0]
    c1 = max(c1, float(np.max(np.abs(MDv / (M * x) - 1.0))))
pm = CASES[("point", 1e10, "H0")]
R.check("C1 CONTROL (point mass, analytic): M_D = M x and C_V/C_T = (1 + x)/x at every node, all four masses, both H, to 1e-9",
        f"max relative deviation {c1:.2e}; C_V/C_T at x = 30: {pm['verlinde']['ratio'][-1]:.6f} (31/30 = {31 / 30:.6f})", c1 < TOL_CTRL)
R.num("C1_max_dev", c1)

# ------------------------------------------------------------------------------------------------ C2
R.banner("C2  CONTROL: Bcommon's exponential-sphere target against CFG44's committed C(r) = (a0/4 pi) M_b(<r), M_b = M P(3, r/h)")
c2, c2_id, mb_dev, rho_dev = 0.0, 0.0, 0.0, 0.0
for (geom, M, hn), c in CASES.items():
    if geom != "expsphere":
        continue
    h = dict(MASSES)[M]
    Mclosed = M * gammainc(3.0, c["r"] / h)
    c2 = max(c2, float(np.max(np.abs(c["CT"] / (c["aV"] / (4 * math.pi) * Mclosed) - 1.0))))
    c2_id = max(c2_id, float(np.max(np.abs(c["CT"] / (c["aV"] / (4 * math.pi) * c["uN"] / G) - 1.0))))
    mb_dev = max(mb_dev, float(np.max(np.abs(c["MBr"] / (c["uN"] / G) - 1.0))))
    rho_dev = max(rho_dev, float(np.max(np.abs(c["dMB"](c["r"]) / (4 * math.pi * c["r"] ** 2 * c["prof"].rho_b(c["r"])) - 1.0))))
R.check("C2 CONTROL: Bcommon's target rho_c r^3 g_tot equals (a0/4 pi) M P(3, r/h) to 1e-9 over x in [0.1, 30], all four masses, both H",
        f"max relative deviation {c2:.2e} (against the profile's own interpolated M_b(<r): {c2_id:.1e}, the algebraic identity)", c2 < TOL_CTRL)
R.check("C2b Verlinde's side uses the same baryons: its closed-form M_b(<r) and 4 pi r^2 rho_b equal Bcommon's profile",
        f"M_b(<r): max relative deviation {mb_dev:.2e} (Bcommon's PCHIP interpolant); rho_b: {rho_dev:.1e}", mb_dev < TOL_CTRL and rho_dev < 1e-12,
        load_bearing=False)
R.num("C2", dict(max_dev_closed_form=c2, max_dev_identity=c2_id, verlinde_side_MB_dev=mb_dev, verlinde_side_rho_dev=rho_dev))

# ------------------------------------------------------------------------------------------------ R1 + H1
R.banner(f"R1  THE RATIO C_cand/C_target  (candidate: {'the target' + chr(39) + 's own cold mass [MUTATE]' if MUTATE else 'Verlinde'}; a0 = a_V in the target)")
SUMM = {}
for (geom, M, hn), c in CASES.items():
    e = c[EVAL]
    SUMM[(geom, M, hn)] = summarise(c["x"], e["ratio"], e["dens"], e["gfr"])


def fmt_int(iv):
    return ", ".join(f"[{a:.3f}, {b:.3f}]" for a, b in iv) if iv else "none"


for hn, H in H_CHOICES:
    P(f"\n  {hn} (a_V = {a_V(H) * SI:.4e} m/s^2)")
    P(f"    {'geometry':10s} {'M_b':>6s} {'r_M kpc':>8s} | ratio at x = 0.1      1       3      10      30 | largest |dev| (x) | x range within 10%")
    for geom in GEOMS:
        for M, h in MASSES:
            s = SUMM[(geom, M, hn)]
            c = CASES[(geom, M, hn)]
            a = s["at"]
            P(f"    {geom:10s} {M:6.0e} {c['rM']:8.3f} | {a['0.1']:13.4f} {a['1']:7.4f} {a['3']:7.4f} {a['10']:7.4f} {a['30']:7.4f} | "
              f"{s['max_dev']:8.4g} ({s['x_max_dev']:.3f}) | {fmt_int(s['within10'])}")
P("\n  the split of the ratio at x = 0.1, 1, 3, 10, 30 into rho_cand/rho_c x g_cand/g_T (H0; the H_Lambda split is in the JSON):")
for geom in GEOMS:
    for M, h in MASSES:
        sp_ = SUMM[(geom, M, "H0")]["split"]
        P(f"    {geom:10s} {M:6.0e}  " + "   ".join(f"x={k}: {v[0]:.3f} x {v[1]:.3f}" for k, v in sp_.items()))
if not MUTATE:
    P("\n  Verlinde's onset criterion (eq. 1.3: dark phenomena where M_B(<r)/(4 pi r^2) < a_0/(8 pi G), a_0 = 6 a_V):"
      "\n    the x range with the baryon surface density ABOVE the threshold, i.e. where eq. 1.3 says the dark force is not yet at work (H0):")
    for geom in GEOMS:
        for M, h in MASSES:
            v = CASES[(geom, M, "H0")]["sigma_above_x"]
            P(f"    {geom:10s} {M:6.0e}  " + ("none in [0.1, 30]" if v is None else f"x in [{v[0]:.3f}, {v[1]:.3f}]"))
    P(f"    point mass analytically: x < 1/sqrt(3) = {1 / math.sqrt(3):.4f}, where Verlinde's ratio is {(1 + 1 / math.sqrt(3)) * math.sqrt(3):.4f};"
      " the ratio stays above 1.1 for all 1/sqrt(3) < x < 10")

n_pass = sum(s["pass_G1"] for s in SUMM.values())
worst = max(SUMM.items(), key=lambda kv: kv[1]["max_dev"])
h1 = n_pass == len(SUMM)
R.check("H1 [HEADLINE] G1: C_cand/C_target in [0.9, 1.1] over x in [0.1, 30] for every mass (1e9-1e12), both geometries and both H choices"
        + ("  [MUTATE: the target's own cold mass]" if MUTATE else ""),
        f"{n_pass}/{len(SUMM)} cases within 10%; worst: {worst[0][0]} M_b = {worst[0][1]:.0e} ({worst[0][2]}), |ratio - 1| = {worst[1]['max_dev']:.4g} "
        f"at x = {worst[1]['x_max_dev']:.3f} (ratio {worst[1]['ratio_at_max_dev']:.6g})", h1)

if MUTATE:
    lit = {k: float(np.max(np.abs(c["literal_pm"]["ratio"] - 1.0))) for k, c in CASES.items() if k[0] == "expsphere"}
    wk = max(lit, key=lit.get)
    xs_ = CASES[wk]["x"][int(np.argmax(np.abs(CASES[wk]["literal_pm"]["ratio"] - 1.0)))]
    pm_lit = max(float(np.max(np.abs(c["literal_pm"]["ratio"] - 1.0))) for k, c in CASES.items() if k[0] == "point")
    R.check("MUTATE-literal: the frozen formula M_b,tot (sqrt(1 + x^2) - 1) taken literally is the target's cold mass only for the point "
            "mass; on the exponential spheres it is not, and its ratio is not 1",
            f"point mass max |ratio - 1| = {pm_lit:.1e}; exponential spheres max |ratio - 1| = {lit[wk]:.3e} ({wk[0]} M_b = {wk[1]:.0e}, {wk[2]}, x = {xs_:.3f}); "
            + "; ".join(f"{k[1]:.0e}/{k[2]}: {v:.3g}" for k, v in lit.items()),
            all(v <= TOL_G1 for v in lit.values()), load_bearing=False)
    R.num("MUTATE_literal_expsphere_max_dev", {f"{k[1]:.0e}|{k[2]}": v for k, v in lit.items()})

R.num("R1", {f"{g}|{M:.0e}|{hn}": dict(r_M_kpc=CASES[(g, M, hn)]["rM"], **{k: v for k, v in s.items()})
             for (g, M, hn), s in SUMM.items()})

# ------------------------------------------------------------------------------------------------ R2
R.banner("R2  THE NORMALISATION: a_V/a0 and the kappa mapping (a0 = kappa c sqrt(G rho_Lambda))")
kV = math.sqrt(8.0 * math.pi / 3.0) / 6.0
kVp = kV / math.sqrt(OMEGA_L)
c_sqrt_G_rhoL = C4.C_SI * math.sqrt(C4.G_SI * C4.RHO_LAMBDA)                      # FP0's rho_Lambda: = 2 x a0_canonical (kappa = 1/2)
r2 = dict(kappa_V=kV, kappa_V_prime=kVp, a_V={}, a_V_over_a0={}, pulls={}, kappa_V_numeric_FP0=None)
for hn, H in H_CHOICES:
    aSI = a_V(H) * SI
    r2["a_V"][hn] = aSI
    for foot, a0 in A0_FOOT_SI.items():
        r2["a_V_over_a0"][f"{hn}|{foot}"] = aSI / a0
    P(f"  {hn:8s}: a_V = {aSI:.5e} m/s^2;  a_V/a0 = {aSI / A0_FOOT_SI['canonical']:.4f} (canonical, rho_Lambda)   {aSI / A0_FOOT_SI['alt']:.4f} (alt, rho_total)")
kV_num = r2["a_V"]["H_Lambda"] / c_sqrt_G_rhoL
H_L_FP0 = float(C4.A0["canonical"]) * C4.Z_FRAME / C4.C_SI * C4.MPC / 1e3     # FP0's H_Lambda (a0 = c H_Lambda / Z) in km/s/Mpc
r2["kappa_V_numeric_FP0"] = kV_num
r2["H_Lambda_FP0_kms_Mpc"] = H_L_FP0
P(f"\n  kappa_V  = sqrt(8 pi/3)/6            = {kV:.5f}   (H_Lambda; with FP0's rho_Lambda numerically {kV_num:.5f}: FP0's H_Lambda is "
  f"{H_L_FP0:.3f} km/s/Mpc against the declared {H_CHOICES[1][1]:.3f})")
P(f"  kappa_V' = sqrt(8 pi/3)/(6 sqrt(Omega_L)) = {kVp:.5f}   (H0)")
P(f"  kappa_V / (1/2) = Z/6 = {kV / 0.5:.5f}  (Z = cH_Lambda/a0 = {C4.Z_FRAME:.4f} for kappa = 1/2; Verlinde's 6 sits where the framework's Z sits)")
for name, mu, sg in KAPPA_WINDOWS:
    pv, pvp = (kV - mu) / sg, (kVp - mu) / sg
    r2["pulls"][name] = dict(window=[mu, sg], kappa_V=pv, kappa_V_prime=pvp, kappa_half=(0.5 - mu) / sg)
    P(f"  window {name:14s} {mu:.3f} +- {sg:.3f}:  kappa_V {pv:+.2f} sigma   kappa_V' {pvp:+.2f} sigma   (kappa = 1/2: {(0.5 - mu) / sg:+.2f} sigma)")
P("  (the windows are on the rho_Lambda footing at Planck's H0; the large-x limit of C_V/C_T with the target at its own footing a0 is a_V/a0)")
R.num("R2", r2)

# ------------------------------------------------------------------------------------------------ R3
R.banner("R3  GATES G2-G5 AS STATEMENTS (no computation; arXiv abstract pages and HTML renderings read on 2026-09-29, nothing downloaded)")
SOURCES = {
    "V16": "Verlinde 2016, arXiv:1611.02269, SciPost Phys. 2, 016 (2017): abstract page and the arXiv / ar5iv HTML rendering",
    "HFB17": "Hees, Famaey & Bertone 2017, arXiv:1702.04358, Phys. Rev. D 95, 064019: abstract page",
    "LMS17": "Lelli, McGaugh & Schombert 2017, arXiv:1702.04355, MNRAS Letters: abstract page",
    "B17": "Brouwer et al. 2017, arXiv:1612.03034, MNRAS 466, 2547: abstract page",
    "H17": "Hossenfelder 2017, arXiv:1703.01415, Phys. Rev. D 95, 124018: abstract page",
}
g1_mark = ("PASS" if h1 else "FAIL") + (" [MUTATE substitution, not Verlinde]" if MUTATE else "")
GATES = [
    dict(gate="G1 target", mark=g1_mark, sources=["this lane, H1"],
         reason=("MUTATE run: the G1 evaluator fed the target's own cold mass; Verlinde's G1 verdict is the main run's" if MUTATE
                 else "computed here (H1); the point mass gives C_V/C_T = (1 + x)/x")),
    dict(gate="G2 CMB and growth", mark="UNDEFINED", sources=["V16", "H17"],
         reason="no cosmological perturbation equations: the abstract claims evidence in galaxies and clusters only, none appear in the HTML "
                "as read, and with no action there is nothing to perturb",
         caveat="the fetched HTML did not reach Section 8.2 (cosmological scenarios; title from the table of contents): confirm against the full text"),
    dict(gate="G3 reciprocity and energy", mark="UNDEFINED", sources=["V16", "H17"],
         reason="the apparent dark mass comes from an elasticity correspondence with no Lagrangian or action, so the reaction on the baryons and the "
                "energy supplied are not defined; Hossenfelder's covariant Lagrangian (a vector field that couples to baryons and drags on them, with "
                "correction terms to the non-covariant formula) would define them but is not tested here"),
    dict(gate="G4 constants", mark="PASS (count only)", sources=["V16"],
         reason="the 1/6 is derived in the paper, 1/(2(d-1)) at d = 4 (eq. 4.49; the (d-1) from the relative normalisation of horizon area and "
                "volume, sec. 2.2; a_M = a_0/6, eq. 1.7): no fitted constant, and it replaces kappa (kappa_V = 0.482 with H_Lambda, 0.583 with H0) "
                "rather than adding one",
         caveat="derived in an argument, not an action, so the gate's 'tied in the same action' clause cannot be checked; eq. 1.2 sets a_0 = cH_0 = c^2/L "
                "with L the Hubble scale, a tie to the total density; a tie to Lambda alone needs the H_Lambda reading"),
    dict(gate="G5 well-posedness and Solar System", mark="FAIL", sources=["V16", "HFB17", "H17"],
         reason="no action and no time-dependent covariant field equations, so ghosts, gradient stability and causality are UNDEFINED; the Solar "
                "System clause fails: applied where it should hold a priori (spherical symmetry, outside the bulk of matter) the weak-field formula "
                "misses the planets' perihelion advances by seven orders of magnitude and is ruled out with high confidence (Hees et al.)",
         context="not a gate: Lelli et al. find EG equivalent to MOND for a point mass but not for finite galaxies (differences in the inner regions), "
                 "consistent with the RAR only with substantially lowered stellar M/L, and predicting a radius-correlated RAR residual that is not "
                 "observed; Hees et al. find marginally acceptable rotation-curve fits with low distances, M/L and H0, and wiggles from the "
                 "derivative term; Brouwer et al. find the parameter-free EG prediction in good agreement with KiDS/GAMA lensing around isolated "
                 "central galaxies"),
]
for g in GATES:
    P(f"  {g['gate']:36s} {g['mark']}")
    P(f"      reason : {g['reason']}")
    for key in ("caveat", "context"):
        if key in g:
            P(f"      {key:7s}: {g[key]}")
    P(f"      sources: {'; '.join(g['sources'])}")
P("\n  sources:")
for k, v in SOURCES.items():
    P(f"    {k:6s} {v}")
R.num("R3", dict(gates=GATES, sources=SOURCES))

# ------------------------------------------------------------------------------------------------ reading
R.banner("READING")
if not MUTATE:
    pmv = SUMM[("point", 1e10, "H0")]
    P(f"  H1 {'PASSES' if h1 else 'FAILS'}: {n_pass}/{len(SUMM)} cases lie within 10% of the target over x in [0.1, 30].")
    P(f"  Point mass: C_V/C_T = (1 + x)/x = {pmv['at']['0.1']:.3f}, {pmv['at']['1']:.3f}, {pmv['at']['3']:.4f}, {pmv['at']['10']:.4f}, "
      f"{pmv['at']['30']:.4f} at x = 0.1, 1, 3, 10, 30; within 10% only on {fmt_int(pmv['within10'])}.")
    P("  Why: Verlinde's M_D = M x at every radius (an r^-2 dark density all the way in; g = g_N + sqrt(a_V g_N), a linear sum), while the")
    P("  target's cold mass is M (sqrt(1 + x^2) - 1) (an r^-1 density inside r_M; g = sqrt(g_N^2 + a0 g_N)).  They share only the deep limit,")
    P("  approached as 1/x.  The density ratio sqrt(1 + x^2)/x carries the small-x failure; the field ratio (1 + x)/sqrt(1 + x^2) (max sqrt 2 at x = 1)")
    P("  carries the large-x tail.")
    P(f"  Normalisation: kappa_V = {kV:.3f} (H_Lambda) and {kVp:.3f} (H0) both lie within 2 sigma of both fitted windows.")
    P("  G2 UNDEFINED, G3 UNDEFINED, G4 PASS (count only), G5 FAIL (Solar System, Hees et al. 2017).  A scoped no-go on G1.")
else:
    P(f"  MUTATE: with the target's own cold mass in place of Verlinde's M_D, H1 {'PASSES' if h1 else 'FAILS'} ({n_pass}/{len(SUMM)} cases); "
      f"largest |ratio - 1| = {worst[1]['max_dev']:.1e}.  The G1 evaluator can pass.")
P("\n  kappa = 1/2 and Omega_c h^2 stay FITTED.  Nothing here says the data favour either model, or that the theory is closed.")

nf = R.write(here=HERE)
sys.exit(1 if nf else 0)
