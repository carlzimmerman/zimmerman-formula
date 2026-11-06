#!/usr/bin/env python3
"""QX24 iter_1 (criteria d4f3f62c47 local / a2e21898a1 origin): is the law's hot/cold step keyed on ENVIRONMENT?
python3 qx24.py [--mutate]   (M2 Newton offsets -> qx24_MUTATE.*)
kappa = 1/2 FITTED; footings never pooled; not theory closed. One thread, seconds."""
import os, sys, json, math, csv
import numpy as np
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "qx24_MUTATE" if MUT else "qx24"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)

# ---- QX20 library (QX16-fixed samples), read-only, exactly as QX23 loads it
src = open(os.path.join(REPO, "closure_2026_11_06", "QX20_failure_ladder", "qx20.py")).read()
NS = {"__file__": os.path.join(REPO, "closure_2026_11_06", "QX20_failure_ladder", "qx20.py"), "__name__": "qx20_lib"}
_argv = sys.argv; sys.argv = [sys.argv[0]]; exec(compile(src[:src.index("BGRID = ")], "qx20_lib", "exec"), NS); sys.argv = _argv
A0, glaw, SP = NS["A0"], NS["glaw"], NS["SP"]
Q20 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX20_failure_ladder", "qx20.json")))
Q18 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX18_elliptical_gate", "qx18.json")))
Q21 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX21_step_origin", "qx21.json")))
LW = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "LW1_law_scorecard", "lw1_dwarfs.json")))
X1 = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount", "x1_per_system.csv"))))
sys.path.insert(0, os.path.join(REPO, "gext_vectors_2026", "src")); import gext_estimator as GE   # read-only import
DATA = os.path.join(REPO, "real_research", "data")
GPC = 4.30091e-3   # G in pc (km/s)^2 / Msun
VC = {"MW": 200.0, "M31": 230.0}
rng = np.random.default_rng(20261124)

def sparc_points(a0, ud=0.5, newton=False):
    """QX23's sparc_points, verbatim logic: per-galaxy (log gbar/a0, residual dex); disc ud, bulge 1.4 ud."""
    law = (lambda g: g) if newton else (lambda g: glaw(g, a0)); out = {}
    for g in SP:
        vb2 = g["vg2"] + (ud / 0.5) * g["vd2"] + (1.4 * ud / 0.7) * g["vbu2"]; r = g["R"]
        ok = vb2 > 0; gb = vb2[ok] / r[ok]; go = g["V"][ok] ** 2 / r[ok]
        out[g["name"]] = (np.log10(gb / a0), np.log10(go / law(gb)))
    return out

# ---- environment inputs
GX = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "gext_vectors_2026", "data", "gext_vectors.csv")))}
est = GE.GextEstimator(os.path.join(REPO, "gext_vectors_2026", "data", "raw", "2mpp_vizier.tsv"),
                       os.path.join(REPO, "gext_vectors_2026", "data", "raw", "mcxc.tsv"), catalog_mode="ks115")
