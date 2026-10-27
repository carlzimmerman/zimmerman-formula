#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D001_filter_calibration.py -- D001: calibrate dust_filters.py against the four known corpses.

Hypothesis (DUST_TASKS.md D001): dust_filters.py reproduces the committed verdicts for all four
candidates catalogued in real_research/reviews/second_field_catalog_2026.py PART G (lines 796-816):
  C1 second shift-symmetric k-essence K_chi(X_chi)          -> DEAD, leg L1+L3 (L2 does NOT kill)
  C2 ungated Proca on J_shift (contact + long-range limits) -> DEAD, leg L1 (both limits)
  C3 field only in the promotion a_0^2(Q,chi)              -> DEAD, leg "none -- the promotion's
                                                            own order counting" (E1/E2 no-free-lunch)
  C4 Proca gated on a fixed bare-Lambda scale              -> CONDITIONAL-DEAD, passes L1/L2/L3/CMB,
                                                            dies on F5 (radial support-sign, fourth leg)

Method: for each corpse write the spec JSON (fields per dust_filters.py) and screen it with the
real CLI (python dust_filters.py --screen <spec>); exit 0 = SCREENED, exit 2 = DEAD, and the
[KILL] lines name the filter(s) that fired. Compare the filter's verdict + killing filter(s) with
the review's verdict + killing leg.  PASS per D001: 4/4 agreement, OR a NAMED disagreement.

KILL: none in this script -- it is a deterministic comparison, not a refutation.  The script exits
0 if the comparison machinery runs and reports its findings honestly.

Search? No.  This is a structural verdict comparison, not a numerological match; no mm_search, no
FDR pre-registration owed.  Footings: N/A -- dust_filters.py is footing-independent BY CONSTRUCTION
(the filters constrain the dust sector; nothing uses a0, kappa, the nu kernel or the promotion).  The
only dimensional anchors the filter reports (crossover r_x/R_supp, the 1.16e3x barotropic floor) are
footing-invariant; both footings shown per R3.
"""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *                       # check / info / finish / A0_CAN / A0_ALT
from dust_filters import (screen, crossover_fraction,
                          mass_fraction_anti_supported, barotropic_verdict)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # qwen_38_experiment
DF   = os.path.join(REPO, "dust_filters.py")
SPEC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "d001_specs")

# ---- the four corpses: spec + the review's COMMITTED verdict and killing leg ----------------------
# Spec fields (dust_filters.py --explain / usage block):
#   suppresses_rho_locally (F1) | hides_energy_from_both (F2) | keeps_sector_warm (F3)
#   support_is_barotropic + Gamma (F4) | gate_is_monotone_in_grad_phi (F5)
CORPSES = [
    ("C1 second shift-symmetric k-essence K_chi(X_chi)",
     dict(name="C1_kessence", suppresses_rho_locally=False, hides_energy_from_both=False,
          keeps_sector_warm=False, support_is_barotropic=True, Gamma=2.0,
          gate_is_monotone_in_grad_phi=False),
     "DEAD", "L1 + L3 (applied to chi); L2 does NOT kill"),
    ("C2 ungated Proca on J_shift (contact + long-range)",
     dict(name="C2_ungated_proca", suppresses_rho_locally=False, hides_energy_from_both=False,
          keeps_sector_warm=False, support_is_barotropic=True, Gamma=2.0,
          gate_is_monotone_in_grad_phi=False),
     "DEAD", "L1 (rho=Q0n -> P=P(rho), stiffest at rec; both limits)"),
    ("C3 field only in the promotion a0^2(Q,chi)",
     dict(name="C3_promotion_only", suppresses_rho_locally=False, hides_energy_from_both=False,
          keeps_sector_warm=False, support_is_barotropic=False,
          gate_is_monotone_in_grad_phi=False),
     "DEAD", "no leg -- the promotion's own order counting (E1/E2 no-free-lunch)"),
    ("C4 Proca gated on a fixed bare-Lambda scale",
     dict(name="C4_fixedlambda_gated", suppresses_rho_locally=False,
          hides_energy_from_both=False, keeps_sector_warm=False,
          support_is_barotropic=True, Gamma=2.0, gate_is_monotone_in_grad_phi=True),
     "CONDITIONAL-DEAD", "passes L1/L2/L3/CMB; dies on F5 (radial support-sign, fourth leg)"),
]


def run_screen(spec, tag):
    """Write the spec JSON inside the repo (never /tmp -- standing rule: write only in this dir)
    and screen it with the real CLI, mirroring the duty's exact instruction."""
    os.makedirs(SPEC_DIR, exist_ok=True)
    p = os.path.join(SPEC_DIR, tag + ".json")
    with open(p, "w") as f:
        json.dump(spec, f, indent=2)
    r = subprocess.run([sys.executable, DF, "--screen", p],
                       capture_output=True, text=True, cwd=REPO)
    killed = []
    for ln in (r.stdout or "").splitlines():
        if "[KILL]" in ln:
            killed.append(ln.split()[1])
    verdict = "SCREENED" if r.returncode == 0 else "DEAD"
    return verdict, killed, p


