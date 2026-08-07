#!/usr/bin/env python3
r"""mi_r_admissibility_bound_2026.py -- does ADMISSIBILITY bound the crossover ratio r, and if so, where?

*** WITHDRAWN IN PART, 2026-08-07, one day after commit -- by mi_psi_search_r2Z_2026.py (27/27). ***
The interpretive claims of checks B2 and C1 ("neither live coefficient is reachable", "admissibility EXCLUDES
both proposals") are WITHDRAWN. The seven-shape ceiling of 9.0168 was a MENU ARTEFACT: the true single-scale
ceiling is exactly 9, and a psi carrying a SECOND scale escapes it entirely -- sup r = +INFINITY, with explicit
admissible psi exhibited at r = 2Z, 4 pi, 100, 1e4 and 1e6, strict margins, 4x-refinement-stable, mpmath 50-dps
cross-checked. So r = 2Z (kappa = 1/2) and r = 4 pi are BOTH admissible. The flip side is equally final: a
constraint that admits every r in [0, infinity) derives NOTHING -- the admissibility route to deriving ANY
coefficient is closed by theorem, and the price of reaching r > 9 is a second scale tuned to a_0. The seven-shape
COMPUTATION below remains correct as a computation about that menu, and this file's own scope caveat ("seven
shapes is not a proof; a single admissible psi reaching 2Z overturns this") is exactly what happened.

THE QUESTION. mi_crossover_master_formula_2026.py (14/14) established that for any inertia functional of the
local de Sitter-Unruh temperature, I(a) = f(T(a)) - f(T_GH) with T = sqrt(a^2+H^2)/2pi, the MOND crossover is
    q = a_0/(c H_Lambda) = 2 c1p / f'(T_GH) = 2/r,    r = f'(T_GH)/c1p,   c1p = lim_{T->inf} f(T)/T
and concluded that r is FREE, so the class does not fix the coefficient. That conclusion assumed EVERY r yields
an admissible theory. This script tests that assumption -- the one thing the master-formula paper did not check.

WHY IT MATTERS. If admissibility bounds r, the coefficient is DERIVED, not fitted. Three possible outcomes,
all decisive: r_max = 2Z = 11.577620 would derive kappa = 1/2; r_max = 4 pi = 12.566371 would derive the
conventional 2 pi a_0 ~ c H_Lambda; r_max = 1 would derive Milgrom 1999's a_0 = 2 c H_Lambda.

THE SETUP, in the variable that makes it clean. Put s = T - T_GH >= 0. Then
    a(s) = 2 pi sqrt(s (s + 2 T_GH)),    I = F(s) = f(T_GH + s) - f(T_GH),   F(0) = 0,
    r = F'(0)/F'(inf),   c1 = c1p/2pi,   c1 a = c1p w(s) with w(s) = sqrt(s (s + 2 T_GH)).
Write F'(s) = c1p [1 + (r-1) psi(s)] with psi(0) = 1, psi(inf) = 0, psi decreasing. Then TWO conditions:
  (A1) mu <= 1 everywhere.  mu = F/(c1p w), and at large s, F -> c1p s + C with C = (r-1) c1p Int psi, while
       w -> s + T_GH. So mu <= 1 requires  (r-1) Int_0^inf psi(s) ds <= T_GH.  [an OFFSET condition]
  (A2) mu MONOTONE increasing (else the kernel is not single-valued and the RAR carries a wiggle):
       F'(s) s (s + 2 T_GH)  >=  F(s) (s + T_GH)   for all s > 0.
Both are derived here, not assumed. (A1) alone is satisfiable for any r by making psi decay fast; the question
is whether (A2) can be satisfied at the same time.

CREDIT. nu = sqrt(1+1/y) and the temperature balance are Milgrom 1999 PLA 253:273 eqs 6-9 (he fixes
a_0_hat = 2 c H_Lambda, i.e. r = 1); eqs 10-11 of the same paper exhibit a SECOND functional with r = 2, and
Milgrom 2008 (arXiv:0801.3133) sec 7.3.1 states in words that the coefficient mismatch "isn't necessarily
meaningful ... would just point to a different effective mu(x)" -- i.e. Milgrom himself noted the family. The
5-acceleration interpretation is Deser & Levin 1997 CQG 14:L163; the temperature sqrt(a^2+Lambda/3)/2pi is
Narnhofer, Peter & Thirring 1996 IJMPB 10:1507. a_lambda = c^2 sqrt(Lambda/3) is Milgrom 1994 Ann.Phys. 229:384.

kappa = 1/2 is FITTED, NOT DERIVED, and nothing below changes that.
Exit 0 = every check held. No check(True); every condition below can fail.
"""
from __future__ import annotations
import math, sys
import numpy as np

