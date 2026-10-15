# Catchment supply and cosmic inventory review — 2026-10-15

Review anchor: `7c1eae898ec964062a01f9a79f8d7b8af5d5d52b` (HEAD at inspection). This is a read-only audit of the existing scientific records using the computation-audit and proof-audit workflows. No scientific code, criteria, output, score, or simulation was changed or rerun. No internet or external messages were used. The repository has unrelated pre-existing modifications; `git status --short` for the seven reviewed lane directories was empty. External calibration sources were not authenticated here.

**Primary verdict: incomplete, with the smallest missing implication being the transition from an externally calibrated catchment budget to an owned, finite cold-mass distribution that forms and lenses as assumed.** CFG803 passes its frozen C-profile comparison. CFG804 supplies a useful conditional finite-edge construction. Neither establishes unique catchment ownership, dynamical filling at its derived budget, or global cosmic closure. These qualifications preserve all published numerical scores.

## What the records establish

| Lane | Raw recorded result | Strongest supported reading |
|---|---|---|
| CFG801 | Canonical primary edge χ² 280.9324; no-edge χ² 83.8596; Δχ² +197.0728, 32 points and four profiled masses. | The specified settled-only edge is strongly disfavored relative to the no-edge template on the raw primary data under the frozen statistic. This is conditional on the data/model construction, including any unmodeled correlated environment. |
| CFG803 | Canonical primary C−B Δχ² +0.13154; full +2.75084. Grid `N_min` is 3/4 primary, 16/24 full for canonical/alt. | Frozen C RESCUES criterion passes. Conditional truncation templates require more supply than N=1; this is a grid threshold after mass profiling, not an independently measured universal N. |
| CFG804 | Primary Δχ² −0.22939/−1.5 canonical/alt. Canonical χ² 83.6296/28, p=1.8994e−7. Full Δχ² +148.6910/+172.2. | A static finite-edge template built using census retention is competitive with the already poor absolute no-edge primary fit. Its full-range fit fails. “No additional fitted N” is accurate; “outer-halo problem closed with no free parameter” exceeds this evidence. |
| CFG805, already present at the review anchor | Canonical full D+2h χ² 170.6631/52, p=1.4990e−14; B+2h χ² 159.6006; Δχ² +11.0625. Primary Δχ² −2.1051. | The subsequent two-halo calculation narrows the outer gap, and its own frozen CLOSED test fails. Do not recommend merely adding a two-halo term as though that work were absent. |

CFG801–805 use the same local B21 Fig. 3 product: four 15-point ESD profiles and a full 60×60 covariance, each bias-corrected by the supplied bias columns. The primary selection has eight radii per bin, hence 32 data entries and 28 nominal degrees of freedom after four mass normalizations. The raw data README confirms the calibration division and ESD/covariance units; it does not by itself authenticate the paper's interpretation of isolation or deprojection.

## The fixed point and input accounting

CFG804 defines, for the galaxy's modeled retained baryon mass B,

`Bcatch = B/f(Mta)`, `fb = 1/(1+5.364)`, `Mta = B/[fb f(Mta)]`, `N = 1/f(Mta)`.

Its numerical iteration is `f <- [f + fret_of(log10(B/(fb*f)))]/2`, initially f=0.10, at most 200 steps, tolerance 1e−12. This implements the stated algebraic fixed point. Because `Mta*f(Mta)` is increasing for this positive, nondecreasing retention law, an admissible solution is unique. The control B=10^10.5 returns N=10 and log Mta≈12.304. The cold budget is `5.364*N*B`; inverting the exact static law gives

`re/rM = sqrt[(5.364*N)*(5.364*N+1)]`, `rM = sqrt(G*B/a0)`.

Canonical primary results reported in `cfg804.out` are N=10.00, 8.83, 7.35, 5.62; log Mta=12.18, 12.53, 12.58, 12.67; edges 324, 453, 439, 429 kpc. These are derived outputs **conditional on the fitted B values and retained-fraction dictionary**, not newly measured catchments.

