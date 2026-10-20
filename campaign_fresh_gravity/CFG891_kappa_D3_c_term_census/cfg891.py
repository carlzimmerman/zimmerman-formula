#!/usr/bin/env python3
"""CFG891: kappa door D3 -- census of every place c meets a0 in the record.

Criteria: FROZEN_CRITERIA.md (committed alone first). kappa = 1/2 is FITTED; this script derives nothing.
It encodes the frozen term table (section 3), classifies each relation symbolically (section 2), runs the
identity-by-construction checks K1-K11 (section 4) and, with CFG891_MUTATE=1, the mutation controls M1-M3
(section 6).

Run from anywhere:
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg891.py                  -> cfg891.out, cfg891_results.json, cfg891_scan.out
    CFG891_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg891.py  -> cfg891_MUTATE.out, cfg891_results_MUTATE.json
Normal run: exit 0 iff all K checks pass. MUTATE run: exit 1 iff every control bites (by design), 2 otherwise.
Reads only text files of the record (read-only) and the CFG894 register CSV. Writes only into this directory.
"""
import csv
import io
import json
import math
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG891_MUTATE", "") == "1"
OUT = io.StringIO()


def say(*a):
    print(*a, file=OUT)


# ----------------------------------------------------------------------------------------------------------
# Symbols. pi is tracked as the positive symbol PI so that its power (the pi-weight) can be read off.
# ----------------------------------------------------------------------------------------------------------
PI = sp.Symbol("PI", positive=True)
a0, c, G, hbar, kB = sp.symbols("a0 c G hbar k_B", positive=True)
kap = sp.Symbol("kappa", positive=True)         # the unknown solved for
kl = sp.Symbol("kappa_law", positive=True)      # the law's kappa (used only in DEF/ID rows)
M, s_, k_, tau, Gam = sp.symbols("M s k tau Gamma", positive=True)
# free / fitted / bounded record constants (any surviving one makes a row a TRADE)
alpha, f_, Cyt, yt, Ls, zq, D_, lam, Cb, kK, kH, kE, w0, xfree = sp.symbols(
    "alpha f C_yt y_t L_star Zq_over_beta2 D lambda_clock C_bare kappa_K k_H k_E w_0 x_free", positive=True)
FREE = {alpha, f_, Cyt, yt, Ls, zq, D_, lam, Cb, kK, kH, kE, w0, xfree}
CNU = sp.Float("0.64761")      # nu_mono phantom-field maximum (CFG893 K6), a transcendental kernel constant
I_B = sp.Float("0.4525")       # k04's kernel integral I (b = I/8pi), a transcendental kernel constant

TIER1 = {
    "TC14": "campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md",
    "TC14c": "campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14_CORRECTIONS_2026-10-16.md",
    "TC16": "campaign_fresh_gravity/THEORY_CANONICAL_2026-10-16.md",
    "TC18": "campaign_fresh_gravity/THEORY_CANONICAL_2026-10-18.md",
    "STAND": "campaign_fresh_gravity/STANDING_2026-10-09_law.md",
    "FE": "FRAMEWORK_EQUATIONS_2026-10-15.md",
    "MASTER": "sol61_push/cold_production_2026_10_11/MASTER_COLD_ENERGY_EQUATIONS.md",
    "C541e": "campaign_fresh_gravity/CFG541_cold_energy_equations_precise/EQUATIONS.md",
    "C541r": "campaign_fresh_gravity/CFG541_cold_energy_equations_precise/README.md",
    "C542a": "campaign_fresh_gravity/CFG542_dissipative_action/ACTION.md",
    "C542r": "campaign_fresh_gravity/CFG542_dissipative_action/README.md",
    "C638": "campaign_fresh_gravity/CFG638_cold_energy_fluid_equations/README.md",
    "C639": "campaign_fresh_gravity/CFG639_deficit_gated_mobility/README.md",
    "C893": "campaign_fresh_gravity/CFG893_kappa_from_cold_energy_structure/README.md",
    "C694": "campaign_fresh_gravity/CFG694_combined_construction/README.md",
    "C695": "campaign_fresh_gravity/CFG695_saturating_vacuum/README.md",
    "C770": "campaign_fresh_gravity/CFG770_cassini_stiff_action/README.md",
    "C807": "campaign_fresh_gravity/CFG807_stiff_vacuum_route/README.md",
    "C760": "campaign_fresh_gravity/CFG760_p_wave_gap/README.md",
    "C762": "campaign_fresh_gravity/CFG762_one_cP/README.md",
    "C775": "campaign_fresh_gravity/CFG775_bh_horizon_dark_energy/README.md",
    "C778": "campaign_fresh_gravity/CFG778_sealed_event_horizon_branch/README.md",
    "C187": "campaign_fresh_gravity/CFG187_aest_lambda_tie_candidate/README.md",
    "C43": "campaign_fresh_gravity/CFG43_fluid_tie/README.md",
    "KC": "kappa_closure/README.md",
    "XR20": "real_research/cross_thread_review_2026_09_26/XR20_README.md",
    "P63": "sonnet55_push/puzzle_32pi/p63_a0_field_coupling/FROZEN_CRITERIA.md",
    "CLK": "sol61_push/CLOCK_COEFFICIENT_BOUND.md",
    "VCLK": "sol61_push/VARIABLE_CLOCK_RESULTS.md",
    "VOFF": "sol61_push/VACUUM_OFFSET_SELECTION_RESULTS.md",
    "SCLK": "sol61_push/SPHERICAL_CLOCK_CONSTRAINTS_RESULTS.md",
    "C349": "campaign_fresh_gravity/CFG349_khronon_memory_switch/README.md",
    "C381": "campaign_fresh_gravity/CFG381_khronon_K_response/README.md",
    "C380": "campaign_fresh_gravity/CFG380_32pi_geometric_door/README.md",
    "C663": "campaign_fresh_gravity/CFG663_lensing_fork/README.md",
    "C847": "campaign_fresh_gravity/CFG847_lensing_slip_bound/README.md",
}

W_DATA = {"rho_DE": (0.227, 0.607), "rho_crit": (0.189, 0.501)}   # rules section 7 (2-sigma of CFG493)


# ----------------------------------------------------------------------------------------------------------
# The frozen term table (FROZEN_CRITERIA section 3). Each row: id, sources (Tier 1 keys), provenance, the
# relation (E = 0, a sympy Relational for inequalities, or None with a declared class), a natural posit
# (report-only) and the source's reason.
#   S: symbol namespace for one footing: rho (density), H (that footing's Hubble rate), FR (Friedmann
#      coefficient, H^2 = FR*G*rho), PIP (portal pi: PI normally, 1 under M1).
# ----------------------------------------------------------------------------------------------------------
def EQ(lhs, rhs):
    """lhs - rhs kept unevaluated, so that a ratio identity does not auto-cancel to 0 before it is classified."""
    return sp.Add(lhs, -rhs, evaluate=False)


