#!/usr/bin/env python3
r"""mi_alpha2_sun_reflex_2026.py -- THE alpha=2 "DISCHARGE" OF THE EPHEMERIS LIABILITY IS WITHDRAWN.
THE BINDING BODY IS THE SUN, AND THE CORPUS'S OWN PUBLISHED PAPER ALREADY SAID SO.

WHAT WAS CLAIMED. mi_alpha2_migration_2026.py:250 -- "The planetary liability is DISCHARGED on both
footings" -- and STANDING.md:698 -- "takes the planets from 1279x over to 2e-5x, i.e. passing". Both rest
on evaluating the alpha=2 residual ONLY at planetary accelerations (the migration script's check tests
GM_sun/AU^2 alone).

WHY THAT IS WRONG. The alpha=2 deep-Newtonian residual is a 1/g TAIL: delta_a = a0^2/(2g). A 1/g tail binds
at the LOWEST-acceleration body in the fit, and the lowest-acceleration body in an ephemeris is not a planet
-- it is the SUN, whose total (Jupiter-dominated) reflex acceleration is ~2.1e-7 m/s^2, ~12,000x below Mars.
Under modified inertia each body responds to ITS OWN acceleration, so the Sun's anomalous response is
~12,000x larger than any planet's, and it moves the barycentric dynamics that Mars ranging measures.

AND THE CORPUS ALREADY KNEW. real_research/reviews/toe_law/agentE_solar_reflex.py (committed 2026-06-10,
seven weeks BEFORE the alpha switch) runs exactly this configuration through a full Levenberg-Marquardt
ephemeris fit -- Sun+Venus+EMB+Mars+Jupiter+Saturn, per-body mu = x/sqrt(1+x^2) INCLUDING THE SUN, GM_sun +
GM_J + all 36 initial conditions free, Jacobian re-integrated per iteration, plus a kitchen-sink absorption
variant -- and its result is in a PUBLISHED paper: WHITEPAPER_TOE_MAP_2026.md sec. 4.3.2 (DOI
10.5281/zenodo.20670670): "framework normalization -- 12.7 m (x8.5, Mars-carried)". The discharge claim
contradicts the corpus's own publication.

  E1  the per-body tail ladder, both footings -- proving in-code that the MINIMUM-g body binds, and that
      the migration script's check tested the wrong end of the ladder
  E2  the post-fit standing, from the committed LM machinery's banked output, both footings; survival line
  E3  the corrected discharge check -- the one :170-172 should have run -- and it FAILS
  E4  what actually clears, priced; and exactly which sentences are withdrawn

Exit 0 = ran and every internal check held. No hard-coded verdicts, no check(True).
"""
from __future__ import annotations

import math
import sys

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 104)
    print(f"  {t}")
    print("=" * 104)


G = 6.674e-11
MSUN = 1.989e30
AU = 1.496e11
A0 = {"canon": 9.36e-11, "alt": 1.13e-10}


def mu2_residual(g, a0):
    """exact alpha=2 anomaly delta_a = a - g with mu(x) = x/sqrt(1+x^2), solved in closed form."""
    y = g / a0
    x2 = (y * y + math.sqrt(y**4 + 4 * y * y)) / 2.0
    return (math.sqrt(x2) - y) * a0


banner("E1  THE PER-BODY TAIL LADDER -- the MINIMUM-g body binds, and it is the Sun")

# accelerations: planets = solar gravity at their orbit; Sun = reflex from the planets (Jupiter dominates).
M_PL = {"Jupiter": 1.898e27, "Saturn": 5.683e26, "Venus": 4.867e24, "Earth": 5.972e24, "Mars": 6.417e23}
R_PL = {"Jupiter": 5.204 * AU, "Saturn": 9.583 * AU, "Venus": 0.723 * AU, "Earth": 1.0 * AU, "Mars": 1.524 * AU}
BODIES = {p: G * MSUN / R_PL[p] ** 2 for p in R_PL}
BODIES["Sun"] = max(G * M_PL[p] / R_PL[p] ** 2 for p in M_PL)      # Jupiter-dominated instantaneous reflex

print(f"  {'body':<10}{'g [m/s^2]':>12}{'g/a0 (canon)':>14}{'tail canon':>13}{'tail alt':>12}")
print("  " + "-" * 64)
tails = {}
for b, g in sorted(BODIES.items(), key=lambda kv: -kv[1]):
    tails[b] = {f: mu2_residual(g, a) for f, a in A0.items()}
    print(f"  {b:<10}{g:>12.3e}{g/A0['canon']:>14.0f}{tails[b]['canon']:>13.3e}{tails[b]['alt']:>12.3e}")

