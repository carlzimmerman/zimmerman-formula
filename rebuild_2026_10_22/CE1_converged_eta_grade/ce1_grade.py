#!/usr/bin/env python3
"""CE1_converged_eta_grade (criteria 38e1a28c55): route E full grader (X74 unchanged) with the converged-cusp native eta.
    python3 ce1_grade.py            # graded (cluster masses at ng 48)
    python3 ce1_grade.py --A4       # post-A4 rerun (needs X77's A4_x77_results.json); outputs CE1_A4_*
    python3 ce1_grade.py --mutate   # eta x 0.5"""
import json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
X74 = os.path.join(RB, "X74_all_measured_native_cf"); X77 = os.path.join(RB, "X77_direct_core_surface_density")
X81P = os.path.join(RB, "X81_core_convergence", "x80_core_convergence.py")
A4, MUT = "--A4" in sys.argv, "--mutate" in sys.argv
argv0 = sys.argv; sys.argv = [X81P]
src = open(X81P).read(); src = src[:src.index("# K1: exact smooth core")]
NS = dict(__file__=X81P, __name__="x81_prefix"); exec(compile(src, X81P, "exec"), NS); sys.argv = argv0
a_fit, M_nfw, eta_of = NS["a_fit_profile"], NS["M_nfw"], NS["eta_of"]
SLOPE = "2.7774425603108597"; MACH = os.path.join(X74, "x74_x30_machinery.log")
TAG = "CE1_A4" if A4 else ("CE1_MUTATE" if MUT else "CE1")
OUT = []
def P(s): print(s, flush=True); OUT.append(s)

def grade(tag, table, fs):
    tab = os.path.join(HERE, f"{tag}_cf_table.json"); json.dump({"note": tag, "cf_by_mass": table}, open(tab, "w"), indent=1)
    names = [os.path.join(X74, f"x74_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.out"), os.path.join(X74, f"x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json")]
    saved = {n: open(n, "rb").read() for n in names if os.path.exists(n)}; keep = open(MACH).read() if os.path.exists(MACH) else None
    for n in saved: os.remove(n)
    env = dict(os.environ, X74_CF=tab, X73_FSTAR=fs, X73_SLOPE=SLOPE, PYTHONHASHSEED="0", OMP_NUM_THREADS="1")
    out = {}
    try:
        p = subprocess.run(["nice", "-n", "15", sys.executable, "x74_native_cf.py"], cwd=X74, env=env, capture_output=True, text=True)
        open(os.path.join(HERE, f"{tag}.log"), "w").write(p.stdout + p.stderr)
        for f in names:
            if os.path.exists(f):
                dst = os.path.join(HERE, f"{tag}_" + os.path.basename(f)); os.replace(f, dst)
                if dst.endswith(".json"): out = json.load(open(dst))
    finally:
        for n, b in saved.items(): open(n, "wb").write(b)
        if keep is not None: open(MACH, "w").write(keep)
    if not out: raise SystemExit(f"UNDECIDED: grader run {tag} wrote no results (exit {p.returncode})")
    return out

def summ(R, foot):
    F = R["footings"][foot]; s = F["sparc"]
    return dict(verdict=F["verdict"], failing=F["failing"], groupsZ=F["groups"]["Z"], sparc_line=all(v["line"] for v in s.values()),
                sparc={k: dict(rms=v["rms"], U=v["U_median"]) for k, v in s.items()})

R0 = {}
if not A4 and not MUT:
    # K1: X77's own table reproduces X77's committed grade
    S77 = json.load(open(os.path.join(X77, "x77_results.json")))["summary"]
    t77 = {f"1e+{e}": S77[f"1e+{e}_ng{64 if e == 12 else 48}"]["cf_equiv"] for e in (12, 13, 14)}
    K = grade("CE1_K1", t77, "0.034"); G = json.load(open(os.path.join(X77, "x77grade_x74_results_fs0.034_nat_s2.7774.json")))
    d = max(abs(K["footings"][f]["sparc"][t][q] - G["footings"][f]["sparc"][t][q]) for f in ("canonical", "alt") for t in G["footings"][f]["sparc"] for q in ("rms", "U_median"))
    P(f"K1 X77 table reproduces X77's committed grade (SPARC rms/U, both footings): max |d| {d:.1e}: {'PASS' if d == 0 else 'FAIL'}"); R0["K1"] = d == 0

