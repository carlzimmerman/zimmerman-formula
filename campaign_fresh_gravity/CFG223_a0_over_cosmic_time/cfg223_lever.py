#!/usr/bin/env python3
"""CFG223 POST HOC diagnostic (written after the main run; reported only, not frozen): why are the baryon-mass bands so wide?
For each point: the median y = g_bar / a0 (canonical), the local slope -d log10 nu / d log10 y of the kernel at that y, and the change of log10 s* per dex of baryon mass
from two small shifts (+-0.03 dex).  The implied a0 scale s* moves by about (dlog D per dex of baryon mass) / (local slope of log nu), so a slowly varying kernel (y of order 1 to 3) turns a small
error in D into a large error in a0.  LambdaCDM has no a0; author decompositions; not a detection; kappa = 1/2 FITTED."""
import os, sys, io, contextlib
sys.dont_write_bytecode = True
import numpy as np
LANE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(LANE, "cfg223_a0_over_time.py")).read()
stop = src.index('P("\\nCONTROLS")')
ns = {"__file__": os.path.join(LANE, "cfg223_a0_over_time.py"), "__name__": "cfg223_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:stop], "cfg223_a0_over_time.py", "exec"), ns)
build_points, implied, NU, A0L, nuv = ns["build_points"], ns["implied"], ns["NU"], ns["A0L"], ns["nuv"]
PTS, _, _ = build_points(mut=False)
OUT = []


def P(s=""):
    print(s); OUT.append(s)


P(__doc__.strip())
P("\n  point            n   median y   local slope -dlog(nu)/dlog(y)   dlog10 s*/d(baryon dex) (+-0.03 dex)   s* per +0.05 dex in D at fixed g_bar")
for p in PTS[:8]:
    y = np.median(p["gb"] / A0L)
    h = 0.02
    slope = -(np.log10(nuv(NU, np.array([y * 10 ** h]))[0]) - np.log10(nuv(NU, np.array([y * 10 ** (-h)]))[0])) / (2 * h)
    lp = float(implied(p["D"] * 10 ** (-0.03), p["gb"] * 10 ** 0.03, NU, A0L)[0][0]); lm = float(implied(p["D"] * 10 ** 0.03, p["gb"] * 10 ** (-0.03), NU, A0L)[0][0])
    d_s = (lp - lm) / 0.06
    l0 = float(implied(p["D"], p["gb"], NU, A0L)[0][0]); l5 = float(implied(p["D"] * 10 ** 0.05, p["gb"], NU, A0L)[0][0])
    P(f"  {p['short']:14s} {p['z'].size:3d}   {y:8.2f}   {slope:28.3f}   {d_s:+34.2f}   x {10 ** (l5 - l0):.2f}")
P("\nReading: the larger the change of log10 s* per dex of baryon mass, the more a small calibration error in D is amplified into a0; it is the slow variation of the kernel at y of order 1 to 3 (slope well below 1/2) that makes the statistical bars small and the baryon bands large.")
open(os.path.join(LANE, "cfg223_lever.out"), "w").write("\n".join(OUT) + "\n")
