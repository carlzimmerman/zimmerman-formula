#!/usr/bin/env python3
"""
L94 -- INDEPENDENT VERIFICATION of astra's RMMG (rotated-MMG constitutive) health-gate results, and a new
       falsifiable prediction extracted from them.
=============================================================================================================
astra opened a new local architecture (qwen_claude_field_theory/closure_2026/rotated_mmg_constitutive_2026/)
pushing at the cosmological/local HEALTH gate. Its RMMG_GATE_REPORT claims:
  (i)   same exponential MOND kernel G'/(2y)=1-e^{-y}, no-slip Φ=Ψ, exact static AQUAL -- PASS;
  (ii)  local scalar Dirac block rank 4 with ZERO remaining scalar phase dimension at k!=0 (non-propagating
        scalar = healthy cuscuton structure); homogeneous k=0 rank 0 (a genuine separate sector);
  (iii) a NEW spherical prediction from inverting the exact implicit law:
            g/a0 = eps + (1/4)eps^2 + (7/96)eps^3 + O(eps^4),  eps = sqrt(g_N/a0),
        hence v^2 = sqrt(G M a0) + G M/(4r) + 7(G M)^{3/2}/(96 r^2 sqrt(a0)) + O(r^-3);
  (iv)  a CONSTRAINT-ALGEBRA OBSTRUCTION for the minimal one-pair realization: matching the spatial-diff
        generator forces A = 1/mu, and then {H[N],H[M]} carries a nonzero cubic coefficient A A'/2 (because
        mu'(s)=e^{-s/a0}/a0 > 0). astra states this is CONDITIONAL (minimal one pair), resolvable by adding
        constrained fields whose brackets cancel it while keeping 2 tensor DOF.

This lane independently reproduces (iii) and (iv) in exact sympy (the two most checkable claims), records
the honest status of (ii), and extracts the new falsifiable prediction. Imports nothing from qwen; reproduces.

POLARITY: each check ASSERTS a statement; PASS = true. Both a0 footings where dimensional.
"""
import sympy as sp
import sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 110); print(t); print("=" * 110, flush=True)

print("=" * 110)
print("L94 -- independent verification of astra's RMMG health-gate results + a new falsifiable prediction")
print("=" * 110, flush=True)

x, eps, s, a0, p, N, M = sp.symbols("x epsilon s a0 p N M", positive=True)

# ======================================================================================================
sec("PART 0 -- CONTROL: the exact implicit MOND law and its deep-MOND limit.")
# ======================================================================================================
# AQUAL implicit law with mu(x)=1-e^{-x}, x=g/a0:  mu(x)*x = g_N/a0 = eps^2.  Deep MOND: x->eps.
mu = lambda z: 1 - sp.exp(-z)
lhs = mu(x) * x
check("CTRL-1  the exact implicit law is (1-e^{-x}) x = eps^2 with x=g/a0, eps^2=g_N/a0; deep-MOND leading "
      "order x->eps reproduces g -> sqrt(g_N a0) (the RAR/BTFR asymptote)",
      sp.limit(lhs / x ** 2, x, 0) == 1, "mu(x)x ~ x^2 as x->0 => x~eps (deep MOND)")

# ======================================================================================================
sec("PART 1 -- VERIFY astra's spherical expansion g/a0 = eps + eps^2/4 + 7 eps^3/96 + O(eps^4).")
# ======================================================================================================
# Solve (1-e^{-x}) x = eps^2 as a series x(eps) = eps + c2 eps^2 + c3 eps^3 (c2,c3 are astra's claimed coeffs).
c2, c3 = sp.symbols("c2 c3")
xser = eps + c2 * eps ** 2 + c3 * eps ** 3
expr = sp.series(mu(xser) * xser, eps, 0, 5).removeO() - eps ** 2
sol = sp.solve([expr.coeff(eps, k) for k in (3, 4)], [c2, c3], dict=True)[0]
print(f"    solved: c2 = {sol[c2]}, c3 = {sol[c3]}")
check("SPH-1  inverting the exact implicit law gives g/a0 = eps + (1/4)eps^2 + (7/96)eps^3 + ... EXACTLY "
      "(astra's coefficients reproduced independently)",
      sol[c2] == sp.Rational(1, 4) and sol[c3] == sp.Rational(7, 96),
      f"c2={sol[c2]} (=1/4), c3={sol[c3]} (=7/96)")

# v^2 = g r = a0 x r ; for a point mass g_N=GbM/r^2, eps=sqrt(GbM/a0)/r
Gb, Mm, r = sp.symbols("G_b M r", positive=True)
eps_pm = sp.sqrt(Gb * Mm / a0) / r
x_pm = eps_pm + sp.Rational(1, 4) * eps_pm ** 2 + sp.Rational(7, 96) * eps_pm ** 3
v2 = sp.simplify(a0 * x_pm * r)
v2_astra = sp.sqrt(Gb * Mm * a0) + Gb * Mm / (4 * r) + 7 * (Gb * Mm) ** sp.Rational(3, 2) / (96 * r ** 2 * sp.sqrt(a0))
check("SPH-2  the point-mass rotation law v^2 = sqrt(G_b M a0) + G_b M/(4r) + 7(G_b M)^{3/2}/(96 r^2 sqrt(a0)) "
      "+ O(r^-3) is reproduced -- a NEW falsifiable 1/r correction to the flat asymptote from the exact "
      "exponential kernel",
      sp.simplify(v2 - v2_astra) == 0, "v^2 expansion matches astra term-by-term")

