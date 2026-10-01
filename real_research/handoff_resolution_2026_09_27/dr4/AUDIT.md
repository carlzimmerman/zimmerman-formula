# XR22 / DR4 amendment audit — HR01

Primary verdict: **computationally verified only in a stated range** for the completed controls and XR31 correction; **incomplete** for a validated DR4 ξ measurement. Full XR22 reproduction is tracked live in `full_records.json`; only completed entries count as reruns. The scripts' original grids and physics are retained. No frozen file, hash receipt or source lane is modified.

The computation contract is the double-filtered static P2 two-body response, followed by the frozen population and γ estimator, both a₀ footings. Arithmetic is NumPy/SciPy double precision (XR31 also uses symbolic/40-digit checks). The code must reproduce numerical observables and control statuses, and deliberate mutations must fail named scientific checks. A successful process exit alone does not establish that contract. ξ is an extra free parameter in this conditional law; fitting it does not satisfy the larger target of κ=1/2 as the sole accepted fit.

## Completed independent checks

- XR31 mutation/main ran in 10.69/11.17 seconds. The intended mutation return code 1 and main return code 0 are accompanied by the same check outcomes as the banked results. The main fold y_f=2.3850815129995344 differs from the banked 2.385081513005839 by 6.3×10⁻¹². Largest shell-radius difference is 6.3×10⁻⁸ AU from that tiny root shift. F6's positive secant stiffness does not prevent a negative slaved longitudinal coefficient. The derivative algebra and three independent fold constructions, rather than agent agreement, support the correction.
- Exact XR22 K0–K3 source-body prefix ran in 26.33 seconds. Both footings, frozen field inversion and the tensor/quadrature checks pass. Deep-MOND ratios are 1.0033834345320258 (ξ/s=.05, q=1), 1.0013877472826498 (.025, q=1), 1.004560351926958 (.05, q=.3); Richardson gives 1.0007225181995245. Maximum discrepancy from the banked values is 7.1×10⁻¹⁵. This finite smooth-source convergence check does not independently authenticate the cited external virial theorem.
- Exact XR22 force mutation ran in 161.76 seconds, rc=1, K4 and K5 fail as intended. K4 canonical extrapolated B=1.094940018279542 versus double-filter kernel ≈1.051979. K5 10-kAU canonical nonlinear B3=1.0465201484797528 versus independent B2R=1.0291527382037755. All 15 numeric differences from the banked mutation are ≤7.1×10⁻¹⁵. These are valid physical-path failure controls, not crashes.
- `forecast_audit.py` independently reconstructs every stored Fisher value for ξ≤.1 pc on both footings from the saved bin derivatives and errors, with maximum absolute difference 7.1×10⁻¹⁵. The floor uncertainties are .204595/.158483. Profiling a completely free common multiplicative amplitude, without the anchor, gives .333840/.263921. A *hypothetical* rank-one 2% common calibration covariance gives .323610/.255240. Those last two are sensitivity experiments, not replacements for a calibrated nuisance model or interpretations of the frozen scalar 2% allowance.

## Mathematical dependency audit

| Obligation | Status | Exact implication / gap |
|---|---|---|
| k04 F6 establishes stable scalar dynamics | Failed | Secant Π/q≥Z is not tangent d g_N/d g_φ at fixed flux. XR31 reconstructs the reduced Routh/Schur operator and finds the negative band. |
| k04 root uniqueness | Passed within the stated kernel/construction | Preserve the restricted F6 reading; do not infer a stable exterior. |
| Four-form correction applies to both standard a₀ footings | Passed | k04 holds Z_four-form/β²=8 fixed. “Tied alt” changes κ and is not the ordinary alternate footing. |
| Two filters implement variational source/output symmetry | Numerical control passed | Dropping output S is detected by K4/K5; this does not alone prove a covariant completion. |
| XR22_common race has historical byte provenance | Not addressed | One Git commit introduces the file; no pre-edit hash is preserved. A claimed added downstream function cannot certify the earlier process bytes. A fresh unchanged-input main run resolves current-source reproducibility only. |
| Finite ξ scan is a continuous ceiling theorem | Conditional | Computed monotonicity on grid and interpolation; no global analytic bound, and single-orientation overshoot occurs. |
| Static radial force rescaling is a self-consistent binary population | Not addressed | A modified anisotropic force changes orbit evolution and potentially steady-state selection. Equal-mass tables do not quantify population mass-ratio bias. |
| σlnξ≈.20/.16 is attainable DR4 uncertainty | Conditional | Fixed calibration, statistical bootstrap, adjacent-knot derivative; no covariance/nuisance/coverage/triples treatment. |
| Separation cut is directly observable | Failed as written in XR22 forecast | Its mask requires both boosted ṽ and the same pair's counterfactual Newtonian ṽ below six. Proposed observable uses separate symmetric cuts and therefore needs new calibration. |
| Action with κ sole fit | Not established | H retains free ξ and inherited external-field/boundary/population prescriptions. |

The secant/tangent counterexample is structural: a scalar force saturated at fixed a₀ tilts downward when the slaved a₀ decreases with source acceleration. It is a failure of this four-form construction and saturated kernel, not a no-go theorem for every environmental-a₀ theory. Negative scalar stiffness is distinguished from the rate computed in one particular kinetic model. The nonlinear endpoint is unknown.

## Exact preregistration choices and outstanding gates

`AMENDMENT13_DRAFT_NOT_FILED.md` is a literal append candidate. It fixes bins, observable, cap symmetry, primary footing, field convention, κ notation, ξ knots/interpolation, bootstrap count/seed, shared-star resampling, separate model covariance, boundary reporting, nuisance profiling, and calibrated confidence-set requirements. It retains the scalar estimator and existing guard rules.

