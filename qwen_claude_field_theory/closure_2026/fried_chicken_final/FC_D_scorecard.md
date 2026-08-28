# FC_D_scorecard — Architecture D = BIMOND + DBI/khronon + a0-line kernel

Compiled from the committed record this session. Every row is tagged
THEOREM | DERIVATION | COMPUTATION | EXTERNAL | MODEL-ASSUMPTION | OPEN | FAILED.
Scripts re-run this session are marked [re-run exit 0].

Published deposit: **DOI 10.5281/zenodo.22015358** — records CONSTRUCTION-level passes
(R1/R3, ephemeris-gap void), **not certification** (STANDING.md; CLOSURE_LEDGER.md:30).

---

## HEADLINE VERDICT: STRUCTURALLY-DEAD (as a distinctive candidate), but NOT on the
## basis the task stated — that basis is a cross-architecture mis-attribution.

The task briefing attributes to D:
- "DOF FAIL (2T+2S localization ghost, (U,ξ) block det = −b² < 0)"
- "c_T FAIL-FLRW (+3.9×10⁻² ⇒ GW170817)"
- "FLRW FAIL (no dS point)"

**These three results are NOT BIMOND-native. They belong to the DW (Deser–Woodard /
Deffayet–Woodard) NONLOCAL-MOND chassis** audited in `papers_2026/PAPER1_carrier_nogos_and_dw_audit.md`
(**DOI 10.5281/zenodo.22132648**), scripts `sf43…sf53_dw_*`. Sources:
- (U,ξ) block [[a,b],[b,0]], det = −b² < 0, "2T+2S": PAPER1 §4.1, lines 25–26, 112;
  script `sf43_dw_localized_dof_ghost_2026.py` [re-run exit 0, 6/6].
- c_T²−1 ≈ +3.9×10⁻² on FLRW from the double-timelike projection R_uu: PAPER1 §4.5,
  lines 155–161. This is the **DBI-khronon completion's** tensor sector, computed inside the DW audit.

Under the program's own rule ("NEVER transfer a result between architectures without PROVING
the map is exact"), those cannot be booked as D's kills. Two committed facts actively
CONTRADICT the stated dead-basis:

1. **sf44 DEMOTED the localization ghost.** `sf44_dw_physical_phase_space_2026.py`
   [re-run exit 0, 6/6]: under the retarded / fixed-IC prescription the (U,ξ) negative-kinetic
   combination has **0 free Cauchy data ⇒ NOT a physical propagating mode**. sf43's (+,−)
   signature is a property of the unrestricted representation only. So even on the DW chassis
   the "DOF FAIL" is not a clean linear-ghost kill.
2. **The BIMOND-native ledger marks DOF and c_T OPEN, not FAIL.** CLOSURE_LEDGER.md:30 /
   NEGATIVE_RESULTS_CLOSURE.md (`BIMOND_DBI_khronon: NOT FROZEN`): "BD ghost UNCHECKED
   (standing rule: quote neither ghost-free nor ghost-ful); no nonlinear DOF count, no c_T,
   no combined lensing, no PPN, no Boltzmann." 10/16 cells OPEN — "the most open chassis."

So D is **not** killed by a committed BIMOND consistency theorem. It is dead for a different,
committed reason: **its one distinctive feature buys nothing, and it inherits an unresolved
tensor-speed liability with zero offsetting passed gates.** Details below.

---

## THE GENUINE BIMOND-NATIVE ADVERSE RESULT (this IS committed and reproduced)

`route6_bimond_twin_2026.py` [re-run exit 0, **30/30**] — a THEOREM, no free parameters,
kernel-independent:

    F_TM(y) = 1 − ν(y),   and the sum rule  F_baryon(y) + F_TM(y) = 1.

Since ν ≥ 1 everywhere (MOND is an enhancement — what the RAR measures), **F_TM ≤ 0
everywhere**: twin matter is invisible in the Newtonian regime and *repulsive* in the MOND
regime. The two-metric structure — BIMOND's entire reason to be tried, so the cosmological
Ω_dm carrier and the galactic phantom could be different objects — **cannot mimic CDM at any
scale, any epoch, any interpolation.** The double count is genuinely broken, but the CMB needs
F_b = 1 AND F_TM = 1 (sum 2) while BIMOND gives 1: *the route breaks the double count and fails
the CMB by the same equation.* Carl's own a₀(z) law makes it fatal — a₀(rec)/a₀(0)=0.0060 makes
recombination the most-Newtonian epoch (y_rec~10³), where F_TM = −(ν−1) = −4.2×10⁻⁴ (a0-line) /
−1.7×10⁻³⁵ (mu10): the required regime ordering is exactly inverted.

**Consequence:** Ω_dm falls back onto the DBI-khronon dust *in our own sector* — the twin metric
adds nothing. So D collapses, for all cosmological purposes, to the khronon completion — the same
DBI-khronon sector whose FLRW tensor speed is c_T²−1 ≈ +3.9×10⁻² in the DW audit. BIMOND does not
escape that liability; it just doesn't gain anything for paying it.

Failure class: **HOST** (the bimetric interaction structure itself; kernel-independent).

---

## GATE SCORECARD (BIMOND-native basis)