def build_rows(S):
    rho, H, FR, PIP = S["rho"], S["H"], S["FR"], S["PIP"]
    Lam = 8 * PIP * G * rho / c**2                   # Lambda = 8 pi G rho / c^2 (the portal)
    RH = c / H                                        # Hubble / de Sitter radius
    q = a0 / (c * H)
    MH = c**3 / (2 * G * H)                           # horizon (Schwarzschild) mass
    Rstar = c / sp.sqrt(G * rho)                      # free-fall radius R* (J = G rho R*^2/c^2 = 1)
    rhoz, Hz, rloc = sp.symbols("rho_z H_z rho_loc", positive=True)
    rows = []

    def R(id_, src, prov, expr=None, declared=None, natural=None, reason="", ineq=False, deftag=False, carrier=None):
        rows.append(dict(id=id_, src=src, prov=prov, expr=expr, declared=declared, natural=natural,
                         reason=reason, ineq=ineq, deftag=deftag, carrier=carrier))

    # L: the law and its rewritings
    R("L01", ["TC14", "FE", "MASTER", "C541e", "TC16", "TC18", "STAND"], "held", a0 - kl * c * sp.sqrt(G * rho),
      deftag=True, reason="the law (kappa FITTED)")
    R("L02", ["TC14", "TC14c"], "target", rho * c**2 - 4 * a0**2 / G,
      reason="'equivalently rho_DE c^2 = 4 a0^2/G (C = 16 pi)': the fitted value restated (rules s2: G rho_L = 4 a0^2)")
    R("L03", ["MASTER", "KC"], "held", Lam * c**4 / a0**2 - 8 * PIP / kl**2, deftag=True,
      reason="Lambda c^4/a0^2 = 8 pi/kappa^2 (32 pi at kappa = 1/2 by choice)")
    R("L04", ["KC", "C380"], "held", c * H / a0 - sp.sqrt(FR) / kl, deftag=True, reason="Z = c H_L/a0")
    R("L05", ["FE", "C775"], "held", a0 / (c * H) - kl / sp.sqrt(FR), deftag=True, reason="q = a0/(c H_inf)")
    R("L06", ["KC"], "held", Lam * (c**2 / a0)**2 - 8 * PIP / kl**2, deftag=True, reason="Lambda l0^2 = 8 pi/kappa^2")
    R("L07", ["TC14", "TC14c"], "held", a0 - kl * c * H / sp.sqrt(FR), deftag=True,
      reason="alt footing a0 = kappa c sqrt(G rho_crit) = kappa sqrt(3/8pi) c H0; CFG833's 1/sqrt(Omega_L) by construction")
    R("L08", ["FE", "TC14", "C775"], "held",
      (kl * c * sp.sqrt(G * rhoz)) / a0 - sp.sqrt(rhoz / rho),
      reason="a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) (flat, tracking, DESI, BH-sourced)")
    R("L09", ["FE", "C187"], "held", a0 - kH * c * H, natural=a0 - c * H,
      reason="rival a0 proportional to H(z); normalisation k_H fitted")
    R("L10", ["FE", "C778"], "held", a0 - kE * c**2 / RH, natural=a0 - c**2 / RH,
      reason="event-horizon branch a0 proportional to c^2/R_E (pure-dS limit R_E = c/H_L; today R_E needs Omega_m)")
    # P: the portal (context)
    R("P01", ["MASTER"], "held", sp.Symbol("Lambda_eff") - 8 * PIP * G * rho / c**2,
      reason="Einstein equation with T^DE: rho_DE reaches c-geometry only as 8 pi G rho/c^2")
    # C: cold-energy sector
    Q = sp.Symbol("Q", positive=True)
    R("C01", ["C541e", "C542a", "MASTER", "C893"], "held", sp.Integer(0) + 3 * H * (1 + (-1)) * rho - Q / c**2,
      reason="exact-Lambda sink: w = -1 forces Q = 0 (a0-free)")
    R("C02", ["C893"], "held", declared="ID",
      reason="d ln a0/dt = Qbar/(2 eps_DE): an ODE whose integration constant is kappa (CFG893 R2)")
    R("C03", ["C541e"], "held", declared="INEQ",
      reason="sink bounds: d rho_DE/rho_DE <= 2.2e-6; local d a0/a0 <= 7e-9 if the energy leaves at c (numeric bounds)")
    R("C04", ["C541e", "C542a", "C893"], "held",
      sp.Le(sp.Symbol("v_s") / c, alpha * CNU * a0 / (c * sp.sqrt(4 * PI * G * rloc))), ineq=True,
      reason="drift causality |v_s| <= c (CFG893 R12)")
    R("C05", ["C893"], "posit", alpha * CNU * a0 / sp.sqrt(4 * PI * G * f_ * rho) - c,
      reason="H12: marginal causality at rho* = f rho_DE (added hypothesis)")
    R("C06", ["C541e"], "held", declared="ID",
      reason="damped psi wave: c is a propagation speed; a0 enters only through the source d(rho_ph(a0)); no equality relates them")
    R("C07", ["C541e", "C893"], "rejected", declared="REJ",
      reason="tau_psi = c/a0: a timescale identification, rejected (unstable; needs kappa > 379 at Delta_loc 1e5)")
    R("C08", ["C541e"], "rejected", sp.Symbol("tau_psi") - 1 / H, reason="tau_psi = 1/H0 (a0-free), rejected")
    phi_dot = sp.Symbol("phidot", positive=True)
    R("C09", ["C542a", "C542r"], "held", 3 * H * phi_dot - Q / phi_dot + c**2 * sp.Symbol("lap_phi"),
      reason="dark-energy scalar equation (a0-free)")
    R("C10", ["C541e", "C541r"], "held", declared="ID",
      reason="Cattaneo / damped-wave Hurwitz condition with K = ck/Gamma: c is a propagation speed")
    R("C11", ["C638"], "held", sp.Symbol("u_char") - sp.sqrt(3) * sp.Symbol("sigma"),
      reason="Israel-Stewart closure; characteristics u +- sqrt3 sigma << c (a0-free)")
    R("C12", ["C639"], "held", sp.Symbol("v_gate") + alpha * sp.Symbol("tau_ff") * sp.Symbol("grad_psi"),
      reason="deficit-gated mobility (c-free; CFG893 K7)")
    # S: the action S2 and the stiffened action
    u_ = sp.Symbol("u", positive=True)
    R("S01", ["TC14", "FE", "C694", "C695", "C770"], "held", 4 * PI * G * sp.Symbol("Wp") - u_**2 / (a0 - u_),
      reason="S2 field law K W' = u^2/(a0 - u), K = 4 pi G (c-free)")
    R("S02", ["C695", "C43"], "held", sp.Symbol("Sigma_ph") - a0 / (PI * G),
      reason="saturation u <= a0 gives Sigma_ph <= a0/(pi G) (c-free)")
    R("S03", ["C807", "C893", "KC", "VOFF"], "held", rho * c**2 - w0 * a0**2 / G,
      reason="vacuum zero mode: W_rem -> W_rem + W0 leaves the EL equations unchanged, so rho_DE c^2 = W0 = w0 a0^2/G has w0 free")
    R("S04", ["C807"], "posit", declared="ILL",
      reason="PAPER42 premise in S2: eps_W = -infinity, eps_Q = +infinity (CFG807 V1)")
    R("S05", ["C807", "TC14"], "posit", rho * c**2 - Cyt * a0**2 / (4 * PI * G),
      reason="vacuum with hand-set turn-off, C(y_t) ~ (pi/2) y_t - logs; C = 16 pi at y_t = 33.98")
    R("S06", ["C807"], "posit", yt - c**2 / (a0 * Ls),
      reason="y_t = c^2/(a0 L*): off by x1.7e8")
    R("S07", ["C694", "C760", "C762"], "held", declared="ID",
      reason="P-wave speed c_P = sqrt(gamma/I) is free; c_P = c is not in the record; no kappa equation")
    R("S08", ["C770"], "pending", declared="PEND", reason="covariant completion of the stiffness term on FRW (door D1)")
    Ia = 4 * PI**4 / 15
    R("S09a", ["KC"], "posit", rho * c**2 - 2 * Ia * a0**2 / (16 * PIP * G),
      reason="k01 K5: nu_RAR unsaturated-branch constant 4 pi^4/15 as vacuum energy, K_B = 0 (forbidden branch)")
    R("S09b", ["KC"], "posit", rho * c**2 - 2 * 2 * a0**2 / (16 * PIP * G),
      reason="k01 K5: exp-carrier constant 2 as vacuum energy, K_B = 0")
    R("S10", ["KC"], "posit", declared="ILL", reason="k02 sequestering average: five orders short")
    # B: black holes and horizons
    R("B01", ["FE", "C775"], "held", EQ(sp.sqrt(G * M / a0) / sp.sqrt((2 * G * M / c**2) * RH), 1 / sp.sqrt(2 * q)),
      natural=sp.sqrt(G * M / a0) / sp.sqrt((2 * G * M / c**2) * RH) - 1, reason="r_M/sqrt(r_s R_H) = 1/sqrt(2q)")
    R("B02", ["C775"], "held", EQ((a0 / (PI * G)) / (MH / (4 * PI * RH**2)), 8 * q),
      natural=(a0 / (PI * G)) / (MH / (4 * PI * RH**2)) - 1, reason="tether capacity / horizon surface density = 8q")
    R("B03", ["C775"], "held", EQ((a0 / (PI * G)) / (MH / (PI * RH**2)), 2 * q),
      natural=(a0 / (PI * G)) / (MH / (PI * RH**2)) - 1, reason="projected = 2q")
    R("B04", ["C775", "FE"], "held", EQ((c**4 / (4 * G * a0)) / MH, 1 / (2 * q)),
      natural=(c**4 / (4 * G * a0)) / MH - 1, reason="BH of surface gravity a0 / horizon mass = 1/(2q)")
    R("B05", ["C775", "FE"], "held", EQ(a0 / (c * H), q), natural=a0 / (c * H) - 1, reason="a0 / dS surface gravity = q")
    R("B06", ["C775"], "held", sp.Symbol("mN_over_MH") - 2 / (3 * sp.sqrt(3)), reason="Nariai mass / M_H (a0-free)")
    R("B07", ["C775", "TC14"], "held", a0**2 - kl**2 * c**2 * G * rho,
      reason="CCBH chain a0^2 = kappa^2 c^2 G Xi int psi a^-3 dt: the law with rho_DE identified")
    # R: relativistic completions and ties
    R("R01", ["C187", "XR20"], "target", a0 / c**2 - sp.Rational(1, 2) * sp.sqrt(Lam / (8 * PIP)),
      reason="AeST/HT tie alpha(Lambda) = kappa sqrt(Lambda/8pi) with kappa = 1/2 written in")
    R("R02", ["C187", "XR20"], "held", a0 - kK * c * 3 * H, natural=a0 - c * 3 * H,
      reason="tie to the aether/khronon expansion K = 3H (rival law), kappa_K free")
    Pcap = (sp.Rational(1, 4) / (8 * PIP)) * rho * c**2
    R("R03", ["C43"], "target", a0**2 - 8 * PIP * G * Pcap,
      reason="fluid cap P_cap = (kappa^2/8pi) rho_L c^2 = a0^2/(8 pi G), kappa = 1/2 written in (also G031)")
    R("R04", ["KC", "XR20", "P63"], "held", a0**2 / (G * rho * c**2) - 2 / (zq + 2 * I_B / (8 * PI)),
      reason="four-form: kappa^2 = 2 beta^2/(Z + 2 b beta^2), b = I/(8 pi) (k04 F2; AS651-658)")
    R("R05", ["XR20", "KC"], "held", declared="ID",
      reason="four-form feedback a0_loc/a0 = 1/(1 + (kappa^2/8pi) F(y)): defines a local a0 for every kappa")
    P0 = c * rho / (3 * H)
    R("R06", ["P63"], "pending", a0 - 4 * PI * G * P0, reason="p63 C1: saturated bound charge (unrun)")
    Zs = c * H / a0
    R("R07", ["P63"], "pending", (Zs / (1 + Zs)) * a0 - c * H / 2, reason="p63 C1b: patch bootstrap (unrun)")
    R("R08", ["P63"], "pending", declared="PEND", reason="p63 C2: flux lattice kappa = kappa1/N (MENU class)")
    R("R09", ["P63"], "pending", declared="PEND", reason="p63 C3: Kaloper-Sorbo hbar audit")
    Cclk = 4 * D_ * (1 + D_)**2 / (3 * (3 * lam - 1))
    R("R10", ["CLK", "VCLK"], "held", Lam * c**4 / a0**2 - Cclk,
      reason="canonical clock coefficient; BBN bound C > 1197.9 gives kappa < 0.145 in that construction")
    R("R11", ["VOFF", "VCLK"], "held", Lam * c**4 / a0**2 - Cb,
      reason="vacuum offset V0: C_bare spans every positive value")
    rU2 = c**2 / (G * sp.Symbol("U", positive=True))
    R("R12", ["SCLK"], "held", rU2 * Lam / c**2 - 16 * PI / sp.Symbol("S_star", positive=True),
      reason="density-length identity r_U^2 Lambda = 16 pi/S* (a0-free)")
    R("R13", ["C349"], "rejected", declared="REJ",
      reason="switch rate Gamma = a0/c (sensitivity only, 0/24 ON): a rate choice, no kappa equation")
    R("R14", ["XR20"], "held", declared="ILL",
      reason="alpha = a0/c^2 promoted to a free field switches MOND off (FP5 / XR20 D3)")
    R("R15", ["XR20"], "held", declared="ID",
      reason="T1e: a matter vacuum moves the observed Lambda but not a0 (tie to the HT constant only)")
    p_vac = -rho
    R("R16", ["XR20"], "held", a0 - kl * c * sp.sqrt(G * (rho - p_vac) / 2),
      reason="evolving-DE tie a0 ~ sqrt(V), V = (rho - p)/2, evaluated at w = -1")
    for tag, C in (("a", sp.Rational(1, 3)), ("b", sp.sqrt(3) / 6), ("c", sp.sqrt(3) / 3)):
        R("R17" + tag, ["C380"], "posit", a0 - C * c**2 * sp.sqrt(Lam),
          reason="CFG380 Lambda-geometry identification a0 = C c^2 sqrt(Lambda), C = %s (CHOSEN)" % C)
    Vol = 24 * PI**2 / Lam**2
    R("R18", ["C380"], "posit", a0 - c**2 / Vol**sp.Rational(1, 4),
      reason="CFG380 R4: a0 = c^2/Vol(S^4_Lambda)^(1/4) (CHOSEN; closest miss x2.56)")
    R("R19", ["KC"], "target", a0 - c**2 / (2 * Rstar),
      reason="free-fall surface gravity at R* = c/sqrt(G rho): J = 1 posited (rules s2), no SdS horizon at R* (k05 H1)")
    R("R20a", ["KC"], "posit", a0 - c * H, reason="k05 R2: dS horizon surface gravity")
    R("R20b", ["KC"], "posit", a0 - c**2 / (2 * RH), reason="k05 R2: Hubble sphere as its own Schwarzschild radius")
    R("R20c", ["KC"], "posit", a0 - c * H / (2 * PI), reason="k05 R2 / k03: Gibbons-Hawking as Unruh (the 0.461 form)")
    R("R20d", ["KC"], "posit", a0 - (4 * PI / 3) * G * rho * Rstar, reason="k05 R2: Newtonian ball of vacuum at R*")
    R("R20e", ["KC"], "posit", a0 - (8 * PI / 3) * G * rho * Rstar,
      reason="k05 R2: Newtonian ball with active mass |rho + 3p| = 2 rho")
    R("R21", ["KC"], "posit", hbar * a0 / (2 * PI * c * kB) - hbar * H / (2 * PI * kB),
      reason="T_Unruh(a0) = T_GH (hbar bookkeeping; algebraically R20a)")
    # X: lensing and relativistic lanes
    R("X01", ["MASTER"], "held", declared="ID",
      reason="weak-field metric with Phi/c^2, Psi/c^2; lensing probes Phi + Psi: c is a unit conversion")
    R("X02", ["MASTER"], "held", sp.Symbol("g_dyn") - sp.Symbol("g_lens") - sp.Symbol("g_s"),
      reason="additive non-lensing prescription (c-free)")
    R("X03", ["C847"], "held", declared="INEQ",
      reason="slip |Phi - Psi|/v_c^2 <= 2e-5 from sigma^2/c^2 and the law's field energy W (kappa-free numeric bound)")
    R("X04", ["C663"], "held", sp.Symbol("lens_resp") - sp.Symbol("dyn_resp"),
      reason="the response sector must lens (no a0-c relation)")
    R("X05", ["C381"], "held", sp.Symbol("ratio_K") - 2 * sp.Symbol("ac_over_c2") * (sp.Symbol("V") / c)**2,
      reason="khronon K response ratio (a0-free)")
    # M: microphysics (MASTER)
    R("M01", ["MASTER"], "held", sp.Symbol("Kforce") - G * a0, reason="K =? G a0 (c-free)")
    R("M02", ["MASTER"], "pending", declared="PEND",
      reason="nodal medium K = q_b^3 v/(2 N m* C^3 h^3) with v = c (door D4); TRADE + hbar expected")
    R("M03", ["MASTER"], "held", sp.Symbol("E_car") - sp.Symbol("m_car") * sp.Symbol("Q_car"),
      reason="carrier charge bound (c = 1 units, a0-free)")
    R("M04", ["MASTER"], "target", a0 - c * sp.sqrt(G * rho) / 2,
      reason="'desired identity' a0 =? (c/2) sqrt(G rho_DE): the target")
    # A: POST-FREEZE ADDITIONS (FROZEN_CRITERIA s1: found by reading the K9 scan lines after the first run;
    #    labelled, none removed; they cannot change N_pfdet or N_half by construction of their classes)
    rhoc, xi = sp.symbols("rho_c xi", positive=True)
    R("A01", ["C893"], "posit", rho * c**2 - rhoc * xi * sp.sqrt(G * M * a0),
      reason="POST-FREEZE. CFG893 R3 (H3): dark energy = accumulated settling energy, eps_DE = rho_DE c^2 = int Q dt (EXCLUDED there)")
    R("A02", ["C893"], "posit", sp.Rational(1, 100) * rho * c**2 - rhoc * xi * sp.sqrt(G * M * a0),
      reason="POST-FREEZE. CFG893 R4 (H4): the sink drives a 1% dark-energy evolution (EXCLUDED there)")
    R("A03", ["KC"], "posit", declared="ILL",
      reason="POST-FREEZE. k01 K3-K4: Lambda-free vacuum with the primitive's zero fixed by an empty Newtonian vacuum: "
             "negative sign and 0.4-0.7% of rho_L, so no real kappa")
    R("A04", ["KC"], "rejected", a0 - 2 * c * H,
      reason="POST-FREEZE. k03's note: Milgrom 1999's construction read as a0 = 2 c H_L (the temperature root), excluded")
    R("A05", ["C187"], "held", declared="ILL",
      reason="POST-FREEZE. CFG187 C2: without the HT multiplier Lambda's equation is local, Lambda ~ Y, so a0 varies in "
             "space (closure; the multiplier is what makes the tie global)")
    return rows


