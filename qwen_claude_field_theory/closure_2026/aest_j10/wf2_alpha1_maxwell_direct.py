"""
wf2_alpha1_maxwell_direct.py
============================================================================
DIRECT determination of the PPN preferred-frame parameter alpha_1 for AeST
(aether + scalar) at the Maxwell point, via the ONE complete published PPN
derivation of a TeVeS/AeST-class theory: Sagi 2009 (PRD 80, 044032,
arXiv:0905.4001), "Preferred frame parameters in TeVeS and its generalization
[with Einstein-aether type vector action]".

WHY Sagi is the right tool:
  * She computes alpha_1, alpha_2 for TeVeS with a GENERAL Einstein-aether
    vector action (4 couplings K, K+, K2, K4) PLUS the scalar (coupling k,
    cosmological value phi0), reading PPN off the *physical* metric g-tilde.
  * AeST is the single-metric descendant of exactly this class. Its vector
    sector is the Maxwell point of the aether, and its scalar is shift-
    symmetric with matter coupled to the SINGLE metric (g-tilde = g).

MAPPING (Sagi eq. between K's and Einstein-aether c_i, her Sec IV):
        c1 - c3 = 2K ,  c1 + c3 = 2K+ ,  c2 = K2 ,  c4 = -K4
  =>    c1 = K + K+ ,  c3 = K+ - K ,  c2 = K2 ,  c4 = -K4

AeST = MAXWELL POINT of the aether:  c1 = K_B, c3 = -K_B, c2 = 0, c4 = 0
  =>  K = K_B ,  K+ = 0 ,  K2 = 0 ,  K4 = 0 .

Sagi's two alpha_1 formulas:
  (A) PURE-AETHER (scalar fully decoupled, k = phi0 = 0), her eq (49):
        alpha_1 = 4[(K - K+)^2 - K4 (K + K+)] / [2 K K+ - (K + K+)]
      -> we CROSS-CHECK this reproduces Foster-Jacobson exactly, then
         evaluate at the AeST Maxwell point.
  (B) WITH SCALAR (physical=disformal metric g-tilde), her eq (39/46):
        alpha_1 = 8 { G[e^{2phi0} - (1-2K)e^{-2phi0}] sinh(2phi0)
                      - (K+ e^{4phi0} + K) } / [2 K K+ - (K + K+)]  - 1
      -> the ENTIRE scalar (phi0) dependence sits in the factors
         {e^{+-2phi0}, e^{+-4phi0}, sinh(2phi0)} which are EXACTLY the
         coefficients of the DISFORMAL physical-metric map
             g-tilde_ab = e^{-2phi} g_ab - 2 A_a A_b sinh(2phi)   (her eq. for g-tilde)
         and the conformal coordinate rescaling x0->e^{phi0}x0.

THE AeST POINT (the crux of this task):
  AeST matter couples to the SINGLE metric g (Einstein Equivalence Principle;
  S_m[g]); there is NO conformal factor e^{-2phi} and NO disformal A A term.
  Hence g-tilde = g, and the whole family of phi0-carrying terms in (B) is
  ABSENT BY CONSTRUCTION. What survives is the Einstein-frame vector
  contribution = (A) = the pure-aether value. Therefore

        alpha_1(AeST, Maxwell) = alpha_1(pure aether, Maxwell) = -4 K_B .

  The scalar's only residual action on the vector sector is to give the
  transverse aether a mass M^2 = (2-K_B)(1+lambda_s)Q0^2/K_B (verified in the
  companion script) which is cosmological (M <~ Mpc^-1) and negligible at PPN
  scales. It does NOT cancel alpha_1.

INTEGRITY: the pure-aether reduction (A)->Foster-Jacobson is a SOLID sympy
identity. The "scalar enters alpha_1 ONLY via the disformal map, absent in
AeST" step is a STRUCTURAL argument read directly off Sagi's formulas + the
AeST single-metric axiom; labelled accordingly.
"""
import sympy as sp

