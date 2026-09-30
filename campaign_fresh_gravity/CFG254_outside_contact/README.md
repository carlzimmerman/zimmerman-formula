# CFG254 — an "outside contact" with the dark energy, and "nothing before recombination": phase-1 hand-check

**Research direction: this lane was directed by the owner (the repository's author), who proposed the idea and asked for it to be tested.**

- **Criteria:** `../CFG254_FROZEN_CRITERIA.md`, written before this lane's script existed. Its sha256 (`6ae882ef…6313`) was recorded in `CFG254_CRITERIA_SHA256.txt` before the script was written. §0 of the criteria is a blindness disclosure. It lists the record numbers and CAMB smoke-test numbers seen beforehand, and one coincidence noticed while planning.
- **κ = ½ FITTED, not derived.** Nothing here says the theory is closed or that any data favour any model. Literature values not already in a committed file are **(memory, UNVERIFIED)**. No downloads.
- **Status:** phase 1. Nothing is committed; the orchestrator reviews and commits.

## The idea (neutral wording)

Our universe sits inside something larger. Recombination was like a paddle striking a water surface, and/or something outside touches the dark energy and drives a "reaction" in it that causes the expansion we see. The owner also suggested that nothing exists before recombination.

## Bottom line (plain)

This is a bold picture, and parts of it can be tested. Where it can be tested, the record says the following.

1. **"Nothing before recombination" is ruled out by the record's own numbers.** With no hot past there would be:
   - no primordial helium: +82σ against Y_P = 0.245 ± 0.003;
   - no deuterium: +88σ;
   - no sound horizon, so no acoustic peaks: 100θ* would be 0, against 1.04109 ± 0.00030, which is +3470σ;
   - no BAO ruler: DESI DR1 implies r_d = 148.6 ± 0.9 Mpc, +167σ from zero;
   - no neutrino background: N_eff = 2.99 ± 0.17, +18σ.

   At fixed Planck parameters, the sound waves must have been running since at least **z ≈ 10⁶**. Even a start at z = 10⁵ leaves the acoustic angle 64σ short. The "created exactly as if it had a past" version fits everything, but only because it is the standard past restated. It is **UNTESTABLE-AS-STATED**.

2. **About the paddle image.** In standard physics the "ripples" the image suggests (the baryon acoustic oscillations) were made **before** recombination and **frozen** at it. Recombination is when the waves stop, not when they start.

3. **A one-time contact that adds dark energy at redshift z_c:**
   - **Late contact.** A contact after z ≈ 1 that switches on **all** of it is **excluded** by the repo's CMB distance priors plus DESI DR1 BAO (Δχ² = 24–1546). The injected fraction A is bounded at 12–56% for z_c between 0.3 and 1.
   - **Earlier contact.** From z_c ≈ 1.5 up to recombination, the repo's distance data **cannot see it** (NON-DIAGNOSTIC). Supernovae and DR2 BAO are not in the repo.
   - **The framework's a₀ does see it** up to z_c ≈ 5. On the tie a₀ = κc√(Gρ_DE), a contact that switched on all the dark energy after z_c would switch off a₀ in galaxies above z_c. At z ≈ 5 the CRISTAL outer-radius rows show more mass discrepancy than that allows, on **both** baryon routes. So such a contact is **disfavoured robustly for every z_c ≤ 5 tested**. This is framework-conditional (ΛCDM supplies the discrepancy with dark matter) and rests on six discs.
4. **A continuing drive** keeps adding energy, so ρ_DE never falls (w ≤ −1 at all times). It carries **0 / 1.1 × 10⁻³ / 5 × 10⁻⁵** of the committed DESI DR2 posterior weight (DESY5 / Pantheon+ / Union3): **EXCLUDED**. It would also make a₀ fall into the past. "Drive, then leak" is just the shape of DESI's own w0–wa fits (the peak is the w = −1 crossing at z ≈ 0.36–0.44). That makes it a restatement, NON-DIAGNOSTIC.
5. **The paddle = recombination (energy from recombination feeds the dark energy).**
   - **Distances.** It changes nothing after recombination, so the distance data cannot test it (Δχ² = 5 × 10⁻⁸) and it keeps the flat a₀.
   - **A coincidence, noticed before the criteria were written.** The hydrogen binding energy at the moment of recombination, 13.6 eV × n_H(z*), is **1.02 ρ_Λc²**.
   - **The reading's own amount is 1.67 ρ_Λc².** That is the energy released over the whole recombination history, kept undiluted by a w = −1 bath.
   - **Look-elsewhere.** The chance that at least one of the menu's candidate energies lands within ×2 is 0.31.
   - **Grade: p\*, a post-hoc coincidence and not a mechanism.**
   - **What it genuinely predicts:** the cosmological recombination lines should be **missing**. They are 1.5 × 10⁻⁸ of the CMB energy at z*, which no current experiment can see.
6. **A bubble collision or brane contact** is **UNTESTABLE-AS-STATED**: no direction, size, amplitude or time is given.
   - The repo holds no CMB map.
   - The SPARC a₀ sky-dipole limit bounds a local dark-energy contrast to below 0.86. It cannot see a horizon-scale contact, which would need a contrast of 93.
   - The published collision searches (memory, UNVERIFIED) found nothing.

**Nothing here is graded as supported.** Every reading adds constants (G5), or is post-hoc (the recombination amount), or restates ΛCDM wherever the data look.

## Run

| mode | command | rc | checks | outputs |
|---|---|---|---|---|
| main | `python3 campaign_fresh_gravity/CFG254_outside_contact/CFG254_handcheck.py` | 0 | 11/11 | `CFG254_handcheck.out`, `CFG254_handcheck_results.json` |
| MUTATE | `MUTATE=1 python3 …/CFG254_handcheck.py` | 1 | 10/12 (L1 and L2 fail, as required) | `CFG254_handcheck_MUTATE.out`, `CFG254_handcheck_results_MUTATE.json` |

**Timing and determinism.** The main run takes about 170 s (the G2 grid is 285 profiled fits), and MUTATE about 80 s. Two main runs gave identical `.out` files (apart from the timing line) and byte-identical `.json`. No bytecode was written. Nothing was written outside this directory.

**Controls (all pass):**
- C0: FP0's a₀ on both footings.
- C1: CAMB reproduces XR26's committed r_drag = 147.0491, 100θ* = 1.041116 and z* = 1089.914.
- C2: this lane's CHW 2019 implementation gives XR26's committed χ² = 1.66414.
- C3: every copied input equals its committed source (CFG4's BAO list, XR26's priors, the θ*, N_eff and BBN observations).
- C4: the r_d spline matches CAMB to 4 × 10⁻⁷.
- C5: the integrator matches scipy quad to 2 × 10⁻¹⁶.
- C6: the chains reproduce CFG195 exactly.
- C7: the exec'd CFG222 machinery reproduces CFG222's committed FLAT and H(z) statistics exactly.

**MUTATE** sets every contact amplitude to zero and restores R1's full past:
- every grid point then gives Δχ² = 0 exactly and a₀(z)/a₀(0) = 1 exactly (L3);
- every G3 law reads SAME-AS-FLAT;
- R1's pulls become −0.6 / −1.4 / −0.1 / +1.8 / −0.3σ (standard cosmology);
- L1 and L2 fail, so rc = 1.

## Results by reading (never pooled)

### R1 — nothing before recombination (G1)
| test (repo numbers) | R1-lit predicts | observed | pull | class |
|---|---|---|---|---|
| (a) Y_P (XR26 / PDG 2024) | 0 | 0.245 ± 0.003 | +81.7σ | CONTRADICTS |
| (b) D/H | 0 | 2.547 ± 0.029 × 10⁻⁵ | +87.8σ | CONTRADICTS |
| (c) 100θ* | 0 (r_s = 0) | 1.04109 ± 0.00030 | +3470σ | CONTRADICTS |
| (d) BAO r_d (DESI DR1 at Planck distances, diagonal) | 0 | 148.64 ± 0.89 Mpc | +167σ | CONTRADICTS |
| (e) N_eff (Planck + BAO 2018, as cited in atomos A05) | 0 | 2.99 ± 0.17 | +17.6σ | CONTRADICTS |

**Standard physics for comparison** (XR26, PArthENoPE): Y_P −0.6σ and D/H −1.4σ.

**Truncated sound horizon at fixed Planck parameters** (illustrative, no re-fit). The fraction of r_s(z*) kept, if sound waves start only at z_start:

| z_start | fraction kept | pull |
|---|---|---|
| 1101 | 0.007 | — |
| 3000 | 0.52 | — |
| 10⁴ | 0.83 | −586σ |
| 10⁵ | 0.982 | −64σ |
| 10⁶ | 0.998 | −6σ |

To be within 1σ, the waves must start before z = 5.9 × 10⁶ (1.3 × 10⁶ for 5σ).

**Reported only.**
- **Helium from stars:** fusing 24.5% of all baryons releases 1.6 × the CMB's energy density (the old "coincidence"). Stellar helium also comes with metals, while Y_P is measured at very low metallicity (memory, UNVERIFIED).
- **The blackbody:** FIRAS limits (memory, UNVERIFIED). A blackbody made in equilibrium at z* does not separate R1-lit from R1-om. The acoustic phases and the super-horizon TE correlation do.

**Verdict: R1-lit CONTRADICTED; R1-om UNTESTABLE-AS-STATED** (a restatement of the standard past).

### R2a — a one-time contact (G2, G3)

**The G2 likelihood:**
- data: CHW 2019 distance priors plus the twelve DESI DR1 BAO numbers (diagonal);
- profiled over ω_b, ω_c, h and n_s;
- ΛCDM: χ²_min = 16.82 for 16 numbers and 4 parameters;
- SN are not scored.

**Step: ρ_DE lower by the fraction A before z_c.**

| z_c | Δχ²(A = 1) | class (A = 1) | A₉₅ (one-sided) | a₀ drop at A₉₅ |
|---|---|---|---|---|
| 0.1 | 1546 | EXCLUDED | 0.37 | −0.10 dex |
| 0.2 | 652 | EXCLUDED | 0.22 | −0.05 dex |
| 0.3 | 509 | EXCLUDED | 0.14 | −0.03 dex |
| 0.5 | 336 | EXCLUDED | 0.12 | −0.03 dex |
| 0.7 | 119 | EXCLUDED | 0.40 | −0.11 dex |
| 1.0 | 24.3 | EXCLUDED | 0.56 | −0.18 dex |
| 1.5 | 1.2 | ALLOWED | 1 | a₀ → 0 allowed |
| 2 to 1090 | −2.1 to 0.9 | NON-DIAGNOSTIC | 1 | a₀ → 0 allowed |

- **H(z)/H_ΛCDM at the A = 1 fits** differs by up to 10–14% for z_c ≤ 0.3, and by ≤ 3.3% for z_c = 1–2.
- **ΛCDM's own onset of acceleration** is at z_acc = 0.65. A constant dark energy becomes dominant late with no event needed, so the late onset does not by itself point to a contact.

**Pulse (width 0.1 in ln(1 + z)):**
- **Excluded at B = 5 for z_c ≤ 3.** B₉₅ runs from 0.12 (z_c = 1) to 1.65 (z_c = 3).
- **TENSION at z_c = 4.**
- **Allowed or NON-DIAGNOSTIC for z_c ≥ 5.** A pulse at z ≈ 5 can raise a₀ there by up to 2.4× without the distances noticing.

**G3, the data** (CFG222 machinery; primary cell ν_mono canonical; every row inherits its gas route's caveat):

| law | RC100 slope | R_e fit | R_e ind | R_out fit | R_out ind | class |
|---|---|---|---|---|---|---|
| FLAT (reference) | −0.029 C | +0.053 over | +0.117 C | +0.019 C | +0.106 C | — |
| STEP A = 1 at z_c = 0.5 … 4 | −0.055 to +0.048 | +0.165 over | +0.267 C | +0.111 over | +0.294 over | **WORSE-THAN-FLAT-ROBUST** |
| STEP A = 1 at z_c = 5 | −0.029 C | +0.148 over | +0.255 C | +0.074 over | +0.265 over | **WORSE-THAN-FLAT-ROBUST** |
| STEP z_c = 1, A₉₅ = 0.56 | −0.012 C | +0.084 over | +0.160 C | +0.055 C | +0.153 C | route-dependent |
| PULSE z_c = 5, B₉₅ = 5 | −0.029 C | −0.004 C | +0.024 C | −0.061 C | +0.004 C | NOT-WORSE |

- **The step result.** A contact that switched on all the dark energy after z_c leaves the z ≈ 5 discs Newtonian on the framework's tie. At the outer radius the data show more discrepancy than that on both baryon routes. This is **framework-conditional**: in ΛCDM dark matter supplies the discrepancy, and nothing bounds the z ≈ 5 dark energy this way. It rests on six discs.
- **The pulse at z_c = 5** sits nearer zero on the CRISTAL rows than flat does. That is the flat law's known small under-prediction at z ≈ 5 on the fit route (CFG213). It is a description, not a detection.

**Post hoc (reported only).**
- 110 of the 285 grid points fit the compressed data better than ΛCDM. The lowest is a pulse at z_c = 0.5 with B = 0.5, at Δχ² = −7.9.
- This is look-elsewhere over 285 points and two shapes. The DR1 BAO are used without their correlations, SN are absent, and DR2 BAO are not in the repo. **Not a detection.**
- Multistart and Powell re-fits agree to 1e-12, so the negative values are properties of this compressed likelihood, not failed fits.

**Verdict: R2a-step and R2a-pulse CONSTRAINED.** They are bounded by distances for late contacts and, on the framework's tie, by the z ≈ 5 a₀ rows for contacts up to z_c = 5. G5 adds +2 constants.

### R2a-rec — the paddle = recombination

| menu item (criteria 4.2c) | J/m³ | /ρ_Λc² (canonical) | /ρ_crit c² (alt) |
|---|---|---|---|
| E1 13.6 eV × n_H(z*) | 5.36e-10 | **1.021** | 0.699 |
| **E2 released over the recombination history (PRIMARY)** | 8.75e-10 | **1.666** | 1.141 |
| E3 E2 + helium | 2.97e-8 | 56.5 | 38.7 |
| E4 Lyman-α × n_H(z*) | 4.02e-10 | 0.766 | 0.524 |
| E5 gas thermal energy at z* | 1.84e-11 | 0.035 | 0.024 |
| E6 photons at z* | 5.9e-2 | 1.1e8 | 7.7e7 |
| E7 / E8 baryons / matter at z* | 4.9e-2 / 0.31 | 9e7 / 6e8 | 6e7 / 4e8 |

- **Look-elsewhere:** K = 6 distinct items spanning 10.2 dex, so P(at least one within ×2) = 0.31.
- **Grade: p\*** (post-hoc, noticed before the criteria and disclosed there).
- **The primary amount misses ρ_Λ by ×1.67.** The instantaneous proxy E1 matches to 2%, but it is not the reading's own amount.
- **Distances:** the step at 1090 with A = 1 gives Δχ² = 4.8 × 10⁻⁸, **NON-DIAGNOSTIC**. It keeps the flat a₀ because it is ΛCDM below z*, a restatement.
- **Missing recombination radiation:** E2/ρ_γ(z*) = 1.5 × 10⁻⁸. That is far below FIRAS, so it is **UNTESTABLE now**, but it is a genuine prediction for future spectral-distortion experiments.
- **Fast-sink kinetics** (reported, illustrative). If the vacuum takes the binding energy instead of a photon, x_e follows Saha: x_e = 0.5 moves from z = 1276 to 1369. The last-scattering redshift moves to z* ≈ 1170, and 100θ* becomes 0.9925, which is −162σ at fixed parameters. That version would already be ruled out. The "photons emitted, then absorbed by the vacuum" version keeps standard kinetics and is not computed.

### R2b — a continuing drive
| chain | f_mono (w ≤ −1 for all z ≤ 2.5) | p(w0 < −1) | crossing fraction, median z |
|---|---|---|---|
| DESY5 | 0 | 0 | 0.9998, 0.405 |
| Pantheon+ | 1.1e-3 | 1.3e-3 | 0.9978, 0.356 |
| Union3 | 5.2e-5 | 5.2e-5 | 0.9998, 0.444 |

- **R2b-mono and R2b-const: EXCLUDED** (CPL chains). The committed example is CFG176's accumulation drive, excluded at 27–36σ.
- **a₀(z)/a₀(0) under constant-w drives:**

  | w | z = 1.5 | z = 5 |
  |---|---|---|
  | −1.05 | −0.03 dex | −0.06 dex |
  | −1.1 | −0.06 dex | −0.12 dex |
  | −1.2 | −0.12 dex | −0.23 dex |
  | −1.5 | −0.30 dex | −0.58 dex |

  All four laws are worse than flat on the CRISTAL fit route (route-dependent).
- **R2b-leak: NON-DIAGNOSTIC.** It is the CPL fits' own shape, and it needs a phantom epoch (CFG176, CFG195).

### R3 — bubble collision / brane contact (G4)
- **Local contrast.** a₀ ∝ √ρ_DE gives a dipole D = ε/2. With A₉₅ = 0.43 (CFG182) or 0.40 (CFG192), the local dark-energy contrast is ε < 0.86 (0.80).
- **Horizon-scale contact.** A gradient over D_M(z*) = 13,869 Mpc would need ε = 93 (87) to show at the SPARC depth (largest distance 127.8 Mpc): **NON-DIAGNOSTIC**.
- **CMB: not tested by the repo.** From memory (UNVERIFIED):
  - Feeney, Johnson, Mortlock & Peiris 2011 searched WMAP7 for collision discs and found four candidates, but no evidence for collisions.
  - The follow-ups (Feeney et al. 2013; Osborne, Senatore & Smith 2013; the Planck isotropy papers) report no detection.
  - The large-angle anomalies sit at about 2–3σ.
- **Verdict: UNTESTABLE-AS-STATED.**

## What would make each idea testable (minimal specifications)

- **R1:** nothing. The literal version is tested and contradicted. The "as if" version can be made testable only by giving up being "as if".
- **R2a:**
  - z_c and the injected amount A;
  - what loses the energy (the exchange rate Q; in 4D GR a source-free step violates the Bianchi identity);
  - for a pulse, how the energy leaves again.

  With those given, distances bound z_c ≲ 1, and on the framework's tie the z ≈ 5 a₀ rows bound z_c ≲ 5.
- **R2a-rec:**
  - the channel: a direct vacuum sink (then a modified recombination code plus the Planck likelihood decides it; the fast-sink limit is already −162σ), or photons absorbed later (then the missing recombination lines decide it, for future spectrometers);
  - an amount fixed **before** looking. E2 misses by ×1.67.
- **R2b:** the drive law ρ_DE(t) or w(z). Monotone injection is already excluded.
- **R3:**
  - the direction (two angles), angular radius, amplitude profile and time of the collision, for the Feeney-template CMB search;
  - for a₀: a contact wall within about 130 Mpc with ε > 0.86 would show in the SPARC dipole.

## Genuinely new testable predictions

1. **On the framework's tie, a₀ in high-z galaxies measures the dark energy where distances cannot.** A contact at z_c between 1.5 and 10 is invisible to the repo's distances, but it predicts a₀ → √(1 − A) a₀ above z_c. The CRISTAL z ≈ 5 rows already disfavour A = 1 for z_c ≤ 5, robustly at R_out and conditional on the framework. a₀ at z > 5 would bound z_c = 5–10.
2. **R2a-rec predicts the absence of the cosmological recombination lines**, which are 1.5 × 10⁻⁸ of the CMB energy at z*. This is a target for future spectral-distortion experiments. The fast-sink version is already excluded by the acoustic angle (illustrative, −162σ).

## Limits and disclosures

- **Inputs.** All inputs are compressed:
  - CHW priors, not the Planck likelihood;
  - DESI DR1 BAO, diagonal (DR2 BAO are not in the repo);
  - no SN outside the chains;
  - CPL chains for R2b.

  The R1 truncation table is at fixed parameters. The fast-sink row is illustrative.
- **The G3 rows** inherit their gas routes (CFG213/220/222). n = 6 or 12, and the verdicts are framework-conditional.
- **Debug runs (in place; the outputs were overwritten):**
  - The first full main run printed "0 SPARC distances" (a fixed-column slice bug); it was fixed to a whitespace split.
  - The same run classed `PULSE z_c=1.0` as WORSE-THAN-FLAT on a floating-point tie (its CRISTAL statistics equal flat's to 1e-16). A 1e-9 tie tolerance was added, and the class became NOT-WORSE.
  - The first MUTATE run left R1's BAO pull at its data-only value; fixed so the full past predicts CAMB's r_drag.
  - One run crashed on a string-concatenation typo.
  - The main-run numbers did not change across these fixes, apart from the R3 numbers (the SPARC fix) and the one G3 class named above; the final main `.out` differs from the one before the wording change only in the verdict and headline wording.
- **Post-hoc additions after the first run:**
  - the "POST HOC" minimum-Δχ² line;
  - the "a₀ → 0 allowed" print;
  - the G3 mention in the R2a-step verdict and headline.
- **Implementation details the criteria did not state:**
  - E2 integrates over z ∈ [50, 1800], to exclude reionization, with x_H = min(x_e, 1);
  - F = 0 is represented by 10⁻⁹.
- **A wording slip in the criteria:** §4.2(b′) says "six rows" but lists five. The five listed were run; C7 checks all six.
- **Memory items, UNVERIFIED:** FIRAS limits; dY/dZ; deuterium destruction; the recombination-line amplitude; the TE super-horizon argument; the bubble-collision literature.
- **Standing rules:** no personal names; κ = ½ FITTED; no "favours" language.

## Files
- `../CFG254_FROZEN_CRITERIA.md`; `CFG254_CRITERIA_SHA256.txt`
- `CFG254_handcheck.py`
- `CFG254_handcheck.out`, `CFG254_handcheck_results.json`
- `CFG254_handcheck_MUTATE.out`, `CFG254_handcheck_results_MUTATE.json`
- `README.md`
