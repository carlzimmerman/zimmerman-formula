#!/usr/bin/env python3
"""
ROUTE B (b): does ANY framework geometric quantity FORCE r=sqrt(2) (cos^2 theta=1/2)?
ROUTE B (c): cross-fermion falsification with REAL PDG masses + neutrino data.

We are RUTHLESS: try every plausible framework geometric route to r=sqrt(2), and concede
honestly where it is a re-labeling / leaves r free / fails cross-fermion.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 50

print("="*78)
print("ROUTE B (b)  --  does framework geometry FORCE r=sqrt(2) ?")
print("="*78)

# --- the framework's forced geometric constants ---
pi = sp.pi
Z2 = sp.Rational(32,3)*pi          # Z^2 = 32pi/3 = Einstein-8pi x Friedmann-3 ... wait: 8pi*4/3? define:
Z2 = 8*pi*sp.Rational(4,3)         # = 32pi/3  (8pi Einstein x 4/3 ... ) keep symbolic
Z  = sp.sqrt(sp.Rational(32,3)*pi) # Z = sqrt(32pi/3) = 5.7888
kappa = sp.Rational(1,2)           # the framework's one free input
seesaw = (sp.Rational(3,1)/(8*pi))**sp.Rational(1,4)  # (3/8pi)^(1/4) = sqrt(2/Z) machine-exact

print("\nForced/canonical framework numbers:")
print("  Z          = sqrt(32pi/3)      =", mp.mpf(sp.N(Z,50)))
print("  Z^2        = 32pi/3            =", mp.mpf(sp.N(sp.Rational(32,3)*pi,50)))
print("  (3/8pi)^1/4 = sqrt(2/Z)        =", mp.mpf(sp.N(seesaw,50)))
print("  kappa      = 1/2")
print("  target r   = sqrt(2)          =", mp.mpf(sp.N(sp.sqrt(2),50)))

print("\n--- enumerate candidate 'forcings' of r and check EXACTLY ---")
sqrt2 = sp.sqrt(2)
cands = {
  "r = sqrt(2)  (TARGET)"                 : sqrt2,
  "1/sqrt(kappa) = sqrt(2)"               : 1/sp.sqrt(kappa),
  "sqrt(2/Z)=(3/8pi)^1/4 (seesaw coeff)"  : seesaw,
  "Z/4"                                   : Z/4,
  "sqrt(Z)/...  -> Z^{1/2}/1.93?"         : sp.sqrt(Z),
  "cube/gauge ratio sqrt(8/12)=sqrt(2/3)" : sp.sqrt(sp.Rational(2,3)),
  "sqrt(N_gen-1)=sqrt(2)  (dim Standard)" : sp.sqrt(2),
  "2/Z"                                   : 2/Z,
  "sqrt(8pi/ (something))"                : None,
}
for name,val in cands.items():
    if val is None:
        continue
    num = mp.mpf(sp.N(val,50))
    eq_exact = sp.simplify(val - sqrt2)==0
    ratio = num/mp.sqrt(2)
    print(f"  {name:42s} = {str(num):>22.22s} | ==sqrt(2)? {str(eq_exact):5s} | /sqrt2 = {str(ratio)[:12]}")

print("""
READING (both ways):
  * 1/sqrt(kappa)=sqrt(2) is EXACT -- but kappa=1/2 is CROSS-SECTOR (a gravity/holography
    normalization, the OUTSIDE fraction of rho_DE), mechanism-free for the Yukawa sector,
    and quark-Koide-FALSIFIED (next section). It is a numerical COINCIDENCE r=1/sqrt(kappa),
    not a derivation: nothing connects the lepton sqrt-mass amplitude to the dark-energy
    fraction. (Banked status; reconfirmed.)
  * sqrt(N_gen-1)=sqrt(2): 'dim Standard = 2' -- this is the re-labeling. dim(Standard)=2
    is a REP-THEORY DIMENSION (an integer count), NOT a vector AMPLITUDE in mass-sqrt space.
    The Koide r=sqrt(2) is the LENGTH of the traceless part RELATIVE to the democratic part;
    that length is a continuous dynamical VEV ratio, not fixed by counting that the standard
    rep is 2-dimensional. (This is exactly the cube/gauge=8/12=2/3 fallacy: a dimension ratio
    is not the angle.) sympy proof of the gap below.
  * (3/8pi)^(1/4)=0.5878 != sqrt(2). The machine-exact seesaw coefficient is NOT r.
  * Z/4=1.447, Z=5.789, sqrt(2/3)=0.816: none equal sqrt(2).
