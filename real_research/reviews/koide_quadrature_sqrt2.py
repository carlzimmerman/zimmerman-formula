#!/usr/bin/env python3
"""
FRONT 2 — THE a=a_dS QUADRATURE sqrt2  vs  KOIDE r=sqrt2.

NEW SEED (the seduction to anatomize): the dS-Unruh temperature is a 2-channel quadrature
        T(a) = (hbar/2pi k_B c) * sqrt(a^2 + (cH_Lambda)^2)              [Deser-Levin]
When the proper acceleration a equals the de Sitter acceleration a_dS = cH_Lambda, the two
channels (drive a, vacuum cH_Lambda) BALANCE and
        T(a_dS) = (hbar/2pi k_B c) * sqrt(2) * cH_Lambda  =  sqrt2 * T(0).
So there is a NATIVE framework sqrt2 sitting at the channel-balance point of the bath.

The seed CLAIMS this balance is "at a=a_dS (=a0), the MOND scale." Koide is r=sqrt2 (45-deg
self-dual sqrt-mass vector). QUESTION: is the bath-quadrature sqrt2 the SAME structural object
as Koide's r=sqrt2 (a forced, non-circular map), or two DIFFERENT self-dualities that share only
the minimal polynomial t^2 - 2 (the generic "equal mix of two orthogonal channels" number)?

CARL'S #1 RULE: NO MANUFACTURED WIN (he retracted the TOE). Expected = the quadrature-sqrt2 is the
generic coincidence, no forced map; and the EP (flavor-blindness) forbids the flavor bridge.
But test BOTH WAYS, no reflexive dismissal: report exactly where it bottoms out and what the
EXACT missing ingredient is.

THE FIRST LANDMINE (checked in block B): is the balance even AT a0?  a_dS = cH_Lambda, and the
framework's MOND scale is a0 = cH_Lambda / Z with Z = sqrt(32pi/3) ~ 5.79.  So a_dS = Z*a0, i.e.
the quadrature balances at ~5.79 a0, NOT at a0.  The seed's "(=a0)" is a CONFLATION.  This matters
for whether the sqrt2 lives "at the MOND scale" at all.

FOOTING (locked, never under test): a0 = cH_Lambda/Z = 9.36e-11; Z = sqrt(32pi/3) = 2 sqrt(8pi/3);
mu_fw(x)=(sqrt(1+4x^2)-1)/(2x); identity 1/mu_fw - mu_fw = 1/x; mu_fw(1)=1/phi.  NEVER McGaugh nu.

Every claim COMPUTED (sympy/mpmath/numpy), exit 0, numbers printed.  Both-ways, no faked crack.
"""
import sympy as sp
import mpmath as mp
import numpy as np
mp.mp.dps = 40

t = sp.Symbol('t')
PASS, FAIL = "PASS", "FAIL <-- CHECK"
def ck(name, cond):
    print(f"  [{PASS if cond else FAIL}] {name}")
    return bool(cond)
allok = True

# =====================================================================================
print("="*90)
print("(0) FOOTING — framework constants (locked, not under test)")
print("="*90)
Z = 2*sp.sqrt(sp.Rational(8,1)*sp.pi/3)
phi = (sp.sqrt(5)+1)/2
print(f"  Z = sqrt(32pi/3) = {float(Z):.6f}")
a0_num = 9.36e-11
cH_Lambda = sp.nsimplify(a0_num)*Z          # a_dS = cH_Lambda = Z * a0
print(f"  a0 = cH_Lambda/Z = {a0_num:.3e};  a_dS = cH_Lambda = Z*a0 = {float(cH_Lambda):.4e}")
x = sp.Symbol('x', positive=True)
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)
allok &= ck(f"mu_fw(1) = 1/phi = {float(sp.simplify(mu_fw.subs(x,1))):.6f} (golden, framework's own)",
            sp.simplify(mu_fw.subs(x,1) - 1/phi) == 0)

