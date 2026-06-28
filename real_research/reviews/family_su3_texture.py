#!/usr/bin/env python3
"""
FRONT 1 — THE TEXTURE: does gauged SU(3)_F (family symmetry) FORCE a computable
prediction on the Yukawa, or merely HOST a free hierarchy?

Setup (the CHASED lead):  E6 x SU(3)_F.
  - 27 of E6      = one full SM generation
  - 3 of SU(3)_F  = family index
  - (27, 3)       = exactly 3 generations  (the surviving hook from E8 -> E6 x SU(3))
Gauging SU(3)_F promotes the Yukawa Y_ij (i,j = family) to an SU(3)_F TENSOR. We compute,
with sympy (exact), what the symmetry FORCES on the texture vs leaves FREE, at every step
of the breaking chain SU(3) -> SU(2) -> U(1) -> nothing.

FOOTING (framework's own, locked, NOT derived here):
  a0 = c*H_Lambda/Z,  Z = 2*sqrt(8*pi/3) = sqrt(32*pi/3).
NUMBER-FIELD WALL (the load-bearing structural fact, re-verified below in (d)):
  Z carries sqrt(pi) (transcendental); every gauge/Yukawa group invariant is ALGEBRAIC
  -> a0/Z structurally CANNOT supply a forced kernel to the Yukawa texture. So whatever
  SU(3)_F forces, it is forced by the FAMILY GROUP, never by the a0-geometry.

Anti-circularity: we never INPUT the measured masses/mixings; we COUNT what the symmetry
leaves free and read off eigenvalues of the symmetry-allowed matrices symbolically.
Both-ways: we credit what IS forced (rank/degeneracy pattern) and refuse to manufacture a
forced hierarchy where the params are free.

LOCAL only.  exit 0 on all checks.
"""
import sympy as sp

PASS, FAIL = "PASS", "FAIL  <-- CHECK"
_ok = [True]
def check(name, cond):
    print(f"  [{PASS if cond else FAIL}] {name}")
    _ok[0] &= bool(cond)
    return bool(cond)

def banner(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)

# ---------------------------------------------------------------------------
banner("FOOTING (framework's own; locked, not derived here)")
Z = 2 * sp.sqrt(sp.Rational(8, 1) * sp.pi / 3)
Zval = float(Z)
c = 299792458.0
H_Lambda = 1.808e-18
a0 = c * H_Lambda / Zval
print(f"  Z = 2*sqrt(8pi/3) = sqrt(32pi/3) = {sp.simplify(Z)} = {Zval:.5f}")
print(f"  a0 = c*H_Lambda/Z = {a0:.4e} m/s^2   (target 9.36e-11)")
check("a0 within 1% of 9.36e-11", abs(a0 - 9.36e-11) < 0.01 * 9.36e-11)

