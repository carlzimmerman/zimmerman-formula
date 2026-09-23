# BH* week — audit, door swing, and the one live framework test (2026-09-22)

Scope: every "black hole star" (BH*) result committed 2026-09-17..22 (waves G–U, Lean I01–I13,
CFJC RFC-0001, opus_49 doors A/B), audited on the framework's own terms, then every open door
swung that the world currently lets swing. Lanes: `L323`, `L324`, `L325` (this directory).
Lean: `fable_independent_2026/lean_2026/I17_bhstar_audit.lean` (8 theorems) and
`I18_qso1_naked_bh.lean` (16 theorems) — both exit 0, zero `sorry`, axioms
{propext, Classical.choice, Quot.sound}.

## 1. Bottom line

* **No Kepler-grade breakthrough this week.** The campaign's one framework-facing result, the
  "regime coincidence" g_B/a0(ρ_gas) = 1.00, is not a framework result (L323, I17). The rest is
  correct textbook stellar physics: the Eddington quartic, Γ₁(β), and L/L_Edd from log g.
* **One new, live, zero-parameter framework test surfaced:** A2744-QSO1, a naked black hole
  weighed dynamically at z = 7.04 (L324, I18). It gives a direct bound on a0 at z = 7.04, and it
  **cuts both ways**:
  - At the paper's headline mass (10^7.7) the flat framework passes.
  - At the low end of the published range (10^6.9) the flat framework **fails**.
  - The a0 ∝ H(z) rival fails at every published mass (0.9–2.0σ at the headline mass).
  - Mass-reading-limited; ΛCDM is not discriminated.

## 2. The new test: the naked-black-hole rotation law (L324 7/7; MUTATE fails K3, K4, K4d, K6)

For a point mass M weighed at small radius, the framework's rotation law has no free parameter:
v_c² = (GM/r)·ν(y), with y = (r_M/r)², r_M = √(GM/a0), and v_flat⁴ = GMa0.

**Under the RAR kernel the phantom fraction is exactly e^{−r_M/r}**
(`phantom_fraction_rar`, `sqrt_y_point_mass`). So "any extended component is sub-dominant at r"
is equivalent to **a0 < GM/(r ln 2)²** (`subdominant_iff_a0_bound`).

Juodžbalis+26 (Nature 2026, arXiv:2508.21748; **published-version numbers**, PMC13215880) find:
* Keplerian rotation of narrow Hα with log M = 7.7 ± 0.3 at i = 52° (MOKA3D, which models the PSF).
* Inclination-corrected spectroastrometric masses of 6.9–7.2.
* A 1-D fit with bins at 100 and 150 pc giving log M sin²i = 6.75 ± 0.15 (a lower limit).
* NFW, NSC and Plummer components all collapse to a point: "any extended mass component is
  sub-dominant at the < 200 pc scales probed".

*(This lane's first commit used arXiv v1: a low mass of 7.2 ± 0.15, bins at 50/100/150 pc. It is
corrected here to the published version.)*

The a0 bound in pass/fail terms (canonical / alt footing; the rival is a0·E(7.04) = 12.84 a0):

| mass reading | 150 pc (outermost bin) | 200 pc (narrow-Hα extent) |
|---|---|---|
| MOKA3D 10^7.7 (headline) | framework **pass** (f_ph 0.16 / 0.19); rival **fail** | framework **pass** (0.26 / 0.29); rival **fail** |
| spectroastrometric 10^7.2 | framework pass (0.36 / 0.39) | framework pass / **edge** (0.46 / 0.497) |
| spectroastrometric 10^6.9 | framework canonical pass (0.48) / alt **FAIL** (0.52) | framework **FAIL** on both (0.58 / 0.61) |
| mass the framework needs | log M > 6.86 / 6.94 | log M > 7.11 / 7.19 |
| mass the rival needs | log M > 7.97 / 8.05 (+0.9 / +1.2σ on 7.7) | log M > 8.22 / 8.30 (+1.7 / +2.0σ) |

Lean-certified (I18, 16 theorems):
* The pass at M = 5.01e7 and the rival's fail at 5.02e7: `framework_passes_150/200` and
  `rival_fails_150/200`.
* **The deficit** at M ≤ 1e7 and M ≤ 7.95e6: `framework_fails_200_low` and `alt_fails_150_low`,
  with `canonical_passes_150_low`.

**Honest scope:**
* "Sub-dominant" is qualitative, and the paper's extended-mass fits used NFW, NSC and Plummer
  shapes, not the MOND phantom profile. Reading it as f_ph < ½ is interpretive.
* Which published mass is right decides the framework's verdict. MOKA3D models the PSF and
  inclination; the low readings come from spectroastrometry.
* ΛCDM is not discriminated, because a small halo passes.

**Registered prediction** (L324 K6), for the ratio v_c/v_Kepler of the weighed inner mass:

| radius | framework | Newton | rival |
|---|---|---|---|
| 300 pc | 1.08–2.03 | 1.00 | 1.75–3.66 |
| 375 pc | 1.15–2.24 | 1.00 | 1.94–4.08 |
| 1 kpc | 1.70–3.54 | 1.00 | 3.09–6.59 |

These bands cover log M 6.75–8.0 (every published reading at 1σ), both footings and three
kernels. Across that full range the framework and rival bands overlap. At any fixed weighed mass
the rival sits ≥ 1.50× above the framework at 375 pc, so the refit must fit M jointly.

