#!/usr/bin/env python3
"""CFG593 constraint (b) (FROZEN_CRITERIA.md sections 2, 3b, 6, 7, 8): the declared profile family against KiDS f30 galaxy lensing,
CFG529's constructions A and B (measured W30 leakage, SHMR term propagated by CFG529's score_vecs), both footings.

Method: the ESD of CFG504's kids_fin / truncate / window is LINEAR in the enclosed-mass profile, so each f30 group gets a fixed linear
operator (15 bins x grid) per construction and SHMR (mixing (1 - f_o) full + f_o stripped built in); any profile is then scored exactly
on that grid.  Controls K3 (i) operator = CFG504 code on the same grid, (ii) lane-convention census reproduces CFG529's stored chi2,
(iii) CFG529's native LCDM rows.
Machinery read-only: CFG529 cfg529_tables (imported) and cfg529_score (exec'd up to its controls block), CFG504 cfg504_own, CFG100 lib,
CFG515 lib, CFG556 (NFW shape via cfg593_lib).

  nice -n 10 python3 cfg593_kids.py                   -> cfg593_kids.out, cfg593_kids_results.json
  CFG593_MUTATE=1 nice -n 10 python3 cfg593_kids.py   -> *_MUTATE.* (MU2: LCDM native rows and the family NFW member inside (b);
                                                          MU1 context: framework census outside) exit 1 = all teeth bite
DIAGNOSTIC, data-driven: allowed profiles are what the data require, not a framework derivation.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, io, json, math, time, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np
import multiprocessing as MP

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg593_lib as FL
LANES = FL.LANES
MUT = os.environ.get("CFG593_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
try:
    os.nice(10)
except OSError:
    pass
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

sys.path.insert(0, os.path.join(LANES, "CFG529_f30_matched_environment"))
with contextlib.redirect_stdout(io.StringIO()):
    import cfg529_tables as TB                                               # noqa: E402  (read-only)
Lc, Cc, O = TB.L, TB.C, TB.O
GSEL = TB.GSEL; FOOTS = TB.FOOTS; SHMRS = TB.SHMRS
NGR = 360
FL.H556()

P(f"CFG593 KiDS {'(MUTATE)' if MUT else ''} -- FROZEN_CRITERIA.md. kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
P("DIAGNOSTIC, data-driven: allowed profiles are what the data require, NOT a framework derivation.")


# ---------------------------------------------------------------- linear operators
def interp_matrix(xq, r):
    """rows: weights such that W @ M = np.interp(xq, r, M)."""
    xq = np.asarray(xq, float); n = len(r); W = np.zeros((len(xq), n)); i = np.arange(len(xq))
    lo = xq <= r[0]; hi = xq >= r[-1]; mid = ~(lo | hi)
    W[i[lo], 0] = 1.0; W[i[hi], n - 1] = 1.0
    j = np.searchsorted(r, xq[mid]) - 1; t = (xq[mid] - r[j]) / (r[j + 1] - r[j])
    W[i[mid], j] = 1 - t; W[i[mid], j + 1] = t
    return W


def kfin_matrix(Mg, r):
    """ESD (15 bins, CFG100 _finish units) = Kf @ M + c  for kids_fin(Mg, r, M)."""
    Rn = np.sqrt(Cc.G_MPC * Mg / Cc.GN).ravel()
    R = Rn[:, None]
    r1 = r[None, :-1]; r2 = r[None, 1:]; dr = np.diff(r)[None, :]
    a1 = np.maximum(r1, R); a2 = np.maximum(r2, R)
    F = lambda x: np.sqrt(np.maximum(x * x - R * R, 0.0)) - R * np.arccos(np.minimum(R / x, 1.0))
    Ac = lambda x: np.arccos(np.minimum(R / x, 1.0))
    Gm = 1.0 / (math.pi * R ** 2) - (F(a2) - F(a1)) / dr / (math.pi * R ** 2) - (Ac(a2) - Ac(a1)) / dr / (2 * math.pi * R)
    n = len(r)
    D = np.zeros((n - 1, n)); D[np.arange(n - 1), np.arange(n - 1)] = -1.0; D[np.arange(n - 1), np.arange(1, n)] = 1.0
    Kds = Gm @ D; Kds[:, 0] += 1.0 / (math.pi * Rn ** 2)
    WN = Cc.WN; Q = np.zeros((15, len(Rn)))
    for b in range(15):
        Q[b, b * WN.shape[1]:(b + 1) * WN.shape[1]] = WN[b] / WN[b].sum()
    Kf = Q @ Kds * 1e-12
    c = Q @ (Mg / (math.pi * Rn ** 2)) * 1e-12
    return Kf, c


def trunc_matrix(r, w):
    n = len(r); T = w[-1] * np.eye(n)
    nz = np.nonzero(w[:-1] > 0)[0]
    for j in nz:
        T += w[j] * interp_matrix(np.minimum(r, O.RTC[j]), r)
    return T


def window_matrix(r, rw, xt):
    n = len(r); rm = np.sqrt(r[1:] * r[:-1])
    f0 = O.ft(r[0] / rw, xt); fk = O.ft(rm / rw, xt)
    Wm = np.zeros((n, n)); Wm[:, 0] = f0
    for i in range(1, n):
        Wm[i, :] = Wm[i - 1, :]
        Wm[i, i - 1] -= fk[i - 1]; Wm[i, i] += fk[i - 1]
    return Wm


def build(g):
    Mg, zl, lms = float(TB.GM[g]), float(TB.GZ[g]), float(TB.GS[g])
    W, RTL, XTW = TB.setup(Mg, zl, lms)
    rta = {ft: Cc.r_ta_law(Mg, Cc.A0[ft], zl) for ft in FOOTS}
    r = np.geomspace(1e-4, max(rta.values()) * 1.0001, NGR)
    Kf, c = kfin_matrix(Mg, r)
    ops = {}
    for s in SHMRS:
        Ts = trunc_matrix(r, W[f"{s}_W30"])
        Ws = window_matrix(r, RTL[s], XTW[s]["prim"])
        fo = FO[s][g]
        ops[("A", s)] = (1 - fo) * Kf + fo * (Kf @ Ts)
        ops[("B", s)] = (1 - fo) * (Kf @ Ws) + fo * (Kf @ Ws @ Ts)
    f, lMta = Lc.fret_census(Mg)
    return g, dict(r=r, c=c, eff=ops, rta=rta, f=f, lMta=lMta, Mg=Mg, zl=zl, lms=lms)


# ---------------------------------------------------------------- CFG529 scoring environment (exec'd read-only)
P529 = os.path.join(LANES, "CFG529_f30_matched_environment", "cfg529_score.py")
_src = open(P529).read(); _cut = _src.index("# ------------------------------------------------------------------ controls K2-K6")
NS = {"__file__": P529, "__name__": "cfg529_ro"}
_e = os.environ.pop("CFG529_MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_cut], "cfg529_score", "exec"), NS)
env_cfg, evec, score_vecs, SMP, MEAS, CONS, model_score = (NS[k] for k in ("env_cfg", "evec", "score_vecs", "SMP", "MEAS", "CONS", "model_score"))
EC30 = {c: env_cfg(c, "f30", MEAS["f30"], MEAS["f30"], "meas") for c in CONS}
GSET, MASK, _ = SMP["f30"]
J529 = json.load(open(os.path.join(LANES, "CFG529_f30_matched_environment", "cfg529_score_results.json")))
J557K = json.load(open(os.path.join(LANES, "CFG557_settling_catchment_derived", "cfg557_kids_results.json")))
J559K = json.load(open(os.path.join(LANES, "CFG559_kinetic_settled_profile", "cfg559_kids_results.json")))
FO = {s: np.clip(GSET.interp(np.clip(MEAS["f30"][s], 0, 1)), 0, 1) for s in SHMRS}
EV = {(c, s): evec(GSET, c, s, "W30", EC30[c]["fE"][s], EC30[c]["tag"] + "|W30") for c in CONS for s in SHMRS}
P(f"  CFG529 environment loaded ({time.time() - T0:.0f} s); f30 groups {len(GSEL)}")

with MP.get_context("fork").Pool(4) as pool:
    BL = dict(pool.map(build, list(GSEL), chunksize=8))
P(f"  operators built for {len(BL)} groups ({time.time() - T0:.0f} s)")


def score_profiles(Md):
    """Md: {g: enclosed non-point mass on BL[g]['r']} -> {cons: score dict}."""
    out = {}
    for c in CONS:
        m = {}
        for s in SHMRS:
            tab = np.zeros((TB.NG, 15))
            for g in GSEL:
                tab[g] = BL[g]["eff"][(c, s)] @ Md[g] + BL[g]["c"] + EV[(c, s)][g]
            m[s] = GSET.stack(tab, MASK)
        o = score_vecs("f30", m["moster"], m["behroozi"])
        out[c] = {k: v for k, v in o.items() if k not in ("model", "model_behroozi")}
    out["allowed"] = bool(all(out[c]["p"] > 0.01 for c in CONS))
    return out


# ---------------------------------------------------------------- family profiles for a KiDS lens
SHAPES = {}
def shape(g):
    if g not in SHAPES:
        SHAPES[g] = FL.ML_shape(BL[g]["lMta"])[0]
    return SHAPES[g]


for _g in GSEL:
    shape(_g)
P(f"  NFW shapes at the census M_ta cached ({time.time() - T0:.0f} s)")


def lens_Md(g, foot, xe, f, y, conv="total", mode="family"):
    b = BL[g]; Mg = b["Mg"]; a0 = Cc.A0[foot]; rta = b["rta"][foot]; fr = b["f"]
    Mta = Mg / (fr * Lc.FB16); supply = (1 - Lc.FB) * Mta
    rM = math.sqrt(Cc.G_MPC * Mg / a0)
    cap = True
    if mode == "census":
        re = min(Lc.r_edge_pm(Mg, Cc.G_MPC, a0, fr), rta); f, rin = 1.0, 0.0; cap = False
    elif mode == "emg":
        re = rta; f, rin = 1.0, 0.0
    else:
        re = min(xe * rta, rta); rin = y * rM
    rg = b["r"]; MLx = shape(g)

    def grid(re_, rin_):
        rr = np.unique(np.concatenate([rg[rg < rta], [x for x in (re_, rin_) if 0 < x < rta], [rta]]))
        S = Mg * (Cc.nu_mono(Cc.G_MPC * Mg / rr ** 2 / a0) - 1.0)
        return rr, np.full_like(rr, Mg), S, Mta * MLx(rr / rta)
    rr, mb, S, ML = grid(re, rin)
    M, inf = FL.family_cum(rr, mb, S, ML, Mta, re, rin, f, supply, cap)
    if M is None:
        re = inf["re_new"]; rr, mb, S, ML = grid(re, rin)
        M, inf = FL.family_cum(rr, mb, S, ML, Mta, re, rin, f, supply, cap=False)
    if conv == "lane":                                    # unsettled cold energy not in the own profile (CFG529 / 557 / 559)
        rin_ = min(rin, re)
        S_in = np.interp(np.minimum(rr, rin_), rr, S); S_e = np.interp(np.minimum(rr, re), rr, S)
        M = Mg + S_in + f * (S_e - S_in)
    return np.interp(rg, rr, M - Mg), dict(re_over_rta=re / rta)


def score_point(args):
    foot, xe, f, y, conv, mode = args
    Md = {}; xs = []
    for g in GSEL:
        Md[g], inf = lens_Md(g, foot, xe, f, y, conv, mode); xs.append(inf["re_over_rta"])
    o = score_profiles(Md); o["re_over_rta_median"] = float(np.median(xs))
    return args, o


res = dict(lane="CFG593", script="cfg593_kids", date="2026-10-10", mutate=MUT, n_groups=int(len(GSEL)), grid_points=NGR,
           settings="kappa = 1/2 FITTED; footings never pooled; nu_mono; candidate B; cold energy mass required; not theory closed; DIAGNOSTIC data-driven")

# controls
lcdm = {f"{c}|{ft}": model_score(EC30[c], "LCDM", ft) for c in CONS for ft in FOOTS}
k3iii = max(abs(lcdm[f"{c}|{ft}"]["chi2"] - J529["rescore_f30"][c][ft]["rows"]["LCDM"]["chi2"]) for c in CONS for ft in FOOTS)
P(f"\nK3 (iii) CFG529 native LCDM f30 chi2: A {lcdm['A|canonical']['chi2']:.3f} (p {lcdm['A|canonical']['p']:.3f}), B {lcdm['B|canonical']['chi2']:.3f} "
  f"(p {lcdm['B|canonical']['p']:.3f}); max |d| vs stored {k3iii:.1e} -> {'PASS' if k3iii <= 0.01 else 'FAIL'}")
res["LCDM_native"] = {k: {kk: vv for kk, vv in v.items() if kk not in ("model", "model_behroozi")} for k, v in lcdm.items()}
res["LCDM_native_allowed"] = bool(all(lcdm[f"{c}|{ft}"]["p"] > 0.01 for c in CONS for ft in FOOTS))

rng = np.random.default_rng(593); G5 = rng.choice(GSEL, 5, replace=False)
k3i = 0.0
for g in G5:
    b = BL[g]; r = b["r"]; foot = "canonical"; a0 = Cc.A0[foot]; rta = b["rta"][foot]
    Md = b["Mg"] * (Cc.nu_mono(Cc.G_MPC * b["Mg"] / np.minimum(r, 0.4 * rta) ** 2 / a0) - 1.0)
    W, RTL, XTW = TB.setup(b["Mg"], b["zl"], b["lms"])
    for s in SHMRS:
        fo = FO[s][g]
        dA = (1 - fo) * O.kids_fin(b["Mg"], r, Md) + fo * O.kids_fin(b["Mg"], r, O.truncate(r, Md, W[f"{s}_W30"]))
        xt = XTW[s]["prim"]
        dB = (1 - fo) * O.kids_fin(b["Mg"], r, O.window(r, Md, RTL[s], xt)) + fo * O.kids_fin(b["Mg"], r, O.window(r, O.truncate(r, Md, W[f"{s}_W30"]), RTL[s], xt))
        for d, c in ((dA, "A"), (dB, "B")):
            mine = b["eff"][(c, s)] @ Md + b["c"]
            k3i = max(k3i, float(np.max(np.abs(mine - d) / np.abs(d))))
P(f"K3 (i) linear operator vs CFG504 kids_fin / truncate / window on the same grid, 5 random groups, A and B, both SHMRs: max rel {k3i:.1e} -> {'PASS' if k3i <= 1e-8 else 'FAIL'}")

with MP.get_context("fork").Pool(4) as pool:
    ctl = dict(pool.map(score_point, [(ft, 0, 0, 0, "lane", "census") for ft in FOOTS]
                        + [(ft, 0, 0, 0, "total", "census") for ft in FOOTS] + [(ft, 0, 0, 0, cv, "emg") for ft in FOOTS for cv in ("total", "lane")]
                        + [(ft, 1.0, 0.0, 0, cv, "family") for ft in FOOTS for cv in ("total", "lane")]))
k3ii = {f"{c}|{ft}": ctl[(ft, 0, 0, 0, "lane", "census")][c]["chi2"] - J529["rescore_f30"][c][ft]["rows"]["CENSUS"]["chi2"] for c in CONS for ft in FOOTS}
k3iip = all(abs(v) <= 0.5 for v in k3ii.values())
P(f"K3 (ii) lane-convention census through the operators vs CFG529 stored census chi2: d = {', '.join(f'{k} {v:+.3f}' for k, v in k3ii.items())} -> {'PASS' if k3iip else 'FAIL'}")
res["controls"] = dict(K3i=k3i, K3i_pass=k3i <= 1e-8, K3ii=k3ii, K3ii_pass=k3iip, K3iii=k3iii, K3iii_pass=k3iii <= 0.01)

def fmt(o):
    return f"A {o['A']['chi2']:.2f} (p {o['A']['p']:.1e}) B {o['B']['chi2']:.2f} (p {o['B']['p']:.1e}) -> {'ALLOWED' if o['allowed'] else 'excluded'}"

P("\nRecord rules and reference profiles on KiDS f30 (b):")
rec = {}
for ft in FOOTS:
    rec[ft] = {
        "CFG556/541 census edge, lane convention (this path)": ctl[(ft, 0, 0, 0, "lane", "census")],
        "CFG556/541 census edge, total profile": ctl[(ft, 0, 0, 0, "total", "census")],
        "emergent edge (x_e = 1, supply cap), total": ctl[(ft, 0, 0, 0, "total", "emg")],
        "emergent edge (x_e = 1, supply cap), lane": ctl[(ft, 0, 0, 0, "lane", "emg")],
        "family NFW member (x_e = 1, f = 0), total": ctl[(ft, 1.0, 0.0, 0, "total", "family")],
        "family NFW member (x_e = 1, f = 0), lane": ctl[(ft, 1.0, 0.0, 0, "lane", "family")],
        "CFG529 census (stored)": {c: {k: J529["rescore_f30"][c][ft]["rows"]["CENSUS"][k] for k in ("chi2", "p", "chi2_inner9", "chi2_outer6")} for c in CONS},
        "CFG557 finite-age supply (stored)": {c: {k: J557K["scores"][ft]["rows"][c][k] for k in ("chi2", "p", "chi2_inner9", "chi2_outer6")} for c in CONS},
        "CFG559 kinetic PRIMARY (stored)": {c: {k: J559K["scores"][ft]["PRIMARY_kin"]["rows"][c][k] for k in ("chi2", "p", "chi2_inner9", "chi2_outer6")} for c in CONS},
        "CFG559 kinetic full supply (stored)": {c: {k: J559K["scores"][ft]["VARIANT_full_kin"]["rows"][c][k] for k in ("chi2", "p", "chi2_inner9", "chi2_outer6")} for c in CONS},
        "LCDM native (CFG529)": {c: res["LCDM_native"][f"{c}|{ft}"] for c in CONS}}
    for n, o in rec[ft].items():
        if "allowed" not in o:
            o["allowed"] = bool(all(o[c]["p"] > 0.01 for c in CONS))
        P(f"  [{ft:9s}] {n:52s} {fmt(o)}")
res["record_rules"] = rec

if MUT:
    teeth = {}
    for ft in FOOTS:
        nfw = rec[ft]["family NFW member (x_e = 1, f = 0), total"]
        teeth[ft] = dict(MU2_LCDM_inside=bool(rec[ft]["LCDM native (CFG529)"]["allowed"]), MU2_nfw_member_inside=bool(nfw["allowed"]),
                         MU1ctx_census_outside=bool(not rec[ft]["CFG529 census (stored)"]["allowed"]))
        P(f"  [{ft}] MU2 LCDM native inside (b): {teeth[ft]['MU2_LCDM_inside']}; family NFW member inside (b): {teeth[ft]['MU2_nfw_member_inside']} (reported); "
          f"framework census outside (b): {teeth[ft]['MU1ctx_census_outside']}")
    allb = all(v["MU2_LCDM_inside"] and v["MU1ctx_census_outside"] for v in teeth.values())
    res["teeth"] = teeth; res["all_teeth_bite"] = bool(allb)
    P(f"\nMUTATE (KiDS): LCDM inside and framework census outside on both footings -> {allb}")
else:
    PTS = FL.family_points()
    tasks = [(ft, xe, f, y, cv, "family") for ft in FOOTS for cv in ("total", "lane") for (xe, f, y) in PTS]
    P(f"\nscoring {len(tasks)} family points (4 processes)")
    with MP.get_context("fork").Pool(4) as pool:
        SC = dict(pool.map(score_point, tasks, chunksize=4))
    scan = {}
    for (ft, xe, f, y, cv, _), o in SC.items():
        scan[f"{ft}|{cv}|{xe:.2f}|{f:.1f}|{y}"] = dict(xe=xe, f=f, y=y, allowed=o["allowed"], chi2_A=o["A"]["chi2"], p_A=o["A"]["p"], chi2_B=o["B"]["chi2"], p_B=o["B"]["p"],
                                                       inner9_A=o["A"]["chi2_inner9"], outer6_A=o["A"]["chi2_outer6"], inner9_B=o["B"]["chi2_inner9"], outer6_B=o["B"]["chi2_outer6"],
                                                       re_over_rta_median=o["re_over_rta_median"])
    res["scan"] = scan
    P("KiDS-allowed region (p > 0.01 in A and B): allowed x_e at each f (y = 0 | 1 | 3 | 10)")
    for ft in FOOTS:
        for cv in ("total", "lane"):
            na = sum(1 for k, v in scan.items() if k.startswith(f"{ft}|{cv}|") and v["allowed"])
            best = min((v for k, v in scan.items() if k.startswith(f"{ft}|{cv}|")), key=lambda v: max(v["chi2_A"], v["chi2_B"]))
            P(f"  [{ft} | {cv}] {na} / {len(PTS)} allowed; best max(chi2_A, chi2_B) {max(best['chi2_A'], best['chi2_B']):.2f} at x_e {best['xe']} f {best['f']} y {best['y']} "
              f"(A {best['chi2_A']:.2f} p {best['p_A']:.1e}; B {best['chi2_B']:.2f} p {best['p_B']:.1e})")
            for f in FL.F_GRID:
                row = []
                for y in (FL.Y_GRID if f < 1 else [0]):
                    xs = [xe for xe in FL.XE_GRID if scan[f"{ft}|{cv}|{xe:.2f}|{f:.1f}|{y}"]["allowed"]]
                    row.append(",".join(f"{x:g}" for x in xs) if xs else "-")
                P(f"     f {f:.1f}: " + " | ".join(row))
    for ft in FOOTS:
        P(f"  [{ft}] max(chi2_A, chi2_B), total, y = 0: rows f = 0..1, columns x_e = " + " ".join(f"{x:g}" for x in FL.XE_GRID))
        for f in FL.F_GRID:
            P(f"     f {f:.1f}: " + " ".join(f"{max(scan[f'{ft}|total|{xe:.2f}|{f:.1f}|0']['chi2_A'], scan[f'{ft}|total|{xe:.2f}|{f:.1f}|0']['chi2_B']):6.1f}" for xe in FL.XE_GRID))

P(f"\nelapsed {time.time() - T0:.0f} s")
json.dump(res, open(os.path.join(HERE, f"cfg593_kids_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg593_kids{SUF}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    sys.exit(1 if res["all_teeth_bite"] else 0)
