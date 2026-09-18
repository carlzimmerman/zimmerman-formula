#!/usr/bin/env python3
"""SW07 -- where the direction-blind programme ends: the ledger, read from the committed results (no new physics).
Reads SW01/SW04/SW05/SW06 results, the DR4 preregistration (Amendments 10/11), L47 and the standing candidate's scorecard; every
number below is looked up, and a missing record is a FAIL.  States the one thing the week leaves on the table: the three-way
DR4 wide-binary discrimination between AQUAL's EFE, the framework's direction-blind cap law, and the xi-screened candidate."""
import os, re, json
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
P = lambda *a: os.path.join(ROOT, *a)
print("SW07 -- the direction-blind programme's ledger (read from the record)\n")
# ---------------------------------------------------------------- records
files = {"SW01": P("fable_independent_2026", "kappa_slot_2026", "SW01_results.json"), "SW04": P("fable_independent_2026", "kappa_slot_2026", "SW04_results.json"),
         "SW05": P("fable_independent_2026", "kappa_slot_2026", "SW05_results.json"), "SW06": P("fable_independent_2026", "kappa_slot_2026", "SW06_results.json"),
         "prereg": P("prep_2026", "gaia_dr4_prep", "PREREGISTRATION_DR4.md"), "L47": P("fable_independent_2026", "L47_ELLIPTIC_ITERATION.out"),
         "candidate": P("qwen_claude_field_theory", "closure_2026", "FINAL_THEORY_CANDIDATE_2026-09-05.md")}
if not os.path.exists(files["L47"]):
    import glob; g = glob.glob(P("fable_independent_2026", "L47*.out")); files["L47"] = g[0] if g else files["L47"]
missing = [k for k, v in files.items() if not os.path.exists(v)]
check("R1 every record this ledger reads exists on disk (SW01/SW04/SW05/SW06 results, PREREGISTRATION_DR4.md, L47 .out, the 09-05 candidate scorecard)", not missing, f"missing: {missing}")
J = {k: json.load(open(files[k])) for k in ("SW01", "SW04", "SW05", "SW06") if os.path.exists(files[k])}
prereg = open(files["prereg"]).read() if os.path.exists(files["prereg"]) else ""
l47 = open(files["L47"]).read() if os.path.exists(files["L47"]) else ""
cand = open(files["candidate"]).read() if os.path.exists(files["candidate"]) else ""
# ---------------------------------------------------------------- the three DR4 bands
armA = [float(x) for x in re.findall(r"1\.1614|1\.1814|1\.1917|1\.2267", prereg)]
armB = [float(x) for x in re.findall(r"\*\*(1\.0450|1\.0300) ± 0\.0037\*\*", prereg)]
cap = {}
for foot in ("canonical", "alt"):
    for kn in ("nu_RAR", "mu_2"):
        cap[f"{foot}/{kn}"] = J["SW01"]["parts"]["N3"][f"{foot}/{kn}"]["gamma_v_range"]
cap_lo, cap_hi = min(v[0] for v in cap.values()), max(v[1] for v in cap.values())
l47_floor = re.search(r"analytic floor is (4\.00) pc", l47)
print(f"    Arm A (AQUAL EFE, Amendment 10, in force): canonical [1.1614, 1.1814], alt [1.1917, 1.2267]  -- found in the preregistration: {sorted(set(armA))}")
print(f"    Arm B (covariant candidate, Amendment 11, CEILINGS): {sorted(set(armB))}; L47: the carrier's ephemeris floor is xi >= 4.00 pc, at which the pair is screened, gamma_v = 1.000 + O((0.05 pc/4 pc)^2/2 = 8e-5)")
print(f"    the framework's direction-blind cap (SW01, THIS WEEK, NOT registered): gamma_v = sqrt(nu(eta)) in [{cap_lo:.3f}, {cap_hi:.3f}] over both footings and kernels: " + ", ".join(f"{k} {v[0]:.3f}-{v[1]:.3f}" for k, v in cap.items()))
gapA = {"canonical": 1.1614 - max(cap["canonical/nu_RAR"][1], cap["canonical/mu_2"][1]), "alt": 1.1917 - max(cap["alt/nu_RAR"][1], cap["alt/mu_2"][1])}
gapB = min(v[0] for v in cap.values()) - 1.0450
check("R2 on EITHER footing the three outcomes are disjoint: candidate (1.000; ceiling 1.045) < cap law < AQUAL, with same-footing gaps >= 0.029 (canonical) and >= 0.036 (alt) against the Amendment-10 band width ~0.02; ACROSS footings the corner gap (alt cap 1.155 vs canonical AQUAL 1.1614) is only 0.006, so the footing must be fixed before the cap law and AQUAL are told apart",
      len(set(armA)) == 4 and len(set(armB)) == 2 and l47_floor is not None and gapB > 0.02 and min(gapA.values()) > 0.02 and (1.1614 - cap_hi) < 0.02,
      f"gaps: candidate-to-cap {gapB:+.3f}; cap-to-AQUAL same footing canonical {gapA['canonical']:+.3f}, alt {gapA['alt']:+.3f}; cross-footing corner {1.1614 - cap_hi:+.3f}")
