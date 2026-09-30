#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG194 attacks A1-A10 (marker choice, radius, inclination, V scale, decomposition, pressure axis) and B1-B4 (disc set).
Written from CFG194_FROZEN_CRITERIA.md alone.  Deterministic except B2 (bootstrap N=2000, seed 194).
    ZF_REPO=<repo> python3 CFG194_attacks_a.py > CFG194_attacks_a.out"""
import sys
import json
import math
import numpy as np
from scipy.optimize import brentq
from CFG194_lib import *   # noqa
import CFG194_lib as L

AS = M.load_sparc_anchor()
mk = load_markers()
sg = load_sigma()
mcur = load_model_curves()
S_model = M.load_kurvs(inc_col="inc_star_deg")
S_model_sfr = M.load_kurvs(inc_col="inc_sfr_deg")
I = {int(r["kurvs_id"]): r for r in read_rows("data_assembly/arxiv_tables/kurvs2023_integrated.csv")}
Vt = {int(r["kurvs_id"]): r for r in read_rows("data_assembly/arxiv_tables/kurvs2023_velocities_at_radii.csv")}
KIN = {int(r["kurvs_id"]): r for r in read_rows("data_assembly/arxiv_tables/kurvs2023_kinematics.csv")}
RMAX = {k: fnum(Vt[k]["R_halpha_max_kpc"]) for k in IDS}
SP1 = spec_s(1.0)
idof = {id(mk[k]): k for k in mk}
RES = {}


def rec(name, S, spx=SP1, extra=None):
    c = cells_three(S, AS, spx)
    d = {l: dict(dprime=c[l]["dprime"], sigma=c[l]["sigma"], z=c[l]["z"], chi2dof=c[l]["chi2dof"]) for l in LAWS}
    d["class"] = classes(c)
    d["n"] = len(S.ids)
    if extra:
        d.update(extra)
    RES[name] = d
    P(f"  {name:58s} n={len(S.ids):2d} " + " ".join(f"{l}:{c[l]['dprime']:+.3f}({c[l]['z']:+.2f})" for l in LAWS) + f"  {d['class']}")
    return c


ROWS_FOR_A10 = {}
prim_S, prim_info = build(rule_primary, mk=mk, sg=sg)
P("=" * 100)
P("CFG194 attacks A/B.  repo=<repo>")
P("=" * 100)
P("\n-- A1 primary")
cp = rec("A1 primary", prim_S)
ROWS_FOR_A10["A1 primary"] = prim_S

# ---------------------------------------------------------------- A2
P("\n-- A2 each side alone")


def rule_side(side):
    def r(mk_, sg_, drop=None):
        o = side_pts(mk_, side, False, drop)
        j = o[-1]
        R = abs(mk_["R"][j])
        s, es = sigma_side(sg_, R, side)
        return dict(R=R, v=abs(mk_["v"][j]), e=mk_["e"][j], side=side, sig=s, esig=es)
    return r


def rule_near(mk_, sg_, drop=None):
    reach = {}
    for side in (1, -1):
        o = side_pts(mk_, side, False, drop)
        reach[side] = abs(mk_["R"][o[-1]])
    side = 1 if reach[1] < reach[-1] else -1
    return rule_side(side)(mk_, sg_, drop)


for nm, rl in (("A2 + side alone", rule_side(+1)), ("A2 - side alone", rule_side(-1)), ("A2 nearer side (shorter reach)", rule_near)):
    S_, i_ = build(rl, mk=mk, sg=sg)
    rec(nm, S_)
    ROWS_FOR_A10[nm] = S_
    RES[nm]["radii"] = [round(x["R"], 2) for x in i_]

# ---------------------------------------------------------------- A3
P("\n-- A3 annulus (both sides pooled; sigma from the farther side at the mean radius)")
for flo in (0.8, 0.7, 0.6):
    for w in (True, False):
        nm = f"A3 annulus [{flo},1] x R_far {'weighted mean' if w else 'median'}"
        S_, i_ = build(rule_annulus, mk=mk, sg=sg, flo=flo, weighted=w)
        rec(nm, S_)
        ROWS_FOR_A10[nm] = S_

# ---------------------------------------------------------------- A4
P("\n-- A4 outer k markers on the farther side")
for k in (2, 3, 5):
    nm = f"A4 outer {k}"
    S_, _ = build(rule_outerk, mk=mk, sg=sg, k=k)
    rec(nm, S_)
    ROWS_FOR_A10[nm] = S_

# ---------------------------------------------------------------- A5
P("\n-- A5 both sides at the shorter radius (V-b), A5x the farther side alone at that same radius, A5y both sides at 0.8 R_max")


def rule_fx(mk_, sg_, drop=None):
    Rs = min(abs(mk_["R"][side_pts(mk_, s, False, drop)[-1]]) for s in (1, -1))
    return rule_far_at(mk_, sg_, Rs, drop)


def rule_by(fr):
    def r(mk_, sg_, drop=None):
        return rule_both_at(mk_, sg_, fr * RMAX[idof[id(mk_)]], drop)
    return r


def rule_fr(fr):
    def r(mk_, sg_, drop=None):
        return rule_far_at(mk_, sg_, fr * RMAX[idof[id(mk_)]], drop)
    return r


Sb, ib = build(rule_bothsides, mk=mk, sg=sg)
rec("A5 V-b both sides, shorter radius", Sb)
Sx, ix = build(rule_fx, mk=mk, sg=sg)
rec("A5x farther side alone at the shorter radius", Sx)
Sy, iy = build(rule_by(0.8), mk=mk, sg=sg)
rec("A5y both sides at 0.8 R_max", Sy)
for nm, S_ in (("A5 V-b both sides, shorter radius", Sb), ("A5x farther side alone at the shorter radius", Sx), ("A5y both sides at 0.8 R_max", Sy)):
    ROWS_FOR_A10[nm] = S_
# the nearer side alone at its own outermost radius is A2 nearer; also the OTHER (nearer) side interpolated at the same radius = A2 nearer
# per-disc |v| on the two sides at the shorter radius (asymmetry diagnostic)
asym = []
for k in IDS:
    m_ = mk[k]
    Rs = min(abs(m_["R"][side_pts(m_, s, False)[-1]]) for s in (1, -1))
    vp = interp_side(m_, +1, Rs)[0]
    vm = interp_side(m_, -1, Rs)[0]
    asym.append((k, round(Rs, 2), round(vp, 1), round(vm, 1), round(100 * (vp / vm - 1), 1)))
P("  per-disc |v| at the shorter radius: (id, R, v+, v-, (v+/v- -1)%)", asym)
RES["A5_asym"] = asym
# also the farther side at the shorter radius vs the primary point: how much V drops going inward
P("  V-b radii:", [round(x['R'], 2) for x in ib], " A5x V:", [round(x['V'], 1) for x in ix], " primary V:", [round(x['V'], 1) for x in prim_info])

# ---------------------------------------------------------------- A6
P("\n-- A6 radius scan: farther side, V at f * R_max(table) (discs where it reaches)")
scan = {}
for fr in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
    S_, i_ = build(rule_fr(fr), mk=mk, sg=sg)
    if len(S_.ids) < 3:
        P(f"  f={fr}: only {len(S_.ids)} discs reach")
        continue
    c = rec(f"A6 f={fr}", S_)
    scan[fr] = dict(n=len(S_.ids), z_flat=c["flat"]["z"], z_rival=c["rival"]["z"], z_T=c["T"]["z"], cls=classes(c))
    ROWS_FOR_A10[f"A6 f={fr}"] = S_
RES["A6"] = scan
Sxx, _ = build(rule_both_at if False else rule_by(0.6), mk=mk, sg=sg)
rec("A6b both sides at 0.6 R_max (extra, labelled)", Sxx)

# ---------------------------------------------------------------- A7
P("\n-- A7 inclination")
Sd, _ = build(rule_primary, mk=mk, sg=sg, inc_col="inc_star_deg")
rec("A7 V-d i_star deprojection and error term", Sd)
Sdp, _ = build(rule_primary, mk=mk, sg=sg, inc_col="inc_star_deg", dep_col="inc_sfr_deg")
rec("A7 V-d' i_star error term only", Sdp)
ROWS_FOR_A10["A7 V-d"] = Sd
for dd in (+5.0, -5.0):
    S_ = copy.copy(prim_S)
    fac = np.array([math.sin(math.radians(fnum(I[k]["inc_sfr_deg"]))) / math.sin(math.radians(fnum(I[k]["inc_sfr_deg"]) + dd)) for k in IDS])
    S_.V = prim_S.V * fac
    S_.eV = prim_S.eV * fac
    rec(f"A7 i_SFR {dd:+.0f} deg, coherent (V scale sin i/sin(i{dd:+.0f}))", S_)
    ROWS_FOR_A10[f"A7 i_SFR {dd:+.0f}"] = S_

# ---------------------------------------------------------------- A8
P("\n-- A8 coherent V-scale grid and crossing scales (primary)")
grid = {}
for vs in np.round(np.arange(0.90, 1.1001, 0.01), 2):
    S_, _ = build(rule_primary, mk=mk, sg=sg, vscale=float(vs))
    c = cells_three(S_, AS, SP1)
    grid[float(vs)] = dict(cls=classes(c), z_flat=c["flat"]["z"], z_rival=c["rival"]["z"], z_T=c["T"]["z"])
P("  v_s : class, z_flat, z_rival")
for vs, d in grid.items():
    P(f"  {vs:5.2f}: {d['cls']:34s} {d['z_flat']:+.2f} {d['z_rival']:+.2f}")


def zf(vs, law, sh):
    S_, _ = build(rule_primary, mk=mk, sg=sg, vscale=vs)
    return cells_law(S_, AS, SP1, law, DEC_MU)["z"] - sh


cross = {}
cross["flat=+2 (lean rival ends below)"] = float(brentq(lambda v: zf(v, "flat", 2.0), 0.85, 1.05, xtol=1e-6))
cross["rival=-2 (lean flat begins below)"] = float(brentq(lambda v: zf(v, "rival", -2.0), 0.80, 1.00, xtol=1e-6))
cross["rival=+2 (lean rival ends above)"] = float(brentq(lambda v: zf(v, "rival", 2.0), 1.0, 1.3, xtol=1e-6))
P("  crossing V scales:", {k: round(v, 4) for k, v in cross.items()})
RES["A8"] = dict(grid=grid, cross=cross)
# the same for the model-value column
Sm_ = S_model


def zfm(vs, law, sh):
    S_ = copy.copy(Sm_)
    S_.V = Sm_.V * vs
    S_.eV = Sm_.eV * vs
    return cells_law(S_, AS, SP1, law, DEC_MU)["z"] - sh


crossm = {"flat=+2": float(brentq(lambda v: zfm(v, "flat", 2.0), 0.85, 1.05)), "rival=-2": float(brentq(lambda v: zfm(v, "rival", -2.0), 0.7, 1.0))}
P("  model-value column crossing scales:", {k: round(v, 4) for k, v in crossm.items()})
RES["A8"]["cross_model"] = crossm

# ---------------------------------------------------------------- A9 decomposition
P("\n-- A9 chain: model at R_max (i_star) -> i_SFR error term -> model at R_out (R, sigma, V move) -> measured V (model errors) -> measured V and marker errors")
info = prim_info
chain = {}
c0 = cells_three(S_model, AS, SP1)
chain["S0 model col 3 at R_max (C1, i_star error term)"] = c0
c1 = cells_three(S_model_sfr, AS, SP1)
chain["S1 + i_SFR in the error term"] = c1
S2 = copy.copy(S_model_sfr)
Vm_out = []
for j, k in enumerate(IDS):
    side = info[j]["side"]
    si = math.sin(math.radians(fnum(I[k]["inc_sfr_deg"])))
    Vm_out.append(abs(np.interp(side * info[j]["R"], mcur[k]["R"], mcur[k]["v"])) / si)
S2.R = np.array([x["R"] for x in info]); S2.V = np.array(Vm_out)
S2.sig = np.array([x["sig"] for x in info]); S2.esig = np.array([x["esig"] for x in info])
S2.grad2 = np.zeros(len(IDS))
chain["S2 model curve read at R_out (radius and sigma effect)"] = cells_three(S2, AS, SP1)
# extra (labelled, added after seeing the S2 step): split S2 into its radius(+model V) part and its sigma part
S2a = copy.copy(S_model_sfr)
S2a.R = S2.R.copy(); S2a.V = S2.V.copy()
S2b = copy.copy(S_model_sfr)
S2b.sig = S2.sig.copy(); S2b.esig = S2.esig.copy()
ca, cb = cells_three(S2a, AS, SP1), cells_three(S2b, AS, SP1)
P("  extra split of S2 (from S1): radius and model-V move only:", fmt_cells(ca))
P("  extra split of S2 (from S1): sigma at R_out same side only :", fmt_cells(cb))
RES["A9_S2split"] = dict(radius_only={l: dict(ca[l]) for l in LAWS}, sigma_only={l: dict(cb[l]) for l in LAWS})
S3 = copy.copy(S2)
S3.V = np.array([x["V"] for x in info])
chain["S3 measured V, table (model) errors (value effect)"] = cells_three(S3, AS, SP1)
S4 = copy.copy(S3)
S4.eV = np.array([x["eV"] for x in info])
chain["S4 measured V and marker errors (= primary; error effect)"] = cells_three(S4, AS, SP1)
prev = None
tot = {l: chain["S4 measured V and marker errors (= primary; error effect)"][l]["z"] - c0[l]["z"] for l in LAWS}
P("  step                                                            " + "   ".join(f"{l:>22s}" for l in LAWS))
dec = {}
for nm, c in chain.items():
    P(f"  {nm:62s}" + "   ".join(f"{c[l]['dprime']:+.4f}+-{c[l]['sigma']:.4f} ({c[l]['z']:+.2f})" for l in LAWS))
    if prev is not None:
        dec[nm] = {l: (c[l]["z"] - prev[l]["z"], c[l]["dprime"] - prev[l]["dprime"]) for l in LAWS}
    prev = c
P("  step changes (dz, dDelta'):")
for nm, d in dec.items():
    P(f"   {nm[:60]:60s}" + "  ".join(f"{l}: {d[l][0]:+.2f} ({d[l][1]:+.4f})" for l in LAWS))
P("  total dz:", {l: round(v, 2) for l, v in tot.items()})
P("  value-only vs sigma-only decomposition of the flat z drop (C-c):")
zc = {}
for l in LAWS:
    dp_new, sg_new, dp_old, sg_old = chain["S4 measured V and marker errors (= primary; error effect)"][l]["dprime"], chain["S4 measured V and marker errors (= primary; error effect)"][l]["sigma"], c0[l]["dprime"], c0[l]["sigma"]
    zc[l] = dict(z_old=dp_old / sg_old, z_new=dp_new / sg_new, value_only=dp_new / sg_old - dp_old / sg_old, sigma_only=dp_old / sg_new - dp_old / sg_old)
    P(f"   {l}: z {zc[l]['z_old']:+.2f} -> {zc[l]['z_new']:+.2f}; value-only {zc[l]['value_only']:+.2f}, sigma-only {zc[l]['sigma_only']:+.2f}")
RES["A9"] = dict(chain={nm: {l: dict(dprime=c[l]["dprime"], sigma=c[l]["sigma"], z=c[l]["z"]) for l in LAWS} for nm, c in chain.items()},
                 steps={nm: {l: list(v) for l, v in d.items()} for nm, d in dec.items()}, total_dz=tot, C_c=zc,
                 Vmodel_at_Rout=[round(x, 1) for x in Vm_out], Vmeasured=[round(x["V"], 1) for x in info])
P("  model curve at R_out vs table col 3 (radius effect on V per disc, %):", [round(100 * (a / fnum(Vt[k]["v_at_last_point_kms"]) - 1), 1) for a, k in zip(Vm_out, IDS)])
P("  measured / model-at-R_out (%):", [round(100 * (x["V"] / a - 1), 1) for x, a in zip(info, Vm_out)])

# ---------------------------------------------------------------- A10 pressure axis
P("\n-- A10 pressure axis: Delta'(s) z for flat / rival / T, crossings, placements vs s_mid (mu = 0.67)")
A10 = {}
for nm, S_ in list(ROWS_FOR_A10.items()) + [("MODEL col 3 (C1)", S_model)]:
    zs = {}
    for s in S_AXIS:
        c = cells_three(S_, AS, spec_s(s))
        zs[s] = {l: c[l]["z"] for l in LAWS}
        zs[s]["cls"] = classes(c)
    cr = crossings(S_, AS)
    above = all((cr["s_mid"] is not None) and (p > cr["s_mid"]) for p in PLACED)
    A10[nm] = dict(z=zs, cross=cr, placements_above_s_mid=above)
    P(f"  {nm:52s} s_mid={cr['s_mid'] if cr['s_mid'] is None else round(cr['s_mid'],3)} s_f2={cr['s_f2'] if cr['s_f2'] is None else round(cr['s_f2'],3)} s_h2={cr['s_h2'] if cr['s_h2'] is None else round(cr['s_h2'],3)} all placed above s_mid: {above}  class@s=0/1: {zs[0.0]['cls']} / {zs[1.0]['cls']}")
RES["A10"] = A10
sm = [v["cross"]["s_mid"] for k, v in A10.items() if v["cross"]["s_mid"] is not None and not k.startswith("MODEL")]
P(f"  s_mid over the measured-marker grid rows: min {min(sm):.3f} max {max(sm):.3f} range {max(sm)-min(sm):.3f}; model-value {A10['MODEL col 3 (C1)']['cross']['s_mid']:.3f}")
RES["A10_range"] = dict(min=min(sm), max=max(sm), range=max(sm) - min(sm))

# ---------------------------------------------------------------- pass/fail (a)
grid_rows = [k for k in RES if k.startswith(("A2 ", "A3 ", "A4 ", "A5 ", "A5x", "A5y", "A7 V-d", "A7 i_SFR")) and isinstance(RES[k], dict) and "class" in RES[k]]
keep = [k for k in grid_rows if RES[k]["class"] == "lean rival"]
noflip = all(RES[k]["rival"]["z"] <= 2.0 for k in grid_rows)
P(f"\n-- (a) verdict: rows A2-A5, A7 (n={len(grid_rows)}): lean rival in {len(keep)} ({len(keep)/len(grid_rows):.2f}); line >= 0.80 -> {'PASS' if len(keep)/len(grid_rows) >= 0.8 and noflip else 'FAIL'}; no row has rival above +2 sigma: {noflip}")
P("   rows not lean rival:", [(k, RES[k]['class']) for k in grid_rows if RES[k]['class'] != 'lean rival'])
RES["a_grid_verdict"] = dict(n=len(grid_rows), keep=len(keep), frac=len(keep) / len(grid_rows), rows_not_rival=[(k, RES[k]["class"]) for k in grid_rows if RES[k]["class"] != "lean rival"])
A5 = RES["A5 V-b both sides, shorter radius"]["class"]
A5xc = RES["A5x farther side alone at the shorter radius"]["class"]
P(f"   V-b flip: A5 (both sides at shorter radius) = {A5}; A5x (farther side alone at the same radius) = {A5xc}; A6 scan classes: " + str({f: d['cls'] for f, d in scan.items()}))
RES["Vb_question"] = dict(A5=A5, A5x=A5xc, scan={f: d["cls"] for f, d in scan.items()})

# ================================================================ B
P("\n" + "=" * 100 + "\n-- B1 leave-one-out (decision cell; T status and break-evens at s=1)")
B1 = {}
for j, k in enumerate(IDS):
    idx = np.array([i for i in range(10) if i != j])
    S_ = subset(prim_S, idx)
    c = cells_three(S_, AS, SP1)
    bes = {l: break_even(S_, AS, SP1, l) for l in LAWS}
    B1[k] = dict(cls=classes(c), z={l: c[l]["z"] for l in LAWS}, dp={l: c[l]["dprime"] for l in LAWS},
                 mu_be={l: bes[l]["mu"] for l in LAWS}, lo_T=bes["T"]["lo"], stT=status(bes["T"]))
    P(f"  drop KURVS-{k:<2d} {B1[k]['cls']:34s} z " + " ".join(f"{c[l]['z']:+.2f}" for l in LAWS) + f"  mu_be(s=1) " + " ".join((f"{bes[l]['mu']:.2f}" if bes[l]['mu'] else 'none') for l in LAWS) + f"  T lower edge {bes['T']['lo']:.2f} -> {status(bes['T'])}")
nrival = sum(1 for d in B1.values() if d["cls"] == "lean rival")
P(f"  lean rival persists in {nrival} of 10 (line >= 8 -> {'PASS' if nrival >= 8 else 'FAIL'}); z_flat range {min(d['z']['flat'] for d in B1.values()):+.2f} .. {max(d['z']['flat'] for d in B1.values()):+.2f}; T gas-allowed at s=1 in {sum(1 for d in B1.values() if d['stT']=='allowed')} of 10")
RES["B1"] = dict(loo=B1, n_rival=nrival)

P("\n-- B2 bootstrap of the ten discs (N=2000, seed 194)")
rng = np.random.default_rng(194)
NB = 2000
cls_count = {}
zs = np.zeros((NB, 3))
Tallowed = 0
for b in range(NB):
    idx = rng.integers(0, 10, 10)
    S_ = subset(prim_S, idx)
    try:
        c = cells_three(S_, AS, SP1)
    except Exception:
        continue
    cl = classes(c)
    cls_count[cl] = cls_count.get(cl, 0) + 1
    zs[b] = [c[l]["z"] for l in LAWS]
    be = break_even(S_, AS, SP1, "T")
    Tallowed += (status(be) == "allowed")
P("  class fractions:", {k: round(v / NB, 3) for k, v in cls_count.items()})
P(f"  P(z_flat > 2) = {np.mean(zs[:,0] > 2):.3f}; P(z_rival within 2) = {np.mean(np.abs(zs[:,1]) <= 2):.3f}; z_flat 16/50/84% = {np.percentile(zs[:,0],[16,50,84]).round(2)}; P(T gas-allowed at s=1) = {Tallowed/NB:.3f}; P(z_T > 2) = {np.mean(zs[:,2] > 2):.3f}")
RES["B2"] = dict(classes={k: v / NB for k, v in cls_count.items()}, P_zflat_gt2=float(np.mean(zs[:, 0] > 2)), P_T_allowed=Tallowed / NB,
                 zflat_pct=np.percentile(zs[:, 0], [16, 50, 84]).tolist())

P("\n-- B3 named subsets")
allmax_clipped = [k for k in IDS if mk[k]["clip"][np.argmax(np.abs(mk[k]["R"]))] == 1]
reach09 = [k for k in IDS if far_side(mk[k])[1] >= 0.9 * RMAX[k]]
ratio = {info[j]["id"]: info[j]["V"] / fnum(Vt[info[j]["id"]]["v_at_last_point_kms"]) - 1 for j in range(10)}
subsets = {
    "drop KURVS-17": [k for k in IDS if k != 17],
    f"drop discs whose outermost plotted marker is clipped {allmax_clipped}": [k for k in IDS if k not in allmax_clipped],
    "drop |measured/model-1| > 15%": [k for k in IDS if abs(ratio[k]) <= 0.15],
    f"keep discs whose farther side reaches >= 0.9 R_max(table) (n={len(reach09)})": reach09,
    "drop KURVS-21 (flagged asymmetric)": [k for k in IDS if k != 21],
    "drop KURVS-13, -17, -21": [k for k in IDS if k not in (13, 17, 21)],
}
B3 = {}
for nm, keepids in subsets.items():
    idx = np.array([IDS.index(k) for k in keepids])
    S_ = subset(prim_S, idx)
    c = cells_three(S_, AS, SP1)
    B3[nm] = dict(cls=classes(c), z={l: c[l]["z"] for l in LAWS}, n=len(idx))
    P(f"  {nm:80s} n={len(idx):2d} " + " ".join(f"{l}:{c[l]['dprime']:+.3f}({c[l]['z']:+.2f})" for l in LAWS) + f" {classes(c)}")
RES["B3"] = B3

P("\n-- B4 extension (labelled, not the headline): all 22 discs with V/sigma0 >= 1.0 and a measured outer point, mu = 0.67")
ids22 = [k for k in sorted(KIN) if fnum(KIN[k]["vrot_over_sigma0"]) >= 1.0]
P("  ids:", ids22)
mk22 = load_markers(ids22)
sg22 = load_sigma(ids22)
try:
    S22, i22 = build(rule_primary, ids=ids22, mk=mk22, sg=sg22)
    xx = S22.R / S22.Reff - 1
    P(f"  x = R_out/R_eff - 1 range {xx.min():.2f}..{xx.max():.2f} (alpha_K clips at [0,4]); V range {S22.V.min():.0f}..{S22.V.max():.0f}")
    c22 = cells_three(S22, AS, SP1)
    P("  extension, primary rule:", fmt_cells(c22))
    Sm22 = M.load_kurvs(ids=tuple(ids22), inc_col="inc_star_deg")
    c22m = cells_three(Sm22, AS, SP1)
    P("  extension, model-value column:", fmt_cells(c22m))
    c22p0 = cells_three(S22, AS, spec_s(0.0))
    P("  extension, primary rule, P0:", fmt_cells(c22p0))
    only12 = [k for k in ids22 if k not in IDS]
    idx = np.array([ids22.index(k) for k in only12])
    S12 = subset(S22, idx)
    c12 = cells_three(S12, AS, SP1)
    P(f"  the {len(only12)} discs NOT in the ten alone:", fmt_cells(c12))
    RES["B4"] = dict(ids=ids22, cells={l: dict(c22[l]) for l in LAWS}, cls=classes(c22), model=classes(c22m), only_new=dict(n=len(only12), cls=classes(c12), z={l: c12[l]["z"] for l in LAWS}))
except Exception as e:
    P("  B4 failed:", repr(e))
    RES["B4"] = dict(error=repr(e))

with open(os.path.join(HERE, "CFG194_attacks_a_results.json"), "w") as f:
    json.dump(RES, f, indent=1, default=jdefault)
P("\ndone")
