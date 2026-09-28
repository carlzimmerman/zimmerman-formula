# Independent bounded quality review of 2026 work orders

Reviewed on 2026-09-27 by the separately assigned 2017–2019 author. This is a read-only review of the task/source artifacts, not execution of any proposed science and not a proof audit of all 250 calculations.

**Primary verdict: correct only after stated restrictions and local corrections.** The requested four source groups have honest data-access prerequisites and useful release-specific targets. One literal set identity is wrong as labelled; several observation-map conventions should be made explicit before dispatch. No task/source/card files were edited.

## Scope and evidence

Read source records Y2026S04 (eROSITA), S07 (wide binaries), S08 (lunar clock), S10 (SN spectral delays), the math/input/output targets of their 100 tasks, selected full records and rendered cards. Rendered examples inspected: MY2026-077, MY2026-153, MY2026-194 and MY2026-247. Inspected the common framework/conditional-data/overlap wrapper in rendered examples. Compared closest earlier-year work orders in the 2017–2019 catalogs; no exhaustive semantic comparison to the other years or all old AS tasks was performed.

Independently reopened these primary pages:

- eROSITA DR2: https://erosita.mpe.mpg.de/dr2/ — release paragraphs explicitly say catalog-only and distinguish DR1 event products; 2026-07-31 news date verified.
- Wide binaries: https://arxiv.org/abs/2601.21728 — v1 2026-01-29, v3 2026-09-19; abstract verifies new/archival RV measurements and explicitly highlights two influential pairs. This authenticates the measurement report, not its anomaly interpretation.
- Lunar clock: https://cpl.iphy.ac.cn/en/article/id/58ff9c62-dd83-4705-ab6f-41fe46ca3c18 — abstract verifies April 2025 dual one-way ranging/time-frequency comparison; citation verifies 2026 volume 43 issue 3. Exact first online day and the reported violation-parameter convention remain unverified here.
- SN: https://arxiv.org/abs/2608.28416 — v1 2026-08-28; abstract verifies A–E spectra, GP spectral-feature fitting, shared-reference delays, and an additional separately published lens-model dependency.

Full numerical tables, raw data, complete likelihoods and covariance payloads were not inspected in this review.

## Corrections and restrictions

1. **MY2026-077 — replace the union identity (P2, definite as a set-union claim).** The displayed `N_union=N1+N_added-N_removed` is the count of the new catalog, not the union of old and new identity sets. For old A={a,b}, new B={b,c}, it gives 2 while the union has 3. Define one-to-one reconciled identity sets first, then use `N2=N1+N_added-N_removed` and `N_union=N1+N_added=N1+N2-N_intersection`. Many-to-many splits/merges need the separately defined reconciliation relation rather than this simple count. The error appears in both JSON and rendered card.

2. **MY2026-194 — define phase units and the integration nullspace (P2, missing convention/restriction).** In the surrounding clock tasks `y` is fractional frequency, so `integral y dt` has units of time. If the intended observable is time deviation, write `x(t)=x0+integral y dt` with x in seconds. If phase is in radians, write `delta_phi(t)=phi0+2*pi*nu0*integral y dt`; for cycles omit 2*pi. Equivalence of phase and frequency likelihoods also requires handling the unknown integration constant and the actual averaging/sampling operator, not covariance alone. Clock literature sometimes calls time deviation phase, so this is a units ambiguity rather than a demonstrated physical contradiction.

3. **MY2026-153 — label the Kepler formula as a reference model (P2, restriction).** `r=a(1-e cos E)` is the bound Kepler ellipse relation; it is not generally a trajectory identity of the filtered, environmentally perturbed MONO two-source system. The card's first-principles paragraph already warns that an effective Kepler-G boost is only an estimator, which is helpful. Make the displayed relation explicitly “Newtonian/Kepler comparison only”; construct the candidate phase-conditioned likelihood from its actual trajectory measure, or define osculating elements and evolve them. The present generic “derive displayed statistic from framework” step otherwise invites an incompatible exact reduction.

4. **MY2026-080 — specify conditioning of the selection factor (P2, ambiguity).** The expression `p(F_true|F_obs,det) proportional to p(F_obs|F_true)n(F_true)S` does not say whether S is evaluated on observed data or latent flux, or whether the likelihood is already conditioned on detection. If detection is a deterministic threshold on the very F_obs conditioned upon, the factor `S(F_obs)` is constant in F_true and should not produce a second latent-flux correction. Use the general joint expression `p(F_true|F_obs,D=1) proportional to n(F_true)p(F_obs,D=1|F_true)` and factor it only after the selection variables are defined. This avoids the common double-selection bias.

