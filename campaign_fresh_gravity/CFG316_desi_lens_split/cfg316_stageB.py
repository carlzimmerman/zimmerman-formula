#!/usr/bin/env python3
"""CFG316 Stage B scoring: the early/late split per isolation definition on K1, its 30-patch jackknife covariance, B's calibrated
prediction, the KiDS split amplitude, the absolute ESD against the law (both footings), and the controls.

Frozen criteria: FROZEN_CRITERIA.md (c57c69a81), D1-D9 binding.  Inputs (outside git): ../_external_data/cfg316_work/cfg316_lenses.npz
(Stage A) and cfg316_stack.npz (cfg316_stageB_stack.py: the only pass that read the real shear).
  samples   headline base = matched (class (b)), FLAG_MASSPDF in [1/5, 5], AGNFRAC < 0.1, 8 < log M* < 11, D5-complete;
            ISO-S (3 Mpc, 1000 km/s), ISO-S4 (4 Mpc, 2000 km/s), ISO-P (the KiDS photo-z rule, C1).
  stat      D = ESD_early - ESD_late on K1 [8..14]; C = leave-one-patch-out jackknife (N = 30), Hartlap (N - p - 2)/(N - 1) = 21/29;
            chi2_0 = D C^-1 D h; chi2_B = (D - D_B) C^-1 (D - D_B) h, 7 dof, D_B = CFG95's calibrated model stacked on THIS sample's
            (log M*, z) weights (CIGALE masses read as Chabrier); A = D88 C^-1 D / D88 C^-1 D88 (D88 = the June KiDS split, CFG88),
            sigma_A by jackknife.  Significances quoted at error scale x1, x1.31 (CFG315 S1) and x1.58 (CFG108) (D8).
  checks    C1 (A_P within 2 sigma of 1; reported also whether C1 can discriminate), C2 (June sums to 1e-9), C3 (nesting, Stage A),
            C4 (randoms and cross shear consistent with zero on K1), H1 / H2 (ISO-S / ISO-S4: p > 0.01 both footings), H3 (A_S - A_P).
MUTATE=1: early/late labels swapped in a random half of the patches (p = 1/2 per patch, seed 316) before stacking; outputs *_MUTATE*.
Run from the repository root: python3 -u campaign_fresh_gravity/CFG316_desi_lens_split/cfg316_stageB.py   (MUTATE=1 for the control)
"""
import os, sys, io, json, math, contextlib
import numpy as np
from scipy.stats import chi2 as CHI2, norm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg316_common import *   # noqa
sys.path.insert(0, CFG)
import CFG7_common as C7       # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("cfg316_stageB", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run from")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: early/late labels swapped per patch (p = 1/2, seed 316) -- the split must vanish within its errors ***")
FOOTS = ("canonical", "alt")
SCALES = (1.0, 1.31, 1.58)
PK = len(K1); H7 = hartlap(NPATCH, PK)
pv = lambda x, k=PK: float(CHI2.sf(x, k))
zs = lambda p: float(norm.isf(p / 2)) if p > 0 else float("inf")

L = np.load(os.path.join(WORK, "cfg316_lenses.npz"))
ST = np.load(os.path.join(WORK, "cfg316_stack.npz"))
A_ = json.load(open(os.path.join(HERE, "cfg316_stageA_results.json")))
idx = ST["idx"]; PL = ST["PL"]
lm, z, Mg = L["logM"][idx], L["z"][idx], L["Mgal"][idx]
clsb, clsa = L["clsb"][idx].astype(int), L["clsa"][idx].astype(int)
patch = L["patch"][idx]
hb = L["mass_ok"][idx] & L["matched"][idx] & L["complete"][idx]
SAMP = {"ISO-S": hb & L["isoS"][idx], "ISO-S4": hb & L["isoS4"][idx], "ISO-P": hb & L["isoP"][idx]}
if MUTATE:
    sw = np.random.default_rng(316).random(NPATCH) < 0.5
    clsb = np.where(sw[patch], 1 - clsb, clsb)
    clsa = np.where(sw[patch], 1 - clsa, clsa)
    P(f"  MUTATE: {int(sw.sum())} of {NPATCH} patches swapped")

