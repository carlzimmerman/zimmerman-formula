# CFG592: a real cosmic-shear likelihood (KiDS-1000 ξ±, DES Y3 ξ±). Verdict: NOT DIAGNOSTIC on every track, by the declared rules; the Δχ² values point against the framework

- **Criteria:** `FROZEN_CRITERIA.md` (commit a3a22a833), committed alone before any data value was read. Date: 2026-10-10.
- **Addendum:** `ADDENDUM_2026-10-10.md` (commit 65fa05a07), committed alone before the frozen main run. It adds the owner's framework-native primary test (Part B) and the evolving-dark-energy variants (Part A). It discloses that the frozen MUTATE tooth had already failed.
- **Settings:** κ = ½ is FITTED. The footings are never pooled. The cold energy's MASS is still required; no particle species. Not "theory closed". Nothing here says the data favour the framework.
- **Numbers:** every number below comes from `cfg592_results.json`, `cfg592_results_MUTATE.json`, `cfg592_native_results.json`, `cfg592_native_results_MUTATE.json`, `cfg592_de_results.json` or `cfg592_final.json`.

## Data and software (`FETCH_LOG.md`)

Total download is about 45.6 MB, under the 400 MB cap. No login or bot check was met. The files live outside git in `_external_data/cfg592_work`.
- KiDS-1000 cosmic-shear release tarball: 17.3 MB.
- DES Y3 2pt FITS file (maglim): 28.3 MB.
- KiDS SOM photo-z covariance, and the DES Y3 cosmosis priors and scale cuts: small text files.
- pyccl 3.3.6 was installed by pip into a venv outside the repository.

## 1. Framework-native test (owner's primary, Part B): `cfg592_native.py`

This test uses no ΛCDM knobs.
- **Model:** the framework's own PM gravitating-field P(k, z), built with the CFG555 machinery.
- **Comparison:** each run's matched S0 PM run, built the same way.
- **Data:** the measured ξ±, the published covariance, n(z) and published cuts.
- **Nuisances:** measurement only — photo-z shifts, DES m, NLA IA (with and without).
- **Background:** the PM's own flat w = −1 background.
- **Not used:** no HMcode, no BAHAMAS, no mass function.

**Coverage, honestly.** The declared resolution cut keeps a data point only if at least 90% of its integrand lies at k ≤ k_Nyq/4.
- **L = 200 Mpc/h runs (all of the 424/425/439/460/518 family, and CFG530 at L200):** none of the 225 KiDS or 227 DES points survive the cut. The k range is 0.04–2.0 h/Mpc at 512³ and ≤ 1.0 at 256³. Small θ needs k > 2, and large θ needs k < 0.04. These runs are NOT DIAGNOSTIC.
- **CFG530 L = 100, N = 512 (k 0.08–4.0):** 20 KiDS points survive (91% lost) and 38 DES points (83% lost). All survivors are ξ− at θ ≈ 25–225′.

**Results for the two covered runs** (IA marginalised; Δχ² is framework − S0; positive means the framework fits worse):

| run | KiDS (20 pts) Δχ² | DES (38 pts) Δχ² | no IA (KiDS / DES) | S0 p-value (KiDS / DES) | framework p-value |
|---|---|---|---|---|---|
| 530 LRcan L100 N512 (canonical) | **+23.85** | +4.20 | +37.09 / +16.06 | 0.71 / 0.33 | 0.008 / 0.21 |
| 530 LRalt L100 N512 (alt) | **+30.04** | +5.56 | +46.00 / +19.57 | 0.71 / 0.33 | 0.001 / 0.18 |

Robustness:
- KiDS canonical: priors × 2 gives +20.34; the fade bracket +15.12; DESI distances +18.06.
- KiDS alt: +25.42; +19.04; +23.17.
- Feedback context (BAHAMAS, externally calibrated, T 7.6–8.0) moves KiDS to +21.6 → +16.8 (canonical) and +27.3 → +21.5 (alt).
- S0 alone fits both surveys acceptably on these points.

**Verdict by the addendum rule: NOT DIAGNOSTIC for every run and both footings.**
- The L200 runs keep no data.
- For the L100 runs the declared tooth NZ2 fails: a 20% excess at k ≥ 1 injected into an S0 mock is not detected on the surviving points (χ² 0.79 KiDS, 0.04 DES; ≥ 9 required).
- A post-hoc check moved the 20% excess to k ≥ 0.3. It is still not detected (χ² 3.68 / 0.73). It has no verdict effect.
- The framework's own source boost is larger than the tooth's 20%: B = P_grav/P_part = 1.20 / 1.36 / 1.32 at k = 0.3 / 0.5 / 1 (canonical L100). That is why its Δχ² is large while the 20% tooth is not detected.
- The raw class would be EXCLUDED on KiDS for both footings. That class is reported only; it is not the verdict.
- **Post-hoc** looser support cuts (no verdict):
  - f ≥ 0.8 keeps 101 KiDS / 103 DES points: Δχ² +38.1 / +3.7 (canonical) and +48.5 / +5.8 (alt).
  - The L200 512³ runs at f ≥ 0.7 give KiDS +5.1 to +7.6 (CFG424 family) and +72.8 / +81.5 (CFG530 L200).
