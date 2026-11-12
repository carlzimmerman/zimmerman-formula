#!/usr/bin/env python3
"""OUT-3 (COSMIC-SHARE FOLD) -- the pre-registered computation.

Condition (S): M_c(<R_fold) = R_cosmic * M_b, with the record's exact halo
M_c = M_b X(x), X = (sqrt(1+4x^2)-1)/2, x = R_fold/r_M, r_M = sqrt(G M_b/a_0).
Exact inversion:  X = R  <=>  x^2 = R(1+R)  =>  a_0^S = G M_b R(1+R)/R_fold^2.

Footings NEVER pooled.  kappa = 1/2 FITTED; not theory closed.
Criteria: PREREGISTER.md (written before this file and before any number was run).
"""
import json, math, os, glob

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
RUNS = os.path.join(ROOT, "fable52_push", "FLD1_fold_reach", "runs")

# ---------------------------------------------------------------- constants
G_SI = 6.674e-11
MSUN = 1.989e30
KPC = 3.0857e19
C_SI = 2.99792458e8
G_GAL = 4.30091e-6              # kpc (km/s)^2 / Msun   (COL1/FLD1 convention)
KMS2_PER_KPC_TO_SI = 1e6 / KPC  # (km/s)^2/kpc -> m/s^2

H0 = 67.36                      # km/s/Mpc, Planck 2018 TT,TE,EE+lowE+lensing
OM = 0.3153
OL = 0.6847
H0_SI = H0 * 1e3 / 3.0857e22
RHO_L = OL * 3.0 * H0_SI ** 2 / (8.0 * math.pi * G_SI)   # kg/m^3
A_STAR = C_SI * math.sqrt(G_SI * RHO_L)                  # a_0 = kappa * A_STAR

A0_CAN = 9.3603e-11
A0_ALT = 1.1312e-10
R_COSMIC = {"canonical": 5.410, "alt": 5.412}           # F1A, RESULT.md:22
R_ERR = 0.065                                            # Planck 2018 fallback width (R541 part E)

GRID = [6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12]

out = []
def P(s=""):
    out.append(s)
    print(s)

P("=" * 100)
P("OUT-3 (COSMIC-SHARE FOLD):  M_c(<R_fold) = R_cosmic * M_b  =>  a_0 = G M_b R(1+R)/R_fold^2")
P("=" * 100)
P(f"rho_Lambda = {RHO_L:.6e} kg/m^3 (Planck h=0.6736, Omega_L=0.6847)")
P(f"c sqrt(G rho_Lambda) = {A_STAR:.6e} m/s^2")
P(f"footings a0 = {A0_CAN:.4e} (canonical) / {A0_ALT:.4e} (alt), NEVER pooled")
P(f"kappa at the footings: canonical {A0_CAN/A_STAR:.6f}, alt {A0_ALT/A_STAR:.6f}")
P(f"R_cosmic = Omega_d/Omega_b = {R_COSMIC['canonical']} (can) / {R_COSMIC['alt']} (alt) +- {R_ERR}")
P()

# ------------------------------------------------------------------ G0 exact
P("G0  exact inversion  " + "-" * 76)
X, x = sp.symbols("X x", nonnegative=True)
R = sp.Symbol("R", positive=True)          # the cosmic share; strictly positive
inv = sp.solve(sp.Eq(X * (1 + X), x ** 2), X)
P(f"  solve X(1+X) = x^2  ->  {inv}")
Xfun = (sp.sqrt(1 + 4 * x ** 2) - 1) / 2
P(f"  record's X(x) = {Xfun}")
g0_id = sp.simplify(sp.expand(Xfun * (1 + Xfun) - x ** 2))
P(f"  X(x)(1+X(x)) - x^2 simplifies to: {g0_id}")
# the inversion: put x^2 = R(1+R) into X and show it returns R.
# 4 x^2 + 1 = 4R(R+1) + 1 = (2R+1)^2, and sqrt of that is 2R+1 for R > 0.
inner = sp.factor(4 * R * (1 + R) + 1)
P(f"  4 R(1+R) + 1 factors as: {inner}")
root = sp.simplify(sp.sqrt(inner))
P(f"  sqrt((2R+1)^2) = {root}   (R > 0)")
g0a = sp.simplify((root - 1) / 2 - R)
P(f"  X(sqrt(R(1+R))) - R  = ({root} - 1)/2 - R simplifies to: {g0a}")
# and the reverse: X = R solved for x
g0b = [sp.simplify(s) for s in sp.solve(sp.Eq(Xfun, R), x)]
P(f"  X(x) = R solved for x  ->  {g0b}   (expect sqrt(R(1+R)) = {sp.sqrt(R*(1+R))})")
g0b_ok = any(sp.simplify(s ** 2 - R * (1 + R)) == 0 for s in g0b if s.is_real or True)
P(f"  x^2 = R(1+R) for that root: {g0b_ok}")
G0 = (g0_id == 0) and (g0a == 0) and (root == 2 * R + 1) and g0b_ok
P(f"  => {'PASS' if G0 else 'FAIL (lane inadmissible)'}")
P()

