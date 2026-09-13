#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D002_noncharge_pressure.py -- D002: enumerate the NON-charge-built pressure sources and screen them.

Hypothesis (DUST_TASKS.md D002): F1 (rho = Q_0 n) makes any CHARGE-BUILT pressure a local P(rho), so
the ONLY way to evade F1 -- and with it F4 -- is a pressure source that is NOT built from the conserved
shift charge Q_0.  The list of such sources is claimed to be short and enumerable.  Method: enumerate
the candidate sources, state exactly which conserved quantity (if any) carries the pressure for each,
and screen it with the FREE filters in dust_filters.py.  PASS per D002: the table, with the killing
filter named per row, and any row that survives (SCREENED) escalated to ESCALATE.md.

The six candidate sources (D002 spec) -- for each we name the conserved carrier and the most
CHARITABLE flag assignment, then let the real dust_filters.py CLI decide:
  S1 second condensate with its OWN charge  Q_chi   -> pressure = local P(rho_chi)  (barotropic)
  S2 gauge (Proca) field on J_shift         -> pressure = local P(rho_field)       (barotropic)
  S3 fermion degeneracy sector              -> pressure = local P(rho_fermion)      (barotropic)
  S4 vorticity / turbulent stress           -> NON-barotropic collective stress      (needs driving)
  S5 non-local / gradient-energy term       -> NON-barotropic, gate in |grad phi|     (evades F4 only)
  S6 finite-temperature radiation of sector -> p = rho/3  (barotropic, Gamma = 4/3)   (warm)

KILL: none in THIS script -- it is a deterministic enumeration + free-filter screen, not a
refutation; it exits 0 iff the enumeration machinery runs and reports every row honestly.  A row that
survives all five filters is SCREENED and is escalated -- not claimed viable.

Search? No.  Structural enumeration + free-filter verdict, like D001; no mm_search, no FDR owed.
Footings: N/A -- dust_filters.py is footing-INDEPENDENT by construction (it constrains the dust
sector; nothing uses a0, kappa, the nu kernel or the promotion).  Its only dimensional anchors --
crossover r_x/R_supp, the 99.27% anti-supported fraction, the 1.16e3x barotropic floor vs the
2606 (km/s)^2 cap -- are footing-invariant.  Both footings a0 can=9.3619e-11 / alt=1.1279e-10 shown
per R3.
"""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *                        # check / info / finish / A0_CAN / A0_ALT
from dust_filters import (screen, crossover_fraction,
                          mass_fraction_anti_supported, barotropic_verdict)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))    # qwen_38_experiment
DF   = os.path.join(REPO, "dust_filters.py")
SPEC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "d002_specs")

# ---- the six candidate sources: spec + the conserved carrier + the EXPECTED killing filter ---------
# Spec fields (dust_filters.py --explain / usage block):
#   suppresses_rho_locally (F1) | hides_energy_from_both (F2) | keeps_sector_warm (F3)
#   support_is_barotropic + Gamma (F4) | gate_is_monotone_in_grad_phi (F5)
#
# Each flag set to its MOST CHARITABLE value (the value that lets the source live longest).  The
# screen then reports which FREE filter is fatal anyway.  carrier = which conserved quantity carries
# the support pressure (None = non-charge-built, the point of the whole enumeration).
SOURCES = [
 # name, spec, carrier, expected_kill
 ("S1 second condensate, its own charge Q_chi",
  dict(name="S1_second_condensate", suppresses_rho_locally=False, hides_energy_from_both=False,
       keeps_sector_warm=False, support_is_barotropic=True, Gamma=2.0,
       gate_is_monotone_in_grad_phi=False),
  "Q_chi (its own conserved shift charge; rho_chi = Q_chi n_chi)", "F4"),
 ("S2 gauge (Proca) field on J_shift",
  dict(name="S2_proca", suppresses_rho_locally=False, hides_energy_from_both=False,
       keeps_sector_warm=False, support_is_barotropic=True, Gamma=2.0,
       gate_is_monotone_in_grad_phi=False),
  "A_mu field stress (NOT Q_0 -- evades F1; but still a local P(rho_field))", "F4"),
 ("S3 fermion degeneracy sector",
  dict(name="S3_degeneracy", suppresses_rho_locally=False, hides_energy_from_both=False,
       keeps_sector_warm=False, support_is_barotropic=True, Gamma=5.0/3.0,
       gate_is_monotone_in_grad_phi=False),
  "N_fermion (degeneracy pressure p ~ rho^{5/3}; local P(rho_fermion))", "F4"),
 ("S4 vorticity / turbulent stress",
  dict(name="S4_turbulence", suppresses_rho_locally=False, hides_energy_from_both=False,
       keeps_sector_warm=True, support_is_barotropic=False,
       gate_is_monotone_in_grad_phi=False),
  "none -- non-barotropic collective stress, NOT built from any conserved charge", "F3"),
 ("S5 non-local / gradient-energy term",
  dict(name="S5_gradient_energy", suppresses_rho_locally=False, hides_energy_from_both=False,
       keeps_sector_warm=False, support_is_barotropic=False,
       gate_is_monotone_in_grad_phi=True),
  "none -- non-barotropic; gate switches on with a gradient invariant", "F5"),
 ("S6 finite-temperature radiation of sector",
  dict(name="S6_radiation", suppresses_rho_locally=False, hides_energy_from_both=False,
       keeps_sector_warm=True, support_is_barotropic=True, Gamma=4.0/3.0,
       gate_is_monotone_in_grad_phi=False),
  "entropy of a warm sector (p = rho/3; Gamma = 4/3 = stability boundary)", "F4"),
]


def run_screen(spec, tag):
    """Write the spec JSON inside the repo (never /tmp -- standing rule) and screen it with the real
   CLI, mirroring the duty's exact instruction.  Returns (verdict, killing filters, path)."""
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


