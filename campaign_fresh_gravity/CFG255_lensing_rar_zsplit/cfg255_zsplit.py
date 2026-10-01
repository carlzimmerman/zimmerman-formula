#!/usr/bin/env python3
"""CFG255 -- does the KiDS-1000 lensing signal at fixed g_bar change with lens redshift as a0 proportional to H(z) predicts?

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG255_lensing_rar_zsplit/FROZEN_CRITERIA.md (8c925db21).
  data     cfg110_perlens.npz (CFG110's per-lens sums of the June KiDS-1000 estimator), lr_lenses.npz, the 50 June patches.
  split    within each colour class: high-z third (z >= class 2/3 quantile) minus low-z third (z < class 1/3 quantile); K1 = bins 8-14.
  models   FLAT = CFG61's law stack (both footings); RIVAL = the same with every profile rebuilt at a0 * E(z_grid) (truncation too);
           LCDM = CFG67's colour-split stack (reported; its tables carry no z dependence beyond the lens mass distribution).
  STAGE=A  the pre-flight: power and amplitude gap from the jackknife covariance alone (D never printed); declared M* drift scenarios.
  STAGE=B  the measurement (run only after stage A is committed).
  MUTATE=1 (stage B): the high-z third's wgE times the model ratio [RIVAL(hi)/RIVAL(lo)] / [FLAT(hi)/FLAT(lo)] (canonical).
Run: STAGE=A python3 campaign_fresh_gravity/CFG255_lensing_rar_zsplit/cfg255_zsplit.py ; then STAGE=B (and STAGE=B MUTATE=1)
"""
import os, sys, io, json, math, time, contextlib
import numpy as np
from scipy.stats import chi2 as CHI2, norm

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
STAGE = os.environ.get("STAGE", "").strip().upper()
MUTATE = os.environ.get("MUTATE", "0") == "1"
assert STAGE in ("A", "B"), "set STAGE=A or STAGE=B"
assert not (MUTATE and STAGE == "A"), "MUTATE applies to stage B only"
SFX = f"_stage{STAGE}" + ("_MUTATE1" if MUTATE else "")
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok, load_bearing=True):
    CHK.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


P(__doc__.split("Run:")[0].strip())
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: the rival's predicted high/low ratio injected into the high-z third -- stage B must reject FLAT ***" if MUTATE else ""))


def lane_prefix(fname, marker):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    src = open(os.path.join(CFG, fname)).read()
    g = {"__file__": os.path.join(CFG, fname), "__name__": "lane_" + fname}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:src.index(marker)], fname, "exec"), g)
    finally:
        os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return g


# ------------------------------------------------------------------ data
LR = os.path.join(REPO, "real_research", "data", "lensing_rar")
PL = np.load(os.path.join(LR, "cfg110_perlens.npz"))
LN = np.load(os.path.join(LR, "lr_lenses.npz"))
J = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))
KG = 1.989e30 / (3.0857e16) ** 2
WG, WW, NNL = PL["WG"].astype(float), PL["WW"].astype(float), PL["NN"].astype(float)
typ, Mgal, zlen = LN["typ"], LN["Mgal"], LN["z"]
patch = J["patch"]
NPAT, K1 = 50, [8, 9, 10, 11, 12, 13, 14]
HART = (NPAT - 14 - 2) / (NPAT - 1)
FOOTS = ("canonical", "alt")
Q1 = {c: float(np.quantile(zlen[typ == c], 1 / 3)) for c in (0, 1)}
Q2 = {c: float(np.quantile(zlen[typ == c], 2 / 3)) for c in (0, 1)}
HI = {c: (typ == c) & (zlen >= Q2[c]) for c in (0, 1)}
LO = {c: (typ == c) & (zlen < Q1[c]) for c in (0, 1)}
E = lambda z: math.sqrt(0.3 * (1 + z) ** 3 + 0.7)

P("\nC1 / C2  CONTROLS (data)")
dev = 0.0
for A, Jk in ((WG, "wgE"), (WW, "W"), (NNL, "NN")):
    S = np.zeros((NPAT, 2, 15)); np.add.at(S, (patch, typ), A)
    dev = max(dev, float(np.max(np.abs(S - J[Jk]) / np.maximum(np.abs(J[Jk]), 1e-300))))
