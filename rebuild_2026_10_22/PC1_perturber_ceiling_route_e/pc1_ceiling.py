#!/usr/bin/env python3
"""PC1_perturber_ceiling_route_e: maximum enclosed mass of a0-floor Burkert halos vs lens perturbers and LG dwarfs.

Frozen criteria: FROZEN_CRITERIA.md (ad466e9c38). Reads X1's per-system CSV, CFG257's binary table, EM1's relation, F3's h, X41's
Sigma_coll, CE1's eta (read-only). One thread, seconds.

    python3 pc1_ceiling.py            -> pc1_ceiling.out, pc1_results.json
    python3 pc1_ceiling.py --mutate   -> Sigma_core = Sigma_a0 / 10, separate outputs; exit 1 if the mutation does not bite
"""
import csv, json, math, os, sys
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
TAG = "_MUTATE" if MUTATE else ""; OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
G, MSUN, PC, MPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16, 3.0856775814913673e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt")
SIG = {f: A0[f] / (2 * math.pi * G) * (0.1 if MUTATE else 1.0) for f in FEET}          # kg/m^2
SIGPC = {f: SIG[f] * PC ** 2 / MSUN for f in FEET}                                     # Msun/pc^2
CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field")
REP = ("indiv:Crater II", "indiv:Antlia II", "indiv:Sagittarius")
P(f"PC1_perturber_ceiling_route_e  {'MUTATE (Sigma / 10)' if MUTATE else 'normal run'}  frozen ad466e9c38")
P(f"kappa = 1/2 FITTED; route E, floor Burkert halos, Sigma = {SIGPC['canonical']:.1f} / {SIGPC['alt']:.1f} Msun/pc^2; not theory closed")

def B(x): x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def rho_hat(s): return 1.0 / ((1 + s) * (1 + s * s))                                    # rho / rho0, s = r/r0
def m2d_hat(X):
    """Projected mass inside R = X r0, in units of rho0 r0^3, line of sight to 100 r0 (3D profile uncut)."""
    def col(u):
        zmax = math.sqrt(max(100.0 ** 2 - u * u, 0.0))
        return 2 * quad(lambda z: rho_hat(math.hypot(u, z)), 0, zmax, limit=200)[0]
    return quad(lambda u: 2 * math.pi * u * col(u), 0, X, limit=200)[0]
# Ceilings are c * Sigma * r^2: c = max over x = r/r0 of pi B(x)/x^2 (3D) or m2d_hat(x)/x^2 (2D); both independent of Sigma and r.
pk3 = minimize_scalar(lambda lx: -math.pi * float(B(math.exp(lx))) / math.exp(2 * lx), bounds=(-3, 4), method="bounded", options={"xatol": 1e-8})
C3, X3 = -pk3.fun, math.exp(pk3.x)
pk2 = minimize_scalar(lambda lx: -m2d_hat(math.exp(lx)) / math.exp(2 * lx), bounds=(-3, 4), method="bounded", options={"xatol": 1e-5})
C2, X2 = -pk2.fun, math.exp(pk2.x)
P(f"Ceiling: M3D(<r) <= {C3:.4f} Sigma r^2 at r/r0 = {X3:.3f}; M2D(<R) <= {C2:.4f} Sigma R^2 at R/r0 = {X2:.3f}")
P(f"Equivalent g_max = {C3 / (2 * math.pi):.4f} a0 (3D){'  [mutated Sigma: /10]' if MUTATE else ''}")
def ceil3(r_pc, f): return C3 * SIGPC[f] * r_pc ** 2
def ceil2(r_pc, f): return C2 * SIGPC[f] * r_pc ** 2

checks = []
# K1 direct grid; K2 small-r limit
xg = np.logspace(-3, 4, 200001); c3g = float(np.max(math.pi * B(xg) / xg ** 2)); k1 = abs(c3g / C3 - 1) < 1e-3
checks.append(("K1 grid ceiling", k1))
xs = 1e-3; k2 = abs(float(B(xs)) * math.pi / ((4 / 3) * math.pi * xs ** 3) - 1) < 1e-3
checks.append(("K2 small-r limit", k2))

EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
a_, b_ = EM1J["rows"]["A_c2b_refit"]["R1"]["a"], EM1J["rows"]["A_c2b_refit"]["R1"]["b"]; h = F3["A_c2b_refit"]["params"]["h"]
RHOC = 3 * (100 * h * 1e3 / MPC) ** 2 / (8 * math.pi * G)
X41 = json.load(open(os.path.join(REB, "X41_collapse_floor_sigma", "x41_collapse_floor_results.json")))
sc11 = X41["sigma_coll_table"]["1e11"][0]
P(f"Floor check: Sigma_coll(1e11) = {sc11:.2f}; x eta 25.94 = {sc11 * 25.94:.1f} Msun/pc^2 vs floor {SIGPC['canonical']:.1f} / {SIGPC['alt']:.1f}")
def solve_r0(Mtot, Rout, Sig):
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    lpk = float(pk.x)
    if lm(lpk) < math.log(Mtot): return math.exp(lpk)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), lpk, xtol=1e-14))
