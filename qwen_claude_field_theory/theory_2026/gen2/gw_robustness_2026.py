#!/usr/bin/env python3
r"""How wrong would the Gen-1 GW no-go have to be to be survivable?
Carl's question: 'maybe something is wrong with GW on this one'.  Test it, don't reassure."""
import numpy as np
def head(t): print("\n"+"="*98+f"\n{t}\n"+"="*98)
c=2.99792458e8; a0=9.3619e-11
L=c**2/a0
head("A -- the anti-suppression factor is arithmetic, not modelling")
print(f"  c^2/a0 = {L:.4e} m  ({L/9.461e15:.2e} light-years) -- a COSMOLOGICAL length,")
print(f"  because a0 is a tiny acceleration.  Any operator carrying 1/a0^2 with two extra")
print(f"  spatial derivatives is therefore ENHANCED, not suppressed, for short waves.")
for f,lab in ((100.0,"LIGO 100 Hz"),(35.0,"GW170817 low band"),(1e3,"LIGO 1 kHz")):
    k=2*np.pi*f/c
    print(f"  {lab:<22} k = {k:.3e} 1/m   (k c^2/a0)^2 = {(k*L)**2:.3e}")
head("B -- how wrong must each ingredient be to rescue eps ~ 1.1e-24?")
k=2*np.pi*100/c; enh=(k*L)**2
need=1e-15                      # |dv/v| bound
eps=1.1e-24
for A,lab in ((1/16,"A at its MAXIMUM (X=1)"),(0.03,"Galactic-path A"),(1e-6,"IGM A (X~1e-3)")):
    pred=3*eps*A*enh            # group-velocity excess
    print(f"  {lab:<26} predicted |dv/v| = {pred:.3e}   exceeds bound by {pred/need:.2e}x")
print()
print(f"  To survive, ONE of these must be wrong by the factor in brackets:")
pred=3*eps*(1e-6)*enh           # already the most generous A
print(f"    the O(1) coefficient (2 or 3):            [{pred/need:.1e}]  -- i.e. ~1e{np.log10(pred/need):.0f}")
print(f"    A along the whole path:                   needs A < {need/(3*eps*enh):.2e}")
Areq=need/(3*eps*enh)
Xreq=np.sqrt(Areq)              # A ~ X^2 at small X
print(f"      A ~ X^2 at small X, so that needs X < {Xreq:.2e}, i.e. g < {Xreq*a0:.2e} m/s^2")
print(f"      -- but even INTERGALACTIC fields are ~1e-13 m/s^2, giving X ~ {1e-13/a0:.1e},")
print(f"         A ~ {(1e-13/a0)**2:.1e}.  Short by {(1e-13/a0)**2/Areq:.1e}.")
print(f"    the GW170817 bound itself:                would have to be weaker by {pred/need:.1e}x")
head("C -- verdict on the Gen-1 GW no-go")
print("  The k^4 structure is KINEMATICS (delta Rbar_ij ~ d^2 gamma) and the 1e42 is")
print("  ARITHMETIC (c^2/a0 is 1e27 m).  Constraint elimination changes K_T and G_T by")
print("  O(1) factors -- it cannot close a 22-to-40 order gap.  I cannot construct a")
print("  version of this calculation in which Y_R survives at eps ~ 1e-24.")
print("  WHAT WOULD OVERTURN IT: if the constraint-reduced quadratic action cancels the")
print("  k^4 term IDENTICALLY (coefficient exactly zero, not small).  That is the one")
print("  possibility the running program is testing, and it is not absurd -- degenerate")
print("  cancellations do happen in constrained systems.  Until it reports, the no-go is")
print("  'robust to everything I can vary', not 'proved'.")
head("D -- THE HONEST LEDGER: GW is NOT the only problem")
rows=[
 ("a0 is NOT derived -- it is an input","INDEPENDENT of GW",
  "the original ambition (a0^2 ~ c^2 G rho_DE) FAILED: X=Y=0 on FLRW, F(0,0)=0"),
 ("eps ~ 1e-24 unprotected by any symmetry","INDEPENDENT",
  "and it sets M* = eps c^4/(G a0) ~ 0.6 Msun -- a preferred mass at the Sun's"),
 ("lam_K -> 1 forced by BBN/CMB, c_s^2 -> 0 there","INDEPENDENT",
  "possible strong coupling; Gen-1 called the corner 'marginal, not comfortably interior'"),
 ("deep-MOND strong coupling at 0.13 mm","INDEPENDENT",
  "F is C^1 but breaks at CUBIC order; an EFT cutoff in the laboratory range"),
 ("not technically natural","INDEPENDENT",
  "loops regenerate (3)R^2, (Lie_u K)^2 etc. with O(1) coefficients; action is not generic at 4th order"),
 ("superluminal khronon in the Newtonian regime","INDEPENDENT",
  "gravitational-Cherenkov and PPN alpha_1,2 constraints NOT computed -- could tighten further"),
 ("the SPARC motivation was never a detection","INDEPENDENT",
  "beta = +0.10 +- 0.078, permutation p ~ 0.2; every control equally null"),
 ("Q2 only at LINEAR order in chi","INDEPENDENT",
  "chi ~ 0.6 is not small; O(chi^2) unknown, needs the implicit 4th-order solver"),
 ("Gen-1 tidal sector excluded by GW170817","THE GW ITEM",
  "~29 orders; Gen-2 repairs THIS ONE ONLY"),
]
for a,b,cx in rows:
    print(f"  [{b:<16}] {a}\n{'':22}{cx}")
print("\n  Gen-2 fixes exactly ONE line of that table.  The other eight are untouched.")