# ------------------------------------------------------------------ the record's model machinery, read-only (CFG95 -> CFG61, CFG55)
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


say("loading CFG95 / CFG61 model machinery (read-only)")
g95 = lane_prefix("CFG95_kids_split_own_calibration.py", "# ================================================================== C1-C3")
g61 = g95["g61"]
LMG, ZG = g61["LMG"], g61["ZG"]
assert list(g61["K1"]) == K1


def make_weights(sel, cls):
    im = np.clip(np.round((lm - LMG[0]) / 0.05).astype(int), 0, len(LMG) - 1)
    iz = np.clip(np.round((z - 0.05) / 0.10).astype(int), 0, len(ZG) - 1)

    def weights(c_, scrit=False):
        w = np.zeros((len(LMG), len(ZG)))
        s = sel & (cls == c_)
        np.add.at(w, (im[s], iz[s]), Mg[s])
        return w * (g61["SW"][None, :] if scrit else 1.0)
    return weights


def use_sample(sel, cls):
    w = make_weights(sel, cls)
    g95["weights"] = w; g61["weights"] = w


def model_D_B(sel, cls, foot, fe=None, fl=None):
    use_sample(sel, cls)
    fe = fe or (lambda m, f=foot: g95["delta_early"](m, f))
    fl = fl or (lambda m, f=foot: g95["delta_late"](f))
    ml, me = g95["stack_true"](0, foot, fl), g95["stack_true"](1, foot, fe)
    return ml, me


def law_cat(sel, cls, foot):
    use_sample(sel, cls)
    return g61["stack"](0, foot, "L", "blue"), g61["stack"](1, foot, "L", "red")


# ------------------------------------------------------------------ data products
J = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))
tg, tw = J["wgE"].sum(0), J["W"].sum(0)
esdJ = tg / tw / KG
D88 = (esdJ[1] - esdJ[0])[K1]


def stats(sel, cls, wts=None):
    Sx = class_patch_sums(PL, cls, patch, sel, wts)
    esd, loo = esd_loo(Sx)
    ex, loox = esdx_loo(Sx)
    D = (esd[1] - esd[0])[K1]
    Dp = loo[:, 1, K1] - loo[:, 0, K1]
    Cd = jk_cov(Dp)
    out = dict(S=Sx, esd=esd, loo=loo, D=D, Dp=Dp, C=Cd, ex=ex, loox=loox,
               n=(int(np.sum(sel & (cls == 1))), int(np.sum(sel & (cls == 0)))))
    try:
        Ci = np.linalg.inv(Cd)
        out["Ci"] = Ci
        out["chi0"] = float(D @ Ci @ D) * H7
        out["A"] = float(D88 @ Ci @ D) / float(D88 @ Ci @ D88)
        reps = np.array([float(D88 @ Ci @ Dp[p]) / float(D88 @ Ci @ D88) for p in range(NPATCH)])
        out["sA"] = float(np.sqrt(jk_cov(reps[:, None])[0, 0]))
        out["Areps"] = reps
    except np.linalg.LinAlgError:
        out["chi0"] = float("nan")
    return out


def sig_line(x2):
    return ", ".join(f"x{s}: chi2 {x2 / s ** 2:.2f} p {pv(x2 / s ** 2):.2e} ({zs(pv(x2 / s ** 2)):.2f} sigma)" for s in SCALES)


# ================================================================== controls C2, C3
R.banner("C2 / C3  CONTROLS")
check("C2 CONTROL: the stacking code on the committed lr_lenses.npz reproduces lr_esd_jackknife.npz sums (wgE, W, NN) to 1e-9 relative",
      f"max relative deviation {float(ST['c2dev']):.1e} (181,477 June lenses, June patch labels)", float(ST["c2dev"]) < 1e-9)
nest = bool(np.all(SAMP["ISO-S"][SAMP["ISO-S4"]]))
check("C3 CONTROL: ISO-S4 within ISO-S; every count printed",
      f"headline base {int(hb.sum()):,}; ISO-S {int(SAMP['ISO-S'].sum()):,}; ISO-S4 {int(SAMP['ISO-S4'].sum()):,}; ISO-P {int(SAMP['ISO-P'].sum()):,}; "
      f"nested {nest}  [Stage A cut sequence: {json.dumps(A_['numbers']['counts'])}]", nest)

