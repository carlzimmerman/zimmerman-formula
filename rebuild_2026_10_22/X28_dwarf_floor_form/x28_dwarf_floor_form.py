#!/usr/bin/env python3
"""X28_dwarf_floor_form: velocity floor (X24, new c0) vs acceleration floor (eta a0, the theory's own scale).

Frozen criteria: FROZEN_CRITERIA.md (32d4323f88, post-hoc envelope disclosed). Reads X1's per-system CSV, X24's JSON and
CFG257's binary table, read-only. One thread, seconds.

    python3 x28_dwarf_floor_form.py            -> .out, _results.json
    python3 x28_dwarf_floor_form.py --mutate   -> a0 swapped between footings, X24 c0 x 1.1 (K0 must fail), _MUTATE outputs
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

PC = 3.0857e16
FOOTS = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0F = {"canonical": A0["alt"], "alt": A0["canonical"]} if MUTATE else A0
H = ("MW ultra-faint", "bright M31", "M31 others")
GRADED = H + ("MW classical",)
REPORT = ("indiv:Crater II", "indiv:Antlia II", "indiv:Canes Venatici I", "indiv:Sagittarius")
K0_REF = {"canonical": (0.596, 0.220, 0.777), "alt": (0.539, 0.185, 0.697)}
SEED, NBOOT = 20261024, 10000
X24 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "X24_dwarf_velocity_floor", "x24_dwarf_velocity_floor_results.json")))
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
        sc = float(r["sigma"]) * b; E = float(r["Delta[iso AQUAL L*0]"])
        siso = sc * 10 ** (-E / 2); r12 = 4.0 / 3.0 * float(r["rh_pc"]) * PC
        out.append(dict(name=r["name"], cls=r["cls"], E=E, s=float(r["sdMC[iso AQUAL L*0]"]), r12=r12,
                        giso=3 * (siso * 1e3) ** 2 / r12))
    return out

def arr(R, k):
    return np.array([q[k] for q in R])
def ep_v(R, c0, a0):
    return np.log10(1 + 3 * (c0 * 1e3) ** 2 / arr(R, "r12") / arr(R, "giso"))
def ep_g(R, eta, a0):
    return np.log10(1 + eta * a0 / arr(R, "giso"))
def ep_n(R, amp, n, a0):           # g_floor = amp * a0 * (r12 / 100 pc)^(-n)
    return np.log10(1 + amp * a0 * (arr(R, "r12") / (100 * PC)) ** (-n) / arr(R, "giso"))
def chi2(R, ep):
    return float(np.sum(((arr(R, "E") - ep) / arr(R, "s")) ** 2))
def calib(R, fn, a0, hi):
    res = minimize_scalar(lambda p: chi2(R, fn(R, p, a0)), bounds=(0.0, hi), method="bounded", options={"xatol": 1e-7})
    p0, cmin = float(res.x), float(res.fun)
    f = lambda p: chi2(R, fn(R, p, a0)) - cmin - 1.0
    lo = brentq(f, 0.0, p0) if p0 > 1e-9 and f(0.0) > 0 else 0.0
    up = brentq(f, p0, hi) if f(hi) > 0 else hi
    return p0, lo, up, cmin
def boot_med(x, s, rng):
    N = len(x); ix = rng.integers(0, N, (NBOOT, N))
    return float(np.median(x)), float(np.std(np.median(x[ix] + s[ix] * rng.standard_normal((NBOOT, N)), axis=1)))

P(f"X28_dwarf_floor_form  {'MUTATE run (a0 swapped, X24 c0 x 1.1)' if MUTATE else 'normal run'}  [POST-HOC, disclosed]")
P("kappa = 1/2 FITTED; footings never pooled; one constant per form, calibrated on LG field only; no numerology; not theory closed")
RES = dict(frozen="32d4323f88", mutate=MUTATE, footings={}); checks = []
for f in FOOTS:
    a0 = A0F[f]; rng = np.random.default_rng(SEED)
    FLD = load(f, ("LG field",)); GR = load(f, GRADED); RH = [q for q in GR if q["cls"] in H]
    FR = RES["footings"][f] = {}
    c0v = calib(FLD, ep_v, a0, 20.0); etg = calib(FLD, ep_g, a0, 2.0)
    x24c0 = X24["footings"][f]["B"]["c0"] * (1.1 if MUTATE else 1.0)
    meds = [float(np.median([q["E"] for q in RH if q["cls"] == c])) for c in H]
    k0 = abs(c0v[0] - x24c0) < 0.01 and all(abs(m - x) <= 0.005 for m, x in zip(meds, K0_REF[f]))
    k1 = abs(chi2(FLD, ep_g(FLD, 0.0, a0)) - chi2(FLD, ep_v(FLD, 0.0, a0))) < 1e-10
    P(f"\n=== [{f}]  a0 {a0:.4e}")
    P(f"  K0 c0 (field) {c0v[0]:.3f} vs X24 {x24c0:.3f}; H medians {[round(m, 3) for m in meds]}: {'PASS' if k0 else 'FAIL'};  "
      f"K1 eta=0 / c0=0 identical: {'PASS' if k1 else 'FAIL'}")
    checks += [(f"K0[{f}]", k0), (f"K1[{f}]", k1)]
    P(f"  calibration (field, 13): F_v c0 {c0v[0]:.2f} [{c0v[1]:.2f}, {c0v[2]:.2f}] km/s (chi2 {c0v[3]:.1f});  "
      f"F_g eta {etg[0]:.4f} [{etg[1]:.4f}, {etg[2]:.4f}] (chi2 {etg[3]:.1f}; eta a0 = {etg[0] * a0:.3e} m/s^2)")
    FR["calib"] = dict(c0=c0v, eta=etg)
    out = {}
    for form, fn, p in (("F_v", ep_v, c0v[0]), ("F_g", ep_g, etg[0])):
        out[form] = {}
        for c in GRADED:
            Rc = [q for q in GR if q["cls"] == c]
            res = arr(Rc, "E") - fn(Rc, p, a0); m, sd = boot_med(res, arr(Rc, "s"), rng)
            out[form][c] = dict(N=len(Rc), median=m, sd=sd, Z=m / sd, chi2N=chi2(Rc, fn(Rc, p, a0)) / len(Rc))
        out[form]["chi2_H"] = chi2(RH, fn(RH, p, a0))
    chi_law = chi2(RH, ep_g(RH, 0.0, a0))
    for c in GRADED:
        v, g = out["F_v"][c], out["F_g"][c]
        P(f"    {c:15s} N {v['N']:2d}  F_v resid {v['median']:+.3f} +- {v['sd']:.3f} (Z {v['Z']:+.2f}, chi2/N {v['chi2N']:6.2f})   "
          f"F_g resid {g['median']:+.3f} +- {g['sd']:.3f} (Z {g['Z']:+.2f}, chi2/N {g['chi2N']:6.2f})")
    d = out["F_v"]["chi2_H"] - out["F_g"]["chi2_H"]
    P(f"  T1 chi2_H: law {chi_law:.1f}; F_v {out['F_v']['chi2_H']:.1f}; F_g {out['F_g']['chi2_H']:.1f}; Delta (F_v - F_g) {d:+.1f}")
    zu = out["F_g"]["MW ultra-faint"]["Z"]
    P(f"  T2 ultra-faint residual under F_g: Z {zu:+.2f}")
    eH = calib(RH, ep_g, a0, 2.0); cH = calib(RH, ep_v, a0, 20.0)
    ovg = not (eH[2] < etg[1] or eH[1] > etg[2]); ovv = not (cH[2] < c0v[1] or cH[1] > c0v[2])
    P(f"  T3 in-sample on H: eta {eH[0]:.4f} [{eH[1]:.4f}, {eH[2]:.4f}] (overlaps field: {ovg});  c0 {cH[0]:.2f} [{cH[1]:.2f}, {cH[2]:.2f}] (overlaps field: {ovv})")
    # reported: power law on all graded + field
    ALL = GR + FLD
    best = (None, 1e99)
    for n in np.linspace(-0.5, 1.5, 201):
        r = minimize_scalar(lambda A: chi2(ALL, ep_n(ALL, A, n, a0)), bounds=(0.0, 5.0), method="bounded")
        if r.fun < best[1]:
            best = ((float(n), float(r.x)), float(r.fun))
    ns = np.linspace(-0.5, 1.5, 201)
    prof = np.array([minimize_scalar(lambda A: chi2(ALL, ep_n(ALL, A, n, a0)), bounds=(0.0, 5.0), method="bounded").fun for n in ns])
    inside = ns[prof - prof.min() <= 1.0]
    P(f"  reported: power law g_floor ~ r12^-n on all {len(ALL)}: n = {best[0][0]:.2f} [{inside.min():.2f}, {inside.max():.2f}] "
      f"(n = 1 velocity, n = 0 acceleration); chi2 {best[1]:.1f}")
    sp = {gx: float(np.log10(1 + etg[0] / gx)) for gx in (0.1, 0.3, 1.0)}
    cost = sp[0.1] > 0.05 or sp[1.0] > 0.05
    P(f"  SPARC cost of F_g (dE at g_obs = 0.1 / 0.3 / 1 a0): {sp[0.1]:.3f} / {sp[0.3]:.3f} / {sp[1.0]:.3f} dex -> {'[SPARC-COST]' if cost else 'ok'}")
    rep = load(f, REPORT)
    P("  reported: " + "; ".join(f"{q['name']} E {q['E']:+.2f} F_g {float(ep_g([q], etg[0], a0)[0]):+.2f} F_v {float(ep_v([q], c0v[0], a0)[0]):+.2f}" for q in rep))
    # K2
    syn = [dict(q) for q in FLD]
    pe = ep_g(syn, 0.1, a0)
    for q, e in zip(syn, pe):
        q["E"] = float(e) + q["s"] * rng.standard_normal()
    rk = calib(syn, ep_g, a0, 2.0); k2 = rk[1] - 0.05 <= 0.1 <= rk[2] + 0.05
    P(f"  K2 eta = 0.1 recovered as {rk[0]:.3f} [{rk[1]:.3f}, {rk[2]:.3f}]: {'PASS' if k2 else 'FAIL'}"); checks.append((f"K2[{f}]", k2))
    allok = all(abs(out["F_g"][c]["Z"]) < 2 for c in H)
    if d >= 4:
        v = "ACCELERATION FLOOR" if allok else "ACCELERATION PREFERRED, PARTIAL"
    elif d <= -4:
        v = "VELOCITY FLOOR"
    else:
        v = "NOT DISTINGUISHED"
    if cost:
        v += " [SPARC-COST]"
    FR.update(forms=out, chi2_H_law=chi_law, delta_chi2_H=d, Z_ufd_Fg=zu, eta_H=eH, c0_H=cH, eta_overlap=ovg, c0_overlap=ovv,
              power_law=dict(n=best[0][0], amp=best[0][1], n68=[float(inside.min()), float(inside.max())]), sparc_cost=sp, verdict=v)
    P(f"  VERDICT [{f}]: {v}")

V = {f: RES["footings"][f]["verdict"] for f in FOOTS}
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"UNDECIDED (footings disagree: {V})"
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
checks.append(("K3", rss < 1.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.1f} s; peak RSS {rss:.3f} GB")
open(os.path.join(HERE, f"x28_dwarf_floor_form{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x28_dwarf_floor_form_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
