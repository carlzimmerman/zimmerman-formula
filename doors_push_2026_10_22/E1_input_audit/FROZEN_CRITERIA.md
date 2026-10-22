# E1_input_audit — FROZEN CRITERIA (written before any script or number of this lane)

Lane of doors push wave E (`../BRIEF.md`, `../BRIEF_E_AUDIT.md`). κ = ½ is FITTED. Both footings reported, never
pooled. Not theory closed. Nothing here says the data favour the framework.

## What is audited

The empirical inputs of the verdicts D1, D2 (+ `prep_2026/gaia_dr4_prep/NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md`),
D4, D5, D6, D7, D7b, D7c, D8 (incl. Stilp+2013), D8b, and the record inputs they rest on: CFG820 globulars
(Υ_V = 1.6 SPS, Pal 3 binaries per CFG334), the κ measurements CFG493 / A51 / A71 / A81, the a₀ footings, the
Cookson+26 and Chae & Yoon 26 wide-binary results, the Hees 2014 / Park 2026 Q₂ bounds
(`prep_2026/planetary_doors/BOUNDS.md`), P4's u and M_c = (Ω_c/Ω_b) M_b.

## Deliverable 1: input ledger

`INPUT_LEDGER.md`: every input → one class → source file → verdicts that use it. Classes (owner rule 2026-10-10):
RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY.
An input built from several steps takes the class of its most contaminated step, and the ledger names that step.

## Deliverable 2: sensitivities (clean substitutes on disk only; no download, no new outside data)

Substitutes, frozen now:
- **S1 background.** Framework-native a₀ band = c·H₀,native/Z with H₀,native from A46 (`a46_results.json`: 2-pt fit,
  3-pt fit, exact map) and the Planck-free CFG886 primary (DESI DR2 BAO + BBN, H_Λ = H₀√(1−Ω_m)). The alt footing
  is tested for whether it exists in the native background.
- **S2 κ.** CFG493, A51, A71, A81 re-expressed in the native background (κ_DE and κ_P3 conventions) over the S1 band.
- **S3 SPS M/L ±0.2 dex** where an SPS M/L is fixed: CFG820 Υ_V (L★ floor; D8 thermal Δχ²), D6 KiDS M★ (u_gal),
  CFG687 stellar fraction f_s (u_MID).
- **S4 standard-MOND machinery inside CFG820** (ν_RAR + algebraic EFE "ν(y_int + y_ext)"): re-evaluate the L★ floor with
  the canonical law ν_L in place of ν_RAR (same EFE recipe), and with ν_L and no EFE term (isolated cluster). Bracket only;
  the action's own (AQUAL-limit) answer is not computed here.
- **S5 Q₂ and γ_v at the native a₀** (D7b, D7c incl. the β family and SPARC side; D2 by interpolation in ln a₀ between its
  two footings, labelled as interpolation). The QUMOND → action field-equation question belongs to lane E2: here it is
  classified and cited only.
- **S6 ΛCDM distances in lensing.** D6 u_gal (KiDS B21, h = 0.70) and u_MID (CFG687 eRASS1 × KiDS, h = 0.70) redone with
  physical scalings at the native h (R ∝ h⁻¹, ΔΣ ∝ h, M★ ∝ h⁻², M_gas ∝ h^(−5/2)); D6's r_sp machinery (NFW c = 4.5,
  r_sp = 0.83 r200m) bracketed by r_sp × 0.8 and × 1.25 in the H-VR profile test.
- **S7 Ω_c/Ω_b.** CFG886 (a) 5.272 ± 0.218 and (b) 6.122 ± 0.321 in place of 5.3643, on A18's R_req = 5.552 ± 0.427.

## Outcome lines (frozen)

For each verdict and each substitute, at the substitute's central value:
- **FLIP**: a pass / fail / excluded / consistent / no-go class in that verdict changes.
- **MATERIAL**: the verdict's headline number moves by ≥ 1σ of its own quoted error, or by ≥ 10 % where no error is
  quoted, or a quoted significance moves by ≥ 1σ.
- **CLEAN**: neither.
- **DEFERRED**: no clean substitute on disk (named, with what would be needed).

Lane verdict: **CRISP FINDING** if any FLIP or MATERIAL; otherwise **NOTHING NEW (clean)**.

## Checks (script `e1_input_audit.py`; one line each; exit 0 iff all pass)

- K1 native a₀ reproduced: c·H₀/Z from A46's H₀ values equals A46's own a0 entries to 1e-6 (relative).
- K2 canonical footing identity: c·H₀√Ω_Λ/Z at (67.4, 0.685) equals 9.36e-11 to 2e-3.
- K3 D7c reproduced: Q₂(β = 2.5, canonical, E0) and the SPARC worst paired z (β = 2.5, canonical) equal
  `d7c_q2_rar_gate_results.json` to 1e-6 (relative) and 0.02.
- K4 CFG820 reproduced: L★_95 on CFG820's grid, both footings, equals `cfg820_results.json` to 5e-3.
- K5 D6 reproduced: u_MID (canonical) = 0.47157 ± 1e-3 and u_gal (canonical) = 0.660 ± 0.002.
- K6 ledger complete: every audited verdict has ≥ 1 ledger row; every row has one of the five classes and a source
  path that exists in the repository.

**MUTATE** (`E1_MUTATE=1`): the native a₀ uses 2π in place of Z. K1 must fail. Output to `*_MUTATE.out`,
`*_results_MUTATE.json`.

Compute: `OMP_NUM_THREADS=1 nice -n 10`, single thread, < 2 GB RSS. Other lanes' scripts are executed read-only
(source text exec'd up to a marker, no file they own is written).
