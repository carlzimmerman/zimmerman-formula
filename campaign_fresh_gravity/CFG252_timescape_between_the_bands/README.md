# CFG252 — dark energy as the void–wall expansion difference ("between the bands"): phase-1 hand-check

- **Criteria:** `../CFG252_FROZEN_CRITERIA.md`, written before this lane's script existed. It includes a blindness disclosure (§0): the a₀/(cH₀) coincidence and rough sizes of (b1) and (b2) were known before writing.
- **κ = ½ FITTED, not derived.**
- **Label: NON-DIAGNOSTIC.** This is a consistency hand-check of a premise swap. Every timescape number is **from memory, unverified**. Nothing here says the theory is closed or that any data favour it.
- **Status:** phase 1. Not committed; the orchestrator reviews and commits.

## The idea (neutral wording)

This is the owner's idea, a mutation of door 11. Between the bands of galaxies, read as the walls and filaments of the cosmic web, one feels the dark energy "slip by". Under test: dark energy is not a constant vacuum but **the difference in expansion between voids and walls**.

The closest published family is the timescape model and related backreaction work. Intended citations, from memory and unverified: Wiltshire 2007 (New J. Phys. 9, 377; PRL 99, 251101), Wiltshire 2009 (PRD 80, 123512), and Buchert's averaging formalism.

**Why it bites.** The framework's tie a₀ = κc√(Gρ_Λ) needs a ρ_Λ, and so do ChainCert's certified `a0_numeric` and its `chain.hflat` premise. Under the mutation there is no ρ_Λ. The tie must be re-expressed in the mutation's own quantities, or it fails. Those quantities are:
- the dressed and bare Hubble rates;
- the void fraction f_v;
- the lapse γ̄.

**Record check.** `grep -ril timescape` finds 6 files: 3 scripts and 3 outputs in `real_research/reviews/` (`mi_phantom_artifact_2026`, `mi_phantom_reframings_audit_2026`, `mi_lowz_anchor_sign_2026`). All name timescape only as prior art. No timescape calculation existed before this lane.

## Run

| mode | command | rc | checks | outputs |
|---|---|---|---|---|
| main | `python3 campaign_fresh_gravity/CFG252_timescape_between_the_bands/CFG252_handcheck.py` | 0 | 6/6 | `CFG252_handcheck.out`, `CFG252_handcheck_results.json` |
| MUTATE | `MUTATE=1 python3 …/CFG252_handcheck.py` | 1 | 5/6 (L1 fails as required) | `CFG252_handcheck_MUTATE.out`, `CFG252_handcheck_results_MUTATE.json` |

- Each run takes under a second and writes only in this directory, with no bytecode.
- Two main runs give byte-identical `.out` and `.json`.
- The key numbers were checked by an independent hand pincer: H_v, the a-1 rows, b1, b2 and the c-common slope all agree to the printed digits.
- **Committed inputs, read-only:**
  - FP0's a₀ and H_Λ;
  - the SPARC profile table in `real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.out`;
  - `prep_2026/a0_line/cosmic_web_environment_results.json`;
  - CFG182's A₉₅.
- **Controls:**
  - C0 reproduces FP0 exactly (H₀ 67.40, Ω_Λ 0.6847).
  - C1 re-derives the note's minimum (1.0766e-10) and Δχ²(0.9361e-10) = 63.90.
  - C2 checks 12 tracker identities in sympy (internal consistency only).
  - C3 checks that P-A and P-B reproduce the recalled derived values. This tests memory consistency, not the literature.

## Model and parameters (from memory, unverified)

- **Model:** the timescape tracker solution (criteria §3, T1–T7).
- **Primary set P-A:** f_v0 = 0.695 and dressed H₀ = 61.7 km/s/Mpc. The tracker then gives:
  - H̄₀ = 50.18 (recalled 50.1);
  - γ̄₀ = 1.3475;
  - Ω_M dressed 0.411, bare 0.168;
  - volume-average age 17.50 Gyr.
- **Robustness sweep:** f_v0 from 0.55 to 0.85 and H₀ ∈ {60, 61.7, 64}, 21 cells. Verdicts stay at P-A.

