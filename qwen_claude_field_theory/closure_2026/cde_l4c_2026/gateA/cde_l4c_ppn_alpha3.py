#!/usr/bin/env python3
"""Provenance audit for the withdrawn CDE-L4C alpha_3 extraction.

The instantaneous-versus-retarded denominator comparison is valid as a
principal response diagnostic.  It is not a boosted 1PN metric solution and
does not by itself determine a standard PPN parameter.  This script now tests
exactly that narrower statement and reports the missing calculation.
"""

from __future__ import annotations

import sys

import sympy as sp


def derive_provenance_audit() -> dict[str, object]:
    k, velocity, light_speed = sp.symbols("k w c", positive=True, real=True)
    omega = k * velocity
    instantaneous = 1 / k**2
    retarded = 1 / (k**2 - omega**2 / light_speed**2)
    mismatch = sp.series(instantaneous - retarded, velocity, 0, 3).removeO()
    normalized_mismatch = sp.simplify(mismatch * k**2 / (velocity**2 / light_speed**2))

    provided = {"scalar_constraint_response", "omega_independence", "principal_mismatch"}
    required = {
        "boosted_g00_to_1PN",
        "boosted_g0i_to_1PN",
        "boosted_gij_to_1PN",
        "constraint_backreaction",
        "matter_solution",
        "standard_PPN_gauge_map",
    }
    return {
        "instantaneous": instantaneous,
        "retarded": retarded,
        "instantaneous_is_omega_independent": sp.diff(instantaneous, velocity) == 0,
        "principal_mismatch": sp.simplify(mismatch),
        "normalized_principal_mismatch": normalized_mismatch,
        "provided_outputs": provided,
        "required_ppn_outputs": required,
        "alpha3_derived": required.issubset(provided),
    }


def main() -> int:
    result = derive_provenance_audit()
    checks = [
        result["instantaneous_is_omega_independent"],
        result["principal_mismatch"] != 0,
        result["normalized_principal_mismatch"] == -1,
        not result["alpha3_derived"],
    ]
    labels = [
        "the CDE-L4C constraint response is omega-independent at this principal level",
        "it differs from a luminal retarded scalar denominator at O(w^2)",
        "the normalized toy denominator mismatch equals -1",
        "the required boosted metric and PPN-gauge outputs were not computed",
    ]

    print("=" * 88)
    print("CDE-L4C PPN PROVENANCE AUDIT: PRINCIPAL MISMATCH IS NOT ALPHA_3")
    print("=" * 88)
    print("  R_constraint =", result["instantaneous"])
    print("  R_retarded =", result["retarded"])
    print("  O(w^2) mismatch =", result["principal_mismatch"])
    print("  normalized mismatch =", result["normalized_principal_mismatch"])
    for okay, label in zip(checks, labels):
        print(f"  [{'PASS' if okay else 'FAIL'}] {label}")
    print("\n[CORRECTED VERDICT]")
    print("  CDE-L4C has an instantaneous principal constraint response, but alpha_3 is OPEN.")
    print("  A full boosted 1PN solution, including all metric components, constraint backreaction,")
    print("  matter equations, and the standard PPN gauge map, is the unavoidable next calculation.")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
