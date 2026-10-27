# X61_switch_at_high_z — FROZEN CRITERIA (committed alone with the ledger, before any script or number of this lane)

Written 2026-10-27, at the owner's request: test the object-keyed switch (X58) at z ≈ 1–2.5, where the crossover mass
should move, against the record's own high-z kinematics.

Standing rules: κ = ½ FITTED. Footings (canonical a₀ 9.3603e-11, alt 1.1312e-10 m/s²) never pooled. Cold dark energy is
the gravitating w ≈ 0 clumping component of dark energy; it is not matter and not a particle. Framework-native only: no
ΛCDM number enters a rule (EM1's M200(M_b) carries a disclosed ΛCDM concentration relation, ledger A6). No fitting.
Not "theory closed". Nothing here may say the data favour the framework.

## 0. What is tested

**The switch (X58, frozen 9964127dfd, hypothesis SW).** Per bound system with halo mass M200:

    above (η Σ_coll(M200, z) > Σ_a₀(z)):  g = g_N[ρ_b + ρ_E]       route E, Newtonian, X43 collapse-cored Burkert halo
    below:                                 g = ν(g_b / a₀(z)) g_b   the law on the baryons alone, no halo

Each object is on ONE branch at ALL radii (the flag is keyed on the object's M200, not on radius). X58 is still running;
only its committed criteria are cited. The owner's phrase "law plus a cold-dark-energy core" for the above branch is read
as X58 defines it: in route E the law is emergent from the a₀ floor and the core adds to it; the force law is Newtonian.

**The crossover at redshift z.** M_×(z) solves η Σ_coll(M, z) = Σ_a₀(z), with
- η = (4/(3B(1))) c_f^{5/4} = 14.83, c_f = 4 (X43, EXTERNAL, unchanged);
- Σ_a₀(z) = a₀ F(z) / (2πG);
- F(z) = the record's M-DEC curve √ρ_DE(z)/ρ_DE(0) with (w₀, w_a) = (−0.838, −0.62) (CFG223/CFG227 `R_dec`) **primary**;
  F ≡ 1 (flat) **variant**;
- Σ_coll(M, z) = Δ ρ_m(z_f) r_f, Δ = 18π², for the half-mass progenitor (X41's convention, unchanged), with the Lacey–Cole
  median formation epoch generalised from z_obs = 0 to the observation epoch:

      δ_c / D(z_f) = δ_c / D(z_obs) + ω̃ S^{1/2},   S = σ²(M/2) − σ²(M),   δ_c = 1.686, ω̃ = 0.974

  At z_obs = 0 this is X41/X43's equation exactly. σ(M) and D(z) are EM1's CLASS backgrounds (bg A primary, bg B reported).

**Hand estimate (HE1, before any script).** Σ_coll ∝ (1 + z_f)² M^{1/3} rises steeply with z_obs while F(z) under M-DEC
falls slightly, so M_× should drop from 10^12.1 (z = 0) to roughly 10^10–10^10.5 by z ≈ 1.5. If so, nearly every high-z
disc in the record lies ABOVE M_×(z_gal) and the below subgroup is empty or tiny. Kept as it falls.

## 1. Predictions (frozen form; the numbers come from the script)

P1. **M_×(z)** at z = 0, 1, 1.5, 2, 2.5, both footings, F = M-DEC (primary) and F = 1 (variant), bg A (bg B reported).

P2. **Per galaxy flag**, above ⇔ M200 > M_×(z_gal) on that footing, for every galaxy in the samples below.
- Halo mass: no high-z lane in the record estimates a halo mass, so for every galaxy **M200 = EM1 R1 (bg A):
  log M200 = 11.18 + 0.90 (log M_b − 10)**. This is a z = 0 relation applied at high z: APPROXIMATE (ledger A5, A6).
- M_b per sample:
  - **KURVS** (CFG140/141, 10 rotation-supported discs, z 1.33–1.61): M_b = M★ (1 + μ), μ = 0.67 central (the paper's 40 %
    molecular), flag robustness over CFG140's bracket μ ∈ {0.25, 0.67, 1.5, 4} and δ M★ ∈ {−0.2, 0, +0.2} dex.
  - **KMOS3D** (CFG99, clean discs, windows LOW 0.6–1.1, MID 1.1–1.9, HIGH ≥ 1.9): M_b = the lane's `Mbar` column (SED M★ +
    Tacconi gas).
  - **SINS/zC-SINF AO** (CFG280, 38 rows, z 1.45–2.52; tier T2 = 18): M_b = M★ (stars only, Table 1): a LOWER bound on M200.
  - **RC100 at z ≥ 2** (CFG227 S4, 41, class D): M_b(< R_e) = (1 − f_DM) V_c² R_e / G from the authors' table: a lower bound.

P3. **Predicted outer behaviour.**
- Below M_×: Δ_pred = 0 (law on baryons with a₀ F(z_gal); no halo; at all radii).
- Above M_×: Δ_pred,i = log₁₀{ G[M_b(<R) + M_E(<R)]/R² / [ν(g_b/(a₀F)) g_b] } at the galaxy's measured radius R, with the
  baryons exactly as the source lane models them, and M_E a Burkert halo at Σ_core = max(Σ_a₀(z), η Σ_coll(M200, z)) holding
  M200 inside R200(z) = [3 M200 / (4π · 200 ρ_crit(z))]^{1/3} (ρ_crit(z) from bg A's CLASS H(z)); X43's solver (compact root,
  saturation counted). The excess Δ_pred > 0 is the switch's high-z signature.

## 2. The statistic (graded on KURVS only; the other samples cannot carry a g_obs statistic, see §4)

- **Observable:** CFG140/141's per-galaxy Δ_L = log₁₀ g_obs − log₁₀[ν(g_bar/(a₀F(z))) g_bar] at R_max (the outermost
  Hα radius, 4–7 R_d), with the record's pipeline exec'd read-only (thin exponential discs, spherical surrogate, CFG140's
  per-object errors). **Primary cell:** P2 (CFG141's measured outer σ), μ = 0.67, δ = 0, F = M-DEC, anchor-corrected by
  CFG140's SPARC z = 0 anchor at the same pressure model, δ and footing (Δ' = Δ − anchor).
- **Subgroups:** A (above M_×(z_gal)) and B (below), by the P2 flag at the same μ, δ, footing.
- **Pooling:** CFG140's `pooled` (inverse variance, Birge-inflated). Residual r_i = Δ'_i − Δ_pred,i.
- **Power (printed first, before any g_obs):** N_A, N_B; σ_diff = √(σ_A² + σ_B²) from the per-object errors; expected
  separation S = (⟨Δ_pred⟩_A − 0) / σ_diff.

## 3. Verdict classes (per footing; primary cell; bg A)

- **NOT DIAGNOSTIC** if N_A < 3 or N_B < 3, or S < 2. The power (N_A, N_B, S) is quoted.
- Otherwise, with D = Δ'_A − Δ'_B (pooled) and its σ_D:
  - **SWITCH PREDICTION SUPPORTED** if D ≥ 2σ_D, |Δ'_B| < 2σ_B, and |⟨r⟩_A| < 2σ_A.
  - **CONTRADICTED** if any of: Δ'_B ≥ 2σ_B (the no-halo subgroup shows an excess); D − ⟨Δ_pred⟩_A ≤ −2σ_D (the
    above subgroup falls short of its predicted excess); D ≤ −2σ_D (the pattern is reversed).
  - **UNDECIDED** otherwise.
- If the footings disagree, the verdict is **UNDECIDED**.

## 4. Reported only (no verdict)

- **R1 above-only reading (KURVS).** If B is empty, the A subgroup alone is compared with route E (Δ_pred) and with the law
  alone (0): pooled r_A and Δ'_A with σ, over P0 / P1 / P2 × μ grid × δ × footing × F. Per cell: route E within 2σ?
  law-only within 2σ? Counted, not graded (pressure support and unmeasured gas are CFG140/141's named walls).
- **R2 counts** on each side of M_×(z_gal) for KMOS3D (LOW / MID / HIGH clean), SINS-AO (T0 / T2), RC100 z ≥ 2, KURVS.
- **R3 descriptive subgroup medians** where the record has a per-galaxy statistic: SINS-AO δ_FLAT (stars only, an upper
  bound) and D; RC100 f_DM(< R_e) (class D). No grade.
- **R4 variants:** F = 1; bg B; M200 ± 0.3 dex (flag robustness).
- **R5 future samples:** what KURVS-like, JWST and the ALMA windows (CFG806 / CFG809) would need to test the split: the
  mass where M_×(z) falls at z 1–2.5, how many galaxies below it, at CFG385's per-galaxy precision.

## 5. Step 0 (stop rule: any failure → STOPPED, no verdict)

Reproduce from committed outputs:
- (a) CFG140 per-galaxy P1 central Δ_flat (printed in `CFG140_kurvs_a0z.out`) to 0.006 and the committed central `df`
  0.3983 to 1e-9; (b) CFG141 P2 central `df` (0.67|0.0|canonical) to 1e-9 and the per-galaxy README Δ_flat to 0.006;
- (c) CFG99: 74 clean HIGH discs; N(g_bar < a₀ at r_out) = 2 / 3 (canonical / alt) from `cfg89_per_object.csv`;
- (d) CFG280: 38 rows, T2 = 18; (e) CFG227 S4 RC100 z ≥ 2: 41 rows;
- (f) X43's crossover at z_obs = 0, F = 1: 10^12.09 / 10^12.43 (to 0.005 dex) and Σ_coll(10^12) = 6.84 (to 0.01).

## 6. Checks (all must pass; the MUTATE twin must fail K1)

- **K0:** step 0 (a)–(f).
- **K1 (switch property):** every galaxy's flag equals an independent recomputation of [M200 > M_×(z_gal)], and its
  Δ_pred equals its branch (0 for B; the route-E value for A) to 1e-12.
- **K2:** generalised EPS: residual of the formation equation < 1e-3 and D(z_f) < D(z_obs) at z_obs = 0, 1, 1.5, 2, 2.5.
- **K3:** Burkert at z: the solved halo returns M200 inside R200(z) to 1e-8 (or is counted saturated).
- **K4:** F(0) = 1 to 1e-15; with F ≡ 1 the law branch reproduces CFG140's flat Δ to 1e-12.
- **K5:** peak RSS < 1 GB; one thread; nice 15.
- **MUTATE (`X61_MUTATE=1`):** every flag inverted (above ↔ below) after the crossover is computed. K1 must FAIL, exit 1.
  Outputs named `_MUTATE`.
