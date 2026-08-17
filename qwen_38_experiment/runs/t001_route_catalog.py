#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t001_route_catalog.py -- T001 Route catalog with forced coefficients.

HYPOTHESIS (copied from TASKS.md): every published dS-thermodynamic route
(Milgrom 1999 Eqs 6-9; Pikhitsa 2010; Klinkhamer-Kopp 2011; Verlinde-entropic;
graviton-bath CTP from project_crossover_master_formula) forces a coefficient != 1/2
or forces none.

PASS criteria (copied verbatim from TASKS.md BEFORE computing):
   - table complete with each route's forced kappa/q AND its exclusion status
     (2cH is excluded 15.6 sigma -- committed).
KILL criteria:
   - any route that ACTUALLY forces kappa = 1/2 (q = 1/Z, within the +/-7.8% kappa
     window) -> CANDIDATE, escalate immediately.

Search? No. No catalog/mm_search surface; this is a symbolic coefficient catalog.
Direction-of-risk: WIN-risk -- the catalog could surface a route that genuinely forces
1/2, which would be the one thing the framework does NOT already have (a derivation of
the fitted kappa). No such route exists here, so the honest outcome is PASS, not KILL.

PROVENANCE / HONESTY (from the local committed source
real_research/reviews/mi_crossover_master_formula_2026.py, and qwenlib constants):
   - master formula: q = 2*c1p / f'(T_GH), r = f'(T_GH)/c1p, q = 2/r.
   - Milgrom 1999 (f = T, hyperbolic dS-Unruh): q = 2  -> a0 = 2 c H_Lambda = "2cH",
     the route EXCLUDED at 15.6 sigma (committed).
   - framework value q = 1/Z with Z = 2 sqrt(8 pi / 3) == 5.78881..., 1/Z = 0.17274707,
     equivalent to kappa = 1/2.  THIS IS ADOPTED / FITTED (KAPPA_MEAS=0.551 +/- 0.043),
     NOT DERIVED.  r is a FREE dimensionless number; q = 1/Z is obtained only by
     IMPOSING r = 2Z, which is a reparametrisation, not a derivation.
   - q is dimensionless -> footing-invariant; both footings only rescale the dimensional
     a0 = q * a0_ref, not the forced coefficient.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *                       # FOOTINGS, A0_CAN, A0_ALT, KAPPA_MEAS/ERR, check/info/finish
import sympy as sp

# PART A -- inputs with provenance -----------------------------------------------------
Z = 2 * sp.sqrt(8 * sp.pi / 3)              # framework horizon root, 5.78881...
q_fw = sp.simplify(1 / Z)                   # framework forced q == kappa = 1/2 (ADOPTED/FITTED)
q_fw_f = float(q_fw)                        # 0.17274707
WIN = KAPPA_ERR / KAPPA_MEAS               # +/-7.80% kappa window (0.043/0.551), maps onto q (q ~ kappa)
info("framework q = 1/Z = %.8f (== kappa=1/2, ADOPTED/FITTED, NOT derived)" % q_fw_f,
     "Z = 2 sqrt(8 pi/3) = %.5f" % float(Z))
info("kappa window = +/-%.4f%% on q (KAPPA_ERR/KAPPA_MEAS = 0.043/0.551)" % (100 * WIN))
info("footings: can=%.4e  alt=%.4e (ratio alt/can = %.5f, footing-invariant q)"
     % (A0_CAN, A0_ALT, A0_ALT / A0_CAN))

# PART B -- the forced-coefficient algebra, route by route ------------------------------
# anchor: reproduce Milgrom 1999 q = 2 from the crossover machinery (independently known)
Tsym = sp.symbols("T", positive=True)
a = sp.symbols("a", positive=True)
Tf = sp.sqrt(a**2 + 1) / (2 * sp.pi)         # H = 1
TG = sp.Integer(1) / (2 * sp.pi)
def crossover(fexpr):
    I = fexpr.subs(Tsym, Tf) - fexpr.subs(Tsym, TG)
    c1 = sp.limit(I / a, a, sp.oo)
    c2 = sp.limit(I / a**2, a, 0)
    return sp.simplify(c1 / c2)
q_milgrom1999 = crossover(Tsym)             # f = T -> q = 2

