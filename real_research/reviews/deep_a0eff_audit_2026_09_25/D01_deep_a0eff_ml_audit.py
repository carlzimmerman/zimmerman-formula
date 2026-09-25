#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
D01 -- AUDIT OF THE "SPARC-DEEP a0_eff = 0.72 a0" CHANNEL (deepseek_push L06 -> N05 -> O04b "joint deep a0_eff = 0.7172 +/- 0.0593,
4.77 sigma below the canonical a0 = 9.3619e-11"), done before any of it is quoted.

THE CLAIM.  L06 applies the alpha = 1 moment identity  E[g_obs^2] = E[g_bar^2] + a0 E[g_bar]  to SPARC rings with g_bar < 0.2 a0 and finds
Delta/(a0 E[g_bar]) = -0.276, i.e. a0_eff = 0.724 a0.  N05, O04b, ZD07-ZD11 and N01 build on it ("a0* ~ 6.0-6.8e-11").

WHAT THIS SCRIPT CHECKS (each can fail):
  D1  the claimed number is reproduced from the lane's own inputs (glm53_push/data/rotation_curve_corpus_v7.json, per-galaxy m2l_disk,
      applied to disc AND bulge, all rings with v_bar^2 > 0) -- so the audit is of the same computation;
  D2  the corpus's V_disk equals SPARC's own 3.6-micron V_disk at Upsilon = 1 (real_research/data/sparc_data), so m2l_disk multiplies
      the 3.6-micron curves;
  D3  the corpus m2l_disk values are NOT 3.6-micron stellar-population values: median and 84th percentile well above 0.5-0.7, and
      the largest values sit on gas-rich dwarfs;
  D4  with the standard 3.6-micron ratios (disc 0.5 or 0.6, bulge 0.7) the SAME statistic on the SAME rings changes sign
      (a0_eff > a0): the deficit is carried by the corpus mass-to-light values, not by the kinematics;
  D5  the alpha = 1 moment estimator is not a0 in the in-force kernel nu(y) = 1/(1 - exp(-sqrt y)): on synthetic rings that obey that
      kernel EXACTLY at the canonical a0 it returns 1.17-1.27 a0 in the deep band -- a bias of the estimator, not a measurement;
  D6  (written BEFORE the run, expecting a pass) the in-force kernel fitted to L06's own deep rings (g_bar < 0.1 a0, standard ratios,
      every ring, unweighted, as L06 uses them) returns kappa = a0/(c sqrt(G rho_Lambda)) in 0.40-0.60 for Upsilon_disc = 0.5-0.7.
      >>> IT FAILED on the first run: kappa = 0.44 / 0.39 / 0.34.  It is kept, printed as FAIL, and not re-cut.  D7 finds the cause.
  D7  the cause of D6: rings with velocity errors above 10 per cent, given equal weight, pull kappa down by ~0.1; with the standard
      quality cut (err/V < 10 per cent) or error weighting the same band gives 0.43-0.56.  The fit returns an injected a0 exactly.
