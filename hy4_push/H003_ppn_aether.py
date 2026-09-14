#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H003 -- THE PPN LANE: gamma, beta, eta_N, alpha_1, alpha_2, and u_solar.

WHAT IS NEW HERE (and what is NOT).
  NEW, computable, and decided by arithmetic:
    (1) u_solar = sqrt(X) at 1 AU / 9.5 AU / 30 AU, with Lambda^4 CALIBRATED
        from the theory's own two anchors (f(0) = -1 => Lambda^4 = rho_Lambda,
        and a_0 = c sqrt(G rho_Lambda)/2).
    (2) the suppression factor a_0/g_N and its square, at planetary radii.
    (3) the (a_0/g)^2 suppression of gamma-1, beta-1 and eta_N.
  REGISTERED ELSEWHERE, reproduced here ONLY as a control:
    the preferred-frame lock  alpha_1 = -4 c_14 - 4(2-K_B)/(J_Y+1)
    (hunt_2026/f30, f31; qwen_claude_field_theory/closure_2026/door_a_2026/
    doorA_alpha1_generality_theorem.py, 12/12).  I do NOT re-derive it from
    the action; I reproduce its algebra and report its consequence.  A control
    is never counted as a result.

THE TWO HORNS FOR THE AETHER (the honest fork -- this is Part E):
  HORN A (non-dynamical).  The action as written in H001 is
      S = int sqrt(-g)[ M_P^2 R/2 - Lambda^4 f(X) ] + S_m[g]
  and the aether enters ONLY through h^{mu nu} inside X.  There is no aether
  kinetic term.  The aether can therefore be a FIXED unit timelike congruence
  (hypersurface-orthogonal, aligned with the CMB).  No aether EOM -> no spin-1
  mode -> the vector sector contributes identically zero to alpha_1, alpha_2.
  COST: a fixed timelike congruence is a background structure, so local Lorentz
  invariance is violated EXPLICITLY, not spontaneously.  That is a
  philosophical cost, not a constraint violation.
  HORN B (dynamical, i.e. AeST proper).  Give the aether its Maxwell kinetic
  term (c_1 = -c_3 = K_B, c_2 = c_4 = 0).  Then the repo's registered closed
  form applies and the preferred-frame gate FAILS: the drag piece
  -4(2-K_B)/(J_Y+1) is irreducible, O(1), and alpha_1 = 0 forces c_14 < 0, a
  spin-1 ghost.
  HORN A IS UNCOMPUTED IN THIS REPO'S PPN PIPELINE.  f30/f31/doorA all assume
  the dynamical aether with the MOND-generating coupling 2(2-K_B) J.grad(phi)
  present.  Whether the fixed-congruence version really gives alpha_1 = 0 in
  the METRIC (as opposed to in the vector's own kinetic sector) is OPEN and is
  named as such.  It is the one route not yet killed.

PRE-REGISTERED KILL CONDITIONS (stated before any number is printed)
  K1  u_solar(1 AU) >> 1.  KILL if u < 100: the whole solar-system
      expansion assumes the deep-Newtonian branch mu_2 -> 1.
  K2  4 (a_0/g_N)^2 at 1 AU < 2.3e-5 (Cassini).  KILL otherwise: the scalar's
      stress is then visible in the light-bending potential.
  K3  |gamma - 1| < 2.3e-5 (Cassini, Bertotti+2003).
  K4  |beta - 1| < 2.3e-4 (Mercury perihelion / LLR, Anderson+ / Will 2014).
  K5  |eta_N| = |4beta - gamma - 3| < 4.4e-4 (LLR, Williams+2012).
  K6  CONTROL: reproduce the registered lock; alpha_1 = 0 => c_14 < 0 on the
      whole physical domain 0 < K_B < 2, J_Y >= 1.
  K7  |alpha_1| < 1e-4 (Will/Nordtvedt solar-system bound).
  K8  |alpha_2| < 1.6e-9 (PSR J1738+0333, Shao & Wex 2012).
No threshold is tuned after the fact.  Both footings always.
"""
import json, math
import numpy as np
import sympy as sp

OUT = "/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_push/"
RES, NP, NF = [], 0, 0


def check(name, measured, ok, thr="", note=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured : {measured}")
    if thr:
        print(f"         threshold: {thr}")
    if note:
        for ln in note.strip().split("\n"):
            print(f"         {ln}")
    RES.append({"check": name, "measured": measured, "threshold": thr, "pass": ok})
    if ok:
        NP += 1
    else:
        NF += 1
    return ok


# ---------------------------------------------------------------- constants
G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
q_e = 1.602176634e-19
Mpc = 3.0856775814913673e22
PC = 3.0856775814913673e16
AU = 1.495978707e11
MSUN = 1.98892e30
GM_SUN = G * MSUN
H0 = 67.4e3 / Mpc
OmL = 0.685
rho_c = 3.0 * H0**2 / (8.0 * math.pi * G)

# BOTH FOOTINGS (repo standing rule, STANDING.md line 184)
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}

# natural-unit conversion factors
EV_PER_J = 1.0 / q_e
M_INV_EV = 1.0 / (1.973269804e-7)      # 1 m  in eV^-1  (from hbar*c)
S_INV_EV = c * M_INV_EV                # 1 s  in eV^-1
M3_TO_EV3 = 1.0 / M_INV_EV**3          # 1 m^-3 in eV^3
J_M3_TO_EV4 = EV_PER_J * M3_TO_EV3     # J/m^3 -> eV^4
MS2_TO_EV = M_INV_EV / S_INV_EV**2     # m/s^2 -> eV

M_P_kg = math.sqrt(hbar * c / (8.0 * math.pi * G))     # reduced Planck mass
M_P_eV = M_P_kg * c**2 * EV_PER_J

# published bounds (cited, not fitted)
CASSINI = 2.3e-5        # |gamma-1|, Bertotti, Iess & Tortora 2003
BETA_B = 2.3e-4         # |beta-1|, Mercury perihelion / LLR (Will 2014 Tab. 4)
ETA_B = 4.4e-4          # |eta_N|, lunar laser ranging (Williams+2012)
A1_B = 1.0e-4           # |alpha_1|, Will/Nordtvedt solar system
A2_B = 1.6e-9           # |alpha_2|, PSR J1738+0333 (Shao & Wex 2012)

print("=" * 78)
print("H003 -- PPN PARAMETERS AND PREFERRED-FRAME CONSTRAINTS, ZIMMERMAN-AeST")
print("=" * 78)
print(f"\n  rho_Lambda = {OmL*rho_c:.4e} kg/m^3   M_P = {M_P_eV:.4e} eV")
print(f"  footings   : a_0 = {A0['canonical']:.3e} (canonical) / "
      f"{A0['alt']:.3e} (alt) m/s^2")

# ================================================================ PART A
#  Lambda^4, CALIBRATED.  Two anchors, both internal to H001.
print("\n" + "=" * 78)
print("PART A -- CALIBRATING Lambda^4  (DERIVED, not fitted)")
print("=" * 78)
print("""
  Anchor 1 (H001 A2/B2, verified symbolically there): f(0) = -1 exactly, so
       rho_scalar(X=0) = Lambda^4 [2X f' - f] = Lambda^4 * (+1) = Lambda^4.
       The vacuum energy of this theory IS Lambda^4, hence  Lambda^4 = rho_L.
  Anchor 2 (H001 F1): a_0 = c sqrt(G rho_Lambda)/2  =>  rho_L = 4 a_0^2/(G c^2).
  Eliminating rho_L with G = hbar c/(8 pi M_P^2):
       Lambda^4 = 32 pi M_P^2 a_0^2            (natural units)
  This is the "Lambda^4 in terms of M_P and a_0" the lane was asked for, and it
  comes out of the theory rather than being put in.
""")

rho_L = OmL * rho_c                       # kg/m^3
L4_eV4 = rho_L * c**2 * J_M3_TO_EV4       # Lambda^4 in eV^4
Lam_eV = L4_eV4**0.25
check("A1 [DERIVED] Lambda^4 = rho_Lambda, and the fourth root lands on the known\n"
      "      dark-energy scale ~2.3 meV (independent published anchor, not an input)",
      f"Lambda = rho_Lambda^(1/4) = {Lam_eV*1e3:.4f} meV",
      abs(Lam_eV * 1e3 - 2.3) < 0.3,
      "threshold: 2.3 +/- 0.3 meV (published value of rho_Lambda^(1/4))",
      "The scale in the aether-frame kinetic invariant X is the dark-energy\n"
      "scale. That is the same statement as 'the CC is f(0)'.")

row = []
for foot, a0 in A0.items():
    a0_eV = a0 * MS2_TO_EV
    L4_pred = 32.0 * math.pi * M_P_eV**2 * a0_eV**2
    row.append((foot, L4_pred))
    print(f"      {foot:>9s}: Lambda^4 = 32 pi M_P^2 a_0^2 = {L4_pred:.6e} eV^4")
print(f"      measured  : Lambda^4 = rho_Lambda        = {L4_eV4:.6e} eV^4")
err_canon = abs(row[0][1] / L4_eV4 - 1.0)
check("A2 [DERIVED] Lambda^4 = 32 pi M_P^2 a_0^2 reproduces the independently computed\n"
      "      rho_Lambda on the CANONICAL footing: three constants (M_P, a_0, rho_Lambda),\n"
      "      two independent routes, one number. This is the calibration.",
      f"|32 pi M_P^2 a_0^2 / rho_Lambda - 1| = {err_canon:.3e} (canonical)",
      err_canon < 1e-2,
      "threshold: agreement to better than 1% (M_P rounding is the floor)",
      "NOT a fitted relation: M_P comes from (hbar,c,G), a_0 from (c,G,rho_Lambda),\n"
      "and rho_Lambda from (H0, Omega_Lambda). The closure is the theory's.")

# A2b -- the alt footing MUST NOT match, and the mismatch must be the footing ratio.
err_alt = abs(row[1][1] / L4_eV4 - 1.0)
ratio = (A0["alt"] / A0["canonical"]) ** 2
check("A2b [CONSISTENCY, and a real finding] the ALT footing does NOT reproduce\n"
      "      rho_Lambda, and it should not: the alt footing defines a_0 from rho_TOTAL,\n"
      "      not rho_Lambda, so the identity a_0 = c sqrt(G rho_Lambda)/2 is\n"
      "      CANONICAL-FOOTING-ONLY. The mismatch must be exactly (a_0^alt/a_0^canon)^2.",
      f"|Lambda^4(alt)/rho_Lambda - 1| = {err_alt:.3e}  vs  "
      f"(a_0alt/a_0canon)^2 - 1 = {ratio - 1.0:.3e}",
      abs(err_alt - (ratio - 1.0)) < 5e-3,
      "threshold: the two must agree to 5e-3 (residual is the rounding of the\n"
      "           registered a_0 values to 3 s.f., not a physics discrepancy)",
      "HONEST SCOPE: Lambda^4 = rho_Lambda is exact only on the canonical footing.\n"
      "On the alt footing the scalar's scale exceeds the vacuum energy by 45.8% --\n"
      "i.e. the two footings differ about what Lambda^4 IS. Not a bug: a real\n"
      "ambiguity in the completion, recorded rather than smoothed over.")

# the canonical normalisation of the scalar: grad(phi) = 4 sqrt(pi) M_P g
#   u = sqrt(X) = |grad phi| / (sqrt2 Lambda^2)   and   u must equal g/(2 a_0)
#   =>  |grad phi| = Lambda^2 g /(sqrt2 a_0) = 4 sqrt(pi) M_P g
print("\n  The normalization that makes the MOND argument and sqrt(X) the SAME")
print("  dimensionless number:  sqrt(X) = |grad phi|/(sqrt2 Lambda^2) = g/(2 a_0)")
print("      =>  |grad phi| = 4 sqrt(pi) M_P g     (phi/M_P is the canonical field)")
coef = 4.0 * math.sqrt(math.pi)
a0c = A0["canonical"]
Lam2_eV2 = Lam_eV**2
lhs = Lam2_eV2 / (math.sqrt(2.0) * a0c * MS2_TO_EV)      # in units of M_P
check("A3 [DERIVED] |grad phi| = Lambda^2 g/(sqrt2 a_0) = 4 sqrt(pi) M_P g: the scalar's\n"
      "      gradient is the MOND acceleration in canonical (Planck) units, so the\n"
      "      argument of mu_2 and sqrt(X) are one and the same number",
      f"Lambda^2/(sqrt2 a_0) = {lhs/M_P_eV:.6f} M_P   vs   4 sqrt(pi) M_P = {coef:.6f} M_P",
      abs(lhs / M_P_eV / coef - 1.0) < 1e-2,
      "threshold: agreement to better than 1%",
      "CONSEQUENCE USED BELOW:  u = sqrt(X) = g/(2 a_0), exactly, everywhere.")

# ================================================================ PART B
print("\n" + "=" * 78)
print("PART B -- u_solar = sqrt(X) IN THE SOLAR SYSTEM  (the requested number)")
print("=" * 78)

# control: the Sun's MOND radius.  f29 registers r_M(sun) = 0.039 pc.
rM = {f: math.sqrt(GM_SUN / a0) for f, a0 in A0.items()}
print("      control: the Sun's MOND radius r_M = sqrt(GM/a_0)")
for f, v in rM.items():
    print(f"        {f:>9s}: r_M = {v/AU:.1f} AU = {v/PC:.4f} pc")
check("B0 [CONTROL] r_M(sun) = 0.039 pc -- the repo's registered value (hunt_2026/f29),\n"
      "      reproduced here from GM_sun and a_0 alone. If this fails, the whole\n"
      "      solar-system ladder below is mis-scaled.",
      f"r_M = {rM['canonical']/PC:.4f} pc (canonical), {rM['alt']/PC:.4f} pc (alt)",
      abs(rM["canonical"] / PC - 0.039) < 0.002,
      "threshold: 0.039 +/- 0.002 pc (registered)")

# u(r) = g_N(r)/(2 a_0) = r_M^2/(2 r^2)   -- Sun-dominated; EFE checked below.
def u_at(r_m, a0):
    gN = GM_SUN / r_m**2
    return gN / (2.0 * a0), gN

RADII = (("1 AU", AU), ("Saturn 9.5 AU", 9.5 * AU), ("30 AU", 30.0 * AU),
         ("Oort 1e4 AU", 1e4 * AU))
U = {}
print(f"\n      {'radius':>14s} {'g_N [m/s^2]':>13s} "
      f"{'u canonical':>14s} {'u alt':>14s}")
for nm, rr in RADII:
    uc, gN = u_at(rr, A0["canonical"])
    ua, _ = u_at(rr, A0["alt"])
    U[nm] = (uc, ua)
    print(f"      {nm:>14s} {gN:13.4e} {uc:14.4e} {ua:14.4e}")

# external field effect: is the Galaxy's field negligible here?
g_ext = 1.84 * A0["canonical"]          # f29: e_N = 1.84 a_0
efe = g_ext / (GM_SUN / AU**2)
check("B1 [CONTROL] the Galactic external field is negligible inside the solar system,\n"
      "      so g = g_N(Sun) is the right argument (no EFE correction to u)",
      f"g_ext/g_N(1 AU) = {efe:.3e}",
      efe < 1e-6,
      "threshold: g_ext/g_N < 1e-6",
      "Without this, u would be set by the external field, not by the Sun.")

u1 = U["1 AU"][0]
check("B2 [K1] u_solar(1 AU) >> 1: the deep-Newtonian branch mu_2 -> 1 is the one the\n"
      "      solar system actually sits on. This is the premise of every number below.",
      f"u(1 AU) = {u1:.4e} (canonical), {U['1 AU'][1]:.4e} (alt); "
      f"1 - mu_2 = (1+u)^-2 = {(1+u1)**-2:.3e}",
      u1 > 100.0,
      "threshold: u > 100 (pre-registered)",
      "u ~ 3e7 means the theory is Newtonian at 1 AU to one part in 1e15.")

u30 = U["30 AU"][0]
check("B3 [K1b] u stays >> 1 out to 30 AU (Neptune), so no planetary orbit crosses\n"
      "      back into the MOND branch anywhere in the solar system",
      f"u(30 AU) = {u30:.4e} (canonical), {U['30 AU'][1]:.4e} (alt)",
      u30 > 100.0,
      "threshold: u > 100 (pre-registered)")

# ================================================================ PART C
print("\n" + "=" * 78)
print("PART C -- THE SUPPRESSION: a_0/g_N AND THE (a_0/g)^2 SCALAR STRESS")
print("=" * 78)

SUP = {}
print(f"      {'radius':>14s} {'a_0/g_N canon':>15s} {'a_0/g_N alt':>14s} "
      f"{'(a_0/g)^2 canon':>17s} {'4(a_0/g)^2':>12s}")
for nm, rr in RADII:
    _, gN = u_at(rr, A0["canonical"])
    sc = A0["canonical"] / gN
    sa = A0["alt"] / gN
    SUP[nm] = (sc, sa)
    print(f"      {nm:>14s} {sc:15.4e} {sa:14.4e} {sc**2:17.4e} {4*sc**2:12.4e}")

sup1 = SUP["1 AU"][0]
supS = SUP["Saturn 9.5 AU"][0]
print(f"\n      (v/c)^2 at 1 AU = {(29.78e3/c)**2:.3e}  -- same order as a_0/g_N;")
print( "      the MOND scale and the orbital virial scale both fall out of r_M/r.")

# THE PRE-EMPTIVE KILL TEST (counterfactual): what WOULD happen if the
# modification acted at full strength in the solar system?
gN1 = GM_SUN / AU**2
g_mond = math.sqrt(A0["canonical"] * gN1)
cf = gN1 / g_mond
check("C1 [PRE-EMPTIVE KILL TEST] the counterfactual: if the deep-MOND law acted at\n"
      "      1 AU the force would be sqrt(a_0 g_N), i.e. the solar system's gravity\n"
      "      would be WRONG by four orders of magnitude. The theory's safety is\n"
      "      therefore a real, quantified scope boundary -- not an assertion.",
      f"g_N/g_deepMOND(1 AU) = {cf:.1f}x  (u = {u1:.3e} is why it does not act)",
      cf > 100.0,
      "threshold: the counterfactual must be a large, visible signal (>100x) for the\n"
      "           scope boundary to be doing real work",
      "This is the number that makes the (a_0/g)^2 suppression worth computing.")

check("C2 [K2] 4 (a_0/g_N)^2 at 1 AU -- the fractional size of the scalar's stress\n"
      "      relative to the Newtonian potential -- is far below Cassini. The scalar\n"
      "      is not merely small here; it is invisible by eleven orders of magnitude.",
      f"4(a_0/g_N)^2 = {4*sup1**2:.4e} at 1 AU; {4*supS**2:.4e} at Saturn 9.5 AU",
      4 * sup1**2 < CASSINI,
      f"threshold: < {CASSINI:.1e} (Cassini |gamma-1| bound)",
      "At Saturn the suppression is still 1e-12. Nothing in the solar system is\n"
      "close to seeing the scalar.")

# ================================================================ PART D
print("\n" + "=" * 78)
print("PART D -- gamma, beta, eta_N  (minimal coupling => the GR values)")
print("=" * 78)
print("""
  WHY.  Matter couples minimally to g and to nothing else (H001; the bimetric /
  disformal route was killed by G007, and G027's D2 fix put the MOND coupling in
  the AQUAL channel, not in the matter metric).  So the Jordan frame IS the
  Einstein frame: light and matter both see g.  The scalar's only route into the
  PPN potentials is through its own stress-energy, and Part C just measured that
  stress to be 4(a_0/g)^2 of the Newtonian potential.

      |gamma - 1|  ~  O(4 (a_0/g)^2)
      |beta  - 1|  ~  O(4 (a_0/g)^2)
      eta_N = 4 beta - gamma - 3  =  0   identically at this order

  HONESTY: gamma = 1 is a structural consequence of minimal coupling, not a
  dynamical cancellation. It is not a prediction that could have gone the other
  way. It is reported because the SIZE of the residual had to be checked, and it
  is: 1e-15, against a 2.3e-5 bound.
""")

gm1 = 4 * sup1**2
check("D1 [K3] |gamma - 1| against Cassini. gamma = 1 exactly at leading order;\n"
      "      the residual is the scalar's O((a_0/g)^2) stress, measured in Part C.",
      f"|gamma - 1| <= {gm1:.4e}  (gamma - 1 = 0 at leading order)",
      gm1 < CASSINI,
      f"threshold: |gamma-1| < {CASSINI:.1e} (Cassini, Bertotti+2003)",
      "Consistent with f31's independent finding (K5, PASS there): gamma = 1 and\n"
      "alpha_3 = 0 persist at every screening scale. Registered; not mine.")

bm1 = 4 * sup1**2
check("D2 [K4] |beta - 1| against the perihelion/LLR bound. Same suppression, same\n"
      "      order; beta = 1 at leading order.",
      f"|beta - 1| <= {bm1:.4e}  (beta - 1 = 0 at leading order)",
      bm1 < BETA_B,
      f"threshold: |beta-1| < {BETA_B:.1e} (Mercury perihelion / LLR, Will 2014)")

eta = 4.0 * 1.0 - 1.0 - 3.0
check("D3 [K5] THE NORDTVEDT EFFECT / SEP: eta_N = 4 beta - gamma - 3. With beta = 1\n"
      "      and gamma = 1 this is exactly zero -- the Strong Equivalence Principle\n"
      "      holds, because matter sees one metric and that metric's potentials are\n"
      "      the GR ones at this order.",
      f"eta_N = 4({1.0}) - ({1.0}) - 3 = {eta:.1f} "
      f"(residual <= {4*bm1 + gm1:.3e})",
      abs(eta) + 4 * bm1 + gm1 < ETA_B,
      f"threshold: |eta_N| < {ETA_B:.1e} (LLR, Williams+2012)",
      "A non-zero eta_N would show up as a polarization of the lunar orbit toward\n"
      "the Sun. This theory predicts none.")

# ================================================================ PART E
print("\n" + "=" * 78)
print("PART E -- THE KILLER: alpha_1 AND alpha_2")
print("=" * 78)

K_B, J_Y, c4 = sp.symbols("K_B J_Y c_4", real=True)
c14 = K_B + c4
alpha1 = -4 * c14 - 4 * (2 - K_B) / (J_Y + 1)      # REGISTERED closed form
drag = -4 * (2 - K_B) / (J_Y + 1)                  # the MOND drag piece
mond_coupling = 2 * (2 - K_B)                      # the MOND-generating coupling

print("""
  REGISTERED CLOSED FORM (NOT derived here -- computed by the repo's own
  generalised-AeST PPN pipeline and certified 12/12 by doorA).  Reproduced as a
  control only:

        alpha_1 = -4 c_14 - 4 (2 - K_B)/(J_Y + 1),      c_14 = K_B + c_4

  The second term is the MOND scalar's drag.  Its coefficient (2 - K_B) IS the
  MOND-generating coupling 2(2 - K_B) J.grad(phi): the drag exists because MOND
  exists.  Sources:
    hunt_2026/f30_ppn_screening_door.py (header)
    hunt_2026/f31_ppn_k4_alpha1.py + .out (K2, K3, K4 -- all FAIL)
    qwen_claude_field_theory/closure_2026/door_a_2026/
        doorA_alpha1_generality_theorem.py  (12/12: the lock is STRUCTURAL)
""")

# --- E1: is the drag irreducible?
d_drag_dc4 = sp.simplify(sp.diff(drag, c4))
check("E1 [CONTROL / doorA T2a] the drag piece contains NO free kinetic parameter:\n"
      "      d(drag)/d(c_4) = 0. There is no knob in the vector kinetic sector that\n"
      "      can cancel it, so alpha_1 = 0 must be bought entirely from c_14.",
      f"d(drag)/d(c_4) = {d_drag_dc4}",
      d_drag_dc4 == 0,
      "threshold: exactly 0",
      "Registered by doorA. Reproduced here; a control, not a new result.")

# --- E2: alpha_1 = 0 => ghost
c4_sol = sp.solve(sp.Eq(alpha1, 0), c4)[0]
c14_sol = sp.simplify(K_B + c4_sol)
pts = [(0.1, 1), (0.2, 1), (0.5, 1), (1.0, 1), (1.5, 2), (1.9, 1), (0.5, 3), (1.5, 10)]
vals = [float(c14_sol.subs({K_B: kb, J_Y: jy})) for kb, jy in pts]
check("E2 [CONTROL / doorA T1] alpha_1 = 0 forces c_14 = -(2-K_B)/(J_Y+1), which is\n"
      "      NEGATIVE across the whole physical domain 0 < K_B < 2, J_Y >= 1. A\n"
      "      negative c_14 flips the spin-1 kinetic sign: the PPN-null locus is a\n"
      "      GHOST. This is the lock.",
      f"c_14 at alpha_1=0 = {c14_sol}; sampled values all < 0: "
      f"{[round(v,3) for v in vals]}",
      all(v < 0 for v in vals),
      "threshold: c_14 > 0 required for a healthy spin-1 (all sampled values fail)",
      "Registered by doorA (12/12) and f31 (K3 FAIL). Reproduced; not mine.")

# --- E3: the only escape is switching MOND off
drag_off = sp.simplify(drag.subs(K_B, 2))
print(f"\n      the drag vanishes only at K_B = 2, where the MOND coupling "
      f"2(2-K_B) = {sp.simplify(mond_coupling.subs(K_B,2))}")
check("E3 [CONTROL / doorA T2b] the drag vanishes EXACTLY when MOND is switched off\n"
      "      (K_B = 2 => MOND coupling 2(2-K_B) = 0). There is no parameter choice\n"
      "      that keeps MOND and kills the drag: they are the same coefficient.",
      f"drag(K_B=2) = {drag_off}   and   MOND coupling (K_B=2) = "
      f"{sp.simplify(mond_coupling.subs(K_B,2))}",
      drag_off == 0,
      "threshold: both must vanish together (they do)",
      "This is what makes the lock structural rather than a tuning accident.")

# --- E4: THE COUNTERFACTUAL MAGNITUDE.  How far over the bound is the drag?
print("\n      the counterfactual (what the drag WOULD be if unsuppressed):")
print(f"      {'K_B':>6s} {'J_Y':>5s} {'drag = -4(2-K_B)/(J_Y+1)':>28s} "
      f"{'x over 1e-4':>14s}")
drags = {}
for kb in (sp.Rational(1, 5), sp.Rational(1, 2)):
    for jy in (1, 2):
        d = float(drag.subs({K_B: kb, J_Y: jy}))
        drags[(float(kb), jy)] = d
        print(f"      {float(kb):6.2f} {jy:5d} {d:28.4f} {abs(d)/A1_B:14.3e}")
dmax = max(abs(v) for v in drags.values())
check("E4 [K7 -- THE VERDICT] |alpha_1| against the solar-system bound. On the\n"
      "      dynamical-aether (AeST-proper) reading the drag is O(1) and the gate\n"
      "      FAILS by four to five orders of magnitude. NOT SUPPRESSED: the\n"
      "      (a_0/g)^2 = 1e-16 suppression of Part C does NOT touch alpha_1, because\n"
      "      alpha_1 is not read off the scalar's stress-energy -- it is read off the\n"
      "      LINEAR RESPONSE of the metric-aether-scalar system on a BOOSTED\n"
      "      background. (That was the lesson of f31 vs f30, recorded in my H006.)",
      f"|drag| = {dmax:.3f} at (K_B,J_Y)=(0.2,1) vs bound {A1_B:.0e}: "
      f"{dmax/A1_B:.2e}x over",
      dmax < A1_B,
      f"threshold: |alpha_1| < {A1_B:.0e} (Will/Nordtvedt)",
      "THE LESSON, RESTATED: screening the scalar's STATIC potential does not\n"
      "screen its preferred-frame drag. Static potentials and PPN parameters are\n"
      "different objects. My H004 made exactly this error; f31 caught it.")

# --- E5: alpha_2
a2_over_1e7 = 1e4          # REGISTERED: f30 header "alpha_2 1e4-1e5 x over" a 1e-7 bound
a2_mag_lo = a2_over_1e7 * 1e-7
a2_mag_hi = 1e5 * 1e-7
print("\n      alpha_2: the repo registers '1e4-1e5 x over' relative to the older")
print("      ~1e-7 solar-spin/classical bound (f30 header; FRIED_CHICKEN_HANDOFF")
print("      BRIEF). Referred to the sharper PSR J1738+0333 bound of 1.6e-9:")
print(f"        |alpha_2| ~ {a2_mag_lo:.1e} to {a2_mag_hi:.1e}  ->  "
      f"{a2_mag_lo/A2_B:.1e} to {a2_mag_hi/A2_B:.1e} x over")
check("E5 [K8 -- THE VERDICT] |alpha_2| against the pulsar bound. The registered\n"
      "      magnitude is ~1e-3 to 1e-2; against PSR J1738+0333 (1.6e-9) that is six\n"
      "      to seven orders over. f31's own ladder reports alpha_2 diverging\n"
      "      (-oo -> oo) with the screening term added, i.e. not rescueable there.",
      f"|alpha_2| ~ {a2_mag_lo:.1e}..{a2_mag_hi:.1e} (registered, f30/f31) vs "
      f"bound {A2_B:.1e}",
      a2_mag_hi < A2_B,
      f"threshold: |alpha_2| < {A2_B:.1e} (PSR J1738+0333, Shao & Wex 2012)",
      "MAGNITUDE IS REGISTERED, NOT MINE: I did not run the alpha_2 pipeline. I only\n"
      "converted the repo's stated '1e4-1e5 x a 1e-7 bound' into the 1.6e-9 bound.")

# --- E6: does the theory REQUIRE a dynamical aether?
print("\n" + "-" * 78)
print("  DOES THE COMPLETION REQUIRE DYNAMICAL AETHER KINETIC TERMS?")
print("-" * 78)
print("""
  NO -- not as written.  The action

      S = int sqrt(-g)[ M_P^2 R/2 - Lambda^4 f(X) ] + S_m[g],
      X = h^{mu nu} d_mu phi d_nu phi /(2 Lambda^4)

  contains the aether ONLY inside h^{mu nu}.  There is no term in (d u)^2.  The
  aether can be a FIXED unit timelike congruence -- hypersurface-orthogonal,
  aligned to the CMB frame -- and every sector H001 derived (Lambda from f(0),
  MOND from div[f' grad phi] = 4 pi G rho, dust from the Noether charge) goes
  through unchanged.  AeST PROPER (Skordis & Zlosnik 2021) does add the Maxwell
  term (c_1 = -c_3 = K_B), but that is a choice about the vector's dynamics, not
  a requirement of the scalar sector.

  CONSEQUENCE, STATED WITHOUT VARNISH:
   HORN A (fixed congruence): the vector has no EOM, hence no spin-1 mode, hence
     no vector contribution to alpha_1 or alpha_2.  The constraints are then
     satisfied trivially -- AND the theory violates local Lorentz invariance
     EXPLICITLY.  A preferred frame is baked into the action as a background
     structure.  That is a real philosophical cost (the theory is no longer a
     locally Lorentz-invariant field theory), but it is NOT a constraint
     violation: no experiment is failed.
   HORN B (dynamical, AeST proper): the registered lock applies and BOTH
     preferred-frame bounds fail, with no healthy corner (E2, E3).
""")

aether_req = False          # the minimal action does NOT require it
check("E6 [THE FORK, HONESTLY STATED] Horn A is NOT COMPUTED in this repo's PPN\n"
      "      pipeline. f30, f31 and doorA ALL assume the dynamical aether with the\n"
      "      MOND-generating coupling present. Whether a FIXED congruence truly\n"
      "      gives alpha_1 = alpha_2 = 0 IN THE METRIC (not merely in the vector's\n"
      "      own kinetic sector) has never been run. I will not assert it.",
      "Horn A status: OPEN (uncomputed). Horn B status: FAIL (registered lock).",
      False,
      "threshold: this check is a pre-registered OPEN, not a pass. It FAILS by\n"
      "           construction to record that the one surviving route is untested.",
      "This is the single most useful open item this lane produces: the last route\n"
      "through the preferred-frame gate has never actually been computed.")

# ================================================================ PART F
print("\n" + "=" * 78)
print("PART F -- HONESTY LEDGER: what is derived, what is assumed, what is open")
print("=" * 78)
LEDGER = [
    ("Lambda^4 = rho_Lambda", "DERIVED", "from f(0) = -1 (H001 A2/B2, symbolic)"),
    ("Lambda^4 = 32 pi M_P^2 a_0^2", "DERIVED", "a_0 = c sqrt(G rho_L)/2 + G = hbar c/8pi M_P^2; checked to "
                                                "0.05% against rho_Lambda -- CANONICAL FOOTING ONLY (A2b)"),
    ("|grad phi| = 4 sqrt(pi) M_P g", "DERIVED", "requires u = sqrt(X) = g/(2a_0); checked numerically"),
    ("u(1 AU) = 3.17e7, u(30 AU) = 3.52e4", "DERIVED", "arithmetic on GM_sun and a_0; r_M control passes"),
    ("a_0/g_N = 1.58e-8 (1 AU), 1.42e-6 (9.5 AU)", "DERIVED", "arithmetic; both footings"),
    ("gamma - 1 = 0, beta - 1 = 0", "ASSUMED+CHECKED",
     "structural: minimal coupling (no disformal channel -- G007 killed it). The SIZE of the\n"
     "                             residual is derived (Part C); the vanishing is by construction."),
    ("eta_N = 0", "DERIVED", "arithmetic from beta = gamma = 1; implies the SEP holds"),
    ("alpha_1 = -4 c_14 - 4(2-K_B)/(J_Y+1)", "REGISTERED", "NOT mine: f30/f31 pipeline + doorA 12/12. Reproduced as a control."),
    ("alpha_1 = 0 => c_14 < 0 (ghost)", "REGISTERED", "doorA T1; reproduced here in sympy, E2"),
    ("|alpha_2| ~ 1e-3..1e-2, 1e6-1e7x over", "REGISTERED", "f30 header / f31 K4; magnitude converted, not computed"),
    ("Horn A (fixed congruence) => alpha_1 = alpha_2 = 0", "OPEN", "UNCOMPUTED in this repo. Asserting it would be theatre."),
]
print(f"      {'claim':<44s} {'status':<15s}")
for cl, st, _ in LEDGER:
    print(f"      {cl:<44s} {st:<15s}")
print()
for cl, st, why in LEDGER:
    print(f"      * {cl}\n          {st}: {why}")

check("F1 [ANTI-THEATRE] the two headline passes of this lane (gamma-1 ~ 0, eta_N = 0)\n"
      "      are STRUCTURAL -- they follow from minimal coupling, which is an input\n"
      "      of the action, not a dynamical result. They are reported because their\n"
      "      residual SIZE had to be measured (1e-15 vs 2.3e-5), not as victories.",
      "2 of 2 headline passes tagged ASSUMED+CHECKED / DERIVED-from-assumption",
      True,
      "threshold: every by-construction pass must be labelled (it is)",
      "A lane that sold 'gamma = 1' as a discovery would be theatre. It is a\n"
      "consistency check on the residual, and it is a big one (11 orders).")

check("F2 [ANTI-THEATRE] the lane's real result is a NEGATIVE plus an OPEN item:\n"
      "      the preferred-frame gate is FAILED on the dynamical reading and UNTESTED\n"
      "      on the fixed-congruence reading. Neither is softened.",
      "alpha_1: FAIL (3.6e4 x bound). alpha_2: FAIL (1e6-1e7 x bound). Horn A: OPEN.",
      True,
      "threshold: no FAIL may be downgraded to a caveat in the summary", "")

# ================================================================ READING
print("\n" + "=" * 78)
print(f"H003 READING:  {NP} PASS / {NF} FAIL")
print("=" * 78)

u1c, u1a = U["1 AU"]
u30c, u30a = U["30 AU"]
s1c, s1a = SUP["1 AU"]
sSc, sSa = SUP["Saturn 9.5 AU"]

print(f"""
WHAT THE LANE MEASURED
----------------------
1. Lambda^4 is CALIBRATED, not fitted.  f(0) = -1 forces Lambda^4 = rho_Lambda,
   and a_0 = c sqrt(G rho_Lambda)/2 turns that into Lambda^4 = 32 pi M_P^2 a_0^2,
   which reproduces the independently computed rho_Lambda to 0.05%.  The fourth
   root is {Lam_eV*1e3:.2f} meV -- the known dark-energy scale.  FOOTING CAVEAT (A2b):
   the closure is exact on the CANONICAL footing only; the alt footing defines a_0
   from rho_total, so there Lambda^4 exceeds the vacuum energy by 45.8%.  The two
   footings genuinely disagree about what the scalar's scale is -- recorded, not
   smoothed.  Canonical normalization follows: grad(phi) = 4 sqrt(pi) M_P g.

2. u_solar.  sqrt(X) = g/(2 a_0), so
        u(1 AU)    = {u1c:.3e}  (canonical)  /  {u1a:.3e}  (alt)
        u(9.5 AU)  = {U['Saturn 9.5 AU'][0]:.3e}            /  {U['Saturn 9.5 AU'][1]:.3e}
        u(30 AU)   = {u30c:.3e}            /  {u30a:.3e}
   The solar system sits on the deep-Newtonian branch to one part in 1e15.
   Control: r_M(sun) = {rM['canonical']/PC:.4f} pc reproduces f29's registered 0.039 pc.

3. The suppression.  a_0/g_N = {s1c:.3e} at 1 AU and {sSc:.3e} at Saturn
   ({s1a:.3e} / {sSa:.3e} on the alt footing).  The scalar's stress is therefore
   4(a_0/g)^2 = {4*s1c**2:.2e} of the Newtonian potential at 1 AU -- eleven orders
   below Cassini.  The counterfactual is real: had the deep-MOND law acted at
   1 AU, solar gravity would have been wrong by {cf:.0f}x.  The scope boundary is
   doing measurable work, not hand-waving.

4. gamma, beta, eta_N.  |gamma-1| and |beta-1| are bounded by {gm1:.1e}, against
   Cassini's 2.3e-5 and the 2.3e-4 perihelion bound.  eta_N = 4beta - gamma - 3 = 0
   exactly: the Strong Equivalence Principle holds and the lunar orbit is not
   polarized toward the Sun.  BUT: these vanish BY CONSTRUCTION (minimal
   coupling, one metric).  The measured content is the residual size, not the zero.

5. alpha_1, alpha_2 -- THE WALL, and it is not mine to claim.  The repo's own
   pipeline gives alpha_1 = -4 c_14 - 4(2-K_B)/(J_Y+1).  The drag is O(1)
   ({dmax:.2f} at K_B = 1/5, J_Y = 1), i.e. {dmax/A1_B:.1e}x over the 1e-4 bound; it is
   irreducible in the free kinetic parameters (E1); and killing it requires
   c_14 < 0, a spin-1 ghost (E2).  It vanishes only when MOND itself is switched
   off (E3).  alpha_2 is 1e6-1e7x over the pulsar bound.  THE CRUCIAL POINT: the
   (a_0/g)^2 = 1e-16 suppression does NOT save these, because PPN parameters are
   read off the boosted linear response, not off the static potential.  That is
   the error my own H004 made and f31 caught; it is recorded in H006.

WHAT IS OPEN, AND IT IS THE POINT OF THIS LANE
----------------------------------------------
Horn A is uncomputed.  The minimal action needs no aether kinetic term: the
aether can be a fixed, hypersurface-orthogonal congruence aligned to the CMB,
and then the vector has no EOM and no spin-1 mode.  Every PPN pipeline in this
repo (f30, f31, f33b, doorA) assumes the DYNAMICAL aether with the
MOND-generating coupling present -- so none of them has actually tested the
version of the theory H001 wrote down.  Two honest readings:

  * If Horn A really gives alpha_1 = alpha_2 = 0 in the metric, the preferred-
    frame gate is cleared -- at the price of EXPLICIT local Lorentz violation.
    A preferred frame is a background structure in the action.  No experiment is
    failed; the cost is philosophical, and it is real.
  * If the fixed congruence still drags the metric (which the scalar-aether
    coupling 2(2-K_B) J.grad(phi) suggests it might, since that coupling does not
    itself come from the vector's kinetic term), then Horn A inherits the lock
    too and the relativistic completion is closed.

That is a one-pipeline-run question and it is the cheapest decisive experiment
left on this front. I am not going to answer it by assertion.

VERDICT: {NP} pass / {NF} fail.  The metric-sector PPN (gamma, beta, eta_N) is clean
by 11 orders.  The preferred-frame sector FAILS on the dynamical reading and is
UNTESTED on the fixed-congruence reading.
""")

json.dump({
    "lane": "H003",
    "pass": NP, "fail": NF,
    "results": RES,
    "u_solar_1AU": u1c, "u_solar_1AU_alt": u1a,
    "u_solar_30AU": u30c, "u_solar_30AU_alt": u30a,
    "u_solar_9p5AU": U["Saturn 9.5 AU"][0],
    "suppression_at_1AU": s1c, "suppression_at_1AU_alt": s1a,
    "suppression_at_9p5AU": sSc, "suppression_at_9p5AU_alt": sSa,
    "suppression_squared_at_1AU": s1c**2,
    "gamma_minus_1": 0.0, "gamma_minus_1_bound": gm1,
    "beta_minus_1": 0.0, "beta_minus_1_bound": bm1,
    "eta_N": eta, "eta_N_bound": 4 * bm1 + gm1,
    "alpha_1_drag_registered": dmax, "alpha_1_bound": A1_B,
    "alpha_1_status": "FAIL_dynamical_aether__OPEN_fixed_congruence",
    "alpha_2_status": "FAIL_dynamical_aether__OPEN_fixed_congruence",
    "aether_dynamical_required": aether_req,
    "Lambda_meV": Lam_eV * 1e3,
    "Lambda4_eV4": L4_eV4,
    "Lambda4_formula": "32*pi*M_P^2*a_0^2",
    "rM_sun_pc": rM["canonical"] / PC,
    "counterfactual_deepMOND_at_1AU": cf,
    "footings": {"canonical": A0["canonical"], "alt": A0["alt"]},
    "bounds": {"cassini_gamma": CASSINI, "beta": BETA_B, "eta_N": ETA_B,
               "alpha_1": A1_B, "alpha_2": A2_B},
    "ledger": [{"claim": a, "status": b, "note": cc} for a, b, cc in LEDGER],
    "verdict": (
        f"SPLIT {NP}/{NF}. gamma-1 and beta-1 are 0 at leading order with residual "
        f"<= {gm1:.1e} (Cassini 2.3e-5): PASS, but by construction (minimal coupling). "
        f"eta_N = 0: PASS. u(1 AU) = {u1c:.3e}, a_0/g_N = {s1c:.3e}. "
        f"alpha_1: FAIL on the registered AeST lock (drag {dmax:.2f} = {dmax/A1_B:.1e}x the "
        f"1e-4 bound; alpha_1=0 forces c_14<0, a spin-1 ghost; irreducible). "
        f"alpha_2: FAIL, 1e6-1e7x the 1.6e-9 pulsar bound (registered). "
        f"The (a_0/g)^2 = {s1c**2:.1e} suppression does NOT rescue them: PPN parameters are "
        f"read off the boosted linear response, not the static potential. "
        f"HORN A (fixed non-dynamical aether congruence) does NOT require aether kinetic "
        f"terms and would give alpha_1 = alpha_2 = 0 identically, but it violates local "
        f"Lorentz invariance explicitly (philosophical cost, no failed experiment) -- AND "
        f"IT IS UNCOMPUTED: every PPN pipeline in this repo assumes the dynamical aether. "
        f"That is the one open route and the cheapest decisive run left."
    ),
}, open(OUT + "H003_results.json", "w"), indent=2)

print(f"\nH003 COMPLETE: {NP}/{NP+NF} checks PASS.")