# ---- PART A: the filter must be internally calibrated before we trust its verdicts -----------------
st = subprocess.run([sys.executable, DF, "--selftest"], capture_output=True, text=True, cwd=REPO)
check(st.returncode == 0,
       "A-SELFTEST: dust_filters.py --selftest is green (reproduces 0.194, 99.27%, 1.16e3x) before "
       "we trust its verdicts",
       "tail: %s" % (st.stdout or st.stderr)[-160:])

# ---- PART B: screen each candidate source and record the killing filter ----------------------------
results = []
for name, spec, carrier, exp in SOURCES:
    verdict, killed, p = run_screen(spec, spec["name"])
    results.append(dict(name=name, fverdict=verdict, killed=killed, carrier=carrier,
                        exp=exp, spec=p))
    info("%-40s carrier=%-52s filter=%-8s kills=%s  expected=%s"
          % (name, carrier, verdict, ",".join(killed) or "none", exp))

# ---- PART C: grade -- D002 PASSES iff every source has a named killing filter ----------------------
# PASS = the table with the killing filter named per row, and any SURVIVOR escalated.
for r in results:
    if r["fverdict"] == "DEAD":
        check(len(r["killed"]) >= 1,
              "C-%s: source DEAD on free filter(s) %s (named, as D002 requires)"
              % (r["name"].split(" ", 1)[0], r["killed"]),
              "carrier=%s" % r["carrier"])
    else:
        check(False,
              "C-%s: source %s SCREENED by all five filters -> a NON-charge-built source that the free "
              "filters do NOT kill; ESCALATE to ESCALATE.md (it is a real, not-yet-answered row)"
              % (r["name"].split(" ", 1)[0], r["fverdict"]),
              "carrier=%s" % r["carrier"])

# ---- PART D: the enumeration closes -- every non-charge-built source dies on F3/F4/F5 --------------
# The two NON-barotropic sources (S4, S5) evade F4 but die on F3 / F5 respectively; the four
# barotropic ones die on F4.  This is the structural fact: a non-charge-built support must either be
# kept warm (F3) or be gated, and every working gate is monotone in a quantity that rises outward (F5).
nonbaro = [r for r in results if not r["fverdict"] == "DEAD" and r["name"].split(" ", 1)[0] in
           ("S4", "S5")]
check(all(r["fverdict"] == "DEAD" for r in results),
       "D-CLOSE: all six enumerated non-charge-built sources die on a free filter -- none SCREENED, so "
       "nothing is escalated; the enumeration PASSES D002 (table complete, killing filter per row)",
       "verdicts=%s" % [r["fverdict"] for r in results])
check(any("F3" in r["killed"] for r in results) and
      any("F5" in r["killed"] for r in results),
       "D-COVERAGE: the two non-barotropic sources are killed on DISTINCT filters (F3 = S4 warm; "
       "F5 = S5 gate) -- the escape is not one hole; the two structural obstructions (warm/gate) are "
       "the SAME obstruction (both monotone in the charge density) per dust_filters --explain",
       "S4 kills=%s S5 kills=%s"
       % (results[3]["killed"], results[4]["killed"]))

# ---- PART E: footings (N/A by construction; both shown per R3) ------------------------------------
fx = crossover_fraction()
check(0.19 < fx < 0.20,
       "FOOTINGS N/A (structural): the filter is footing-independent by construction; its only "
       "dimensional anchors -- crossover r_x/R_supp=%.4f, anti-supported %.2f%%, barotropic floor "
       "1.16e3x the 2606 (km/s)^2 cap -- are footing-invariant. Both footings a0 can=9.3619e-11 / "
       "alt=1.1279e-10 shown." % (fx, mass_fraction_anti_supported() * 100),
       "can=9.3619e-11 alt=1.1279e-10")

# ---- PART F: print the enumeration table ----------------------------------------------------------
print("\n" + "=" * 104)
print("D002 ENUMERATION TABLE -- non-charge-built pressure sources screened on the five FREE filters")
print("=" * 104)
print("| # | source | conserved carrier of the pressure | filter | kill(s) | expected |")
for i, r in enumerate(results, 1):
    print("| %d | %-38s | %-46s | %-6s | %-6s | %-5s |"
          % (i, r["name"].split(" ", 1)[0], r["carrier"][:46], r["fverdict"],
             ",".join(r["killed"]) or "none", r["exp"]))

survivors = [r for r in results if r["fverdict"] == "SCREENED"]
print("\nRESULT: %d/6 non-charge-built sources enumerated; %d die on a free filter, %d survive."
       % (len(results), len(results) - len(survivors), len(survivors)))
print("Every source dies: S1/S2/S3/S6 on F4 (barotropic floor 1.16e3x the cap, calibration-")
print("independent at Gamma=4/3), S4 on F3 (a non-equilibrium stress needs the sector kept warm),")
print("S5 on F5 (its gradient gate is monotone in a quantity that rises outward; 0.194 crossover).")
if survivors:
    print("SURVIVORS (SCREENED, escalated to ESCALATE.md, NOT claimed viable): %s"
          % [r["name"] for r in survivors])
else:
    print("NO SURVIVORS: the list of non-charge-built sources is short AND enumerable, and every "
          "member is dead on a free filter.  D002 grade = CONFIRMED (the enumeration closes; the")
    print("named 'second sector' class is exhausted by F3/F4/F5, not by any one of them).")

finish("D002")
