#!/usr/bin/env python3
"""X49_dwarfs_route_e_floor: LG dwarfs under route E with a0-floor Burkert halos (X43's rule below the crossover).

Frozen criteria: FROZEN_CRITERIA.md (fa308d2c47). Reads X1's per-system CSV, CFG257's binary table, EM1's committed relation,
F3's background h and X41's Sigma_coll table (read-only). One thread, seconds.

    python3 x49_dwarfs.py            -> .out, _results.json
    python3 x49_dwarfs.py --mutate   -> Sigma_core = Sigma_a0 / 10 (K1 must fail)
"""
import csv, json, math, os, sys, time, resource
import numpy as np
from scipy.optimize import brentq, minimize_scalar

T0 = time.time(); MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
TAG = "_MUTATE" if MUTATE else ""; OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
G, MSUN, PC, MPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16, 3.0856775814913673e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt")
SIG = {f: A0[f] / (2 * math.pi * G) * (0.1 if MUTATE else 1.0) for f in FEET}
SIGPC = {f: SIG[f] * PC ** 2 / MSUN for f in FEET}
CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field")
REP = ("indiv:Crater II", "indiv:Antlia II", "indiv:Canes Venatici I", "indiv:Sagittarius", "M31 dE")
K0_REF = {"canonical": {"MW ultra-faint": 0.596, "bright M31": 0.220, "M31 others": 0.777}, "alt": {"MW ultra-faint": 0.539, "bright M31": 0.185, "M31 others": 0.697}}
P(f"X49_dwarfs_route_e_floor  {'MUTATE (Sigma_core = Sigma_a0 / 10)' if MUTATE else 'normal run'}")
P(f"kappa = 1/2 FITTED; route E, a0-floor Burkert halos (rho0 r0 = {SIGPC['canonical']:.1f} / {SIGPC['alt']:.1f} Msun/pc^2); not theory closed")

def B(x): x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
SAT = {"n": 0}
def solve_r0(Mtot, Rout, Sig):
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    lpk = float(pk.x)
    if lm(lpk) < math.log(Mtot): SAT["n"] += 1; return math.exp(lpk)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), lpk, xtol=1e-14))
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
a_, b_ = EM1J["rows"]["A_c2b_refit"]["R1"]["a"], EM1J["rows"]["A_c2b_refit"]["R1"]["b"]; h = F3["A_c2b_refit"]["params"]["h"]
RHOC = 3 * (100 * h * 1e3 / MPC) ** 2 / (8 * math.pi * G)
X41 = json.load(open(os.path.join(REB, "X41_collapse_floor_sigma", "x41_collapse_floor_results.json")))
sc11 = X41["sigma_coll_table"]["1e11"][0]
P(f"Sigma_coll(1e11) = {sc11:.2f} Msun/pc^2 (X41; monotone rising in M): every dwarf (M200 << 1e11) sits on the floor -> c_f-independent")

def halo(Mb_msun, fair=False):
    M200 = (6.364 * Mb_msun if fair else 10 ** (a_ + b_ * (math.log10(Mb_msun) - 10))) * MSUN
    R200 = (3 * M200 / (4 * math.pi * 200 * RHOC)) ** (1 / 3)
    return M200, R200
checks = []
# K1
for f in FEET:
    Sig0 = A0[f] / (2 * math.pi * G)
    M2, R2 = halo(10 ** 10.9)                                                  # gives M200 ~ 1e12
    M2 = 1e12 * MSUN; R2 = (3 * M2 / (4 * math.pi * 200 * RHOC)) ** (1 / 3)
    r0 = solve_r0(M2, R2, SIG[f]); Mchk = math.pi * SIG[f] * r0 ** 2 * float(B(R2 / r0))
    k1 = abs(SIG[f] / Sig0 - 1) < 1e-10 and abs(Mchk / M2 - 1) < 1e-8
    checks.append((f"K1[{f}]", k1))
P(f"K1 Sigma_core = a0/(2 pi G) and M(<R200) = M200 at 1e12: {all(c[1] for c in checks)}")
SAT["n"] = 0

ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}; med_free = float(np.median(list(arr_free.values())))
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
def rows(f, classes, fair=False):
    out = []
    for r in X1:
        if r["footing"] != f or r["cls"] not in classes: continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        b = arr_free.get(r["name"], med_free if (mv is not None and mv > -7.7) else 1.0)
        sc = float(r["sigma"]) * b; r12 = 4 / 3 * float(r["rh_pc"]) * PC; Mb = 10 ** float(r["logMstar"])
        gobs = 3 * (sc * 1e3) ** 2 / r12; gN = G * (Mb / 2) * MSUN / r12 ** 2
        M200, R200 = halo(Mb, fair); r0 = solve_r0(M200, R200, SIG[f]); Mh = math.pi * SIG[f] * r0 ** 2 * float(B(min(r12, R200) / r0))
        gp = gN + G * Mh / r12 ** 2
        out.append(dict(name=r["name"], cls=r["cls"], lm=float(r["logMstar"]), E=math.log10(gobs / gp), EN=math.log10(gobs / gN),
                        DN=float(r["Delta[Newton]"]), s=float(r["sdMC[Newton]"]), Eiso=float(r["Delta[iso AQUAL L*0]"]),
                        r0_kpc=r0 / (1e3 * PC), M200=M200 / MSUN))
    return out
