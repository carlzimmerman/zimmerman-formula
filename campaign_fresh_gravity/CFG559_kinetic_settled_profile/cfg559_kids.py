#!/usr/bin/env python3
"""CFG559 task 2 (ii) (FROZEN_CRITERIA.md, criteria commit 8485002fc): KiDS f30 with the kinetic settled profile.
Machinery: CFG529's cfg529_score.py exec'd read-only up to its controls block and cfg529_tables.py imported read-only; CFG557's edge
(edge_new with s_c* at the group's census M_ta and lens z) copied.  ONE change in the variants path: the intrinsic cumulative phantom on
the extended grid Md(r) -> Md(r) + Md(r_out) Delta m(r / r_out), and construction A evaluated on the extended grid (the tail lies beyond r_out).
Tables cached outside git: ../../../_external_data/cfg559_work/
  nice -n 10 python3 cfg559_kids.py               -> cfg559_kids.out, cfg559_kids_results.json (primary + full-supply variant)
  CFG559_MUTATE=1 nice -n 10 python3 cfg559_kids.py -> *_MUTATE.* (MK0: CFG557 cached tables re-scored = CFG557 chi2; kinetic path with
                                                     Delta m = 0 vs the source path (reported); MK2: sigma x 2 tables)
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
D557 = os.path.join(LANES, "CFG557_settling_catchment_derived")
sys.path.insert(0, HERE); sys.path.insert(0, D557)
MUTATE = os.environ.get("CFG559_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg559_work"))
W557 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg557_work"))
os.makedirs(WORK, exist_ok=True)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
try:
    os.nice(10)
except OSError:
    pass

import cfg557_lib as LIB
import cfg559_lib as K9
JD = json.load(open(os.path.join(D557, "cfg557_derive_results.json")))
J557K = json.load(open(os.path.join(D557, "cfg557_kids_results.json")))
assert JD["verdict"]["tested"] == "ff"

sys.path.insert(0, os.path.join(LANES, "CFG529_f30_matched_environment"))
with contextlib.redirect_stdout(io.StringIO()):
    import cfg529_tables as TB                                               # noqa: E402
Lc, Cc, O = TB.L, TB.C, TB.O
GSEL = TB.GSEL

def edge_new(Mg, a0, f, sc):
    """CFG557's edge_new, copied."""
    re0 = Lc.r_edge_pm(Mg, Cc.G_MPC, a0, f)
    return re0 * Lc.ln_fac(f) / math.log1p(f * Lc.FB / ((1.0 - Lc.FB) * sc))

def variants_kin(Mg, zl, a0, rout, rext, W, RTL, XTW, dmf):
    """cfg529_tables.variants with the ONE change (Md + Md(r_out) Delta m(r / r_out); A on the extended grid)."""
    r0, Md0, r, Md = O.kids_Md_ext(Mg, zl, a0, rout, max(rext, 6 * rout), intrinsic=True)
    Mk = Md + Md0[-1] * dmf(r / rout)
    out = {"full": O.kids_fin(Mg, r, Mk)}
    for s in TB.SHMRS:
        for k in ("W10", "W30"):
            out[f"tr_{s}_{k}"] = O.kids_fin(Mg, r, O.truncate(r, Mk, W[f"{s}_{k}"]))
        xt = XTW[s]["prim"]
        out[f"prim_full_{s}"] = O.kids_fin(Mg, r, O.window(r, Mk, RTL[s], xt))
        out[f"prim_tr_{s}_W30"] = O.kids_fin(Mg, r, O.window(r, O.truncate(r, Mk, W[f"{s}_W30"]), RTL[s], xt))
    return out

def work(args):
    g, scs, jobs = args                    # scs: {foot|variant: s_c}; jobs: list of (tag, variant, kind)
    Mg, zl, lms = TB.GM[g], TB.GZ[g], TB.GS[g]
    W, RTL, XTW = TB.setup(Mg, zl, lms)
    f, lMta = Lc.fret_census(Mg)
    out = {}
    for foot in TB.FOOTS:
        a0 = Cc.A0[foot]
        rta = Cc.r_ta_law(Mg, a0, zl)
        rext = max(max(8 * XTW[s][w] * RTL[s] for s in TB.SHMRS for w in TB.O.WINS), 6 * rta)
        for tag, variant, kind in jobs:
            sc = scs[f"{foot}|{variant}"]
            re = edge_new(Mg, a0, f, sc); rout = min(re, rta)
            dmf = K9.DM(lMta, foot, variant, kind)
            x99 = (min(dmf.r99() * rout, rta) / rta) if kind != "sharp" else rout / rta
            out[f"{tag}|{foot}|x"] = re / rta; out[f"{tag}|{foot}|x99"] = x99; out[f"{tag}|{foot}|re_Mpc"] = re
            for v, arr in variants_kin(Mg, zl, a0, rout, rext, W, RTL, XTW, dmf).items():
                out[f"{tag}|{foot}|{v}"] = arr
            if tag == "SHARPPATH":                                    # the source path, for the reported comparison
                for v, arr in TB.variants(Mg, zl, a0, rout, rext, W, RTL, XTW).items():
                    out[f"SRC|{foot}|{v}"] = arr
    return g, out

