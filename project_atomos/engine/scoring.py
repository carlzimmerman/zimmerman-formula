#!/usr/bin/env python3
"""
scoring.py — UNCERTAINTY-AWARE scoring. Carl's #1 emphasis (a) this run, made real.

THE RULE: a 6-digit match to a 2-digit-known constant is meaningless. A formula is only a
*candidate hit* if it lands WITHIN the measurement error of the target; and the figure of merit
is always n-sigma agreement + surplus bits RELATIVE TO THE TOLERANCE, never a raw digit-count.

This module is the single place that turns a (candidate value, target Target) pair into the
uncertainty-aware numbers the engine ranks by and the FDR gate weights by:

  - n_sigma         = |val - value| / sigma                 (how many measurement-sigmas off)
  - within(k)       = n_sigma <= k                          (the hit predicate; default k=1)
  - tol_match       = the FRACTIONAL tolerance = rel_precision (sigma/|value|) of the TARGET.
                      THIS is the tol the engine/gate use — NOT an arbitrary 1e-4. So a blunt
                      target (rel 0.1) gets a loose window and a 6-digit "match" earns nothing;
                      a sharp target (rel 1e-9) demands a 9-digit landing to even count.
  - surplus_bits    = bits of agreement EARNED, capped at n_digits_known of the target. A match
                      tighter than the measurement is pure noise and earns NO extra bits (the cap
                      is exactly Carl's "6-digit match to a 2-digit constant is meaningless").

DESIGN: pure functions over a targets.pdg_constants.Target (duck-typed: needs .value, .sigma,
.rel_precision, .n_digits). No global state. Used by:
  - engine/search.py     (Search.tol defaulted to the target's rel_precision; score caps fit-bits)
  - run_atomos.py        (per-candidate headline = n_sigma + surplus_bits)
  - gate/fdr.py          (the FDR tight window = the measurement tolerance; bits capped at n_digits)
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class ScoreCard:
    """The uncertainty-aware verdict on one (value, target) pair. Every number here is
    relative to the MEASUREMENT uncertainty, never a bare digit count."""
    value: float
    target_value: float
    sigma: float
    rel_error: float          # |val-tv|/|tv|  (raw closeness — advisory only)
    n_sigma: float            # |val-tv|/sigma  (THE figure of merit)
    within_1sigma: bool
    within_2sigma: bool
    tol_used: float           # the fractional tolerance actually applied (= target rel_precision)
    n_digits_known: float     # how many sig figs the target pins (cap on meaningful match depth)
    fit_bits: float           # bits of agreement, CAPPED at n_digits_known (excess = noise = 0)
    fit_bits_uncapped: float  # what the raw closeness would claim (for the demotion diagnostic)
    demoted: bool             # True if the raw match was deeper than the measurement justifies

    @property
    def headline(self) -> str:
        cap = " [DEMOTED: match deeper than measurement]" if self.demoted else ""
        return (f"n_sigma={self.n_sigma:.2f} (tol={self.tol_used:.1e}, "
                f"{self.n_digits_known:.1f} digits known) -> {self.fit_bits:.1f} fit-bits{cap}")


def _safe_log2(x: float) -> float:
    return math.log2(x) if x > 0 else float("inf")


def score_value(value: float, target,
                k_hit: float = 1.0,
                floor_rel: float = 1e-12) -> ScoreCard:
    """Score a candidate `value` against a `target` (Target with .value/.sigma/.rel_precision/
    .n_digits). Returns a ScoreCard whose every number is uncertainty-aware.

    floor_rel : the deepest fractional match we will ever credit (numerical noise floor, ~1e-12),
                so a value that happens to be machine-equal to the target does not claim infinite
                bits. The n_digits cap below is the *physical* (measurement) cap; this is the
                *numerical* one.
    """
    tv = float(target.value)
    sigma = float(target.sigma)
    rel_prec = float(target.rel_precision)
    n_digits = float(target.n_digits)

    val = float(value)
    abs_dev = abs(val - tv)
    rel_error = abs_dev / abs(tv) if tv != 0 else float("inf")
    n_sigma = abs_dev / sigma if sigma > 0 else float("inf")

    # the tolerance the engine/gate APPLY is the target's own relative precision (its 1-sigma
    # fractional error). This is the load-bearing move: the window is the measurement, not a
    # fixed 1e-4. A blunt target gets a loose window; a sharp one a tight window.
    tol_used = rel_prec

    # bits of agreement the RAW closeness would claim: -log2(rel_error), floored at floor_rel.
    raw_rel = max(rel_error, floor_rel)
    fit_bits_uncapped = -_safe_log2(raw_rel)

    # the CAP: you cannot earn more bits than the measurement pins. n_digits_known sig figs
    # ~ n_digits * log2(10) bits of *meaningful* precision. Any match tighter than the
    # measurement error is fitting noise and earns NOTHING beyond the cap.
    bit_cap = n_digits * math.log2(10.0) if math.isfinite(n_digits) and n_digits > 0 else 0.0
    fit_bits = min(fit_bits_uncapped, bit_cap)
    demoted = fit_bits_uncapped > bit_cap + 1e-9

    return ScoreCard(
        value=val, target_value=tv, sigma=sigma, rel_error=rel_error,
        n_sigma=n_sigma, within_1sigma=(n_sigma <= k_hit), within_2sigma=(n_sigma <= 2 * k_hit),
        tol_used=tol_used, n_digits_known=n_digits,
        fit_bits=fit_bits, fit_bits_uncapped=fit_bits_uncapped, demoted=demoted,
    )


def measurement_tol(target, min_tol: float = 1e-10, max_tol: float = 0.2) -> float:
    """The fractional tolerance the engine should search with for THIS target = its relative
    precision, clamped to a sane band. Clamps:
      - min_tol: never demand more than ~10 digits even from a 1e-12-known target (engine
        precision floor; mpmath dps=40 is fine but the germ pool is finite, so don't ask for
        impossible depth).
      - max_tol: a blunt target (rel 0.2+) still gets at most a 20% window, else everything 'hits'.
    """
    rp = float(target.rel_precision)
    if not math.isfinite(rp) or rp <= 0:
        return max_tol
    return max(min_tol, min(max_tol, rp))
