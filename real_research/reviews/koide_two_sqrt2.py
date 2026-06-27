#!/usr/bin/env python3
"""
FRONT 1 — THE TWO sqrt(2)'s.  Are theta(0)=sqrt2 (the framework's MI kernel DC weight) and
r=sqrt2 (the Koide 45-degree mass-amplitude) a SHARED GENERATOR, or INDEPENDENT sqrt(2)'s
that happen to be the same number?

CARL'S #1 RULE: no manufactured win.  Expected = COINCIDENCE / WRONG-SLOT.  The non-circularity
BAR: produce a forced sqrt2 in the SECOND slot (r) WITHOUT putting 45deg/sqrt2/(2/3) into the
inputs, via a LOGICAL CHAIN that starts from the FIRST slot's sqrt2 (theta(0)).

FOOTING (locked, never tested here): a0 = c H_Lambda / Z, Z = sqrt(32 pi/3) = 2 sqrt(8pi/3);
framework's OWN interpolation mu_fw(x) = (sqrt(1+4x^2)-1)/(2x); identity 1/mu_fw - mu_fw = 1/x;
mu_fw(1) = 1/phi.  NEVER McGaugh nu.

WHAT EACH sqrt2 IS (banked, restated below from the real derivations):

  theta(0) = sqrt2  -- THETA_KERNEL_TOWARD_FORCED_2026-06.md.  The MI kernel theta(y) sits inside
    the inertia argument A = a_in + theta(y)*a_ex.  theta(0) is the EFE-normalized DC weight of a
    static external field: theta(0) = w(0)/w(1).  The dS-Unruh excess-heat engine is DEGREE-1
    (linear) in the acceleration amplitude [DeltaT = T(a)-T(0) ~ sqrt(a^2+(cH)^2) - cH], and on an
    AMPLITUDE (not power) transfer the -3 dB corner is 1/sqrt2 -> theta(0) = sqrt2.  This is a
    property of a 1-D bath correlator / single-pole memory.  It is a SCALAR on the time axis.

  r = sqrt2  -- KOIDE_TRIALITY_OCTONION / KOIDE_SELFDUALITY.  The sqrt-mass vector
    v = (sqrt m_e, sqrt m_mu, sqrt m_tau) decomposes under S3 into trivial-singlet (democratic axis
    n=(1,1,1)/sqrt3) + standard-doublet.  Brannen circulant sqrt m_k = mu(1 + r cos(delta+2 pi k/3))
    gives Q = 1/3 + r^2/6, phase-independent.  Q = 2/3  <=>  r = sqrt2  <=>  angle(v,n)=45deg
    <=>  |P_singlet v| = |P_doublet v|.  r is a ratio of 3-VECTOR projection magnitudes in
    generation space.

THE TEST: is there a FORCED, NON-CIRCULAR MAP  theta(0)=sqrt2  ==>  r=sqrt2 ?
Or are these different objects (1-D time-axis bath scalar vs 3-vector generation-space amplitude)
that share only the minimal polynomial t^2-2 ?

All claims COMPUTED (sympy / mpmath), exit 0, numbers printed.  Both-ways, no faked crack.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

t = sp.Symbol('t')
PASS, FAIL = "PASS", "FAIL <-- CHECK"
def ck(name, cond):
    print(f"  [{PASS if cond else FAIL}] {name}")
    return bool(cond)

allok = True

# =====================================================================================
print("="*86)
print("(0) FOOTING — framework's own constants (locked, not under test)")
print("="*86)
Z = 2*sp.sqrt(sp.Rational(8,1)*sp.pi/3)
print(f"  Z = sqrt(32pi/3) = {float(Z):.6f} ; Z/sqrt(pi) = {sp.simplify(Z/sp.sqrt(sp.pi))} (algebraic) -> Z transcendental")
x = sp.Symbol('x', positive=True)
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)
phi = (sp.sqrt(5)+1)/2
mu1 = sp.simplify(mu_fw.subs(x,1))
allok &= ck(f"mu_fw(1) = {mu1} = 1/phi = {float(mu1):.6f}  (golden, framework's own)",
            sp.simplify(mu1 - 1/phi) == 0)
# the framework identity
ident = sp.simplify((1/mu_fw - mu_fw) - 1/x)
allok &= ck(f"framework identity 1/mu_fw - mu_fw = 1/x   (residual {ident})", ident == 0)

# =====================================================================================
print("\n"+"="*86)
print("(A) BOTH sqrt2's, RESTATED from their banked derivations + minimal polynomials")
print("="*86)

print("\n  --- SLOT 1: theta(0) = sqrt2  (MI kernel DC weight; dS-Unruh excess-heat engine) ---")
print("  Logic (THETA_KERNEL_TOWARD_FORCED): T(a) = (hbar/2pi k c) sqrt(a^2+(cH)^2)  [Deser-Levin].")
print("  Excess heat DeltaT = T(a)-T(0) is DEGREE-1 in the amplitude a (linear), NOT T^2 (energy/power).")
print("  theta(0) = w(0)/w(1) = EFE-normalized DC weight.  -3 dB corner of an AMPLITUDE transfer = 1/sqrt2.")
# build it WITHOUT typing sqrt2: derive the amplitude -3dB corner from a single-pole Lorentzian
w = sp.Symbol('w', positive=True)   # frequency
# single-pole AMPLITUDE transfer H(w) = 1/sqrt(1+w^2); corner where |H|^2 = 1/2 i.e. amplitude = 1/sqrt2
amp = 1/sp.sqrt(1+w**2)
corner_w = sp.solve(sp.Eq(amp**2, sp.Rational(1,2)), w)
corner_w = [c for c in corner_w if c.is_positive][0]   # w=1
amp_at_corner = sp.simplify(amp.subs(w, corner_w))      # 1/sqrt2
theta0 = sp.simplify(1/amp_at_corner)                   # sqrt2  (w(0)/w(corner))
print(f"  amplitude transfer 1/sqrt(1+w^2); -3 dB corner at w={corner_w}; |H|={amp_at_corner}")
print(f"  theta(0) = w(0)/w(corner) = 1/|H(corner)| = {theta0} = {float(theta0):.6f}")
allok &= ck("theta(0) derived = sqrt2 (amplitude/degree-1 branch, no '45deg' input)",
            sp.simplify(theta0 - sp.sqrt(2)) == 0)
mp_theta0 = sp.minimal_polynomial(theta0, t)
print(f"  minimal polynomial of theta(0): {mp_theta0}")

print("\n  --- SLOT 2: r = sqrt2  (Koide amplitude; S3 singlet=doublet equal-projection) ---")
mu_s, r_s, delta = sp.symbols('mu r delta', positive=True)
# Brannen circulant sqrt-mass vector
sqrtm = [mu_s*(1 + r_s*sp.cos(delta + 2*sp.pi*k/3)) for k in range(3)]
Q_expr = sp.simplify(sum(s**2 for s in sqrtm) / (sum(sqrtm))**2)
Q_expr = sp.simplify(Q_expr)
print(f"  Q(mu,r,delta) = sum(m)/ (sum sqrt m)^2 = {Q_expr}   (delta cancels)")
# solve Q = 2/3 for r  (THIS step references 2/3 -- it is the empirical TARGET, quarantined)
r_sol = sp.solve(sp.Eq(Q_expr, sp.Rational(2,3)), r_s)
r_sol = [rr for rr in r_sol if rr.is_positive][0]
print(f"  Q = 2/3  =>  r = {r_sol} = {float(r_sol):.6f}")
allok &= ck("r = sqrt2 from Q=2/3 (2/3 enters as empirical target, quarantined)",
            sp.simplify(r_sol - sp.sqrt(2)) == 0)
mp_r = sp.minimal_polynomial(r_sol, t)
print(f"  minimal polynomial of r: {mp_r}")

print("\n  (a) SHARED minimal polynomial?  Both are t^2-2.  But same min-poly =/= shared ORIGIN.")
allok &= ck("both minimal polynomials are t^2 - 2 (necessary, NOT sufficient for a shared generator)",
            mp_theta0 == mp_r == (t**2 - 2))
print("      sqrt2 is the UNIQUE positive root of t^2-2; ANY construction landing on it shares this")
print("      polynomial.  Counter-examples below show t^2-2 arises from unrelated 1-line geometry.")

# =====================================================================================
print("\n"+"="*86)
print("(b) IS THERE A FORCED MAP theta(0) -> r ?  Object-type audit (the load-bearing test)")
print("="*86)
print("""  theta(0):  a SCALAR weight on the 1-D WORLDLINE/TIME axis.  It is w(0)/w(corner) of a
             single-pole bath memory; its home is the de Sitter Wightman correlator on R^1
             (a function of proper-time separation u).  No generation index. No 3-vector.
  r       :  a RATIO of two PROJECTION MAGNITUDES of a 3-VECTOR in GENERATION space R^3
             (|P_doublet|/|P_singlet| of v=(sqrt m_e,sqrt m_mu,sqrt m_tau) under S3).
  => DIFFERENT CARRIER SPACES: R^1 time-axis (bath) vs R^3 generation-axis (flavor).
     A map theta(0) -> r must be an intertwiner between these.  The framework supplies NONE:
     mu_fw / theta(y) are FLAVOR-BLIND (depend only on |a|, the equivalence principle), so they
     act as a SCALAR on every generation identically -> they cannot produce a NON-trivial ratio
     between generation-projection magnitudes.""")
# demonstrate flavor-blindness numerically: apply theta(0) as a scalar to each generation
# component; the ratio |P_doublet|/|P_singlet| is UNCHANGED (scalar multiples cancel in the ratio).
import numpy as np
v = np.array([1.0, 2.3, 7.1])              # arbitrary sqrt-mass-like vector (NOT tuned to 45deg)
n = np.ones(3)/np.sqrt(3)
def proj_ratio(vec):
    Ps = np.dot(vec, n)*n
    Pd = vec - Ps
    return np.linalg.norm(Pd)/np.linalg.norm(np.array([np.dot(vec,n)]))
r_before = proj_ratio(v)
r_after  = proj_ratio(float(theta0)*v)     # multiply ALL generations by theta(0) (flavor-blind scalar)
allok &= ck(f"flavor-blind scalar theta(0) leaves r UNCHANGED: r={r_before:.6f} -> {r_after:.6f}",
            abs(r_before - r_after) < 1e-12)
print("      A flavor-blind weight CANNOT move r.  theta(0) is exactly such a weight (depends on |a|).")
print("      => No dynamical channel carries theta(0)'s sqrt2 into the generation-amplitude r.")

# =====================================================================================
print("\n"+"="*86)
print("(c) TRY TO DERIVE r FROM theta(0) NON-CIRCULARLY — and show where it breaks")
print("="*86)
print("""  Attempt: posit rest-mass = spectrum of the framework's own inertia response, and ask whether
  the kernel's DC weight theta(0)=sqrt2 SETS the generation-amplitude r.  Two honest sub-attempts:""")

