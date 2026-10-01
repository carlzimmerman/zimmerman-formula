#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG260 MEASUREMENT: the implied a0 (CFG223's s*) of the BUDHIES HI sample at z ~ 0.2 from the HI line widths, under the frozen protocol (FROZEN_CRITERIA.md section 7 + Addenda 1 and 2).
RUN ONCE, after the pre-flight (04dbf45d4) and this script are committed.  The first run is the result; nothing is re-run to change it.  A lower-quality row (PF-D2 NOT DRAWABLE): the selection bias of the
pre-flight is one-directional (LOW), so a measured s* is a lower bound on the implied a0 within the other systematics.  kappa = 1/2 FITTED; no sentence says the data favour a law or a framework.
SELFTEST=1 fabricates widths from the NON-width inputs (isotropic inclinations at s = 1, no selection) and never reads a real width: it exists to debug this script blind.
Outputs: cfg260_measure.out, cfg260_results.json, cfg260_points.csv (chart_a0z_points.csv shape + recipe-band columns).
"""
import os, sys, json, math, time, csv
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg260_core as C

SELF = os.environ.get("SELFTEST", "").strip() == "1"
SFX = "_SELFTEST" if SELF else ""
T0 = time.time()
LOG = []


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


CK = []
RES = {}


def check(name, detail, ok, kind="control"):
    CK.append(dict(name=name, detail=detail, ok=bool(ok), kind=kind))
    P(f"  [{'PASS' if ok else 'FAIL'}] ({kind}) {name}\n         {detail}")


def jc(o):
    if isinstance(o, dict):
        return {str(k): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jc(v) for v in o]
    if isinstance(o, np.generic):
        return o.item()
    if isinstance(o, np.ndarray):
        return jc(o.tolist())
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    return o


P(__doc__.strip())
P(f"\n  mode: {'SELFTEST (fabricated widths; no real width read)' if SELF else 'MEASUREMENT (real widths)'}")
GALS = C.load_galaxies(widths=not SELF)
if SELF:
    rs = np.random.default_rng(np.random.SeedSequence([260, 999]))
    aa = C.Arr(GALS)
    _, _, Mb_, R_ = C.baryons(aa, C.REC0)
    gb_ = C.G * Mb_ * C.MSUN / R_ ** 2
    Vp_ = np.sqrt(gb_ * C.nuv(C.NU, gb_ / C.A0["canonical"]) * R_) / 1e3
    sini_ = np.sqrt(1 - rs.uniform(0, 1, aa.n) ** 2)
    Wf = 2 * Vp_ * sini_ * (1 + aa.z) + C.REC0["delta"] + rs.normal(0, 15.0, aa.n)
    for g, w in zip(GALS, Wf):
        g["w50"], g["e_w50"] = float(w), 15.0
A0C, A0A = C.A0["canonical"], C.A0["alt"]

# ================================================================================================ controls
P("\n" + "=" * 110 + "\nCONTROLS\n" + "=" * 110)
w_all = np.array([g["w50"] for g in GALS])
check("M3 CONTROL: every tabulated width is finite and positive" + (" (SELFTEST: fabricated)" if SELF else ""), f"min {w_all.min():.1f}, max {w_all.max():.1f} km/s; N = {len(w_all)}", bool(np.all(np.isfinite(w_all)) and np.all(w_all > 0)))
SETS = [("PC", "PRIMARY (Addendum 2): P with completeness ratio c >= 1.0"), ("PC075", "extra rung: P with c >= 0.75 (not in the frozen list)"), ("PC125", C.SUBSET_LABEL["PC125"]), ("PC15", C.SUBSET_LABEL["PC15"]),
        ("P", C.SUBSET_LABEL["P"]), ("S1", C.SUBSET_LABEL["S1"]), ("S2", C.SUBSET_LABEL["S2"]), ("S3", C.SUBSET_LABEL["S3"]), ("S4", C.SUBSET_LABEL["S4"]), ("S5", C.SUBSET_LABEL["S5"]),
        ("S6", C.SUBSET_LABEL["S6"]), ("S7", C.SUBSET_LABEL["S7"]), ("S8", C.SUBSET_LABEL["S8"])]
SUBSET_FN = dict(C.SUBSETS)
SUBSET_FN["PC075"] = lambda g: C.SUBSETS["P"](g) and g["c"] >= 0.75
sizes = {k: sum(1 for g in GALS if SUBSET_FN[k](g)) for k, _ in SETS}
check("M2 CONTROL: the set sizes equal the pre-flight's (P 110, PC 32, PC125 13, PC15 7)", str(sizes), sizes["P"] == 110 and sizes["PC"] == 32 and sizes["PC125"] == 13 and sizes["PC15"] == 7)
RES["sizes"] = sizes

# ================================================================================================ the analysis of one set in one frame
FRAMES = (("observed", 1), ("rest", 0))
LAW = ("FLAT", "RIVAL")


def recipe_flagged(a, W, rec):
    """the frozen recipe band (section 3 step 11) with the solver's no-root flag kept: a knob with an unbounded bracket is excluded from the quadrature and listed"""
    rows, noroot = {}, []
    for key, br, label in C.KNOBS:
        ls, us = [], []
        for v in br:
            r_ = dict(rec); r_[key] = v
            l_, u_, _ = C.s_star(a, W, r_)
            ls.append(l_); us.append(u_)
        half = 0.5 * abs(ls[1] - ls[0]) if not any(us) else float("nan")
        if any(us):
            noroot.append(key)
        rows[key] = dict(label=label, brackets=br, log_s=ls, noroot=us, half=half)
    hq = math.sqrt(sum(v["half"] ** 2 for v in rows.values() if not math.isnan(v["half"])))
    single = {}
    for name, upd in (("H2 (M_H2 = 0.3 M_HI added)", dict(h2=0.3)), ("P2 kernel", dict(kernel="P2")), ("other frame (k flipped)", dict(k=1 - rec["k"]))):
        r_ = dict(rec); r_.update(upd)
        l_, u_, _ = C.s_star(a, W, r_)
        single[name] = l_ if not u_ else float("nan")
    return rows, hq, single, noroot


