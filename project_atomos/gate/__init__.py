"""
project_atomos.gate — the three-part validator that tells a real relation from a
fitted coincidence.

Public API:
    from gate import validate, fdr_test, forced_kernel_detector, interlock_check
    result = validate(candidate)   # -> Verdict

A candidate is CERTIFIED only if all three gates pass (A: FDR-survival,
B: forced kernel, C: interlock). Anything else is FDR-DEAD with the tell.

Provenance / spec: ../notes/GATE_SPEC.md, ../notes/ENGINE_REVERSE_ENGINEERING.md.
"""
from .fdr import fdr_test, build_value_set, FDRResult
from .forced_kernel import forced_kernel_detector, KernelResult
from .interlock import interlock_check, InterlockResult
from .verdict import validate, Verdict

__all__ = [
    "validate", "Verdict",
    "fdr_test", "build_value_set", "FDRResult",
    "forced_kernel_detector", "KernelResult",
    "interlock_check", "InterlockResult",
]
