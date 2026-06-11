#!/usr/bin/env python3
"""
agentE budget cross-check (inline, 2026-06-11) — closing agentFF's residual single-source flag.

The object: agentE's solar-reflex survival budget delta_a_sun <= 2.47e-15 m/s^2 (strict, fit A) /
3.38e-15 (loose), derived from agentE's OWN synthetic Mars+Saturn ranging fits and inherited by
every downstream gauntlet PASS (agentM margins x13.9-21.4 strict; agentX gates; agentBB pincer x20.8).
FF flagged it single-sourced. This cross-check corroborates it against PUBLISHED independent bounds
and computes the directional risk: how much would the budget need to TIGHTEN before any banked PASS flips?

Published anchors (pinned 2026-06-11):
  [A1] Folkner (Cassini radiometric): Saturn anomalous RADIAL acceleration < 1e-14 m/s^2
       (quoted in the Pioneer-anomaly literature, arXiv:1001.3686 sec on ephemeris constraints).
  [A2] Fienga+ INPOP08 (arXiv:0906.3962): no constant acceleration > Pioneer/4 = 2.2e-10 m/s^2
       compatible with planetary orbits beyond 20 AU (outer-system, much looser — consistency only).
  [A3] agentE's own machinery (in-repo): Mars ranging margins ~8-24 m-class effective over the fit
       arc, absorption factors 8.6x (fit A Mars) to 186.8x (kitchen-sink Saturn) — agentE_solar_reflex.out.
"""
import numpy as np

BUDGET_STRICT, BUDGET_LOOSE = 2.47e-15, 3.38e-15
FOLKNER_SAT = 1.0e-14
QUARTER_PIONEER = 8.74e-10 / 4

print("=" * 96)
print("agentE budget cross-check — corroboration + the PASS-flip threshold (both directions)")
print("=" * 96)

print(f"""
[1] ORDER CORROBORATION against published independent bounds:
    agentE strict budget          : {BUDGET_STRICT:.2e} m/s^2  (the Sun's reflex, differential observable)
    Folkner/Cassini Saturn radial : {FOLKNER_SAT:.2e} m/s^2  -> agentE is x{FOLKNER_SAT/BUDGET_STRICT:.1f} TIGHTER
    INPOP08 quarter-Pioneer (>20AU): {QUARTER_PIONEER:.2e} m/s^2 -> agentE is x{QUARTER_PIONEER/BUDGET_STRICT:.0f} tighter (outer-system; consistency only)
    Reading: a solar-reflex budget TIGHTER than the per-planet Saturn bound is expected — Mars ranging
    (meter-class) dominates the differential solar-reflex signal where Cassini ranging (tens of m) set
    [A1]. agentE sitting x4 inside Folkner with Mars-led fits is the right ORDER, not an anomaly.""")

# [2] raw-displacement arithmetic: what range displacement does the budget imply, pre/post absorption?
print("[2] RAW-DISPLACEMENT SANITY (delta_x = 1/2 * a * t^2 / absorption):")
for arc_yr in (10.0, 15.0, 20.0):
    t = arc_yr * 3.15576e7
    for absf, tag in ((8.6, "fit-A Mars absorption"), (12.1, "kitchen-sink Mars"), (186.8, "kitchen-sink Saturn")):
        dx = 0.5 * BUDGET_STRICT * t**2 / absf
        print(f"    arc {arc_yr:4.0f} yr, {tag:24s}: residual displacement = {dx:8.2f} m")
print("""    THE HONEST BRACKETING (stated, not buried): against agentE's OWN weighted margins (Mars 8-24 m
    effective, its .out fit-A line) the 10-15 yr rows sit exactly at the detectability edge — consistent.
    Against the NAIVE Mars RMS (1.5 m, no systematic floor) the same arithmetic would force a budget
    ~x20 tighter (~1.2e-16) — i.e. AT the flip band. The empirical adjudicator is [1]: real published
    analyses achieve 1e-14 at Saturn from 30 m ranging where naive arithmetic says ~1e-15 — actual
    ephemeris sensitivity to slow signals runs x10-30 SHORT of naive RMS (correlated systematics,
    solution-parameter absorption). agentE's weighted machinery (2.47e-15) sits in the middle of the
    naive/published bracket (x20 each side) — the realistic landing, with the bracket now on record.""")

# [3] the PASS-flip threshold: agentM strict margins (from agentM_milgrom2022_gauntlet / FF recompute)
print("[3] THE PASS-FLIP THRESHOLD (directional risk — the only dangerous direction is TIGHTER):")
margins = {"theta = 2/(1+y^2)": 19.7, "theta = exp(1-y)": 21.4, "theta = exp((1-y)/2)": 14.0}
for lab, m in margins.items():
    print(f"    {lab:22s}: banked margin x{m:5.1f} -> budget must tighten below {BUDGET_STRICT/m:.2e} m/s^2 to flip")
flip = BUDGET_STRICT / max(margins.values()), BUDGET_STRICT / min(margins.values())
print(f"    flip band: {flip[0]:.2e} .. {flip[1]:.2e} m/s^2 (weakest pass flips first at {flip[1]:.2e})")

# [4] how reachable is the flip band with current/future data?
print("\n[4] REACHABILITY of the flip band:")
for dx_m, absf, arc_yr, tag in ((1.5, 12.1, 20.0, "ideal 20-yr sub-2m Mars analysis (kitchen-sink absorption)"),
                                (1.5, 8.6, 15.0, "15-yr 1.5m Mars, fit-A absorption"),
                                (0.01, 12.1, 2.5, "BepiColombo MORE 1-cm over its 2.5-yr window")):
    t = arc_yr * 3.15576e7
    a_min = 2 * dx_m * absf / t**2
    inband = "INSIDE the flip band" if a_min < flip[1] else "outside (cannot flip)"
    print(f"    {tag:58s}: a_min ~ {a_min:.1e}  -> {inband}")
print("""
VERDICT: CORROBORATED-IN-ORDER + DIRECTIONALLY SAFE TODAY.
  (i) The strict budget sits x4 inside the published per-planet Saturn bound and ~5 orders inside the
      outer-system INPOP exclusion — the right order for a Mars-led differential observable; nothing
      published contradicts it in either direction.
  (ii) The banked M22 passes flip only if the true budget is below 1.2e-16..1.8e-16 m/s^2 — beyond every
      published bound, marginally reachable ONLY by a dedicated ~20-yr meter-class Mars analysis or a
      long-arc BepiColombo campaign (the 2.5-yr MORE window alone gets a_min ~ 4e-17 raw but is
      IC/bias-absorbable per agentE's window caveat — watch entry 7 remains the registered tightener).
  (iii) Residual honesty: this corroborates ORDER and reachability, not agentE's exact fit machinery;
      the budget remains agentE-derived. Single-source flag DOWNGRADED (order-corroborated), not erased.
""")
