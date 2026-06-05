#!/usr/bin/env python3
r"""
RED-TEAM the strained-horizon null:  try HARD to break the three obstructions and FORCE kappa=1/2.
HONESTY MANDATE: the expected outcome is the freedom persists; we attempt to falsify that.

Obstruction we attack:  on-shell, the deep-MOND canonical momentum Theta^r = 2 L'(Y) grad phi
collapses to -M/(4 pi r^2) (a0 CANCELS).  We test:
  (A) Is the a0-cancellation an artifact of the exponent 3/2?  Scan f(x)~x^p; only p=3/2 is deep-MOND.
  (B) Does a C(Q) prefactor (the FULL AeST vertex, not bare AQUAL) restore a0-sensitivity?
  (C) Can the SECOND-order (strain) piece -- the O(eps^3) free energy itself, not its momentum --
      carry a0 in a way the first law can use, with a sqrt(pi) and a clean 1/2?
  (D) Brute force: is there ANY assignment that yields kappa=1/2 with sqrt(pi) from sqrt(Lambda)
      and a forced rational 1/2 -- or does every closure attempt insert the answer?
"""
import sympy as sp

G, M, a0, r, R, Lam, c, hbar, p = sp.symbols('G M a0 r R Lambda c hbar p', positive=True)

print("="*100)
print(" (A)  Is the a0-cancellation special to p=3/2, or generic?  Scan L = -Y^p / (norm).")
print("="*100)
# General MOND-like Lagrangian L = -k_p Y^p / (G a0^{2p-2}) so that units work and a0 is the scale.
# Deep-MOND requires the field eq  div(|grad phi|^{2p-2} grad phi /a0^{2p-2}) = 4 pi G rho.
# For a point mass: |grad phi|^{2p-2} grad phi = G M a0^{2p-2}/r^2  => grad phi = (G M)^{1/(2p-1)} a0^{...}/r^{2/(2p-1)}.
# The DEEP-MOND (flat rotation curve) case is p=3/2 EXACTLY (gives grad phi ~ 1/r).  Show momentum's a0:
print("  Field eq exponent:  |grad phi|^(2p-2) grad phi ~ G M a0^(2p-2)/r^2.")
# canonical momentum density Theta^r = dL/d(grad phi) = -2 p k_p Y^{p-1} grad phi / (G a0^{2p-2}); on-shell:
# solve grad phi from field eq:
gp = sp.symbols('gp', positive=True)   # = |grad phi|
field_eq = sp.Eq(gp**(2*p-2)*gp, G*M*a0**(2*p-2)/r**2)   # = G M a0^{2p-2}/r^2  (Gauss law, modified)
gp_sol = sp.solve(field_eq, gp)
print(f"  grad phi on-shell solutions: {gp_sol}")
gp_os = gp_sol[0]
# momentum ~ Y^{p-1} grad phi / a0^{2p-2} = gp^{2p-1}/a0^{2p-2}; substitute:
mom = sp.simplify(gp_os**(2*p-1)/a0**(2*p-2))
print(f"  canonical momentum ~ grad phi^(2p-1)/a0^(2p-2) on-shell = {sp.simplify(mom)}")
print(f"     -> a0-dependence:  exponent of a0 = {sp.simplify(sp.log(mom)/sp.log(a0)).subs([(G,1),(M,1),(r,1)])}")
# evaluate a0-power as function of p:
a0_power = sp.simplify(sp.diff(sp.log(mom), a0)*a0)   # logarithmic derivative = power of a0
print(f"     a0-power(p) = {sp.simplify(a0_power)}")
print(f"     at p=3/2:  a0-power = {sp.simplify(a0_power.subs(p, sp.Rational(3,2)))}  (=0 => a0 cancels!)")
print("""
   RESULT:  the modified Gauss law forces grad phi ~ (GM a0^{2p-2})^{1/(2p-1)}/r^{2/(2p-1)}, and the
   canonical momentum becomes  ~ G M / r^2  with a0-power = 0  FOR ALL p (the Gauss law is, by
   construction, the statement that the momentum flux = G M, a0-free).  The a0-cancellation is NOT
   a 3/2 accident -- it is the modified Gauss law itself:  the horizon sees only the ENCLOSED MASS,
   never the coupling a0.  This is why NO horizon-flux/entropy argument can see a0.  (Gauss's theorem.)
""")