def analyse(key, k):
    sel = [g for g in GALS if SUBSET_FN[key](g)]
    a = C.Arr(sel); W = np.array([g["w50"] for g in sel])
    rec = dict(C.REC0, k=k)
    d = C.derive(a, W, rec); ok = d["ok"]
    n, drop = int(ok.sum()), int((~ok).sum())
    D, gb, go, z = d["D"][ok], d["gb"][ok], d["go"][ok], a.z[ok]
    tag = zlib_tag(key, k)
    r, lb, I = C.boot_interval(D, gb, C.NU, A0C, B=10000, tag=tag)
    exp = C.expectations(dict(go=go), z, lb, I, C.NU, A0C)
    bb = C.baryon_bands(a, W, rec)
    rows, hrec, single, rnr = recipe_flagged(a, W, rec)
    lb_btfr, _ = C.s_btfr(a, W, rec)
    l_alt = float(C.implied(D, gb, C.NU, A0A)[0][0])
    # diagnostics: the measured-to-predicted edge-on width, x = (W_c / 2) / V_pred, with V_pred the RAR value at s = 1
    Vp = np.sqrt(gb * C.nuv(C.NU, gb / A0C) * d["R"][ok] if np.ndim(d["R"]) else gb * C.nuv(C.NU, gb / A0C) * d["R"]) / 1e3
    Wc = (W[ok] - rec["delta"]) / (1 + z) ** k
    xq = np.percentile(Wc / 2.0 / Vp, [10, 25, 50, 75, 90, 100])
    thr_ratio = a.sint[ok] / (W[ok] * a.spk_thr[ok])
    out = dict(set=key, frame=k, n=n, dropped=drop, z_med=float(np.median(z)), z_min=float(z.min()), z_max=float(z.max()), **{kk: r[kk] for kk in ("s", "log_s", "unbounded", "unb_frac", "sd_log", "lo68", "hi68", "lo95", "hi95")},
               a0=r["s"] * A0C, alt_s=10 ** l_alt, alt_check=float(abs(l_alt + math.log10(A0A / A0C) - r["log_s"])),
               y_q=np.percentile(d["y"][ok], [5, 25, 50, 75, 95]), frac_y03=float((d["y"][ok] < 0.3).mean()),
               bands={f"{t:+.2f}": dict(s=v[0], noroot=v[1]) for t, v in bb.items()}, recipe_half=hrec, recipe_noroot=rnr,
               recipe={kk: dict(label=v["label"], brackets=v["brackets"], log_s=v["log_s"], noroot=v["noroot"], half=v["half"]) for kk, v in rows.items()}, single={kk: v for kk, v in single.items()},
               btfr_s=10 ** lb_btfr, x_q=xq, thr_ratio_q=np.percentile(thr_ratio, [0, 5, 25, 50, 75, 100]), w_q=np.percentile(W[ok], [5, 25, 50, 75, 95]),
               ew_med=float(np.median([g["e_w50"] for g in sel])))
    for L in LAW:
        e = exp[L]
        sL = e["s"]
        out[L] = dict(s=sL, sd_diff=e["sd_diff"], pull=(r["log_s"] - e["log_s"]) / e["sd_diff"], pull_recipe=(r["log_s"] - e["log_s"]) / math.sqrt(e["sd_diff"] ** 2 + hrec ** 2),
                      in95=bool(r["lo95"] <= sL <= r["hi95"]), in95_recipe=bool(r["lo95"] * 10 ** (-hrec) <= sL <= r["hi95"] * 10 ** hrec),
                      b15=bool(min(r["lo95"], bb[-0.15][0], bb[0.15][0]) <= sL <= max(r["hi95"], bb[-0.15][0], bb[0.15][0])),
                      b30=bool(min(r["lo95"], bb[-0.30][0], bb[0.30][0]) <= sL <= max(r["hi95"], bb[-0.30][0], bb[0.30][0])))
    return out