- MUTATE NZ1 (source = 0 reproduces S0) bites: |Δχ²| = 0.

**What would make this diagnostic:** saved snapshots at z = 0.5 and 1 (so the source is not held from z = 0), and boxes that resolve k ≈ 0.02–10 h/Mpc together. For example, L ≥ 400 Mpc/h at N ≥ 1024, or a box ladder.

## 2. Frozen track (criteria a3a22a833): HMcode-2020 × BAHAMAS (T marginalised 7.3–8.3) × R(k)

**Controls pass:**
- **C1 (ΛCDM S8 with S8 free):**
  - KiDS 0.7694 [0.7467, 0.7941] against the released ξ± chain median 0.7656.
  - DES 0.8061 [0.7854, 0.8283] against the recalled 0.772. |Δ| = 0.034 is inside the 0.04 tolerance but on the high side; Ω_m is fixed at 0.314 here.
- **C2 (own projection vs pyccl, same P):** χ² distance 0.017 (KiDS), 0.038 (DES).
- ΛCDM mode A: χ²/N = 1.18 (KiDS), 1.05 (DES).
- Planck S8 tension of ΛCDM in this likelihood: 2.31σ (KiDS), 1.03σ (DES).

**MUTATE:** MU1 bites (R ≡ 1 is exact). MU3 bites. **MU2 FAILS on both surveys:** χ²_min = 1.09; the injected 20% excess is absorbed by T and IA. **So by the frozen rule every framework class of this track is NOT DIAGNOSTIC.**

**The raw Δχ² is reported, not a verdict.** The table gives mode A (cosmology fixed, σ8 = 0.811); in brackets, the raw class the robustness rule would have given. The S8-free column is the best-fit S8 for KiDS / DES.

| model | canonical KiDS / DES | alt KiDS / DES | S8 free: S8 (can.) | S8 free: S8 (alt) |
|---|---|---|---|---|
| PRIMARY (CFG559 kinetic, z = 0) | +21.47 (EXCL) / +3.96 | +41.97 (EXCL) / +6.17 | 0.746 / 0.794 | 0.726 / 0.790 |
| PRIMARY z-scaled (declared s(z)) | +13.32 / +2.56 | +26.03 / +4.22 | 0.756 / 0.793 | 0.741 / 0.793 |
| emergent edge | +21.30 / +1.31 | +21.86 / +2.57 | 0.777 / 0.790 | 0.762 / 0.790 |
| r200m scope | +5.18 / +0.16 | +2.88 / +0.52 | 0.786 / 0.804 | 0.775 / 0.803 |

- **Feedback limit.** In every framework PRIMARY fit, T is pinned at the edge of the allowed feedback range, 8.3. The ΛCDM fits sit at 8.30 (KiDS, also the edge) and 8.20 (DES).
- **With S8 free,** the PRIMARY Δχ² nearly vanishes (+0.18 / +1.40 canonical). But it needs S8 = 0.746 on KiDS. That is 3.7σ below Planck (0.832 ± 0.013, recalled); alt needs 0.726, 5.1σ below.
- **The emergent edge is not a clean survivor here.** Its KiDS Δχ² is +21.3 / +21.9, and with S8 free it is +17.8 / +12.7. Its R < 1 at k ≈ 1 leaves too little power even at T = 7.3.
- **Only r200m scope (alt) is CONSISTENT** in the raw class. It is NOT DIAGNOSTIC by MU2 like the rest.
- **Comparison with CFG590.** CFG590's projected-A shortcut said EXCLUDED. The proper likelihood shows the excess is partly absorbed by T and IA, and the tooth shows this setup cannot exclude a 20% small-scale excess at all.

## 3. Evolving dark energy (Part A, `cfg592_de.py`; context)