check("C1 CONTROL: per-lens sums reproduce the June per-patch sums to 1e-9 relative", f"max relative deviation {dev:.1e}", dev < 1e-9)
fr = {c: (HI[c].sum() / (typ == c).sum(), LO[c].sum() / (typ == c).sum()) for c in (0, 1)}
c2 = all(not np.any(HI[c] & LO[c]) and all(abs(f - 1 / 3) < 0.01 for f in fr[c]) for c in (0, 1))
check("C2 CONTROL: the thirds are disjoint and each holds 1/3 of its class to 1%",
      "; ".join(f"class {c}: z < {Q1[c]:.3f} ({fr[c][1]:.3f}) / z >= {Q2[c]:.3f} ({fr[c][0]:.3f}); median z lo {np.median(zlen[LO[c]]):.3f}, "
                f"hi {np.median(zlen[HI[c]]):.3f}" for c in (0, 1)), c2)

# ------------------------------------------------------------------ models (read-only reuse of CFG61 / CFG67)
g61 = lane_prefix("CFG61_kids_colour_split.py", "\nRES = {}\n")
PROF, LMG, ZG, RG, EDGES, SUB = g61["PROF"], g61["LMG"], g61["ZG"], g61["RG"], g61["EDGES"], g61["SUB"]
fcold, G_SI, MSUN, MPC, im61, iz61, Mg61 = g61["fcold"], g61["G_SI"], g61["MSUN"], g61["MPC"], g61["im"], g61["iz"], g61["Mg"]
assert np.array_equal(Mg61, Mgal) and np.array_equal(g61["typ"], typ)
C61 = g61["C"]
g67 = lane_prefix("CFG67_lcdm_control_kids_split.py", "def stack(cls, kind, dshift=0):")
TAB, im67 = g67["TAB"], g67["im"]
LRG = np.log(RG)


def rival_prof(scale_fn):
    """Rebuild the red law profiles with a0 -> a0(foot) * scale_fn(z) (truncation included); restores C.A0 afterwards."""
    base = dict(C61.A0); out = {}
    try:
        for foot in FOOTS:
            for z in ZG:
                C61.A0[foot] = base[foot] * scale_fn(float(z))
                for lm in LMG:
                    out[(foot, "red", lm, z)] = g61["profiles"](lm, z, foot, "red")
                C61.A0[foot] = base[foot]
    finally:
        C61.A0.clear(); C61.A0.update(base)
    return out


def law_stack(mask, foot, prof):
    w = np.zeros((len(LMG), len(ZG)))
    np.add.at(w, (im61[mask], iz61[mask]), Mg61[mask])
    out = np.zeros(15)
    for k in range(15):
        lg = np.linspace(math.log(EDGES[k]), math.log(EDGES[k + 1]), SUB + 1)
        gs = np.exp(0.5 * (lg[1:] + lg[:-1]))
        num = den = 0.0
        for a in range(len(LMG)):
            for b in range(len(ZG)):
                if w[a, b] <= 0: continue
                Mtab = 10 ** LMG[a] * (1 + fcold(LMG[a]))
                pr = prof[(foot, "red", LMG[a], ZG[b])]
                Rj = np.sqrt(G_SI * Mtab * MSUN / gs) / MPC
                ds = np.interp(np.log(Rj), LRG, pr["dsL"]) + pr["Mb"] / (math.pi * Rj ** 2)
                wj = w[a, b] / gs
                num += float(np.sum(wj * ds)); den += float(np.sum(wj))
        out[k] = num / den / 1e12
    return out


def lcdm_stack(mask, kind):
    w = np.zeros(len(LMG)); np.add.at(w, im67[mask], Mgal[mask])
    out = np.zeros(15)
    for k in range(15):
        lg = np.linspace(math.log(EDGES[k]), math.log(EDGES[k + 1]), 9)
        gs = np.exp(0.5 * (lg[1:] + lg[:-1]))
        num = den = 0.0
        for a in range(len(LMG)):
            if w[a] <= 0: continue
            Mtab = 10 ** LMG[a] * (1 + fcold(LMG[a])); pr = TAB[kind][LMG[a]]
            Rj = np.sqrt(G_SI * Mtab * MSUN / gs) / MPC
            ds = np.interp(np.log(Rj), LRG, pr["ds"]) + pr["Mb"] / (math.pi * Rj ** 2)
            num += float(np.sum(w[a] / gs * ds)); den += float(np.sum(w[a] / gs))
        out[k] = num / den / 1e12
    return out


