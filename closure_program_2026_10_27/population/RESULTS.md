# M6 population accounting — 27 October 2026

**Result: the population cost is now quantified; M6 is not excluded by this calculation.** The native-h rescaling of the published all-galaxy census gives 4.699% of cosmic baryons in stars, 5.815% in stars plus atomic gas including helium, and approximately 5.979% after the quoted molecular component is added. The relevant isolated/law-selected fraction of this inventory has not been established. The supplied allowed fractions remain conditional on X57's variance prescription, with no calibrated physical forest limit.

This is a bounded population computation, not a new survey fit or a full native-cosmology reanalysis. The primary sources retain their distance models, mass estimators, completeness corrections and selection definitions. The exact accounting statements below require baryon ancestry in the counted M6 patches.

## 1. Source-supported inventory

Use h=0.6856427, omega_b=0.0223081 and Omega_m=0.2976016. Then Omega_b=0.04745335 and rho_b=6.191314829e9 Msun/Mpc^3. The denominator is the independently saved coordinator capacity input. All densities below are z=0 comoving densities.

| Component | Native-h density, Msun/Mpc^3 | Fraction of all cosmic baryons |
|---|---:|---:|
| Galaxy-bound stars, Chabrier IMF | 2.9090840e8 | 0.04698653 |
| Atomic hydrogen | 5.1949433e7 | 0.00839069 |
| Atomic gas with helium factor 1.33 | 6.9092745e7 | 0.01115962 |
| Quoted molecular component, counted once | 1.0161537e7 | 0.00164126 |
| Stars + atomic gas + helium | 3.6000115e8 | 0.05814615 |
| Stars + cold gas, baseline convention | 3.7016269e8 | 0.05978741 |