# ================================================================== per isolation definition
R.banner("THE SPLIT PER ISOLATION DEFINITION (K1, class (b), 30-patch jackknife)")
RES = {}
for nm, sel in SAMP.items():
    ne, nl = int(np.sum(sel & (clsb == 1))), int(np.sum(sel & (clsb == 0)))
    if ne == 0 or nl == 0:
        P(f"  {nm}: early {ne}, late {nl} -> NO MEASUREMENT POSSIBLE (empty class)")
        RES[nm] = None
        continue
    s = stats(sel, clsb)
    DB = {}
    for foot in FOOTS:
        ml, me = model_D_B(sel, clsb, foot)
        DB[foot] = (me - ml)[K1]
    s["DB"] = DB
    s["chiB"] = {f: float((s["D"] - DB[f]) @ s["Ci"] @ (s["D"] - DB[f])) * H7 for f in FOOTS}
    RES[nm] = s
    P(f"  {nm}: early {ne}, late {nl}")
    P(f"    D (Msun/pc^2)        {np.round(s['D'], 2).tolist()}")
    P(f"    jackknife sigma      {np.round(np.sqrt(np.diag(s['C'])), 2).tolist()}")
    P(f"    KiDS June D (CFG88)  {np.round(D88, 2).tolist()}")
    for f in FOOTS:
        P(f"    D_B ({f:9s})       {np.round(DB[f], 2).tolist()}")
    P(f"    chi2 vs zero: {sig_line(s['chi0'])}")
    for f in FOOTS:
        P(f"    chi2 vs D_B ({f}): {sig_line(s['chiB'][f])}")
    P(f"    A (amplitude of the June KiDS split shape) = {s['A']:.3f} +- {s['sA']:.3f}")

# ------------------------------------------------------------------ C1, H1, H2, H3
R.banner("C1 / H1 / H2 / H3")
sp = RES["ISO-P"]
if sp is not None:
    c1 = abs(sp["A"] - 1) < 2 * sp["sA"]
    check("C1 CONTROL [decisive contrast]: ISO-P on the overlap reproduces a split consistent with the committed KiDS split (A_P within 2 sigma of 1)",
          f"A_P = {sp['A']:.3f} +- {sp['sA']:.3f} ((A-1)/sigma {(sp['A'] - 1) / sp['sA']:+.2f}; A/sigma {sp['A'] / sp['sA']:+.2f}); "
          f"N early {sp['n'][0]}, late {sp['n'][1]}", c1)
    disc = sp["sA"] < 0.5
    check("C1-INFO (reported) can C1 discriminate? (sigma_A < 0.5, i.e. a KiDS-size split is >= 2 sigma_A from zero)",
          f"sigma_A = {sp['sA']:.3f}: a split of zero is {abs(sp['A']) / sp['sA']:.2f} sigma from A_P and a KiDS-size split {abs(sp['A'] - 1) / sp['sA']:.2f} "
          f"sigma; C1 {'CAN' if disc else 'CANNOT'} tell them apart", True, load_bearing=False)
else:
    c1 = False
    check("C1 CONTROL [decisive contrast]: ISO-P reproduces the KiDS split", "ISO-P sample empty", False)
    disc = False
for hn, nm in (("H1 [HEADLINE]", "ISO-S"), ("H2", "ISO-S4")):
    s = RES[nm]
    if s is None:
        check(f"{hn} with {nm}, B's prediction (D = D_B) is consistent on K1, p > 0.01 both footings -- EVALUABLE?"
              + ("  [MUTATE]" if MUTATE else ""),
              f"NOT EVALUABLE: the {nm} sample is empty ({int(SAMP[nm].sum())} lenses; Stage A). Neither reading (PASS: isolation removes "
              f"the split; FAIL: the split survives) applies.", False)
    else:
        ok = all(pv(s["chiB"][f]) > 0.01 for f in FOOTS)
        check(f"{hn} with {nm}, B's prediction (D = D_B) is consistent on K1: p > 0.01 both footings" + ("  [MUTATE]" if MUTATE else ""),
              "; ".join(f"{f}: chi2 {s['chiB'][f]:.2f}/7 p {pv(s['chiB'][f]):.2e}" for f in FOOTS), ok)
