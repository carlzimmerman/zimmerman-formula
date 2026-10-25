#!/usr/bin/env python3
"""X31 P2 (per-system clusters): X21's unbinned per-cluster machinery (exec'd read-only from x21_switch_anatomy.py, step 3 cut)
with the feedback ratio F as the variable.  Criteria: FROZEN_CRITERIA.md (1aa11f9bcb) section 5 P2, AMENDMENT_A1 (358e3859ed).
Variables: V0 MGAS500 (control) and V1 KT (both must reproduce X21's JSON to <= 1e-9: K5), F1 F_cl, F2 F_exc (thermal excess).
Run:   OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 15 python3 x31_cluster_F_unbinned.py          -> x31_cluster_F_unbinned.out / _results.json
       X31_MUTATE=1 ...  (F_cl, F_exc permuted across clusters, seed 3131: K6 must FAIL; exit 1)
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import os, sys, math, json
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
os.environ.pop("X21_MUTATE", None)
sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import quad
from scipy.stats import mannwhitneyu

ME = os.path.abspath(__file__); HERE = os.path.dirname(ME); REB = os.path.dirname(HERE)
X21PATH = os.path.join(REB, "X21_cluster_switch_anatomy", "x21_switch_anatomy.py")
X21J = json.load(open(os.path.join(REB, "X21_cluster_switch_anatomy", "x21_switch_anatomy_results.json")))
MUT31 = os.environ.get("X31_MUTATE", "") == "1"; TAG31 = "_MUTATE" if MUT31 else ""

# ---- frozen constants (section 2), identical to the class script
G_ = 6.674e-11; MSUN_ = 1.989e30; KPC_ = 3.0857e19; MPC_ = KPC_ * 1e3; KB_ = 1.380649e-23; MP_ = 1.67262192e-27; KEV_ = 1.602176634e-16; MU_ = 0.6
KC = 0.5 ** (2.3 - 1.3)
ETA = (KC * (8.0 ** -1.3 - 100.0 ** -1.3) / 1.3) / ((0.5 ** 0.7 - 0.1 ** 0.7) / 0.7 + KC * (0.5 ** -0.3 - 100.0 ** -0.3) / 0.3)
ESN = 1.0 * 1e44 * ETA / (1 - 0.4) / MSUN_ / 1e6                 # (km/s)^2 per unit M*/M_den
ERE = 1.5 * KB_ * 2e4 / (MU_ * MP_) / 1e6


def f_cluster(kT, M500c, R500c, mode):
    """F for one cluster from eRASS1 KT [keV], M500 [1e13 Msun], R500 [kpc]."""
    M5 = M500c * 1e13 * MSUN_; R5 = R500c / 1e3 * MPC_; sig2 = G_ * M5 / (2 * R5) / 1e6; kT500 = MU_ * MP_ * G_ * M5 / (2 * R5)
    kTJ = kT * KEV_ if mode == "ICM" else max(kT * KEV_ - kT500, 0.0)
    e = (1 / 1.2) * 1.5 * kTJ / (MU_ * MP_) / 1e6 + (0.2 / 1.2) * ESN + ERE
    return e / sig2


# ---- X21's source, read-only, with: no re-exec, its own MUTATE off, outputs renamed into this lane, F labels inserted, VARS extended, step 3 cut
TX = open(X21PATH).read()
TX = TX.replace('if os.environ.get("MallocMediumZone") != "0":\n    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})\n', "")
TX = TX.replace('MUT = os.environ.get("X21_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""', 'MUT = False; TAG = TAG31')
TX = TX.replace('OUTF = open(os.path.join(HERE, f"x21_switch_anatomy{TAG}.out"), "w")', 'OUTF = open(os.path.join(HERE, f"x31_cluster_F_unbinned{TAG}.out"), "w")')
INS = '''LAB["CX"] = LAB["L300"]/LAB["L500"]
LAB["FCL"] = np.array([f_cluster(k, m, r, "ICM") if k > 0 else np.nan for k, m, r in zip(col("KT"), col("M500"), col("R500"))])
LAB["FEX"] = np.array([f_cluster(k, m, r, "EXC") if k > 0 else np.nan for k, m, r in zip(col("KT"), col("M500"), col("R500"))])
if MUT31:
    _pm = np.random.default_rng(3131).permutation(N); LAB["FCL"] = LAB["FCL"][_pm]; LAB["FEX"] = LAB["FEX"][_pm]
'''
assert TX.count('LAB["CX"] = LAB["L300"]/LAB["L500"]\n') == 1
TX = TX.replace('LAB["CX"] = LAB["L300"]/LAB["L500"]\n', INS)
i0 = TX.index("VARS = ["); i1 = TX.index("TEST = {}; BINT = {}")
TX = TX[:i0] + 'VARS = [("V0", "MGAS500 (control)", "Mg", "log"), ("V1", "KT", "KT", "log"), ("F1", "F_cl", "FCL", "log"), ("F2", "F_exc", "FEX", "log")]\n' + TX[i1:]
TX = TX[:TX.index("# ============================================================== STEP 3")]
for s_ in ('OUTF = open(os.path.join(HERE, f"x31_cluster_F_unbinned{TAG}.out"), "w")', 'VARS = [("V0", "MGAS500 (control)"', 'LAB["FCL"]'):
    assert s_ in TX, s_
NS = {"__file__": ME, "__name__": "x21_exec", "TAG31": TAG31, "MUT31": MUT31, "f_cluster": f_cluster}
exec(compile(TX, X21PATH, "exec"), NS)
say, check, CHECKS, RES, TEST, BINT, LAB, N, rss, T0, time = (NS[k] for k in ("say", "check", "CHECKS", "RES", "TEST", "BINT", "LAB", "N", "rss", "T0", "time"))

# ---- K5: X21 reproduction (V0, V1 cells)
say("\n=== X31 P2 checks and summary")
dev = 0.0; nnum = 0
for vk in ("V0", "V1"):
    for cl, o in TEST[vk]["cells"].items():
        ref = X21J["tests"][vk]["cells"][cl]
        for q in ("b", "s_b", "Z_lin", "D_med", "Z_b", "Z_c", "p_scan"):
            dev = max(dev, abs(o[q] - ref[q])); nnum += 1
check("K5", dev <= 1e-9, f"X21 V0/V1 cells reproduced: max |dev| {dev:.1e} over {nnum} numbers", "<= 1e-9")
# ---- K6: each cluster's F recomputes from its own eRASS1 row
E = NS["E"]; JI = NS["JI"]
rec = np.array([f_cluster(float(E["KT"][j]), float(E["M500"][j]), float(E["R500"][j]), "ICM") if float(E["KT"][j]) > 0 else np.nan for j in JI])
ok = np.isfinite(rec)
k6 = float(np.nanmax(np.abs(LAB["FCL"][ok] / rec[ok] - 1))) if ok.any() else float("inf")
k6 = k6 if np.array_equal(np.isfinite(LAB["FCL"]), ok) else max(k6, 1.0)
check("K6", k6 <= 1e-12, f"F_cl per cluster vs recomputation from its own KT, M500, R500: max rel dev {k6:.1e} ({int(ok.sum())} clusters with KT)", "<= 1e-12")
# ---- tercile medians and Mann-Whitney (MGAS500 terciles as X7/X19)
Mgl = LAB["Mg"]; q3 = np.quantile(Mgl, [1/3, 2/3]); T3ID = np.digitize(Mgl, q3)
SUM = {}
for vk, lk in (("F1", "FCL"), ("F2", "FEX")):
    v = LAB[lk]; med = [float(np.nanmedian(v[(T3ID == t) & np.isfinite(v)])) for t in range(3)]; n = [int(((T3ID == t) & np.isfinite(v)).sum()) for t in range(3)]
    a = v[(T3ID == 0) & np.isfinite(v)]; b = v[(T3ID > 0) & np.isfinite(v)]; mw = mannwhitneyu(a, b, alternative="two-sided")
    SUM[vk] = dict(tercile_median=med, tercile_n=n, mw_T1_vs_T23_p=float(mw.pvalue), median_T1=float(np.median(a)), median_T23=float(np.median(b)))
    say(f"  {vk} ({TEST[vk]['name']}): MGAS500-tercile medians {' / '.join(f'{m:.3f}' for m in med)} (n {n}); T1 {np.median(a):.3f} vs T2+T3 {np.median(b):.3f}, Mann-Whitney p {mw.pvalue:.2g};"
        f" class {TEST[vk]['cls']}" + (f" ({TEST[vk]['shape']})" if TEST[vk]["shape"] else "") + f"; Spearman with MGAS500 {TEST[vk]['spearman']:+.2f}")
    for cl, o in TEST[vk]["cells"].items():
        say(f"     {cl}: lin b {o['b']:+.3f}+-{o['s_b']:.3f} (Z {o['Z_lin']:+.2f}, p_perm {o['p_lin']:.3f}); median step {o['D_med']:+.3f} (Z {o['Z_med']:+.2f}); "
            f"joint Z_b {o['Z_b']:+.2f} Z_c {o['Z_c']:+.2f}; scan p {o['p_scan']:.3f}; Z_b at fixed MGAS500 {o['Z_b_fixed_mass']:+.2f}")
pk = rss(); check("K4", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
npass = sum(ok_ for _, ok_ in CHECKS)
RES.update(x31_criteria="1aa11f9bcb", x31_mutate=MUT31, x31_summary=SUM, runtime_s=time.time() - T0, peak_rss_GB=pk, N=N)
RES.pop("budget", None)
say(f"X31 P2 COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time() - T0:.0f} s]")
NS["OUTF"].close()
REPO = os.path.dirname(REB)
txt = open(os.path.join(HERE, f"x31_cluster_F_unbinned{TAG31}.out")).read().replace(REPO, "<repo>").replace(os.path.dirname(REPO), "<parent>")
open(os.path.join(HERE, f"x31_cluster_F_unbinned{TAG31}.out"), "w").write(txt)
json.dump(RES, open(os.path.join(HERE, f"x31_cluster_F_unbinned_results{TAG31}.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
sys.exit(0 if npass == len(CHECKS) and not MUT31 else 1)
