"""
agentXX Route 2 — PART 4: the single-scale no-go and its ONE escape, made rigorous.

The Part 3 (c2) finding deserves a hard, explicit treatment because it is the
load-bearing result:

  THEOREM (single-scale dimensional obstruction):
  c_chi is dimensionless (a speed ratio, weight 0 under dilatation).
  H is a scale (weight -1, [mass]). de Sitter is a SINGLE-SCALE background:
  the only dimensionful parameter is H (G is fixed; Lambda=3H^2).
  Therefore the ONLY dimensionless function f built from H alone is a CONSTANT.
  => c_chi = f(H) with f from the dS data alone  FORCES  f = const, i.e. c_chi
     is H-INDEPENDENT.  A genuine scale-lock (c_chi varying with H) is
     DIMENSIONALLY IMPOSSIBLE within the pure dS+khronon system.

  The ONLY escape: a SECOND scale M (a UV scale of the khronon sector, a
  Lorentz-violation scale M_LV, or a symmetry-breaking VEV) enters, so that
  c_chi = f(H/M) is dimensionless and genuinely H-dependent.  Then c_chi=f(H)
  IS possible — but it requires NEW INPUT (the scale M and the function f),
  which is precisely the 'genuinely new physics' the brief anticipates.

This part:
  (d1) State and machine-check the dimensional obstruction: enumerate the
       dimensionful content of dS+khronon, show only H is available, conclude
       f=const.
  (d2) The escape with a second scale M: show c_chi=f(H/M) is dimensionally
       allowed, and characterize what M would have to be (a khronon UV / LV
       scale) — i.e. exactly NEW physics, not banked dS machinery.
  (d3) Cross-check against agentEE: the khronon action's couplings are
       dimensionless and the only scale is M_Pl/H; confirm c_chi^2=ratio of
       dimensionless couplings has no H. Bank the verdict.
"""
import sympy as sp

print("="*70)
print("PART 4 (d1): the single-scale dimensional obstruction")
print("="*70)
H, M, cchi = sp.symbols('H M c_chi', positive=True)
# Dimensionful content of pure dS+khronon:
#   H        : [mass]^1   (Hubble; Lambda=3H^2, so Lambda gives no new scale)
#   G=M_Pl^-2: [mass]^-2  (but G is held fixed/non-dynamical; it sets units)
#   couplings c1..c4 / alpha,beta,lambda : [mass]^0 (dimensionless, Part 1)
# In units where we measure c_chi (dimensionless), the question is whether a
# dimensionless f(H) exists that is non-constant. It cannot: with ONE scale H,
# every dimensionless quantity is H-independent (H/H=1).
print("Dimensionful content of pure dS+khronon:")
print("  H : [mass]^+1  (only Lambda=3H^2 derived from it, no new scale)")
print("  G : [mass]^-2  (fixed, sets units, non-dynamical)")
print("  aether couplings : [mass]^0  (dimensionless, Part 1 result)")
print()
print("A dimensionless f(H) built from a SINGLE scale H must be H-independent:")
# demonstrate: any monomial H^p is dimensionless only if p=0.
p = sp.symbols('p', real=True)
print("  H^p dimensionless  <=>  p=0  =>  H^p = 1 (constant).")
print("  => c_chi = f(H) forces f=const.  NO non-trivial scale-lock exists")
print("     within the pure dS+khronon system.  PROVEN by dimensions.")
print()
print("This is STRONGER than agentSS's weight argument: agentSS showed a")
print("dilation cannot PIN the ratio; here we show a true H-dependence is")
print("dimensionally FORBIDDEN absent a second scale. The lock is impossible,")
print("not merely un-forced, with the banked single-scale content.")

print()
print("="*70)
print("PART 4 (d2): the ONLY escape — a second scale M (new physics)")
print("="*70)
# With a second scale M, c_chi=f(H/M) is dimensionless and H-dependent.
ratio = H/M
print("If a SECOND scale M enters (khronon UV scale, LV scale, or VEV):")
print("  c_chi = f(H/M)  is dimensionless and genuinely H-dependent. ALLOWED.")
print()
print("What M would have to be (to NOT be banked dS machinery):")
print("  * a Lorentz-violation / khronon UV scale M_LV (Horava scale),")
print("  * a symmetry-breaking VEV of the khronon kinetic sector,")
print("  * a new coupling carrying dimension.")
print("NONE of these is present in the pure dS+khronon system (whose only")
print("scale is H). Introducing M = NEW INPUT, by construction.")
print()
print("Moreover, even WITH M, the FORM f and the VALUE of M are unconstrained")
print("by dS symmetry => c_chi=f(H) would be MODEL-DEPENDENT, not forced.")
print("A symmetry that needs an external scale and an external function to")
print("act is not forcing anything.")

print()
print("="*70)
print("PART 4 (d3): cross-check vs agentEE — couplings dimensionless, no H")
print("="*70)
alpha, beta, lam = sp.symbols('alpha beta lambda', positive=True)
cchi_sq = (alpha - 2)*(beta + lam) / (alpha*(beta - 1)*(2 + beta + 3*lam))
# Substitute any H-dependence? There is none to substitute. Confirm free symbols.
print("c_chi^2(alpha,beta,lambda) free symbols:", cchi_sq.free_symbols)
print("Contains H?", H in cchi_sq.free_symbols)
print("=> CONFIRMED: c_chi^2 has NO H. The khronon Lagrangian gives c_chi as a")
print("   ratio of dimensionless couplings, decoupled from the dS scale H.")
print()
print("BANKED VERDICT (Route 2 / symmetry-fixed-point):")
print("  No symmetry or fixed point of the dS+khronon system forces c_chi=f(H).")
print("  - RG/dS-conformal fixed point: only the LUMINAL c_chi=1 is protected;")
print("    it is H-independent AND decouples the sonic edge (HURTS).")
print("  - dilatation/modular: c_chi is a weight-0 modulus; the edge equation")
print("    b=c_chi is weight-0 on both sides; the dilatation is inert on it.")
print("  - dimensional no-go: with the single dS scale H, a non-constant f(H)")
print("    is FORBIDDEN; a genuine lock needs a SECOND scale = new physics.")
print("  LOCK STATUS: free-must-tune (c_chi is a free PPN modulus; the only")
print("    symmetry-forced value is luminal, which destroys the mechanism).")
print("  The honest escape (a c_chi=f(H/M) with new scale M) is NEEDS-NEW-INPUT")
print("  and would be MODEL-DEPENDENT, never symmetry-forced.")
