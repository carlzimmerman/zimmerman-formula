"""RB1R blind re-grade: form B retained fraction f_ret in the X-COP clusters.

Usage (from anywhere):
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 19 python3 -I -B rb1r.py

Reads real_research/data/xcop/ relative to the repository root (found from this file's location).
Writes rb1r.out, rb1r.json, rb1r_MUTATE.out, rb1r_MUTATE.json next to this file.

f_ret(<r) = R M_b(<r) / [M_dyn(<r) - M_b(<r)], +inf if M_dyn <= M_b. Class statistic: median over systems with a 95 %
interval from 10,000 bootstrap resamples. Lines: ceiling (lower end > 1 fails), floor (upper end < 0.85 fails).
"""
import io
import json
import os
import sys

import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "real_research", "data", "xcop")

R_MAIN = 5.41
R_BRACKET = 5.562
FOOTINGS = {"canonical": {"a0": 9.3603e-11, "h": 0.65}, "alt": {"a0": 1.1312e-10, "h": 0.65}}
H_DATA = 0.7
N_BOOT = 10000
N_DRAW = 4000
SEED_BOOT = 20261114
SEED_DRAW = 20261115
SEED_PLANT = 20261116
CEIL = 1.0
FLOOR = 0.85
BIG = 1e30  # stand-in for +inf inside percentile arithmetic
OTHER_MASSES = ["M_NFW", "M_EIN", "M_ISO", "M_BUR"]

OUT = io.StringIO()


def p(*a):
    s = " ".join(str(x) for x in a)
    OUT.write(s + "\n")
    print(s)


# ---------------------------------------------------------------- core functions

def f_ret(mdyn, mb, R):
    mdyn = np.asarray(mdyn, float)
    mb = np.asarray(mb, float)
    mdyn, mb = np.broadcast_arrays(np.atleast_1d(mdyn), np.atleast_1d(mb))
    out = np.full(mdyn.shape, np.inf)
    ok = mdyn > mb
    out[ok] = R * mb[ok] / (mdyn[ok] - mb[ok])
    return out


def interp_loglog(rt, mt, r):
    """log-log linear interpolation inside the table span only; nan outside."""
    rt = np.asarray(rt, float)
    mt = np.asarray(mt, float)
    ok = np.isfinite(rt) & np.isfinite(mt) & (rt > 0) & (mt > 0)
    rt, mt = rt[ok], mt[ok]
    o = np.argsort(rt)
    rt, mt = rt[o], mt[o]
    r = np.atleast_1d(np.asarray(r, float))
    out = np.full(r.shape, np.nan)
    inside = (r >= rt[0]) & (r <= rt[-1]) & (r > 0)
    out[inside] = np.exp(np.interp(np.log(r[inside]), np.log(rt), np.log(mt)))
    return out


def interp_loglin(rt, yt, r):
    """y linear in log r, inside the table span only (used for fractional errors)."""
    rt = np.asarray(rt, float)
    yt = np.asarray(yt, float)
    ok = np.isfinite(rt) & np.isfinite(yt) & (rt > 0)
    rt, yt = rt[ok], yt[ok]
    o = np.argsort(rt)
    rt, yt = rt[o], yt[o]
    r = np.atleast_1d(np.asarray(r, float))
    out = np.full(r.shape, np.nan)
    inside = (r >= rt[0]) & (r <= rt[-1]) & (r > 0)
    out[inside] = np.interp(np.log(r[inside]), np.log(rt), yt)
    return out


def class_stat(fr, seed=SEED_BOOT):
    fr = np.asarray(fr, float)
    n = len(fr)
    if n == 0:
        return {"n": 0, "median": None, "lo": None, "hi": None}
    v = np.where(np.isfinite(fr), fr, BIG)
    med = float(np.median(v))
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(N_BOOT, n))
    meds = np.median(v[idx], axis=1)
    lo, hi = np.percentile(meds, [2.5, 97.5])
    fix = lambda x: float("inf") if x >= BIG / 10 else float(x)
    return {"n": n, "median": fix(med), "lo": fix(lo), "hi": fix(hi)}


def word(st):
    if st["n"] < 5:
        return "NOT EVALUABLE"
    if st["lo"] > CEIL:
        return "AMOUNT BREAKS THE CEILING"
    if st["hi"] < FLOOR:
        return "AMOUNT BELOW THE FLOOR"
    return "AMOUNT CONSISTENT ON BOTH SIDES"


