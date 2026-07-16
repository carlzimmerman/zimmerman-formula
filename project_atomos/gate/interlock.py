"""
GATE C — interlock.

"Does the structure force >=2 independent observables, or tie >=3 constants with 1
parameter?"

Two pass-modes (either passes):
  C1 — multi-observable forcing: the structure forces >=2 independent observables from
       the SAME parameters (a0: Einstein + Friedmann + dS-Unruh form = 3 anchors, 1 kappa).
  C2 — Koide-class: the relation ties >=3 measured constants with <=1 free parameter
       (Koide: 3 lepton masses, 0 params).

PLUS the interlock FALSIFICATION (the teeth, from koide_geometry_crossfermion):
  a claimed-universal mechanism must hold on every sector it governs. The gate runs the
  SAME relation on independent sectors via `cross_sector` and demands consistency. If the
  relation is claimed family-universal and fails elsewhere, C FAILS unless a
  charged-lepton-specific ingredient legitimately restricts it.

Reports the Q1/Q2 split honestly: a real empirical interlock (C2 pass) whose current
*mechanism* fails Gate B is "REAL-PUZZLE-RE-LABELED" (the Koide verdict) — flagged, not
hidden, and not counted as a forced kernel.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class InterlockResult:
    passed: bool
    mode: str                 # "C1" | "C2" | "none"
    cross_sector_ok: bool
    cross_sector_detail: dict
    tell: str


def interlock_check(candidate) -> InterlockResult:
    """GATE C. Returns InterlockResult(passed, ...)."""
    il = candidate.interlock

    # --- which mode (if any) does the candidate satisfy? ---
    c1 = il.n_independent_observables >= 2
    c2 = (il.n_constants_tied >= 3) and (il.n_free_in_interlock <= 1)
    mode = "C1" if c1 else ("C2" if c2 else "none")

    # --- cross-sector falsification ---
    cross_ok = True
    detail = {}
    if il.cross_sector is not None:
        detail = il.cross_sector()  # {sector: {'value':..., 'target':..., 'ok':bool}}
        sectors_fail = [s for s, d in detail.items() if not d.get("ok", False)]
        if il.claimed_universal and sectors_fail and not il.sector_specific_ingredient:
            # universal claim contradicted elsewhere, with no restricting ingredient
            cross_ok = False
        # If NOT claimed universal, or a sector-specific ingredient is named, failing on
        # other sectors is EXPECTED and does not falsify (Koide IS lepton-specific).

    passed = (c1 or c2) and cross_ok

    if not (c1 or c2):
        tell = (f"interlock-FAIL: neither C1 ({il.n_independent_observables} observables, "
                f"need >=2) nor C2 ({il.n_constants_tied} constants tied with "
                f"{il.n_free_in_interlock} free, need >=3 & <=1) -> one-number "
                f"re-description.")
    elif not cross_ok:
        bad = [s for s, d in detail.items() if not d.get("ok", False)]
        tell = (f"interlock-FAIL: claimed family-universal but contradicted on "
                f"{bad} with no charged-lepton-specific ingredient -> cross-sector kill.")
    else:
        extra = ""
        if il.cross_sector is not None and il.sector_specific_ingredient:
            extra = (f" (correctly restricted by '{il.sector_specific_ingredient}'; "
                     f"other sectors deviate as expected, not a falsification)")
        tell = (f"PASS via {mode}: "
                + (f"{il.n_independent_observables} independent observables forced by "
                   f"the same parameters" if c1 else
                   f"{il.n_constants_tied} constants tied with {il.n_free_in_interlock} "
                   f"free parameter(s)")
                + extra)

    return InterlockResult(passed=passed, mode=mode, cross_sector_ok=cross_ok,
                           cross_sector_detail=detail, tell=tell)