if __name__ == "__main__":
    P(f"CFG559 KiDS {'(MUTATE)' if MUTATE else ''} -- FROZEN_CRITERIA.md (8485002fc). kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
    ZN = np.round(np.arange(0.10, 0.501, 0.05), 3)
    EP = {z: LIB.Epoch(float(z)) for z in ZN}
    SC = {}
    for g in GSEL:
        Mg, zl = float(TB.GM[g]), float(TB.GZ[g])
        f, lMta = Lc.fret_census(Mg)
        Mta_h = 10 ** lMta; Mb_h = Mg * Lc.H16
        j = int(np.clip(np.searchsorted(ZN, zl) - 1, 0, len(ZN) - 2)); w = (zl - ZN[j]) / (ZN[j + 1] - ZN[j])
        row = {}
        for foot in TB.FOOTS:
            s0 = LIB.s_catch(EP[ZN[j]], Mta_h, Mb_h, foot, math.inf); s1 = LIB.s_catch(EP[ZN[j + 1]], Mta_h, Mb_h, foot, math.inf)
            row[f"{foot}|primary"] = (1 - w) * s0 + w * s1; row[f"{foot}|full"] = 1.0
        SC[g] = row
    P(f"  s_c* for {len(GSEL)} f30 groups ({time.time() - T0:.0f} s)")
    if MUTATE:
        rng = np.random.default_rng(559)
        G20 = set(np.sort(rng.choice(GSEL, 20, replace=False)).tolist())
        tasks = [(g, SC[g], [("KIN2", "primary", "kin2")] + ([("SHARPPATH", "primary", "sharp")] if g in G20 else [])) for g in GSEL]
    else:
        tasks = [(g, SC[g], [("KIN", "primary", "kin"), ("KINFULL", "full", "kin")]) for g in GSEL]
    with MP.get_context("fork").Pool(4) as pool:
        resl = pool.map(work, tasks, chunksize=4)
    P(f"  tables built for {len(resl)} groups ({time.time() - T0:.0f} s)")
    keys = set().union(*[o.keys() for _, o in resl])
    TAB = {}
    for k in keys:
        ex = next(np.asarray(o[k]) for _, o in resl if k in o)
        arr = np.full((TB.NG,) + ex.shape, np.nan)
        for g, o in resl:
            if k in o:
                arr[g] = o[k]
        TAB[k] = arr
    np.savez_compressed(os.path.join(WORK, f"cfg559_kids_tables{SUF}.npz"), **TAB)

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

    res = dict(lane="CFG559", script="cfg559_kids", date="2026-10-10", mutate=MUTATE, criteria_commit="8485002fc",
               settings="kappa = 1/2 FITTED; footings never pooled; nu_mono; cold energy mass required; not theory closed")
    dmx = 0.0
    for c in CONS:
        for foot in FOOTS:
            dmx = max(dmx, abs(score(EC30[c], T29, f"{foot}|dir|census|")["chi2"] - J529["rescore_f30"][c][foot]["rows"]["CENSUS"]["chi2"]))
    P(f"\nKK0 scorer reproduces CFG529's stored census chi2: max |d| {dmx:.1e} -> {'PASS' if dmx <= 1e-6 else 'FAIL'}")
    res["KK0"] = dict(maxd=dmx, passed=dmx <= 1e-6)

    def block(tag, foot):
        rows = {}
        for c in CONS:
            o = score(EC30[c], TAB, f"{tag}|{foot}|")
            ref = J529["rescore_f30"][c][foot]
            o["Delta_vs_best_node"] = o["chi2"] - ref["edge_ref"]["chi2_best"]; o["best_node_x"] = ref["edge_ref"]["best_x"]
            s7 = J557K["scores"][foot]["rows"][c]
            o["sharp_chi2"] = s7["chi2"]; o["sharp_p"] = s7["p"]; o["sharp_inner9"] = s7["chi2_inner9"]; o["sharp_outer6"] = s7["chi2_outer6"]
            rows[c] = {k: v for k, v in o.items() if k not in ("model", "model_behroozi")}
        x99 = TAB[f"{tag}|{foot}|x99"][GSEL]; x = TAB[f"{tag}|{foot}|x"][GSEL]
        return dict(rows=rows, x_median=float(np.nanmedian(x)), x99_median=float(np.nanmedian(x99)), x99_min=float(np.nanmin(x99)), x99_max=float(np.nanmax(x99)),
                    passed=bool(all(rows[c]["p"] > 0.01 for c in CONS)))

    if MUTATE:
        T7 = dict(np.load(os.path.join(W557, "cfg557_kids_tables.npz")))
        mk0 = 0.0
        for foot in FOOTS:
            for c in CONS:
                mk0 = max(mk0, abs(score(EC30[c], T7, f"{foot}|")["chi2"] - J557K["scores"][foot]["rows"][c]["chi2"]))
        P(f"MK0 sigma = 0: CFG557's cached tables through this scorer vs CFG557's stored chi2 (A, B, both footings): max |d| {mk0:.1e} -> {'BITES' if mk0 <= 1e-6 else 'FAILS'}")
        rel = 0.0
        G20l = sorted(G20)
        for foot in FOOTS:
            for v in [k.split("|", 2)[2] for k in TAB if k.startswith(f"SRC|{foot}|")]:
                a = TAB[f"SHARPPATH|{foot}|{v}"][G20l]; b = TAB[f"SRC|{foot}|{v}"][G20l]
                rel = max(rel, float(np.nanmax(np.abs(a - b) / (np.abs(b) + 1e-6 * np.nanmax(np.abs(b))))))
        P(f"  reported: kinetic code path with Delta m = 0 vs the source path, 20 random groups: max rel table difference {rel:.1e}")
        J1 = json.load(open(os.path.join(HERE, "cfg559_kids_results.json")))
        res["MK0"] = dict(maxd_chi2=mk0, bites=mk0 <= 1e-6, kinetic_path_dm0_vs_source_max_rel=rel)
        res["MK2"] = {}
        ok = True
        for foot in FOOTS:
            b = block("KIN2", foot); b1 = J1["scores"][foot]["PRIMARY_kin"]
            larger = b["x99_median"] > b1["x99_median"]; ok = ok and larger
            b["x99_median_sigma1"] = b1["x99_median"]; b["x99_larger"] = bool(larger)
            res["MK2"][foot] = b
            P(f"  [{foot}] MK2 sigma x 2: median x_99 {b['x99_median']:.3f} (sigma x1 {b1['x99_median']:.3f}) -> larger: {larger};  "
              + "; ".join(f"{c}: chi2 {b['rows'][c]['chi2']:.2f} (p {b['rows'][c]['p']:.1e}) inner9 {b['rows'][c]['chi2_inner9']:.2f} outer6 {b['rows'][c]['chi2_outer6']:.2f} "
                          f"(sigma x1 {b1['rows'][c]['chi2']:.2f})" for c in CONS))
        res["all_teeth_bite_kids"] = bool(mk0 <= 1e-6 and ok)
        P(f"MUTATE (KiDS part): MK0 bites and MK2 spreads the edge on both footings -> {res['all_teeth_bite_kids']}")
        json.dump(res, open(os.path.join(HERE, f"cfg559_kids_results{SUF}.json"), "w"), indent=1, default=float)
        open(os.path.join(HERE, f"cfg559_kids{SUF}.out"), "w").write("\n".join(OUT) + "\n")
        sys.exit(1 if res["all_teeth_bite_kids"] else 0)

    P("\nRe-score on f30 (measured leakage) with the kinetic settled profile; PASS iff p > 0.01 in A and B")
    res["scores"] = {}
    for foot in FOOTS:
        res["scores"][foot] = {}
        for tag, nm in (("KIN", "PRIMARY_kin"), ("KINFULL", "VARIANT_full_kin")):
            b = block(tag, foot); res["scores"][foot][nm] = b
            P(f"  [{foot}] {nm}: edge x median {b['x_median']:.3f}, kinetic x_99 median {b['x99_median']:.3f} ({b['x99_min']:.3f}-{b['x99_max']:.3f}) "
              f"-> {('PASS' if b['passed'] else 'FAIL') if nm.startswith('PRIMARY') else '(variant, reported)'}")
            for c in CONS:
                o = b["rows"][c]
                P(f"      {c}: chi2 {o['chi2']:.2f} (p {o['p']:.1e}) [sharp {o['sharp_chi2']:.2f}]; inner9 {o['chi2_inner9']:.2f} [sharp {o['sharp_inner9']:.2f}], "
                  f"outer6 {o['chi2_outer6']:.2f} [sharp {o['sharp_outer6']:.2f}]; Delta vs best node (x {o['best_node_x']:.2f}) {o['Delta_vs_best_node']:+.2f}")
        res["scores"][foot]["passed"] = res["scores"][foot]["PRIMARY_kin"]["passed"]
    P(f"\nelapsed {time.time() - T0:.0f} s")
    json.dump(res, open(os.path.join(HERE, f"cfg559_kids_results{SUF}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"cfg559_kids{SUF}.out"), "w").write("\n".join(OUT) + "\n")
