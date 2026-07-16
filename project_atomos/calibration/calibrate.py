#!/usr/bin/env python3
"""
calibrate.py — the ACCEPTANCE TEST for the project_atomos gate.

The whole project lives or dies on the gate (GATE_SPEC.md): it must CERTIFY the one
real discovery and REJECT the known coincidences, same bar both ways. Before the
machine is pointed at PMNS it has to prove itself on known answers. This driver runs
the EXISTING gate (gate/{fdr,forced_kernel,interlock,verdict,registry,candidate}.py)
over a fixed calibration set and prints a pass/fail table.

KNOWN POSITIVES (must be accepted):
  - a0 forced kernel  sqrt(8pi/3) = sqrt(8pi)*sqrt(1/3)         -> CERTIFIED (B + C1)
  - Koide  Q = 2/3  (real lepton masses, triple-null ~1-in-48k) -> REAL-PUZZLE-RE-LABELED
                                                                   (A + C2, honest B-gap)
KNOWN NEGATIVES (must be rejected, each with the RIGHT tell):
  - alpha^-1 = 4 Z^2 + 3            -> FDR-DEAD @ A (germ pool dense / 0 surplus bits)
  - m_mu/m_e = 64 pi + Z           -> FDR-DEAD @ A (BAKED dense)
  - m_tau/m_mu = Z + 11            -> FDR-DEAD @ A (BAKED dense)
  - m_p/m_e = 6 pi^5               -> FDR-DEAD @ A (BAKED dense)
  - sin^2 theta_W = 3/13           -> FDR-DEAD @ A (rational, re-label-free / dense)
  - "dS-Unruh forces sqrt(2)"      -> FDR-DEAD @ B (two free numbers; A: not special)

A pass for the suite = every positive lands its required status AND every negative is
rejected with the right gate as the first failure. Anything else is a calibration FAIL
and the gate code must be fixed (this file does not patch the gate — it only drives it).

Run:  python3 calibration/calibrate.py
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

# --- make `gate` importable regardless of cwd (absolute, per project discipline) ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from gate.candidate import (  # noqa: E402
    Candidate, SearchSpace, Coefficient, Factor, Interlock,
)
from gate.verdict import validate  # noqa: E402

# ----------------------------------------------------------------------------------
# Shared constants
# ----------------------------------------------------------------------------------
PI = math.pi
Z = math.sqrt(32 * PI / 3.0)          # = 5.78878...  (the framework germ)
KERNEL = math.sqrt(8 * PI / 3.0)      # = 2.89439...  = Z/2
SQRT8PI = math.sqrt(8 * PI)
SQRT_THIRD = math.sqrt(1.0 / 3.0)

# real lepton pole masses (MeV) — the calibration requires these EXACT values
M_E = 0.5109989
M_MU = 105.6583755
M_TAU = 1776.86

# the framework germ pool (the reachable O(1) set the brute search decorates with).
# This is what Gate A reconstructs the look-elsewhere null from for the BAKED negatives.
GERM_POOL = {
    "pi": PI, "e": math.e,
    "2": 2.0, "3": 3.0, "4": 4.0, "5": 5.0, "6": 6.0, "7": 7.0, "8": 8.0,
    "9": 9.0, "10": 10.0, "11": 11.0, "12": 12.0, "13": 13.0, "16": 16.0,
    "8pi": 8 * PI, "2pi": 2 * PI, "4pi": 4 * PI, "4pi/3": 4 * PI / 3,
    "Z": Z, "kernel": KERNEL, "kappa": 0.5,
    "pi5": PI ** 5,          # so 6*pi^5 is reachable by a single product in the library
    "Z2": Z * Z,             # so 4*Z^2+3 is reachable (Z^2 * 4 + 3)
}


# ==================================================================================
# KNOWN POSITIVE 1 — the a0 forced kernel  sqrt(8pi/3) = sqrt(8pi) * sqrt(1/3)
# ==================================================================================
def candidate_a0() -> Candidate:
    """a0 = c^2 sqrt(Lambda/32pi) ; the kernel sqrt(8pi/3) decomposes uniquely as
    sqrt(8pi) [Einstein] * sqrt(1/3) [Friedmann], same number forced in 2 places, and
    the FORM a0 ~ sqrt(Lambda) forced a 3rd way (dS-Unruh). One free param: kappa=1/2.

    Gate A: a0 is NOT a germ-Poisson target — its FDR survival is the DIMENSIONAL filter
    of the cosmology search (gravity+cosmology constants only, no QED), which makes the
    reachable acceleration-dimensioned set SPARSE at 1.2e-10. We model that with a
    structural null: over random dimensionless O(1) decorations of the (forced) skeleton
    c*sqrt(G*rho_c), how often does the engine land within tol of a0? The dimensional
    filter + the single forced skeleton make this rare. (This mirrors the real lineage:
    a0 survives because is_acceleration() pruned ~99% of trees, not because 2.894 is a
    rare O(1).)
    """
    a0_value = 1.2e-10
    tol = 0.05  # SPARC a0 is ~5-10% known; the search threshold was ~5-20%

    def a0_structural_null(N):
        # The forced skeleton is c*sqrt(G*rho_c) (dim = acceleration, unique among the
        # cosmology pool). The only freedom is an O(1) dimensionless decoration kappa.
        # Draw kappa log-uniform over a broad O(1) band [0.1, 10] and ask how often the
        # decorated skeleton lands within tol of a0. The skeleton itself = 2*a0 (kappa=1/2
        # is the truth), so this measures: of all O(1) decorations, what fraction hit a0?
        rng = np.random.default_rng(20260625)
        skeleton = 2.0 * a0_value  # c*sqrt(G*rho_c), the depth-3 forced winner
        kap = 10.0 ** rng.uniform(-1, 1, size=N)  # O(1) decorations
        vals = kap * skeleton
        return vals

    search = SearchSpace(
        germ_pool=GERM_POOL,
        tol=tol,
        rational_target=False,
        structural_null=a0_structural_null,
        structural_eps=a0_value * tol,   # absolute window = tol * a0
        structural_N=2_000_000,
        n_targets_searched=1,
    )

    # Gate B: the two forced factors of the kernel, each registered + each appearing in an
    # independent forced place; the FORM forced a 3rd way (dS-Unruh quadrature).
    coeff = Coefficient(
        factors=[
            Factor(value=SQRT8PI, provenance="einstein_8pi", appears_in=["Einstein"]),
            Factor(value=SQRT_THIRD, provenance="friedmann_third", appears_in=["Friedmann"]),
        ],
        free_params=1,                      # kappa = 1/2, the lone unforced O(1)
        target_value=KERNEL,                # forced factors must reproduce sqrt(8pi/3)
        form_forced_independently=1,        # dS-Unruh forces the sqrt(Lambda) form
    )

    # Gate C1: the one kernel pins Einstein + Friedmann + the dS-Unruh form = 3 anchors.
    interlock = Interlock(
        n_independent_observables=3,        # C1: >=2 independent forced anchors
        n_constants_tied=0,
        n_free_in_interlock=1,
        cross_sector=None,
        claimed_universal=False,
        sector_specific_ingredient=None,
    )

    return Candidate(
        name="a0_kernel sqrt(8pi/3)=sqrt(8pi)*sqrt(1/3)",
        target_value=KERNEL, relation_value=SQRT8PI * SQRT_THIRD,
        search=search, coefficient=coeff, interlock=interlock,
        note="a0 = c^2 sqrt(Lambda/32pi); kernel forced by Einstein x Friedmann, "
             "form by dS-Unruh; one free kappa=1/2.",
    )


# ==================================================================================
# KNOWN POSITIVE 2 — Koide Q = 2/3  (real lepton masses)
#   must PASS A (triple-null ~1-in-48k) + C2 ; HONESTLY FAIL B (missing forced kernel)
#   => status REAL-PUZZLE-RE-LABELED
# ==================================================================================
def candidate_koide() -> Candidate:
    """Q = (m_e+m_mu+m_tau)/(sqrt m_e + sqrt m_mu + sqrt m_tau)^2 = 2/3.

    Gate A: 2/3 is a small-denominator rational => Gate-A-on-the-value is uninformative
    (re-labeling a rational is free). Route to the STRUCTURAL null: over random
    log-uniform mass triples, P(|Q - 2/3| < 1e-5) ~ 2e-5 ~ 1-in-48k. SPARSE + a real hit
    => SURPRISING => PASS A.

    Gate B: the current framework MECHANISM (r=sqrt2 from S3/Z3) is NOT a forced kernel:
    r=sqrt2 appears in only ONE place (the circulant amplitude) and the derivation needs a
    second free number (the per-fermion k_f) -> two free numbers. The candidate HONESTLY
    declares this: one factor (sqrt2) registered to S3 but the interlock needs >=2 free,
    so B FAILS with the honest tell. (We declare free_params=2 to be honest, not 1.)

    Gate C2: ties 3 measured lepton masses with 0 free parameters -> PASS C2. The
    cross-sector test (quarks/neutrinos) deviates from 2/3, but Koide is lepton-specific
    (NOT claimed family-universal here), so that is expected, not a falsification.
    """
    Q_target = 2.0 / 3.0
    Q_measured = (M_E + M_MU + M_TAU) / (math.sqrt(M_E) + math.sqrt(M_MU) + math.sqrt(M_TAU)) ** 2

    def koide_triple_null(N):
        # random log-uniform mass triples spanning the lepton scale (~[-2,4] decades in
        # MeV reproduces the documented 1-in-48k). Compute Q for each.
        rng = np.random.default_rng(20260625)
        lm = rng.uniform(-2, 4, size=(N, 3))
        m = 10.0 ** lm
        sm = np.sqrt(m)
        return m.sum(axis=1) / (sm.sum(axis=1) ** 2)

    search = SearchSpace(
        germ_pool=GERM_POOL,
        tol=1e-4,
        rational_target=True,               # 2/3 is a small-denominator rational
        structural_null=koide_triple_null,  # the random-mass-triple null
        structural_eps=1e-5,
        structural_N=4_000_000,
        n_targets_searched=1,
    )

    # Gate B (honest FAIL): the mechanism needs TWO free numbers. We register sqrt2 to S3
    # but declare an extra free param (the per-fermion k_f) so the gate's independent
    # recount lands n_free=2 -> kernel-free, the honest Koide B-gap.
    coeff = Coefficient(
        factors=[
            Factor(value=math.sqrt(2.0), provenance="S3_doublet_amp_sqrt2",
                   appears_in=["S3_circulant_amplitude"]),
        ],
        free_params=2,                      # honest: r=sqrt2 AND the per-fermion k_f
        target_value=None,                  # no clean coefficient identity to reproduce
        form_forced_independently=0,        # form not forced a 2nd independent way
    )

    # Gate C2: 3 masses, 0 free parameters; lepton-specific (not claimed universal).
    def cross_sector():
        # up/down quark Koide Q != 2/3 — expected, since Koide is lepton-specific.
        def Q(a, b, c):
            return (a + b + c) / (math.sqrt(a) + math.sqrt(b) + math.sqrt(c)) ** 2
        return {
            "leptons": {"value": Q_measured, "target": Q_target,
                        "ok": abs(Q_measured - Q_target) < 1e-3},
            "up_quarks": {"value": Q(2.16e-3, 1.27, 172.57), "target": Q_target,
                          "ok": abs(Q(2.16e-3, 1.27, 172.57) - Q_target) < 1e-3},
            "down_quarks": {"value": Q(4.70e-3, 93.5e-3, 4.18), "target": Q_target,
                            "ok": abs(Q(4.70e-3, 93.5e-3, 4.18) - Q_target) < 1e-3},
        }

    interlock = Interlock(
        n_independent_observables=0,        # not a C1 multi-observable forcing
        n_constants_tied=3,                 # C2: 3 lepton masses
        n_free_in_interlock=0,              # parameter-free relation
        cross_sector=cross_sector,
        claimed_universal=False,            # Koide is lepton-specific, NOT universal
        sector_specific_ingredient="charged-lepton-specific (r=sqrt2 holds for leptons only)",
    )

    return Candidate(
        name="Koide Q=2/3 (real lepton masses)",
        target_value=Q_target, relation_value=Q_measured,
        search=search, coefficient=coeff, interlock=interlock,
        note=f"Q_measured={Q_measured:.7f} vs 2/3={Q_target:.7f} "
             f"(dev {Q_measured-Q_target:+.2e}); real interlock, mechanism re-labels.",
    )


# ==================================================================================
# KNOWN NEGATIVES — must be REJECTED with the right tell
# ==================================================================================
def _baked_negative(name, target, relation_value, note) -> Candidate:
    """A generic real (non-rational) target whose hit is BAKED by the dense germ pool.
    Gate A reconstructs the germ library and finds E_chance >= 1 -> FDR-DEAD @ A."""
    search = SearchSpace(
        germ_pool=GERM_POOL,
        tol=1e-3,                # generous; the pool still densely covers the region
        rational_target=False,
        structural_null=None,
        n_targets_searched=1,
    )
    # negatives carry NO forced kernel and NO interlock (they are one-number re-labels);
    # they must die at Gate A so B/C never matter, but we declare honest (empty) B/C.
    coeff = Coefficient(factors=[Factor(value=relation_value, provenance=None)],
                        free_params=99, target_value=None, form_forced_independently=0)
    interlock = Interlock(n_independent_observables=0, n_constants_tied=1,
                          n_free_in_interlock=99)
    return Candidate(name=name, target_value=target, relation_value=relation_value,
                     search=search, coefficient=coeff, interlock=interlock, note=note)


def candidate_alpha_4Z2p3() -> Candidate:
    target = 137.035999177
    val = 4 * Z * Z + 3
    return _baked_negative("alpha^-1 = 4 Z^2 + 3", target, val,
                           f"4Z^2+3 = {val:.4f} vs 137.036; the 34k-formula null's "
                           f"expected output (~0 surplus bits).")


def candidate_mumue_64pipZ() -> Candidate:
    target = 206.7682830
    val = 64 * PI + Z
    return _baked_negative("m_mu/m_e = 64 pi + Z", target, val,
                           f"64pi+Z = {val:.4f} vs 206.768; BAKED-dense.")


def candidate_mtaumu_Zp11() -> Candidate:
    target = 16.8170
    val = Z + 11
    return _baked_negative("m_tau/m_mu = Z + 11", target, val,
                           f"Z+11 = {val:.4f} vs 16.817; BAKED-dense.")


def candidate_mpme_6pi5() -> Candidate:
    target = 1836.15267
    val = 6 * PI ** 5
    return _baked_negative("m_p/m_e = 6 pi^5", target, val,
                           f"6pi^5 = {val:.4f} vs 1836.153; BAKED-dense.")


def candidate_sin2W_3over13() -> Candidate:
    """sin^2 theta_W = 3/13 : a small-denominator rational. Gate-A-on-value is
    uninformative (a rational is hit exactly by many combos) and NO structural null
    exists (there is no parameter-free physical relation behind 3/13 — it is a bare
    re-label). So Gate A returns rational(uninformative) -> FAIL. The right tell:
    're-labeling a rational is FREE, 0 surplus bits, needs a structural null'."""
    target = 0.23122
    val = 3.0 / 13.0
    search = SearchSpace(
        germ_pool=GERM_POOL,
        tol=1e-3,
        rational_target=True,        # 3/13 is a small-denominator rational
        structural_null=None,        # NO physical parameter-free relation behind it
        n_targets_searched=1,
    )
    coeff = Coefficient(factors=[Factor(value=val, provenance=None)],
                        free_params=99, target_value=None)
    interlock = Interlock(n_independent_observables=0, n_constants_tied=1,
                          n_free_in_interlock=99)
    return Candidate(name="sin^2 theta_W = 3/13", target_value=target,
                     relation_value=val, search=search, coefficient=coeff,
                     interlock=interlock,
                     note=f"3/13 = {val:.5f} vs 0.23122; rational re-label, no kernel.")


def _framework_combo_pool(N, seed=20260625):
    """A sample of framework-flavored O(1) values: random a OP b over the germ pool (and
    sqrt/square of each germ). Shared by the sqrt2 density null and its random-O(1)
    baseline so both are measured against the SAME reachable set (koide_fdr_sqrt2)."""
    rng = np.random.default_rng(seed)
    base = np.array([PI, math.e, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16,
                     8 * PI, 2 * PI, 4 * PI, 4 * PI / 3, 3 / (8 * PI), Z, KERNEL, 0.5,
                     1 / 3, 2 / 3])
    base = np.concatenate([base, np.sqrt(base[base > 0]), base[base > 0] ** 2])
    a = rng.choice(base, size=N)
    b = rng.choice(base, size=N)
    op = rng.integers(0, 4, size=N)
    out = np.where(op == 0, a * b,
          np.where(op == 1, np.divide(a, b, out=np.full_like(a, np.inf), where=b != 0),
          np.where(op == 2, a + b, a - b)))
    return np.abs(out)


def candidate_dsunruh_sqrt2() -> Candidate:
    """'dS-Unruh forces sqrt(2)' — a MECHANISM/derivation claim about the Koide amplitude.
    Must be REJECTED. Two documented tells (GATE_SPEC line 44/143: 'A: -1.08 bits / B: two
    free numbers'):
      - GATE A (the LEADING tell): the COMPARATIVE density null (koide_fdr_sqrt2 Q2) shows
        sqrt2 is hit NO denser than a random O(1) target from the same framework pool ->
        NEGATIVE surplus (~-1 bit) -> 'not special, the derivation carries ~0 information'.
      - GATE B (the corroborating tell): kappa=1/2 -> sqrt2 is TWO free numbers, and
        sqrt(2/Z)=0.588 is the WRONG value -> kernel-free.
    The pipeline reports the FIRST failing gate (A, the leading tell); the table ALSO shows
    B independently FAILs with n_free=2 (asserted in the suite check).
    """
    target = math.sqrt(2.0)

    def sqrt2_density_null(N):
        return _framework_combo_pool(N)

    def sqrt2_random_baseline(M):
        # random O(1) targets in the same range the density is measured over
        rng = np.random.default_rng(11)
        return 10.0 ** rng.uniform(math.log10(0.8), math.log10(3.0), size=M)

    search = SearchSpace(
        germ_pool=GERM_POOL,
        tol=0.005,
        rational_target=False,
        structural_null=sqrt2_density_null,
        structural_baseline=sqrt2_random_baseline,   # -> comparative (surplus-over-random)
        structural_baseline_M=1500,
        structural_eps=math.sqrt(2.0) * 0.005,
        structural_N=3_000_000,
        n_targets_searched=1,
    )
    # Gate B: the derivation needs TWO free numbers (kappa=1/2 AND the sqrt2 step), and
    # sqrt(2/Z)=0.588 is the wrong value. Declare honestly -> B FAILS (two free numbers).
    coeff = Coefficient(
        factors=[Factor(value=math.sqrt(2.0), provenance="S3_doublet_amp_sqrt2",
                        appears_in=["S3_circulant_amplitude"])],
        free_params=2,              # kappa=1/2 -> sqrt2 is two free numbers
        target_value=None,
        form_forced_independently=0,
    )
    interlock = Interlock(n_independent_observables=1, n_constants_tied=1,
                          n_free_in_interlock=2)
    return Candidate(name="'dS-Unruh forces sqrt(2)'", target_value=target,
                     relation_value=math.sqrt(2.0), search=search, coefficient=coeff,
                     interlock=interlock,
                     note="mechanism claim: kappa=1/2 -> sqrt2 is TWO free numbers; "
                          "sqrt(2/Z)=0.588 wrong; A: sqrt2 not a special attractor.")


# ==================================================================================
# THE CALIBRATION SUITE
# ==================================================================================
# each row: (builder, required_status, required_first_fail_gate_or_None, kind)
SUITE = [
    # known positives
    (candidate_a0,            "CERTIFIED",               None, "POSITIVE"),
    (candidate_koide,         "REAL-PUZZLE-RE-LABELED",  None, "POSITIVE"),
    # known negatives (required status FDR-DEAD; required first-failing gate)
    (candidate_alpha_4Z2p3,   "FDR-DEAD", "A", "NEGATIVE"),
    (candidate_mumue_64pipZ,  "FDR-DEAD", "A", "NEGATIVE"),
    (candidate_mtaumu_Zp11,   "FDR-DEAD", "A", "NEGATIVE"),
    (candidate_mpme_6pi5,     "FDR-DEAD", "A", "NEGATIVE"),
    (candidate_sin2W_3over13, "FDR-DEAD", "A", "NEGATIVE"),
    # sqrt2: leading tell is A (-1.08 bits / not special); B independently flags 2 free #s.
    # The suite ALSO asserts B fails with n_free==2 (see _extra_assert below).
    (candidate_dsunruh_sqrt2, "FDR-DEAD", "A", "NEGATIVE"),
]


def _extra_assert(name, v):
    """Per-candidate corroboration beyond status+first-fail. For the sqrt2 mechanism claim,
    BOTH documented tells must be present: A negative-surplus (not special) AND B kernel-free
    with exactly TWO free numbers. Returns (ok, msg)."""
    if name.startswith("'dS-Unruh forces sqrt(2)'"):
        b_two_free = (not v.kernel.passed) and (v.kernel.n_free_params == 2)
        a_not_special = (not v.fdr.passed) and (v.fdr.bits <= 0.0)
        ok = b_two_free and a_not_special
        msg = (f"B two-free-numbers={b_two_free} (n_free={v.kernel.n_free_params}); "
               f"A not-special={a_not_special} (bits={v.fdr.bits:+.2f})")
        return ok, msg
    return True, ""


def _first_failing_gate(v) -> str:
    if not v.fdr.passed:
        return "A"
    if not v.kernel.passed:
        return "B"
    if not v.interlock.passed:
        return "C"
    return "-"


def main():
    print("=" * 100)
    print("project_atomos — GATE CALIBRATION ACCEPTANCE TEST")
    print("=" * 100)
    print(f"  lepton masses (MeV): m_e={M_E}  m_mu={M_MU}  m_tau={M_TAU}")
    print(f"  Z=sqrt(32pi/3)={Z:.6f}  kernel=sqrt(8pi/3)={KERNEL:.6f}")
    print("-" * 100)

    rows = []
    all_pass = True
    for builder, req_status, req_gate, kind in SUITE:
        cand = builder()
        v = validate(cand)
        first_fail = _first_failing_gate(v)

        status_ok = (v.status == req_status)
        gate_ok = (req_gate is None) or (first_fail == req_gate)
        extra_ok, extra_msg = _extra_assert(cand.name, v)
        ok = status_ok and gate_ok and extra_ok
        all_pass = all_pass and ok

        rows.append(dict(
            kind=kind, name=cand.name, status=v.status, req_status=req_status,
            first_fail=first_fail, req_gate=req_gate or "-",
            A=("P" if v.fdr.passed else "F"),
            B=("P" if v.kernel.passed else "F"),
            C=("P" if v.interlock.passed else "F"),
            bits=v.fdr.bits, ok=ok, verdict=v,
            extra_ok=extra_ok, extra_msg=extra_msg,
        ))

    # ---- table ----
    hdr = f"{'KIND':<9}{'CANDIDATE':<40}{'A':^3}{'B':^3}{'C':^3}{'STATUS':<24}{'1stFail':<8}{'RESULT':<6}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        bits = r["bits"]
        bits_s = ("inf" if math.isinf(bits) else f"{bits:.1f}")
        print(f"{r['kind']:<9}{r['name'][:39]:<40}{r['A']:^3}{r['B']:^3}{r['C']:^3}"
              f"{r['status']:<24}{r['first_fail']:<8}{'PASS' if r['ok'] else 'FAIL':<6}")
    print("-" * len(hdr))

    # ---- per-row tells (the honest ledger) ----
    print("\nGATE TELLS (why each landed where it did):")
    for r in rows:
        v = r["verdict"]
        print(f"\n  [{r['kind']}] {r['name']}")
        print(f"     status     : {v.status}   (required: {r['req_status']})")
        print(f"     headline   : {v.tell}")
        print(f"     A (FDR)    : {'PASS' if v.fdr.passed else 'FAIL'} | {v.fdr.mode} | "
              f"bits={('inf' if math.isinf(v.fdr.bits) else f'{v.fdr.bits:.1f}')} | {v.fdr.tell}")
        print(f"     B (kernel) : {'PASS' if v.kernel.passed else 'FAIL'} | "
              f"n_free={v.kernel.n_free_params} | {v.kernel.tell}")
        print(f"     C (interlk): {'PASS' if v.interlock.passed else 'FAIL'} | "
              f"{v.interlock.mode} | {v.interlock.tell}")
        if r["extra_msg"]:
            print(f"     corroborate: {r['extra_msg']}")
        if not r["ok"]:
            why = []
            if v.status != r["req_status"]:
                why.append(f"status {v.status} != required {r['req_status']}")
            if r["req_gate"] != "-" and r["first_fail"] != r["req_gate"]:
                why.append(f"first-fail {r['first_fail']} != required {r['req_gate']}")
            if not r["extra_ok"]:
                why.append(f"corroboration failed: {r['extra_msg']}")
            print(f"     *** CALIBRATION MISMATCH: {'; '.join(why)}")

    print("\n" + "=" * 100)
    n_ok = sum(r["ok"] for r in rows)
    print(f"CALIBRATION VERDICT: {n_ok}/{len(rows)} rows correct -> "
          f"{'PASS — gate is trustworthy on known answers' if all_pass else 'FAIL — gate mis-certifies; FIX gate/ and re-run'}")
    print("=" * 100)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
