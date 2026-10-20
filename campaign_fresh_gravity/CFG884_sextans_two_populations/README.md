# CFG884 — Sextans' two stellar populations against one finite cold clump

Criteria: `FROZEN_CRITERIA.md` (eb5c21709, committed alone before the script; owner block 880–889).
Run: `OMP_NUM_THREADS=1 python3 cfg884.py` (`CFG884_MUTATE=injectC|injectX` → separate `*_MUTATE_<mode>.*` outputs). About 11 s,
one core, ~130 MB. κ = ½ fitted; ν_e; footings never pooled; no dark-matter particle; not theory closed.

## Question
Sextans has a compact, colder metal-rich population (MR) and an extended, hotter metal-poor one (MP). Does one CFG877 finite
cold clump supply the potential both need, or does MP need extended extra mass?

## Inputs
**Populations — PROVISIONAL.** Tolstoy et al. 2025 Table 2, from another session's web-tool extraction, copied into
`inputs_tolstoy2025_table2.json`:
- MR: Rh 0.339° (circularized a = 428 pc at 84.7 kpc), σ 7.0 ± 0.4 km/s;
- MP: Rh 0.62° (a = 783 pc), σ 10.5 (+0.8/−0.7) km/s.

**Stars.** LVD Sextans, L_V = 2.56e5 L_⊙ at 84.7 kpc, Υ_V 2 (bracket 1–3), no gas. The stellar mass is laid out as two
Plummer spheres in the populations' 0.63/0.37 proportions; the LVD single Plummer is a grid variant.

**Models (no refit; the extra component adds linearly to the law, as in CFG870/877):**
- (L) law alone;
- (C) law + CFG877 clump (M_cl 5.25e6 / 4.24e6 M_⊙, capped at 237 / 205 pc);
- (X) law + CFG870 uncapped cored component (V_x 10.65 / 10.59 km/s, r_c 104 pc).

**Prediction.** Constant-β spherical Jeans for each Plummer tracer, averaged over the projected profile.
- **Primary: whole population.** This is exactly β-independent, since it equals (1/3)∫4πr³ν g dr for any spherical g.
- **Lenient nuisance grid:** Υ, geometry (circularized or major axis), distance ±0.1 mag, aperture (1.0°, 1.5°, ∞), stellar
  profile, β ∈ {−0.5, 0, +0.3} and Rh ± 1σ.
- **Statistic:** z = ln(σ_obs/σ_pred) over the split error, plus a 0.05 floor.

## Result — CLASS: **CLUMP SHORT, EXTENDED MARGINAL** (canonical, the headline); alt: SEXTANS NEEDS EXTENDED MASS

| σ_pred (km/s), whole population, Υ 2, circularized | MR (obs 7.0 ± 0.4) | MP (obs 10.5 +0.8/−0.7) | MP z, full grid |
|---|---|---|---|
| L law alone, canonical / alt | 4.03 (z +7.2) / 4.22 (+6.5) | 4.56 (+9.8) / 4.78 (+9.3) | ≥ +7.2 / ≥ +6.7 |
| **C finite clump**, canonical / alt | 5.57 (+3.0) / 5.49 (+3.1) | **5.46 (+7.7) / 5.50 (+7.6)** | **+5.5 to +9.5 / +5.3 to +9.5** |
| X extended component, canonical / alt | 7.17 (−0.3) / 7.25 (−0.5) | 7.59 (+3.8) / 7.69 (+3.65) | +2.17 to +4.6 / +1.97 to +4.5 |

**Reading:**
- **One finite clump is robustly too small for Sextans.**
  - At every point of the lenient grid, model C under-predicts MP by at least 5.3σ on both footings. Its maximum is
    6.6 km/s against 10.5.
  - At the primary point it also under-predicts MR, by ~3σ (5.57 against 7.0); this is not robust (1.6σ at the lenient end).
  - This confirms, with full Jeans moments, the CFG877 audit's single-population shortfall (×3.7 M_cl in the Wolf form).
- **The CFG870 extended form fits MR but not MP.**
  - At the primary point X sits on MR (z −0.3) and under-predicts MP by 3.8σ (3.65σ alt).
  - It never over-predicts MR anywhere in the grid (z −1.7 to +0.5).
  - It reaches MP only in the grid's extreme corner, with every lenient choice at once: Υ 3, far distance, 1° aperture, LVD
    stellar profile, opposite anisotropies (MR β −0.5, MP β +0.3, the latter violating the An–Evans cusp condition) and
    Rh ± 1σ.
  - There the alt footing scrapes under 2σ (|z| 1.986), which makes the alt class SEXTANS NEEDS EXTENDED MASS. The canonical
    footing does not (best 2.17), so it is CLUMP SHORT, EXTENDED MARGINAL.
