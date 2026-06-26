import sympy as sp, mpmath as mp
mp.mp.dps=40
print("="*70)
print("ROUTE 1 — S3/A4 FLAVON POTENTIAL: VERDICT CONSOLIDATION")
print("="*70)
print("""
MAP (no 2/3 inputted):  sqrt-mass vector x_i, S3-decompose into
  singlet s (democratic (1,1,1)) + doublet d (orthogonal complement).
  Brannen amplitude:  r^2 = 2 (d/s)^2.
  => r=sqrt2  <=>  d = s  (doublet magnitude EQUALS singlet magnitude, 50/50 split).
  [Q=1/3+r^2/6 only used to LABEL r=sqrt2<->Q=2/3 a posteriori; never in any V.]

FINDING 1 (renormalizable S3 potential minima):
  The MINIMA of every natural renormalizable S3-invariant polynomial potential
  (built from e1,q,c,t and quartics, NO 2/3) sit at the residual-subgroup
  alignments:  (1,1,1)->r=0 ;  (1,1,0)/(0,1,1)->r=1 ;  (0,0,1)->r=2 ;
  (1,1,-1)->r=4 ;  pure-doublet->r=inf.   These are RATIONAL r (Q in {1/3,1/2,1,3}).
  r=sqrt2 (irrational) is NEVER a symmetry-protected vacuum.

FINDING 2 (tuning, not forcing):
  To land the VEV at r=sqrt2 needs the S2-branch ratio b/a = 4-3sqrt2 = -0.2426...,
  which imposes a CODIMENSION-2 tuned relation on the couplings (m2,L,h,k).
  r drifts CONTINUOUSLY through sqrt2 only on a measure-zero tuned surface. NOT forced.

FINDING 3 (the steelman that DID hit r=sqrt2 -- and why it's dead):
  The ratio-invariant  f2 = d^2 s^2 / q^2  (q=d^2+s^2)  is extremized EXACTLY at d=s
  => r=sqrt2, and its definition has NO 2/3.  BUT:
   (a) it is NOT a renormalizable potential -- it's a degree-0 ratio; its extremum is
       pure AM-GM ('maximize product d^2*s^2 at fixed sum q' => d^2=s^2). A generic
       balance principle, not a flavor dynamics. Choosing to extremize d*s rather than
       d (=>r=2) or s (=>r=0) is the SMUGGLE: 'balance the two irreps' is logically
       'set d=s' = 'set r=sqrt2' = re-labeling #168.
   (b) FLAVOR-BLIND => FALSIFIED: AM-GM equal-split forces r=sqrt2 (Q=2/3) for ALL
       sectors. Quarks measured at r=1.759 (up, Q=0.849) and r=1.545 (down, Q=0.731),
       NOT sqrt2. No sector label in f2 -> cannot be lepton-specific. Cross-fermion KILL.

LEPTON-SPECIFICITY: none of the S3 invariants carry a sector label, so any principle
  that forces 45deg forces it universally -> contradicts quarks. The potential route
  provides NO mechanism for 'leptons only'.

VERDICT: NULL.  No invariant-built S3/A4 potential FORCES r=sqrt2 as its vacuum.
  Natural minima land at rational r (0,1,2,4,inf); r=sqrt2 is reachable only by
  codim-2 tuning or by the AM-GM equal-split ratio, which is (a) a disguised
  'set d=s' smuggle and (b) flavor-blind hence quark-falsified.  168th re-labeling.
""")
# numeric confirmations
def Q(t): 
    x=[mp.sqrt(m) for m in t]; return sum(t)/sum(x)**2
me,mmu,mtau=mp.mpf('0.51099895e-3'),mp.mpf('0.1056583755'),mp.mpf('1.77686')
print("lepton Q =", mp.nstr(Q((me,mmu,mtau)),10), " (r=sqrt2 target Q=2/3)")
print("4-3sqrt2  =", mp.nstr(4-3*mp.sqrt(2),12), " (the tuned VEV ratio for r=sqrt2)")
print("sqrt2     =", mp.nstr(mp.sqrt(2),12))