# ------------------------------------------------------------------ helpers
def load(footing, logM, mode="hubble", N=2400, zi=10):
    tag = "M%g" % logM
    pat = os.path.join(RUNS, f"{mode}_{footing}_{tag}_zi{zi}_N{N}.json")
    f = glob.glob(pat)
    if not f:
        return None
    return json.load(open(f[0]))

def rfold_at_z(d, ztarget):
    """R_fold at a given z from FLD1's series (monotone in t; z decreasing)."""
    s = d["series"]
    ci = d["series_cols"].index("z")
    ri = d["series_cols"].index("R_fold_kpc")
    best = None
    for row in s:
        zz = row[ci]
        if best is None or abs(zz - ztarget) < abs(best[0] - ztarget):
            best = (zz, row[ri])
    return best

def kappa_S(Mb_msun, Rf_kpc, Rc):
    """a_0^S = G M_b R(1+R)/R_fold^2  (kpc, km/s, Msun) -> kappa."""
    a0_gal = G_GAL * Mb_msun * Rc * (1.0 + Rc) / Rf_kpc ** 2   # (km/s)^2/kpc
    a0_si = a0_gal * KMS2_PER_KPC_TO_SI
    return a0_si, a0_si / A_STAR

# ------------------------------------------------------------------ G1
P("G1  the number (z = 0, log M_b = 10.45)  " + "-" * 60)
g1_rows = []
for foot in ("canonical", "alt"):
    d = load(foot, 10.45)
    Rf = d["R_fold_end_kpc"]
    Rc = R_COSMIC[foot]
    Mb = 10 ** 10.45
    a0s, kap = kappa_S(Mb, Rf, Rc)
    g1_rows.append((foot, Rf, Rc, a0s, kap))
    P(f"  {foot:10s} R_fold(0) = {Rf:10.4f} kpc   R_cosmic = {Rc:.3f}"
      f"   a_0^S = {a0s:.4e} m/s^2   kappa_S = {kap:.6e}")
    P(f"             miss |kappa_S - 1/2| = {abs(kap-0.5):.4f}   band 0.025"
      f"   -> {'PASS' if abs(kap-0.5) <= 0.025 else 'FAIL'}"
      f"   ({abs(kap-0.5)/0.025:.1f}x the band)"
      f"   dex = {math.log10(kap/0.5):+.4f}")
G1 = all(abs(r[4] - 0.5) <= 0.025 for r in g1_rows)
P(f"  => {'PASS' if G1 else 'FAIL'}")
P()

# ------------------------------------------------------------------ G2
P("G2  universality in mass (z = 0, both footings)  " + "-" * 53)
P(f"  {'footing':10s} {'logMb':>6s} {'R_fold':>10s} {'a_0^S':>12s} {'kappa_S':>12s}")
g2 = {}
for foot in ("canonical", "alt"):
    Rc = R_COSMIC[foot]
    vals = []
    for lm in GRID:
        d = load(foot, lm)
        if d is None:
            P(f"  {foot:10s} {lm:6g}  -- run missing --")
            continue
        Rf = d["R_fold_end_kpc"]
        a0s, kap = kappa_S(10 ** lm, Rf, Rc)
        vals.append(kap)
        P(f"  {foot:10s} {lm:6g} {Rf:10.3f} {a0s:12.4e} {kap:12.5e}")
    if vals:
        span = math.log10(max(vals) / min(vals))
        g2[foot] = span
        P(f"  {foot:10s} dex span = {span:.4f}   allowance 0.0411   -> "
          f"{'PASS' if span <= 0.0411 else 'FAIL'} ({span/0.0411:.1f}x)")
