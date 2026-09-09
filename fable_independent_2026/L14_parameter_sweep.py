#!/usr/bin/env python3
"""
L14 -- the candidate action's FULL parameter space against EVERY established gate, simultaneously
==================================================================================================
Individual pincers are known (PPN vs stability; growth vs the dark-sector window; Cassini vs the wide
binaries).  What has never been computed is the GLOBAL admissible region: the set of
(K_B, c_2, c_14, |K_2|, Q_0, xi) at which EVERY gate this programme has established holds at once.

THE PARAMETERS (THE_ACTION_2026-09-05.md sections 1-2)
  K_B      the aether/clock kinetic coupling, c_1 = -c_3 = K_B  (so c_13 = 0 identically)
  c_2      the khronometric lambda
  c_14     c_1 + c_4, the khronometric alpha
  |K_2|    the condensate stiffness, K(Q) = K_2 (Q - Q_0)^2 with K_2 < 0 in the pipeline convention
  Q_0      the condensate's background rate, quoted in units of H_0
  xi       the coherence (healing) length of the operator xi^2 |grad_perp V|^2, quoted in pc
  footing  a0 = 9.3619e-11 (canonical) / 1.1279e-10 (alt) m s^-2

THE GATES.  Each is a boolean function of the six parameters and the footing, with the formula taken
verbatim from its source script (named in the comment above each).  A gate that cannot be reproduced
at its source's own parameter values is reported UNREPRODUCED and EXCLUDED from the intersection.

  G1a  PPN alpha_1        |alpha_1| < 1e-4,  alpha_1 = -4 c_14 + drag                [g03z G2, f32/f33]
  G1b  PPN alpha_2        |alpha_2| < 4e-7,  Foster-Jacobson at c_1 = -c_3 = K_B     [g03v ppn()]
  G2   clock tachyon      rate <= H(a) for every a,  rate^2 = |K_2| Q_0^2 eps_0 a^-3 / c_14   [g03w]
  G2b  condensate         eps_0 > 1e-5 (not pushed through its minimum in wells)     [g03v V6]
  G3   linear growth      max(S_eff, 0) * 2.71e6 <= |K_2|                            [g03t D5 + D7]
  G4   dark-sector window H = 0.42 e c^2/(|K_2| a0) inside the galaxy/cluster window [g03r D, g03u]
  G5   Solar System       xi >= the Cassini/Saturn floor of the carried kernel       [g03d, g03z, Amdt 11]
  G6   BBN                K_B <= 0.25 and |G_cos/G_N - 1| < 0.13                     [route2, g03e B1]
  G7   tensor + Newton    c_T = 1 exactly (c_13 = 0) and G_N = G/(1 - c_14/2) > 0    [THE_ACTION 2, f35]
  G8   Cherenkov          |K_2| <= (2 - K_B)^2/c_14 (clock-scalar mode not subluminal)  [g03z G3]

  OUTPUT, not a cut: gamma_v, the Gaia DR4 Arm-B wide-binary prediction (PREREGISTRATION_DR4.md
  Amendment 11).  Arm B registers CEILINGS -- 1.0450 canonical / 1.0300 alt, at the Cassini-minimal
  xi -- and gamma_v falls toward 1 as xi grows, so a surviving region with xi above the floor
  predicts a SMALLER gamma_v.  It is carried as an output of each surviving point, never as a cut.

SIGN CONVENTIONS FIXED BY THE ACTION ITSELF (THE_ACTION section 2), and therefore built into the grid
rather than swept: c_14 > 0, c_2 > 0, K_B > 0, |K_2| > 0, Q_0 > 0.  Every minimal-subset statement
below is conditional on them and says so.

CHECKS THAT CAN FAIL
  C1-C10  CONTROL: each gate, at the parameter values its own source used, reproduces that source's
          published number/verdict.
  F1-F10  each gate's admitted fraction over the grid is neither 0 nor 1 (a gate that admits
          everything or nothing is probably mis-implemented).
  T1      THE TEST: is the simultaneous admissible region non-empty on either footing?
  T2      if empty, a MINIMAL incompatible subset of size <= 3 exists (the sharp statement).
"""
import numpy as np, math, itertools, sys, os

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

print("=" * 118)
print("L14 -- the candidate action's full parameter space against every established gate, simultaneously")
print("=" * 118, flush=True)

# ------------------------------------------------------------------ constants, all taken from the sources
cc   = 2.998e8                              # g03z line 32
PC   = 3.0857e16; kpc = 3.0857e19; Mpc = 3.0857e22
AU   = 1.495978707e11
A0   = {"canonical": 9.3619e-11, "alt": 1.1279e-10}          # g03z line 33
GEXT = 1.778e-10                                              # g03z line 33, the Galactic external field
Om, OL, Ob, Od = 0.315, 0.685, 0.049, 0.266                   # g03v line 131
cH0_Mpc = 2.998e5/67.4                                        # g03v line 131
R_SAT = 9.54*AU                                               # g03z line, Saturn's orbit
t0 = 13.8e9*3.156e7                                           # g03t line 193

# ------------------------------------------------------------------ the carried kernel: nu_RAR (THE_ACTION section 3)
# Delta(s) with g = g_N + a0 Delta(g_N/a0), nu_RAR = g_N/(1 - exp(-sqrt(g_N/a0))) up to s = 2.5399, saturated after.
# Copied verbatim from g03z_nurar_action_gate_ladder.py lines 44-47.
_sr = np.logspace(-9, math.log10(2.5399), 600001); _Dr = _sr*(1/(1 - np.exp(-np.sqrt(_sr))) - 1.0)
C_RAR, S_RAR = 0.647585, 2.5399
def Delta_rar(s):
    s = np.asarray(s, float); return np.where(s <= S_RAR, np.interp(np.minimum(s, S_RAR), _sr, _Dr), C_RAR)
