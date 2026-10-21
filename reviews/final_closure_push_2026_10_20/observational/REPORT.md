# Observational closure audit, 2026-10-20

The canonical native-input shear run survives its frozen **relative** classification, but its apparent advantage disappears when both arms can fit one shared form of lensing amplitude. The CMB gate cannot discriminate the recorded templates. These are limitations on the present evidence, not a revised frozen verdict or theory closure.

## New executable discriminator

The most useful bounded check was to give each KiDS model exactly the same extra positive amplitude, while retaining its original five photo-z nuisances, intrinsic-alignment nuisance, priors, covariance, 108 kept points and measured power-spectrum nodes. The amplitude multiplies the entire predicted GG+GI+II shear vector. This is a **post hoc shape diagnostic**, not a self-consistent cosmological parameter change and not a new pass/fail rule.

For each nuisance vector x, the added amplitude is profiled analytically:

\[
A(x)=\max\left(0,\frac{t(x)^TC^{-1}d}{t(x)^TC^{-1}t(x)}\right),\qquad
Q(x)=[d-A(x)t(x)]^TC^{-1}[d-A(x)t(x)]+\pi(x).
\]

The existing bounded L-BFGS-B nuisance fit then minimizes Q. Three starts were used for each arm, including the frozen optimum and both signs of the initial IA nuisance.

| native canonical KiDS model | frozen total χ² | amplitude-profiled total χ² | fitted amplitude |
|---|---:|---:|---:|
| NCS0 matched control | 154.7623744853 | 120.0145987266 | 0.7212703142 |
| NC1x framework | 144.6844638801 | 120.9562100568 | 0.7584430016 |
| framework minus control | **−10.0779106052** | **+0.9416113302** | — |

Both frozen scores reproduce exactly in the existing Anaconda environment. All six optimizer runs converge; different starts agree within 3×10⁻¹¹ in total χ². An independent uniform-power-rescaling identity passes: multiplying either input P matrix by 1.1 leaves its profiled objective unchanged to <10⁻⁹, with A divided by 1.1. This tests the analytic projection rather than merely restating the fitted number.

**Interpretation:** the recorded −10.08 advantage is an amplitude benefit against a control that predicts too much shear. After allowing the same amplitude freedom, the framework has no observed shape advantage in this diagnostic (Δχ² +0.94). This does not exclude the framework and does not change NC1x's frozen HOLDS/CONSISTENT label. No significance is assigned to +0.94. The extra amplitude is deliberately unconstrained and is not a derivation of new cosmological parameters.

Files: `shear_amplitude_profile.py`, `shear_contract_conda.json`, `shear_run_conda/result.json`, and `shear_run_conda/manifest.json`. Runtime 8.50 s; peak RSS 265,158,656 bytes. One process and numerical thread; no multiprocessing or simulation. Python 3.13.9, NumPy 1.26.4, SciPy 1.14.1, Astropy 7.2.0. The original system-Python attempt failed because Astropy was unavailable; its failed record is retained in `shear_run/`.

## Independent CMB power calculation

Using the stored nine-band CFG917 vectors and the actual published PR4 covariance, define δ=B_F−B_S0 and q=δᵀC⁻¹δ. Under a fixed Gaussian covariance the simple-template statistic D=χ²(F)−χ²(S0) has mean q and variance 4q when S0 is true, and mean −q when F is true. Thus √q measures the template separation independently of the particular observed residual.

| pair | q | √q | √q after projecting out physical amplitude |
|---|---:|---:|---:|
| NC1x/NCS0, native canonical | 0.02112019 | 0.14533 | 0.10497 |
| T1x/P0, inherited canonical | 0.01824358 | 0.13507 | 0.09622 |
| T2x/P0, inherited alt | 0.01675781 | 0.12945 | 0.09251 |

The amplitude projection uses **B(A)=A(B+F_fid)−F_fid**, retaining the published additive correction. It does not incorrectly scale that fixed correction. For NC1x the amplitude-free observed Δχ² is −0.10626; inherited values are −0.11894 and −0.11385.