def zlib_tag(key, k):
    import zlib
    return zlib.crc32(f"{key}|{k}".encode()) % 100000


# ================================================================================================ run
P("\n" + "=" * 110 + "\nRESULTS (s* = the a0 scale relative to canonical 9.3603e-11; 68 / 95 % galaxy-bootstrap intervals, B = 10,000)\n" + "=" * 110)
RESULTS = {}
for key, label in SETS:
    for fname, k in FRAMES:
        r = analyse(key, k)
        RESULTS[f"{key}|{fname}"] = r
        b15 = (min(r["bands"]["-0.15"]["s"], r["bands"]["+0.15"]["s"]), max(r["bands"]["-0.15"]["s"], r["bands"]["+0.15"]["s"]))
        b30 = (min(r["bands"]["-0.30"]["s"], r["bands"]["+0.30"]["s"]), max(r["bands"]["-0.30"]["s"], r["bands"]["+0.30"]["s"]))
        P(f"  {key:6s} [{fname:8s}] N {r['n']:3d}" + (f" (dropped {r['dropped']})" if r["dropped"] else "") + f"  z {r['z_med']:.3f}: s* = {r['s']:.3f}  68% [{r['lo68']:.3f}, {r['hi68']:.3f}]  95% [{r['lo95']:.3f}, {r['hi95']:.3f}]  a0 = {r['a0'] * 1e10:.3f}e-10;  "
          f"baryon +-0.15 [{b15[0]:.3f}, {b15[1]:.3f}]  +-0.30 [{b30[0]:.3f}, {b30[1]:.3f}];  recipe +-{r['recipe_half']:.3f} dex{(' (no-root knobs excluded: ' + ','.join(r['recipe_noroot']) + ')') if r['recipe_noroot'] else ''};  BTFR route {r['btfr_s']:.3f};  y median {r['y_q'][2]:.3f} (y<0.3: {r['frac_y03']:.2f})")
RES["results"] = RESULTS
RES["sets"] = dict(SETS)

# ================================================================================================ the readings (no verdict words)
P("\n" + "=" * 110 + "\nPULLS AND FLAGS (primary set PC; statistics-only pull, recipe-widened pull; flags: in the 95 % interval / recipe-widened / +-0.15 band-widened / +-0.30 band-widened)\n" + "=" * 110)
for fname, k in FRAMES:
    r = RESULTS[f"PC|{fname}"]
    for L in LAW:
        e = r[L]
        P(f"  PC [{fname}] vs {L}: expected s*_L = {e['s']:.3f}; pull {e['pull']:+.2f} (recipe-widened {e['pull_recipe']:+.2f}); flags {''.join('Y' if e[f] else 'n' for f in ('in95', 'in95_recipe', 'b15', 'b30'))}")

P("\n" + "=" * 110 + "\nTHE COMPLETENESS LADDER (observed-frame branch, then rest-frame; median s* against the completeness threshold; the pre-flight's mock biases are the interpretive table)\n" + "=" * 110)
for fname, k in FRAMES:
    P(f"  [{fname}] " + "; ".join(f"{key} (N {RESULTS[f'{key}|{fname}']['n']}) {RESULTS[f'{key}|{fname}']['s']:.3f} [{RESULTS[f'{key}|{fname}']['lo68']:.2f}, {RESULTS[f'{key}|{fname}']['hi68']:.2f}]" for key in ("P", "PC075", "PC", "PC125", "PC15")))

P("\n" + "=" * 110 + "\nDIAGNOSTICS (reported after the widths were read; no decision depends on them)\n" + "=" * 110)
allsel = [g for g in GALS if not g["e0"]]
aA = C.Arr(allsel); Wa = np.array([g["w50"] for g in allsel])
rth = aA.sint / (Wa * aA.spk_thr)
rq = np.percentile(rth, [0, 1, 5, 25, 50])
P(f"  empirical detection ratio S_int / (W50 x S_thr(f = 1)) over all {len(allsel)} galaxies (excluding E0): min {rq[0]:.2f}, 1% {rq[1]:.2f}, 5% {rq[2]:.2f}, 25% {rq[3]:.2f}, median {rq[4]:.2f} (the lower envelope estimates the survey's effective f)")
for key in ("PC", "PC125", "PC15", "P"):
    r = RESULTS[f"{key}|observed"]
    P(f"  {key}: x = (W_c/2)/V_pred (observed frame) quantiles 10/25/50/75/90/100: {np.round(r['x_q'], 2).tolist()}; detection-ratio quantiles 0/5/25/50/75/100: {np.round(r['thr_ratio_q'], 2).tolist()}; W50 quantiles 5/25/50/75/95: {np.round(r['w_q'], 0).tolist()}; median tabulated error {r['ew_med']:.1f} km/s")
