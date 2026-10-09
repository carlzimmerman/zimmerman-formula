# CFG512: gravitational waves as tests of the framework

Criteria frozen first: [FROZEN_CRITERIA.md](FROZEN_CRITERIA.md), commit c072a709d, committed alone before any script.
Offline only: the DESI DR2 chains already on disk plus forecasts. Nothing was downloaded. Forecast inputs (event rates,
distance errors, lensing noise, spike forms, LISA thresholds) are **recalled from the literature and unverified**.

- κ = ½ is FITTED.
- The cold energy's mass is still required.
- The supply per galaxy is a postulate.
- This is not "theory closed".

| run | outputs | checks | exit code |
|---|---|---|---|
| main | `cfg512_gw.out`, `cfg512_results.json` | 14/14 pass | 0 |
| MUTATE (`CFG512_MUTATE=1`) | `cfg512_gw_MUTATE.out`, `cfg512_results_MUTATE.json` | 12/14; exactly T4 (GW170817) and C-TRACK fail, as required | 1, as required |
| first main run (kept) | `cfg512_gw_run1.out` | 13/14; T3 failed on a sign-convention bug (Disclosure 1) | 1 |

    nice -n 15 python3 campaign_fresh_gravity/CFG512_gravitational_waves/cfg512_gw.py
    CFG512_MUTATE=1 nice -n 15 python3 campaign_fresh_gravity/CFG512_gravitational_waves/cfg512_gw.py

Each run takes a few seconds.

## Bottom line

- **No gravitational-wave test is decisive for the framework** under the frozen rule. Where the framework makes a
  relativistic prediction (c_T, Ξ, Shapiro), it is the same as ΛCDM's. Near black holes, the recipe's prediction is the
  same as MOND's.
- **The most decisive GW test is LISA EMRI environmental dephasing**, and it only cuts one way.
  - The recipe's headline rule (R1: the cold energy relaxes to the phantom) predicts **no detectable dress**:
    ΔΦ(4 yr) = 5e-8 to 5e-6 rad.
  - An undisturbed CDM Gondolo-Silk spike gives 11 to 1.2e4 rad.
  - If LISA detects a spike-level dress, the relaxed-phantom rule and standard MOND are both falsified. Only the
    unrelaxed variant would survive, and that variant is CDM-identical.
  - A null result does not discriminate: a stellar-heated ΛCDM spike is also undetectable.
- **The siren route does not change the a₀(z) bottleneck.**
  - The current DESI DR2 chains already pin the law's predicted a₀(z) to ±0.04 dex at z = 2.5, seven times tighter than
    the galaxy route's 0.3 dex calibration wall.
  - Einstein Telescope sirens tighten that by only 5–7%; ET + Cosmic Explorer by 23–25%.
  - What limits the test is the high-z rotation-curve measurement, not the prediction.

## The GW test table

σ values come from this lane's Fisher forecast unless marked (r) for recalled.

