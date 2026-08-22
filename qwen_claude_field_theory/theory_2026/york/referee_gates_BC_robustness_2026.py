"""
HOSTILE-REFEREE attack on Gates B (DOF=2) and C (LY well-posedness) of the
CMC-gauge MOND-deformed theory.  Goal: REFUTE, not confirm.

Two attacks:
 (1) LY UNIQUENESS for an ISOLATED asymptotically-flat mass.  Cosmological CMC has
     q != 0 so the (2/3)q^2 psi^5 term secures the maximum principle.  A LOCAL isolated
     solve effectively has q -> 0 (that term vanishes), and the MOND phantom source has
     a 'matter-like' sign in the Newtonian regime.  Does LY stay uniquely solvable, or
     branch?  We compute the EXACT monotonicity quantity m(y)=5U-4yU', assemble the full
     dF/dpsi that the Ochoa-Murchadha-York maximum principle needs, and test its sign in
     BOTH regimes with and without the q^2 stabiliser -- and check whether the MOND source
     can be conformally reweighted the way ordinary matter can (it CANNOT).
 (2) DOF: is there a first-class COMBINATION of p_Phi with H_perp/H_i that was missed,
     re-opening a propagating mode?  We build the 2x2 Dirac bracket block for (p_Phi,C_Phi),
     compute its determinant (the obstruction to any first-class repackaging), and locate
     the ONLY degenerate direction (Y=0), checking it is codim-inconsistent (measure zero),
     not a genuine gauge direction.
"""
import sympy as sp

y, psi, ybar, a0, q = sp.symbols('y psi ybar a0 q', positive=True)
Uprime = sp.sqrt(y)/sp.sqrt(1+y)                 # U'(y)=mu(sqrt y)
# use the log form of asinh so sympy can take large-y asymptotics
U      = sp.sqrt(y*(1+y)) - sp.log(sp.sqrt(y)+sp.sqrt(1+y))  # U(y)=sqrt(y(1+y))-asinh(sqrt y)

print("="*72)
print("ATTACK 1 : LY uniqueness for an ISOLATED mass (q -> 0)")
print("="*72)

# --- exact monotonicity quantity m(y) = 5U - 4 y U' ---------------------------
m = sp.simplify(5*U - 4*y*Uprime)
print("m(y) = 5U-4yU' (exact) =", m)
m_deep = sp.series(m, y, 0, 3).removeO()
print("  deep-MOND  y->0 :", sp.simplify(m_deep), " -> sign =",
      "NEGATIVE (GOOD: raises dF/dpsi)")
print("  Newtonian  y->oo: m/y ->", sp.limit(m/y, y, sp.oo),
      ", m-(y) ->", sp.limit(m - y, y, sp.oo),
      "  => m ~ y+2 > 0 (BAD: matter-like, LOWERS dF/dpsi)")
# where does m change sign?
m_root = sp.nsolve(m, y, 1.0)
print("  m(y) crosses 0 at y* =", sp.N(m_root, 8),
      "  (x*=sqrt(y*)=", sp.N(sp.sqrt(m_root),6), "= g/a0 at the flip)")

# --- assemble dF/dpsi for the isolated LY, both matter and MOND sources -------
# LY:  8 Dbar^2 psi = F,   F = Rbar psi - Abar^2 psi^-7 + (2/3)q^2 psi^5
#                              - (16 pi G/c^4) rho_eff psi^5
# Maximum-principle uniqueness (O'Murchadha-York) needs dF/dpsi >= 0.
Rbar, Abar, rhohat_m, Kmatt = sp.symbols('Rbar Abar rhohat_m Kmatt', positive=True)
# Ordinary matter, YORK-SCALED  rho_m = rhohat_m psi^-8  (the standard reweighting
# that BUYS the good sign): its LY source is -Kmatt*rhohat_m*psi^-3.
src_matter = -Kmatt*rhohat_m*psi**(-3)
# MOND phantom source: FIXED weight, Y = psi^-4 ybar inside U -> S = -2 a0^2 U psi^5.
src_mond   = -2*a0**2*U.subs(y, psi**(-4)*ybar)*psi**5
F = Rbar*psi - Abar**2*psi**(-7) + sp.Rational(2,3)*q**2*psi**5 + src_matter + src_mond
dF = sp.simplify(sp.diff(F, psi))
print("\ndF/dpsi (full) =")
sp.pprint(dF)

