# Exploratory empirical discriminator, 2026-10-19

No repository file was edited. All runs used own scratch scripts and frozen copies, with no project source-script imports or execution. Shared HEAD observed during snapshot was `bb25c4ddd46bbecfbad2e32c88a9802ac0e55cc2` (different from task-start HEAD because other researchers were active); the repository was dirty. The load-bearing input SHA256s are in `source_provenance.json`; original sources had the same hashes at final verification.

## Finding

The raw MW/M31 geometric-mean extra-speed mismatch is explained algebraically by the hosts' law-velocity distributions. The inference `Vx² = Vlaw²(10^Delta - 1)` means:

`log Vx = log Vlaw + 0.5 log10(10^Delta - 1)`.

Canonical selected sample (Delta > 0.05, 10 MW + 10 M31 + 5 field): the M31-minus-MW means in those three quantities are respectively +0.181680, +0.191404, and -0.009724 dex. The normalized-excess gap has descriptive bootstrap SE 0.104545 dex. Selected hosts have mean log stellar mass 5.758462 vs 6.478223 and mean Delta 0.434129 vs 0.438625. Same gbar does not mean same Vlaw: Vlaw² = r g_law and in the deep regime Vlaw scales approximately as stellar mass^(1/4).

This does NOT remove CFG857's size-conditioned host coefficient. With its identical intercept + log(size/0.3kpc) + M31 design, +0.175361 dex splits into +0.043725 from log Vlaw and +0.131636 from normalized excess (stratified-bootstrap SE 0.061230). The pooled logVx-versus-logM slope +0.088610 is the sum of +0.263718 in law velocity and -0.175108 in normalized excess. Thus the apparent nearly constant Vx is a cancellation in this selected sample, and is not independent information beyond the measured dispersions and baryonic law.

## Forward comparison actually executed

Retain all 29 CFG828 pressure-supported dwarf rows, including four canonical Delta <= 0.05 rows (Hercules, Andromeda II, Sagittarius, NGC147). Use existing CFG824 observed sigma, CFG827 SFH M/L, LVD radius and luminosity, canonical/alt a0 and nu_e. Reconstruct gbar and Delta from those independent inputs to <1e-10 dex. The sigma_law² convention is r*g_law/3.

Two models, each one constrained parameter, were fitted to equal-object mean squared errors in log10 observed LOS dispersion:

- Additive: sigma_pred² = sigma_law² + A, A >= 0. Equivalent circular extra speed sqrt(3A).
- Multiplicative: sigma_pred² = Q sigma_law², Q >= 1.

No measurement-error weighting, latent nuisance distributions, intrinsic-scatter fit, selection likelihood, radius or M/L uncertainties, or per-star velocity likelihood was included. These are finite prediction re-scores, not likelihood ratios, significance tests, selection corrections, or independent new observations.

| Sample and validation | N | Additive RMSE | Multiplicative RMSE |
|---|---:|---:|---:|
| All satellites, train MW/test M31 and reverse, pooled | 24 | 0.162771 | 0.158960 |
| log gbar < -11.9 satellites, same host splits | 16 (8+8) | 0.193808 | 0.145324 |
| All 29, leave one object out | 29 | 0.127681 | 0.154604 |
| log gbar < -11.9, leave one object out | 21 | 0.141951 | 0.143189 |

RMSE unit is dex in log10 sigma. The model ranking depends on validation/population. At low gbar, fit MW A=14.6963 (km/s)² or Q=2.76202; fit M31 A=46.7849 or Q=3.14301. Alt-footing low-g host validation gives 0.190467 versus 0.145345 dex, same qualitative result.

Crucial fragility: omit Hercules, and low-g host validation becomes additive 0.130417 vs multiplicative 0.135294 dex, reversing the apparent preference. Hercules has observed sigma 2.25 km/s, law sigma ~2.200 km/s, and Delta +0.01955, so CFG856/857 dropped precisely a useful counter-control to a positive variance floor. For 1,000 stratified host resamples with refits, the canonical additive-minus-multiplicative RMSE difference has central 95% interval [-0.079479,+0.140305] dex and is positive in 0.748 of draws. This is descriptive resampling, not a calibrated significance claim. No model preference is established.

## Strongest next move

Predeclare a homogeneous forward per-star dispersion analysis that retains near/below-law systems and holds out an entire host. Include Hercules and low-dispersion controls such as Crater II explicitly; test a variance floor against a proportional-law effect using the same membership, velocity-error, binary, and aperture treatment. Match or model law velocity/stellar mass as well as gbar. Re-reducing Hercules is particularly discriminating because one near-law low-dispersion system reverses this cheap cross-host score. Existing evidence supports neither treating the raw 9.4/14.3 km/s host split as an environmental signal nor declaring a universal floor from SPARC compatibility alone. Global dispersion alone cannot establish physical origin; projected-virial and spatial/epoch information remain necessary.

## Evidence and reproduction

- `run/manifest.json`, `run/result.json`: primary decomposition and forward scores.
- `robustness_run/manifest.json`, `robustness_run/result.json`: all 16 one-object deletions and 1,000 stratified resamples with refits; selected-mean uncertainty and mass-slope decomposition.
- `verify_run/manifest.json`, `verify_run/result.json`: exact synthetic additive/multiplicative parameter recovery, 10,001-point grid checks of every full and host additive optimum, and unchanged original-source hashes.

All three have `run.status = completed` and passed the skill manifest validator. Bounds: 45s wall timeout for the first two runs, 40s CPU, one conventional numerical-library thread, at most 128KiB stdout/stderr; verification 15s wall and one thread. No resource truncation. Random generators are NumPy PCG64, seed 20261019; primary decomposition 2,000 stratified draws; robustness 1,000 draws. These bootstrap SEs intentionally differ from CFG857's unstratified bootstrap.

A fresh replay preserving this evidence is:

```bash
python3 /private/tmp/zimmerman_empirical_host_20261019_gcjfj1az/replay.py
```

The launcher creates a new scratch directory, reruns all three contracts and validates all manifests. Source-hash verification at the end deliberately fails if repository data have since changed; the frozen-copy numerical results remain independently reproducible. Each manifest records complete argv, exact code/input hashes, software versions, timings, and results. `PACKET_SHA256.json` hashes every delivered file except itself.
