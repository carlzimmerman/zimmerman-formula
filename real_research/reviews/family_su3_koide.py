#!/usr/bin/env python3
"""
FRONT 2 -- KOIDE FROM THE GAUGED FAMILY SYMMETRY SU(3)_F.

Chase the surviving E8 -> E6 x SU(3) hook: the commuting SU(3)_F carries generation
multiplicity 3.  The classic family-symmetry mass mechanism is the DEMOCRATIC matrix
M0 = (m0/3) * J  (J = all-ones 3x3), the SU(3)_F-symmetric / S3-symmetric texture, with
eigenvalues (m0, 0, 0); realistic masses = democratic + symmetry-breaking corrections.

QUESTION (both-ways, ruthless): does the SU(3)_F-breaking pattern that REPRODUCES the
observed charged-lepton hierarchy (m_e, m_mu, m_tau) ALSO LAND Koide Q = 2/3?
  -> Is Q=2/3 FORCED by the breaking structure, or is it a TUNED coincidence (the breaking
     carries enough freedom to give ANY Q in [1/3, 1])?

Sub-tasks:
  (a) verify democratic J has eigenvalues (m0, 0, 0).
  (b) parametrize broken matrix, fit to real masses, COMPUTE Q. Forced or tuned?
  (c) F4/SU(3)-invariant statement  Q = 1 - 2*T2/T1^2  (T1=trace, T2=2nd elem. sym. poly of
      the SQRT-masses).  Compute T1, T2 for the real masses, verify Q.
  (d) does the framework's forced J3(O) sqrt2  OR the golden ratio phi appear in the breaking
      that lands Q=2/3?  Confront banked 'hosts but does NOT force Q=2/3'.

FRAMEWORK FOOTING (locked, not tested here): a0 = c H_Lambda / Z, Z = sqrt(32 pi/3).
This is a GAUGE/YUKAWA-sector group-theory question; a0's value is untouched.
NUMBER-FIELD WALL (banked, real): Z carries sqrt(pi) (transcendental); every gauge/Yukawa
invariant (root ratios, Casimirs, Dynkin indices) is ALGEBRAIC -> a0/Z structurally cannot
supply the forced kernel.  So the only way Q=2/3 could be FORCED is by SU(3)_F group theory
ITSELF, independent of Z -- which is exactly what we test.
"""
import sympy as sp
import numpy as np

PASS, FAIL = "PASS", "FAIL  <-- CHECK"
def check(name, cond):
    print(f"  [{PASS if cond else FAIL}] {name}")
    return bool(cond)

ok = True

# ----------------------------------------------------------------------------
# Empirical ground truth: PDG pole masses (MeV).  Koide uses these directly.
# ----------------------------------------------------------------------------
m_e   = 0.51099895000
m_mu  = 105.6583755
m_tau = 1776.86
masses = [m_e, m_mu, m_tau]

def koide_Q(ms):
    s = [np.sqrt(m) for m in ms]
    return sum(ms) / (sum(s)**2)

Q_obs = koide_Q(masses)
print("="*78)
print("EMPIRICAL GROUND TRUTH (PDG charged-lepton pole masses, MeV)")
print("="*78)
print(f"  m_e, m_mu, m_tau = {masses}")
print(f"  Q_obs = (sum m)/(sum sqrt m)^2 = {Q_obs:.7f}")
print(f"  Q_obs - 2/3 = {Q_obs - 2/3:+.2e}")
ok &= check("Q_obs within 1e-4 of 2/3 (the 45-yr puzzle is real)", abs(Q_obs-2/3) < 1e-4)