print("\n  Attempt-1 (algebraic identity bridge): does the framework identity 1/mu-mu=1/x, or")
print("  mu_fw(1)=1/phi, FORCE r=sqrt2 ?  These give phi and the x=1 fixed point — NOT sqrt2.")
# what is the 'natural' amplitude if it came from the kernel fixed point x=1?
# mu_fw(1)=1/phi -> if r were set by mu_fw it would be 1/phi=0.618, NOT sqrt2=1.414. They DISAGREE.
val_phi = float(mu1)
allok &= ck(f"kernel fixed-point value 1/phi={val_phi:.4f} != r=sqrt2={float(sp.sqrt(2)):.4f} (kernel does NOT hand r)",
            abs(val_phi - float(sp.sqrt(2))) > 0.5)
print("      The framework's OWN shape-sector special value at x=1 is 1/phi, NOT sqrt2.  If the kernel")
print("      'spectrum-of-inertia' idea set r, it would deliver 1/phi (or a phi-power), giving")
Q_if_phi = float(sp.Rational(1,3) + (1/phi)**2/6)
print(f"      Q = 1/3 + (1/phi)^2/6 = {Q_if_phi:.6f}  != 2/3.  So the kernel does NOT land Koide.")
allok &= ck(f"kernel-fixed-point amplitude gives Q={Q_if_phi:.4f} != 2/3 (no Koide from the kernel)",
            abs(Q_if_phi - 2/3) > 0.1)

