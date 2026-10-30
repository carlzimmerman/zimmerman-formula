#!/usr/bin/env python3
"""SH1_softened_halo_grade: route E's full grader (X74 unchanged, via CE1's call) on eta = R x CE1's converged eta; MW and KiDS via X79's text.
    python3 sh1_grade.py          # K1, K2, all medians, ends if a median passes
    python3 sh1_grade.py --mutate # R = 0.3 at all masses
    python3 sh1_grade.py --x79    # K3 + MW and KiDS for every scenario"""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
X74 = os.path.join(RB, "X74_all_measured_native_cf"); X79 = os.path.join(RB, "X79_native_eta_mw_kids"); CE1 = os.path.join(RB, "CE1_converged_eta_grade")
SLOPE = "2.7774425603108597"; MACH = os.path.join(X74, "x74_x30_machinery.log")
CE = json.load(open(os.path.join(CE1, "ce1_results.json"))); ETA = {e: CE["eta"][str(e)] for e in (12, 13, 14)}
RS = (0.573, 0.685, 0.817); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
cf = lambda eta: 4 * (eta / 10.82) ** 0.8
def etas(sc, R, k="med"): return {12: R * ETA[12][k], 13: (R if sc == "B" else 1.0) * ETA[13][k], 14: (R if sc == "B" else 1.0) * ETA[14][k]}

def grade(tag, eta, fs):
    tab = os.path.join(HERE, f"{tag}_cf_table.json"); json.dump({"note": tag, "cf_by_mass": {f"1e+{e}": cf(v) for e, v in eta.items()}}, open(tab, "w"), indent=1)
    names = [os.path.join(X74, f"x74_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.out"), os.path.join(X74, f"x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json")]
    saved = {n: open(n, "rb").read() for n in names if os.path.exists(n)}; keep = open(MACH).read() if os.path.exists(MACH) else None
    for n in saved: os.remove(n)
    env = dict(os.environ, X74_CF=tab, X73_FSTAR=fs, X73_SLOPE=SLOPE, PYTHONHASHSEED="0", OMP_NUM_THREADS="1"); out = {}
    try:
        p = subprocess.run(["nice", "-n", "15", sys.executable, "x74_native_cf.py"], cwd=X74, env=env, capture_output=True, text=True)
        for f in names:
            if os.path.exists(f):
                dst = os.path.join(HERE, f"{tag}_" + os.path.basename(f)); os.replace(f, dst)
                if dst.endswith(".json"): out = json.load(open(dst))
    finally:
        for n, b in saved.items(): open(n, "wb").write(b)
        if keep is not None: open(MACH, "w").write(keep)
    if not out: raise SystemExit(f"UNDECIDED: grader run {tag} wrote no results (exit {p.returncode})")
    return out, p.stdout

def summ(R, foot):
    F = R["footings"][foot]; s = F["sparc"]
    return dict(verdict=F["verdict"], failing=F["failing"], groupsZ=F["groups"]["Z"], sparc_line=all(v["line"] for v in s.values()),
                sparc={k: dict(rms=v["rms"], U=v["U_median"]) for k, v in s.items()})
def ok(s): return s["sparc_line"] and not s["failing"]

def x79_run(kind, tag, ev):
    """X79's text, read-only, with only EV / _EV replaced; __file__ here so outputs land in this lane."""
    src = os.path.join(X79, f"x79_{kind}.py"); T = open(src).read(); new = f"np.array({ev!r})"
    if kind == "mw":
        pat = 'EV = np.array([S77["1e+12_ng64"]["eta_med"], S77["1e+13_ng48"]["eta_med"], S77["1e+14_ng48"]["eta_med"]])'; assert T.count(pat) == 1
        T = T.replace(pat, "EV = " + new)
    else:
        pat = '_EV = np.array([_S77["1e+12_ng64"]["eta_med"], _S77["1e+13_ng48"]["eta_med"], _S77["1e+14_ng48"]["eta_med"]])'; assert T.count(pat) == 1
        T = T.replace(pat, "_EV = " + new)
    d = os.path.join(HERE, "x79_" + tag); os.makedirs(d, exist_ok=True); me = os.path.join(HERE, f"x79_{kind}.py"); open(me, "w").write(T)  # script in HERE so its REB resolves
    before = set(os.listdir(HERE))
    p = subprocess.run(["nice", "-n", "15", sys.executable, me], cwd=HERE, capture_output=True, text=True,
                       env=dict(os.environ, X79_ETA="native", PYTHONHASHSEED="0", OMP_NUM_THREADS="1"))
    open(os.path.join(d, f"x79_{kind}.log"), "w").write(p.stdout + p.stderr); os.remove(me)
    for f in set(os.listdir(HERE)) - before - {f"x79_{kind}.py"}: os.replace(os.path.join(HERE, f), os.path.join(d, f))
    return p

