# Session 2 calcs: results (2026-10-06)

Criteria: `FROZEN_CRITERIA.md`. The main section and Addenda F, D and S were each written before their scripts ran. κ = ½ fitted; both footings. No dark-matter particle; the cold mass is still required. **Nothing here is committed by me** (`ai_slop/` is the owner's). Every number below is printed by the script named.

| test | script | verdict | key numbers |
|---|---|---|---|
| C0 literature | (arXiv API abstract, 2203.05750) | applies to a granular (virialized) fluid halo | Dalal & Kravtsov 2022: m > 3e-19 eV at 99%, 7–15× above the light end |
| G0 ambient MW-fluid heating | `ufd_soliton_test.py` | PASS | worst Δσ² = 3.9e-7 (km/s)² over 10 Gyr |
| T1 scaling regression (31 UFDs) | `ufd_soliton_test.py` | **soliton-traced DISFAVOURED**; harmonic core DISFAVOURED; law shape allowed | b = −0.16 ± 0.22, c = +0.14 ± 0.13; Mahalanobis: law 1.88, soliton 6.23, core 6.32, ΛCDM-cusp 3.32 (reported) |
| T2 implied field mass | `ufd_soliton_test.py` | **FAIL** | median m = 3.9e-21 eV (16–84%: 1.7e-21 – 9.0e-21); 1/31 in window; log-m scatter 0.38 dex |
| T3 free soliton (reported) | `ufd_soliton_test.py` | — | at 2e-20 eV: r_c ≈ 8.5 pc, M_sol ≈ 6.5e5 M☉, r_c/λ ≈ 0.05 |
| MUTATE (ρ_c ×10) | `ufd_soliton_test.py --mutate` | detected, exit 1 | K3 ratio 10.0 |
| F fossil-phantom switch | `fossil_switch.py` | **FAIL** | nominal yield: −0.18 / −0.19 dex at 2e-20 (−2.1 / −2.3σ); +0.16 / +0.14 at 4.4e-20 |
| F post-hoc (reported) | `fossil_posthoc_scatter.py` | — | the switch raises the resolved scatter from 0.20 to 0.33–0.39 dex; the median crosses zero near 3.7e-20 eV (a one-parameter fit, not a test) |
| D SPARC a₀ by distance method | `sparc_a0_by_distance.py` | not significant | flow − ladder = +0.151 ± 0.084 (1.8σ, Υ 0.5); +0.113 ± 0.093 (1.2σ, Υ 0.7) |
| D MUTATE (ladder g_obs ÷ 1.2) | `--mutate` | detected, exit 1 | Δ moved +0.21 / +0.22, not the frozen +0.158 (see disclosures) |
| S super spirals vs retention levels | `super_spirals_retention.py` | all 23 GALAXY-LEVEL; nine fastest BETWEEN | f = 0.160 ± 0.061 (all), 0.485 ± 0.238 (nine fastest, canonical); alt 0.143 / 0.460 |
| S MUTATE (no phantom) | `--mutate` | detected, exit 1 | nine-fastest f +0.187 |
| S post-hoc (reported) | `super_spirals_posthoc_corr.out` | — | Spearman f vs V = +0.70 (p 2e-4). **Shared-variable warning:** V enters both f and the axis |

## Disclosures (fixes and departures, none changing a frozen threshold)
1. **D, bootstrap count** cut from 1000 to 500/200 after the first launch timed out with no output written.
2. **D, H₀-null sign.** The frozen formula had the sign wrong. a₀ ∝ D⁻² ∝ H₀² for Hubble-flow distances, so the corrected value is H₀_null = 73 × 10^(−Δ/2) = 61.3 (Υ 0.5) / 64.1 (Υ 0.7). The MUTATE run then showed the estimator's real distance response is about D^−2.7, not D⁻² (most SPARC points are not deep-MOND). With the measured exponent, H₀_null ≈ 64.7 / 66.4, so Planck-like H₀ would reduce Δ to +0.06 / +0.02. Neither Δ is significant, so none of this is an H₀ measurement.
3. **D, MUTATE.** Exit 1 came from the frozen expectation (+0.158 ± 0.02) being wrong, not from a broken control. The mutation is detected (Δ moved +0.21).
4. **S, enclosed mass.** v1 divided by the *total* M_b, which is not cm08's definition (enclosed in the aperture). That made MUTATE fail to detect (+0.013). Fixed to the Newtonian-equivalent enclosed mass g_N r²/G from CFG56's own bulge + disc g_N. The frozen text ("cm08's definition exactly") is unchanged.
5. **S, bootstrap.** M_law is rescaled with M_b as √M_b inside the bootstrap (a declared approximation).

## What this settles
- **The light-end soliton idea for the ultra-faints is dead.** The data reject its scaling (6.2 in the fit metric). If the stars traced a soliton, the implied mass would be 3.9e-21 eV, which is outside CFG367's window and 80× below the Dalal–Kravtsov bound.
- **The fossil-phantom switch is dead.** It fails as frozen and nearly doubles the scatter.
- **The ultra-faints follow the law's *shape*** (σ independent of r_half, σ ∝ M★^0.14±0.13 against 0.25) **with a +0.35 dex offset.** This is a normalisation failure, not a scaling failure. The ΛCDM cusp row is also allowed (3.32 against the 3.44 line), so the shape does not separate the law from ΛCDM.
- **SPARC shows no significant distance-method systematic** in a₀ (1.2–1.8σ).
- **Super spirals:** the 23 as a whole sit at the galaxy retention level (0.16). The nine fastest sit between the two levels, closer to 0.6. f rises with V, but V is on both sides of that correlation, and ΛCDM also predicts more dark mass in more massive discs. This is consistent with a temperature- or mass-keyed step and confirms nothing.
