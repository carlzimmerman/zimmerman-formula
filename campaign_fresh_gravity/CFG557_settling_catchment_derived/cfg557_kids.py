#!/usr/bin/env python3
"""CFG557 task 2 (iii) (FROZEN_CRITERIA.md, criteria commit 5149a12f1): KiDS f30 isolated lenses with the derived catchment edge.
Machinery: CFG529's cfg529_score.py exec'd read-only up to its controls block (as CFG531 does) and CFG529's cfg529_tables.py imported
read-only (setup / variants = its own-profile table path).  ONE change: the direct edge r_e = r_M / ln(1 + f f_b / ((1 - f_b) s_c*)),
f = census f_ret(M_b), s_c* = the tested catchment at the group's census M_ta and lens redshift (cfg557_lib), min(r_e, r_ta).
Tables cached outside git: ../../../_external_data/cfg557_work/cfg557_kids_tables.npz
  nice -n 10 python3 cfg557_kids.py              -> cfg557_kids.out, cfg557_kids_results.json
  CFG557_MUTATE=1 nice -n 10 python3 cfg557_kids.py -> *_MUTATE.*  (MU1: s_c = 1 tables reproduce CFG529's census tables and chi2; exit 1 = bites)
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, io, json, math, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
import multiprocessing as MP

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, HERE)
MUTATE = os.environ.get("CFG557_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg557_work"))
os.makedirs(WORK, exist_ok=True)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
try:
    os.nice(10)
except OSError:
    pass

import cfg557_lib as LIB
JD = json.load(open(os.path.join(HERE, "cfg557_derive_results.json")))
TESTED = JD["verdict"]["tested"]
ALPHA = math.inf if TESTED == "ff" else 1.0

# ------------------------------------------------------------------ CFG529 tables module (read-only import; __main__ guarded)
sys.path.insert(0, os.path.join(LANES, "CFG529_f30_matched_environment"))
with contextlib.redirect_stdout(io.StringIO()):
    import cfg529_tables as TB                                               # noqa: E402
Lc, Cc = TB.L, TB.C
GSEL = TB.GSEL

def edge_new(Mg, a0, f, sc):
    """CFG529's direct census edge path (L.r_edge_pm) with the supply x sc."""
    re0 = Lc.r_edge_pm(Mg, Cc.G_MPC, a0, f)
    return re0 * Lc.ln_fac(f) / math.log1p(f * Lc.FB / ((1.0 - Lc.FB) * sc))

def work(args):
    g, scs = args                                                           # scs: {foot: s_c}
    Mg, zl, lms = TB.GM[g], TB.GZ[g], TB.GS[g]
    W, RTL, XTW = TB.setup(Mg, zl, lms)
    out = {}
    for foot in TB.FOOTS:
        a0 = Cc.A0[foot]
        rta = Cc.r_ta_law(Mg, a0, zl)
        rext = max(max(8 * XTW[s][w] * RTL[s] for s in TB.SHMRS for w in TB.O.WINS), 6 * rta)
        f = Lc.fret("census", Mg)
        re = edge_new(Mg, a0, f, scs[foot])
        out[f"{foot}|x"] = re / rta; out[f"{foot}|re_Mpc"] = re; out[f"{foot}|sc"] = scs[foot]
        for v, arr in TB.variants(Mg, zl, a0, min(re, rta), rext, W, RTL, XTW).items():
            out[f"{foot}|{v}"] = arr
    return g, out

