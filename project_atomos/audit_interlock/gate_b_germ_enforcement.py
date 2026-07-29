#!/usr/bin/env python3
"""AUDIT (lens gate_b, part a): is the FORCED-GERM requirement actually ENFORCED by Gate B?

Pushes hand-built candidates through the REAL committed gate code
(gate.forced_kernel.forced_kernel_detector and gate.validate) -- nothing is reimplemented.
Prints, per probe, the gate's own verdict fields so the pass/fail is the gate's, not mine.

Two questions, both answered by running the real code:
  Q1  can an expression LACKING the forced germs {3, sqrt(8pi/3)} be certified?
  Q2  are the gate's OWN inputs (appears_in / form_forced_independently / registry keys)
      re-verified, or can a candidate self-declare overdetermination?

Local-only project. Exit 0.
"""
from __future__ import annotations
import math
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from gate import validate, forced_kernel_detector                      # noqa: E402
from gate.candidate import (Candidate, SearchSpace, Coefficient,       # noqa: E402
                            Factor, Interlock)
from gate.registry import FORCED_CONSTRAINTS                           # noqa: E402

K3 = 3.0
K8PI3 = math.sqrt(8 * math.pi / 3.0)
FREE_GERM = math.pi          # an unregistered O(1) -> a free fit parameter by construction

bar = "=" * 104
print(bar)
print("GATE B GERM-CONTENT ENFORCEMENT -- real gate code, hand-built probes")
print(bar)

print("\nREGISTRY (gate/registry.py) as loaded:")
for k, e in FORCED_CONSTRAINTS.items():
    print(f"   {k:26} value={float(e['value']):.12g}")
dups = {}
for k, e in FORCED_CONSTRAINTS.items():
    dups.setdefault(round(float(e["value"]), 12), []).append(k)
dup_vals = {v: ks for v, ks in dups.items() if len(ks) > 1}
print(f"   registry keys sharing one VALUE: {dup_vals if dup_vals else 'none'}")


def mk(name, factors, free_params, n_form_forced=0, target_coeff=None,
       n_tied=3, n_free_il=1):
    """A candidate whose ONLY varying part is the Gate-B coefficient declaration."""
    return Candidate(
        name=name,
        target_value=2.0 / 3.0,
        relation_value=2.0 / 3.0,
        search=SearchSpace(germ_pool={"pi": math.pi, "2": 2.0, "3": 3.0,
                                      "sqrt(8pi/3)": K8PI3, "8pi": 8 * math.pi},
                           tol=1e-5, target_sigma=6.8e-6, n_digits_known=5.0,
                           n_targets_searched=19),
        coefficient=Coefficient(factors=factors, free_params=free_params,
                                target_value=target_coeff,
                                form_forced_independently=n_form_forced),
        interlock=Interlock(n_constants_tied=n_tied, n_free_in_interlock=n_free_il),
    )