Even the optimal one-sided fixed-template 3σ test has only 0.20–0.22% power for these separations (Gaussian false-positive rate 0.135%). This statement concerns the explicitly stated simple-template experiment, not the full robustness-class rule. The primary Δχ²≥9 requirement is even less attainable here; adding the robust-member requirement cannot improve its power. The current CMB CONSISTENT classification therefore provides almost no discrimination between these pairs.

The calculation reproduces all three stored χ² values and fitted amplitudes to <10⁻⁹. Two independent small-matrix implementations, Cholesky whitening and partial-pivot Gaussian elimination, agree on q to <10⁻¹³. Only standard-library arithmetic was used. Runtime <0.01 s in the child; peak RSS 13,107,200 bytes. Files: `cmb_separation.py`, `cmb_run_measured/result.json`, and `cmb_run_measured/manifest.json`.

The dominant coverage limitation is structural: native PR4 signal fractions are 0.149725 from measured z≤1 box scales, 0.154288 from box scales at z>1 using continuation, and 0.695984 from k below the box. Equality of the arms on those large scales is imposed by the model continuation. An absolute PR4 fit near p=0.4 cannot test physics that the projected templates barely change.

## Raw evidence versus criteria

1. **CFG654 A2:** NC1x has Δχ² −10.0779, robustness −6.13/−13.78/−8.75/−12.74, KiDS CONSISTENT, and A2 HOLDS. Its own T-OWN=17.1065 passes. DES T-OWN=8.1378 fails, so DES remains NOT DIAGNOSTIC despite its negative relative Δχ². These labels are reproduced, not redefined.
2. **Absolute versus relative fit:** fixed-amplitude KiDS data-only χ² is 138.82536 (framework) and 146.70606 (control); the reported N_kept=108 convention gives p=0.02442 and 0.007846. Applying that same 108-dof survival function to the *total* penalized χ² instead gives 0.01064 and 0.002144, explaining A3's 0.011/0.002 disclosure. Neither convention is a fully calibrated goodness-of-fit test after constrained nuisance fitting. Quote its convention beside p; do not turn Δχ²<0 into an adequate absolute fit.
3. **CFG654 validation:** V-N1 remains **FAIL as frozen**: native CMB maximum deviation 0.04154046 exceeds 0.03. The post-freeze lattice-mode-average diagnostic reduces the mismatch to 0.000249935 and explicitly preserves the original failure. Original §4 calls V-N1 a must-pass check; production §3 explicitly gates on V-R alone. Report this mismatch beside the scorer HOLDS result. The diagnostic explains the discretization issue; it does not make the original validation criterion pass.
4. **CFG909:** the class survives the declared projection/covariance variants; those projection changes are not self-consistent cosmology changes. Its range of Δχ² amplitudes already warned against reading a model preference. The new amplitude profile is a separate, stronger diagnostic of that same issue, with no weight in CFG909's frozen classification.
5. **CFG917:** frozen K3b fails for every pair, so the frozen class and gate remain **NOT DIAGNOSTIC**. A1 replaces the erroneous data-identity premise with K3b′ and yields CONSISTENT/PASS. A1 is explicitly post hoc after the NC1x result; its commit precedes T1x/T2x results. Both labels must remain visible. The Part-A MUTATE also prints `bites: False` because its positive-boost sign clause is inapplicable to suppression; its separate SAFE label does not erase this diagnostic qualification.
6. **No retroactive gate:** CFG917 is not a CFG654 verdict input. CFG654's time condition and named CFG649 clause were not met. Treat it as adjacent evidence, not as an extra frozen gate that NC1x passed.

The checked freeze commits are A2 `fce7b081a0`, A3 `d2f59b90f2`, CFG917 original `0289e4ad4`, and post-hoc A1 `187f895aa`. Each original/amendment path is isolated in its stated commit. The review did not alter any of them.

## Native-input and parameter obligations