=> NO framework geometric quantity FORCES r=sqrt(2) except the cross-sector kappa coincidence.
""")

# ---- the rep-dimension-vs-amplitude gap, made rigorous ----
print("-"*70)
print("[b'] WHY 'dim(Standard)/dim(Perm)=2/3' is NOT Koide (the slop's central error)")
print("-"*70)
# The slop claims Q = dim(Standard)/dim(Perm) = 2/3. Test: that identity is INDEPENDENT
# of the masses. But Q manifestly DEPENDS on the masses (Q=1/3+r^2/6). A mass-independent
# integer ratio cannot equal a mass-dependent observable except by accident at one r.
r = sp.symbols('r', positive=True)
Q_r = sp.Rational(1,3)+r**2/6
print("  Q(r) = 1/3 + r^2/6  is mass-dependent (varies with r).")
print("  dim(Standard)/dim(Perm) = 2/3 is a FIXED INTEGER RATIO (mass-independent).")
print("  They coincide ONLY at the single r where Q(r)=2/3, i.e. r=sqrt(2):")
print("    solve 1/3+r^2/6 = 2/3 ->", sp.solve(sp.Eq(Q_r,sp.Rational(2,3)),r))
print("  So '2/3 = 8/12 = dim ratio' does NOT explain WHY r lands at sqrt(2);")
print("  it RE-LABELS the answer 2/3. The decomposition 3=1+2 (perm=trivial+standard) is")
print("  REAL and forced by S3, but it fixes the SUBSPACES, not the LENGTH RATIO r. Proof:")

# S3 decomposition is real: project (sqrt m) onto democratic + traceless. The amplitude
# r is the RATIO |traceless|/|democratic| -- a free continuous number for ANY 3-vector.
a,b,c = sp.symbols('a b c', positive=True)  # = sqrt m_i, totally free
v = sp.Matrix([a,b,c])
n = sp.Matrix([1,1,1])
proj_dem = (v.dot(n)/n.dot(n))*n            # democratic (trivial-rep) component
proj_std = v - proj_dem                      # traceless (standard-rep) component
amp_ratio2 = sp.simplify(proj_std.dot(proj_std)/proj_dem.dot(proj_dem))  # = |std|^2/|dem|^2
print("  For an ARBITRARY sqrt-mass vector (a,b,c):  |standard|^2/|democratic|^2 =")
print("    ", amp_ratio2)
# Relate to r: for the Koide circulant, |std|^2/|dem|^2 should equal r^2/2.
# Check with circulant numbers:
M_,r_ = sp.symbols('M_ r_', positive=True)
circ = [M_*(1+r_*sp.cos(2*sp.pi*k/3)) for k in range(3)]
vc = sp.Matrix(circ)
pd = (vc.dot(n)/3)*n
ps = vc - pd
ratio_circ = sp.simplify(ps.dot(ps)/pd.dot(pd))
print("  For the Koide circulant: |standard|^2/|democratic|^2 =", ratio_circ, " = r^2/2")
print("  => r^2/2 is the S3 standard/trivial AMPLITUDE-SQUARED ratio. S3 says NOTHING about")
print("     its value; it is a free VEV ratio. Q=2/3 <=> this ratio = 1 (equal partition).")
print("     'Equal partition of trivial vs standard' is the REAL geometric content -- but")
print("     S3 rep theory does NOT force equal partition; that is the unexplained dynamics.")
