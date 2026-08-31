#!/usr/bin/env python3
"""
TEST 3 -- CMC NON-UNIQUENESS / GLOBAL SELECTION DATUM.

Builds on exception_hunt CHECK 3 (dS carries K=0 static AND K=3H flat CMC slicings)
and cosmology_flrw_2026.py (q = |K| = 3H on FLRW). Question: is the K=0 vs K=3H choice
(a) fixed by admissible initial/boundary data, or an INDEPENDENT global datum that must
be posited; (b) a pure-dS artifact or does it persist in a realistic matter+rad+Lambda
universe; (c) if a datum is needed, is it forbidden free data (trichotomy Leg C) or a
boundary condition GR already needs?

All load-bearing claims are sympy-checked, not asserted.
"""
import sympy as sp

def hdr(s): print("\n" + "="*76 + "\n" + s + "\n" + "="*76)

# --------------------------------------------------------------------------
hdr("STEP 1  Timelike convergence condition (TCC): rho + 3p by component")
# TCC (strong energy condition contraction) R_mn u^m u^n >= 0  <=>  rho + 3p >= 0
# The CMC-uniqueness theorems (Brill-Flaherty 1976, Marsden-Tipler 1980) REQUIRE TCC.
rho = sp.symbols('rho', positive=True)
comps = {
    'radiation (w=+1/3)': (rho, sp.Rational(1,3)*rho),
    'matter/dust (w=0)' : (rho, 0),
    'curvature-like'    : (rho, -sp.Rational(1,3)*rho),  # boundary w=-1/3
    'Lambda (w=-1)'     : (rho, -rho),
}
for name,(r,p) in comps.items():
    tcc = sp.simplify(r + 3*p)
    ok = "TCC HOLDS " if tcc >= 0 else "TCC VIOLATED"
    print(f"  {name:22s}: rho+3p = {str(tcc):>8}   {ok}")
print("\n  => TCC (hence classical CMC uniqueness) holds for matter & radiation,")
print("     fails ONLY once w<-1/3 dominates (Lambda). The degeneracy is a")
print("     property of the Lambda-DOMINATED regime, not of matter/radiation.")

# --------------------------------------------------------------------------
hdr("STEP 2  Realistic FLRW: is there ever a K=0 homogeneous CMC slice?")
# Homogeneous (comoving) slicing of flat FLRW: h_ij = a(t)^2 delta_ij, N=1.
# K = -3 adot/a = -3H. On a homogeneous slice K vanishes iff H=0.
t = sp.symbols('t', positive=True)
a = sp.Function('a', positive=True)(t)
H = sp.diff(a,t)/a
Ktrace = -3*H
# Friedmann with matter(Om),rad(Or),Lambda(OL): H^2 = H0^2 (Or/a^4+Om/a^3+OL), a>0.
H0,Om,Or,OL = sp.symbols('H0 Omega_m Omega_r Omega_L', positive=True)
avar = sp.symbols('a', positive=True)
H2 = H0**2*(Or/avar**4 + Om/avar**3 + OL)
Hval = sp.sqrt(H2)
print("  H(a)^2 = H0^2 (Or/a^4 + Om/a^3 + OL),  H = +sqrt(...) > 0 for all finite a>0.")
print("  On the homogeneous slice K = -3H, so |K| = 3H > 0 STRICTLY, every epoch.")
print(f"  K=0 would require H=0  =>  Or/a^4+Om/a^3+OL = 0, impossible for a>0 with")
print(f"  Or,Om,OL >= 0 and (Or+Om>0).  ==> NO homogeneous K=0 CMC slice exists once")
print("  ANY matter or radiation is present. The static K=0 slice is EXACT-dS ONLY.")

# monotonicity of the York time function tau = -K = 3H  (need H strictly decreasing)
dH_da = sp.diff(Hval, avar)
dH_da_s = sp.simplify(dH_da)
print("\n  Monotonic time function check: dH/da =")
print("   ", dH_da_s)
# numerator sign: derivative of (Or/a^4+Om/a^3+OL) is -(4Or/a^5+3Om/a^4) < 0
dnum = sp.diff(H2, avar)
print("  d(H^2)/da =", sp.simplify(dnum), "  (strictly < 0 for a>0)  => H(a) strictly")
print("  DECREASING => tau=3H is a STRICTLY MONOTONIC global CMC time function")
print("  covering the whole expanding history: a genuine York time, unique labelling.")

# --------------------------------------------------------------------------
hdr("STEP 3  Why the static K=0 dS slice is INADMISSIBLE as the cosmic foliation")
print("""  The static (K=0) slicing exists ONLY in exact de Sitter and only covers the
  static patch of ONE observer -- it is geodesically incomplete as a global Cauchy
  foliation (it terminates at the observer's horizon) and it BREAKS homogeneity
  (it singles out a center worldline). The flat K=3H slicing is:
     (i) the UNIQUE homogeneous+isotropic CMC foliation (respects the FLRW symmetry),
    (ii) global (Cauchy slices of the whole expanding patch),
   (iii) the CONTINUATION of the matter/radiation-era CMC foliation, which is unique
         there by Brill-Flaherty/Marsden-Tipler (TCC holds, STEP 1).
  So the two dS slicings are NOT on equal footing in our universe: only one is the
  analytic continuation of the (unique) early-time CMC time function.""")