runs = json.load(open(os.path.join(X77, "A4_x77_results.json" if A4 else "x77_results.json")))["runs"]
P(f"{TAG}: converged-cusp eta (exact NFW at each run's c_nfw, x_c 0.001); kappa = 1/2 FITTED; not theory closed")
ETA = {}
for e in (12, 13, 14):
    ng = 64 if (e == 12 or A4) else 48
    rs = [r for k, r in runs.items() if k.startswith(f"M1e{e}_") and k.endswith(f"_ng{ng}") and r.get("c_nfw")]
    v = np.array([float(eta_of(a_fit(M_nfw(r["c_nfw"]), 0.001))) for r in rs]) * (0.5 if MUT else 1.0)
    b = np.median(v[np.random.default_rng(20261030).integers(0, len(v), (10000, len(v)))], axis=1)
    ETA[e] = dict(ng=ng, n=len(v), per_run=v.tolist(), med=float(np.median(v)), p16=float(np.percentile(b, 16)), p84=float(np.percentile(b, 84)),
                  measured_X77_med=float(np.median([r["S"]["eta"] for r in rs])))
    P(f"  1e{e} ng {ng} (n {len(v)}): eta_conv {ETA[e]['med']:.2f} [68% {ETA[e]['p16']:.2f}, {ETA[e]['p84']:.2f}]  (X77 at the cut {ETA[e]['measured_X77_med']:.2f})"
      + ("" if ng == 64 else "  [ng 48]"))
if not A4 and not MUT:
    R0["K2"] = abs(ETA[12]["med"] - 25.94) <= 0.01; P(f"K2 1e12 converged median vs X81 25.94: {ETA[12]['med']:.4f}: {'PASS' if R0['K2'] else 'FAIL'}")
cf = lambda eta: 4 * (eta / 10.82) ** 0.8
RES = dict(checks=R0, eta=ETA, runs={})
pts = ("med",) if MUT else ("med", "p16", "p84")
for fs in ("0.034",) if MUT else ("0.034", "0.0615"):
    for k in pts:
        table = {f"1e+{e}": cf(ETA[e][k]) for e in (12, 13, 14)}
        R = grade(f"{TAG}_{k}_fs{fs}", table, fs)
        RES["runs"][f"{k}_fs{fs}"] = dict(cf_table=table, canonical=summ(R, "canonical"), alt=summ(R, "alt"))
        for foot in ("canonical", "alt"):
            s = RES["runs"][f"{k}_fs{fs}"][foot]
            P(f"  f* {fs} {k} [{foot}] c_f-eq {', '.join(f'{v:.2f}' for v in table.values())}: {s['verdict']}; SPARC "
              f"{'PASS' if s['sparc_line'] else 'FAIL'} (U {s['sparc']['A_c2b_refit']['U']:.2f}/{s['sparc']['B_cfg886_bg']['U']:.2f}, rms {s['sparc']['A_c2b_refit']['rms']:.4f}); "
              f"groups Z {s['groupsZ']:+.2f}; failing: {s['failing']}")
if MUT:
    base = json.load(open(os.path.join(HERE, "ce1_results.json")))["runs"]["med_fs0.034"]["canonical"]["sparc"]["A_c2b_refit"]["U"]
    dU = RES["runs"]["med_fs0.034"]["canonical"]["sparc"]["A_c2b_refit"]["U"] - base
    P(f"MUTATE eta x 0.5: canonical SPARC median Upsilon moves {dU:+.3f} (must rise > 0.01): {'PASS' if dU > 0.01 else 'FAIL'}")
else:
    LAB = {}
    for fs in ("0.034", "0.0615"):
        for foot in ("canonical", "alt"):
            ok = [(not RES["runs"][f"{k}_fs{fs}"][foot]["failing"]) and RES["runs"][f"{k}_fs{fs}"][foot]["sparc_line"] for k in pts]
            LAB[f"{fs}_{foot}"] = ("CONVERGED NATIVE PASS" if all(ok) else "KNIFE EDGE" if ok[0] else "CONVERGED NATIVE FAIL")
            P(f"LABEL f* {fs} {foot}: {LAB[f'{fs}_{foot}']}" + ("" if A4 else " [cluster masses ng 48]"))
    RES["labels"] = LAB
json.dump(RES, open(os.path.join(HERE, f"{TAG.lower()}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"{TAG.lower()}.out"), "w").write("\n".join(OUT) + "\n")
