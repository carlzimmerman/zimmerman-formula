#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L390 -- KiDS-1000 WITH THE CARRIER RESOLVED, AT THE LINEAR VACUUM GATE (p = 1, x_c0 = 2.5): L375's test, same-cell.

WHY.  L375 resolved the triggered carrier around KiDS lenses (spherical shell model: secondary infall, the bins' baryons,
Newtonian carrier per L353, L365's trigger) and scored the carrier's OWN projected profile on KiDS with the switch at the
p = 2, x_c0 = 2 cell: it passed (-11.5/-8.4).  DE1/DE2 (dark_energy_2026) moved the construction to the linear gate
p = 1, x_c0 = 2.5 (the p = 2 cell fails the flat-a0 flagship), and L388 re-runs the cosmology there.  Passes are never
pooled across cells, so KiDS is re-scored at the new cell: the switched phantom at the new cell's x_c,eff(0.25) (L359's
own K1 entry), the bins' baryonic masses REFITTED at the new cell, and the carrier halos re-run with those masses.

METHOD: L375's halo() imported unchanged; L360's KiDS machinery loaded unedited (as L375); L375's template() and kids()
reproduced line for line.  Kicks 575, 600, 625, 650 km/s (L388's grid), fiducial accretion history.
PRE-DECLARED (before the run): H: at the linear gate the resolved carrier halo passes KiDS (Delta chi^2 <= +4 against the
unswitched model, both footings) at every kick 575-650 km/s.
CHECKS
  C1 CONTROL: at the p = 2, x_c0 = 2 cell, with L375's own baryonic masses and seeds, the fiducial (650 km/s) score
     reproduces L375's committed Delta chi^2 exactly (same code path).
  C2 CONTROL: with the decay off, KiDS rejects the carrier halo at the new cell (> +100, both footings), as L375's C1.
  R1 = H.  W (informational): the refitted baryonic masses, S per bin, the p = 1, x_c0 = 1.5 cell alongside.
MUTATE=1: v_k = 0 in every decaying run at the new cell: R1 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/dark_sector_2026/L390_kids_resolved_linear_gate.py
"""
import os, sys, json, math, time, io, contextlib
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from L375_triggered_carrier_galaxy_retention import halo, M200_BINS, RAP   # noqa: E402  (L375's shell model, unchanged)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L390_kids_resolved_linear_gate"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L390", "cell": "p=1, x_c0=2.5", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_PASS = True                                               # H, set before the run
NEW, OLD, OLD1 = "p=1, x_c0=2.5", "p=2, x_c0=2.0", "p=1, x_c0=1.5"
VK = (575.0, 600.0, 625.0, 650.0)


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


if __name__ == "__main__":
    P(__doc__)
    P60 = os.path.join(REPO, "real_research", "g03_audit_2026", "L360_assembled_construction_kids.py")
    N60 = {"__name__": "l360", "__file__": P60}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(P60).read().split("BASE = {")[0], N60)
    fit_comb, fit_model, A052, XE59 = N60["fit_comb"], N60["fit_model"], N60["A0"], N60["XE59"]
    project_M2, annulus_esd, rr, Rp, Rd, MS = [N60[k] for k in ("project_M2", "annulus_esd", "rr", "Rp", "Rd", "MS")]
    MPCm = N60["L52"]["MPCm"]
    FOOT = ("canonical", "alt")
    XE = {c_: round(XE59[(float(c_.split(",")[0][2:]), float(c_.split("=")[2]))], 4) for c_ in (NEW, OLD, OLD1)}
    BASE = {f_: fit_model(A052[f_], 0.0, "none", True)[0] for f_ in FOOT}
    MB = {c_: [10 ** lm_ for lm_, _, _ in fit_model(A052["canonical"], XE[c_], "compensated", True)[1]] for c_ in (NEW, OLD)}
    P(f"  x_c,eff(0.25): {XE};  fitted M_b: new cell {[f'{x:.2e}' for x in MB[NEW]]}, L375's cell {[f'{x:.2e}' for x in MB[OLD]]}")
    OUT["numbers"]["x_c_eff_0.25"] = XE; OUT["numbers"]["M_b"] = MB

    N = int(os.environ.get("L390_N", "60000"))
    cfgs = []
    for b in range(4):                                           # C1: L375's own cell, masses and seeds
        cfgs.append((f"old_b{b}_nodecay", b, MB[OLD][b], 650.0, 0.0, 0.75, True, N, 100 + b))
        cfgs.append((f"old_b{b}_fid", b, MB[OLD][b], 650.0, 10.0, 0.75, True, N, 200 + b))
    for b in range(4):                                           # the new cell
        cfgs.append((f"new_b{b}_nodecay", b, MB[NEW][b], 650.0, 0.0, 0.75, True, N, 1100 + b))
        for v in VK:
            cfgs.append((f"new_b{b}_v{int(v)}", b, MB[NEW][b], 0.0 if MUTATE else v, 10.0, 0.75, True, N, 1200 + 10 * b + int(v) // 25))
    if MUTATE:
        P("  MUTATE: v_k = 0 in every decaying run at the new cell")
    with Pool(int(os.environ.get("L390_POOL", "4"))) as pool:
        res = dict(pool.map(halo, cfgs, chunksize=1))
    P(f"  {len(cfgs)} halos done   [{time.time() - T0:.0f}s]")

    def template(runs):                                          # L375's template(), line for line
        TC = []
        for b, d in enumerate(runs):
            e = d["edges"]; rm = np.sqrt(e[1:] * e[:-1]); vol = 4 / 3 * math.pi * (e[1:] ** 3 - e[:-1] ** 3)
            rho = d["hist"] * d["m"] / vol
            rho_si = np.interp(np.log(rr / MPCm * 1e3), np.log(rm), rho, left=rho[0], right=0.0) * MS / (MPCm / 1e3) ** 3
            M2 = project_M2(rho_si)
            TC.append(annulus_esd(lambda R, M2=M2: np.interp(np.log(R), np.log(Rp), M2), Rd[b]))
        return TC

    def kids(TC, cell):                                          # L375's kids()
        return {f_: float(fit_comb(A052[f_], XE[cell], TC, [1.0])[0] - BASE[f_]) for f_ in FOOT}

    banner("C1, C2  CONTROLS")
    R75 = json.load(open(os.path.join(HERE, "L375_triggered_carrier_galaxy_retention_results.json")))["numbers"]["table"]["fid"]["kids"][OLD]
    k_old = kids(template([res[f"old_b{b}_fid"] for b in range(4)]), OLD)
    d1 = max(abs(k_old[f_] - R75[f_]) for f_ in FOOT)
    check("C1 at L375's cell (p = 2, x_c0 = 2) with L375's masses and seeds, the fiducial KiDS score reproduces L375's committed value",
          f"{ {f_: round(v, 4) for f_, v in k_old.items()} } vs L375 { {f_: round(v, 4) for f_, v in R75.items()} } (max |diff| {d1:.1e})", d1 < 1e-6)
    k0 = kids(template([res[f"new_b{b}_nodecay"] for b in range(4)]), NEW)
    check("C2 with the decay off KiDS rejects the carrier halo at the new cell (> +100, both footings)", f"{k0}", min(k0.values()) > 100)

    banner("KiDS AT THE LINEAR GATE, CARRIER RESOLVED")
    TAB = {}
    for v in VK:
        t = f"v{int(v)}"; runs = [res[f"new_b{b}_{t}"] for b in range(4)]
        S = [runs[b]["M_ap"] / res[f"new_b{b}_nodecay"]["M_ap"] for b in range(4)]
        TC = template(runs); kn, k1 = kids(TC, NEW), kids(TC, OLD1)
        TAB[t] = dict(S=S, kids=kn, kids_p1_x1p5=k1, pass_=all(x <= 4.0 for x in kn.values()))
        P(f"    {t}: S by bin {[round(x, 3) for x in S]}  |  KiDS at p = 1, x_c0 = 2.5: {kn['canonical']:+.1f}/{kn['alt']:+.1f} "
          f"{'ok' if TAB[t]['pass_'] else 'FAIL'}   (p = 1, x_c0 = 1.5 alongside: {k1['canonical']:+.1f}/{k1['alt']:+.1f})")
    OUT["numbers"].update(table=TAB, controls=dict(C1=k_old, C2=k0))
    check("W (informational) S per bin and the p = 1, x_c0 = 1.5 cell alongside", "see table", True, "reported either way", load_bearing=False)

    banner("R1  THE HYPOTHESIS (set before the run)")
    check("R1 = H: at the linear gate the resolved carrier halo passes KiDS on both footings at every kick 575-650 km/s",
          "; ".join(f"{t}: {d['kids']['canonical']:+.1f}/{d['kids']['alt']:+.1f}" for t, d in TAB.items()),
          all(d["pass_"] for d in TAB.values()) == EXPECT_PASS)

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