**Candidate rates at z = 0** (km/s/Mpc):

| | rate | value |
|---|---|---|
| H1 | dressed | 61.70 |
| H2 | bare, and every region's own-clock rate | 50.18 |
| H3 | void, volume time | 55.86 |
| H4 | void, timed by wall clocks (= 1.5 H̄ in the tracker) | 75.27 |
| H5 | wall, volume time | 37.24 |

**SPARC bands:**
- **S1 (primary):** the clustered 2σ interval of the per-galaxy-Υ profile likelihood, [9.229e-11, 1.2662e-10].
- **S2 (reported):** [9.595e-11, 1.1937e-10]. On S2 the canonical footing itself sits at −2.40σ.

## Results by reading (P-A; never pooled)

| reading | a₀ (m/s²) | /a₀_can | S1 | class | sweep |
|---|---|---|---|---|---|
| a-0 literal: no Λ, so Ω_Λ^eq = 0 | 0 | 0 | — | **DIES** | 21/21 |
| a-1 total density × H1 (dressed) | 1.0355e-10 | 1.106 | in | **p\*** (the same value in the homogeneous twin: the a₀/(cH₀) coincidence) | 21/21 p* |
| a-1 × H2 (bare) | 8.422e-11 | 0.900 | out | FAIL | 19 FAIL / 2 PASS |
| **a-1 × H3 (void rate, volume time)** | **9.3755e-11** | **1.002** | in (+1.6% above the lower edge) | **PASS (G-T1 only)** | **11 PASS / 10 FAIL: parameter-dependent** |
| **a-1 × H4 (void rate, wall clocks)** | **1.2633e-10** | **1.350** | in (0.2% below the upper edge) | **PASS (G-T1 only)** | **12 PASS / 9 FAIL: parameter-dependent** |
| a-1 × H5 (wall rate) | 6.250e-11 | 0.668 | out | FAIL | 21/21 FAIL |
| a-2 non-matter share × H1 (1 − Ω_M = 0.589) | 7.948e-11 | 0.849 | out | FAIL | 20 FAIL / 1 PASS |
| a-2 × H2 (Ω̄_k + Ω̄_Q = 0.832) | 7.682e-11 | 0.821 | out | FAIL | 21/21 FAIL |
| a-2 × H3, H4 (void, Ω_M = 0) | same as a-1 × H3, H4 | | | same | same |
| a-2 × H5 (wall, Ω_M = 1 locally) | 0 | 0 | — | **DIES** | 21/21 |
| a-3 borrowed Ω_Λ = 0.6847 × H1 / H3 / H4 | 8.57e-11 / 7.76e-11 / 1.045e-10 | 0.92 / 0.83 / 1.12 | out / out / in | FAIL / FAIL / p* (borrowed) | |
| b1 c²Δ/L (Δ = 0.35–0.50; L = 10–50 Mpc) | 2.0e-8 to 1.5e-7 | 216–1556 | — | **DIES** (+2.3 to +3.2 dex) | |
| b2 c dγ̄/dt (volume / wall time; POST-HOC) | 5.75e-11 / 7.75e-11 | 0.61 / 0.83 | out | FAIL (capped p*) | wall time: 5 of 21 in band |
| c-own (own-clock H = H̄ everywhere) | the H2 rows | | | contrast 0, enforced by the premise (p*); its value FAILs | |
| c-common (common clock: voids × 1.5) | | | | G-T2 below | |
| c-local (the a-2 tie per region) | 0 in walls | | | **DIES** | |

The two PASS values are each reached by both a-1 and a-2. In a void Ω_M = 0, so both give κ′ = ½√(3/8π) = 0.17275.

## Which readings die immediately, and why