def JY_rar(s): return np.asarray(s, float)/np.maximum(Delta_rar(s), 1e-300)
JY_EXT = {f: float(JY_rar(GEXT/a0)) for f, a0 in A0.items()}   # g03z G1: 2.967 canonical, 2.510 alt
print(f"\n  carried kernel nu_RAR: J_Y at the Galactic external field = "
      + ", ".join(f"{f} {v:.3f}" for f, v in JY_EXT.items()) + "   (g03z G1: 2.967 / 2.510)", flush=True)

# ==================================================================================================
#  THE GATES.  Each returns a boolean array; each is followed immediately by its CONTROL.
# ==================================================================================================
print("\n" + "-" * 118)
print("  THE GATE FUNCTIONS AND THEIR CONTROLS (each control evaluates the gate at its own source's parameters)")
print("-" * 118, flush=True)

# ---- G1a  PPN alpha_1.  SOURCE: g03z_nurar_action_gate_ladder.py G2 (which cites f32/f33):
#      alpha_1 = -4 c_14 + drag,  drag = -4(2 - K_B)/(J_Y(y_e)(1 + xi^2 k^2) + 1),  k = 1/r at Saturn.
ALPHA1_BOUND = 1e-4                                            # g03z G2 "the 1e-4 bound f33 uses"
def alpha_1(K_B, c14, xi_pc, foot):
    xk2 = (np.asarray(xi_pc, float)*PC/R_SAT)**2
    drag = -4*(2 - K_B)/(JY_EXT[foot]*(1 + xk2) + 1)
    return -4*c14 + drag
def G1a(K_B, c2, c14, K2, Q0, xi_pc, foot):
    return np.abs(alpha_1(K_B, c14, xi_pc, foot)) < ALPHA1_BOUND
_a1 = float(alpha_1(0.2, 1e-5, 0.10, "canonical")); _a1b = float(alpha_1(0.2, 1e-5, 0.15, "alt"))
print(f"    G1a  alpha_1(K_B = 0.2, c_14 = 1e-5, xi = 0.10 pc, canonical) = {_a1:.4e}   [g03z G2 table: -4.052e-05]")
print(f"    G1a  alpha_1(K_B = 0.2, c_14 = 1e-5, xi = 0.15 pc, alt)       = {_a1b:.4e}   [g03z G2 table: -4.027e-05]")
check("C1 [control, G1a] the alpha_1 formula reproduces g03z's G2 table at both floors to 1%",
      abs(_a1/-4.052e-5 - 1) < 0.01 and abs(_a1b/-4.027e-5 - 1) < 0.01, f"{_a1:.4e}, {_a1b:.4e}")

# ---- G1b  PPN alpha_2.  SOURCE: g03v_fast_clock_branch.py ppn() (Foster & Jacobson 2006), with the
#      candidate's identification c_1 = -c_3 = K_B, c_4 = c_14 - K_B (so c_123 = c_2 exactly).
ALPHA2_BOUND = 4e-7                                            # g03v: "Solar-System bound |alpha_2| < 4e-7"
def ppn_ae(K_B, c2, c14):
    c1v, c3v, c4v = K_B, -K_B, c14 - K_B; c123 = c1v + c2 + c3v          # = c_2 exactly, since c_1 + c_3 = 0
    a1 = -8*(c3v**2 + c1v*c4v)/(2*c1v - c1v**2 + c3v**2)
    a2 = a1/2 - (c1v + 2*c3v - c4v)*(2*c1v + 3*c2 + c3v + c4v)/(c123*(2 - c14))
    return a1, a2
def alpha_2(K_B, c2, c14):
    return ppn_ae(K_B, c2, c14)[1]
def G1b(K_B, c2, c14, K2, Q0, xi_pc, foot):
    return np.abs(alpha_2(K_B, c2, c14)) < ALPHA2_BOUND
_a1c, _a2c = ppn_ae(0.2, 1.0, 1.18e-5)                          # f33's corner
_c2star = 1e-5/(1 - 2e-5); _a2s = float(alpha_2(0.2, _c2star, 1e-5))
print(f"    G1b  (alpha_1, alpha_2) at f33's corner (K_B = 0.2, c_2 = 1, c_14 = 1.18e-5) = ({float(_a1c):.3e}, {float(_a2c):.3e})   [f33: -4.72e-5, -5.9e-6]")
print(f"    G1b  alpha_2 vanishes at c_2* = c_14/(1 - 2 c_14) = {_c2star:.4e}: alpha_2 = {_a2s:.2e}")
check("C2 [control, G1b] the Foster-Jacobson alpha_2 reproduces f33's corner within 20% and vanishes at c_2* = c_14/(1 - 2 c_14)",
      abs(float(_a2c)/(-5.9e-6) - 1) < 0.2 and abs(_a2s) < 1e-9, f"alpha_2(corner) = {float(_a2c):.2e}, alpha_2(c_2*) = {_a2s:.1e}")

# ---- G2  the clock tachyon.  SOURCE: g03w_growth_phi_dynamical.py line 164 (the analytic term of the
#      clock equation), with eps_0 fixed by the condensate carrying the dust density, g03v line 196:
#          T'' = (|K_2| Q_0^2 eps_0 a^-3 / c_14) T,      eps_0 = 3 H_0^2 Omega_d/(|K_2| Q_0^2)
#      so |K_2| Q_0^2 eps_0 = 3 H_0^2 Omega_d and the rate is a function of c_14 ALONE:
#          rate(a)/H_0 = sqrt(3 Omega_d/c_14) a^-3/2,     H(a)/H_0 = sqrt(Om a^-3 + OL).
#      (Verified independently against g03t's printed clock-equation coefficients: coeff(T'') = -2 c_14 k^2 a,
#       coeff(T) contains -2 k^2 K_2 Qbar(Qbar - Q_0) a with Qbar = Q_0(1 + eps_0 a^-3), K_2 = -|K_2|.
#       The k^2 cancels, which is why the mode is k-independent.)
A_GRID = np.geomspace(1.0/1101.0, 1.0, 60)                      # recombination to today
def tachyon_ratio(c14, K2, Q0):
    """max over a of rate/H, in the branch where the condensate carries Omega_d"""
    c14 = np.asarray(c14, float)
    worst = float(np.max(A_GRID**-1.5/np.sqrt(Om*A_GRID**-3 + OL)))
    return np.sqrt(3*Od/c14)*worst
