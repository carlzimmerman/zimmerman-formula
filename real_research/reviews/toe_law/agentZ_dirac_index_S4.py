#!/usr/bin/env python3
r"""
METHOD 1 -- ATIYAH-SINGER CHARACTERISTIC-CLASS COMPUTATION of the generation
index on the FORCED Hartle-Hawking Euclidean S^4 nucleation saddle.

Question: is N_gen = |index of the twisted Dirac operator D_E on the round S^4|,
E = the internal SO(10) bundle of the SO(3,11) graviGUT fermions?

Atiyah-Singer (twisted spin Dirac, 4D):
    index(D_E) = int_{S^4} [ Ahat(TS^4) * ch(E) ]_{4-form}
              = int_{S^4} [ (1 - p_1(TS^4)/24 + ...) * (rk E + ch_1(E) + ch_2(E) + ...) ]_4
              = int_{S^4} [ ch_2(E) - (rk E) p_1(TS^4)/24 ]
ch_2(E) = (1/2)(c_1^2 - 2 c_2)(E);  for a bundle with c_1=0 (e.g. an SU(n)/SO(n)
structure), ch_2 = -c_2, and int_{S^4} ch_2(E) = -int c_2(E) = the 2nd Chern
NUMBER = the INSTANTON NUMBER n of the SO(10) bundle (up to the Dynkin-index
normalization of the fermion rep).

This script computes every piece in sympy, extracts the 4-form, integrates over
S^4, and asks: does the index equal 3, a fixed non-3, or n (free)?
"""

import sympy as sp

print("=" * 78)
print("STEP 0.  Geometry of the FORCED saddle: round Euclidean S^4 of radius ell.")
print("=" * 78)

# Hartle-Hawking de Sitter instanton: round S^4 of radius ell_dS = sqrt(3/Lambda).
ell, Lambda = sp.symbols('ell Lambda', positive=True)
ell_dS = sp.sqrt(3 / Lambda)
print(f"  ell_dS = sqrt(3/Lambda) = {ell_dS}")
print("  S^4 is the round 4-sphere: a SYMMETRIC, conformally-flat Einstein space.")

# Euler characteristic and signature of S^4 (topological invariants -- no metric).
chi_S4 = 2          # chi(S^n) = 2 for even n
sigma_S4 = 0        # signature of a 4-manifold; b_2(S^4)=0 so sigma=0
print(f"  chi(S^4)      = {chi_S4}   (Gauss-Bonnet:  int e(TS^4) = chi)")
print(f"  signature(S^4)= {sigma_S4}   (Hirzebruch:    int p_1/3   = sigma)")
print("  pi_1(S^4) = 0  -> SIMPLY CONNECTED -> no Wilson-line generation mechanism.")
print()

print("=" * 78)
print("STEP 1.  Gravitational A-hat genus of TS^4.  Show p_1(S^4)=0 in cohomology.")
print("=" * 78)

# Pontryagin number p_1[S^4] from Hirzebruch signature theorem:  sigma = p_1[M]/3.
p1_number_S4 = 3 * sigma_S4   # = int_{S^4} p_1(TS^4)
print("  Hirzebruch signature:  sigma(M^4) = (1/3) int_{M} p_1(TM)")
print(f"    => int_{{S^4}} p_1(TS^4) = 3*sigma = 3*{sigma_S4} = {p1_number_S4}")
print("  Hence the ONLY characteristic 4-form of the tangent bundle integrates to 0.")
print()
print("  A-hat genus to 4-form order:  Ahat = 1 - p_1/24 + (7 p_1^2 - 4 p_2)/5760 - ...")
print("  The 4-form piece of Ahat(TS^4) is  -p_1(TS^4)/24, and")
print(f"    int_{{S^4}} ( -p_1/24 ) = -(1/24)*int p_1 = -(1/24)*{p1_number_S4} = "
      f"{sp.Rational(-1,24)*p1_number_S4}")
print("  => the PURE-GRAVITY (rk E)*Ahat_2 term contributes EXACTLY 0 on S^4.")
print("     (signature(S^4)=0 => p_1=0 => no gravitational generation contribution.)")
print()

print("=" * 78)
print("STEP 2.  Chern character of the internal SO(10) bundle E.")
print("=" * 78)

# Formal Chern roots x_i of E; ch(E)=sum exp(x_i); ch_2 = (1/2) sum x_i^2.
# Work with the integrated 2nd Chern number directly: define the instanton number.
n = sp.symbols('n', integer=True)        # instanton number  n = int_{S^4} ch_2(E) for the DEFINING (vector) rep, suitably normalized
rkE = sp.symbols('r', positive=True)     # rank of E (carries the fermion rep dimension)

