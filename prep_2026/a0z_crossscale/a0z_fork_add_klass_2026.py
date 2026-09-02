#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
a0z_fork_add_klass_2026.py -- a twelfth constraint for the a0(z) fork from existing data: KLASS lensed low-mass galaxies at cosmic noon.
=========================================================================================================================================
Girard+ 2020 (MNRAS 497, 173; arXiv:2006.14633): 44 lensed star-forming galaxies, 0.6 < z < 2.3 (mean z ~ 1.3), 8.1 < log M* < 11.0
(median 9.5), KMOS seeing-limited, pressure-corrected V_circ = sqrt(v_rot^2 + 3.4 sigma_0^2).  Their stellar Tully-Fisher relation,
log V = b + 0.274 (log M* - 10.10) with the local Reyes+ 2011 zero-point b = 2.127, shows a VELOCITY zero-point offset of +0.18 dex for
the full sample (+0.22 for the regular rotators), i.e. the galaxies rotate 51% faster at fixed stellar mass than local ones; the authors
attribute it to higher gas fractions.  Read through the framework's own kernel in the deep-MOND regime, v^4 = G M_b a_0, at fixed M*:
        Delta log a_0 = 4 Delta log V - Delta log(M_b/M*),
with the baryonic-to-stellar correction from gas fractions that KLASS did NOT measure: molecular gas from the Tacconi+ 2018 scaling
(mu_H2 ~ 1.7 at z = 1.3, log M* = 9.5, main sequence), atomic gas taken as local-like (M_HI/M* ~ 1), against local SPARC-like
1 + f = 2 at the same M*: Delta log(M_b/M*) = +0.27 +/- 0.20.  So Delta log a_0 = 0.72 - 0.27 = +0.45, with a total systematic of
0.35 dex (gas 0.20, pressure correction / beam smearing 0.25, in quadrature) -- FACE VALUE, before the lever and the apparent-drift
nuisance.  Exposure w = 1.00 (seeing-limited, uncorrected for selection / beam smearing: the maximal drift channel, as [4]-[6]).
Lever: median M* 3e9 with gas ~ 1e10 at r_e ~ 2-3 kpc gives g_bar ~ 0.5-1.0 a_0.
FUDS (arXiv:2608.04371) was also examined: its bins stop at z <= 0.12 with zero-points +/-0.06 dex, no lever; not added.
The fork's committed machinery is loaded by exec (its prints suppressed) and the odds recomputed with and without [12], plus the
LCDM-native laws of a0z_lcdm_native_hypothesis_2026.py.  Both ways.  Checks CAN fail.
"""
import io, os, sys, math, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "a0z_fork_likelihood_2026.py")).read()
ns = {"__file__": os.path.join(HERE, "a0z_fork_likelihood_2026.py"), "__name__": "parent"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[:src.index("PAIRS = [")], ns)
MODELS, POINTS, ln_evidence, lever = ns["MODELS"], ns["POINTS"], ns["ln_evidence"], ns["lever"]
OM, OL = ns["OM"], ns["OL"]; h = 0.674
E = lambda z: np.sqrt(OM*(1+z)**3 + OL); f = lambda x: np.log(1+x) - x/(1+x)
def c_DM14(M, z):
    a = 0.520 + (0.905 - 0.520)*np.exp(-0.617*z**1.21); b = -0.101 + 0.026*z
    return 10**(a + b*np.log10(M*h/1e12))
def make_R(cfun, M=1e12):
    c0 = cfun(M, 0.0); base = c0**2/f(c0)
    return lambda z, w0=None, wa=None: E(np.asarray(z, float))**(4/3)*(cfun(M, np.asarray(z, float))**2/f(cfun(M, np.asarray(z, float))))/base
MODELS["M-LCDM-DM14"] = make_R(c_DM14); MODELS["M-LCDM-MAG"] = lambda z, w0=None, wa=None: (1.0 + np.asarray(z, float))**0.92
ORDER = ["M-FLAT", "M-DEC", "M-RISE", "M-LCDM-DM14", "M-LCDM-MAG"]
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
# ---------------------------------------------------------------- the KLASS point
dV = 0.18; dMb = 0.27; sig_gas = 0.20; sig_kin = 0.25
val = 4*dV - dMb; sig_tot = math.sqrt(sig_gas**2 + sig_kin**2 + (4*0.03)**2)     # + the fit error on the offset (~0.03 in log V)
KL = dict(tag="[12] KLASS Girard+20", cite="Girard+2020 MNRAS 497,173 arXiv:2006.14633 (44 lensed low-mass SFGs, KMOS)",
          kind="RATIO", zrep=1.3, val=val, sig_stat=0.12, sig_tot=sig_tot, gbar_lo=0.5, gbar_hi=1.0, w=1.00,
          prov=f"DERIVED HERE: velocity ZP offset +0.18 dex (V_circ, full sample) -> 4x = +0.72 in log a0 at fixed M*, minus the gas correction +0.27 (Tacconi+18 H2 + local-like HI vs SPARC-like local): +{val:.2f} +/- {sig_tot:.2f} FACE VALUE",
          wnote="1.00 MAXIMAL: seeing-limited KMOS, pressure-corrected V_circ, no selection/beam-smearing correction -- the same channel as [4]-[6]")
y = math.sqrt(KL["gbar_lo"]*KL["gbar_hi"]); KL["y_gbar"] = y; KL["L"] = lever(y); KL["dedil_val"] = KL["val"]/KL["L"]; KL["dedil_sig"] = KL["sig_tot"]/KL["L"]; KL["dedil_sig_stat"] = KL["sig_stat"]/KL["L"]
P("="*100); P("[12] KLASS as a fork constraint (face value, then the lever)"); P("="*100)
info(f"z = 1.3, log10 a0(z)/a0(0) = {val:+.2f} +/- {sig_tot:.2f} (face), lever L = {KL['L']:.2f} (g_bar/a0 ~ {y:.2f}) -> de-diluted {KL['dedil_val']:+.2f} +/- {KL['dedil_sig']:.2f}")
info("laws at z = 1.3: " + ", ".join(f"{m}: {float(np.log10(MODELS[m](1.3))):+.2f}" for m in ORDER))
check("K1 at FACE VALUE the KLASS point sits ABOVE every law including a0 ~ H(z): it is an apparent-rise point of the Ciocan/MSA-3D class, not evidence for any law in the fork",
      val > max(float(np.log10(MODELS[m](1.3))) for m in ORDER), f"face +{val:.2f} vs max law +{max(float(np.log10(MODELS[m](1.3))) for m in ORDER):.2f}")
P(""); P("="*100); P("odds with and without [12], drift ceilings 0 / 0.92 / 1.22 / 1.50 (log10 B, positive favours the first)"); P("="*100)
pts_with = POINTS + [KL]
rows = []
for label, pmax in (("face value", 0.0), ("Magneticum p<0.92", 0.92), ("MSA-3D p<1.22", 1.22), ("loose p<1.50", 1.50)):
    lz0 = {m: ln_evidence(m, pmax, pts=POINTS)[0] for m in ORDER}; lz1 = {m: ln_evidence(m, pmax, pts=pts_with)[0] for m in ORDER}
    b = lambda lz, a_, c_: (lz[a_] - lz[c_])/math.log(10)
    rows.append((label, b(lz0, "M-FLAT", "M-LCDM-DM14"), b(lz1, "M-FLAT", "M-LCDM-DM14"), b(lz0, "M-DEC", "M-RISE"), b(lz1, "M-DEC", "M-RISE")))
    info(f"{label:20s}: FLAT/LCDM-DM14 {rows[-1][1]:+7.2f} -> {rows[-1][2]:+7.2f} | DEC/RISE {rows[-1][3]:+7.2f} -> {rows[-1][4]:+7.2f}")
shift = [abs(r[2] - r[1]) for r in rows[1:]]
check("K2 with the drift nuisance on (p_max >= 0.92) the twelfth point moves every FLAT-vs-LCDM verdict by < 1.0 in log10 B: it is absorbed by the same apparent-drift channel as the other uncorrected points -- the fork stays UNDECIDED and prior-dominated",
      all(s < 1.0 for s in shift), "shifts: " + ", ".join(f"{s:.2f}" for s in shift))
check("K3 at face value (no drift allowed) the point pushes AGAINST the framework: FLAT/LCDM-DM14 falls, DEC/RISE falls -- reported against interest", rows[0][2] < rows[0][1] and rows[0][4] < rows[0][3], f"face: FLAT/LCDM {rows[0][1]:+.1f} -> {rows[0][2]:+.1f}, DEC/RISE {rows[0][3]:+.1f} -> {rows[0][4]:+.1f}")
P(""); P("="*100); P("VERDICT"); P("="*100)
P("  Read through the framework's kernel with gas fractions from scaling relations, KLASS's lensed low-mass galaxies at z ~ 1.3 rotate")
P("  too fast at fixed stellar mass for ANY a0(z) law, including a0 ~ H(z): an apparent-rise point of the Ciocan class, carried by the")
P("  same uncorrected channel (seeing-limited kinematics, pressure correction, unmeasured gas).  Added as [12] it is absorbed by the")
P("  drift nuisance and the fork stays undecided; at face value it leans against the framework.  FUDS has no lever below z = 0.12.")
P("  There is no creative reading of the existing archives that decides this; the decisive object still has to be measured.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
