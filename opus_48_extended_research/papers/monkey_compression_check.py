#!/usr/bin/env python3
"""Verify every number in MONKEY_COMPRESSION.md ("Monkeys, Hamlet, and the Price of a Prompt").

Conventions (as stated in the paper's Appendix A):
  27-key uniform keyboard; expected wait W(N) = 27^N keystrokes for an N-character
  target (sliding-window, non-self-overlapping approximation); 1e6 monkeys at
  2 keystrokes/s each -> aggregate R = 2e6 keys/s; year = 3.156e7 s; age of the
  universe = 1.38e10 yr; Hamlet ~ 130,000 characters.

Exit 0 iff every claim checks within its stated tolerance.  No inputs, no network.
"""
import math
import sys

LOG27 = math.log10(27.0)
R = 2.0e6                # aggregate keystrokes / second
YEAR = 3.156e7           # seconds
UNIVERSE = 1.38e10       # years
FAILURES = []


def check(name, got, want, rtol):
    ok = abs(got - want) <= rtol * abs(want)
    print(f"[{'ok' if ok else 'FAIL'}] {name:58s} got {got:.6g}  want {want:.6g}  rtol {rtol:g}")
    if not ok:
        FAILURES.append(name)


def log10_wait_years(n_chars):
    """log10 of expected wait in years for an n-character target."""
    return n_chars * LOG27 - math.log10(R) - math.log10(YEAR)


# ---- 1. constants ----
check("log10(27)", LOG27, 1.431364, 1e-6)

# ---- 2. Hamlet directly (exponents; the numbers only fit in logs) ----
lg_keys = 130000 * LOG27
check("Hamlet: log10(keystrokes)", lg_keys, 186077.3, 1e-5)
check("Hamlet: log10(seconds)", lg_keys - math.log10(R), 186071.0, 1e-5)
lg_years = log10_wait_years(130000)
check("Hamlet: log10(years)", lg_years, 186063.5, 1e-5)
check("Hamlet: log10(universe ages)", lg_years - math.log10(UNIVERSE), 186053.4, 1e-5)
# monkeys barely matter: aggregate rate removes ~6.3 units from the exponent
check("Hamlet: exponent drop from all monkey throughput", math.log10(R), 6.3, 2e-3)
# Hamlet-length robustness band quoted in Appendix A
check("Hamlet 120k chars: log10(keystrokes)", 120000 * LOG27, 171764, 5e-3)
check("Hamlet 180k chars: log10(keystrokes)", 180000 * LOG27, 257646, 5e-3)

# ---- 3. prompt table ----
check('"write hamlet in full" (20): keystrokes', 27.0**20, 4.24e28, 5e-3)
check('"write hamlet in full" (20): seconds', 27.0**20 / R, 2.12e22, 5e-3)
check('"write hamlet in full" (20): years', 27.0**20 / R / YEAR, 6.72e14, 5e-3)
check('"write hamlet in full" (20): universe ages', 27.0**20 / R / YEAR / UNIVERSE, 4.87e4, 5e-3)

check('"write hamlet" (12): keystrokes', 27.0**12, 1.501e17, 5e-3)
check('"write hamlet" (12): seconds', 27.0**12 / R, 7.50e10, 5e-3)
check('"write hamlet" (12): years', 27.0**12 / R / YEAR, 2378.0, 5e-3)

check("8-char prompt: keystrokes", 27.0**8, 2.82e11, 5e-3)
check("8-char prompt: days", 27.0**8 / R / 86400.0, 1.63, 5e-3)

check('"hamlet" (6): keystrokes', 27.0**6, 3.874e8, 5e-3)
check('"hamlet" (6): seconds', 27.0**6 / R, 193.7, 5e-3)
check('"hamlet" (6): minutes', 27.0**6 / R / 60.0, 3.23, 5e-3)

# ---- 4. derived claims ----
check("monkeys for 'write hamlet' in one expected day",
      27.0**12 / 86400.0 / 2.0, 8.7e11, 2e-2)
check('bits in "hamlet" (6 * log2 27)', 6 * math.log2(27.0), 28.5, 2e-3)
check("politeness factor 27^14", 27.0**14, 1.09e20, 5e-3)
check("time compression Hamlet-direct vs 'write hamlet' (log10)",
      log10_wait_years(130000) - math.log10(27.0**12 / R / YEAR), 186060.1, 1e-5)
check("prompt-side compression 27^(130000-12) (log10)",
      (130000 - 12) * LOG27, 186060.1, 1e-5)

# each character removed divides the wait by exactly 27
check("per-character factor W(12)/W(11)", 27.0**12 / 27.0**11, 27.0, 1e-12)

# ---- 5. string lengths used in the paper ----
for s, n in (("write hamlet in full", 20), ("write hamlet", 12), ("hamlet", 6)):
    check(f'len("{s}")', float(len(s)), float(n), 0)
check("politeness overhead: 20 - 6 chars", 20.0 - 6.0, 14.0, 0)

print()
if FAILURES:
    print(f"{len(FAILURES)} FAILED: {FAILURES}")
    sys.exit(1)
print("ALL CHECKS PASS -- every number in MONKEY_COMPRESSION.md verified.")
sys.exit(0)
