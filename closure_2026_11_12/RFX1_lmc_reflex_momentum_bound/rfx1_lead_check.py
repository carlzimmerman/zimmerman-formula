#!/usr/bin/env python3
"""RFX1 lead's check, written 2026-11-12 AFTER the result was read. Not graded; changes no label.
Usage: python3 -I -B rfx1_lead_check.py      (no data file; reads rfx1.py beside it and LMC1's committed results)

Why: the published apexes fall in two groups (positive l: Petersen and Penarrubia 2021, Yaaqib et al. 2024;
negative l: Chandra et al. 2024, Bystrom et al. 2025, Li et al. 2026; all PROVISIONAL, SOURCES.md), and the
frozen bound B_first uses one look-back window (last apocentre to today). This check asks how the bound's size
and direction depend on the window T: V(T) = -mu (v_rel(today) - v_rel(today - T)), the inner Galaxy's velocity
change over the last T, which is what a halo that stopped following T ago would see at most.

  C1  B(T) and its direction for T = 50 ... 1500 Myr and at the last apocentre, the largest B(T) over the
      window, for the four primary configurations, with the angle to each published apex.
  C2  for each published measurement, the window T whose direction is closest to its apex, and the bound at
      that window beside the measured amplitude.
  C3  the apex of LMC1's rigid model (its 50-80 kpc full-sky dipole) against each published apex.
  C4  the same table with the standard-model literature's masses (BORROWED, context only, no label): if the
      direction-matched bound of C2 falls below the measurements even then, C2 cannot be held against the
      framework; it shows the momentum-window picture is not what those measurements are.

rfx1.py's own constants, field, LMC phase-space and helper functions are taken by parsing its source and
executing only the statements up to its orbit section (no output file is opened, nothing is rewritten).
"""
import os, sys, ast, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
tree = ast.parse(open(os.path.join(HERE, "rfx1.py")).read())
stop = next(n.lineno for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "back_orbit")
def wanted(n):
    if n.lineno >= stop: return False
    if isinstance(n, (ast.Import, ast.ImportFrom, ast.ClassDef)): return True
    if isinstance(n, ast.FunctionDef): return n.name not in ("say", "sec", "check", "stop_if_failed")
    if isinstance(n, ast.Assign): return not any(isinstance(t, ast.Name) and t.id in ("OUT", "FAIL", "FITS") for t in n.targets)
    return False
H = {"__name__": "rfx1_functions", "__file__": os.path.join(HERE, "rfx1.py")}
exec(compile(ast.Module(body=[n for n in tree.body if wanted(n)], type_ignores=[]), "rfx1.py", "exec"), H)
KMS, XL0, VL0, FIELDS, lb, sep = H["KMS"], H["XL0"], H["VL0"], H["FIELDS"], H["lb"], H["sep"]
# copied from rfx1.py (defined there after the orbit section): the dynamical mass inside r_c and the primary m_L
def mdyn(ft, rc): return float(H["g_model"](rc, ft)) * (rc * H["KPC"]) ** 2 / H["G"] / H["MSUN"]
M_L_R1 = 3.2e9 + 3.1e8 + 5.6e8

OUT = open(os.path.join(HERE, "rfx1_lead_check.out"), "w")
def say(s=""):
    print(s); OUT.write(s + "\n")

def track(F, mL, mMW, dt=0.1):
    """relative orbit back from today, d'' = -(1 + mL/mMW) g(|d|) d_hat, to the last apocentre (rfx1's equation)."""
    q = 1.0 + mL / mMW; x = np.array(XL0, float); v = np.array(VL0, float) * KMS; h = -dt
    def acc(x):
        r = float(np.linalg.norm(x)); return -q * F.gs(r) / r * x, r
    a, r = acc(x); T = [0.0]; V = [v / KMS]; Rr = [r]; phase = 0
    for k in range(1, 60001):
        v = v + 0.5 * h * a; x = x + h * v; a, r = acc(x); v = v + 0.5 * h * a
        if phase == 0 and r > Rr[-1] and k > 1: phase = 1
        elif phase == 1 and r < Rr[-1]: break
        T.append(k * dt); V.append(v / KMS); Rr.append(r)
    return np.array(T), np.array(V), np.array(Rr)

