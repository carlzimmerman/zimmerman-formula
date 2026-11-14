# Latest supernova work: independent bounded audit

2026-11-14. Read-only audit of Claude's lanes, with new scratch artifacts only in this directory. Original repository was dirty and actively changing. AGB5 snapshots were pinned at **19:00:06 UTC**, rather than treating the live lane as a finished paper. Initial repository HEAD observed: `956cefbe24c4c51f34d8744df848eead0eedcc11`.

## Finding that must reach the handoff

**AGB5 supersedes the broad reading that a mass step accounts for the published age slope.** On the original published residual tables, a substantial fitted age slope remains with a mass step free. This does not invalidate AGB4's Pantheon+ regression; it limits that regression's interpretation to its data and standardization.

AGB5's frozen K4 failed, so the original result remains **NOT EVALUABLE under its frozen gates**. A disclosed amendment, written after seeing all results, substitutes bootstrap errors and a residualized shuffle check. Its current output is `A = 0.792687 ± 0.189525`, with Δχ²(0) = 17.4933 and Δχ²(1) = 1.19653. Its frozen vocabulary says REQUIRED / FRAGILE, with table 1 alone only FAVOURED and the structural errors-in-variables fork UNDECIDED. This is an amended, model-dependent regression association; it is not proof of age causation or a validated cosmological correction.

## Independently recomputed

Both computations use separate parsers and SVD coefficients / QR covariance, without importing Claude's fit or loader code. Both runner manifests validate with `run.status = completed`.

| Check | Fresh result | Scope |
|---|---|---|
| AGB4 primary raw, no mass step | A = 0.2972187932 ± 0.1942697535; Δχ²(1) = 13.08669 | All 286 unique SDSS IDs; 8 bins |
| AGB4 primary raw, mass step free | A = 0.1944613196 ± 0.2096737519; Δχ²(1) = 14.75994 | Agreement with stored amplitude within 8.3e-11 |
| AGB4 raw, full supplied covariance sensitivity, mass step free | A = 0.2002344361 ± 0.2022745213; Δχ²(1) = 15.63303 | Diagonal covariance choice does not explain the small slope; published covariance held fixed |
| AGB4 published magnitudes | M0 A = 0.0434673675 ± 0.1680239858; M1 A = 0.1055222732 ± 0.1887707531 | Both stored fits also reproduced |
| AGB5 table 1, mass step free | β = −0.0159666728242 mag/Gyr; g = 0.0587826298 mag; n = 187 | Formula slope error = 0.0067000690; stored bootstrap error not recomputed |
| AGB5 table 2, mass step free | β = −0.0353901626879 mag/Gyr; g = 0.0407239827 mag; n = 101 | Formula slope error = 0.0075028532; stored bootstrap error not recomputed |
| AGB5 combined | A = 0.7926866371 ± 0.1895246929 | Fresh slopes combined using **stored** bootstrap errors; arithmetic verified |

The two AGB5 no-step slopes also independently reproduce: −0.0245909004 and −0.0384904021 mag/Gyr. All four slopes agree with stored results to < 6e-16. The finite WLS assertions are verified; bootstrap calibration and structural optimization are **read, not rerun**.

## Read, not independently rerun

- AGB3R's blind build reports D2 A = 0.389 ± 0.079, rejecting both A = 0 and A = 1 in its two-component star-formation-to-age template. It is therefore incorrect to call its result "no age dependence." Halving the template changes the amplitude to 0.778 ± 0.159 and the verdict. This is calibration dependence, explicitly exposed by the frozen fork.
- AGB3R's present-acceleration word is fragile: full-sample fixed A = 1 gives q0 ≈ +0.092 with Δχ²(today) ≈ 1.25; DES-only gives q0 ≈ −0.444 and Δχ² ≈ 7.18. The full drift is dominated by the low-redshift legacy versus DES transition. These are fits within the specified flat w0–wa family and BAO combination; no universal cosmological conclusion was checked here.
- AGB5's post hoc same-host comparison reports, with a mass step free, A = 0.670 ± 0.247 on the claim's residuals, A = 0.152 ± 0.171 on Pantheon+ residuals, and A = 0.555 ± 0.119 for their difference (185 common objects). This is a useful **reported post hoc discriminator** for residual-definition/standardization dependence, not an independently verified discovery in this audit.
- AGB5's EIV structural fork is A = 1.648 ± 1.435, UNDECIDED. The original residual plain regression and a latent-age regression are materially different estimands. Correlation of an age proxy with stretch does not by itself calibrate the intrinsic progenitor-age response.

## Interpretation

AGB4 is a successful numerical test of a **fixed −0.030 mag/Gyr regression template against measured host-age point estimates**, with stated nuisance terms. Calling that "age bias excluded" without its conditions is too broad. A free mass step can absorb part of an association, but which covariate is causal is not identified by fitting both. AGB5 supplies direct evidence against the stronger claim that the original published slope disappears with the mass step: it does not, especially in table 2.

The productive next comparison is the same-host residual change under explicit standardization and age-error models, preserving the frozen/amended/post hoc distinction. None of AGB3R, AGB4 or AGB5 evaluates a0, selects the theory's closure coefficient, or closes its field equations. These lanes improve empirical model checking; they do not constitute direct progress on those missing theory derivations.

## Reproduction and provenance

- AGB4 command: `/private/tmp/forj0332-fit-venv/bin/python codex_mass_budget_2026_11_14/latest_sn_review/check_primary.py codex_mass_budget_2026_11_14/latest_sn_review/run/result.json` (executed under the bounded runner; exact runner command in `run/manifest.json`).
- AGB5 command: `/private/tmp/forj0332-fit-venv/bin/python codex_mass_budget_2026_11_14/latest_sn_review/check_agb5.py codex_mass_budget_2026_11_14/latest_sn_review/run_agb5/result.json` (exact runner command in `run_agb5/manifest.json`).
- Python 3.9.6, NumPy 1.26.4, SciPy 1.13.1; deterministic; 30-second cap each, one numerical-library thread. Input snapshots are pinned before/after in manifests.
- `agb5_snapshot_provenance.json`: 18 live-lane/source snapshots, hashes equal before copy, after copy and snapshot. `read_provenance.json`: other audited AGB3R/AGB4 file hashes.
- AGB5 criteria SHA256: `376036f20c6e67d99c1832fbf1f5c41152086bd0358c2c4f7b5427bdcd2368cd`.
- AGB5 amendment SHA256: `82f3d13e4f6cd6a6fb9f7f548b0f399b3ac9ece3b6be2cf959381b796ea847b1`.
- AGB5 amended results SHA256: `bcdf6e85e4574018777a775eeaa05a9b59329d7a5804bd7f12413133ea7a34d2`.
- AGB5 same-host post hoc results SHA256: `c8814d982631ec29e5deb0982ae6748e0de97955be17a5c8e9d7c2460791e51c`.

No external paper's detailed estimator definition was authenticated in this audit. AGB5's frozen criteria explicitly label its paper-method reading provisional; numerical reproduction of table slopes does not authenticate the source's method. No existing lane was edited, no full cosmological fit rerun, and no scientific status ledger promoted.