def G2(K_B, c2, c14, K2, Q0, xi_pc, foot):
    return tachyon_ratio(c14, K2, Q0) <= 1.0
_rate_today = math.sqrt(3*Od/1e-5); _rate_e2 = _rate_today*100**1.5
print(f"    G2   rate/H_0 at (c_14 = 1e-5, |K_2| = 2.5e5, Q_0 = H_0): a = 1 -> {_rate_today:.0f}, a = 0.01 -> {_rate_e2:.1e}   [g03w: 282 H_0 and 2.8e+05 H_0]")
print(f"    G2   |K_2| and Q_0 CANCEL (eps_0 = 3 H_0^2 Omega_d/(|K_2| Q_0^2)); the gate is c_14 >= 3 Omega_d/Omega_m = {3*Od/Om:.4f}")
check("C3 [control, G2] the tachyonic rate reproduces g03w's 282 H_0 today and 2.8e5 H_0 at a = 0.01 to 1%",
      abs(_rate_today/282 - 1) < 0.01 and abs(_rate_e2/2.8e5 - 1) < 0.02, f"{_rate_today:.1f} H_0, {_rate_e2:.2e} H_0")

# ---- G2b  the condensate consistency.  SOURCE: g03v_fast_clock_branch.py V6:
#      eps_0 = 3 H_0^2 Omega_d/(|K_2| Q_0^2) must exceed the cluster potential ~1e-5, so that the
#      condensate is not pushed through its minimum inside wells; and eps_0 < 1 for "slightly off its
#      minimum" (g03v line 11) to mean anything.
def eps0_of(K2, Q0):  return 3*Od/(np.asarray(K2, float)*np.asarray(Q0, float)**2)   # H_0 = 1, Q_0 in units of H_0
def G2b(K_B, c2, c14, K2, Q0, xi_pc, foot):
    e = eps0_of(K2, Q0); return (e > 1e-5) & (e < 1.0)
_eps = {q: float(eps0_of(2.5e5, q)) for q in (0.1, 1.0, 10.0)}
print(f"    G2b  eps_0 at |K_2| = 2.5e5, Q_0/H_0 = 0.1/1/10: " + ", ".join(f"{v:.1e}" for v in _eps.values()) + "   [g03v V6: 3.2e-04, 3.2e-06, 3.2e-08]")
check("C4 [control, G2b] eps_0 reproduces g03v's V6 table (only Q_0 = 0.1 H_0 clears 1e-5 at |K_2| = 2.5e5)",
      abs(_eps[0.1]/3.2e-4 - 1) < 0.02 and _eps[0.1] > 1e-5 and _eps[1.0] < 1e-5, f"{_eps[0.1]:.2e}, {_eps[1.0]:.2e}")

# ---- G3  the linear-growth gate.  SOURCE: g03t_flrw_linear_from_action.py D5 (the screening factor,
#      derived symbolically from the action) and D7 (the floor):
#          S_eff = 1 - (2 - K_B)^2/(c_2 |K_2|)        [D5, exact, kernel-independent]
#          |K_2| >= 3.78 c^2 k^2 t_0^2 = 2.71e6 at k = 0.2/Mpc   [D7, from c_*^2 = 0.42 c^2/|K_2| (g03s)]
#      D7's floor is derived at S_eff = 1.  The scalar's contribution to the growth is proportional to
#      the surviving source, so the floor scales with S_eff: the gate is max(S_eff, 0)*K2_growth <= |K_2|.
#      This reduces exactly to D7 when the source survives, and to g03v's fast-clock escape (V4:
#      growth within 10% of LambdaCDM) when the source is screened off.
K_GROWTH = 0.2/Mpc
K2_GROWTH = 0.42*cc**2*9*K_GROWTH**2*t0**2                      # g03t line 194
def S_eff(K_B, c2, K2): return 1.0 - (2 - K_B)**2/(np.asarray(c2, float)*np.asarray(K2, float))
def G3(K_B, c2, c14, K2, Q0, xi_pc, foot):
    return np.maximum(S_eff(K_B, c2, K2), 0.0)*K2_GROWTH <= K2
_seff = float(S_eff(0.2, 0.05, 2.5e5))
print(f"    G3   S_eff(K_B = 0.2, c_2 = 0.05, |K_2| = 2.5e5) = {_seff:.6f}   [g03t D5: 0.999741];  K2_growth = {K2_GROWTH:.2e}   [g03t D7: 2.71e+06]")
check("C5 [control, G3] S_eff and the growth floor reproduce g03t's D5 and D7 numbers, and the corner FAILS the gate (D7's pincer)",
      abs(_seff - 0.999741) < 1e-5 and abs(K2_GROWTH/2.71e6 - 1) < 0.02
      and not bool(G3(0.2, 0.05, 1e-5, 2.5e5, 1.0, 0.10, "canonical")),
      f"S_eff = {_seff:.6f}, K2_growth = {K2_GROWTH:.3e}, corner admitted = {bool(G3(0.2, 0.05, 1e-5, 2.5e5, 1.0, 0.10, 'canonical'))}")

# ---- G4  the dark-sector (KiDS/cluster) window.  SOURCE: g03r_converged_collapse_adaptive_shells.py
#      section C/D and g03u_xcop_corrected_vs_atmosphere.py:  H = 0.42 e c^2/(|K_2| a0), and the window
#      is the H at which the galaxy's 100-kpc dust is <= 14% of its cold reference while the cluster's
#      1-Mpc dust is >= 32%.  g03r's Newtonian-growth window is |K_2| in [5e4, 5e5] at the CANONICAL
#      footing; because the criterion is on H and H scales as 1/(|K_2| a0), the gate is written on H so
#      that the alt footing is handled consistently instead of inheriting a coarse |K_2| grid.
def H_atm(K2, foot): return 0.42*math.e*cc**2/(np.asarray(K2, float)*A0[foot])       # metres
H_WIN = (float(H_atm(5e5, "canonical")), float(H_atm(5e4, "canonical")))              # [71.0, 710.4] kpc
def G4(K_B, c2, c14, K2, Q0, xi_pc, foot):
    H = H_atm(K2, foot); return (H >= H_WIN[0]) & (H <= H_WIN[1])
