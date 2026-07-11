#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROUTE B -- does any MICROPHYSICAL principle PIN the Poisson ratio (the mu_s/K_F split,
           equivalently beta = mu_s/(3 K_eff)) of the written elastic dark-energy solid?
================================================================================================
Branch-B Cassini quadrupole:  Q2_med = w * Q2_scalar,  w = 1/(1 + 4 beta/kappa_t),  kappa_t=0.5 PINNED.
PASS iff beta >= beta_crit = kappa_t*(Q2_scalar/CEIL - 1)/4  (a FLOOR; bigger beta = stiffer shear = easier pass).
Lane 2 already showed: the action writes ONE shear relation  K_F + mu_s/6 = K_eff  (the l=0 Verlinde
monopole match), so beta is BOUNDED (0,2) but the split (Poisson ratio) is NOT pinned by that alone.

This route stress-tests FOUR candidate closures that might supply the missing second relation:
  (1) VERLINDE's own emergent-elasticity stress law (SciPost Phys 2 016, eq 7.20)
  (2) ENW three-scalar solid EFT (arXiv:1210.0569, eq 2.16): does SO(3)+w pin shear/bulk?
  (3) STABILITY / POSITIVITY / CAUSALITY: do they carve more than 0<beta<2?
  (4) the "1/6" lemma re-read as an energy partition -> beta=2/7: derivation or coincidence?

VERDICT: PIN (Cassini closes at that value) or FREE (genuine residual material parameter)?

Literature parameters QUOTED with their definitions:
  * ENW eq (2.16):   c_L^2 = 1 + (2/3) F_XX X^2/F_X + (8/9)(F_Y+F_Z)/F_X ,
                     c_T^2 = 1 + (2/3)(F_Y+F_Z)/F_X .
    Shear enters ONLY via (F_Y+F_Z); the extra longitudinal stiffness enters via F_XX (independent).
  * Verlinde eq (7.20):  sigma_ij = (a0^2/8piG)(eps_ij - eps_kk delta_ij)
    => 2 mu = a0^2/8piG => mu = a0^2/16piG ;  lambda = -a0^2/8piG = -2 mu ;
       P-wave modulus M = lambda + 2 mu = 0 (Verlinde states it explicitly: pressure waves have zero velocity).
"""
import numpy as np
import sympy as sp

# ------------------------------------------------------------------ constants (SI) + footings
c_l  = 2.99792458e8
G    = 6.674e-11
Z    = float(np.sqrt(32*np.pi/3.0))                 # 5.7888
A0   = {"canonical": 9.36e-11, "alt": 1.13e-10}
Q2_CEIL = 5.2e-27                                   # Cassini 2-sigma ceiling [s^-2]
Q2_SCAL = {"canonical": 2.2e-26, "alt": 3.0e-26}    # banked scalar-class Q2 (central, both solvers agree)
KAPPA_T = 0.5                                        # Lane-1 PINNED bulk tangent stiffness

def w_pwave(beta, kt=KAPPA_T):  return 1.0/(1.0 + 4.0*beta/kt)
def beta_crit(foot, kt=KAPPA_T):
    return kt*(Q2_SCAL[foot]/Q2_CEIL - 1.0)/4.0
def cassini(beta, foot, kt=KAPPA_T):
    bc = beta_crit(foot, kt); q2 = w_pwave(beta,kt)*Q2_SCAL[foot]
    return ("PASS" if beta>=bc else f"FAIL {q2/Q2_CEIL:.2f}x"), bc

print("="*96)
print(" ROUTE B -- can any microphysical principle PIN the Poisson ratio (beta = mu_s/3K_eff)?")
print("="*96)
for foot in ("canonical","alt"):
    print(f"   beta_crit [{foot:<9}] = {beta_crit(foot):.3f}   (Cassini PASS floor, kappa_t=0.5)")
BC_CANON = beta_crit("canonical"); BC_ALT = beta_crit("alt")

# ================================================================================================
# CANDIDATE (1) -- VERLINDE's emergent elasticity  (SciPost Phys 2 016, sec 6-7)
# ================================================================================================
print("\n" + "="*96)
print("[1] VERLINDE stress law eq (7.20):  sigma_ij = (a0^2/8piG)(eps_ij - eps_kk delta_ij)")
print("="*96)
mu_sym, lam, K_eff_sym = sp.symbols('mu lambda K_eff', real=True)
# Verlinde: coefficient of eps_ij = 2 mu = a0^2/8piG ;  coefficient of eps_kk delta_ij = lambda = -a0^2/8piG
# In K_eff units (K_eff = a0^2/16piG):  2 mu = 2 K_eff => mu_V = K_eff ;  lambda_V = -2 K_eff
mu_V   = 1.0     # in units of K_eff = a0^2/16piG
lam_V  = -2.0    # in units of K_eff
Mwave  = lam_V + 2*mu_V         # P-wave (longitudinal) modulus
Kbulk  = lam_V + 2*mu_V/3.0     # bulk modulus (d=3):  K = lambda + 2mu/(d-1) = lambda + mu
Kbulk3 = lam_V + mu_V           # d=3 convention K=lambda+mu (Verlinde's "K=lambda+2mu/(d-1)")
poisson_V = lam_V/(2*(lam_V+mu_V))
print(f"    => mu_V   = {mu_V:.3f} K_eff   (Verlinde SHEAR modulus = a0^2/16piG = the framework's K_eff exactly)")
print(f"    => lambda_V = {lam_V:.3f} K_eff = -2 mu_V")
print(f"    => P-wave modulus M = lambda+2mu = {Mwave:.3f} K_eff  (Verlinde: 'vanishing P-wave modulus', c_L=0)")
print(f"    => bulk modulus K = lambda+mu = {Kbulk3:.3f} K_eff  (NEGATIVE)")
print(f"    => Poisson ratio nu = lambda/2(lambda+mu) = {poisson_V:.3f}  (=+1, stability BOUNDARY lambda+2mu>=0 SATURATED)")
print("""
    READING FOR THE FRAMEWORK:
    (i)  Verlinde PINS a definite elastic structure (lambda=-2mu, nu=+1, M=0) -- so 'emergent
         elasticity' is NOT Poisson-free; it fixes the ratio. BUT it fixes a DEGENERATE medium:
         zero longitudinal stiffness and a NEGATIVE bulk modulus (lambda+mu<0).
    (ii) That structure is FORBIDDEN by the framework's OWN ghost/stability wall: the framework
         requires V''=K_F>0 (positive bulk stiffness). Verlinde's M=0 needs K_F+4mu_s/3=0 => K_F<0.
         So the framework CANNOT adopt Verlinde's Poisson ratio; the two media disagree in the bulk.
    (iii)The ONLY transferable number is the shear MAGNITUDE mu_V = a0^2/16piG. If (and only if) one
         identifies the framework shear modulus mu_s with Verlinde's mu_V, then mu_s = a0^2/16piG.""")