The stellar input is rho_star=(2.97±0.04_random±0.58_systematic±0.20_CV)e8 h70 Msun/Mpc^3; h70=h/0.7. Its full uncertainty is about 21%, not the approximately 1% fitting uncertainty. Table 7 requires +0.0807 dex on both normalization coefficients. Stellar masses are Chabrier; no helium factor is added to them. [Driver et al. 2022, arXiv v1, Table 7 and §§6–7](https://arxiv.org/html/2203.08539v1).

The HI input is Omega_HI=(3.9±0.1_random±0.6_systematic)e-4 h70^-1, including self-absorption correction. HI plus helium uses 1.33; changing it to 1.4 raises the baseline cold fraction to 0.06037476. [Jones et al. 2018, arXiv v1, abstract](https://arxiv.org/abs/1802.00053).

The molecular input is Omega_mol=(5.34±0.47)e-5 h^-1: this uses h, **not h70**. The baseline counts it once. A subsequent source cross-check resolves helium: xCOLD GASS total molecular masses already include helium; Fletcher uses that same Accurso conversion. The saved extra-1.33 result F_cold=0.06032903 is therefore a deliberate double-counting sensitivity, not an equally valid physical convention. The stars-plus-HI subtotal is independent of molecular calibration. [Fletcher et al., accepted manuscript, abstract and §3.4](https://discovery.ucl.ac.uk/10112984/1/staa3025.pdf).

**Fix-forward source note:** [Saintonge et al. 2017, version of record, §2.5 column 20, printed p8/PDF p9](https://purehost.bath.ac.uk/ws/portalfiles/portal/163826676/Saintonge2017_arXiv.pdf) explicitly includes helium in molecular mass; Fletcher §2.1 equation (1) uses the same Accurso conversion. `helium_evidence_2026_10_27.json` supersedes the uncertainty wording in the immutable saved input record. Baseline numerical results are unchanged.

Masses scale as h^-2 and number densities as h^3, hence mass densities as h. Original flat Omega_m=0.3 distances are retained. A distance-only sensitivity check to native Omega_m changes D_C at z=0.1 by 0.0179%; this is not a recomputation of Vmax or sample membership. The results field named `density_shell_proxy_distance_inverse` is only the inverse-distance representative-sphere scaling, not the exact differential-shell selection correction. The headline census uses only the explicit published h scalings.

## 2. Exact necessary accounting and conditional capacity

Let q_star, q_HI and q_mol be the **mass fractions**, within each cosmic component, in the galaxy population that independently requires M6. Then the observed selected inventory is

F_selected = 0.04698653 q_star + 0.01115962 q_HI + 0.00164126 q_mol.

If all those baryons descend from the counted patches and epsilon is selected present-day cold baryons divided by the initial baryons in those patches, conservation gives

F_patch = F_selected / epsilon >= F_selected, with 0 < epsilon <= 1.

This is the strict stellar-only route as well: F_patch >= 0.04698653 q_star. It does not require assumptions about star-formation efficiency beyond the closed-reservoir inequality. It is conditional on the empirical stellar-mass scale and patch ancestry. There is no numerical lower bound on the required q_star in the inspected sources. Incoming baryons from outside counted patches require an explicit lineage calculation; a present-day census alone cannot then bound primordial patch mass by this formula.

For the common-selection scenario q_star=q_HI=q_mol=q, the coordinator's exact two-phase proxy ceilings B=0.06061499 / 0.04856637 imply

q <= 1.013842 epsilon (canonical), and q <= 0.812318 epsilon (alt).

| Retained cold-baryon fraction epsilon | Maximum q, canonical | Maximum q, alt |
|---:|---:|---:|
| 0.25 | 0.2535 | 0.2031 |
| 0.50 | 0.5069 | 0.4062 |
| 0.75 | 0.7604 | 0.6092 |
| 1.00 | 1.0000, capped | 0.8123 |

Conversely, required q=0.25, 0.50, 0.75, 1.00 needs epsilon >= 0.2466, 0.4932, 0.7398, 0.9863 canonical, or >= 0.3078, 0.6155, 0.9233, 1.2310 alt. These are scenarios, not measured efficiencies or priors. At the central census, assigning all cold galaxy baryons to the alt prescription exceeds its proxy capacity even at epsilon=1; that is not exclusion of M6's actual selected subset or a physical forest result.

Additional warm gas, expelled material or baryons in the same surrounding environment consume the same patch budget. An initial-reservoir multiplier zeta=M_patch_initial/M_selected_cold is simply 1/epsilon; it must not be multiplied in again as a separate penalty. For q=0.5, zeta must be <=2.028 canonical or <=1.625 alt under this prescription.

Changing only the stellar density by the source's ±21% sensitivity gives F_cold=0.04992024–0.06965458 and, at epsilon=0.5, q_max=0.4351–0.6071 canonical or 0.3486–0.4864 alt. This envelope is not a confidence interval; HI systematics, stellar covariances and selection uncertainties remain. No 95% or sigma exclusion is inferred.

## 3. What environment evidence does and does not supply

[Alpaslan et al. 2015, arXiv v1, Table 1 (PDF p7)](https://arxiv.org/pdf/1505.05518) reports fitted integrated stellar-mass fractions of 30% ungrouped, 70% not in a close pair and 4% in voids. These are not number fractions. Its pair definition is projected separation 100 h^-1 kpc and velocity separation 1000 km/s (§3); ungrouped objects may be centrals of undetected groups (PDF p12). These categories do not implement the M6 isolation criterion.

Even treating the 30%/70% marginals as exact on a common population, the joint ungrouped-and-unpaired mass fraction is only bounded by 0 <= q_joint <= 0.30. Multiplying the marginals assumes independence; adding them double-counts. Transferring those older fitted fractions to the present census adds a sample/mass-range assumption.

As an explicitly conditional example, q_star=0.30 costs F_star,selected=0.01409596. The minimum stellar retention is 0.23255 canonical or 0.29024 alt. If the same 30% of *every* cold component is selected, minimum cold retention is 0.29590/0.36931. If those stars instead accompany all cosmic HI and molecular gas, it is 0.44373/0.55382. Gas selection therefore matters independently of stellar selection.

The local ALFALFA-SDSS CSV has 31,503 rows, but lacks the survey weights and environment flags needed here. Its flux/width selection also excludes a simple sum-to-density conversion. Its SHA256 was checked; it is not used to pretend to measure isolated cosmic density. The source-dependent RESOLVE/ECO alternative has different finite volumes, completeness limits and gas conventions; it is not silently pooled into a cosmic isolated census.

## 4. Mass range and patch-count route

The corrected double-Schechter stellar fit was integrated in physical native-h masses. Analytic incomplete-gamma mass integrals agree with direct log-mass quadrature. Rounded coefficients reproduce the independently quoted total density to 0.106%.

| Stellar mass cut/range, Msun | Fraction of all fitted stellar mass | Number density, Mpc^-3 |
|---|---:|---:|
| >=1e8 | 0.98478 | 0.043320 |
| >=1e9 | 0.95435 | 0.015245 |
| >=1e10 | 0.84185 | 0.005543 |
| 1e9–1e11 | 0.69145 | 0.014734 |
| 1e10–1e11 | 0.57895 | 0.005033 |

These counts use the fitted mass function and are not isolated counts. The coordinator's fixed-radius prescription allows n_patch=0.0103212/0.00706378 Mpc^-3. **If exactly one galaxy occupies each patch**, it can cover at most 67.70%/46.34% of the >=1e9 number population, or 23.83%/16.31% above 1e8. The count constraint is not restrictive for all >=1e10 objects. This count test must be combined with mass per patch; allocating the same median patch to every mass cannot establish full-population feasibility. Fragmentation, mergers and radius variation require an explicit occupation/union-volume model.

A separate finite-bin check avoids extrapolation to unobserved low masses: placing every object in the published 0.25-dex bins from 1.0423e8 to 5.8614e11 native Msun at its lower bin edge gives rho_star >=2.17713e8 **for the adopted central binned estimates**, or F_star>=0.0351642. This is a mathematical lower-edge bound on those estimates, not a hard observational lower confidence bound. Applying a 0.79 scale gives 0.0277797 as a sensitivity case.

Fletcher's host-mass cut of 1e9 at h=0.7 becomes 1.0423e9 Msun here. Combining its 73% HI and 89% molecular host fractions with the stellar fit gives F_cold=0.0544050 above that cut. This is another mass-selected central estimate, not an isolated population. Transfer between the surveys' stellar-mass calibrations is an extra approximation beyond the explicit h conversion.

## 5. Conditional representative-patch mapping

The coordinator's [separate mapping result](/Users/carlzimmerman/new_physics/zimmerman-formula/closure_program_2026_10_27/patch_galaxy_mapping/run/results.json) retains the original X22 representative effective baryon mass of 7.33935e9 Msun and pairs one descendant with one enriched patch. This algebra implies epsilon=0.201848/0.172415 and descendant mass densities 7.57509e7/5.18435e7 Msun/Mpc^3. Relative to the entire census these are inventory ratios 0.20464/0.14006. **They are not fractions of the actual population covered:** X22 uses a law-inferred effective mass, not a demonstrated census total, and a median object does not represent the mass function.

If a different prescription instead assigns each native Lagrangian volume as M_gal/rho_b, then initial enriched mass=(1+delta_b)M_gal and epsilon=1/(1+delta_b). This is a separate mass-scaled identity with epsilon=0.190994/0.163144. It changes the patch-size distribution, so the inherited forest response cannot be retained without recalculation. Independent algebra and source inspection support these conditional identities; neither is a formation-efficiency measurement.

## 6. Finite next closure step

1. Freeze the actual required population predicate: stellar/baryonic mass range, the same isolation threshold used in the law test, and whether central/group galaxies or only disks qualify. This prevents selecting q after seeing the budget.
2. Measure its weighted stellar density using the survey's selection and completeness model. A stellar-only lower requirement is already sufficient to compare once q_star is measured; gas then strengthens it. Use joint environment memberships, not products of marginal fractions. Cross-match HI/molecular measurements or report separate bounded gas fractions and non-detection treatment.
3. Assign patch masses/radii and ancestry by galaxy mass, then integrate the selected mass function and occupation. Explicitly account for mergers, repeated counting and unobserved baryon phases. The representative median-patch efficiency is a separate scenario, not an observed efficiency.
4. Compare that required reservoir to a physically calibrated forest limit under the same perturbation model. The current variance ceiling and NOT DIAGNOSTIC forest response cannot supply that limit. A population-capacity violation becomes branch exclusion only after both sides are justified.

This population work does not derive kappa, evolve the patches or establish a dynamically admissible galaxy profile.

## Reproduction and evidence

- `helium_evidence_2026_10_27.json`: subsequently authenticated helium convention; supersedes only the historical molecular ambiguity interpretation.
- `mapping_review.json`: independent Decimal accounting checks and hashes for the coordinator's conditional mapping.
- `inputs.json`: exact transcribed source values, URLs, versions, locators, conventions, local-data SHA256 and selection limitations. Remote source bytes are not cached or claimed hashed.
- `compute_population.py`: deterministic calculation; no network or catalogue fitting.
- `contract.json`: claim, bounds, pinned execution inputs, software versions and non-claims.
- `run/results.json`: full numerical tables, including additional q/epsilon cases.
- `run/manifest.json`: input/output SHA256, exact command, native runtime, resource limits, completion status. Thirteen assertions passed; the manifest validator passed. The bounded command completed in 1.27 seconds. Validation confirms provenance and numerical invariants, not the physical interpretation.

Quick numerical reproduction (choose a new output filename to preserve the recorded run):

```sh
/Users/carlzimmerman/new_physics/_external_data/tools/pysco_venv/bin/python closure_program_2026_10_27/population/compute_population.py /tmp/m6-population-results.json
```

The saved manifest contains the exact bounded-run command and the SHA256 values of the code, transcription, capacity input and inspected local catalogue. No original science artifact, live job, commit or external message was changed by this work.
