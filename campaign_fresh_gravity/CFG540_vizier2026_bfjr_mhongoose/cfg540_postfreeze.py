#!/usr/bin/env python3
"""CFG540 POST-FREEZE diagnostics (2026-10-09; no verdict weight; written after the primary results were seen).
1. Groups: why the census edge moves them +0.14/+0.15 dex. Census f_ret per group, r_edge/Re, Delta(edge) vs f_ret and log Mb;
   the same statistic with the CFG515 brackets f_ret = 0.07 / 0.18 (constant) and with no edge.
2. Groups: if Mbar omits hot intragroup gas, how much extra baryonic mass would null the no-edge / edge residual (deep MOND
   sigma^4 ~ M: Delta_M = 4 Delta) -- arithmetic only.
3. Ellipticals: the uniform-mass offset expressed as a baryonic mass-scale shift (Delta / s), and Delta vs catalogue g_bar
   inside the class.
4. Dwarfs: which objects the edge moves.
5. Groups, edge-placement check: the primary uses CFG515's POINT-MASS r_edge. Group baryons are extended (a >> r_M), so their
   phantom grows more slowly and the supply cap M_cold = 5.364 M_b / f_ret is reached farther out. Variant "cap": freeze the
   phantom where its own enclosed mass reaches the supply cap (R2 read literally). Census f_ret.
"""
import os, math, json
import numpy as np
import cfg540_bfjr as C

HERE = C.HERE
OUT = []


def log(s=""):
    print(s); OUT.append(s)


def pred_const_f(o, a0, f):
    kind = "hern"
    M = 10 ** o["lM"] * C.MSUN; a = o["Re"] * C.KPC / C.HERN_RE; GM = C.G * M; a0d = a0 * a * a / GM
    xedge = None if f is None else (1.0 / math.sqrt(a0d)) / C.ln_fac(f)
    return 0.5 * math.log10(C.sigma2(kind, a0d, 0.0, None, xedge) * GM / a) - 3.0


def pred_cap(o, a0):
    M = 10 ** o["lM"] * C.MSUN; a = o["Re"] * C.KPC / C.HERN_RE; GM = C.G * M; a0d = a0 * a * a / GM
    f = C.fret_census(10 ** o["lM"])[0]
    rho, m = C.prof("hern", C.X)
    gN = m / C.X ** 2; g = C.nu(gN / a0d) * gN
    mph = (g - gN) * C.X ** 2
    from cfg515_lib import COLD_PER_B
    cap = COLD_PER_B / f
    k = np.where(mph >= cap)[0]
    xe = None if len(k) == 0 else float(C.X[k[0]])
    xpm = (1.0 / math.sqrt(a0d)) / C.ln_fac(f)
    return 0.5 * math.log10(C.sigma2("hern", a0d, 0.0, None, xe) * GM / a) - 3.0, (xe if xe else np.inf) / xpm


