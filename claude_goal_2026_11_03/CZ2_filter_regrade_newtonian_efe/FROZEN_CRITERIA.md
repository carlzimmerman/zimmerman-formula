# CZ2_filter_regrade_newtonian_efe — FROZEN CRITERIA (before any script; no new number computed)

Owner, 2026-11-03: "Run CZ2". CZ1 (8e701cc3e6) found that the KT dwarf and Cassini rows put the MOND field (200 km/s)²/D, and
the observed Galactic field, into QUMOND's ν. The field equation's ν takes |∇Φ_N|, the Newtonian total. CZ1 reported the
change as unlabelled numbers only, because its form-check label missed a frozen tolerance (A1). This lane re-grades the three
filter forms on all four tests with the Newtonian external field, under its own labels.

κ = 1/2 FITTED, held fixed. Footings never pooled. No cold component, no particle. Not theory closed. Nothing here says the
data favour the framework. No download. Small job, one thread.

## The model change (adopted from the field equation, not graded here)
The external field inside ν is the host's **Newtonian** field. Nothing else changes from the copied code.
- Dwarfs: g_Ne = G M_MW / D² for MW satellites (M_MW,b = 7.0e10 M☉, KT15's frozen value; D heliocentric), 0 otherwise
  (CZ1's E1). E2 (MW + M31 vector sum) is printed beside, not graded.
- Cassini: η_N from inverting ν(y) y = η0, η0 = 2.32e-10 / a0 (CZ1 Part C). η_N replaces η0 everywhere in the Sun's model:
  in the field that sets ξ and in KT16's integral.
CZ1's Label A missed its 10 % line because the 1D quadrature total differs from McGaugh–Milgrom's asymptote by ν/(ν − 1); that
gap is a property of the 1D form used in every KT lane, not of which field enters ν. Stated, not re-litigated.

## Candidates (all already in the record)
- **LOC**: KT26/KT27's local rule ξ_loc = |g|² / (|d|g|/dr| g*), |g| the total board-law field (external included), row-wise.
- **TID**: KT28's tidal rule ξ_tid = (4/√3) τ³ / (|dτ/dr|² g*), τ from the system's own field g_int = ν(√(g_N² + g_Ne²)/a0) g_N.
- **HALF**: KT25's constant ξ = r_M / 2 (reference).
KT17's 0.55 r_M is printed beside on Cassini and the dwarfs, not graded.

## Tests per candidate and footing
- **T0 Milky Way: carried, not rerun.** KT17's MW model has no external field, so the change doesn't touch it. Read from the
  committed JSON: LOC = KT26 `mw|<foot>|0.5`, TID = KT28 `kt28_mw.json` `mw|<foot>|0.5`, HALF = KT25 `mw|<foot>|0.5`. Pass if
  n_pass ≥ 1 (KT26/KT28's line). Corner-cell caveats carry over.
- **T1 Cassini: recomputed** with η_N. Pass if Q2 ≤ 5.2e-27 s⁻² (KT16's ceiling).
- **T2 dwarfs: recomputed** with E1. Pass if ≥ 15/24 (the record line, KT25/KT27/KT28, unchanged). Printed beside and labelled
  separately: **STRICT** = count ≥ plain QUMOND's count under the same E1 field (no worse than no filter).
- **T3 SPARC: carried, not rerun.** KT19's SPARC code has no external field. LOC = KT27 `sparc|<foot>`, TID = KT28
  `sparc|<foot>`, HALF = KT25 `kt25_sparc.json` `<foot>`. Pass if the stored `ok` / label is a pass (d rms ≤ 0.005 and
  |median| ≤ 0.05, their frozen lines).

**Label per candidate and footing: <CAND> SURVIVES** if T0–T3 all pass; **<CAND> FAILS: <tests>** otherwise. The STRICT dwarf
line is reported next to each label as "STRICT pass/fail" and doesn't change it.

## Expectation on record, not blind
CZ1 already printed LOC and HALF under the corrected field:
- LOC dwarfs E1 17/24 both footings (plain 18), Cassini 0.0039 / 0.0215 x ceiling. With KT26's MW (0 / 30 cells) and KT27's
  SPARC (fail / pass): **I expect LOC FAILS: T0, T3 on canonical and LOC SURVIVES on alt, STRICT fail (17 < 18).**
- HALF: dwarfs 18/24, Cassini 1.179 / 2.97 x: **I expect HALF FAILS: T1 on both footings.** That reverses KT25's canonical
  survival.
- TID is new: Cassini was 0.11 / 0.21 x with η0 and the corrected field raised the other forms' Q2 by 2.5–10x, so T1 is open
  on alt. Dwarfs probably near 18. KT28's MW (0 / 19) and SPARC (fail / pass) mean canonical fails regardless.
So the only open grades are TID T1 and T2. This is the third grading of these rules (KT26/27, KT28, here); LOC and TID were
both chosen after seeing earlier fails. Two rules x two footings: a single survival is not a detection of anything.

## Checks
- K1: with the KT field (E0 = 200²/D, η0) the code reproduces KT28's TID rows (Cassini 0.11 / 0.209 x, dwarfs 15/24 both,
  Fornax 9.0 / 9.4 km/s) and KT27's LOC rows (Cassini 0.0005 / 0.0021, dwarfs 14/24).
- K2: with E1 / η_N it reproduces CZ1's LOC and HALF numbers (dwarfs 17 and 18, Fornax 11.94 / 12.52, Cassini 0.003948 /
  0.02147 and 1.179 / 2.97).
- K3: the carried T0/T3 values match the READMEs (KT26 0 / 30, KT28 0 / 19, KT25 9 / 78; SPARC d rms KT27 +0.0129 / +0.0031,
  KT28 +0.0079 / +0.0005, KT25 +0.0021 / -0.0006).
- MUTATE: ν = 1; Cassini Q2 must be 0 and the dwarfs fall to plain Newton (CZ1: 3/24); the run exits 1.

## Stated approximations (carried from the KT lanes)
1D quadrature external field, QUMOND's anisotropic factor ignored; spherical row-wise smoothing, not mass-conserving; |g| not
iterated; MW one ξ value at R0, in-plane, corner cells only (share 0.26–0.35, none at 0.12, strict h fails); SPARC medians near
the 0.05 line; M_MW,b 7e10 from KT15.
