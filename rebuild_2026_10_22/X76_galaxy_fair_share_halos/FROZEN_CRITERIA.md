# X76_galaxy_fair_share_halos: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** X74_smooth_core_lensing and X75 found route E's galaxy halos too light at 50–300 kpc: 0.3–0.5 dex short
for lensing and 0.6–0.8 dex for satellites. In both, M200 came from EM1's SPARC relation. The clusters use a different,
native rule (X30 prep, X43/X73): the halo holds the fair share of cold dark energy,

    M_fair = R_nat · M_b,tot,

distributed with the core Σ = max(Σ_a0, ηΣ_coll) out to the self-consistent turnaround radius

    r_ta = [3 (Ω_m/Ω_b) M_b,tot / (4π · 5.55 · ρ_m)]^{1/3} / (1+z).

Does that same rule, applied to galaxies, supply the mass that lensing and satellites need? Nothing is fitted.

## The rule for galaxies (PRIMARY)

- **Baryons:** M_b,tot = M★ + M_cold + M_hot, F2's inventory, with M_hot = 0.5 M★ in total. The hot gas profile stays
  F2's, (r/100 kpc)³ capped.
- **Normalisation:** native as X73 and GS1: h 0.6856427, Ω_m 0.2976016, ω_b 0.0223081, giving R_nat = (Ω_m − Ω_b)/Ω_b
  ≈ 5.27. ρ_m is the native mean density.
- **Halo mass and edge:** M_fair = R_nat · M_b,tot inside r_ta, truncated at r_ta (no R200).
- **Core:** Σ = max(Σ_a0, η(c_f 4)·Σ_coll(M_fair + M_b,tot)) with X70/X73's smooth shape, η × B1/B_S(1).
- **Redshift for r_ta:** z = 0.285 for KiDS lenses (X53's z_eff); the median host z for GAMA satellites.

## Pre-registered expectation (written before any number)

At log M★ = 10.9, M_b,tot ≈ 1.3e11, so M_fair + M_b ≈ 8e11 spread to r_ta ≈ 0.8 Mpc. That is below EM1's SPARC M200
(~1e12.05) and more extended. **I expect the fair-share rule to supply less mass inside 300 kpc than the SPARC
relation, and so to fail both probes, worse than SPARC.**

## Grading

**Lensing (X53 harness, unchanged rule):**
- Δχ²(H2H − L2H) and X53's class, all radii and primary, both footings;
- compared with X74_smooth_core_lensing's SPARC halos (+423.7 / +458.4).

**Satellites (X75 harness, unchanged measurement):** the X75 frozen sample's measured σ, both footings:
- χ² at budget multiplier 1;
- the best common log multiplier m on M_b,tot over a grid of −0.5 to +1.7 dex, with its Δχ² = 1 range.

**Lensing profile (reported):** the same multiplier profiled through X53's A1 machinery (common m, with 2h, truncated
at r_ta).

## Verdict (per footing)

- **FAIR SHARE SUPPLIES THE MASS** if the satellite m is consistent with 0 within 2σ and lensing Δχ²(H2H − L2H) on all
  radii is below X74_smooth_core_lensing's SPARC value.
- **FAIR SHARE FALLS SHORT: needs m = …** otherwise. The needed multiplier is reported per probe: this is the baryon
  budget, including undetected CGM, that the rule would need.

## Checks

- **K1:** with the fair-share switch off, the halo masses equal X74_smooth_core_lensing's smooth halos exactly.
- **K2:** r_ta(M) reproduces X30's r_ta_com formula at native parameters for a test mass to 1e-12.
- **K3:** the halo mass solved to r_ta equals M_fair to 1e-8 (unsaturated) for a test lens.
- **MUTATE:** m = +1 must raise both the predicted σ and ΔΣ at 100 kpc.

κ = ½ FITTED; c_f EXTERNAL; footings never pooled; cold dark energy is a gravitating field component, never a particle;
not theory closed; nothing here says the data favour the framework. One thread, nice 15.
