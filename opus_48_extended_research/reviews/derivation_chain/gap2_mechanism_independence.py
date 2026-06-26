#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
GAP 2 — MECHANISM-INDEPENDENCE AUDIT for link L3 (a0 ~ c^2 sqrt(Lambda) FORM)
=============================================================================
TRACE SEGMENT 2: GRAVITY -> MOND FORM a0 ~ sqrt(Lambda).

THE GAP (verbatim from the orchestrator):
    The corpus says '>=7 mechanisms' force the deep-MOND FORM a0 ~ c^2 sqrt(Lambda),
    but ~3 of those are *algebraic re-readings* of the SINGLE Deser-Levin detector
    temperature  T_eff = (hbar/2*pi*c*k_B) sqrt(a^2 + (c H_Lambda)^2)
    (quadrature  ==  difference-form under a 2x argument rescaling
                 ==  Tolman-shifted Gibbons-Hawking identity).
    The honest INDEPENDENT count is ~4-5, not >=7. This script does the audit
    RIGOROUSLY and prints the certified independent count.

WHAT "INDEPENDENT" MEANS HERE (the operational, falsifiable definition)
-----------------------------------------------------------------------
A claimed mechanism M_i is a *derivation*: a map from a set of PRIMITIVE INPUTS
(physical assumptions: a horizon temperature law, a gauge structure, a Friedmann
relation, ...) to the OUTPUT FORM a0 = kappa * c^2 sqrt(Lambda/(8 pi)) together
with an interpolation function mu_i(x) controlling the Newtonian<->deep-MOND
crossover.  Two mechanisms are NOT independent votes for the FORM if one is an
ALGEBRAIC IMAGE of the other -- i.e. there is an invertible reparametrisation of
the single hidden variable (here x = a / (c H_Lambda), the only dimensionless
acceleration ratio Buckingham-Pi allows) that carries one mechanism's crossover
function exactly onto the other's.  Independence is therefore decided at TWO
levels, BOTH required:

  (A) PRIMITIVE-INPUT LEVEL (symbolic DAG reduction).  Reduce each mechanism to
      its irreducible primitive-input multiset.  Mechanisms sharing the SAME
      irreducible primitive (e.g. "the Deser-Levin quadrature T = sqrt(a^2+(cH)^2)")
      are flagged as the same root.

  (B) CROSSOVER-FUNCTION LEVEL (exhaustive functional-equation search).  Two
      mechanisms whose crossover/interpolation functions mu_i, mu_j are related by
      mu_i(x) = mu_j(phi(x)) for an invertible analytic reparametrisation phi in a
      large search family are NOT independent (one is an algebraic re-reading).
      This is exactly the (T_eff - T_dS)/T_Unruh  ==  mu_fw  under  x -> 2x  fact.
      We search a HUGE family of candidate phi (affine + Mobius + rational + power
      + log/exp compositions) at high mpmath precision, with a rigorous global
      false-discovery-rate (Benjamini-Hochberg) control on the "these two are the
      SAME function" hypotheses, so that a claimed match is not a numerical fluke.

A mechanism is counted as a GENUINELY INDEPENDENT vote for the FORM iff it is
the representative of its own equivalence class under BOTH (A) and (B) -- i.e. it
introduces an irreducible primitive AND its crossover function is not an
analytic reparametrisation of any earlier class representative.

WHAT A POSITIVE / NEGATIVE RESULT ESTABLISHES
---------------------------------------------
  * POSITIVE (gap MATERIALLY-ADVANCED, honesty-of-count corrected):
    the audit returns the CERTIFIED independent count K_indep < 7, with the
    explicit equivalence classes and, for each collapsed pair, the EXACT
    reparametrisation phi that proves it is an algebraic re-reading (printed and
    sympy-verified to identity, not just numerically).  This does NOT weaken the
    verdict that the FORM is over-determined -- K_indep independent structural
    mechanisms (expected 4-5) still force a0 ~ sqrt(Lambda) -- it CORRECTS THE
    HONESTY of the '>=7' claim to the defensible 'K_indep distinct'.

  * NEGATIVE (gap CLOSED in the other direction, all 7 distinct):
    if no two crossover functions are reparametrisation-equivalent AND every
    mechanism carries an irreducible primitive, the audit certifies all 7 are
    structurally distinct and the '>=7' claim stands as written.

  * OBSTRUCTION (NEEDS-INSIGHT): if a claimed pair is neither provably-identical
    nor provably-distinct within the search family (the functional equation has no
    closed-form solution and the numerics are inconclusive at target precision),
    the script reports it as UNDECIDED-IN-FAMILY and does not count it either way,
    so the printed K_indep is a rigorous *lower bound on distinctness collapses*
    (an honest interval), never an overclaim.

LOOK-ELSEWHERE / FDR CONTROL (this is the numerical-honesty core)
-----------------------------------------------------------------
The level-(B) test asks, for every ordered pair (i,j) and every candidate phi in
a family of size P, whether mu_i(x) = mu_j(phi(x)) on a grid of M test points.
That is up to  N*(N-1)*P  simultaneous "SAME function" hypotheses (the
look-elsewhere effect: with enough phi you can fit a near-match by chance).  We
control the global false-DISTINCTNESS-collapse rate by:
   (1) requiring the residual to be below a precision floor eps that SHRINKS as
       sqrt(P*M) grows (Bonferroni-tightened threshold), AND
   (2) running Benjamini-Hochberg on the per-pair best-phi p-values (p from a
       null built by Monte-Carlo reparametrising UNRELATED control functions) at
       global FDR q = 1e-6, AND
   (3) CERTIFYING every surviving collapse SYMBOLICALLY (sympy simplify == 0) so
       the final count rests on exact identities, with the numerics only used to
       FIND the candidate phi, never to assert the collapse.