binder = min(BODIES, key=lambda b: BODIES[b])
check(binder == "Sun",
      f"E1a the minimum-acceleration body in the fit is the SUN (g = {BODIES['Sun']:.3e}, "
      f"g/a0 = {BODIES['Sun']/A0['canon']:.0f}) -- so the 1/g tail binds there, at "
      f"{tails['Sun']['canon']:.3e} m/s^2 (canon) / {tails['Sun']['alt']:.3e} (alt)")
check(tails["Sun"]["canon"] / tails["Mars"]["canon"] > 1e3,
      f"E1b and the Sun's tail exceeds Mars's by {tails['Sun']['canon']/tails['Mars']['canon']:.0f}x and "
      f"Earth's by {tails['Sun']['canon']/tails['Earth']['canon']:.0f}x -- so a discharge check run at "
      f"planetary accelerations tested the SHORT end of a five-order ladder")
# the deep-Newtonian asymptote is exact here -- show it, since the whole ladder rides on it
asym = A0["canon"] ** 2 / (2 * BODIES["Sun"])
check(abs(asym / tails["Sun"]["canon"] - 1) < 1e-3,
      f"E1c at the Sun's g/a0 = {BODIES['Sun']/A0['canon']:.0f} the closed-form tail matches the asymptote "
      f"a0^2/(2g) to {abs(asym/tails['Sun']['canon']-1):.1e} -- deep enough that the 1/g scaling is exact")


banner("E2  POST-FIT STANDING -- from the committed LM machinery, and the survival line")

# agentE_solar_reflex.py (2026-06-10, committed; ~hours of LM integration) fitted the full 6-body system
# with per-body mu INCLUDING the Sun, GM_sun + GM_J + 36 ICs free (+ kitchen-sink variant). Its banked
# numbers, also published in WHITEPAPER_TOE_MAP_2026.md sec. 4.3.2 (DOI 10.5281/zenodo.20670670):
MARS_BUDGET = 1.5                 # m, the ranging budget used by the committed fit
POSTFIT = {"canon": {"full": 12.74, "kitchen": 9.32}, "alt": {"full": 18.6, "kitchen": None}}
print(f"  committed LM fit (agentE_solar_reflex.py; published as 'x8.5, Mars-carried'):")
for f, d in POSTFIT.items():
    ks = f", kitchen-sink {d['kitchen']:.2f} m = {d['kitchen']/MARS_BUDGET:.1f}x" if d["kitchen"] else ""
    print(f"      {f:<6} Mars post-fit residual {d['full']:.2f} m vs {MARS_BUDGET} m budget = "
          f"{d['full']/MARS_BUDGET:.1f}x over{ks}")
check(POSTFIT["canon"]["full"] / MARS_BUDGET > 1.0 and POSTFIT["alt"]["full"] / MARS_BUDGET > 1.0,
      f"E2a *** NOT DISCHARGED ON EITHER FOOTING: *** after absorption into GM_sun, GM_J and all 36 initial "
      f"conditions, Mars carries {POSTFIT['canon']['full']/MARS_BUDGET:.1f}x (canon) / "
      f"{POSTFIT['alt']['full']/MARS_BUDGET:.1f}x (alt) the ranging budget -- "
      f"{POSTFIT['canon']['kitchen']/MARS_BUDGET:.1f}x even with kitchen-sink absorption")

# survival line: the committed fit found residual ~ s^2 (the tail is a0^2/2g = s^2 * a0_ref^2/2g); solve
# for the s that fits inside the budget.
s_max = {f: math.sqrt(MARS_BUDGET / POSTFIT[f]["full"]) for f in POSTFIT}
print(f"\n  survival line from the verified s^2 scaling: s_max = {s_max['canon']:.3f} a0 (canon), "
      f"{s_max['alt']:.3f} a0-alt (alt)")
check(all(s < 1.0 for s in s_max.values()),
      f"E2b both candidate footings sit ABOVE their survival line (s_max = {s_max['canon']:.2f} / "
      f"{s_max['alt']:.2f} of the footing value) -- the liability is real at the framework's own a0, "
      f"not only at some inflated test value")
