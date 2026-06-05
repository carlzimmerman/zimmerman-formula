#!/usr/bin/env python3
"""
STEP 4 -- The DECISIVE matching: MOND free energy (R_dS cutoff) vs de Sitter first law.
=======================================================================================
We steelman the route. Three matching prescriptions a closure could use; for each we
solve in sympy for what a0 it forces, and read off the rational prefactor kappa in
a0 = kappa * c * sqrt(G rho_Lambda).  The hard constraint: sqrt(pi) may come ONLY from
sqrt(G rho_Lambda); the leftover rational must be EXACTLY 1/2 for a closure.

de Sitter (Gibbons-Hawking) thermodynamics, exact (restoring c, hbar):
  H_L = c sqrt(Lambda/3)              (de Sitter Hubble)
  R_dS = c/H_L = sqrt(3/Lambda) c     (horizon radius)
  T_dS = hbar H_L / (2 pi)            (GH temperature, /kB)
  S_dS = A/(4 lP^2) = pi R_dS^2 c^3/(G hbar)   (BH entropy, A=4pi R_dS^2)
  rho_Lambda = Lambda c^2/(8 pi G)    (Einstein vacuum density)
"""
import sympy as sp

print("="*78)
print("STEP 4: decisive matching -- does any prescription FORCE kappa=1/2?")
print("="*78)

a0, G, M, Lam, c, hbar, kappa = sp.symbols('a0 G M Lambda c hbar kappa', positive=True)
pi = sp.pi

# de Sitter quantities (exact)
H_L  = c*sp.sqrt(Lam/3)
R_dS = c/H_L
T_dS = hbar*H_L/(2*pi)
S_dS = pi*R_dS**2*c**3/(G*hbar)        # = A/4 lP^2 with A=4pi R_dS^2, lP^2=G hbar/c^3
rho_L = Lam*c**2/(8*pi*G)

print("\nde Sitter quantities (sympy):")
print("  R_dS  =", sp.simplify(R_dS))
print("  T_dS  =", sp.simplify(T_dS))
print("  S_dS  =", sp.simplify(S_dS))
print("  rho_L =", sp.simplify(rho_L))

# The TARGET relation we test for forcing:  a0 = kappa * c * sqrt(G rho_L)
a0_target = kappa*c*sp.sqrt(G*rho_L)
a0_target = sp.simplify(a0_target)
print("\n  TARGET: a0 = kappa c sqrt(G rho_L) =", a0_target)
print("    => with kappa=1/2:  a0 =", sp.simplify(a0_target.subs(kappa, sp.Rational(1,2))))
print("    Z = cH_L/a0 at kappa=1/2:",
      sp.simplify((c*H_L/a0_target.subs(kappa, sp.Rational(1,2)))),
      " (should be sqrt(32pi/3) =", float(sp.sqrt(32*pi/3)), ")")
Zhalf = sp.simplify(c*H_L/a0_target.subs(kappa, sp.Rational(1,2)))
print("    Z numerically:", float(Zhalf))

# ---------------------------------------------------------------------------
# MOND on-shell action (from Step 3), restore c:  L has dims energy/volume.
# I_phi = -(1/3) M sqrt(G M a0) log(R_dS/r_in)   [c=1].  We keep the IR (R_dS) piece.
# Its DERIVATIVE wrt the horizon (the 'first law' lever) is what a closure would match.
# ---------------------------------------------------------------------------
r_in = sp.symbols('r_in', positive=True)
I_phi = -sp.Rational(1,3)*M*sp.sqrt(G*M*a0)*sp.log(R_dS/r_in)
print("\nMOND on-shell free energy (IR piece):")
print("  I_phi =", I_phi)

print("""
================================================================================
PRESCRIPTION A -- 'energy-balance': set |I_phi| (the MOND vertex free energy) equal
to the de Sitter heat T_dS S_dS that the SAME horizon carries.  (Verlinde-style:
the MOND elastic energy = the displaced dark-energy entropy's free energy.)
================================================================================""")
# T_dS * S_dS (the horizon's own free energy scale)
TS = sp.simplify(T_dS*S_dS)
print("  T_dS * S_dS =", TS, "  (the horizon free-energy scale)")
# Solve |I_phi| = T_dS S_dS for a0 -- but I_phi ~ M^{3/2}, TS independent of M:
# this can only hold at ONE special M. Solve for that M, then see if a0 drops out.
solA = sp.solve(sp.Eq(-I_phi, TS), a0)
print("  Solve -I_phi = T_dS S_dS for a0:")
for s in solA:
    print("    a0 =", sp.simplify(s))
