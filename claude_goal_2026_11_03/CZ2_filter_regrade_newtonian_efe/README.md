# CZ2_filter_regrade_newtonian_efe: with the Newtonian external field, the TIDAL rule SURVIVES on alt (and is no worse than plain QUMOND on the dwarfs); the LOCAL rule SURVIVES on alt but one dwarf below plain; KT25's r_M/2 FAILS Cassini on both footings. Canonical keeps no filter form

Criteria `FROZEN_CRITERIA.md` (1fadaa469a), committed alone before the script. Run `OMP_NUM_THREADS=1 python3 -I cz2.py`, output `cz2.out` / `cz2.json`, timing `cz2.time` (21 min, 0.21 GB); MUTATE twin `cz2_MUTATE.*`. No download. κ = ½ FITTED, held fixed. Footings never pooled. No cold component, no particle. Not theory closed. Nothing here says the data favour the framework.

The one change from the KT lanes: the external field inside QUMOND's ν is the host's Newtonian field (dwarfs G M_MW / D², M_MW,b 7e10; Cassini η from inverting ν(y) y = 2.32e-10 / a0). Cassini and dwarfs recomputed; MW and SPARC carried from the committed KT JSON (those models have no external field).

| footing | form | T0 MW cells | T1 Cassini Q2/ceiling | T2 dwarfs (line 15; plain 18) | T3 SPARC d rms | **Label** | STRICT (≥ plain) |
|---|---|---|---|---|---|---|---|
| canonical | LOC ξ_loc (KT26/27) | 0 | 0.0039 | 17 | +0.0129 | **FAILS: MW, SPARC** | fail |
| canonical | TID ξ_tid (KT28) | 0 | 0.208 | 18 | +0.0079 | **FAILS: MW, SPARC** | pass |
| canonical | HALF r_M/2 (KT25) | 9 | **1.179** | 18 | +0.0021 | **FAILS: Cassini** | pass |
| alt | LOC | 30 | 0.0215 | 17 | +0.0031 | **SURVIVES** | fail (17 < 18) |
| alt | TID | 19 | 0.442 | 18 | +0.0005 | **SURVIVES** | pass |
| alt | HALF | 78 | **2.97** | 18 | -0.0006 | **FAILS: Cassini** | pass |

The labels match the expectation written in the criteria for LOC and HALF (CZ1 had already printed those numbers); TID's Cassini and dwarf rows were the only open grades, and both pass.

## Reading
- **The record's filter verdicts change.** KT25's ε = κ on canonical, the record's only all-four survivor before this, fails Cassini once the Sun's external field is Newtonian (0.48 → 1.18x). KT27's local-rule dwarf failure was the MOND-field artefact (14 → 17, Fornax back). KT28's tidal rule on alt keeps all four, with Cassini now 0.44x rather than 0.21x.
- **Canonical has no surviving filter form.** Alt has two, both local and mass-free; TID is the cleaner, since it ties plain QUMOND on the dwarfs and LOC sits one below.
- **The dwarfs no longer discriminate.** With the Newtonian field every form is at plain QUMOND's 18/24 or one below; the filter adds nothing there. Fornax now comes out at 12.5–13.2 km/s at Υ = 2 (obs 11.7 ± 0.9), passing inside the Υ 1–3 grid, high rather than low.

## As hard as a fail
- **Third grading, two post hoc rules.** LOC and TID were each proposed after an earlier fail; two rules x two footings were tried. One survival on one footing is not a detection of anything.
- **T0 is carried and is corner cells only:** alt TID's 19 cells are all BV2, R_d 2.6, Σ_b +2σ, M_bb at the box top, thick share 0.26–0.35, none at the star-count share 0.12, strict h fails; one ξ value at R0, in-plane, no vertical tidal term.
- **T3 is carried and sits near the median line:** TID alt median +0.043 against 0.05; inner points lose phantom.
- **Cassini margin for TID alt is 2.3x**, inside the reach of the approximations: 1D quadrature external field, QUMOND's anisotropic factor ignored, spherical row-wise smoothing (not mass-conserving), |g| not iterated, and the Newtonian Galactic field from inverting the simple ν.
- E2 (MW + M31 Newtonian vector sum, printed beside, not graded): plain 17 on both footings; TID 16 canonical, 17 alt (equal to plain); LOC 16 on both. All are above the 15 line; Andromeda I is lost in every arm.
- The dwarf model's M_MW,b 7e10 gives a MOND field 14–17 % under (200 km/s)²/D (CZ1 K2); a heavier MW strengthens the external field.

## Checks
K1: with the KT field the code reproduces KT27's LOC (Cassini 0.0005 / 0.0021, dwarfs 14) and KT28's TID (0.11 / 0.209, dwarfs 15, Fornax 9.0 / 9.4). K2: with the Newtonian field it reproduces CZ1 (LOC 0.003948 / 0.02147, HALF 1.179 / 2.97, dwarfs 18 / 17, Fornax 11.94 / 12.52). K3: carried MW and SPARC values match the READMEs. 0 failed checks.