ok: list[tuple[bool, str]] = []
def check(c, m):
    c = bool(c); ok.append((c, m)); print(f"  [{'OK' if c else 'FAIL'}] {m}"); return c
def banner(t):
    print("\n" + "=" * 104); print(f"  {t}"); print("=" * 104)

Z = 2*math.sqrt(8*math.pi/3); TWOZ = 2*Z; FOURPI = 4*math.pi; TG = 1.0/(2*math.pi)

# --- psi shapes: psi(0)=1, decreasing, integrable. delta is the transition scale. -------
SHAPES = {
    "exp(-s/d)":        (lambda s, d: np.exp(-s/d),                 lambda d: d),
    "exp(-(s/d)^2)":    (lambda s, d: np.exp(-(s/d)**2),            lambda d: d*math.sqrt(math.pi)/2),
    "sech(s/d)":        (lambda s, d: 1.0/np.cosh(s/d),             lambda d: d*math.pi/2),
    "1/(1+(s/d)^2)":    (lambda s, d: 1.0/(1.0+(s/d)**2),           lambda d: d*math.pi/2),
    "(1+s/d)^-2":       (lambda s, d: (1.0+s/d)**-2.0,              lambda d: d),
    "(1+s/d)^-3":       (lambda s, d: (1.0+s/d)**-3.0,              lambda d: d/2),
    "1/(1+(s/d)^4)":    (lambda s, d: 1.0/(1.0+(s/d)**4),           lambda d: d*math.pi/(4*math.sin(math.pi/4))),
}

def admissible(r, delta, shape, n=600001, smax_mult=1e7):
    """Return (ok, min_of_A2_margin, max_mu). c1p = 1 WLOG (q is invariant under f -> alpha f + b)."""
    psi, Ipsi = SHAPES[shape]
    if (r-1.0)*Ipsi(delta) > TG:                     # (A1) offset condition, analytic
        return False, float("nan"), float("inf")
    s = np.logspace(math.log10(delta*1e-6), math.log10(max(smax_mult*delta, 1e6)), n)
    Fp = 1.0 + (r-1.0)*psi(s, delta)                 # F'(s)
    F  = np.concatenate(([0.0], np.cumsum(0.5*(Fp[1:]+Fp[:-1])*np.diff(s))))
    w  = np.sqrt(s*(s+2*TG))
    mu = F/w                                          # c1p = 1
    marg = Fp*s*(s+2*TG) - F*(s+TG)                   # (A2): must be >= 0
    return (marg[1:].min() >= -1e-12) and (mu.max() <= 1.0+1e-9), marg[1:].min(), mu.max()

def max_r(shape, rlo=1.0, rhi=1e4):
    """Largest r admissible for this shape, optimising delta at each r."""
    def any_delta(r):
        for d in np.logspace(-9, 2, 220):
            if admissible(r, d, shape)[0]:
                return True
        return False
    if not any_delta(1.0 + 1e-9):
        return float("nan")
    lo, hi = rlo, rhi
    if any_delta(hi):
        return float("inf")
    for _ in range(45):
        mid = math.sqrt(lo*hi)
        if any_delta(mid): lo = mid
        else: hi = mid
    return lo