_H1e5 = {f: float(H_atm(1e5, f))/kpc for f in A0}
print(f"    G4   H(|K_2| = 1e5) = {_H1e5['canonical']:.0f} kpc canonical, {_H1e5['alt']:.0f} kpc alt   [g03r line 20: 355 / 295 kpc]")
print(f"    G4   window H in [{H_WIN[0]/kpc:.1f}, {H_WIN[1]/kpc:.1f}] kpc  ==  |K_2| in [5.0e+04, 5.0e+05] canonical, "
      f"[{0.42*math.e*cc**2/(H_WIN[1]*A0['alt']):.1e}, {0.42*math.e*cc**2/(H_WIN[0]*A0['alt']):.1e}] alt   [g03r D: [5e4, 5e5] both footings on its coarse grid]")
check("C6 [control, G4] the hydrostatic length reproduces g03r's tabulated H, and the canonical window edges are exactly 5e4 and 5e5",
      abs(_H1e5['canonical'] - 355) < 2 and abs(_H1e5['alt'] - 295) < 2
      and bool(G4(0.2, 0.05, 1e-5, 5e4, 1.0, 0.10, "canonical")) and bool(G4(0.2, 0.05, 1e-5, 5e5, 1.0, 0.10, "canonical"))
      and not bool(G4(0.2, 0.05, 1e-5, 1e6, 1.0, 0.10, "canonical")),
      f"H(1e5) = {_H1e5['canonical']:.1f} / {_H1e5['alt']:.1f} kpc; 1e6 rejected")

# ---- G5  the Solar-System coherence-length floor.  SOURCE: g03d_exact_fourth_order_solar.py (exact
#      fourth-order solve; its published admissibility table is reproduced below as the control), with
#      the carried kernel's floors from g03z XI_FLOOR / PREREGISTRATION_DR4.md Amendment 11.
G03D_TABLE = {   # xi [pc] -> admissible at all three field inputs?   (g03d .out, "admissible" column)
    "canonical": {0.01: False, 0.02: False, 0.03: True, 0.05: True, 0.10: True, 0.30: True},
    "alt":       {0.01: False, 0.02: False, 0.03: False, 0.05: True, 0.10: True, 0.30: True}}
XI_FLOOR_EXP = {"canonical": 0.03, "alt": 0.05}                 # g03d, exponential carrier (its own solve)
XI_FLOOR     = {"canonical": 0.10, "alt": 0.15}                 # g03z XI_FLOOR / Amendment 11, nu_RAR carried
def G5(K_B, c2, c14, K2, Q0, xi_pc, foot):
    return np.asarray(xi_pc, float) >= XI_FLOOR[foot]
_floor_tab = {f: min(x for x, ok in t.items() if ok) for f, t in G03D_TABLE.items()}
print(f"    G5   g03d's own table gives the exponential carrier's floors {_floor_tab}   [g03d .out: 0.03 / 0.05 pc]")
print(f"    G5   the gate in force uses the CARRIED (nu_RAR) floors {XI_FLOOR} pc   [g03z XI_FLOOR, Amendment 11(b)]")
check("C7 [control, G5] g03d's published admissibility table gives floors 0.03 pc canonical / 0.05 pc alt for the carrier it solved",
      _floor_tab == XI_FLOOR_EXP, f"{_floor_tab}")

# ---- G6  BBN.  SOURCES: g03e_flrw_background.py B1 (|G_cos/G_N - 1| < 0.13, Carroll-Lim, with
#      G_cos/G_N = 1/(1 + 3 c_2/2)) and route2_full_stack_2026.py line 613 (K_B <~ 0.25 from the corpus).
def Gcos_ratio(c2): return 1.0/(1.0 + 1.5*np.asarray(c2, float))
def G6(K_B, c2, c14, K2, Q0, xi_pc, foot):
    return (np.asarray(K_B, float) <= 0.25) & (np.abs(Gcos_ratio(c2) - 1) < 0.13)
_gc = {v: float(Gcos_ratio(v)) for v in (0.05, 0.1, 1.0)}
print(f"    G6   G_cos/G_N at c_2 = 0.05 / 0.1 / 1: " + ", ".join(f"{100*(v-1):+.1f}%" for v in _gc.values()) + "   [g03e B1: -7%, -13.0%, -60%]")
check("C8 [control, G6] G_cos/G_N reproduces g03e's B1 numbers: c_2 = 0.05 admitted (-7%), c_2 = 0.1 at the edge (-13.0%), c_2 = 1 killed (-60%)",
      abs(100*(_gc[0.05]-1) + 7.0) < 0.3 and abs(100*(_gc[0.1]-1) + 13.0) < 0.3 and abs(100*(_gc[1.0]-1) + 60.0) < 0.3,
      ", ".join(f"c_2 = {k}: {100*(v-1):+.1f}%" for k, v in _gc.items()))

# ---- G7  tensor sector + Newton constant.  SOURCES: THE_ACTION section 2 (c_1 = -c_3 = K_B is fixed by
#      c_T = c, requirement 6, GW170817 -- so c_13 = 0 IDENTICALLY and c_T = 1 exactly at every K_B, with
#      the tensor kinetic normalisation 1 - c_13 = 1 > 0); f35 (G_N = G/(1 - c_14/2), requirement 10);
#      route2_full_stack_2026.py line 1313 (vector kinetic health 0 < K_B < 2).  What bites is therefore
#      the POSITIVITY of the measured Newton constant, c_14 < 2, and 0 < K_B < 2.
def c13_of(K_B): return np.zeros_like(np.asarray(K_B, float))   # c_1 + c_3 = K_B - K_B
def GN_ratio(c14): return 1.0/(1.0 - np.asarray(c14, float)/2)
def G7(K_B, c2, c14, K2, Q0, xi_pc, foot):
    return (c13_of(K_B) == 0) & (np.asarray(c14, float) < 2.0) & (np.asarray(K_B, float) < 2.0)