def R200_of(M_msun): return (3 * M_msun * MSUN / (4 * math.pi * 200 * RHOC)) ** (1 / 3)
def M200_of_r0(r0_pc, f):
    """M200 (Msun) whose compact root is r0, by direct inversion of solve_r0's relation."""
    r0 = r0_pc * PC
    gg = lambda lm: math.pi * SIG[f] * r0 ** 2 * float(B(R200_of(math.exp(lm)) / r0)) / MSUN - math.exp(lm)
    return math.exp(brentq(gg, math.log(1e2), math.log(1e15)))
for f in FEET:
    M2 = 1e12; R2 = R200_of(M2); r0 = solve_r0(M2 * MSUN, R2, SIG[f]); Mchk = math.pi * SIG[f] * r0 ** 2 * float(B(R2 / r0)) / MSUN
    checks.append((f"K3[{f}]", abs(Mchk / M2 - 1) < 1e-6))

# Section 2: perturbers (CFG666's table)
PERT = [("J0946 dark <0.3 kpc", "3D", 300., 5.8e8, 0.3e8, 8 * 5.0e6), ("J0946 dark <0.6 kpc", "3D", 600., 1.1e9, 0.05e9, 8 * 5.0e6),
        ("B1938 A <0.6 kpc", "3D", 600., 1.13e8, 0.06e8, 8 * 5.4e7), ("B1938 V 80 pc", "2D", 80., 1.13e6, 0.04e6, 0.0)]
RES = dict(frozen="ad466e9c38", mutate=MUTATE, C3=C3, X3=X3, C2=C2, X2=X2, g_max_a0=C3 / (2 * math.pi), footings={})
def cls(R): return "ALLOWED" if R <= 1 else ("MARGINAL" if R <= 2 else "EXCEEDS")
for f in FEET:
    FR = RES["footings"][f] = dict(perturbers={}, dwarfs={})
    P(f"\n=== [{f}] perturbers")
    for name, st, r, M, s, Mb in PERT:
        C = ceil3(r, f) if st == "3D" else ceil2(r, f); x = X3 if st == "3D" else X2; r0 = r / x
        R = (M - 2 * s - Mb) / C; R0 = (M - 2 * s) / C
        try: M200 = M200_of_r0(r0, f)
        except ValueError: M200 = float("nan")
        c = cls(R); FR["perturbers"][name] = dict(ceiling=C, R=R, R_dark=R0, cls=c, r0_pc=r0, M200_at_peak=M200)
        P(f"  {name:22s} {st} M_obs {M:.3g} ceiling {C:.3g}  R {R:7.2f}  R(dark) {R0:7.2f}  {c:8s} peak r0 {r0:6.1f} pc, M200 there {M200:.2e}")
    # Luminous J0946
    C1 = ceil2(1000., f); lo, hi = 1.0e8, 8.3e8 + C1; ov = hi >= 10 ** 8.1 and lo <= 10 ** 10.0
    Qs = {"M_b+C over M_b at 1 kpc, M_b low": (1.0e8 + C1) / 1.0e8, "same, M_b high": (8.3e8 + C1) / 8.3e8}
    FR["luminous_J0946"] = dict(ceiling_1kpc=C1, band=[lo, hi], consistent=ov, Q=Qs)
    P(f"  J0946 luminous: 2D ceiling(<1 kpc) {C1:.3g}; band [{lo:.3g}, {hi:.3g}] vs 95% [{10**8.1:.3g}, {10**10.0:.3g}]: {'CONSISTENT' if ov else 'INCONSISTENT'}; Q {Qs}")

# Section 3: dwarfs, X49's rows conventions
ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}; med_free = float(np.median(list(arr_free.values())))
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
def rows(f, classes):
    out = []
    for r in X1:
        if r["footing"] != f or r["cls"] not in classes: continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        b = arr_free.get(r["name"], med_free if (mv is not None and mv > -7.7) else 1.0)
        sc = float(r["sigma"]) * b; r12 = 4 / 3 * float(r["rh_pc"]) * PC; Mb = 10 ** float(r["logMstar"])
        gobs = 3 * (sc * 1e3) ** 2 / r12; gN = G * (Mb / 2) * MSUN / r12 ** 2
        M200 = 10 ** (a_ + b_ * (math.log10(Mb) - 10)); R200 = R200_of(M200)
        r0 = solve_r0(M200 * MSUN, R200, SIG[f]); Mh = math.pi * SIG[f] * r0 ** 2 * float(B(min(r12, R200) / r0))
        gX49 = gN + G * Mh / r12 ** 2
        Cmax = C3 * SIG[f] * r12 ** 2; gC = gN + G * Cmax / r12 ** 2
        out.append(dict(name=r["name"], cls=r["cls"], E49=math.log10(gobs / gX49), EC=math.log10(gobs / gC), s=float(r["sdMC[Newton]"]),
                        gobs_a0=gobs / A0[f], M200_x49=M200, need_halo=max(gobs - gN, 0.0), r12=r12))
    return out
