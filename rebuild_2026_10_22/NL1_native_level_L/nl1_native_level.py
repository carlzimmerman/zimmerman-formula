#!/usr/bin/env python3
"""NL1_native_level_L: the concentration level L from the framework's own ng 64 zooms, graded on CL2's full line set.
Frozen criteria 7493e2902a (committed alone, before any ng 64 zoom finished). Measurement: X48's measure() imported read-only.
Grade: LEE1's executed copy of CL2's harness (read-only, up to its Part B), as LEE1 grades one (T, L) draw.

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run (after the zooms finish):  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I nl1_native_level.py      (NL1_MUTATE=1 twin)
"""
import os, sys, json, math, glob, hashlib, importlib.util
import numpy as np

MUTN = os.environ.get("NL1_MUTATE", "0") == "1"
TAGN = "_MUTATE" if MUTN else ""
HERE_NL = os.path.dirname(os.path.abspath(__file__)); REB_NL = os.path.dirname(HERE_NL); REPO_NL = os.path.dirname(REB_NL)
X48 = os.path.join(REB_NL, "X48_native_cf_zoom")
OUTN = []
def Q(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTN.append(s)
Q(f"NL1_native_level_L (criteria 7493e2902a){'  [MUTATE: A2 reference x1.1]' if MUTN else ''}; kappa = 1/2 FITTED; not theory closed")
chk = {}

# ---------- 1. native level from the ng 64 zooms
spec = importlib.util.spec_from_file_location("x48_analyze_ro", os.path.join(X48, "x48_analyze.py")); XA = importlib.util.module_from_spec(spec)
sys.argv_bak = sys.argv; sys.argv = ["x48_analyze_ro"]; spec.loader.exec_module(XA); sys.argv = sys.argv_bak
N = 12000; xs = XA.synthetic_nfw(4.0, N, 1); msyn = 1.0 / N
res = XA.measure(xs, msyn, (N * msyn) / (4 / 3 * math.pi) / (18 * math.pi ** 2), 1e-4)
chk["K0_measure"] = res.get("flag") == "ok" and abs(res["cf"] / 4.0 - 1) < 0.15
A2 = json.load(open(os.path.join(X48, "x48_analyze_results_ng48_A2.json")))["cf_by_mass"]
ref12 = A2["1e+12"] * (1.1 if MUTN else 1.0)
chk["K1"] = all(abs(a - b) <= 0.01 for a, b in zip((ref12, A2["1e+13"], A2["1e+14"]), (11.63, 8.22, 7.31)))
Q(f"  K0 measure() on synthetic NFW c 4: {res.get('cf', float('nan')):.3f}: {'PASS' if chk['K0_measure'] else 'FAIL'};  K1 A2 medians {ref12:.2f} / {A2['1e+13']:.2f} / {A2['1e+14']:.2f}: {'PASS' if chk['K1'] else 'FAIL'}")
runs = {}
for d in sorted(glob.glob(os.path.join(X48, "runs", "M1e12_s*_ng64"))):
    sn = os.path.join(d, "snap_zf.npz")
    if not os.path.exists(sn): runs[os.path.basename(d)] = dict(flag="not finished"); continue
    Z = np.load(sn); meta = json.loads(str(Z["meta"]))
    rho_mz = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + meta["zf"]) ** 3
    o = XA.measure(Z["x"], float(Z["m"]), rho_mz, meta["eps"]); o.update(seed=meta["seed"], ng=meta["ng"], N=meta["N"])
    runs[os.path.basename(d)] = {k: (float(v) if isinstance(v, (np.floating, float, int)) and not isinstance(v, bool) else v) for k, v in o.items()}
    Q(f"  {os.path.basename(d)}: {o['flag']}" + (f", c_f {o['cf']:.2f} (NFW-fit {o['c_nfw_fit']:.2f})" if o["flag"] == "ok" else ""))
