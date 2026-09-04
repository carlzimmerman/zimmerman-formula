#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""f27 -- which liability rows are NEWTONIAN rather than MOND, and does SIZE order them?

THE HYPOTHESIS BEING TESTED, stated before the numbers.  f23/f24 show any one-kernel modified-gravity static limit
of the framework predicts a Solar-System quadrupole 6-9x the Cassini ceiling, and the repository's own lensing axis
kills modified inertia at ~20 sigma.  The one structure that passes both is a response with a finite COHERENCE LENGTH
xi: Newtonian for systems smaller than xi, MOND above it.  The Solar System (0.1 pc) and the Gaia wide binaries
(0.01-0.1 pc) would then be Newtonian -- Cassini passes, gamma_v = 1.00 in DR4 -- while discs (kpc) and dwarf
spheroidals (~0.3 kpc) keep the RAR.  Such a xi would have to sit between ~0.1 pc and ~200 pc.  Globular clusters
(r_h ~ 20 pc) are the systems on disk that straddle that range.  This file asks the liability ledger, row by row:
is the framework's miss on a row the miss of MOND against a NEWTONIAN system?  For each row B = log10(g_obs/g_MOND)
is carried; the Newtonian residual is B_N = B + log10 nu(y).  A row is 'Newtonian-side' when |B_N| < 0.15 and
|B_N| < |B|; 'MOND-side' when |B| < 0.15 and |B| < |B_N|; 'neither' otherwise.  Then: does a single size split
separate the two sides?  Every check can fail; the size-ordering check is a hypothesis check whose FAIL is a result.
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import *
from u10_ledger import ledger

ck = Check(); rng = np.random.default_rng(27)
rows = ledger("canonical", "iso")
rows_efe = {r["name"]: r for r in ledger("canonical", "published")}
P("=" * 118); P("f27 -- the Newtonian side of the ledger, ordered by size"); P("=" * 118)
P(f"  {'row':22s} {'class':8s} {'r [kpc]':>8s} {'log y':>6s} {'B_MOND':>7s} {'B_MOND,EFE':>11s} {'B_Newton':>9s}  side")
side = {}
for r in sorted(rows, key=lambda r: r["r_kpc"]):
    BN = r["B"] + math.log10(float(nu_s(r["y"])))
    Be = rows_efe[r["name"]]["B"]
    if abs(BN) < 0.15 and abs(BN) < abs(r["B"]): s = "NEWTON"
    elif abs(r["B"]) < 0.15 and abs(r["B"]) < abs(BN): s = "MOND"
    elif abs(Be) < 0.15 and abs(Be) < abs(BN): s = "MOND(EFE)"
    else: s = "neither"
    side[r["name"]] = (s, r["r_kpc"], r["B"], BN, Be)
    P(f"  {r['name']:22s} {r['cls']:8s} {r['r_kpc']:8.3f} {math.log10(r['y']):6.2f} {r['B']:+7.3f} {Be:+11.3f} {BN:+9.3f}  {s}")
gc = {n: side[n] for n in ("pal3", "pal4", "pal14", "ngc2419")}
n_newton_gc = sum(1 for v in gc.values() if v[0] == "NEWTON")
info("outer-halo globular clusters (r_h ~ 16-28 pc): " + "; ".join(f"{n}: {v[0]} (B_MOND {v[2]:+.2f}, B_N {v[3]:+.2f})" for n, v in gc.items()))
ck("G1 three of the four globular-cluster rows are NEWTONIAN-side: the framework over-predicts them by 0.2-0.9 dex "
   "while Newtonian gravity lands within 0.15 dex.  These are the ~20 pc systems", n_newton_gc >= 3, f"{n_newton_gc} of 4")
big_mond = [n for n, v in side.items() if v[1] > 0.2 and v[0].startswith("MOND")]
big_newton = [n for n, v in side.items() if v[1] > 0.2 and v[0] == "NEWTON"]
info(f"rows larger than 0.2 kpc: MOND-side {big_mond}; NEWTON-side {big_newton}")
ck("G2 (HYPOTHESIS CHECK -- a FAIL is a result) size orders the ledger: every Newtonian-side row is smaller than "
   "every MOND-side row.  If this fails, the coherence-length reading is not a clean statement about this ledger, "
   "and the clean sub-parsec probes (Cassini, done; Gaia DR4, pending) carry it alone",
   len(big_newton) == 0, f"Newtonian-side rows above 0.2 kpc: {big_newton}")
# AUC of Newtonian-side against log size, with a permutation null
lab = np.array([1.0 if side[r["name"]][0] == "NEWTON" else 0.0 for r in rows if side[r["name"]][0] != "neither"])
xr = np.array([math.log10(r["r_kpc"]) for r in rows if side[r["name"]][0] != "neither"])
def auc(x, y):
    pos, neg = x[y == 1], x[y == 0]
    return float(np.mean([(a < b) + 0.5*(a == b) for a in pos for b in neg]))       # 'smaller is Newtonian'
a_obs = auc(xr, lab); nulls = np.array([auc(xr, rng.permutation(lab)) for _ in range(5000)])
p = float(np.mean(nulls >= a_obs))
info(f"'smaller is Newtonian' AUC over {len(lab)} classified rows = {a_obs:.3f}, permutation p = {p:.3f}")
ck("G3 the tendency 'smaller systems are the Newtonian ones' is present but, on this ledger, is not significant on its "
   "own (this check records the strength: it PASSES only if p < 0.05)", p < 0.05, f"AUC {a_obs:.3f}, p = {p:.3f}")
P("\n  the two sub-parsec probes, for the record:")
P("    Solar System (0.1 pc): modified gravity with the framework's kernel gives 6.2-8.8x the Cassini ceiling (f23, f24); a")
P("      coherence length xi >> 0.1 pc makes the Solar System Newtonian and the quadrupole vanishes.")
P("    Gaia wide binaries (0.01-0.1 pc): the framework's pre-registered prediction is gamma_v = 1.16-1.23 (EFE on); a")
P("      coherence length predicts 1.00.  DR4 decides.  The Cassini <-> wide-binary lock is exactly this statement.")
sys.exit(ck.done())