if RES["ISO-S"] is None or sp is None:
    check("H3 A_S (ISO-S) vs A_P (ISO-P, same lenses): the difference with its jackknife error",
          "NOT EVALUABLE: ISO-S is empty", False)

# ================================================================== reported rows on the non-empty frozen sample(s)
R.banner("REPORTED ROWS (on ISO-P, the only non-empty frozen sample; class (b) unless stated)")
if sp is not None:
    selP = SAMP["ISO-P"]
    # D6: M* bins and the reweighting
    rows6 = []
    for lo, hi in ((10.0, 10.5), (10.5, 11.0)):
        sb = selP & (lm >= lo) & (lm < hi)
        ne, nl = int(np.sum(sb & (clsb == 1))), int(np.sum(sb & (clsb == 0)))
        if min(ne, nl) < 5:
            rows6.append(f"{lo}-{hi}: early {ne}, late {nl} -> not measurable"); continue
        s = stats(sb, clsb)
        rows6.append(f"{lo}-{hi}: early {ne}, late {nl}; chi2 vs 0 {s['chi0']:.2f} (p {pv(s['chi0']):.2e}); A {s['A']:.3f} +- {s['sA']:.3f}")
    hb_e, _ = np.histogram(lm[selP & (clsb == 1)], bins=np.arange(8.0, 11.05, 0.1))
    hb_l, _ = np.histogram(lm[selP & (clsb == 0)], bins=np.arange(8.0, 11.05, 0.1))
    ib = np.clip(np.digitize(lm, np.arange(8.0, 11.05, 0.1)) - 1, 0, len(hb_e) - 1)
    rw = np.where(clsb == 0, np.where(hb_l[ib] > 0, hb_e[ib] / np.maximum(hb_l[ib], 1), 0.0), 1.0)
    srw = stats(selP, clsb, wts=rw)
    rows6.append(f"late reweighted to the early M* histogram (0.1 dex): chi2 vs 0 {srw['chi0']:.2f} (p {pv(srw['chi0']):.2e}); "
                 f"A {srw['A']:.3f} +- {srw['sA']:.3f}; effective late N {rw[selP & (clsb == 0)].sum() ** 2 / np.sum(rw[selP & (clsb == 0)] ** 2):.0f}")
    check("D6 (reported) M* bins 10.0-10.5 / 10.5-11.0 and the R-row reweighting", "; ".join(rows6), True, load_bearing=False)
    # R4: class (a)
    s4 = stats(selP, clsa)
    check("R4 (reported) the split with the class from CIGALE colours (option a)",
          f"early {s4['n'][0]}, late {s4['n'][1]}; D {np.round(s4['D'], 1).tolist()}; chi2 vs 0 {s4['chi0']:.2f} (p {pv(s4['chi0']):.2e}); "
          f"A {s4['A']:.3f} +- {s4['sA']:.3f}", True, load_bearing=False)
    # R5: uniform differential offset Delta on CFG95's grid
    DG = np.round(np.arange(0.0, 0.5001, 0.025), 3)
    r5 = {}
    for Dv in DG:
        ml, me = model_D_B(selP, clsb, "canonical", fe=lambda m, d=Dv: d, fl=lambda m: 0.0)
        Dm = (me - ml)[K1]
        r5[float(Dv)] = float((sp["D"] - Dm) @ sp["Ci"] @ (sp["D"] - Dm)) * H7
    ok5 = [d for d, x in r5.items() if pv(x) > 0.05]
    check("R5 (reported) chi2 against a uniform differential M/L offset Delta (0-0.5 dex, canonical; a diagnostic, not a fit)",
          ", ".join(f"{d:g}: {x:.1f}" for d, x in list(r5.items())[::2]) + f" | p > 0.05 for Delta in "
          f"{(f'{min(ok5):.3f}-{max(ok5):.3f}') if ok5 else 'none'}", True, load_bearing=False)
    # R6: WMAP7 -> Planck uniform offset bracket on D_B
    r6 = {}
    for foot in FOOTS:
        ml, me = model_D_B(selP, clsb, foot, fe=lambda m, f=foot: g95["delta_early"](m, f) - 0.04,
                           fl=lambda m, f=foot: g95["delta_late"](f) - 0.04)
        r6[foot] = float(np.max(np.abs((me - ml)[K1] - sp["DB"][foot])))
    check("R6 (reported) the WMAP7 -> Planck distance rescaling of CIGALE masses (uniform -0.04 dex) on D_B",
          "; ".join(f"{f}: max |change in D_B| on K1 {r6[f]:.3f} Msun/pc^2 (sigma(D) min {np.min(np.sqrt(np.diag(sp['C']))):.1f})" for f in FOOTS),
          True, load_bearing=False)
    # R7: drop each K1 bin
    drops = []
    for j_ in range(PK):
        keep = [i for i in range(PK) if i != j_]
        Cj = sp["C"][np.ix_(keep, keep)]
        drops.append(float(sp["D"][keep] @ np.linalg.solve(Cj, sp["D"][keep])) * hartlap(NPATCH, PK - 1))
    check("R7 (reported) K1 with each bin dropped (chi2 vs zero, 6 dof)",
          "; ".join(f"drop {K1[j_]}: {x:.1f} (p {pv(x, PK - 1):.2f})" for j_, x in enumerate(drops)), True, load_bearing=False)