def planted_rows(S):
    """K11 classifier controls (excluded from every count)."""
    rho, H = S["rho"], S["H"]
    return [
        dict(id="K11_ineq", src=[], prov="held", expr=sp.Le(a0, c * H), declared=None, natural=None, reason="planted",
             ineq=True, deftag=False, carrier=None, expect="INEQ"),
        dict(id="K11_id", src=[], prov="held", expr=a0**2 - kl**2 * c**2 * G * rho, declared=None, natural=None,
             reason="planted", ineq=False, deftag=False, carrier=None, expect="ID"),
        dict(id="K11_H", src=[], prov="held", expr=a0 - c * H / 3, declared=None, natural=None, reason="planted",
             ineq=False, deftag=False, carrier=None, expect="H-ODD"),
        dict(id="K11_pf", src=[], prov="held", expr=rho * c**2 - 4 * a0**2 / G, declared=None, natural=None,
             reason="planted", ineq=False, deftag=False, carrier=None, expect="PF-RAT"),
        dict(id="K11_trade", src=[], prov="held", expr=a0 - xfree * c * sp.sqrt(G * rho), declared=None,
             natural=None, reason="planted", ineq=False, deftag=False, carrier=None, expect="TRADE"),
        dict(id="K11_hbar", src=[], prov="held", expr=a0 * hbar - c**2 * sp.sqrt(G * rho) * hbar**2, declared=None,
             natural=None, reason="planted", ineq=False, deftag=False, carrier=None, expect="HBAR"),
    ]


