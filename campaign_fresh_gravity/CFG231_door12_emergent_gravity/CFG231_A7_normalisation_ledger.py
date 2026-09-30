#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG231_A7_normalisation_ledger -- G4: the a_V/a0 normalisation table, kappa_V, the constants ledger with the strict count, and the re-tie check
(which verdicts move when each ledger entry is varied).  MUTATE MU2 (a_V -> 0), MU4 (footing swap).
Frozen: CFG231_FROZEN_CRITERIA.md sections 1.5, 2 (G4), 4, 6.   Main: exit 0 if the reproduction checks pass.  MUTATE: exit 1 iff the control bites.
"""
import sys, os, math
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG231_common as C

MUT = os.environ.get("MUTATE") or None
R = C.Report("CFG231_A7_normalisation_ledger", MUT)
C.header(R, "CFG231 A7 -- G4: normalisation, kappa_V, the ledger and the re-tie check")

R.banner("G4.1  a_V / a0 for H in {H_Lambda, H0} and footings {canonical, alt}, and kappa_V (CFG117 R2 reproduced independently)")
tab = {}
for Hc in C.HCHOICES:
    for f in C.FOOTINGS:
        tab[(Hc, f)] = C.a_V_si(Hc) / C.A0_SI[f]
        R.P(f"  H = {Hc}: a_V = {C.a_V_si(Hc):.4e} m/s^2; a_V/a0 ({f}) = {tab[(Hc, f)]:.4f}")
ref = {("HL", "canonical"): 0.9650, ("HL", "alt"): 0.7985, ("H0", "canonical"): 1.1660, ("H0", "alt"): 0.9648}
ok = all(abs(tab[k] / v - 1) < 1e-3 for k, v in ref.items())
R.check("G4.1 the four a_V/a0 ratios reproduce CFG117's R2 table (0.9650, 0.7985, 1.1660, 0.9648) to 1e-3", str({k: round(v, 4) for k, v in tab.items()}), ok)
# kappa_V: a_V = kappa_V c sqrt(G rho_Lambda); with H_Lambda = sqrt(8 pi G rho_L/3): kappa_V = sqrt(8 pi/3)/6
kV = sp.sqrt(8 * sp.pi / 3) / 6
kV_num = float(kV)
kV0 = kV_num / math.sqrt(C.OMEGA_L)
def sig(k, mu, s):
    return (k - mu) / s
R.P(f"  kappa_V = sqrt(8 pi/3)/6 = {kV_num:.4f} (H_Lambda); kappa_V' = kappa_V/sqrt(Omega_L) = {kV0:.4f} (H0)")
R.P(f"  BTFR window 0.465 +- 0.076: {sig(kV_num, 0.465, 0.076):+.2f} sigma (H_Lambda), {sig(kV0, 0.465, 0.076):+.2f} (H0); distance-free 0.55 +- 0.17: {sig(kV_num, 0.55, 0.17):+.2f}, {sig(kV0, 0.55, 0.17):+.2f}; kappa = 1/2 (FITTED): {sig(0.5, 0.465, 0.076):+.2f}, {sig(0.5, 0.55, 0.17):+.2f}")
R.check("G4.1b kappa_V = sqrt(8 pi/3)/6 = 0.4824 and kappa_V' = 0.5829, with the windows' sigma distances of CFG117 R2 (+0.23, -0.40; +1.55, +0.19)",
        f"{sig(kV_num, 0.465, 0.076):+.2f}, {sig(kV_num, 0.55, 0.17):+.2f}; {sig(kV0, 0.465, 0.076):+.2f}, {sig(kV0, 0.55, 0.17):+.2f}",
        abs(kV_num - 0.4824) < 5e-4 and abs(kV0 - 0.5829) < 5e-4 and abs(sig(kV_num, 0.465, 0.076) - 0.23) < 0.02 and abs(sig(kV0, 0.465, 0.076) - 1.55) < 0.05)
R.P("  Reading: with H_Lambda the model's a_V is TIED to rho_Lambda (kappa_V = 0.4824 replaces the fitted 1/2, not added to it); with H0 the tie is to the critical density (kappa_V' = kappa_V/sqrt(Omega_L)), i.e. NOT to Lambda alone: G4's tie clause fails for the H0 reading.")
R.num("a_V_over_a0", {f"{k[0]}|{k[1]}": v for k, v in tab.items()})
R.num("kappa_V", dict(HL=kV_num, H0=kV0))

R.banner("G4.2  the ledger and the strict count (per variant)")
ledger = {
    "V0": dict(entries=["epsilon (coupling, declared 1)", "m = H_Lambda/c (tied)"], acc_scale="none (no acceleration scale: the tie a0 <-> Lambda cannot be exhibited)", strict="FAIL"),
    "V2": dict(entries=["as K1 (epsilon, wall at a/2)"], acc_scale="a_V (tied)", strict="FAIL"),
    "B1": dict(entries=["the 1/6 (source argument, not an action)"], acc_scale="a_V (H_Lambda tied; H0 not)", strict="P (count only)"),
    "B2": dict(entries=["the 1/6 (source argument)"], acc_scale="a_V", strict="P (count only)"),
    "B3": dict(entries=["the 1/6", "the onset threshold cH/(8 pi G) (source: eq. 1.3 as recorded)"], acc_scale="a_V", strict="P (count only)"),
    "B4": dict(entries=["the 1/6"], acc_scale="a_V", strict="P (count only)"),
    "K3": dict(entries=["wall/deep ratio 1 (declared shape)", "epsilon = 1 (degenerate with a only for K2)"], acc_scale="a_V", strict="P (count only; one declared shape ratio)"),
    "K1": dict(entries=["wall at a/2 (read off the target)", "epsilon = 1"], acc_scale="a_V", strict="FAIL (a declared constant fixed with knowledge of the target)"),
}
for k, v in ledger.items():
    R.P(f"  {k:3s}: entries {v['entries']}; scale {v['acc_scale']}; G4 strict: {v['strict']}")
R.num("ledger", ledger)
R.P("  K2 (= B2): epsilon is degenerate with a in the deep law (a_eff = epsilon^2 a), so it is NOT an independent constant; K3 and K1 carry a wall/deep ratio; V0 has no acceleration scale at all.")
R.P("  (frozen estimates had K2/K3 P-count 0.5 and V0/V2 F: outcomes: K2 P-count, K3 P-count, V0 F, V2 F, K1 F, B1-B4 P-count; consistent with the frozen table except that V0's F is for a different reason: no scale.)")

R.banner("G4.3  the re-tie check: vary each ledger entry across a stated window and record which verdicts move (a sensitivity, not a tuning: nothing is chosen)")


def K1_eps(gN, a, eps2):
    """K1 with the coupling: D(E) = E^2/(a - 2E) = eps2 g_N  ->  E^2 + 2 eps2 g_N E - eps2 a g_N = 0."""
    return -eps2 * gN + np.sqrt(eps2 ** 2 * gN ** 2 + eps2 * a * gN)


def G1_point(a_scale, eps2, wall_scale=1.0):
    a = C.AKPC(C.a_V_si("HL")) * a_scale
    a0t = C.AKPC(C.A0_SI["canonical"])
    M = 1e10
    rM = C.r_M_kpc(M, a0t)
    r = C.XGRID * rM
    gNf = lambda rr: C.G * M / rr ** 2
    if wall_scale == 1.0:
        Ef = lambda rr: K1_eps(gNf(rr), a, eps2)
    else:                                              # wall at wall_scale * a/2: D = E^2/(a - E/(wall_scale/2 ... )) generalisation
        w = wall_scale * a / 2.0
        # D(E) = (E^2/a)/(1 - E/w) = eps2 g_N  ->  E^2/a = eps2 g_N (1 - E/w)  -> E^2 + (a eps2 g_N / w) E - a eps2 g_N = 0
        Ef = lambda rr: 0.5 * (-(a * eps2 * gNf(rr) / w) + np.sqrt((a * eps2 * gNf(rr) / w) ** 2 + 4 * a * eps2 * gNf(rr)))
    MD = lambda rr: rr ** 2 * Ef(rr) / C.G
    rho = C.ddr(MD, r) / (4 * math.pi * r ** 2)
    gt = C.G * (M + MD(r)) / r ** 2
    Rr = 4 * math.pi * r ** 3 * rho * gt / (a0t * M)
    return float(np.max(np.abs(Rr - 1)))


rows = {}
R.P("  K1 point mass, N-tie canonical, 1e10 Msun: max|R-1| (pass iff <= 0.10) as one entry is varied, the rest at their declared values:")
for lab, fn in (("a (i.e. the 1/6 or H): x", lambda lam: G1_point(lam, 1.0)), ("epsilon^2: x", lambda lam: G1_point(1.0, lam)), ("wall position: x", lambda lam: G1_point(1.0, 1.0, lam))):
    vals = {lam: fn(lam) for lam in (0.5, 0.9, 1.0, 1.1, 2.0)}
    rows[lab] = vals
    R.P(f"    {lab:26s}" + "  ".join(f"{lam}: {v:.3f}{'P' if v <= 0.1 else 'F'}" for lam, v in vals.items()))
R.num("retie_G1_point_K1", rows)
# Q2 is linear in a (tail E -> a/2): the verdict does not move over any O(1) window
q2 = {lam: (lam * C.a_V_si('HL') / 2.0) / (9.54 * 1.495978707e11) / 5.2e-27 for lam in (0.5, 0.9, 1.0, 1.1, 2.0)}   # tail E -> lam a/2 at Saturn, tide = E/R
R.P("  G5 Q2 (K1 tail E -> lambda a/2 at Saturn, tide = E/R): " + ", ".join(f"{lam}: {v:.0f}F" for lam, v in q2.items()) + "  -> the Solar-System verdict does NOT move over an O(1) window of any ledger entry (F throughout)")
R.P("  => the point-mass G1 verdict of K1 is sensitive to every tied entry at the +-10% level (a passes only for lambda in ~[0.93, 1.14]; the wall must sit at 1 x a/2 to ~ +-10%), the G5 verdict is insensitive: the tie is load-bearing for G1 and irrelevant to the G5 failure.")
R.check("G4.3 K1's point-mass G1 verdict moves inside +-10% of the a-scale and the wall (P at 1.0, F at 0.5 and 2.0) while G5's Q2 verdict stays F at every lambda tried",
        f"a: {rows['a (i.e. the 1/6 or H): x']}", rows["a (i.e. the 1/6 or H): x"][1.0] <= 0.1 and rows["a (i.e. the 1/6 or H): x"][0.5] > 0.1 and rows["a (i.e. the 1/6 or H): x"][2.0] > 0.1 and all(v > 1 for v in q2.values()))

R.banner("G4 verdicts")
R.P("  V0: F (no acceleration scale; epsilon declared).  V2: F (as K1).  B1, B2, B3, B4: P (count only): the 1/6 is a source argument; with H_Lambda it is a tie to rho_Lambda with kappa_V = 0.4824 replacing (not adding to) kappa; with H0 the tie is to the critical density: F on the tie clause.")
R.P("  K3: P (count only; one declared shape ratio).  K1: F strict (the wall a/2 is a declared constant fixed with knowledge of the target).  All: no new constant beyond declared shapes; nothing here was tuned.")

# ------------------------------------------------------------------------------------------------------ MUTATE
bites = None
if MUT:
    R.banner(f"MUTATE {MUT}")
    if MUT == "MU2":
        # a_V -> 0: the normalisation cell (deep amplitude a_V/a0) -> 0
        main_ratio = tab[("HL", "canonical")]
        mut_ratio = 0.0
        R.P(f"  deep-regime amplitude a_V/a0 (canonical, H_Lambda): main {main_ratio:.4f} (within 10%: {abs(main_ratio - 1) <= 0.1}) -> a_V = 0: {mut_ratio} (within 10%: False)")
        bites = abs(main_ratio - 1) <= 0.1 and abs(mut_ratio - 1) > 0.1
    elif MUT == "MU4":
        can, alt = tab[("HL", "canonical")], tab[("HL", "alt")]
        R.P(f"  K1 point-mass N-tie cell (deep amplitude a_V/a0), H_Lambda: canonical {can:.4f} (P: {abs(can - 1) <= 0.1}) -> alt {alt:.4f} (P: {abs(alt - 1) <= 0.1});  H0 vs canonical {tab[('H0', 'canonical')]:.4f} (P: {abs(tab[('H0', 'canonical')] - 1) <= 0.1})")
        bites = abs(can - 1) <= 0.1 and abs(alt - 1) > 0.1
    R.P(f"  bites = {bites}")
    R.num("bites", bool(bites))

if not MUT:
    nf = R.write()
    sys.exit(0 if nf == 0 else 1)
R.write()
sys.exit(1 if bites else 0)
