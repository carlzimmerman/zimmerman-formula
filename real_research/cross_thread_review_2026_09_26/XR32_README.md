# XR32 — does the chain's late-time dark-fluid conversion lower weak-lensing S8 by the right amount, and keep CMB lensing, clusters, RSD and Σm_ν consistent?

Cross-thread review, 2026-09-27. Three scripts and a shared module in this folder, read-only on every other file. Every
number below comes from a runnable script in this folder with controls (not committed by this lane); each script has a
MUTATE run (conversion switched off) that must fail and does (rc = 1).

- The dark fluid is FK1/FP10's classical field, not a particle species; **the dark mass is still required**.
- κ = ½ does not enter. No constant was added. a₀ enters only through the MOND-phantom stand-in, on both footings
  (canonical 9.3603 × 10⁻¹¹, alt 1.1312 × 10⁻¹⁰ m s⁻²).
- **Normalisation assumption:** Planck 2018 ΛCDM (TT,TE,EE+lowE+lensing posterior means, Σm_ν = 0.06 eV), pending XR26
  (whether the chain's early universe is ΛCDM). Truth: S8 = 0.831 (CAMB), Planck quotes 0.832 ± 0.013.
- XR19's histories come from its results JSON, which was **uncommitted** when this lane ran; FP10's from its committed JSON.
- The MOND phantom enters **only as a labelled bracket**: none, or a 1.7 Mpc stand-in (H_Y's z = 0 band-pass length). The
  separator is under repair (FP19) and the chain's KiDS projection is being fixed (FP20); esd_of_M is not used anywhere.

## The answer

**Without the phantom, yes for the low-z weak-lensing S8 — but not cleanly, and not for the other probes.**

1. The conversion lowers the linear σ8 by 5.0–6.9% across δ_t0 = 5.31–25. On Planck's normalisation that is S8 =
   0.774–0.789 (nominal 0.774).
2. A survey fitting the chain's shear with ΛCDM templates would infer:
   - S8 = 0.766 in the KiDS-1000 set-up and 0.752 in the DES-Y3 set-up (nominal cell);
   - 0.759–0.779 (KiDS) and 0.741–0.778 (DES) across every history and footing (primary recapture reading).

   That lands on KiDS-1000, DES Y3 and HSC Y3, and about 2σ below KiDS-Legacy.
3. The fits are not clean:
   - they lean on nuisances pinned at their prior edges (KiDS A_bary = 2.0; DES η_IA = −3);
   - they leave a noiseless χ²_min of 4–52 (KiDS, 225 points; the halo-only history fits best) and 12–32 (DES, 273
     points): the small-scale suppression is not shaped like ΛCDM plus feedback.
4. With the phantom stand-in, the shear is not ΛCDM-like at all (χ²_min 540–2877 for KiDS, 112–280 for DES). The MOND sector's small-scale
   lensing decides this lane's bracket, and it cannot be settled here.
5. The other probes all move against the chain:
   - CMB lensing drops 2.4% (band-weighted) over L = 40–763;
   - cluster counts drop to 0.64–0.81 of ΛCDM's;
   - RSD fσ8 drops 3.5–7%;
   - the lensing channel acts like +0.10 eV of neutrino mass.

## 1. Matter power (`XR32_matter_power.py`: main 11/12, rc = 1 — H1e fell; MUTATE rc = 1)

**Method.**
- Linear, two components: L319's validated solver (exec'd via L357's committed head, unedited). The cold phase and
  cohort-resolved free-streaming daughters (kicked at v_k, Hubble-cooled) are coupled through Poisson, on XR19's
  S(a) = 1 − F_esc(a).
- Nonlinear: a halo-model response applied to CAMB HMcode-2020, P_chain = R(k, z) × P_HMcode.
  - Sheth–Tormen and NFW.
  - Every halo keeps its baryons and a retained carrier fraction ret(M, z).
  - The raw halo model is 10–26% below HMcode in the transition regime, which is why it enters only as a ratio.
- Recapture readings:
  - **primary (phase-space):** carrier that arrives unconverted converts in place (1 − L357's esc()). Free daughters are
    recaptured up to the Tremaine–Gunn limit ρ_d ≤ f_max (4π/3) v_esc³, with σ_d(z) from the history. This is an upper
    bound on recapture.
  - in place;
  - no recapture (FP10's optimistic reading);
  - the committed PM retention (L388).

| history | σ8 ratio z = 0 / 0.5 / 1 / 2 / 3 | S8 (Planck-normalised) |
|---|---|---|
| halo only | 0.956 / 0.962 / 0.970 / 0.982 / 0.990 | 0.794 |
| **nominal (δ_t0 5.31)** | **0.931** / 0.948 / 0.963 / 0.981 / 0.990 | **0.774** |
| most conservative | 0.942 / 0.956 / 0.967 / 0.982 / 0.990 | 0.783 |
| pump = full density | 0.924 / 0.942 / 0.959 / 0.981 / 0.990 | 0.768 |
| δ_t0 7.54 / 14.6 / 22.8 / 25 | 0.935 / 0.943 / 0.949 / 0.950 (z = 0) | 0.777 / 0.784 / 0.789 / 0.789 |
| v_k 575 / 650 | 0.936 / 0.920 (z = 0) | 0.778 / 0.765 |

- **Small scales, linear.** T²(k = 1 h/Mpc, z = 0.5) = 0.118. Two thirds of the matter is free-streaming daughters at
  z < 1.
- **Retained carrier (primary, z = 0.5).** 0.008 at 10¹² M☉, 0.12 at 10¹³, 0.57 at 10¹⁴ and 0.96 at 10¹⁵ (free-daughter
  σ_d = 136 km/s). The committed PM gives 0.07 / 0.11 / 0.50 / 0.82.
- **Response R(k = 0.3 / 1 / 3 h/Mpc, z = 0.5):**

| reading | no phantom | 1.7 Mpc stand-in (canonical / alt) |
|---|---|---|
| **primary** | 0.751 / 0.377 / 0.285 | 0.921 / 0.904 / 2.61 ; 0.939 / 0.982 / 3.02 |
| in place | 0.783 / 0.522 / 0.575 | 0.955 / 1.166 / 3.42 |
| no recapture | 0.680 / 0.112 / 0.103 | 0.848 / 0.551 / 2.22 |
| PM (L388) | 0.738 / 0.328 / 0.254 | 0.908 / 0.846 / 2.56 |

**The phantom stand-in.** Each halo's GP0 'observed' bound baryons with ν_mono, truncated at L = 1.7 Mpc physical at every
z and compensated there (L363/MS3's transform). Only halos of 10¹⁰–10^15.5 M☉ carry it, the record's halo-model range.
- Its sharp edge rings: R reaches ~3 at k ≈ 3 h/Mpc.
- H_Y's heat-kernel form (reported only) instead gives 2–7× ΛCDM at k ≲ 1.
- The stand-in's form therefore matters as much as its presence.

**Checks.**
- C1–C5 pass:
  - XR19's seven S8 values and FP10 A8's three are reproduced exactly;
  - the recombination is bit-identical;
  - no conversion gives T² = 1 and R = 1 exactly;
  - Planck σ8 = 0.8109, S8 = 0.8312.
- H1a–H1d and H1f pass.
- **H1e fell:** the sharp stand-in gives R(1, 0.5) = 0.904 / 0.982, not > 1.
- MUTATE fails H1a, H1c, H1d and H1f.

## 2. The S8 a survey would infer (`XR32_survey_s8.py`: main 11/13, rc = 1 — H2c and H2d fell; MUTATE rc = 1)

**Set-ups.**
- **KiDS-1000.** Five Z_B bins, 9 θ bins over 0.5–300′, ξ₋ above 4′ (225 points).
  - n(z): stacks of the DR4.1 gold catalogue's photo-z PDFs, moment-matched to Asgari+21 Table A.1. This is an
    approximation; the tails come out lighter.
  - Covariance: analytic Gaussian, 777.4 deg².
- **DES Y3.** The official 2pt file (n(z), covariance), with the ΛCDM-optimised scale cuts (273 points).
- **Templates** (CAMB):
  - KiDS: HMcode-2016 with A_bary ∈ [2, 3.13] and NLA A_IA;
  - DES: Takahashi halofit with NLA (A₁, η₁);
  - Ωm and S8 free; h, ω_b and n_s fixed at the truth.
- The chain's data are noiseless: R(k, z) × the survey's own template at the Planck truth.

**Controls.**

| control | result |
|---|---|
| Limber vs CAMB's lensing windows (CAMB exact below ℓ = 100) | max 0.34% at ℓ = 30–3000 (CAMB's own Limber output departs from its exact result by up to 1.15% at ℓ < 100) |
| Hankel vs analytic | 5 × 10⁻⁴ |
| truth recovered | ΔS8 = +0.0000 (KiDS) / −0.0008 (DES) |
| **real DES Y3 data through the same pipeline** | S8 = 0.795, χ² = 286 for 273 points (published 0.772 ± 0.018) |
| truth-fit Δχ² = 1 width | ±0.013 (KiDS), ±0.010 (DES), against the published ±0.018 (fewer free parameters) |

**Inferred S8.** Nominal cell unless stated; χ²_min is noiseless.

| configuration | KiDS-1000 set-up | DES-Y3 set-up |
|---|---|---|
| truth (Planck 2018) | 0.831 | 0.831 |
| **nominal, primary, no phantom** | **0.766** (A_bary 2.00, A_IA −0.18; χ² 40) | **0.752** (η_IA −3.0; χ² 27) |
| in place / no recapture / PM | 0.753 / 0.755 / 0.760 | 0.757 / **0.695** / 0.738 |
| halo population = cold field | 0.765 | 0.748 |
| δ_t0 7.54 / 14.6 / 22.8 / 25 | 0.769 / 0.773 / 0.776 / 0.776 | 0.751 / 0.755 / 0.761 / 0.762 |
| halo only / most conservative / pump s = 1 | 0.779 / 0.772 / 0.762 | 0.778 / 0.755 / 0.750 |
| v_k 575 / 650 | 0.770 / 0.759 | 0.757 / 0.741 |
| 1.7 Mpc stand-in, canonical / alt | 0.771 (χ² 1001) / 0.766 (χ² 1509) | 0.760 (χ² 141) / 0.760 (χ² 195) |
| heat-kernel stand-in / running L(z) (sensitivities) | ≥ 1.12, the grid edge (χ² 383) / 0.739 (χ² 335) | ≥ 1.12 (χ² 893) / 0.753 (χ² 49) |

**Against the published values** (nominal, primary, no phantom; in published σ, then with Planck's 0.013 added):

| published | value | this lane | tension |
|---|---|---|---|
| KiDS-1000 ξ± (Asgari+21) | 0.764 +0.018 −0.017 | 0.766 | +0.1σ (+0.1) |
| KiDS-Legacy (Wright+25) | 0.815 +0.016 −0.021 | 0.766 | −2.3σ (−2.0) |
| DES Y3 ΛCDM-optimised (Amon/Secco+22) | 0.772 +0.018 −0.017 | 0.752 | −1.2σ (−0.9) |
| DES Y3 fiducial | 0.759 +0.025 −0.023 | 0.752 | −0.3σ (−0.3) |
| HSC Y3 ξ± (Li+23) | 0.769 +0.031 −0.034 | 0.766 | −0.1σ |
| HSC Y3 C_ℓ (Dalal+23) | 0.776 +0.032 −0.033 | 0.752 | −0.7σ |

**Hypotheses.**
- H2a passes: ΔS8 = −0.065 (KiDS) and −0.079 (DES).
- H2b passes: no higher than the linear S8 of 0.774.
- H2e passes: χ² 40.
- **H2c fell:** the stand-in does not push S8 above the truth.
- **H2d fell:** the chain does not overshoot the low-z values; it lands on them.

MUTATE fails H2a.

## 3. Consistency (`XR32_consistency.py`: main 7/9, rc = 1 — H3b and H3d fell; MUTATE rc = 1)

- **CMB lensing** (Limber against CAMB's own lensing potential: 0.21% at L = 40–763).
  - The C_L ratio at L = 100 / 300 / 763 / 1000 is 0.995 / 0.972 / 0.899 / 0.858.
  - The amplitude over ACT DR6's L = 40–763 is **A = 0.976** (ten equal bands) or 0.954 (cosmic-variance weights). It
    ranges 0.968–0.983 over every history and reading.
  - That is **−1.6σ against ACT DR6's A_lens = 1.013 ± 0.023**, and σ8^CMBL = 0.801 against ACT+Planck's 0.812 ± 0.013
    (−0.85σ).
  - Conversion is not small at z ~ 1–3: early halo escapes give F_esc = 0.49 / 0.62 at z = 3 / 2.
  - **H3b fell narrowly:** |A − 1| = 0.024 against 0.023.
  - The 1.7 Mpc stand-in gives A = 1.045–1.059. Holding L at its z = 0 value to z ~ 2 is unphysical, since H_Y's own
    L(2) = 0.18 Mpc; with the running L it gives A = 0.980.
- **Σm_ν.**
  - CAMB's lensing slope is −0.246 per eV at fixed θ*.
  - The conversion's lensing change equals **+0.098 eV** (0.069–0.13 eV over the histories), about 5 × DESI DR2's
    σ(Σm_ν) = 0.020 eV if lensing carried the constraint.
  - The expansion history is untouched (daughters' w ~ 10⁻⁷), so only the lensing channel of DESI + CMB moves. It moves
    **in the direction that worsens** the preference for Σm_ν,eff < 0 (σ = 0.053 eV, 3σ below the oscillation floor).
- **Cluster counts.** eRASS1-like: z 0.1–0.8, M500c > 1.5/3 × 10¹⁴ M☉. SPT-like: z 0.25–1.78, M500c > 3.5/5 × 10¹⁴ M☉.
  These selections are proxies.
  - Primary recapture, no phantom: N/N_ΛCDM = 0.64–0.81, a count-equivalent **S8 = 0.768–0.813**.
    - Consistent with SPT (0.795 ± 0.029).
    - 5–9σ below eRASS1 (0.86 ± 0.01), which already sits above Planck.
  - In place: 0.787–0.800.
  - PM: 0.749–0.784.
  - **No recapture: 0.56–0.57** (clusters lose 80% of their carrier).
  - The phantom inside R500 (not band-limited there) raises counts 1.4–3.3× in the recapture readings (S8_eq
    0.89–0.97).
  - Over every history and both halo populations (primary, no phantom): S8_eq 0.755–0.817.
  - Recapture preserves the counts only partly (H3c passes: below Planck).
- **RSD.**
  - fσ8 is lower by 7.3 / 6.5 / 5.8 / 5.0 / 3.9 / 3.5% at DESI DR1's z_eff = 0.295 … 1.491.
  - f is scale-dependent: the ratio is 0.997 / 0.986 / 0.918 at k = 0.05 / 0.1 / 0.2 h/Mpc (z = 0.51).
  - Implied σ8 = 0.768 (0.760–0.780 over the histories), **−2.2σ against DESI DR1's 0.842 ± 0.034**. Planck ΛCDM sits at
    −0.9σ. **H3d fell.**

MUTATE gives A = 1, ΛCDM counts, and no fσ8 change, so H3a fails.

## Robustness (δ_t0 5.31–25, both footings, the phantom bracket)

- **Canonical footing** (δ_t0 band 7.54–14.6):
  - linear S8 0.777–0.784;
  - survey S8 0.769–0.773 (KiDS) and 0.751–0.755 (DES).
- **Alt footing** (band 7.54–22.8):
  - linear S8 0.777–0.789;
  - survey S8 0.769–0.776 (KiDS) and 0.751–0.761 (DES).
  - The footing enters only through the band edge and the phantom stand-in.
- **The largest lever is recapture.** No recapture drops the DES-set-up S8 to 0.695 and the clusters to S8_eq 0.56. It
  is followed by the MOND phantom (χ² ~ 10³, sign-changing ringing) and the stand-in's edge form.
- κ is untouched. Every number rides on Planck's normalisation (±0.013 on S8).

## Disclosures

1. **Exploratory work first** (session scratch, not committed):
   - timing tests of CAMB and the solver;
   - the exact reproductions of XR19's nominal S8 and FP10 A8;
   - unit tests of the module.
   All hypotheses were written, time-stamped, before any full run (2026-09-27T14:01Z) and copied unchanged into the
   docstrings.
2. **Smoke runs** (`XR32_OUTDIR` in scratch; one for Part 1, two for Part 2, one for Part 3). What they found and changed:
   - **Phantom range.** The phantom's 2-halo factor reached B_ph = 8–75 when every halo down to 10⁶ M☉ carried an
     isolated 1.7 Mpc phantom. The record's 10¹⁰–10^15.5 M☉ range was adopted.
   - **Phantom edge form.** The truncated (sharp) and heat-kernel forms were both computed before the stand-in's form was
     fixed. The sharp one was kept, as the literal "within L" and the record's convention.
   - **J₄ bug.** A bug in the bin-averaged J₄ (a dropped antiderivative constant) made ξ₋ wrong. It was fixed and checked
     to 2 × 10⁻⁴.
   - **C1 changed.** C1 was changed to use CAMB's exact result below ℓ = 100, after a direct test showed CAMB's Limber
     output dips ~1% at ℓ ~ 40–45.
   - **Outcomes seen, nothing changed.** The smoke runs' H-outcomes were seen before the recorded runs; no hypothesis or
     threshold was changed.
3. **Recorded runs.** MUTATE first, then the main run, for each script, from the same code. The main runs exit 1 on the
   hypotheses that fell (H1e; H2c, H2d; H3b, H3d), kept as run.

## Limits

- **Halo-model level only.** There is no N-body or particle-mesh check.
- **Recapture.** It is a phase-space upper bound, bracketed by three other readings.
- **Survey stand-ins.**
  - The KiDS-1000 n(z) are moment-matched stand-ins, and the KiDS covariance is Gaussian.
  - h, n_s, ω_b, photo-z and m are not marginalised. The inferred S8 is a best fit, not a marginal posterior.
- **The phantom** is a stand-in bracket, isolated per halo.
- **Cluster and RSD comparisons** use selection proxies and equal-weight bins, not the surveys' likelihoods.
- **Σm_ν** is a lensing-channel equivalence, not a joint DESI fit.

## Files

- `XR32_common.py`: the shared machinery.
- `XR32_matter_power.py`, with `.out`, `_MUTATE.out`, `_results.json` and `_results_MUTATE.json`.
- `XR32_survey_s8.py`, with the same four outputs.
- `XR32_consistency.py`, with the same four outputs.
- `XR32_README.md`: this file.

## Reproduction

Run from the repository root, MUTATE first:

```
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR32_matter_power.py   # ~3 min
python3 real_research/cross_thread_review_2026_09_26/XR32_matter_power.py
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR32_survey_s8.py      # ~15 min
python3 real_research/cross_thread_review_2026_09_26/XR32_survey_s8.py
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR32_consistency.py    # ~3 min
python3 real_research/cross_thread_review_2026_09_26/XR32_consistency.py
```

Inputs:
- XR19's results JSON (on disk, uncommitted);
- FP10's and L388's committed JSONs;
- the DES Y3 2pt file (`deepseek_push/data2/`);
- the KiDS DR4.1 gold catalogue (`real_research/data/lensing_rar/`).

At most two threads (CAMB's OpenMP; the solver on two workers).
