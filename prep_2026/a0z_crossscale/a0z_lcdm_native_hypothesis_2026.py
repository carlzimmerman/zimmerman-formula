#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
a0z_lcdm_native_hypothesis_2026.py -- THE SPECIFIC FRAMEWORK-vs-LambdaCDM TEST, run on the data in hand.
=========================================================================================================
The committed joint likelihood (a0z_fork_likelihood_2026.py) compares three framework-side laws (DEC, RISE, FLAT) over
the 10 committed high-z constraints, with LambdaCDM's apparent-a0 drift treated only as a NUISANCE.  It never asked the
question the user asks: framework vs LambdaCDM.  LambdaCDM has no fundamental a0; its RAR scale is EMERGENT from halo
structure and RISES with redshift (crispy_fabric_prediction_2026.py): a_s(z)/a_s(0) = E(z)^{4/3} [c^2/f(c)](z)/[c^2/f(c)](0).
So add it as a fourth ZERO-PARAMETER hypothesis:
    M-LCDM-DM14 : structure-only rise, Dutton-Maccio 2014 c(M,z), M_200 = 1e12     (x1.23 @z=1, x1.76 @z=2, x2.57 @z=3)
    M-LCDM-D08  : same with Duffy 2008                                              (x1.43, x2.28, x3.37)
    M-LCDM-MAG  : the hydrodynamical apparent rise, (1+z)^{0.92} (Magneticum x3 @z=2.3)  -- structure + assembly + selection