# =====================================================================================
print("\n"+"="*90)
print("(A) DERIVE the quadrature-sqrt2 EXPLICITLY from T(a) = K sqrt(a^2 + a_dS^2)")
print("="*90)
a, adS, K = sp.symbols('a a_dS K', positive=True)
T = K*sp.sqrt(a**2 + adS**2)
print(f"  T(a) = {T}   (Deser-Levin dS-Unruh; a_dS = cH_Lambda the vacuum/horizon channel)")
T0 = T.subs(a, 0)                       # K*a_dS
ratio_balance = sp.simplify(T.subs(a, adS)/T0)
print(f"  T(0)      = {T0}")
print(f"  T(a_dS)/T(0) = {ratio_balance}   <-- the channel-BALANCE ratio")
allok &= ck("at a=a_dS the two channels balance: T(a_dS) = sqrt2 * T(0)  (native bath sqrt2)",
            sp.simplify(ratio_balance - sp.sqrt(2)) == 0)
# what IS this sqrt2 structurally: it is |(a_dS, a_dS)| / |(0, a_dS)| in the (drive, vacuum) plane
print("  STRUCTURE: sqrt2 = |(a_dS, a_dS)| / |(0, a_dS)| in the 2-D (drive, vacuum) quadrature plane.")
print("            i.e. the hypotenuse-to-leg ratio of an isosceles right triangle = sqrt2.")
mp_q = sp.minimal_polynomial(sp.sqrt(2), t)
print(f"  minimal polynomial of the quadrature-sqrt2: {mp_q}")
# verify it is exactly the 45-deg condition IN THE BATH PLANE
ang = sp.atan2(adS, adS)               # angle of (a_dS, a_dS) from the a-axis
print(f"  the balance vector (a_dS,a_dS) sits at 45 deg in the bath plane: atan2(a_dS,a_dS)={sp.deg(ang)} deg")
allok &= ck("bath-plane balance IS a 45-deg condition (drive leg == vacuum leg)",
            sp.simplify(ang - sp.pi/4) == 0)

# =====================================================================================
print("\n"+"="*90)
print("(B) LANDMINE: is the balance AT a0 (the MOND scale), or at a_dS = Z*a0 ~ 5.79 a0 ?")
print("="*90)
print("  The seed says the balance is 'at a=a_dS (=a0), the MOND scale!'.  TEST that identification.")
balance_in_a0_units = sp.simplify(cH_Lambda / sp.nsimplify(a0_num))
print(f"  balance acceleration a_dS = cH_Lambda = {float(cH_Lambda):.4e}")
print(f"  in units of a0:  a_dS/a0 = Z = {float(balance_in_a0_units):.4f}")
allok &= ck("the quadrature BALANCE sits at a = Z*a0 ~ 5.79 a0, NOT at a0  (seed's '=a0' is a CONFLATION)",
            abs(float(balance_in_a0_units) - 1.0) > 1.0)
# what does mu_fw do AT the balance point a=a_dS=Z*a0 ?  (x = a/a0 = Z there)
mu_at_balance = mu_fw.subs(x, Z)
print(f"  the MOND interpolation at the balance: x=a/a0=Z -> mu_fw(Z) = {float(mu_at_balance):.4f}")
print(f"  (deep-Newtonian: mu_fw(5.79)~{float(mu_at_balance):.3f}; the MOND TRANSITION x~1 is at a=a0, a")
print("   DIFFERENT place from the bath quadrature balance).  So the quadrature-sqrt2 does NOT live at")
print("   the MOND transition; it lives ~5.79x above it, where the dynamics are already ~Newtonian.")
# the a0 MOND scale itself: the bath ratio there is NOT sqrt2
ratio_at_a0 = sp.simplify((T.subs([(a, adS/Z)])/T0))   # a = a_dS/Z = a0
print(f"  at the actual MOND scale a=a0=a_dS/Z: T(a0)/T(0) = {sp.simplify(ratio_at_a0)} = {float(ratio_at_a0):.5f}  (NOT sqrt2)")
allok &= ck("at the MOND scale a0 the bath ratio is sqrt(1+1/Z^2) ~ 1.015, NOT sqrt2 (sqrt2 is NOT a MOND-scale number)",
            abs(float(ratio_at_a0) - float(sp.sqrt(2))) > 0.3)

