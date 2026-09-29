#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG165 attacks (a)-(d) on CFG160, exactly as frozen in CFG165_FROZEN_CRITERIA.md section 6.  Labelled sensitivity grids,
not new headlines.  ZF_REPO=<repo> python3 CFG165_attacks_abcd.py > CFG165_attacks.out ; rc 0 always."""
import os
import sys
import json
import math
import csv
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
import CFG165_referee_kurvs_p4 as M

P = lambda *a: print(*a, flush=True)
S = M.load_kurvs()
AS = M.load_sparc_anchor()
SP = M.SP
OUT = {}
DEC = M.DEC
xK = S.R / S.Reff - 1
p4 = SP["P4"]


def dec_cell(sp, sp_anchor=None, mu=0.67, gas_scale=2.0, S_=None):
    c = M.cell(S_ or S, AS, sp, mu, 0.0, "canonical", sp_anchor=sp_anchor, gas_scale=gas_scale)
    return c


def fmt(c):
    return (f"flat {c['flat']['dprime']:+.3f} +-{c['flat']['sigma']:.3f} ({c['flat']['z']:+.2f}s)  rival {c['H']['dprime']:+.3f} "
            f"+-{c['H']['sigma']:.3f} ({c['H']['z']:+.2f}s)  -> {M.classify(c['flat']['z'], c['H']['z'])}")


def grid_lean_count(sp, sp_anchor=None):
    n = 0
    for mu in M.MUS:
        for dl in M.DELS:
            for ft in M.FOOTS:
                c = M.cell(S, AS, sp, mu, dl, ft, sp_anchor=sp_anchor)
                n += M.classify(c["flat"]["z"], c["H"]["z"]) == "lean rival"
    return n


# =========================================================================================================== (a)
P("=" * 100 + "\n(a) FORKING PATHS: alternative alpha(x) shapes / normalisation / R_e,gas / P3 (labelled sensitivity grid)\n" + "=" * 100)
med_p4 = float(np.median(M.alpha_K(xK)))
P(f"median alpha over the ten (P4) = {med_p4:.3f}")
shapes = {
    "Kretschmer table (primary)": lambda x: M.alpha_K(x),
    "linear 1.475+1.204x": lambda x: 1.475 + 1.204 * np.clip(x, 0, 4),
    "abstract-linear 1+0.75x": lambda x: 1.0 + 0.75 * np.clip(x, 0, 4),
    "self-grav shape rescaled 1.265 R/Re": lambda x: 1.265 * (np.clip(x, 0, 4) + 1),
    "constant 1": lambda x: 1.0 + 0 * x,
    "constant 2": lambda x: 2.0 + 0 * x,
    "constant 2.53": lambda x: 2.533 + 0 * x,
    "constant 3": lambda x: 3.0 + 0 * x,
    "constant 3.955": lambda x: 3.955 + 0 * x,
    "table, held flat beyond x=3": lambda x: M.alpha_K(np.minimum(x, 3.0)),
    "table at x+0.5": lambda x: M.alpha_K(x + 0.5),
    "table at x-0.5": lambda x: M.alpha_K(x - 0.5),
}
resA = {}
P("\n-- decision cell, shape variants (anchor uses the same shape)")
for nm, f in shapes.items():
    sp = M.spec("alpha", fn=(lambda f_: (lambda S_, anc: f_(S_.R / S_.Reff - 1.0)))(f))
    c = dec_cell(sp)
    med = float(np.median(f(xK)))
    ratio = med / med_p4
    cls = M.classify(c["flat"]["z"], c["H"]["z"])
    resA[nm] = dict(median_alpha=med, ratio=ratio, flat=c["flat"]["dprime"], H=c["H"]["dprime"], zf=c["flat"]["z"], zh=c["H"]["z"], cls=cls)
    P(f"  {nm:38s} med alpha {med:5.2f} (x{ratio:4.2f})  {fmt(c)}")
OUT["a_shapes"] = resA
inband = [k for k, v in resA.items() if 0.75 <= v["ratio"] <= 1.25]
fail_shape = [k for k in inband if resA[k]["cls"] != "lean rival"]
P(f"  shapes within x[0.75,1.25] of P4's median alpha: {inband}")
P(f"  of these, class != 'lean rival': {fail_shape}")
P(f"  (a1) PRE-DECLARED TEST 'lean is not a forking-path artefact of the alpha shape': {'PASS' if not fail_shape else 'FAIL'}")

P("\n-- normalisation scan s (alpha x s), decision cell; break-even s")
scan = {}
for s_ in (0.3, 0.5, 0.6, 0.75, 1.0, 1.25, 1.4):
    c = dec_cell(M.spec("P4", scale=s_))
    scan[s_] = (c["flat"]["dprime"], c["H"]["dprime"], c["flat"]["z"], c["H"]["z"], M.classify(c["flat"]["z"], c["H"]["z"]))
    P(f"  s={s_:4.2f}: {fmt(c)}")
OUT["a_scale"] = scan


def f_flat(s_):
    return dec_cell(M.spec("P4", scale=s_))["flat"]["dprime"]


def f_h(s_):
    return dec_cell(M.spec("P4", scale=s_))["H"]["dprime"]


try:
    sb_f = brentq(f_flat, 0.0, 1.0)
except Exception:
    sb_f = float("nan")
try:
    sb_h = brentq(f_h, 0.5, 2.0)
except Exception:
    sb_h = float("nan")
P(f"  break-even s: flat Delta'=0 at s={sb_f:.3f} [hand est 0.3]; rival Delta'=0 at s={sb_h:.3f} [hand est 0.96]")
# scale at which flat drops below +2 sigma
try:
    sb_f2 = brentq(lambda s_: dec_cell(M.spec("P4", scale=s_))["flat"]["z"] - 2.0, 0.0, 1.0)
except Exception:
    sb_f2 = float("nan")
P(f"  flat falls below +2s (z=2) at s={sb_f2:.3f}")
OUT["a_breakeven_s"] = dict(flat=sb_f, rival=sb_h, flat_2sigma=sb_f2)

P("\n-- R_e,gas / R_eff scan (KURVS only; anchor unchanged)")
rescan = {}
for k in (1.0, 1.25, 1.5, 2.0, 3.0):
    c = dec_cell(M.spec("P4", Refac=k))
    rescan[k] = (c["flat"]["dprime"], c["H"]["dprime"], c["flat"]["z"], c["H"]["z"])
    P(f"  R_e/R_eff={k:4.2f}: {fmt(c)}")
OUT["a_Re"] = rescan

P("\n-- P3 at the decision cell (the 'first reading favouring the rival' check)")
c3 = dec_cell(SP["P3"])
c4 = dec_cell(p4)
c2 = dec_cell(SP["P2"])
P(f"  P2: {fmt(c2)}\n  P3: {fmt(c3)}\n  P4: {fmt(c4)}")
OUT["a_P3_vs_P4"] = dict(P3=dict(flat=c3["flat"]["dprime"], H=c3["H"]["dprime"], zf=c3["flat"]["z"], zh=c3["H"]["z"], cls=M.classify(c3["flat"]["z"], c3["H"]["z"])),
                         P4=dict(flat=c4["flat"]["dprime"], H=c4["H"]["dprime"], zf=c4["flat"]["z"], zh=c4["H"]["z"], cls=M.classify(c4["flat"]["z"], c4["H"]["z"])))
P(f"  lean-rival cells in the 24-cell grid: P3 {grid_lean_count(SP['P3'])}, P4 {grid_lean_count(p4)}, P2 {grid_lean_count(SP['P2'])}")
OUT["a_lean_rival_cells"] = dict(P2=grid_lean_count(SP["P2"]), P3=grid_lean_count(SP["P3"]), P4=grid_lean_count(p4))

# =========================================================================================================== (b)
P("\n" + "=" * 100 + "\n(b) GAS PRIOR: molecular-only mu=0.67 vs total (molecular + HI), repo data only\n" + "=" * 100)


def fl(x):
    try:
        return float(x)
    except Exception:
        return float("nan")


ph = list(csv.DictReader(open(os.path.join(M.REPO, "data_assembly/kmos3d_phibss/phibss13_joined.csv"))))
mu_ph = []
for r in ph:
    m, ms, z = fl(r["mmol_msun"]), fl(r["mstar_msun"]), fl(r["z_co"])
    if np.isfinite(m) and np.isfinite(ms) and ms > 0 and 9.5 <= math.log10(ms) <= 10.6 and 0.9 <= z <= 2.4 and int(fl(r["co_upper_limit"]) or 0) == 0:
        mu_ph.append(m / ms)
sh = list(csv.DictReader(open(os.path.join(M.REPO, "data_assembly/arxiv_tables/sharma2024_gs21b.csv"))))
mu_h2, mu_hi = [], []
for r in sh:
    ms, h2, hi = fl(r["Mstar"]), fl(r["MH2"]), fl(r["MHI"])
    if r["Mstar_flag"] == "OK" and np.isfinite(ms) and ms > 0 and 9.5 <= math.log10(ms) <= 10.6 and np.isfinite(h2) and np.isfinite(hi):
        mu_h2.append(h2 / ms)
        mu_hi.append(hi / ms)


def q(a):
    a = np.array(a)
    return (len(a), float(np.percentile(a, 16)), float(np.median(a)), float(np.percentile(a, 84))) if len(a) else (0, nan, nan, nan)


nan = float("nan")
qph, qh2, qhi = q(mu_ph), q(mu_h2), q(mu_hi)
P(f"  PHIBSS (z 0.9-2.4, logM* 9.5-10.6, CO-detected, CO-selected so biased high): n={qph[0]}  M_mol/M* 16/50/84% = {qph[1]:.2f} / {qph[2]:.2f} / {qph[3]:.2f}")
P(f"  Sharma+2024 (z 0.76-1.04, logM* 9.5-10.6, Mstar_flag OK; values are the paper's fitted/stacked gas, not per-galaxy detections): n={qh2[0]}  M_H2/M* {qh2[1]:.2f} / {qh2[2]:.2f} / {qh2[3]:.2f};  M_HI/M* {qhi[1]:.2f} / {qhi[2]:.2f} / {qhi[3]:.2f}")
OUT["b_gas_repo"] = dict(phibss=qph, sharma_h2=qh2, sharma_hi=qhi)
tot_med = qh2[2] + qhi[2]
tot_ph = qph[2] + qhi[2]
cands = {"mol-only, paper 40% (decision cell)": 0.67, "PHIBSS median mol": qph[2], "Sharma median mol": qh2[2],
         "Sharma total (H2+HI) median": tot_med, "Sharma total, 16th pct": qh2[1] + qhi[1], "Sharma total, 84th pct": qh2[3] + qhi[3],
         "PHIBSS mol + Sharma HI (medians)": tot_ph}
P("\n-- decision cell at each repo-derived mu")
resB = {}
for nm, mu in cands.items():
    c = M.cell(S, AS, p4, mu, 0.0, "canonical")
    resB[nm] = dict(mu=mu, flat=c["flat"]["dprime"], H=c["H"]["dprime"], zf=c["flat"]["z"], zh=c["H"]["z"], cls=M.classify(c["flat"]["z"], c["H"]["z"]))
    P(f"  {nm:38s} mu={mu:5.2f}: {fmt(c)}")
OUT["b_decision_at_repo_mu"] = resB

P("\n-- gas-disc scale variants at mu_tot values (HI more extended than 2 R_d, so less enclosed at R_max)")
for gs in (2.0, 3.0, 4.0):
    for mu in (1.5, 2.0, 4.0):
        c = M.cell(S, AS, p4, mu, 0.0, "canonical", gas_scale=gs)
        P(f"  gas scale {gs:.0f} R_d, mu={mu:3.1f}: {fmt(c)}")
        OUT.setdefault("b_gas_scale", {})[f"{gs}|{mu}"] = (c["flat"]["dprime"], c["H"]["dprime"], c["flat"]["z"], c["H"]["z"])

P("\n-- log-mu grid: class and break-even mu (bootstrap of the ten galaxies, 2000 resamples, seed 165)")
lg = np.linspace(math.log10(0.1), math.log10(10.0), 41)
mug = 10 ** lg
POs = [M.per_object(S, p4, mu, 0.0, "canonical") for mu in mug]
ap = M.anchor_pool(p4, 0.0, "canonical", AS)["flat"]
base = []
for mu, po in zip(mug, POs):
    mf = M.pool(po["d_flat"], po["e_flat"])[0] - ap[0]
    mh = M.pool(po["d_H"], po["e_H"])[0] - ap[0]
    base.append((mf, mh))
base = np.array(base)


def crossing(y):
    idx = np.where((y[:-1] > 0) & (y[1:] <= 0))[0]
    if not len(idx):
        return float("nan")
    i = idx[0]
    t = y[i] / (y[i] - y[i + 1])
    return 10 ** (lg[i] + t * (lg[i + 1] - lg[i]))


be_f, be_h = crossing(base[:, 0]), crossing(base[:, 1])
rng = np.random.default_rng(165)
bf, bh = [], []
n = len(S.ids)
for _ in range(2000):
    ix = rng.integers(0, n, n)
    yf, yh = [], []
    for po in POs:
        yf.append(M.pool(po["d_flat"][ix], po["e_flat"][ix])[0] - ap[0])
        yh.append(M.pool(po["d_H"][ix], po["e_H"][ix])[0] - ap[0])
    bf.append(crossing(np.array(yf)))
    bh.append(crossing(np.array(yh)))
bf, bh = np.array(bf), np.array(bh)
pc = lambda a: tuple(float(np.nanpercentile(a, p)) for p in (16, 50, 84))
P(f"  break-even mu (Delta'=0): flat {be_f:.2f} (bootstrap 16/50/84: {pc(bf)}, nan-frac {np.mean(np.isnan(bf)):.2f});  rival {be_h:.2f} ({pc(bh)}, nan-frac {np.mean(np.isnan(bh)):.2f})   [hand est: flat 2.0, rival 0.65]")
OUT["b_breakeven_mu"] = dict(flat=be_f, rival=be_h, flat_boot=pc(bf), rival_boot=pc(bh))
mid = math.sqrt(be_f * be_h)
P(f"  geometric midpoint of the two break-evens = {mid:.2f}: total gas above it reads flat, below it reads rival")
tot_cls = resB["Sharma total (H2+HI) median"]["cls"]
q16 = resB["Sharma total, 16th pct"]["cls"]
P(f"  (b) PRE-DECLARED TEST 'lean rival persists at mu_tot from the repo data and its 16-84% range': {'PASS' if (tot_cls == 'lean rival' and q16 == 'lean rival' and resB['Sharma total, 84th pct']['cls'] == 'lean rival') else 'FAIL'}  (median-total class: {tot_cls})")

# =========================================================================================================== (c)
P("\n" + "=" * 100 + "\n(c) ANCHORS: SPARC and KROSS under a pressure correction of this size\n" + "=" * 100)
KR = M.load_kross()
P(f"  KROSS n={len(KR.ids)} (RT/RT+, v/sigma0>=1, finite M*, r_im, sigma0)")
a0 = M.per_object(AS, SP["P0"], None, 0.0, "canonical", anchor=True)
a4 = M.per_object(AS, p4, None, 0.0, "canonical", anchor=True)
a2 = M.per_object(AS, SP["P2"], None, 0.0, "canonical", anchor=True)
pl = lambda d, e: M.pool(d, e)
P(f"  (c1) SPARC anchor pooled Delta_flat: P0 {pl(a0['d_flat'], a0['e_flat'])[0]:+.3f}, P2 {pl(a2['d_flat'], a2['e_flat'])[0]:+.3f}, P4 {pl(a4['d_flat'], a4['e_flat'])[0]:+.3f}  (shift P0->P4 = {pl(a4['d_flat'], a4['e_flat'])[0]-pl(a0['d_flat'], a0['e_flat'])[0]:+.3f}; hand est +0.013 to +0.02)")
xA = AS.R / AS.Reff - 1
P(f"  SPARC anchor x range {xA.min():.2f}..{xA.max():.2f}, alpha {M.alpha_K(xA).min():.2f}..{M.alpha_K(xA).max():.2f}; median Vc2/V2 (P4) {np.median(a4['Vc2_over_V2']):.3f}, max {a4['Vc2_over_V2'].max():.3f}")
resC = {}
bins = [(-9, 1.5), (1.5, 2.5), (2.5, 99)]
for lo, hi in bins:
    m = (xA >= lo) & (xA < hi)
    if m.sum() > 2:
        P(f"  anchor x in [{lo},{hi}): n={m.sum():2d}  pooled Delta_flat P0 {pl(a0['d_flat'][m], a0['e_flat'][m])[0]:+.3f}  P4 {pl(a4['d_flat'][m], a4['e_flat'][m])[0]:+.3f}")
P("  anchor sigma sensitivity (sigma_anchor km/s -> anchor pooled offset and decision-cell Delta'_flat / rival):")
for sg in (7.0, 10.0, 15.0):
    AS2 = M.load_sparc_anchor()
    AS2.sig0 = np.full(len(AS2.ids), sg)
    AS2.sig = AS2.sig0.copy()
    c = M.cell(S, AS2, p4, 0.67, 0.0, "canonical")
    P(f"    sigma={sg:4.1f}: anchor {c['flat']['anchor']:+.3f}   Delta'_flat {c['flat']['dprime']:+.3f} ({c['flat']['z']:+.2f}s)  Delta'_H {c['H']['dprime']:+.3f} ({c['H']['z']:+.2f}s)")
    resC[f"sigma_anchor_{sg}"] = (c["flat"]["anchor"], c["flat"]["dprime"], c["H"]["dprime"])

P("\n  (c3) KURVS - KROSS differential (raw pooled Delta, mu=0.67 both, canonical; anchor cancels)")
diffs = {}
for nm in ("P0", "P1", "P2", "P4"):
    sp = p4 if nm == "P4" else SP[nm]
    ck = M.per_object(S, sp, 0.67, 0.0, "canonical")
    cr = M.per_object(KR, sp, 0.67, 0.0, "canonical")
    kf, ke, _ = M.pool(ck["d_flat"], ck["e_flat"])
    kh, keh, _ = M.pool(ck["d_H"], ck["e_H"])
    rf, re_, _ = M.pool(cr["d_flat"], cr["e_flat"])
    rh, reh, _ = M.pool(cr["d_H"], cr["e_H"])
    diff = kf - rf
    de = math.sqrt(ke ** 2 + re_ ** 2)
    pred_rival = (kf - kh) - (rf - rh)
    zflat = diff / de
    zriv = (diff - pred_rival) / de
    anc = M.anchor_pool(sp, 0.0, "canonical", AS)["flat"]
    ka = math.sqrt(re_ ** 2 + anc[1] ** 2)
    ka_h = math.sqrt(reh ** 2 + anc[1] ** 2)
    diffs[nm] = dict(kurvs=kf, kross=rf, diff=diff, err=de, pred_rival=pred_rival, z_vs_flat=zflat, z_vs_rival=zriv, kross_H=rh,
                     kross_dprime_flat=rf - anc[0], kross_dprime_H=rh - anc[0], kross_sig=ka, kross_z_flat=(rf - anc[0]) / ka, kross_z_H=(rh - anc[0]) / ka_h)
    P(f"   {nm}: Delta_flat KURVS {kf:+.3f}+-{ke:.3f}, KROSS {rf:+.3f}+-{re_:.3f} (n={len(KR.ids)}); differential {diff:+.3f} +-{de:.3f}; flat predicts 0 ({zflat:+.1f}s), rival predicts {pred_rival:+.3f} ({zriv:+.1f}s from it)")
    P(f"        KROSS anchor-corrected Delta': flat {rf-anc[0]:+.3f} ({(rf-anc[0])/ka:+.1f}s)  rival {rh-anc[0]:+.3f} ({(rh-anc[0])/ka_h:+.1f}s)   [KROSS median z {np.median(KR.z):.2f}; the stellar-mass-only P0 is the no-correction scenario]")
OUT["c_differential"] = diffs
okdiff = abs(diffs["P4"]["z_vs_flat"]) <= 2 and abs(diffs["P4"]["z_vs_rival"]) <= 2
P(f"   (c3) PRE-DECLARED TEST P4 differential within 2s of BOTH flat and rival predictions: {'CONSISTENT' if okdiff else 'FAIL'} (z vs flat {diffs['P4']['z_vs_flat']:+.1f}, vs rival {diffs['P4']['z_vs_rival']:+.1f}; FAIL-flat if |z vs flat| > 2)")

P("\n  (c4) size of the correction: Vc/V - 1")
for nm, Sx, sp in (("KURVS P4", S, p4), ("KURVS P2", S, SP["P2"]), ("KURVS P3", S, SP["P3"]), ("KROSS P4", KR, p4), ("KROSS P1", KR, SP["P1"])):
    po = M.per_object(Sx, sp, 0.67, 0.0, "canonical")
    r = np.sqrt(po["Vc2_over_V2"]) - 1
    P(f"   {nm}: min {r.min():.2f}, median {np.median(r):.2f}, max {r.max():.2f}; fraction above 0.87: {np.mean(r > 0.87):.2f}; count above 0.87: {int((r > 0.87).sum())}/{len(r)}")
    resC[f"size_{nm}"] = (float(r.min()), float(np.median(r)), float(r.max()), int((r > 0.87).sum()))
OUT["c_misc"] = resC
po4 = M.per_object(S, p4, 0.67, 0.0, "canonical")
P(f"   (c4) PRE-DECLARED TEST P4 max Vc/V-1 <= 0.87 (Sharma+2021's 10-87% per the repo's ONE_OFF note): {'PASS' if (np.sqrt(po4['Vc2_over_V2']) - 1).max() <= 0.87 else 'FAIL'}")

# =========================================================================================================== (d)
P("\n" + "=" * 100 + "\n(d) RANGE AND SCATTER AT R_max\n" + "=" * 100)
P(f"  x = R_max/R_eff - 1 range {xK.min():.2f}..{xK.max():.2f}; galaxies outside [0,4]: {int(np.sum((xK < 0) | (xK > 4)))}; alpha clipped == unclipped: {bool(np.all(M.alpha_K(xK) == -0.146*xK**2 + 1.204*xK + 1.475))}")
P(f"  R_max/R_eff = {', '.join(f'{v:.2f}' for v in (S.R/S.Reff))}")
P(f"  log10 M* range {S.logM.min():.2f}..{S.logM.max():.2f} (Kretschmer profiles quoted above 10^9.5): {int(np.sum(S.logM < 9.5))} below")
P(f"  alpha(x=0)=1.475 (table) vs '~1 at R_e' (abstract as quoted): ratio {1.475/1.0:.3f}; alpha(x=4)=3.955 vs '4': fine")
lg_x = np.argsort(-xK)
P("  largest x: " + ", ".join(f"{S.name[j]}({xK[j]:.2f})" for j in lg_x[:4]) + "  | README claims 13, 17, 21 'have the largest x' -> " + ("13 is 4th" if list(np.argsort(-xK)[:3]) != [S.ids.index(21), S.ids.index(8), S.ids.index(17)] else ""))
P("  (d2) x shifts / hold-flat beyond x=3 are in the (a) table above")

P("\n  (d3) scatter as a RANDOM per-galaxy lognormal(0,0.4) on alpha (20000 draws, seed 165) vs CFG160's coherent x0.6/x1.4")
rng = np.random.default_rng(165)
al0 = M.alpha_K(xK)
res_mc = []
for _ in range(20000):
    al = al0 * np.exp(rng.normal(0, 0.4, len(al0)))
    sp = M.spec("alpha", fn=(lambda a_: (lambda S_, anc: a_ if not anc else M.alpha_K(S_.R / S_.Reff - 1)))(al))
    c = M.cell(S, AS, sp, 0.67, 0.0, "canonical", sp_anchor=p4)
    res_mc.append((c["flat"]["dprime"], c["H"]["dprime"]))
res_mc = np.array(res_mc)
sdf, sdh = res_mc[:, 0].std(), res_mc[:, 1].std()
c4d = dec_cell(p4)
sig_eff_f = math.sqrt(c4d["flat"]["sigma"] ** 2 + sdf ** 2)
sig_eff_h = math.sqrt(c4d["H"]["sigma"] ** 2 + sdh ** 2)
P(f"   MC mean Delta'_flat {res_mc[:,0].mean():+.3f} sd {sdf:.3f}; Delta'_H {res_mc[:,1].mean():+.3f} sd {sdh:.3f}   [hand est extra sd 0.027]")
P(f"   sigma inflated {c4d['flat']['sigma']:.3f} -> {sig_eff_f:.3f}: z_flat {c4d['flat']['dprime']/sig_eff_f:+.2f}, z_H {c4d['H']['dprime']/sig_eff_h:+.2f}  [hand est 2.8, -0.1]")
zf_e, zh_e = c4d["flat"]["dprime"] / sig_eff_f, c4d["H"]["dprime"] / sig_eff_h
cls_e = M.classify(zf_e, zh_e)
P(f"   class under random-scatter-inflated errors: {cls_e}")
OUT["d_random_scatter"] = dict(sd_flat=float(sdf), sd_H=float(sdh), sig_eff_flat=sig_eff_f, sig_eff_H=sig_eff_h, z_flat=zf_e, z_H=zh_e, cls=cls_e)
top3_ok = [S.name[j] for j in np.argsort(-np.abs(po4["d_flat"] - np.median(po4["d_flat"])))[:3]]
P(f"   (d) PRE-DECLARED TEST no galaxy outside [0,4]: PASS; class unchanged under random-scatter inflation: {'PASS' if cls_e == 'lean rival' else 'FAIL'}; 'largest x = 13, 17, 21' statement: {'PASS' if set(S.name[j] for j in lg_x[:3]) == {'KURVS-13','KURVS-17','KURVS-21'} else 'FAIL (largest x are ' + ', '.join(S.name[j] for j in lg_x[:3]) + ')'}")

json.dump(OUT, open(os.path.join(M.HERE, "CFG165_attacks_results.json"), "w"), indent=1,
          default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
P("\nwritten CFG165_attacks_results.json")