# transfer: mu_s = mu_V = a0^2/16piG.  But framework K_eff = a0^2/16piG too => mu_s = K_eff => beta:
beta_V_transfer = 1.0/3.0    # mu_s=K_eff => beta = mu_s/(3 K_eff) = 1/3
print(f"         Then mu_s = K_eff  =>  beta = mu_s/(3 K_eff) = 1/3 = {beta_V_transfer:.3f}")
print(f"         BUT this DOUBLE-COUNTS a0^2/16piG (Verlinde's mu vs framework's K_eff) and still")
print(f"         sits at the TOP of the natural window. Cassini at beta=1/3:")
for foot in ("canonical","alt"):
    tag,bc = cassini(beta_V_transfer, foot)
    print(f"            [{foot:<9}] beta=0.333 vs beta_crit={bc:.3f}  ->  {tag}")
print("    VERDICT (1): Verlinde does NOT deliver a framework-ADMISSIBLE pin (his nu=+1 violates K_F>0).")
print("                 His only transferable magnitude gives beta<=1/3, which MARGINALLY FAILS canonical.")

# ================================================================================================
# CANDIDATE (2) -- ENW three-scalar solid EFT  (arXiv:1210.0569, eq 2.16)
# ================================================================================================
print("\n" + "="*96)
print("[2] ENW solid EFT eq (2.16): are shear & bulk INDEPENDENT Lagrangian data, or pinned by SO(3)+w?")
print("="*96)
FX, FXX, FYZ, X = sp.symbols('F_X F_XX F_YZ X', real=True)   # FYZ := F_Y + F_Z
cT2 = 1 + sp.Rational(2,3)*FYZ/FX                               # transverse (shear) speed^2
cL2 = 1 + sp.Rational(2,3)*FXX*X**2/FX + sp.Rational(8,9)*FYZ/FX # longitudinal (bulk) speed^2
print("    c_T^2 = 1 + (2/3)(F_Y+F_Z)/F_X            <- SHEAR: depends ONLY on the combo (F_Y+F_Z)")
print("    c_L^2 = 1 + (2/3)F_XX X^2/F_X + (8/9)(F_Y+F_Z)/F_X   <- BULK: adds an INDEPENDENT term F_XX")
diff = sp.simplify(cL2 - cT2)
print(f"    c_L^2 - c_T^2 = {diff}")
print("""    => The SHEAR sector is governed by (F_Y+F_Z); the extra LONGITUDINAL stiffness by F_XX.
       F_XX (2nd deriv wrt the compression invariant X) and (F_Y+F_Z) (1st derivs wrt the shear
       invariants Y,Z) are INDEPENDENT data of the free Lagrangian F(X,Y,Z). The internal SO(3)
       fixes only the FORM (Y,Z always enter as F_Y+F_Z); it does NOT relate F_XX to (F_Y+F_Z).""")