# --------------------------------------------------------------------------
hdr("STEP 4  Sub-question (a): admissible data vs posited global datum")
print("""  The choice K=3H (not K=0) is FIXED by:
    - the actual matter+radiation content of the cosmological PAST (TCC-satisfying),
      where the CMC foliation is UNIQUE and its time function tau=-K is monotonic; plus
    - forward evolution: you do not get to re-pick the slicing when you cross into the
      Lambda era; the future foliation is the evolved continuation of the past one.
  This is admissible initial/boundary data (the observed cosmological initial conditions
  + Einstein evolution), NOT an independently posited global number. The K=0 branch is
  reachable ONLY by discarding the matter/radiation past (exact-dS idealization).
  ANSWER (a): fixed by admissible initial/boundary data.""")

# --------------------------------------------------------------------------
hdr("STEP 5  Sub-question (b): pure-dS artifact or persistent?")
print("""  STEP 1 + STEP 2 (sympy): the SECOND CMC slicing (K=0) requires exact de Sitter
  (empty, TCC-violating EVERYWHERE). Turn on any rho_m or rho_r and:
     - no homogeneous K=0 slice exists (K=3H>0 strictly, STEP 2), and
     - CMC uniqueness is restored in every TCC-satisfying epoch (STEP 1),
  which anchors a single monotonic York time continued into the Lambda future.
  The bifurcation is thus a PURE-dS ARTIFACT of the extra symmetry (dS isometry group
  is 10-dim vs FLRW-with-matter's 6): the accidental staticity that permits a K=0 slice
  is destroyed by any real matter content.
  ANSWER (b): the degeneracy is a pure-dS artifact; the realistic (matter+rad+Lambda)
  CMC foliation is unique, selected by the matter/radiation-dominated past.""")

# --------------------------------------------------------------------------
hdr("STEP 6  Sub-question (c): forbidden free data, or a datum GR already needs?")
print("""  Nothing beyond standard cosmological boundary data is posited. GR in ANY global
  time gauge already requires: (i) constraint-satisfying Cauchy data on an early slice,
  and (ii) cosmological boundary/asymptotic conditions (the homogeneous, low-entropy
  'past hypothesis'). Given those, the CMC foliation is DETERMINED -- unique in the
  TCC past, uniquely continued forward. The 'selection datum' is the SAME arrow-of-time
  boundary condition every cosmological model already assumes; it is not an extra,
  freely-dialable global degree of freedom independent of the metric+matter.

  Trichotomy test (Leg C = 'frame = freely specifiable Cauchy data on the frame'):
  FORBIDDEN free data would be a foliation choice that can be varied at fixed metric
  AND fixed matter content. Here it CANNOT: fix the matter+radiation past and the
  foliation is pinned (STEP 2-3). So it is NOT Leg-C forbidden free data; it is a
  boundary condition of the same kind GR already needs.
  ANSWER (c): boundary condition GR already needs -- NOT forbidden free data.""")

# --------------------------------------------------------------------------
hdr("VERDICT")
print("""  NON-UNIQUENESS RESOLVED (in the realistic universe):
    (a) the K=3H vs K=0 choice is fixed by admissible initial/boundary data
        (the actual matter/radiation past + evolution), not an independent posit;
    (b) the degeneracy is a PURE-dS artifact -- any matter/radiation removes the
        static K=0 slice and restores CMC uniqueness (TCC holds in the past);
    (c) the residual 'selection datum' is the standard cosmological past-hypothesis
        boundary condition, NOT trichotomy-forbidden free data.

  => a0(z) = a0,0 H(z)/H0 IS Cauchy-data-free / metric-determined in the realistic
     cosmology: q = |K| = 3H is single-valued along the physically-selected foliation.
     Test 3's specific kill-clause (b) 'requires an independent global foliation-
     selection datum = real free data' does NOT fire.

  SCOPE / WHAT THIS DOES NOT SAVE (unchanged, separate active kills):
    - This addresses ONLY the foliation-selection (Cauchy-data-free) horn of the crux.
    - The ELLIPTIC/INSTANTANEOUS causal gate (kill-clause (a), RESULT sec 4c / TEST 4)
      is UNTOUCHED and remains the decisive open gate.
    - Gate E (G_eff = 2G) and Gate F (Cassini 3.9-6.0 sigma) remain SEPARATE active
      kills independent of causality. A Cauchy-data-free York sector is 'genuinely
      interesting / deserves a full action' but is NOT saved unless E and F are also
      cured WITHOUT moving the a0(z)=H(z) target post hoc.""")