# KA3: estimator vs gext_vectors.csv on 3 SPARC rows
rows = list(GX.values()); ka3 = []
for r in (rows[0], rows[len(rows) // 2], rows[-1]):
    no = est.eN_at(float(r["ra"]), float(r["dec"]), float(r["D"]))["eN"]
    ka3.append(abs(math.log10(no) - float(r["log_eN_noclu"])))
KA3 = max(ka3) <= 1e-3

# elliptical positions: SLUGGS median GC position where present; else literature J2000 written here (disclosed)
LIT = {"NGC720": (28.252, -13.739), "NGC1407": (55.049, -18.580), "NGC4125": (182.025, 65.174), "NGC4261": (184.847, 5.825),
       "NGC4472": (187.445, 8.000), "NGC4649": (190.917, 11.553), "NGC6482": (267.953, 23.072)}
sl = {}
for ln in open(os.path.join(DATA, "sluggs_forbes2017_gcvel.tsv")):
    t = ln.split("\t")
    if len(t) < 4 or ln.startswith("#"): continue
    nm = t[1].strip().split("_")[0]
    try: sl.setdefault(nm, []).append((float(t[2]), float(t[3])))
    except ValueError: continue
HUM = {}
for ln in open(os.path.join(DATA, "humphrey2006_ellipticals.tsv")):
    if ln.startswith("#") or ln.startswith("name"): continue
    t = ln.rstrip("\n").split("\t"); HUM[t[0]] = float(t[3])
EPOS = {}
for nm in LIT:
    if nm in sl and len(sl[nm]) >= 10:
        a = np.array(sl[nm]); EPOS[nm] = (float(np.median(a[:, 0])), float(np.median(a[:, 1])), "SLUGGS GC median")
    else: EPOS[nm] = (LIT[nm][0], LIT[nm][1], "literature J2000 (not from a file)")

RES = dict(tag=TAG, criteria="d4f3f62c47 (origin a2e21898a1)", note="kappa = 1/2 FITTED; not theory closed",
           KA3=dict(max_dex=max(ka3), ok=KA3), ell_positions=EPOS, foot={})
P("QX24 environment key. kappa = 1/2 FITTED; not theory closed." + ("  [MUTATE M2: Newton offsets]" if MUT else ""))
P(f"KA3 estimator vs gext_vectors.csv (3 rows): max {max(ka3):.1e} dex -> {'PASS' if KA3 else 'FAIL'}")

SAT_CLASSES = ("MW classical", "bright M31", "M31 others", "M31 dE")      # T3a set (ultra-faints excluded); indiv:* added below
for f in ("canonical", "alt"):
    a0 = A0[f]; ps = LW["footings"][f]["per_system"]; sparc = Q20[f]["sparc_mean"]; R = {}
    x1 = {r["name"]: r for r in X1 if r["footing"] == f}
    def off(n):
        return float(x1[n]["Delta[Newton]"]) if MUT else float(ps[n]["plain"])
    names = [n for n in ps if n in x1]
    cls = {n: ps[n]["cls"] for n in names}
    xe = {n: float(x1[n]["x_e_mid"]) for n in names}
    # tidal susceptibility
    tau = {}
    for n in names:
        r = x1[n]; host = r["host"]
        if host not in VC: continue
        Re = float(r["rh_pc"]); sg = float(r["sigma"]); d = float(r["d_host_kpc"]) * 1e3
        MW_ = 4 * sg ** 2 * Re / GPC; Mh = VC[host] ** 2 * d / GPC
        tau[n] = Re / (d * (MW_ / (3 * Mh)) ** (1 / 3))
    graded = [n for n in names if cls[n] in ("MW classical", "bright M31")]
    field = [n for n in names if cls[n] == "LG field"]
    Ds = float(np.median([off(n) for n in graded]) - sparc)
    xc = float(math.sqrt(max(xe[n] for n in field) * np.median([xe[n] for n in graded])))
    KA1 = abs(float(np.median([ps[n]["plain"] for n in names if cls[n] == "MW classical"])) - 0.2445) <= 1e-4 if f == "canonical" else None
    KA2 = abs(sparc - Q20[f]["sparc_mean"]) <= 1e-6
    R["key"] = dict(Delta_s=Ds, x_c=xc, n_graded=len(graded), n_field=len(field))
    P(f"\n[{f}] key E: Delta_s {Ds:+.3f} dex (graded satellites median {np.median([off(n) for n in graded]):+.3f} - SPARC {sparc:+.3f}); "
      f"x_c {xc:.4f} (field max x_e {max(xe[n] for n in field):.4f}, graded sat median {np.median([xe[n] for n in graded]):.4f})"
      + (f"; KA1 {'PASS' if KA1 else 'FAIL'}" if KA1 is not None else "") + f"; KA2 {'PASS' if KA2 else 'FAIL'}")
    R["KA1"] = KA1; R["KA2"] = KA2

    # T1 KiDS isolated lenses (carried)
    t1 = Q21["T1"]; D, s = t1["Dx"], t1["s_tot"]; z = D / s
    T1 = "KILLED" if z >= 3 else ("COMPATIBLE" if abs(z) < 2 else "NO VERDICT")
    R["T1"] = dict(pred=0.0, D=D, s_tot=s, z=z, label=T1, carried="QX21 T1, known before freeze")
    P(f"T1 KiDS isolated early/late: E predicts 0; observed {D:+.3f} +- {s:.3f} (carried QX21) z {z:.2f} -> {T1}")

    # T2 ellipticals
    E2 = {}
    for nm, (ra, de, srcp) in EPOS.items():
        Dm = HUM[nm]
        no = est.eN_at(ra, de, Dm)["eN"] * GE.A0 / a0; mx = est.eN_at(ra, de, Dm, completeness=True, missing_baryons_x8=True)["eN"] * GE.A0 / a0
        o = Q18["foot"][f]["per_galaxy"][nm]["kroupa"]
        E2[nm] = dict(x_e_noclu=no, x_e_maxclu=mx, offset=o, pos=srcp)
    low = [v["offset"] for v in E2.values() if v["x_e_noclu"] < xc]; high = [v["offset"] for v in E2.values() if v["x_e_noclu"] >= xc]
    if len(low) < 2: T2 = "NO VERDICT"
    elif np.median(low) > 0.15: T2 = "KILLED"
    elif np.median(low) <= 0.15 and (not high or np.median(high) >= Ds - 0.15): T2 = "COMPATIBLE"
    else: T2 = "NO VERDICT"
    rho2 = spearmanr([math.log10(v["x_e_noclu"]) for v in E2.values()], [v["offset"] for v in E2.values()])
    R["T2"] = dict(per=E2, n_low=len(low), median_low=float(np.median(low)) if low else None,
                   n_high=len(high), median_high=float(np.median(high)) if high else None, spearman=[float(rho2[0]), float(rho2[1])], label=T2)
    P(f"T2 ellipticals: below x_c {len(low)} (median {np.median(low) if low else float('nan'):+.3f}), above {len(high)} "
      f"(median {np.median(high) if high else float('nan'):+.3f}); Spearman offset vs log x_e {rho2[0]:+.2f} (p {rho2[1]:.2f}) -> {T2}")
    for nm, v in E2.items():
        P(f"   {nm:8s} x_e noclu {v['x_e_noclu']:.4f} maxclu {v['x_e_maxclu']:.4f} offset {v['offset']:+.3f} [{v['pos'][:18]}]")

    # T3 satellites: environment vs tides
    sats = [n for n in names if (cls[n] in SAT_CLASSES or cls[n].startswith("indiv:")) and n in tau]
    sats = list(dict.fromkeys(sats))
    safe = [n for n in sats if tau[n] < 0.05]
    fmed = float(np.median([off(n) for n in field]))
    if len(safe) < 5: T3a = "NO VERDICT"; lo = hi = med = float("nan")
    else:
        v = np.array([off(n) for n in safe]); fv = np.array([off(n) for n in field])
        b = [np.median(rng.choice(v, len(v))) - np.median(rng.choice(fv, len(fv))) for _ in range(10000)]
        med = float(np.median(v) - fmed); lo, hi = float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
        T3a = "STEP SURVIVES TIDES" if (med >= 0.15 and lo > 0) else ("TIDES ACCOUNT" if lo <= 0 <= hi else "NO VERDICT")
    allsat = [n for n in names if cls[n] != "LG field" and n in tau]
    lx = np.array([math.log10(xe[n]) for n in allsat]); lt = np.array([math.log10(tau[n]) for n in allsat]); ov = np.array([off(n) for n in allsat])
    def partial(a, b, c):
        ra, rb, rc = (np.argsort(np.argsort(x)) for x in (a, b, c))
        def res(y, x): A = np.vstack([x, np.ones_like(x)]).T; return y - A @ np.linalg.lstsq(A, y, rcond=None)[0]
        return float(np.corrcoef(res(ra.astype(float), rc.astype(float)), res(rb.astype(float), rc.astype(float)))[0, 1])
    p_x = partial(ov, lx, lt); p_t = partial(ov, lt, lx)
    sh = np.array([partial(ov, rng.permutation(lx), lt) for _ in range(1000)]); p95 = float(np.percentile(np.abs(sh), 95))
    M1 = float(np.mean(np.abs(sh) < p95))
    R["T3"] = dict(n_sats=len(sats), n_safe=len(safe), safe=safe, safe_minus_field=med, ci95=[lo, hi], field_median=fmed, label_T3a=T3a,
                   T3b=dict(N=len(allsat), partial_rho_xe_given_tau=p_x, partial_rho_tau_given_xe=p_t, shuffle_p95_abs=p95,
                            xe_trend_beyond_shuffle=abs(p_x) > p95), M1_frac_below_p95=M1)
    P(f"T3a tidally safe satellites (tau < 0.05): N {len(safe)} of {len(sats)}; median - field {med:+.3f} [{lo:+.3f},{hi:+.3f}] -> {T3a}")
    tq = np.percentile([tau[n] for n in sats], [10, 50, 90])
    R["T3"]["tau_p10_p50_p90"] = [float(x) for x in tq]
    P(f"   safe: {', '.join(safe)}; tau over the T3a set p10/p50/p90 {tq[0]:.3f}/{tq[1]:.3f}/{tq[2]:.3f} (reported)")
    P(f"T3b all satellites N {len(allsat)}: partial rho(offset, log x_e | log tau) {p_x:+.2f}; partial rho(offset, log tau | log x_e) {p_t:+.2f}; "
      f"shuffle |rho| 95th pct {p95:.2f} -> x_e trend {'beyond' if abs(p_x) > p95 else 'within'} shuffle")

    # T4 SPARC
    pts = sparc_points(a0, newton=MUT)
    resid = {n: float(np.mean(v[1])) for n, v in pts.items()}
    xs = {n: float(GX[n]["log_eN_noclu"]) for n in resid if n in GX}
    xev = {n: 10 ** xs[n] * GE.A0 / a0 for n in xs}
    dense = [n for n in xev if xev[n] >= xc]; rest = [n for n in xev if xev[n] < xc]
    if len(dense) < 5: T4 = "NO VERDICT (no power)"; dd = sd = float("nan")
    else:
        dd = float(np.mean([resid[n] for n in dense]) - np.mean([resid[n] for n in rest]))
        bs = [np.mean([resid[n] for n in rng.choice(dense, len(dense))]) - np.mean([resid[n] for n in rng.choice(rest, len(rest))]) for _ in range(4000)]
        sd = float(np.std(bs))
        T4 = "KILLED" if dd <= Ds - 3 * sd else ("COMPATIBLE" if abs(dd - Ds) <= 2 * sd else "NO VERDICT")
    rho4 = spearmanr([math.log10(xev[n]) for n in xev], [resid[n] for n in xev])
    R["T4"] = dict(n=len(xev), n_dense=len(dense), dense=dense, dense_minus_rest=dd, sigma=sd, pred=Ds, label=T4,
                   spearman=[float(rho4[0]), float(rho4[1])], x_e_range=[min(xev.values()), max(xev.values())])
    P(f"T4 SPARC: N {len(xev)}, x_e {min(xev.values()):.4f}-{max(xev.values()):.4f}; dense (x_e >= x_c) {len(dense)}; "
      f"dense - rest {dd:+.3f} +- {sd:.3f} vs E {Ds:+.3f} -> {T4}; Spearman resid vs log x_e {rho4[0]:+.2f} (p {rho4[1]:.2f})")

    graded_kill = any(lab == "KILLED" for lab in (T1, T2, T4))
    overall = "KILLED" if graded_kill else ("SUPPORTED" if (T3a == "STEP SURVIVES TIDES" and "COMPATIBLE" in (T1, T2, T4)) else "NO VERDICT")
    R["overall"] = overall
    P(f"[{f}] OVERALL: {overall}")
    if MUT: R["M2_Delta_s_shift"] = None
    RES["foot"][f] = R

if MUT:
    base = json.load(open(os.path.join(HERE, "qx24.json")))
    for f in ("canonical", "alt"):
        sh = RES["foot"][f]["key"]["Delta_s"] - base["foot"][f]["key"]["Delta_s"]
        RES["foot"][f]["M2_Delta_s_shift"] = sh
        P(f"M2 [{f}] Newton: Delta_s shift {sh:+.3f} dex -> {'BITES' if abs(sh) > 0.3 else 'DOES NOT BITE'}")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=str)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