# ch(E) = rk + ch_1 + ch_2 + ...   On S^4 only ch_2 (a 4-form) survives the integral.
# For a bundle with structure group SO(10) and an instanton in pi_3(SO(10))=Z,
#   int_{S^4} ch_2(E_rep) = T(rep) * n,    T = Dynkin index (rep-dependent normalization).
T_rep = sp.symbols('T', positive=True)   # Dynkin index of the fermion rep under SO(10)
ch2_integral = T_rep * n
print("  ch(E) = rk(E) + ch_1(E) + ch_2(E) + ...   ;  H^2(S^4)=0 => ch_1 integrates to 0.")
print("  pi_3(SO(10)) = Z : an SO(10) bundle over S^4 is classified by ONE integer n")
print("    (the instanton number / transition function winding).")
print(f"  int_{{S^4}} ch_2(E) = T(rep) * n = {ch2_integral}   (T = Dynkin index of the rep).")
print()

print("=" * 78)
print("STEP 3.  Assemble the Atiyah-Singer integrand and extract the 4-form.")
print("=" * 78)

# Symbolic 4-form bookkeeping: represent the cohomology degree with a nilpotent 'vol'
# Build the product Ahat(TS^4)*ch(E) symbolically and integrate (= pick the 4-form #).
# Pieces, written as their INTEGRALS over S^4 (numbers):
I_grav  = rkE * sp.Rational(-1,24) * p1_number_S4   # (rk E)*int(-p_1/24)
I_gauge = ch2_integral                              # int ch_2(E)
index = sp.simplify(I_grav + I_gauge)
print("  index(D_E) = int_{S^4}[ Ahat(TS^4) ch(E) ]_4")
print("             = (rk E)*int(-p_1/24)  +  int ch_2(E)")
print(f"             = {I_grav}  +  {I_gauge}")
print(f"             = {index}")
print()
print("  Since p_1(S^4)=0, the gravitational term VANISHES and")
print("    index(D_E) = int_{S^4} ch_2(E) = T(rep) * n  = the SO(10) instanton number.")
print()

print("=" * 78)
print("STEP 4.  Is the bundle (hence n) FORCED or FREE?  Two scenarios.")
print("=" * 78)
print()
print("  (A) FORCED -- standard embedding (spin connection -> gauge connection).")
print("      The only canonical, metric-determined SO(10) connection on the round S^4")
print("      is obtained by embedding the Levi-Civita SO(4) holonomy into SO(10).")
print("      The round S^4 is conformally flat: its self-dual/anti-self-dual Weyl")
print("      tensor vanishes (C=0), so the induced gauge field strength has")
print("      int ch_2 proportional to int (R ^ R)-type density that, for the")
print("      MAXIMALLY SYMMETRIC S^4, gives instanton number tied to p_1(S^4)=0:")
n_forced_standard = 0
print(f"          => n_forced = {n_forced_standard}  (no net instanton; index = 0).")
print("      Index = 0  => VECTORLIKE, ZERO net chiral generations.  NOT 3.")
print()
print("  (B) FREE -- a hand-placed flux / non-canonical bundle.")
print("      Any n in pi_3(SO(10)) = Z is a topologically allowed input by choice.")
print("      Then index = T(rep)*n is a FREE integer scaled by the Dynkin index.")
print("      3 is reachable ONLY if T(rep)*n can equal 3 for integer n -- tested next.")
print()

print("=" * 78)
print("STEP 5.  Dynkin-index PARITY obstruction for the chiral family rep (the 16).")
print("=" * 78)
# Dynkin indices from the IDENTITY  l(R)*dim(G) = C2(R)*dim(R), with C2 computed
# from the highest-weight formula  C2(R) = <lambda, lambda + 2 rho>  in ONE
# normalization (so the RATIO l(16)/l(10) is convention-independent).
# SO(10)=D5: orthonormal e-basis. rho=(4,3,2,1,0). HW(10)=e1, HW(16)=(1/2)(e1+...+e5).
rho   = sp.Matrix([4, 3, 2, 1, 0])
hw10  = sp.Matrix([1, 0, 0, 0, 0])
hw16  = sp.Matrix([sp.Rational(1,2)] * 5)
def C2(lam):                       # <lam, lam + 2 rho>
    return (lam.T * (lam + 2 * rho))[0]