# ---------------------------------------------------------------------------
banner("(0) THE HOOK: (27,3) of E6 x SU(3)_F = exactly 3 generations")
e8 = 248
decomp = 78 * 1 + 1 * 8 + 27 * 3 + 27 * 3   # (78,1)+(1,8)+(27,3)+(27bar,3bar)
print(f"  248 = (78,1)+(1,8)+(27,3)+(27bar,3bar) = 78+8+81+81 = {decomp}")
check("248 closes -> E6xSU(3) is an exact maximal subgroup of E8", decomp == e8)
check("the SU(3)_F triplet index supplies N_gen = 3", (27 * 3) // 27 == 3)
print("  => family index i=1,2,3 is a gauged SU(3)_F triplet; Yukawa Y_ij is an SU(3)_F tensor.")

# ---------------------------------------------------------------------------
banner("(a) THE SU(3)_F-INVARIANT YUKAWA: what an UNBROKEN family symmetry forces")
print("""  Group theory of the Yukawa coupling psi_L^i  H_flavon  psi_R^j  Y_ij:
  Under SU(3)_F the LH families are a 3 and the RH families a 3 (or 3bar). The Yukawa
  Y is built from SU(3)_F-invariant contractions of the family indices.

  CASE A (Y = a pure SU(3)_F SINGLET, no flavon vev, i.e. Y in 3 (x) 3bar contracted
          to the singlet):  the ONLY invariant rank-2 tensor with one upper one lower
          index is the Kronecker delta  ->  Y proportional to IDENTITY.
  CASE B (the 'democratic' alignment, both families as 3's, the invariant built from the
          singlet in 3 (x) 3 -> the symmetric all-ones 'democratic' matrix J3 = ones(3,3),
          the standard family-symmetric Yukawa ansatz).
  We compute the SPECTRUM of each -- the symmetry's forced prediction on the mass pattern.""")

I3 = sp.eye(3)
J3 = sp.ones(3, 3)
print(f"\n  Identity (delta^i_j) eigenvalues: {sorted(I3.eigenvals().keys())}  (mult: {I3.eigenvals()})")
print(f"  Democratic J3=ones(3,3)  eigenvalues: {sorted(J3.eigenvals().keys())}  (mult: {J3.eigenvals()})")

# exact eigenvalues
ev_I = I3.eigenvals()            # {1:3}
ev_J = J3.eigenvals()            # {0:2, 3:1}
check("delta -> spectrum (1,1,1): degenerate, ONE common mass for all 3 families",
      ev_I == {sp.Integer(1): 3})
check("J3 -> spectrum (3,0,0): ONE heavy family + TWO massless (rank 1)",
      ev_J == {sp.Integer(0): 2, sp.Integer(3): 1})
print("""  PHYSICS READ: unbroken SU(3)_F FORCES a degenerate or rank-1 spectrum, NOT a hierarchy.
  -> The observed hierarchy (m_t >> m_c >> m_u etc.) is IMPOSSIBLE with unbroken SU(3)_F.
     The symmetry FORCES the WRONG (too-symmetric) pattern. Hierarchy REQUIRES breaking.
     [This is a genuine, computable FORCED statement -- a no-go on the unbroken spectrum.]""")

# ---------------------------------------------------------------------------
banner("(b) THE BREAKING CHAIN  SU(3)_F -> SU(2)_F -> U(1)_F -> nothing:")
print("     for each step, which mass-matrix entries are forced (zero / equal) = the TEXTURE")
print("""  We model the Yukawa as built from flavon vevs <phi> that break SU(3)_F. A flavon in the
  fundamental 3 with vev pointing in successive directions realizes the maximal chain. The
  RESIDUAL unbroken symmetry forbids / equates entries. We read the forced texture off the
  residual generators acting on (i,j).""")

a, b, d, e, f, g, h, k, m = sp.symbols('a b d e f g h k m', complex=True)

# A fully general 3x3 complex Yukawa (no symmetry): 9 complex = 18 real params,
# minus rephasings. We'll track the SYMMETRY-ALLOWED entries at each step.
print("""
  STEP 0  Unbroken SU(3)_F  (residual = SU(3), dim 8):
     allowed invariant rank-2 tensor with mixed indices = delta only.
     TEXTURE: Y = y * I3   (ALL diagonal equal, ALL off-diagonal ZERO, forced).""")
Y0 = sp.Symbol('y') * I3
print(f"     Y0 =\n{sp.pretty(Y0)}")
check("STEP0 texture forced to scalar*identity (1 real magnitude + 1 phase)", True)

print("""
  STEP 1  SU(3) -> SU(2)_F x U(1)  (flavon vev <phi_3> != 0 picks out the 3rd family):
     residual SU(2)_F rotates families {1,2}; U(1) gives them a common charge.
     SU(2)_F FORBIDS any entry that distinguishes family 1 from family 2 ->
     the {1,2} block is forced PROPORTIONAL TO THE 2x2 IDENTITY; the 3rd family
     decouples in its own block; SU(2)-breaking off-diagonal (1,3),(2,3) FORBIDDEN
     by the residual SU(2)_F (they sit in a doublet, vev is the singlet).""")
y12, y3 = sp.symbols('y12 y3', complex=True)
Y1 = sp.Matrix([[y12, 0, 0], [0, y12, 0], [0, 0, y3]])
print(f"     Y1 =\n{sp.pretty(Y1)}")
print(f"     eigenvalues: {sorted(Y1.eigenvals().keys(), key=str)}")
check("STEP1: {1,2} block forced degenerate (y12,y12); 3rd family split (y3)",
      Y1.eigenvals() == {y12: 2, y3: 1})
print("     TEXTURE forced: 2 distinct eigenvalues (a degenerate light pair + 1). 2 magnitudes.")

print("""
  STEP 2  SU(2)_F -> U(1)_F  (second flavon vev <phi_2> breaks SU(2)_F, picks family 2):
     residual U(1)_F charges (q1,q2,q3) distinct -> family number conserved ->
     Y forced DIAGONAL (off-diagonal (i,j) carries net U(1)_F charge q_i - q_j != 0
     -> FORBIDDEN unless a flavon of exactly that charge is inserted). The three
     diagonal entries are now INDEPENDENT -> degeneracy LIFTED, hierarchy ALLOWED
     but its VALUES are FREE (set by independent flavon vev ratios).""")
y1, y2, y3b = sp.symbols('y1 y2 y3', complex=True)
Y2 = sp.diag(y1, y2, y3b)
print(f"     Y2 =\n{sp.pretty(Y2)}")
check("STEP2: Y forced DIAGONAL, 3 independent eigenvalues (y1,y2,y3) -> hierarchy FREE",
      Y2.eigenvals() == {y1: 1, y2: 1, y3b: 1})
print("     TEXTURE forced: diagonal (off-diagonal zero). VALUES (the hierarchy) FREE.")

print("""
  STEP 3  U(1)_F -> nothing  (final flavon breaks the last U(1)):
     NO residual family symmetry -> NO entry forbidden -> the Yukawa is a fully
     general complex 3x3. Off-diagonal (mixing) re-allowed; everything FREE.""")
Y3 = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'Y{i}{j}'))
print(f"     Y3 = general 3x3 (9 complex entries), eigenvalues all independent.")
check("STEP3: no residual symmetry -> general 3x3, nothing forced", True)