def per_system_errors(mdyn, sd, mg, sg, ms, ss, R, rng):
    """lognormal draws; returns half 16-84 width and 2.275th percentile of f_ret."""
    dd = mdyn * np.exp(sd * rng.standard_normal(N_DRAW))
    gg = mg * np.exp(sg * rng.standard_normal(N_DRAW))
    s_ = ms * np.exp(ss * rng.standard_normal(N_DRAW)) if ms > 0 else np.zeros(N_DRAW)
    fr = f_ret(dd, gg + s_, R)
    v = np.where(np.isfinite(fr), fr, BIG)
    p16, p84, p2 = np.percentile(v, [16, 84, 2.275])
    return 0.5 * (min(p84, BIG) - p16), float(p2)


# ---------------------------------------------------------------- data

def load():
    names = sorted(d for d in os.listdir(DATA) if os.path.isdir(os.path.join(DATA, d)))
    cl = {}
    units = {}
    for n in names:
        d = os.path.join(DATA, n)
        with fits.open(os.path.join(d, f"{n}_hydro_mass.fits")) as h:
            t = h[1].data
            hdr = h[1].header
            c = {"name": n, "R500_hdr": float(hdr["R500"]), "z": float(hdr["REDSHIFT"]),
                 "h_r": np.array(t["RADIUS"], float)}
            for col in ["M_FORW", "EM_FORW"] + OTHER_MASSES + ["E" + m for m in OTHER_MASSES]:
                c["h_" + col] = np.array(t[col], float)
            units["hydro"] = dict(zip(h[1].columns.names, h[1].columns.units))
            c["hydro_cols"] = list(h[1].columns.names)
        with fits.open(os.path.join(d, f"{n}_fgas_profile.fits")) as g:
            t = g[1].data
            assert abs(float(g[1].header["R500"]) - c["R500_hdr"]) < 1e-6
            c["g_x"] = np.array(t["RADIUS"], float)
            c["g_r"] = c["g_x"] * c["R500_hdr"]
            c["g_m"] = np.array(t["MGAS"], float)
            lo = np.array(t["MGAS_LO"], float)
            hi = np.array(t["MGAS_HI"], float)
            # LO/HI found to be offsets (both much smaller than MGAS); check per row
            c["gas_lohi_are_offsets"] = bool(np.all(hi < c["g_m"]))  # a bound HI would exceed MGAS
            if c["gas_lohi_are_offsets"]:
                c["g_sf"] = 0.5 * (lo + hi) / c["g_m"]
            else:  # bounds
                c["g_sf"] = 0.5 * (hi - lo) / c["g_m"]
            units["gas"] = dict(zip(g[1].columns.names, g[1].columns.units))
        sp = os.path.join(d, f"{n}_mstar.fits")
        c["has_star"] = os.path.exists(sp)
        if c["has_star"]:
            with fits.open(sp) as s:
                t = s[2].data
                c["s_r"] = np.array(t["RADIUS"], float)
                c["s_m"] = np.array(t["MSTAR"], float)
                lo = np.array(t["MSTAR_LO"], float)
                hi = np.array(t["MSTAR_HI"], float)
                bounds = np.all((lo <= c["s_m"]) & (hi >= c["s_m"]))
                c["star_lohi_are_bounds"] = bool(bounds)
                c["s_sf"] = np.where(c["s_m"] > 0, 0.5 * (hi - lo) / np.where(c["s_m"] > 0, c["s_m"], 1), np.nan) if bounds \
                    else 0.5 * (lo + hi) / c["s_m"]
                units["star_ext2"] = dict(zip(s[2].columns.names, s[2].columns.units))
        cl[n] = c
    with open(os.path.join(DATA, "xcop_r500_ettori2019.json")) as f:
        ett = json.load(f)
    return names, cl, units, ett


def profile(c, mkey="M_FORW", q=None):
    """Masses on the kept gas-grid radii. q: (x_grid, ratio) for imputed stars."""
    r = c["g_r"]
    md = interp_loglog(c["h_r"], c["h_" + mkey], r)
    frac_d = c["h_E" + mkey] / c["h_" + mkey]
    sd = interp_loglin(c["h_r"], frac_d, r)
    mg = c["g_m"].copy()
    sg = c["g_sf"].copy()
    if c["has_star"] and q is None:
        ms = interp_loglog(c["s_r"], c["s_m"], r)
        ss = interp_loglin(c["s_r"], c["s_sf"], r)
    elif q is not None:
        ratio = interp_loglog(q[0], q[1], c["g_x"])
        ms = ratio * mg
        ss = np.full(r.shape, q[2])
    else:
        ms = np.full(r.shape, np.nan)
        ss = ms
    keep = np.isfinite(md) & np.isfinite(mg) & np.isfinite(ms) & (mg > 0) & (md > 0) & np.isfinite(sd) & np.isfinite(sg) & np.isfinite(ss)
    return {"r": r[keep], "x": c["g_x"][keep], "md": md[keep], "sd": sd[keep], "mg": mg[keep], "sg": sg[keep],
            "ms": ms[keep], "ss": ss[keep]}