# ----------------------------------------------------------------------------------------------------------
# Classifier (FROZEN_CRITERIA section 2)
# ----------------------------------------------------------------------------------------------------------
def footing(name, PIP=PI, FR=None):
    rho = sp.Symbol("rho_DE" if name == "rho_DE" else "rho_crit", positive=True)
    H = sp.Symbol("H_L" if name == "rho_DE" else "H_0", positive=True)
    if FR is None:
        FR = 8 * PIP / 3
    return dict(name=name, rho=rho, H=H, FR=FR, PIP=PIP)


def pi_weight(expr):
    e = sp.powsimp(sp.expand_power_base(sp.simplify(expr), force=True), force=True)
    coeff, k = e.as_coeff_exponent(PI)
    if coeff.has(PI):
        return None, None
    return sp.nsimplify(coeff) if not coeff.atoms(sp.Float) else coeff, k


def solve_kappa(E, S):
    """Substitute the law (kappa unknown) and the footing's Friedmann relation, solve for kappa^2."""
    rho, H, FR = S["rho"], S["H"], S["FR"]
    Es = E.subs(H, sp.sqrt(FR * G * rho)).subs(a0, kap * c * sp.sqrt(G * rho))
    sols = [x for x in sp.solve(sp.Eq(Es, 0), kap) if x.is_positive is not False]
    return [sp.simplify(x**2) for x in sols]


