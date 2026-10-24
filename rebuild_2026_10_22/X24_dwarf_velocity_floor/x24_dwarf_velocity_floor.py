#!/usr/bin/env python3
"""X24_dwarf_velocity_floor: is the hosted-dwarf extra host-driven or mass-driven, and does one velocity floor fix it?

Frozen criteria: FROZEN_CRITERIA.md (7a79903c3f, post-hoc, disclosed). Reads X1's per-system CSV and CFG257's
Arroyo-Polonio table, read-only. One thread, seconds.

    python3 x24_dwarf_velocity_floor.py            -> .out, _results.json
    python3 x24_dwarf_velocity_floor.py --mutate   -> E from the AQUAL + EFE column (K0 must fail), _MUTATE outputs
"""
import csv, json, math, os, resource, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize_scalar, brentq

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)

FOOTS = ("canonical", "alt")
H = ("MW ultra-faint", "bright M31", "M31 others")
GRADED = H + ("MW classical",)
REPORT = ("indiv:Crater II", "indiv:Antlia II", "indiv:Canes Venatici I", "indiv:Sagittarius", "M31 dE")
K0_REF = {"canonical": (0.596, 0.220, 0.777), "alt": (0.539, 0.185, 0.697)}
WIN = (5.4, 6.8)
SEED, NBOOT, NPERM = 20261024, 10000, 20000
ECOL = "Delta[AQUAL + EFE L*0 (exact MOND + EFE)]" if MUTATE else "Delta[iso AQUAL L*0]"
SCOL = "sdMC[" + ECOL[len("Delta["):]

ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping",
                                            "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values())))
X1 = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount", "x1_per_system.csv"))))

def load(foot, classes):
    out = []
    for r in X1:
        if r["footing"] != foot or r["cls"] not in classes:
            continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        b = arr_free.get(r["name"], med_free if (mv is not None and mv > -7.7) else 1.0)
        sc = float(r["sigma"]) * b; E = float(r[ECOL])
        out.append(dict(name=r["name"], cls=r["cls"], lm=float(r["logMstar"]), E=E, s=float(r[SCOL]),
                        sc=sc, siso=sc * 10 ** (-E / 2)))
    return out

def epred(siso, c0):
    return np.log10(1.0 + (c0 / np.asarray(siso)) ** 2)
def chi2(R, c0):
    E = np.array([q["E"] for q in R]); s = np.array([q["s"] for q in R]); si = np.array([q["siso"] for q in R])
    return float(np.sum(((E - epred(si, c0)) / s) ** 2))
def calib(R):
    res = minimize_scalar(lambda c: chi2(R, c), bounds=(0.0, 20.0), method="bounded", options={"xatol": 1e-6})
    c0, cmin = float(res.x), float(res.fun)
    f = lambda c: chi2(R, c) - cmin - 1.0
    lo = brentq(f, 0.0, c0) if c0 > 1e-6 and f(0.0) > 0 else 0.0
    hi = brentq(f, c0, 20.0) if f(20.0) > 0 else 20.0
    return c0, lo, hi, cmin
def boot_med(x, s, rng):
    N = len(x); ix = rng.integers(0, N, (NBOOT, N))
    return float(np.median(x)), float(np.std(np.median(x[ix] + s[ix] * rng.standard_normal((NBOOT, N)), axis=1)))
def spearman(x, y):
    rx = np.argsort(np.argsort(x, axis=-1), axis=-1).astype(float); ry = np.argsort(np.argsort(y, axis=-1), axis=-1).astype(float)
    rx -= rx.mean(axis=-1, keepdims=True); ry -= ry.mean(axis=-1, keepdims=True)
    return (rx * ry).sum(-1) / np.sqrt((rx ** 2).sum(-1) * (ry ** 2).sum(-1))

