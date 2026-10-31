# GH10_dr2_ksz_published_points: FROZEN CRITERIA (committed alone; array names and shapes listed, no kSZ value read)

**Question.** GH8/GH9's DR1 stack has a marginal control. Hadzhiyska+ 2026 (arXiv:2604.19745) published DESI DR2 × ACT DR6 kSZ profiles with covariances at S/N 7–9. Using only those points, **is the gas around log M★ 10.5–11 galaxies at the level route E's lensing rescue needs (Zhang's gas to 1.8 R_vir)?**

## Data

- `_external_data/desi_dr2_ksz_zenodo/` (zenodo.19160138, owner OK). Real-space profiles `Fig6_BGS_BRIGHT-20.2_logm*.npz` (R, th, prof, yerr, cov); ratio to lensing `Fig8_*`; mass histogram `Fig2`; z histogram `Fig3`.
- Published fiducials as stated in the paper: T̂ = −(1/r)(σ_rec/c) Σ T v_rec/c / Σ (v_rec/c)², CAP = disc − equal-area ring, μK arcmin², hILC map, 1.6′ beam, σ_true 300 km/s, r 0.64.
- **Not native, stated in advance:** these points inherit Planck 2018 reconstruction, r_fid and σ_true. A scales as 300 km/s / σ_true and with the published r. Native inputs apply only to the model's geometry (h 0.679, Ω_m 0.3085).

## Differential bin

The paper uses thresholds. T(10.5–11) comes from nesting: w = N(10.5–11)/N(>10.5) from Fig2's histogram; T_bin = [T(>10.5) − (1−w) T(>11)]/w; C_bin = [C(>10.5) − (1−w)² C(>11)]/w², assuming the disjoint samples have independent errors and equal v² weighting. **PRIMARY:** this bin. Reported: T(>10.5) as published, and the 10–10.5 bin built the same way with the lowest GH9 Δ extrapolated (its corrected mass overlaps Zhang's lower bin half; no grade).

## Model

GH7's Zhang gas (β 0.43, r_c 6 kpc, 1.84 M★ in R_vir, μ_e 1.14, cut at k = 1, 1.8, 3), Table 1 R_vir, 1.6′ Gaussian beam, at each published θ. Model T(θ) = T_CMB (σ_true/c) τ_CAP(θ) × disc area. Mix over five 0.1 dex CIGALE cells and z, weighted by counts from Fig2 (mass) and DR1 BGS (`gh6_bgs.npz`, z within each cell; the M_r < −20.2 cut is not applied there, reported against Fig3). **Mass:** log M★ − Δ_j from GH9 (the 10.5–10.6 cell takes GH9's lowest cell), plus the h term as GH7.

## Verdict (PRIMARY: A(1.8), all published θ, full C_bin, Hartlap not applied since the paper's 10,000 bootstrap covariance is used directly)

A(k) = (m C⁻¹ T)/(m C⁻¹ m).
- **BELOW NEED:** A(1.8) + 2σ < 1.
- **ABOVE NEED:** A(1.8) − 2σ > 1.
- **CONSISTENT WITH NEED:** otherwise, if A(1.8)/σ ≥ 3.
- **NOT DETECTED:** otherwise.

Reported at the same fit: χ² at A = 1 for each k, A(1), A(3), the D = 0 fit (no mass offset), θ ≤ 3′ only, and Fig8's ratio.

**Interpretation lock.** The stack is all galaxies: satellites and two-halo signal **add** to T and are not subtracted.
- BELOW is therefore conservative.
- CONSISTENT or ABOVE does **not** show the need is met for isolated centrals, and can't retire GH8; that case is read as "the published sample doesn't constrain it, and it disagrees with GH8/GH9 only if centrals are shown to carry it".
- Any result here says nothing about the law winning. Extent beyond k is not graded: gas shape and two-halo are degenerate here.

## Checks

- **K1:** my model at GH7's θ grid matches `gh7_cap.npz` shape within 2 % for z and mass cells tested (θ ≥ 2′).
- **K2:** √(T C⁻¹ T)-style S/N of T(>10.5) reproduces the paper's Table 4 value (8.23) within 25 %, else the units or reading are wrong and the lane stops.
- **K3:** Fig6's labels contain >10.5 and >11, and N(>10.5) from Fig2 is within 20 % of 2.26M × the published fraction, or is otherwise reported.
- **K4:** C_bin is positive definite. If not, use the diagonal + report.
- **K5:** injected A = 0.5 × model into T returns 0.5 within 1e-6.
- **MUTATE:** T → −T flips A exactly.

**Scope.** κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework. Small job, one thread.
