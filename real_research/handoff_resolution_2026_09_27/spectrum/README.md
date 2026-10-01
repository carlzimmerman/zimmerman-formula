# Physical-wavenumber correction to XR28

`check_transfer.py` evaluates the original and corrected XR28 transfer functions against the independent Colossus 1.3.9 Eisenstein--Hu implementation at 3,000 physical wavenumbers, 10^-5 through 10^3 Mpc^-1. The corrected result differs by at most 3.33e-16; the original differs by up to 1.114 relative. Both retain sigma8=.811 by construction, so the normalization control alone cannot find this units error.

The two substitutions are the existing FP24 correction: remove `/h` from `0.43*k*s/h`, and use `k/h` in q when the input k is physical Mpc^-1. No fit is performed. At z=1 the corrected Correa mass histories are 0.9111, 0.9144 and 0.9414 times the originals for final masses 10^13, 10^14 and 10^15 solar masses. These input changes require rerunning the cluster calculation; they do not themselves establish a cluster fit.

The v2 bounded manifests in `main/` and `mutate/` pin the audit script and original XR28 source. The mutation selects the original formula and fails the named independent transfer check while retaining the normalization check. The installed Colossus version is recorded but its package source is not included in the declared input closure. The first unrecorded attempt encountered NumPy Boolean JSON serialization, which was fixed before these recorded executions.

The corrected full cluster reruns have `_corrected` directory suffixes in `../reproduction/`; each contains a correction record and a complete corrected common-module copy. Unmodified-source reproductions are retained separately. Cluster verdicts must be read with their convergence controls, not inferred from successful execution or agreement with historical outputs.