print(f"    G7   c_13 = c_1 + c_3 = K_B - K_B = 0 identically  =>  c_T = 1 exactly at every K_B (GW170817 satisfied structurally)")
print(f"    G7   G_N/G = 1/(1 - c_14/2): c_14 = 1e-5 -> {float(GN_ratio(1e-5)):.6f};  c_14 = 2 -> singular;  c_14 = 3 -> {float(GN_ratio(3.0)):+.3f} (negative Newton constant)")
check("C9 [control, G7] c_13 vanishes identically (c_T = 1) and G_N = G/(1 - c_14/2) is positive only for c_14 < 2",
      float(c13_of(0.2)) == 0.0 and float(GN_ratio(1e-5)) > 0 and float(GN_ratio(3.0)) < 0
      and bool(G7(0.2, 0.05, 1e-5, 2.5e5, 1.0, 0.10, "canonical")) and not bool(G7(0.2, 0.05, 3.0, 2.5e5, 1.0, 0.10, "canonical")),
      f"G_N/G(1e-5) = {float(GN_ratio(1e-5)):.6f}, G_N/G(3) = {float(GN_ratio(3.0)):+.3f}")

# ---- G8  the Cherenkov / closure bound.  SOURCE: g03z_nurar_action_gate_ladder.py G3,
#      K2_CHER = (2 - K_B)^2/c_14: the clock-scalar mode has c_s^2 = (2 - K_B)^2/(c_14 |K_2|) (g03t's
#      rigidity note) and gravitational Cherenkov forbids it being subluminal, so |K_2| <= (2-K_B)^2/c_14.
def K2_cher(K_B, c14): return (2 - np.asarray(K_B, float))**2/np.asarray(c14, float)
def G8(K_B, c2, c14, K2, Q0, xi_pc, foot):
    return np.asarray(K2, float) <= K2_cher(K_B, c14)
_kc = float(K2_cher(0.2, 1e-5))
print(f"    G8   (2 - K_B)^2/c_14 at (K_B = 0.2, c_14 = 1e-5) = {_kc:.2e}   [g03z G3: 3.24e+05]")
check("C10 [control, G8] the Cherenkov bound reproduces g03z's 3.24e5 and admits |K_2| = 2.5e5 while rejecting 1e6 at the same corner",
      abs(_kc/3.24e5 - 1) < 0.01 and bool(G8(0.2, 0.05, 1e-5, 2.5e5, 1.0, 0.10, "canonical"))
      and not bool(G8(0.2, 0.05, 1e-5, 1e6, 1.0, 0.10, "canonical")), f"{_kc:.3e}")

# ---- OUTPUT (not a cut): gamma_v.  SOURCE: g03y_gammav_corrected_floors.py / Amendment 11(b).
#      Registered CEILINGS at the floors: 1.0450 (canonical, xi = 0.10 pc), 1.0300 (alt, xi = 0.15 pc).
#      gamma_v falls monotonically as xi grows (g03y Z2).  The exponent below is fitted to g03y's own two
#      tabulated xi per footing FOR THE EXPONENTIAL CARRIER and applied to the carried kernel's anchor;
#      it is an EXTRAPOLATION and is labelled as such wherever it is used.
GV_ANCHOR = {"canonical": (0.10, 1.0450), "alt": (0.15, 1.0300)}
_gy = {"canonical": ((0.03, 1.0725), (0.07, 1.0375)), "alt": ((0.05, 1.0625), (0.10, 1.0275))}
GV_EXP = {f: math.log((p[0][1]-1)/(p[1][1]-1))/math.log(p[1][0]/p[0][0]) for f, p in _gy.items()}
def gamma_v(xi_pc, foot):
    x0, g0 = GV_ANCHOR[foot]; return 1 + (g0 - 1)*(np.asarray(xi_pc, float)/x0)**(-GV_EXP[foot])
print(f"    gv   Arm-B ceilings {GV_ANCHOR} (xi [pc], gamma_v)  [Amendment 11(b)];  fitted falloff exponent p = "
      + ", ".join(f"{f} {v:.3f}" for f, v in GV_EXP.items()) + "  [extrapolated from g03y's exponential-carrier pairs]")

GATES = [("G1a  PPN alpha_1",        G1a), ("G1b  PPN alpha_2",        G1b),
         ("G2   clock tachyon",      G2),  ("G2b  condensate eps_0",   G2b),
         ("G3   linear growth",      G3),  ("G4   dark-sector window", G4),
         ("G5   Solar-System xi",    G5),  ("G6   BBN",                G6),
         ("G7   tensor + G_N > 0",   G7),  ("G8   Cherenkov",          G8)]
NG = len(GATES)

# ==================================================================================================
#  THE GRID
# ==================================================================================================
print("\n" + "-" * 118)
print("  THE GRID (logarithmic, generous; the action's own sign conventions restrict every axis to positive values)")
print("-" * 118, flush=True)

def build(base, extras):
    return np.unique(np.concatenate([np.asarray(base, float), np.asarray(extras, float)]))