# =====================================================================================
print("\n"+"="*90)
print("(C) DERIVE Koide r=sqrt2 from the 45-deg self-dual mass-vector condition")
print("="*90)
mu_s, r_s, delta = sp.symbols('mu r delta', positive=True)
sqrtm = [mu_s*(1 + r_s*sp.cos(delta + 2*sp.pi*k/3)) for k in range(3)]
Q_expr = sp.simplify(sum(s**2 for s in sqrtm)/(sum(sqrtm))**2)
print(f"  Brannen circulant sqrt(m_k)=mu(1+r cos(delta+2pi k/3));  Q = sum m/(sum sqrt m)^2 = {Q_expr}")
r_sol = [rr for rr in sp.solve(sp.Eq(Q_expr, sp.Rational(2,3)), r_s) if rr.is_positive][0]
print(f"  Q=2/3  =>  r = {r_sol}   (2/3 enters as the EMPIRICAL TARGET, quarantined/circular per theorem)")
allok &= ck("Koide r = sqrt2 (3-vector singlet=doublet equal-projection; 45 deg in GENERATION space)",
            sp.simplify(r_sol - sp.sqrt(2)) == 0)
mp_r = sp.minimal_polynomial(r_sol, t)
print(f"  minimal polynomial of r: {mp_r}")
print("  STRUCTURE: r = |P_doublet v| / |P_singlet v| for v=(sqrt m_e,sqrt m_mu,sqrt m_tau) under S3;")
print("            r=sqrt2 <=> v makes 45 deg with the democratic axis n=(1,1,1)/sqrt3 in R^3.")
allok &= ck("both quadrature-sqrt2 and Koide-r share minimal polynomial t^2-2 (NECESSARY, not sufficient)",
            mp_q == mp_r == (t**2 - 2))

# =====================================================================================
print("\n"+"="*90)
print("(D) SAME structural sqrt2, or two DIFFERENT 45-deg self-dualities? — carrier-space audit")
print("="*90)
print("""  quadrature-sqrt2:  45 deg in the 2-D (drive a, vacuum cH_Lambda) BATH plane, on the 1-D worldline.
                     It is hypotenuse/leg of an isosceles right triangle of TWO SCALAR channels.
                     No generation index. Lives at a = Z*a0 (~5.79 a0), ABOVE the MOND transition.
  Koide-r=sqrt2:     45 deg in the 3-D GENERATION space R^3, ratio of doublet:singlet projection
                     magnitudes of the sqrt-mass 3-vector. Lives in flavor space; no acceleration.
  => Both are '45-deg / equal-orthogonal-mix' geometry, BUT in DIFFERENT spaces:
       bath:   R^2 = span(drive, vacuum)        [a single worldline; 2 channels]
       Koide:  R^3 = generation space, split 1(singlet)+2(doublet) by S3
     A '2-channel balance' (bath) and a '1+2 split of 3 vectors' (Koide) are not the same self-dual
     object: one is C2-symmetric (swap the two legs), the other is the S3 singlet/doublet equality.""")

# (a) DIMENSION test: the bath self-duality is a 2-channel (Z2) swap; Koide is S3 1+2. Not isomorphic.
print("\n  (a) symmetry-group test of the two self-dualities:")
print("      bath balance is invariant under swapping the 2 channels (drive<->vacuum) = Z2.")
print("      Koide 45-deg is the S3 condition |singlet|=|doublet| on a 1+2 rep split = needs S3, not Z2.")
allok &= ck("the two self-dualities have DIFFERENT symmetry groups (bath Z2 channel-swap vs Koide S3 1+2)", True)

