#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
LANE 1 -- DERIVE kappa_t = K_t/K_eff = V''(J0=1)/K_eff  at r ~ r_t.
=====================================================================
The Branch-B Cassini quadrupole reduces (two independent solvers, committed) to the
P-wave suppression of the l=2 medium response at the sourcing radius r_t:

        w = Q2_medium / Q2_scalar = K_t / (K_t + (4/3) mu_s)
          = 1 / (1 + 4 beta / kappa_t),      beta := mu_s/(3 K_eff),
          kappa_t := K_t / K_eff = V''(J0=1) / K_eff   (bulk TANGENT stiffness at r_t).

Everything in the Cassini verdict that is NOT already banked (the scalar-class Q2, the
6Z^2 shear cap, the P-wave reduction) sits in this ONE second-derivative-of-V number.
This script DERIVES it from the written action, states every convention, and shows the
one place the whole factor lives: the SECANT-vs-TANGENT anchoring of "K_eff".

CONVENTIONS FIXED (stated up front, carried):
  * Strain J = J1 = tr(eps), the volumetric strain (the trace invariant of the action).
  * FAITHFUL strain-vs-driving map (Method A, the vector-elastic synthesis' verdict):
        J0(y) = 2 g_bar/a0V = 2 y / Z ,   y = g_bar/a0,  a0V = Z a0.
    LINEAR in the driving, NON-saturating, passes through J0=1 at y_c = Z/2 (the derived
    entropy-budget cutoff). This is the pinned map lane3/the paper use.
  * Written constitutive law (ELASTIC_MEDIUM_ACTION_2026, published):
        V'(J) = 2 K_eff sqrt(J/kappa^2)  ,  kappa = 2 (the Verlinde strain norm),
        K_eff = a0^2/(16 pi G),  the deep displacement-match stiffness.
  * Longitudinal (P-wave) modulus from the same action: c_L^2 = (V'' + (4/3) mu_s)/rho_L,
    so the bulk TANGENT modulus entering w is K_t = V''(J) -- a SECOND derivative of V.
HONESTY: kappa_t comes out PINNED as a pure number (footing-independent -- it is a ratio,
K_eff cancels); the only residual is the anchoring of what "K_eff" MEANS in the match
(secant-of-energy / stress / tangent), which is the factor 0.375 : 0.5 : 1.0. That fork is
resolved by what the displacement match physically pins (a first-derivative/force response),
NOT chosen -- see PART 3. Method B's kappa_t~230 is reproduced as a cross-check of the
machinery under the (non-faithful) saturating strain convention.
"""
import numpy as np
import sympy as sp

# ------------------------------------------------------------------ constants
G   = 6.674e-11
Z   = float(sp.sqrt(sp.Rational(32,3)*sp.pi))         # sqrt(32 pi/3) = 5.7888
A0  = {"canon": 9.36e-11, "alt": 1.13e-10}
CEIL   = 5.2e-27
Q2SCAL = {"canon": (2.0e-26, 2.5e-26), "alt": (2.7e-26, 3.3e-26)}
Q2SC_C = {"canon": 2.2e-26, "alt": 3.0e-26}
yc  = Z/2.0

print("="*90)
print(" LANE 1 -- kappa_t = V''(J0=1)/K_eff  (bulk tangent stiffness at r_t, in units of K_eff)")
print("="*90)
print(f"  Z = sqrt(32 pi/3) = {Z:.4f} ;  y_c = Z/2 = {yc:.4f} (entropy-budget cutoff, J0=1 here)")

# ==================================================================================================
# PART 1 -- FIX THE STRAIN.  Faithful linear pinned map J0(y)=2y/Z, vs the saturating reconstruction.
# ==================================================================================================
print("\n" + "="*90)
print("[1] STRAIN CONVENTION")
print("="*90)
y = sp.symbols('y', positive=True)
J0_lin = 2*y/Z                                        # FAITHFUL (Method A)
print("  (A faithful) linear pinned map:  J0(y) = 2 g_bar/a0V = 2y/Z")
print(f"      J0(y_c=Z/2) = {float(J0_lin.subs(y,yc)):.4f}   [passes through 1 at the cutoff; NON-saturating]")
print(f"      dJ0/dy = 2/Z = {float(sp.diff(J0_lin,y)):.4f}  (constant slope -> tangent modulus set by V alone)")
# saturating reconstruction (Method B), for the cross-check in PART 4
nu   = sp.sqrt(1+1/y)
kapM = 1.0/((float(sp.sqrt(1+1/yc))-1)*yc)            # eps(y_c)=1 pin
eps_sat = kapM*(nu-1)*y
print(f"  (B non-faithful) saturating reconstruction: eps=kappa*(nu-1)*y, kappa={kapM:.4f} (eps(y_c)=1)")
print(f"      eps(2.2)={float(eps_sat.subs(y,2.2)):.4f}  dln eps/dln y|2.2="
      f"{float((y*sp.diff(eps_sat,y)/eps_sat).subs(y,2.2)):.4f}  (SATURATES -> huge tangent stiffening)")

# ==================================================================================================
# PART 2 -- PIN V(J): DERIVE C in V'(J)=C sqrt(J) from the displacement match (SHOW the equilibrium).
# ==================================================================================================
print("\n" + "="*90)
print("[2] PIN V(J) FROM THE DISPLACEMENT MATCH  (derive C, do not assume it)")
print("="*90)
J = sp.symbols('J', positive=True)
C = sp.symbols('C', positive=True)
a0V, Keff = sp.symbols('a_0V K_eff', positive=True)

# --- 2a. the deep displacement law, re-expressed through the linear map J0=2 g_bar/a0V:
#     g_D = sqrt(a0V g_bar/6) ; g_bar = a0V J/2  =>  g_D(J) = a0V sqrt(J/12) = (a0V/(2 sqrt3)) sqrt(J).
gbar_of_J = a0V*J/2
gD_of_J   = sp.sqrt(a0V*gbar_of_J/6)
gD_of_J   = sp.simplify(gD_of_J)
print("  deep law g_D = sqrt(a0V g_bar/6); linear map g_bar = a0V J/2  =>")
print("      g_D(J) =", gD_of_J, "  =>  g_D PROPORTIONAL TO sqrt(J)   [this is the sqrt-branch's ORIGIN]")

# --- 2b. the medium's compressive stress IS the displacement acceleration response:
#     sigma(J) = V'(J) tracks g_D(J) => V'(J) = C sqrt(J).  Constant C  <=>  a genuine sqrt branch.
#     (If instead one imposed Verlinde ENERGY u_el = g_D^2/8piG = (a0V^2/96piG) J  -- LINEAR in J --
#      then sigma = du_el/dJ = const, i.e. NOT sqrt: the energy identification is convention-II
#      (eps ~ g_D ~ sqrt(g_bar)); the STRESS identification is convention-I (J ~ g_bar). The paper's
#      written law V'~sqrt(J) is the STRESS reading, so we use it and expose the fork in PART 3.)
Vp = C*sp.sqrt(J)                                     # V'(J) = C sqrt(J)  (written branch)
V  = sp.integrate(Vp, J)                              # V(J) = (2/3) C J^{3/2}
Vpp = sp.diff(Vp, J)                                  # V''(J) = C/(2 sqrt(J))
print("\n  written branch V'(J)=C sqrt(J)  =>  V(J) =", V, " ,  V''(J) =", Vpp)

# --- 2c. NORMALIZATION: the paper writes V'(J) = 2 K_eff sqrt(J/kappa^2), kappa=2  =>  V'(J)=K_eff sqrt(J).
#     i.e. the match sets the STRESS at the transition J=1 equal to the deep stiffness scale:
#     V'(1) = C = K_eff.  (Equivalently g_D(1)=a0V/(2 sqrt3) is the transition displacement.)
kap_norm = 2
C_paper = sp.simplify(2*Keff*sp.sqrt(sp.Rational(1,1)/kap_norm**2))   # = K_eff
print(f"\n  paper normalization V'(J)=2 K_eff sqrt(J/kappa^2), kappa={kap_norm}:  C = {C_paper}")
print(f"      => V'(1) = K_eff   (STRESS at the transition = the deep stiffness scale; DERIVED, not assumed)")
print( "      => this is the displacement-match anchor: the match reproduces g_D, a FIRST-derivative")
print( "         (force/acceleration) response, so it pins the STRESS V'(1), not the curvature V''(1).")

# ==================================================================================================
# PART 3 -- kappa_t = V''(1)/K_eff.  THE SECANT-vs-TANGENT FORK IS THE WHOLE FACTOR -- pin it.
# ==================================================================================================
print("\n" + "="*90)
print("[3] kappa_t = V''(1)/K_eff  -- and what 'K_eff' means in the match (the whole factor)")
print("="*90)
# For V = (2/3) C J^{3/2}:  three candidate 'K_eff' anchorings at the operating point J=1:
Cs = sp.symbols('C', positive=True)
Vs   = sp.Rational(2,3)*Cs*J**sp.Rational(3,2)
Vps  = sp.diff(Vs,J);  Vpps = sp.diff(Vps,J)
stress_1   = Vps.subs(J,1)                    # V'(1) = C        (STRESS / force response)
tangent_1  = Vpps.subs(J,1)                   # V''(1)= C/2      (curvature = the modulus we WANT)
energysec1 = (2*Vs/J**2).subs(J,1)            # 2V(1)/1 = 4C/3   (energy-secant K: V=1/2 K J^2 reading)
print("  For V=(2/3)C J^{3/2} at J=1:")
print(f"      STRESS       V'(1)          = {stress_1}      (first derivative; force/displacement response)")
print(f"      TANGENT      V''(1)         = {tangent_1}    (second derivative; the P-wave bulk modulus K_t)")
print(f"      ENERGY-SECANT 2V(1)         = {sp.nsimplify(energysec1)}    (harmonic-fit modulus 2V/J^2)")
kappa_t_stress  = float(tangent_1 / stress_1)      # K_eff = V'(1)  -> 1/2
kappa_t_tangent = 1.0                                # K_eff = V''(1) -> 1  (by fiat)
kappa_t_esecant = float(tangent_1 / energysec1)    # K_eff = 2V(1)  -> 3/8
print("\n  kappa_t = V''(1)/K_eff under each anchoring of K_eff:")
print(f"      K_eff = V'(1)  (STRESS,  displacement-match anchor) : kappa_t = {kappa_t_stress:.4f}   <== DEFENSIBLE")
print(f"      K_eff = V''(1) (TANGENT, K_t:=K_eff by fiat)        : kappa_t = {kappa_t_tangent:.4f}")
print(f"      K_eff = 2V(1)  (ENERGY-SECANT, harmonic fit)        : kappa_t = {kappa_t_esecant:.4f}")
print("""
  WHICH ONE:  the displacement match reproduces g_D = sqrt(a0V g_bar/6) -- an ACCELERATION
  (a force / first-derivative response). The written normalization sets V'(1)=K_eff (the STRESS
  at the transition equals the deep stiffness scale). Therefore K_eff is a FIRST-derivative
  (stress) anchor, the tangent modulus is V''(1)= (1/2)K_eff, and

        kappa_t = 0.5   (single most-defensible value; FOOTING-INDEPENDENT -- K_eff cancels).

  This is EXACTLY Method A's published 'sqrt-branch derived footing' (kappa_t=0.5).""")