and treat the exposure-weighted contamination nuisance IDENTICALLY for every model (the same beam/pressure/selection
channels exist in a LambdaCDM universe; keeping the nuisance for the LCDM laws is the CONSERVATIVE choice against them).
Outputs: log10 B(FLAT / LCDM-*) and (DEC / LCDM-*) at face value and at the three drift ceilings; leave-Ciocan-out;
the dominant point; and the FORECAST: the BTFR zero-point precision at z = 2.5 that would decide FLAT vs LCDM-DM14 at 20:1.
Everything is computed with the parent's own machinery (loaded by exec, its prints suppressed), so the numbers are on the
same footing as the committed odds.  Checks can FAIL.  Footing-independent (ratios only).
"""
import io, os, sys, math, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.join(HERE, "a0z_fork_likelihood_2026.py")
src = open(PARENT).read()
cut = src.index("PAIRS = [")
ns = {"__file__": PARENT, "__name__": "parent_loaded"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[:cut], ns)
MODELS, POINTS, ln_evidence, R_flat, R_dec = ns["MODELS"], ns["POINTS"], ns["ln_evidence"], ns["R_flat"], ns["R_dec"]
OM, OL = ns["OM"], ns["OL"]
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)

# ---------------------------------------------------------------- the LambdaCDM-native laws (from crispy_fabric_prediction_2026.py)
h = 0.674
E = lambda z: np.sqrt(OM*(1+z)**3 + OL)
f = lambda x: np.log(1+x) - x/(1+x)
def c_DM14(M, z):
    a = 0.520 + (0.905 - 0.520)*np.exp(-0.617*z**1.21); b = -0.101 + 0.026*z
    return 10**(a + b*np.log10(M*h/1e12))
def c_D08(M, z): return 5.71*(M*h/2e12)**(-0.084)*(1+z)**(-0.47)
def make_R(cfun, M=1e12):
    c0 = cfun(M, 0.0); base = c0**2/f(c0)
    def R(z, w0=None, wa=None):
        z = np.asarray(z, float); cz = cfun(M, z)
        return E(z)**(4/3)*(cz**2/f(cz))/base
    return R
MODELS["M-LCDM-DM14"] = make_R(c_DM14)
MODELS["M-LCDM-D08"] = make_R(c_D08)
MODELS["M-LCDM-MAG"] = lambda z, w0=None, wa=None: (1.0 + np.asarray(z, float))**0.92
ORDER = ["M-FLAT", "M-DEC", "M-RISE", "M-LCDM-DM14", "M-LCDM-D08", "M-LCDM-MAG"]
P("="*100); P("A. the laws at the data's redshifts (ratio a0(z)/a0(0); footing-independent)"); P("="*100)
info(f"{'z':>5} " + " ".join(f"{m:>12s}" for m in ORDER))
for z in (0.9, 1.0, 2.0, 2.3, 2.5, 3.25):
    info(f"{z:5.2f} " + " ".join(f"{float(MODELS[m](z)):12.3f}" for m in ORDER))
check("A1 the LambdaCDM-native structural laws rise x1.5-2.5 by z = 2 and lie BELOW the E(z) rival and the Magneticum apparent rise",
      1.5 < float(MODELS['M-LCDM-DM14'](2.0)) < 2.5 and float(MODELS['M-LCDM-D08'](2.0)) < float(ns['R_rise'](2.0)) and float(MODELS['M-LCDM-DM14'](2.3)) < 3.0)

# ---------------------------------------------------------------- B. the odds, apples to apples
P(""); P("="*100); P("B. joint odds over the 10 committed constraints, identical nuisance treatment for every model"); P("="*100)
CEILINGS = [("face value (no drift)", 0.0), ("Magneticum ceiling p<0.92", 0.92), ("MSA-3D measured p<1.22", 1.22), ("loose p<1.50", 1.50)]
def lnZ_all(pts=None, **kw):
    return {m: ln_evidence(m, pm, pts=pts, **kw)[0] for m in ORDER for pm in [None]} if False else None
results = {}
info(f"{'ceiling':28s} " + " ".join(f"{m:>13s}" for m in ORDER) + "  | log10B FLAT/DM14  FLAT/D08  FLAT/MAG  DEC/DM14")
for label, pmax in CEILINGS:
    lnZ = {m: ln_evidence(m, pmax)[0] for m in ORDER}
    results[label] = lnZ
    b = lambda a_, c_: (lnZ[a_] - lnZ[c_])/math.log(10)
    info(f"{label:28s} " + " ".join(f"{lnZ[m]:13.2f}" for m in ORDER)
         + f"  | {b('M-FLAT','M-LCDM-DM14'):+8.2f} {b('M-FLAT','M-LCDM-D08'):+9.2f} {b('M-FLAT','M-LCDM-MAG'):+9.2f} {b('M-DEC','M-LCDM-DM14'):+9.2f}")
bf = {label: {("M-FLAT", m): (results[label]["M-FLAT"] - results[label][m])/math.log(10) for m in ("M-LCDM-DM14", "M-LCDM-D08", "M-LCDM-MAG")} for label, _ in CEILINGS}
vals_dm14 = [bf[l][("M-FLAT", "M-LCDM-DM14")] for l, _ in CEILINGS]
info(f"B  log10 B(FLAT / LCDM-DM14) across the drift ladder: {[round(v,2) for v in vals_dm14]}  -> worst case |log10 B| = {min(abs(v) for v in vals_dm14):.2f} (20:1 needs 1.30)")
check("B1 NO prior-robust verdict yet: the FLAT-vs-LCDM-native odds do not clear 20:1 at every ceiling (the data in hand cannot decide framework vs LambdaCDM)",
      min(abs(v) for v in vals_dm14) < 1.30, "honest: undecided" )
sign_flip = (max(vals_dm14) > 0) and (min(vals_dm14) < 0)
info(f"B2 sign of the FLAT/LCDM-DM14 odds across ceilings: {'FLIPS' if sign_flip else 'stable'}  ({'prior-dominated' if sign_flip else 'direction robust, size not'})")

# ---------------------------------------------------------------- C. leave-Ciocan-out and dominant point
P(""); P("="*100); P("C. robustness: drop the dominant point (Ciocan), and the drop-9-and-10 sensitivity"); P("="*100)
pts_noC = [p_ for p_ in POINTS if not p_["tag"].startswith("[2]")]
pts_no910 = [p_ for p_ in POINTS if not (p_["tag"].startswith("[9]") or p_["tag"].startswith("[10]"))]
for name, pts in (("drop Ciocan [2]", pts_noC), ("drop [9],[10] (estimate-coded)", pts_no910)):
    row = []
    for label, pmax in CEILINGS:
        lnZ = {m: ln_evidence(m, pmax, pts=pts)[0] for m in ("M-FLAT", "M-LCDM-DM14", "M-LCDM-D08", "M-LCDM-MAG")}
        row.append((label[:14], (lnZ["M-FLAT"]-lnZ["M-LCDM-DM14"])/math.log(10), (lnZ["M-FLAT"]-lnZ["M-LCDM-MAG"])/math.log(10)))
    info(f"{name:32s}: " + "; ".join(f"{l}: FLAT/DM14 {a:+.2f}, FLAT/MAG {b:+.2f}" for l, a, b in row))
# per-point pull under FLAT vs LCDM-DM14 at face value: who carries the verdict?
info("per-point chi2 at face value (no drift): FLAT vs LCDM-DM14 vs LCDM-MAG")
for p_ in POINTS:
    cf = ns["point_chi2"](p_, "M-FLAT", 0.0, drift_on=False); cl = ns["point_chi2"](p_, "M-LCDM-DM14", 0.0, drift_on=False); cm = ns["point_chi2"](p_, "M-LCDM-MAG", 0.0, drift_on=False)
    info(f"   {p_['tag']:26s} z={p_['zrep']:.2f} w={p_['w']:.2f}: chi2 FLAT {cf:6.2f}  LCDM-DM14 {cl:6.2f}  LCDM-MAG {cm:6.2f}   {'-> favours LCDM' if cl < cf - 1 else ('-> favours FLAT' if cf < cl - 1 else '')}")

# ---------------------------------------------------------------- D. THE TEST: what measurement decides it
P(""); P("="*100); P("D. the decisive measurement: BTFR / deep-MOND zero-point at z = 2.5 (lever ~ 1), precision needed for 20:1"); P("="*100)
for zt in (2.0, 2.5, 3.0):
    dlt = float(np.log10(MODELS["M-LCDM-DM14"](zt))) - 0.0
    dlt8 = float(np.log10(MODELS["M-LCDM-D08"](zt)))
    sig20 = dlt/math.sqrt(2*1.30*math.log(10))
    info(f"z = {zt}: FLAT predicts 0.00 dex; LCDM-native predicts {dlt:+.2f} (DM14) / {dlt8:+.2f} (D08) dex in the M(v) zero-point"
         f" -> ONE clean deep-MOND point with sigma <= {sig20:.2f} dex (DM14) decides at 20:1; the current best single point is Big Wheel (z=3.25, +/-0.22 dex, N=1)")
sig_need_25 = float(np.log10(MODELS["M-LCDM-DM14"](2.5)))/math.sqrt(2*1.30*math.log(10))
check("D1 a single deep-MOND BTFR zero-point at z = 2.5 with sigma <= 0.15 dex separates FLAT from LCDM-native (DM14) at 20:1 -- a JWST/ALMA-scale measurement, not a survey",
      0.10 < sig_need_25 < 0.20, f"sigma needed = {sig_need_25:.3f} dex")
P(""); P("="*100); P("VERDICT"); P("="*100)
P("  Framework-vs-LambdaCDM, on the data in hand: UNDECIDED and prior-dominated -- the same conclusion the committed fork likelihood reached")
P("  among the framework's own laws.  The test that decides it is specific: the BTFR / deep-MOND zero-point of massive discs at z ~ 2.5,")
P("  where the framework's flat law predicts 0.00 dex and LambdaCDM's emergent halo scale predicts +0.3 to +0.4 dex; one clean point at")
P("  +/-0.15 dex decides at 20:1.  Existing clean points (Big Wheel z=3.25 at +0.06 +/- 0.22; McGaugh+24 null) lean flat but are too coarse.")
P("  Both ways: a measured rise on that arm kills the framework's flat law (and standard MOND with it); a measured constancy forces the")
P("  LambdaCDM fabric change of crispy_fabric_prediction_2026.py.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