# ---- PART A: the filter must be internally calibrated before we trust its verdicts ----------------
st = subprocess.run([sys.executable, DF, "--selftest"], capture_output=True, text=True, cwd=REPO)
check(st.returncode == 0,
      "A-SELFTEST: dust_filters.py --selftest is green (the filter reproduces its own committed "
      "numbers before we trust its verdicts)",
      "tail: %s" % (st.stdout or st.stderr)[-160:])

# ---- PART B: screen each corpse and record filter verdict + killing filter(s) ---------------------
results = []
for name, spec, rv, leg in CORPSES:
    verdict, killed, p = run_screen(spec, spec["name"])
    results.append(dict(name=name, fverdict=verdict, killed=killed,
                        rv=rv, leg=leg, spec=p,
                        rv_dead="DEAD" in rv))
    info("%-42s filter=%-8s kills=%-8s  review=%-15s leg=%s"
         % (name, verdict, ",".join(killed) or "none", rv, leg))

# ---- PART C: compare verdicts and legs, grade the disagreements ----------------------------------
# C1, C2: the filter must reproduce DEAD.
for i in (0, 1):
    r = results[i]
    check(r["fverdict"] == "DEAD" and r["rv_dead"],
          "C%d REPRODUCED: filter verdict %s == review %s"
          % (i + 1, r["fverdict"], r["rv"]),
          "filter kills %s; review leg: %s" % (r["killed"], r["leg"]))

# C3: the coverage gap on the VERDICT -- the filter SCREENS it clean, the review kills it.
c3 = results[2]
check(c3["fverdict"] == "SCREENED" and c3["rv_dead"],
      "C3 NAMED-DISAGREEMENT (verdict): filter SCREENS the promotion-only field clean, review "
      "kills it DEAD on the promotion's own order counting (E1/E2 no-free-lunch)",
      "coverage gap: none of the five FREE filters is a no-free-lunch / parameter-free-shortfall "
      "filter; SCREENED = 'earns a session', NOT 'viable' -- the filter never claims it alive")

# C4: verdict agrees (both dead) but the killing LEG differs -- the filter over-fires F4.
c4 = results[3]
check(c4["fverdict"] == "DEAD" and c4["rv_dead"],
      "C4 VERDICT AGREES: filter DEAD == review CONDITIONAL-DEAD (both dead)",
      "filter kills %s" % c4["killed"])
check(set(c4["killed"]) == {"F4", "F5"},
      "C4 NAMED-DISAGREEMENT (leg): filter fires BOTH F4 and F5, but the review tames F4 (the "
      "fixed-Lambda gate removes the rho_rec/rho_supp barotropic amplification) and kills on F5",
      "coverage gap: F4 has NO gate dimension -- it evaluates the UNGATED barotropic violation, so "
      "it over-fires for a gated candidate; the taming is an F5/derivation, not a free filter")

