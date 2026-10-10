#!/usr/bin/env python3
"""CFG593 POST-HOC diagnostic (dated 2026-10-10; NOT a verdict input; written after the frozen verdict was computed).
Why is the KiDS-allowed region of the family EMPTY even at f = 0 (the family's NFW member) when CFG529's native LCDM passes?
The family is normalised by the framework's census catchment (M_ta = M_g / (f_ret f_b), law r_ta); CFG529's LCDM by the SHMR halo.
  D1  lens-weighted ratios: census M_ta and law-r_ta mass vs the SHMR LCDM turnaround mass (Moster; CFG504 r_ta_lcdm).
  D2  NFW member with the catchment mass scaled by lambda (r_ta at fixed turnaround density, r_ta ~ lambda^(1/3)).
  D3  the family's NFW member and f = 1 members with the SHMR LCDM normalisation (M_ta, r_ta from the SHMR halo).
  D4  the whole family grid with the SHMR LCDM normalisation, intersected with the frozen shear-allowed set (cfg593_shear_results.json):
      the halo model's catchment is itself the LCDM turnaround mass of each halo, so D4 puts both data sets on one normalisation.
Machinery: cfg593_kids.py exec'd up to its results block, with the operator grid extended to 2 x the larger r_ta (coarser grid; disclosed).
  nice -n 10 python3 cfg593_posthoc.py -> cfg593_posthoc.out, cfg593_posthoc_results.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.join(HERE, "cfg593_kids.py")
src = open(PK).read()
src = src.replace("max(rta.values()) * 1.0001", "max(max(rta.values()), TB.EL.r_ta_lcdm(lms, zl, 'moster')[0]) * 2.0")
cut = src.index("res = dict(lane=")
os.environ["CFG593_MUTATE"] = "0"
NS = globals()                                                              # exec'd into __main__ so worker functions pickle by reference
_KEEP = (HERE, PK)
exec(compile(src[:cut], "cfg593_kids_ro", "exec"), NS)
HERE, PK = _KEEP
OUT.clear()
P("CFG593 POST-HOC (dated 2026-10-10; NOT a verdict input). kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
EL = TB.EL

# D1
W = np.zeros(TB.NG)
for k in range(15):
    W += np.bincount(GSET.gi[MASK], weights=GSET.WW[MASK, k], minlength=TB.NG)
LC = {}
for g in GSEL:
    b = BL[g]
    rL, M200 = EL.r_ta_lcdm(b["lms"], b["zl"], "moster")
    rho_ta = EL.rho_m(b["zl"]) * EL.LL.dta(b["zl"])
    LC[g] = dict(rta=rL, Mta=4 * math.pi / 3 * rL ** 3 * rho_ta, rho_ta=rho_ta)
d1 = {}
for ft in FOOTS:
    rc = np.array([BL[g]["Mg"] / (BL[g]["f"] * Lc.FB16) / LC[g]["Mta"] for g in GSEL])
    rl = np.array([4 * math.pi / 3 * BL[g]["rta"][ft] ** 3 * LC[g]["rho_ta"] / LC[g]["Mta"] for g in GSEL])
    w = W[GSEL]
    def wmed(x):
        o = np.argsort(x); c = np.cumsum(w[o]); return float(x[o][np.searchsorted(c, 0.5 * c[-1])])
    d1[ft] = dict(census_Mta_over_LCDM_Mta_wmedian=wmed(rc), lawrta_mass_over_LCDM_Mta_wmedian=wmed(rl),
                  rta_law_over_rta_LCDM_wmedian=wmed(np.array([BL[g]["rta"][ft] / LC[g]["rta"] for g in GSEL])))
    P(f"D1 [{ft}] lens-weighted medians: census M_ta / LCDM M_ta {d1[ft]['census_Mta_over_LCDM_Mta_wmedian']:.3f}; "
      f"law-r_ta mass / LCDM M_ta {d1[ft]['lawrta_mass_over_LCDM_Mta_wmedian']:.3f}; r_ta,law / r_ta,LCDM {d1[ft]['rta_law_over_rta_LCDM_wmedian']:.3f}")


def Md_member(g, Mta, rta, xe, f, foot, y=0):
    b = BL[g]; Mg = b["Mg"]; a0 = Cc.A0[foot]; supply = (1 - Lc.FB) * Mta
    MLx = FL.ML_shape(math.log10(Mta * Lc.H16))[0]
    re = min(xe * rta, rta); rin = y * math.sqrt(Cc.G_MPC * Mg / a0); rg = b["r"]
    def grid(re_):
        rr = np.unique(np.concatenate([rg[rg < rta], [x for x in (re_, rin) if 0 < x < rta], [rta]]))
        S = Mg * (Cc.nu_mono(Cc.G_MPC * Mg / rr ** 2 / a0) - 1.0)
        return rr, np.full_like(rr, Mg), S, Mta * MLx(rr / rta)
    rr, mb, S, ML = grid(re)
    M, inf = FL.family_cum(rr, mb, S, ML, Mta, re, rin, f, supply, True)
    if M is None:
        re = inf["re_new"]; rr, mb, S, ML = grid(re)
        M, inf = FL.family_cum(rr, mb, S, ML, Mta, re, rin, f, supply, cap=False)
    return np.interp(rg, rr, M - Mg)


def task(args):
    kind, ft, lam, xe, f = args[:5]; y = args[5] if len(args) > 5 else 0
    Md = {}
    for g in GSEL:
        b = BL[g]
        if kind == "census":
            Mta = lam * b["Mg"] / (b["f"] * Lc.FB16); rta = b["rta"][ft] * lam ** (1 / 3)
        else:
            Mta = lam * LC[g]["Mta"]; rta = LC[g]["rta"] * lam ** (1 / 3)
        Md[g] = Md_member(g, Mta, rta, xe, f, ft, y)
    o = score_profiles(Md)
    return args, dict(chi2_A=o["A"]["chi2"], chi2_B=o["B"]["chi2"], p_A=o["A"]["p"], p_B=o["B"]["p"], inner9_A=o["A"]["chi2_inner9"], outer6_A=o["A"]["chi2_outer6"],
                      inner9_B=o["B"]["chi2_inner9"], outer6_B=o["B"]["chi2_outer6"], allowed=o["allowed"])


LAMS = [0.5, 0.7, 1.0, 1.4, 2.0, 3.0]
tasks = [("census", ft, l, 1.0, 0.0) for ft in FOOTS for l in LAMS]
tasks += [("lcdm", ft, 1.0, xe, f) for ft in FOOTS for (xe, f) in ((1.0, 0.0), (0.45, 1.0), (0.7, 1.0), (0.85, 1.0), (0.45, 0.5))]
with MP.get_context("fork").Pool(4) as pool:
    R = dict(pool.map(task, tasks))
res = dict(lane="CFG593", script="cfg593_posthoc", date="2026-10-10", note="POST-HOC, not a verdict input", D1=d1, D2={}, D3={}, D4={})
for (kind, ft, l, xe, f), o in R.items():
    tag = f"{kind}|{ft}|lam{l}|xe{xe}|f{f}"
    (res["D2"] if kind == "census" else res["D3"])[tag] = o
    P(f"{'D2' if kind == 'census' else 'D3'} [{ft}] {kind:6s} normalisation x {l:.1f}, x_e {xe}, f {f}: A {o['chi2_A']:.2f} (p {o['p_A']:.1e}; inner9 {o['inner9_A']:.1f} outer6 {o['outer6_A']:.1f}) "
      f"B {o['chi2_B']:.2f} (p {o['p_B']:.1e}; inner9 {o['inner9_B']:.1f} outer6 {o['outer6_B']:.1f}) -> {'ALLOWED' if o['allowed'] else 'excluded'}")
JS = json.load(open(os.path.join(HERE, "cfg593_shear_results.json")))
PTS = FL.family_points()
t4 = [("lcdm", ft, 1.0, xe, f, y) for ft in FOOTS for (xe, f, y) in PTS]
with MP.get_context("fork").Pool(4) as pool:
    R4 = dict(pool.map(task, t4, chunksize=4))
for ft in FOOTS:
    kd = {}; ov = []
    for (xe, f, y) in PTS:
        o = R4[("lcdm", ft, 1.0, xe, f, y)]; k = f"{xe:.2f}|{f:.1f}|{y}"
        sh = JS["scan"][f"{ft}|cen|{k}"]
        kd[k] = dict(xe=xe, f=f, y=y, chi2_A=o["chi2_A"], chi2_B=o["chi2_B"], kids_allowed=o["allowed"], shear_allowed=sh["allowed_fid"], shear_Zmax=sh["Zmax_best_fid"])
        if o["allowed"] and sh["allowed_fid"]:
            ov.append(k)
    na = sum(v["kids_allowed"] for v in kd.values())
    res["D4"][ft] = dict(points=kd, n_kids_allowed=int(na), overlap=ov)
    P(f"D4 [{ft}] SHMR-LCDM normalisation: KiDS-allowed {na} / {len(PTS)}; overlap with the frozen shear-allowed set: {len(ov)} points")
    for f in FL.F_GRID:
        row = []
        for y in (FL.Y_GRID if f < 1 else [0]):
            xs = [xe for xe in FL.XE_GRID if f"{xe:.2f}|{f:.1f}|{y}" in ov]
            row.append(",".join(f"{x:g}" for x in xs) if xs else "-")
        P(f"     overlap f {f:.1f}: " + " | ".join(row))
    for f in FL.F_GRID:
        P(f"     KiDS max chi2 y=0 f {f:.1f}: " + " ".join(f"{max(kd[f'{xe:.2f}|{f:.1f}|0']['chi2_A'], kd[f'{xe:.2f}|{f:.1f}|0']['chi2_B']):6.1f}" for xe in FL.XE_GRID))
json.dump(res, open(os.path.join(HERE, "cfg593_posthoc_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg593_posthoc.out"), "w").write("\n".join(OUT) + "\n")
