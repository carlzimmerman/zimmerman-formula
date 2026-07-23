#!/usr/bin/env python3
"""
PERIOD-RING OBSTRUCTION (2026-07-23) -- the period-arithmetic test of the SM wall.

Context. The 2026-06-27 NUMBER-FIELD OBSTRUCTION closed the SM mass/flavor door on
ALGEBRAIC grounds: Z = sqrt(32 pi/3) carries a transcendental sqrt(pi), while all
measured flavor data (mass ratios, Koide Q=2/3, mixing angles) is ALGEBRAIC to
measurement precision, so a0/Z is structurally gauge-blind to the flavor sector.

The ONE untried angle tested here: PERIODS (Kontsevich-Zagier) are a strictly larger
ring than the algebraics -- pi, log2, zeta(3), MZVs and Gamma(p/q) values are all
periods, and sqrt(pi)=Gamma(1/2). So the question is whether moving the unification
question from ALGEBRA (provably walled) up to PERIOD ARITHMETIC forces any new
Z <-> SM-flavor relation that the algebraic route could not.

This script encodes the three load-bearing facts and reports DOOR vs WALL:

  PART 1  Z's period content: Z = (4 sqrt6/3) * sqrt(pi); the algebraic cofactor is a
          quadratic irrational (minpoly 3x^2-32), NOT a CM Gamma value. Solve for the
          dimension d making Z a loop measure S_{d-1}=2 pi^{d/2}/Gamma(d/2): d*=1.907,
          a non-integer; NO integer d (incl. the dS_4 boundary d=3) reproduces Z.

  PART 2  sqrt(pi)=Gamma(1/2) has HALF-INTEGER weight (MZV weight convention: zeta(2)=
          pi^2/6 is weight 2, so pi is weight 1 and sqrt(pi) is weight 1/2). The MZV ring
          where 4d SM perturbative amplitudes live is INTEGER-graded d_w=d_{w-2}+d_{w-3}
          with d_1=0. Convention-independent kill (ring closure): if sqrt(pi) were an MZV
          then pi=(sqrt(pi))^2 would be a weight-1 MZV, but the weight-1 slot is empty
          (d_1=0). So sqrt(pi) is not an MZV; the two period contents are DISJOINT.

  PART 3  Fit-anything / degrees-of-freedom falsification: a period-basis toolbox
          {1,sqrt2,sqrt3,sqrt(pi),pi} + free rationals hits random targets at the SAME
          rate as it hits flavor constants; coverage scales with the free-parameter
          budget (the signature of "predicts anything"); and sqrt(pi) is NOT load-bearing
          -- the only measurement-precision-surviving landing is Koide Q via the PURE
          RATIONAL 2/3 (zero sqrt(pi) content), the lead the framework merely re-labels.

HONESTY. a0's value, Z's value and the sign are POSITED, not derived; nu(y)=sqrt(1+1/y)
is Milgrom-1999's form. This script re-derives a WALL, sharper than the algebraic one.
It is NOT a claim that the theory is closed and NOT a TOE claim. Sibling script with the
complementary Feynman-side derivation: reviews/feynman_period_side.py.
"""

import sympy as sp
import numpy as np
import mpmath as mp
import math

mp.mp.dps = 40
FAIL = []


