#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG313 PRE-FLIGHT -- reproduces the hand pre-flight of FROZEN_CRITERIA.md section 7 from the committed functions (no population is scored):
M_c(native) = M_* / f_b against h48's Moster halo_mass and CFG36's Mandelbaum M_200c, and the law's edge phantom per unit baryon mass against the
native cold share (Omega_c/Omega_b) = 5.364 (f_ex > 0 needs M_ph,edge / M_b < 5.364).
P1  CONTROL  f_b = 0.02237/(0.02237 + 0.1200) as CFG35's FB.
P2  the frozen ratios (two significant figures) reproduced.
P3  f_ex(native) = 0 at every pre-flight mass, both footings; f_ex(Moster) > 0 for the ultra-faint and classical masses (the committed rule bites there).
MUTATE=1: f_b x 0.5 -- P3 must still hold (the pre-flight's MUTATE prediction); P2 fails by design (the ratios double).
Run: python3 campaign_fresh_gravity/CFG313_native_collapse_mass/cfg313_preflight.py
"""
import os, sys, io, math, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("cfg313_preflight", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(LANES, "CFG36_colour_split_collapse.py")).read()
g = {"__file__": os.path.join(LANES, "CFG36_colour_split_collapse.py"), "__name__": "cfg36"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================================================ H1")], "CFG36", "exec"), g)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
FB = g["FB"] * (0.5 if MUTATE else 1.0); hm = g["g35"]["halo_mass"]; col = g["collapse"]; ep = g["edge_phantom"]
check("P1 CONTROL: f_b = 0.02237 / (0.02237 + 0.1200) (CFG35's FB)", f"f_b = {g['FB']:.6f}; (1 - f_b)/f_b = {(1 - g['FB']) / g['FB']:.4f}",
      abs(g["FB"] - 0.02237 / 0.14237) < 1e-15)
FROZEN = {1e3: 6.4e-6, 1e4: 6.4e-5, 1e6: 1.2e-3, 1e7: 4.6e-3, 1e8: 1.7e-2, 5e10: 0.16, 10 ** 11.5: 0.010}
FROZEN_MB = {(5e10, "blue"): 0.32, (5e10, "red"): 0.14, (10 ** 11.5, "red"): 0.039}
dev, rows = 0.0, []
for ms, fr in FROZEN.items():
    r = (ms / FB) / float(hm(ms)); rows.append(f"{ms:.1e}: {r:.2g}")
    dev = max(dev, abs(float(f"{r:.2g}") / fr - 1))
for (ms, c), fr in FROZEN_MB.items():
    r = (ms / FB) / col(ms, c); rows.append(f"{ms:.1e} {c}: {r:.2g}")
    dev = max(dev, abs(float(f"{r:.2g}") / fr - 1))
check("P2 the frozen native/Moster and native/Mandelbaum ratios reproduced (two significant figures)", "; ".join(rows) + f"; max relative deviation {dev:.2g}", dev < 1e-9)
fx_nat, fx_mos, rows = [], [], []
for ms in (1e3, 1e4, 1e6, 1e7, 1e8, 1e10, 5e10, 10 ** 11.5):
    for f in ("canonical", "alt"):
        ph = ep(ms, f, 0.40)
        fx_nat.append(max(0.0, 1 - ph / ((1 - FB) * ms / FB))); fx_mos.append((ms, max(0.0, 1 - ph / ((1 - g["FB"]) * float(hm(ms))))))
        if f == "canonical":
            rows.append(f"{ms:.0e}: M_ph,edge/M_b {ph / ms:.0f}")
check("P3 f_ex(native) = 0 at every pre-flight mass, both footings; f_ex(Moster) > 0 at M_* = 1e3-1e7",
      "; ".join(rows) + f"; native cold share {(1 - FB) / FB:.2f} M_b; max f_ex(native) {max(fx_nat):.3f}; f_ex(Moster) at 1e3-1e7 {min(x for m, x in fx_mos if m <= 1e7):.2f}-{max(x for m, x in fx_mos if m <= 1e7):.2f}",
      max(fx_nat) == 0.0 and all(x > 0 for m, x in fx_mos if m <= 1e7))
nf = R.write(here=HERE)
sys.exit(1 if nf else 0)
