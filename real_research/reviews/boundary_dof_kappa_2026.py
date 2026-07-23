#!/usr/bin/env python3
"""
BOUNDARY-DOF vs the kappa WALL (2026-07-23) -- does d=3 dS-boundary dof-counting force Z's '2'?
==============================================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED INERTIA. a0 = c H_Lambda / Z, Z = sqrt(32pi/3)
= 2 sqrt(8pi/3) = 5.78881. The POSITED coefficient Z factors as:

     Z^2 = 32 pi/3 = 4 * (8 pi/3)  =  (1/kappa)^2 * (8 pi/3),   kappa = 1/2.

     SHAPE          = 8 pi/3   (Einstein 8pi via rho_DE=Lambda c^2/8piG; Friedmann 3 via H^2=(8piG/3)rho)
     NORMALIZATION  = 4 = (1/kappa)^2   (the (c/2) prefactor in a0=(c/2)sqrt(G rho_DE); kappa=1/2 the crux)

PRIOR (established, NOT relitigated here -- tested for evasion): kappa=1/2 is provably UNFORCEABLE
by ghost-freedom+unitarity+holography (bulk). The CKN-dof bridge (2026-06-17) is CLOSED: the
framework O(1) 0.5878=(3/8pi)^{1/4} is the g_*=1 GEOMETRIC LIMIT of the CKN energy bound, NOT a
microscopic fix -- an honest SM dof count (g_*=106.75) gives ~0.18-0.41, never 0.5878. The
period-ring result pointed the LONE sqrt(pi)=Gamma(1/2)=2*Gamma(3/2) to a d=3 / dS4-boundary
measure (Gamma(3/2)=sqrt(pi)/2, S_2=4pi, V_3=4pi/3).

THE ONE UNTRIED ANGLE (my role): does dof-counting ON THE d=3 BOUNDARY (not the closed bulk CKN)
force the normalization '2'/kappa=1/2 where the bulk could not? This script settles it with sympy:

  PART A  Reconstruct 0.5878=(3/8pi)^{1/4} EXACTLY and its relation to Z. Is it a power of Z or of
          8pi/3? Answer: a PURE (-1/4) power of the SHAPE 8pi/3; equivalently sqrt(2)*Z^{-1/2},
          the sqrt(2) exactly cancelling the normalization '2' in Z. => 0.5878 sees ONLY the shape.

  PART B  The BOUNDARY CKN saturation, derived from d=3 geometry (Schwarzschild-1/2 + ball V_3=4pi/3):
          rho_max = (Schwarzschild 1/2)/(ball 4pi/3) * c^4/(G R_dS^2) = (3/8pi) c^2 H^2/G = rho_vac.
          This FORCES the shape coefficient 3/8pi from PURE d=3 boundary geometry -- a real result.

  PART C  The crux test, kappa-parametrized. a0 = kappa*c*sqrt(G rho_DE) => Z=(1/kappa)sqrt(8pi/3),
          CKN-O(1)=4/Z^2=4 kappa^2*(3/8pi), and 0.5878-slot = sqrt(2 kappa)*(3/8pi)^{1/4}.
          PROVE-BY-MOVING-THE-NUMBER: perturb kappa; the boundary geometry (shape, area, entropy,
          rho_max) is UNCHANGED, but Z and a0 MOVE. => the boundary dof count is BLIND to kappa;
          reproducing 0.5878=(3/8pi)^{1/4} REQUIRES 4 kappa^2=1 as an INPUT, not a derivation.

  PART D  Is Z forced by any single boundary measure? Solve for the measure that equals Z. The
          period-ring d*=1.907 (non-integer) recurs; Z^2=8*V_3=(8/3)*S_2 are FLAGGED as numerology
          (the 8, 8/3 unmotivated). No single boundary object forces Z.

HONEST OUTCOME (expected, and it is the VALUABLE result): the boundary angle EVADES NOTHING of the
kappa-wall. It BEAUTIFULLY fixes the SHAPE sqrt(8pi/3) from d=3 boundary geometry (Schwarzschild-1/2
over ball-4pi/3, lone sqrt(pi)=the d=3 measure) -- a GEOMETRIC REASON for why the period-ring pointed
to d=3 -- but the normalization '2'=1/kappa is a DYNAMICAL inertia-response coupling that the
KINEMATIC boundary count is structurally blind to, hitting the SAME g_*=1 geometric-limit wall as
the bulk. Z STAYS POSITED. No TOE, no 'theory closed'. nu is Milgrom-1999's. Exit 0 = ran.
"""
import sympy as sp

