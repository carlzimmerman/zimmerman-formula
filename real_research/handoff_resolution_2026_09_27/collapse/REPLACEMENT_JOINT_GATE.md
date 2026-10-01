# Conserved replacement: conditional KiDS and SPARC joint gate

The reservoir-capped P2 family has a conditional survivor, but no parameter-free joint success. With the existing Moster stellar-to-halo mapping and the stars-only KiDS endpoint Mb/Mstar=1, the capped model passes the existing relative KiDS gate when four inherited two-halo amplitudes are fitted within [0,2]. The primary transfer Mb/Mstar=1.4 misses that gate on both a0 footings. Fixed unit two-halo amplitude does not satisfy the original comparison against unbounded P2 without a two-halo term. SPARC is unchanged at its fitted stellar mass-to-light ratios because no measured point exhausts the supplied halo reservoir.

This is an explicitly conditional cross-population transfer, not the same HOD population as CMASS. Both a0 footings are inherited from FP0; kappa=1/2 remains FITTED. Nothing here derives shell crossing, a conserved dynamical current, or the host-reservoir relation.

## Definition and independently inherited inputs

For point baryons, the scored mass is

Mtot(r)=Mb+min{Mb[sqrt(1+a0 r²/(G Mb))−1], Mh−Mb}.

The reservoir edge is re²=G(Mh−Mb)(Mh+Mb)/(a0 Mb), with exterior total mass Mh retained. No edge length is fitted. KiDS uses the redshift-dependent Moster mapping in `CFG3_common.py` at z=.25 and its already declared Mb/Mstar endpoints 1, 1.4, 2 (`CFG3_kids.py`). SPARC uses `CFG2_common.mass_budget`, including its inherited bulge proxy and 1.33 MHI, and the same source's z=0 Moster inversion. The reservoir is Mh−Mb, as in the conserved CMASS prescription; it is not an extra NFW halo added to the phantom.

The existing CFG4/FP1 KiDS mass grid spans log10(Mb/Msun)=9.8–11.8. The exact FP20 projector, four-bin covariance, radial data, and two-halo template are reused. Baryonic masses and stellar mass-to-light ratio remain inherited nuisance parameters; free two-halo amplitudes are **fitted nuisance parameters**, not predictions. No Moster coefficient, a0, reservoir normalization, or edge parameter is refitted.

The scored family is the **budget-only cap**. CMASS additionally uses a first-turnaround source gate whose seed depends on a retained-carrier table at z=.5. That extra gate is not transferred to z=.25 KiDS or z=0 SPARC: it would require an epoch- and population-appropriate retained fraction and seed history. Thus these results identify the stronger surviving static mass-budget construction, not a full reproduction of the CMASS gate for different galaxies. SPARC retains its algebraic RAR approximation and applies a spherical dark-cap acceleration min(gphi,G Mc/r²); this is not a nonspherical disc field solution.

## Reproduction and the inherited optimization defect

`replacement_joint_gate.py` reproduces the old KiDS unbounded P2 scores 139.800159/133.947771 and SPARC weighted RMS to roundoff. Its primary capped KiDS penalties with A≤2 are +13.34698/+25.77505. The stars-only endpoint gives −1.90460/+5.84341. The Mb/Mstar=2 endpoint gives +67.02978/+111.69078. All those use the source's original fitting procedure.

That source procedure chooses each bin's mass/amplitude with diagonal errors, then reports the full-covariance chi-squared. It does **not** minimize the reported statistic. Indeed a fixed unit amplitude can sometimes produce a smaller reported score than the supposedly profiled interval containing that value. These scores are reproduction evidence only; the main inference below uses a new full-covariance optimization.

## Corrected full-covariance comparison

`replacement_covariance_fit.py` minimizes (prediction−data)^T C^-1 (prediction−data), with the exact supplied covariance. It linearly interpolates the original .05-dex mass-grid profiles, retains the original mass bounds, and uses bounded least squares from 200 starting points per fixed-amplitude case and 201 per free-amplitude case, including the inherited fit and the newly optimized fixed-unit solution. Random starting points use seed 20260927. This finds explicit admissible solutions and strong numerical candidate minima; it does not prove global optimality across the piecewise profile surface. In particular a failed gate is not a universal exclusion of every admissible fit.

The refitted unbounded P2 baseline scores are:

| two-halo treatment | canonical | alternate |
|---|---:|---:|
| absent | 138.96728 | 133.63657 |
| fixed A=1 in every bin | 199.53695 | 196.12144 |
| four amplitudes fitted in [0,2] | 137.69325 | 132.60005 |