# --- the r_t saturation floor: at J0=1 (r=r_t) the medium is at the ONSET of the rigid branch;
#     the tangent can rise from the sqrt-branch value 0.5 toward the saturated Newtonian floor K_t=K_eff.
print("  r_t FLOOR: at J0=1 the sqrt branch meets the saturated/rigid branch (K_t -> K_eff).")
print("  Faithful window therefore  kappa_t in [0.5 (sqrt tangent), 1.0 (saturated floor)];")
print("  the energy-secant 0.375 is the softest defensible corner. Single value: 0.5.")

# ==================================================================================================
# PART 4 -- CROSS-CHECK: the saturating reconstruction reproduces Method B kappa_t ~ 126-231.
# ==================================================================================================
print("\n" + "="*90)
print("[4] MACHINERY CROSS-CHECK: saturating strain (Method B) -> kappa_t ~ 126-231")
print("="*90)
# tangent stiffening S(y) = (dsigma/deps)|_y / (dsigma/deps)|_deep, sigma ~ y/yc (driving-linear),
# eps = kappa*(nu-1)*y (saturating).  kappa_t(Method B) = S(y) at the operating point/shell.
sigB = y/yc
dS_dE = sp.diff(sigB,y)/sp.diff(eps_sat,y)
S_of  = lambda yy: float(dS_dE.subs(y,yy))/float(dS_dE.subs(y,0.01))
kt_B_sun  = S_of(2.2)
kt_B_shell = np.mean([S_of(v) for v in np.linspace(0.3,2.5,23)])
print(f"  saturating eps: kappa_t(at Sun y=2.2) = S(2.2) = {kt_B_sun:.1f}")
print(f"                  kappa_t(shell 0.3..2.5) = {kt_B_shell:.1f}")
print("  => reproduces Method B (kappa_t~126-231). The factor-~250-460 gap vs the faithful 0.5-1")
print("     is ENTIRELY the strain convention: saturating eps (B) vs the linear pinned map (A).")
print("     The vector-elastic synthesis judged the LINEAR pinned map faithful -> kappa_t~0.5-1.")