LOAD-BEARING for this audit's verdict on O04b: D1-D5 (they decide whether the claimed number is a measurement of a0).  D6/D7 are the
deep band read with the in-force kernel: an against-interest finding (the band leans low under one weighting), not a verdict on O04b.
The exit code counts load-bearing failures only; D6's FAIL is printed and recorded in the results file.
MUTATE=1 sets every corpus m2l_disk to 0.5 before D1: the reproduction of 0.724 must then FAIL (rc = 1).
Run from the repository root:  python3 real_research/reviews/deep_a0eff_audit_2026_09_25/D01_deep_a0eff_ml_audit.py
"""
import os, sys, json, glob, math
import numpy as np
from scipy.optimize import minimize_scalar

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
A0 = 9.3619e-11                         # canonical footing (the lane's own constant)
KPC = 3.0856775814913673e19
A_L = 2 * A0                            # c sqrt(G rho_Lambda) on the same footing, so kappa = a0 / A_L
CH = []
def P(*a): print(*a, flush=True)
def check(name, measured, ok, reading="", load_bearing=True):
    CH.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}" + (f"\n         reading:  {reading}" if reading else ""))
def banner(t): P("\n" + "=" * 112 + "\n" + t + "\n" + "=" * 112)
P(__doc__)

corpus = json.load(open(os.path.join(ROOT, "glm53_push", "data", "rotation_curve_corpus_v7.json")))
GAL = [g for g in corpus["galaxies"] if g.get("survey") == "SPARC"]
if MUTATE:
    for g in GAL: g["m2l_disk"] = 0.5

def build(ud=None, ub=None):
    """rings as in L06: per-galaxy corpus m2l on disc AND bulge when ud is None; otherwise fixed (ud, ub)."""
    X, Y, N = [], [], []
    for g in GAL:
        m2l = g.get("m2l_disk") or 0.0
        m2l = m2l if m2l > 0 else 0.5
        d_, b_ = (m2l, m2l) if ud is None else (ud, ub)
        for p in g.get("data") or []:
            vb2 = math.copysign(p["Vgas"] ** 2, p["Vgas"]) + d_ * p["Vdisk"] ** 2 + b_ * p["Vbul"] ** 2
            if vb2 <= 0 or p["Vobs"] <= 0: continue
            R = p["Rad"] * KPC
            X.append(vb2 * 1e6 / R); Y.append((p["Vobs"] * 1e3) ** 2 / R); N.append(g["galaxy"])
    return np.array(X), np.array(Y), np.array(N)
def moment(X, Y):
    return 1.0 + np.mean(Y ** 2 - X ** 2 - A0 * X) / (A0 * np.mean(X))
nu = lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(y)))

banner("D1  REPRODUCE THE CLAIMED NUMBER FROM THE LANE'S OWN INPUTS")
X, Y, N = build(); m = X < 0.2 * A0
r_claim = moment(X[m], Y[m])
check("D1 the corpus inputs reproduce a0_eff/a0 = 0.724 on 1152 deep rings from 135 galaxies", f"{r_claim:.4f} on {m.sum()} rings / {len(np.unique(N[m]))} galaxies",
      abs(r_claim - 0.724) < 0.002 and m.sum() == 1152)

banner("D2  THE CORPUS V_disk IS SPARC's 3.6-MICRON V_disk AT UPSILON = 1")
worst, ncmp = 0.0, 0
for g in GAL:
    f = os.path.join(ROOT, "real_research", "data", "sparc_data", f"{g['galaxy']}_rotmod.dat")
    if not os.path.exists(f): continue
    r = np.genfromtxt(f, comments="#"); cv = np.array([p["Vdisk"] for p in g["data"]]); n = min(len(cv), len(r))
    worst = max(worst, float(np.max(np.abs(cv[:n] - r[:n, 4])))); ncmp += 1
check("D2 corpus V_disk equals the SPARC rotmod V_disk (Upsilon = 1, 3.6 micron) for every galaxy compared", f"{ncmp} galaxies, max |difference| = {worst:.3f} km/s",
      ncmp >= 170 and worst < 0.01, "so m2l_disk is a 3.6-micron mass-to-light ratio, directly comparable with 0.5-0.7")

banner("D3  THE CORPUS MASS-TO-LIGHT VALUES")
ml = np.array([g.get("m2l_disk") or 0.0 for g in GAL]); ml = ml[ml > 0]
fg = []
for g in GAL:
    v = g.get("data") or []
    if not v: continue
    last = v[-1]; vb = last["Vgas"] ** 2 + last["Vdisk"] ** 2 + last["Vbul"] ** 2
    fg.append((g.get("m2l_disk") or 0.0, last["Vgas"] ** 2 / vb if vb > 0 else np.nan, g["galaxy"]))
top = sorted(fg, key=lambda t: -t[0])[:6]
check("D3 the corpus m2l_disk distribution is far above 3.6-micron population values (median > 0.9, 84th percentile > 2)",
      f"median {np.median(ml):.2f}, 16/84% {np.percentile(ml,16):.2f}/{np.percentile(ml,84):.2f}; largest: " + ", ".join(f"{t[2]} {t[0]:.2f} (gas share at R_last {t[1]:.2f})" for t in top),
      (not MUTATE) and np.median(ml) > 0.9 and np.percentile(ml, 84) > 2.0,
      "stellar population models give 0.5-0.7 at 3.6 micron (Meidt+2014, Schombert+2019); these values are fits, and they are applied to bulges too")

banner("D4  SAME STATISTIC, SAME RINGS, STANDARD RATIOS")
res4 = {}
for ud, ub in ((0.5, 0.7), (0.6, 0.7), (0.7, 0.7)):
    Xs, Ys, Ns = build(ud, ub); ms = Xs < 0.2 * A0
    res4[(ud, ub)] = (moment(Xs[ms], Ys[ms]), int(ms.sum()), len(np.unique(Ns[ms])))
    P(f"    Upsilon_disc = {ud}, Upsilon_bul = {ub}: a0_eff/a0 = {res4[(ud,ub)][0]:.3f} on {res4[(ud,ub)][1]} rings / {res4[(ud,ub)][2]} galaxies")
check("D4 with standard 3.6-micron ratios the deep-band statistic is ABOVE 1 (the sign of the claimed deficit reverses)",
      ", ".join(f"({k[0]},{k[1]}): {v[0]:.3f}" for k, v in res4.items()), all(v[0] > 1.0 for v in res4.values()),
      "the 0.72 is carried by the corpus mass-to-light values, not by the rotation curves")

banner("D5  WHAT THE MOMENT ESTIMATOR RETURNS FOR DATA THAT OBEY THE IN-FORCE KERNEL EXACTLY")
Xs, Ys, Ns = build(0.5, 0.7)
res5 = {}
for cut in (0.2, 0.1, 0.05):
    ms = Xs < cut * A0; syn = Xs[ms] * nu(Xs[ms] / A0)
    res5[cut] = moment(Xs[ms], syn)
    P(f"    g_bar < {cut} a0: moment estimator on exact-kernel synthetic rings (a0 = canonical) returns {res5[cut]:.3f} a0")
check("D5 the alpha = 1 moment estimator is biased high by 15-30 per cent for nu_RAR data in the deep band (it is not the kernel's a0)",
      ", ".join(f"<{k}: {v:.3f}" for k, v in res5.items()), all(1.15 < v < 1.30 for v in res5.values()))

banner("D6  THE IN-FORCE KERNEL ON L06's OWN DEEP RINGS (standard ratios), AS PRE-STATED")
def fit(X_, Y_, w=None):
    w = np.ones_like(X_) if w is None else w
    f = lambda la: np.sum(w * (np.log10(Y_) - np.log10(X_ * nu(X_ / 10 ** la))) ** 2)
    return 10 ** minimize_scalar(f, bounds=(-11.5, -9.0), method="bounded", options=dict(xatol=1e-8)).x
kap, inj = [], []
for ud in (0.5, 0.6, 0.7):
    Xs, Ys, _ = build(ud, 0.7); ms = Xs < 0.1 * A0
    kap.append(fit(Xs[ms], Ys[ms]) / A_L)
    for fac in (0.7, 1.0, 1.3):
        inj.append(fit(Xs[ms], Xs[ms] * nu(Xs[ms] / (fac * A0))) / (fac * A0))
P(f"    kappa (g_bar < 0.1 a0, every ring, unweighted) at Upsilon_disc = 0.5/0.6/0.7: " + " / ".join(f"{k:.3f}" for k in kap))
check("D6 (pre-stated, NOT load-bearing) the in-force kernel on L06's rings gives kappa in 0.40-0.60 for Upsilon_disc 0.5-0.7",
      f"kappa {min(kap):.3f}-{max(kap):.3f}", 0.40 < min(kap) and max(kap) < 0.60,
      "a FAIL here is an against-interest finding about the deep band; D7 diagnoses it", load_bearing=False)

banner("D7  WHY: POINT QUALITY AND WEIGHTING (the SPARC files carry the velocity errors the corpus rings drop)")
rows = []
for ud in (0.5, 0.6, 0.7):
    X_, Y_, E_ = [], [], []
    for f in sorted(glob.glob(os.path.join(ROOT, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
        r = np.genfromtxt(f, comments="#")
        if r.ndim != 2 or r.shape[1] < 6: continue
        R, V, eV, Vg, Vd, Vb = (r[:, i] for i in range(6))
        ok = (R > 0) & (V > 0) & (eV > 0)
        vb2 = np.sign(Vg) * Vg ** 2 + ud * Vd ** 2 + 0.7 * Vb ** 2
        ok &= vb2 > 0
        X_.append(vb2[ok] / (R[ok] * KPC) * 1e6); Y_.append((V[ok] * 1e3) ** 2 / (R[ok] * KPC)); E_.append(eV[ok] / V[ok])
    X_, Y_, E_ = np.concatenate(X_), np.concatenate(Y_), np.concatenate(E_)
    m_ = X_ < 0.1 * A0
    sig = 2 * E_ / math.log(10)
    rows.append((ud, fit(X_[m_], Y_[m_]) / A_L, fit(X_[m_ & (E_ < 0.1)], Y_[m_ & (E_ < 0.1)]) / A_L,
                 fit(X_[m_], Y_[m_], 1 / (sig[m_] ** 2 + 0.034 ** 2)) / A_L, int(m_.sum()), int((m_ & (E_ < 0.1)).sum())))
for ud, a, b, c, n1, n2 in rows:
    P(f"    Upsilon_disc = {ud}: every point unweighted {a:.3f} (N {n1});  err/V < 10% {b:.3f} (N {n2});  every point error-weighted {c:.3f}")
check("D7 the low deep-band values come from equal weight on poor points: the quality cut or error weighting raises kappa by >= 0.05 at every Upsilon, to 0.43-0.56",
      "; ".join(f"U={r[0]}: {r[1]:.3f} -> {r[2]:.3f} / {r[3]:.3f}" for r in rows),
      all(min(r[2], r[3]) - r[1] >= 0.05 for r in rows) and all(0.42 < x < 0.57 for r in rows for x in (r[2], r[3])), load_bearing=False)
check("D7b the fit is not an echo: it returns an injected a0 (0.7, 1.0, 1.3 x canonical) to < 0.1 per cent on the real g_bar",
      f"worst {max(abs(v - 1) for v in inj) * 100:.3f}%", max(abs(v - 1) for v in inj) < 1e-3, load_bearing=False)

banner("VERDICT")
nfail = sum(1 for _, ok, lb in CH if not ok and lb)
nfail_all = sum(1 for _, ok, _lb in CH if not ok)
P("  The 'SPARC-deep a0_eff = 0.72 a0' that anchors O04b's 'joint 0.7172 +/- 0.0593, 4.77 sigma below canonical' is reproduced exactly")
P("  from its inputs (D1) and is carried by the corpus v7 per-galaxy disc mass-to-light ratios (median 1.17, up to 15 on gas-rich")
P("  dwarfs, applied to bulges too) that multiply SPARC's own 3.6-micron curves (D2, D3).  With 3.6-micron population ratios the same")
P("  statistic on the same rings is 1.6-1.9 (D4), and even that is not the kernel's a0: the estimator is biased high by ~20 per cent for")
P("  data obeying the in-force kernel (D5).  So O04b is not a measurement of a0 against the canonical value, and the downstream")
P("  'a0* ~ 6.0-6.8e-11' (N01, ZD07-ZD11) inherits the artefact.")
P("  AGAINST INTEREST (D6, D7): read with the in-force kernel, the deep band is NOT a clean confirmation of 1/2 either.  On L06's rings,")
P("  every point unweighted, kappa = 0.34-0.44; with the standard quality cut or error weighting, 0.43-0.56.  The deep band measures")
P("  kappa only to about +/-0.1 once point selection is varied -- far from the 4.77 sigma claimed, in either direction.")
P("  The two other O04b channels (dwarfs 0.64 +/- 0.16, Milky Way 0.80 +/- 0.24) are each within 2 sigma of 1 and use their own inputs.")
P(f"\n  {len(CH) - nfail_all}/{len(CH)} checks pass; load-bearing failures: {nfail}" + (" (MUTATE run: D1 must fail)" if MUTATE else ""))
json.dump({"mutate": MUTATE, "checks": {n: {"ok": ok, "load_bearing": lb} for n, ok, lb in CH}, "claim_reproduced": r_claim, "standard_ratio_values": {f"{k[0]}/{k[1]}": v[0] for k, v in res4.items()},
           "moment_bias_on_kernel_data": res5, "kappa_deep_band_L06_rings_unweighted": kap, "kappa_deep_band_by_selection": rows},
          open(os.path.join(HERE, "D01_results" + ("_MUTATE" if MUTATE else "") + ".json"), "w"), indent=1, default=float)
sys.exit(1 if nfail else 0)