# ---------------------------------------------------------------------------
# 0. Symbols
# ---------------------------------------------------------------------------
c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4', real=True)
K, Kp, K2, K4  = sp.symbols('K K_plus K2 K4', real=True)     # Sagi's vector couplings
KB             = sp.symbols('K_B', positive=True)
phi0, G        = sp.symbols('phi0 G', real=True)

print("="*74)
print("STEP 1  Foster-Jacobson alpha_1 (pure Einstein-aether), independent form")
print("="*74)
# Foster-Jacobson gr-qc/0509083 (= Oost-Mukohyama-Wang 1802.04303 eq 3.4)
alpha1_FJ = -8*(c3**2 + c1*c4) / (2*c1 - c1**2 + c3**2)
print("alpha_1_FJ(c_i) =", alpha1_FJ)

print("\n" + "="*74)
print("STEP 2  Sagi eq(49) [pure aether] in K-variables -> map to c_i -> == FJ ?")
print("="*74)
# Sagi eq (49):
alpha1_Sagi_pure = 4*((K - Kp)**2 - K4*(K + Kp)) / (2*K*Kp - (K + Kp))
print("alpha_1_Sagi_pure(K,K+,K2,K4) =", alpha1_Sagi_pure)

# mapping c_i <-> K's :  c1=K+K+, c3=K+-K, c2=K2, c4=-K4
map_c_to_K = {c1: K + Kp, c3: Kp - K, c2: K2, c4: -K4}
alpha1_FJ_inK = alpha1_FJ.subs(map_c_to_K)

diff = sp.simplify(alpha1_Sagi_pure - alpha1_FJ_inK)
print("\nsimplify( Sagi_eq49  -  FJ[c_i(K)] ) =", diff)
assert diff == 0, "Sagi eq(49) does NOT match Foster-Jacobson -- transcription error!"
print("  => SOLID: Sagi's pure-aether alpha_1 == Foster-Jacobson (framework validated).")

print("\n" + "="*74)
print("STEP 3  Evaluate the pure-aether alpha_1 at the AeST MAXWELL point")
print("="*74)
# AeST Maxwell point in K-variables:
maxwell_K = {K: KB, Kp: 0, K2: 0, K4: 0}
a1_maxwell = sp.simplify(alpha1_Sagi_pure.subs(maxwell_K))
print("K=K_B, K+=0, K2=0, K4=0  ->  alpha_1 =", a1_maxwell)

# cross-check directly through the c_i / FJ route
maxwell_c = {c1: KB, c3: -KB, c2: 0, c4: 0}
a1_maxwell_FJ = sp.simplify(alpha1_FJ.subs(maxwell_c))
print("via Foster-Jacobson c1=K_B,c3=-K_B,c2=c4=0  ->  alpha_1 =", a1_maxwell_FJ)
assert sp.simplify(a1_maxwell - a1_maxwell_FJ) == 0
print("  => SOLID:  alpha_1(pure aether, Maxwell) = -4 K_B  (two independent routes agree)")

print("\n" + "="*74)
print("STEP 4  WHERE the scalar's handle on alpha_1 lives in TeVeS (eq 39/46)")
print("="*74)
# Sagi eq (39)/(46), the WITH-scalar alpha_1, read off the DISFORMAL physical
# metric g-tilde = e^{-2phi} g - 2 A A sinh(2phi) (her metric def) with the
# conformal potential rescalings  Ubar=e^{-2phi0}U, Vbar=e^{-4phi0}V, ...
e2  = sp.exp(2*phi0);  em2 = sp.exp(-2*phi0)
e4  = sp.exp(4*phi0);  sh2 = sp.sinh(2*phi0)
alpha1_Sagi_scalar = 8*( G*(e2 - (1 - 2*K)*em2)*sh2 - (Kp*e4 + K) ) / (2*K*Kp - (K + Kp)) - 1
print("alpha_1_Sagi_scalar(K,K+,phi0,G) =")
sp.pprint(alpha1_Sagi_scalar)