C2_10, C2_16 = C2(hw10), C2(hw16)
# l(R) proportional to dim(R)*C2(R); take ratio (convention-independent).
l_vector_10 = sp.Integer(1)                          # set l(10)=1 (normalization)
l_spinor_16 = sp.Rational(16 * C2_16, 10 * C2_10)    # = l(16)/l(10) in these units
ratio = l_spinor_16
print("  SO(10)=D5 Dynkin indices from C2(R)=<lam,lam+2rho> (highest-weight formula):")
print(f"     C2(10 vector) = {C2_10}   C2(16 spinor) = {C2_16}")
print(f"     l(10  vector)  = {l_vector_10}   (normalization)")
print(f"     l(16  spinor)  = dim*C2 ratio = (16*{C2_16})/(10*{C2_10}) = {l_spinor_16}")
print(f"     l(16)/l(10)    = {ratio}   (this RATIO is normalization-independent, =2)")
assert ratio == 2, "Dynkin ratio must be 2"
print()
print("  The chiral family is the 16 (the forced SO(3,11) Majorana-Weyl content).")
print("  Its index over S^4 is  index_16 = l(16) * k = 2k  for the bundle integer k.")
k = sp.symbols('k', integer=True)
index_16 = l_spinor_16 * k
print(f"     index_16 = l(16)*k = {index_16}")
print()
# Solve 2k = 3 over the integers (k declared integer => sympy returns [] if none).
sol_int = sp.solve(sp.Eq(index_16, 3), k)               # k is integer-typed
kfree = sp.symbols('kf')                                 # un-typed, to expose the rational root
sol_rat = sp.solve(sp.Eq(2 * kfree, 3), kfree)
print(f"  Solve  index_16 = 2k = 3  over the RATIONALS:  k = {sol_rat[0]}  (= 3/2, NOT an integer)")
print(f"  Solve  index_16 = 2k = 3  over the INTEGERS (sympy, k declared Integer): {sol_int}")
print(f"     integer solutions: {sol_int}  (EMPTY) => index_16 is ALWAYS EVEN.")
print("  => N_gen = |index_16| in {0,2,4,...};  3 is PARITY-FORBIDDEN on this saddle.")
print()

# Brute scan to make the parity statement concrete and irrefutable.
reachable = sorted({abs(2*kk) for kk in range(-6, 7)})
print(f"  Brute scan |2k| for k in [-6..6]: {reachable}")
print(f"  Is 3 in the reachable set? {3 in reachable}")
print()

print("=" * 78)
print("STEP 6.  Cross-check -- could the chi=2 Euler class supply '3'? (No.)")
print("=" * 78)
print("  The only OTHER metric-forced characteristic number of S^4 is the Euler")
print("  number chi(S^4)=2 (the Pfaffian of the curvature, a 4-form).  But the")
print("  Dirac index is built from p_1 (a Chern/Pontryagin trace), NOT from the")
print("  Pfaffian; there is NO canonical map turning chi=2 into an instanton")
print("  number, and 2 != 3 in any case.  No characteristic number of S^4 equals 3.")
for nm, val in [("chi(S^4)", 2), ("sigma(S^4)", 0), ("p_1[S^4]", 0),
                ("Ahat-grav index", 0), ("Euler/2", 1)]:
    print(f"     {nm:18s} = {val}   equals 3? {val == 3}")
print()

print("=" * 78)
print("VERDICT")
print("=" * 78)
print("  index(D_E on S^4) = int_{S^4} ch_2(E) = (Dynkin index)*(instanton integer).")
print("   * p_1(S^4)=0  => the gravitational Ahat term is exactly 0 (computed).")
print("   * FORCED standard embedding on the round S^4 => n=0 => index 0 (vectorlike).")
print("   * FREE hand-placed bundle => index = l(rep)*k, a free even integer for the 16.")
print("   * The chiral family is the 16 with l(16)/l(10)=2 => index = 2k ALWAYS EVEN")
print("     => N_gen=3 is PARITY-FORBIDDEN; no characteristic number of S^4 is 3.")
print()
print("  => N_gen is NOT forced to 3 by this index. It is either 0 (forced embedding)")
print("     or a free EVEN integer (placed bundle). 3 arises by NEITHER. The S^4")
print("     spacetime-saddle route does NOT deliver a second derived SM fact.")
print("     N=3 stays FITTED / quarantined. (No manufactured win; the index reduces")
print("     CLEANLY and the FORM 'one chiral 16 from SO(3,11)' is the separate")
print("     forced result, unaffected.)")