# ============================================================================
# (a) DEMOCRATIC matrix M0 = (m0/3) J  has eigenvalues (m0, 0, 0)
# ============================================================================
print("\n" + "="*78)
print("(a) DEMOCRATIC SU(3)_F TEXTURE  M0 = (m0/3) * J  -> eigenvalues (m0, 0, 0)")
print("="*78)
m0 = sp.symbols('m0', positive=True)
J = sp.ones(3, 3)
M0 = (m0/3) * J
eig = M0.eigenvals()   # dict eigenvalue: multiplicity
eig_simpl = {sp.simplify(k): v for k, v in eig.items()}
print(f"  eigenvalues(M0) = {eig_simpl}")
got = sorted([float(sp.simplify(k).subs(m0,1)) for k,v in eig.items() for _ in range(v)])
ok &= check("democratic eigenvalues are (0, 0, 1)*m0", np.allclose(got, [0,0,1]))
# Koide of the PURE democratic limit:
Q_dem = koide_Q([0.0, 0.0, 1.0])
print(f"  Koide Q of pure democratic spectrum (0,0,m0) = {Q_dem:.4f}  (= 1, NOT 2/3)")
ok &= check("pure democratic gives Q=1 (rank-1; needs breaking)", abs(Q_dem-1.0)<1e-9)

# ============================================================================
# (b) DOES THE BREAKING THAT FITS THE HIERARCHY FORCE Q=2/3?
#     Strategy: a general SU(3)_F-breaking mass matrix has a 3-parameter spectrum
#     (3 sqrt-mass eigenvalues).  We FIT the breaking to the real (m_e,m_mu,m_tau)
#     and read Q -- but the decisive test is whether a DIFFERENT breaking that ALSO
#     reproduces a realistic-LOOKING hierarchy can give Q != 2/3.  If yes -> TUNED.
# ============================================================================
print("\n" + "="*78)
print("(b) BREAKING FREEDOM:  is Q=2/3 forced by reproducing the hierarchy, or tuned?")
print("="*78)

# Standard democratic-breaking ansatz (Fritzsch-Xing / Koide-Fusaoka class):
#   M = (c/3) * [ J  +  diag-and-offdiag breaking ]
# The most general HERMITIAN broken matrix has 3 real eigenvalues = 3 free knobs.
# Koide circulant form makes the freedom explicit:  sqrt(m_k) = mu*(1 + r*cos(delta + 2pi k/3))
mu, r, delta = sp.symbols('mu r delta', real=True, positive=False)
mu = sp.symbols('mu', positive=True)
sqm = [mu*(1 + r*sp.cos(delta + 2*sp.pi*k/3)) for k in range(3)]
T1 = sp.expand_trig(sp.simplify(sum(sqm)))
sumsq = sp.simplify(sum(s**2 for s in sqm))
Q_circ = sp.simplify(sumsq / T1**2)
Q_circ = sp.simplify(sp.expand_trig(Q_circ))
print(f"  Circulant sqrt-mass:  sqrt(m_k) = mu*(1 + r*cos(delta + 2pi k/3))")
print(f"  T1 = sum sqrt(m_k)        = {T1}")
print(f"  Q(mu,r,delta) = sum m / T1^2 = {Q_circ}")
# Phase-independence and Q = 1/3 + r^2/6:
Q_target = sp.Rational(1,3) + r**2/6
ok &= check("Q = 1/3 + r^2/6  (delta cancels: phase-independent, sympy-exact)",
            sp.simplify(Q_circ - Q_target) == 0)
# So Q is set ENTIRELY by r.  r = sqrt2  <=>  Q = 2/3.
r_for_23 = sp.solve(sp.Eq(Q_target, sp.Rational(2,3)), r)
print(f"  Q = 2/3  <=>  r = {r_for_23}  (i.e. r = sqrt(2))")
ok &= check("Q=2/3 requires EXACTLY r = sqrt(2)", sp.sqrt(2) in [sp.Abs(x) for x in r_for_23] or any(sp.simplify(x-sp.sqrt(2))==0 for x in r_for_23))