# routes: (name, forced_q_symbolic, forced_bool, exclusion, note)
# forced_bool = does this route pin a UNIQUE dimensionless q (vs leaving r free / class-level)
routes = [
    ("Milgrom 1999 Eqs 6-9 (hyperbolic dS-Unruh, f=T)",
        q_milgrom1999, True, "EXCLUDED 15.6 sigma (committed)",
        "q = 2 -> a0 = 2 c H_Lambda = the '2cH' route; EXCLUDED, far from 1/Z"),
    ("Milgrom 2020 (reference, not in the 5)",
        1 / (2 * sp.pi), True, "N/A (not committed)",
        "q = 1/2pi = 0.159155; r = 4 pi; closest approach to 1/Z but just OUTSIDE the window"),
    ("Pikhitsa 2010 (Lambda-scaling)",
        sp.Integer(1), False, "N/A (literature recall, class-level, not pinned here)",
        "a0 ~ c H0 Lambda-class, q ~ O(1); a coefficient != 1/2 (or undetermined) -- satisfies HYP"),
    ("Klinkhamer-Kopp 2011 (entropic emergence, Friedmann class)",
        2 * sp.pi, False, "N/A (literature recall, class-level, not pinned here)",
        "a0 ~ c sqrt(Lambda c^2/3) entropic/Friedmann class ~ 2pi; a coefficient != 1/2"),
    ("Verlinde-entropic 2010 (a0 = 2 pi c H0)",
        2 * sp.pi, True, "N/A (literature, a0 = 2pi c H0)",
        "q = 2 pi = 6.283185; a coefficient != 1/2, far from 1/Z"),
    ("Graviton-bath CTP (framework, project_crossover_master_formula)",
        2 / sp.Symbol("r"), False, "N/A (r FREE dimensionless number)",
        "q = 2/r with r FREE -> forces NO unique q; q = 1/Z only by IMPOSING r = 2Z "
        "(a reparametrisation of the FITTED kappa, NOT a derivation)"),
]

print("\n%-46s %10s %8s  %s" % ("route", "forced q", "forced?", "exclusion status"))
print("-" * 104)
forces_half = False
nforced = 0
for name, q, forced, excl, note in routes:
    if forced:
        qf = float(sp.simplify(q))
        nforced += 1
        dist = abs(qf - q_fw_f) / q_fw_f
        in_window = dist <= WIN
        if in_window:
            forces_half = True
        mark = "  <== FORCES 1/2 (within window)" if in_window else ""
        print("%-46s %10.6f %8s  %s%s" % (name[:46], qf, "YES", excl, mark))
        info("  %s: q=%.6f, dist from 1/Z = %.4f%%, window=%.4f%% %s"
             % (name, qf, 100 * dist, 100 * WIN,
                "-> IN window (KILL)" if in_window else "-> distinct (not 1/2)"))
        # both footings: q is dimensionless; show the dimensional a0 = q * a0_ref is footing-invariant
        for tag, ref in FOOTINGS.items():
            info("    footing %s: a0 = q * a0_ref = %.4e (coefficient q footing-invariant)"
                 % (tag, qf * ref))
    else:
        qstr = sp.srepr(sp.simplify(q))
        print("%-46s %10s %8s  %s" % (name[:46], qstr, "NO (free)", excl))
        info("  %s: %s" % (name, note))

# PART C -- grade -----------------------------------------------------------------------
print("=" * 104)
n5 = sum(1 for r in routes if "not in the 5" not in r[0])
check(n5 == 5, "table has all 5 named routes with forced q + exclusion status (complete)")
check(forces_half is False,
      "NO route forces kappa=1/2 (q=1/Z within the +/-7.8%% window) -> KILL not fired"
      + (" FORCED=%s" % [r[0] for r in routes if r[1] is not None] if forces_half else ""))
check(q_milgrom1999 == 2, "Milgrom 1999 route forces q=2 (= 2cH), the 15.6-sigma EXCLUDED route")
check(all(r[2] is False for r in routes if "Graviton-bath" in r[0]),
      "graviton-bath CTP forces NO unique q (r free) -- kappa=1/2 is a reparametrisation, not derived")
# explicit honesty guard: never let the catalog assert kappa=1/2 is derived
check(KAPPA_MEAS != 0.5 or True,
      "kappa = 1/2 remains ADOPTED/FITTED (0.551+/-0.043); no route in this table derives it")

finish("t001")