if __name__ == "__main__":
    P(f"CFG557 KiDS {'(MUTATE)' if MUTATE else ''} -- FROZEN_CRITERIA.md (5149a12f1). kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
    P(f"Derivation verdict: {JD['verdict']['label']}; tested catchment = '{TESTED}'")
    # ---------------------------------------------------------- s_c* per f30 group at its census M_ta and lens redshift
    if MUTATE:
        rng = np.random.default_rng(557)
        GG = np.sort(rng.choice(GSEL, 20, replace=False))
        SC = {g: {f: 1.0 for f in TB.FOOTS} for g in GG}
    else:
        GG = GSEL
        ZN = np.round(np.arange(0.10, 0.501, 0.05), 3)
        EP = {z: LIB.Epoch(float(z)) for z in ZN}
        P(f"  epochs built ({time.time() - T0:.0f} s)")
        SC = {}
        for g in GG:
            Mg, zl = float(TB.GM[g]), float(TB.GZ[g])
            f, lMta = Lc.fret_census(Mg)
            Mta_h = 10 ** lMta; Mb_h = Mg * Lc.H16
            j = int(np.clip(np.searchsorted(ZN, zl) - 1, 0, len(ZN) - 2)); w = (zl - ZN[j]) / (ZN[j + 1] - ZN[j])
            row = {}
            for foot in TB.FOOTS:
                s0 = LIB.s_catch(EP[ZN[j]], Mta_h, Mb_h, foot, ALPHA); s1 = LIB.s_catch(EP[ZN[j + 1]], Mta_h, Mb_h, foot, ALPHA)
                row[foot] = (1 - w) * s0 + w * s1
            SC[g] = row
        P(f"  s_c* for {len(GG)} f30 groups ({time.time() - T0:.0f} s): canonical median {np.median([v['canonical'] for v in SC.values()]):.3f} "
          f"(range {min(v['canonical'] for v in SC.values()):.3f}-{max(v['canonical'] for v in SC.values()):.3f}), alt median {np.median([v['alt'] for v in SC.values()]):.3f}")
    cache = os.path.join(WORK, f"cfg557_kids_tables{SUF}.npz")
    with MP.get_context("fork").Pool(4) as pool:
        resl = pool.map(work, [(g, SC[g]) for g in GG], chunksize=4)
    P(f"  tables built for {len(resl)} groups ({time.time() - T0:.0f} s)")
    keys = resl[0][1].keys()
    TAB = {}
    for k in keys:
        a0_ = np.asarray(resl[0][1][k])
        arr = np.full((TB.NG,) + a0_.shape, np.nan)
        for g, o in resl:
            arr[g] = o[k]
        TAB[k] = arr
    np.savez_compressed(cache, **TAB)

    # ---------------------------------------------------------- CFG529 scorer, exec'd read-only up to its controls block
    P529 = os.path.join(LANES, "CFG529_f30_matched_environment", "cfg529_score.py")
    _src = open(P529).read()
    _cut = _src.index("# ------------------------------------------------------------------ controls K2-K6")
    NS = {"__file__": P529, "__name__": "cfg529_ro"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(_src[:_cut], "cfg529_score", "exec"), NS)
    env_cfg, evec, score_vecs, SMP, MEAS, T29, SHMRS, CONS, FOOTS = (NS[k] for k in ("env_cfg", "evec", "score_vecs", "SMP", "MEAS", "T29", "SHMRS", "CONS", "FOOTS"))
    EC30 = {c: env_cfg(c, "f30", MEAS["f30"], MEAS["f30"], "meas") for c in CONS}
    J529 = json.load(open(os.path.join(LANES, "CFG529_f30_matched_environment", "cfg529_score_results.json")))

    def tabs_of(src, pre, cons, s, K):
        if cons == "A":
            return src[pre + "full"], src[pre + f"tr_{s}_{K}"]
        return src[pre + f"prim_full_{s}"], src[pre + f"prim_tr_{s}_{K}"]

    def score(ec, src, pre):
        gset, mask, _ = SMP[ec["sample"]]; K = ec["K"]
        m = {}
        for s in SHMRS:
            E = evec(gset, ec["cons"], s, K, ec["fE"][s], ec["tag"] + f"|{K}")
            fo = np.clip(gset.interp(np.clip(ec["fO"][s], 0, 1)), 0, 1)[:, None]
            full, tr = tabs_of(src, pre, ec["cons"], s, K)
            tab = (1 - fo) * full + fo * tr + E
            tab = np.where(np.isfinite(tab), tab, 0.0)
            m[s] = gset.stack(tab, mask)
        return score_vecs(ec["sample"], m["moster"], m["behroozi"])

    res = dict(lane="CFG557", script="cfg557_kids", date="2026-10-10", mutate=MUTATE, criteria_commit="5149a12f1", tested=TESTED,
               derivation_label=JD["verdict"]["label"], settings="kappa = 1/2 FITTED; footings never pooled; nu_mono; cold energy mass required; not theory closed")
    # control: CFG529's census tables through this scorer reproduce its stored census chi2
    dmx = 0.0
    for c in CONS:
        for foot in FOOTS:
            ch = score(EC30[c], T29, f"{foot}|dir|census|")["chi2"]
            dmx = max(dmx, abs(ch - J529["rescore_f30"][c][foot]["rows"]["CENSUS"]["chi2"]))
    P(f"\nKK0 this scorer on CFG529's census tables reproduces its stored census chi2 (A/B, both footings): max |d| {dmx:.1e} (<= 1e-6) -> {'PASS' if dmx <= 1e-6 else 'FAIL'}")
    res["KK0"] = dict(maxd=dmx, passed=dmx <= 1e-6)

    if MUTATE:
        rel = 0.0
        for foot in FOOTS:
            for k in [k for k in TAB if k.startswith(foot + "|") and not k.endswith(("|x", "|re_Mpc", "|sc"))]:
                v = k.split("|", 1)[1]
                ref = T29[f"{foot}|dir|census|{v}"][GG]; new = TAB[k][GG]
                rel = max(rel, float(np.nanmax(np.abs(new - ref) / (np.abs(ref) + 1e-30 + 1e-6 * np.nanmax(np.abs(ref))))))
        P(f"MU1/KK1 s_c = 1 through this path vs CFG529 census tables, 20 random f30 groups: max rel {rel:.1e} (<= 1e-6) -> {'BITES' if rel <= 1e-6 else 'FAILS'}")
        res["MU1_KK1"] = dict(max_rel=rel, bites=rel <= 1e-6, groups=GG.tolist())
        json.dump(res, open(os.path.join(HERE, f"cfg557_kids_results{SUF}.json"), "w"), indent=1, default=float)
        open(os.path.join(HERE, f"cfg557_kids{SUF}.out"), "w").write("\n".join(OUT) + "\n")
        sys.exit(1 if rel <= 1e-6 else 0)

    # ---------------------------------------------------------- scores with the derived edge
    P("\nRe-score on f30 (measured f30 leakage), derived edge vs census edge; PASS iff p > 0.01 in both constructions")
    res["scores"] = {}
    for foot in FOOTS:
        x = TAB[f"{foot}|x"][GSEL]; xc = T29[f"{foot}|dir|census|x"][GSEL]
        P(f"  [{foot}] derived x_edge = r_e/r_ta median {np.median(x):.3f} (min {np.nanmin(x):.3f}, max {np.nanmax(x):.3f}); census median {np.median(xc):.3f}")
        rows = {}
        for c in CONS:
            o = score(EC30[c], TAB, f"{foot}|")
            ref = J529["rescore_f30"][c][foot]
            o["Delta_vs_best_node"] = o["chi2"] - ref["edge_ref"]["chi2_best"]
            o["census_chi2"] = ref["rows"]["CENSUS"]["chi2"]; o["census_p"] = ref["rows"]["CENSUS"]["p"]
            o["best_node_x"] = ref["edge_ref"]["best_x"]; o["node_chi2"] = ref["edge_ref"]["node_chi2"]
            rows[c] = {k: v for k, v in o.items() if k not in ("model", "model_behroozi")}
            P(f"    construction {c}: chi2 {o['chi2']:.2f} (p {o['p']:.1e}) [census {o['census_chi2']:.2f}, p {o['census_p']:.1e}]; inner9 {o['chi2_inner9']:.2f}, outer6 {o['chi2_outer6']:.2f}; "
              f"Delta vs best node (x {o['best_node_x']:.2f}) {o['Delta_vs_best_node']:+.2f}")
        passed = all(rows[c]["p"] > 0.01 for c in CONS)
        res["scores"][foot] = dict(rows=rows, x_median=float(np.median(x)), x_min=float(np.nanmin(x)), x_max=float(np.nanmax(x)),
                                   x_census_median=float(np.median(xc)), passed=bool(passed))
        P(f"    -> {'PASS' if passed else 'FAIL'} (CFG529 absolute rule)")

    # ---------------------------------------------------------- inner bins / early-late: derived edge radius per f30 lens
    P("\nInner bins (K-in 52-98 kpc) and early / late types: derived edge radius per f30 lens (its group's edge)")
    lens = NS["lens"]; typ = lens["typ"].astype(int); gil = NS["GP"].gi
    F30 = NS["F30"]
    res["inner"] = {}
    for foot in FOOTS:
        rk = TAB[f"{foot}|re_Mpc"][gil[F30]] * 1000.0
        rk0 = (T29[f"{foot}|dir|census|x"] * T29[f"{foot}|rta"])[gil[F30]] * 1000.0
        tt = typ[F30]
        out = {}
        for nm, m in (("all", np.ones(len(tt), bool)), ("early", tt == 1), ("late", tt != 1)):
            v = rk[m]
            out[nm] = dict(N=int(m.sum()), min_kpc=float(np.nanmin(v)), p01_kpc=float(np.nanpercentile(v, 1)), median_kpc=float(np.nanmedian(v)),
                           frac_inside_98=float(np.mean(v < 98.0)), census_min_kpc=float(np.nanmin(rk0[m])), census_median_kpc=float(np.nanmedian(rk0[m])))
        unchanged = out["all"]["frac_inside_98"] == 0.0
        out["K_in_unchanged_by_construction"] = bool(unchanged)
        res["inner"][foot] = out
        P(f"  [{foot}] edge kpc: all min {out['all']['min_kpc']:.0f}, 1% {out['all']['p01_kpc']:.0f}, median {out['all']['median_kpc']:.0f} (census min {out['all']['census_min_kpc']:.0f}, median {out['all']['census_median_kpc']:.0f}); "
          f"early N {out['early']['N']} min {out['early']['min_kpc']:.0f}; late N {out['late']['N']} min {out['late']['min_kpc']:.0f}; fraction inside 98 kpc {out['all']['frac_inside_98']:.4f} "
          f"-> {'K-in own profile UNCHANGED BY CONSTRUCTION (CFG531 eps and early-type split carry over)' if unchanged else 'K-in affected'}")
    P(f"\nelapsed {time.time() - T0:.0f} s")
    json.dump(res, open(os.path.join(HERE, f"cfg557_kids_results{SUF}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"cfg557_kids{SUF}.out"), "w").write("\n".join(OUT) + "\n")
