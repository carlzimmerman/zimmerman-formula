# CFG512 FROZEN CRITERIA: gravitational waves as tests of the framework

Written and committed alone, before any script for this lane exists. Offline only: on-disk data plus forecasts. Nothing is
downloaded. κ = ½ is FITTED. The cold energy's mass is still required. Not theory closed.

Terminology: "dark energy" (ρ_DE, the background's w0/wa component); "cold energy" (the lumpy, gravitating component,
Ω_c/Ω_b = 5.36, that settles into the law's phantom; the supply per galaxy is a postulate, E2 of CFG500's RECIPE).

The law: a0(z) = κ c √(G ρ_DE(z)), κ = ½ fitted; footings 9.36e-11 (ρ_Λ) / 1.13e-10 (ρ_crit). So
Δlog10 a0(z) ≡ log10 a0(z)/a0(0) = ½ log10 f_DE(z), with CPL f_DE(z) = (1+z)^{3(1+w0+wa)} exp(−3 wa z/(1+z)).
The ratio does not depend on κ or the footing (κ cancels); the absolute level does. Both footings are reported for levels.

## 0. Status words and the DISTINCT / DECISIVE rule (declared before computing)

- A prediction counts as **DISTINCT** only if it differs from ΛCDM's AND from standard MOND's prediction for the same
  observable by more than the 1σ forecast error of a NAMED experiment (σ_exp from this lane's forecast, or from a recalled
  published forecast flagged as such).
- **DECISIVE = Y** only if the difference is ≥ 3 σ_exp from BOTH rivals for that named experiment AND the outcome could
  falsify the framework (a framework kill, not only a rival kill). Otherwise N.
- A test where the framework's prediction equals ΛCDM's (or MOND's) is reported as a CONSISTENCY test (a possible kill of
  a sector, e.g. the chassis), never as support.
- "Standard MOND" = non-relativistic QUMOND/AQUAL with constant a0 and no cold matter; where a relativistic completion is
  needed, AeST (c_T = 1) is the stated comparator and TeVeS/bimetric dark-matter emulators are reported separately.

## 1. Part 1: standard sirens → w0, wa → the framework's a0(z) prediction

**Baseline (current).** The DESI DR2 public chains already on disk (fable_independent_2026/data/desi_dr2_w0wa_thinned/,
CMB + DESI BAO + {Pantheon+, Union3, DESY5}; columns weight, w, wa, omegam; L275). From them: the weighted band of
Δlog10 a0 at z = 0.5, 1, 2.5 (16/50/84) and a Gaussian prior Fisher on (Ωm, w0, wa) from the chain covariance. H0 is not
in the thinned chains, so H0 is FREE in every siren Fisher (conservative). The three SN branches are never pooled.

**Siren scenarios (assumptions recalled from the literature, UNVERIFIED, flagged in every output):**

| id | experiment | events | z distribution | per-event σ_dL/dL |
|---|---|---|---|---|
| S0 | current LVK (GW170817 bright siren) | 1 | z = 0.0098 | 0.14 (inclination-limited) + 200 km/s peculiar velocity |
| S1 | LVK O5-era bright BNS | 30 | uniform in z, 0.02–0.15 | 0.10 + peculiar velocity 200 km/s |
| S2 | LISA massive-BH binaries with EM counterpart (Tamanini et al. 2016-like "mid" yield, 4–5 yr) | 25 | p(z) ∝ z² e^{−z/1.0}, z ≤ 8, deterministic quantiles | instrument 0.02 ⊕ weak lensing σ_lens(z) = 0.066 [(1 − (1+z)^{−0.25})/0.25]^{1.8} (Tamanini 2016 / Hirata 2010 fit, recalled) |
| S3 | Einstein Telescope BNS with GRB/kilonova counterpart (Belgacem et al. 2019-like) | 1000 | p(z) ∝ dV/dz × SFR(z)/(1+z) truncated at z = 2 (Madau-Dickinson SFR, recalled), quantiles | 0.10 × dL(z)/dL(1) (floor 0.01) ⊕ σ_lens(z) |
| S3p | pessimistic ET | 200 | as S3 | as S3 |
| S4 | ET + Cosmic Explorer network, optimistic | 3000 | as S3 but z ≤ 3 | 0.05 × dL(z)/dL(1) (floor 0.01) ⊕ σ_lens(z) |

Redshifts are taken as exact (EM counterpart). Fiducials: each SN branch's chain mean (w0, wa, Ωm), plus ΛCDM
(−1, 0, 0.3111), H0 = 67.7. Fisher parameters (H0, Ωm, w0, wa); for the Ξ forecast (Part 2) also Ξ0 with n = 2.5 fixed.

