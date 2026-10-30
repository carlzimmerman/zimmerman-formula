# GH8_ksz_velocity_hardened: FROZEN CRITERIA (committed alone, before any hardened velocity exists)

**Why.** GH7's positive control fell short (S/N 3.81 vs 4), so its MW-mass shortfall is void. This lane improves the velocities and
the control's filter, re-runs the control first, and looks at MW-mass centrals only if it passes.

**One round only.** The MW-mass stack from GH7 has already been seen (A(1.8) 0.07 ± 0.14 at R 0.724), so these changes are not blind to
it. To limit forking: the changes below are fixed in advance, none is tuned on results, and **if the control fails again, kSZ with the
DR1 pipeline is closed and no further hardening is tried.**

## Data (nothing new fetched)

GH7's map, lenses and apertures (`gh7_lenses.npz`, `gh7_cap.npz`). All BGS with masses in `gh6_bgs.npz` as tracers.

## Hardened velocities

1. **Mesh 6 Mpc/h** (8 in GH7), CIC read (nearest cell in GH7). Smoothing stays 12.5 Mpc/h.
2. **Randoms by photometric region:** north (Dec > 32.375 and RA 90–280) and the rest each get their own sky-count map and z pool, 10× the data.
3. **RSD removed iteratively:** three iterations of x = s − (ψ(x)·r̂) r̂, where ψ already carries β. The lens is read at its corrected position.
4. **β = 0.44 stays INHERITED, not native.** A scales as β_true/0.44.

## Calibration R

Lognormal catalogue mock: input P(k) is iterated twice so that the mock's measured redshift-space P(k), through the same mask and mesh,
matches the data's. Particles are drawn per cell, displaced by their linear v_los, then pushed through the identical iterated reconstruction.

- **R_fm** = Cov(v_true, v_rec)/Var(v_rec) from this mock: PRIMARY. r_mock is an upper bound (no sub-mesh velocity); R is not affected by
  uncorrelated small-scale velocity.
- **R_cut:** the same with the input P(k) below k = 0.02 h/Mpc replaced by a power law through k 0.02–0.05, in case low-k data power is
  systematic.
- **R_ctx** = 0.64 × 300 km/s / data rms v_rec (context only).
- A class that differs across the three is **R-LIMITED**, which is not a result.

## Estimator

GH7's, plus inverse-variance weights: w_i(θ) = 1/variance of CAP(θ) among lenses in the same nside 8 pixel, or the global variance if the pixel has
< 500 lenses. T̂(θ) = −Σ w c u / Σ w u². Means are removed in 10 z bins; covariance and σ come from velocity shuffles.

## Positive control (runs first)

- All BGS, no central cut, z 0.1–0.5, log M★ > 10.5, 11, 11.25.
- Matched filter with each sample's own (z, lm) cells: Zhang's profile shape at k = 1.8, using R_vir from Table 1 for that lens's mass, rather than GH7's fixed MW-mass shape.
- **Rule, same threshold as GH7: best S/N ≥ 4 validates. Below 4: lane ends VOID, MW-mass centrals are not re-stacked.**

## MW-mass verdict (only if validated; as GH7, PRIMARY A(1.8) at R_fm, shuffle σ)

- **GAS DETECTED:** A(1.8)/σ ≥ 3 and shuffle p < 0.003.
- **BELOW ROUTE E'S NEED:** A(1.8) + 2σ < 1 (2σ using the larger of the shuffle and jackknife errors).
- **INCONCLUSIVE:** otherwise.
- **Normalisation lock:** if A(1) is also below 1 by more than 2σ, the BELOW class is worded "below Zhang-normalised gas at every extent"; the shortfall then
  concerns the X-ray normalisation or the column, not extension past R_vir.
- **Extent** is claimed only if S(1.8 − 1) ≥ 3 at all three R and the GH7 extent rules agree across them.

## Checks

- **K1:** at the real settings, iterated reconstruction on the mock gives r no lower than no iteration.
- **K2:** the mock's measured P(k) matches the data's within 10 % over k 0.03–0.3 after matching.
- **K3:** mock r_mock > 0.3, correct sign.
- **K4:** per-lens model injection into the control recovers A = 1 within 2 %.
- **MUTATE:** v → −v flips T̂ exactly; shuffled stack is a null (p > 0.01). The control with shuffled velocities gives |S/N| < 3.

**Scope.** Two-halo adds to any signal; a control detection does not calibrate amplitude; published work on DR2 is context only. κ = ½ FITTED; c_f EXTERNAL; cold dark energy
is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework. One thread, nice 15, RSS < 6 GB.