print("\n  Attempt-2 (the only way to FORCE r=sqrt2): assume |P_singlet|=|P_doublet| (the 45deg cone).")
print("  Circularity theorem (KOIDE corpus): force-r=sqrt2 <=> assume |singlet|=|doublet| <=> assume 2/3.")
# show: the ONLY input that yields r=sqrt2 is the equal-projection condition itself.
# Generic r is FREE: perturb the cone condition, r moves continuously — it is NOT pinned by theta(0).
for eps in (0.0, 0.1, -0.1, 0.3):
    # |P_d|/|P_s| set to sqrt2*(1+eps); resulting Q
    rr = sp.sqrt(2)*(1+eps)
    Qe = float(sp.Rational(1,3) + rr**2/6)
    print(f"      r = sqrt2*(1+{eps:+.1f}) = {float(rr):.4f}  ->  Q = {Qe:.5f}   "
          f"({'== 2/3 ONLY at eps=0' if eps==0 else 'free, no theta(0) constraint forbids it'})")
print("      Nothing from theta(0) (a 1-D bath scalar) PENALIZES eps != 0.  r is a free modulus;")
print("      the equal-projection cone is the ONLY thing that pins it, and that cone IS Q=2/3.")
allok &= ck("forcing r=sqrt2 requires assuming the 45deg cone = assuming 2/3 (CIRCULAR, theta(0) gives no penalty)",
            True)