# ================================================================== C4: randoms and cross shear
R.banner("C4  CONTROL: random points and cross shear on K1")
PLr = ST["PLr"]; rpatch = ST["rpatch"]
Sr = np.zeros((4, NPATCH, 15))
for q in range(4):
    np.add.at(Sr[q], rpatch, PLr[:, q, :])
tgr, twr = Sr[0].sum(0), Sr[1].sum(0)
er = tgr / twr / KG
looR = (tgr[None] - Sr[0]) / (twr[None] - Sr[1]) / KG
Cr = jk_cov(looR[:, K1])
x2r = float(er[K1] @ np.linalg.solve(Cr, er[K1])) * H7
txr = Sr[3].sum(0)
exr = txr / twr / KG
looXR = (txr[None] - Sr[3]) / (twr[None] - Sr[1]) / KG
x2xr = float(exr[K1] @ np.linalg.solve(jk_cov(looXR[:, K1]), exr[K1])) * H7
xl = []
for nm in ("ISO-P",):
    s = RES[nm]
    if s is None: continue
    for c_ in (0, 1):
        cx = jk_cov(s["loox"][:, c_, K1])
        xl.append(float(s["ex"][c_, K1] @ np.linalg.solve(cx, s["ex"][c_, K1])) * H7)
selB = hb
sB = stats(selB, clsb)
for c_ in (0, 1):
    cx = jk_cov(sB["loox"][:, c_, K1])
    xl.append(float(sB["ex"][c_, K1] @ np.linalg.solve(cx, sB["ex"][c_, K1])) * H7)
c4 = pv(x2r) > 0.01 and pv(x2xr) > 0.01 and all(pv(x) > 0.01 for x in xl)
check("C4 CONTROL: random points give Delta Sigma consistent with zero on K1 (additive bias); cross shear consistent with zero",
      f"randoms (20,000): tangential {np.round(er[K1], 2).tolist()} chi2 {x2r:.2f}/7 (p {pv(x2r):.2f}); cross chi2 {x2xr:.2f} (p {pv(x2xr):.2f}); "
      f"lens cross shear (ISO-P late/early, base late/early): " + ", ".join(f"{x:.1f} (p {pv(x):.2f})" for x in xl), c4)