def main():
    rows = C.read_tian()
    prim = json.load(open(os.path.join(HERE, "cfg540_bfjr_results.json")))
    res = {}
    log("CFG540 POST-FREEZE diagnostics (no verdict weight)")
    gi = [i for i, o in enumerate(rows) if o["sample"] == "Galaxy group"]
    for fk, a0 in C.FOOT.items():
        r = {}
        D_edge = np.array(prim["footings"][fk]["runs"]["beta+0.0"]["Delta"])[gi]
        D_no = np.array(prim["footings"][fk]["runs"]["beta+0.0_noedge"]["Delta"])[gi]
        fr = np.array([C.fret_census(10 ** rows[i]["lM"])[0] for i in gi])
        lM = np.array([rows[i]["lM"] for i in gi]); Re = np.array([rows[i]["Re"] for i in gi])
        rM = np.sqrt(C.G * 10 ** lM * C.MSUN / a0) / C.KPC
        xe = rM / np.array([C.ln_fac(f) for f in fr])
        log(f"\n=== {fk} ===  groups N {len(gi)}: census f_ret median {np.median(fr):.3f} (range {fr.min():.3f}-{fr.max():.3f}); "
            f"r_M median {np.median(rM):.0f} kpc; r_edge/Re median {np.median(xe / Re):.2f} (range {np.min(xe / Re):.2f}-{np.max(xe / Re):.2f})")
        ls = np.array([rows[i]["ls"] for i in gi])
        for nm, f in (("f07", 0.07), ("f18", 0.18), ("f100", 1.0)):
            lp = np.array([pred_const_f(rows[i], a0, f) for i in gi])
            d = ls - lp
            r[nm] = dict(mean=float(d.mean()), se=float(d.std(ddof=1) / math.sqrt(len(d))))
            log(f"  constant f_ret {f:.2f}: groups mean Delta {d.mean():+.3f} +- {r[nm]['se']:.3f}")
        log(f"  census edge: {D_edge.mean():+.3f}; no edge: {D_no.mean():+.3f}")
        for lo, hi in ((0, 0.12), (0.12, 0.4), (0.4, 1.0)):
            k = (fr >= lo) & (fr < hi)
            if k.sum():
                log(f"  f_ret [{lo:.2f},{hi:.2f}) N {k.sum():2d}: Delta edge {D_edge[k].mean():+.3f}, no edge {D_no[k].mean():+.3f}, "
                    f"r_edge/Re median {np.median((xe / Re)[k]):.2f}")
        sl_e = float(np.polyfit(lM, D_edge, 1)[0]); sl_n = float(np.polyfit(lM, D_no, 1)[0])
        log(f"  dDelta/dlogMb: edge {sl_e:+.3f}, no edge {sl_n:+.3f}")
        log(f"  extra baryons to null (deep MOND, Delta_M = 4 Delta): no edge {4 * D_no.mean():+.2f} dex; with census edge, more than "
            f"{4 * D_edge.mean():+.2f} dex (edge also moves out as M grows)")
        cp = [pred_cap(rows[i], a0) for i in gi]
        dcap = ls - np.array([c[0] for c in cp]); ratio = np.array([c[1] for c in cp])
        r["cap_variant"] = dict(mean=float(dcap.mean()), se=float(dcap.std(ddof=1) / math.sqrt(len(dcap))),
                                edge_ratio_cap_over_pointmass_median=float(np.median(ratio)))
        log(f"  supply-cap edge variant (phantom frozen where it reaches 5.364 M_b/f_ret): groups mean Delta {dcap.mean():+.3f} +- "
            f"{r['cap_variant']['se']:.3f}; cap edge / point-mass edge median {np.median(ratio):.2f}")
        r.update(fret_median=float(np.median(fr)), fret_min=float(fr.min()), fret_max=float(fr.max()),
                 redge_over_Re_median=float(np.median(xe / Re)), census=float(D_edge.mean()), noedge=float(D_no.mean()),
                 slope_lM_edge=sl_e, slope_lM_noedge=sl_n)
        # ellipticals
        ei = [i for i, o in enumerate(rows) if C.CLASS[o["sample"]] == "ELLIPTICALS"]
        De = np.array(prim["footings"][fk]["runs"]["beta+0.0"]["Delta"])[ei]
        st = prim["footings"][fk]["runs"]["beta+0.0"]["classes"]["ELLIPTICALS"]
        sbar = st["sys"] / 0.10
        xg = np.array([rows[i]["lg"] for i in ei]) - math.log10(a0)
        sg = float(np.polyfit(xg, De, 1)[0])
        log(f"  ELLIPTICALS: mean Delta {st['mean']:+.3f} with s_bar {sbar:.3f} -> baryonic mass-scale shift to null {st['mean'] / sbar:+.2f} dex "
            f"(Chabrier->Salpeter is about +0.25 dex); dDelta/dlog(gbar/a0) inside class {sg:+.3f}")
        r.update(ell_mass_shift_to_null=float(st["mean"] / sbar), ell_s_bar=float(sbar), ell_slope_vs_gbar=sg)
        # dwarfs moved by edge
        di = [i for i, o in enumerate(rows) if C.CLASS[o["sample"]] == "DWARFS"]
        Dd = np.array(prim["footings"][fk]["runs"]["beta+0.0"]["Delta"]); Dn = np.array(prim["footings"][fk]["runs"]["beta+0.0_noedge"]["Delta"])
        mv = [(rows[i]["id"], rows[i]["sample"], float(Dd[i] - Dn[i])) for i in di if abs(Dd[i] - Dn[i]) >= 0.005]
        log(f"  dwarfs moved >= 0.005 dex by the edge: {len(mv)} " + ", ".join(f"{a} ({b}) {c:+.3f}" for a, b, c in mv))
        r["dwarfs_moved_by_edge"] = mv
        res[fk] = r
    json.dump(res, open(os.path.join(HERE, "cfg540_postfreeze_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg540_postfreeze.out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