def at_radius(c, rr, mkey="M_FORW"):
    """All three masses interpolated at one radius rr (kpc); None if any cannot be."""
    md = interp_loglog(c["h_r"], c["h_" + mkey], rr)[0]
    sd = interp_loglin(c["h_r"], c["h_E" + mkey] / c["h_" + mkey], rr)[0]
    mg = interp_loglog(c["g_r"], c["g_m"], rr)[0]
    sg = interp_loglin(c["g_r"], c["g_sf"], rr)[0]
    if not c["has_star"]:
        return None
    ms = interp_loglog(c["s_r"], c["s_m"], rr)[0]
    ss = interp_loglin(c["s_r"], c["s_sf"], rr)[0]
    v = [md, sd, mg, sg, ms, ss]
    if not all(np.isfinite(v)):
        return None
    return {"r": rr, "x": rr / c["R500_hdr"], "md": md, "sd": sd, "mg": mg, "sg": sg, "ms": ms, "ss": ss}


def last_point(pr):
    if len(pr["r"]) == 0:
        return None
    i = int(np.argmax(pr["r"]))
    return {k: float(v[i]) for k, v in pr.items()}


def run_class(points, R, label, gas_scale=1.0, star_scale=1.0, dyn_scale=1.0, verbose=True, seed_draw=SEED_DRAW):
    """points: list of (name, point dict). Returns stats, word, per-system rows."""
    rng = np.random.default_rng(seed_draw)
    rows = []
    frs = []
    for name, pt in points:
        md = pt["md"] * dyn_scale
        mg = pt["mg"] * gas_scale
        ms = pt["ms"] * star_scale
        fr = float(f_ret(md, mg + ms, R)[0])
        err, p2 = per_system_errors(md, pt["sd"], mg, pt["sg"], ms, pt["ss"], R, rng)
        rows.append({"name": name, "r_kpc": pt["r"], "r_R500": pt["x"], "M_dyn": md, "M_gas": mg, "M_star": ms,
                     "f_ret": fr, "f_ret_err": err, "p2275": p2, "above1_2sigma": bool(p2 > 1)})
        frs.append(fr)
    st = class_stat(frs)
    w = word(st)
    n_above = sum(r_["above1_2sigma"] for r_ in rows)
    if verbose:
        p(f"\n[{label}]  R = {R}  n = {st['n']}")
        p(f"  {'cluster':8s} {'r kpc':>8s} {'r/R500':>7s} {'M_dyn':>10s} {'M_gas':>10s} {'M_star':>10s} {'f_ret':>7s} {'err':>6s}")
        for r_ in rows:
            p(f"  {r_['name']:8s} {r_['r_kpc']:8.1f} {r_['r_R500']:7.3f} {r_['M_dyn']:10.4e} {r_['M_gas']:10.4e} "
              f"{r_['M_star']:10.4e} {r_['f_ret']:7.4f} {r_['f_ret_err']:6.3f}{'  >1 at 2 sigma' if r_['above1_2sigma'] else ''}")
        p(f"  median {st['median']:.4f}  95% [{st['lo']:.4f}, {st['hi']:.4f}]  systems above 1 at >2 sigma: {n_above}  -> {w}")
    return {"label": label, "R": R, "stats": st, "word": w, "n_above1_2sigma": n_above, "systems": rows}


# ---------------------------------------------------------------- main

def build_q(names, cl, mkey="M_FORW"):
    seven = [n for n in names if cl[n]["has_star"]]
    prs = {n: profile(cl[n], mkey) for n in seven}
    xmin = min(prs[n]["x"].min() for n in seven)
    xmax = max(prs[n]["x"].max() for n in seven)
    xg = np.exp(np.linspace(np.log(xmin), np.log(xmax), 60))
    rat = np.array([interp_loglog(prs[n]["x"], prs[n]["ms"] / prs[n]["mg"], xg) for n in seven])
    cnt = np.sum(np.isfinite(rat), axis=0)
    qx = xg[cnt >= 3]
    qv = np.array([np.nanmedian(rat[:, j]) for j in np.nonzero(cnt >= 3)[0]])
    sfr = float(np.median([last_point(prs[n])["ss"] for n in seven]))
    return (qx, qv, sfr)


