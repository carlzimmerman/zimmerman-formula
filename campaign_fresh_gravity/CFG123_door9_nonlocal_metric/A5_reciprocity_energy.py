#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A5_reciprocity_energy -- G3 of CFG123_FROZEN_CRITERIA.md.

Which pass line applies (declared in the frozen file): in a diffeomorphism-invariant metric theory with universal minimal coupling there is no baryon-fluid exchange term; the
CFG48 G4 reaction line (<= 0.10 g_law over x in [0.3, 30]) is scored with reaction := |g_baryon - g_tot,mechanism| = 0 by construction (the whole force on baryons IS the metric's).
G3-a  conservation: the T0b residual of A1 (read from A1's results, exact 0).
G3-b  energy: E_eff = int rho_eff c^2 dV out to r_ta (rho_eff = m^2 Phi_N/(12 pi G), A1/A2) against (1/2) M_b V_f^2, V_f^4 = G M_b a0, in BOTH r_ta conventions
      (CFG48's Gcommon convention and B's committed CFG7_common.r_ta_law with nu_mono), both a0 footings, |E_eff| (the effective density is NEGATIVE).
The trap avoided (frozen text): reading 'reaction' as delta g itself would make G3 incompatible with G1 for x >= 0.5 (delta g/g_law of the target = 1 - 1/sqrt(1+x^2)); tabulated.
Pre-registered P6: reaction 0 by construction; E_eff/E_orb <= 1e-6 in both conventions (the frozen G3 text said 'hand estimate ~1e-10 or smaller'; the check below is the P6 line).
MUTATE: not applicable (exit 3).
"""
import os, sys, math, json
import numpy as np
from scipy.special import gammainc
from scipy.integrate import quad
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg123_common import *
import CFG7_common as C7
from Bcommon import G as GK, KPC_M

MUT = mutate_mode()
if MUT != "":
    print("A5: MUTATE mode", MUT, "not applicable"); sys.exit(3)
R = Report("A5_reciprocity_energy", MUT)
R.banner("A5 G3: reciprocity and energy")
lam, sol = rr_background()
mu = math.sqrt(lam)
CK = C_SI / 1e3                                                          # km/s
mK = mu * (H0_KMS_MPC / 1e3) / CK                                        # 1/kpc

# G3-a
p = os.path.join(HERE, "A1_localised_action_results.json")
if os.path.exists(p):
    j = json.load(open(p))
    t0b = [c for c in j["checks"] if c["name"].startswith("T0b")]
    R.check("G3-a: T0b (Noether/Bianchi identity, exact, A1) holds: the total stress is conserved once the auxiliary-field equations hold, universal coupling => no separate reaction", t0b[0]["detail"] if t0b else "missing", bool(t0b and t0b[0]["ok"]))
else:
    R.check("G3-a: A1 results present", "A1_localised_action_results.json missing (run A1 first)", False)
R.P("    reaction := |g_baryon - g_tot,mechanism| = 0 by construction (same metric for every species): the CFG44 N11/CFG48 G4 reaction line (<= 0.10 g_law) is met exactly, vacuously.")
R.P("    the trap: delta g/g_law of the TARGET = 1 - 1/sqrt(1 + x^2) at x = " + ", ".join(f"{x:g}: {1 - 1 / math.sqrt(1 + x * x):.3f}" for x in XGRID) + "; a naive 'reaction = delta g' reading would fail 0.10 for x >= 0.5, i.e. G3-naive and G1 could never both hold.")

# G3-b
import importlib.util
spec = importlib.util.spec_from_file_location("Gcommon", os.path.join(REPO, "campaign_fresh_gravity", "CFG48_gap1_switch", "Gcommon.py"))
Gc = importlib.util.module_from_spec(spec); spec.loader.exec_module(Gc)


def E_eff(M, rta_kpc, a0K, h=H_EXP_KPC):
    """int_0^{r_ta} rho_eff c^2 4 pi r^2 dr with rho_eff = m^2 Phi_N/(12 pi G), exponential sphere (kpc, km/s, Msun)."""
    f = lambda r: (mK ** 2 * (-GK * M * gammainc(3.0, r / h) / r - GK * M / (2 * h) * (1 + r / h) * math.exp(-r / h)) / (12 * math.pi * GK)) * CK ** 2 * 4 * math.pi * r * r
    return quad(f, 0, rta_kpc, limit=400, points=[h, 10 * h, 100 * h])[0]


R.P("\n  E_eff = int rho_eff c^2 dV (out to r_ta) versus (1/2) M_b V_f^2, V_f^4 = G M_b a0 (Msun (km/s)^2):")
R.P("  footing     M_b     r_ta(CFG48) r_ta(committed nu_mono) [kpc] | E_eff [Msun km2/s2] | E_orb | |E_eff|/E_orb (CFG48 / committed)")
worst = 0.0
rows = {}
for foot, a0_si in A0_FOOT.items():
    a0K = a0_si * KPC_M / 1e6
    for M in MASSES:
        rta48 = Gc.r_ta_kpc(M)
        rtac = 1e3 * float(C7.r_ta_law(M, C7.A0["canonical" if foot == "canonical" else "alt"], C7.nu_mono, 1.0))
        E48, Ec = E_eff(M, rta48, a0K), E_eff(M, rtac, a0K)
        Vf2 = math.sqrt(GK * M * a0K)
        Eorb = 0.5 * M * Vf2
        rows[(foot, M)] = (abs(E48) / Eorb, abs(Ec) / Eorb)
        worst = max(worst, abs(E48) / Eorb, abs(Ec) / Eorb)
        R.P(f"  {foot:9s}  {M:.0e}   {rta48:8.1f}   {rtac:9.1f}        | {E48:+.3e} / {Ec:+.3e} | {Eorb:.3e} | {abs(E48) / Eorb:.3e} / {abs(Ec) / Eorb:.3e}")
R.num("Eeff_over_Eorb_max", worst)
R.check("G3-b: |E_eff| <= (1/2) M_b V_f^2 in both r_ta conventions, both footings, all four masses (pass line 1)", f"max ratio {worst:.3e}", worst <= 1.0)
R.check("P6 (pre-registered): E_eff/E_orb <= 1e-6 in both conventions (hand estimate 'about 1e-10 or smaller')", f"max ratio {worst:.3e}", worst <= 1e-6)
R.verdict("G3 (reciprocity and energy)", "PASS (vacuous)" if worst <= 1.0 else "FAIL",
          f"reaction 0 by construction; |E_eff|/E_orb <= {worst:.2e}; the pass is a consequence of the mechanism being negligible (G1), not support")
sys.exit(finish(R, MUT))