| Input class | Count and role |
|---|---|
| Measured survey input | One four-bin ESD data vector, radii, calibration and covariance; 32 primary or 60 full entries. |
| Fitted to these data | Four independent log B normalizations per model/range, on a 0.01 dex grid with three coordinate sweeps. CFG805 adds four nonnegative bias amplitudes, for eight fitted nuisance parameters per model. |
| Externally calibrated physical input | One piecewise retention function; cosmic cold/baryon ratio 5.364; fixed a0 footing with κ=1/2 fitted elsewhere. The retention relation has six independent scalar anchors if continuity is imposed: 0.10, 12.5, 13.5, 0.45, 0.30, 0.90; 0.55 is the continuous value at the second breakpoint. Their uncertainties are not propagated here. |
| Derived | fb, fixed-point f, Mta, N, budget and static edge. No independent KiDS N fit in CFG804. |
| Structural assumptions | A modeled central-galaxy B is the retained fraction of its entire catchment; the complementary baryons imply a corresponding cold budget; that budget belongs to this halo and occupies the exact-law profile to a sharp edge. These are not supplied by reciprocal algebra. |

There is an unresolved native-unit dictionary. CFG416's criteria explicitly use threshold masses in Msun/h, and `cfg416_pm.py:275–279` computes Mta in Msun/h, passes `log10(Mta)` to `fret_of`, and divides Mta by 0.674 when constructing physical baryon mass. CFG556 retains that native h-unit convention (`cfg556_halo_model.py:45–46,87–92,116–118`). CFG804 passes `logMb−log10(f*FB)` directly into the same thresholds (`cfg804.py:19–32`) while its lensing normalization uses physical G and pc. This establishes a translation obligation; it does **not** authorize silently inserting an h factor. The original census calibration must determine whether thresholds, masses, and the modeled retained component have the same definitions. CFG416 also declares that its PM does not deplete baryons; its growth result does not validate the inventory assumed in CFG804.

Implementation limits: CFG804 rounds N to the nearest 0.25 grid value for the projected template (`:52–57`) but prints continuous N and its continuous edge (`:93–95`). It uses numerical line-of-sight integration and three coordinate sweeps, without a recorded independent global optimum or discretization error bound. Its fixed-point loop has no explicit nonconvergence exception. These are audit obligations, not grounds to alter the recorded verdict without a new authorized check.

## The CFG748 → CFG803 → CFG804 bridge

CFG748 is a restricted radial-shell experiment with point baryons, critical self-gravity cancellation, deep cubic pressure, a reflecting boundary at r=0.5, core mass 0.5, initially stationary shells, R0=200 and a supplied total mass of about 200 B (`cfg748.py:9–24`). It does not form that supply from a cosmological catchment.

Its **uniform** last window gives m(<r)/r≈0.999,1.001,0.998,0.996,0.945 at r=2,5,10,20,50. But uniform energy error is 0.003234, above the frozen 0.001 bound, and the no-force MUTATE tooth does not bite (1.42 against 1.5). The combined frozen lane result is C1 FAIL, C2 STALLED because the half-supply start remains deficient at 50 rM. Those disclosed control outcomes must travel with the later use of its table.

CFG803's frozen C template uses the **5000–6000** window, although called a late-window table. Its `fill` function is multiplied into the local exact-law density (`cfg803.py:21–28,44`), while CFG748 actually measures an enclosed deep-law quantity m(<r)/r (`cfg748.py:41`). In general an enclosed multiplier F gives a local density proportional to `d[r F(r)]/dr`, not simply F times the reference local density. Nor is CFG748's deep equilibrium m=r identical to the exact finite-radius law. This is an approximate profile-transfer assumption, not an exact import of the simulated density.

Furthermore C holds fill=0.948 beyond 50 rM and projects to infinity. Its mass therefore diverges. The printed N≈37 is the *initial law mass within 200 rM*, not a mass bound implemented in C. Thus the frozen profile comparison passes, but it is not a finite-supply dynamical theorem. CFG804 instead tests a static exact-law truncation at N≈6–10; no reviewed record demonstrates that a halo with that finite supplied mass, realistic age and angular momentum forms that particular filled edge profile.

## Unique cosmic inventory and double-counting

The useful conditional bookkeeping identity is: for disjoint owned catchments C_i, let `Bi = integral_Ci rho_b dV` and `Bgal_i=fi*Bi`. Then `sum_i 5.364*Bi <= 5.364*Bcosmic`, with equality only if the catchments exhaust the baryon inventory and all cold mass is represented. Expelled/diffuse baryons stay in the global inventory. Satellite and central retained components must be allocated once, and remaining free cold mass must be recorded. An ownership kernel with weights summing to one can replace a hard partition.