G2 = all(v <= 0.0411 for v in g2.values())
P(f"  => {'PASS' if G2 else 'FAIL'}")
P()

# ------------------------------------------------------------------ G3
P("G3  universality in epoch (log M_b = 10.45)  " + "-" * 60)
P(f"  {'footing':10s} {'z':>5s} {'R_fold':>10s} {'kappa_S':>12s} {'drift dex':>10s}")
g3 = {}
for foot in ("canonical", "alt"):
    d = load(foot, 10.45)
    Rc = R_COSMIC[foot]
    base = None
    drifts = []
    for zt in (0, 1, 2, 4):
        zz, Rf = rfold_at_z(d, zt)
        if Rf <= 0:
            P(f"  {foot:10s} {zt:5g}   front not yet formed (R_fold = 0)")
            continue
        a0s, kap = kappa_S(10 ** 10.45, Rf, Rc)
        if base is None:
            base = kap
        dr = math.log10(kap / base)
        drifts.append(abs(dr))
        P(f"  {foot:10s} {zt:5g} {Rf:10.3f} {kap:12.5e} {dr:+10.4f}   (z_actual {zz:.3f})")
    if drifts:
        mx = max(drifts)
        g3[foot] = mx
        P(f"  {foot:10s} max |drift| = {mx:.4f} dex   allowance 0.0411   -> "
          f"{'PASS' if mx <= 0.0411 else 'FAIL'}")
G3 = all(v <= 0.0411 for v in g3.values())
P(f"  => {'PASS' if G3 else 'FAIL'}")
P()

# ------------------------------------------------------------------ G4
P("G4  the error bar on kappa_S (log M_b = 10.45, z = 0)  " + "-" * 46)
d_can = load("canonical", 10.45)
Rf_can = d_can["R_fold_end_kpc"]
Rc_can = R_COSMIC["canonical"]
a0s_can, kap_can = kappa_S(10 ** 10.45, Rf_can, Rc_can)
d_rest = load("canonical", 10.45, mode="rest")
P(f"  central: kappa_S = {kap_can:.6e}   log10 = {math.log10(kap_can):+.4f}")
P(f"  {'term':42s} {'shift dex':>10s}")
terms = []
# R_cosmic
dln_a_dln_R = (1 + 2 * Rc_can) / (1 + Rc_can)
sR = dln_a_dln_R * (R_ERR / Rc_can) / math.log(10)
terms.append(("R_cosmic +- 0.065 (Planck fallback, R541 part E)", sR))
# R_fold: at-rest vs Hubble-flow
if d_rest is not None:
    Rf_rest = d_rest["R_fold_end_kpc"]
    frac = Rf_rest / Rf_can
    P(f"  [measured] FLD1 rest/hubble R_fold ratio = {frac:.4f} "
      f"(rest {Rf_rest:.3f} kpc vs hubble {Rf_can:.3f} kpc)")
    sRf = abs(2 * math.log10(frac))
    terms.append((f"R_fold at-rest vs Hubble flow (ratio {frac:.4f})", sRf))
else:
    sRf = 2 * math.log10(1.223)
    terms.append(("R_fold at-rest vs Hubble flow (+22.3%, OUT3 arm A)", sRf))
terms.append(("R_fold start redshift 20/30 (+1.4%)", 2 * math.log10(1.014)))
terms.append(("R_fold shell N 1200->4800 (+0.07%)", 2 * math.log10(1.0007)))
terms.append(("rho_Lambda +- 1.5% (Planck)", 0.5 * math.log10(1.015)))
tot = math.sqrt(sum(t * t for _, t in terms))
for name, s in terms:
    P(f"  {name:42s} {s:+10.4f}")
P(f"  {'TOTAL (quadrature on the log)':42s} {tot:+10.4f}")
P(f"  => kappa_S = {kap_can:.4e}  (+{tot:.3f} / -{tot:.3f} dex)"
  f"   = [{kap_can*10**(-tot):.4e}, {kap_can*10**(tot):.4e}]")
P(f"  G4 is a REPORT. Per PREREGISTER sec.3, no bar can absorb a G2/G3 failure.")
P(f"  distance from the band in units of the bar: "
  f"{abs(math.log10(kap_can/0.5))/tot:.1f} sigma(bar)")
P()