| Gate | Status | Basis | Failure class | Evidence |
|---|---|---|---|---|
| R1 (free function eats local total field) | PASS | construction | NONE | DOI 22015358; STANDING.md "R1/R3 by construction" |
| R3 (no G̃/G_N split) | PASS | construction | NONE | DOI 22015358 |
| Ephemeris / solar-system gap | PARTIAL | construction | NONE | 1-AU anomaly 1e-3458.7 (DOI 22015358); **flagged interpolation-dependent** (STANDING owed #3) — robustness UNVERIFIED |
| DOF / BD ghost (2 gravitational DOF) | OPEN | — | (unresolved) | BD UNCHECKED, standing rule "neither ghost-free nor ghost-ful"; route6 G2 "COULD NOT DETERMINE nonlinear BD ghost for Milgrom's own contraction"; sf12 12/12 shows the only route to a lapse degeneracy (V=N·F(X)+N̂·B(X), X lapse-free) **replaces BIMOND with a Hassan–Rosen host** (D2) — so it doesn't close BIMOND |
| c_T = 1 (GW170817) | OPEN/ADVERSE | COMPUTATION on DW/khronon, transfer UNPROVEN | COUPLING/HOST | c_T²−1 ≈ +3.9×10⁻² computed for the DBI-khronon FLRW projection R_uu in PAPER1 §4.5 (DOI 22132648), "modulo one unverified cancellation." NOT computed for the BIMOND host itself. D shares the khronon sector (route6) but the map is not proven. This is the decisive open item. |
| FLRW / cosmology (dS point, w) | PARTIAL/ADVERSE | THEOREM (route6) + MODEL-ASSUMPTION | HOST | route6 THEOREM: twin sector cannot carry Ω_dm; Ω_dm reverts to DBI-khronon w=0 dust. No committed BIMOND-native "no-dS-point" script exists — the task's "FLRW FAIL (no dS)" is not located in the BIMOND record (it is a DW-chassis property). Booked HONESTLY as: distinctive cosmological mechanism FAILED, background dS UNCOMPUTED for the host. |
| PPN (γ, β, α_i) | OPEN | — | — | not computed (STANDING/ledger) |
| Combined-limit lensing Φ+Ψ | OPEN | — | — | owed item #2, not computed |
| Boltzmann (growth, ISW, lensing potential) | OPEN | — | — | owed item #1, not computed |
| Khronon single-invariant F(A²) 2T+1S no-go (E01) | OPEN/AT-RISK | — | HOST | if the khronon is single-invariant hypersurface-orthogonal it risks PAPER1 Theorem 1 (2T+1S). Not evaluated for D's khronon. |

Passed hard certification gates: **0**. Construction-level passes: R1, R3 (+ ephemeris caveated).

---

## HOST vs KERNEL classification of every adverse item

- **Twin-sector / double-count failure (route6):** HOST. Follows from GR-recovery + MOND
  enhancement alone (F_TM = 1−ν ≤ 0); no kernel, no parameter can rescue it. Verified for both
  the a0-line kernel and mu10.
- **c_T²−1 ≈ +3.9×10⁻² (DW/khronon):** COUPLING/HOST — set by the double-timelike R_uu projection
  of the khronon completion, not by the MOND free function. Kernel-independent in origin.
  Transfer to the BIMOND host is UNPROVEN (so booked OPEN, not FAILED, for D).
- **Localization ghost det=−b² (DW):** CONSTRAINT-ARCHITECTURE, and **not D's** — DW nonlocal
  chassis, and demoted to non-fatal by sf44 under the retarded prescription.

---

## WHY THE OVERALL LABEL IS STRUCTURALLY-DEAD (optimizer verdict, stated honestly)

D is **not** killed by a clean committed BIMOND ghost/DOF/c_T theorem — those cells are OPEN,
and the specific kills the briefing cited belong to the DW chassis (DOI 22132648) and were
partly demoted (sf44). Reporting them as D's would manufacture a deficit.

But under the mission's optimizer ("smallest theory that survives the entire filter"), D is
dead as a live candidate on committed grounds:
1. Its **only distinctive structural feature** (two metrics → separate Ω_dm carrier) is a
   parameter-free THEOREM-level failure (route6, 30/30): the bimetric buys no dark matter, so
   D collapses to the DBI-khronon completion with **no advantage over the other chassis.**
2. In that collapse it **inherits the DBI-khronon c_T²−1 ≈ +3.9×10⁻² FLRW liability** (GW170817
   ~13 orders) with no committed cancellation.
3. It has passed **zero** hard certification gates (DOF, c_T, PPN, lensing, Boltzmann all OPEN);
   the repo's own ledger calls it "the most open chassis — freezing restarts the program from
   near zero."

An architecture whose distinctive mechanism is refuted and which then reduces to a completion
carrying a live, uncancelled c_T failure is not the smallest surviving theory. **STRUCTURALLY-DEAD.**

## THE ONE CALCULATION THAT WOULD DECIDE IT

Compute c_T on the **actual BIMOND + DBI-khronon FLRW background** (not the DW audit's): does the
+3.9×10⁻² tensor-speed excess transfer, or does the full second-order Ricci scalar R^(2)|_TT
protect c_T = 1 (as it does on Minkowski)? A committed c_T = 1 result here would be the single
fact that reopens D from STRUCTURALLY-DEAD to CONDITIONALLY-VIABLE (the BD-ghost DOF certificate
would then become the next gate). Until then the c_T cell is OPEN-ADVERSE and D stays dead.

---
Scripts reproduced this session (exit 0): route6_bimond_twin_2026.py (30/30),
sf12_adjudicate_sf11b_2026.py (12/12), sf43_dw_localized_dof_ghost_2026.py (6/6),
sf44_dw_physical_phase_space_2026.py (6/6).
Records read: STANDING.md, CLOSURE_LEDGER.md:30, NEGATIVE_RESULTS_CLOSURE.md,
papers_2026/PAPER1_carrier_nogos_and_dw_audit.md §4.1/§4.5.