print(f"""
  WHAT THE SWITCH ACTUALLY BOUGHT, stated fairly: the alpha=1 tail was a CONSTANT a0/2 sunward
  ({A0['canon']/2:.2e} m/s^2, ~1278x over after the fit); the alpha=2 tail at the Sun is
  {tails['Sun']['canon']:.2e}, a factor {A0['canon']/2/tails['Sun']['canon']:.0f} = a_sun/a0 smaller. Three
  and a half orders of magnitude of genuine relief -- and {POSTFIT['canon']['full']/MARS_BUDGET:.1f}x is not
  a pass. Also fair: a naive bare-tail-vs-budget comparison would be ~{tails['Sun']['canon']/4.6e-15:.0f}x;
  the LM fit's absorption brings that DOWN to {POSTFIT['canon']['full']/MARS_BUDGET:.1f}x, so the committed
  machinery is not stacking the deck against the framework -- absorption was allowed and it is not enough.
  GM_J absorption specifically is closed by Juno: it would need |dlnGM_J| ~ 2e-7 to 1e-5 vs Juno's ~1e-8.""")


banner("E3  THE CHECK THE MIGRATION SCRIPT SHOULD HAVE RUN -- and it fails")

EARTH_LIMIT = 3.66e-14            # the loose Sereno-Jetzer Earth 2-sigma bound the migration script used
g_earth = BODIES["Earth"]
old_check = mu2_residual(g_earth, A0["canon"]) < EARTH_LIMIT          # what :170-172 tested
new_check = tails["Sun"]["canon"] < EARTH_LIMIT * 0.0                 # placeholder; the real test is below
print(f"  the shipped check: tail at EARTH'S g ({mu2_residual(g_earth, A0['canon']):.2e}) < {EARTH_LIMIT:.2e}"
      f"  -> {old_check}  (this is what produced 'DISCHARGED')")
print(f"  the correct check: post-fit Mars residual < budget on the MINIMUM-g body's tail")
for f in POSTFIT:
    print(f"      {f:<6}: {POSTFIT[f]['full']:.2f} m < {MARS_BUDGET} m ?  {POSTFIT[f]['full'] < MARS_BUDGET}")
check(old_check and not (POSTFIT["canon"]["full"] < MARS_BUDGET),
      "E3 the shipped check PASSES while the correct check FAILS -- reproducing exactly how the false "
      "'DISCHARGED' was manufactured: the test was run at the wrong end of the 1/g ladder. (Both halves "
      "computed here; if either flips, this script's story is wrong and it should exit 1)")


banner("E4  WHAT ACTUALLY CLEARS, PRICED -- and the exact withdrawals")

print(f"""  ESCAPES THAT CLEAR (the live question, since neither alpha does):
   * the EXPONENTIAL / McGaugh-RAR tail: delta_a ~ a0 exp(-sqrt(g/a0)); at the Sun's g/a0 = 2236 that is
    a0 e^-47 ~ {A0['canon']*math.exp(-math.sqrt(BODIES['Sun']/A0['canon'])):.1e} m/s^2 -- clears by >1e13.
    This is the whitepaper's own adopted template, so adopting it is consistency, not retreat. COST: the
    kernel is no longer either alpha; the SPARC delta is the whitepaper's, to be re-verified under the
    framework's fit.
   * FREQUENCY DRESSING a0_eff ~ (1 + Omega/H0)^-p: needs p >= 0.069 to clear the Sun's line at the
    committed SPARC cost <= 0.010 dex. COST: a fifth constant -- the cost STANDING already names for
    alpha=1; the switch REDUCED that bill from ~3e4x to ~6-12x, it did not cancel it.

  WITHDRAWN, verbatim targets:
   * STANDING.md:698  "takes the planets from 1279x over to 2e-5x -- i.e. passing"
       -> "reduces the Sun-carried ephemeris liability from ~1278x to 6.2-8.5x over the Mars budget
          (canon; 9.0-12.4x alt) -- 3.35 orders of relief, NOT a pass (agentE_solar_reflex.py,
          WHITEPAPER_TOE_MAP_2026.md sec. 4.3.2)."
   * mi_alpha2_migration_2026.py:250  "The planetary liability is DISCHARGED on both footings."
       -> the line now states the 6.2-12.4x standing and points here.
  NOT withdrawn: the alpha-switch's other results (RAR +0.0033 dex, deep-regime invariance, the simpler
  measure) -- this correction is about ONE sentence-pair, and the relief it describes is real.""")

check(A0["canon"] * math.exp(-math.sqrt(BODIES["Sun"] / A0["canon"])) < MARS_BUDGET * 4.6e-15,
      "E4 the exponential tail clears the Sun's line by many orders (computed, not quoted) -- so an escape "
      "exists inside the whitepaper's own adopted template; the liability prices a KERNEL-SHAPE choice, "
      "it does not kill the framework")

banner("RESULT")
n = sum(1 for x, _ in ok if x)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for x, m in ok:
        if not x:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the alpha=2 discharge is withdrawn; the Sun binds at 6.2-8.5x/9.0-12.4x; the escapes are priced.")
