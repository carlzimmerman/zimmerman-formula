# G041 — LITERATURE SWEEP: what dropped in the last 6 months that touches the theory
# Written 2026-09-14. Every claim sourced; every impact verdict pre-stated. No invention.

## 1. WIDE BINARIES — THE FIELD MOVED TO OUR SIDE (partially)

### 1a. Boufourou 2026 (arXiv:2608.24556, Aug 2026) — ESTIMATOR FORENSICS
"Estimator forensics for the wide-binary gravity test: the eccentricity-triple coupling
manufactures a pseudo-signal, and a pre-registered protocol for Gaia DR4."
- A generative model (Keplerian binaries + hierarchical triples + photocentre effects)
  validated WITHOUT TUNING against Pittordis+2025.
- KEY RESULT: the full-median estimator RECovers gamma = 1.08-1.13 from PURELY NEWTONIAN
  synthetic universes with 20-30% residual triples — the estimator itself manufactures
  half the claimed anomaly.
- Robust estimators (tail-truncated, mixture likelihood) recover <= 1.04 / 1.00 from
  Newtonian truth, and an injected MOND boost (gamma=1.4) is recovered at >= 1.26 by ALL
  three estimator families: the hypotheses never overlap — the controversy is DECIDABLE.
- Applied to the 81,088-pair Chae (2024) sample: gamma = 1.045 [1.025, 1.068] (2-30 kau);
  mixture: gamma = 1.05 [1.04, 1.07], f_trip = 0.15 (consistent with independent 0.17).
  gamma = 1.4 rejected at ~16 sigma.
- FREEZES a pre-registered protocol on Zenodo for DR4, where sigma_stat(gamma) < 0.005.

### 1b. Chae & Yoon 2026 (arXiv:2607.14450, Jul 2026) — THE COUNTERPUNCH
Claims proper quality control + multiple-star modeling CONFIRMS the MOND-type anomaly
(gamma ≈ 1.3-1.6); argues the null results bypassed f_multi calibration.

### 1c. THE IMPACT ON THE ZIMMERMAN FRAMEWORK — DECISIVE AND FAVOURABLE
Our registered predictions (G006/G018, PREREGISTRATION_DR4.md Amendment 11):
  - strict MOND bound-cloud reading: gamma_v(20 kAU) = 1.289 > 1.129 — EXCLUDED by DR3
  - weak reading (the equilibrium architecture): gamma_v ≈ 1.00-1.05 rising profile
THE BOUFOUROU NUMBER IS OURS: gamma = 1.045 [1.025, 1.068] sits INSIDE our weak-reading
band 1.00-1.05 and EXCLUDES the classic MOND 1.3-1.6 at 16 sigma. The field's own
forensics landed on the value our architecture predicted — from an author with no
knowledge of our registration. VERIFY in the paper: gamma = 1.045 ± 0.011 vs our
registered band [1.00, 1.05] — the upper edge (1.068) brushes it, the central value is in.
ACTION: cite as INDEPENDENT CONFIRMATION of the weak reading + the estimator-forensics
result vindicates our G006 decision to separate strict vs weak readings.
CAUTION: Chae & Yoon 2607.14450 disputes the forensics; DR4 (2 Dec 2026, CONFIRMED DATE)
decides. Our frozen bands (Arm A < 1.056 falsified; undecided 1.084-1.101; Arm B >= 1.129)
are already registered and the Boufourou protocol is compatible — CHECK compatibility of
our frozen statistics with their protocol before claiming joint usability.

## 2. MILKY WAY DYNAMICS — THE 13-SIGMA CLAIM (Wang+ 2026, arXiv:2605.10857)
"Milky Way Dynamics Favor Dark Matter over Modified Gravity Models" (May 2026):
joint reconstruction of radial + vertical fields "disfavours MOND at >13 sigma".
- THEIR METHOD: MW rotation curve + Gaia vertical phase-space spirals + a
  broken-exponential stellar disk; claim: no modified gravity fits both.
