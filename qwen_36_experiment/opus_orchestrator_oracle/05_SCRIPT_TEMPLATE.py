#!/usr/bin/env python3
r"""<script_name>.py -- <ONE LINE: what question this answers, and the verdict>.

COPY THIS FILE. Keep the structure. Delete these instructions when done.

DOCSTRING CONTRACT -- every script in this corpus has all six parts:
  1. THE QUESTION. One paragraph. What is being asked and why it is open. Name the door.
  2. THE METHOD. How it is computed. Every approximation LABELLED as such.
  3. THE ANSWER. The verdict, with the numbers, stated up front. Do not bury it.
  4. CREDIT. The prior art (see 02_HOUSE_RULES.md R2). Mandatory if you use any of those objects.
  5. AGAINST INTEREST. What this script found that cuts AGAINST the framework. If genuinely nothing,
     write "searched, none found" -- but search first. A script with no against-interest section is
     assumed not to have looked.
  6. SCOPE. What class the result holds in, and one thing outside that class. Never claim closure.

Both a0 footings on every dimensional number (canonical 9.3614e-11, ALT 1.13e-10).
kappa = 1/2 is FITTED, NOT DERIVED.

Exit 0 = every check held. No check(True); every condition below can fail.
"""
from __future__ import annotations

import math
import sys

# ---------------------------------------------------------------------------------------------------
# locked constants -- copy from 04_FRAMEWORK_FACTS.md, never invent
G = 6.67430e-11
C_L = 2.99792458e8
LAM = 1.0908e-52
RHO_L = LAM * C_L**2 / (8 * math.pi * G)
CHL = C_L**2 * math.sqrt(LAM / 3)                 # 5.4194e-10
A0 = {"canonical": 9.3614e-11, "ALT": 1.13e-10}
Z_FW = 2 * math.sqrt(8 * math.pi / 3)             # 5.788810036466
KPC = 3.0856775814913673e19

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    """Record a check. `msg` must state the CLAIM and the NUMBER that establishes it."""
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 100)
    print(f"  {t}")
    print("=" * 100)


# ---------------------------------------------------------------------------------------------------
banner("S1  <what this section establishes>")

# ... compute ...

check(...,
      "S1a <the claim>, established by <the number>. <Why this check can fail: name an input that would "
      "break it.>")

# MANDATORY: prove by moving the number (03_NUMERIC_HAZARDS.md item 3)
banner("S2  PROVE BY MOVING THE NUMBER")
# something that SHOULD move:
check(...,
      "S2a doubling <input> changes <output> by <predicted factor>, confirming the dependence is real and not "
      "an accident of one parameter choice")
# something that should NOT move:
check(...,
      "S2b changing <irrelevant input> leaves <output> fixed to <tolerance>, confirming no spurious dependence")

# MANDATORY: refine once
banner("S3  REFINEMENT")
check(...,
      "S3a refining the grid/quadrature/series 4x moves the answer by <amount>, below the <tolerance> the "
      "conclusion needs -- so the result is resolved and not a discretisation artefact")

# MANDATORY: both footings
banner("S4  BOTH FOOTINGS")
for _nm, _a0 in A0.items():
    print(f"  footing {_nm:<10} a0 = {_a0:.4e} -> <result> = ...")
check(...,
      "S4a the verdict is the same on both footings (<value canonical> vs <value ALT>), so it does not depend "
      "on the a0 convention")

# MANDATORY: free-parameter count (02_HOUSE_RULES.md R1)
banner("S5  FREE PARAMETER COUNT")
N_FREE_BEFORE = 1        # kappa
N_FREE_AFTER = ...       # count them honestly
print(f"  free dimensionless parameters before: {N_FREE_BEFORE}   after: {N_FREE_AFTER}")
check(N_FREE_AFTER >= 0 and isinstance(N_FREE_AFTER, int),
      f"S5a free-parameter count is {N_FREE_AFTER}. If it is not LOWER than {N_FREE_BEFORE}, this is a "
      f"REPARAMETRISATION and not a derivation, and the ledger entry must say so in those words")

# ---------------------------------------------------------------------------------------------------
banner("RESULT")
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0. <the verdict in 2-4 lines, including what cuts against the framework and the scope>")
print("  kappa = 1/2 remains FITTED, NOT DERIVED.")