# EOS: for a solid the background is unstrained (isotropic), so w is set by F, F_X at background ONLY.
print("""    EOS w:  a solid sits UNSTRAINED at the background => the background stress is isotropic and
       w = p/rho is fixed by F and X F_X at the background. The shear modulus is a PERTURBATIVE
       (2nd-order) quantity that does NOT enter the background => w=-1 places NO constraint on it.
       (Concretely: w=-1 needs the background F to mimic a cosmological constant; (F_Y+F_Z) is free.)""")
# map to framework:  c_T^2 ~ mu_s/rho_L,  c_L^2 ~ (V''+4mu_s/3)/rho_L.  The bulk term V'' <-> F_XX-controlled,
# independent of mu_s <-> (F_Y+F_Z).  Hence mu_s/K_F (the Poisson ratio, = beta) is a FREE FUNCTION.
print("    MAP: c_T^2=mu_s/rho_L (shear) and the extra c_L^2 term=V''(bulk) track the SAME independent")
print("         F_XX vs (F_Y+F_Z) split. => the framework's mu_s/K_F ratio (=> beta) is a FREE function.")
print("    VERDICT (2): ENW EFT leaves the shear/bulk ratio GENUINELY FREE. SO(3)+EOS do NOT pin beta.")

# ================================================================================================
# CANDIDATE (3) -- STABILITY / POSITIVITY / CAUSALITY:  do they carve MORE than 0<beta<2 ?
# ================================================================================================
print("\n" + "="*96)
print("[3] STABILITY / POSITIVITY / CAUSALITY window on beta")
print("="*96)
# framework moduli in K_eff units:  mu_s = 3 beta ,  K_F = 1 - beta/2 ,  P-wave M = K_F + 4 mu_s/3.
# background energy density:  rho_L c^2 = 3(Z a0)^2/(8piG) = 6 Z^2 * K_eff   (since a0^2/8piG = 2 K_eff)
rhoLc2_over_Keff = 6*Z**2
print(f"    Background: rho_L c^2 = 6 Z^2 K_eff = {rhoLc2_over_Keff:.1f} K_eff  (Z^2=32pi/3).")
b = sp.symbols('beta', real=True)
mu_s = 3*b; K_F = 1 - b/2; Mwave_fw = K_F + sp.Rational(4,3)*mu_s
print(f"    mu_s = 3 beta,  K_F = 1 - beta/2,  M(P-wave) = K_F + 4 mu_s/3 = {sp.simplify(Mwave_fw)}  (units K_eff)")
# (a) ghost/gradient: mu_s>0 -> beta>0 ;  K_F>0 -> beta<2
print("    (a) mu_s>0 (no shear ghost)  => beta > 0")
print("    (b) K_F=V''>0 (no bulk ghost/gradient instab) => 1-beta/2>0 => beta < 2   <-- BINDING upper wall")
# (c) subluminal shear:  c_T^2 = mu_s/rho_L = 3 beta K_eff /(6 Z^2 K_eff) = beta/(2 Z^2) <= 1
bmax_cT = 2*Z**2
# (d) subluminal long:  c_L^2 = M/rho_L = (1+11 beta/6)/(6 Z^2) <= 1
bmax_cL = sp.solve(sp.Eq(Mwave_fw/rhoLc2_over_Keff, 1), b)
print(f"    (c) subluminal shear c_T<=c => beta <= 2 Z^2 = {float(bmax_cT):.1f}   (FAR weaker than 2)")
print(f"    (d) subluminal long  c_L<=c => beta <= {float(bmax_cL[0]):.1f}   (FAR weaker than 2)")
# shear-wave speed at beta=2:
cT_at2 = np.sqrt(2/ (2*Z**2))
print(f"    NOTE: the quoted 'v_T<=0.17c refusal' is just the beta=2 endpoint restated:")
print(f"          at beta=2, c_T = sqrt(beta/2Z^2) c = {cT_at2:.3f}c ~ 0.17c. The real wall is K_F>0.")
print("    VERDICT (3): positivity+causality give the OPEN interval 0 < beta < 2. They BOUND, do NOT PIN.")
print("                 Subluminality is slack; the binding walls are mu_s>0 and K_F>0 (the same (0,2)).")