# ================================================================== the absolute ESD against the law (CFG315's environment question)
R.banner("ABSOLUTE ESD vs THE LAW (nu_mono, both footings), K1: CFG315's environment question")
ABS = {}
for nm, sel in (("ISO-P (photo-z isolated)", SAMP["ISO-P"]), ("complete base (NOT isolated)", hb)):
    s = stats(sel, clsb)
    if min(s["n"]) == 0: continue
    o14 = np.concatenate([s["esd"][0, K1], s["esd"][1, K1]])
    loo14 = np.concatenate([s["loo"][:, 0, K1], s["loo"][:, 1, K1]], axis=1)
    C14 = jk_cov(loo14)
    h14 = hartlap(NPATCH, 14)
    out = {}
    for foot in FOOTS:
        for lab, (ml, me) in (("catalogue M*", law_cat(sel, clsb, foot)), ("B-calibrated M*", model_D_B(sel, clsb, foot))):
            m14 = np.concatenate([ml[K1], me[K1]])
            Ci = np.linalg.inv(C14) * h14
            Q = float(m14 @ Ci @ o14) / float(m14 @ Ci @ m14); sQ = float(1 / np.sqrt(m14 @ Ci @ m14))
            qc = []
            for c_, mm_ in ((0, ml), (1, me)):
                Cc = jk_cov(s["loo"][:, c_, K1]); Cci = np.linalg.inv(Cc) * H7
                qc.append((float(mm_[K1] @ Cci @ s["esd"][c_, K1]) / float(mm_[K1] @ Cci @ mm_[K1]), float(1 / np.sqrt(mm_[K1] @ Cci @ mm_[K1]))))
            x2_1 = float((o14 - m14) @ Ci @ (o14 - m14))
            out[f"{foot}|{lab}"] = dict(Q=Q, sQ=sQ, late=qc[0], early=qc[1], chi2_Q1=x2_1)
            P(f"  {nm:30s} {foot:9s} {lab:16s}: Q = ESD_obs/ESD_law = {Q:.2f} +- {sQ:.2f} (late {qc[0][0]:.2f} +- {qc[0][1]:.2f}, early "
              f"{qc[1][0]:.2f} +- {qc[1][1]:.2f}); chi2(Q = 1) {x2_1:.1f}/14 (p {pv(x2_1, 14):.1e})")
    ABS[nm] = out
check("E1 (reported) CFG315's environment question: does strict (spectroscopic) isolation remove the x1.8-3.3 excess?",
      "NOT ANSWERABLE with the frozen samples: ISO-S and ISO-S4 are empty. Rows above: the photo-z-isolated (ISO-P) and the non-isolated "
      "complete DESI lenses on KiDS shear (raw lensfit e, no m-correction: about 1.5% low; KiDS reads 8.6% low vs DES+HSC, CFG315).",
      True, load_bearing=False)

# ================================================================== MUTATE reading
if MUTATE and sp is not None:
    check("MUTATE: with labels swapped per patch the ISO-P split vanishes within its errors (chi2 vs zero p > 0.01)",
          f"chi2 {sp['chi0']:.2f}/7 (p {pv(sp['chi0']):.3f}); A {sp['A']:.3f} +- {sp['sA']:.3f}", pv(sp["chi0"]) > 0.01)

# ================================================================== decision
if RES["ISO-S"] is None:
    reading = ("NOT DIAGNOSTIC: under the frozen rules the spectroscopic-isolation samples (ISO-S, ISO-S4) are EMPTY on the KiDS-1000 x DESI "
               "DR1 overlap (D5 completeness keeps 1,034 of 48,497 lenses and none of them passes ISO-S); H1-H3 are not evaluable. "
               + ("C1 (ISO-P, 296 lenses) is " + ("consistent with the KiDS split" if c1 else "NOT consistent with the KiDS split")
                  + (" but cannot discriminate it from zero" if not disc else "") + "." if sp is not None else ""))
else:
    reading = "see H1-H3"
P(f"\n    READING (declared): {reading}")
R.num("counts", {k: int(v.sum()) for k, v in SAMP.items()})
R.num("ISO-P", None if sp is None else dict(D=sp["D"].tolist(), sigma=np.sqrt(np.diag(sp["C"])).tolist(), chi0=sp["chi0"], A=sp["A"],
                                              sA=sp["sA"], DB={f: sp["DB"][f].tolist() for f in FOOTS}, chiB=sp["chiB"], n=sp["n"]))
R.num("C4", dict(rand=x2r, rand_x=x2xr, lens_x=xl)); R.num("ABS", ABS); R.num("reading", reading)
nf = R.write(here=HERE)
sys.exit(1 if nf else 0)