def classify(row, S):
    rho, H, FR = S["rho"], S["H"], S["FR"]
    out = dict(id=row["id"], prov=row["prov"], src=row["src"], reason=row["reason"], k2=None, pi_weight=None,
               hbar_weight=0, value=None, free=[], natural=None, carrier=None)
    if row["declared"] is not None:
        out["cls"] = row["declared"]
        out["declared"] = True
        return out
    out["declared"] = False
    E = row["expr"]
    fs = E.free_symbols
    has_c = bool(fs & {c, H}) or (row["ineq"] and bool(fs & {c, H}))
    if a0 not in fs or not has_c:
        out["cls"] = "NA"
        return out
    out["carrier"] = "H" if H in fs else "rho"
    if row["ineq"]:
        out["cls"] = "INEQ"
        return out
    # identity test with the law's kappa symbolic
    Eid = E.subs(H, sp.sqrt(FR * G * rho)).subs(a0, kl * c * sp.sqrt(G * rho))
    if sp.simplify(Eid) == 0:
        out["cls"] = "DEF" if row["deftag"] else "ID"
    else:
        sols = solve_kappa(E, S)
        if not sols:
            out["cls"] = "NOSOL"
        else:
            k2 = sols[0]
            out["k2"] = str(k2).replace("PI", "pi")
            out["k2_sym"] = k2
            fk = k2.free_symbols - {PI}
            out["free"] = sorted(str(x) for x in fk)
            if fk & {hbar, kB}:
                out["cls"] = "HBAR"
                out["hbar_weight"] = int(sp.degree(sp.numer(sp.together(k2)), hbar) -
                                         sp.degree(sp.denom(sp.together(k2)), hbar))
            elif fk & FREE:
                out["cls"] = "TRADE"
            elif fk:
                out["cls"] = "MASS"
            elif k2.atoms(sp.Float):
                out["cls"] = "CONT"
                out["value"] = float(sp.sqrt(k2.subs(PI, sp.pi)))
            else:
                coeff, w = pi_weight(k2)
                out["pi_weight"] = int(w) if w is not None else None
                out["value"] = float(sp.sqrt(k2.subs(PI, sp.pi)))
                if w == 0:
                    out["cls"] = "PF-RAT" if sp.nsimplify(coeff).is_rational else "PF-ALG"
                elif out["carrier"] == "H":
                    out["cls"] = "H-ODD" if int(w) % 2 else "H-EVEN"
                else:
                    out["cls"] = "RHO-PI"
                out["k2_exact_quarter"] = bool(sp.simplify(k2 - sp.Rational(1, 4)) == 0)
    if E.has(hbar):
        out["hbar_in_relation"] = True
    if row["natural"] is not None:
        ns = solve_kappa(row["natural"], S)
        if ns:
            k2n = ns[0]
            cn, wn = pi_weight(k2n)
            out["natural"] = dict(k2=str(k2n).replace("PI", "pi"), pi_weight=int(wn) if wn is not None else None,
                                  value=float(sp.sqrt(k2n.subs(PI, sp.pi))))
    return out


def counts(cl):
    det_pf = [r for r in cl if r["cls"] in ("PF-RAT", "PF-ALG") and r["prov"] in ("held", "posit", "rejected")]
    half = [r for r in det_pf if r.get("k2_exact_quarter")]
    wi_half = [r for r in cl if r["cls"] in ("PF-RAT", "PF-ALG") and r["prov"] == "target" and r.get("k2_exact_quarter")]
    n_c = [r for r in cl if r["cls"] != "NA"]
    if half:
        outcome = "EXACT-1/2 AVAILABLE"
    elif det_pf:
        outcome = "pi-FREE BUT NOT 1/2"
    else:
        outcome = "NONE CAN"
    return dict(N_c=len(n_c), N_pfdet=len(det_pf), N_half=len(half), N_live=len(half), N_wi_half=len(wi_half),
                pfdet_ids=[r["id"] for r in det_pf], half_ids=[r["id"] for r in half],
                wi_half_ids=[r["id"] for r in wi_half], outcome=outcome)


def run_census(S, extra=None):
    rows = build_rows(S) + (extra or [])
    cl = [classify(r, S) for r in rows]
    return rows, cl, counts(cl)


# ----------------------------------------------------------------------------------------------------------
# Tier 1 scan (K9) and Tier 2/3 register (K10)
# ----------------------------------------------------------------------------------------------------------
A0_RE = re.compile(r"(a₀|a0|a_0|a_\{0\})")
C_RE = re.compile(r"((^|[^A-Za-z_])c([^A-Za-z_]|$)|c²|c\^|cH|Λ|Lambda|H∞|H_|H₀|H0|horizon|R_E|R_H|ρ_DE|rho_DE|rm DE)")