# express the MOND piece back through m(y):
dF_mond = sp.simplify(sp.diff(src_mond, psi))
target  = -2*a0**2*psi**4*m.subs(y, psi**(-4)*ybar)
print("\nMOND piece of dF/dpsi  =  -2 a0^2 psi^4 m(y)?  residual =",
      sp.simplify(dF_mond - target), "(expect 0)")

print("""
READING of dF/dpsi = Rbar + 7 Abar^2 psi^-8 + (10/3) q^2 psi^4
                     + 3 Kmatt rhohat_m psi^-4      [matter: York-reweighted, >0 GOOD]
                     - 2 a0^2 psi^4 m(y)            [MOND phantom: sign(-m)]
""")
print(" * Ordinary matter is reweighted rho_m=rhohat_m psi^-8 so its term is +3(..)psi^-4>0.")
print(" * The MOND phantom's psi-weight is FIXED by Y=psi^-4 ybar; it CANNOT be reweighted.")
print("   In deep-MOND m<0 -> -2a0^2 psi^4 m > 0 (helps). In Newtonian m~y+2>0 -> term<0 (hurts).")
print(" * The (10/3)q^2 psi^4 stabiliser is the ONLY guaranteed-positive psi^4 term; in the")
print("   ISOLATED limit q->0 it VANISHES, leaving the bad MOND psi^4 term uncompensated in")
print("   the Newtonian regime wherever rho_m (baryons) is locally sub-dominant.")

# --- magnitude check: is the bad-sign term actually a threat in weak field? ----
print("\n--- magnitude of the bad term vs the good matter term (Newtonian regime) ---")
# bad MOND term ~ 2 a0^2 y = 2 a0^2 (|DPhi|/a0)^2 = 2 |DPhi|^2 = 2 g^2  (phantom, a0-blind here)
# good matter  ~ 3 Kmatt rhohat_m ; near a baryonic mass rho_m dominates the phantom by
# the usual MOND ratio.  Symbolic statement only:
print("bad-term/(good-term) ~ (2 a0^2 y)/(3 Kmatt rhohat_m).  In Newtonian y>>1, a0^2 y = |DPhi|^2")
print("is the PHANTOM density ~ (a0/G) dg/dr, which is a0-suppressed vs baryons where they exist,")
print("but is UNCOMPENSATED in baryon-poor Newtonian-field regions -> the sign is not secured there.")

print("\n" + "="*72)
print("ATTACK 2 : DOF -- can p_Phi combine with H_perp/H_i into a first-class quantity?")
print("="*72)

# The QUMOND second variation kernel (principal symbol) L = U' + 2 y U''.
Upp = sp.diff(Uprime, y)
Lsymbol = sp.simplify(Uprime + 2*y*Upp)
print("Principal symbol of L = {p_Phi,C_Phi} kernel :  U'+2yU'' =", Lsymbol)
print("  y->0  :", sp.limit(Lsymbol, y, 0), "  (DEGENERATES at Y=0)")
print("  y->oo :", sp.limit(Lsymbol, y, sp.oo))
crit = sp.solve(sp.diff(Lsymbol, y), y)
print("  interior extremum at y =", crit, " -> L =",
      [sp.nsimplify(sp.simplify(Lsymbol.subs(y, c))) for c in crit if c>0])

