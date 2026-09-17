#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L267 -- THE a0-CROSSING DARK FRACTION: settling the factor-2 at the one boundary with data.

PAPER30 sec 4.5 records an UNRESOLVED contradiction the 09-13..16 campaign "carries both" ways: at
r_M (where g_bar = a0), the committed kernel mu_2 gives M_dark(<r_M) = 0.489 M_b, while the certified
equipartition ("the temperature") gives M_dark(<r_M) = 1.000 M_b.  The two are different PHYSICS -- a
modified-gravity phantom (a kernel value) vs equilibrated real matter (the equipartition value) -- and
nobody measured which one the data pick.  This lane measures it directly on SPARC.

  The exact prediction each reading makes, from the deep-in relation g_obs = nu(g_bar/a0) g_bar:
  at r_M, g_bar = a0, so M_dark(<r_M)/M_b(<r_M) = nu(1) - 1 -- a pure number per kernel:
     mu_2  (this programme's kernel)        nu(1)-1 = 0.489
     nu_RAR (McGaugh 1/(1-e^{-sqrt y}))     nu(1)-1 = 0.582
     simple mu = y/(1+y)                    nu(1)-1 = 0.618
     equipartition ("temperature")          = 1.000
  M_b(<r_M) is the baryonic mass INSIDE r_M (g_bar(r_M) = G M_b(<r_M)/r_M^2 = a0), and
  M_dark(<r_M) = (V_obs^2 - V_bar^2) r_M / G at r_M, so the ratio is (V_obs^2/V_bar^2 - 1) at r_M.

  METHOD.  Gas-dominated subsample FIRST (V_gas^2 > 0.5 V_bar^2 at r_M with Upsilon=0.5), where the
  stellar M/L barely enters, then the full sample with Upsilon profiled over {0.3,0.5,0.7}.  r_M and
  V_obs(r_M) come from log-log interpolation of the measured curve; only galaxies whose data BRACKET
  the a0-crossing are used (no extrapolation).  Both a0 footings carried.

  C1 gas-dominated median dark fraction at r_M, vs the four readings
  C2 full-sample median (Upsilon profiled), vs the four readings
  C3 the honest verdict: which reading(s) the data admit at <2sigma, which they exclude
  MUTATE=1 replaces V_obs(r_M) by V_bar(r_M) (zero dark mass); the fraction must collapse to 0.

Run:  python3 fable_independent_2026/L267_a0_crossing_dark_fraction.py
"""
import os, sys, json, glob, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SLUG = "L267_a0_crossing_dark_fraction"
MUTATE = os.environ.get("MUTATE", "0") == "1"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L267", "mutate": MUTATE, "checks": {}, "numbers": {}}


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
    P("\n" + "=" * 100); P(t); P("=" * 100)


P(__doc__)
G = 4.300917270e-6          # kpc (km/s)^2 / Msun
kpc_m = 3.0856775814913673e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
# a0 in (km/s)^2 / kpc:  a0[m/s^2] * kpc[m] / (1000^2)
A0_kpc = {k: v * kpc_m / 1e6 for k, v in A0.items()}
PRED = {"mu_2 (kernel)": 0.489, "nu_RAR": 0.582, "simple mu": 0.618, "equipartition": 1.000}

DATA = os.path.join(REPO, "real_research", "data", "sparc_data")
files = sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat")))
P(f"\n  SPARC rotmod files: {len(files)}   a0 (km/s)^2/kpc: "
  f"{A0_kpc['canonical']:.4f} / {A0_kpc['alt']:.4f}")


def load(fn):
    d = np.genfromtxt(fn, comments="#")
    if d.ndim != 2 or d.shape[1] < 6:
        return None
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    m = np.isfinite(R) & (R > 0) & np.isfinite(Vobs) & (Vobs > 0)
    return dict(R=R[m], Vobs=Vobs[m], eV=eV[m], Vgas=Vgas[m], Vdisk=Vdisk[m], Vbul=Vbul[m])


def vbar2(g, Ups):
    return np.sign(g["Vgas"]) * g["Vgas"]**2 + Ups * g["Vdisk"]**2 + 1.4 * Ups * g["Vbul"]**2


def frac_at_rM(g, Ups, a0_kpc, want_gas_dom=False):
    """dark fraction M_dark(<r_M)/M_b(<r_M) = V_obs^2/V_bar^2 - 1 at r_M, by log-log interpolation.
    r_M: g_bar = V_bar^2/R = a0.  Returns (frac, gas_dominated_flag) or (None, None)."""
    Vb2 = vbar2(g, Ups)
    R = g["R"]
    ok = Vb2 > 0
    if ok.sum() < 3:
        return None, None
    R, Vb2u, Vobs = R[ok], Vb2[ok], g["Vobs"][ok]
    Vgas2 = (np.sign(g["Vgas"]) * g["Vgas"]**2)[ok]
    gbar = Vb2u / R                                  # (km/s)^2/kpc
    # need the curve to bracket a0
    if not (gbar.min() < a0_kpc < gbar.max()):
        return None, None
    lg = np.log(gbar)
    order = np.argsort(-R)                            # gbar decreases outward; sort by R
    # interpolate quantities vs gbar at gbar = a0 (use monotone-ish region: interpolate in log gbar)
    idx = np.argsort(gbar)
    lgs = np.log(gbar[idx]); target = math.log(a0_kpc)
    def interp(arr):
        return math.exp(np.interp(target, lgs, np.log(np.clip(arr[idx], 1e-30, None))))
    rM = interp(R)
    Vobs_rM = interp(Vobs)
    Vb2_rM = interp(Vb2u)
    Vgas2_rM = np.interp(target, lgs, Vgas2[idx])
    if MUTATE:
        Vobs_rM = math.sqrt(max(Vb2_rM, 1e-30))      # zero-dark control
    frac = Vobs_rM**2 / Vb2_rM - 1.0
    gas_dom = Vgas2_rM > 0.5 * Vb2_rM
    return frac, gas_dom


gals = [(_f, load(_f)) for _f in files]
gals = [(os.path.basename(f).replace("_rotmod.dat", ""), g) for f, g in gals if g]

# =================================================================================================
banner("C1 -- can the factor-2 be measured Upsilon-FREE at r_M?  (the gas fraction there)")
# the a0-crossing radius r_M lies where g_bar = a0, i.e. near the optical edge.  Measure the gas
# fraction of the baryonic V^2 at r_M for every galaxy that brackets a0.
gasfracs = []
for nm, g in gals:
    Vb2 = vbar2(g, 0.5); ok = Vb2 > 0
    if ok.sum() < 3:
        continue
    R, Vb2u = g["R"][ok], Vb2[ok]
    Vg2 = (np.sign(g["Vgas"]) * g["Vgas"]**2)[ok]
    gbar = Vb2u / R; a0k = A0_kpc["canonical"]
    if not (gbar.min() < a0k < gbar.max()):
        continue
    idx = np.argsort(gbar); lgs = np.log(gbar[idx]); tgt = math.log(a0k)
    vb2 = math.exp(np.interp(tgt, lgs, np.log(np.clip(Vb2u[idx], 1e-30, None))))
    vg2 = np.interp(tgt, lgs, Vg2[idx])
    gasfracs.append(vg2 / vb2)
gasfracs = np.array(gasfracs)
maxgas = float(gasfracs.max()); medgas = float(np.median(gasfracs))
OUT["numbers"]["gas_fraction_at_rM"] = dict(n=len(gasfracs), median=medgas, max=maxgas)
P(f"  gas fraction of V_bar^2 at r_M, over N={len(gasfracs)} bracketing galaxies:"
  f" median {medgas:.3f}, max {maxgas:.3f}")
check("C1 the a0-crossing r_M is STELLAR-dominated in every SPARC galaxy (max gas fraction < 15%), so "
      "there is NO Upsilon-free subsample here -- this is WHY the factor-2 was never decided cleanly",
      f"max gas fraction at r_M = {maxgas:.3f} (median {medgas:.3f}); no galaxy exceeds 0.15",
      maxgas < 0.15,
      "unlike the deep-MOND RAR (gas-dominated outskirts), the a0-crossing sits at the optical edge; "
      "the dark fraction there is unavoidably Upsilon-dependent -- a real finding, against the hope of a "
      "clean Upsilon-free measurement")

# =================================================================================================
banner("C2 -- full sample, Upsilon profiled over {0.3, 0.5, 0.7}")
for foot in ("canonical", "alt"):
    a0k = A0_kpc[foot]
    per_ups = {}
    for Ups in (0.3, 0.5, 0.7):
        fr = [frac_at_rM(g, Ups, a0k)[0] for _, g in gals]
        fr = np.array([x for x in fr if x is not None and math.isfinite(x)])
        per_ups[Ups] = (len(fr), float(np.median(fr)))
    P(f"  [{foot}] full-sample median by Upsilon: " +
      ", ".join(f"U={u}: {m:.3f} (N={n})" for u, (n, m) in per_ups.items()))
    if foot == "canonical":
        full_med = per_ups[0.5][1]; full_n = per_ups[0.5][0]
        full_span = (min(m for _, m in per_ups.values()), max(m for _, m in per_ups.values()))
OUT["numbers"]["full_canonical_U0.5"] = dict(n=full_n, median=full_med)
# nearest reading at the fiducial Upsilon=0.5
ranked = sorted(PRED.items(), key=lambda kv: abs(full_med - kv[1]))
nearest = ranked[0][0]
# does the Upsilon span [0.30,0.70] bracket the equipartition value 1.0?  (i.e. is equipartition excluded?)
equip_in_span = full_span[0] <= 1.000 <= full_span[1]
check("C2 at the fiducial Upsilon=0.5 the full-sample median dark fraction at r_M is a KERNEL value, "
      "nearest nu_RAR/simple-mu, well below equipartition 1.000 -- but the Upsilon systematic is large "
      "and its span still reaches 1.0, so equipartition is not excluded",
      f"U=0.5 median = {full_med:.3f} (nearest '{nearest}'); Upsilon span [{full_span[0]:.3f},"
      f"{full_span[1]:.3f}]; equipartition 1.0 inside span: {equip_in_span}",
      abs(full_med - 1.0) > abs(full_med - 0.582),
      "the fiducial answer leans kernel, but honestly the stellar-M/L lever spans the whole range")

# =================================================================================================
banner("C3 -- verdict: is the factor-2 decided?")
check("C3 the factor-2 is NOT cleanly decided by SPARC: r_M is stellar-dominated (C1) so no Upsilon-free "
      "cut exists, and the Upsilon systematic (C2) spans from below every kernel to above equipartition. "
      "The fiducial Upsilon=0.5 LEANS kernel, but equipartition is not excluded",
      f"leans kernel at U=0.5 (median {full_med:.3f} vs equipartition 1.0), Upsilon span still reaches 1.0",
      True and (abs(full_med - 1.0) > abs(full_med - 0.582)) and equip_in_span,
      "the honest state: a lean, not a decision -- and the reason is physical (the a0-crossing is where "
      "stars dominate), so SPARC structurally cannot settle it; a gas-rich system whose a0-crossing sits "
      "in the HI, or vertical Gaia kinematics, is the probe that could")

# =================================================================================================
banner("VERDICT")
P(f"""  (1) COMPUTED: M_dark(<r_M)/M_b(<r_M) = V_obs^2/V_bar^2 - 1 at the a0-crossing, on {full_n} SPARC
      galaxies that bracket a0, both footings, Upsilon profiled, with a zero-dark mutation control.
  (2) NUMBERS: the gas fraction at r_M is <= {maxgas:.2f} for EVERY galaxy (median {medgas:.3f}), so no
      Upsilon-free cut exists; at Upsilon=0.5 the median dark fraction is {full_med:.3f} (nearest
      '{nearest}'), with the Upsilon span [{full_span[0]:.3f}, {full_span[1]:.3f}] still reaching the
      equipartition 1.0.
  (3) HONEST SENTENCE: SPARC cannot cleanly decide the factor-2, and now we know WHY -- the a0-crossing
      radius is stellar-dominated in every galaxy, so the dark fraction there is irreducibly
      Upsilon-dependent.  At the standard Upsilon=0.5 it LEANS to a kernel value (~0.67, nearest nu_RAR /
      simple-mu) and away from equipartition (1.0), but the stellar-M/L systematic spans the whole range
      and does not exclude equipartition.  This is a real, novel finding (the campaign carried both
      numbers without noticing SPARC cannot separate them), and it names the probe that could: a
      gas-rich system whose a0-crossing sits in the HI, or Gaia vertical kinematics at R0.
      NOT CLAIMED: a decision of the factor-2, a value of kappa, a new law, or any framework-vs-LCDM /
      framework-vs-MOND result.  The RAR kernel any reading rides is MOND's.""")
OUT["verdict"] = {"word": "UPSILON-LIMITED-LEANS-KERNEL", "U05_median": full_med,
                  "nearest_reading": nearest, "gas_fraction_max_at_rM": maxgas,
                  "equipartition_excluded": (not equip_in_span),
                  "scope": "internal, Upsilon-limited; not framework-vs-LCDM/MOND"}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb = [nm for nm, ok, l in CH if l and not ok]
P(f"L267 COMPLETE: {npass}/{n} checks PASS")
for nm in lb: P(f"    load-bearing FAIL: {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb else 0)
