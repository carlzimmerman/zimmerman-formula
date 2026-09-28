# CFG8 — FG001's one cost: Chae's external-field signal, refit under the framework's own law

Script: `CFG8_chae_kernel.py`.
- Outputs: `CFG8_chae_kernel.out` and `CFG8_chae_kernel_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. It injects a field of 0.05, which is recovered at 12.6σ (rc = 1).
- Committed in 302ff4bd9.

κ = ½ is fitted. Both a₀ footings are used.

## What was done

All 153 SPARC galaxies of Chae et al. 2020 (i ≥ 30°, Q ≤ 2) were refit with his exact priors and likelihood.
- **Priors:** Υ_disk, Υ_bulge, Υ_gas, distance and inclination, as in his Table 1.
- **External field:** e uniform on [−0.5, 0.5].
- **Law:** his eq. 6, extended to any law by the same 1-D AQUAL construction: ν_e(z; e) = [F(z + z_e) − e]/z, with F(Z) = ν(Z)Z and e = F(z_e).
- **Sampler:** an in-house affine-invariant ensemble sampler.
- **The seven laws:**
  - V1: the simple function at Chae's g†;
  - V2: the RAR at g†;
  - V3: the simple function at the canonical a₀;
  - V4 and V5: P2 at the canonical and alt a₀;
  - V6 and V7: ν_mono at the canonical and alt a₀.

## Results

| check | result |
|---|---|
| C0: the general form equals his eq. 6 for the simple function | 3.5e-13, pass |
| C2: his own numbers | low-acceleration median +0.041 (his 0.052 ± 0.011); NGC 5055 +0.053 (0.054); NGC 5033 +0.104 (0.104). Pass |
| C1: single-realization recovery | **failed as declared** (NGC 5055 −1.26σ). The threshold ignored the realization's own 1σ scatter. C1b, noiseless and labelled, shows the sampler unbiased to ≤ 0.08σ |
| H1: under the framework's law the median e lies within 2σ of zero | **failed**. P2: +0.021 (1.7σ) canonical, +0.032 (2.7σ) alt. ν_mono: +0.034 (2.2σ) canonical, +0.041 (3.0σ) alt |
| H2: the fitted e is uncorrelated with his independent environmental field | pass under every law, his own included (Spearman p 0.57–0.87). The weighted slope, 0.55–0.87 ± 0.25, rests on a few precise galaxies |
| R2: the low-acceleration RAR downturn at SPARC's nominal mass models | V1 −0.076; V4 (P2, canonical) −0.007 ± 0.007; V6 −0.036; V7 −0.066 |

## Standing

The cost is reduced, not removed.
- At the canonical footing the framework's own law brings Chae's signal to 1.7–2.2σ, and his downturn vanishes under P2.
- The alt footing keeps 2.7–3.0σ.
- No law produces an environmental rank correlation.
- NGC 5055 and NGC 5033 want a field under every law, and they carry the weighted slope.
