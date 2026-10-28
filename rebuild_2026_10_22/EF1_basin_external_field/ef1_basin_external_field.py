#!/usr/bin/env python3
"""EF1_basin_external_field: LG field dwarfs under X1's exact 2D AQUAL+EFE solver with the external field of the LG basin's total mass.
Frozen criteria d9343614cc (committed alone). Solver: d10_solver read-only with S1's/X1's wrappers (copied verbatim: Grid2D(nper=24, Nt=16),
logG = E-W/E-V Jeans estimators, R12 = 4/3). Residuals: HO3's committed law-branch E (stellar sigma).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I ef1_basin_external_field.py      (EF1_MUTATE=1 twin)
"""
import os, sys, csv, json, math, hashlib, resource
import numpy as np
from scipy import stats

MUT = os.environ.get("EF1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
sys.path.insert(0, os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar"))
import d10_solver as S   # noqa: E402  (read-only)
G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16     # X1's constants
KPC = 1e3 * PC; R12 = 4.0 / 3.0
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt")
SEED, P0, PMIN = 20261027, 0.0455, 0.01
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
P(f"EF1_basin_external_field (criteria d9343614cc){'  [MUTATE: M_basin x100]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")

GR = S.Grid2D(nper=24, Nt=16)
def logG(y, xe, Lam=0.0):
    iso = xe <= 0
    sv = S.Solver2D(GR, y, 0.0 if iso else xe, Lam, isolated=iso)
    U, res, it = sv.solve(tol=1e-10)
    rf, gr = sv.field_monopole(); _, vir, wo = S.jeans(rf, gr, [])
    return math.log10(6 * wo * R12 / y), math.log10(6 * vir * R12 / y)

BS1 = json.load(open(os.path.join(REB, "BS1_basin_switch", "bs1_basin_switch_results.json")))
lgM = BS1["LG"]["basin"]["lgM"]; FR = BS1["LG"]["field_R_kpc"]
Mbasin = 10 ** lgM * (100 if MUT else 1)
X1 = [r for r in csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))) if r["cls"] == "LG field"]
HO3 = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(REB, "HO3_dwarf_individuals_heldout", "ho3_dwarf_individuals_per_object.csv")))}
TB = {f: json.load(open(os.path.join(REB, "X1_hosted_recount", f"x1_stage_tables_{f}.json")))["tables"] for f in FEET}
FD1 = json.load(open(os.path.join(REB, "FD1_field_dwarf_audit", "fd1_field_dwarf_audit_results.json")))

def s2_threshold(N):
    rng = np.random.default_rng(SEED); qs = []
    for _ in range(4): qs.append(np.median(np.abs(rng.standard_normal((50000, N))), axis=1))
    return float(np.percentile(np.concatenate(qs), 99))
def rules(Z):
    Z = np.asarray(Z, float); N = len(Z); a = np.abs(Z); k = int((a >= 2).sum()); p1 = float(stats.binom.sf(k - 1, N, P0))
    med = float(np.median(a)); zmax = float(a.max()); p2 = float(2 * stats.norm.sf(zmax)); p3 = float(-math.expm1(N * math.log1p(-p2))) if p2 < 1 else 1.0
    return dict(k=k, S1_p=p1, med=med, t2=s2_threshold(N), zmax=zmax, S3_p=p3, ok=dict(S1=p1 >= PMIN, S2=med <= s2_threshold(N), S3=p3 >= PMIN))

