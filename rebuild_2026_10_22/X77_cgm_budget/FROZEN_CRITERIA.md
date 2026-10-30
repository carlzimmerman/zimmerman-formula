# X77_cgm_budget: FROZEN CRITERIA (committed alone, before any graded number)

**Question.** X76 showed that the clusters' fair-share rule needs a galaxy's baryon budget M_b,tot multiplied by
10^m to match the outer data:
- satellites (X75 data), per bin: m = +1.25 (log M★ 10.6–10.8) and +1.30 (10.8–11.0), canonical;
- lensing (KiDS, A1 profile, all radii), per bin: m = +0.90 and +0.85, canonical.

The owner chose to test whether an undetected hot circumgalactic medium (CGM), counted into the budget out to the
self-consistent r_ta exactly as the clusters count measured gas (GC2/GS1), can supply that.

## Measured input (verified from the paper's TeX source, not a web summary)

Zhang et al. 2024, A&A 690, A267 (arXiv 2401.17308): eRASS:4 stacks of SDSS centrals.
- Source: `_external_data/arxiv_src/2401.17308/e-print.tar.gz`, sha256 8e0a0305…63d46bf, fetched 2026-10-29 with
  the owner's OK.
- **MW-mass bin (log M★ 10.5–11.0, median M★ 5.5e10):**
  - f_b,hot+star(<R_vir) = 0.12 ± 0.06, with M_vir = 1.3e12 and T_vir = 0.22 keV;
  - β = 0.43 (+0.10 / −0.06), r_c = 6 kpc (Table 4).
- **M31-mass bin (11.0–11.25, median M★ 1.3e11):**
  - f_b = 0.07 ± 0.02, with M_vir = 4.2e12;
  - β = 0.37 (+0.04 / −0.02), r_c = 4 kpc.
- **R_vir (Table 1, interpolated in log M_h):** 196 kpc (MW-mass) and 281 kpc (M31-mass).
- **Hot CGM inside R_vir:** M_hot = f_b M_vir − M★, i.e. 1.01e11 ± 0.78e11 (MW-mass) and 1.64e11 ± 0.84e11 (M31-mass).
- **Disclosed:** the R_vir aperture and M_vir come from the paper's ΛCDM/Moster SHMR. They are used only as the
  aperture and normalisation the measurement is reported in, never as a model input. T = T_vir and Z = 0.3 Z☉ are the
  paper's case.

## Budget rule (PRIMARY, nothing fitted)

- **Profile:** ρ_hot ∝ [1 + (r/r_c)²]^{−3β/2}, normalised to M_hot(<R_vir), and extrapolated without a cut.
- **Budget:** M_b,tot(r) = M★ + M_cold + M_hot(<r), with M_cold from F2's relation. The stars and cold gas are taken
  at the bin's median M★.
- **Turnaround radius:** solved self-consistently, r_ta = X76's `rta_pc(M_b,tot(r_ta), z)` at the X75 median host
  z = 0.1797 (native).
- **Achieved multiplier:** m_CGM = log10[M_b,tot(r_ta) / (M★ + M_cold + 0.5 M★)], i.e. relative to X76's observed
  budget.

**Graded for the MW-mass bin,** which spans X75/B21 bins 3–4 (log M★ 10.6–11.0). Needed m: satellites +1.25 / +1.30;
lensing +0.90 / +0.85. Use the smaller of each pair, +1.25 (satellites) and +0.85 (lensing). The M31 bin is reported
only.

**Edges:**
- *generous:* f_b + 1σ (0.18) and β − 1σ (0.37), the shallower profile;
- *tight:* f_b − 1σ (0.06) and β + 1σ (0.53).

## Verdict (frozen)

- **CGM BUDGET SUPPLIES THE MASS:** central m_CGM ≥ +1.25 (satellites and lensing both met).
- **CGM BUDGET SUPPLIES LENSING ONLY:** +0.85 ≤ m_CGM < +1.25 at central.
- **CGM BUDGET ONLY AT THE GENEROUS EDGE:** central m_CGM < +0.85, but the generous edge ≥ +0.85.
- **CGM BUDGET EXCLUDED:** the generous edge m_CGM < +0.85.

**Reported:**
- r_ta, r_ta/R_vir, and the fraction of M_hot(<r_ta) lying beyond R_vir (pure extrapolation; Zhang measure only out to
  R_vir);
- the M31 bin;
- the 3 R_vir closure check (their R_c ≈ 3 R_vir).

## Scope and disclosures (frozen)

- **A budget test, not a profile regrade.** The extra CGM mass is not added to the gravitating profile beyond X76's
  0.5 M★. An honest pass would need a full X75/X53 regrade with the gas included.
- **The reservoir is mostly extrapolation.** Zhang detect the CGM only to R_vir; most of any reservoir out to r_ta
  lies beyond what is measured.
- κ = ½ FITTED; c_f EXTERNAL; footings never pooled (this is a canonical-footing budget; X76's alt needs are within
  0.05); cold dark energy is a gravitating field component, never a particle; not theory closed.

## Checks

- **K1:** the β-profile mass integral matches the closed form ∫4πr²ρ dr by quadrature to 1e-8.
- **K2:** the r_ta fixed point satisfies r_ta = rta_pc(M_b,tot(r_ta)) to 1e-10.
- **K3:** with M_hot(<r) ≡ 0.5 M★ (X76's inventory), m_CGM = 0 exactly.
- **MUTATE:** setting β = 0.25 must raise m_CGM.