banner("A  THE CONTROL: r = 1 (Milgrom 1999, f = T) must be admissible")
s = np.logspace(-9, 9, 600001); Fp = np.ones_like(s); F = s.copy()
w = np.sqrt(s*(s+2*TG)); mu = F/w; marg = Fp*s*(s+2*TG) - F*(s+TG)
print(f"  r = 1:  min (A2) margin = {marg.min():.6e}   max mu = {mu.max():.12f}")
check(marg.min() >= -1e-15 and mu.max() <= 1.0+1e-12,
      f"A1 r = 1 satisfies BOTH conditions exactly: the (A2) margin is s(s+2T_GH) - s(s+T_GH) = s T_GH >= 0 "
      f"identically, and max mu = {mu.max():.12f} <= 1. So Milgrom's own f = T is admissible, which anchors the "
      f"test on the one case whose answer is known independently")

banner("B  IS r BOUNDED? maximum admissible r over seven psi shapes, delta optimised")
print(f"  {'psi shape':<20}{'max admissible r':>20}{'vs 2Z = 11.5776':>18}{'vs 4pi = 12.5664':>19}")
print("  " + "-" * 77)
res = {}
for nm in SHAPES:
    rm = max_r(nm); res[nm] = rm
    v2 = "-" if not np.isfinite(rm) else f"{rm/TWOZ:.4f}"
    v4 = "-" if not np.isfinite(rm) else f"{rm/FOURPI:.4f}"
    print(f"  {nm:<20}{rm:>20.6f}{v2:>18}{v4:>19}")
best = max(v for v in res.values() if not math.isnan(v))
check(all(not math.isnan(v) for v in res.values()),
      f"B1 every shape admits SOME r > 1, so the class is not rigid at r = 1 -- the sharp-drop argument that "
      f"suggested r = 1 was uniquely admissible does NOT survive a general search. Best over shapes: "
      f"r_max = {best:.6f}")
check(best < TWOZ and best < FOURPI and best > 1.0,
      f"B2 *** the maximum admissible r over all seven shapes is {best:.6f}, which is BELOW both 2Z = "
      f"{TWOZ:.6f} and 4 pi = {FOURPI:.6f}. So of the shapes tested, NEITHER live coefficient is reachable: "
      f"kappa = 1/2 needs r = 2Z = {TWOZ/best:.3f}x the largest admissible r found, and the conventional "
      f"2 pi a_0 ~ c H_Lambda needs {FOURPI/best:.3f}x. This check FAILS if any shape reaches 2Z ***")

banner("C  THE VERDICT ON r = 2Z AND r = 4 pi SPECIFICALLY")
for label, rv in (("2Z  (kappa = 1/2)", TWOZ), ("4 pi (conventional)", FOURPI), ("2   (Milgrom 1999 eq.10)", 2.0)):
    hits = [(d, admissible(rv, d, nm)) for nm in SHAPES for d in np.logspace(-9, 2, 220)]
    good = [(d, nm) for (d, (o, _, _)), nm in zip(hits, [nm for nm in SHAPES for _ in range(220)]) if o]
    print(f"  r = {rv:>10.6f}  {label:<26} admissible for {len(good):>4} (shape, delta) pairs")
    if good: print(f"      e.g. delta = {good[0][0]:.3e}")
adm2Z = any(admissible(TWOZ, d, nm)[0] for nm in SHAPES for d in np.logspace(-9, 2, 220))
adm4p = any(admissible(FOURPI, d, nm)[0] for nm in SHAPES for d in np.logspace(-9, 2, 220))
check((not adm2Z) and (not adm4p),
      f"C1 *** r = 2Z (kappa = 1/2) is NOT ADMISSIBLE over any of the 1540 (shape, delta) pairs tested, and "
      f"neither is r = 4 pi. Milgrom 1999's own second coefficient r = 2 IS admissible, in 1133 of them. So "
      f"admissibility is not merely a constraint -- within the shapes tested it EXCLUDES both live coefficient "
      f"proposals and admits Milgrom's. This check FAILS the moment any shape admits 2Z, which is exactly the "
      f"result that would put kappa = 1/2 back in play ***")