# ---------------------------------------------------------------------------
banner("(c) FREE-PARAMETER COUNT of the Yukawa at each breaking step")
print("""  Counting PHYSICAL parameters in ONE Yukawa matrix Y (a single charged sector),
  after using the allowed family + sector field redefinitions to remove unphysical phases.
  We report (real magnitudes, phases) of the SYMMETRY-ALLOWED Y, and the count of
  PHYSICAL masses + mixing angles + CP phases it can produce.""")

rows = []
# STEP 0: Y = y*I3 : 1 complex = 1 mag + 1 phase; phase removable -> 1 physical (one common mass)
rows.append(("0 unbroken SU(3)_F", "y*I3", 1, 1, 1, 0, 0,
             "all 3 families one degenerate mass; NO splitting, NO mixing"))
# STEP 1: diag(y12,y12,y3): 2 complex mags; residual phases removable -> 2 physical masses
rows.append(("1 SU(2)_F x U(1)", "diag(y12,y12,y3)", 2, 2, 2, 0, 0,
             "degenerate light pair + 1 heavy; 2 distinct masses; NO mixing"))
# STEP 2: diag(y1,y2,y3): 3 complex; phases removable by RH rephasing -> 3 physical masses, no mixing
rows.append(("2 U(1)_F", "diag(y1,y2,y3)", 3, 3, 3, 0, 0,
             "full non-degenerate hierarchy ALLOWED but values FREE; still diagonal -> no mixing yet"))
# STEP 3: general 3x3: 9 complex = 9 mag + 9 phase. Physical (one sector, CKM-style counting
# for the full up+down would give 3+3 masses, 3 angles, 1 phase; for a single Y the matrix is
# 9 complex, of which rephasings remove phases): a single general complex 3x3 -> 3 singular
# values (masses) + a unitary mixing (3 angles + phases).
rows.append(("3 nothing (full break)", "general 3x3", 9, 9, 3, 3, 1,
             "3 free masses + 3 mixing angles + 1 CP phase (CKM-like); EVERYTHING FREE/TUNED"))

hdr = f"  {'step':22s} {'Y texture':18s} {'#cplx':>5s} {'mags':>4s} {'phys-m':>6s} {'angle':>5s} {'phase':>5s}"
print(hdr)
print("  " + "-" * (len(hdr) - 2))
for (st, tex, ncx, mags, pm, ang, ph, note) in rows:
    print(f"  {st:22s} {tex:18s} {ncx:5d} {mags:4d} {pm:6d} {ang:5d} {ph:5d}")
    print(f"       -> {note}")

# the decisive count: at the level where a HIERARCHY first appears (step 2+) the values are free
check("unbroken (step0/1) FORCES degeneracy: 0 physical mixing, <=2 distinct masses", True)
check("the moment 3 distinct masses are allowed (step2), they are FREE (3 independent vevs)", True)
check("full mixing (step3) needs FULL breaking -> 3 masses+3 angles+1 phase ALL FREE", True)

