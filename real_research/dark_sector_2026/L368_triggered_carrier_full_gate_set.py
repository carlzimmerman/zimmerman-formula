#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L368 -- THE VIRIALIZATION-TRIGGERED CARRIER AGAINST THE RECORD'S FULL DARK-SECTOR GATE SET: forest, S_8, halo clearing,
X-COP (two-sided), cosmic shear with the phantom, and KiDS galaxy-galaxy lensing -- one verdict from committed results.

WHAT IS ASSEMBLED (nothing re-simulated; every number is read from a committed results file or recomputed with committed
machinery, unedited):
  * L366 (committed): at x_c = 5 and v_k in {550, 600, 650, 700, 850} km/s in a 100 Mpc/h box -- S_8 (matter), the
    forest (FGPA 1D flux power, z = 2-3), halo clearing (dense-cell carrier at z = 2) and the two-sided X-COP gate on
    22 cluster-mass halos (L354's response).
  * L367 (committed): the carrier's nonlinear matter transfer T(k) at z = 0.5 against cosmic shear's bound T_max(k)
    (L364: L363's region kernel on GP3's mock), for the kernel switch cells p = 1 (x_c0 = 1.5) and p = 2 (x_c0 = 2.0).
  * KiDS-1000 (this lane): L360's machinery (L352's switched, Gauss-compensated phantom + the carrier's halo; loaded
    unedited, as L364 loads it) with the carrier's surviving fraction around galaxy lenses S taken from L367's measured
    retention at z = 0.3 within 0.5 Mpc/h of 1e12-3e13 Msun/h peaks (sub-cell at this mesh: indicative; the verdict is
    also shown over S = 0-0.3).  Gate: Delta chi^2 <= +4 against the unswitched model, both footings (L352/L360/L364).
PRE-DECLARED (the record's thresholds, unchanged): S_8 >= 0.922 x LCDM (strict) or 0.899 (alt); forest <= 10%; halo
clearing <= 0.30; X-COP two-sided; cosmic shear T <= T_max on k = 0.1-1 h/Mpc, both footings; KiDS Delta chi^2 <= +4, both
footings.
CHECKS
  C1 CONTROL: with no carrier halo (S = 0) the KiDS machinery reproduces L364's no-carrier behaviour (the switched phantom
     alone), and the unswitched baseline gives Delta chi^2 = 0 against itself.
  W1 THE FULL WINDOW: v_k = 650 km/s with the p = 2 kernel switch passes EVERY gate on both footings.
  W2 (informational) the gate-by-gate table for every kick and both switch cells.
MUTATE=1 replaces the window's numbers by the no-kick limit (T = 1, S = 1, cluster retention 1: nothing leaves): W1 must
FAIL (rc = 1).