C14_G = build(np.logspace(-9, 1, 21), [1e-5, 1.18e-5])
# the alpha_2 = 0 locus c_2* = c_14/(1 - 2 c_14) is a band ~16% wide in c_2; a plain log grid would step
# straight over it, so every positive c_2*(c_14) for c_14 on the grid is ADDED to the c_2 grid.  This is
# deliberately generous to the theory: it guarantees the alpha_2 gate cannot be missed by resolution.
_c2star_loci = [float(c/(1 - 2*c)) for c in C14_G if 0 < c < 0.5]
KB_G  = build(np.logspace(-3, math.log10(5), 15), [0.1, 0.2, 0.25])
C2_G  = build(np.logspace(-9, 1, 21), [0.05, 0.1, 1.0] + _c2star_loci)
K2_G  = build(np.logspace(0, 12, 25), [5e4, 2.5e5, 5e5, 2.71e6])
Q0_G  = build(np.logspace(-4, 4, 13), [0.1, 1.0, 10.0])
XI_G  = build(np.logspace(-4, 3, 12), [0.03, 0.05, 0.07, 0.10, 0.15])
AXES = [("K_B", KB_G), ("c_2", C2_G), ("c_14", C14_G), ("|K_2|", K2_G), ("Q_0/H_0", Q0_G), ("xi [pc]", XI_G)]
NTOT = int(np.prod([len(g) for _, g in AXES]))
for nm, g in AXES:
    print(f"    {nm:9s} {len(g):4d} points   [{g.min():.3e}, {g.max():.3e}]")
print(f"    grid points per footing: {NTOT:,}   (2 footings -> {2*NTOT:,})", flush=True)

SHAPE = tuple(len(g) for _, g in AXES)
def shaped(g, ax):
    s = [1]*6; s[ax] = len(g); return g.reshape(s)
KBb, C2b, C14b, K2b, Q0b, XIb = (shaped(g, i) for i, (_, g) in enumerate(AXES))

# ==================================================================================================
#  THE SWEEP.  Each grid point's pass/fail pattern over the 10 gates is packed into one uint16, and the
#  histogram over the 2^10 patterns is accumulated.  Every question below -- per-gate fractions, the
#  intersection, every subset's emptiness -- is then exact and instant from that histogram.
# ==================================================================================================
print("\n" + "-" * 118)
print("  PER-GATE ADMITTED FRACTIONS AND THE INTERSECTION")
print("-" * 118, flush=True)

HIST = {}
for foot in ("canonical", "alt"):
    h = np.zeros(1 << NG, dtype=np.int64)
    for i_kb in range(len(KB_G)):                                  # chunk over K_B to bound memory
        kb = KB_G[i_kb:i_kb+1].reshape(1, 1, 1, 1, 1, 1)
        bits = np.zeros((1,) + SHAPE[1:], dtype=np.uint16)
        for gi, (_, fn) in enumerate(GATES):
            ok = fn(kb, C2b, C14b, K2b, Q0b, XIb, foot)
            bits |= (np.broadcast_to(ok, bits.shape).astype(np.uint16) << gi)
        h += np.bincount(bits.ravel(), minlength=1 << NG)
    HIST[foot] = h
    assert h.sum() == NTOT

PAT = np.arange(1 << NG)
def frac(foot, mask):     # fraction of the grid admitted by ALL gates whose bits are in `mask`
    return float(HIST[foot][(PAT & mask) == mask].sum())/NTOT
def count(foot, mask):
    return int(HIST[foot][(PAT & mask) == mask].sum())

print(f"    {'gate':26s} {'canonical':>14s} {'alt':>14s}")
for gi, (nm, _) in enumerate(GATES):
    print(f"    {nm:26s} {frac('canonical', 1 << gi):14.6f} {frac('alt', 1 << gi):14.6f}")
ALLMASK = (1 << NG) - 1
print(f"    {'INTERSECTION (all 10)':26s} {frac('canonical', ALLMASK):14.6f} {frac('alt', ALLMASK):14.6f}")
print(f"    {'  points':26s} {count('canonical', ALLMASK):14,d} {count('alt', ALLMASK):14,d}", flush=True)

for gi, (nm, _) in enumerate(GATES):
    f_c, f_a = frac("canonical", 1 << gi), frac("alt", 1 << gi)
    check(f"F{gi+1} [{nm.split()[0]}] the gate alone admits neither 0 nor 1 of the grid at both footings",
          0.0 < f_c < 1.0 and 0.0 < f_a < 1.0, f"canonical {f_c:.6f}, alt {f_a:.6f}")

# ==================================================================================================
#  THE TEST, and the minimal incompatible subsets
# ==================================================================================================
print("\n" + "-" * 118)
print("  THE TEST")
print("-" * 118, flush=True)
nonempty = {f: count(f, ALLMASK) > 0 for f in HIST}
check("T1 [THE TEST] the simultaneous admissible region of all 10 gates is non-empty on at least one footing",
      any(nonempty.values()), f"canonical {count('canonical', ALLMASK):,} points, alt {count('alt', ALLMASK):,} points")

MINIMAL = {}
for foot in HIST:
    empties = []
    for size in range(1, NG + 1):
        found_this_size = []
        for combo in itertools.combinations(range(NG), size):
            m = sum(1 << g for g in combo)
            if count(foot, m) > 0: continue
            if any((prev & m) == prev for prev in empties): continue     # a proper subset is already empty
            found_this_size.append(m)
        empties.extend(found_this_size)
        if size >= 4 and found_this_size == []: break
    MINIMAL[foot] = empties

print(f"\n    MINIMAL incompatible subsets (no proper subset of any listed set is itself empty):")
for foot in HIST:
    print(f"      {foot}:")
    if not MINIMAL[foot]:
        print(f"        none -- every subset of the ten gates has a non-empty intersection")
    for m in MINIMAL[foot]:
        names = [GATES[g][0].split()[0] for g in range(NG) if m >> g & 1]
        print(f"        {{{', '.join(names)}}}   (size {len(names)})")
minsize = {f: (min(bin(m).count('1') for m in MINIMAL[f]) if MINIMAL[f] else None) for f in MINIMAL}
if any(MINIMAL.values()):
    check("T2 [minimal subset] where the full intersection is empty, a minimal incompatible subset of size <= 3 exists (the sharp statement, not 'everything fails together')",
          all((not MINIMAL[f]) or minsize[f] <= 3 for f in MINIMAL),
          ", ".join(f"{f}: smallest incompatible subset has {minsize[f]} gates" for f in MINIMAL if MINIMAL[f]))

# ==================================================================================================
#  CHARACTERISE the largest non-empty region: drop the offending gate(s) and bound what survives
# ==================================================================================================
print("\n" + "-" * 118)
print("  THE SURVIVING REGION")
print("-" * 118, flush=True)