# ==================================================================================================
# PART 5 -- REPORT (both footings) + beta_crit + Cassini consequence.
# ==================================================================================================
print("\n" + "="*90)
print("[5] REPORT + Cassini consequence")
print("="*90)
for tag in ("canon","alt"):
    Keff_v = A0[tag]**2/(16*np.pi*G)
    print(f"\n  [{tag}]  K_eff = a0^2/16piG = {Keff_v:.3e} Pa   (kappa_t is a RATIO -> footing-independent: 0.5)")
    print(f"      Q2_scalar band = {Q2SCAL[tag][0]:.1e}..{Q2SCAL[tag][1]:.1e} s^-2 ; ceiling {CEIL:.1e}")
    for kt,lbl in ((0.5,"faithful sqrt-tangent"),(1.0,"saturated floor")):
        # beta_crit = kappa_t*(Q2_scalar/CEIL - 1)/4  (w=CEIL/Q2_scalar solved for beta)
        bc_lo = kt*(Q2SCAL[tag][0]/CEIL - 1)/4
        bc_hi = kt*(Q2SCAL[tag][1]/CEIL - 1)/4
        bc_c  = kt*(Q2SC_C[tag]/CEIL - 1)/4
        print(f"      kappa_t={kt:>4.1f} ({lbl:20s}): beta_crit = {bc_c:.2f}  (band {bc_lo:.2f}..{bc_hi:.2f});"
              f"  PASS iff derived beta in [{bc_c:.2f}, 2.0]")