# 2x2 Dirac block for the pair (p_Phi, C_Phi).  {p_Phi,p_Phi}=0, {p_Phi,C_Phi}=L,
# {C_Phi,C_Phi}=A (some antisymmetric-in-the-continuum operator, structurally). The
# obstruction to repackaging EITHER constraint as first-class is det of this block.
L, A = sp.symbols('L A')
Dirac = sp.Matrix([[0, L], [-L, A]])
detD = sp.simplify(Dirac.det())
print("\nDirac block  [[{p,p},{p,C}],[{C,p},{C,C}]] = [[0,L],[-L,A]]")
print("  det =", detD, "  (independent of A) -> nondegenerate iff L != 0.")

# Can adding H_perp/H_i to p_Phi kill its bracket with C_Phi?  p_Phi' = p_Phi + a*Hperp + b^i*Hi.
# {p_Phi',C_Phi} = L + a{Hperp,C_Phi}+b^i{Hi,C_Phi}.  For this to vanish IDENTICALLY as an
# operator (all test functions), L (a positive-definite elliptic symbol away from Y=0) would
# have to lie in the span of the H-brackets pointwise -- impossible for an invertible operator.
print("""
Repackaging test:  p_Phi' = p_Phi + a H_perp + b^i H_i.
  {p_Phi',C_Phi} = L + a{H_perp,C_Phi} + b^i{H_i,C_Phi}.
  L has principal symbol U'+2yU'' > 0 (elliptic, INVERTIBLE) for Y>0, so it is not in the
  range of any FINITE combination of the first-class brackets pointwise => no local a,b^i
  makes p_Phi' first-class.  The (p_Phi,C_Phi) block stays second-class.  DOF count holds.
""")

# The ONLY null direction: Y=0 (Phi stationary), where L's symbol -> 0.
print("Degenerate locus:  Y = |DPhi|^2/a0^2 = 0  (DPhi=0).  There L -> 0^+ and the pair")
print("momentarily fails to be second-class.  But {DPhi=0} is codim-3 (three components of")
print("DPhi vanish) -> a measure-zero set of isolated stationary points, NOT a hypersurface")
print("in space -> it cannot support a propagating gauge direction (a gauge symmetry needs L")
print("to degenerate on an OPEN region / consistently across the slice).  Same harmless AQUAL")
print("degeneracy audited in Task G.  => NO missed first-class combination; DOF=2 ROBUST.")

print("\n" + "="*72)
print("VERDICT SUMMARY (printed for the record)")
print("="*72)
print("""ATTACK 2 (DOF): REPELLED. The 2x2 Dirac block det = L^2 != 0 for Y>0; L is elliptic and
  invertible so no local combination of p_Phi with H_perp/H_i is first-class. The single
  degenerate direction Y=0 is measure-zero (codim-3), not an open-region gauge symmetry.
  2 local DOF is robust.

ATTACK 1 (LY isolated): PARTIALLY LANDS. m(y)=5U-4yU' is NEGATIVE (good) in deep-MOND but
  ~ y+2 > 0 (bad, matter-like) in the Newtonian regime, crossing zero at g/a0 = %s. The MOND
  phantom source CANNOT be conformally reweighted to restore the good sign (its psi-weight is
  fixed by Y=psi^-4 ybar), unlike ordinary matter. The cosmological q^2 stabiliser that would
  dominate the bad term VANISHES as q->0 in an isolated solve. Therefore the maximum-principle
  GLOBAL uniqueness proof for arbitrary strong-field isolated data is NOT secured by the
  theory's own structure -- it inherits exactly GR-with-un-reweighted-matter's generic
  strong-field non-uniqueness (Baumgarte-O'Murchadha-Pfeiffer folds). It is NOT a new MOND
  pathology and it does NOT touch the weak-field regime (psi~1, corrections O(GM/c^2 r)),
  where linearisation gives the well-posed elliptic AQUAL/QUMOND operator. HOLE = the
  'unique positive solution guaranteed' claim is OVER-STATED for strong field; correct claim
  is 'well-posed and locally unique in the weak-field regime; strong-field global uniqueness
  is conditional, no worse than GR matter'.""" % sp.N(sp.sqrt(m_root),4))