def scan_tier1():
    per, lines = {}, []
    for key, rel in TIER1.items():
        path = os.path.join(ROOT, rel)
        n = 0
        with open(path, encoding="utf-8") as fh:
            for i, ln in enumerate(fh, 1):
                if A0_RE.search(ln) and C_RE.search(ln):
                    n += 1
                    lines.append("%s:%d: %s" % (rel, i, ln.strip()[:220]))
        per[key] = n
    return per, lines


VOID_KEYS = ("VOID", "CONDITIONAL", "RETRACTED", "WITHDRAWN", "DISCARD", "MENU", "NUMEROLOGY")
TIER2_EXTRA = (["K515", "K507", "K508", "K506", "K492", "K486", "K487", "K580", "K208", "K594", "K079", "K375",
                "K345", "K574", "K416", "K418", "K126", "K127", "K128"]
               + ["K%03d" % i for i in range(538, 546)] + ["K%03d" % i for i in range(69, 73)]
               + ["K%03d" % i for i in range(232, 237)])


def d3_from_register(r):
    cls, v = r["cls"], r["verdict"].upper()
    if cls == "odd":
        return "H-ODD"
    if cls == "any":
        return "RHO (density route)"
    if cls == "cont":
        return "CONT"
    if cls == "menu":
        return "MENU"
    if cls == "pend":
        return "PEND"
    if cls in ("audit", "lean", "obs", "nk"):
        return "not a trial (%s)" % cls
    # descriptive mapping only (enters no count and not the verdict); word-boundary match so that
    # "boundary" is not read as "BOUND" (post-run refinement, disclosed in the README)
    v = " " + re.sub(r"[^A-Z0-9/ -]", " ", v) + " "
    for keys, lab in ((("VOID", "CIRCULAR"), "VOID"), (("CONDITIONAL",), "CONDITIONAL"), (("BOUND",), "INEQ"),
                      (("TRADE", "FREE RATIO", "FREE", "FIT"), "TRADE/FREE"),
                      (("IDENTITY", "CONDITION", "TIED", "HOMOGENEITY", "IDENTICAL"), "ID/CONDITION"),
                      (("CLOSURE", "NO-GO", "NOT SELECTED", "EXCLUDED", "FAIL", "BLOCKED", "CLOSED", "DEAD", "MISS",
                        "DOES NOT", "NOT LIVE", "SLOT"), "CLOSURE")):
        if any(re.search(r"(?<![A-Z])" + re.escape(k) + r"(?![A-Z])", v) for k in keys):
            return lab
    return "OTHER (no number)"


def register():
    path = os.path.join(ROOT, "campaign_fresh_gravity/CFG894_kappa_campaign_ledger/kappa_attempts_register.csv")
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    t2 = [r for r in rows if ("sol61_push" in r["path"] and re.search("32pi", r["path"], re.I))
          or r["kid"] in TIER2_EXTRA]
    t3 = [r for r in rows if r["half"] == "1"]
    return rows, t2, t3


# ----------------------------------------------------------------------------------------------------------
# Checks K1-K11
# ----------------------------------------------------------------------------------------------------------
def k1_forbidden():
    me = open(os.path.abspath(__file__), encoding="utf-8").read().splitlines()
    forb = ["9.36e-11", "9.3603e-11", "1.13e-10", "1.1312e-10", "1.2e-10", "0.417", "0.465", "0.551", "5.7888", "0.1727", "5.364"]  # I1-LIST
    hits = [(i + 1, s) for i, ln in enumerate(me) if "# I1-LIST" not in ln for s in forb if s in ln]
    return hits