def main():
    names, cl, units, ett = load()
    res = {"lane": "RB1R", "seeds": {"boot": SEED_BOOT, "draw": SEED_DRAW, "plant": SEED_PLANT}}
    p("RB1R blind re-grade: form B f_ret in X-COP clusters")
    p("Units found: hydro", units["hydro"])
    p("Units found: gas", units["gas"])
    p("Units found: star ext2", units.get("star_ext2"))
    for n in names:
        c = cl[n]
        p(f"  {n:8s} R500_hdr {c['R500_hdr']:7.1f} kpc  R500_json {1000*ett[n]['R500']:7.1f} kpc  "
          f"hydro {c['h_r'].min():.0f}-{c['h_r'].max():.0f} kpc  gas x {c['g_x'].min():.3f}-{c['g_x'].max():.3f}  "
          f"star {'%.0f-%.0f kpc' % (c['s_r'].min(), c['s_r'].max()) if c['has_star'] else 'none'}"
          f"{'  star LO/HI bounds' if c.get('star_lohi_are_bounds') else ''}")
    p("  json clusters without a folder:", sorted(set(ett) - set(names)))

    # known answers
    ka = {}
    mb = np.array([1e13, 3.7e13, 8.1e13])
    ka["KA4"] = {str(R): float(np.max(np.abs(f_ret((1 + R) * mb, mb, R) - 1))) for R in (R_MAIN, R_BRACKET)}
    ka["KA4_pass"] = all(v < 1e-12 for v in ka["KA4"].values())
    nstar = sum(cl[n]["has_star"] for n in names)
    ka["KA5"] = {"folders": len(names), "with_star": nstar, "json_entries": len(ett)}
    ka["KA5_pass"] = (len(names) == 12 and nstar == 7)
    p("\nKA-4 max |f_ret - 1|:", ka["KA4"], "pass" if ka["KA4_pass"] else "FAIL")
    p("KA-5 parser:", ka["KA5"], "pass" if ka["KA5_pass"] else "FAIL")
    res["known_answers"] = ka

    seven = [n for n in names if cl[n]["has_star"]]
    pts7 = [(n, last_point(profile(cl[n]))) for n in seven]
    res["footings"] = {}
    graded_dump = []
    for fn, fv in FOOTINGS.items():
        p(f"\n==================== footing {fn} (a0 = {fv['a0']}, h = {fv['h']}; no a0 enters this class)")
        out = {"a0": fv["a0"], "h": fv["h"]}
        out["graded"] = run_class(pts7, R_MAIN, f"{fn} GRADED C-X 7 clusters, last radius, M_FORW")
        graded_dump.append(json.dumps(out["graded"], sort_keys=True))
        br = {}
        br["R5562"] = run_class(pts7, R_BRACKET, f"{fn} bracket R = 5.562")
        # R500 from Ettori json
        pr5 = []
        dropped = []
        for n in seven:
            pt = at_radius(cl[n], 1000.0 * ett[n]["R500"])
            if pt is None:
                dropped.append(n)
            else:
                pt["x"] = pt["r"] / (1000.0 * ett[n]["R500"])
                pr5.append((n, pt))
        br["R500"] = run_class(pr5, R_MAIN, f"{fn} bracket at R500 (Ettori json), dropped {dropped}")
        # all 12 with imputed stars
        q = build_q(names, cl)
        pts12 = []
        for n in names:
            pr = profile(cl[n]) if cl[n]["has_star"] else profile(cl[n], q=q)
            pts12.append((n, last_point(pr)))
        br["all12"] = run_class(pts12, R_MAIN, f"{fn} bracket all 12 (5 imputed stars), last radius")
        br["all12"]["q_span_x"] = [float(q[0].min()), float(q[0].max())]
        br["all12"]["q_values_ends"] = [float(q[1][0]), float(q[1][-1])]
        br["all12"]["imputed_star_frac_err"] = q[2]
        # h rescale
        gs = (H_DATA / fv["h"]) ** 0.5
        br["h_spec"] = run_class(pts7, R_MAIN, f"{fn} bracket h {H_DATA}->{fv['h']} (spec: f_gas ~ h^-1/2, x{gs:.4f})",
                                 gas_scale=gs)
        br["h_extra_std"] = run_class(pts7, R_MAIN, f"{fn} EXTRA (not in spec) h {H_DATA}->{fv['h']}, gas h^-3/2, stars h^-1",
                                      gas_scale=(H_DATA / fv["h"]) ** 1.5, star_scale=(H_DATA / fv["h"]) ** 1.0)
        for b in (0.1, 0.2):
            br[f"bias_{b}"] = run_class(pts7, R_MAIN, f"{fn} bracket hydrostatic bias b = {b}", dyn_scale=1 / (1 - b))
        for mk in OTHER_MASSES:
            ptsm = [(n, last_point(profile(cl[n], mk))) for n in seven]
            ptsm = [(n, x) for n, x in ptsm if x is not None]
            br["mass_" + mk] = run_class(ptsm, R_MAIN, f"{fn} bracket mass estimate {mk}")
        out["brackets"] = br
        res["footings"][fn] = out
    ka["KA6_footings_identical"] = graded_dump[0].replace("canonical", "X") == graded_dump[1].replace("alt", "X")
    p("\nKA-6 footings identical (graded class):", ka["KA6_footings_identical"])

    # ---------------- mutations
    mut = io.StringIO()
    global OUT
    main_out = OUT
    OUT = mut
    m = {}
    p("RB1R mutations and planted classes")
    m["M1_Rx2"] = run_class(pts7, 2 * R_MAIN, "M1: R x 2 on the graded class")
    m["M1_bites"] = m["M1_Rx2"]["stats"]["lo"] > CEIL
    p("  M1 bites (lower end > 1):", m["M1_bites"])
    base = res["footings"]["canonical"]["graded"]
    m["M2_dyn_half"] = run_class(pts7, R_MAIN, "M2a: M_dyn x 0.5", dyn_scale=0.5)
    m["M2_nostars"] = run_class(pts7, R_MAIN, "M2b: stars set to zero", star_scale=0.0)
    m["M2a_raises"] = m["M2_dyn_half"]["stats"]["median"] > base["stats"]["median"]
    m["M2b_lowers"] = m["M2_nostars"]["stats"]["median"] < base["stats"]["median"]
    p("  M2a raises median:", m["M2a_raises"], "  M2b lowers median:", m["M2b_lowers"])
    rng = np.random.default_rng(SEED_PLANT)
    for tag, target, want in [("P07", 0.7, "AMOUNT BELOW THE FLOOR"), ("P13", 1.3, "AMOUNT BREAKS THE CEILING")]:
        pts = []
        for i in range(7):
            mbar = 10 ** rng.uniform(13.0, 14.0)
            f = target * np.exp(0.05 * rng.standard_normal())
            mg = 0.9 * mbar
            ms = 0.1 * mbar
            md = mbar * (1 + R_MAIN / f)
            pts.append((f"{tag}_{i}", {"r": 1000.0, "x": 1.0, "md": md, "sd": 0.05, "mg": mg, "sg": 0.03, "ms": ms, "ss": 0.2}))
        m[tag] = run_class(pts, R_MAIN, f"planted {tag} at f_ret = {target}")
        m[tag + "_reads_as_wanted"] = m[tag]["word"] == want
        p(f"  {tag} reads {m[tag]['word']}; wanted {want}: {m[tag + '_reads_as_wanted']}")
    OUT = main_out
    with open(os.path.join(HERE, "rb1r_MUTATE.out"), "w") as f:
        f.write(mut.getvalue())
    with open(os.path.join(HERE, "rb1r_MUTATE.json"), "w") as f:
        json.dump(m, f, indent=1, default=float)

    # ---------------- words per footing
    ok = ka["KA4_pass"] and ka["KA5_pass"] and ka["KA6_footings_identical"]
    p("\n==================== WORDS")
    res["words"] = {}
    for fn in FOOTINGS:
        g = res["footings"][fn]["graded"]
        w = g["word"] if (ok and m["M1_bites"]) else "NO VERDICT"
        res["words"][fn] = w
        st = g["stats"]
        p(f"  {fn}: {w}   median {st['median']:.4f} [{st['lo']:.4f}, {st['hi']:.4f}] n={st['n']}")
        for k, b in res["footings"][fn]["brackets"].items():
            s = b["stats"]
            p(f"     reported {k:14s} n={s['n']:2d} median {s['median']:.4f} [{s['lo']:.4f}, {s['hi']:.4f}] -> {b['word']}")
    res["mutations_summary"] = {k: v for k, v in m.items() if not isinstance(v, dict)}
    with open(os.path.join(HERE, "rb1r.out"), "w") as f:
        f.write(OUT.getvalue())
    with open(os.path.join(HERE, "rb1r.json"), "w") as f:
        json.dump(res, f, indent=1, default=float)


if __name__ == "__main__":
    main()