# ---- PART D: the filter is SOUND (no false-alive) even where it is INCOMPLETE ---------------------
screened = [r for r in results if r["fverdict"] == "SCREENED"]
check(len(screened) == 1 and screened[0]["name"].startswith("C3"),
      "SOUND (no false-alive): the only corpse the filter screens clean is C3, the no-free-lunch / "
      "promotion-order-counting case, where SCREENED is the HONEST output (not a claimed viability)",
      "screened=%s" % [r["name"].split(" ", 1)[0] for r in screened])
# leg-compat note: C1/C2 filter-kill F4 is the barotropic FACE of the review's L1 (charge-built
# pressure is a local P(rho)); so their verdict+leg are compatible even though the label differs.
c1c2_leg_ok = all("F4" in results[i]["killed"] for i in (0, 1))
check(c1c2_leg_ok,
      "C1/C2 LEG COMPATIBLE: filter kill F4 (barotropic P(rho)) is the barotropic manifestation of "
      "the review's L1 (rho=Q0n forces a charge-built, hence local, pressure)",
      "C1 kills=%s C2 kills=%s" % (results[0]["killed"], results[1]["killed"]))

# ---- PART E: footings (N/A by construction; both shown per R3) -----------------------------------
fx = crossover_fraction()
check(0.19 < fx < 0.20,
      "FOOTINGS N/A (structural): the filter is footing-independent by construction; its only "
      "dimensional anchors -- crossover r_x/R_supp=%.4f, anti-supported %.2f%%, barotropic floor "
      "1.16e3x the 2606 (km/s)^2 cap -- are footing-invariant. Both footings a0 can=9.3619e-11 / "
      "alt=1.1279e-10 shown." % (fx, mass_fraction_anti_supported() * 100),
      "can=9.3619e-11 alt=1.1279e-10")

# ---- PART F: tally the agreement and print the comparison table ---------------------------------
n_verdict_agree = sum(1 for r in results if (r["fverdict"] == "SCREENED") == (not r["rv_dead"]))
n_verdict_gap = sum(1 for r in results if r["fverdict"] == "SCREENED" and r["rv_dead"])
n_leg_gap = 1 if set(c4["killed"]) == {"F4", "F5"} else 0   # C4 over-fires F4
info("TALLY: verdict agreement %d/4 (C1,C2,C4 all dead); named disagreements = %d verdict gap (C3) "
     "+ %d leg gap (C4)" % (n_verdict_agree, n_verdict_gap, n_leg_gap))

print("\n" + "=" * 100)
print("D001 COMPARISON TABLE -- dust_filters.py vs second_field_catalog_2026.py PART G")
print("=" * 100)
print("| # | corpse | filter | kill(s) | review | review leg | agreement |")
for i, r in enumerate(results, 1):
    if r["fverdict"] == "SCREENED" and r["rv_dead"]:
        agr = "DISAGREE(verdict): SCREENED vs DEAD -- no-free-lunch coverage gap"
    elif r["name"].startswith("C4"):
        agr = "AGREE(verdict dead); LEG differs F4 vs F5 -- F4 has no gate dimension"
    else:
        agr = "AGREE (F4 = barotropic face of L1)"
    print("| %d | %-38s | %-8s | %-6s | %-14s | %-40s | %s |"
          % (i, r["name"].split(" ", 1)[0], r["fverdict"],
             ",".join(r["killed"]) or "none", r["rv"], r["leg"], agr))
print("\nRESULT: 3/4 verdict agreement (C1,C2,C4 all DEAD); 2 NAMED DISAGREEMENTS -- C3 (verdict: "
      "filter SCREENED vs review DEAD, a no-free-lunch case the five FREE filters do not cover) and "
      "C4 (leg: filter over-fires F4 for a gated candidate because F4 has no gate dimension). Both are "
      "COVERAGE GAPS, not false-alive (the filter never declares a dead corpse viable). D001 grade = "
      "NAMED-DISAGREEMENT -> per D001 this flags 'the filter must be fixed before any other D-task "
      "runs'; ESCALATED: whether to ENHANCE dust_filters.py (add a no-free-lunch filter; give F4 a "
      "gate dimension) vs leave it as a free screen is Carl's call, not the worker's.")

finish("D001")