The following are substantive unfinished work, not cosmetic filing choices:

1. Quantitative hidden-triple/contamination model and external calibration bounds. A separation-dependent inflation can mimic the signal. No XR22 result supplies that model.
2. Full seven-bin plus anchor systematic covariance. The frozen σ_sys(γ̂)=.020 cannot be treated as seven independent median errors or as a rank-one error without justification. Overlapping anchor and separation samples require joint covariance.
3. The bounded cap/covariance recalculation has now been executed: CORRECTED_STATISTIC_AUDIT.md records three seeds and actual nine-summary joint covariance with profiled calibration. The cut makes zero difference in these clean samples; floor profile errors are .349–.372/.260–.275. Extending to contaminants, calibrated coverage and the full final population remains open. The banked .2046/.1585 forecast is not silently transferable.
4. Self-consistent orbit and real Galactic-direction/mass-ratio bias validation, or a quantitative pre-data model discrepancy allowance and explicitly conditional interpretation. The rough −.001 to −.002 γ mass-ratio estimate in XR22 was not run through the estimator.
5. Finite-MC/force-table/interpolation uncertainty and midpoint tests. The two estimator paths can differ by .005 and the grid step is .0025. Those numbers are numerical/model resolutions, not measured data errors.
6. Injection/recovery coverage at the ξ floor and Newtonian limit, goodness-of-fit calibration and contamination stress tests. Fisher information does not establish these. The proposed 2,000 realizations per point is a new reviewable choice and has not been run.

The draft deliberately provides a fallback of measured medians and a conditional exploratory profile if these gates remain open. Thus it can record the forecast and correction without falsely claiming a fully validated ξ measurement protocol. It must not be represented as resolving all scientific prerequisites to filing a definitive ξ test.

## Provenance and bounded interpretation

`full_reproduction.py` copies the three XR22 scripts into a repository-layout mirror, symlinks read-only dependencies, and executes MUTATE/main sequentially per lane with XR22_NPROC=1 and numerical-library thread settings at one. The current force production table is copied initially for the mirror; after the exact force main completes, the statistics lane consumes its new output. No dry-run substitute is used. XR31 main/mutation and K0–K3 records are in `bounded_records.json`; their byte hashes are not identical to banked files because of timing and tiny numerical differences. `full_records.json` records source working-tree hashes before and after each process, exact argv, runtime, rc and recursive numeric comparisons. Resource settings are cooperative; no hard memory/CPU limit or measured peak RSS is claimed.

Sources at Git HEAD 48905ae11213afcb9ff1b7726530bb5dd1933fe3 are read from the actual working tree and hashed, since the repository is dirty with unrelated work. Legacy-schema computation manifests honestly retain their weaker provenance guarantees; supporting raw records contain extra hashes and comparisons. The snapshot and prospective hash receipt generated locally are review artifacts, never the live registration or AMENDMENT13_HASH.txt.

Additional convention check: the force law uses the FP0 exact footings, while the estimator uses its own frozen rounded 9.36e-11/1.13e-10 binning constants. GEXT_PHYS is exactly 1.7784e-10. The draft states both instead of silently unifying them. K0 also inherits the alpha_c renormalization statement from FP14; its zero-switch and scale checks do not independently rederive that upstream claim.

Executed extension: CORRECTED_STATISTIC_AUDIT.md documents the new symmetric-cap and paired-bootstrap calculation rather than merely proposing one. Its moderate seed dependence and explicit lack of coverage/contamination validation are retained. The proposed 100-system and 2,000-bootstrap/realization constants are labeled new design choices throughout.

Scheduling note: the coordinator later authorized considering three workers after a memory assessment. Read-only process inspection confirmed that the pool was still active and at least one 40-task worker generation had completed, but the code persists no exact live task counter. A proposed termination/restart was rejected by automatic approval review because the run has no checkpoint and the review did not find explicit user authorization to discard its work. No process was terminated, no workaround was attempted, and the original single-worker run continues. `planned_restart_not_executed/` preserves the rejected plan and contemporaneous log snapshot; it is not an abandoned computation record.

## Analytic reconstruction of the saturated-branch failure

The sign result has an exact reduction in the stated k04 model, independent of the numerical root finder. Write r=a₀,loc/a₀, y=g_N/a₀, s=y/r, D=Δ_sat>0, j=j_sat, and c=(2−K_B)/(8π Zt), with Zt=Z_four-form/β²=8. On the saturated branch F=sD−j and the normalized fixed-flux equation is r[1+cF]=1. Hence

    r(1−cj)+cDy=1,
    u(y)=g_φ/a₀ = D(1−cDy)/(1−cj),
    du/dy = −cD²/(1−cj),
    C_L,eff = −(1−cj)/(cD²),   y_off = 1/(cD).

For the registered diagnostic coupling, c>0 and 1−cj>0, so the whole admissible saturated branch with u>0 has negative C_L,eff. Substituting D≈.647610 and j≈.452525 yields −238.62 and y_off≈155.234 at K_B=0. The exact fold just below saturation still needs the smooth-kernel root calculation, which XR31 reproduces. C_T,eff=y/u remains positive on this branch. Thus a positive secant flux root and a monotone *total* observed acceleration do not establish ellipticity of the slaved scalar sector. The broader “convexity implies F≥0” statement requires the kernel's adopted normalization J(0)=0; it is not invariant under an arbitrary additive constant in J. This note audits the normalized k04 construction only.