- **a-0 (literal).** A universe with no Λ has nothing for the tie to tie to: a₀ = 0.
- **b1 (spatial lapse gradient).** It is 2.3–3.2 dex above a₀. Read as a static lapse, it would accelerate galaxies at void edges by 6×10⁵ to 5×10⁶ km/s per Gyr, above the speed of light, against observed void outflows of a few hundred km/s (from memory). The timescape lapse is a clock rate that accumulates over cosmic time, not a static potential.
- **c-local, and a-2 × H5.** Applied region by region, the non-matter tie gives a₀ = 0 in walls, where the idealised model puts every galaxy.
- **The rest.** a-2 on the global averages (dressed and bare) fails the band low, at 0.82–0.85 a₀_can. The borrowed a-3 rows cannot pass by construction.

## Gates

**G-T1 (value).** Two readings reach PASS on the frozen rules, both total-density ties to the void expansion rate:
- 9.38e-11 in volume time;
- 1.263e-10 timed by wall clocks.

Both sit at the band's edges. Both are **parameter-dependent**: each is in S1 in only about half of the literature sweep, and neither is inside S2 (the volume-time value is 2.3% below S2's lower edge). The dressed-H₀ tie is always in band, but it is the a₀/(cH₀) coincidence: it gives the same 1.0355e-10 in an Einstein–de Sitter universe with no voids.

**G-T2 (environment).**
- **The void-rate ties read globally** (every galaxy reads the cosmic void rate) have no environment dependence by construction. Read locally, they become c-common.
- **c-common predicts a₀ higher in voids** by +0.176 dex, a slope of −0.145 (δ_v = −0.8) or −0.116 (δ_v = −0.9) per dex of 1 + δ.
  - Primary limit, 2M++ clean, N = 52: −0.083 ± 0.135. That gives z = −0.46 (and −0.24): **CONSISTENT, UNDERPOWERED**.
  - Secondary limit, 2MRS clean, N = 38: +0.029 ± 0.075. That gives **TENSION at −2.31σ** at b = 1, δ_v = −0.8, and consistent at −1.9σ or less in the other three cells.
  - The record's clean sample has **0 deep-void galaxies**. About 266 are needed (committed power estimate).
- **The ρ_local exclusion** (13σ SBeff, ~34σ kNN, ~7.5σ Ursa Major; "7–34σ" in the memory note) tests slope **+0.5, a₀ higher in dense regions**. That is the opposite sign, so it is **N/A here**: it does not bear on a void-enhanced a₀.
- **Sky dipole:** a local-H anisotropy of 0.01–0.05 (from memory) against CFG182's A₉₅ = 0.425: consistent, non-diagnostic.

**G-T3 (a₀(z)).** Every reading with a₀ > 0 **rises with z**; none is flat-like. **The premise swap forfeits the framework's distinctive flat a₀(z)** and puts the tie in the rival's class.

| reading | Δlog a₀ at z = 1.5 | rival | Δlog a₀ at z = 5 | rival |
|---|---|---|---|---|
| void-rate PASS rows | +0.53 (volume) / +0.48 (wall clocks) | +0.375 | +1.09 / +1.00 | +0.92 |
| dressed-H₀ tie | +0.41 (rival-like) | +0.375 | | |

- The void-rate rows are steeper than the rival, so both **inherit CFG213's route-dependent disfavour** of a rising a₀ at z ≈ 5. On the fit route the rival already over-predicts the mass discrepancy.
- Timescape's dressed H(z)/H₀ is 2.56 at z = 1.5 against ΛCDM's 2.37, and 7.92 at z = 5 against 8.29.
- **Grade: NOT DECIDED.** No committed high-z result robustly excludes a rising a₀:
  - KURVS: fragile, calibration-bound;
  - CFG213: route-dependent;
  - CFG197: one-sided;
  - CFG196: cannot discriminate;
  - MUSE-DARK: nothing established.

**G-T4 (premise; from memory, unverified; not tested here): PREMISE CONTESTED.**
- **Claimed support:**
  - SN fits: Leith, Ng & Wiltshire 2008; Smale & Wiltshire 2011, sensitive to the light-curve fitter; Dam, Heinesen & Wiltshire 2017 (JLA), roughly indistinguishable from ΛCDM;
  - Pantheon+ analyses (Lane et al. 2025, MNRAS; Seifert et al. 2025, MNRAS Letters) reporting Bayesian evidence for timescape over ΛCDM for some redshift cuts.