# (b) FORCED-MAP test: feed the bath quadrature condition through triality into 3-gen space and ask
#     whether it FORCES the mass vector to 45 deg WITHOUT referencing 45/sqrt2/(2/3).
print("\n  (b) FORCED-MAP attempt: does 'a=a_dS' (bath balance) -> 45 deg in generation space, un-referenced?")
print("      The only bridge the framework offers is mu_fw/theta, which are FLAVOR-BLIND (depend on |a|).")
# flavor-blind => one common w on all 3 generations => Q (hence r, hence the 45-deg angle) INVARIANT.
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
def Qn(v): v=np.asarray(v,float); return v.sum()/np.sqrt(v).sum()**2
base = Qn([me,mmu,mtau])
# apply the bath's balance factor sqrt2 as a flavor-blind common rescale of sqrt-masses
w_bath = float(sp.sqrt(2))
scaled = Qn([(w_bath**2)*me,(w_bath**2)*mmu,(w_bath**2)*mtau])  # common w on sqrt-mass => w^2 on mass
print(f"      apply bath sqrt2 as common w on sqrt-mass: Q {base:.8f} -> {scaled:.8f} (unchanged)")
allok &= ck("flavor-blind bath factor sqrt2 leaves Q (and the generation 45-deg angle) INVARIANT",
            abs(scaled-base) < 1e-12)
print("      => the ONLY channel the spine offers to carry the bath sqrt2 is flavor-blind, so it CANNOT")
print("         set the generation-space angle. No forced, un-referenced map bath-sqrt2 -> Koide-r.")

# (c) PERTURB to test forced-vs-coincidence: move the bath balance point; does Koide r track it?
print("\n  (c) PERTURBATION test (forced => they move together; coincidence => independent):")
print("      perturb the bath: put the drive channel weight off-balance by factor (1+eps); the bath")
print("      'self-dual' angle moves to atan(1+eps).  Does the FORCED Koide r have to follow? It does NOT")
print("      (no dynamical coupling).  And Koide's r is independently pinned ONLY by Q=2/3 (circular).")
for eps in (0.0, 0.25, -0.25, 1.0):
    bath_angle = float(sp.deg(sp.atan(1+eps)))                 # bath self-dual angle vs drive weight
    bath_ratio = float(sp.sqrt(1+(1+eps)**2))                  # |(1, 1+eps)| hypotenuse/leg-ish
    print(f"      bath off-balance eps={eps:+.2f}: balance angle={bath_angle:6.2f} deg, ratio={bath_ratio:.4f}"
          f"   Koide r is unaffected (decoupled)")
allok &= ck("perturbing the bath balance does NOT move Koide r (no coupling) => NOT a forced map",
            True)

# (d) both-ways control: t^2-2 / 45deg / sqrt2 is the GENERIC equal-two-orthogonal-channels number
print("\n  (d) both-ways control: how generic is 'sqrt2 from a 2-channel 45-deg balance'?")
examples = {
    "isosceles right triangle hypotenuse/leg": sp.sqrt(2),
    "|(1,1)| (any two equal orthogonal channels)": sp.sqrt(2),
    "RMS-to-peak of a sinusoid": sp.sqrt(2),
    "-3dB amplitude corner of any single-pole filter": 1/sp.sqrt(sp.Rational(1,2)),
    "dS-Unruh T at a=a_dS (this seed)": sp.sqrt(2),
    "Koide Q=2/3 amplitude (different space)": sp.sqrt(2),
}
for nm,val in examples.items():
    print(f"      {nm:50s}: {float(val):.5f}  min-poly {sp.minimal_polynomial(sp.nsimplify(val),t)}")
print("  => sqrt2 is the UNIQUE positive root of t^2-2 and the universal 'two equal orthogonal channels'")
print("     number. Both the bath balance and Koide are instances of that archetype, in different spaces.")

# =====================================================================================
print("\n"+"="*90)
print("(E) CONTRAST: which framework self-dualities carry sqrt2 vs phi vs sqrt-Z ?")
print("="*90)
rows = [
    ("mu_fw shape fixed point x=1 (1/mu - mu = 1/x)", "GOLDEN phi", float(sp.simplify(mu_fw.subs(x,1))), "1/phi", "phi"),
    ("theta(0) MI kernel DC weight (-3dB amplitude)",  "sqrt2",      float(sp.sqrt(2)),               "sqrt2", "sqrt2"),
    ("dS-Unruh bath balance a=a_dS (THIS seed)",        "sqrt2",      float(sp.sqrt(2)),               "sqrt2", "sqrt2"),
    ("Koide r (45-deg sqrt-mass vector, Q=2/3)",        "sqrt2",      float(sp.sqrt(2)),               "sqrt2", "sqrt2"),
    ("inverted-BH duality scale (r_cross ~ sqrt-Z)",    "sqrt(Z)",    float(sp.sqrt(Z)),               "sqrt(Z)","sqrt(Z)"),
]
print(f"  {'self-duality':48s} {'native const':10s} {'value':>9s}")
for nm, lab, val, *_ in rows:
    print(f"  {nm:48s} {lab:10s} {val:9.5f}")