- **Background:** DESI DR2 + CMB + DES-Y5 CPL chain, used for both models. The median point is w0 −0.753, wa −0.851. A_s is held at the w = −1 value.
- **Framework:** a0(z)/a0(0) = √(ρ_DE(z)/ρ_DE(0)) = 1.060 / 1.010 / 0.865 at z = 0.5 / 1 / 2. This enters R through its own a0-sensitivity, read from the two footings (p(k = 1) = +1.36 for PRIMARY).
- **The ΛCDM control in the same background:** χ² 267.4–269.1 (KiDS).
- **The w = −1 check reproduces the frozen numbers** to 0.05 in Δχ².
- **Result:** the PRIMARY Δχ² moves only slightly. KiDS goes +21.47 → +20.91 (canonical) and +41.97 → +44.04 (alt). Across the 16th–84th percentile points, canonical KiDS spans +16.7 to +22.1.

## 4. How much each inherited assumption moves the framework's Δχ² (`cfg592_final.out`)

KiDS canonical (alt in brackets):

| change | Δχ² |
|---|---|
| HMcode × R(k), frozen (225 points) | +21.47 (+41.97) |
| … with S8 free | +0.18 (+2.42) |
| … with DESI w0wa + a0 tracking | +20.91 (+44.04) |
| PM-native, no feedback, IA marginalised (20 points) | +23.85 (+30.04) |
| PM-native, no IA | +37.09 (+46.00) |
| PM-native, boost fade bracket | +15.12 (+19.04) |
| PM-native, DESI distances | +18.06 (+23.17) |
| PM-native + BAHAMAS T 7.6 / 8.0 (externally calibrated) | +21.58 / +16.79 (+27.31 / +21.54) |

DES moves the same way at about one fifth of the size (canonical: +3.96 frozen, +4.20 native).

**Summary:**
- The **S8 freedom** is the only assumption that removes the framework's KiDS penalty, and it does so only by moving S8 away from Planck.
- **Evolving dark energy** moves it by 0.6–2; **feedback** (T 7.6–8.0) and **DESI distances** move it by 2–9.
- **Holding the source at z = 0 versus fading it** moves it by about 9–11.
- **IA** moves it by 13–16, in the direction that hurts the framework when IA is switched off.
- The HMcode × R and PM-native routes agree in sign and rough size on KiDS. They use different data subsets, so this is not a like-for-like comparison.

## Inherited ΛCDM-calibrated ingredients (flagged)

1. HMcode-2020 nonlinear model (frozen track).
2. BAHAMAS feedback calibration (frozen track; context only in the native track).
3. Tinker / Duffy / Moster halo-model inputs inside R(k) (CFG556–559).
4. The EH no-wiggle IC spectrum of every PM run (the engines' only ΛCDM input).
5. The PM's flat w = −1 background and Planck-like constants.
6. Survey nuisance priors (SOM photo-z, m, IA prior ranges), calibrated on ΛCDM image simulations.
7. The frozen Planck-like cosmology (Ω_m fixed; massless neutrinos versus the surveys' massive ones).

## Disclosures (dated 2026-10-10)

- KiDS θ-bin averaging uses θ weighting; the pair-count weighting is not available. DES uses NLA, not its fiducial TATT. The shear-ratio and 3×2pt parts are not used. Ω_m is fixed (0.3138), whereas the papers marginalise it; the DES S8 shift of +0.034 is consistent with that.
- The frozen criteria text quoted S8 = 0.8314. With this Ω_m, σ8 = 0.811 is S8 = 0.8294 (used).
- The native track uses particle P at z = 0.5 / 1 from run JSONs.
  - CFG530 L200 N512 has no S0 run JSON, so both models use D² scaling there.
  - Both PM boxes carry their own sample variance at low k, which is not in the covariance; it cancels largely in Δχ² because the ICs are the same.
  - For z > 1, both models use linear-growth extrapolation.
  - CFG527 is matched to the CFG359 S0, as in CFG555.
- Code edits after the main runs, with no effect on results:
  - In `cfg592_like.py`: process count, thread pinning, and a bool cast so the MUTATE JSON writes (the first MUTATE JSON was truncated; it was rerun with identical numbers).
  - In `cfg592_native.py`: the footing-summary label "NOT DIAGNOSTIC (every run)" replaces "MIXED" when every run is NOT DIAGNOSTIC. This is a wording fix, not a rule change. The post-hoc tooth and post-hoc support thresholds were also added; they are labelled and carry no verdict.
- CFG591's R(k, z) was not committed at freeze time and was not used.

## Scripts

- `cfg592_like.py` (frozen): about 45 min with 3 processes.
- `cfg592_native.py` (Part B): about 3 min with 4 processes; `CFG592_MUTATE=1` for the MUTATE runs.
- `cfg592_de.py` (Part A): about 35 min.
- `cfg592_final.py`: the tables, with no new computation.
- Run each with `nice -n 10`.
