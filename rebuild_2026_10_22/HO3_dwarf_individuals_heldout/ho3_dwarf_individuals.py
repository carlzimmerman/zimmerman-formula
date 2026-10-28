#!/usr/bin/env python3
"""HO3_dwarf_individuals_heldout: per-object held-out test of the frozen CL2 picture on X1's 89 LG dwarfs per footing.

Frozen criteria: FROZEN_CRITERIA.md (554597b160, committed alone). Satellites (X1 host MW/M31, or M200 > 10^12.3) carry
route E = Newtonian baryons + X51's cooling-floor a0-floor Burkert halo; isolated LG field dwarfs follow the law on baryons,
g = g_N nu(g_N/a0). Machinery: X51's committed script executed read-only as a text copy with X62's LF_G edit (as X62's
run_x51 and CL2 do), plus one bookkeeping edit that keeps g_pred, g_N, g_h, host per row. One thread, seconds.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ho3_dwarf_individuals.py                 -> .out, _results.json, _per_object.csv
    HO3_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ho3_dwarf_individuals.py    -> *_MUTATE.* (flag inverted; K1 must fail)
"""
import os, sys, io, json, math, time, csv, resource, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy import stats
from scipy.optimize import minimize

T0 = time.time(); MUTATE = os.environ.get("HO3_MUTATE", "") == "1"; TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
FEET = ("canonical", "alt"); A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
MSUN = 1.98847e30; LOGM_SWITCH = 12.3
SEED = 20261027; P0 = 0.0455; PMIN = 0.01
P(f"HO3_dwarf_individuals_heldout  {'MUTATE (satellite flag inverted)' if MUTATE else 'normal run'}   criteria 554597b160")
P("kappa = 1/2 FITTED; footings never pooled (canonical primary); CL2 picture: route E (cold dark energy halo, X51) if satellite or M200 > 1e12.3, else the law on baryons; not theory closed")

# ------------------------------------------------------------------ the switch (X62's LF_G, satellite flag)
MODE = {"m": "on"}
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / y)
def LF_G(gb, gh, a0, key="dwarfs", above=False):
    gb = float(gb); gh = float(gh); law = nu(gb / a0) * gb if gb > 0 else gb; rE = gb + gh
    if MODE["m"] == "off": return rE
    if MODE["m"] == "law": return law
    use_rE = (not above) if MUTATE else bool(above)
    return rE if use_rE else law

def run_copy(mode):
    MODE["m"] = mode; tag = f"{mode}{TAG}"
    src = open(os.path.join(REB, "X51_dwarf_cooling_floor", "x51_dwarfs.py")).read()
    ed = [("gp = gN + G * Mh / r12 ** 2",
           'gp = float(LF_G(gN, G * Mh / r12 ** 2, A0[f], "dwarfs", r["host"] in ("MW", "M31") or M200 / MSUN > 10 ** 12.3))'),
          ('out.append(dict(name=r["name"], cls=r["cls"],',
           'out.append(dict(host=r["host"], gp=gp, gN=gN, gh=G * Mh / r12 ** 2, gobs=gobs, name=r["name"], cls=r["cls"],'),
          ('f"x51_dwarfs{TAG}.out"', f'"ho3_x51copy_{tag}.out"'), ('f"x51_dwarfs_results{TAG}.json"', f'"ho3_x51copy_{tag}_results.json"')]
    for old, new in ed:
        assert src.count(old) == 1, old[:60]; src = src.replace(old, new)
    ns = {"__file__": os.path.join(HERE, "ho3_x51copy.py"), "__name__": "ho3_x51copy", "LF_G": LF_G}
    argv0 = sys.argv; sys.argv = [ns["__file__"]]
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try: exec(compile(src, ns["__file__"], "exec"), ns)
            except SystemExit: pass
    finally:
        sys.argv = argv0
    return ns