“Native” removes the inherited EH/backscaled-growth construction from these production inputs. It does not remove the late-time model dependence of the Planck base-ΛCDM TT,TE,EE+lowE chain used for ω_b, ω_c, A_s, n_s and θ*. Its lensing smoothing depends on late clustering. H0 is inferred from θ* rather than predicted; massless neutrinos, empirical f_ret and cooling inputs, one seed, finite box support, nuisance priors and survey covariance remain shared. A same-pipeline comparison does not cancel these assumptions. Likewise the PR4 common additive fiducial correction need not cancel from Δχ²: changing it by h changes Δχ² by −2δᵀC⁻¹h.

κ=1/2 remains fitted; the canonical/alt acceleration footings remain separate; required cold-energy mass has not been derived by these observational passes. A successful native alt run would remove one specific input-dependence condition, not these other obligations.

## Live run and exact next action

At **2026-10-20 15:21:55 UTC**, chain7 had no completion sentinels. NC2x's JSON contained only `zi`, with alt footing and native_cmb inputs; latest printed engine checkpoint was step 5/150, a=0.0228. The watch log continued updating (11:21:49 EDT: RSS 26.53 GB, recorded peak 42.09 GB; swap 3344 MB versus start 2557 MB). This is an incomplete, apparently live run, not a failed or complete alt test. `ps` was denied by the sandbox, so process identity was not independently confirmed. No process, guard, output or queue was changed. Full read-time hashes and log tails are in `live_job_snapshot.json`.

**Next:** let the existing chain7 run finish and execute its already queued MUTATE-first NC2x scorer. Do not launch another PM job. Before any alt result is interpreted, require all of:

```bash
E=/Users/carlzimmerman/new_physics/_external_data
test -f "$E/overnight_chain/chain7_state/NC2x.ok"
test -f "$E/overnight_chain/chain7_state/scoreNC2x_mut.ok"
test -f "$E/overnight_chain/chain7_state/scoreNC2x.ok"
rg 'chain7 done' "$E/overnight_chain/chain.log"
```

Then read `campaign_fresh_gravity/CFG654_independent_inputs/cfg654_native_results_NC2x{,_MUTATE}.json`, apply A3 unchanged, and run CFG917's already specified NC2x commands one at a time, reporting frozen and A1 classes side by side. Follow with a separately labeled amplitude-profile sensitivity on NC2x using the same diagnostic contract. That finishes the missing two-footing native observational check; it cannot establish theory closure.

For a genuine discriminating improvement after that, freeze a **self-consistent parameter/amplitude treatment** (including its external prior and both arms' response) before inspecting its new fit. The post hoc global amplitude in this review is a diagnostic tool, not that physical treatment. A larger-scale or higher-L CMB check needs demonstrable template separation/power before a nondetection can count as evidence.

## Provenance and bounds

Requested base: `f659e6d8e1ee4cf2b756f091aff56b018da1fb1e`. All 56 reviewed internal canonical/CFG654/CFG909/CFG917 source, criteria and result files match that base byte for byte; exact current and base SHA-256 are in `review_inputs.json`. The shared workspace advanced by unrelated concurrent commits during the audit; each run's v2 manifest records its actual observed HEAD and dirty state. No commit, publication or chat message was made by this subtask.

External raw/run inputs are pinned in `external_inputs.json` and checked before and after the shear run; the CMB result records its own raw-input before/after hashes. External inventories are explicitly part of the runner contract; the runner's own input list only supports paths inside the repository. All four v2 records validate against current internal hashes, including the two unsuccessful attempts. Read `run.status`: evidence of a failed run is not a successful computation. The first CMB launch with POSIX memory/CPU setup failed in `preexec_fn`; the successful reruns use measured RSS and no requested affinity/hard-memory cap. macOS affinity is unavailable; numerical-library thread variables are one and the scripts create no workers. These runs remained far below 1 GB. No process was monitored or terminated for resource use.

Outcome: **implementation and finite assertion verified in the stated range**, conditional on the published covariance, stored templates and the stated numerical nuisance optimization. The inference is evidence calibration and amplitude sensitivity, not universal physical closure.