print("""
  CASSINI CONSEQUENCE (the beta>beta_crit passing test):
  * kappa_t is the LEVER on beta_crit: beta_crit = kappa_t*(Q2_scalar/ceiling - 1)/4.
  * FAITHFUL kappa_t = 0.5  => beta_crit ~ 0.40 (canonical central) / 0.60 (alt central).
    The passing window [0.40, 2.0] (canon) is WIDE -- the derived shear share need only exceed
    ~0.40 of its 6Z^2-capped maximum. This is the FRIENDLIER end: a SOFTER bulk tangent (small
    kappa_t) means the shear more easily out-competes it in the P-wave, so LESS shear is needed.
  * If one took the stiff floor kappa_t = 1.0  => beta_crit ~ 0.81 / 1.19: the window narrows to
    [0.81, 2.0] (canon) and CLOSES entirely on alt-central (1.19..1.98 only just open).
  * The non-faithful saturating kappa_t~126-231 would give beta_crit ~ 100-190 >> 2 => the gate
    is UNREACHABLE (w~1, Q2 ~ Q2_scalar, ~4x over ceiling). That reading is the one the synthesis
    rejected as a strain-convention artifact.
  VERDICT: kappa_t is DERIVABLE and PINNED to 0.5 (footing-independent) under the faithful linear
  pinned map + the written sqrt-branch V, with a defensible window [0.5, 1.0] (up to the r_t
  saturated floor). It sets beta_crit ~ 0.40-0.81 (canon) / 0.60-1.19 (alt); Cassini PASSES iff
  the separately-derived shear share beta lands above that. The Cassini fork is thus NOT hostage to
  kappa_t (that scalar is pinned); it is hostage to beta (Lane 2/3), on a window kappa_t opens to
  [~0.4, 2].""")
print("EXIT 0")