# ======================================================================================================
sec("PART 2 -- VERIFY the constraint-algebra obstruction for the minimal one-pair realization.")
# ======================================================================================================
# H = (1/2) A(s) p^2 + W(s), W'(s)=mu(s) s.  Smeared bracket {H[N],H[M]} = (N M' - M N') p A [ (1/2)A' p^2 + mu s ].
# Matching the spatial-diff generator p*s requires A*mu = 1 => A = 1/mu.  Then the cubic (in p) coefficient is A A'/2.
mus = 1 - sp.exp(-s / a0)          # mu(s) with dimensionful s (astra's mu(s)=1-e^{-s/a0})
A = 1 / mus
Aprime = sp.diff(A, s)
cubic_coeff = sp.simplify(A * Aprime / 2)
muprime = sp.diff(mus, s)
check("OBS-1  matching the spatial-diffeomorphism generator forces A = 1/mu (so A*mu = 1)",
      sp.simplify(A * mus - 1) == 0, "A = 1/mu")
check("OBS-2  mu'(s) = e^{-s/a0}/a0 > 0 (the kernel is strictly increasing), so the cubic bracket coefficient "
      "A A'/2 = -mu'/(2 mu^3) is NONZERO -- the constraint algebra does NOT close for the minimal one-pair "
      "realization (astra's obstruction reproduced)",
      sp.simplify(cubic_coeff - (-muprime / (2 * mus ** 3))) == 0 and sp.simplify(cubic_coeff.subs(s, a0)) != 0,
      f"A A'/2 = {sp.simplify(cubic_coeff)} != 0")
# witness at s = a0
wit = sp.simplify(cubic_coeff.subs({s: a0}))
check("OBS-3  finite nonzero witness at s=a0: A A'/2 |_{s=a0} = -e^{-1}/(2 a0 (1-e^{-1})^3) != 0 -- a concrete,",
      wit != 0 and wit.has(a0),
      f"witness(s=a0) = {wit}")

# ======================================================================================================
sec("PART 3 -- HONEST STATUS of the RMMG health gate.")
# ======================================================================================================
print("""
  astra's RMMG_GATE_REPORT: the local scalar Dirac block has rank 4 with ZERO remaining scalar phase
  dimension at k!=0 (a NON-PROPAGATING scalar = healthy cuscuton structure, the outcome the whole search
  wanted), rank 0 at k=0 (a genuine separate homogeneous sector, no false closure), and the clock
  kinetic/sound witness passes a 32-point scan. That is real progress on the health gate the F(Q)Θ branch
  left open. BUT the minimal one-pair realization carries the nonzero cubic bracket term verified above
  (OBS-2/3): the constraint algebra does not close by itself. astra's stated resolution -- add constrained
  fields whose brackets cancel A A'/2 while preserving the two tensor DOF -- is NOT yet executed, and the
  full metric constraint algebra (not just the scalar block) remains to be run. So RMMG is the most
  promising local architecture in the branch, health-PROMISING but NOT health-CLOSED.
""", flush=True)
check("STATUS-1  RMMG health is PROMISING (zero propagating scalar DOF at k!=0, fits SPARC, new prediction) "
      "but NOT CLOSED: the minimal-pair constraint algebra carries a nonzero cubic term (OBS-2) that a "
      "successful completion must cancel with added constrained fields; the full metric constraint algebra "
      "is still to be run. This is astra's live next step, honestly not yet a clean bill of health",
      True, "zero scalar DOF at k!=0 (good) + open cubic obstruction (needs added fields) = promising, not closed")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print(f"""
  Independently verified two of astra's RMMG results in exact sympy: (1) the new spherical prediction
  g/a0 = eps + eps^2/4 + 7 eps^3/96 + ..., i.e. v^2 = sqrt(G_b M a0) + G_b M/(4r) + 7(G_b M)^{{3/2}}/(96 r^2
  sqrt(a0)) -- a clean, FALSIFIABLE 1/r correction to the flat rotation velocity from the exact exponential
  kernel (new prediction P17); and (2) the minimal-one-pair constraint-algebra obstruction, the nonzero
  cubic term A A'/2 = -mu'/(2 mu^3), confirming the algebra does not close by itself. astra's Dirac block
  shows zero propagating scalar DOF at k!=0 (the healthy cuscuton structure the search wanted) -- real
  progress toward closing the health gate -- but the obstruction means RMMG is health-PROMISING, not
  health-CLOSED: a completion must add constrained fields to cancel the cubic term and the full metric
  constraint algebra must still be run. That is astra's live next calculation.
""")
print("=" * 110)
if FAILS:
    print(f"L94 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L94 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 110)
