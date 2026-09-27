# New bounded calculation: DESI Lyα geometry versus the Unite central background

**Date:** 2026-09-27. **Contract:** Take the two published DESI DR2 Lyα full-shape distances at `z=2.33` and their reported correlation, and compute the Alcock–Paczyński shape that follows from the *central* flat CPL parameters in the newly published Unite paper. This is a conditional background check. It does not fit raw spectra or supernovae, infer an acceleration law, or test the unfinished gravity action.

## Primary inputs

- [DESI DR2 Results IV, Eq. 26](https://arxiv.org/html/2607.27410v3): `D_M/r_d=39.32±0.33`, `D_H/r_d=8.600±0.066`, correlation `ρ=0.225`, at `z_eff=2.33`. The [data availability section](https://arxiv.org/html/2607.27410v3) says the underlying analysis data will be made public with DR2. These summary data are already enough for the restricted shape check.
- [Unite v2 abstract](https://arxiv.org/abs/2609.05053v2): central flat-CPL values `(Ω_m,w_0,w_a)=(0.305,-0.861,-0.60)`. Its Hubble diagram and likelihood are promised upon acceptance and were unavailable at this check. The same abstract reports asymmetric *marginal* errors; no joint parameter covariance is provided there.

## Equations and method

For a spatially flat matter+CPL background with `w(z)=w_0+w_a z/(1+z)` and negligible radiation in this limited calculation,

```text
X(z) = ρ_DE(z)/ρ_DE(0)
     = (1+z)^[3(1+w_0+w_a)] exp[-3w_a z/(1+z)]
E(z)^2 = Ω_m(1+z)^3 + (1-Ω_m) X(z)
I(z)   = ∫_0^z dz'/E(z')
D_M/r_d = q I(z),      D_H/r_d = q/E(z),     q = c/(H_0 r_d)
F_AP = D_M/D_H = E(z) I(z).
```

The sound horizon and Hubble normalization cancel in `F_AP`. I integrate `I` by composite Simpson quadrature. For a more faithful use of the reported two-dimensional measurement, [the script](lyalpha_shape_check.py) minimizes `χ²=(d-qv)^T C^-1(d-qv)` analytically over the one nuisance scale `q`, using `C_12=ρ σ_M σ_H`. That leaves one descriptive shape degree of freedom for **fixed** model parameters. The script also propagates the distance covariance to the observed ratio for orientation.

## Reproducible result

Run `python3 real_research/sol_data_search/lyalpha_shape_check.py`; [JSON output](lyalpha_shape_result.json) records all numbers.

| Fixed background shape | Predicted `F_AP` | Profiled `χ²` for the DESI distance pair |
|---|---:|---:|
| DESI observed | `4.57209 ± 0.04580` (linear covariance propagation) | — |
| Unite central `(0.305,-0.861,-0.60)` | `4.47766` | `4.329` |
| Flat ΛCDM at the **same** `Ω_m=0.305` | `4.51944` | `1.335` |
| Flat ΛCDM at DESI's reported Lyα-only central `Ω_m=0.325` | `4.57242` | `0.00005` |

The Unite central trajectory is `0.09443` below the measured ratio. Its scale-profiled conditional `χ²=4.329` would correspond to `p≈0.037` for one Gaussian shape degree of freedom **if the Unite parameters were exact and the data were an independent Gaussian check**. Neither condition holds: Unite's parameter covariance is missing, it uses DESI BAO inputs that overlap the Lyα analysis, the Lyα likelihood is more detailed than the summary Gaussian, and this sandbox calculation omits radiation/other fitted ingredients. **This is a targeted sensitivity flag, not a 2σ contradiction or a new joint model preference.** The ΛCDM `Ω_m=0.325` control nearly reproduces the published ratio, which checks the distance convention and arithmetic.

The 4096-versus-8192-panel Simpson difference in `F_AP` is `1.24e-14`, far below the published precision. This verifies numerical convergence of the restricted integral; it says nothing about model-systematic or posterior uncertainty.

## How this helps closure

The new AP summary creates a sharp, sound-horizon-free target for any proposed FLRW background. A candidate action must yield `H(z)` and therefore `F_AP(z)`; the DESI pair can then reject incompatible backgrounds without first assuming a dark-energy density or an `a0(z)` law. A complete theory test also requires the action's perturbation/lensing predictions. The optional `a0∝√ρ_DE` bridge is not assumed here, and this calculation cannot certify or refute the 13-requirement theory.

Next analysis gate: release or obtain the DESI full-shape likelihood and Unite covariance/likelihood, define a common dataset with the shared DESI BAO correlations removed or modeled, and compare *posterior predictive* `F_AP` distributions from explicit action solutions. Until then the central-value mismatch must remain conditional.
