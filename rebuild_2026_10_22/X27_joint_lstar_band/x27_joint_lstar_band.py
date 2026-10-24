#!/usr/bin/env python3
"""X27_joint_lstar_band: the joint L* band from the outer globulars (D10 floor, read) and the LG dwarfs (X1's v3 columns).

Frozen criteria: FROZEN_CRITERIA.md (4bf6612dc5). Reads X1's per-system CSV, CFG257's binary table and
V3_FULL_PICTURE.md (for the floor), read-only. One thread, seconds.

    python3 x27_joint_lstar_band.py            -> .out, _results.json
    python3 x27_joint_lstar_band.py --mutate   -> screening sign flipped (K4 must fail), _MUTATE outputs
"""
import csv, json, math, os, resource, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize_scalar

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)

PC = 3.0857e16
FOOTS = ("canonical", "alt")
FLOOR = {"canonical": 21.682, "alt": 22.849}
X1_FLOOR = {"canonical": 21.68, "alt": 22.85}           # the L* at which X1's 'floor' column was solved
H = ("MW ultra-faint", "bright M31", "M31 others")
CLS = H + ("MW classical", "LG field")
REPORT = ("indiv:Crater II", "indiv:Antlia II", "indiv:Canes Venatici I", "indiv:Sagittarius", "M31 dE")
K0_REF = {"canonical": (0.596, 0.220, 0.777), "alt": (0.539, 0.185, 0.697)}
COLS = {"0": "AQUAL + EFE L*0 (exact MOND + EFE)", "floor": "v3 L*floor", "24": "v3 L*24", "90": "v3 L*90"}

ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping",
                                            "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values())))
X1 = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount", "x1_per_system.csv"))))
DOC = open(os.path.join(REPO, "covariant_push_2026_10_22", "V3_FULL_PICTURE.md")).read()

def load(foot, classes):
    out = []
    for r in X1:
        if r["footing"] != foot or r["cls"] not in classes:
            continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        b = arr_free.get(r["name"], med_free if (mv is not None and mv > -7.7) else 1.0)
        r12 = 4.0 / 3.0 * float(r["rh_pc"]) * PC
        q = dict(name=r["name"], cls=r["cls"], Eiso=float(r["Delta[iso AQUAL L*0]"]), r12=r12,
                 gobs=3 * (float(r["sigma"]) * b * 1e3) ** 2 / r12)
        for k, c in COLS.items():
            q["D" + k], q["s" + k] = float(r[f"Delta[{c}]"]), float(r[f"sdMC[{c}]"])
        if MUTATE:
            for k in ("floor", "24", "90"):
                q["D" + k] = q["D0"] - (q["D" + k] - q["D0"])
        out.append(q)
    return out

def interp(R, foot, L, key="D"):
    xs = np.log10([X1_FLOOR[foot], 24.0, 90.0]); lx = math.log10(L)
    return np.array([float(np.interp(lx, xs, [q[key + "floor"], q[key + "24"], q[key + "90"]])) for q in R])

def chi2_M0(R, foot, L):
    return float(np.sum((interp(R, foot, L) / interp(R, foot, L, "s")) ** 2))
def chi2_M1(R, foot, L, c0):
    D, s = interp(R, foot, L), interp(R, foot, L, "s")
    go = np.array([q["gobs"] for q in R]); r12 = np.array([q["r12"] for q in R])
    gp = go * 10 ** (-D) + 3 * (c0 * 1e3) ** 2 / r12
    return float(np.sum(((np.log10(go) - np.log10(gp)) / s) ** 2))
def prof_M1(R, foot, L):
    res = minimize_scalar(lambda c: chi2_M1(R, foot, L, c), bounds=(0.0, 30.0), method="bounded", options={"xatol": 1e-5})
    return float(res.fun), float(res.x)

def upper(Ls, chi):
    i0 = int(np.argmin(chi)); cmin = chi[i0]
    for i in range(i0, len(Ls)):
        if chi[i] - cmin >= 3.84:
            # linear root between i-1 and i in log L
            a, b = chi[i - 1] - cmin - 3.84, chi[i] - cmin - 3.84
            t = a / (a - b) if a != b else 0.0
            return float(10 ** (math.log10(Ls[i - 1]) + t * (math.log10(Ls[i]) - math.log10(Ls[i - 1])))), float(Ls[i0]), float(cmin)
    return float("inf"), float(Ls[i0]), float(cmin)

def bracket(L):
    return "> 90" if not math.isfinite(L) else ("[floor, 24]" if L <= 24 else "(24, 90)")
def band_class(fl, up):
    if up < fl:
        return "EMPTY"
    return "PINNED" if up / fl < 1.5 else "BOUNDED"

