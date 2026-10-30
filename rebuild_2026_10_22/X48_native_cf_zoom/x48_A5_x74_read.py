#!/usr/bin/env python3
"""X48 AMENDMENT A5: graded X74 SPARC read (criteria a0cbcc6928). X74's script unchanged, c_f = {1e12: A5, 1e13/1e14: A4},
canonical footing, slope 2.7774, f* 0.034 and 0.0615; repeated at the A5 bootstrap 16th/84th; MUTATE c_f(1e12) x 2.
SPARC line per footing = line on both backgrounds (rms <= 0.110 and median Upsilon in [0.50, 0.80]).
Outputs renamed x74_A5read_* inside X74's directory (X74's own A4 outputs never touched); summary x48_A5_x74_read.{out,json} here.
    python3 x48_A5_x74_read.py         # graded read (needs x48_grade_A5.json and x48_analyze_results_ng64_A4.json)
    python3 x48_A5_x74_read.py K2      # K2: table {7.7395930714417345, 4, 4} at f* 0.034 reproduces pre-read P1 exactly"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); X74 = os.path.join(os.path.dirname(HERE), "X74_all_measured_native_cf")
SLOPE = "2.7774425603108597"
MACH = os.path.join(X74, "x74_x30_machinery.log")

def run(tag, c12, c13, c14, fs):
    tab = os.path.join(X74, f"x74_A5read_cf_{tag}.json")
    json.dump({"note": f"X48 A5 X74 read {tag}", "cf_by_mass": {"1e+12": c12, "1e+13": c13, "1e+14": c14}}, open(tab, "w"), indent=1)
    keep = open(MACH).read() if os.path.exists(MACH) else None
    # X74's own post-A4 outputs share these exact names: back them up, run, rename ours, restore theirs
    names = [os.path.join(X74, f"x74_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.out"), os.path.join(X74, f"x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json")]
    saved = {n: open(n, "rb").read() for n in names if os.path.exists(n)}
    for n in saved: os.remove(n)
    env = dict(os.environ, X74_CF=tab, X73_FSTAR=fs, X73_SLOPE=SLOPE, PYTHONHASHSEED="0", OMP_NUM_THREADS="1")
    try:
        p = subprocess.run(["nice", "-n", "15", sys.executable, "x74_native_cf.py"], cwd=X74, env=env, capture_output=True, text=True)
        open(os.path.join(X74, f"x74_A5read_{tag}.log"), "w").write(p.stdout + p.stderr)
        out = {}
        for f in names:
            if os.path.exists(f):
                dst = os.path.join(X74, f"x74_A5read_{tag}_" + os.path.basename(f)); os.replace(f, dst)
                if dst.endswith(".json"): out = json.load(open(dst))
    finally:
        for n, b in saved.items(): open(n, "wb").write(b)
        if keep is not None: open(MACH, "w").write(keep)
    if not out: raise SystemExit(f"UNDECIDED: X74 run {tag} wrote no results (exit {p.returncode})")
    return out

def sparc(R, foot):
    s = R["footings"][foot]["sparc"]
    return dict(line=all(v["line"] for v in s.values()), **{k: dict(rms=v["rms"], U=v["U_median"], n_active=v["n_active"]) for k, v in s.items()})

if len(sys.argv) > 1 and sys.argv[1] == "K2":
    R = run("K2", 7.7395930714417345, 4.0, 4.0, "0.034")
    P = json.load(open(os.path.join(X74, "preread_P1_fs0.034_x74_results_fs0.034_nat_s2.7774.json")))
    d = max(abs(R["footings"][f]["sparc"][t][q] - P["footings"][f]["sparc"][t][q]) for f in ("canonical", "alt") for t in P["footings"][f]["sparc"] for q in ("rms", "U_median"))
    print(f"X48 A5 K2 (X74 read reproduces pre-read P1 SPARC): max |d| {d:.1e}: {'PASS' if d == 0 else 'FAIL'}"); sys.exit(0 if d == 0 else 1)

G = json.load(open(os.path.join(HERE, "x48_grade_A5.json")))
A4p = os.path.join(HERE, "x48_analyze_results_ng64_A4.json")
OUT = ["X48 A5 X74 SPARC read (1e12 at ng 80 [A5], 1e13/1e14 at ng 64 [A4]); kappa = 1/2 FITTED; footings never pooled; not theory closed"]
if not os.path.exists(A4p):
    OUT.append("UNDECIDED: no A4 table"); print("\n".join(OUT)); open(os.path.join(HERE, "x48_A5_x74_read.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1)
A4 = {float(k): v for k, v in json.load(open(A4p))["cf_by_mass"].items() if v is not None}
c13, c14 = A4.get(1e13), A4.get(1e14)
if c13 is None or c14 is None:
    OUT.append("UNDECIDED: A4 table lacks 1e13/1e14"); print("\n".join(OUT)); open(os.path.join(HERE, "x48_A5_x74_read.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1)
pts = dict(med=G["hi"]["median"], p16=G["hi"]["boot68"][0], p84=G["hi"]["boot68"][1])
RES = dict(table=dict(c12=pts, c13=c13, c14=c14), runs={})
for fs in ("0.034", "0.0615"):
    for k, c12 in pts.items():
        R = run(f"{k}_fs{fs}", c12, c13, c14, fs)
        RES["runs"][f"{k}_fs{fs}"] = dict(c12=c12, canonical=sparc(R, "canonical"), alt=sparc(R, "alt"),
                                          verdict={f: R["footings"][f]["verdict"] for f in ("canonical", "alt")},
                                          failing={f: R["footings"][f]["failing"] for f in ("canonical", "alt")},
                                          groupsZ={f: R["footings"][f]["groups"]["Z"] for f in ("canonical", "alt")})
        r = RES["runs"][f"{k}_fs{fs}"]
        OUT.append(f"  f* {fs} {k} c_f(1e12) {c12:.3f}: canonical SPARC {'PASS' if r['canonical']['line'] else 'FAIL'} "
                   f"(U {r['canonical']['A_c2b_refit']['U']:.2f}/{r['canonical']['B_cfg886_bg']['U']:.2f}); alt {'PASS' if r['alt']['line'] else 'FAIL'} "
                   f"(U {r['alt']['A_c2b_refit']['U']:.2f}); failing canonical: {r['failing']['canonical']}; alt: {r['failing']['alt']}")
lab = {}
for fs in ("0.034", "0.0615"):
    cls = [RES["runs"][f"{k}_fs{fs}"]["canonical"]["line"] for k in ("med", "p16", "p84")]
    lab[fs] = ("SPARC SETTLED PASS" if all(cls) else "SPARC SETTLED FAIL") if len(set(cls)) == 1 else f"SPARC {'PASS' if cls[0] else 'FAIL'} [KNIFE EDGE]"
    OUT.append(f"  LABEL f* {fs} (canonical): {lab[fs]}")
M = run("MUTATE_fs0.034", 2 * pts["med"], c13, c14, "0.034")
dU = abs(sparc(M, "canonical")["A_c2b_refit"]["U"] - RES["runs"]["med_fs0.034"]["canonical"]["A_c2b_refit"]["U"])
RES["mutate"] = dict(dU=dU, ok=dU > 0.01); RES["labels"] = lab
OUT.append(f"  MUTATE c_f(1e12) x 2: canonical median Upsilon moves {dU:.2f} (> 0.01 required): {'PASS' if dU > 0.01 else 'FAIL (harness insensitive)'}")
print("\n".join(OUT)); open(os.path.join(HERE, "x48_A5_x74_read.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "x48_A5_x74_read.json"), "w"), indent=1)