print("="*100)
print(" (B)  Does the full AeST C(Q) prefactor (not bare AQUAL) restore a0-sensitivity on-shell?")
print("="*100)
Q, KB = sp.symbols('Q K_B', real=True)
C = sp.Function('C')
# AeST vertex C(Q) Y^{3/2}.  On a STATIC background the aether A^mu is unit timelike, Q = A.grad phi.
# For a static field grad phi is spatial, A is timelike => Q = A^mu grad_mu phi = A^t grad_t phi = 0
# (static: grad_t phi = 0).  So Q=0 on static configs => C(Q)->C(0)=const, a pure number absorbed into a0.
print("  On a STATIC configuration grad_t phi = 0 and the aether is timelike (A^i=0), so")
print("  Q = A^mu grad_mu phi = A^t grad_t phi = 0.  => C(Q) -> C(0) = const, reabsorbed into a0.")
print("  The C(Q) prefactor adds NOTHING new for the static point-mass strain (Q=0).  Same a0-blindness.")
print("  (Only TIME-DEPENDENT / cosmological configs have Q!=0 -- and those are the homogeneous saddle,")
print("   where Ybar=0 instead.  Either Y=0 (cosmo) or Q=0 (static): the vertex never sees a0 on-shell.)\n")

print("="*100)
print(" (C)  Can the O(eps^3) free energy ITSELF (carrying a0^{3/2}) feed a first law that gives 1/2?")
print("="*100)
# The free energy I = -(1/(3 G a0))(G M a0)^{3/2} log(R/r_t) DOES carry a0^{3/2}.  For it to fix a0 we need
# an INDEPENDENT equation of the form  I = (something a0-free).  The only candidate is the horizon
# 'heat' T*S.  But:  (i) M-power mismatch (3/2 vs 1), shown already; (ii) even matching the COEFFICIENT
# requires picking the mass M.  Try the 'natural' closure: set the log to O(1) and M = horizon mass,
# and see what a0 the COEFFICIENT match gives -- does sqrt(pi) and 1/2 appear?
# Natural horizon mass M_H ~ c^2/(2G) * R_dS (the mass whose Schwarzschild radius = R_dS):
R_dS = sp.sqrt(3/Lam)               # (c=1)
M_H  = R_dS/(2*G)                   # Schwarzschild mass of the horizon (c=1): 2GM=R => M=R/2G
# de Sitter free energy (the thing to match): F_dS = -T S = -(hbar/2pi R_dS)(pi R_dS^2/(hbar G)) = -R_dS/(2G).
F_dS = -R_dS/(2*G)
print(f"  de Sitter free energy F_dS = -T_dS S_dS = {sp.simplify(F_dS)}  (= -M_H, the horizon mass; c=1)")
# MOND free energy with M=M_H, log~1.  CORRECT on-shell action (sibling PART A'):
#   I = -(1/(3 G a0)) (G M a0)^{3/2} log(R/r_t)  -- the 1/(G a0) prefactor was previously DROPPED.
I_mond = -(G*M_H*a0)**sp.Rational(3,2)/(3*G*a0)   # *log ~ 1; simplifies to -(1/3) sqrt(G) M_H^{3/2} sqrt(a0)
print(f"  MOND free energy (M=M_H, log~1)  I = -(1/(3 G a0))(G M_H a0)^(3/2) = {sp.simplify(I_mond)}")
# 'closure' attempt: set I_mond = F_dS and solve for a0:
sol_a0 = sp.solve(sp.Eq(I_mond, F_dS), a0)
print(f"  set I_mond = F_dS, solve a0:  {sol_a0}")
for s in sol_a0:
    s = sp.simplify(s)
    print(f"     a0 = {s}")
    # target a0 = c^2 sqrt(Lam/(32 pi)) = sqrt(Lam/(32pi)) (c=1):  a0 ~ Lambda^{1/2}.
    Lam_power_forced = sp.simplify(sp.diff(sp.log(s), Lam)*Lam)   # power of Lambda in the forced a0
    print(f"        Lambda-power of forced a0 = {Lam_power_forced}   (TARGET a0~sqrt(Lam) needs power 1/2)")
    G_power_forced   = sp.simplify(sp.diff(sp.log(s), G)*G)
    print(f"        G-power of forced a0      = {G_power_forced}   (a0=c^2 sqrt(Lam/32pi) has G-power 0!)")
    print(f"        contains pi?  {'pi' in str(s)}   (target needs sqrt(pi); this has none)")
    # extract the pure coefficient of sqrt(Lambda) and compare to the target 1/sqrt(32 pi) (c=1):
    coeff_forced = sp.simplify(s/sp.sqrt(Lam))
    coeff_target = sp.simplify(1/sp.sqrt(32*sp.pi))
    ratio        = sp.simplify(coeff_forced/coeff_target)
    print(f"        forced coeff of sqrt(Lam) = {coeff_forced} ~ {float(coeff_forced):.4f}"
          f"   (it is 6 sqrt(3); the free-fall target is 1/2 -- NOT matched)")
    print(f"        target coeff 1/sqrt(32pi) = {coeff_target} ~ {float(coeff_target):.4f}"
          f"   (forced/target = {ratio} ~ {float(ratio):.1f}x off, and pi-less)")