| test | framework prediction | ΛCDM | MOND | experiment (σ) | decisive? |
|---|---|---|---|---|---|
| GW speed c_T | **c_T = 1 exactly.** Option A chassis, β = 0: c_T² = 1/(1−β), derived symbolically. MUTATE β = 0.01 gives c_T − 1 = 5.0e-3, which GW170817 flags. Option C: c_T = 1 is declared, not derived | 1 | AeST: 1. TeVeS/bimetric class: ≠ 1, already excluded | GW170817/GRB170817A, −3e-15 < c_T − 1 < 7e-16 (r). **Passed** | **N.** Consistency test; same as ΛCDM |
| GW vs EM Shapiro delay | **Δt = 0.** The phantom is filled by cold energy, which is real mass on the one metric | 0 | AeST: 0. Dark-matter emulators (GWs blind to the phantom): **157 days** (this lane's MW counterfactual) | GW170817 (Δt ≈ 1.7 s, r). **Passed** | **N.** Kills emulators, not the framework |
| Ξ(z) = d_GW/d_EM (GW friction) | **Ξ ≡ 1.** α_M = 0 exactly for symbolic (β, c₂, α); no tensor mass term. MOND-sector phase through a 100 kpc halo ≤ 9e-16 rad (PTA), 9e-21 rad (LISA), 9e-26 rad (LVK). Option C: declared | 1 | 1 (AeST) | σ(Ξ0) with H0 free: LVK O5 0.25, LISA 0.11, ET 0.018, ET+CE 0.0125 | **N.** Same as ΛCDM. A measured Ξ ≠ 1 would kill chassis A |
| sirens → w0, wa → predicted a₀(z) | Δlog a₀ = ½ log f_DE. On the DESI branches: +0.014 to +0.037 dex (z 0.5), −0.005 to +0.014 (z 1), **−0.084 to −0.109 (z 2.5)**. 0 if w = −1. σ_pred at z 2.5: 0.039–0.044 now; 0.036–0.042 with ET; 0.029–0.034 with ET+CE | no a₀ | flat: 0. The a₀ ∝ H(z) rival: +0.57 dex at z 2.5 | galaxy a₀(z): 0.3 dex wall at z ≈ 2.5 | **N.** The measurement is the bottleneck. Tracking minus flat (0.08–0.11 dex) is a third of the wall |
| cold-energy dress around massive black holes (LISA EMRI, m = 10 M☉, last 4 yr) | **R1 relaxed phantom: ΔΦ = 5e-8 to 5e-6 rad, no detectable dress.** ν_mono's log tail gives ρ_ph ≈ a₀h/(2πG r): 1e8 to 7e9 M☉/pc³ at ISCO. With ν_RAR's exponential tail: 0. The unrelaxed D2 spike: 11 to 1.2e4 rad (CDM-identical within ×1.2) | Gondolo-Silk spike: 12 to 1.1e4 rad. Heated r^−3/2 spike: 4e-6 to 3e-3 rad | 0. The phantom is a field, not matter. Static orbit shift ≤ 6e-10 rad | LISA, ΔΦ ≳ 0.1–1 rad (r) | **N.** Equals MOND, and ΛCDM is not unique here. **One-sided:** a detected spike kills R1 and MOND |
| khronon dipole / scalar polarisation | Pb-dot deviation ≤ 4.9e-13 (CFG291); scalar mode amplitude ∝ α_c ≤ 3.2e-9 | 0 | model-dependent | binary pulsars, LVK polarisation tests | **N** |
| PTA: ultralight-field pressure oscillation | outside the band: f = 1.5e-4 to 2.6e-2 Hz for the CFG474 window (m ≥ 3e-19 eV); residual ≤ 8e-22 s | none (WIMP-like) | none | NANOGrav/IPTA/SKA (band 1e-9–1e-7 Hz) | **N** |
| PTA: subhalo Doppler/Shapiro | same as CDM: the cold energy is CDM-like on tested scales (CFG474); its small-scale spectrum is unspecified. Not computed | CDM subhalos: undetectable for standard NFW subhalos (Ramani et al. 2020, r) | smooth phantom: none | SKA-era PTAs | **N** |

## Part 1: standard sirens → a₀(z)

**Assumptions** (frozen §1, recalled):

| id | scenario | events | per-event distance error |
|---|---|---|---|
| S0 | GW170817 | 1 | 14% + peculiar velocity |
| S1 | LVK O5 | 30 BNS at z < 0.15 | 10% |
| S2 | LISA massive-BH binaries | 25, p(z) ∝ z²e^−z | 2% ⊕ lensing (Tamanini/Hirata fit) |
| S3 | ET | 1000 BNS to z = 2 | 10% at z = 1, ∝ d_L ⊕ lensing |
| S3p | ET, pessimistic | 200 | as S3 |
| S4 | ET + CE | 3000 to z = 3 | 5% |

Redshifts come from EM counterparts. **H0 is free throughout**, because the thinned chains carry no H0. That is
conservative.

**Results** (Pantheon+ / Union3 / DESY5, never pooled):

| quantity | z = 0.5 | z = 1 | z = 2.5 |
|---|---|---|---|
| prediction Δlog a₀ (chain median) | +0.014 / +0.037 / +0.025 | −0.004 / +0.014 / +0.004 | −0.083 / −0.107 / −0.098 |
| σ, DESI DR2 chains alone (now) | 0.007 / 0.012 / 0.007 | 0.012 / 0.014 / 0.012 | 0.039 / 0.044 / 0.041 |
| σ, ET (1000) alone | 0.08 / 0.06 / 0.07 | 0.26 / 0.22 / 0.24 | 0.82 / 0.74 / 0.78 |
| σ, ET+CE (3000) alone | 0.019 / 0.015 / 0.017 | 0.07 / 0.06 / 0.06 | 0.24 / 0.22 / 0.23 |
| σ, LISA (25) alone | 0.5 | 0.3 | 2.4 |
| σ, ET + chains | 0.0065 / 0.0091 / 0.0064 | 0.010 / 0.011 / 0.010 | 0.036 / 0.042 / 0.038 |
| σ, ET+CE + chains | 0.0055 / 0.0069 / 0.0055 | 0.0076 / 0.0078 / 0.0076 | 0.029 / 0.034 / 0.031 |
| a₀ ∝ H(z) rival | +0.13 | +0.25 | +0.57 |

Frozen verdicts:
- **P1a FALSE.** ET + prior does not halve the chain-only σ: 0.039 → 0.036 on Pantheon+.
  - Post-hoc and not frozen: adding an H0 prior of 0.5% to ET+CE gives 0.028–0.031. That still is not a halving.
- **P1b TRUE.** The current prediction σ at z = 2.5 is 0.039–0.044 dex, below a third of the 0.3 dex wall.
- **P1c FALSE.** Tracking minus flat at z = 2.5 is −0.08 to −0.11 dex. That is far below the 0.9 dex needed for galaxies
  to resolve it.

The siren route's real value is different: it is an SN-systematics-free check of whether w ≠ −1. ET+CE alone gives
σ(w0) ≈ 0.14. That decides whether the framework predicts flat a₀ (w = −1) or a 0.1 dex decline by z = 2.5.

## Part 2: d_GW vs d_EM

**The derivation** (sympy, exact metric diag(−1, a²e^h, a²e^−h, a²), u = ∂_t, aether/khronon convention
L = R − βK_ijK^ij − c₂K² + α a·a):
- K = 3H exactly.
- K_ijK^ij = 3H² + ḣ²/2.
- a·a = 0 on FRW. The law is off on the background (S1).

The linear tensor equation is **ḧ + 3Hḣ − h_zz/[(1−β) a²] = 0**, with no mass term. So:
- α_M = 0, and **Ξ(z) ≡ 1** for every β, c₂ and α.
- c_T² = 1/(1−β), which is 1 at the record's β = 0.

Control: an explicit running M_T²(t) does produce the extra friction dln M_T²/dt.

Inside halos, the filtered MOND term enters the tensor sector only at O((g/c²)²): ≤ 9e-16 rad of phase even at PTA
frequencies.

Ξ = 1 is therefore a **consistency** prediction, shared with GR/ΛCDM and AeST.
- MUTATE β = 0.01 leaves Ξ = 1 but gives c_T − 1 = 5e-3, which GW170817 catches. That is the correct division of labour.
- Under option C (recipe), Ξ = 1 and c_T = 1 are declared, not derived. They are untested by declaration.

## Part 3: cold-energy dress around massive black holes

**ν_mono does give a phantom near a black hole.** The finding turns on the kernel's log splice:
- h(y) = (ν−1)y grows like δh_p ln y: h = 1.64 at y = 1e14. So g_ph = a₀h(y) does not vanish where g ≫ a₀.
- ρ_ph = (1/4πGr²) d(r² a₀h)/dr ≈ a₀h/(2πG r). That is a 1/r cusp whose ρ·r is about 0.18 kg/m² at every host. This
  is the same order as an NFW halo's ρ_s r_s (0.12–0.25 kg/m²).
- With ν_RAR's exponential tail the phantom is identically 0 (h(1e4) = 4e-40). **The answer is kernel-dependent.**

Under ownership, O1 (the BH is part of the galaxy's baryons) and O2 (the BH owns no phantom) differ by only ×1.5.

**The recipe's relaxed dress gives no detectable dephasing.**
- The density is large at ISCO (1e8 to 7e9 M☉/pc³), but the 4-yr ΔΦ is only 5e-8 to 5e-6 rad. That is 4–7 orders
  below LISA's threshold for every host (4.3e6, 1e6, 1e5 M☉).
- Frozen rule: **NO DETECTABLE DRESS.** The static phantom's conservative orbit shift is ≤ 6e-10 rad.

**The disclosed variant D2 is CDM-like.** If relaxation does not act in the nucleus, the collisionless cold energy is
adiabatically compressed by BH growth. Its 1/r seed has CDM-like surface density, so the Gondolo-Silk spike
matches the ΛCDM spike to ×1.2: 11–1.2e4 rad.

So the EMRI test probes the **relaxation rule R1 in nuclei**, not the framework against ΛCDM directly.
- Recipe (relaxed): equals MOND (no dress).
- Unrelaxed: equals CDM.

The friction is evaluated at full density with no halo feedback, so it is an upper estimate. Published spike
analyses with feedback (Kavanagh et al. 2020, r) give smaller dephasing.

## Part 4: pulsar timing

In every surviving CFG474 window (m ≥ 3e-19 eV), the cold energy's pressure oscillation is at f ≥ 1.5e-4 Hz. That is
three decades above the PTA band, with a residual ≤ 8e-22 s.

- Control: the Khmelnitsky-Rubakov amplitude is reproduced to 6% at 1e-22 eV.
- Subhalo Doppler/Shapiro signals equal CDM's, because the cold energy is CDM-like on tested scales and the record
  does not specify its small-scale spectrum.
- **No framework-distinct PTA prediction.**

## Controls and MUTATE

| control | what it checks | result |
|---|---|---|
| K1 | the chains reproduce L275's z = 2.5 medians | to 0.0005 dex |
| K2 | Fisher sanity | σ(H0)/H0 = 0.0500 for one 5% event; exact linear scaling |
| K3 | sympy controls | the GR limit and the running-Planck-mass friction both come out right |
| K4 | direct h_mono against CFG5_common.nu_mono | agrees to 0 |
| K5 | vacuum quadrupole phase against analytic | agrees to < 1e-3 |
| K6 | Khmelnitsky-Rubakov Ψ_c | reproduced |

MUTATE:
- M1 (β = 0.01) fails T4 (GW170817), as required.
- M2 (a₀ forced flat) fails C-TRACK, as required. The comparison check confirms that flat-forcing changes the
  prediction by 0 at the ΛCDM fiducial and by 0.08–0.11 dex at z = 2.5 on every DESI branch.

## Disclosures

1. **Run 1 sign-convention bug.** Run 1 (kept: `cfg512_gw_run1.out`) wrote +βK_ijK^ij, which gave c_T² = 1/(1+β), and T3
   failed. The record's convention (L340/CFG292, Jacobson-Mattingly) is −βK_ijK^ij, so the sign was fixed. α_M = 0 and
   the no-mass result did not depend on the sign.
2. **The Gondolo-Silk inner edge was not frozen.** The frozen spec named the GS spike but not its inner edge. GS's
   (1 − 4R_s/r)³ cut is zero at 8GM/c², which removes the whole 4-yr window of the 4.3e6 M☉ host. A relativistic-edge
   row (4GM/c², Sadeghian-like, r) was therefore added after run 1, for both the D2 and ΛCDM spikes. Both edges are
   reported.
3. **Recalled ΛCDM comparator inputs.** The ΛCDM halo for each host uses M200 ∝ M_BH^(1/1.65) and c = 10 (recalled,
   declared). The spike numbers are order-of-magnitude comparators.
4. **H0 free and the Ξ0 forecast.** H0 is free in all siren Fishers. Literature forecasts that include CMB H0
   information quote tighter σ(Ξ0) for ET (≈ 0.008, r).
5. **ΛCDM fiducial covariance.** The ΛCDM fiducial borrows the Pantheon+ chain covariance as its prior.
6. **Superseded L275 reading.** L275 called the density mapping "rejected" in favour of a pressure mapping. This lane
   uses the owner's stated law a₀ = κc√(Gρ_DE) (feedback 10-06), which is the density mapping.
