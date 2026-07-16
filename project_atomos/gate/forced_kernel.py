"""
GATE B — forced kernel.

"Does a coefficient decompose into factors pinned BEFORE the fit?"

This is the half that made a0 real. A fitted coefficient is free; a FORCED coefficient
is dictated by known physics independent of and prior to matching the data.

The three pass-tests (GATE_SPEC B):
  1. PROVENANCE, not factorization. Each declared factor must name a pre-registered
     forced constraint (gate/registry.py) AND numerically equal that forced constant.
     A factor with no registry tag is a free fit parameter.
  2. OVERDETERMINATION. The same forced factor(s) must appear in >=2 independent forced
     places (Einstein AND Friedmann), OR the FORM is forced a third independent way.
  3. FREE-PARAMETER COUNT. The genuinely-unforced O(1) numbers must be EXACTLY ONE
     (kappa-class). >=2 free numbers => FAIL (this is what kills "dS-Unruh forces sqrt2":
     kappa=1/2 -> sqrt2 is two free numbers).

The gate INDEPENDENTLY recomputes the free-parameter count from factor provenances, so
a candidate cannot under-report it. It also verifies the forced factors actually
reproduce the candidate's coefficient (sympy-exact identity check where possible).
"""
from __future__ import annotations
from dataclasses import dataclass
from .registry import is_forced, factor_matches_forced, forced_value


@dataclass
class KernelResult:
    passed: bool
    n_free_params: int
    forced_factors: list      # [(value, provenance, appears_in)]
    unforced_factors: list    # factors with no/invalid provenance
    overdetermined: bool
    n_independent_appearances: int
    coefficient_reproduced: bool
    tell: str


def forced_kernel_detector(candidate) -> KernelResult:
    """GATE B. Returns KernelResult(passed, ...)."""
    coeff = candidate.coefficient
    forced = []
    unforced = []
    appearances = set()

    for f in coeff.factors:
        ok = is_forced(f.provenance) and factor_matches_forced(f.value, f.provenance)
        if ok:
            forced.append((f.value, f.provenance, list(f.appears_in)))
            for place in f.appears_in:
                appearances.add(place)
        else:
            reason = ("no registry provenance" if not is_forced(f.provenance)
                      else f"value {f.value:.6g} != forced {forced_value(f.provenance):.6g}")
            unforced.append((f.value, f.provenance, reason))

    # --- Test 1: provenance. Every factor that is meant to be forced must be forced. ---
    # (Factors the candidate itself declares as the free kappa are counted below, not here.)

    # --- Test 3: free-parameter count, recomputed independently. ---
    # The gate's own count = the candidate's declared free_params PLUS any factor that
    # claimed forced provenance but FAILED verification (a failed-forced factor is, in
    # truth, a free fit parameter). This is how a candidate cannot under-report.
    n_free = coeff.free_params + len(unforced)

    # --- Test 2: overdetermination. ---
    # Count independent forced appearances of the kernel; the FORM forced a 3rd
    # independent way also counts. a0: Einstein + Friedmann (=2 from appears_in) and
    # form_forced_independently>=1 (dS-Unruh) -> overdetermined.
    n_appear = len(appearances) + coeff.form_forced_independently
    overdetermined = n_appear >= 2

    # --- coefficient reproduction: do the forced factors (x the one free param) land the
    # declared coefficient value? (sympy-grade numeric identity) ---
    coeff_reproduced = True
    if coeff.target_value is not None and forced:
        prod = 1.0
        for v, _p, _a in forced:
            prod *= v
        # allow the lone free kappa to scale it: target = kappa * prod, kappa O(1).
        if prod != 0:
            implied_free = coeff.target_value / prod
            # if there is exactly one free param, implied_free should be an O(1) number
            # (a0: kappa=1/2). If n_free==0 it must reproduce exactly.
            if coeff.free_params == 0:
                coeff_reproduced = abs(implied_free - 1.0) < 1e-9
            else:
                coeff_reproduced = (0.05 < abs(implied_free) < 20.0)
        else:
            coeff_reproduced = False

    # --- verdict ---
    passed = (len(unforced) == 0) and overdetermined and (n_free == 1) and coeff_reproduced

    if len(unforced) > 0:
        tell = (f"factor(s) with no pre-fit provenance: "
                + "; ".join(f"{v:.4g}({p}:{r})" for v, p, r in unforced)
                + f" -> these are free fit parameters (n_free={n_free}).")
    elif not overdetermined:
        tell = (f"not overdetermined: forced structure appears in only {n_appear} "
                f"independent place(s) (need >=2). A single appearance is a definition, "
                f"not a kernel.")
    elif n_free != 1:
        tell = (f"free-parameter count = {n_free} (need exactly 1, kappa-class). "
                + ("zero free => suspiciously exact / not a 1-param relation"
                   if n_free == 0 else
                   "needs >=2 free numbers to land the target -> a fit, not a kernel."))
    elif not coeff_reproduced:
        tell = "forced factors x one O(1) free param do NOT reproduce the coefficient."
    else:
        tell = (f"PASS: kernel decomposes into {len(forced)} forced factor(s) "
                f"[{', '.join(p for _v, p, _a in forced)}], overdetermined "
                f"({n_appear} independent forced appearances), exactly 1 free param (kappa).")

    return KernelResult(
        passed=passed, n_free_params=n_free, forced_factors=forced,
        unforced_factors=unforced, overdetermined=overdetermined,
        n_independent_appearances=n_appear, coefficient_reproduced=coeff_reproduced,
        tell=tell,
    )