ok = [r["cf"] for r in runs.values() if r.get("flag") == "ok"]
RES = dict(criteria="7493e2902a", mutate=MUTN, runs=runs, A2=A2)
if len(ok) < 7:
    Q(f"\n=== NOT READY: {len(ok)} of 9 ng 64 runs ok (needs 7). Nothing graded.")
    RES["verdict"] = "NOT READY"; RES["checks"] = chk
    json.dump(RES, open(os.path.join(HERE_NL, f"nl1_native_level_results{TAGN}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE_NL, f"nl1_native_level{TAGN}.out"), "w").write("\n".join(OUTN) + "\n"); sys.exit(2)
c64 = float(np.median(ok)); R = c64 / ref12; Lnat = round(7.31 * R, 4)
bs = np.random.default_rng(20261028); bm = [np.median(bs.choice(ok, len(ok))) for _ in range(2000)]
L68 = [round(7.31 * float(np.percentile(bm, 16)) / ref12, 4), round(7.31 * float(np.percentile(bm, 84)) / ref12, 4)]
Q(f"\n  ng 64: {len(ok)} ok, median c {c64:.3f} (ng 48 {ref12:.2f}) -> R {R:.4f} -> L_nat = 7.31 R = {Lnat:.4f}  (68% {L68})")
RES.update(c64=c64, R=R, L_nat=Lnat, L68=L68)

# ---------- 2. grade on CL2's harness (LEE1's executed copy, read-only up to Part B)
LS = open(os.path.join(REB_NL, "LEE1_look_elsewhere", "lee1.py")).read()
LS = LS[:LS.index("# ================= Part B: 24 seeded draws =================")]
os.environ.pop("LEE1_MUTATE", None)
NS = {"__file__": os.path.join(HERE_NL, "lee1_ro.py"), "__name__": "lee1_ro"}
exec(compile(LS, os.path.join(REB_NL, "LEE1_look_elsewhere", "lee1.py"), "exec"), NS)
chk["K0_lee1"] = all(ok_ for k, ok_ in NS["checks"] if k.startswith(("K0", "K2a", "K2b")))
Q(f"  K0 LEE1 Step-0 checks: {'PASS' if chk['K0_lee1'] else 'FAIL'}")
def grade_cfg(T, L, lab):
    tag = f"shpS9_L{L}_T{T}"
    NS["STAT"].clear(); R43c, _ = NS["call"](NS["run_x43"], "on", tag + "_B"); F53c = NS["call"](NS["run_x53"], "on", tag); F53cre = NS["call"](NS["run_x53"], "off", tag)
    g = NS["grade"](R43c, F53c, F53cre, NS["R51"], lab)
    return dict(T=T, L=L, fails_canonical=g["canonical"]["fails"], fails_alt=g["alt"]["fails"])
def cl3_T(L): return round(12.2357 + (L - 3.75) * (12.149 - 12.2357) / (3.9 - 3.75), 4)
G = {}
G["PRIMARY"] = grade_cfg(12.3, Lnat, f"PRIMARY: L_nat {Lnat}, T 12.3")
G["CL3_T"] = grade_cfg(cl3_T(Lnat), Lnat, f"CL3 crossover T {cl3_T(Lnat)}, L_nat {Lnat}")
G["L68_lo"] = grade_cfg(12.3, L68[0], f"L68 low {L68[0]}"); G["L68_hi"] = grade_cfg(12.3, L68[1], f"L68 high {L68[1]}")
G["R1_reference"] = grade_cfg(12.3, 7.31, "uncorrected reference L 7.31")
RES["grades"] = G
pc = G["PRIMARY"]["fails_canonical"]
V = "L DERIVED: THE NATIVE LEVEL PASSES" if not pc else "NATIVE LEVEL FAILS: " + ", ".join(pc)
if L68[0] < 4.17 and L68[1] > 3.64 and not (3.64 <= L68[0] and L68[1] <= 4.17): V += " [CONVERGENCE INCONCLUSIVE]"
RES["verdict"] = V
for k, g in G.items(): Q(f"  {k:13s} T {g['T']} L {g['L']}: canonical {'PASS ALL' if not g['fails_canonical'] else ', '.join(g['fails_canonical'])}")
chk["K2"] = NS["rss_all"]() < 1.0
RES["checks"] = chk
Q(f"\n=== VERDICT: {V}\nchecks {sum(chk.values())}/{len(chk)}")
fn = os.path.join(HERE_NL, f"nl1_native_level_results{TAGN}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
Q(f"results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE_NL, f"nl1_native_level{TAGN}.out"), "w").write("\n".join(OUTN).replace(REPO_NL, "<repo>") + "\n")
sys.exit(0 if all(chk.values()) else 1)