- **Tensions:**
  - The dressed H₀ ≈ 61–62 km/s/Mpc is below both the distance ladder (~73) and Planck-ΛCDM (67.4). Timescape attributes local differences to non-linear local expansion (Hubble-flow variance, Wiltshire et al. 2013), which is not established.
  - There is no full perturbation theory. So there is no CMB power spectrum, growth or σ₈ prediction; the CMB is used through the acoustic scale with re-fitted baryon parameters (Nazer & Wiltshire 2015).
  - No DESI DR2 BAO fit is known to this lane (unknown, not absent).
- **Theoretical objections:** Green & Wald 2011/2014 (backreaction cannot mimic dark energy in their framework), disputed by Buchert et al. 2015. Numerical-relativity simulations (Bentivegna & Bruni 2016; Macpherson, Price & Lasky 2019; Adamek et al. 2019) find backreaction on the global expansion at about 10⁻³–10⁻² from ΛCDM-like initial conditions, not order one.

## Reported only (post hoc, not findings)

- **The near-equality a-1 × H3 = 1.002 a₀_can** holds because at P-A the tracker's void rate (55.86) is within 0.2% of ΛCDM's H_Λ = √Ω_Λ H₀ = 55.77 km/s/Mpc. This was noticed after the numbers. It holds at the recalled P-A values only: across the sweep the row spans 0.83–1.20 a₀_can. It is a coincidence of unverified inputs, not a result.
- **The "slip" as a speed.** The differential expansion across a void, (H_v − H_w)R, is 186 km/s at 10 Mpc and 559 km/s at 30 Mpc in volume time (251 and 753 km/s by wall clocks). This is the scale of observed void outflows, so the felt "slip" has a kinematic reading. It is descriptive only.
- **Possible prior art for b2.** In the timescape literature the relative deceleration of regional frames under the "cosmological equivalence principle" has been compared with the MOND scale (from memory, unverified; intended citation Wiltshire 2008, PRD 78, 084032). Phase 2 must check whether b2 is already published.

## Disclosed departures and corrections

1. **Criteria §7, "a-1 is unchanged" under MUTATE,** holds for the H1 (dressed) row only.
   - The H2 and H5 rows move onto H1's value, because in Einstein–de Sitter bare = wall = dressed.
   - The H3 and H4 rows vanish, because there are no voids.
   - The load-bearing requirement (L1 fails, rc = 1) and the change of headline hold as frozen.
2. **Headline wording was corrected after the first runs; no number changed.** The first MUTATE headline said the in-band rows were "identical to the inhomogeneous run's value", which is true for H1 only. The first main headline listed the two PASS values four times (a-1 and a-2 coincide on void rows). Both were reworded, and both modes were re-run; the final outputs are the ones in this directory.
3. **The brief said `grep -ril timescape` finds nothing.** It finds six prior-art mentions and no calculation (see "Record check").

## What phase 2 would need

1. **The data chat verifies every from-memory item** against the papers, and records corrections as an appended addendum to the criteria:
   - T1–T7 and P-A/P-B (especially f_v0, H̄₀, γ̄₀);
   - the recent Pantheon+ fits and their f_v0;
   - the Hubble-flow variance amplitude;
   - timescape's CMB, BAO and DESI status;
   - the b2 prior-art question.
   The two PASS rows sit 1.6% and 0.2% inside the band, so a small correction to f_v0 or H₀ can move either one out.
2. **If a void-rate PASS survives verification,** freeze its a₀(z) confrontation before any number, through the committed high-z pipelines: CFG213's DysmalPy route, CFG197's floor, and the KURVS P4 map. It rises more steeply than a₀ ∝ H(z), so CFG213's z ≈ 5 route bears on it first.
3. **For c-common, obtain deep-void galaxies** with redshift-independent distances. The record has none, and about 266 clean galaxies are needed for 3σ on a slope of this size. The 2MRS −2.3σ cell is the only tension on record and rests on galaxy counts with bias b = 1.