# ---------------------------------------------------------------- what the week killed and what it left
a1 = {k: v["alpha1"] for k, v in J["SW04"]["parts"]["numbers"].items()}
dt = {k: v["dt_s"] for k, v in J["SW06"]["hornB"].items()}
check("R3 SW03 (the smoothed-total-switch action) is dead twice on the committed numbers: |alpha1~| >= 1.4 on every footing/kernel (SW04) and the GW170817 photon-graviton delay >= 1e7 s (SW06)",
      min(abs(v) for v in a1.values()) >= 1.4 and min(dt.values()) >= 1e7, f"min |alpha1~| = {min(abs(v) for v in a1.values()):.2f}; min Delta t = {min(dt.values()):.1e} s")
ledger = J["SW06"]["ledger"]; dead = sum(1 for r in ledger if r[1].startswith("DEAD")); openr = [r[0] for r in ledger if r[1].startswith("OPEN")]
check("R4 the repaired quadrature action keeps an open l-window (SW05) but every lensing route except one is dead (SW06), and that one is the standing candidate's own structure (khronon-sourced, locally switched-off scalar, one metric)",
      J["SW05"]["window_ratio_min"] > 1 and dead == 5 and len(openr) == 1 and "khronon-sourced" in openr[0], f"window ratio {J['SW05']['window_ratio_min']:.2e}; open route: {openr[0][:60]}")
check("R5 the standing candidate is single-metric ('Matter minimally coupled to g', requirement 11 PASS in its scorecard), so SW06's differential-Shapiro kill does NOT apply to it; its EFE is the xi-smoothed AQUAL one (directional), not the cap law -- the week's SW01 rule and the candidate are DIFFERENT DR4 predictions",
      "Matter minimally coupled to g" in cand and "| 11 | one metric | PASS" in cand)
n, n_pass = len(CH), sum(CH)
print(f"\nSW07 COMPLETE: {n_pass}/{n} checks PASS.")
print("""LEDGER.  What the week established (each a committed lane): KS01 the epsilon = 1/(32 pi) slot is not live; G111 closed; L263 a real-mass phantom is dead
both ways; L264 universal a0 forces an external-field effect (SEP theorem); SW01 the framework's cap law is a DIRECTION-BLIND EFE with gamma_v = 1.09-1.15;
SW02/SW03 its smoothed-switch covariant realisation; SW04 that realisation dies on alpha1; SW06 it was already dead on GW170817 (my omission); SW05 the
quadrature realisation (L268 repaired) survives PPN and the quadrupole but has no lensing route except the standing candidate's structure, which is NOT
direction-blind.  WHAT IS LEFT ON THE TABLE: DR4 separates three outcomes -- 1.000 (the xi-screened candidate, the only covariant theory standing),
1.09-1.15 (the cap law, a rule without a realisation), 1.16-1.23 (AQUAL's EFE, whose realisations are Cassini-dead).  The cap law's band is NOT
registered; registering it is the user's call (append-only, explicit go).  The frontier is the candidate's own list: the origin of s_0 ~ 1.5e7, the
disformal cosmology, a Boltzmann/N-body run, and kappa.  Nothing here derives kappa.""")