P(f"X24_dwarf_velocity_floor  {'MUTATE run (E from the AQUAL + EFE column)' if MUTATE else 'normal run'}  [POST-HOC, disclosed]")
P("kappa = 1/2 FITTED; footings never pooled; one new constant c0 (calibrated on LG field only); not theory closed")
RES = dict(frozen="7a79903c3f", mutate=MUTATE, footings={}); checks = []
for f in FOOTS:
    rng = np.random.default_rng(SEED)
    FLD = load(f, ("LG field",)); HH = load(f, GRADED); RH = [q for q in HH if q["cls"] in H]
    FR = RES["footings"][f] = {}
    P(f"\n=== [{f}]")
    meds = [float(np.median([q["E"] for q in RH if q["cls"] == c])) for c in H]
    k0 = all(abs(m - r) <= 0.005 for m, r in zip(meds, K0_REF[f])) and len(FLD) == 13
    P(f"  K0 H plain medians {[round(m, 3) for m in meds]} vs X19 {list(K0_REF[f])}; field N {len(FLD)}: {'PASS' if k0 else 'FAIL'}")
    checks.append((f"K0[{f}]", k0))
    k1 = max(abs(math.log10(q["sc"] ** 2 / q["siso"] ** 2) - q["E"]) for q in FLD + HH) < 1e-12
    checks.append((f"K1[{f}]", k1)); P(f"  K1 sigma_iso round trip: {'PASS' if k1 else 'FAIL'}")

    # Test A
    hw = [q for q in HH if WIN[0] <= q["lm"] <= WIN[1]]; fw = [q for q in FLD if WIN[0] <= q["lm"] <= WIN[1]]
    eh, sh = np.array([q["E"] for q in hw]), np.array([q["s"] for q in hw])
    ef, sf = np.array([q["E"] for q in fw]), np.array([q["s"] for q in fw])
    N = 10000; ih, i_f = rng.integers(0, len(hw), (N, len(hw))), rng.integers(0, len(fw), (N, len(fw)))
    dd = np.median(eh[ih] + sh[ih] * rng.standard_normal(ih.shape), 1) - np.median(ef[i_f] + sf[i_f] * rng.standard_normal(i_f.shape), 1)
    D = float(np.median(eh) - np.median(ef)); sD = float(np.std(dd)); ZD = D / sD
    lmF = np.array([q["lm"] for q in FLD]); EF = np.array([q["E"] for q in FLD])
    rho = float(spearman(lmF, EF))
    perm = np.array([rng.permutation(len(EF)) for _ in range(NPERM)])
    pr = float((np.sum(spearman(np.broadcast_to(lmF, perm.shape), EF[perm]) <= rho) + 1) / (NPERM + 1))
    rhoAll = float(spearman(np.array([q["lm"] for q in HH + FLD]), np.array([q["E"] for q in HH + FLD])))
    A = "HOST-DRIVEN" if ZD >= 2 else ("MASS-DRIVEN" if (abs(ZD) < 1 and rho < 0 and pr < 0.05) else "MIXED")
    FR["A"] = dict(N_hosted_window=len(hw), N_field_window=len(fw), med_hosted=float(np.median(eh)), med_field=float(np.median(ef)),
                   D=D, sd=sD, Z=ZD, field_rho=rho, field_p=pr, all_rho=rhoAll, label=A)
    P(f"  Test A window log M* {WIN}: hosted N {len(hw)} median {np.median(eh):+.3f}; field N {len(fw)} median {np.median(ef):+.3f}; "
      f"D {D:+.3f} +- {sD:.3f} (Z {ZD:+.2f})")
    P(f"         field-only Spearman(E, log M*) {rho:+.3f}, one-sided p {pr:.4f}; all dwarfs (H + classical + field) {rhoAll:+.3f}  -> {A}")

    # Test B
    c0, lo, hi, cmin = calib(FLD)
    chi_law_F = chi2(FLD, 0.0)
    P(f"  Test B c0 (field, 13) = {c0:.2f} km/s [{lo:.2f}, {hi:.2f}] (chi2 {cmin:.1f} vs law {chi_law_F:.1f}, N 13)")
    FR["B"] = dict(c0=c0, c0_lo=lo, c0_hi=hi, chi2_field=cmin, chi2_field_law=chi_law_F, classes={})
    allpass = True
    for c in GRADED:
        R = [q for q in HH if q["cls"] == c]
        E = np.array([q["E"] for q in R]); s = np.array([q["s"] for q in R]); si = np.array([q["siso"] for q in R])
        res = E - epred(si, c0); m, sd = boot_med(res, s, rng); z = m / sd
        cf, cl = chi2(R, c0) / len(R), chi2(R, 0.0) / len(R)
        FR["B"]["classes"][c] = dict(N=len(R), median_resid=m, sd=sd, Z=z, chi2N_floor=cf, chi2N_law=cl,
                                     median_sigma_iso=float(np.median(si)), median_sigma_c=float(np.median([q["sc"] for q in R])))
        if c in H and abs(z) >= 2:
            allpass = False
        P(f"    {c:15s} N {len(R):2d}  sigma_c {np.median([q['sc'] for q in R]):5.2f}  sigma_iso {np.median(si):5.2f}  "
          f"resid {m:+.3f} +- {sd:.3f} (Z {z:+.2f})  chi2/N floor {cf:6.2f} vs law {cl:6.2f}")
    chiH_f, chiH_l = chi2(RH, c0), chi2(RH, 0.0)
    B = "FLOOR REPRODUCES THE DWARFS" if (allpass and chiH_f < chiH_l) else ("FLOOR PARTIAL" if chiH_f < chiH_l else "FLOOR FAILS")
    FR["B"].update(chi2_H_floor=chiH_f, chi2_H_law=chiH_l, label=B)
    P(f"    H total chi2 floor {chiH_f:.1f} vs law {chiH_l:.1f} (N {len(RH)})  -> {B}")
    c0H, loH, hiH, _ = calib(RH)
    FR["B"]["c0_fit_on_H_reported"] = [c0H, loH, hiH]
    P(f"    reported: c0 fitted on H (in-sample) {c0H:.2f} [{loH:.2f}, {hiH:.2f}] km/s")
    rep = load(f, REPORT)
    P("    reported (floor can only raise E_pred): " + "; ".join(
        f"{q['name']} E {q['E']:+.2f} pred {float(epred(q['siso'], c0)):+.2f}" for q in rep))
    P(f"    reported SPARC: at V = 100 km/s (sigma = V/sqrt2) dE = {float(epred(100 / math.sqrt(2), c0)):.5f} dex; "
      f"at V = 30 km/s {float(epred(30 / math.sqrt(2), c0)):.4f} dex")
    # K2
    syn = [dict(q) for q in FLD]
    for q in syn:
        q["E"] = float(epred(q["siso"], 4.0)) + q["s"] * rng.standard_normal()
    c2, l2, h2, _ = calib(syn); k2 = l2 - 0.5 <= 4.0 <= h2 + 0.5
    P(f"  K2 positive control: c0 = 4 recovered as {c2:.2f} [{l2:.2f}, {h2:.2f}]: {'PASS' if k2 else 'FAIL'}")
    checks.append((f"K2[{f}]", k2))
    FR["verdict"] = dict(A=A, B=B)

VA = {f: RES["footings"][f]["verdict"]["A"] for f in FOOTS}; VB = {f: RES["footings"][f]["verdict"]["B"] for f in FOOTS}
RES["verdict"] = dict(A=VA["canonical"] if VA["canonical"] == VA["alt"] else "UNDECIDED (footings disagree)",
                      B=VB["canonical"] if VB["canonical"] == VB["alt"] else "UNDECIDED (footings disagree)")
P(f"\n=== VERDICT  Test A: {RES['verdict']['A']}   Test B: {RES['verdict']['B']}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
checks.append(("K3", rss < 1.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.1f} s; peak RSS {rss:.3f} GB")
open(os.path.join(HERE, f"x24_dwarf_velocity_floor{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x24_dwarf_velocity_floor_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if n == len(checks) else 1)