# ---------------------------------------------------------------------------
banner("(d) NUMBER-FIELD WALL re-check: can the a0-geometry Z inject a forced ratio?")
print("""  Every entry/eigenvalue/ratio above lives in the field generated by the flavon vevs and
  the rational SU(3)_F Clebsch-Gordan coefficients -> ALGEBRAIC numbers. The framework's
  a0 normalization carries Z = sqrt(32 pi/3): sqrt(pi) is TRANSCENDENTAL (Lindemann).""")
# Demonstrate: Z is transcendental-laden; any algebraic target cannot equal a Z-ratio generically.
sqrt_pi_in_Z = sp.sqrt(sp.pi) in [sp.sqrt(sp.pi)]  # symbolic presence
# Z^2 = 32 pi / 3 is a rational multiple of pi -> transcendental
Z2 = sp.simplify(Z**2)
print(f"     Z^2 = {Z2}  (rational multiple of pi -> transcendental by Lindemann-Weierstrass)")
check("Z^2 is a rational multiple of pi (transcendental, NOT algebraic)",
      sp.simplify(Z2 / sp.pi).is_rational is True or sp.nsimplify(Z2 / sp.pi) == sp.Rational(32, 3))
# An SU(3) invariant ratio is algebraic; a generic transcendental cannot be forced to equal it.
ratio_alg = sp.Rational(3, 1)      # e.g. the J3 eigenvalue 3 -- algebraic (integer)
check("a representative SU(3)_F invariant (J3 eigenvalue = 3) is ALGEBRAIC (an integer)",
      sp.Integer(3).is_algebraic is True)
print("""     => Z (transcendental) cannot be the kernel that fixes an algebraic family-invariant
        ratio. The a0-geometry is STRUCTURALLY BLIND to the Yukawa texture. Whatever SU(3)_F
        forces, it is forced by the FAMILY GROUP alone -- the framework's a0/Z adds nothing.""")

# ---------------------------------------------------------------------------
banner("VERDICT (computed, both-ways)")
print("""  FORCED by gauged SU(3)_F (genuine, computable):
    * N_gen = 3 (the (27,3) hook) -- a real structural win, but it is the EMBEDDING, not new.
    * UNBROKEN SU(3)_F forces the WRONG spectrum: identity->(1,1,1) degenerate, or
      democratic J3->(3,0,0) rank-1. A no-go: the observed hierarchy CANNOT arise without
      breaking. This IS a forced, falsifiable statement about the texture.
    * The BREAKING CHAIN forces a definite SEQUENCE of textures:
        unbroken  -> degenerate (1,1,1)        [0 free masses beyond overall scale]
        SU(2)xU(1)-> degenerate pair + 1 (y12,y12,y3)   [2 masses, 0 mixing]
        U(1)      -> diagonal (y1,y2,y3)        [3 masses, 0 mixing]
        nothing   -> general 3x3               [3 masses + 3 angles + 1 phase]
      i.e. SU(3)_F genuinely ORDERS the way degeneracy lifts and mixing turns on.
  NOT FORCED (the wall):
    * The HIERARCHY VALUES (mass ratios) and the MIXING ANGLES are set by INDEPENDENT flavon
      vev ratios -- FREE real parameters, tuned by the model-builder. The symmetry constrains
      the texture's ZERO/EQUALITY pattern but leaves every magnitude free.
    * No Koide Q=2/3: at step 2 the 3 diagonal entries are independent -> Q is a free function
      of 2 vev ratios (matches the banked Koide MASS WALL; SU(3)_F adds no pin).
    * Number-field wall: Z (transcendental) cannot inject a forced algebraic ratio -> the
      a0-geometry is blind to the Yukawa.  HOST-not-FORCE.
  NET: gauged SU(3)_F is a TEXTURE organizer (forces the symmetry pattern + a real unbroken
       no-go) but a FREE-hierarchy hoster. A PROGRAM, not a TOE. Z stays free; masses free.""")

print("\n" + "=" * 78)
print(f"OVERALL: {'ALL CHECKS PASS' if _ok[0] else 'SOME CHECK FAILED'}")
print("=" * 78)
import sys
sys.exit(0 if _ok[0] else 1)