- **Why the extended form struggles: the MR/MP contrast.**
  - For any flat-V_c component, a Plummer tracer's whole-population σ²_los is V_c²/3 whatever its size. X adds about the
    same ~35–37 km²/s² to both populations.
  - The observed σ² ratio is 2.25. MP needs a circular velocity that still rises between ~0.4 and ~2 kpc.
- **Global check (reported):**
  - the model mixtures are L 4.2, C 5.5 and X 7.3 km/s against the measured FLAMES global 8.3 ± 0.3;
  - the observed population mixture is 8.47.
- **EFE variant (reported):** applying the MW field (CFG820 form, g_ext = 0.011 a0) halves the law's dispersion and lowers every
  prediction (C: MP 3.6 km/s; X: MP 6.4). So the isolated law is the lenient choice, as frozen.

## Required-mass diagnostic (reported; whole population, central values; extra mass's gravity added linearly in Newtonian form)
- **On top of the law alone (circularized):**
  - MP alone needs ≥ 4.9e7 M_⊙ (9.3 M_cl).
  - Both tracers together need ≥ **6.4e8 M_⊙ = 122 M_cl**, with mass reaching ≥ 1.67 kpc.
  - Alt: 7.6e8 M_⊙ = 181 M_cl, ≥ 1.81 kpc. Major-axis geometry: 7.5e8 / 8.9e8.
  - These use the sharp two-tracer floor from the CFG853 packet, whose numbers K3 reproduces with that packet's inputs.
- **On top of law + clump, no finite positive extra-mass profile fits both central values.**
  - The residual ratio R = 8.2 (7.8 alt) exceeds the limit h³ = 6.1 that even mass at infinity cannot pass. The clump already
    uses up most of MR's room.
  - Such a profile becomes possible only if σ_MR ≥ 7.42 km/s (7.36 alt), i.e. ~+1σ.
  - This is a central-value statement, not an error-weighted exclusion. It suggests the missing mass must be spread out
    rather than added on top of a compact core.

## Controls
- **K1a PASS:** the kernel reproduces the analytic isotropic Plummer-in-Plummer aperture average to ≤ 4e-12 at X = 0.5, 1, 3
  and ∞.
- **K1b PASS:** the whole-population value is the same for β = −0.5, 0 and +0.3 (4e-12). At R_max = 50a the three β agree
  to 1.7e-6.
- **K1c PASS (CFG877 identity):**
  - M_cl matches `cfg877_results.json` (≤ 4e-16);
  - the cap radius is 237.2 / 204.6 pc (the audit's 237 / 205);
  - a re-implementation of CFG876/877's Wolf-form Sextans prediction equals the stored 5.565162739890 / 5.533173671715 km/s
    (≤ 9e-16).
- **K1d (reported):** the Jeans whole-population σ² is within 3 % of the Wolf form g(r12) r12/3 (ratios 0.997–1.029).
- **K1e (added after freezing, reported):** an independent brute-force nested quadrature of the anisotropic Jeans projection
  inside R_max = a agrees with the kernel to 1e-11 for β = −0.5 and +0.3.
- **K3 (reported, external):** CFG853's law-baseline moments and two-tracer floor are reproduced with that packet's inputs
  to ≤ 8e-8.
- **MUTATE, required behaviour met:**
  - injectC (σ_obs := model C's prediction) gives FINITE CLUMP CONSISTENT on both footings, so the class flips.
  - injectX gives X matches on both footings and is not BOTH FORMS FAIL. Its classes come out as canonical FINITE CLUMP
    CONSISTENT and alt UNDECIDED, because the lenient grid lets C reach X-like dispersions within 2σ.
  - The real MP value (10.5) is far beyond that reach.

## Disclosures
- **Provisional inputs:**
  - The population numbers are a web-tool extraction never checked against the publisher's table.
  - They are elliptical number-density fits and Gaussian widths of a selected 303-star sample, not complete spherical virial
    moments. The Jeans tracer density is taken equal to the sample weighting.
  - No radial coverage was available, hence the aperture variants.
  - One LVD ellipticity is used for both populations.
  - The 0.63/0.37 number fractions are read as stellar-mass fractions.
- **Not modelled:** membership, binaries (they inflate σ; none is subtracted), instrument offsets, Sextans' tidal history
  and non-equilibrium.
- **Seen before freezing:** CFG853's numbers and the hand estimates (C MP ≈ 5.1, X MP ≈ 7.4 km/s, disclosed in the criteria).
  The outcome matches those estimates.
- **Post-freeze additions, all reported and none affecting a class:** K1e, the "closest shared point" print, and the σ_MR
  threshold line.
- **Construction:** the extra component's gravity is added linearly (CFG870/877's construction), not passed through ν_e. A
  reading where cold energy's gravity is boosted by the law would need less mass and is not tested.
- **Scope:** Sextans is one galaxy. This bears on whether one universal finite clump suffices; it does not derive the
  missing mass.