# ================================================================================================
# CANDIDATE (4) -- the "1/6" lemma re-read as an energy partition -> beta = 2/7
# ================================================================================================
print("\n" + "="*96)
print("[4] Does the J2 = J1^2/6 lemma FORCE beta = 2/7 (mu_s=K_F), or is that a coincidence of reading?")
print("="*96)
J1s = sp.symbols('J1', positive=True)
KFs, muss, Keffs = sp.symbols('K_F mu_s K_eff', positive=True)
J2s  = J1s**2/6                          # compatibility lemma (deep radial profile) -- a KINEMATIC identity
Sig  = sp.Rational(1,2)*J2s
u_shear = muss*Sig                       # = mu_s J1^2/12
u_bulk  = sp.Rational(1,2)*KFs*J1s**2
# SUM relation (already uses the 1/6 once):  u_shear+u_bulk = (1/2)K_eff J1^2
sum_rel = sp.simplify(sp.Eq((u_shear+u_bulk)/(sp.Rational(1,2)*J1s**2), Keffs))
print(f"    Deep-energy SUM (uses the lemma ONCE):  K_F + mu_s/6 = K_eff   [{sum_rel}]")
# The '2/7' reading: DEMAND additionally u_shear = (1/6) u_bulk:
ratio = sp.simplify(u_shear/u_bulk)      # = mu_s/(6 K_F)
print(f"    'energy-partition' reading DEMANDS  u_shear/u_bulk = {ratio} = 1/6  => mu_s = K_F.")
beta_27 = sp.Rational(2,7)
print(f"    Solving mu_s=K_F with K_F=K_eff(1-beta/2), mu_s=3beta K_eff:  beta = 2/7 = {float(beta_27):.3f}.")
print("""
    IS THIS A DERIVATION?  NO -- it is DOUBLE-DIPPING the same identity:
      * J2=J1^2/6 is a KINEMATIC invariant-relation of the deep displacement profile (geometry of the
        strain), NOT a dynamical statement about how energy splits between shear and bulk.
      * The '1/6' has ALREADY been consumed once: it is exactly why the shear share is mu_s/6 in the
        SUM relation K_F + mu_s/6 = K_eff.  Re-using J2=J1^2/6 to ALSO set u_shear/u_bulk=1/6 asserts
        mu_s=K_F, i.e. Poisson ratio nu=1/4 -- the textbook 'Poisson solid' default, an ELASTICITY
        ASSUMPTION, not a consequence. The energy partition depends on mu_s and K_F, which the lemma
        does not fix; only their SUM is fixed.
    => beta=2/7 is a COINCIDENCE of the nu=1/4 reading, NOT forced by the written action.""")
for foot in ("canonical","alt"):
    tag,bc = cassini(float(beta_27), foot)
    print(f"    Cassini at beta=2/7=0.286 [{foot:<9}]: vs beta_crit={bc:.3f} -> {tag}")

# ================================================================================================
# VERDICT
# ================================================================================================
print("\n" + "="*96)
print(" ROUTE B VERDICT")
print("="*96)
print(f"""  NO microphysical principle in the WRITTEN action pins the Poisson ratio (the mu_s/K_F split, beta):
    (1) VERLINDE: his emergent elasticity DOES pin a Poisson ratio (nu=+1, lambda=-2mu, VANISHING
        P-wave modulus) -- but that medium is DEGENERATE (negative bulk) and FORBIDDEN by the
        framework's own K_F>0 stability. His only transferable magnitude (mu_s=a0^2/16piG) gives
        beta<=1/3, which double-counts the normalization and still MARGINALLY FAILS canonical.
    (2) ENW solid EFT (eq 2.16): shear ~(F_Y+F_Z), extra bulk ~F_XX are INDEPENDENT Lagrangian data;
        SO(3) fixes only the FORM, and w=-1 is a background statement blind to the shear modulus.
        => the shear/bulk ratio is a GENUINELY FREE function.  beta FREE.
    (3) STABILITY/POSITIVITY/CAUSALITY: carve the OPEN interval 0<beta<2 (K_F>0 & mu_s>0 binding;
        subluminality slack). BOUND, not PIN.
    (4) beta=2/7: the nu=1/4 'Poisson-solid' default, obtained by DOUBLE-DIPPING the J2=J1^2/6 lemma
        (already spent on the SUM relation). A coincidence of one reading, NOT a derivation.

  => beta is a GENUINE FREE MATERIAL PARAMETER of the written action -- the honest final residual.
     Route B PINS nothing; it leaves beta FREE within (0,2).
     Cassini floor beta_crit = {BC_CANON:.3f} (canonical) / {BC_ALT:.3f} (alt), kappa_t=0.5.
     Natural-elasticity closures (nu=1/4 -> beta=2/7=0.286; Verlinde-magnitude -> beta=1/3=0.333)
     cluster JUST BELOW the canonical floor (MARGINAL FAIL x1.05-1.3) and BELOW the alt floor.
     The free window (0,2) STRADDLES beta_crit: a shear-STIFFER-than-natural medium (beta>~{BC_CANON:.2f})
     passes; nothing in the action forces it there. => Cassini door NEITHER shut NOR pinned open.""")
print("EXIT 0")
