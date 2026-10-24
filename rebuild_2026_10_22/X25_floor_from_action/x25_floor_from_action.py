#!/usr/bin/env python3
"""X25_floor_from_action: is X24's velocity floor c0 the v3s held medium's own sound speed c_s^2 = 2 pi G rho0 L*^2?

Frozen criteria: FROZEN_CRITERIA.md (230c922864). Reads X1's per-system CSV, X24's JSON and CFG257's binary table,
read-only. One thread, seconds.

    python3 x25_floor_from_action.py            -> .out, _results.json
    python3 x25_floor_from_action.py --mutate   -> c_s^2 -> 2 gamma_L rho0 (K1 must fail), _MUTATE outputs
"""
import csv, json, math, os, resource, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)

G, PC, MSUN = 6.674e-11, 3.0857e16, 1.989e30
FOOTS = ("canonical", "alt")
LFLOOR = {"canonical": 21.68, "alt": 22.85}
H = ("MW ultra-faint", "bright M31", "M31 others")
GRADED = H + ("MW classical",)
K0_REF = {"canonical": (0.596, 0.220, 0.777), "alt": (0.539, 0.185, 0.697)}
MULT = 2.0 if MUTATE else 1.0
X24 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "X24_dwarf_velocity_floor", "x24_dwarf_velocity_floor_results.json")))
ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping",
                                            "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values())))
X1 = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount", "x1_per_system.csv"))))

def cs_kms(rho_msun_pc3, Lpc):
    return math.sqrt(MULT * 2 * math.pi * G * rho_msun_pc3 * MSUN / PC ** 3) * Lpc * PC / 1e3

def load(foot):                       # X24's loader + this lane's densities
    out = []
    for r in X1:
        if r["footing"] != foot or r["cls"] not in GRADED:
            continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        b = arr_free.get(r["name"], med_free if (mv is not None and mv > -7.7) else 1.0)
        E = float(r["Delta[iso AQUAL L*0]"]); sc = float(r["sigma"]) * b; siso = sc * 10 ** (-E / 2)
        r12 = 4.0 / 3.0 * float(r["rh_pc"]) * PC
        gN = G * (10 ** float(r["logMstar"]) / 2) * MSUN / r12 ** 2
        giso = 3 * (siso * 1e3) ** 2 / r12
        rho_mean = 3 * (giso - gN) / (4 * math.pi * G * r12) / MSUN * PC ** 3
        rho_loc = giso / (4 * math.pi * G * r12) / MSUN * PC ** 3
        dv = {L: float(r["Delta[AQUAL + EFE L*0 (exact MOND + EFE)]"]) - float(r[f"Delta[v3 L*{L}]"]) for L in ("floor", "24", "90")}
        out.append(dict(name=r["name"], cls=r["cls"], E=E, rho=rho_mean, rho_loc=rho_loc, dv=dv))
    return out

P(f"X25_floor_from_action  {'MUTATE run (c_s^2 -> 2 gamma_L rho0)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; no new constant (L* is the action's); not theory closed")
RES = dict(frozen="230c922864", mutate=MUTATE, footings={}); checks = []

# K1: ZT11 at R0
zt = {("canonical", 24): (0.059, 0.96), ("canonical", 90): (0.059, 3.6), ("alt", 24): (0.068, 1.0), ("alt", 90): (0.068, 3.8)}
k1 = all(abs(cs_kms(rho, L) / v - 1) < 0.03 for (f, L), (rho, v) in zt.items())
P("K1 c_s vs ZT11 at R0: " + ", ".join(f"{f} {L} pc {cs_kms(rho, L):.2f} (ZT11 {v})" for (f, L), (rho, v) in zt.items())
  + f": {'PASS' if k1 else 'FAIL'}"); checks.append(("K1", k1))