checks = []
# ------------------------------------------------------------------ Step 0 / K0
X62J = json.load(open(os.path.join(REB, "X62_environment_keyed_switch", "x62_x51copy_on_results.json")))["footings"]
X51J = json.load(open(os.path.join(REB, "X51_dwarf_cooling_floor", "x51_dwarfs_results.json")))["footings"]
ns_off = run_copy("off"); ns_on = run_copy("on")
k0_on = all(abs(ns_on["RES"]["footings"][f]["classes"][c][q] - X62J[f]["classes"][c][q]) < 1e-9 for f in FEET for c in X62J[f]["classes"] for q in ("median", "Z")) and \
        all(abs(ns_on["RES"]["footings"][f]["individuals"][k] - v) < 1e-9 for f in FEET for k, v in X62J[f]["individuals"].items())
k0_off = all(abs(ns_off["RES"]["footings"][f]["classes"][c]["median"] - X51J[f]["classes"][c]["median"]) < 1e-9 for f in FEET for c in X51J[f]["classes"])
P(f"STEP 0: copy 'on' reproduces X62 x51copy_on (class medians, Z, 7 individuals) to 1e-9: {'PASS' if k0_on else 'FAIL'}; 'off' reproduces X51 class medians to 1e-9: {'PASS' if k0_off else 'FAIL'}")
P("  X62 on, canonical: " + "; ".join(f"{c} {v['median']:+.3f} (Z {v['Z']:+.2f})" for c, v in ns_on["RES"]["footings"]["canonical"]["classes"].items()))
checks.append(("K0_step0", k0_on and k0_off))
if not (k0_on and k0_off) and not MUTATE:
    P("STEP 0 FAILED: the machinery is not reproduced; lane stops, no held-out number graded.")
    open(os.path.join(HERE, f"ho3_dwarf_individuals{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1)

# ------------------------------------------------------------------ held-out rows (all 89 per footing)
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
ALLCLS = tuple(dict.fromkeys(r["cls"] for r in X1))
ISO_X1 = {(r["footing"], r["name"]): float(r["Delta[iso AQUAL L*0]"]) for r in X1}
MODE["m"] = "on"
ROWS = {f: ns_on["rows"](f, ALLCLS) for f in FEET}

# S2 null thresholds (frozen: 2e5 draws, default_rng(20261027), fresh per N)
def s2_threshold(N):
    rng = np.random.default_rng(SEED); qs = []
    for _ in range(4):                                                         # 4 x 5e4 = 2e5 draws, memory-light
        qs.append(np.median(np.abs(rng.standard_normal((50000, N))), axis=1))
    return float(np.percentile(np.concatenate(qs), 99))
S2T = {}
def thr(N):
    if N not in S2T: S2T[N] = s2_threshold(N)
    return S2T[N]
def rules(Z):
    Z = np.asarray(Z, float); N = len(Z); a = np.abs(Z)
    k = int((a >= 2).sum()); p1 = float(stats.binom.sf(k - 1, N, P0))
    med = float(np.median(a)); t2 = thr(N)
    zmax = float(a.max()); p2 = float(2 * stats.norm.sf(zmax)); p3 = float(-math.expm1(N * math.log1p(-p2))) if p2 < 1 else 1.0
    ok = dict(S1=p1 >= PMIN, S2=med <= t2, S3=p3 >= PMIN)
    return dict(N=N, k_beyond2=k, S1_p=p1, median_absZ=med, S2_threshold=t2, maxabsZ=zmax, S3_p=p3, ok=ok,
                verdict="CONSISTENT WITH ERRORS" if all(ok.values()) else "EXCESS SCATTER: " + ", ".join(r for r, v in ok.items() if not v))
def sig_int(E, s):
    nll = lambda p: 0.5 * float(np.sum((E - p[0]) ** 2 / (s ** 2 + p[1] ** 2) + np.log(s ** 2 + p[1] ** 2)))
    r = minimize(nll, [float(np.median(E)), 0.1], method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-10, maxiter=4000))
    return float(r.x[0]), float(abs(r.x[1]))

RES = dict(criteria="554597b160", mutate=MUTATE, footings={})
k1_all = True; csv_rows = []
for f in FEET:
    R = ROWS[f]; a0 = A0[f]; nviol = 0; nh = 0; nl = 0
    for x in R:
        flag = x["host"] in ("MW", "M31") or x["M200"] > 10 ** LOGM_SWITCH
        exp = x["gN"] + x["gh"] if flag else float(nu(x["gN"] / a0) * x["gN"])
        nviol += int(abs(x["gp"] / exp - 1) > 1e-12); nh += int(flag); nl += int(not flag)
        x["branch"] = "route E halo" if flag else "law"; x["Z"] = x["E"] / x["s"]
    k1 = nviol == 0 and nh == 76 and nl == 13; k1_all &= k1
    P(f"\n=== [{f}]  K1 switch: {nh} halo / {nl} law, {nviol} violations -> {'PASS' if k1 else 'FAIL'}")
    sat = [x for x in R if x["host"] in ("MW", "M31")]; iso = [x for x in R if x["host"] not in ("MW", "M31")]
    k2d = float(np.median([abs(x["E"] - ISO_X1[(f, x["name"])]) for x in iso])); k2 = k2d < 0.03
    P(f"  K2 isolated E vs X1 iso AQUAL column: median |dE| {k2d:.4f} dex -> {'PASS' if k2 else 'FAIL'}")
    checks += [(f"K1_switch[{f}]", k1), (f"K2_iso_vs_X1[{f}]", k2)]
    FR = RES["footings"][f] = {"subsamples": {}}
    for lab, S in (("satellites", sat), ("isolated", iso)):
        E = np.array([x["E"] for x in S]); s = np.array([x["s"] for x in S]); Z = E / s
        g = rules(Z); mu, si = sig_int(E, s); chi2 = float((Z ** 2).sum())
        rho = stats.spearmanr([x["lm"] for x in S], E)
        g.update(sign_pos=float((E > 0).mean()), chi2=chi2, chi2_p=float(stats.chi2.sf(chi2, len(Z))), ml_mean=mu, sigma_int=si,
                 spearman_E_logMstar=float(rho[0]), spearman_p=float(rho[1]), median_E=float(np.median(E)),
                 beyond2=sorted([(x["name"], round(x["Z"], 2)) for x in S if abs(x["Z"]) >= 2], key=lambda t: -abs(t[1])))
        FR["subsamples"][lab] = g
        P(f"  {lab:10s} N {g['N']:2d}: median E {g['median_E']:+.3f}; |Z|>=2: {g['k_beyond2']} (S1 binom p {g['S1_p']:.2e} {'PASS' if g['ok']['S1'] else 'FAIL'}); "
          f"median|Z| {g['median_absZ']:.2f} vs null99 {g['S2_threshold']:.2f} ({'PASS' if g['ok']['S2'] else 'FAIL'}); max|Z| {g['maxabsZ']:.2f} (S3 p {g['S3_p']:.2e} {'PASS' if g['ok']['S3'] else 'FAIL'}) -> {g['verdict']}")
        P(f"     reported: E>0 fraction {g['sign_pos']:.2f}; chi2 {chi2:.1f}/{len(Z)} (p {g['chi2_p']:.1e}); ML mean {mu:+.3f}, sigma_int {si:.3f} dex; Spearman(E, log M*) {g['spearman_E_logMstar']:+.3f} (p {g['spearman_p']:.3f})")
        P("     |Z| >= 2: " + ("; ".join(f"{n} {z:+.2f}" for n, z in g["beyond2"]) or "none"))
    S74 = [x for x in sat if x["name"] not in ("Crater II", "Antlia II")]
    g74 = rules(np.array([x["Z"] for x in S74])); FR["reported_satellites_minus_CraterII_AntliaII"] = g74
    P(f"  reported: satellites without Crater II, Antlia II (N {g74['N']}): |Z|>=2 {g74['k_beyond2']} (p {g74['S1_p']:.2e}); median|Z| {g74['median_absZ']:.2f}/{g74['S2_threshold']:.2f}; max|Z| {g74['maxabsZ']:.2f} (p {g74['S3_p']:.2e}) -> {g74['verdict']}")
    flags = {}
    for nm in ("Leo T", "Phoenix"):
        x = next(q for q in R if q["name"] == nm)
        fl = "ABOVE PICTURE" if x["Z"] >= 2 else ("BELOW PICTURE" if x["Z"] <= -2 else "CONSISTENT")
        flags[nm] = dict(E=x["E"], s=x["s"], Z=x["Z"], flag=fl, branch=x["branch"], E_X1_iso=ISO_X1[(f, nm)])
        P(f"  {nm}: E {x['E']:+.3f} +- {x['s']:.3f} (Z {x['Z']:+.2f}) on the {x['branch']} branch -> {fl}  [X1 iso column {ISO_X1[(f, nm)]:+.3f}]")
    FR["flags"] = flags
    bad = [f"{lab} ({', '.join(r for r, v in FR['subsamples'][lab]['ok'].items() if not v)})" for lab in ("satellites", "isolated") if not all(FR["subsamples"][lab]["ok"].values())]
    FR["verdict"] = "HELD-OUT PASS" if not bad else "HELD-OUT FAIL: " + "; ".join(bad)
    P(f"  VERDICT [{f}]: {FR['verdict']}")
    for x in R:
        csv_rows.append([f, x["name"], x["host"], x["cls"], x["branch"], f"{x['lm']:.2f}", f"{x['E']:.6f}", f"{x['s']:.6f}", f"{x['Z']:.4f}", f"{x['M200']:.4e}"])
V = {f: RES["footings"][f]["verdict"] for f in FEET}
VC = {f: V[f].split(":")[0] for f in FEET}                                     # frozen: footings disagree = different verdict class (post-run fix, disclosed)
RES["verdict"] = (f"{VC['canonical']} on both footings (canonical: {V['canonical']} | alt: {V['alt']})" if VC["canonical"] == VC["alt"]
                  else f"SPLIT (canonical primary): canonical {V['canonical']} | alt {V['alt']}")
P(f"\n=== VERDICT: {RES['verdict']}")

# ------------------------------------------------------------------ K3 rule calibration
rngk = np.random.default_rng([SEED, 3])
def fail_rate(N, scale, n=2000):
    return float(np.mean([not all(rules(scale * rngk.standard_normal(N))["ok"].values()) for _ in range(n)]))
fr76, fr13, fp76 = fail_rate(76, 1.0), fail_rate(13, 1.0), fail_rate(76, 2.0)
k3 = fr76 <= 0.04 and fr13 <= 0.04 and fp76 >= 0.90
P(f"K3 rule calibration: null fail rate N76 {fr76:.4f}, N13 {fr13:.4f} (<= 0.04); planted 2x scatter N76 fail rate {fp76:.4f} (>= 0.90): {'PASS' if k3 else 'FAIL'}")
RES["K3"] = dict(null_fail_76=fr76, null_fail_13=fr13, planted_fail_76=fp76)
checks.append(("K3_calibration", k3))
r_ = rss(); checks.append(("K4_rss", r_ < 1.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(bool(ok) for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.1f} s; peak RSS {r_:.2f} GB")
open(os.path.join(HERE, f"ho3_dwarf_individuals{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"ho3_dwarf_individuals_results{TAG}.json"), "w"), indent=1, default=float)
with open(os.path.join(HERE, f"ho3_dwarf_individuals_per_object{TAG}.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["footing", "name", "host", "cls", "branch", "logMstar", "E", "s", "Z", "M200_Msun"]); w.writerows(csv_rows)
sys.exit(0 if n == len(checks) else 1)
