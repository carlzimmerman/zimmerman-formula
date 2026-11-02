#!/usr/bin/env python3
"""Applies CG1's repairs A1-A7 to the local copy of the gate (exact string replacements, each must match once). project_atomos untouched."""
import sys
def rep(fn, pairs):
    s = open(fn).read()
    for a, b in pairs:
        assert s.count(a) == 1, (fn, a[:50], s.count(a))
        s = s.replace(a, b)
    open(fn, "w").write(s)
rep("gate/candidate.py", [("    structural_N: int = 4_000_000\n", "    structural_N: int = 4_000_000\n    # CG1 A1: the value the structural null is compared with, in the null's own units. None = target_value.\n    structural_target: Optional[float] = None\n    structural_relation: Optional[float] = None   # CG1 A4: the relation, same units; None = relation_value\n")])
rep("gate/fdr.py", [
("PASS_BITS = 10.0   # operational threshold from GATE_SPEC A\n", "PASS_BITS = 10.0   # operational threshold from GATE_SPEC A\n\n# CG1 switches. All True is the repaired gate; all False reproduces the original.\nREPAIRS = dict(A2=True, A3=True, A4=True)\n"),
("""    p = float(np.mean(np.abs(out - target) < eps))
    return p
""", """    p = float(np.mean(np.abs(out - target) < eps))
    return p


def _support_mismatch(structural_null, target, N):
    \"\"\"CG1 A2: a target outside the null's support is a unit or scale error, not a surprise.\"\"\"
    out = np.asarray(structural_null(N))
    out = out[np.isfinite(out)]
    return not (out.min() <= target <= out.max())
"""),
("""    Comparable density => ~0 bits; LESS dense => NEGATIVE bits (the documented -1.08 for
    sqrt2 => 'not special, the derivation carries no information'). Returns""", """    Comparable density => ~0 bits. CG1 A6: as computed, MORE dense => NEGATIVE bits (a hit
    there is less surprising; the documented -1.08 for sqrt2), LESS dense => positive. Returns"""),
("""special = "SURPRISING: denser than a random O(1)" if passed else""", """special = "sparser than a random O(1), a hit is surprising" if passed else"""),
("""("NOT special: <= random density (mechanism carries ~0 info)\"""", """("NOT special: >= random density (mechanism carries ~0 info)\""""),
("""        p = _structural_null(s.structural_null, candidate.target_value,
                             s.structural_eps, s.structural_N)
""", """        tgt = s.structural_target if s.structural_target is not None else candidate.target_value
        rel = s.structural_relation if s.structural_relation is not None else candidate.relation_value
        if REPAIRS["A2"] and _support_mismatch(s.structural_null, tgt, s.structural_N):
            return FDRResult(passed=False, bits=0.0, mode="NULL-SCALE-MISMATCH", e_chance=float("nan"), n_hit=-1, chance_prob=float("nan"),
                             tell=f"target {tgt:.4g} is outside the null's support: unit or scale mismatch, no evidence either way")
        p = _structural_null(s.structural_null, tgt,
                             s.structural_eps, s.structural_N)
        if REPAIRS["A3"] and p == 0:
            p = 3.0 / s.structural_N   # CG1 A3: an upper limit, finite bits
        if REPAIRS["A4"] and abs(rel - tgt) >= s.structural_eps:
            return FDRResult(passed=False, bits=0.0, mode="NO-HIT", e_chance=float("nan"), n_hit=0, chance_prob=p,
                             tell=f"relation {rel:.5g} is outside the window {tgt:.5g} +- {s.structural_eps:.3g}; null P {p:.3e}, no hit to grade")
"""),
("""    n_hit, e_chance = _poisson_e_chance(candidate.target_value, lib, s.tol)
""", """    n_hit, e_chance = _poisson_e_chance(candidate.target_value, lib, s.tol)
    if REPAIRS["A4"] and abs(candidate.relation_value - candidate.target_value) > s.tol * abs(candidate.target_value):
        return FDRResult(passed=False, bits=0.0, mode="NO-HIT", e_chance=e_chance, n_hit=n_hit, chance_prob=1.0,
                         tell=f"relation {candidate.relation_value:.6g} is outside tol {s.tol} of the target; E_chance {e_chance:.2f}")
"""),
])
rep("gate/forced_kernel.py", [
("""@dataclass
class KernelResult:""", """# CG1 A5: True requires the implied free number to be p/q, p, q <= 4; False is the original 0.05-20 test.
REPAIR_A5 = True
SIMPLE = sorted({p / q for p in range(1, 5) for q in range(1, 5)})


@dataclass
class KernelResult:"""),
("""                coeff_reproduced = (0.05 < abs(implied_free) < 20.0)
""", """                coeff_reproduced = (any(abs(abs(implied_free) - k) < 1e-9 for k in SIMPLE) if REPAIR_A5 else (0.05 < abs(implied_free) < 20.0))
"""),
("""                f"({n_appear} independent forced appearances), exactly 1 free param (kappa).")
""", """                f"({n_appear} declared forced appearances; DECLARED, NOT VERIFIED), exactly 1 free param (kappa).")
"""),
])
rep("gate/interlock.py", [("""        tell = (f"PASS via {mode}: "
""", """        tell = (f"PASS via {mode} (DECLARED, NOT VERIFIED): "
""")])