Neither CFG804 nor the reviewed source experiment constructs this partition or kernel. Applying N separately to every galaxy and summing overlapping host/satellite/environment catchments could double-count the same supply. Conversely, a stacked lensing correlation legitimately contains matter around multiple lenses: summing these overlapping conditional profiles does not by itself yield the universe's mass. A global overclosure claim requires the unique mass field and population weights.

ARGON09 is located at `argon_push/ARGON09_mass_bookkeeping_2026-10-15/`. Its raw results retain mean B1=5.3047 times settled supply and B2 proxy=15.9728 B, and its provisional debris budget 0.25 B is far below that proxy. These motivate an inventory check, but do not close it:

- B1 uses B21's ESD-to-circular-velocity conversion as a surrogate for enclosed mass; correct application of that conversion is not a general deprojection theorem.
- B2 uses `pi*R²*DeltaSigma_exc` (`mass_bookkeeping.py:78–102`). The exact identity is `pi*R²*DeltaSigma = Mcyl(<R) − pi*R²*Sigma(R)`. For an isothermal projected tail Sigma=A/R, the proxy equals **half** the cylindrical mass, so the criteria's “exact for isothermal-like tails” wording is not an exact mass identity. The existing number remains an approximate aperture proxy.
- B3 (`:104–113`) assumes `rho_b=n_g*B`, explicitly putting all cosmic baryons in the representative lenses; n_g=0.03 and rM=12 kpc are provisional. The reported ratio 166 and 31× budget follow from that surrogate, not a unique cosmic inventory. This assumption excludes the very diffuse catchment baryons that increase N in CFG804. Neither genuine overclosure nor its absence is established. The n_g sensitivity uses a printed divisor 3.15 rather than the formula's cube-root scaling; it should be audited without rewriting the historical output.
- B5 is **absent from the frozen B1–B4 criteria**. Code `:115–125` compares a provisional projected **Sigma** estimate to an observed **DeltaSigma** excess, with a ±1 dex gate around a hard-coded 3.0. It does not compute `Sigma_bar−Sigma`, fit the full covariance, propagate environmental calibration, or use an isolation-matched galaxy–matter correlation. Its success cannot prove the web fully accounts for the signal or turn the original CFG801 result into an empirically established “untested” claim. A modeled-environment subtraction remains a useful next test.
- The output's “0 FAIL” records B3/B5/B4 check objects; B1/B2 are printed rather than separately asserted. The report's statements about physical closure are stronger than that program contract.

CFG805 goes further by computing DeltaSigma, but still has material limits: four fitted biases; inherited cosmology/initial conditions; failed sigma8 reconstruction control (0.75430 versus snapshot 0.779); exclusion mutation only partly meets its declared tooth; and fixed exclusion radii copied from CFG804 while masses are reprofiled (`cfg805.py:65–66,78–108`). Excluding a sphere in a matter autocorrelation is not yet a derivation of an isolation-selected, uniquely owned galaxy–matter cross-correlation. The no-exclusion bracket is explicitly disclosed as double-counting its own catchment, and even its improved absolute fit remains poor.

## Directed next work and completion evidence

1. **Resolve definitions and controls before another rescue fit.** Produce a source-backed dictionary for retention mass units, central versus all retained baryons, h/h70 conventions, a0 footing and the exact observable Sigma/DeltaSigma. State which CFG748 enclosed profile is transferred and how it generates density. Completion evidence: dimensionally consistent equations with source locators; preserved historical results; independently checked projection/mass integrals and explicitly dispositioned failed controls.
2. **Build one finite owned inventory.** Specify catchment ownership for hosts, satellites, overlaps and diffuse baryons; conserve baryons and cold mass separately. Use the same inventory for one-halo mass and environmental correlations. Completion evidence: per-region and global conservation residuals, duplicate-allocation audit, mass-function/population weighting and a remainder account. Do not diagnose universe overclosure by summing overlapping stacked halos.
3. **Test the smallest physical bridge.** Given the audited census budget, show that finite supplied matter forms the assumed radial distribution within available time, or derive and project the actual distribution it does form. Carry the CFG748 energy/mutation failures and finite-radius/deep-law distinction into the design. Completion evidence: controlled conservation, sensitive negative control, and a profile derived from finite matter rather than an infinite continuation.
4. **Then score an isolation-matched full ESD prediction.** CFG805 is the existing partial advance. Resolve its projection/exclusion/normalization obligations and compare both edge and no-edge models with the same independently constrained environmental term and nuisance treatment. Completion evidence: an ownership-consistent galaxy–matter cross-correlation; full covariance score; both footings separately; primary and outer results; acceptable absolute goodness of fit and the predeclared relative criterion. A relative Δχ² pass against a poor reference alone is not empirical closure.