5. **MY2026-165 — state the stationary conservative domain (P2, restriction).** A scalar `v_esc^2=2(Phi_boundary-Phi)` is an energy threshold for a stationary conservative potential per unit appropriate mass, with the escape surface and frame fixed. A rotating tidal environment can require an effective potential/Jacobi integral and a time-dependent environment need not admit a single escape speed. The boundary caveat and failed-route continuation are good; add the stationarity/frame/integral-of-motion qualification rather than assuming that a boundary alone suffices.

## Data-access and empirical-claim checks

- **eROSITA MY2026-082 and -091: passed at work-order scope.** They explicitly request the catalog-only identifiability boundary and do not claim DR2 contains resolved pressure/temperature profiles. MY2026-090 (external weak-lensing calibration), -087 (variability), and -099 (count/background model) may require additional products, but the acquisition step and missing-product completion condition prevent a false data-availability claim. Keep those tasks conditional unless the exact required fields/calibration are obtained.
- **Lunar clock MY2026-176, -195, -196: passed at work-order scope.** They preserve uncertainty in alpha convention, do not identify alpha with a0, and do not promote one hydrogen-clock comparison into a universal strong-equivalence test. The publisher issue is verified; the source record honestly distinguishes it from an unverified exact first-online date.
- **Wide binaries MY2026-162, -169, -173, -175: passed at work-order scope.** Influence of the two systems is a source-supported target; scalar RAR substitution and a population anomaly as action closure are explicitly disallowed. Energy/angular-momentum conservation is correctly conditioned on action symmetries.
- **SN MY2026-226, -227, -238, -239, -247: no blocker found in the stated scope.** Source-frame time and shared-reference covariance are distinguished; independent intrinsic-clock information is required for a time-dilation claim; algebraically dependent delay cycles are not counted independently; an independent physical-metric lens map is required before inferring a distance. For -239, when only reference-image delays are supplied, the derived cycle is an identity rather than an empirical consistency test; its existing failed-route continuation already addresses this.
- The rendered common wrapper correctly uses vacuum energy density V0 with `a0^2=G_N V0/4` and `H_vac^2=8*pi*G_E V0/(3c^2)` under its stated vacuum-background assumptions. It also correctly separates the two a0 normalizations and conditional GR/LambdaCDM posteriors.

## Earlier-year overlap and reuse map

These are reusable generic obligations, not automatic duplicates of the 2026 measured output:

| 2026 task | Earlier task | Required incremental work |
|---|---|---|
| MY2026-152 | MY2018-063 | Apply the perspective-motion correction with the 2026 spectroscopy epochs and covariance; reuse the kinematic derivation. |
| MY2026-164 | MY2018-054 | Refit selection-conditioned chance alignment for the measured 36-system sample, especially its influential systems. |
| MY2026-166 | MY2018-055 | Use the actual new follow-up multiplicity diagnostics and source-window mismatch, not repeat the photocenter identity. |
| MY2026-158 | MY2018-067 | Reuse the external-field derivation; evaluate the new 3D orientation/velocity likelihood. |
| MY2026-169 | MY2018-068 | Reuse finite-filter two-source lemmas; derive the measured-sample force/velocity response and retain non-spherical environment. |
| MY2026-227 | MY2019-041 | Shared-reference covariance algebra is old; spectral-phase extraction and feature covariance are the new measurement operator. |
| MY2026-247 | MY2019-026 | Reuse the metric Fermat derivation; SN2025wny needs its own authenticated lens map and spectral-delay likelihood. |

The 2026 new-information text and rendered reuse instructions generally preserve these distinctions. Explicitly naming these MY IDs in reuse notes would reduce duplicate execution, but they should not be hard dependencies unless their actual result is needed and exists.

## Dependency and obligation summary

Primary-source authentication -> measured-data payload -> candidate action-to-observable map -> selection/calibration likelihood -> measured result -> scoped common-action gate implication. Source authentication was rechecked at page/abstract level; data payloads and candidate maps remain named open inputs. The work orders generally preserve this dependency chain. The cheapest next action is to correct -077, clarify -194/-153/-080/-165, regenerate the affected cards, and verify their rendered equation/condition blocks. No science execution is necessary for those authoring corrections.

## Reviewed artifact hashes

- `2026_tasks.json`: `ba6e3bedff8c91a403a5b480ab054a4321b1a8d1895aafc2312af46a97cee8e0`
- `2026_sources.json`: `7ca0bb0f64e1bc480022ac31226101811ded49f11eeaaff7fc812aa5f61ddcc1`
- `2018_tasks.json`: `dea8f151dd068107b11dac46eb4b6795ca541b3ba14839f729417ab8fab2eaa1`
- `2019_tasks.json`: `300d08d2f0fd3817d075989ff2b2eae96ddd62c729fd702082125e0a2e31b128`