For capped P2, the penalties against a baseline with **the same two-halo treatment** are:

| Mb/Mstar | no two-halo canonical/alternate | fixed A=1 canonical/alternate | fitted A≤2 canonical/alternate |
|---|---:|---:|---:|
| 1 | +17.662 / +29.347 | −41.162 / −45.738 | −0.766 / +5.218 |
| 1.4 (primary) | +43.693 / +67.102 | −48.557 / −34.010 | +11.317 / +25.636 |
| 2 | +121.274 / +191.101 | +7.816 / +60.784 | +63.532 / +107.996 |

The inherited relative gate is a penalty ≤9. Fixed-unit rows beat a **poor fixed-unit baseline**, so those negative differences alone do not establish that fixed A=1 fits the observations adequately. Against the refitted unbounded-P2/no-two-halo reference that defines CFG4's original comparison, fixed A=1 gives +19.408/+16.747 (stars-only), +12.013/+28.475 (primary), and +68.386/+123.268 (ratio 2): none passes on both footings. This comparison changes the two-halo treatment and is therefore labeled separately, rather than substituted for the matched comparison.

Against that same original-style reference, the fitted-amplitude stars-only endpoint gives −2.040/+4.182 and the primary gives +10.043/+24.600. The canonical primary is close to the numerical gate; its failure is scoped to this bounded optimization and supplied mapping. The stronger statement is the direct witness: the stars-only/free-amplitude endpoint passes both reference conventions. It is not robust across the inherited mass-transfer bracket.

The actual fitted two-halo amplitudes (bins 1–4) are:

| Mb/Mstar | canonical | alternate |
|---|---|---|
| 1 | .912, .014, .396, .000 | .936, .127, 1.179, .000 |
| 1.4 | .954, .806, 1.334, .603 | .967, .850, 1.642, .472 |
| 2 | .981, .988, 1.761, 1.122 | .995, 1.166, 2.000, 1.661 |

No absolute goodness-of-fit or joint likelihood pass is inferred from this relative gate. The covariance fit is a separate improved computation; it does not rewrite the original stored scores.

## SPARC and meaningful controls

The mass cap leaves the fitted SPARC result exactly equal to P2: weighted RMS .108271861 at Upsilon=.70 canonical and .103548976 at Upsilon=.65 alternate, satisfying the inherited .110-dex/[.50,.80] gate. There are zero capped measured points at those fits. The largest required dark-mass fractions of the supplied reservoir are .72820/.83487. Thus this is a conditional inner-law preservation result, not an independent prediction of reservoir size. The Newtonian negative control gives .275477506 dex at the upper grid boundary Upsilon=1.20.

The main static computation has 88/88 controls pass. Deliberate MUTATE deletes dark mass outside the reservoir edge and fails all 82 exterior Gauss-retention controls while leaving baseline controls intact. Its primary KiDS penalties with fitted A≤2 become +187.21/+222.46. The full-covariance computation passes its whitening identity, inherited-score reproduction, direct quadratic-score identity, and admissible-score comparisons. Its separate MUTATE discards covariance cross terms and fails the named whitening/score identity controls rather than crashing.

A projection-domain discriminator extends the source grid from 30 Mpc/4000 points to 100 Mpc/8000 points. The primary cap-minus-baseline penalties move by at most .011 across the scored amplitude treatments. The original-grid baseline tolerances intentionally remain unchanged in this refinement run and fail by .0038/.0037; those two failures are recorded, not relabeled successes. The primary selected cap edges are all inside 1.14 Mpc, so the unused high-mass trial edges exceeding 30 Mpc do not drive the score. An initial control mistakenly tested outer-grid saturation for every mass; preserved `.initial` artifacts show this. It was corrected to probe outside max(grid end,2re), without changing the scientific profiles or scores.

## Provenance and remaining implication

All new runs use `/usr/bin/python3`, no CLASS and no parallel workers. Each is guarded by `record_child.py`; source/data inputs are read-only and their before/after hashes match. `replacement_joint_manifest.json` and `replacement_covariance_manifest.json` record source hashes, versions, controls and failures; full input manifests, raw logs, per-start optimizations and JSON results are beside them. The static suite reads 189 inputs per run. Source lane files were not changed.

The remaining physical input is not a numerical edge length. It is a justified mapping from the selected galaxies to conserved dark reservoirs, plus the region/retention evolution and a predicted environmental/two-halo response. An existing empirical mapping supplies a conditional calculation and exposes its dependence: changing only its already declared baryon-to-stellar interpretation changes the joint relative verdict. A single conditional passing endpoint with fitted two-halo amplitudes is the strongest surviving result established here.