# HONEST statement: eq(39) is NOT algebraically reducible to eq(49) by killing
# sinh -- the two derivations live in DIFFERENT frames (eq 39 has the disformal
# potential rescalings baked in; the '-1' and overall 8x are disformal-frame
# artefacts).  What IS a clean, true fact: the ENTIRE {phi0, G}-dependence of
# eq(39) is carried by the factors {e^{+-2phi0}, e^{+-4phi0}, sinh(2phi0)},
# which are EXACTLY the coefficients of the disformal map + conformal rescaling.
carriers = alpha1_Sagi_scalar.atoms(sp.exp, sp.sinh)
print("\nphi0/G-carrying factors in eq(39):", carriers)
print("  -> ALL are disformal/conformal-map coefficients (g-tilde = e^{-2phi}g")
print("     - 2 A A sinh 2phi ; x0->e^{phi0}x0).  The scalar reaches alpha_1")
print("     ONLY by deforming the PHYSICAL metric away from the Einstein metric.")

print("\n" + "="*74)
print("STEP 5  The AeST axiom removes exactly this handle")
print("="*74)
print("""  AeST (Skordis-Zlosnik): matter couples to the SINGLE metric g (EEP,
  S_m[g]); the physical metric IS the Einstein metric, g-tilde = g.  There is
  NO conformal factor e^{-2phi} and NO disformal 2 A A sinh(2phi) term.

  Consequence chain (this is the actual AeST argument, NOT a limit of eq 39):
    (i)  alpha_1 is a SPIN-1 / transverse-vector quantity: Sagi eq(49) and
         Foster-Jacobson carry NO c_123 = c1+c2+c3 (the spin-0 combination).
         Verify the scalar-blindness structurally:""")
# alpha_1 has no c2 dependence at all (c2 is the pure spin-0 aether coupling):
print("        d(alpha_1_FJ)/d c2 =", sp.diff(alpha1_FJ, c2), " (c2 absent => spin-0 blind)")
print("""    (ii) AeST's vector (spin-1) sector = the pure-aether Maxwell point
         (the -(K_B/2)F^2 term IS Einstein-aether c1=K_B,c3=-K_B,c2=c4=0);
         the shift-symmetric scalar touches the transverse aether ONLY through
         a mass M^2=(2-K_B)(1+lambda_s)Q0^2/K_B  (companion script), M<~Mpc^-1.
    (iii)physical=Einstein metric => alpha_1 is read straight off the Einstein-
         frame vector result = eq(49) at Maxwell = -4 K_B, with NO disformal
         rescaling and NO scalar entry.
  => alpha_1(AeST) = -4 K_B.  The scalar does NOT cancel it.""")

print("\n" + "="*74)
print("STEP 6  Numbers: the near-kill")
print("="*74)
print(" alpha_1(AeST) = -4 K_B   (SOLID at the Einstein-frame / massless-vector level)\n")
print(f"   {'K_B':>10}   {'alpha_1=-4K_B':>16}")
for kb in [0.25, 0.1, 2.5e-2, 2.5e-5, 2.5e-6]:
    print(f"   {kb:>10.3g}   {-4*kb:>16.3e}")
print("""
 Bounds on alpha_1:
   |alpha_1| < 1e-4     lunar laser ranging (classic; Will 2014)
   |alpha_1| ~ few 1e-5 binary pulsars (Shao-Wex 2012; PSR J2317+1439 in Sagi)
 => |alpha_1| = 4 K_B < 1e-4   forces   K_B < 2.5e-5
    (< 1e-5 pulsar bound        forces   K_B < 2.5e-6)

 AeST phenomenology / stability uses K_B up to O(0.1-0.25) (BBN <~0.25).
 alpha_1 pushes K_B ~4 orders BELOW that natural range -> near-kill of the
 O(0.1) K_B window, INDEPENDENTLY of alpha_2.  And unlike TeVeS, AeST cannot
 buy it back with the scalar: the single-metric axiom removes the disformal
 handle that let Sagi tune TeVeS's alpha_1 to zero.
""")
print("DONE.")