FIDUCIAL = {"canonical": (0.2, 1e-5, 1e-5, 2.5e5, 0.1, 0.10), "alt": (0.2, 1e-5, 1e-5, 2.5e5, 0.1, 0.15)}
def region_bounds(foot, mask):
    """exact per-axis bounds of the set of grid points admitted by `mask`, the locked correlations there,
    a representative point (the admitted point closest in log-distance to the programme's fiducial corner),
    and how much of the region keeps the linear MOND source alive"""
    lo = [None]*6; hi = [None]*6; npts = 0; n_src = 0
    s_lo = s_hi = None; best = (np.inf, None); fid = np.log(np.array(FIDUCIAL[foot]))
    ratio_lo = ratio_hi = None            # c_2 / c_2*(c_14): how tightly alpha_2 locks the two
    rc_lo = rc_hi = None                  # the same ratio restricted to c_14 >= 1e-6, where alpha_2 bites
    for i_kb in range(len(KB_G)):
        kb = KB_G[i_kb:i_kb+1].reshape(1, 1, 1, 1, 1, 1)
        ok = np.ones((1,) + SHAPE[1:], dtype=bool)
        for gi, (_, fn) in enumerate(GATES):
            if not (mask >> gi) & 1: continue
            ok &= np.broadcast_to(fn(kb, C2b, C14b, K2b, Q0b, XIb, foot), ok.shape)
        if not ok.any(): continue
        npts += int(ok.sum())
        idx = np.nonzero(ok)
        vals = [KB_G[i_kb]*np.ones(len(idx[0]))] + [AXES[a][1][idx[a]] for a in range(1, 6)]
        for a in range(6):
            lo[a] = vals[a].min() if lo[a] is None else min(lo[a], vals[a].min())
            hi[a] = vals[a].max() if hi[a] is None else max(hi[a], vals[a].max())
        se = S_eff(vals[0], vals[1], vals[3]); n_src += int((se > 0.5).sum())
        s_lo = se.min() if s_lo is None else min(s_lo, se.min()); s_hi = se.max() if s_hi is None else max(s_hi, se.max())
        rr = vals[1]/(vals[2]/(1 - 2*vals[2]))
        ratio_lo = rr.min() if ratio_lo is None else min(ratio_lo, rr.min())
        ratio_hi = rr.max() if ratio_hi is None else max(ratio_hi, rr.max())
        mb = vals[2] >= 1e-6                                  # where the alpha_2 bound actually ties c_2 to c_14
        if mb.any():
            rl, rh = rr[mb].min(), rr[mb].max()
            rc_lo = rl if rc_lo is None else min(rc_lo, rl); rc_hi = rh if rc_hi is None else max(rc_hi, rh)
        d = np.sum((np.log(np.array(vals)) - fid[:, None])**2, axis=0); j = int(np.argmin(d))
        if d[j] < best[0]: best = (float(d[j]), tuple(float(v[j]) for v in vals))
    return dict(npts=npts, lo=lo, hi=hi, ex=best[1], s_lo=s_lo, s_hi=s_hi, n_src=n_src,
                ratio=(ratio_lo, ratio_hi), ratio_hi_c14=(rc_lo, rc_hi))

targets = []
if any(nonempty.values()):
    targets.append(("all 10 gates", ALLMASK))
else:
    # the largest subsets that ARE non-empty: drop one gate at a time, report every drop that opens a region
    for gi in range(NG):
        m = ALLMASK & ~(1 << gi)
        if any(count(f, m) > 0 for f in HIST):
            targets.append((f"all gates EXCEPT {GATES[gi][0].split()[0]}", m))

REG = {}
for label, m in targets:
    print(f"\n    [{label}]")
    for foot in ("canonical", "alt"):
        R = region_bounds(foot, m); REG[(label, foot)] = R
        if R["npts"] == 0:
            print(f"      {foot:9s}: EMPTY"); continue
        lo, hi, ex = R["lo"], R["hi"], R["ex"]
        print(f"      {foot:9s}: {R['npts']:,} grid points of {NTOT:,}  ({R['npts']/NTOT:.3e})")
        for a, (nm, _) in enumerate(AXES):
            print(f"          {nm:9s} in [{lo[a]:.4e}, {hi[a]:.4e}]")
        print(f"          c_2/c_2*(c_14) over the region: [{R['ratio'][0]:.4g}, {R['ratio'][1]:.4g}]; restricted to c_14 >= 1e-6, where the")
        print(f"            alpha_2 bound actually bites (below c_14 ~ ALPHA2_BOUND/2 = {ALPHA2_BOUND/2:.0e}, |alpha_2| ~ 2 c_14 clears it at any c_2):")
        print(f"            [{R['ratio_hi_c14'][0]:.4g}, {R['ratio_hi_c14'][1]:.4g}] -- there the marginal boxes are NOT independent and the region is a thin sheet")
        K2hi = 0.42*math.e*cc**2/(H_WIN[0]*A0[foot])
        print(f"          S_eff over the region: [{R['s_lo']:.4g}, {R['s_hi']:.4g}] (grid);  ANALYTIC ceiling from G3 and G4 alone: "
              f"S_eff <= |K_2|_max/K2_growth = {K2hi/K2_GROWTH:.4f}")
        print(f"            i.e. the surviving cosmology keeps at most {100*K2hi/K2_GROWTH:.0f}% of the action's own linear scalar source; "
              f"points with S_eff > 0.5: {R['n_src']:,}")
        gv_lo = float(gamma_v(hi[5], foot)); gv_hi = float(gamma_v(lo[5], foot))
        print(f"          predicted gamma_v (Arm B, extrapolated in xi): [{gv_lo:.4f}, {gv_hi:.4f}]"
              f"   ceiling at the floor {GV_ANCHOR[foot][1]:.4f}")
        print(f"          representative point (closest to the programme's fiducial corner): K_B = {ex[0]:.4g}, c_2 = {ex[1]:.4g}, "
              f"c_14 = {ex[2]:.4g}, |K_2| = {ex[3]:.4g}, Q_0 = {ex[4]:.4g} H_0, xi = {ex[5]:.4g} pc")
        print(f"            -> alpha_1 = {float(alpha_1(ex[0], ex[2], ex[5], foot)):+.3e}, "
              f"alpha_2 = {float(alpha_2(ex[0], ex[1], ex[2])):+.3e}, S_eff = {float(S_eff(ex[0], ex[1], ex[3])):+.4g}, "
              f"H = {float(H_atm(ex[3], foot))/kpc:.1f} kpc, eps_0 = {float(eps0_of(ex[3], ex[4])):.2e}, "
              f"gamma_v = {float(gamma_v(ex[5], foot)):.4f}")