print("""
   RESULT:  forcing I_mond = F_dS by hand yields a0 = 6 sqrt(3) sqrt(Lambda) -- the RIGHT FORM:
   Lambda-power 1/2 and G-power 0, i.e. it IS of the form c sqrt(G rho_Lam) ~ c^2 sqrt(Lambda).
   So the single-M closure DOES reproduce the correct a0 ~ sqrt(Lambda) scaling (the earlier
   'wrong Lambda-power 1/6' claim was an ARTIFACT of a dropped 1/(G a0) prefactor -- now fixed).
   BUT the forced rational is 6 sqrt(3) ~ 10.39, NOT the free-fall 1/2 -- and it carries NO pi,
   while the target a0 = c^2 sqrt(Lam/32pi) needs 1/sqrt(32pi) ~ 0.0997 (off by factor ~104).
   And we still had to INSERT M = M_H and log ~ 1 by hand.  So: right FORM, but a DIFFERENT,
   pi-less number set by the cubic and the chosen M -- inserted M and no sqrt(pi), so nothing
   forces kappa = 1/2.  Still not a closure.
""")

print("="*100)
print(" (D)  Where could sqrt(pi) come from, and is the rational ever forced to 1/2?")
print("="*100)
print("""  HARD CONSTRAINT (proven elsewhere): sqrt(32pi/3) not in Q(pi); the irreducible sqrt(pi) can ONLY
   come from sqrt(G rho_Lam) ~ sqrt(Lambda/8pi)... wait, rho_Lam = Lam c^2/(8 pi G) => sqrt(G rho_Lam) =
   c sqrt(Lam/8pi), which carries 1/sqrt(8pi) -- a sqrt(pi) in the DENOMINATOR.  a0 = (c/2) sqrt(G rho_Lam)
   then = (c^2/2) sqrt(Lam/8pi) = c^2 sqrt(Lam/32pi).  So the sqrt(pi) enters via rho_Lam's 8 pi G (the
   Einstein coupling), and the rational 1/2 is the free-fall kappa.""")
rho_Lam = Lam*c**2/(8*sp.pi*G)
a0_target = (c/2)*sp.sqrt(G*rho_Lam)
print(f"  a0 = (c/2) sqrt(G rho_Lam) = {sp.simplify(a0_target)}  (c kept)")
print(f"     = c^2 sqrt(Lam/32pi)? -> {sp.simplify(a0_target - c**2*sp.sqrt(Lam/(32*sp.pi)))==0}")
print("""
   The strained-horizon free energy produces a0 ~ sqrt(Lambda) (FORM forced) but:
     * its prefactor is a pure rational from the cubic (-1/3) and the chosen M -- NEVER pinned to 1/2;
     * it carries NO independent sqrt(pi) (the area's 4pi cancels L's 1/12pi);
   so the sqrt(pi) MUST still be imported from rho_Lam's Einstein 8piG (exactly as the homogeneous
   route), and the leftover rational is set by the free-fall convention kappa=1/2 -- a POSIT, not forced.
""")

print("#"*100)
print("# RED-TEAM VERDICT:  all three obstructions survive every attack.")
print("#  (A) a0-cancellation in the horizon momentum is GAUSS'S LAW (true for all p) -- horizon sees")
print("#      only enclosed mass, never the coupling a0.  Unbreakable.")
print("#  (B) C(Q) prefactor: Q=0 on static strains (and Y=0 on cosmo) -- vertex never sees a0 on-shell.")
print("#  (C) Matching the O(eps^3) free energy to F_dS gives the RIGHT FORM a0~sqrt(Lam) (Lam-power 1/2,")
print("#      G-power 0) but a pi-less rational 6sqrt3 ~ 10.4 (NOT 1/2), only after INSERTING M=M_H and")
print("#      log~1, and with NO sqrt(pi).  Right form, wrong (pi-less) number -- inserted, not forced.")
print("#  (D) sqrt(pi) must still come from rho_Lam (Einstein 8piG); the rational stays free (kappa=1/2")
print("#      is the free-fall posit, NOT forced to 1/2 by anything here).")
print("#  ==> FREEDOM PERSISTS.  kappa NOT forced.  The off-saddle route fails for the SAME structural")
print("#      reason as the on-saddle one, now made on-shell-explicit: the modified Gauss law makes the")
print("#      horizon a0-blind.")
print("#"*100)