checks = {}; RES = dict(criteria="d9343614cc", mutate=MUT, lgM_basin=lgM, footings={})
# K1: isolated deep-limit control (X1 C3a)
y = 1e-3; ex = (2.0 / 9.0) * math.sqrt(y)
d = S.Solver2D(GR, y, 0.0, 0.0, isolated=True); d.solve(tol=1e-10); rf, gr = d.field_monopole(); _, vir, wo = S.jeans(rf, gr, [])
checks["K1"] = abs(math.log10(vir / ex)) <= 0.005 if vir > 0 else False                       # A1: ex is sigma^2 (X1 C3a)
P(f"  K1 isolated deep-limit (sigma^4 = 4/81 G M a0) at y 1e-3: solver sigma^2 {vir:.5f} vs {ex:.5f}: {'PASS' if checks['K1'] else 'FAIL'}")
k0 = True; k3 = True
for f in FEET:
    a0 = A0[f]; rows = []
    P(f"\n=== [{f}] a0 {a0:.4e}; LG basin log M {lgM:.3f}")
    for r in X1:
        if r["footing"] != f: continue
        nm = r["name"]; t = TB[f][nm]; y0 = t["y0"]
        Rk = FR.get(nm)
        xe = (G * Mbasin * MSUN / (Rk * KPC) ** 2 / a0) if Rk else t["xe"]["E_mid"]
        k3 &= xe < 0.1
        li = logG(y0, 0.0)[0]; le = logG(y0, xe)[0]; lx = logG(y0, t["xe"]["E_mid"])[0]
        if nm in ("IC 1613", "WLM", "Leo T"):
            ref = t["emb0"][1][0] - t["iso0"][1][0]; dd = abs((lx - li) - ref); k0 &= dd <= 0.002
            P(f"   K0 {nm}: solver (emb - iso) at X1 x_e {lx - li:+.4f} vs X1 tables {ref:+.4f} (|d| {dd:.4f})")
        E0 = float(HO3[(f, nm)]["E"]); s = float(HO3[(f, nm)]["s"]); E = E0 - (le - li)
        # FD1 baryon variant: y0 scaled by M_b(FD1 M+G)/M* (same r_h)
        fdr = [x for x in FD1["footings"][f]["runs"]["M+G"]["rows"] if x["name"] == nm][0]
        y1 = y0 * 10 ** (fdr["logMb"] - float(r["logMstar"]))
        lv1 = logG(y1, xe)[0] - logG(y1, 0.0)[0]
        rows.append(dict(name=nm, R_kpc=Rk, xe_basin=xe, xe_X1=t["xe"]["E_mid"], y0=y0, dEF=le - li, dEF_X1=lx - li, E_HO3=E0, E_EF=E, s=s, Z=E / s, dEF_FD1baryons=lv1))
        P(f"   {nm:16s} R {Rk if Rk else float('nan'):7.1f} kpc  x_e {xe:.4f} (X1 {t['xe']['E_mid']:.4f})  y0 {y0:.3f}  EFE shift {le - li:+.4f}  E {E0:+.3f} -> {E:+.3f}  Z {E / s:+.2f}  [FD1-baryon shift {lv1:+.4f}]")
    R = rules([x["Z"] for x in rows]); ic = [x for x in rows if x["name"] == "IC 1613"][0]
    v = "BASIN FIELD RESOLVES IC 1613" if abs(ic["Z"]) < 2 else ("BASIN FIELD REDUCES IC 1613" if abs(ic["Z"]) <= 0.5 * 6.75 else "BASIN FIELD DOES NOT HELP")
    P(f"  field rules: S1 k {R['k']} p {R['S1_p']:.3f}; S2 {R['med']:.2f}/{R['t2']:.2f}; S3 max {R['zmax']:.2f} p {R['S3_p']:.2e} -> {R['ok']}")
    P(f"  VERDICT [{f}]: {v} (IC 1613 Z {ic['Z']:+.2f})")
    RES["footings"][f] = dict(rows=rows, rules=R, verdict=v)
checks["K0"] = bool(k0); checks["K3"] = bool(k3)
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; checks["K2"] = peak < 1.0
RES["checks"] = checks
P(f"\n  K0 {'PASS' if k0 else 'FAIL'}; K3 x_e < 0.1 for all {'PASS' if k3 else 'FAIL'}; K2 peak RSS {peak:.2f} GB")
fn = os.path.join(HERE, f"ef1_basin_external_field_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(checks.values())}/{len(checks)}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"ef1_basin_external_field{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(checks.values()) else 1)