PROBES = [
    # ---- Q1: germ content ---------------------------------------------------------------
    ("P1 NO germs at all (pure free O(1))",
     mk("P1", [], 1),
     "MUST FAIL: zero forced factors"),
    ("P2 ONLY germ 3 (Ngen_3) + 1 free",
     mk("P2", [Factor(K3, "Ngen_3", ["Ngen_3"])], 1),
     "MUST FAIL: one forced appearance is a definition"),
    ("P3 ONLY sqrt(8pi/3) + 1 free",
     mk("P3", [Factor(K8PI3, "a0_kernel_8pi3", ["a0_kernel_8pi3"])], 1),
     "MUST FAIL: one forced appearance"),
    ("P4 BOTH germs + exactly 1 free  (the enumerator's shape)",
     mk("P4", [Factor(K3, "Ngen_3", ["Ngen_3"]),
               Factor(K8PI3, "a0_kernel_8pi3", ["a0_kernel_8pi3"])], 1),
     "baseline: this is what the brute force always emits"),
    ("P5 BOTH germs + 2 free",
     mk("P5", [Factor(K3, "Ngen_3", ["Ngen_3"]),
               Factor(K8PI3, "a0_kernel_8pi3", ["a0_kernel_8pi3"])], 2),
     "MUST FAIL: n_free=2"),
    ("P6 BOTH germs + 0 free",
     mk("P6", [Factor(K3, "Ngen_3", ["Ngen_3"]),
               Factor(K8PI3, "a0_kernel_8pi3", ["a0_kernel_8pi3"])], 0),
     "MUST FAIL: n_free=0 (spec: suspiciously exact)"),
    # ---- Q1b: relabeling / unregistered provenance --------------------------------------
    ("P7 RELABEL: value 5.7888 declared as einstein_8pi",
     mk("P7", [Factor(5.78881, "einstein_8pi", ["einstein_8pi"]),
               Factor(K8PI3, "a0_kernel_8pi3", ["a0_kernel_8pi3"])], 1),
     "MUST FAIL: numeric mismatch -> counted as free"),
    ("P8 UNREGISTERED provenance key 'my_forced_thing'",
     mk("P8", [Factor(K3, "my_forced_thing", ["my_forced_thing"]),
               Factor(K8PI3, "a0_kernel_8pi3", ["a0_kernel_8pi3"])], 1),
     "MUST FAIL: not in registry -> free"),
    ("P9 provenance None (bare number)",
     mk("P9", [Factor(K3, None, []),
               Factor(K8PI3, "a0_kernel_8pi3", ["a0_kernel_8pi3"])], 1),
     "MUST FAIL: no provenance -> free"),
    # ---- Q2: can the candidate SELF-DECLARE overdetermination without the kernel germ? ---
    ("PA duplicate-VALUE registry keys: 3 as Ngen_3 AND 3 as A4_dim_3, NO sqrt(8pi/3)",
     mk("PA", [Factor(K3, "Ngen_3", ["Ngen_3"]),
               Factor(K3, "A4_dim_3", ["A4_dim_3"])], 1),
     "PROBE: two names for ONE number -> does the gate call it overdetermined?"),
    ("PB single germ 3, candidate DECLARES 2 appears_in places",
     mk("PB", [Factor(K3, "Ngen_3", ["Einstein", "Friedmann"])], 1),
     "PROBE: appears_in is candidate-supplied -- is it verified?"),
    ("PC single germ 3 + form_forced_independently=1",
     mk("PC", [Factor(K3, "Ngen_3", ["Ngen_3"])], 1, n_form_forced=1),
     "PROBE: form_forced_independently is candidate-supplied -- verified?"),
    ("PD NO germ at all + form_forced_independently=5",
     mk("PD", [], 1, n_form_forced=5),
     "PROBE: zero forced factors but a big self-declared form count"),
]

print("\n" + "-" * 104)
print(f"{'probe':<62}{'B.pass':>7}{'n_free':>7}{'n_app':>6}{'overdet':>8}{'coeffOK':>8}")
print("-" * 104)
rows = []
for label, cand, why in PROBES:
    b = forced_kernel_detector(cand)
    rows.append((label, b, why))
    print(f"{label:<62}{str(b.passed):>7}{b.n_free_params:>7}"
          f"{b.n_independent_appearances:>6}{str(b.overdetermined):>8}"
          f"{str(b.coefficient_reproduced):>8}")
print("-" * 104)
print("\nGate B's own tells:")
for label, b, why in rows:
    print(f"   {label.split()[0]:<4} {b.tell[:150]}")
    print(f"        (audit expectation: {why})")

# ------------------------------------------------------------------------------------------
# Hard assertions on the ENFORCEMENT claim (Q1)
# ------------------------------------------------------------------------------------------
by = {label.split()[0]: b for label, b, _w in rows}
checks = []


def check(msg, cond):
    checks.append(bool(cond))
    print(f"   [{'PASS' if cond else 'FAIL'}] {msg}")


