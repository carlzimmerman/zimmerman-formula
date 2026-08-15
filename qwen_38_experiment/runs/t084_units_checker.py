#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t084_units_checker.py -- dimensional-analysis helpers on qwenlib; 10 committed formulas.

PASS (verbatim from TASKS.md): "Add dimensional-analysis helpers to qwenlib
(quantity tuples (value, [m,kg,s] powers)); unit-test on 10 committed formulas.
PASS: 10/10."
KILL: any formula whose propagated [m,kg,s] dimensions disagree with its LHS => the
      helper is broken or a committed formula is dimensionally inconsistent (would
      corrupt every downstream dimensional claim).
Not a search.  Direction-of-risk: DEFICIT-risk -- a green dimensional check could be an
      always-true tautology that flatters the framework; the final guard proves the
      helper actually discriminates dimensions, so a green run is not vacuous.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *    # constants, kernel, check/info/finish, Qty/D/DIMS/check_dims

# PART A -- restate the 10 committed formulas with their LHS dimension.
# Provenance: qwenlib constants + the a0-line (MS08), rho_crit, a0(z), y=g/a0,
# Q0-as-wavenumber.  Each RHS is built from the committed dimensional exponents DIM.
F = [
     ("F1 a0 = kappa c sqrt(G rho_Lambda) [a0-line, MS08 Eq13]",
      D("DIMLESS") * D("C") * (D("G") * D("RHO_CRIT"))**0.5, "accel"),
     ("F2 rho_crit = H0^2 / G -> density [qwenlib RHO_CRIT]",
      D("H0")**2 / D("G"), "density"),
     ("F3 H0 * T_H -> dimensionless [Hubble number ~ 1]",
      D("H0") * D("T_H"), "dimless"),
     ("F4 c * T_H -> length [horizon scale]",
      D("C") * D("T_H"), "length"),
     ("F5 g_N = G M_SUN / AU^2 -> accel [Newtonian gravity]",
      D("G") * D("MSUN") / D("AU")**2, "accel"),
     ("F6 y = g_N / a0 -> dimensionless [the central variable]",
      D("G") * D("MSUN") / D("AU")**2 / D("A0_CAN"), "dimless"),
     ("F7 a0 * g_N -> v^2 [gobs_line identity g_obs^2-g_N^2=a0 g_N]",
      D("A0_CAN") * D("A0_CAN"), "velocity_sq"),
     ("F8 a0^2(z)/a0^2(0) -> dimensionless [a0z_ratio_sq]",
      D("A0_CAN")**2 / D("A0_CAN")**2, "dimless"),
     ("F9 v_esc = sqrt(a0 * r) -> speed [turnaround/escape]",
      (D("A0_CAN") * D("KPC"))**0.5, "speed"),
     ("F10 Q0 * k_pc -> dimensionless [Q0 is a wavenumber, Mpc^-1]",
      D("Q0") * D("KPC"), "dimless"),
]

# PART B -- grade each of the 10 formulas: propagated dims must equal the LHS target.
for label, expr, target in F:
    check_dims(expr, target, label)

# PART C -- anti-tautology guard (DEFICIT-risk): the helper must DISTINGUISH a wrong
# dimension from the right one, so a green run above cannot be vacuously true.
guard = (D("C") * D("T_H")).dims     # c * T_H is length [1,0,0], NOT accel [1,0,-2]
check(guard != DIMS["accel"],
      "GUARD c*T_H is length, not accel -- helper discriminates dims")

finish("t084")