P("\nC3 / C4  CONTROLS (models)")
c61 = json.load(open(os.path.join(CFG, "CFG61_kids_colour_split_results.json")))["numbers"]["RES"]["canonical"]
full = {c: typ == c for c in (0, 1)}
d3 = max(float(np.max(np.abs(law_stack(full[0], "canonical", PROF) / np.array(c61["ml"]) - 1))),
         float(np.max(np.abs(law_stack(full[1], "canonical", PROF) / np.array(c61["me"]) - 1))))
check("C3 CONTROL: the FLAT machinery reproduces CFG61's committed law stacks (canonical, both classes) to 1e-9", f"max relative deviation {d3:.1e}", d3 < 1e-9)
PROF1 = rival_prof(lambda z: 1.0)
d4 = max(float(np.max(np.abs(law_stack(m, f, PROF1) / law_stack(m, f, PROF) - 1))) for m in (HI[0], LO[1]) for f in FOOTS)
check("C4 CONTROL: the RIVAL machinery with E(z) = 1 reproduces FLAT to 1e-9", f"max relative deviation {d4:.1e}", d4 < 1e-9)
PROFR = rival_prof(E)
P(f"  rival profiles rebuilt at a0 x E(z) on z grid {ZG.tolist()} (E = {[round(E(z), 3) for z in ZG]})  [{time.time() - T0:.0f} s]")
KIND = {0: "blue", 1: "red"}
MOD = {"FLAT": {}, "RIVAL": {}, "HL": {}}
for f in FOOTS:
    MOD["FLAT"][f] = np.concatenate([(law_stack(HI[c], f, PROF) - law_stack(LO[c], f, PROF))[K1] for c in (0, 1)])
    MOD["RIVAL"][f] = np.concatenate([(law_stack(HI[c], f, PROFR) - law_stack(LO[c], f, PROFR))[K1] for c in (0, 1)])
    MOD["HL"][f] = {c: dict(Fh=law_stack(HI[c], f, PROF)[K1], Fl=law_stack(LO[c], f, PROF)[K1],
                            Rh=law_stack(HI[c], f, PROFR)[K1], Rl=law_stack(LO[c], f, PROFR)[K1]) for c in (0, 1)}
MOD["LCDM"] = np.concatenate([(lcdm_stack(HI[c], KIND[c]) - lcdm_stack(LO[c], KIND[c]))[K1] for c in (0, 1)])
LHL = {c: (lcdm_stack(HI[c], KIND[c])[K1], lcdm_stack(LO[c], KIND[c])[K1]) for c in (0, 1)}

# ------------------------------------------------------------------ data difference and jackknife
WGd = WG.copy()
if MUTATE:
    for c in (0, 1):
        h = MOD["HL"]["canonical"][c]
        ratio = (h["Rh"] / h["Rl"]) / (h["Fh"] / h["Fl"])
        idx = np.where(HI[c])[0]
        WGd[np.ix_(idx, K1)] = WG[np.ix_(idx, K1)] * ratio[None, :]


def esd_and_loo(mask, wg):
    g = wg[mask][:, K1]; w = WW[mask][:, K1]; pa = patch[mask]
    tg, tw = g.sum(0), w.sum(0)
    Sg = np.zeros((NPAT, len(K1))); Sw = np.zeros((NPAT, len(K1)))
    np.add.at(Sg, pa, g); np.add.at(Sw, pa, w)
    return tg / tw / KG, (tg[None] - Sg) / (tw[None] - Sw) / KG


def diff_vec(pairs, wg):
    D, L = [], []
    for A, B in pairs:
        ea, la = esd_and_loo(A, wg); eb, lb = esd_and_loo(B, wg)
        D.append(ea - eb); L.append(la - lb)
    return np.concatenate(D), np.concatenate(L, axis=1)


def jcov(L):
    Rr = L - L.mean(0); return (NPAT - 1) / NPAT * (Rr.T @ Rr)


def x2(r, Cm):
    return float(r @ np.linalg.solve(Cm, r)) * HART


pv = lambda x, k=14: float(CHI2.sf(x, k))
zs = lambda p: float(norm.isf(p / 2)) if p > 0 else float("inf")
PAIRS = [(HI[0], LO[0]), (HI[1], LO[1])]
D, L = diff_vec(PAIRS, WGd)            # D is NOT printed in stage A
Cm = jcov(L)

# amplitude: per class log10 of ratio of pair-weighted sums over K1, jackknife sigma; combined inverse-variance
wk = {c: NNL[typ == c][:, K1].sum(0) for c in (0, 1)}