## Provenance and hashes

Last relevant lane commits: CFG803 `856892748`; CFG804 `67774ce37`; ARGON09 `20eb8caea`; CFG416 `3b96babc306d01437de3cdcd9418cc9a55099cd0`; CFG748 `2309081590cac3189e161f8d02d647c5ed02b6b1`; CFG805 diagnostic is the review anchor. Criteria-first revisions named by records: CFG803 `5c3468ec0`, CFG804 `22cdbecf9`, CFG748 `3eedeacd4`, ARGON09 `038d3858e`, CFG805 `11b9e3f03`.

SHA-256, read directly at the anchor (lane names below abbreviate their directories):

```text
51fa12bf5325a6bbb2e18a996a676231996f46c3289e571d407426e8e2cd6c68 CFG801/FROZEN_CRITERIA.md
cad4510cb2ff9854a7d9d3256e6172d74e3e0a79596ddd360c877c4ad20cc845 CFG801/cfg801.py
d5b978312e856c63aa80cfcf96f7718322cf16464c4ae353d34fb41fc074e3ee CFG801/cfg801_results.json
3255c5639f4e5c57625a73d595d552f601877f4b30f762dd26b977de3d059afe CFG803/FROZEN_CRITERIA.md
9d042b4d21ba8cf99dccd8fb85de0cdd5f91738cf19f6b72c7b02dcb5048cb75 CFG803/cfg803.py
d336a3d6893a42260d7ee1a69e8a8146a3ed1414e2d62eb79d6ea9b72a627090 CFG803/cfg803_results.json
73d2f29ef4bd3ef761999df411f51092273617f860bf794c6715a0386834a031 CFG804/FROZEN_CRITERIA.md
48c20895f73981be42dabfe16f812afc085dfe799f175895a2d3a9ddb6a45aa9 CFG804/cfg804.py
3b05dabb1ad8fa07e0ef2a09db7ff4b8009e632c9b76a739b8734b9048e06e3a CFG804/cfg804_results.json
e74ae319b02fb84c3b3f859048259da76c47784dab5867165a6b97f719f78b0c CFG416/cfg416_pm.py
465fa044d3f673167a4f5e334c0b5c839f42438d29fc10c4f6a20a3b2b27c7e1 CFG748/cfg748.py
101fd444770337a0e837fb20871bf2020387b29929f2b4214a7376b1e18cf806 CFG748/cfg748_uniform.json
996544108d87629b10f33660823415fa4a445237b007223130e899f0740c8e2d CFG805/FROZEN_CRITERIA.md
a2c89ad488ec054dae682b018280e97696cb4353220e51e55130afc6167dd60c CFG805/cfg805.py
ce9e174482ebef2649c371037905d15f04b49f749ea253ecc23181ecdf296b03 CFG805/cfg805_results.json
96abab61866891038bdc1d4beb047e476aa9e0aef2a87b98b992a096eb7fb403 ARGON09/FROZEN_CRITERIA.md
8ede9ee4ad6cd7073337b5f73ea12b6909e75daced42b8a325ca0ba45d7fc77a ARGON09/mass_bookkeeping.py
57bcd122a777cf2a955ee0947ae32c28ea6c3a13b2d6038320af167d088a5fcd ARGON09/mass_bookkeeping_results.json
e258ec32f8b87195b50ea5a8c691e36aa50d5e503f6bdff8b88c08a01f6b1504 ARGON09/REPORT.md
```

Scope limits: this is an artifact/code interpretation audit, not independent reproduction, source authentication, or a new simulation. No numerical correction or rescore has been applied. Environment/library versions and complete original-run provenance were not independently reconstructed. The conclusions concern the named transitions and bounded evidence, not a refutation of the whole framework.