if "--x79" in sys.argv:
    S77 = json.load(open(os.path.join(RB, "X77_direct_core_surface_density", "x77_results.json")))["summary"]
    ev0 = [S77["1e+12_ng64"]["eta_med"], S77["1e+13_ng48"]["eta_med"], S77["1e+14_ng48"]["eta_med"]]
    for name, ev in [("K3", ev0)] + [(f"{sc}_R{R}", list(etas(sc, R).values())) for sc in "AB" for R in RS]:
        for kind in ("mw", "kids"):
            p = x79_run(kind, name.replace(".", "p"), ev); P(f"  {name} {kind}: exit {p.returncode}")
    open(os.path.join(HERE, "sh1_x79.out"), "a").write("\n".join(OUT) + "\n"); sys.exit()

if "--mutate" in sys.argv:
    R, _ = grade("SH1_MUTATE", {e: 0.3 * ETA[e]["med"] for e in ETA}, "0.034"); s = summ(R, "canonical")
    b = json.load(open(os.path.join(HERE, "sh1_results.json")))["runs"]["B_R0.573_fs0.034"]["canonical"]["sparc"]["A_c2b_refit"]["U"]
    u = s["sparc"]["A_c2b_refit"]["U"]; P(f"MUTATE R 0.3: canonical SPARC U {u:.3f} vs B R 0.573 {b:.3f}: {'PASS' if u > b else 'FAIL'}; failing {s['failing']}")
    open(os.path.join(HERE, "sh1_mutate.out"), "w").write("\n".join(OUT) + "\n"); json.dump(dict(U=u, base=b, s=s), open(os.path.join(HERE, "sh1_mutate_results.json"), "w"), indent=1); sys.exit()

P("SH1 softened halos through route E's full grader; kappa = 1/2 FITTED; footings never pooled; not theory closed")
K, _ = grade("SH1_K1", etas("B", 1.0), "0.034"); G = json.load(open(os.path.join(CE1, "CE1_med_fs0.034_x74_results_fs0.034_nat_s2.7774.json")))
d = max(abs(K["footings"][f]["sparc"][t][q] - G["footings"][f]["sparc"][t][q]) for f in ("canonical", "alt") for t in G["footings"][f]["sparc"] for q in ("rms", "U_median"))
P(f"K1 R = 1 reproduces CE1 (SPARC rms/U, both footings): max |d| {d:.1e}: {'PASS' if d == 0 else 'FAIL'}")
RES = dict(K1=d == 0, runs={}, labels={})
for sc in "AB":
    for R in RS:
        for fs in ("0.034", "0.0615"):
            e = etas(sc, R); key = f"{sc}_R{R}_fs{fs}"; G, so = grade("SH1_" + key, e, fs)
            if sc == "A" and R == 0.817 and fs == "0.034":
                m = re.search(r"eta\(M\) at 1e12/13/14/15: ([\d.]+)", so); v = float(m.group(1)); RES["K2"] = abs(v - 21.2) <= 0.01; P(f"K2 grader eta(1e12) at R 0.817: {v:.3f}: {'PASS' if RES['K2'] else 'FAIL'}")
            RES["runs"][key] = dict(eta=e, canonical=summ(G, "canonical"), alt=summ(G, "alt"))
            for foot in ("canonical", "alt"):
                s = RES["runs"][key][foot]; lab = "SOFTENED FAIL"
                if ok(s):
                    ends = []
                    for k in ("p16", "p84"):
                        Ge, _ = grade(f"SH1_{key}_{k}", etas(sc, R, k), fs); ends.append(ok(summ(Ge, foot)))
                    lab = "SOFTENED PASS" if all(ends) else "KNIFE EDGE"; s["ends_ok"] = ends
                RES["labels"][f"{key}_{foot}"] = lab
                P(f"  {sc} R {R} f* {fs} [{foot}] eta {e[12]:.2f}/{e[13]:.2f}/{e[14]:.2f}: {lab}; SPARC U {s['sparc']['A_c2b_refit']['U']:.2f}/{s['sparc']['B_cfg886_bg']['U']:.2f} rms {s['sparc']['A_c2b_refit']['rms']:.4f}; groups Z {s['groupsZ']:+.2f}; failing {s['failing']}")
            json.dump(RES, open(os.path.join(HERE, "sh1_results.json"), "w"), indent=1); open(os.path.join(HERE, "sh1.out"), "w").write("\n".join(OUT) + "\n")