def amp_from(hi, lo, c):
    return float(np.log10(np.sum(wk[c] * hi) / np.sum(wk[c] * lo)))


def data_amp(wg):
    out = {}
    for c in (0, 1):
        eh, lh = esd_and_loo(HI[c], wg); el, ll = esd_and_loo(LO[c], wg)
        a = amp_from(eh, el, c)
        reps = np.array([amp_from(lh[p], ll[p], c) for p in range(NPAT)])
        out[c] = (a, float(np.sqrt((NPAT - 1) / NPAT * np.sum((reps - reps.mean()) ** 2))))
    return out


AD = data_amp(WGd)
SIG = {c: AD[c][1] for c in (0, 1)}
wiv = {c: 1 / SIG[c] ** 2 for c in (0, 1)}
comb = lambda v: float(sum(wiv[c] * v[c] for c in (0, 1)) / sum(wiv.values()))
SIG_A = float(1 / math.sqrt(sum(wiv.values())))
AM = {}
for f in FOOTS:
    h = MOD["HL"][f]
    AM[("FLAT", f)] = comb({c: amp_from(h[c]["Fh"], h[c]["Fl"], c) for c in (0, 1)})
    AM[("RIVAL", f)] = comb({c: amp_from(h[c]["Rh"], h[c]["Rl"], c) for c in (0, 1)})
AM["LCDM"] = comb({c: amp_from(LHL[c][0], LHL[c][1], c) for c in (0, 1)})

# ================================================================== STAGE A
P("\nSTAGE A  THE PRE-FLIGHT (covariance and models only; the data difference D is not printed)")
rng = np.random.default_rng(255)
nulls = []
for t in range(200):
    pairs = []
    for c in (0, 1):
        idx = np.where(typ == c)[0]; u = rng.random(len(idx))
        A = np.zeros(len(typ), bool); B = np.zeros(len(typ), bool)
        A[idx[u < 1 / 3]] = True; B[idx[u > 2 / 3]] = True
        pairs.append((A, B))
    Dn, Ln = diff_vec(pairs, WG)
    nulls.append(x2(Dn, jcov(Ln)))
mn = float(np.mean(nulls))
check("C5 CONTROL: covariance calibration -- mean Hartlap chi2 of 200 random one-third vs one-third draws (14 bins) in [9.8, 18.2]",
      f"mean {mn:.2f}, median {np.median(nulls):.2f}, 16-84% {np.percentile(nulls, 16):.1f}-{np.percentile(nulls, 84):.1f}", 9.8 <= mn <= 18.2)
POW = {f: x2(MOD["RIVAL"][f] - MOD["FLAT"][f], Cm) for f in FOOTS}
DA = {f: AM[("RIVAL", f)] - AM[("FLAT", f)] for f in FOOTS}
check("A1 (pre-flight) power Delta chi2_pred(RIVAL vs FLAT) from the covariance alone; POSSIBLE_STAT needs >= 9 on both footings",
      "; ".join(f"{f}: {POW[f]:.2f}" for f in FOOTS) + f"  (LCDM vs FLAT canonical: {x2(MOD['LCDM'] - MOD['FLAT']['canonical'], Cm):.2f})", True, load_bearing=False)
check("A2 (pre-flight) amplitude gap Delta A = A_RIVAL - A_FLAT (dex, combined) against the jackknife sigma_A",
      "; ".join(f"{f}: A_FLAT {AM[('FLAT', f)]:+.4f}, A_RIVAL {AM[('RIVAL', f)]:+.4f}, gap {DA[f]:+.4f}" for f in FOOTS)
      + f"; A_LCDM {AM['LCDM']:+.4f}; sigma_A {SIG_A:.4f} (late {SIG[0]:.4f}, early {SIG[1]:.4f})", True, load_bearing=False)
POSS_STAT = all(POW[f] >= 9 for f in FOOTS)
POSS_SYS = {d: all(abs(DA[f]) >= 2 * math.sqrt(SIG_A ** 2 + (d / 2) ** 2) for f in FOOTS) for d in (0.0, 0.02, 0.05)}
check("A4 (pre-flight) DECISION", f"POSSIBLE_STAT {POSS_STAT}; POSSIBLE_SYS at delta = 0 / 0.02 / 0.05 dex: "
      f"{POSS_SYS[0.0]} / {POSS_SYS[0.02]} / {POSS_SYS[0.05]}  (delta = 0 is the statistics-only reference, not a scenario)", True, load_bearing=False)