def boot(E, s, rng, n=10000):
    N = len(E); ix = rng.integers(0, N, (n, N)); return float(np.median(E)), float(np.std(np.median(E[ix] + s[ix] * rng.standard_normal((n, N)), axis=1)))
K4_REF = {"canonical": 0.476, "alt": 0.459}
labels = {}
for f in FEET:
    FR = RES["footings"][f]; rng = np.random.default_rng(20261026); R = rows(f, CLS + REP)
    P(f"\n=== [{f}] dwarfs, E_C = log10(g_obs / (g_N + g_ceiling))")
    for c in CLS:
        q = [x for x in R if x["cls"] == c]; E = np.array([x["EC"] for x in q]); s = np.array([x["s"] for x in q])
        m, sd = boot(E, s, rng); z = m / sd; above = [x["name"] for x in q if x["EC"] > 2 * x["s"]]
        FR["dwarfs"][c] = dict(N=len(q), median_EC=m, sd=sd, Z_C=z, n_above_2s=len(above), above=above, median_E49=float(np.median([x["E49"] for x in q])))
        P(f"  {c:15s} N {len(q):2d}: E_C {m:+.3f} +- {sd:.3f} (Z_C {z:+.2f}); above ceiling by >2s: {len(above)}; X49 E median {FR['dwarfs'][c]['median_E49']:+.3f}")
    if not MUTATE:
        checks.append((f"K4[{f}]", abs(FR["dwarfs"]["MW ultra-faint"]["median_E49"] - K4_REF[f]) < 0.005))
    for c in REP:
        for x in [x for x in R if x["cls"] == c]:
            P(f"  reported {x['name']:18s} E_C {x['EC']:+.3f} +- {x['s']:.3f}  g_obs {x['gobs_a0']:.3f} a0")
    uf = FR["dwarfs"]["MW ultra-faint"]; zc = uf["Z_C"]
    labels[f] = "NO M200 RESCUES" if zc > 2 else ("CEILING ADMITS" if abs(zc) < 2 else "BELOW CEILING")
    # Follow-up frozen for the non-rescue labels: the M200 each ultra-faint would need, vs X49's extrapolated M200.
    need = []
    for x in [y for y in R if y["cls"] == "MW ultra-faint"]:
        Mneed = x["need_halo"] * x["r12"] ** 2 / G
        Cm = C3 * SIG[f] * x["r12"] ** 2
        if Mneed >= Cm: need.append(dict(name=x["name"], reachable=False)); continue
        if Mneed <= 0: need.append(dict(name=x["name"], reachable=True, M200=0.0, ratio=0.0)); continue
        # compact branch (r12 > peak x means r0 small); scan r0 outward from the compact root for the lowest M200 that encloses Mneed
        lr = np.linspace(math.log(x["r12"] * 1e-4), math.log(x["r12"] / X3), 4000)
        Mi = math.pi * SIG[f] * np.exp(2 * lr) * B(x["r12"] / np.exp(lr))
        i = int(np.argmax(Mi >= Mneed)); r0_pc = math.exp(lr[i]) / PC
        try: m = M200_of_r0(r0_pc, f)
        except ValueError: m = float("nan")
        need.append(dict(name=x["name"], reachable=True, M200=m, ratio=m / x["M200_x49"]))
    FR["ufd_needed_M200"] = need
    ok = [n for n in need if n["reachable"] and n["M200"] > 0 and n["M200"] == n["M200"]]
    P(f"  LABEL [{f}]: {labels[f]} (Z_C {zc:+.2f}); reachable {sum(n['reachable'] for n in need)}/{len(need)}; median M200 needed {np.median([n['M200'] for n in ok]):.2e}, median over X49's {np.median([n['ratio'] for n in ok]):.1f}x")
RES["labels"] = labels

P("\nChecks: " + ", ".join(f"{n} {'PASS' if v else 'FAIL'}" for n, v in checks))
if MUTATE:
    base = json.load(open(os.path.join(HERE, "pc1_results.json")))
    bite = all(abs(base["footings"][f]["perturbers"]["J0946 dark <0.3 kpc"]["ceiling"] / RES["footings"][f]["perturbers"]["J0946 dark <0.3 kpc"]["ceiling"] - 10) < 1e-6
               and RES["footings"][f]["dwarfs"]["MW ultra-faint"]["Z_C"] > base["footings"][f]["dwarfs"]["MW ultra-faint"]["Z_C"] for f in FEET)
    P(f"MUTATE bite (ceiling /10 and Z_C up, both footings): {bite}")
    RES["mutate_bite"] = bite
json.dump(RES, open(os.path.join(HERE, f"pc1_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"pc1_ceiling{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUTATE: sys.exit(0 if RES["mutate_bite"] else 1)
sys.exit(0 if all(v for _, v in checks) else 1)