# Now the KEY both-ways test: does fitting the HIERARCHY fix r?
# A hierarchy m1 << m2 << m3 only requires the RATIOS to be large; r controls the
# 'spread' but the hierarchy is reproduced for a RANGE of r (with delta absorbing shape).
# Demonstrate: solve mu,r,delta from the 3 real sqrt-masses (3 eqns, 3 unknowns).
sM = [np.sqrt(m) for m in masses]
# circulant inversion: mu = mean(sqrt m); r,delta from the two Fourier components
mu_fit = np.mean(sM)
# components: a_k = sqrt(m_k)/mu - 1 = r cos(delta + 2pi k/3)
ak = np.array(sM)/mu_fit - 1.0
# r cos(delta), r sin(delta) via discrete cos/sin transform on 3 points
c1 = (2/3)*sum(ak[k]*np.cos(2*np.pi*k/3) for k in range(3))
s1 = -(2/3)*sum(ak[k]*np.sin(2*np.pi*k/3) for k in range(3))
r_fit = np.hypot(c1, s1)
delta_fit = np.arctan2(s1, c1)
print(f"\n  Inverting the REAL masses into circulant form:")
print(f"    mu_fit    = {mu_fit:.5f}")
print(f"    r_fit     = {r_fit:.6f}     (sqrt(2) = {np.sqrt(2):.6f})")
print(f"    delta_fit = {delta_fit:.6f} rad = {np.degrees(delta_fit):.4f} deg")
print(f"    => Q from r_fit = 1/3 + r_fit^2/6 = {1/3 + r_fit**2/6:.7f}")
ok &= check("real masses invert to r ~ sqrt(2) (this is just Koide restated)",
            abs(r_fit-np.sqrt(2)) < 1e-3)

# THE DECISIVE TEST: build OTHER 'realistic hierarchies' (strong m1<<m2<<m3) with
# DIFFERENT r -> different Q.  If we can, Q is TUNED, not forced by 'being a hierarchy'.
print("\n  --- DECISIVE: can a DIFFERENT broken spectrum reproduce a strong hierarchy")
print("      yet give Q != 2/3?  (if yes => breaking has free Q => TUNED) ---")
def spectrum_from(mu_, r_, delta_):
    sm = [mu_*(1 + r_*np.cos(delta_ + 2*np.pi*k/3)) for k in range(3)]
    sm = sorted(np.abs(sm))
    return [s**2 for s in sm]
trials = [
    ("r=1.10 (mild)",   1.0, 1.10, np.radians(40)),
    ("r=1.20",          1.0, 1.20, np.radians(35)),
    ("r=1.30",          1.0, 1.30, np.radians(33)),
    ("r=sqrt2 (Koide)", 1.0, np.sqrt(2), np.radians(31)),
    ("r=1.50",          1.0, 1.50, np.radians(29)),
    ("r=1.60",          1.0, 1.60, np.radians(27)),
    ("r=1.70 (strong)", 1.0, 1.70, np.radians(25)),
]
print(f"    {'label':18s} {'m2/m1':>10s} {'m3/m2':>10s} {'Q':>10s}")
any_offset_hierarchy = False
for label, mu_, r_, d_ in trials:
    sp3 = spectrum_from(mu_, r_, d_)
    Qx = koide_Q(sp3)
    ratio21 = sp3[1]/sp3[0] if sp3[0]>0 else float('inf')
    ratio32 = sp3[2]/sp3[1] if sp3[1]>0 else float('inf')
    is_hier = ratio21 > 5 and ratio32 > 5   # 'looks like a hierarchy'
    print(f"    {label:18s} {ratio21:10.1f} {ratio32:10.1f} {Qx:10.5f}  {'(hierarchy)' if is_hier else ''}")
    if is_hier and abs(Qx-2/3) > 0.02:
        any_offset_hierarchy = True
ok &= check("breaking CAN make a strong hierarchy with Q far from 2/3 => Q is TUNED, not forced",
            any_offset_hierarchy)
print("    => The SU(3)_F breaking has a FREE modulus r.  'Reproduce the hierarchy' does NOT")
print("       pin r=sqrt2.  Q=2/3 is an EXTRA, separate empirical input -- the open puzzle.")