print("  => a0 depends on M and log(R_dS/r_in): NOT a pure horizon relation.")
print("     The M-dependence (M^{-3} from inverting M^{3/2}=const) is fatal: a0 is")
print("     not fixed to c sqrt(G rho_L) at all. Prescription A does NOT close.")

print("""
================================================================================
PRESCRIPTION B -- 'differential first law': delta Q = T_dS delta S_dS for adding
mass M to the horizon, with delta Q identified as the MOND free energy I_phi.
This is the route's literal claim: the mass's MOND vertex IS the heat that changes
the horizon entropy.
================================================================================""")
# de Sitter first law: adding energy E=Mc^2 changes the horizon.
# Standard GH first law (Spradlin-Strominger-Volovich, Cai-Kim):  dE = -T_dS dS_dS
# for the OBSERVER's static patch (the famous minus sign), or |dE| = T |dS|.
# delta S from adding mass M: use S_dS(Lam) and that mass shifts effective Lambda? No --
# cleaner: the horizon FIRST LAW for a Schwarzschild-de Sitter mass M (small M):
#   T_dS delta S_horizon = -delta M c^2   (Gibbons-Hawking: mass DECREASES horizon area)
# So the heat scale per unit mass is just c^2 (times O(1)). Let's be exact:
Mc2 = M*c**2
print("  de Sitter first law (small mass M in static patch): |delta Q| = M c^2")
print("    (T_dS delta S_dS = M c^2 to leading order -- this is just E=Mc^2).")
# Now set the MOND free energy = M c^2 and solve for a0:
solB = sp.solve(sp.Eq(-I_phi, Mc2), a0)
print("  Set -I_phi = M c^2, solve for a0:")
for s in solB:
    print("    a0 =", sp.simplify(s))
print("""  => a0 ~ c^4/(G M log^2) : DEPENDS ON M (the test mass!) and on log(R_dS/r_in).
     A universal constant a0 cannot equal something that scales as 1/M. The MOND
     free energy being M^{3/2} while the heat is M^1 forces a0 ~ M^{-1}. FATAL.
     Prescription B does NOT close -- and tells us WHY: the cubic vertex's M^{3/2}
     vs the first law's M^1 is a structural power mismatch, not a tunable constant.""")

print("""
================================================================================
PRESCRIPTION C -- 'horizon self-energy / dimensional': the ONLY way to kill the M
and log dependence is to evaluate the MOND free energy AT the horizon's own
self-gravitating mass M = M_dS and identify the log as O(1).  Does THAT force kappa?
================================================================================""")
# The de Sitter horizon's own mass (Schwarzschild radius = R_dS): M_dS = R_dS c^2/(2G)
M_dS = R_dS*c**2/(2*G)
print("  Horizon mass M_dS = R_dS c^2/2G =", sp.simplify(M_dS))
# Evaluate I_phi at M = M_dS, set log -> 1 (O(1)), and demand -I_phi = M_dS c^2:
I_at = -sp.Rational(1,3)*M_dS*sp.sqrt(G*M_dS*a0)   # log set to 1
print("  I_phi(M_dS, log=1) =", sp.simplify(I_at))
solC = sp.solve(sp.Eq(-I_at, M_dS*c**2), a0)
print("  Set -I_phi(M_dS) = M_dS c^2, solve for a0:")
for s in solC:
    s = sp.simplify(s)
    print("    a0 =", s)
    # express as kappa * c sqrt(G rho_L) and extract kappa
    kap = sp.simplify(s / (c*sp.sqrt(G*rho_L)))
    print("      => a0 / (c sqrt(G rho_L)) = kappa =", sp.nsimplify(sp.simplify(kap)),
          "=", float(kap))