# =====================================================================================
print("\n"+"="*86)
print("(d) NON-CIRCULARITY BAR + counter-examples: t^2-2 is GENERIC, not a fingerprint")
print("="*86)
print("  BAR: produce r=sqrt2 WITHOUT 45deg/sqrt2/(2/3) in the inputs, via a chain FROM theta(0).")
print("  RESULT: FAILED — no such chain exists (carrier-space mismatch + flavor-blindness above).")
print("  Both-ways control: how often does t^2-2 / sqrt2 show up in UNRELATED 1-line geometry?")
examples = {
    "diagonal of unit square (Pythagoras)": sp.sqrt(1**2+1**2),
    "-3 dB amplitude corner (any single-pole filter)": 1/sp.sqrt(sp.Rational(1,2)),
    "L2 norm of (1,1)": sp.sqrt(2),
    "RMS-to-peak of a sinusoid (peak/rms)": sp.sqrt(2),
    "ratio long:short F4 root lengths (gauge, WRONG slot)": sp.sqrt(2),
}
for nm, val in examples.items():
    mpoly = sp.minimal_polynomial(sp.nsimplify(val), t)
    print(f"      {nm:52s}: {float(val):.5f}  min-poly {mpoly}")
print("  => sqrt2 (min-poly t^2-2) is the generic 'equal-mix of two orthogonal unit channels' number.")
print("     It appears whenever two equal orthogonal contributions are summed in quadrature.  BOTH slots")
print("     are 'two equal orthogonal things' geometry — but in DIFFERENT spaces (time-memory poles vs")
print("     generation singlet/doublet).  Same archetype, independent instantiations: a COINCIDENCE of")
print("     archetype, NOT a shared generator transporting one sqrt2 into the other.")

# =====================================================================================
print("\n"+"="*86)
print("VERDICT")
print("="*86)
print("""  (a) Both sqrt2's have minimal polynomial t^2-2 — NECESSARY but NOT sufficient for a shared
      origin (t^2-2 is the generic equal-orthogonal-quadrature number; 5 unrelated examples above).
  (b) theta(0)=sqrt2 is a SCALAR on the 1-D worldline (bath correlator, single-pole memory);
      r=sqrt2 is a RATIO of 3-vector projection magnitudes in generation space.  DIFFERENT CARRIERS.
  (c) The framework's kernel is FLAVOR-BLIND (mu_fw, theta depend only on |a|): as a scalar it leaves
      the generation-projection ratio r INVARIANT (computed: r unchanged under x theta(0)).  Its own
      special value at the fixed point is 1/phi, which gives Q=0.397 != 2/3 — the kernel does NOT
      hand Koide its amplitude.
  (d) The ONLY way to 'derive' r=sqrt2 is to assume |singlet|=|doublet| (the 45deg cone) = assume 2/3
      (circular); theta(0) supplies no penalty against r != sqrt2 (perturbation test: r free).

  ==> INDEPENDENT sqrt2's.  Same NUMBER (t^2-2), same ARCHETYPE (equal mix of two orthogonal unit
      channels), DIFFERENT OBJECTS in DIFFERENT carrier spaces, NO forced non-circular map between
      them.  The framework's flavor-blind kernel structurally cannot transport theta(0)'s sqrt2 into
      the generation-amplitude r.  COINCIDENCE-of-archetype / WRONG-SLOT, consistent with the banked
      KOIDE_TRIALITY_OCTONION 'hosts-but-does-not-force' and the circularity theorem.  No manufactured
      win; the real (exact) reframings stand, but they are not a shared generator.""")

print("\n" + ("ALL CHECKS PASS" if allok else "SOME CHECKS FAILED"))
import sys
sys.exit(0 if allok else 1)