# K2: deep-MOND point mass, local = mean/3
gM, r = 1.0, 2.0
g = lambda rr: math.sqrt(gM) / rr                            # deep MOND, g ~ 1/r
loc = (1 / (4 * math.pi)) * (1 / r ** 2) * (2 * r * g(r) + r ** 2 * (-g(r) / r))
mean = 3 * g(r) / (4 * math.pi * r)
k2 = abs(loc / mean - 1 / 3) < 1e-12
P(f"K2 deep-MOND local/mean phantom density = {loc / mean:.15f} (1/3): {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))

for f in FOOTS:
    R = load(f); FR = RES["footings"][f] = {}
    c0 = X24["footings"][f]["B"]["c0"]; lo, hi = X24["footings"][f]["B"]["c0_lo"], X24["footings"][f]["B"]["c0_hi"]
    meds = [float(np.median([q["E"] for q in R if q["cls"] == c])) for c in H]
    k0 = all(abs(m - x) <= 0.005 for m, x in zip(meds, K0_REF[f])) and abs(c0 - (4.59 if f == "canonical" else 4.05)) < 0.01
    P(f"\n=== [{f}]  X24 field c0 {c0:.2f} [{lo:.2f}, {hi:.2f}] km/s; K0 {'PASS' if k0 else 'FAIL'}")
    checks.append((f"K0[{f}]", k0))
    Ls = {"floor": LFLOOR[f], "24": 24.0, "90": 90.0}
    FR["c0_field"] = [c0, lo, hi]; FR["classes"] = {}
    d1 = {}
    for Lk, L in Ls.items():
        ok = True
        for c in GRADED:
            rc = [q for q in R if q["cls"] == c]
            mc = float(np.median([cs_kms(q["rho"], L) for q in rc]))
            FR["classes"].setdefault(c, {})[f"cs_{Lk}"] = mc
            ok = ok and lo <= mc <= hi
        d1[Lk] = ok
    for c in GRADED:
        rc = [q for q in R if q["cls"] == c]
        rho_m = float(np.median([q["rho"] for q in rc])); rho_l = float(np.median([q["rho_loc"] for q in rc]))
        Lneed = c0 / cs_kms(rho_m, 1.0)
        dvs = {Lk: float(np.median([q["dv"][Lk] for q in rc])) for Lk in Ls}
        FR["classes"][c].update(rho_mean=rho_m, rho_local=rho_l, L_need_pc=Lneed, dE_v3=dvs,
                                cs_local_24=float(np.median([cs_kms(q["rho_loc"], 24.0) for q in rc])))
        P(f"  {c:15s} rho_ph {rho_m:.3g} Msun/pc3 (local {rho_l:.3g}); c_s {FR['classes'][c]['cs_floor']:.2f} / "
          f"{FR['classes'][c]['cs_24']:.2f} / {FR['classes'][c]['cs_90']:.2f} km/s at L* floor/24/90; L*,need {Lneed:.0f} pc; "
          f"dE_v3 (L* on - off) {dvs['floor']:+.3f} / {dvs['24']:+.3f} / {dvs['90']:+.3f}")
    allR = [q for q in R]
    d2med = {Lk: float(np.median([q["dv"][Lk] for q in allR])) for Lk in Ls}
    sign = "RIGHT (floor-like)" if d2med["24"] > 0 else "WRONG (screening)"
    ufd = float(np.median([cs_kms(q["rho"], 24.0) for q in R if q["cls"] == "MW ultra-faint"]))
    oth = float(np.median([cs_kms(q["rho"], 24.0) for q in R if q["cls"] != "MW ultra-faint"]))
    FR.update(D1=d1, D2_median_dE=d2med, D2_sign=sign, D3_ratio_ufd_over_others=ufd / oth)
    P(f"  D1 (all classes inside c0 interval): " + ", ".join(f"L* {k}: {'pass' if v else 'fail'}" for k, v in d1.items()))
    P(f"  D2 median dE_v3 over {len(allR)} systems: floor {d2med['floor']:+.3f}, 24 {d2med['24']:+.3f}, 90 {d2med['90']:+.3f} dex -> {sign}")
    P(f"  D3 c_s(UFD)/c_s(others) at 24 pc = {ufd / oth:.2f} ({'right direction' if ufd / oth < 1 else 'wrong direction'}; UFDs want ~0.78)")
    if sign.startswith("WRONG"):
        v = "WRONG SIGN"
    elif any(d1.values()):
        v = "FLOOR DERIVED"
    else:
        v = "TOO SMALL"
    FR["verdict"] = v; P(f"  VERDICT [{f}]: {v}")

V = {f: RES["footings"][f]["verdict"] for f in FOOTS}
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else "UNDECIDED (footings disagree)"
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
checks.append(("K3", rss < 1.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.1f} s; peak RSS {rss:.3f} GB")
open(os.path.join(HERE, f"x25_floor_from_action{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x25_floor_from_action_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if n == len(checks) else 1)
