# CFG254 — an "outside contact" with the dark energy, and "nothing before recombination": FROZEN CRITERIA

**Research direction: this lane was directed by the owner (the repository's author), who proposed the idea and asked for it to be tested.**

Written 2026-09-30, before `CFG254_outside_contact/CFG254_handcheck.py` existed and before any number in this lane was computed by a script. Nothing below may change after a script number is seen; any later deviation goes in the lane README as a disclosed departure. The orchestrator reviews and commits this file. **κ = ½ is FITTED, not derived.** Nothing in this lane says the theory is closed or that any data favour any model. Every literature value not already in a committed file is marked **(memory, UNVERIFIED)**. No downloads.

## 0. What the author knew before writing (blindness disclosure)

- **Committed record numbers read while planning** (inputs, not new data):
  - XR26 (`real_research/cross_thread_review_2026_09_26/`): standard BBN at Planck's ω_b gives Y_P = 0.2470 (PRIMAT) / 0.2467 (PArthENoPE) against the cited 0.245 ± 0.003, and D/H = 2.448 / 2.587 × 10⁻⁵ against 2.547 ± 0.029 × 10⁻⁵ (PDG 2024, as cited there); CAMB at the Planck 2018 best fit gives z* = 1089.91, r_s(z*) = 144.39 Mpc, r_drag = 147.049 Mpc; the Chen, Huang & Wang 2019 (CHW) distance-prior χ² of ΛCDM at the Planck point is 1.664.
  - `real_research/reviews/mi_cmb_camb_run_2026.py`: 100θ* = 1.04109 ± 0.00030 (Planck 2018).
  - `project_atomos/A05_derived_mass_prediction.py`: N_eff = 2.99 ± 0.17 (Planck + BAO 2018, as cited there).
  - CFG4: the twelve DESI DR1 BAO numbers (DESI 2024 III, Table 1, diagonal errors).
  - CFG6 / CFG176 / CFG195: the committed DESI DR2 w0–wa chains; p(w0 < −1) = 0 / 1.3 × 10⁻³ / 5 × 10⁻⁵ (DESY5 / Pantheon+ / Union3); w = −1 crossing in 99.8–100% of the weight at median z = 0.405 / 0.356 / 0.444; CFG176's accumulation reading (a₀ ∝ t, a phantom drive) excluded at 27–36σ.
  - CFG213 / CFG220 / CFG222: at z ≈ 5 the flat law is DISFAVOURED-over on the CRISTAL R_e fit route (data want slightly MORE mass discrepancy than flat a₀ gives) and CONSISTENT on the independent route; RC100's flat slope is −0.029 [−0.072, +0.002]. So **a law that LOWERS a₀ at high z was known in advance to move the fit-route rows the wrong way.**
  - CFG182 / CFG192: SPARC a₀ sky-dipole NULL, A₉₅ = 0.43 (0.40).
- **Numbers seen in a CAMB smoke test** run in the scratchpad before this file (the Planck 2018 best fit): CAMB sound_horizon(z) = 0.0265 / 2.649 / 24.41 / 69.00 / 144.40 Mpc at z = 10⁷ / 10⁵ / 10⁴ / 3000 / 1089.9; x_e = 1.040 / 0.955 / 0.562 / 0.145 / 0.0127 at z = 2000 / 1500 / 1300 / 1100 / 900; CAMB's default BBN predictor gives Y_p = 0.24718 and D/H = 2.4501 × 10⁻⁵ at ω_b = 0.02236. So the R1 truncation numbers in §4.1 are **not blind**.
- **A coincidence noticed while planning (POST-HOC-FLAGGED).** A mental estimate found that the hydrogen binding energy released at recombination, 13.6 eV × n_H(z*), is about 1.0 × ρ_Λc² (canonical footing). It was noticed **before** this file and is therefore capped at **p\*** (§6) whatever its precision. The author expects the integrated version (E2 below) to come out larger by a factor ~1.3–1.6, because much of the release happens at z > z*. Other members of the menu (§4.2c) were chosen after this was noticed; the menu is declared in full to expose the look-elsewhere freedom.
- Nothing was estimated for the G2 fits or the G3 rows of any contact law.

## 1. The idea (neutral wording) and what is already known

The owner's idea: our universe sits inside something larger. Recombination was like a paddle striking a water surface, and/or something outside comes into contact with the dark energy and drives a "reaction" in it that causes the expansion we observe. The owner also suggested that nothing exists before recombination.

**Already told to the owner (standard physics), recorded here as known:** the light-element abundances (BBN), the CMB acoustic peaks (sound waves in the plasma before recombination) and the CMB's blackbody spectrum are evidence of physics before recombination. This lane checks that with the repository's numbers where it has them (§4.1).

**A plain note on the image.** In standard cosmology the "ripples" the paddle picture evokes (the baryon acoustic oscillations) were made **before** recombination and **frozen** at it: recombination is when the waves stop, not when they start. This is standard physics, not a result of this lane.

## 2. Inputs (read-only)

| input | source |
|---|---|
| a₀ footings 9.3603 × 10⁻¹¹ / 1.1312 × 10⁻¹⁰ m/s², H_Λ | `real_research/derivation_chain_2026/FP0_core_postulates_results.json` |
| Planck 2018 best fit, CHW distance priors and correlation matrix | `XR26_cmb.py` (parsed at run time and compared with the lane's copy) |
| XR26 committed K1 and C2 numbers; BBN B2 numbers | `XR26_cmb_results.json`, `XR26_bbn_results.json` |
| DESI DR1 BAO, 12 numbers | `campaign_fresh_gravity/CFG4_cosmology.py` (parsed at run time) |
| DESI DR2 w0–wa thinned chains | `fable_independent_2026/data/desi_dr2_w0wa_thinned/` via `CFG6_common.load_chain` |
| CFG195 crossing fractions and medians | `CFG195_de_flow_referee/CFG195_desi_bound_results.json` |
| high-z a₀ machinery (RC100, CRISTAL, four kernel/footing cells) | the CFG222 script's definitions section, exec'd read-only (no writes) |
| CFG222 committed FLAT / H(z) statistics | `cfg222_lcdm_proxy_results.json` |
| 100θ* = 1.04109 ± 0.00030; N_eff = 2.99 ± 0.17 | the two files named in §0 |
| SPARC distances (for R3's depth) | `real_research/data/SPARC_Lelli2016c.mrt` |
| CAMB 1.6.6 (installed; background, x_e(z), sound horizon, BBN tables) | runs locally |

## 3. The readings (scored separately, never pooled)

- **R1-lit, nothing before recombination (literal).** There were no dynamics before z*: the state at z* was not produced by a hot past. No BBN, no pre-recombination sound waves, no neutrino decoupling.
- **R1-om, the "created as if" version.** The universe began at z* already in exactly the state a hot past would have left. By construction this matches every observation that the standard past matches. It is labelled **UNTESTABLE-AS-STATED** and is a restatement of the standard past, not an alternative to it.
- **R2a, a one-time contact at z_c.**
  - **R2a-step(z_c, A):** ρ_DE(z) = ρ_DE0 for z ≤ z_c and (1 − A) ρ_DE0 for z > z_c, with A ∈ [0, 1] (energy injected, not removed). A = 1 means no dark energy before the contact: "the contact switched it on".
  - **R2a-pulse(z_c, B):** ρ_DE(z) = ρ_DE0 [1 + B g(z)] / [1 + B g(0)], g = exp(−[ln((1+z)/(1+z_c))]² / (2 × 0.1²)), B ≥ 0. The width 0.1 in ln(1 + z) is a declared shape, not scanned. A pulse needs the injected energy to be removed again, which needs a second exchange; recorded, not modelled.
  - **R2a-rec (the paddle = recombination):** z_c = z* and A = 1, with the injected amount supplied by recombination itself (§4.2c). Covariantly this is an interacting vacuum with an energy-transfer rate Q proportional to the recombination rate (energy leaves the baryon–photon sector and enters the vacuum), so it is not ruled out by the Bianchi identity. The step and pulse in 4D GR need the same kind of exchange with an unspecified source; that is recorded, not modelled.
- **R2b, a continuing external drive.**
  - **R2b-mono:** injection that never stops, so ρ_DE never decreases with time: w(z) ≤ −1 at every z.
  - **R2b-const(w):** the constant-w drive family, ρ_DE ∝ (1 + z)^{3(1+w)} with w ∈ {−1.05, −1.10, −1.20, −1.50} (declared).
  - **R2b-leak:** drive, then leakage, so ρ_DE has one interior maximum. Under CPL that maximum is the w = −1 crossing.
- **R3, bubble collision / brane contact.** The contact is local on the sky: a disc-like or dipole-like pattern.

## 4. What is computed

### 4.1 R1 (G1)
Pulls are (observed − prediction)/σ, prediction = the reading's own value.
- **(a) Helium:** no BBN ⇒ primordial Y_P = 0, against 0.245 ± 0.003. Reported beside it (memory, UNVERIFIED): stellar helium comes with metals (dY/dZ of order 1–3), and Y_P is measured in regions of very low metallicity, so stars cannot supply it; the energy density released by fusing 24.5% of all baryons is computed and compared with the CMB's (the old energy "coincidence"), reported only.
- **(b) Deuterium:** no BBN ⇒ D/H = 0 (stars destroy deuterium; no known astrophysical source at this level, memory UNVERIFIED), against 2.547 ± 0.029 × 10⁻⁵.
- **(c) Acoustic scale:** with no sound waves before z*, r_s(z*) = 0 and θ* = 0, against 100θ* = 1.04109 ± 0.00030. Also the truncated sound horizon r_s(z*; z_start) = s(z*) − s(z_start), with s = CAMB's sound_horizon, at fixed Planck parameters, for z_start ∈ {1.01(1 + z*) − 1, 1200, 1500, 2000, 3000, 5000, 10⁴, 3 × 10⁴, 10⁵, 10⁶}, and the z_start at which the fixed-parameter θ* pull is 1, 3 and 5σ. **Illustrative:** a re-fit could absorb part of a small truncation through the r_s–H₀ degeneracy; no re-fit is done, and none can recover θ* from r_s = 0.
- **(d) BAO:** each DESI DR1 number, at Planck 2018 distances, implies an r_d; the inverse-variance mean and its pull from 0 are printed. A literal R1 has no BAO feature at all.
- **(e) Neutrino background:** N_eff = 0 (neutrinos decouple at T ≈ 1 MeV, z ≈ 6 × 10⁹, before z*) against 2.99 ± 0.17.
- **(f) Blackbody (reported, not a pull):** FIRAS |μ| < 9 × 10⁻⁵, |y| < 1.5 × 10⁻⁵ (memory, UNVERIFIED). A blackbody is compatible with R1-om (made in equilibrium) and does not by itself separate R1-lit from R1-om; the acoustic phases and the super-horizon TE correlation (memory, UNVERIFIED) do.
- **G1 class per test:** CONTRADICTS if |pull| ≥ 5; TENSION 3–5; CONSISTENT < 3. **R1-lit FAILS G1** if any repo-number test CONTRADICTS.

### 4.2 R2a (G1, G2, G3, G5)
- **(a) Expansion history (G2).** Compressed likelihood = CHW 2019 distance priors (R, l_A, ω_b, n_s, with correlations, their own definitions as in XR26) + the 12 DESI DR1 BAO numbers (diagonal; the DM–DH correlations are ignored, as in CFG4; disclosed). r_d from a CAMB spline in (ω_b, ω_c), m_ν = 0.06 eV, N_eff = 3.046. Free: ω_b, ω_c, h, n_s (profiled, Nelder–Mead). **SN are not in the repo outside the DESI chains and are not scored** (they matter most for low z_c; disclosed).
  - z_c grid: {0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10, 30, 100, 1090}.
  - Step: Δχ²(A) = χ²_min(A) − χ²_min(0) on A ∈ {0, 0.1, …, 1.0}; **A₉₅(z_c)** = the A where Δχ² = 2.71 (one-sided 95%, A ≥ 0), by root-finding between grid points; 1 if never reached.
  - Pulse: B ∈ {0, 0.1, 0.2, 0.5, 1, 2, 5} for z_c ≤ 10; **B₉₅(z_c)** the same way (5 if never reached).
  - **G2 class at A = 1 (step) and B = 5 (pulse):** EXCLUDED if Δχ² ≥ 9; TENSION 4–9; ALLOWED < 4; NON-DIAGNOSTIC if Δχ² < 1.
  - Reported: H(z)/H_ΛCDM(z) at the profiled best fit for A = 1 and A = A₉₅ at z ∈ {0.5, 1, 2, 3, 5, 10}; the ΛCDM onset of acceleration z_acc (q = 0).
- **(b) The framework's a₀ (G3, theory).** On the canonical tie a₀ = κc√(Gρ_DE): step ⇒ a₀(z > z_c)/a₀(0) = √(1 − A); pulse ⇒ √([1 + Bg(z)]/[1 + Bg(0)]). Printed at z ∈ {0.85, 1.5, 2.5, 5} for A = 1 and A₉₅ (step), B₉₅ (pulse). a₀(0) is unchanged on both footings (ρ_DE0 and ρ_total today are fixed). On the alt footing (ρ_total) a₀ ∝ H(z) is the rival law in every reading; noted, not re-scored. **Keeps flat** if |log₁₀ a₀(z)/a₀(0)| ≤ 0.05 dex at every z ≤ 5.
- **(b′) The data (G3, data).** Each law F(z) = a₀(z)/a₀(0) is run through the CFG222 machinery on six rows: RC100 committed (slope of δ on z), CRISTAL R_e fit route (n = 12), R_e independent (six), R_out fit (six), R_out independent (six). Primary cell ν_mono canonical (verdict CONSISTENT / DISFAVOURED-over / DISFAVOURED-under from the bootstrap 95% CI, as CFG222); the other three cells' z(own) reported. F = 0 is represented by F = 10⁻⁹ (Newtonian limit).
  - Laws run: STEP(z_c, A) for z_c ∈ {0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0} at A = 1 and at A = A₉₅(z_c) (if > 0.01); PULSE(z_c, B₉₅) for z_c ∈ {1, 2, 3, 5}; R2b-const(w) for the four w; FLAT and H(z) as references.
  - **G3-data class per law:** SAME-AS-FLAT if F ≡ 1 over every row's redshifts; otherwise, against flat's verdict on the same row: WORSE-THAN-FLAT-ROBUST if the law is DISFAVOURED on both routes at the same radius (R_e fit + R_e independent, or R_out fit + R_out independent) where flat is not DISFAVOURED on both; WORSE-THAN-FLAT-ROUTE-DEPENDENT if DISFAVOURED on any row where flat is CONSISTENT, or on a row where flat is DISFAVOURED in the same direction with a larger |median|/|slope|; NOT-WORSE otherwise. Every row inherits its gas route's caveat.
- **(c) R2a-rec: the amount.** Menu of recombination-era energy densities, each compared with ρ_Λc² (canonical footing) and ρ_crit c² (alt footing):
  - **E2 (PRIMARY):** the hydrogen binding energy released over the recombination history, ∫ 13.598 eV × n_H(z) × (−dx_H/dz) dz, n_H(z) = n_H0 (1 + z)³, x_H = min(x_e, 1) from CAMB (z ≤ 1800). A w = −1 bath keeps each injection undiluted, so this is the reading's own amount.
  - E1: 13.598 eV × n_H(z*) (instantaneous at z*).
  - E3: E2 plus helium (24.587 eV and 54.418 eV per He, released where CAMB's x_e − 1 falls through (f_He, 2f_He] and (0, f_He]).
  - E4: 10.199 eV (Lyman-α) × n_H(z*).
  - E5: the gas thermal energy (3/2)(n_H + n_He + x_e n_H) k T(z*).
  - E6: the photon energy density at z*.
  - E7: ρ_b(z*) c².
  - E8: ρ_m(z*) c².
  - **Look-elsewhere:** the number of menu items within a factor 2 of ρ_Λc²; with K = the number of physically distinct items (E1/E2/E4 count as one) and a log-uniform prior over the menu's own span, the chance that at least one lands within ×2 is 1 − (1 − log₁₀4/span)^K. Printed.
  - **Grade:** capped at **p\*** (POST-HOC-FLAGGED, §0) whatever the ratio. It cannot pass G5.
- **(d) R2a-rec: consequences that are not the amount.**
  - Distances: the step at z_c = 1090 with A = 1 is scored in (a); expected NON-DIAGNOSTIC.
  - The recombination radiation: in standard physics the binding energy ends in photons (the cosmological recombination lines). If it goes into the vacuum instead, those photons are missing. The fraction E2/ρ_γ(z*) is printed; the predicted line amplitude (memory, UNVERIFIED: of order 10⁻⁹ of the CMB) is far below FIRAS. **UNTESTABLE with present data; a genuine prediction for future spectral-distortion experiments.**
  - Kinetics, **fast-sink limit (reported, not load-bearing):** if the vacuum takes the energy directly instead of a photon, the Lyman-α / ground-state bottleneck disappears and x_e tracks Saha. The Saha x_e = 0.5 redshift vs CAMB's is printed, and the implied θ* shift at fixed parameters (z* scaled by the same (1 + z) ratio). The slow-sink version (photons emitted, then absorbed by the vacuum) leaves the kinetics standard and is not computed.

### 4.3 R2b (G2, G3)
- From the three committed DESI DR2 chains (CPL, weighted): f_mono = the weight with w0 ≤ −1 and w0 + wa × 2.5/3.5 ≤ −1 (w ≤ −1 for all z ∈ [0, 2.5]); p(w0 ≤ −1); the crossing fraction and median z_cross (control against CFG195).
- **G2 class for R2b-mono:** EXCLUDED if f_mono < 0.0027 in all three chains; TENSION if < 0.05 in all three; else ALLOWED. R2b-const(w) inherits R2b-mono's class (it is a member).
- R2b-leak: CONSISTENT with the chains' shape by construction and **NON-DIAGNOSTIC** (the shape is the CPL fits' own, a restatement); it needs a phantom epoch (NEC violation, CFG176/CFG195).
- a₀(z)/a₀(0) = (1 + z)^{3(1+w)/2} for R2b-const, printed at z ∈ {0.85, 1.5, 2.5, 5}; G3 as in 4.2(b, b′).

### 4.4 R3 (G4)
- The repo holds no CMB map. **CMB disc features and large-angle anomalies: NOT TESTED BY THE REPO**; literature (memory, UNVERIFIED): Feeney, Johnson, Mortlock & Peiris 2011 (PRL 107, 071301; PRD 84, 043507) searched WMAP 7-year for collision discs, flagged four candidate features, and found the evidence did not favour collisions (a bound on the expected number of observable collisions of order 1.6 at 68%); follow-ups (Feeney et al. 2013 with polarisation forecasts; Osborne, Senatore & Smith 2013 on WMAP 9-year; the Planck isotropy papers 2013 XXIII, 2015 XVI, 2018 VII) report no detection; the known large-angle anomalies (low quadrupole, hemispherical power asymmetry, the cold spot) sit at about 2–3σ with look-elsewhere caveats.
- **The a₀ dipole:** with a₀ ∝ √ρ_DE, a local DE contrast ε across the SPARC volume gives an a₀ dipole D ≈ ε/2. A₉₅ = 0.43 ⇒ ε < 0.86 locally. A horizon-scale gradient of total contrast ε over L = D_M(z*) gives D ≈ (ε/2)(d/L) at the SPARC depth d (the largest SPARC distance, read from the table). The ε needed to reach A₉₅ is printed. **NON-DIAGNOSTIC** if it exceeds 1.
- Isotropic readings (R1, R2a, R2b) pass G4 **by construction** (enforced by the premise; reported, not scored).

### 4.5 G5, constants count
Baseline: the framework's κ (FITTED) and ρ_Λ (a measured input), plus the ΛCDM parameters. Declared counts of added constants: R1: 0 (and it deletes the early universe); R2a-step: +2 (z_c, A); R2a-pulse: +2 (z_c, B) plus a declared shape; R2a-rec: 0 added, and ρ_Λ would become derived (−1) **only if** a reading with a mechanism fixed the amount before seeing it (it did not: p\*); R2b-mono: ≥ +1 (the drive rate); R2b-const: +1 (w); R3: ≥ +4 (two direction angles, angular radius, amplitude; plus the collision time). **G5 PASS** only for ≤ 0 added with no post-hoc element.

## 5. Checks in the script

- **Controls (must pass in both modes):**
  - C0: κ = ½ with H₀ = 67.4, Ω_Λ = 0.6847 reproduces FP0's canonical a₀ (to 1e-4) and alt a₀ (κ√(1/Ω_Λ), to 1e-4).
  - C1: CAMB at the Planck 2018 best fit reproduces XR26's committed r_drag, 100θ*, z* (to 0.02 Mpc, 1e-5, 0.01).
  - C2: this lane's CHW implementation gives XR26's committed χ² = 1.6641 at the Planck point (to 1e-3).
  - C3: the BAO list and the CHW means/errors/correlations parsed from CFG4 and XR26 equal the lane's copies exactly.
  - C4: the r_d spline agrees with CAMB directly at five off-grid points to 2e-4 relative, and r_d changes by < 1e-4 relative for h ± 0.05.
  - C5: the fast integrator agrees with scipy quad for D_M(z*), r_s(z*) and D_M at a BAO redshift, with and without a step at z_c = 1.5, to 1e-7 relative.
  - C6: the chains reproduce CFG195's crossing fractions and median z_cross (to 1e-6, the same definitions) and p(w0 < −1).
  - C7: the exec'd CFG222 machinery reproduces CFG222's committed FLAT and H(z) primary-cell statistics (all six rows) to 1e-9.
- **Load-bearing:**
  - L1: the contact bites: some R2a grid point changes E(z) by more than 10⁻³ at some z ≤ z*.
  - L2: R1-lit contradicts the measured θ* at ≥ 5σ.
  - L3: ΛCDM is recovered exactly at zero amplitude: A = 0, B = 0 and w = −1 give Δχ² = 0 (to 1e-9) and a₀(z)/a₀(0) = 1 exactly.
- **MUTATE=1** sets every contact amplitude to zero (A = 0, B = 0, w = −1 in every R2 evaluation) and restores the full past in R1 (z_start → ∞). Required: L1 and L2 FAIL (rc = 1); L3 holds for **every** grid point; the G3 laws all read SAME-AS-FLAT. Outputs are separate: `CFG254_handcheck_MUTATE.out` and `CFG254_handcheck_results_MUTATE.json` (main: `CFG254_handcheck.out`, `CFG254_handcheck_results.json`). The headline line differs between the modes.

## 6. Classes per reading, labels and the restatement rule

- **CONTRADICTED:** fails G1 or G2 on repo numbers (CONTRADICTS at ≥ 5σ, or EXCLUDED).
- **CONSTRAINED:** allowed only inside a bounded region (A₉₅, B₉₅, or a z_c range); the bound is the result.
- **NON-DIAGNOSTIC:** allowed, and the repo's data cannot tell it from ΛCDM with flat a₀.
- **UNTESTABLE-AS-STATED:** predicts nothing specific; the minimal specification that would make it testable is named.
- **p\*:** a post-hoc numerical coincidence; never a pass.

**Restatement is not a pass.** A reading that passes a gate only because it is ΛCDM (plus the flat a₀ law) at every epoch the gate sees — zero amplitude, a contact hidden where nothing is measured, or a universe "created as if" it had a past — has shown compatibility, not support. No reading in this lane can be graded as supported.

## 7. What a phase 2 would need (not done here)

1. Verify every (memory, UNVERIFIED) item against the papers; correct this file only by an appended addendum.
2. A real SN likelihood for low-z_c steps, and DESI DR2 BAO with correlations.
3. For R2a-rec: a modified recombination code (energy sink in the three-level atom) and the Planck likelihood, to replace the fast-sink illustration.
4. For R3: a specified collision (direction, angular radius, amplitude, time) confronted with the Planck maps through the Feeney et al. template pipeline.