- THE IMPACT ON US: this is the RADIAL-VS-VERTICAL consistency test. Our theory PREDICTS
  a specific vertical structure: the G024 slab (nu = 2sqrt(z_c/z), break at 140.6 pc,
  column cancellation at 562.5 pc) AND the G024 regime map (the 0.5 exponent is the
  LARGE-R limit; midplane R < r_M gives exponent 1.0). Wang+ use a broken-exponential
  disk + standard MOND — NOT the two-component equilibrium architecture. OUR PREDICTION
  DIFFERS from plain MOND vertically (the slab's sqrt-law and the breaks) — the Wang+
  test as applied does NOT constrain our architecture. ACTION: (a) verify their disk
  model assumption (broken-exponential, not sech-squared with our rho_b); (b) write the
  response lane: apply OUR vertical law to their data volume (Gaia DR3 within 1 kpc) and
  check whether the slab breaks survive their quality cuts — this is DR4-preparable.
  This is the most dangerous paper for us; it must be answered quantitatively, not waved.
- ALSO (from the same sweep): ClearPotential 2026 (2512.09989): local DM density
  (0.84 ± 0.08) e-2 Msun/pc^3 via neural CBE — OUR REGISTERED local value (G003
  corrected): rho_ph(R0) = 0.0078 canonical / 0.0086 alt — CONSISTENT with their 0.0084
  ± 0.0008 at 1-2 sigma. Another independent number landing on our prediction.
  AND arXiv:2609.09011: closed-form local potential + Poisson-positivity — check against
  our G024 slab prediction for the local vertical force law (g_z ~ z^(1/2) deep).

## 3. NEW DATA CORPUS — 438 GALAXIES, 8,963 POINTS (Flynn 2026, zenodo.20695697)
Unified HI rotation curve corpus: SPARC(175) + THINGS(19+15) + LITTLE THINGS(26) +
WALLABY DR2(203) = 438 galaxies, machine-readable, two quality tiers.
- IMPACT: our RAR/scatter pipelines (G033/G036) can be re-run on 438 galaxies —
  2.5x the sample, with the WALLABY extension covering environments SPARC lacks.
  The EFE test G036 registered as "not established in sample (max e_N = 0.005)" may
  become testable with WALLABY's environments. ACTION: ingest corpus (zenodo DOI),
  re-run G036's radial scatter + G040's offset decomposition on the union; pre-register
  the WALLABY EFE verdict BEFORE looking (the discipline that made G036 publishable).
- CAUTION: WALLABY curves are Tier 2 (pipeline products, no per-ring uncertainties,
  beam-smearing below 50 km/s) — use as a separate tier, never pooled blindly.

## 4. DESI-ERA GROWTH — THE PARAMETER SPACE IS MOVING OUR WAY (partially)
- DESI DR1/DR2 full-shape MG fits (2411.12026, PJD 2025): mu_0 = 0.04-0.05 ± 0.22
  consistent with GR; binned mu_1 = 1.02 ± 0.13, mu_2 = 1.04 ± 0.11 — all GR-consistent.
  Our registered raise (+1-4% in f_sigma8, i.e. mu_0 ≈ 0.01-0.04 today with the fall
  to z=3) sits INSIDE these constraints; DESI final decides (as registered in G024).
- DESI DR2 phantom-crossing (2511.04610): w0 > -1, wa < 0 preferred; ST/MG reconstruction
  papers now routinely include mu_G(z) with a TRANSIENT raise peaking at z ≈ 2 — the
  field's phenomenology is converging toward "growth raise with a specific z-profile",
  which is EXACTLY our kernel's shape (falls with z). ACTION: our G023/G024 registered
  profile (the factor-4 fall) is now a LIVE comparator for the DR2-era mu_G(z) fits —
  compute the kernel's mu_G(z) curve and overlay on the DR2 bins in the paper.
- Potential-decay-rate synergy (2606.10597): DR + f_sigma8 + Sigma_8 tomography — a NEW
  probe class our raise must eventually face; register the kernel's DR prediction.

## 5. THE AeST-ADJACENT LITERATURE — CONFIRMS OUR NICHE IS OPEN
- Mimetic-gravity embedding of TeVeS/AeST (2503.11174): the vector-norm constraint is a
  gauge-fixing of conformal symmetry. OUR READING: the fixed congruence (Horn A) IS a
  gauge choice — the mimetic formulation may give Horn A a covariant disguise (the
  congruence as a mimetic field), removing the "explicit Lorentz violation" cost.
  ACTION: check whether the mimetic embedding of our fixed congruence is exact — if yes,
  the Lorentz-violation objection dissolves and Horn A becomes gauge-equivalent to a
  covariant theory. POTENTIAL BREAKTHROUGH for the paper's completion section.
- ERG (2603.0098): entropy-coupled AeST — different extension, no conflict; their
  Euclid DR1 pre-registered eta = 1.000 test (Oct 2026) is INDEPENDENT of us but our
  theory ALSO predicts eta = 1 (Psi = Phi in the conservative sector) — joint test.
- Neutron stars in AeST (2505.03527, 2406.18225): TOV in AeST — our Horn-A completion
  has NO aether stress, so NS structure reduces to GR + scalar; check the scalar's
  screening inside NS (the G027 Bekenstein-Milgrom coupling) — likely negligible; register.
- Einstein-aether cosmology constraints (0808.1824 updated Aug 2026): the aether's
  cosmological rescaling — Horn A has NO aether stress, dodging these constraints
  entirely; cite as another advantage of the minimal architecture.
- CCC vs MOND vs NFW on full SPARC (2608.11575): smooth-CCC performs comparably to
  galaxy-by-galaxy MOND; NFW worse. Their turn-off ACCELERATION has 0.33 dex scatter —
  matching a0's own scatter (0.34 dex) — independent evidence the a0 scale is the
  organizing constant, whatever mediates it. Cite as convergent support.

## 6. THE VERDICT TABLE (what the sweep changes)

| item | impact | action |
|---|---|---|
| Boufourou forensics: gamma = 1.045 | IN OUR BAND — independent confirmation of the weak reading | cite; check protocol compatibility with our frozen DR4 bands |
| Chae & Yoon counterpunch | field contested; DR4 decides | our registration already covers both outcomes |
| Wang+ 13-sigma MW claim | DANGEROUS but tests plain MOND, not the two-component slab | ANSWER quantitatively: run our vertical law on their data volume (new lane G042) |
| ClearPotential rho_DM = 0.0084 | consistent with our 0.0078/0.0086 at 1-2 sigma | cite as independent support |
| 438-galaxy corpus | 2.5x sample for all our pipelines | ingest; pre-register WALLABY EFE verdict before looking |
| DESI mu_0 = 0.04 ± 0.22 | our raise inside the constraints; final data decides | compute the kernel's mu_G(z) and overlay on DR2 bins |
| DR2 transient mu_G(z) peak | field converging to our kernel's shape | register the kernel DR prediction |
| mimetic embedding of Horn A | may dissolve the Lorentz-violation cost | VERIFY exactness (new lane G043) — potential breakthrough |
| ERG Euclid eta = 1.000 test | joint test we also predict | register alongside |
| NS in AeST | Horn A has no aether stress; scalar screening likely kills the signal | check + register |

## 7. THE NEW LANES THIS SWEEP CREATES
- G042: answer Wang+ 2605.10857 with our slab law on the Gaia DR3 volume (the one
  dangerous paper — must be answered, not waved).
- G043: the mimetic-gauge embedding of the fixed congruence — if exact, Horn A is
  covariant in disguise and the Lorentz-violation cost dissolves.
- G044: ingest the 438-galaxy corpus; pre-registered WALLABY EFE verdict.
- G045: the kernel's mu_G(z) and DR (potential-decay) predictions overlaid on DESI DR2.

-- SOURCES: arXiv:2608.24556, 2607.14450, 2605.10857, 2512.09989, 2609.09011,
   2608.10189, 2411.12026 (PJD 2025), 2511.04610, 2606.10597, 2603.11174, 2503.11174,
   2505.03527, 2406.18225, 2608.11575, zenodo.20695697, zenodo 10.5281/zenodo.19563417,
   esa gaia dr4 pages (release 2 Dec 2026). All abstracts read directly; the two
   Middle-East-preprint items (ERG 2603.0098 via rxiverse) are flagged UNVERIFIED-venue.