**Outputs.** σ(Δlog10 a0) at z = 0.5, 1, 2.5 for: chains alone; sirens alone; sirens + chain prior. The rival
a0 ∝ H(z) and flat a0 are tabulated at the same z.

**Part 1 verdict rules (frozen).**
- P1a *sirens improve the prediction*: σ(Δlog a0, z = 2.5) for S3 + prior ≤ ½ × chains-alone σ, on every SN branch.
- P1b *the prediction is cleaner than the galaxy-route measurement*: σ_pred(z = 2.5) ≤ 0.10 dex (one third of the
  ~0.3 dex calibration wall, CFG240/PAPER38) with the CURRENT chains alone. If P1b holds, the siren route does NOT change
  the bottleneck (the measurement is), and that is reported as the finding whatever P1a says.
- P1c *flat vs DE-tracking resolvable by galaxies?*: the DESI-tracking minus flat difference at z = 2.5 vs the 0.3 dex
  wall; resolvable only if |difference| ≥ 3 × 0.3 dex.
- DISTINCT test for the siren route itself: sirens measure w(z), which is the same in ΛCDM-with-w and the framework; the
  route is a distance/expansion test and is NOT counted as a framework test unless combined with a high-z a0 measurement.

## 2. Part 2: d_GW vs d_EM (GW friction) on the record's chassis

- Derivation target: the tensor quadratic action of C-H/K (L340: I_CH + c³/16πG ∫√−g [α_c a·a − c_2 K²], β = 0, so c_T = 1;
  CFG292 T1: (1 − β) λ² = k²) on a flat FRW background with the law OFF on the background (S1, CFG487). Symbolic (sympy)
  with the exact metric diag(−1, a² e^{h}, a² e^{−h}, a²), h = h(t, z), aether/khronon u = ∂_t.