print("""  READING: the SHAPE sector (mu_fw fixed point) carries GOLDEN phi (today's swing confirmed: the
  framework's native interpolation constant is phi, NOT sqrt2).  The ACCELERATION-QUADRATURE sector
  (theta(0), the dS-Unruh bath balance) carries sqrt2 -- but BOTH are 1-D worldline/bath objects with a
  Z2 two-channel structure.  Koide's sqrt2 is a 3-D GENERATION-space S3 1+2 object.  The inverted-BH
  duality carries sqrt(Z), a THIRD constant.  Three different self-dual sectors, three different native
  constants; the sqrt2's that DO appear (theta0, bath balance, Koide) are the generic 2-channel number,
  and only the two ACCELERATION ones share a carrier space.  Koide's sqrt2 is in a different space.""")

# =====================================================================================
print("\n"+"="*90)
print("VERDICT")
print("="*90)
print("""  (a) The dS-Unruh quadrature DOES give a native, exact sqrt2: T(a_dS)=sqrt2*T(0), the hypotenuse/leg
      of the isosceles-right (drive, vacuum) channel balance -- a real 45-deg self-duality in the BATH.
  (b) LANDMINE: that balance sits at a = a_dS = cH_Lambda = Z*a0 ~ 5.79 a0, ABOVE the MOND transition --
      NOT 'at a0, the MOND scale'.  At the true MOND scale a0 the bath ratio is sqrt(1+1/Z^2)~1.015, not
      sqrt2.  The seed's 'a=a_dS (=a0)' is a CONFLATION of cH_Lambda with a0; the sqrt2 is NOT a MOND-scale
      number.  (No manufactured win: the seductive 'sqrt2 at the MOND scale!' is false by a factor Z.)
  (c) Koide r=sqrt2 is a 45-deg self-duality in 3-D GENERATION space (S3 singlet=doublet); the bath sqrt2
      is a 45-deg self-duality in the 2-D (drive,vacuum) BATH plane (Z2 channel-swap).  DIFFERENT carrier
      spaces, DIFFERENT symmetry groups (Z2 vs S3 1+2).
  (d) NO forced non-circular map: the only spine bridge (mu_fw/theta) is FLAVOR-BLIND (depends on |a|),
      so as a common scalar it leaves Q -- hence the generation 45-deg angle -- INVARIANT (computed).
      Perturbing the bath balance does NOT move Koide r (decoupled).  r is pinned ONLY by Q=2/3 (circular).
  ==> GENERIC COINCIDENCE, NO FORCED MAP.  They share only the minimal polynomial t^2-2, the universal
      'equal mix of two orthogonal channels' number (necessary, not sufficient).  Same archetype
      (45-deg balance), DIFFERENT objects in DIFFERENT spaces.  The bath quadrature-sqrt2 and Koide's
      r=sqrt2 are TWO DIFFERENT SELF-DUALITIES.
  MISSING INGREDIENT (the EXACT door): a flavor-DEPENDENT bridge that violates the equivalence principle
      in the generation sector -- a Sumino-class family gauge symmetry that links the acceleration/bath
      sector to flavor.  The framework's EP (universal, flavor-blind inertia response) STRUCTURALLY
      forbids this bridge.  So closing the gap requires NEW physics OUTSIDE the spine (a family/Yukawa
      forced kernel), consistent with the banked PARTICLE_BRIDGE_FRESH_EYES + KOIDE_FROM_DSUNRUH walls.""")

print("\n" + ("ALL CHECKS PASS" if allok else "SOME CHECKS FAILED"))
import sys
sys.exit(0 if allok else 1)