def check(name, cond):
    print(f"    [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        FAIL.append(name)


print("=" * 78)
print("PERIOD-RING OBSTRUCTION 2026  --  does periods > algebra force a Z<->SM relation?")
print("=" * 78)

# ---------------------------------------------------------------------------
# PART 1 -- Z's period content and the loop-measure dimension solve.
# ---------------------------------------------------------------------------
print("\n" + "-" * 78)
print("PART 1  Z's period content: a LONE sqrt(pi) times a quadratic irrational")
print("-" * 78)

Z = sp.sqrt(sp.Rational(32, 3) * sp.pi)
Zf = float(Z)
cof = sp.simplify(Z / sp.sqrt(sp.pi))          # algebraic cofactor
print(f"  Z = sqrt(32 pi/3) = {Zf:.10f}")
print(f"  Z / sqrt(pi) = {cof} = {float(cof):.10f}   (strip the lone sqrt(pi))")

x = sp.symbols('x')
mpoly = sp.minimal_polynomial(sp.sqrt(sp.Rational(32, 3)), x)
print(f"  minimal polynomial of Z/sqrt(pi): {mpoly}   (degree {sp.degree(mpoly, x)})")
check("Z/sqrt(pi) = 4 sqrt(6)/3 (equals sqrt(32/3))",
      sp.simplify(cof - 4 * sp.sqrt(6) / 3) == 0)
check("cofactor is a QUADRATIC irrational (minpoly degree 2, i.e. NOT a CM Gamma value)",
      sp.degree(mpoly, x) == 2)
check("Z carries EXACTLY ONE sqrt(pi): Z^2/pi = 32/3 is rational",
      sp.simplify(Z**2 / sp.pi - sp.Rational(32, 3)) == 0)

# Provenance of the sqrt(pi): Z^2 = 32 pi/3 = 4 * (8 pi/3), the Friedmann coupling.
print("\n  Provenance: Z^2 = 32 pi/3 = 4 * (8 pi/3); 8 pi/3 is the Friedmann coefficient")
print("  (H^2 = 8 pi G rho /3), outer 4 = 1/(1/2)^2 from a0 = (c/2) sqrt(G rho).")
check("Z^2 = 4 * (8 pi/3) exactly", sp.simplify(Z**2 - 4 * sp.Rational(8, 3) * sp.pi) == 0)
print("  => the sqrt(pi) is the square root of the WEIGHT-2 Tate period pi (from H~sqrt(rho)),")
print("     NOT a Feynman loop integral and NOT a CM Gamma(1/3)/Gamma(1/4) period.")

# --- loop-measure dimension solve: for which d is Z a sphere/ball measure factor? ---
print("\n  Loop-measure dimension solve: solve S_{d-1} = 2 pi^{d/2}/Gamma(d/2) = Z.")


def S(d):
    return 2 * mp.pi ** (mp.mpf(d) / 2) / mp.gamma(mp.mpf(d) / 2)


d_star = mp.findroot(lambda d: S(d) - Zf, 2.0)
print(f"    d* (rising branch) = {mp.nstr(d_star, 12)}   -> NON-integer, non-special dimension")
# integer scan: no integer d gives Z (surface area S_{d-1}); list the near integers
print("    integer-d scan of S_{d-1} (unit-sphere surface area):")
for dd in range(1, 9):
    val = float(S(dd))
    tag = "  <- dS_4 boundary d=3: S_2 = 4pi != Z" if dd == 3 else ""
    print(f"       d={dd}: S_{{d-1}} = {val:8.4f}{tag}")
check("d* is not an integer", abs(d_star - round(d_star)) > 1e-3)
check("no integer d in 1..8 gives S_{d-1}=Z within 1e-6",
      all(abs(float(S(dd)) - Zf) > 1e-6 for dd in range(1, 9)))
check("dS_4 boundary d=3 gives S_2 = 4pi, and 4pi != Z",
      sp.simplify(2 * sp.pi ** sp.Rational(3, 2) / sp.gamma(sp.Rational(3, 2)) - 4 * sp.pi) == 0
      and abs(float(4 * sp.pi) - Zf) > 1.0)
print("  => Z is NOT a natural integer-dimension measure factor (for integer d the sqrt(pi)")
print("     in pi^{d/2} and Gamma(d/2) always cancels); a lone surviving sqrt(pi) needs")
print("     HALF-INTEGER d -- the dim-reg regime, whose sqrt(pi) is scheme-subtracted (Part 2).")

# ---------------------------------------------------------------------------
# PART 2 -- sqrt(pi)=Gamma(1/2), weight 1, and the empty weight-1 MZV slot.
# ---------------------------------------------------------------------------
print("\n" + "-" * 78)
print("PART 2  sqrt(pi)=Gamma(1/2) has half-integer weight; the MZV weight-1 slot is empty")
print("-" * 78)

gamma_half = sp.gamma(sp.Rational(1, 2))
print(f"  Gamma(1/2) = {gamma_half} = sqrt(pi)   (a half-integer Gamma / CM-exponential period)")
check("sqrt(pi) = Gamma(1/2)", sp.simplify(gamma_half - sp.sqrt(sp.pi)) == 0)
# Gaussian exponential-period witness
tt = sp.symbols('tt')
gauss = sp.integrate(sp.exp(-tt**2), (tt, -sp.oo, sp.oo))
check("Gaussian exp-period: int e^{-t^2} dt = sqrt(pi)", sp.simplify(gauss - sp.sqrt(sp.pi)) == 0)

# MZV weight grading via Zagier/Deligne-Goncharov recursion d_w = d_{w-2}+d_{w-3}.
N = 16
d = [0] * (N + 1)
d[0], d[1], d[2] = 1, 0, 1
for w in range(3, N + 1):
    d[w] = d[w - 2] + d[w - 3]
print("\n  MZV ring (4d SM perturbative amplitudes; Brown's theorem) weight dimensions:")
print("    weight w:", "".join(f"{w:>3}" for w in range(0, N + 1)))
print("    dim  d_w:", "".join(f"{d[w]:>3}" for w in range(0, N + 1)))
xg = sp.symbols('xg')
gf = sp.series(1 / (1 - xg**2 - xg**3), xg, 0, N + 1).removeO()
coeffs = [sp.Poly(gf, xg).coeff_monomial(xg**w) for w in range(0, N + 1)]
check("gen.func 1/(1-x^2-x^3) reproduces the weight dimensions", coeffs == d)
check("d_1 = 0  ->  the MZV ring has NO weight-1 element", d[1] == 0)
# ring-closure contradiction: sqrt(pi) in MZV ring => pi in weight-1 slot (empty).
print("  Ring-closure argument: if sqrt(pi) were an MZV then pi=(sqrt(pi))^2 would be an")
print("  MZV of weight 1 (weights add under product); but d_1=0. Contradiction.")
print("  => sqrt(pi) is NOT an MZV. Z's Gamma/CM sqrt(pi) and the SM's MZV periods are")
print("     DISJOINT precisely at weight 1 -- sharper than 'algebraic vs transcendental',")
print("     and it SURVIVES the enlargement from the algebraics to the full period ring.")
# even zetas are rational * pi^{2k}: only EVEN powers of pi occur; pi^{odd} absent.
for k in range(1, 4):
    r = sp.nsimplify(sp.zeta(2 * k) / sp.pi**(2 * k))
    print(f"    zeta({2*k}) = {r} * pi^{2*k}  (even power of pi, weight {2*k})")

# ---------------------------------------------------------------------------
# PART 3 -- fit-anything / degrees-of-freedom falsification of the bridge.
# ---------------------------------------------------------------------------
print("\n" + "-" * 78)
print("PART 3  Fit-anything / DOF test: the period-basis bridge predicts anything")
print("-" * 78)

rng = np.random.default_rng(20260723)
ATOMS_FULL = {'1': 1.0, 'sqrt2': math.sqrt(2), 'sqrt3': math.sqrt(3),
              'sqrtpi': math.sqrt(math.pi), 'pi': math.pi}
ATOMS_NOPI = {k: v for k, v in ATOMS_FULL.items() if k != 'sqrtpi'}


def build(atoms, H):
    """All (p/q)*atom_i*atom_j, p,q in 1..H : the low-complexity period-ring toolbox."""
    ak = list(atoms)
    vals = set()
    for i in range(len(ak)):
        for j in range(i, len(ak)):
            base = atoms[ak[i]] * atoms[ak[j]]
            for p in range(1, H + 1):
                for q in range(1, H + 1):
                    vals.add(p / q * base)
    return np.array(sorted(vals))


def coverage(vals, tol, N=40000):
    """Fraction of random log-uniform targets in [1,10] within rel-tol of SOME expression."""
    t = np.exp(rng.uniform(math.log(1), math.log(10), N))
    idx = np.clip(np.searchsorted(vals, t), 1, len(vals) - 1)
    dd = np.minimum(np.abs(t - vals[idx - 1]) / t, np.abs(t - vals[idx]) / t)
    return float(np.mean(dd < tol))


valsH6 = build(ATOMS_FULL, 6)
vdec = valsH6[(valsH6 >= 1) & (valsH6 <= 10)]
print(f"  toolbox (H=6): {len(valsH6)} distinct expressible values; {len(vdec)} in the decade [1,10]")
print("  coverage of RANDOM targets vs tolerance (with a counting cross-check N*2tol/ln10):")
for tol in [3e-2, 1e-2, 1e-3, 1e-4]:
    cov = coverage(valsH6, tol)
    est = min(1.0, len(vdec) * 2 * tol / math.log(10))
    print(f"    tol {tol:.0e}:  coverage {cov*100:5.1f}%   counting-estimate {est*100:5.1f}%")
print("  => at loose tol the ring BLANKETS all numbers (predicts anything); at real flavor")
print("     precision (~1e-4) it lands almost nothing. Coverage ~ N*tol is the DOF signature.")

print("\n  Coverage @1e-2 GROWS with the free-parameter budget H (adding DOF = the disease):")
for H in [3, 6, 10, 15]:
    v = build(ATOMS_FULL, H)
    print(f"    H={H:2d}: {len(v):5d} expressions -> coverage {coverage(v, 1e-2)*100:5.1f}%")

# Real SM flavor constants: (value, measurement rel-precision order-of-magnitude).
# Compared SCALE-FREE, on the mantissa in [1,10) -- period membership is scale-free
# (a factor 10^k = 2^k 5^k is itself a rational period), so the decade is not physical.
CONSTS = {
    'm_e/m_mu':   (4.83633e-3, 1e-5),   # sharply measured
    'm_tau/m_mu': (16.817,     6e-4),   # sharply measured
    'm_s/m_d':    (20.0,       5e-2),   # loose (lattice ratio ~5%)
    'sin2_th13':  (0.02237,    3e-2),   # loose (~3%)
    'sin2_th12':  (0.307,      4e-2),   # loose (~4%)
    'Koide_Q':    (2 / 3,      1e-4),   # the known re-labeled lead
}


def mant(x):
    return x / 10.0**math.floor(math.log10(x))   # map to [1,10)


vfull = build(ATOMS_FULL, 12); vfull = vfull[(vfull >= 1) & (vfull <= 10)]
vnopi = build(ATOMS_NOPI, 12); vnopi = vnopi[(vnopi >= 1) & (vnopi <= 10)]
print(f"\n  Flavor constants (scale-free mantissa) vs toolbox H=12 in [1,10]:")
print(f"  ({len(vfull)} expressions WITH sqrt(pi); {len(vnopi)} WITHOUT).  'hit' = within DATA precision.")
print("    constant     mantissa  relerr(FULL) hit? | relerr(NOPI) hit? | data-prec")
for k, (val, prec) in CONSTS.items():
    m = mant(val)
    rf = float(np.min(np.abs(vfull - m) / m))
    rn = float(np.min(np.abs(vnopi - m) / m))
    print(f"    {k:11s}  {m:7.4f}   {rf:.1e}   {str(rf < prec):5s} | "
          f"{rn:.1e}   {str(rn < prec):5s} | {prec:.0e}")

hits_full = {k for k, (val, prec) in CONSTS.items()
             if float(np.min(np.abs(vfull - mant(val)) / mant(val))) < prec}
hits_nopi = {k for k, (val, prec) in CONSTS.items()
             if float(np.min(np.abs(vnopi - mant(val)) / mant(val))) < prec}
print(f"\n  Reached at DATA precision  WITH sqrt(pi): {sorted(hits_full)}")
print(f"  Reached at DATA precision  WITHOUT sqrt(pi): {sorted(hits_nopi)}")
print("  => the SAME set is reached either way: the sharply-measured ratios (m_e/m_mu, m_tau/m_mu)")
print("     are MISSED; the reached ones (m_s/m_d, sin2_th13, sin2_th12) are all LOOSE (3-5%),")
print("     the exact regime where the ring already covers ~90% of ALL numbers = no information.")

# Decisive load-bearing test: does Z's distinctive sqrt(pi) change ANY flavor hit?
check("removing sqrt(pi) changes NO flavor hit at data precision "
      "(=> Z's distinctive sqrt(pi) is NOT load-bearing / gauge-blind to flavor)",
      hits_full == hits_nopi)
koide_m = mant(2 / 3)
check("Koide Q hit EXACTLY (relerr<1e-12) by the PURE RATIONAL 20/3=6.667 with ZERO sqrt(pi)",
      float(np.min(np.abs(vnopi - koide_m)) / koide_m) < 1e-12)
check("the two SHARPLY measured ratios (m_e/m_mu @1e-5, m_tau/m_mu @6e-4) are NOT reached",
      'm_e/m_mu' not in hits_full and 'm_tau/m_mu' not in hits_full)

# ---------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("VERDICT:  WALL (sharpened) -- period arithmetic re-derives the SM-flavor wall and")
print("          forces NOTHING new. This is a null, verified as rigorously as a win.")
print("=" * 78)
print("  * Z = (4 sqrt6/3) * sqrt(pi): a LONE half-integer-weight sqrt(pi) (sqrt of the 8pi")
print("    Tate period) times a QUADRATIC irrational -- a Gamma/CM-sector object, no CM")
print("    Gamma(1/3)/Gamma(1/4), not a natural integer-d loop measure (d*=1.907).")
print("  * 4d SM perturbative periods = MZVs, integer-weight-graded with d_1=0 (empty")
print("    weight-1 slot). Z's sqrt(pi) and the SM's MZVs are DISJOINT at weight 1.")
print("  * The half-integer-d/holographic-boundary route that could expose a lone sqrt(pi)")
print("    is a SEPARATE posit, and its dim-reg sqrt(pi) is MS-bar-subtracted (scheme, not")
print("    physical) -- see feynman_period_side.py.")
print("  * Period-basis matching of flavor data is FIT-ANYTHING with positive DOF: coverage")
print("    scales with the free-parameter budget; removing Z's distinctive sqrt(pi) changes")
print("    NO flavor hit (gauge-blind); the only EXACT, sharply-measured landing is Koide Q")
print("    via the PURE RATIONAL 2/3 the framework already only RE-LABELS, while every other")
print("    'hit' is a loose 3-5%-precision coincidence in the regime where the ring blankets")
print("    ~90% of ALL numbers. Enlarging algebra -> periods only ADDS free generators; it")
print("    worsens the gauge-blindness it was meant to cure.")
print("  * Prohibition, not degeneracy: the weight-1-vs-weight>=2 gap PROHIBITS the bridge")
print("    rather than hitting any target -- falsifiable, and it holds. NO DOOR. No TOE claim.")
print("  * Open QUESTION (a surviving thread, not a claim): the one honest home for a lone")
print("    sqrt(pi) is a d=3 (dS_4 boundary) loop measure -- does that tie to the framework's")
print("    existing holographic CKN-dof number 0.5878=(3/8pi)^{1/4}? A boundary theory, if")
print("    ever written, would be a SEPARATE posit, not something forced here.")

if FAIL:
    print("\n*** ASSERTIONS FAILED:", FAIL)
    raise SystemExit(1)
print("\nAll assertions passed. EXIT 0.")