- Ξ(z) = d_GW/d_EM = exp(∫_0^z δ(z')/(1+z') dz'), δ = −½ dln M_T²/dln a, M_T² the coefficient of ḣ².
- **Frozen predictions to check:** (i) M_T² = (1 − β) M_P², constant, so α_M = 0 and Ξ(z) ≡ 1 exactly at β = 0 (and also
  at β ≠ 0); (ii) c_T² = 1/(1 − β) = 1 at β = 0; (iii) no h² mass term; (iv) the MOND sector (filtered a·a) does not enter
  the linear tensor equation on FRW (a = 0), and inside halos its quadratic-in-h piece is bounded by (g/c²)² relative to k²;
  the accumulated phase through a 100 kpc halo is computed and must be < 1e-6 rad for LVK and LISA frequencies to count as
  "no effect"; (v) single-metric coupling: photons and GWs share the same Shapiro delay including the phantom (Boran et al.
  2018 test), Δt_GW−EM = 0.
- Option C (recipe, CFG500): no chassis, Ξ = 1 and c_T = 1 are DECLARED by B1/L1 (GR background, GR lensing), not derived;
  reported as UNTESTED-BY-DECLARATION.
- Measurement forecast: σ(Ξ0) for S1–S4 from this lane's Fisher (Ξ(z) = Ξ0 + (1 − Ξ0)/(1+z)^n, n = 2.5).
- Expected status: CONSISTENCY test only (framework = GR = ΛCDM here), not DISTINCT.

## 3. Part 3: cold-energy dress around massive black holes and EMRI dephasing

- Kernel: the record's ν_mono (CFG5_common.py: ν_RAR up to y*, monotone log splice δ = 0.05). Its tail
  h(y) ≡ (ν − 1) y grows like δ h_p ln y, so the phantom acceleration g_ph = a0 h(y) does NOT vanish at y ≫ 1.
  Comparator kernel ν_RAR (pure exponential tail): phantom ≈ 0. Both are reported; the kernel dependence is a finding.
- Phantom density (spherical): ρ_ph = (1/4πG r²) d/dr [r² a0 h(y(r))], y = g_b/a0.
- Ownership readings (S2 is declared, not derived): O1 the BH is part of its galaxy's baryons (g_b includes GM/r²);
  O2 the BH carries no phantom (like the Sun), g_b from the nuclear star cluster only (ρ* ∝ r^{−7/4}, M*(<r_h) = 2M,
  r_h = GM/σ², M–σ: M = 3.1e8 Msun (σ/200 km/s)^{4.38}, recalled).
- Cold-energy dress readings: D1 relaxed (R1 rule: cold energy = phantom target, the recipe's headline); D2 a
  Gondolo-Silk adiabatic spike (γ = 1 seed → γ_sp = 7/3, α_γ = 0.122, recalled) seeded by the D1 profile, IF relaxation
  does not act in the nucleus (disclosed variant, not the recipe's rule). Standard MOND: the phantom is a field, not matter:
  no friction, no accretion (dress = 0). ΛCDM comparator: NFW-seeded Gondolo-Silk spike (cold, no annihilation) and its
  stellar-heated r^{−3/2} version (both recalled forms).
- Hosts: M = 4.3e6 Msun (MW-like), 1e6, 1e5 Msun; compact object m = 10 Msun; circular quasi-Newtonian inspiral, quadrupole
  GW loss, plunge at r_ISCO = 6GM/c², last 4 yr; dynamical friction F = 4πG²m²ρ lnΛ / v², lnΛ = ln √(M/m), full density
  (upper estimate); collisionless accretion drag included.
- **Dephasing thresholds (recalled, flagged):** LISA detectable if ΔΦ_GW ≥ 1 rad (conservative); ≥ 0.1 rad (optimistic).
- **Frozen rule:** the framework predicts "NO detectable dress" if ΔΦ(D1, O1 and O2) < 0.1 rad for every host. It predicts a
  DETECTABLE dress if ΔΦ(D1) ≥ 1 rad for some host. Intermediate = MARGINAL. DISTINCT vs MOND (= 0) and vs ΛCDM spike by the §0 rule.
  The static phantom's conservative effect on the orbit (δΩ²/Ω² = h/y) is also computed.

## 4. Part 4: pulsar timing

- Cold energy behaves as CDM on tested scales (CFG474: mass ≥ 3e-19 eV if a wave field; λ_dB ≤ 0.2 pc at 200 km/s).
- Computed: the ultralight-field pressure oscillation (Khmelnitsky-Rubakov form, Ψ_c = πGρ/(m²) in natural units) at the
  window edges 3e-19 eV and 5.3e-17 eV: frequency vs the PTA band (1e-9–1e-7 Hz) and residual amplitude.
- Subhalo Doppler/Shapiro: compared qualitatively with recalled forecasts (Dror et al. 2019; Ramani et al. 2020): no
  framework-distinct number unless the cold energy's small-scale spectrum differs from CDM, which the record does not specify.
- Expected: NOT DISTINCT. A "framework-distinct" PTA claim requires §0.

## 5. Controls (must pass in the main run)

- K1 the chains reproduce L275's density-mapping medians at z = 2.5 within 0.005 dex.
- K2 Fisher sanity: with σ_dL → 1e-6 for 1000 events the Fisher errors shrink ∝ σ; a single low-z event constrains
  H0 to σ_dL × H0 within 10%.
- K3 sympy: GR limit (β = λ_K − 1 = 0) gives ḧ + 3Hḣ + k²h/a² = 0; a time-dependent M_T²(t) control yields the friction
  2H(1 + α_M/2) with α_M = dln M_T²/dln a.
- K4 the direct h_mono matches CFG5_common.nu_mono at y = 1 … 1e6 to 1e-6.
- K5 dephasing engine: with ρ = 0, ΔΦ = 0; the vacuum 4-yr N_cycles matches the analytic quadrupole formula within 1e-3.

## 6. MUTATE (CFG512_MUTATE=1; separate outputs *_MUTATE.out, *_results_MUTATE.json)

- M1 chassis with c_T ≠ 1: β = 0.01. It MUST be flagged by GW170817 (|c_T − 1| = 5e-3 vs the bound −3e-15 < c_T − 1 < 7e-16,
  Abbott et al. 2017 GW170817/GRB170817A, recalled). The main-run check "c_T consistent with GW170817" must FAIL.
- M2 a0 forced flat: Δlog a0 ≡ 0. It must change the siren-route prediction only where w ≠ −1: the difference
  (tracking − flat) must be 0 (to 1e-12) at the ΛCDM fiducial and non-zero (> 0.01 dex at z = 2.5) at every DESI branch;
  the propagated siren σ becomes 0. The main-run check "prediction tracks ρ_DE" must FAIL under M2.
- The MUTATE run must exit 1 with exactly those checks flipped.

## 7. Reporting

README with a table of GW tests: test | framework prediction | ΛCDM | MOND | experiment | decisive? (Y/N), plus the single
most decisive GW test for the framework. A fail is reported as hard as a win. No "the data favour". κ fitted; cold energy's
mass required; supply per galaxy a postulate; not theory closed.