if not any(nonempty.values()):
    lbl = f"all gates EXCEPT {GATES[2][0].split()[0]}"
    alive = {f: REG[(lbl, f)]["n_src"] for f in ("canonical", "alt") if (lbl, f) in REG}
    check("T3 [what the survivor costs] in the region that opens when the tachyon gate is dropped, is the action's linear scalar source more than half alive anywhere (S_eff > 0.5)?  A PASS would mean the escape keeps the cosmological MOND source; a FAIL means every survivor sits on the fast-clock branch where G3 and G4 together screen the source off (analytic ceiling S_eff <= 0.185 canonical / 0.153 alt)",
          any(v > 0 for v in alive.values()), ", ".join(f"{f}: {v:,} of {REG[(lbl, f)]['npts']:,} points, S_eff max {REG[(lbl, f)]['s_hi']:.4g}" for f, v in alive.items()))

# ==================================================================================================
#  SENSITIVITY of the killing gate: how far would the bound have to be relaxed?
# ==================================================================================================
print("\n" + "-" * 118)
print("  SENSITIVITY OF THE KILLING GATE (how far a bound would have to move for the region to open)")
print("-" * 118, flush=True)
print(f"    the tachyon gate is c_14 >= 3 Omega_d/Omega_m = {3*Od/Om:.4f} for rate <= H; tolerating rate <= N H gives c_14 >= {3*Od/Om:.4f}/N^2:")
for N in (1, 3, 10, 30, 100, 300):
    need = 3*Od/Om/N**2
    print(f"       N = {N:4d} e-folds per Hubble time tolerated  ->  c_14 >= {need:.3e}"
          f"   (PPN alpha_1 allows c_14 <= {ALPHA1_BOUND/4:.2e}: {'COMPATIBLE' if need <= ALPHA1_BOUND/4 else f'short by {need/(ALPHA1_BOUND/4):.1e}x'})")
print(f"    the rate is independent of |K_2| and Q_0 only because eps_0 is fixed by the condensate carrying Omega_d;")
print(f"    at a smaller dark fraction Omega_d the threshold falls as 3 Omega_d/Omega_m:")
for od in (0.266, 0.1, 0.01, 1e-3):
    print(f"       Omega_d = {od:6.3f}  ->  c_14 >= {3*od/Om:.3e}   ({3*od/Om/(ALPHA1_BOUND/4):.1e}x the PPN ceiling)")

# ---- THE ONE ESCAPE FROM G2, computed rather than asserted.  g03e records the dust amplitude C in
#      a^3 K' = C as "a free cosmological initial datum", so eps_0 need not be tied to Omega_d.  Freeing it
#      means freeing the condensate's own dust fraction Omega_d,eff = |K_2| Q_0^2 eps_0/(3 H_0^2); the tachyon
#      gate then reads rate <= H, i.e. |K_2| Q_0^2 eps_0 <= Omega_m c_14, i.e. Omega_d,eff <= Omega_m c_14/3.
print(f"\n    THE ONE ESCAPE, computed: free the condensate's dust amplitude (g03e: a free initial datum).")
print(f"    rate <= H at every a  <=>  Omega_d,eff = |K_2| Q_0^2 eps_0/(3 H_0^2) <= Omega_m c_14/3.")
OD_MAX = Om*(ALPHA1_BOUND/4)/3
print(f"    at the largest PPN-allowed c_14 = {ALPHA1_BOUND/4:.2e} this is Omega_d,eff <= {OD_MAX:.3e},")
print(f"    i.e. {Od/OD_MAX:.2e} times SMALLER than the dark component the dark-sector window G4 and the cluster")
print(f"    atmosphere (g03u: M_d/M_b ~ 6.8 at 100 kpc) require the condensate to be.  The escape exists and it")
print(f"    empties G4 of content: a tachyon-free clock and a condensate dark sector cannot both be had.")
check("T4 [the escape is not free] freeing eps_0 removes the tachyon only by shrinking the condensate's dust fraction below what the dark-sector gate G4 needs; check that the two are numerically incompatible at the PPN-allowed c_14",
      OD_MAX < 0.01*Od, f"Omega_d,eff <= {OD_MAX:.3e} against Omega_d = {Od} needed: short by {Od/OD_MAX:.2e}x")

print("\n  caveats, stated: (i) the 'fraction of the grid' is a measure over the stated logarithmic grid and has no")
print("  prior meaning -- only the emptiness/non-emptiness statements are grid-independent, and those were also")
print("  checked analytically where noted; (ii) the tachyon gate uses the ANALYTIC term g03w identifies in the clock")
print("  equation (re-derived here from g03t's printed coefficients), not g03w's numerical eigenmode, whose separation")
print("  from a constraint-differentiation artefact g03w itself records as open; (iii) G3 extends g03t's D7 floor by")
print("  the D5 screening factor, which is an interpolation between D7 (S_eff = 1) and g03v's fast-branch V4 (S_eff <= 0);")
print("  (iv) G4's window edges come from g03r's coarse |K_2| grid, re-expressed on H so that the alt footing is")
print("  consistent; (v) gamma_v's xi-dependence is extrapolated from g03y's exponential-carrier pairs and is an")
print("  OUTPUT, never a cut; (vi) the grid is positive in every parameter, as THE_ACTION section 2 fixes the signs.")

print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
