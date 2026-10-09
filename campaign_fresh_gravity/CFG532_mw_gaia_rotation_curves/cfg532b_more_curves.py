#!/usr/bin/env python3
"""CFG532b: the review's other Gaia-era MW curves (Wang+23, Jiao+23, Zhou+23, SL23 DR3+, Feng+26 Cepheids) with the CFG532
method unchanged, plus a combined slope test by tracer class (one curve per shared-data group).

Frozen criteria: FROZEN_CRITERIA_v2.md (committed alone first, fe132d6c7). CFG532's machinery (law, score, fits) is executed
read-only from cfg532_mw_curves.py (the part above its RES definition); tables are parsed from the arXiv .tex line ranges.
MUTATE (CFG532B_MUTATE=1): M1 law off, M2 baryons x 0.5, M3 injected Keplerian tail. Exit 1 = DETECTED.
kappa = 1/2 is FITTED; both footings never pooled; cold energy mass still required; not theory closed.
Run: nice -n 10 python3 cfg532b_more_curves.py   (2 threads)
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "2"
os.environ["CFG532_MUTATE"] = "0"
import sys, json, math, time, io, contextlib, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "cfg532_mw_curves.py")
src = open(SRC).read()
head = src.split("RES = dict(mutate=MUTATE")[0]
ns = {"__file__": os.path.abspath(SRC), "__name__": "cfg532_import"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(head, "cfg532_head", "exec"), ns)
assert all(ok for ok, _ in ns["CHECKS"]), "CFG532 controls failed on import"
EXT = ns["EXT"]
SRCDIR = os.path.join(EXT, "cfg532_work", "src")
score, v_model, b1mix, chi2, pval, fit_nfw, fit_kepler = (ns[k] for k in
                                                          ("score", "v_model", "b1mix", "chi2", "pval", "fit_nfw", "fit_kepler"))
slope_orig = ns["slope"]
FOOTS, G = ns["FOOTS"], ns["G"]
MUTATE = os.environ.get("CFG532B_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.append(s)


def check(cond, msg):
    CHECKS.append((bool(cond), msg)); P(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
    return bool(cond)


# window control: score() calls the global name `slope` in ns; we swap in a windowed version per class
WIN = {"lo": 15.0, "hi": 27.5}


def slope_win(R, V, E, lo=None, hi=None):
    return slope_orig(R, V, E, WIN["lo"] if lo is None else lo, WIN["hi"] if hi is None else hi)


ns["slope"] = slope_win
T0 = time.time()
P("=" * 112)
P(f"CFG532b  the review's other Gaia-era MW curves; combined slope by tracer class   {'*** MUTATE ***' if MUTATE else 'PRIMARY'}")
P("kappa = 1/2 FITTED; footings 9.36e-11 / 1.13e-10 never pooled; nu_mono; census baryons held; cold energy mass still required")
P("=" * 112)


# ------------------------------------------------------------------ table extraction (from .tex line ranges; no digitising)
def parse(relpath, l0, l1, ncol_min=3):
    lines = open(os.path.join(SRCDIR, relpath)).read().split("\n")
    rows, where = [], []
    for i in range(l0 - 1, l1):
        t = lines[i].split("%")[0].replace("\\\\", "").replace("\\hline", "")
        cells = [c.strip() for c in t.split("&")]
        if len(cells) < ncol_min:
            continue
        try:
            vals = [float(c) for c in cells[:3]]
        except ValueError:
            continue
        rows.append(vals); where.append(i + 1)
    a = np.array(rows)
    return a[:, 0], a[:, 1], a[:, 2], where


TABLES = {
    "Wang23": dict(file="2211.05668/HFW-3DRC-v1.tex", lines=(777, 802), R0=8.34, vsun="(U,V,W)sun = (11.1, 12.24, 7.25) km/s",
                   err="stat", cls="RGB/LIM", grp="LIM", nexp=19),
    "Jiao23": dict(file="2309.00048/rc_mw_z3.tex", lines=(4, 27), R0=8.34, vsun="as Wang+23 (Jiao re-derives Wang's data)",
                   err="published (incl. sys)", cls="RGB/LIM", grp="LIM", nexp=18),
    "Zhou23": dict(file="2212.10393/GRC.tex", lines=(447, 488), R0=8.122, vsun="V_R 11.1, V_phi 245.6 km/s (GRC.tex line 65)",
                   err="stat", cls="RGB/LIM", grp="APOGEE-RGB", nexp=34),
    "SL23_DR3plus": dict(file="2302.01379/ms.tex", lines=(284, 335), R0=8.122, vsun="(see paper)", err="published",
                         cls="RGB/LIM", grp="LIM", nexp=None, report_only=True),
    "Feng26_Cepheids": dict(file="2512.21780/Main.tex", lines=(233, 252), R0=8.275, vsun="Z_sun 0.025 kpc (Main.tex line 170)",
                            err="stat (bootstrap)", cls="Cepheid", grp="Cepheid", nexp=12),
}
NOT_SCORED = {"Mroz19": "1810.02131/pap.tex: only a model-parameter table (no RC table); text slope -1.34 +- 0.21 km/s/kpc, 4 <~ R <~ 20 kpc, R0 8.09",
              "Ablimit20": "2004.13768/arxiv.tex: no table environment",
              "SylosLabini24": "2410.14307/manuscript.tex: only table is sigma_vz coefficients (no in-plane RC table)"}
P("\n--- extraction")
CURVES = {}
for k, t in TABLES.items():
    R, V, S, where = parse(t["file"], *t["lines"])
    t.update(N=len(R), first_line=where[0], last_line=where[-1], Rmin=float(R.min()), Rmax=float(R.max()))
    if t["err"].startswith("stat"):
        E = np.hypot(S, 0.03 * V); E5 = np.hypot(S, 0.05 * V)
    else:
        E = S.copy(); E5 = None
    CURVES[k] = dict(R=R, V=V, E=E, rand=S, E5=E5, R0=t["R0"], meta=t)
    P(f"  {k:<16} {t['file']}:{where[0]}-{where[-1]}  N {len(R):2d}  R {R.min():.2f}-{R.max():.2f}  R0 {t['R0']}  err {t['err']}  [{t['cls']}/{t['grp']}]")
    if t["nexp"] is not None:
        check(len(R) == t["nexp"], f"X {k}: parsed {len(R)} rows (table has {t['nexp']})")
for k, why in NOT_SCORED.items():
    P(f"  {k:<16} NOT SCORED -- {why}")
# CFG532's two on-disk curves, same code path
for k in ("C1_Ou24", "C2_Eilers19"):
    c = dict(ns["CURVES"][k])
    c["meta"] = dict(cls="RGB/LIM", grp="APOGEE-RGB", R0=c["R0"], err="CFG532 convention")
    c["E5"] = None
    CURVES[k.split("_", 1)[1]] = c

if MUTATE:
    # M3: inject a Keplerian tail beyond 15 kpc into every RGB/LIM curve (own errors kept)
    MUT3 = {}
    for k, c in CURVES.items():
        if c["meta"]["cls"] != "RGB/LIM":
            continue
        V15 = float(np.interp(15.0, c["R"], c["V"]))
        Vk = np.where(c["R"] >= 15.0, V15 * (c["R"] / 15.0) ** -0.5, c["V"])
        cc = dict(c); cc["V"] = Vk; MUT3[k] = cc


# ------------------------------------------------------------------ per-curve scoring (CFG532 method)
def class_window(c):
    if c["meta"]["cls"] == "Cepheid":
        return 10.0, float(c["R"].max())
    return 15.0, 27.5


def score_curve(kind, foot, c, scale=1.0, E=None, Rscale=1.0):
    WIN["lo"], WIN["hi"] = class_window(c)
    if Rscale != 1.0:
        WIN["hi"] = WIN["hi"] if c["meta"]["cls"] != "Cepheid" else float(c["R"].max() * Rscale)
    m = (c["R"] * Rscale >= WIN["lo"]) & (c["R"] * Rscale <= WIN["hi"])
    if m.sum() < 4:
        return None
    return score(kind, foot, c, scale=scale, E=E, Rscale=Rscale)


RES = dict(mutate=MUTATE, extraction={k: {kk: vv for kk, vv in t.items() if kk not in ()} for k, t in TABLES.items()},
           not_scored=NOT_SCORED, cells={}, comparators={}, systematics={}, combined={}, cepheid={}, published_slopes={},
           dr4={}, mutate_rows={})
NEW = ["Wang23", "Jiao23", "Zhou23", "SL23_DR3plus", "Feng26_Cepheids"]
fmt = ns["fmt"]

if MUTATE:
    P("\n--- MUTATE M1 law off / M2 baryons x 0.5 (new curves)")
    det = []
    for foot in FOOTS:
        for k in NEW:
            c = CURVES[k]
            o = score_curve("N", foot, c)
            RES["mutate_rows"][f"M1|{k}|{foot}"] = o
            det.append(o["p_census"] < 1e-6); P(f"  M1 {k:<16} {foot:<9} {fmt(o)}")
            for kind in ("RMv", "RMphi"):
                o = score_curve(kind, foot, c, scale=0.5)
                RES["mutate_rows"][f"M2|{k}|{foot}|{kind}"] = o
                det.append(o["p_census"] < 1e-6 and o["verdict"] != "CONSISTENT")
                P(f"  M2 {k:<16} {foot:<9} {kind:<5} {fmt(o)}")

# ------------------------------------------------------------------ combined slope machinery
def delta(kind, foot, c):
    WIN["lo"], WIN["hi"] = class_window(c)
    bd, sb, n = slope_win(c["R"], c["V"], c["E"])
    mx, key = b1mix(1.0)
    bl, _, _ = slope_win(c["R"], v_model(kind, mx, key, foot, c["R"]), c["E"])
    return bd - bl, sb, n, bd, bl


def combine(ds, ss, rho):
    ds, ss = np.asarray(ds), np.asarray(ss)
    C = np.diag(ss ** 2)
    for i, j in itertools.combinations(range(len(ds)), 2):
        C[i, j] = C[j, i] = rho * ss[i] * ss[j]
    Ci = np.linalg.inv(C); one = np.ones(len(ds))
    var = 1.0 / (one @ Ci @ one); mean = var * (one @ Ci @ ds)
    return float(mean), float(math.sqrt(var))


def class_verdict(Z, sbar, bl):
    if sbar > abs(bl + 0.5) / 2:
        return "NOT DIAGNOSTIC"
    return "SHAPE CONSISTENT" if abs(Z) <= 2 else ("SHAPE TENSION" if abs(Z) <= 3 else "SHAPE EXCLUDED")


APO, LIM = ["Ou24", "Eilers19", "Zhou23"], ["Jiao23", "Wang23"]


def run_combined(curves, label):
    out = {}
    for foot in FOOTS:
        for kind in ("RMv", "RMphi"):
            d = {k: delta(kind, foot, curves[k]) for k in APO + LIM}
            rows = {}
            for a, b in itertools.product(APO, LIM):
                for rho in (0.0, 0.5):
                    m, s = combine([d[a][0], d[b][0]], [d[a][1], d[b][1]], rho)
                    bl = 0.5 * (d[a][4] + d[b][4])
                    rows[f"{a}+{b}|rho{rho}"] = dict(mean=m, sig=s, Z=m / s, verdict=class_verdict(m / s, s, bl))
            prim = rows["Ou24+Jiao23|rho0.0"]; prim5 = rows["Ou24+Jiao23|rho0.5"]
            Zs = [r["Z"] for r in rows.values()]
            out[f"{foot}|{kind}"] = dict(per_curve={k: dict(delta=v[0], sig=v[1], n=v[2], b_data=v[3], b_law=v[4], Z=v[0] / v[1])
                                                    for k, v in d.items()},
                                         pairs=rows, primary=prim, primary_rho05=prim5, Z_range=[min(Zs), max(Zs)])
            P(f"  [{label}] {foot:<9} {kind:<5} primary Ou+Jiao: Delta {prim['mean']:+.3f} +- {prim['sig']:.3f}  Z {prim['Z']:+.2f} "
              f"({prim['verdict']}); rho 0.5: Z {prim5['Z']:+.2f} ({prim5['verdict']}); all pairs Z {min(Zs):+.2f}..{max(Zs):+.2f}")
    return out


if MUTATE:
    P("\n--- MUTATE M3 injected Keplerian tail (R >= 15) into every RGB/LIM curve; primary combined |Z| must exceed 3")
    r3 = run_combined(MUT3, "M3")
    RES["mutate_rows"]["M3"] = r3
    for kf, v in r3.items():
        det.append(abs(v["primary"]["Z"]) > 3 and abs(v["primary_rho05"]["Z"]) > 3)
    detected = all(det)
    check(detected, f"MUTATE DETECTED in {sum(det)}/{len(det)} cells (M1, M2 every new curve; M3 combined |Z| > 3 indep and rho 0.5)")
    RES["mutate_detected"] = detected
else:
    P("\n--- comparators (NFW on B1 Newtonian + NFW; Kepler R >= 19; slope in the class window)")
    mN, _ = b1mix(1.0)
    for k in NEW:
        c = CURVES[k]
        WIN["lo"], WIN["hi"] = class_window(c)
        nf = fit_nfw(c, mN)
        kp = fit_kepler(c) if (c["R"] >= 19).sum() >= 2 else None
        bd, sb, n = slope_win(c["R"], c["V"], c["E"])
        bn, _, _ = slope_win(c["R"], nf["vfun"](c["R"]), c["E"])
        RES["comparators"][k] = dict(NFW=dict(M200=nf["M200"], c=nf["c"], chi2=nf["chi2"], p=nf["p"], slope=bn, dslope_sig=(bd - bn) / sb),
                                     Kepler=kp, slope_data=bd, slope_err=sb, n_slope=n, window=[WIN["lo"], WIN["hi"]],
                                     slope_kepler_sig=(bd + 0.5) / sb, slope_flat_sig=bd / sb)
        ktxt = f"Kepler(R>=19,n={kp['n']}) M {kp['M']:.2e} chi2 {kp['chi2']:.1f} p {kp['p']:.2f}" if kp else "Kepler: <2 pts at R>=19"
        P(f"  {k:<16} win {WIN['lo']:.1f}-{WIN['hi']:.1f} (n {n}) data slope {bd:+.3f}+-{sb:.3f} (Kepler {(bd + 0.5) / sb:+.1f}sig, flat "
          f"{bd / sb:+.1f}sig) | NFW M200 {nf['M200']:.2e} c {nf['c']:.1f} chi2 {nf['chi2']:.1f}/{len(c['R'])} p {nf['p']:.2f} "
          f"slope {bn:+.3f} ({(bd - bn) / sb:+.1f}sig) | {ktxt}")

    P("\n--- law cells, new curves (B1 census held; s* post hoc, reported only)")
    for foot in FOOTS:
        for kind in ("RMv", "RMphi", "ALG"):
            for k in NEW:
                o = score_curve(kind, foot, CURVES[k])
                if o is None:
                    P(f"  {foot:<9} {kind:<5} {k:<16} slope NOT DIAGNOSTIC (<4 pts in window)"); continue
                o["report_only"] = bool(TABLES[k].get("report_only", False))
                RES["cells"][f"{k}|{foot}|{kind}"] = o
                P(f"  {foot:<9} {kind:<5} {k:<16} {fmt(o)}{'  (REPORTED ONLY)' if o['report_only'] else ''}")

    P("\n--- Cepheid window variant 15 kpc - R_max (frozen: < 4 points -> NOT DIAGNOSTIC)")
    c = CURVES["Feng26_Cepheids"]
    n15 = int(((c["R"] >= 15) & (c["R"] <= c["R"].max())).sum())
    P(f"  Feng26: {n15} points in 15-{c['R'].max():.2f} kpc -> {'NOT DIAGNOSTIC' if n15 < 4 else 'scored'}")
    RES["cepheid"]["n_15_Rmax"] = n15

    P("\n--- systematics S1 table errors only, S2 5% (stat-only curves), S3 R0 -> 8.178 (crude)")
    for foot in FOOTS:
        for kind in ("RMv", "RMphi"):
            for k in NEW:
                c = CURVES[k]
                base = RES["cells"].get(f"{k}|{foot}|{kind}")
                if base is None:
                    continue
                rows = {}
                if c["meta"]["err"].startswith("stat"):
                    rows["S1_table_only"] = score_curve(kind, foot, c, E=c["rand"])
                    rows["S2_5pct"] = score_curve(kind, foot, c, E=c["E5"])
                if abs(c["R0"] - 8.178) > 1e-6:
                    rows["S3_R0_8.178"] = score_curve(kind, foot, c, Rscale=8.178 / c["R0"])
                for kk, o in rows.items():
                    if o is None:
                        continue
                    o["flips"] = o["verdict"] != base["verdict"]
                    P(f"  {foot:<9} {kind:<5} {k:<16} {kk:<14} {fmt(o)}{'  <-- FLIP' if o['flips'] else ''}")
                RES["systematics"][f"{k}|{foot}|{kind}"] = rows

    P("\n--- combined slope, RGB/LIM class (one per shared-data group: APOGEE-RGB x LIM)")
    RES["combined"]["RGB_LIM"] = run_combined(CURVES, "RGB/LIM")
    P("\n--- Cepheid class (Feng+26 alone; Mroz+19 and Ablimit+20 have no table)")
    for foot in FOOTS:
        for kind in ("RMv", "RMphi"):
            d = delta(kind, foot, CURVES["Feng26_Cepheids"])
            Z = d[0] / d[1]
            v = class_verdict(Z, d[1], d[4])
            RES["cepheid"][f"{foot}|{kind}"] = dict(delta=d[0], sig=d[1], n=d[2], b_data=d[3], b_law=d[4], Z=Z, verdict=v)
            P(f"  {foot:<9} {kind:<5} Feng26 10-{CURVES['Feng26_Cepheids']['R'].max():.2f} kpc: data {d[3]:+.3f} +- {d[1]:.3f} law {d[4]:+.3f} "
              f"Z {Z:+.2f} -> {v}")

    P("\n--- published linear slope (text, not a table; reported only): Mroz+19 dTheta/dR -1.34 +- 0.21 km/s/kpc, 4-20 kpc")
    Rg = np.linspace(4.0, 20.0, 33)
    for foot in FOOTS:
        for kind in ("RMv", "RMphi"):
            mx, key = b1mix(1.0)
            v = v_model(kind, mx, key, foot, Rg)
            g = float(np.polyfit(Rg, v, 1)[0])
            RES["published_slopes"][f"Mroz19|{foot}|{kind}"] = dict(law_dVdR=g, pub=-1.34, pub_err=0.21, Z=(-1.34 - g) / 0.21)
            P(f"  {foot:<9} {kind:<5} law dV/dR (even grid 4-20) {g:+.2f} km/s/kpc vs -1.34 +- 0.21 -> {(-1.34 - g) / 0.21:+.1f} sigma")

    P("\n--- Gaia DR4 decider")
    for foot in FOOTS:
        for kind in ("RMv", "RMphi"):
            cb = RES["combined"]["RGB_LIM"][f"{foot}|{kind}"]
            pc = cb["per_curve"]
            bl = 0.5 * (pc["Ou24"]["b_law"] + pc["Jiao23"]["b_law"])
            bdm = cb["primary"]["mean"] + bl
            mx, key = b1mix(1.0)
            Vg = v_model(kind, mx, key, foot, np.array([15.0, 20.0, 25.0]))
            ce = RES["cepheid"][f"{foot}|{kind}"]
            RES["dr4"][f"{foot}|{kind}"] = dict(rgb_sig_needed_vs_measured=abs(cb["primary"]["mean"]) / 3,
                                                rgb_sig_needed_vs_kepler=abs(bl + 0.5) / 3, rgb_now_sig=cb["primary"]["sig"],
                                                ceph_sig_needed_vs_measured=abs(ce["delta"]) / 3, ceph_now_sig=ce["sig"],
                                                V15=float(Vg[0]), V20=float(Vg[1]), V25=float(Vg[2]), b_law=bl, b_meas_comb=bdm)
            P(f"  {foot:<9} {kind:<5} RGB/LIM: law {bl:+.3f} vs combined measured {bdm:+.3f}; sigma now {cb['primary']['sig']:.3f}, "
              f"needed (3 sig vs measured) {abs(cb['primary']['mean']) / 3:.3f}, (3 sig vs Kepler) {abs(bl + 0.5) / 3:.3f} | Cepheid: "
              f"sigma now {ce['sig']:.3f}, needed {abs(ce['delta']) / 3:.3f} | census V(15/20/25) {Vg[0]:.1f}/{Vg[1]:.1f}/{Vg[2]:.1f}")

if not MUTATE:
    P("\n--- POST-RUN diagnostic (added after the first run; NOT in the frozen criteria; no verdict input)")
    P("  (a) the same combined slope statistic applied to an NFW fitted to each curve (B1 Newtonian + NFW, as in the comparators)")
    mN, _ = b1mix(1.0)
    dn = {}
    for k in APO + LIM:
        c = CURVES[k]
        WIN["lo"], WIN["hi"] = class_window(c)
        nf = fit_nfw(c, mN)
        bd, sb, _ = slope_win(c["R"], c["V"], c["E"])
        bn, _, _ = slope_win(c["R"], nf["vfun"](c["R"]), c["E"])
        dn[k] = (bd - bn, sb, bn, nf["M200"])
    rows = {}
    for a, b in itertools.product(APO, LIM):
        for rho in (0.0, 0.5):
            m, s_ = combine([dn[a][0], dn[b][0]], [dn[a][1], dn[b][1]], rho)
            rows[f"{a}+{b}|rho{rho}"] = dict(mean=m, sig=s_, Z=m / s_)
    Zs = [r["Z"] for r in rows.values()]
    RES["post_run"] = dict(NFW_combined=rows, NFW_per_curve={k: dict(delta=v[0], sig=v[1], b_nfw=v[2], M200=v[3]) for k, v in dn.items()},
                           NFW_Z_range=[min(Zs), max(Zs)])
    pr = rows["Ou24+Jiao23|rho0.0"]; pr5 = rows["Ou24+Jiao23|rho0.5"]
    P(f"      fitted-NFW primary Ou+Jiao: Delta {pr['mean']:+.3f} +- {pr['sig']:.3f} Z {pr['Z']:+.2f}; rho 0.5 Z {pr5['Z']:+.2f}; "
      f"all pairs Z {min(Zs):+.2f}..{max(Zs):+.2f}  (NFW slopes: " + ", ".join(f"{k} {v[2]:+.3f}" for k, v in dn.items()) + ")")

RES["checks"] = [dict(ok=a, msg=b) for a, b in CHECKS]
RES["runtime_s"] = time.time() - T0
P(f"\nchecks: {sum(a for a, _ in CHECKS)}/{len(CHECKS)} pass; runtime {RES['runtime_s']:.0f} s")


def jc(o):
    if isinstance(o, dict):
        return {k: jc(v) for k, v in o.items() if not callable(v)}
    if isinstance(o, (list, tuple)):
        return [jc(v) for v in o]
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.floating, np.integer, np.bool_)):
        return o.item()
    return o


json.dump(jc(RES), open(os.path.join(HERE, f"cfg532b_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg532b{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUTATE:
    sys.exit(1 if RES.get("mutate_detected") else 0)
sys.exit(0 if all(a for a, _ in CHECKS) else 2)