PUB = [("PP21 40-120 kpc", 32.0, 4.0, 56.0, -34.0), ("Yaaqib+24 50+ kpc", 40.0, 7.0, 38.0, -37.0),
       ("Chandra+24 100 kpc", 37.0, 9.0, -80.0, -59.0), ("Bystrom+25 >50 kpc", 34.0, 10.6, -72.7, -52.9),
       ("Li+26 50-120 kpc", 24.0, 3.8, -34.8, -37.8), ("Li+26 80-120 kpc", 44.0, 5.4, -28.3, -23.8)]
MB = H["M_b"](200.0)
CASES = [("R1 canonical", "canonical", M_L_R1, MB), ("R1 alt", "alt", M_L_R1, MB),
         ("R2 canonical", "canonical", 2.5e10, mdyn("canonical", 40.0)), ("R2 alt", "alt", 2.5e10, mdyn("alt", 40.0)),
         # C4, CONTEXT ONLY, BORROWED standard-model masses in the canonical field (rfx1 mutation M3's masses): is the
         # direction-matched comparison of C2 too tight for ANY LMC? No label, no verdict.
         ("C4 BORROWED context 1.5e11 / 1.0e12", "canonical", 1.5e11, 1.0e12),
         ("C4 BORROWED context 1.5e11 / 1.3e12", "canonical", 1.5e11, 1.3e12)]
say("RFX1 LEAD'S CHECK (after the result; not graded; changes no label)")
say(f"LMC today: toward (l, b) = ({lb(XL0)[0]:.1f}, {lb(XL0)[1]:.1f}) from the Galactic centre; "
    f"opposite its velocity: ({lb(-VL0)[0]:.1f}, {lb(-VL0)[1]:.1f})")
for name, ft, mL, mMW in CASES:
    mu = mL / (mMW + mL); T, V, Rr = track(FIELDS[ft], mL, mMW)
    VB = -mu * (V[0][None, :] - V); B = np.linalg.norm(VB, axis=1)
    say(""); say("=" * 100)
    say(f"{name}: m_L {mL:.3e}, m_MW {mMW:.3e}, mu {mu:.4f}; last apocentre {Rr[-1]:.1f} kpc at -{T[-1]:.0f} Myr")
    say("=" * 100)
    say("C1  window T [Myr]   B(T) [km/s]   toward (l, b)   angle to: " + " | ".join(p[0] for p in PUB))
    marks = [50, 100, 150, 200, 300, 400, 500, 750, 1000, 1500, T[-1]]
    for t in marks:
        if t > T[-1]: continue
        k = int(np.argmin(np.abs(T - t))); l, b = lb(VB[k])
        say(f"    {T[k]:8.0f}        {B[k]:6.2f}      ({l:7.1f}, {b:6.1f})   " + " | ".join(f"{sep(l, b, p[3], p[4]):5.1f}" for p in PUB)
            + ("   <- last apocentre (B_first)" if k == len(T) - 1 else ""))
    km = int(np.argmax(B)); l, b = lb(VB[km])
    say(f"    largest B(T) over the window: {B[km]:.2f} km/s at T = {T[km]:.0f} Myr, toward ({l:.1f}, {b:.1f}); "
        f"B_first {B[-1]:.2f}")
    say("C2  for each measurement: the window whose direction is closest to its apex, and the bound there")
    for p in PUB:
        ang = np.array([sep(*lb(VB[k]), p[3], p[4]) for k in range(1, len(T), 10)]); ks = np.arange(1, len(T), 10)
        kb = int(ks[int(np.argmin(ang))])
        say(f"    {p[0]:20s} measured {p[1]:4.1f} +/- {p[2]:4.1f}: closest direction at T = {T[kb]:5.0f} Myr "
            f"({ang.min():4.1f} deg off), bound there {B[kb]:5.2f} km/s, measured minus bound {(p[1] - B[kb]) / p[2]:+.1f} sigma_meas")
say(""); say("=" * 100)
say("C3  LMC1's rigid model (apex = minus its 50-80 kpc full-sky dipole vector), angle to each published apex")
say("=" * 100)
L1 = json.load(open(os.path.join(HERE, "..", "LMC1_lmc_pull_on_halo_stars", "lmc1_results.json")))
for ft in ("canonical", "alt"):
    for k in ("low", "central", "high"):
        d = L1["footings"][ft]["dip50"][k]; l, b = lb(-np.array(d["vec"]))
        say(f"    {ft:9s} {k:7s}: |d| {d['amp']:5.2f} km/s, apex ({l:7.1f}, {b:6.1f}); " + " | ".join(f"{p[0]} {sep(l, b, p[3], p[4]):5.1f}" for p in PUB))
say("")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()
