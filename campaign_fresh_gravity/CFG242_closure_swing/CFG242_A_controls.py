#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG242_A_controls -- route A (L14a), stage 0: the REPRODUCTION CONTROLS of the frozen plan (CFG242_FROZEN_CRITERIA.md, section 4.2, gate order 0).

Frozen control (arm A1): late reaction/g_law 0.065 / 0.53 / 2.13 / 7.46 / 22.5 at x = 0.3 / 1 / 3 / 10 / 30 (pressure-slaved) and energy ratio
72.8 / 49.6 / 23.0 (CFG48 r_ta) and 318 / 179 / 57 (B's committed r_ta) at 1e9 / 1e10 / 1e12 Msun, within 1%; plus the CFG72 light-cone
width -> 0 control.  A failed control stops the arm.

This script recomputes the closed forms (a/g_law = theta^T_M / g_law with theta^T_M = (3/4) a0 [pressure] or (3/8) a0 (2+x^2)/(1+x^2)
[sigma], g_law = g_N sqrt(1+x^2) = a0 sqrt(1+x^2)/x^2; E_c/((1/2) M_b V_f^2) = 1.5 r_e/r_M with r_e = 0.4 r_ta, V_f^4 = G M_b a0) and compares
them with (i) the numbers frozen in section 4.2, (ii) the COMMITTED CFG72 / CFG70 results JSON (read-only; those lanes are not re-run here;
the committed numbers are the reference), and (iii) a forward-marched fluid equation (retarded exponential kernel, step target) for the
static limit.  Both footings are carried where it matters (the closed forms depend on a0 only through x).
MUTATE: not used here (the controls are reference checks).
"""
import os, sys, json, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.integrate import solve_ivp
import CFG242_common as C

R = C.Run("CFG242_A_controls")
P = R.P
P(__doc__.strip())

XS = (0.3, 1.0, 3.0, 10.0, 30.0)


def react_P(x):    # (3/4) a0 / g_law
    return 0.75 * x * x / math.sqrt(1 + x * x)


def react_S(x):    # (3/8) a0 (2+x^2)/(1+x^2) / g_law
    return 0.375 * (2 + x * x) / (1 + x * x) * x * x / math.sqrt(1 + x * x)


R.banner("C-A1  late-time reaction on the baryons, closed forms (r = 1 closed ledger)")
frozen = [0.065, 0.53, 2.13, 7.46, 22.5]
got = [react_P(x) for x in XS]
P("    x            " + "  ".join(f"{x:8.1f}" for x in XS))
P("    pressure     " + "  ".join(f"{v:8.4f}" for v in got) + "     (frozen: " + " / ".join(map(str, frozen)) + ")")
P("    sigma        " + "  ".join(f"{react_S(x):8.4f}" for x in XS))
R.check("C-A1 pressure-slaved reaction/g_law reproduces the frozen numbers to 1%", max(abs(g / f - 1) for g, f in zip(got, frozen)) < 0.01,
        f"max rel dev {max(abs(g / f - 1) for g, f in zip(got, frozen)):.2e}")
c72 = json.load(open(os.path.join(C.REPO, "campaign_fresh_gravity/CFG72_lightcone_exchange/cfg72_lightcone_exchange_results.json")))["numbers"]
rtP = c72["reaction_table"]["1e+09/point/P"]; rtS = c72["reaction_table"]["1e+09/point/S"]
dP = max(abs(a / b - 1) for a, b in zip(got, rtP)); dS = max(abs(react_S(x) / b - 1) for x, b in zip(XS, rtS))
R.check("C-A1b the closed forms equal the COMMITTED CFG72 'reaction_table' point-mass rows (the light-cone width -> 0 limit, 1e-13 in CFG72), P and S", dP < 1e-6 and dS < 1e-6,
        f"max rel dev P {dP:.1e}, S {dS:.1e}  (CFG72 committed values read, not re-run)")

R.banner("C-A2  energy ratio E_c(<r_e)/((1/2) M_b V_f^2) = 1.5 r_e/r_M in both r_ta conventions")
C7 = C.load_c7()
frozen48 = {1e9: 72.8, 1e10: 49.6, 1e12: 23.0}
frozenB = {1e9: 318.0, 1e10: 179.0, 1e12: 57.0}
c70 = json.load(open(os.path.join(C.REPO, "campaign_fresh_gravity/CFG72_lightcone_exchange/cfg72_lightcone_exchange_results.json")))["numbers"]["E1"]
ok48 = okB = True
rows = {}
for Mb in (1e9, 1e10, 1e12):
    rM = C.r_M_kpc(Mb)
    e48 = 1.5 * 0.4 * C.r_ta48_kpc(Mb) / rM
    eB_mono = 1.5 * 0.4 * 1e3 * float(C7.r_ta_law(Mb, C7.A0["canonical"], C7.nu_mono, 1.0)) / rM
    eB_p2 = 1.5 * 0.4 * 1e3 * float(C7.r_ta_law(Mb, C7.A0["canonical"], C7.nu_p2, 1.0)) / rM
    rows[f"{Mb:.0e}"] = dict(CFG48=e48, B_nu_mono=eB_mono, B_P2=eB_p2)
    ok48 &= abs(e48 / frozen48[Mb] - 1) < 0.01
    okB &= abs(eB_mono / frozenB[Mb] - 1) < 0.01 or abs(eB_p2 / frozenB[Mb] - 1) < 0.01
    cm = c70[f"{Mb:.0e}".replace("e+0", "e+0") + "/CFG48"]["point"] if f"{Mb:.0e}/CFG48" in c70 else float("nan")
    P(f"    M_b {Mb:.0e}: CFG48 {e48:7.2f} (frozen {frozen48[Mb]})   committed r_ta: nu_mono {eB_mono:7.1f}, P2 {eB_p2:7.1f} (frozen {frozenB[Mb]})")
R.check("C-A2 energy ratios in CFG48's r_ta reproduce 72.8 / 49.6 / 23.0 to 1%", ok48, str({k: round(v['CFG48'], 2) for k, v in rows.items()}))
R.check("C-A2b energy ratios in B's committed r_ta reproduce 318 / 179 / 57 to 1% (nu_mono or P2 kernel, as in CFG70's own wording)", okB,
        str({k: (round(v['B_nu_mono'], 1), round(v['B_P2'], 1)) for k, v in rows.items()}))
R.num("energy_ratios", rows)

R.banner("C-A3  forward-marched fluid equation: retarded exponential kernel, step target, static limit (theta' = (theta^T - theta - r/c)/tau)")
cc, tau, thT = 1.0, 0.7, 1.0          # numerical test data (units where the stiffness is 1); not model numbers
for r in (1.0, 0.0):
    sol = solve_ivp(lambda t, y: [(thT - y[0] - r / cc) / tau], (0, 60 * tau), [0.0], rtol=1e-11, atol=1e-13)
    th = sol.y[0, -1]
    a_over = -cc * (th - thT)            # a / theta^T_M at late time
    R.check(f"C-A3 late-time reaction / theta^T_M = r (r = {r:g})", abs(a_over - r) < 1e-6, f"{a_over:.8f}")
R.finish()
