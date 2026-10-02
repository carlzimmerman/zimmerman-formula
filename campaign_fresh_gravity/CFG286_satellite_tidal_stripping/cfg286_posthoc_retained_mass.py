#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG286 POST-HOC (labelled; written after the main and MUTATE runs; no verdict depends on it): WHY IS THE STRIPPING INERT?

Reads the committed main-run table cfg286_pericentres.csv (r_t, M_c per satellite) and reports, per population and footing, the fraction of
each satellite's collapse-debris mass that the frozen rule removes (1 - M_NFW(<r_t) / M_c, with r_t capped at R_200) beside the fraction
of the debris inside the estimator radius r_ev, M_NFW(<r_ev) / M_c.  The NFW helper is h48's committed nfw_enclosed (exec'd through
CFG45's prefix, read-only).  Satellites with f_ex = 0 carry no debris and are listed separately.
Run: python3 campaign_fresh_gravity/CFG286_satellite_tidal_stripping/cfg286_posthoc_retained_mass.py
"""
import sys
sys.dont_write_bytecode = True
import os, io, csv, math, json, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
_src = open(os.path.join(LANES, "CFG45_rule_readings.py")).read()
g45 = {"__file__": os.path.join(LANES, "CFG45_rule_readings.py"), "__name__": "cfg45_prefix"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_src.index("FLOORS = (1e8, 3e8, 1e9, 3e9, 1e10)")], "CFG45_rule_readings.py", "exec"), g45)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
nfw = g45["nfw_enclosed"]
RHO_C = g45["g36"]["RHO_C"]

lines = []
P = lambda s="": (print(s), lines.append(s))
P(__doc__.split("Run: python3")[0].strip())
fl = lambda v: float("inf") if v == "inf" else float(v)
out = {}
for foot in ("canonical", "alt"):
    P(f"\n  --- {foot} ---")
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "cfg286_pericentres.csv"))) if r["footing"] == foot]
    for pop in ("ufd", "ufd_ul", "cls", "m31", "col"):
        rs = [r for r in rows if r["pop"] == pop]
        removed, inside_ev, zero = [], [], []
        for r in rs:
            Mc, fex, rt, rev = fl(r["M_c"]), fl(r["fex"]), fl(r["r_t_kpc"]), fl(r["r_ev_kpc"])
            if fex == 0:
                zero.append(r["name"]); continue
            R200 = (3 * Mc / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0
            removed.append(1.0 - float(nfw(Mc, min(rt, R200))) / Mc)
            inside_ev.append(float(nfw(Mc, rev)) / Mc)
        removed, inside_ev = np.array(removed), np.array(inside_ev)
        out[f"{pop}|{foot}"] = dict(n=len(rs), n_fex0=len(zero), fex0=zero, removed_median=float(np.median(removed)) if len(removed) else None,
                                   removed_range=[float(removed.min()), float(removed.max())] if len(removed) else None,
                                   inside_rev_median=float(np.median(inside_ev)) if len(inside_ev) else None)
        if len(removed):
            P(f"    {pop:7s} n={len(rs):2d}: debris removed by stripping, median {np.median(removed):.1%} (range {removed.min():.1%}-{removed.max():.1%}); "
              f"debris inside r_ev, median {np.median(inside_ev):.2%} of M_c" + (f"; f_ex = 0 (no debris): {', '.join(zero)}" if zero else ""))
P("\n  Reading: the frozen truncation removes most of each satellite's collapse mass (its outer halo), but the dispersion is measured at r_ev,")
P("  inside which about 0.03-1 per cent of M_c sits (medians) and which lies well inside r_t; so the predicted dispersions do not move.  POST-HOC, not a verdict.")
json.dump(out, open(os.path.join(HERE, "cfg286_posthoc_retained_mass_POSTHOC_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg286_posthoc_retained_mass_POSTHOC.out"), "w").write("\n".join(lines) + "\n")
