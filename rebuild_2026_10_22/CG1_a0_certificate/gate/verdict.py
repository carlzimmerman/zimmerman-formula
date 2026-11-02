"""
Top-level validator: compose GATE A (FDR), GATE B (forced kernel), GATE C (interlock).

Pipeline rule (GATE_SPEC "How the three compose"):
  candidate -> A -> B -> C ; CERTIFIED iff all three pass.

But the gate must report the HONEST middle status the spec demands:
  - A relation that passes A (via the structural null) and C2 (Koide-class interlock)
    but whose current MECHANISM fails B (kernel-free; needs >=2 free numbers) is NOT
    certified, and NOT dismissed: it is "REAL-PUZZLE-RE-LABELED" — a genuine empirical
    interlock without a forced kernel yet. That is the exact, honest Koide verdict.
  - Everything else that fails any gate is FDR-DEAD with the tell of the first gate it
    fails (A: dense/0-bits/rational; B: no-provenance/>=2-free; C: re-description/cross-kill).
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .fdr import fdr_test, FDRResult
from .forced_kernel import forced_kernel_detector, KernelResult
from .interlock import interlock_check, InterlockResult


@dataclass
class Verdict:
    name: str
    status: str           # "CERTIFIED" | "REAL-PUZZLE-RE-LABELED" | "FDR-DEAD"
    fdr: FDRResult
    kernel: KernelResult
    interlock: InterlockResult
    tell: str             # the headline reason
    rel_error: float      # |relation - target|/|target| (closeness sanity, not a gate)

    @property
    def certified(self) -> bool:
        return self.status == "CERTIFIED"


def validate(candidate) -> Verdict:
    """Run all three gates and return the composed Verdict.

    Note: we run ALL THREE gates (not short-circuit) so the verdict can report the full
    A/B/C profile and distinguish CERTIFIED from REAL-PUZZLE-RE-LABELED. The pipeline
    pass/fail logic still requires all three for CERTIFIED.
    """
    a = fdr_test(candidate)
    b = forced_kernel_detector(candidate)
    c = interlock_check(candidate)

    tv = candidate.target_value
    rel_error = abs(candidate.relation_value - tv) / abs(tv) if tv else float("nan")

    if a.passed and b.passed and c.passed:
        status = "CERTIFIED"
        tell = (f"CERTIFIED: A(bits={a.bits:.1f}) + B(forced kernel, 1 free param) + "
                f"C({c.mode}). The a0/Koide signature: one-parameter, forced-kernel, "
                f"interlocking.")
    elif a.passed and c.passed and (c.mode == "C2") and (not b.passed):
        # the honest Koide middle: real empirical interlock, kernel-free mechanism
        status = "REAL-PUZZLE-RE-LABELED"
        tell = (f"REAL-PUZZLE-RE-LABELED: A passes (structural null surprising) and C2 "
                f"passes ({candidate.interlock.n_constants_tied} constants, "
                f"{candidate.interlock.n_free_in_interlock} free), but B FAILS "
                f"[{b.tell}]. A genuine interlock WITHOUT a forced kernel yet — the open "
                f"target, honestly labeled. NOT a win, NOT a dismissal.")
    else:
        status = "FDR-DEAD"
        # tell of the FIRST gate it fails (pipeline order A -> B -> C)
        if not a.passed:
            tell = f"FDR-DEAD @ GATE A: {a.tell}"
        elif not b.passed:
            tell = f"FDR-DEAD @ GATE B: {b.tell}"
        else:
            tell = f"FDR-DEAD @ GATE C: {c.tell}"

    return Verdict(name=candidate.name, status=status, fdr=a, kernel=b,
                   interlock=c, tell=tell, rel_error=rel_error)