P(f"X27_joint_lstar_band  {'MUTATE run (screening sign flipped)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; M0 literal v3s (verdict), M1 + X24 floor profiled (qualifier); not theory closed")
RES = dict(frozen="4bf6612dc5", mutate=MUTATE, footings={}); checks = []
kd = "21.682 / 22.849" in DOC
for f in FOOTS:
    R = load(f, CLS); FR = RES["footings"][f] = {}
    meds = [float(np.median([q["Eiso"] for q in R if q["cls"] == c])) for c in H]
    k0 = all(abs(m - x) <= 0.005 for m, x in zip(meds, K0_REF[f])) and len(R) == 82 and kd
    P(f"\n=== [{f}]  N {len(R)}; floor (D10, read) {FLOOR[f]} pc; K0 {'PASS' if k0 else 'FAIL'}")
    checks.append((f"K0[{f}]", k0))
    k1 = all(np.allclose(interp(R, f, L), [q["D" + k] for q in R], atol=1e-12, rtol=0)
             for L, k in ((X1_FLOOR[f], "floor"), (24.0, "24"), (90.0, "90")))
    checks.append((f"K1[{f}]", k1))
    k2 = abs(chi2_M1(R, f, 30.0, 0.0) - chi2_M0(R, f, 30.0)) < 1e-10
    checks.append((f"K2[{f}]", k2))
    Ls = np.logspace(math.log10(X1_FLOOR[f]), math.log10(90.0), 400)
    c0M = np.array([chi2_M0(R, f, L) for L in Ls])
    pM1 = [prof_M1(R, f, L) for L in Ls]; c1M = np.array([p[0] for p in pM1]); c0s = np.array([p[1] for p in pM1])
    k4 = bool(chi2_M0(R, f, 24.0) >= chi2_M0(R, f, X1_FLOOR[f]))
    checks.append((f"K4[{f}]", k4))
    P(f"  K1 grid round trip {'PASS' if k1 else 'FAIL'}; K2 M1(c0=0) = M0 {'PASS' if k2 else 'FAIL'}; "
      f"K4 chi2 floor->24 non-decreasing {'PASS' if k4 else 'FAIL'}")
    up0, Lmin0, cmin0 = upper(Ls, c0M); up1, Lmin1, cmin1 = upper(Ls, c1M)
    P(f"  M0 literal v3s: chi2 at floor / 24 / 90 = {chi2_M0(R, f, X1_FLOOR[f]):.1f} / {chi2_M0(R, f, 24):.1f} / {chi2_M0(R, f, 90):.1f}; "
      f"min {cmin0:.1f} at {Lmin0:.2f} pc (chi2/N {cmin0 / len(R):.2f}); L*,up {up0:.2f} pc {bracket(up0)}")
    i24 = int(np.argmin(abs(Ls - 24.0)))
    P(f"  M1 + floor (c0 profiled): chi2 at floor / 24 / 90 = {c1M[0]:.1f} / {c1M[i24]:.1f} / {c1M[-1]:.1f} "
      f"(c0 {c0s[0]:.2f} / {c0s[i24]:.2f} / {c0s[-1]:.2f} km/s); min {cmin1:.1f} at {Lmin1:.2f} pc (chi2/N {cmin1 / len(R):.2f}); "
      f"L*,up {up1:.2f} pc {bracket(up1)}")
    # A1 (post-result, reported only): M0 bound with errors scaled by sqrt(chi2_min/N)
    upS = upper(Ls, c0M / (cmin0 / len(R)))[0]
    P(f"  A1 reported: M0 with errors scaled by sqrt(chi2/N) = {math.sqrt(cmin0 / len(R)):.2f}: L*,up {upS:.1f} pc {bracket(upS)}")
    FR["A1_M0_scaled_L_up"] = upS
    b0, b1 = band_class(FLOOR[f], up0), band_class(FLOOR[f], up1)
    lab = b0 + (" [SHORTFALL-DRIVEN]" if b0 != b1 else "")
    P(f"  joint band M0: [{FLOOR[f]}, {up0:.2f}] pc -> {b0}; M1: [{FLOOR[f]}, {up1:.2f}] -> {b1}  => {lab}")
    byc = {}
    for c in CLS:
        Rc = [q for q in R if q["cls"] == c]
        byc[c] = {k: float(np.median([q["D" + k] for q in Rc])) for k in ("0", "floor", "24", "90")}
    P("  class medians Delta (L* 0 / floor / 24 / 90): " + "; ".join(
        f"{c} {v['0']:+.2f}/{v['floor']:+.2f}/{v['24']:+.2f}/{v['90']:+.2f}" for c, v in byc.items()))
    rep = load(f, REPORT)
    P("  reported systems Delta (0 / floor / 24 / 90): " + "; ".join(
        f"{q['name']} {q['D0']:+.2f}/{q['Dfloor']:+.2f}/{q['D24']:+.2f}/{q['D90']:+.2f}" for q in rep))
    FR.update(N=len(R), floor=FLOOR[f], M0=dict(L_up=up0, L_min=Lmin0, chi2_min=cmin0, bracket=bracket(up0), band=b0),
              M1=dict(L_up=up1, L_min=Lmin1, chi2_min=cmin1, bracket=bracket(up1), band=b1,
                      c0_at_floor=float(c0s[0]), c0_at_24=float(c0s[i24]), c0_at_90=float(c0s[-1])),
              label=lab, class_medians=byc)

V = {f: RES["footings"][f]["label"] for f in FOOTS}
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"UNDECIDED (footings disagree: {V})"
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
checks.append(("K3", rss < 1.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.1f} s; peak RSS {rss:.3f} GB")
open(os.path.join(HERE, f"x27_joint_lstar_band{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x27_joint_lstar_band_results{TAG}.json"), "w"), indent=1, default=str)
sys.exit(0 if n == len(checks) else 1)