**Decisive next step — the data are public:** Zenodo 19402518 (narrow-Hα cube, 86 MB; full cube
6.4 GB). BlackTHUNDER is JWST PID 5015. MOKA3D is public (github cosimomarconcini/moka_3d). The
lens model is the public UNCOVER A2744 model. Refit jointly (M, i, law) with
v_c = √(GM/r)/√(1 − e^{−r_M/r}). The law adds no parameter beyond Kepler's. Then measure the
outflow-separated narrow-line rotation at 300–450 pc.

## 3. The audit of the week (L323 9/9; MUTATE p = 5 fails R3; Lean I17)

* **The regime coincidence is not a framework result.**
  - a0(ρ) is evaluated at the gas's own density. The framework's law is flat, a0 = κc√(Gρ_DE),
    and the local-density branch is excluded as an environmental law on SPARC (13σ internal,
    ~34σ kNN, 6.8σ 2M++).
  - The ratio is exactly 2(v_c/c)(t_ff/t_dyn) (`ratio_is_freefall_kinematics`): 1.00 =
    2 × 9.9e-4 × 504. It is a kinematic number of the envelope.
  - A crossing exists and is unique in every ρ ∝ r^−p envelope with p < 4
    (`unique_crossing`, `crossing_antitone`), so its existence is not a finding.
  - The chance that the crossing lands within ×2 of the Balmer layer is P = 0.31.
  - Propagated from the campaign's own input ranges, the honest error bar is ±0.47 dex, not
    "±0.02".
  - The same classifier labels the air at the Earth's surface "strong-a0" (g/a0(ρ) = 0.0073;
    `lab_air_strong_a0`).
* **KP1** is equivalent to its defining transition (`kp1_iff_transition`; I11 proved only →),
  so it carries no content beyond the definition.
* **KP2's M^{1/4}** follows from the published family scaling alone (`kp2_from_family`).
* **The framework's own prediction for BH* envelopes is a null.** Every layer sits at
  ≥ 5.6e5 a0 (flat, both footings).
* **Wave U** ("Γ 13% above the cap") is inside the log g error. It flips sign at solar
  composition: 56.6 at κ_es = 0.40, 48.1 at 0.34 (`gamma_solar_composition`). The identity is
  L/L_Edd with M taken from log g, not a new observable.

**Lean audit of I01–I13** (independent pass, all 13 compile clean):
* Most load-bearing theorems are substitution identities.
* No file imports another, so every "via I0x" link is a hand-copied hypothesis.
* I04 `kappa_min_tabulated` is vacuous: the hypothesis restates the conclusion.

Docstring-vs-theorem corrections, recorded here and not edited in place:
* **I10:** 9.47e6 × 1e-4 = 947 < 1e3. The theorem proves only 1e2 (`void_threshold_corrected`).
* **I05 and bhstar_m1:** "~500×" should read ~5×10⁵×.
* **I01:** two of the three R_crit/r_M values are inverted. They are √11/5, √5/2 and √3, not
  √11/5, 2/√5 and 1/√3.
* **I02:** the header's inequality direction is reversed relative to `S5_bound`.
* **I04:** "GR-unstable via ceiling_unstable" is not in Lean, and it conflicts with I06 without
  a retraction.
* **I09:** it mixes two timescales that differ by √2.
* **I11:** "zero free parameters" overstates it, because κ = ½ (fitted) enters through c/2.
  5.01e68 m assumes μ = 1.4.
* **I12:** κ_es = 0.40 (pure H) is unstated.
* **bhstar scripts:** C = 2.99772458e8 is a digit typo (7e-5 relative; no result changes).

## 4. Door swing (every open door; "swings are cheap, keys are not")

| door | swung how | result |
|---|---|---|
| D-N7 r_B reverberation | literature to Sept 2026 | **Shut.** No firm lag for any LRD. TWINKLE (18 LRDs) and NEXUS (17) find no variability. Ji+25's "≳ 45 ld" is ≈ 34 ld from its own "9 light-months/(1+z)", so the 40.9 ld KP1 value is not below it. KP1 has no framework content anyway (§3). |
| KP2 / KP3 / R-F3 per object | public data (L325) | **KP2 undecided.** Slope 0.32 ± 0.12 (N = 11): ¼ is within 1σ, ½ is 1.5σ away. The ×1.68 clustering clause **fails** (velocities spread ×7.8). **KP3 cannot run**: no per-object n_H is published. **R-F3:** the [36, 90] range is too narrow; stacks span 30–123, and the one per-object fit (the Egg) gives 226. |
| D-YM4 MESA / pulsational ceiling | profile search | **Shut.** Accreting-SMS profiles (Saio/Nandal GENEC, Herrington MESA) are "on request" only, and MESA is not installed. Saio+24 gives the structural reason n = 3 lands at 6.6e7: accreting SMS have extended outer layers. Their Table 1 gives M_GRI 0.82–10.6 × 10⁵ Msun over Ṁ 0.05–1000 Msun/yr. |
| D-YM1 X_d constant | lawful-source search | **Unlock re-specified.** Bravyi–DiVincenzo–Loss, CMP 284 (2008) 481, arXiv:0707.1894 (open) says Yarotsky 2004 never stated ε₀ explicitly. BDL re-derive it with tracked constants (2⁻¹⁷Δ/(dJ), two-body qubits). The key is extending that derivation to four-body plaquettes on L²(SU(N)) links, which is swarm-addressable. The JMP paper is not the key. |
| D-YM2 / D-N5 Clay walls | — | Not swung: no data or constant moves them. |
| D-YM3 / D-N6 | — | Killed with proof; reopening needs a new action or coupling premise. |
