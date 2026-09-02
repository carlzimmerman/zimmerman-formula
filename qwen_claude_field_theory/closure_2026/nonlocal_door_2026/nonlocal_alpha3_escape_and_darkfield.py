#!/usr/bin/env python3
"""Deprecated verifier for the withdrawn universal dark-field claim.

The original version returned success after hard-coding two central physics
claims and treating a response-denominator mismatch as alpha_3.  Keep this
entry point so old command ledgers fail honestly instead of silently
certifying the withdrawn result.
"""

from __future__ import annotations

from nonlocal_universal_claim_audit_2026 import derive_nonlocal_claim_audit


def main() -> int:
    result = derive_nonlocal_claim_audit()
    aqual = result["aqual"]
    ratio = result["ratio_lock"]
    ppn = result["ppn"]

    claimed_implications = {
        "toy retarded denominator derives alpha_3=0": ppn["alpha3_derived"],
        "toy denominator proves no added gravitational mode": ppn["gravitational_dof_derived"],
        "local exterior MOND cannot carry enclosed mass": not aqual["exterior_flux_contains_mass"],
        "ratio lock survives a different/sourced current": ratio["sourced_ratio_derivative"] == 0,
    }

    print("=" * 88)
    print("WITHDRAWN CLAIM VERIFIER: NONLOCAL ALPHA3 ESCAPE / UNIVERSAL DARK FIELD")
    print("=" * 88)
    for label, established in claimed_implications.items():
        print(f"  [{'PASS' if established else 'FAIL'}] {label}")
    print("\n[CORRECTED VERDICT]")
    print("  The universal theorem is not established.  The local AQUAL flux is a counterexample to")
    print("  its enclosed-mass premise; the shared-current ratio lock is conditional; and neither")
    print("  alpha_3 nor N_grav follows from the scalar response denominator.  Use")
    print("  nonlocal_universal_claim_audit_2026.py for the surviving scoped obstruction.")
    return 0 if all(claimed_implications.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