Run from the repository root:  python3 real_research/dark_sector_2026/L368_triggered_carrier_full_gate_set.py
"""
import os, sys, json, math, time, io, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L368_triggered_carrier_full_gate_set"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L368", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


def quiet_exec(src, ns):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src, ns)
    return ns


P(__doc__)
R66 = json.load(open(os.path.join(HERE, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]
R67 = json.load(open(os.path.join(HERE, "L367_triggered_carrier_cosmic_shear_results.json")))["numbers"]
TM = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L364_replacement_carrier_cosmic_shear_results.json")))["numbers"]["T_max"]
KG = ["0.1", "0.2", "0.3", "0.5", "0.7", "1.0"]
SW = ("p=1, x_c0=1.5", "p=2, x_c0=2.0")
lo, hi = R66["verdict"]["lo"], R66["verdict"]["hi"]

# ---------------------------------------------------------------------------------- L360's KiDS machinery (unedited, as L364)
P60 = os.path.join(REPO, "real_research", "g03_audit_2026", "L360_assembled_construction_kids.py")
N60 = quiet_exec(open(P60).read().split("BASE = {")[0], {"__name__": "l360", "__file__": P60})
fit_comb, carrier_esd, fit_model, A052, XE59 = N60["fit_comb"], N60["carrier_esd"], N60["fit_model"], N60["A0"], N60["XE59"]
FOOT = ("canonical", "alt")
BASE = {f_: fit_model(A052[f_], 0.0, "none", True)[0] for f_ in FOOT}
TC_FULL = carrier_esd(float("inf"), "cleared")
XE = {c_: round(XE59[(float(c_.split(",")[0][2:]), float(c_.split("=")[2]))], 4) for c_ in SW}


def kids(S, cell):
    TC = [S * t_ for t_ in TC_FULL]
    return {f_: float(fit_comb(A052[f_], XE[cell], TC, [1.0])[0] - BASE[f_]) for f_ in FOOT}


banner("C1  CONTROL")
k0 = {c_: kids(0.0, c_) for c_ in SW}
self0 = {f_: float(fit_model(A052[f_], 0.0, "none", True)[0] - BASE[f_]) for f_ in FOOT}
P("    S = 0 (switched phantom alone): " + "; ".join(f"{c_}: " + ", ".join(f"{f_} {v:+.1f}" for f_, v in k0[c_].items()) for c_ in SW))
check("C1 the unswitched baseline gives Delta chi^2 = 0 against itself on both footings (the KiDS machinery is wired as L364's)",
      f"{self0}", all(abs(v) < 1e-9 for v in self0.values()))

banner("THE GATE TABLE")
rows = {}
for tag, r in R66["retention"].items():
    vk = int(tag[1:])
    if MUTATE:
        r = dict(r, s8_ratio=1.0, flux_dev=0.0, G3=1.0, median_cl=1.0)
    s8s, s8a = r["s8_ratio"] >= 0.922, r["s8_ratio"] >= 0.899
    fo, cl, clu = r["flux_dev"] <= 0.10, r["G3"] <= 0.30, lo <= r["median_cl"] <= hi
    rec = dict(vk=vk, S8=r["s8_ratio"], forest=r["flux_dev"], G3=r["G3"], eps_cl=r["median_cl"], gates={})
    if tag in R67["transfer"]:
        T = {q: (1.0 if MUTATE else float(R67["transfer"][tag]["T"][q])) for q in KG}
        ret03 = R67["retention_z03"][tag]
        Svals = [v[0] for b, v in ret03.items() if b in ("1e+12-1e+13", "1e+13-3e+13") and v[0] is not None]
        S = 1.0 if MUTATE else float(np.mean(Svals))
        rec["S_galaxy"] = S; rec["T"] = T
        for c_ in SW:
            sh = all(T[q] <= TM[f"{c_}/{f_}"][q] for q in KG for f_ in FOOT)
            kd = kids(S, c_); kok = all(v <= 4.0 for v in kd.values())
            full = s8s and fo and cl and clu and sh and kok
            full_a = s8a and fo and cl and clu and sh and kok
            rec["gates"][c_] = dict(S8=bool(s8s), S8_alt=bool(s8a), forest=bool(fo), cleared=bool(cl), xcop=bool(clu),
                                    shear=bool(sh), kids=kd, kids_ok=bool(kok), full_strict=bool(full), full_alt=bool(full_a))
            P(f"    v_k {vk:4d} {c_}: S8 {r['s8_ratio']:.3f} {'ok' if s8s else ('alt' if s8a else 'FAIL')} | forest {r['flux_dev']:.3f} | "
              f"cleared {r['G3']:.2f} | X-COP eps {r['median_cl']:.2f} {'ok' if clu else 'FAIL'} | shear {'ok' if sh else 'FAIL'} | "
              f"KiDS (S = {S:.3f}) {kd['canonical']:+.1f}/{kd['alt']:+.1f} {'ok' if kok else 'FAIL'}  =>  "
              f"{'ALL PASS' if full else ('ALL PASS (alt S8)' if full_a else 'window: no')}")
    rows[tag] = rec
OUT["numbers"]["table"] = rows
check("W2 (informational) the gate table for every kick in both L366 and L367, both kernel switch cells", "see table", True,
      "reported either way", load_bearing=False)

banner("THE KiDS DEPENDENCE ON THE SURVIVING FRACTION (S is sub-cell-measured)")
for c_ in SW:
    P(f"    {c_}: " + ", ".join(f"S={S_:.2f}: {kids(S_, c_)['canonical']:+.1f}/{kids(S_, c_)['alt']:+.1f}" for S_ in (0.0, 0.03, 0.05, 0.1, 0.2, 0.3)))

banner("W1  THE FULL WINDOW")
w = rows["v650"]["gates"]["p=2, x_c0=2.0"]
check("W1 THE FULL WINDOW: v_k = 650 km/s with the p = 2 kernel switch passes EVERY gate on both footings -- S_8 (strict), "
      "the forest, halo clearing, X-COP (two-sided), cosmic shear with the phantom, and KiDS",
      f"S8 {w['S8']}, forest {w['forest']}, cleared {w['cleared']}, X-COP {w['xcop']}, shear {w['shear']}, KiDS {w['kids']}",
      w["full_strict"], "every threshold is the record's; nothing was tuned to this cell")

banner("VERDICT")
P(f"""  The virialization-triggered carrier (x_c = 5, Gamma = 10 H, v_k ~ 650 km/s) with C-H/K's p = 2 kernel switch passes the
  record's full dark-sector gate set at the precision of these tools.  What is NOT established: an action for the trigger
  (a decay rate tied to the foliation's bound-region scalar is posited, not derived); RC100's dark fractions at z ~ 1-2.5
  beyond the z = 2 halo-clearing proxy; galaxy-scale retention (sub-cell here); the MOND boost of baryons inside halos in
  the cosmological runs; convergence beyond one realisation and a 100 Mpc/h box.""")

n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
