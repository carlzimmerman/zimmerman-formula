#!/usr/bin/env python3
"""LW1 dwarfs (FROZEN_CRITERIA.md part 3): X51's path, the law plain and with the record's external field. --mutate: a0 x 1.5. Solves cached in cache_dwarfs. kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, sys
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"; sys.dont_write_bytecode = True
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
sys.path.insert(0, os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar")); import d10_solver as S
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; AX = 1.5 if MUT else 1.0; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
# X51's constants for its statistic, Z2's for its solver inputs: each lane's own, as the record ran them
G5, MS5, PC5 = 6.67430e-11, 1.98847e30, 3.0856775814913673e16; GZ, MSZ, PCZ = 6.67430e-11, 1.989e30, 3.0856775814913673e16; KPC = 1e3 * PCZ
A0 = dict(canonical=9.3603e-11 * AX, alt=1.1312e-10 * AX); FEET = ("canonical", "alt"); CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field")
A_H = 3.0 * KPC; GE2 = 2.0592e-10; MHOST = {"MW": 6.0e10, "M31": 1.0e11, "field": 6.0e10}; R12 = 4.0 / 3.0
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-300))
def g_host(R, Mb, a0): gN = GZ * Mb * MSZ / (R + A_H) ** 2; return 0.5 * gN * (1 + np.sqrt(1 + 4 * a0 / gN))
def Mb_hi(a0): gN = GE2 ** 2 / (GE2 + a0); return gN * (8 * KPC + A_H) ** 2 / GZ / MSZ
def hostm(h, ek, a0): return MHOST[h] * {"E_lo": 4.0e10 / 6.0e10, "E_mid": 1.0, "E_hi": Mb_hi(a0) / 6.0e10}[ek]
GR = S.Grid2D(nper=24, Nt=16); CD = os.path.join(HERE, "cache_dwarfs"); os.makedirs(CD, exist_ok=True); CF = os.path.join(CD, f"solves{TAG}.json"); CACHE = json.load(open(CF)) if os.path.exists(CF) else {}; NS = [0]
def logG(y, xe):
    k = f"{y!r}|{xe!r}"
    if k in CACHE: return CACHE[k]
    iso = xe <= 0; sv = S.Solver2D(GR, y, 0.0 if iso else xe, 0.0, isolated=iso); sv.solve(tol=1e-10); rf, gr = sv.field_monopole(); _, vir, wo = S.jeans(rf, gr, []); v = math.log10(6 * wo * R12 / y); CACHE[k] = v; NS[0] += 1
    if NS[0] % 20 == 0: json.dump(CACHE, open(CF + ".tmp", "w")); os.replace(CF + ".tmp", CF)
    return v
ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv")))); arrf = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}; medf = float(np.median(list(arrf.values())))
X1 = list(csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv"))))
Z2T = json.load(open(os.path.join(RB, "Z2_satellite_systematics", "z2_stage_tables.json")))
def rows(f):
    a0 = A0[f]; o = []
    for r in X1:
        if r["footing"] != f or r["cls"] not in CLS: continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None; b = arrf.get(r["name"], medf if (mv is not None and mv > -7.7) else 1.0); sc = float(r["sigma"]) * b; r12 = 4 / 3 * float(r["rh_pc"]) * PC5; Mb = 10 ** float(r["logMstar"]); gobs = 3 * (sc * 1e3) ** 2 / r12; gN = G5 * (Mb / 2) * MS5 / r12 ** 2
        y = GZ * Mb * MSZ / ((float(r["rh_pc"]) * PCZ) ** 2 * a0); dh = float(r["d_host_kpc"]) if r["d_host_kpc"] not in ("", None) else None; host = r["host"]; xe = {e: float(g_host(dh * KPC, hostm(host if host in MHOST else "field", e, a0), a0) / a0) for e in ("E_lo", "E_mid", "E_hi")} if dh else dict(E_lo=0.0, E_mid=0.0, E_hi=0.0)
        ge = xe["E_mid"] * a0; x = xe["E_mid"]; gNe = ge * x / (1 + x); gs = gN + gNe; g2 = float(nu(gs / a0) * gs - (nu(gNe / a0) * gNe if gNe > 0 else 0.0))
        o.append(dict(name=r["name"], cls=r["cls"], host=host, EN=math.log10(gobs / gN), plain=math.log10(gobs / (float(nu(gN / a0)) * gN)), E2=math.log10(gobs / g2), s=float(r["sdMC[Newton]"]), y=y, xe=xe, xe_x1=float(r["x_e_mid"]) if r["x_e_mid"] not in ("", None) else None, dh=dh, lE=float(r["Delta[AQUAL + EFE L*0 (exact MOND + EFE)]"]), lN=float(r["Delta[Newton]"]), lI=float(r["Delta[iso AQUAL L*0]"])))
    return o
def boot(E, s, rng, n=10000):
    N = len(E); ix = rng.integers(0, N, (n, N)); return float(np.median(E)), float(np.std(np.median(E[ix] + s[ix] * rng.standard_normal((n, N)), axis=1)))
def grade(R, key):
    rng = np.random.default_rng(20261026); o = {}
    for c in CLS:
        q = [x for x in R if x["cls"] == c]; m, sd = boot(np.array([x[key] for x in q]), np.array([x["s"] for x in q]), rng); o[c] = dict(N=len(q), median=m, sd=sd, Z=m / sd)
    return o
P(f"LW1 dwarfs {'MUTATE a0 x 1.5' if MUT else ''}; X51's estimator, law nu; kappa = 1/2 FITTED; not theory closed")
RES = dict(mutate=MUT, footings={}); FG = json.load(open(os.path.join(RB, "FG1_final_grade", "fg1_harness_results.json")))["C4"]; k1 = []; k4a = []; k4b = []
for f in FEET:
    R = rows(f)
    for x in R:
        x["E0"] = x["EN"] - logG(x["y"], 0.0); x["E1"] = x["EN"] - logG(x["y"], x["xe"]["E_mid"]); x["E1lo"] = x["EN"] - logG(x["y"], x["xe"]["E_lo"]); x["E1hi"] = x["EN"] - logG(x["y"], x["xe"]["E_hi"])
        if not MUT:
            t = Z2T.get(f"{f}|{x['name']}")
            if t: k4a += [abs(logG(t["y0"], t["xe"]) - t["emb0"][1]), abs(logG(t["y0"], 0.0) - t["iso0"][1])]; k4b.append(abs(t["xe"] - x["xe"]["E_mid"]))
            if x["xe_x1"] is not None: k4b.append(abs(x["xe"]["E_mid"] - x["xe_x1"]))
    json.dump(CACHE, open(CF, "w")); F = RES["footings"][f] = dict(n=len(R), rows={k: grade(R, k) for k in ("plain", "E0", "E1", "E1lo", "E1hi", "E2")}, record_E1_X1={c: float(np.median([x["lE"] for x in R if x["cls"] == c])) for c in CLS})
    if not MUT: k1.append(max(max(abs(F["rows"]["plain"][c]["median"] - FG[f]["dwarfs"][c]["median"]), abs(F["rows"]["plain"][c]["Z"] - FG[f]["dwarfs"][c]["Z"])) for c in CLS))
    P(f"[{f}] N {len(R)}; xe median by class: " + ", ".join(f"{c} {np.median([x['xe']['E_mid'] for x in R if x['cls'] == c]):.3f}" for c in CLS))
    for k, lab in (("plain", "plain nu(g_N), FG1's"), ("E0", "E0 solver, isolated"), ("E1", "E1 PRIMARY solver + EFE"), ("E1lo", "E1 E_lo host"), ("E1hi", "E1 E_hi host"), ("E2", "E2 algebraic QUMOND")):
        P(f"  {lab:26s}: " + "; ".join(f"{c} {F['rows'][k][c]['median']:+.3f} (Z {F['rows'][k][c]['Z']:+.2f})" for c in CLS) + f"; line {'PASS' if all(abs(F['rows'][k][c]['Z']) < 2 for c in CLS) else 'FAIL'}")
    P("  X1's own MC median, AQUAL + EFE: " + ", ".join(f"{c} {v:+.3f}" for c, v in F["record_E1_X1"].items()))
    per = {x["name"]: dict(cls=x["cls"], xe=x["xe"]["E_mid"], plain=x["plain"], E1=x["E1"]) for x in R}; F["per_system"] = per
if not MUT:
    RES["K1"] = max(k1); RES["K4_solver"] = max(k4a) if k4a else None; RES["K4_xe"] = max(k4b); P(f"K1 plain vs FG1 C4 Dw |d| {RES['K1']:.1e}: {'PASS' if RES['K1'] <= 1e-6 else 'FAIL'}"); P(f"K4 solver vs Z2's stage emb0, iso0 max |d| {RES['K4_solver']:.1e}, {len(k4a)} values: {'PASS' if RES['K4_solver'] <= 1e-6 else 'FAIL'}; xe against Z2, X1 max |d| {RES['K4_xe']:.1e}: {'PASS' if RES['K4_xe'] <= 1e-6 else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, f"lw1_dwarfs{TAG}.json"), "w"), indent=1); open(os.path.join(HERE, f"lw1_dwarfs{TAG}.out"), "w").write("\n".join(OUT) + "\n")