def main():
    say("CFG891 -- kappa door D3: census of every place c meets a0 in the record")
    say("kappa = 1/2 FITTED (CFG493). Footings never pooled. No derivation attempted. Not theory closed.")
    say("mode:", "MUTATE" if MUTATE else "normal")
    say("")
    S_DE = footing("rho_DE")
    S_CR = footing("rho_crit")
    rows, cl, cnt = run_census(S_DE)
    checks = {}

    if not MUTATE:
        # ---------------- the table
        say("== Tier 1 census (rho_DE footing; classes identical on rho_crit, K6) ==")
        say("%-6s %-8s %-9s %-10s %-26s %-6s %-9s %s" % ("id", "prov", "class", "carrier", "kappa^2", "pi-w", "kappa",
                                                          "natural (report-only)"))
        for r in cl:
            nat = ""
            if r.get("natural"):
                nat = "k2=%s w=%s k=%.4f" % (r["natural"]["k2"], r["natural"]["pi_weight"], r["natural"]["value"])
            k2 = r["k2"] or ""
            if r["cls"] == "TRADE":
                k2 = k2 + "  [free: %s]" % ",".join(r["free"])
            val = "%.4f" % r["value"] if r["value"] is not None else ""
            say("%-6s %-8s %-9s %-10s %-26s %-6s %-9s %s" % (r["id"] + ("+" if r["id"].startswith("A0") else ""), r["prov"], r["cls"] + ("*" if r["declared"] else ""),
                                                              r["carrier"] or "", k2, "" if r["pi_weight"] is None else r["pi_weight"],
                                                              val, nat))
        say("(* = declared class, no symbolic kappa form; reason in the JSON. + = post-freeze addition, labelled)")
        say("")
        hist = {}
        for r in cl:
            hist[r["cls"]] = hist.get(r["cls"], 0) + 1
        say("class histogram:", json.dumps(dict(sorted(hist.items()))))
        say("counts:", json.dumps({k: v for k, v in cnt.items()}))
        say("")
        say("determinate values against W_data (report only, no evidential weight):")
        for r in cl:
            if r["value"] is not None:
                lo, hi = W_DATA["rho_DE"]
                say("  %-6s %-8s %-7s kappa = %.4f  %s" % (r["id"], r["prov"], r["cls"], r["value"],
                                                           "inside" if lo <= r["value"] <= hi else "outside"))
        say("")

        # ---------------- K1
        h = k1_forbidden()
        checks["K1_forbidden_constants"] = (len(h) == 0, "hits: %s" % h)
        # ---------------- K2 (printed above); record that every determinate row printed its kappa^2 and free list
        det = [r for r in cl if r["k2"] is not None]
        checks["K2_symbolic_kappa2_printed"] = (all(r["k2"] for r in det), "%d rows with a solved kappa^2" % len(det))
        # ---------------- K3 scaling
        lG, mu, nu = sp.symbols("lG mu nu", positive=True)
        bad = []
        rho, H = S_DE["rho"], S_DE["H"]
        for row, r in zip(rows, cl):
            if r["k2"] is None:
                continue
            E = row["expr"]
            Esc = E.subs({G: lG * G, rho: mu * rho, c: nu * c, a0: nu * sp.sqrt(lG * mu) * a0, H: sp.sqrt(lG * mu) * H},
                         simultaneous=True)
            if Ls in E.free_symbols:
                Esc = Esc.subs(Ls, Ls * nu / sp.sqrt(lG * mu))  # L* scales like c/sqrt(G rho)
            rc_ = sp.Symbol("rho_c", positive=True)
            Esc = Esc.subs({M: M * nu**3 / (lG * sp.sqrt(lG * mu)), rc_: mu * rc_}, simultaneous=True)  # mass ~ c^3/(G H)
            ks = solve_kappa(Esc, S_DE)
            if not ks or sp.simplify(ks[0] - r["k2_sym"]) != 0:
                bad.append(r["id"])
        checks["K3_scaling_invariance"] = (len(bad) == 0, "non-invariant: %s" % bad)
        # ---------------- K4 rename test
        bad_id, wi_res = [], []
        for row, r in zip(rows, cl):
            if row["declared"] is not None or row["ineq"] or row["expr"] is None:
                continue
            E = row["expr"].subs(H, sp.sqrt(S_DE["FR"] * G * rho))
            E4 = sp.simplify(E.subs(kl, sp.Rational(2, 5)).subs(a0, sp.Rational(2, 5) * c * sp.sqrt(G * rho)))
            if r["cls"] in ("DEF", "ID"):
                if E4 != 0:
                    bad_id.append(r["id"])
            if r["prov"] == "target" and r.get("k2_exact_quarter"):
                wi_res.append((r["id"], "fails at kappa_law = 2/5 (restates the law)" if E4 != 0 else "STILL HOLDS"))
        ok4 = (len(bad_id) == 0) and all(x[1].startswith("fails") for x in wi_res)
        checks["K4_rename_test"] = (ok4, "DEF/ID broken: %s; WI rows: %s" % (bad_id, wi_res))
        # ---------------- K5 Friedmann tautology
        Zsq = sp.simplify(((c * H) / (sp.Rational(1, 2) * c * sp.sqrt(G * rho)))**2 - 32 * PI / 3)
        Zsq = sp.simplify(Zsq.subs(H, sp.sqrt(S_DE["FR"] * G * rho)))
        l04 = [r for r in cl if r["id"] == "L04"][0]
        checks["K5_Friedmann_tautology"] = (Zsq == 0 and l04["cls"] == "DEF",
                                            "Z^2 - 32pi/3 at kappa=1/2 -> %s for every rho; L04 class %s" % (Zsq, l04["cls"]))
        # ---------------- K6 footings
        _, cl2, cnt2 = run_census(S_CR)
        same = [a["cls"] for a in cl] == [b["cls"] for b in cl2]
        checks["K6_footings_identical_classes"] = (same and cnt2["N_half"] == cnt["N_half"] and
                                                   cnt2["N_pfdet"] == cnt["N_pfdet"],
                                                   "rho_crit counts %s" % json.dumps({k: cnt2[k] for k in ("N_c", "N_pfdet", "N_half")}))
        # ---------------- K7 hbar bookkeeping
        r21 = [r for r in cl if r["id"] == "R21"][0]
        hb_rows = [r["id"] for r in cl if r["cls"] == "HBAR"]
        checks["K7_hbar"] = (r21["cls"] == "H-ODD" and r21.get("hbar_in_relation") and not hb_rows,
                             "R21 (hbar in relation) -> %s, hbar cancels; HBAR rows in census: %s; no un-ratioed 1/4" % (r21["cls"], hb_rows))
        # ---------------- K8 pi-parity
        m, rr = sp.Symbol("m", integer=True), sp.Symbol("r", positive=True)
        k2g = sp.simplify((rr * PI**m * c * sp.sqrt(S_DE["FR"] * G * rho) / (c * sp.sqrt(G * rho)))**2)
        k2g = sp.powsimp(sp.expand_power_base(k2g, force=True), force=True)
        base_, expo = sp.powsimp(k2g / (sp.Rational(8, 3) * rr**2), force=True).as_base_exp()
        expo = expo if base_ == PI else sp.nan
        parity = sp.Mod(expo, 2)
        hrows = [(r["id"], r["pi_weight"]) for r in cl if r["carrier"] == "H" and r["pi_weight"] is not None]
        checks["K8_pi_parity"] = (sp.simplify(expo - (2 * m + 1)) == 0 and parity == 1 and all(w % 2 == 1 for _, w in hrows),
                                  "a0 = r pi^m c H => kappa^2 = (8/3) r^2 pi^(%s), (mod 2) = %s; H-type rows %s" % (expo, parity, hrows))
        # ---------------- K9 coverage
        per, hitlines = scan_tier1()
        cited = set(k for row in rows for k in row["src"])
        uncited = [k for k in TIER1 if k not in cited]
        withhits_uncited = [k for k in TIER1 if per[k] > 0 and k not in cited]
        checks["K9_coverage"] = (not uncited, "files %d, with hits %d, total hit lines %d; uncited files: %s" % (
            len(TIER1), sum(1 for k in per if per[k] > 0), sum(per.values()), uncited))
        with open(os.path.join(HERE, "cfg891_scan.out"), "w", encoding="utf-8") as fh:
            fh.write("CFG891 Tier 1 scan: lines where an a0 token and a c-carrier token co-occur (read-only text scan)\n")
            for k in TIER1:
                fh.write("%-6s %3d  %s\n" % (k, per[k], TIER1[k]))
            fh.write("\n")
            fh.write("\n".join(hitlines) + "\n")
        # ---------------- K10 register
        allrows, t2, t3 = register()
        t2map = [(r["kid"], r["src"], r["cls"], r["half"], d3_from_register(r), r["kappa"], r["verdict"]) for r in t2]
        live_t2 = [x for x in t2map if (x[2] in ("odd", "any", "cont") and x[5] and abs(float(x[5]) - 0.5) < 1e-12)
                   or (x[3] == "1" and not any(k in x[6].upper() for k in VOID_KEYS))]
        t3_bad = [r["kid"] for r in t3 if not any(k in r["verdict"].upper() for k in VOID_KEYS)]
        checks["K10_register"] = (len(t2) > 0 and not live_t2 and not t3_bad,
                                  "Tier 2 rows %d (sol61 32pi %d + door starts %d); live candidates %s; Tier 3 half=1 rows %d, un-voided %s" % (
                                      len(t2), sum(1 for r in t2 if "sol61_push" in r["path"] and re.search("32pi", r["path"], re.I)),
                                      sum(1 for r in t2 if not ("sol61_push" in r["path"] and re.search("32pi", r["path"], re.I))),
                                      live_t2, len(t3), t3_bad))
        # ---------------- K11 classifier controls
        pc = [(p["id"], p["expect"], classify(p, S_DE)["cls"]) for p in planted_rows(S_DE)]
        checks["K11_classifier_controls"] = (all(e == g for _, e, g in pc), "%s" % pc)

        say("== Tier 2 (register rows in scope) ==")
        h2 = {}
        for x in t2map:
            h2[x[4]] = h2.get(x[4], 0) + 1
        say("D3 class histogram:", json.dumps(dict(sorted(h2.items()))))
        for x in t2map:
            if x[2] in ("odd", "any", "cont", "menu") or x[3] == "1":
                say("  %-5s %-12s cls=%-5s half=%s kappa=%-6s %s | %s" % (x[0], x[1], x[2], x[3], x[5], x[4], x[6][:90]))
        say("Tier 3: %d rows with half = 1 in the whole register; all carry a void-type verdict: %s" % (len(t3), not t3_bad))
        say("")
        say("== Checks ==")
        allok = True
        for k, (ok, msg) in checks.items():
            allok &= bool(ok)
            say("[%s] %s: %s" % ("PASS" if ok else "FAIL", k, msg))
        say("")
        say("== Verdict (frozen section 5) ==")
        say("N_c = %d, N_pfdet = %d %s, N_half = N_live = %d, N_wi_half = %d %s" % (
            cnt["N_c"], cnt["N_pfdet"], cnt["pfdet_ids"], cnt["N_half"], cnt["N_wi_half"], cnt["wi_half_ids"]))
        say("OUTCOME:", cnt["outcome"])
        say("kappa = 1/2 FITTED; not theory closed.")
        res = dict(mode="normal", counts=cnt, counts_rho_crit=cnt2, checks={k: [bool(v[0]), v[1]] for k, v in checks.items()},
                   rows=[{k: v for k, v in r.items() if k != "k2_sym"} for r in cl],
                   tier2=[dict(kid=x[0], src=x[1], cls=x[2], half=x[3], d3=x[4], kappa=x[5]) for x in t2map],
                   tier3_unvoided=t3_bad, scan_per_file=per)
        write("cfg891.out", "cfg891_results.json", res)
        return 0 if allok else 1

    # ------------------------------------------------------------------ MUTATE controls (section 6)
    say("== baseline ==", json.dumps({k: cnt[k] for k in ("N_c", "N_pfdet", "N_half", "outcome")}), cnt["pfdet_ids"])
    # M1: portal pi removed (8 pi -> 8 in H, Lambda and S09's normalisation)
    S_M1 = footing("rho_DE", PIP=sp.Integer(1))
    _, cl1, c1 = run_census(S_M1)
    r18 = [r for r in cl1 if r["id"] == "R18"][0]
    m1 = c1["N_pfdet"] > cnt["N_pfdet"] and r18["cls"] not in ("PF-RAT", "PF-ALG")
    say("M1 portal 8pi -> 8:", json.dumps({k: c1[k] for k in ("N_c", "N_pfdet", "N_half", "outcome")}), c1["pfdet_ids"],
        "| R18 ->", r18["cls"], r18["k2"], "|", "BITES" if m1 else "DOES NOT BITE")
    # M2: planted live row
    plant = dict(id="M2_plant", src=[], prov="held", expr=S_DE["rho"] * c**2 - 4 * a0**2 / G, declared=None,
                 natural=None, reason="planted live row (provenance held)", ineq=False, deftag=False, carrier=None)
    _, cl2, c2 = run_census(S_DE, extra=[plant])
    m2 = c2["N_half"] == cnt["N_half"] + 1 and c2["outcome"] == "EXACT-1/2 AVAILABLE"
    say("M2 planted live row:", json.dumps({k: c2[k] for k in ("N_c", "N_pfdet", "N_half", "outcome")}), c2["half_ids"],
        "|", "BITES" if m2 else "DOES NOT BITE")
    # M3: d = 5 with the 8 pi G_d convention, H^2 = 16 pi G rho/((d-1)(d-2)) = (4 pi/3) G rho
    d = 5
    S_M3 = footing("rho_DE", FR=16 * PI / ((d - 1) * (d - 2)))
    _, cl3, c3 = run_census(S_M3)
    base = {r["id"]: r for r in cl}
    ratios, wsame = [], True
    for r in cl3:
        b = base[r["id"]]
        if b["carrier"] == "H" and b.get("k2_sym") is not None and b["cls"] not in ("TRADE",) and r.get("k2_sym") is not None:
            ratios.append((r["id"], str(sp.simplify(r["k2_sym"] / b["k2_sym"]))))
            wsame &= (r["pi_weight"] == b["pi_weight"])
    halves_all = all(x[1] == "1/2" for x in ratios)
    moves = all(x[1] in ("1/2", "2") for x in ratios) and len(ratios) > 0
    counts_same = c3["N_half"] == cnt["N_half"] and c3["N_pfdet"] == cnt["N_pfdet"]
    m3 = moves and wsame and counts_same
    say("M3 d = 5: H-type kappa^2 ratios (d5/d4):", ratios)
    say("   as frozen ('every determinate H-type kappa^2 halves'):", "PASS" if halves_all else
        "FAIL (rows with ratio 2: %s; H sits in the denominator there)" % [x[0] for x in ratios if x[1] == "2"])
    say("   pi-weights unchanged:", wsame, "| N_half, N_pfdet unchanged:", counts_same,
        json.dumps({k: c3[k] for k in ("N_pfdet", "N_half")}), "|", "BITES (values move, classes do not)" if m3 else "DOES NOT BITE")
    say("   S3 note (report only): Gauss-law convention pi-weight of Omega_(d-2) = floor((d-1)/2):",
        {dd: (dd - 1) // 2 for dd in (4, 5, 6, 7)})
    allbite = m1 and m2 and m3
    say("")
    say("MUTATE:", "all controls bite -> exit 1 (by design)" if allbite else "a control did not bite -> exit 2")
    res = dict(mode="MUTATE", baseline=cnt, M1=dict(counts=c1, R18=r18["cls"], bites=m1),
               M2=dict(counts=c2, bites=m2), M3=dict(counts=c3, ratios=ratios, halves_as_frozen=halves_all,
                                                      weights_same=wsame, bites=m3))
    write("cfg891_MUTATE.out", "cfg891_results_MUTATE.json", res)
    return 1 if allbite else 2


def write(outname, jsonname, res):
    txt = OUT.getvalue()
    with open(os.path.join(HERE, outname), "w", encoding="utf-8") as fh:
        fh.write(txt)
    with open(os.path.join(HERE, jsonname), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=str)
    sys.stdout.write(txt)


if __name__ == "__main__":
    sys.exit(main())