def boot(E, s, rng, n=10000):
    N = len(E); ix = rng.integers(0, N, (n, N)); return float(np.median(E)), float(np.std(np.median(E[ix] + s[ix] * rng.standard_normal((n, N)), axis=1)))
def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float); ry = np.argsort(np.argsort(y)).astype(float); rx -= rx.mean(); ry -= ry.mean()
    return float((rx * ry).sum() / math.sqrt((rx ** 2).sum() * (ry ** 2).sum()))
RES = dict(frozen="fa308d2c47", mutate=MUTATE, footings={})
for f in FEET:
    rng = np.random.default_rng(20261026); R = rows(f, CLS); FR = RES["footings"][f] = {"classes": {}}
    k0 = all(abs(float(np.median([q["Eiso"] for q in R if q["cls"] == c])) - v) < 0.005 for c, v in K0_REF[f].items())
    k2 = float(np.median([abs(q["EN"] - q["DN"]) for q in R])) < 0.03
    checks += [(f"K0[{f}]", k0), (f"K2[{f}]", k2)]
    P(f"\n=== [{f}]  K0 X24 medians {'PASS' if k0 else 'FAIL'}; K2 no-halo vs X1 Newton {'PASS' if k2 else 'FAIL'}")
    fails = []
    for c in CLS:
        q = [x for x in R if x["cls"] == c]; E = np.array([x["E"] for x in q]); s = np.array([x["s"] for x in q])
        m, sd = boot(E, s, rng); z = m / sd; ok = abs(z) < 2
        if not ok: fails.append(f"{c} ({'UNDER' if m > 0 else 'OVER'}, Z {z:+.2f})")
        FR["classes"][c] = dict(N=len(q), median=m, sd=sd, Z=z, reproduced=ok, r0_kpc=float(np.median([x["r0_kpc"] for x in q])),
                                M200=float(np.median([x["M200"] for x in q])))
        P(f"  {c:15s} N {len(q):2d}: E {m:+.3f} +- {sd:.3f} (Z {z:+.2f}) {'REPRODUCED' if ok else 'FAIL'}; median M200 {FR['classes'][c]['M200']:.2e}, r0 {FR['classes'][c]['r0_kpc']:.2f} kpc")
    rho = spearman(np.array([x["lm"] for x in R]), np.array([x["E"] for x in R]))
    Rf = rows(f, CLS, fair=True); fv = {}
    for c in CLS:
        Ef = np.array([x["E"] for x in Rf if x["cls"] == c]); sf = np.array([x["s"] for x in Rf if x["cls"] == c]); m, sd = boot(Ef, sf, rng); fv[c] = dict(median=m, Z=m / sd)
    P(f"  reported: Spearman(E, log M*) over five classes {rho:+.3f} (X24 iso: -0.63); fair-share variant: " + "; ".join(f"{c} {v['median']:+.2f} (Z {v['Z']:+.1f})" for c, v in fv.items()))
    rep = rows(f, REP)
    P("  reported individuals: " + "; ".join(f"{x['name']} E {x['E']:+.2f}" for x in rep))
    v = "FLOOR HALOS FIT THE DWARFS" if not fails else "FAIL: " + ", ".join(fails)
    FR.update(verdict=v, spearman_E_logMstar=rho, fair_share=fv, individuals={x["name"]: x["E"] for x in rep}, saturated=SAT["n"])
    P(f"  saturated solves {SAT['n']}; VERDICT [{f}]: {v}"); SAT["n"] = 0
V = {f: RES["footings"][f]["verdict"].split(":")[0] for f in FEET}
RES["verdict"] = RES["footings"]["canonical"]["verdict"] if V["canonical"] == V["alt"] else f"UNDECIDED {V}"
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6); checks.append(("K3", rss < 1.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.1f} s; peak RSS {rss:.2f} GB")
open(os.path.join(HERE, f"x49_dwarfs{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x49_dwarfs_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
