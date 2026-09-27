# Deeper data audit: SPT-3G D1 lensing likelihood

**Checked 2026-09-27.** The [official release instructions](https://pole.uchicago.edu/public/data/omori26/likelihoods/overview.html) point to [`spt_candl_data`](https://github.com/SouthPoleTelescope/spt_candl_data), version 3.0.0 or later. I inspected its public checkout at commit `efe35b7bfd815a115d5123e210a6849a4175bc81` (2026-09-01). It contains the actual 17-bin `C_L^(κκ)` vectors, CMB-marginalized 17×17 covariances and window functions for polarization-only (`PP`), minimum-variance (`GMV`) and foreground-profile-hardened (`GMVprof`) estimators. The [original paper](https://arxiv.org/abs/2608.31136) is D12 in this folder's inventory. An exact-paper bandpower/covariance analysis was absent from the repo before this folder; other ACT and Planck lensing work in the repo is not this D1 data product.

## Quantitative audit of the released data

The [audit script](spt_d1_covariance_audit.py) reads the **lensing-only** covariance, checks its symmetry and positive definiteness, and computes each window's effective multipole `Σ_L L W_bL / Σ_L W_bL`. For nested prefixes of the 17 bins it computes `Q_n=d_nᵀ C_n⁻¹ d_n`, with the *measured* bandpowers `d` used as a self-template. `Q_n/Q_17` is a covariance-aware diagnostic of where a fixed amplitude-like signal is measured. It is **not** a theory likelihood, detection significance or a statement that all physical sensitivity lies below the largest effective `L`; the windows have width and the model changes with scale.

| Estimator | First 4 bins, `L_eff,max≈114` | First 8, `L_eff,max≈303` | First 12, `L_eff,max≈790` | Full `Q_17` |
|---|---:|---:|---:|---:|
| Polarization-only (`PP`) | 21.4% | 68.4% | **98.3%** | 838.22 |
| Minimum-variance (`GMV`) | 15.2% | 58.9% | **96.6%** | 1407.88 |
| Profile-hardened (`GMVprof`) | 16.4% | 60.5% | **96.4%** | 1371.52 |

This points to a focused first test: predict the *shape* of the action's lensing spectrum through the first twelve SPT windows, then run the complete official likelihood. A model with a sharp enhancement or suppression near `L≈100–800` cannot hide it merely by fitting small-scale bins. The `PP` estimator gives a separate foreground-resistant estimator of the **same sky**, not an independent observation that can be multiplied with GMV.

The likelihood's [release README](https://github.com/SouthPoleTelescope/spt_candl_data/blob/efe35b7bfd815a115d5123e210a6849a4175bc81/spt_candl_data/SPT3G_D1_KK_v0/README.md) exposes a crucial trap: the published raw bandpowers are **not** to be compared directly with a binned gravity spectrum. The model first applies a 14-parameter systematics/foreground emulator to the binned theory, then additive lensing-response (`N1`) and measured-primary-CMB response corrections. Near its training center the emulator ratio is about `0.86–0.94` by band. Omitting it can manufacture an apparent low-lensing signal. The package applies a Hartlap correction based on 498 simulations and 17 bins. Its lensing-only covariance already propagates primary-CMB uncertainty; using that variant together with a primary-CMB likelihood would double count the primary information. For a joint fit the package supplies a different covariance and theory-driven response variant.

## Reproduce and use correctly

```sh
git clone https://github.com/SouthPoleTelescope/spt_candl_data.git /tmp/spt_candl_data
git -C /tmp/spt_candl_data checkout efe35b7bfd815a115d5123e210a6849a4175bc81
python3 real_research/sol_data_search/spt_d1_covariance_audit.py /tmp/spt_candl_data
```

The script requires NumPy. [Its machine-readable result](spt_d1_covariance_result.json) includes SHA-256 hashes of the nine source files and all effective multipoles; the 564 MB external checkout is not copied into this repo. The source files are public and the result can be recreated from the pinned commit.

**Action-level gate:** derive `C_L^(κκ)` from the same action that yields its structure growth and galaxy lensing, including `Φ+Ψ`, early-time normalization and nonlinear effects. Pass it through the 17 official windows, the estimator-specific nuisance and response terms, and the correct covariance. The present construction does not yet supply a validated spectrum for that operation, so these released bandpowers are a concrete next test rather than a pass or failure. The release's [map documentation](https://pole.uchicago.edu/public/data/omori26/maps/overview.html) still says the lensing maps are forthcoming; map access is unnecessary for the released bandpower likelihood.