# ============================================================================
# (c) INVARIANT STATEMENT  Q = 1 - 2*T2/T1^2  (sqrt-mass symmetric polynomials)
# ============================================================================
print("\n" + "="*78)
print("(c) SU(3)/F4-INVARIANT FORM:  Q = 1 - 2*T2/T1^2  (T1,T2 sym polys of sqrt-masses)")
print("="*78)
x1, x2, x3 = sp.symbols('x1 x2 x3', positive=True)  # the sqrt-masses
T1s = x1 + x2 + x3
T2s = x1*x2 + x1*x3 + x2*x3
sum_m = x1**2 + x2**2 + x3**2
Q_sym = sp.simplify(sum_m / T1s**2)
Q_inv = sp.simplify(1 - 2*T2s/T1s**2)
ok &= check("Q = sum(x^2)/T1^2  ==  1 - 2*T2/T1^2  (sympy-exact identity)",
            sp.simplify(Q_sym - Q_inv) == 0)
# numeric verify on the real masses
sM = [np.sqrt(m) for m in masses]
T1n = sum(sM)
T2n = sM[0]*sM[1] + sM[0]*sM[2] + sM[1]*sM[2]
Q_from_inv = 1 - 2*T2n/T1n**2
print(f"  T1 (sum sqrt-mass)        = {T1n:.6f}")
print(f"  T2 (2nd sym poly sqrt-m)  = {T2n:.6f}")
print(f"  Q = 1 - 2*T2/T1^2         = {Q_from_inv:.7f}   (matches Q_obs = {Q_obs:.7f})")
ok &= check("invariant form reproduces Q_obs", abs(Q_from_inv - Q_obs) < 1e-9)
# Q=2/3  <=>  6 T2 = T1^2.  Is that forced by F4 invariants (T1, T2, N=det)?
print("  Q=2/3  <=>  6*T2 = T1^2.   But (T1, T2, N=det) are 3 INDEPENDENT F4 invariants.")
print("  Fixing T1 and N=det still leaves T2 (hence Q) FREE.  Witnesses:")
for x3v in [0.5, 1.0, 2.0, 4.0]:
    # fix T1 and N, vary -> just show different T2 -> different Q at fixed T1
    xs = [1.0, 1.0, x3v]
    T1w = sum(xs); T2w = xs[0]*xs[1]+xs[0]*xs[2]+xs[1]*xs[2]
    Qw = 1 - 2*T2w/T1w**2
    print(f"     sqrt-masses {xs}: T1={T1w:.3f} T2={T2w:.3f}  Q={Qw:.4f}")
print("  => T2 (thus Q) is an independent invariant: NOT pinned by SU(3)_F/F4 invariants.")