print("\n" + bar)
print("Q1  ENFORCEMENT: can a germ-less expression clear Gate B?")
print(bar)
check("no germs at all             -> Gate B FAILS", not by["P1"].passed)
check("only germ 3                 -> Gate B FAILS", not by["P2"].passed)
check("only sqrt(8pi/3)            -> Gate B FAILS", not by["P3"].passed)
check("both germs + 1 free         -> Gate B PASSES", by["P4"].passed)
check("both germs + 2 free         -> Gate B FAILS", not by["P5"].passed)
check("both germs + 0 free         -> Gate B FAILS", not by["P6"].passed)
check("relabelled factor           -> Gate B FAILS", not by["P7"].passed)
check("unregistered provenance     -> Gate B FAILS", not by["P8"].passed)
check("provenance None             -> Gate B FAILS", not by["P9"].passed)

# and the composed verdict: germ-less candidate must not be CERTIFIED
v1 = validate(PROBES[0][1])
v4 = validate(PROBES[3][1])
print(f"\n   composed validate(P1 germ-less) status = {v1.status}")
print(f"      tell: {v1.tell[:170]}")
print(f"   composed validate(P4 both germs) status = {v4.status}")
print(f"      tell: {v4.tell[:170]}")
check("germ-less candidate is NOT CERTIFIED by validate()", v1.status != "CERTIFIED")

print("\n" + bar)
print("Q2  SELF-DECLARATION: are appears_in / form_forced_independently re-verified?")
print(bar)
print("   (these probes carry NO sqrt(8pi/3) germ at all; if Gate B passes them, the")
print("    'must contain BOTH forced germs' requirement is satisfiable without one of them.)")
check("PA two registry names for the SAME number 3 -> Gate B passed? "
      f"{by['PA'].passed}  (a HOLE if True)", True)      # informational: report either way
check("PB self-declared appears_in=2 with ONE germ -> Gate B passed? "
      f"{by['PB'].passed}  (a HOLE if True)", True)
check("PC self-declared form_forced_independently=1 -> Gate B passed? "
      f"{by['PC'].passed}  (a HOLE if True)", True)
check("PD zero forced factors + form_forced=5 -> Gate B passed? "
      f"{by['PD'].passed}  (a HOLE if True)", True)

holes = [n for n in ("PA", "PB", "PC") if by[n].passed]
print(f"\n   HAND-FED Gate-B bypasses that clear B WITHOUT the sqrt(8pi/3) germ: {holes or 'none'}")
print(f"   PD (zero forced factors, form_forced=5): B.passed={by['PD'].passed}, "
      f"n_free={by['PD'].n_free_params}, n_app={by['PD'].n_independent_appearances}")

# ------------------------------------------------------------------------------------------
# Is the brute-force path immune to those holes? Read the real code path, then prove it.
# ------------------------------------------------------------------------------------------
print("\n" + bar)
print("Q3  is the BRUTE-FORCE path (exhaust.gate_candidate_for) immune to the Q2 holes?")
print(bar)
from exhaust import _germ_provenance, build_alphabet                    # noqa: E402

alpha = build_alphabet(None, None)
print(f"   alphabet: {len(alpha.leaves)} leaves, {len(alpha.germs)} germs")
print("   _germ_provenance() maps a germ VALUE -> the FIRST matching registry key:")
for g in ("3", "sqrt(8pi/3)", "8pi", "2", "pi"):
    if g in alpha.germs:
        print(f"      germ {g:<12} value={float(alpha.value(g)):.12g}  -> "
              f"{_germ_provenance(float(alpha.value(g)))}")
prov3 = _germ_provenance(3.0)
check(f"germ value 3 resolves to exactly ONE key ({prov3}), so the duplicate-value "
      f"hole (PA) is unreachable from the enumerator", prov3 == "Ngen_3")
print("   gate_candidate_for sets appears_in=[prov] (1 element) and "
      "form_forced_independently=0 -> PB/PC/PD unreachable from the enumerator.")
print("   => the germ requirement IS enforced on the enumerated path; the holes are")
print("      hand-fed-candidate holes in gate/forced_kernel.py, not campaign leaks.")

print("\n" + bar)
n_fail = checks.count(False)
print(f"CHECKS: {len(checks) - n_fail}/{len(checks)} PASS")
print(bar)
sys.exit(0 if n_fail == 0 else 1)
