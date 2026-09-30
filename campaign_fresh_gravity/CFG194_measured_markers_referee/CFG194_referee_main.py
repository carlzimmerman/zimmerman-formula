#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG194 main run + MUTATE -- referee re-derivation of CFG189, written from CFG194_FROZEN_CRITERIA.md alone.
    ZF_REPO=<repo> python3 CFG194_referee_main.py                > CFG194_main.out            (rc 0 iff my own controls pass)
    MUTATE={1..6} ZF_REPO=<repo> python3 CFG194_referee_main.py  > CFG194_MUTATE_<k>.out      (rc 1 iff the control bites)
Variant BS needs CFG184's functions, which may only be opened after this file's outputs are saved: BS is computed in
CFG194_bs_post.py (post-comparison), a labelled departure from the frozen plan.
"""
import sys
import json
import math
import numpy as np
from CFG194_lib import *   # noqa
import CFG194_lib as L
_E_RIVAL = L._E_RIVAL

MODE = os.environ.get("MUTATE", "0")
out = {"mode": MODE, "controls": {}, "rows": {}, "numbers": {}}
ctrl_ok = []


def check(name, ok, meas):
    ctrl_ok.append(bool(ok))
    out["controls"][name] = dict(ok=bool(ok), measured=str(meas))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {meas}")


PL = {}     # pass-line rows: name -> list of (label, ok, detail)


def row(pl, label, ok, detail):
    PL.setdefault(pl, []).append((label, bool(ok), detail))
    P(f"    {pl} {'ok  ' if ok else 'MISS'} {label}: {detail}")


P("=" * 110)
P(f"CFG194 referee re-derivation of CFG189.  MODE={MODE}.  repo=<repo>")
P("=" * 110)
if MODE == "4":
    E_T = lambda z: np.ones_like(np.asarray(z, float))   # noqa  (T := flat)
    L.E_T = E_T
    cells_three.__globals__["E_T"] = E_T
AS = M.load_sparc_anchor()
mk = load_markers()
sg = load_sigma()
mcur = load_model_curves()
S_model = M.load_kurvs(inc_col="inc_star_deg")          # model-value column: control C1 only
S_model_sfr = M.load_kurvs(inc_col="inc_sfr_deg")
SP1 = spec_s(1.0)
Ivals = {int(r["kurvs_id"]): r for r in read_rows("data_assembly/arxiv_tables/kurvs2023_integrated.csv")}
Vtab = {int(r["kurvs_id"]): r for r in read_rows("data_assembly/arxiv_tables/kurvs2023_velocities_at_radii.csv")}

# ------------------------------------------------------------------------------------------ controls
P("\n-- controls")
cm = cells_three(S_model, AS, SP1)
ok1 = abs(cm["flat"]["dprime"] - 0.1441) < 5e-4 and abs(cm["rival"]["dprime"] + 0.0060) < 5e-4 and abs(cm["T"]["dprime"] - 0.3227) < 5e-4
check("C1 model col 3, i_star error term, my sigma_out: flat +0.1441 / rival -0.0060 / T +0.3227 to 5e-4", ok1,
      f"{cm['flat']['dprime']:+.4f} / {cm['rival']['dprime']:+.4f} / {cm['T']['dprime']:+.4f}")
# C3 law patches
base = M.cell(S_model, AS, SP1, DEC_MU, 0.0, "canonical")
with law_ctx(E_flat):
    lf = M.cell(S_model, AS, SP1, DEC_MU, 0.0, "canonical")
d1 = abs(lf["H"]["dprime"] - base["flat"]["dprime"]) + abs(lf["H"]["sigma"] - base["flat"]["sigma"])
with law_ctx(_E_RIVAL):
    lr = M.cell(S_model, AS, SP1, DEC_MU, 0.0, "canonical")
d2 = abs(lr["H"]["dprime"] - base["H"]["dprime"])
t0, t85, t15 = float(tt0_dex(0.0)), float(tt0_dex(0.85)), float(tt0_dex(1.5))
check("C3 E:=1 makes H = flat (0.0); original E replays the rival (0.0); t/t0 dex 0 / -0.3264 / -0.5099 to 0.002",
      d1 == 0.0 and d2 == 0.0 and abs(t0) < 1e-12 and abs(t85 + 0.3264) < 0.002 and abs(t15 + 0.5099) < 0.002, (d1, d2, t0, round(t85, 4), round(t15, 4)))
# C4 digitisation control
rat = []
for k in IDS:
    Rm = fnum(Vtab[k]["R_halpha_max_kpc"])
    si = math.sin(math.radians(fnum(Ivals[k]["inc_sfr_deg"])))
    mv = np.interp(Rm, mcur[k]["R"], mcur[k]["v"])
    rat.append(abs(mv) / si / fnum(Vtab[k]["v_at_last_point_kms"]))
check("C4 digitisation: model curve at R_max / sin i_SFR = Table B1 col 3 within 1.5% (ten discs)", max(abs(np.array(rat) - 1)) < 0.015,
      f"ratios {min(rat):.4f}..{max(rat):.4f}")
# C5 structure
allrows = read_rows("data_assembly/arxiv_tables/kurvs_rc_profiles/kurvs_rc_points.csv")
ncl = sum(int(fnum(r["clipped_white_marker"])) for r in allrows)
nten = sum(len(mk[k]["R"]) for k in IDS)
sides_ok = all(len(side_pts(mk[k], s)) > 0 for k in IDS for s in (1, -1))
check("C5 structure: 511 markers, 18 clipped, ten discs present, 231 markers in them, every side has an unclipped marker",
      len(allrows) == 511 and ncl == 18 and len(mk) == 10 and nten == 231 and sides_ok, (len(allrows), ncl, len(mk), nten, sides_ok))
sgn = {k: (int(np.sum(np.sign(mk[k]["R"]) * np.sign(mk[k]["v"]) > 0)), len(mk[k]["R"])) for k in IDS}
P("  sign structure (markers with sign(v)=sign(R), of all):", sgn)

# ------------------------------------------------------------------------------------------ mutations
rng = np.random.default_rng(194)


def build_mode(rule, **kw):
    if MODE == "1":
        kw["vscale"] = 10 ** 0.3
    if MODE == "3":
        kw["dep_col"] = "none"
    if MODE == "5" and rule is rule_primary and not kw:
        def rule_inner(mk_, sg_, drop=None, _kk=[0]):
            k = [kk for kk in IDS if mk[kk] is mk_][0]
            Rm = fnum(Vtab[k]["R_halpha_max_kpc"])
            side, R = far_side(mk_, False, drop)
            o = side_pts(mk_, side, False, drop)
            j = [i for i in o if abs(mk_["R"][i]) >= 0.25 * Rm][0]
            Rj = abs(mk_["R"][j])
            s, es = sigma_side(sg_, Rj, side)
            return dict(R=Rj, v=abs(mk_["v"][j]), e=mk_["e"][j], side=side, sig=s, esig=es)
        rule = rule_inner
    S, info = build(rule, mk=mk, sg=sg, **kw)
    if MODE == "6":
        p = rng.permutation(len(S.ids))
        S.sig = S.sig[p]; S.esig = S.esig[p]
    return S, info



# ------------------------------------------------------------------------------------------ primary
P("\n-- primary: farther side's outermost UNCLIPPED marker; V=|v|/sin i_SFR; error = mean bar/sin i_SFR; sigma at R_out, same side")
S, info = build_mode(rule_primary)
Vt = np.array([fnum(Vtab[k]["v_at_last_point_kms"]) for k in IDS])
Rmt = np.array([fnum(Vtab[k]["R_halpha_max_kpc"]) for k in IDS])
ratio = S.V / Vt - 1
for j, i in enumerate(info):
    P(f"  KURVS-{i['id']:<2d} R_out={i['R']:6.2f} (table R_max {Rmt[j]:5.2f}) side {i['side']:+d}  V_out={i['V']:6.1f}+-{i['eV']:5.1f} vs model {Vt[j]:6.1f}: {100*ratio[j]:+6.1f}%   sigma={i['sig']:5.1f}+-{i['esig']:4.1f} (CFG165 sigma_out at R_max {S_model.sig[j]:5.1f}+-{S_model.esig[j]:4.1f})")
prim = cells_three(S, AS, SP1)
P("  decision cell (mu=0.67, s=1):", fmt_cells(prim))
out["numbers"]["primary"] = {l: dict(prim[l]) for l in LAWS}
out["numbers"]["per_disc"] = [dict(i, ratio=float(r)) for i, r in zip(info, ratio)]
out["numbers"]["model"] = {l: dict(cm[l]) for l in LAWS}
P("  model-value :", fmt_cells(cm))

# variants
P("\n-- variants (decision cell)")
var = {}
Sa, _ = build_mode(rule_outerk, k=3)
var["V-a outer three"] = cells_three(Sa, AS, SP1)
Sb, ib = build_mode(rule_bothsides)
var["V-b both sides, shorter radius"] = cells_three(Sb, AS, SP1)
Sc, ic = build_mode(rule_primary, allow_clipped=True)
var["V-c clipped included"] = cells_three(Sc, AS, SP1)
Sd, _ = build_mode(rule_primary, inc_col="inc_star_deg")
var["V-d i_star deprojection and error term"] = cells_three(Sd, AS, SP1)
Sdp, _ = build_mode(rule_primary, inc_col="inc_star_deg", dep_col="inc_sfr_deg")
var["V-d' i_star error term only (diagnostic)"] = cells_three(Sdp, AS, SP1)
for n, c in var.items():
    P(f"  {n:42s}", fmt_cells(c))
out["numbers"]["variants"] = {n: {l: dict(c[l]) for l in LAWS} for n, c in var.items()}
P("  V-b radii:", [round(i['R'], 2) for i in ib])
P("  V-c outer radii / V:", [(round(i['R'], 2), round(i['V'], 1)) for i in ic])

# headline
P("\n-- shifts (measured primary minus model) and the headline")
lab, cls_m, cls_p, dz = headline_label(cm, prim)
dd = {l: prim[l]["dprime"] - cm[l]["dprime"] for l in LAWS}
for l in LAWS:
    P(f"  {l:6s} shift {dd[l]:+.4f} dex, dz {dz[l]:+.2f}")
nmatch = sum(1 for n, c in var.items() if classes(c) == cls_m and not n.startswith("V-d'"))
nflip = sum(1 for n, c in var.items() if classes(c) != cls_p and not n.startswith("V-d'"))
P(f"  class model {cls_m}; measured {cls_p}; HEADLINE = {lab}; variants (excl. BS, deferred, and V-d') whose class differs from the primary: {nflip} of 4")
out["numbers"]["headline"] = dict(label=lab, cls_model=cls_m, cls_primary=cls_p, shifts=dd, dz=dz, n_variants_flipping=nflip)

# ------------------------------------------------------------------------------------------ break-evens
P("\n-- break-evens mu_be [1-sigma edges], gas status vs ceiling 3.47, across s (decision-cell footing)")
BE = {}
for tag, SS in (("model", S_model), ("measured", S)):
    for s in S_AXIS:
        for law in LAWS:
            be = break_even(SS, AS, spec_s(s), law)
            BE[(tag, s, law)] = be
            P(f"  {tag:8s} s={s:4.2f} {law:6s} mu_be={('none (over)' if be['mu'] is None else f'{be['mu']:.3f} [{be['lo']:.3f}, {be['hi'] if be['hi'] is not None else float('nan'):.3f}]'):32s} status {status(be)}")
out["numbers"]["break_even"] = {f"{t}|{s}|{l}": dict(v, status=status(v)) for (t, s, l), v in BE.items()}
P("\n-- fit points s0 (Delta'=0) at mu = 0.67")
FP = {}
for tag, SS in (("model", S_model), ("measured", S)):
    FP[tag] = {l: fit_point_s(SS, AS, l) for l in LAWS}
    P(f"  {tag:8s}", FP[tag])
out["numbers"]["fit_points"] = FP
P("\n-- P0 (s=0) at mu=0.67")
c0 = cells_three(S, AS, spec_s(0.0))
P("  measured P0:", fmt_cells(c0))
c0m = cells_three(S_model, AS, spec_s(0.0))
P("  model    P0:", fmt_cells(c0m))
out["numbers"]["P0_measured"] = {l: dict(c0[l]) for l in LAWS}

# ------------------------------------------------------------------------------------------ C2'
P("\n-- C2': velocity-marker radius against the nearest sigma-profile marker radius (same side, any sigma marker)")
n_over, per = 0, {}
offs = {}
for k in IDS:
    for R in mk[k]["R"]:
        m = np.sign(sg[k]["R"]) == np.sign(R)
        d = np.min(np.abs(sg[k]["R"][m] - R))
        if d > 0.02:
            n_over += 1
            per[k] = per.get(k, 0) + 1
            j = np.argmin(np.abs(sg[k]["R"][m] - R))
            offs.setdefault(k, []).append(float(R - sg[k]["R"][m][j]))
P(f"  markers with |R_v - R_sigma| > 0.02 kpc: {n_over} of {nten}; per disc {per}")
P("  offsets (kpc) per disc:", {k: [round(x, 3) for x in v] for k, v in offs.items()})
out["numbers"]["C2prime"] = dict(n_over=n_over, n=nten, per=per, offs=offs)

# ------------------------------------------------------------------------------------------ pass lines
P("\n-- pass lines (targets = CFG189 README numbers, read, not blind)")
if MODE == "0":
    row("P1", "C1 reproduces (see controls)", ok1, "")
    tgtratio = {3: 10.5, 7: -15.2, 8: -6.6, 9: 0.4, 11: -3.3, 13: 9.7, 15: -6.5, 16: -5.8, 17: -22.3, 21: -6.0}
    for j, i in enumerate(info):
        row("P2", f"KURVS-{i['id']} measured/model", abs(100 * ratio[j] - tgtratio[i["id"]]) <= 1.0, f"{100*ratio[j]:+.1f}% vs {tgtratio[i['id']]:+.1f}%")
    for i, rr in ((3, 10.06), (16, 10.05), (17, 7.34)):
        j = IDS.index(i)
        row("P2", f"KURVS-{i} R_out", abs(info[j]["R"] - rr) <= 0.02, f"{info[j]['R']:.3f} vs {rr}")
    tg = dict(flat=(0.125, 0.051, 2.4), rival=(-0.021, None, -0.4), T=(0.295, None, 5.5))
    for l in LAWS:
        t = tg[l]
        row("P3", f"{l} Delta'", abs(prim[l]["dprime"] - t[0]) <= 0.008, f"{prim[l]['dprime']:+.4f} vs {t[0]:+.3f}")
        row("P3", f"{l} z", abs(prim[l]["z"] - t[2]) <= 0.25, f"{prim[l]['z']:+.2f} vs {t[2]:+.1f}")
    row("P3", "flat sigma", abs(prim["flat"]["sigma"] / 0.051 - 1) <= 0.08, f"{prim['flat']['sigma']:.4f} vs 0.051")
    row("P3", "SPARC anchor / model-value cell (C1)", ok1, "")
    tv = {"V-a outer three": ((2.4, -1.0, 5.9), "lean rival"), "V-b both sides, shorter radius": ((0.1, -3.2, 3.4), "lean flat"),
          "V-c clipped included": ((2.8, 0.1, 5.7), "lean rival"), "V-d i_star deprojection and error term": ((2.2, -0.7, 5.3), "lean rival")}
    row("P4", "primary class", classes(prim) == "lean rival", classes(prim))
    for n, (zt, cl) in tv.items():
        c = var[n]
        row("P4", f"{n} class", classes(c) == cl, f"{classes(c)} vs {cl}")
        row("P4", f"{n} z", all(abs(c[l]["z"] - zz) <= 0.35 for l, zz in zip(LAWS, zt)), " ".join(f"{c[l]['z']:+.2f}" for l in LAWS) + f" vs {zt}")
    row("P4", "BS class / z", False, "DEFERRED to CFG194_bs_post.py (CFG184's functions may only be opened after this run is saved); counted as not-yet-scored, not as a pass")
    row("P5", "shifts dex", all(abs(dd[l] - t) <= 0.006 for l, t in zip(LAWS, (-0.019, -0.015, -0.027))), " ".join(f"{dd[l]:+.4f}" for l in LAWS) + " vs -0.019 -0.015 -0.027")
    row("P5", "dz", all(abs(dz[l] - t) <= 0.3 for l, t in zip(LAWS, (-0.84, -0.29, -1.46))), " ".join(f"{dz[l]:+.2f}" for l in LAWS) + " vs -0.84 -0.29 -1.46")
    row("P5", "label CHANGED", lab == "CHANGED", lab)
    row("P5", "1 of 5 variants flips (4 of 4 checked here)", nflip == 1, f"{nflip} of 4 checked (BS deferred)")
    for tag, tg3 in (("measured", (1.86, 0.50, 3.80)), ("model", (2.11, 0.62, 4.34))):
        tol = 0.06 if tag == "measured" else 0.04
        for l, t in zip(LAWS, tg3):
            b = BE[(tag, 1.0, l)]["mu"]
            row("P6", f"{tag} mu_be s=1 {l}", b is not None and abs(b / t - 1) <= tol, f"{b if b is None else round(b,3)} vs {t}")
    bT = BE[("measured", 1.0, "T")]
    row("P6", "T lower edge at s=1 below 3.47 (gas-allowed)", bT["lo"] < GAS_CEIL, f"{bT['lo']:.3f}")
    for s, t in ((1.42, 4.97), (3.0, 9.11)):
        b = BE[("measured", s, "T")]
        row("P6", f"T central s={s}, and excluded", b["mu"] is not None and abs(b["mu"] / t - 1) <= 0.06 and b["lo"] > GAS_CEIL, f"{b['mu']:.3f} lo {b['lo']:.3f} vs {t}")
    row("P6", "T at P0 z +0.9", abs(c0["T"]["z"] - 0.9) <= 0.3, f"{c0['T']['z']:+.2f}")
    fpm = FP["measured"]
    row("P6", "fit points 0.42 / 1.12 / <0", isinstance(fpm["flat"], float) and abs(fpm["flat"] - 0.42) <= 0.05 and abs(fpm["rival"] - 1.12) <= 0.05 and fpm["T"] == "<0", str(fpm))
    n22 = (n_over >= 20 and n_over <= 24) and nten == 231
    row("P7", "22 of 231", n22, f"{n_over} of {nten}")
    r17 = per.get(17, 0) == 20 and abs(np.median(offs.get(17, [0])) - 0.065) < 0.01 if 17 in offs else False
    row("P7", "20 in KURVS-17 at ~0.065", r17, f"{per.get(17,0)} at median offset {np.median(offs.get(17,[np.nan])):.3f}")
    row("P7", "2 in KURVS-3", per.get(3, 0) == 2, f"{per.get(3,0)}")
    row("P7", "no others", set(per) <= {3, 17}, str(per))
    P("\n-- verdict per pass line")
    verd = {}
    for pl in sorted(PL):
        oks = [r[1] for r in PL[pl]]
        v = "REPRODUCES" if all(oks) else ("DISAGREES" if not any(oks) else "PARTIAL")
        verd[pl] = v
        P(f"  {pl}: {v}  ({sum(oks)}/{len(oks)} rows)")
    out["verdict"] = verd
    out["rows"] = {pl: [dict(label=a, ok=b, detail=c) for a, b, c in v] for pl, v in PL.items()}

# ------------------------------------------------------------------------------------------ MUTATE bite logic
bite = None
if MODE != "0":
    P("\n-- MUTATE evaluation (exit 1 iff the control bites)")
    if MODE == "1":
        bite = classes(prim) != "lean rival"     # main-run class is lean rival (primary; see main output)
        P(f"  class after the mutation: {classes(prim)}; main-run class is lean rival -> bite={bite}")
    elif MODE == "2":
        sw = M.classify(prim["rival"]["z"], prim["flat"]["z"])
        bite = sw != "lean rival"
        P(f"  class with the law labels swapped: {sw} (real class {classes(prim)}) -> bite={bite}")
    elif MODE == "3":
        bite = classes(prim) != "lean rival"
        P(f"  class without deprojection: {classes(prim)} -> bite={bite}")
    elif MODE == "4":
        same = all(abs(prim["T"][k] - prim["flat"][k]) < 1e-9 for k in ("dprime", "sigma", "z"))
        dzT = prim["T"]["z"] - cm["T"]["z"]
        dzF = prim["flat"]["z"] - cm["flat"]["z"]
        bite = same and abs(dzT - dzF) < 1e-9
        P(f"  T rows equal flat's: {same}; T shift z {dzT:+.4f} vs flat {dzF:+.4f} -> bite={bite}")
    elif MODE == "5":
        dflat = prim["flat"]["dprime"] - 0.1249
        bite = abs(dflat) > 0.05
        P(f"  flat Delta' {prim['flat']['dprime']:+.4f} vs main-run +0.1249: |diff| {abs(dflat):.4f} -> bite={bite}")
    elif MODE == "6":
        bite = classes(prim) != "lean rival"
        P(f"  class after sigma permutation (seed 194): {classes(prim)} -> bite={bite} (informational: exit 0 is allowed)")
    out["bite"] = bool(bite)

# ------------------------------------------------------------------------------------------ write
tag = "main" if MODE == "0" else f"MUTATE_{MODE}"
with open(os.path.join(HERE, f"CFG194_{tag}_results.json"), "w") as f:
    json.dump(out, f, indent=1, default=jdefault)
if MODE == "0":
    P(f"\nmain exit: my own controls {'all pass' if all(ctrl_ok) else 'FAIL'}")
    sys.exit(0 if all(ctrl_ok) else 1)
sys.exit(1 if bite else 0)