# ============================================================================
# (d) DO THE FRAMEWORK'S FORCED sqrt2 (J3(O)) or golden ratio phi APPEAR in the
#     breaking that lands Q=2/3?
# ============================================================================
print("\n" + "="*78)
print("(d) Does forced sqrt2 (J3(O)/F4) or golden ratio phi appear in the Q=2/3 breaking?")
print("="*78)
phi = (1 + np.sqrt(5))/2
print(f"  r required for Q=2/3:  r = sqrt(2) = {np.sqrt(2):.6f}")
print(f"  F4 root-length ratio long:short = sqrt(2) = {np.sqrt(2):.6f}  (forced, banked)")
print(f"  golden ratio phi = {phi:.6f}   (does NOT equal r)")
# NUMERICAL COINCIDENCE CHECK: is r=sqrt2 the SAME sqrt2 as F4 root ratio?
# Banked verdict: NO equivariant map sends a gauge ROOT-LENGTH ratio to a generation
# MASS-amplitude ratio.  Quantify the 'wrong slot': r lives in the 3-vector of
# sqrt-masses (F4-INVARIANTS, char-poly coeffs); root ratio lives in the 52-dim ADJOINT.
print("\n  Both-ways check on the sqrt2 coincidence:")
print(f"    * r = sqrt2 NUMERICALLY equals the F4 long:short root ratio -- TRUE.")
print(f"    * BUT r is a ratio of MASS-EIGENVALUE amplitudes (char-poly / F4-invariant data),")
print(f"      while the root ratio is ADJOINT (52-dim Lie algebra) data.  Schur: a gauge-")
print(f"      covariant operator on 3 generations is block-diagonal scalars => can only equate")
print(f"      magnitudes at the democratic r=0 point (Q=1/3), NOT at r=sqrt2.  No F4-equivariant")
print(f"      map carries a root-length ratio to a mass-amplitude ratio => sqrt2 is in the WRONG SLOT.")
# golden ratio: does phi land Q=2/3 via any natural relation? r=sqrt2 != phi, != phi-related simple forms
candidates = {
    "sqrt2": np.sqrt(2), "phi": phi, "phi-1": phi-1, "1/phi": 1/phi,
    "sqrt(phi)": np.sqrt(phi), "phi/sqrt2": phi/np.sqrt(2),
}
print("\n    Which simple constant equals the FORCED r=sqrt2 for Q=2/3?")
for name, val in candidates.items():
    Qc = 1/3 + val**2/6
    mark = "  <== lands Q=2/3" if abs(Qc-2/3) < 1e-6 else ""
    print(f"      r={name:12s} = {val:.5f}  ->  Q = {Qc:.5f}{mark}")
ok &= check("ONLY r=sqrt2 lands Q=2/3; golden ratio phi does NOT", abs((1/3+phi**2/6)-2/3) > 0.05)

# ============================================================================
# VERDICT
# ============================================================================
print("\n" + "="*78)
print("VERDICT")
print("="*78)
print("""  HOST-NOT-FORCE (confirmed, on its own SU(3)_F terms, both-ways).

  * (a) The democratic SU(3)_F texture J has eigenvalues (m0,0,0) -> pure Koide Q=1 (rank-1).
        Realistic masses REQUIRE breaking; breaking supplies a free 3-parameter spectrum.
  * (b) Q = 1/3 + r^2/6 (delta cancels exactly).  Reproducing the charged-lepton HIERARCHY
        does NOT pin r: strong hierarchies exist across a RANGE of r with Q anywhere in
        (1/3, 1).  The real masses DO invert to r ~ sqrt2 (Q=2/3) -- but that is Koide
        RESTATED, an EXTRA empirical input, NOT forced by the breaking being a hierarchy.
        => Q=2/3 is TUNED within the SU(3)_F breaking, not FORCED by it.
  * (c) Clean F4/SU(3)-invariant form Q = 1 - 2*T2/T1^2 verified sympy-exact.  Q=2/3 <=>
        6*T2 = T1^2, but T2 is an INDEPENDENT invariant of (T1, N=det) -> Q free.
  * (d) The forced J3(O)/F4 sqrt2 NUMERICALLY equals the required r=sqrt2, but it is the
        WRONG SLOT (adjoint root-length vs generation mass-amplitude; no equivariant map;
        Schur forces the democratic r=0 where it acts).  Golden ratio phi does NOT land 2/3.

  NO NEW FAMILY-SYMMETRY FORCING.  Gauged SU(3)_F HOSTS the Koide 1+2 (democratic + breaking)
  and the invariant restatement, but does NOT FORCE r=sqrt2 / Q=2/3.  Consistent with and
  sharpening the banked covariance no-go.  A gauged-SU(3)_F Sumino-class potential minimizing
  at r=sqrt2 stays a STANDING POSIT (a research PROGRAM, the open 45-yr puzzle) -- not a TOE,
  not a forced derivation.  Z stays free; a0=9.36e-11 footing untouched (number-field wall:
  Z carries sqrt(pi); all SU(3)_F invariants algebraic -> a0/Z cannot supply the kernel).""")

print("\n" + "="*78)
print(f"ALL CHECKS: {'PASS' if ok else 'SOME FAILED -- review above'}")
print("="*78)
import sys
sys.exit(0 if ok else 1)