NUM.update(power=POW, amp_models={f"{k[0]}_{k[1]}" if isinstance(k, tuple) else k: v for k, v in AM.items()}, sigma_A=SIG_A,
           sigma_A_class=SIG, null_mean=mn, possible_stat=POSS_STAT, possible_sys={str(k): v for k, v in POSS_SYS.items()},
           quantiles=dict(q1=Q1, q2=Q2), models={k: (v.tolist() if isinstance(v, np.ndarray) else {f: x.tolist() for f, x in v.items()})
                                                   for k, v in MOD.items() if k != "HL"})

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT")
    XS = {"zero": x2(D, Cm), "LCDM": x2(D - MOD["LCDM"], Cm)}
    for f in FOOTS:
        XS[f"FLAT_{f}"] = x2(D - MOD["FLAT"][f], Cm); XS[f"RIVAL_{f}"] = x2(D - MOD["RIVAL"][f], Cm)
    check("B1 chi2 of D (high-z third minus low-z third, K1, both classes; Hartlap, 14 dof)",
          "; ".join(f"{k} {v:.2f} (p {pv(v):.2e})" for k, v in XS.items())
          + f"\n         D late {np.round(D[:7], 3).tolist()} early {np.round(D[7:], 3).tolist()} (Msun/pc^2)"
          + f"\n         sigma late {np.round(np.sqrt(np.diag(Cm))[:7], 3).tolist()} early {np.round(np.sqrt(np.diag(Cm))[7:], 3).tolist()}",
          True, load_bearing=False)
    A_data = comb({c: AD[c][0] for c in (0, 1)})
    check("B2 amplitude A_data +- sigma_A (combined) against the models (dex)",
          f"A_data {A_data:+.4f} +- {SIG_A:.4f} (late {AD[0][0]:+.4f} +- {AD[0][1]:.4f}, early {AD[1][0]:+.4f} +- {AD[1][1]:.4f}); "
          + "; ".join(f"{f}: FLAT {AM[('FLAT', f)]:+.4f} ({(A_data - AM[('FLAT', f)]) / SIG_A:+.2f} sigma), RIVAL {AM[('RIVAL', f)]:+.4f} "
                      f"({(A_data - AM[('RIVAL', f)]) / SIG_A:+.2f} sigma)" for f in FOOTS)
          + f"; LCDM {AM['LCDM']:+.4f} ({(A_data - AM['LCDM']) / SIG_A:+.2f} sigma)", True, load_bearing=False)
    readings = {}
    for f in FOOTS:
        pf, pr = pv(XS[f"FLAT_{f}"]), pv(XS[f"RIVAL_{f}"]); dx = XS[f"RIVAL_{f}"] - XS[f"FLAT_{f}"]
        if pf > 0.01 and pr < 0.01 and dx >= 9: readings[f] = "FLAT-consistent, the rival disfavoured"
        elif pr > 0.01 and pf < 0.01 and -dx >= 9: readings[f] = "the rival favoured"
        else: readings[f] = "not separated"
    gated = [d for d in (0.02, 0.05) if POSS_SYS[d]]
    words = ("verdict words released at delta = " + ", ".join(map(str, gated))) if gated else \
        "NO verdict words: stage A gave POSSIBLE_SYS at no declared drift scenario, so the reading is DESCRIPTIVE ONLY"
    check("B3 the reading (by A4's gate)", "; ".join(f"{f}: {r}" for f, r in readings.items()) + f"\n         {words}", True, load_bearing=False)
    if MUTATE:
        rej = all(pv(XS[f"FLAT_{f}"]) < 0.01 or readings[f] == "the rival favoured" for f in FOOTS)
        check("MUTATE CONTROL: with the rival's ratio injected, FLAT is rejected (p < 0.01) or the rival is favoured, both footings "
              "(if not, the test is NON-DISCRIMINATING)", "; ".join(f"{f}: p_FLAT {pv(XS[f'FLAT_{f}']):.2e}, {readings[f]}" for f in FOOTS), rej)
    NUM.update(D=D.tolist(), sigma=np.sqrt(np.diag(Cm)).tolist(), chi2=XS, A_data=A_data, A_class=AD, readings=readings, gated=gated)

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - T0:.0f} s)")
open(os.path.join(HERE, f"cfg255{SFX}.out"), "w").write("\n".join(LOG) + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, numbers=NUM), open(os.path.join(HERE, f"cfg255{SFX}_results.json"), "w"), indent=1, default=float)
sys.exit(1 if nf else 0)