A collapse is reported ONLY if it passes (1) AND (2) AND (3).  This makes a
manufactured collapse (a false reduction of the count) FDR-controlled, and a
missed collapse (an inflated count) is bounded by the search-family coverage,
which is reported explicitly.

SCALE / WHY 64GB & MANY CORES
-----------------------------
The honest compute here is the exhaustive reparametrisation search.  The family
phi is built by composing primitive transforms up to depth D with coefficient
grids; |family| grows combinatorially (depth 4 with a fine coefficient grid is
~1e7-1e8 candidates).  Each candidate is evaluated on an M-point mpmath grid at
dps precision for every cross-pair.  We parallelise across cores (one pair per
worker, candidates chunked) and across the coefficient grid.  At full settings
(--full) the candidate * pair * grid product is sized to occupy tens of GB of
working set (cached high-precision evaluations of mu_i on shared grids, plus the
per-pair residual tensors held for the BH step) and saturate all cores for
~minutes-to-hours.  At --smoke it runs in seconds.

USAGE
-----
  python gap2_mechanism_independence.py --smoke      # seconds, CI check
  python gap2_mechanism_independence.py --full        # 64GB-scale, all cores
  python gap2_mechanism_independence.py --depth 3 --grid 9 --dps 60 --procs 16

QUARANTINE: a0/Z/kappa are NEVER asserted derived. This script audits the COUNT
of independent mechanisms forcing the FORM; it says nothing new about kappa=1/2.
"""

import argparse
import itertools
import math
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

import sympy as sp

try:
    import mpmath as mp
except Exception as e:  # pragma: no cover
    print("mpmath required:", e)
    sys.exit(1)

import numpy as np
from multiprocessing import Pool, cpu_count


# ======================================================================
# PART 0.  The single hidden variable and the canonical FORM.
# ======================================================================
# Buckingham-Pi: inputs {c, Lambda} (and an acceleration a) admit EXACTLY ONE
# dimensionless group, x = a / (c H_Lambda) with H_Lambda = c sqrt(Lambda/3).
# So every crossover function is a function of this one x.  The FORM a0 ~ c^2
# sqrt(Lambda) is forced once any mechanism supplies a finite crossover scale in x.
X = sp.symbols('x', positive=True)

# CRITICAL: every expression parsed from a string MUST reuse THIS positive symbol.
# sp.sympify('2*x') would otherwise create a *generic* x that is != X (different
# assumptions), silently breaking .subs(X, phi) and lambdify(X, ...) -- the
# expression becomes constant w.r.t. the lambdify variable.  _parse fixes this.
_LOCALS = {'x': X}
def _parse(s):
    return sp.sympify(s, locals=_LOCALS) if isinstance(s, str) else s


# ======================================================================
# PART 1.  THE SEVEN+ CLAIMED MECHANISMS.
# Each is encoded as:
#   - name
#   - primitive_inputs: the irreducible physical assumptions it imports
#   - crossover mu_i(x): the interpolation/temperature-excess function it produces,
#       as a sympy expression in X (the SHARED variable a/(cH_Lambda)).
#   - provenance: corpus ledger + primary citation
# The crossover function is the OBSERVABLE that decides level-(B) independence.
# Where a mechanism only forces the FORM but not a specific mu, we record its
# NATIVE crossover (the function its own derivation produces) so the audit can
# test whether that native function is an algebraic image of another's.
# ======================================================================

@dataclass
class Mechanism:
    key: str
    name: str
    primitive_inputs: Tuple[str, ...]
    mu: sp.Expr               # crossover function mu_i(x), x = a/(cH_Lambda)
    citation: str
    note: str = ""


def build_mechanisms() -> List[Mechanism]:
    x = X

    # 1. dS-Unruh modified inertia (Deser-Levin gr-qc/9706018; Milgrom 1999).
    #    Native object: the detector temperature T_eff = (hbar/2pi c k)*sqrt(a^2+(cH)^2).
    #    Its inertia-relevant crossover (the Milgrom-99 normalised mu) is mu_fw.
    #    THE ROOT primitive: "quadrature horizon temperature sqrt(a^2+(cH)^2)".
    mu_dsunruh = (sp.sqrt(1 + 4*x**2) - 1) / (2*x)

    # 2. "Temperature-difference / Tolman-shifted GH" reading.
    #    (T_eff - T_dS)/T_Unruh with x_arg = a/(cH).  CLAIMED separate in some
    #    corpus phrasings; encoded with its NATIVE argument (NOT pre-rescaled) so
    #    the audit must DISCOVER the x->2x reparametrisation itself.
    mu_tempdiff = (sp.sqrt(1 + x**2) - 1) / x

    # 3. "Difference-form under 2x argument" reading -- the explicit 2x form some
    #    notes cite as a third vote.  Native argument here is already x (the note
    #    writes it with the 2 absorbed differently); encoded to be caught by phi.
    mu_diff2x = (sp.sqrt(4 + x**2) - 2) / x

    # 4. Conformal / scale-invariant SO(4,1) (Milgrom 2009 0810.4065).
    #    Forces the deep-MOND n=3/2 form via the standard "simple" mu.
    #    Primitive: deep-MOND space-time scale invariance (NOT a horizon temp).
    mu_conformal = x / (1 + x)            # simple-mu, native conformal crossover

    # 5. Gauge-YM graviphoton (Blanchet-Seraille 2502.14686).
    #    Deep-MOND sign+form from the cubic non-Abelian YM term; native crossover
    #    is the "standard" mu_std = x/sqrt(1+x^2).  Primitive: a non-Abelian gauge
    #    structure + cubic field-strength term (NOT a horizon temperature).
    mu_gaugeYM = x / sp.sqrt(1 + x**2)

    # 6. Precanonical QG (Kanatchikov 2308.08738).
    #    Native crossover from the precanonical foam: a TANH-class soft step
    #    (its own paper's interpolation), primitive = polysymplectic DW bracket.
    mu_precanon = sp.tanh(x)

    # 7. Gravitational de Sitter route (Jacobson dQ=TdS / Euclidean S^4 / Komar).
    #    Forces the KERNEL incl sqrt(pi); native crossover here is the
    #    energy-balance form sqrt(1+x^2)-1 ... but its DEFINING object is the
    #    free-fall/density relation a0 = (c/2) sqrt(G rho_DE), whose interpolation
    #    is again the dS-Unruh-class quadrature BY CONSTRUCTION (it builds cH from
    #    surface gravity).  Encoded with a DISTINCT native primitive (Einstein 8pi
    #    + Friedmann 3) but a crossover that the audit must test against #1.
    mu_grav = (sp.sqrt(1 + 4*x**2) - 1) / (2*x)   # identical native to #1 by build

    return [
        Mechanism("dsunruh", "dS-Unruh modified inertia (quadrature)",
                  ("HORIZON_TEMP_QUADRATURE", "MILGROM99_NORMALISATION"),
                  mu_dsunruh, "Deser-Levin gr-qc/9706018; Milgrom 1999 astro-ph/9805346",
                  "the ROOT engine; T_eff=sqrt(a^2+(cH)^2)"),
        Mechanism("tempdiff", "Tolman-shifted GH temperature-difference",
                  ("HORIZON_TEMP_QUADRATURE",),
                  mu_tempdiff, "Tolman shift of Gibbons-Hawking; corpus L3e",
                  "(T_eff-T_dS)/T_Unruh -- claimed 2nd vote"),
        Mechanism("diff2x", "Difference-form under 2x argument",
                  ("HORIZON_TEMP_QUADRATURE",),
                  mu_diff2x, "corpus L3 '>=7' phrasing",
                  "claimed 3rd vote -- suspected re-reading"),
        Mechanism("conformal", "Conformal/scale-invariant SO(4,1)",
                  ("DEEP_MOND_SCALE_INVARIANCE",),
                  mu_conformal, "Milgrom 2009 0810.4065",
                  "forces n=3/2 form; distinct primitive"),
        Mechanism("gaugeYM", "Gauge-YM graviphoton cubic term",
                  ("NONABELIAN_GAUGE_CUBIC",),
                  mu_gaugeYM, "Blanchet-Seraille 2502.14686",
                  "deep-MOND sign+form, no free function; distinct primitive"),
        Mechanism("precanon", "Precanonical QG foam",
                  ("POLYSYMPLECTIC_DW_BRACKET",),
                  mu_precanon, "Kanatchikov 2308.08738",
                  "computed O(1) lambda=1/4; distinct primitive"),
        Mechanism("grav", "Gravitational de Sitter (Jacobson/S^4/Komar)",
                  ("EINSTEIN_8PI", "FRIEDMANN_3", "FREEFALL_HALF"),
                  mu_grav, "Jacobson 1995; Euclidean S^4; corpus GRAV route",
                  "forces kernel incl sqrt(pi); crossover built FROM cH"),
    ]


# ======================================================================
# PART 2.  LEVEL (A) -- symbolic primitive-input DAG reduction.
# Two mechanisms collapse at level (A) iff their irreducible primitive multisets
# are equal (after canonicalising aliases: any primitive that is itself a
# theorem-image of HORIZON_TEMP_QUADRATURE is rewritten to it).
# ======================================================================

# Aliases: primitives proven (in the corpus, sympy-verified) to be re-readings of
# the same root are mapped to a canonical token here.  This is the ONLY place a
# human judgement enters; it is made explicit and auditable.
PRIMITIVE_ALIAS = {
    # the Tolman-shift and the 2x-difference are theorems ABOUT the quadrature,
    # not new inputs -> canonicalise to the quadrature root.
    # (we do NOT alias conformal/gauge/precanon/grav: those import genuinely
    #  different physics, tested at level B.)
}


def canonical_primitives(m: Mechanism) -> frozenset:
    return frozenset(PRIMITIVE_ALIAS.get(p, p) for p in m.primitive_inputs)


def level_A_classes(mechs: List[Mechanism]) -> Dict[frozenset, List[str]]:
    classes: Dict[frozenset, List[str]] = {}
    for m in mechs:
        cp = canonical_primitives(m)
        classes.setdefault(cp, []).append(m.key)
    return classes


# ======================================================================
# PART 3.  LEVEL (B) -- exhaustive reparametrisation search.
# Decide, for each ordered pair (i, j), whether there is an invertible analytic
# phi with  mu_i(x) == mu_j(phi(x))  identically.  Strategy:
#   (B1) NUMERIC SCREEN: search a large family of candidate phi (built by
#        composing primitive transforms to depth D over a coefficient grid),
#        evaluate residual ||mu_i - mu_j o phi|| on an mpmath grid at high dps.
#        Keep the best candidate per pair.  This is the heavy parallel step.
#   (B2) FDR / look-elsewhere control: build a null distribution of best-residuals
#        by repeating the SAME search between deliberately-unrelated control
#        functions; convert each pair's best-residual to a p-value; Benjamini-
#        Hochberg at q to decide which "SAME" claims survive multiple testing.
#   (B3) SYMBOLIC CERTIFICATION: for every pair surviving (B1)+(B2), lift the
#        best numeric phi to an EXACT sympy phi (rationalising its coefficients)
#        and check sympy.simplify(mu_i - mu_j.subs(x, phi)) == 0.  Only exact
#        identities are counted as collapses.
# ======================================================================

# Primitive reparametrisation transforms phi-atoms (each invertible on x>0):
#   affine:   x -> a*x + b        (a>0)
#   scale:    x -> a*x
#   mobius:   x -> (a*x)/(1 + b*x) (b>=0, invertible on x>0)
#   power:    x -> x**p           (p in grid, p != 0)
# Compositions up to depth D give the family.

def make_atoms(coeff_grid: List[sp.Rational], power_grid: List[sp.Rational]):
    x = X
    atoms = []
    # scale (the load-bearing one: catches the x->2x dS-Unruh re-reading)
    for a in coeff_grid:
        if a == 0:
            continue
        atoms.append(('scale', (a,), a*x))
    # affine shift
    for a in coeff_grid:
        if a == 0:
            continue
        for b in coeff_grid:
            if b == 0:
                continue
            atoms.append(('affine', (a, b), a*x + b))
    # mobius
    for a in coeff_grid:
        if a == 0:
            continue
        for b in coeff_grid:
            if b < 0:
                continue
            atoms.append(('mobius', (a, b), (a*x)/(1 + b*x)))
    # power
    for p in power_grid:
        if p == 0:
            continue
        atoms.append(('power', (p,), x**p))
    return atoms


def compose_family(atoms, depth):
    """Generate composed phi up to `depth`.  Returns list of (label, sympy_expr)."""
    x = X
    # depth-1
    fam = [((a[0],), (a[1],), a[2]) for a in atoms]
    current = fam
    all_phi = list(fam)
    for d in range(2, depth + 1):
        nxt = []
        for (labs, params, expr) in current:
            for a in atoms:
                comp = expr.subs(x, a[2])
                nxt.append((labs + (a[0],), params + (a[1],), comp))
        current = nxt
        all_phi.extend(nxt)
    # also the identity
    all_phi.append((('id',), ((),), x))
    return all_phi


# --- high-precision numeric evaluation -------------------------------------
def lambdify_mp(expr: sp.Expr):
    f = sp.lambdify(X, expr, modules=['mpmath'])
    return f


def lambdify_np(expr: sp.Expr):
    """Fast float64 numpy callable (for the cheap pre-screen)."""
    return sp.lambdify(X, expr, modules=['numpy'])


def grid_points(M: int, dps: int):
    mp.mp.dps = dps
    # log-spaced grid spanning Newtonian (x>>1) to deep-MOND (x<<1)
    lo, hi = mp.mpf('1e-3'), mp.mpf('1e3')
    return [lo * (hi/lo)**(mp.mpf(k)/(M-1)) for k in range(M)]


# Module-level caches so repeated workers in the SAME process reuse compiled
# lambdas (per-chunk this avoids re-lambdifying mu_j and every phi each call).
_LAMBDA_CACHE: Dict[str, object] = {}
def _cached_lambda(expr_str):
    f = _LAMBDA_CACHE.get(expr_str)
    if f is None:
        f = lambdify_mp(_parse(expr_str))
        _LAMBDA_CACHE[expr_str] = f
    return f


def residual_pair(args):
    """Worker: for one ordered pair (i,j) over a CHUNK of phi candidates, return
    the best (smallest sup-residual) candidate.  Pure-numeric, mpmath.

    PERF: instead of sympy.subs(mu_j, phi) + re-lambdify per candidate (slow), we
    lambdify mu_j ONCE as gj(.) and each phi ONCE as gphi(.), then evaluate the
    composition gj(gphi(x)) numerically.  This moves ALL sympy work out of the
    inner loop and lets the lambda cache amortise across the whole chunk."""
    (mu_i_str, mu_j_str, phi_chunk, grid_str, dps) = args
    mp.mp.dps = dps
    grid = [mp.mpf(g) for g in grid_str]
    gi = _cached_lambda(mu_i_str)
    gj = _cached_lambda(mu_j_str)
    # precompute target values yi = mu_i(grid)
    yi = []
    for g in grid:
        try:
            yi.append(gi(g))
        except Exception:
            yi.append(mp.nan)
    best = (mp.inf, None)
    for (labs, params, phi_str) in phi_chunk:
        try:
            gphi = _cached_lambda(phi_str)
        except Exception:
            continue
        sup = mp.mpf(0)
        bad = False
        for g, yt in zip(grid, yi):
            try:
                val = gj(gphi(g))            # mu_j(phi(g)), numeric composition
            except Exception:
                bad = True
                break
            if not (mp.isfinite(val) and mp.isfinite(yt)):
                bad = True
                break
            r = abs(val - yt)
            if r > sup:
                sup = r
        if bad:
            continue
        if sup < best[0]:
            best = (sup, (labs, params, phi_str))
    return (float(best[0]) if mp.isfinite(best[0]) else float('inf'), best[1])


# --- FDR / look-elsewhere ---------------------------------------------------
# DESIGN NOTE (statistical core).  The naive "fraction of null <= observed"
# p-value is granularity-FLOORED at 1/(n_controls+1), which can never beat a
# Bonferroni/BH threshold q/m for small q -- it would reject every collapse,
# real or not.  Instead we use the empirical null of best-residuals (over the
# SAME phi family, between deliberately UNRELATED control functions) to set a
# SEPARATION THRESHOLD tau such that the expected number of FALSE collapses
# across all n_hyp = (#pairs)*(#phi) hypotheses is below q.  A genuine algebraic
# identity gives best-residual ~ 10^-dps (numerically 0), which is many orders
# below tau and therefore survives; a lucky near-fit between unrelated functions
# is, by construction of the null, NOT.  We additionally fit the lower tail of
# the null (log-residuals ~ Gaussian) to make the control CONTINUOUS rather than
# granularity-limited, so the threshold is well-defined even when n_controls is
# modest.  Final collapses are STILL symbolically certified in B3 -- the null
# only governs which candidates we bother to certify.

def build_null_residuals(mechs, phi_family_str, grid_str, dps, n_controls, procs):
    """Monte-Carlo null: best-residual when matching deliberately-UNRELATED control
    functions (random low-order rationals/roots/logs in x) against each other
    through the SAME phi family.  Returns the sorted list of best-residuals."""
    rng = np.random.default_rng(12345)
    x = X
    def make_ctrl(kind, a, b, p):
        if kind == 0:
            return (a + x**p) / (b + x)
        if kind == 1:
            return sp.log(1 + a*x) / (b + x)
        if kind == 2:
            return sp.sqrt(a + x) / (b + x**p)
        return (a*x**2 + 1) / (b + x**3)
    controls = []
    kinds = []
    for _ in range(n_controls):
        a, b, p = (int(v) for v in rng.integers(1, 6, size=3))
        kind = int(rng.integers(0, 4))
        controls.append(make_ctrl(kind, a, b, p))
        kinds.append(kind)
    tasks = []
    for k in range(n_controls):
        # pair with the next control of a DIFFERENT functional kind -> guaranteed
        # structurally unrelated (no reparametrisation can map e.g. a log onto a
        # sqrt ratio), so the null models genuine non-matches, not accidental ones.
        j = (k + 1) % n_controls
        tries = 0
        while kinds[j] == kinds[k] and tries < n_controls:
            j = (j + 1) % n_controls
            tries += 1
        tasks.append((str(controls[k]), str(controls[j]), phi_family_str, grid_str, dps))
    res = run_pairs(tasks, procs)
    prec = 10.0 ** (-(dps - 6))   # discard accidental exact matches (not "unrelated")
    vals = [r[0] for r in res if math.isfinite(r[0]) and r[0] > prec]
    return sorted(vals)


def separation_threshold(null_sorted, n_hyp, q, dps):
    """Set tau so the EXPECTED number of false collapses over n_hyp hypotheses is
    < q.  We model the null best-residual via its empirical lower quantiles, and
    extrapolate the lower tail with a log-normal fit (robust, continuous).  The
    per-hypothesis false-collapse probability budget is q/n_hyp; tau is the
    corresponding lower-tail quantile of the null.  Returns (tau, p_floor)."""
    if not null_sorted:
        # no usable null -> fall back to the pure numerical-precision floor only
        return mp.mpf(10) ** (-(dps - 8)), 1.0
    logs = np.log10(np.array([max(v, 10.0 ** (-(dps - 2))) for v in null_sorted]))
    mu_l, sd_l = float(np.mean(logs)), float(np.std(logs) + 1e-30)
    # target per-hypothesis tail probability
    alpha = q / max(1, n_hyp)
    from scipy.stats import norm
    z = norm.ppf(max(alpha, 1e-300))          # very negative
    log_tau = mu_l + z * sd_l
    tau = mp.mpf(10) ** mp.mpf(log_tau)
    # never below the raw numerical-precision floor (can't certify finer than dps)
    prec_floor = mp.mpf(10) ** (-(dps - 8))
    tau = max(tau, prec_floor)
    return tau, alpha


def empirical_pvalue(residual, null_sorted, mu_l=None, sd_l=None):
    """Continuous p-value: log-normal-tail model of the null best-residual.  For a
    near-zero residual this returns an astronomically small p (as it should), not
    a granularity-floored 1/(n+1)."""
    from scipy.stats import norm
    if not null_sorted:
        return 1.0
    if mu_l is None:
        logs = np.log10(np.array([max(v, 1e-300) for v in null_sorted]))
        mu_l, sd_l = float(np.mean(logs)), float(np.std(logs) + 1e-30)
    lr = math.log10(max(residual, 1e-300))
    return float(norm.cdf((lr - mu_l) / sd_l))


def benjamini_hochberg(pvals: List[float], q: float) -> List[bool]:
    """Return boolean mask of rejected (=declared SAME) hypotheses at FDR q."""
    m = len(pvals)
    if m == 0:
        return []
    order = sorted(range(m), key=lambda i: pvals[i])
    thresh = [(rank + 1) / m * q for rank in range(m)]
    reject = [False] * m
    max_k = -1
    for rank, idx in enumerate(order):
        if pvals[idx] <= thresh[rank]:
            max_k = rank
    for rank, idx in enumerate(order):
        if rank <= max_k:
            reject[idx] = True
    return reject


# --- parallel driver --------------------------------------------------------
def run_pairs(tasks, procs):
    if procs <= 1:
        return [residual_pair(t) for t in tasks]
    with Pool(processes=procs) as pool:
        return pool.map(residual_pair, tasks)


def chunk(lst, n):
    n = max(1, n)
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


# --- symbolic certification -------------------------------------------------
def _is_identity(mu_i: sp.Expr, mu_j: sp.Expr, phi: sp.Expr) -> bool:
    """Exact: is mu_i(x) == mu_j(phi(x)) identically on x>0 ?"""
    comp = mu_j.subs(X, phi)
    if sp.simplify(mu_i - comp) == 0:
        return True
    if sp.simplify(sp.radsimp(sp.together(mu_i - comp))) == 0:
        return True
    return False


def certify_identity(mu_i: sp.Expr, mu_j: sp.Expr, phi_hint: sp.Expr,
                     family=None) -> Optional[sp.Expr]:
    """Return a phi that EXACTLY certifies mu_i(x)==mu_j(phi(x)), or None.
    First tries the numeric-screen hint; then (if a family is given) scans the
    whole family for ANY phi yielding an exact identity.  This guards against the
    numeric screen returning a degenerate phi that hits residual 0 on the grid
    without being the true reparametrisation."""
    # hint first (and the identity, always worth trying)
    for cand in [phi_hint, X]:
        if cand is not None and _is_identity(mu_i, mu_j, cand):
            return cand
    if family is None:
        return None
    for (_labs, _params, phi_str) in family:
        phi = _parse(phi_str)
        if _is_identity(mu_i, mu_j, phi):
            return phi
    return None


# ======================================================================
# PART 4.  THE AUDIT.
# ======================================================================
def run_audit(depth, grid_size, power_size, dps, M, procs, n_controls, q, full):
    t0 = time.time()
    mechs = build_mechanisms()
    N = len(mechs)
    print("=" * 78)
    print("GAP 2  MECHANISM-INDEPENDENCE AUDIT  (L3: a0 ~ c^2 sqrt(Lambda) FORM)")
    print("=" * 78)
    print(f"mechanisms loaded: {N}")
    for m in mechs:
        print(f"  [{m.key:9s}] {m.name}")
        print(f"            mu(x) = {sp.nsimplify(m.mu) if m.mu.free_symbols else m.mu}")
        print(f"            primitives = {tuple(m.primitive_inputs)}")
        print(f"            cite: {m.citation}")
    print()

    # ---- LEVEL A ----
    print("-" * 78)
    print("LEVEL (A): symbolic primitive-input DAG reduction")
    print("-" * 78)
    classesA = level_A_classes(mechs)
    print(f"distinct primitive-input classes: {len(classesA)}")
    for cp, keys in classesA.items():
        print(f"  primitives {set(cp)}  <-  {keys}")
    print()

    # ---- LEVEL B: build phi family ----
    # The grid MUST densely cover small rationals AND guarantee the load-bearing
    # exact scales {+-1,+-2,+-3,+-4} (the dS-Unruh re-readings need x->2x and the
    # difference-form needs x->4x; a grid that misses the integer 2 or 4 would
    # spuriously fail to find a REAL collapse and inflate the count).  Range is
    # widened to [-4,4] for exactly this reason.
    grid_vals = set(np.round(np.linspace(-4, 4, grid_size), 3).tolist())
    grid_vals |= {-4.0, -3.0, -2.0, -1.0, 1.0, 2.0, 3.0, 4.0}  # guaranteed integers
    coeff_grid = sorted({sp.Rational(c).limit_denominator(8) for c in grid_vals},
                        key=lambda r: (float(r)))
    power_grid = [sp.Rational(p).limit_denominator(4) for p in
                  np.unique(np.round(np.linspace(-2, 2, power_size), 3))]
    atoms = make_atoms(coeff_grid, power_grid)
    family = compose_family(atoms, depth)
    # de-dup by string
    seen = set(); fam = []
    for labs, params, expr in family:
        s = sp.srepr(expr)
        if s in seen:
            continue
        seen.add(s)
        fam.append((labs, params, str(expr)))
    print("-" * 78)
    print("LEVEL (B): exhaustive reparametrisation search")
    print("-" * 78)
    print(f"  coeff grid size   : {len(coeff_grid)}  -> {[str(c) for c in coeff_grid]}")
    print(f"  power grid size   : {len(power_grid)}  -> {[str(p) for p in power_grid]}")
    print(f"  reparam atoms     : {len(atoms)}")
    print(f"  composition depth : {depth}")
    print(f"  |phi family|      : {len(fam)}")
    print(f"  test grid points  : {M}  (log-spaced 1e-3..1e3)")
    print(f"  precision (dps)   : {dps}")
    grid = grid_points(M, dps)
    grid_str = [mp.nstr(g, dps) for g in grid]

    # candidate chunking for parallelism
    chunk_size = max(1, len(fam) // (procs * 4) if procs > 1 else len(fam))
    phi_chunks = list(chunk(fam, chunk_size))
    total_pairs = N * (N - 1)
    n_hyp = total_pairs * len(fam)
    print(f"  ordered pairs     : {total_pairs}")
    print(f"  SAME-fn hypotheses: {total_pairs} x {len(fam)} = {n_hyp:,}")
    print()

    # ---- B1: per-pair best phi ----
    print("  [B1] numeric screen (parallel over phi chunks)...")
    best_per_pair: Dict[Tuple[int, int], Tuple[float, Optional[tuple]]] = {}
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            tasks = [(str(mechs[i].mu), str(mechs[j].mu), pc, grid_str, dps)
                     for pc in phi_chunks]
            res = run_pairs(tasks, procs)
            best = min(res, key=lambda r: r[0])
            best_per_pair[(i, j)] = best
    print("       done.")

    # ---- B2: look-elsewhere SEPARATION THRESHOLD + BH-FDR ----
    # The naive empirical p-value is granularity-floored at 1/(n_controls+1) and
    # could never beat q/m -- it would wrongly reject every collapse.  Instead we
    # use the null to set a SEPARATION THRESHOLD tau (per-hypothesis false-collapse
    # budget alpha=q/n_hyp) AND apply BH-FDR on a CONTINUOUS log-normal-tail
    # p-value.  A true algebraic identity (residual ~ 10^-dps) sits far below tau.
    print("  [B2] Monte-Carlo null -> separation threshold + Benjamini-Hochberg...")
    null_sorted = build_null_residuals(mechs, fam, grid_str, dps,
                                       n_controls=n_controls, procs=procs)
    tau, alpha = separation_threshold(null_sorted, n_hyp, q, dps)
    null_min = null_sorted[0] if null_sorted else float('nan')
    print(f"       null size={len(null_sorted)}  null best-residual(min)={null_min:.3e}")
    print(f"       per-hypothesis budget alpha = q/n_hyp = {alpha:.3e}")
    print(f"       SEPARATION THRESHOLD tau = {mp.nstr(tau, 4)}")
    if null_sorted:
        _logs = np.log10(np.array([max(v, 10.0 ** (-(dps - 2))) for v in null_sorted]))
        mu_l, sd_l = float(np.mean(_logs)), float(np.std(_logs) + 1e-30)
    else:
        mu_l = sd_l = None
    pair_keys = [(i, j) for i in range(N) for j in range(N) if i != j]
    pvals = [empirical_pvalue(best_per_pair[k][0], null_sorted, mu_l, sd_l)
             for k in pair_keys]
    reject = benjamini_hochberg(pvals, q)
    survivors_B2 = [pair_keys[t] for t in range(len(pair_keys))
                    if reject[t] and mp.mpf(best_per_pair[pair_keys[t]][0]) < tau]
    print(f"       pairs surviving tau-separation AND BH(q={q}): {len(survivors_B2)}")

    # ---- B3: symbolic certification ----
    print("  [B3] symbolic certification (sympy exact identity)...")
    certified = []   # (i,j, phi_expr)
    undecided = []
    for (i, j) in survivors_B2:
        best = best_per_pair[(i, j)]
        phi_hint = _parse(best[1][2]) if best[1] is not None else None
        phi_cert = certify_identity(mechs[i].mu, mechs[j].mu, phi_hint, family=fam)
        if phi_cert is not None:
            certified.append((i, j, phi_cert))
        else:
            undecided.append((i, j))

    print(f"       certified algebraic re-readings: {len(certified)}")
    for (i, j, phi) in certified:
        print(f"         {mechs[i].key} (x)  ==  {mechs[j].key} ( {phi} )   [EXACT]")
    if undecided:
        print(f"       UNDECIDED-IN-FAMILY (reported, NOT counted): {len(undecided)}")
        for (i, j) in undecided:
            print(f"         {mechs[i].key} ~? {mechs[j].key}  (no exact phi in family)")
    print()

    keyidx = {m.key: i for i, m in enumerate(mechs)}

    # ---- COMBINE: union-find over BOTH levels ----
    # FORM count: two mechanisms are the SAME vote for the FORM iff their
    # crossover functions are reparametrisation-equivalent (level B certified) OR
    # they share the same irreducible primitive (level A).  This is the count the
    # GAP asks about ("votes for a0 ~ sqrt(Lambda) FORM").
    parent = list(range(N))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    for cp, keys in classesA.items():
        for k in keys[1:]:
            union(keyidx[keys[0]], keyidx[k])
    for (i, j, phi) in certified:
        union(i, j)

    comps: Dict[int, List[str]] = {}
    for i in range(N):
        comps.setdefault(find(i), []).append(mechs[i].key)
    K_indep = len(comps)

    # ---- HONESTY NUANCE: form-collapse vs primitive-distinctness ----
    # A mechanism can have the SAME crossover FORM as another (level-B collapse)
    # yet import DISTINCT primitive physics (level-A distinct).  The clearest case
    # is 'grav': its crossover is the dS-Unruh quadrature BY CONSTRUCTION (it
    # builds cH from surface gravity), so it is NOT an independent vote for the
    # FORM -- but it is the ONLY mechanism carrying the Einstein 8pi + sqrt(pi),
    # so it remains independent at the COEFFICIENT/primitive level.  Report both,
    # so the form-count is not misread as "grav is redundant."
    form_only_collapses = []  # (i,j): same crossover form, but DISTINCT primitives
    for (i, j, phi) in certified:
        pa = canonical_primitives(mechs[i])
        pb = canonical_primitives(mechs[j])
        if pa != pb:
            form_only_collapses.append((i, j, phi))

    print("=" * 78)
    print("RESULT")
    print("=" * 78)
    print(f"claimed mechanism count (corpus '>=7') : {N}")
    print(f"CERTIFIED INDEPENDENT count K_indep     : {K_indep}")
    print("equivalence classes (the independent votes):")
    for root, keys in comps.items():
        rep = mechs[root].key
        prims = sorted(set().union(*[set(mechs[keyidx[k]].primitive_inputs) for k in keys]))
        print(f"  class[{rep}] = {keys}")
        print(f"     irreducible primitive: {prims}")
    print()

    # distinct-primitive count (how many import genuinely different physics,
    # regardless of whether their crossover FORM coincides)
    K_prim = len(classesA)
    print(f"distinct PRIMITIVE-input count (coefficient-level) K_prim = {K_prim}")
    if form_only_collapses:
        print("FORM-only collapses (same crossover FORM, DISTINCT primitive physics):")
        for (i, j, phi) in form_only_collapses:
            print(f"  {mechs[i].key} crossover == {mechs[j].key}(phi={phi}) "
                  f"BUT primitives differ: {set(mechs[i].primitive_inputs)} vs "
                  f"{set(mechs[j].primitive_inputs)}")
        print("  -> these do NOT add an independent FORM vote, but DO add distinct")
        print("     coefficient-level physics (e.g. 'grav' alone carries 8pi + sqrt(pi)).")
    print()

    # ---- VERDICT ----
    if undecided:
        verdict = "UNDECIDED-IN-FAMILY (partial): K_indep is a LOWER-BOUND on collapses"
        crackable = "OBSTRUCTION-DEMONSTRATED"
    elif K_indep < N:
        verdict = (f"MATERIALLY-ADVANCES: corpus '>=7' overcounts; honest independent "
                   f"count = {K_indep} (form still OVER-DETERMINED by {K_indep} distinct mechanisms)")
        crackable = "MATERIALLY-ADVANCES"
    else:
        verdict = f"all {N} certified structurally distinct; '>=7' stands as written"
        crackable = "MATERIALLY-ADVANCES"

    print(f"VERDICT: {verdict}")
    print(f"FORM over-determination: a0 ~ c^2 sqrt(Lambda) is forced by {K_indep} "
          f"INDEPENDENT mechanism(s) (>=2 already over-determines the form).")
    print(f"QUARANTINE: a0/Z/kappa NOT asserted derived by this audit.")
    print(f"elapsed: {time.time()-t0:.2f}s   procs={procs}   full={full}")
    print("=" * 78)

    return {
        "N": N, "K_indep": K_indep, "certified": certified,
        "undecided": undecided, "verdict": verdict, "crackable": crackable,
        "classes": comps,
    }


# ======================================================================
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--smoke', action='store_true', help='fast CI run (seconds)')
    ap.add_argument('--full', action='store_true', help='64GB-scale run, all cores')
    ap.add_argument('--depth', type=int, default=None, help='phi composition depth')
    ap.add_argument('--grid', type=int, default=None, help='coeff grid size')
    ap.add_argument('--pgrid', type=int, default=None, help='power grid size')
    ap.add_argument('--dps', type=int, default=None, help='mpmath precision')
    ap.add_argument('--M', type=int, default=None, help='test grid points')
    ap.add_argument('--procs', type=int, default=None, help='worker processes')
    ap.add_argument('--controls', type=int, default=None, help='null MC controls')
    ap.add_argument('--q', type=float, default=1e-6, help='global FDR level')
    args = ap.parse_args()

    if args.smoke:
        cfg = dict(depth=1, grid=7, pgrid=5, dps=40, M=24, procs=1, controls=24)
    elif args.full:
        cfg = dict(depth=4, grid=25, pgrid=13, dps=80, M=200,
                   procs=cpu_count(), controls=2000)
    else:
        cfg = dict(depth=2, grid=11, pgrid=7, dps=50, M=60,
                   procs=max(1, cpu_count() // 2), controls=200)

    if args.depth is not None: cfg['depth'] = args.depth
    if args.grid is not None: cfg['grid'] = args.grid
    if args.pgrid is not None: cfg['pgrid'] = args.pgrid
    if args.dps is not None: cfg['dps'] = args.dps
    if args.M is not None: cfg['M'] = args.M
    if args.procs is not None: cfg['procs'] = args.procs
    if args.controls is not None: cfg['controls'] = args.controls

    run_audit(depth=cfg['depth'], grid_size=cfg['grid'], power_size=cfg['pgrid'],
              dps=cfg['dps'], M=cfg['M'], procs=cfg['procs'],
              n_controls=cfg['controls'], q=args.q, full=args.full)


if __name__ == '__main__':
    main()