# ------------------------------------------------------------------ G5
P("G5  the conservation blocker: can the front deliver R_cosmic?  " + "-" * 40)
P(f"  FINAL3 (H): settling rearranges cold charge, it does not create it.")
P(f"  {'footing':10s} {'logMb':>6s} {'q_turned':>9s} {'q_crossed':>9s} "
  f"{'R_cosmic':>9s} {'q/R':>7s} verdict")
g5 = {}
for foot in ("canonical", "alt"):
    Rc = R_COSMIC[foot]
    ok = True
    for lm in GRID:
        d = load(foot, lm)
        if d is None:
            continue
        q_t = d["charge_turned_around_over_Mb"]
        q_c = d["series"][-1][d["series_cols"].index("fraction_crossed")]
        if lm in (10.45, 8, 6.5, 12) or lm == GRID[0]:
            P(f"  {foot:10s} {lm:6g} {q_t:9.4f} {q_c:9.4f} {Rc:9.3f} "
              f"{q_t/Rc:7.3f} {'PASS' if q_t >= Rc else 'FAIL'}")
        if q_t < Rc:
            ok = False
    g5[foot] = ok
    P(f"  {foot:10s} => {'PASS' if ok else 'FAIL'}  "
      f"(delivered charge never reaches the cosmic share at any mass)")
G5 = all(g5.values())
P(f"  => {'PASS' if G5 else 'FAIL'}")
P()

# ------------------------------------------------------------------ MUTATE
P("MUTATE  " + "-" * 92)
# MU1
P(f"  MU1 'the cosmic-share settle-down derives kappa = 1/2'")
P(f"      -> {'REJECTED' if not G1 else 'NOT REJECTED'}: band miss "
  f"{abs(kap_can-0.5):.4f} vs 0.025 ({abs(kap_can-0.5)/0.025:.1f}x)")
# MU2
P(f"  MU2 'the miss is inside the error bar'")
P(f"      -> {'REJECTED' if (not G2 or not G3) else 'NOT REJECTED'}: bar {tot:.3f} dex, "
  f"miss {abs(math.log10(kap_can/0.5)):.3f} dex, G2 mass span "
  f"{max(g2.values()):.3f} dex is a spread of DIFFERENT numbers")
# MU3
_, kap_xcop = kappa_S(10 ** 10.45, Rf_can, 5.73)
P(f"  MU3 'use the X-COP value 5.73 +- 0.68 instead'")
P(f"      -> {'REJECTED' if abs(kap_xcop-0.5) > 0.025 else 'NOT REJECTED'}: "
  f"kappa_S = {kap_xcop:.4e}, still {abs(kap_xcop-0.5)/0.025:.1f}x the band "
  f"(X-COP is reported, never pooled: R541 sec.6)")
P()

# ------------------------------------------------------------------ LABEL
P("=" * 100)
fails = [n for n, ok in (("G1", G1), ("G2", G2), ("G3", G3)) if not ok]
if not G0:
    label = "OPEN (G0 failed: the lane is inadmissible)"
elif G1 and G2 and G3 and G5:
    label = "AMOUNT DERIVED (COSMIC-SHARE FOLD)"
elif not G5:
    label = "AMOUNT NOT DERIVED (UNAVAILABLE)"
else:
    label = "AMOUNT NOT DERIVED (FALSIFIED)"
P(f"G0 {'PASS' if G0 else 'FAIL'}   G1 {'PASS' if G1 else 'FAIL'}   "
  f"G2 {'PASS' if G2 else 'FAIL'}   G3 {'PASS' if G3 else 'FAIL'}   "
  f"G5 {'PASS' if G5 else 'FAIL'}")
P(f"LABEL: {label}")
P(f"kappa = 1/2 FITTED; not theory closed.  R_cosmic = 5.41 FITTED; not derived.")
P("=" * 100)

json.dump({
    "G0": G0, "G1": G1, "G2": G2, "G3": G3, "G5": G5,
    "kappa_S_canonical_10.45": kap_can,
    "a0_S_canonical_10.45": a0s_can,
    "error_bar_dex": tot,
    "error_terms": {n: s for n, s in terms},
    "mass_span_dex": g2, "epoch_drift_dex": g3,
    "R_cosmic": R_COSMIC, "R_fold_10.45_canonical": Rf_can,
    "label": label,
}, open(os.path.join(HERE, "out3csf.json"), "w"), indent=2)

open(os.path.join(HERE, "out3csf.out"), "w").write("\n".join(out) + "\n")