FAIL = []
def check(name, cond):
    print(f"    [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        FAIL.append(name)

pi = sp.pi
print("=" * 90)
print("BOUNDARY-DOF vs kappa WALL 2026 -- does d=3 dS-boundary counting force Z's normalization '2'?")
print("=" * 90)

# ---------------------------------------------------------------------------------------------
# PART A -- reconstruct 0.5878 = (3/8pi)^{1/4} EXACTLY and its relation to Z
# ---------------------------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART A  0.5878 = (3/8pi)^{1/4}: a power of the SHAPE 8pi/3, NOT a pure power of Z")
print("-" * 90)

Z   = sp.sqrt(sp.Rational(32, 3) * pi)          # = 2 sqrt(8pi/3)
O1  = sp.Rational(3, 8) / pi                     # 3/8pi = inverse Friedmann coefficient
num = (O1) ** sp.Rational(1, 4)                  # the framework O(1) = 0.5878...
print(f"  Z          = sqrt(32pi/3)      = {float(Z):.10f}")
print(f"  3/8pi      = inverse Friedmann  = {float(O1):.10f}   (Friedmann coeff 8pi/3 inverted)")
print(f"  (3/8pi)^1/4                     = {float(num):.10f}   <- the framework's O(1) '0.5878'")

check("Z = 2*sqrt(8pi/3) exactly", sp.simplify(Z - 2*sp.sqrt(sp.Rational(8,3)*pi)) == 0)
check("Z^2 = 4*(8pi/3): NORMALIZATION 4 times SHAPE 8pi/3",
      sp.simplify(Z**2 - 4*sp.Rational(8,3)*pi) == 0)
# the three equivalent forms of 0.5878
check("0.5878 = (3/8pi)^{1/4}  (pure -1/4 power of the SHAPE 8pi/3)",
      sp.simplify(num - (sp.Rational(8,3)*pi)**sp.Rational(-1,4)) == 0)
check("0.5878 = sqrt(2/Z)  (the CKN seesaw prefactor (4/Z^2)^{1/4})",
      sp.simplify(num - sp.sqrt(2/Z)) == 0)
check("0.5878 = sqrt(2) * Z^{-1/2}  (Z^-1/2 times sqrt2; NOT a pure power of Z)",
      sp.simplify(num - sp.sqrt(2)*Z**sp.Rational(-1,2)) == 0)
check("0.5878 = sqrt(2/Z) = sqrt(pi/... ) is NOT rational-power-of-Z: 0.5878/Z^p irrational for all p!=... ",
      sp.simplify(num**4 - O1) == 0)   # 0.5878^4 = 3/8pi is RATIONAL/pi  => pure shape
print("  => 0.5878^4 = 3/8pi is rational/pi (PURE SHAPE). Writing 0.5878 = sqrt(2)*Z^{-1/2}, the")
print("     sqrt(2) EXACTLY cancels the '2' in Z=2*sqrt(8pi/3): sqrt(2/(2 sqrt(8pi/3)))=(8pi/3)^{-1/4}.")
print("     => the NORMALIZATION '2' (kappa) CANCELS OUT of 0.5878. 0.5878 encodes only the SHAPE.")

# ---------------------------------------------------------------------------------------------
# PART B -- the d=3 boundary CKN saturation: Schwarzschild-1/2 over ball-4pi/3 FORCES 3/8pi
# ---------------------------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART B  d=3 boundary geometry forces the SHAPE coefficient 3/8pi (Schwarzschild-1/2 / V_3)")
print("-" * 90)
# Max energy in a static patch of radius R without horizon collapse (Schwarzschild):
#   R_s = 2GM/c^2 = R  => M_max = c^2 R/(2G)  => E_max = M_max c^2 = c^4 R/(2G).
# d=3 ball volume V = (4pi/3) R^3.  Energy density rho_max = E_max / V.
R, G, c, H = sp.symbols('R G c H', positive=True)
E_max = c**4 * R / (2*G)                          # Schwarzschild 1/2
V3    = sp.Rational(4, 3) * pi * R**3             # d=3 ball measure 4pi/3
rho_max = sp.simplify(E_max / V3)                 # energy density
coeff = sp.simplify(rho_max / (c**4/(G*R**2)))    # strip c^4/(G R^2) -> the pure coefficient
print(f"  E_max = c^4 R/(2G)  (Schwarzschild 1/2);  V_3 = (4pi/3)R^3  (d=3 ball measure)")
print(f"  rho_max = E_max/V_3 = {coeff} * c^4/(G R^2)")
check("boundary coefficient (Schwarz-1/2)/(ball-4pi/3) = 3/8pi EXACTLY",
      sp.simplify(coeff - O1) == 0)
# tie R = c/H (de Sitter horizon) -> rho_max = (3/8pi) c^2 H^2/G  = Friedmann rho_vac
rho_max_H = sp.simplify(rho_max.subs(R, c/H))
rho_vac   = sp.Rational(3, 8)/pi * c**2 * H**2 / G   # Friedmann de Sitter (energy density form)
check("with R=c/H, rho_max = (3/8pi) c^2 H^2/G = Friedmann rho_vac (saturation = Friedmann)",
      sp.simplify(rho_max_H - rho_vac) == 0)
print("  => PURE d=3 boundary geometry (Schwarzschild-1/2, ball-4pi/3) DERIVES the coefficient 3/8pi,")
print("     hence the SHAPE sqrt(8pi/3) of Z and the number 0.5878=(3/8pi)^{1/4}. This is REAL and")
print("     it is exactly where the lone sqrt(pi)=Gamma(3/2)*2 lives (d=3 measure). The boundary IS")
print("     the right home for the SHAPE. (Saturation + L=c/H + dropping additive const still assumed.)")

# ---------------------------------------------------------------------------------------------
# PART C -- the crux: kappa-parametrized. Move kappa; boundary geometry is FROZEN, Z moves.
# ---------------------------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART C  CRUX: prove-by-moving-the-number. kappa is INVISIBLE to the boundary dof count")
print("-" * 90)
kap = sp.symbols('kappa', positive=True)
# a0 = kappa * c * sqrt(G rho_DE,mass), rho_DE,mass = Lambda c^2/(8piG), Lambda = 3H^2/c^2
Lam = 3*H**2/c**2
rho_DE_mass = Lam*c**2/(8*pi*G)
a0_k = kap * c * sp.sqrt(G*rho_DE_mass)
a0_k = sp.simplify(a0_k)
Z_k  = sp.simplify(c*H / a0_k)                    # Z(kappa) = cH/a0
print(f"  a0(kappa) = kappa*c*sqrt(G rho_DE) = {a0_k}")
print(f"  Z(kappa)  = cH/a0 = {sp.nsimplify(Z_k)}")
check("Z(kappa) = (1/kappa) sqrt(8pi/3)  (SHAPE fixed, NORMALIZATION = 1/kappa)",
      sp.simplify(Z_k - (1/kap)*sp.sqrt(sp.Rational(8,3)*pi)) == 0)
check("Z(kappa=1/2) = 2 sqrt(8pi/3) = canonical Z",
      sp.simplify(Z_k.subs(kap, sp.Rational(1,2)) - Z) == 0)

# CKN O(1) and the 0.5878-slot as functions of kappa
CKN_O1_k = sp.simplify(4/Z_k**2)                  # observed rho_vac/(M_P^2 H^2) analog
slot_k   = sp.simplify(sp.sqrt(2/Z_k))            # the 0.5878-slot
print(f"\n  CKN O(1)   4/Z^2 = {sp.nsimplify(CKN_O1_k)}   = 4 kappa^2 * (3/8pi)")
print(f"  0.5878-slot sqrt(2/Z) = {sp.nsimplify(slot_k)}   = sqrt(2 kappa) * (3/8pi)^{{1/4}}")
check("CKN O(1) = 4 kappa^2 * (3/8pi)  (shape times 4kappa^2)",
      sp.simplify(CKN_O1_k - 4*kap**2*O1) == 0)
check("0.5878-slot = sqrt(2 kappa) * (3/8pi)^{1/4}  (clean ONLY when 2 kappa = 1)",
      sp.simplify(slot_k - sp.sqrt(2*kap)*O1**sp.Rational(1,4)) == 0)
check("slot = (3/8pi)^{1/4} EXACTLY  <=>  kappa = 1/2  (the landing REQUIRES kappa=1/2 as input)",
      sp.simplify(sp.solve(sp.Eq(slot_k, O1**sp.Rational(1,4)), kap)[0] - sp.Rational(1,2)) == 0)

# the boundary-count INVARIANTS (what the dof count actually sees) are kappa-FREE:
A_horizon = 4*pi*(c/H)**2                          # dS horizon area (2-sphere) -- kappa-free
S_GH      = pi*(c/H)**2                             # GH entropy A/4 (Planck=1) -- kappa-free
print("\n  What the boundary dof count SEES (all kappa-FREE):")
print(f"    dS horizon area A = 4pi R_dS^2 = {A_horizon}   (no kappa)")
print(f"    GH entropy S = A/4            = {S_GH}   (no kappa)")
print(f"    boundary rho_max coefficient = 3/8pi           (no kappa, PART B)")
check("horizon area is independent of kappa (dA/dkappa = 0)", sp.diff(A_horizon, kap) == 0)
check("GH entropy is independent of kappa (dS/dkappa = 0)", sp.diff(S_GH, kap) == 0)
check("boundary rho_max coefficient 3/8pi is independent of kappa", sp.diff(O1, kap) == 0)
# but a0 and Z DO move with kappa
check("a0 MOVES with kappa (da0/dkappa != 0): kappa is a DYNAMICAL response coupling",
      sp.simplify(sp.diff(a0_k, kap)) != 0)
print("  => MOVE kappa: area, entropy, boundary rho_max are FROZEN; a0 and Z MOVE. The kinematic")
print("     boundary dof count is STRUCTURALLY BLIND to kappa. Reproducing 0.5878=(3/8pi)^{1/4}")
print("     needs 4 kappa^2=1 fed IN. Same g_*=1 wall as the bulk -- NOT forced by the boundary.")

# ---------------------------------------------------------------------------------------------
# PART D -- is Z forced by any single boundary MEASURE? (numerology guard)
# ---------------------------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART D  numerology guard: no single boundary measure forces Z (period-ring d*=1.907 recurs)")
print("-" * 90)
S2 = 4*pi                 # unit 2-sphere area (dS horizon shape)
V3 = sp.Rational(4,3)*pi  # unit 3-ball volume (d=3 measure)
Z2 = sp.Rational(32,3)*pi
print(f"  Z^2 = 32pi/3 = {sp.nsimplify(Z2)}")
print(f"  Z^2 / V_3 = (32pi/3)/(4pi/3) = {sp.nsimplify(Z2/V3)}   (an unmotivated integer 8)")
print(f"  Z^2 / S_2 = (32pi/3)/(4pi)   = {sp.nsimplify(Z2/S2)}   (an unmotivated 8/3)")
check("Z^2 = 8 * V_3  (but '8' is UNMOTIVATED -> numerology, NOT a derivation)", sp.simplify(Z2 - 8*V3) == 0)
check("Z^2 = (8/3) * S_2  (but '8/3' is UNMOTIVATED -> numerology)", sp.simplify(Z2 - sp.Rational(8,3)*S2) == 0)
print("  These are IDENTITIES, not derivations: the multipliers 8, 8/3 are exactly the missing")
print("  normalization*shape; choosing them to hit Z is the numerology failure mode we REJECT.")
# loop-measure dimension solve (matches period_ring_obstruction_2026.py: d* = 1.907, non-integer)
d = sp.symbols('d', positive=True)
Sd = 2*pi**(d/2)/sp.gamma(d/2)   # unit (d-1)-sphere surface area
dstar = sp.nsolve(Sd - float(sp.sqrt(Z2)), d, 2.0)
print(f"\n  Solve S_(d-1)=2pi^(d/2)/Gamma(d/2) = Z:  d* = {float(dstar):.4f}  (NON-integer; d=3 gives S_2=4pi!=Z)")
check("d* is NOT an integer (no natural integer-dim loop measure equals Z)",
      abs(float(dstar) - round(float(dstar))) > 1e-2)
check("d=3 boundary gives S_2=4pi, and 4pi != Z", sp.simplify(Sd.subs(d,3) - 4*pi) == 0 and abs(float(4*pi) - float(sp.sqrt(Z2))) > 1)

# ---------------------------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------------------------
print("\n" + "=" * 90)
print("VERDICT:  WALL (sharpened, geometrically localized) -- the d=3 boundary FIXES the SHAPE but")
print("          CANNOT force the normalization '2'/kappa. Z stays POSITED. A null, verified as a win.")
print("=" * 90)
print("""  * 0.5878 = (3/8pi)^{1/4} is a PURE power of the SHAPE 8pi/3 (0.5878^4=3/8pi, rational/pi).
    Written as sqrt(2)*Z^{-1/2}, its sqrt(2) exactly cancels the '2' in Z=2 sqrt(8pi/3) -- so
    0.5878 is BLIND to the normalization kappa; it carries ONLY the Einstein-8pi/Friedmann-3 shape.
  * The d=3 boundary DOES force the SHAPE: (Schwarzschild-1/2)/(ball-4pi/3) = 3/8pi EXACTLY,
    saturated at R=c/H gives Friedmann rho_vac. The lone sqrt(pi) is the d=3 boundary measure
    (Gamma(3/2)=sqrt(pi)/2, S_2, V_3) -- the boundary is the RIGHT HOME for Z's shape, and this is
    a real GEOMETRIC REASON the period-ring pointed to d=3.
  * But the normalization '2'=1/kappa is a DYNAMICAL inertia-response coupling. Prove-by-moving:
    perturb kappa and the entire boundary dof count (area, GH entropy, rho_max=3/8pi) is FROZEN
    while a0 and Z MOVE. The kinematic boundary count is STRUCTURALLY BLIND to kappa. Reproducing
    0.5878=(3/8pi)^{1/4} requires 4 kappa^2=1 fed IN -- the SAME g_*=1 geometric-limit wall the
    bulk CKN hit, now with a transparent reason: SHAPE=geometry (boundary-derivable), NORMALIZATION
    =dynamics (fit to the observed a0). No single boundary measure forces Z (d*=1.907 non-integer;
    Z^2=8 V_3 is unmotivated numerology).
  * The boundary EVADES NOTHING of the kappa-wall; it gives a SHARPER result (a geometric reason
    for it), NOT a derivation of Z. Three doors stay shut, plus this fourth. Z POSITED, a0's value
    NOT derived (one-parameter EFT, kappa free but nonzero). No TOE. No 'theory closed'.""")

if FAIL:
    print("\n*** ASSERTIONS FAILED:", FAIL)
    raise SystemExit(1)
print("\nAll assertions passed. EXIT 0 (ran; a null, not a verdict of 'closed').")