banner("C2  REFINEMENT -- an exclusion claim is worthless if it moves with the grid")
rm_lo = max_r("(1+s/d)^-2")
_orig = admissible
def admissible(r, delta, shape, n=2400001, smax_mult=1e8):   # 4x the grid, 10x the domain
    return _orig(r, delta, shape, n=n, smax_mult=smax_mult)
rm_hi = max_r("(1+s/d)^-2")
admissible = _orig
print(f"  best shape (1+s/d)^-2:  r_max = {rm_lo:.6f} at n=6.0e5, smax=1e7*delta")
print(f"                          r_max = {rm_hi:.6f} at n=2.4e6, smax=1e8*delta   (shift {abs(rm_hi/rm_lo-1)*100:.4f}%)")
check(abs(rm_hi/rm_lo - 1) < 0.05 and rm_hi < TWOZ,
      f"C2 refining the grid 4x and the domain 10x moves r_max by {abs(rm_hi/rm_lo-1)*100:.4f}%, far below the "
      f"{100*(TWOZ/rm_lo-1):.1f}% gap to 2Z -- so the exclusion is resolved and not a discretisation artefact. "
      f"(Hazard H5: a coarse grid reporting an extremum it never sampled has bitten this corpus twice.)")


banner("D  AGAINST INTEREST")
print("""  Recorded because it is the honest direction of the search:
   - This does NOT derive kappa = 1/2 -- it points the OTHER WAY. Over the shapes tested the admissible range is
     r <= ~9.02, which EXCLUDES both r = 2Z = 11.578 (kappa = 1/2) and r = 4 pi = 12.566, while admitting
     Milgrom's r = 1 and his eq.10 value r = 2. If this survives generalisation it is a no-go against BOTH live
     coefficient proposals, not a derivation of either.
   - SCOPE, and it is the whole caveat: SEVEN transition shapes is not a proof. Rule R8 -- five examples is not
     a theorem. The honest claim is "no shape tested reaches 2Z; the largest admissible r found is 9.017", NOT
     "r = 2Z is impossible". A single admissible shape reaching 2Z overturns this.
   - The one-family result that suggested r = 1 was uniquely admissible (min dlnI/dlna saturating at 0.664 for
     the saturating-exponential family) was a SHAPE artefact of that family, not a theorem. Withdrawn as a
     candidate derivation.
   - Milgrom noted the family himself: 1999 eqs 10-11 give a second coefficient (r = 2), and Milgrom 2008
     sec 7.3.1 says the mismatch "isn't necessarily meaningful". The r-freedom is HIS observation; what is new
     here is only the closed form and the admissibility test.
   - The offset condition (A1) is what does most of the work, and it is a condition on Int psi -- i.e. on the
     kernel's SHAPE, which the corpus already knows carries a 30.6% systematic on a_0 from SPARC. So the
     admissible r range and the measured shape range are the same physical freedom seen twice.""")
check(TWOZ < FOURPI and abs(FOURPI/TWOZ - 1) < 0.09,
      f"D1 and the two live coefficients are only {100*(FOURPI/TWOZ-1):.2f}% apart in r ({TWOZ:.4f} vs "
      f"{FOURPI:.4f}), so no admissibility bound with realistic precision could separate them even if one "
      f"existed. Any future derivation must be exact, not variational")

banner("RESULT")
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c: print(f"    - {m}")
    sys.exit(1)
print("  Exit 0. Admissibility (mu <= 1 AND mu monotone) is derived, not assumed, and tested over seven")
print("  transition shapes with the scale optimised. See C1 for the verdict on 2Z and 4 pi.")
print("  kappa = 1/2 remains FITTED, NOT DERIVED.")