RES["diag"] = dict(detection_ratio_all=rq)
check("M1 CONTROL: the alt footing implies the same absolute a0 (s*_alt a0_alt = s*_canonical a0_canonical) in every row", f"max |d log10| = {max(r['alt_check'] for r in RESULTS.values()):.1e}", max(r["alt_check"] for r in RESULTS.values()) < 1e-9)

# ================================================================================================ the points file (chart_a0z_points.csv shape + recipe columns)
cols = ["lane", "object", "gas_class", "z", "z_shown", "no_root", "s_star", "a0_1e-10_m_s2", "stat68_lo", "stat68_hi", "stat95_lo", "stat95_hi", "inner_lo", "inner_hi", "inner_noroot_corner", "outer_lo", "outer_hi", "outer_noroot_corner",
        "recipe_half_dex", "recipe_lo", "recipe_hi", "n", "frame", "quality", "recipe_noroot_knobs"]
ref = os.path.join(C.LANES, "CHART_a0z_combined_2026-09-30", "chart_a0z_points.csv")
ref_cols = open(ref).readline().strip().split(",")
check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{ref_cols == cols[:18]}", ref_cols == cols[:18])
POINTS = [("PC", "observed", "BUDHIES PC (observed-frame widths): lower-quality, selection-limited"), ("PC", "rest", "BUDHIES PC (rest-frame widths): lower-quality, selection-limited"),
          ("PC125", "observed", "BUDHIES PC125 (c >= 1.25, observed-frame)"), ("PC15", "observed", "BUDHIES PC15 (c >= 1.5, observed-frame)"), ("P", "observed", "BUDHIES P-all (selection-dominated, observed-frame)"),
          ("S1", "observed", "BUDHIES inner members (EFE / stripping zone, observed-frame)")]
with open(os.path.join(HERE, f"cfg260_points{SFX}.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(cols)
    for key, fname, obj in POINTS:
        r = RESULTS[f"{key}|{fname}"]
        b15 = (min(r["bands"]["-0.15"]["s"], r["bands"]["+0.15"]["s"]), max(r["bands"]["-0.15"]["s"], r["bands"]["+0.15"]["s"]))
        b30 = (min(r["bands"]["-0.30"]["s"], r["bands"]["+0.30"]["s"]), max(r["bands"]["-0.30"]["s"], r["bands"]["+0.30"]["s"]))
        nr15 = int(r["bands"]["-0.15"]["noroot"] or r["bands"]["+0.15"]["noroot"]); nr30 = int(r["bands"]["-0.30"]["noroot"] or r["bands"]["+0.30"]["noroot"])
        qual = "lower bound (selection acts low)" if key in ("PC", "PC125", "PC15") else ("selection-dominated, do not read as a0" if key == "P" else "environment: ram-pressure / external field")
        w.writerow(["CFG260", obj, "HI", f"{r['z_med']:.4f}", f"{r['z_med']:.4f}", int(r["unbounded"]), f"{r['s']:.6f}", f"{r['a0'] * 1e10:.6f}", f"{r['lo68']:.6f}", f"{r['hi68']:.6f}", f"{r['lo95']:.6f}", f"{r['hi95']:.6f}",
                    f"{b15[0]:.6f}", f"{b15[1]:.6f}", nr15, f"{b30[0]:.6f}", f"{b30[1]:.6f}", nr30, f"{r['recipe_half']:.4f}", f"{r['s'] * 10 ** (-r['recipe_half']):.6f}", f"{r['s'] * 10 ** r['recipe_half']:.6f}", r["n"], fname, qual, ";".join(r["recipe_noroot"])])
P(f"\n  points written: cfg260_points{SFX}.csv ({len(POINTS)} rows)")

nf = sum(1 for c in CK if not c["ok"])
P(f"\n  {len(CK) - nf}/{len(CK)} controls pass" + ("" if not nf else " -> CONTROL FAILURES") + f"  ({time.time() - T0:.0f} s)")
RES["checks"] = CK; RES["seconds"] = round(time.time() - T0, 1); RES["mode"] = "SELFTEST" if SELF else "MEASUREMENT"
json.dump(jc(RES), open(os.path.join(HERE, f"cfg260_results{SFX}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg260_measure{SFX}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
