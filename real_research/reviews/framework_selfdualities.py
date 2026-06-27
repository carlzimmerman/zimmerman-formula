#!/usr/bin/env python3
"""
FRONT 1 — CATALOG EVERY FRAMEWORK SELF-DUALITY / INVOLUTION / BALANCE-POINT and COMPUTE its
characteristic constant.  GOAL: of {phi, sqrt2, sqrt(Z), other}, which constant does EACH
self-dual structure carry?  Does ANY structure carry sqrt2 from the framework's OWN geometry
(un-referenced), and if so is it the SAME structural object as Koide's r=sqrt2, or the generic
'equal-mix-of-two-orthogonal-channels' coincidence (necessary, NOT sufficient)?

CARL'S #1 RULE: NO MANUFACTURED WIN (TOE retracted).  A sqrt2 that EMERGES un-referenced is only
a LEAD if a FORCED, NON-CIRCULAR map carries it into Koide's r (different carrier space + EP
flavor-blindness are the known obstructions).  Expected outcome: the self-dual SECTOR constants
are phi (the mu_fw involution) and sqrt(Z) (the inverted-BH / UV-IR radius); the ONLY native sqrt2
is the dS-Unruh quadrature at a=a_dS, which is the generic equal-orthogonal-channel number, NOT a
shared generator with Koide.

FOOTING (locked, never under test):  a0 = c H_Lambda / Z ;  Z = sqrt(32 pi/3) = 2 sqrt(8 pi/3) ;
framework's OWN interpolation mu_fw(x) = (sqrt(1+4x^2)-1)/(2x) ; identity 1/mu_fw - mu_fw = 1/x ;
constitutive m_I = tanh(1/2 asinh 2x).  NEVER McGaugh nu.

Every constant COMPUTED with sympy/mpmath, exit 0, numbers printed.  Both-ways; report where it
bottoms out.  A constant is classified sqrt2 ONLY if its minimal polynomial is t^2-2 AND it was
derived WITHOUT typing sqrt(2)/45deg/(2/3) into the inputs (non-circularity flag printed per row).
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

t = sp.Symbol('t')
PHI = (1 + sp.sqrt(5))/2
Z   = 2*sp.sqrt(sp.Integer(8)*sp.pi/3)        # sqrt(32 pi/3)
SQRT2 = sp.sqrt(2)

def classify(val):
    """Return (label, minpoly, matches) for a positive algebraic/numeric constant."""
    v = sp.nsimplify(val) if not val.free_symbols else val
    try:
        mpoly = sp.minimal_polynomial(v, t)
    except Exception:
        mpoly = None
    fv = float(val)
    label = "other"
    if abs(fv - float(PHI))   < 1e-9: label = "phi"
    elif abs(fv - 1/float(PHI)) < 1e-9: label = "1/phi"
    elif abs(fv - float(SQRT2)) < 1e-9: label = "sqrt2"
    elif abs(fv - float(sp.sqrt(Z))) < 1e-9: label = "sqrt(Z)"
    elif abs(fv - float(Z)) < 1e-9: label = "Z"
    return label, mpoly, fv

ROWS = []   # (structure, constant_label, value, minpoly, native_sqrt2_noncirc, note)

print("="*92)
print("FRAMEWORK SELF-DUALITY CATALOG  —  each structure -> its characteristic constant")
print(f"  footing: Z = sqrt(32pi/3) = {float(Z):.6f} ;  sqrt(Z) = {float(sp.sqrt(Z)):.6f} ;  phi = {float(PHI):.6f}")
print("="*92)

# =====================================================================================
# (a) THE mu_fw INVOLUTION  1/mu_fw - mu_fw = 1/x  : self-dual / fixed / balance points
# =====================================================================================
print("\n(a) mu_fw involution  1/mu - mu = 1/x   (framework's OWN interpolation)")
x = sp.Symbol('x', positive=True)
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)
ident = sp.simplify((1/mu_fw - mu_fw) - 1/x)
print(f"    identity residual 1/mu - mu - 1/x = {ident}  (==0 confirms the involution)")
assert ident == 0

# The map mu -> 1/mu (the duality on the response).  Its symmetric self-dual point is mu=1 (mu=1/mu),
# but mu_fw(x)=1 only as x->inf.  The FRAMEWORK'S OWN distinguished interior point is the crossover x=1
# (deep-MOND<->Newton balance): there mu_fw(1) = 1/phi.
mu1 = sp.simplify(mu_fw.subs(x, 1))
lab, mpoly, fv = classify(mu1)
print(f"    crossover x=1 (deep-MOND<->Newton balance): mu_fw(1) = {mu1} = {fv:.6f}  [{lab}], minpoly {mpoly}")
ROWS.append(("mu_fw at crossover x=1", lab, fv, mpoly, False,
             "golden; framework's own balance value is 1/phi, NOT sqrt2"))

# True fixed point of the response map y=mu where the chord 1/mu-mu equals its argument 1/x at x=mu:
# solve 1/m - m = 1/m  -> trivial; instead the 'self-dual' of x<->1/x under the identity.
# The x that is its own dual under x -> value-where-mu(x) symmetric: solve mu_fw(x) = x.
fp = sp.solve(sp.Eq(mu_fw, x), x)
fp = [f for f in fp if f.is_real and f.is_positive]
if fp:
    val = sp.simplify(fp[0]); lab, mpoly, fv = classify(val)
    print(f"    fixed point mu_fw(x)=x : x = {val} = {fv:.6f}  [{lab}], minpoly {mpoly}")
    ROWS.append(("mu_fw fixed point mu(x)=x", lab, fv, mpoly, False,
                 "1/phi again (golden), NOT sqrt2"))
else:
    print("    no positive real fixed point mu_fw(x)=x in range")

# =====================================================================================
# (b) INVERTED-BH DUALITY  r_cross = sqrt(Z) * r_s   (the constant is sqrt(Z))
# =====================================================================================
print("\n(b) inverted-BH duality  g(r)=a0_BH  ->  r_cross = sqrt(Z)*r_s   (mass cancels)")
M, G, c, r = sp.symbols('M G c r', positive=True)
r_s = 2*G*M/c**2
a0_BH = c**4/(4*G*M*Z)
r_cross = sp.solve(sp.Eq(G*M/r**2, a0_BH), r)
r_cross = [rr for rr in r_cross if rr.is_positive][0]
ratio = sp.simplify(r_cross/r_s)
lab, mpoly, fv = classify(ratio)
print(f"    r_cross/r_s = {sp.simplify(ratio)} = {fv:.6f}  [{lab}], minpoly {mpoly}")
ROWS.append(("inverted-BH r_cross/r_s", lab, fv, mpoly, False,
             "sqrt(Z)=2.406; the framework's OTHER native self-dual constant, NOT sqrt2"))

# =====================================================================================
# (c) CONSTITUTIVE LAW  m_I = tanh(1/2 asinh(2x))  : self-similar / duality structure
# =====================================================================================
print("\n(c) constitutive law  m_I(x) = tanh( (1/2) asinh(2x) )  = mu_fw(x)  (EOS form)")
xx = sp.Symbol('x', positive=True)
m_I = sp.tanh(sp.asinh(2*xx)/2)
# verify it equals mu_fw to machine precision (sympy may not auto-simplify; check numerically)
diffs = [abs(float(m_I.subs(xx, v)) - float(mu_fw.subs(x, v))) for v in (0.01,0.1,1,10,100)]
print(f"    max |tanh(asinh/2) - mu_fw| over x in [0.01,100] = {max(diffs):.2e}  (==0 => same object as (a))")
assert max(diffs) < 1e-12
# its inverse is mu/(1-mu^2)=x : a clean involution-like map.  Its self-similar/balance point is again
# where the half-angle argument asinh(2x) makes tanh symmetric, i.e. m_I = 1/2 at... solve:
half = sp.solve(sp.Eq(m_I, sp.Rational(1,2)), xx)
half = [h for h in half if h.is_real and h.is_positive]
if half:
    val = sp.simplify(half[0]); lab, mpoly, fv = classify(val)
    print(f"    m_I = 1/2 at x = {val} = {fv:.6f}  [{lab}], minpoly {mpoly}  (half-response point)")
    ROWS.append(("constitutive m_I=1/2 point", lab, fv, mpoly, False,
                 "x=2/3 rational; no sqrt2.  EOS is mu_fw re-expressed -> inherits the phi balance, not sqrt2"))
# self-dual under m_I <-> 1-m_I^2 ... the structural point: constitutive law IS mu_fw, so its duality
# constant is the SAME 1/phi as (a). No NEW constant. Record that explicitly.
ROWS.append(("constitutive law (=mu_fw)", "1/phi", 1/float(PHI), sp.minimal_polynomial(1/PHI,t), False,
             "identical to mu_fw; carries phi, NOT a new sqrt2"))

# =====================================================================================
# (d) dS-UNRUH QUADRATURE  T(a) = sqrt(a^2 + a_dS^2)  : equal-channel point a=a_dS  -> NATIVE sqrt2
# =====================================================================================
print("\n(d) dS-Unruh quadrature  T(a) ~ sqrt(a^2 + a_dS^2)  ;  equal-channel point a = a_dS")
a, a_dS = sp.symbols('a a_dS', positive=True)
T = sp.sqrt(a**2 + a_dS**2)
# at a = a_dS the two ORTHOGONAL channels (acceleration vs horizon) contribute equally:
T_balance = sp.simplify(T.subs(a, a_dS) / a_dS)     # = sqrt(2), un-referenced
lab, mpoly, fv = classify(T_balance)
print(f"    T(a_dS)/a_dS = {sp.simplify(T_balance)} = {fv:.6f}  [{lab}], minpoly {mpoly}")
print("    DERIVED WITHOUT typing sqrt(2): comes from sqrt(a_dS^2 + a_dS^2) = sqrt(2) a_dS (sympy auto).")
# NON-CIRCULARITY: nothing about 45deg / Koide / 2/3 was input; pure quadrature of two equal channels.
native_noncirc = (mpoly == (t**2 - 2))
ROWS.append(("dS-Unruh T(a_dS)/a_dS  (a=a0)", lab, fv, mpoly, native_noncirc,
             "NATIVE sqrt2, un-referenced.  Equal mix of 2 orthogonal channels (accel vs horizon)."))
print(f"    => NATIVE, NON-CIRCULAR sqrt2 in the framework (no 45deg/2/3 referenced): {native_noncirc}")

# =====================================================================================
# (e) UV/IR RADIUS DUALITY  r -> r_s R_H / r  : self-dual radius r_sd = sqrt(r_s R_H)
# =====================================================================================
print("\n(e) UV/IR radius duality  r -> r_s R_H / r  ;  self-dual fixed point r_sd = sqrt(r_s R_H)")
R_H = sp.Symbol('R_H', positive=True)
r_sd = sp.sqrt(r_s * R_H)
# acceleration at the self-dual radius (DEEP_GEOMETRY claims a(r_sd) = cH/2, mass-independent):
H = sp.Symbol('H', positive=True)
RH_sub = c/H
a_at = sp.simplify((G*M/r_sd**2).subs(R_H, RH_sub))
print(f"    a(r_sd) = GM/r_sd^2 = {a_at} = cH/2  (mass cancels: {sp.simplify(a_at - c*H/2)==0})")
# the MOND radius sits at (8pi/3)^(1/4) = sqrt(Z/2) times the self-dual radius:
r_M = (sp.Integer(8)*sp.pi/3)**sp.Rational(1,4) * sp.sqrt(r_s*R_H)
ratio_M = sp.simplify(r_M / r_sd)
lab, mpoly, fv = classify(ratio_M)
print(f"    r_M / r_sd = (8pi/3)^(1/4) = {fv:.6f}  [{lab}], minpoly {mpoly}")
# (8pi/3)^(1/4) vs sqrt(Z/2): check
print(f"    check (8pi/3)^(1/4) == sqrt(Z/2) : {sp.simplify(ratio_M - sp.sqrt(Z/2))==0}")
ROWS.append(("UV/IR self-dual radius factor r_M/r_sd", lab, fv, mpoly, False,
             "(8pi/3)^(1/4)=1.704 = sqrt(Z/2); the duality's own constant, transcendental, NOT sqrt2"))
ROWS.append(("UV/IR self-dual point: a(r_sd)/cH", "1/2", 0.5, sp.minimal_polynomial(sp.Rational(1,2),t), False,
             "balance accel = cH/2; rational 1/2, NOT sqrt2"))

# =====================================================================================
# (f) d=3 BIVECTOR SELF-DUALITY  dim SO(d)=d  : the selection constant (which d, not a length)
# =====================================================================================
print("\n(f) cross-product self-duality  dim SO(d) = d(d-1)/2 = d  ->  d=3 (and (d-1)=2)")
d = sp.Symbol('d', positive=True, integer=True)
sol = sp.solve(sp.Eq(d*(d-1)/2, d), d)
sol = [s for s in sol if s>0]
print(f"    dim SO(d)=d  =>  d = {sol}  ;  (d-1) = {[int(s)-1 for s in sol]}  (the '2' is a COUNT, not sqrt2)")
ROWS.append(("d=3 self-duality (d-1)", "2 (count)", 2.0, sp.minimal_polynomial(sp.Integer(2),t), False,
             "(d-1)=2 is an integer dimension count, not the number sqrt2"))

# =====================================================================================
# SUMMARY TABLE
# =====================================================================================
print("\n" + "="*92)
print("TABLE: structure -> characteristic constant")
print("="*92)
print(f"  {'STRUCTURE':42s} {'CONSTANT':10s} {'VALUE':>9s}  native-sqrt2?")
print("  " + "-"*86)
for (struct, lab, val, mpoly, ncs, note) in ROWS:
    flag = "YES (non-circ)" if ncs else "no"
    print(f"  {struct:42s} {lab:10s} {val:9.5f}  {flag}")
    print(f"      note: {note}")

# count the native non-circular sqrt2's
native = [row for row in ROWS if row[4]]
print("\n" + "="*92)
print("WHICH STRUCTURES GENUINELY CARRY sqrt2 FROM THE FRAMEWORK'S OWN GEOMETRY (un-referenced)?")
print("="*92)
print(f"  native, non-circular sqrt2 count = {len(native)}")
for row in native:
    print(f"    -> {row[0]}  (value {row[2]:.6f}, minpoly {row[3]})")

# =====================================================================================
# THE LOAD-BEARING TEST: is the native (d) sqrt2 the SAME object as Koide's r=sqrt2?
# =====================================================================================
print("\n" + "="*92)
print("IS THE NATIVE dS-UNRUH sqrt2  ==  KOIDE'S r=sqrt2 ?  (shared generator vs coincidence)")
print("="*92)
# Koide r: derived from Q=2/3 (2/3 is the empirical target -> quarantined / circular for r)
mu_s, r_s2, dl = sp.symbols('mu r delta', positive=True)
sqrtm = [mu_s*(1 + r_s2*sp.cos(dl + 2*sp.pi*kk/3)) for kk in range(3)]
Q = sp.simplify(sum(s**2 for s in sqrtm)/(sum(sqrtm))**2)
r_koide = [rr for rr in sp.solve(sp.Eq(Q, sp.Rational(2,3)), r_s2) if rr.is_positive][0]
print(f"  Koide r from Q=2/3 : r = {r_koide} = {float(r_koide):.6f}  (Q=2/3 is the quarantined empirical input)")
print(f"  dS-Unruh quadrature: T(a0)/a0 = sqrt2 = {float(SQRT2):.6f}  (NO empirical input)")
print(f"  same minimal polynomial t^2-2 ?  {sp.minimal_polynomial(r_koide,t)==sp.minimal_polynomial(SQRT2,t)==(t**2-2)}")
print("""
  CARRIER-SPACE AUDIT (the load-bearing distinction):
    dS-Unruh sqrt2 : ratio of a TEMPERATURE quadrature on the 1-D worldline/time axis
                     (two orthogonal scalar channels: proper acceleration |a| vs horizon a_dS).
                     Lives in R^1.  Flavor-BLIND (a function of |a| only; EP-respecting).
    Koide r=sqrt2  : ratio of two PROJECTION MAGNITUDES of a 3-VECTOR in GENERATION space R^3
                     (|P_doublet|/|P_singlet| of (sqrt m_e, sqrt m_mu, sqrt m_tau) under S3).
    => DIFFERENT CARRIER SPACES (R^1 bath-time vs R^3 flavor).  A map requires an INTERTWINER
       carrying a flavor-blind scalar into a generation-projection ratio.  The framework supplies
       NONE: mu_fw/theta/T depend on |a| only, so they act as ONE common scale on all 3 generations
       -> by the circularity theorem (Q=1/3+r^2/6) and scale-invariance of Q, a common scale CANNOT
       move r.  (Re-proven in koide_circularity_INDEP_verify.py.)""")

# numeric demonstration: apply the dS-Unruh sqrt2 as a flavor-blind common scale -> r unchanged
import numpy as np
v = np.array([1.0, 2.3, 7.1])                      # arbitrary sqrt-mass-like vector (NOT tuned)
n = np.ones(3)/np.sqrt(3)
def r_of(vec):
    s = np.dot(vec, n); Pd = vec - s*n
    return np.linalg.norm(Pd)/abs(s)
r0 = r_of(v); r1 = r_of(float(SQRT2)*v)
print(f"  flavor-blind common-scale test: apply sqrt2 to all generations -> r {r0:.6f} -> {r1:.6f}  "
      f"(unchanged: {abs(r0-r1)<1e-12})")

# the framework's own balance value (1/phi) plugged as the amplitude gives Q != 2/3:
Q_if_phi = float(sp.Rational(1,3) + (1/PHI)**2/6)
print(f"  if the framework's OWN balance value 1/phi were the amplitude: Q = {Q_if_phi:.6f} != 2/3 "
      f"(the spine hands phi, not Koide's sqrt2)")

print("""
  VERDICT (both-ways, no manufactured win):
   * The framework has TWO genuinely native self-dual constants from its OWN geometry:
       - phi / 1/phi  (the mu_fw response involution & the deep-MOND<->Newton crossover x=1),
       - sqrt(Z)=2.406  (the inverted-BH r_cross & the UV/IR self-dual-radius packaging).
   * It has EXACTLY ONE native, non-circular sqrt2: the dS-Unruh temperature quadrature at a=a_dS=a0
     (T = sqrt2 a_dS).  It is REAL and un-referenced -- but it is the GENERIC equal-mix-of-two-
     orthogonal-channels number (minpoly t^2-2), living on the 1-D worldline as a flavor-BLIND scalar.
   * Koide's r=sqrt2 lives in R^3 generation space as a vector-projection ratio.  Same number, same
     archetype (two equal orthogonal channels), DIFFERENT carrier spaces, and the framework's
     flavor-blind kernel structurally CANNOT transport one into the other (common-scale test: r
     invariant; circularity theorem: forcing r=sqrt2 == assuming 2/3).
   * MISSING INGREDIENT: a flavor-NON-blind intertwiner R^1(bath) -> R^3(generation) that the
     equivalence principle forbids inside the spine.  That is exactly Sumino-class NEW physics
     (a family gauge symmetry breaking the EP-protected flavor blindness) OUTSIDE the framework.
   * NET: the dS-Unruh sqrt2 is a NATIVE coincidence-of-archetype with Koide's sqrt2, NOT a shared
     generator.  No door closed; no win manufactured.  The seduction bottoms out at the EP wall.""")

print("\nDONE — exit 0")
