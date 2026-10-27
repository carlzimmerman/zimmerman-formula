# Owner arrivals CFG919/920: impact on capture and source closure

Read-only reconciliation, 2026-10-20. This ingests the owner results committed as CFG919 `8c46b7a2e` and CFG920 `b2d0bff6a`, after the original closure checkpoint `f659e6d8e1ee4cf2b756f091aff56b018da1fb1e`. No scientific rerun, empirical fit, replacement gate or change to an existing packet was made.

**Closure impact:** neither arrival closes the physical capture/source gap. CFG919 finds a coarse ordering of excess by support class but contradicts the tested one-parameter selector at the primary systematic floor, with an explicit fragility qualification. CFG920 leaves D-i **UNDERDETERMINED** at its declared sample-median level, while exposing conditional per-dwarf failures and a demanding timing/chemical model. An ordering is not a force-law derivation; chemical tension is not an unconditional falsification of D-i.

## CFG919: ordering survives; the simple selector does not pass

The frozen hypothesis H-KIN asks whether one pressure-support measure determines the excess at matched baryonic acceleration. Its primary measure is f_P=3σ²/(v²+3σ²). In the raw result, V0 is **SELECTOR CONTRADICTED on both footings, both AS FROZEN and UNDER A1**, and **FRAGILE**. The contradiction is `C3 (F1 and F2 FAIL)`: C1 and C2 have zero elements under both rules, and no class-weighted W test triggers.

| raw V0 result | canonical | alt |
|---|---:|---:|
| ordering statistic T | 0.528473 | 0.528208 |
| ordering permutation p | 0.002 | 0.002 |
| F1: E=A f_P, χ²/32 dof | 89.4155/32 | 93.5256/32 |
| F1 p | 2.4759×10⁻⁷ | 6.0990×10⁻⁸ |
| F2: fixed pressure step, p | 1.4287×10⁻⁸ | 1.3803×10⁻⁸ |

Pressure/spheroid classes tend to sit above rotation/disc classes. That is an empirical class-ordering result under the adopted proxies and covariance, not evidence that a single pressure fraction fixes the amount of retained cold mass. In matched low-acceleration windows the dwarfs' E is about 3–5 times the spheroid lenses' E, whereas the linear f_P ratio is only 1/0.8=1.25. At assigned f_P≈1, dwarf and cluster residuals have different acceleration trends. These facts explain why ordering can coexist with failed common forms. They do not validate a new force law, a baryonic-stress source term, or a unique capture selector.

**Sensitivity must remain beside the headline.** The primary floor is 0.05 dex per cell. Under declared V6, a 0.10-dex floor, F1 has p=0.05619 canonical and p=0.03838 alt; the resulting classes are **SUPPORTED** and **NOT DIAGNOSTIC**, respectively. The primary contradiction is therefore explicitly FRAGILE. V1–V5 and V7 retain the contradiction. One cannot quote an unconditional rejection of every kinematic selector, or an established universal selector, from these results.

**Frozen versus post hoc calibration.** Criteria are `8d34dc761`; A1 is `5c9edd07b`, explicitly POST HOC after the frozen injection test failed. Frozen I1 recovered SUPPORTED in 85% of 200 injected linear-selector realizations, below the required 90%; A1 recovers 91%. Frozen/A1 I2 is 92%/92.5%, and I0 is 0.5%. Shuffle controls bite. A1 changes C1's comparison to the pressure-supported mean; it does not change the form fits or the observed V0 classification because C1 never fires. Thus the raw frozen result and A1 result agree, while the original injection-calibration failure remains part of the record. The agreement is not a license to erase A1's post hoc status.

**Proxy and coverage limits.** Dwarf f_P is assigned by class; the lane lacks dwarf/cluster within-class kinematic measurements. Lensing f_P=0.2/0.8 is a Sérsic proxy for central galaxies, while its gravity measurement is at 30–300 kpc. SPARC uses measured rotation and an assumed gas dispersion; globular rotation is measured for 10 of 31 and otherwise imputed, and globular tests carry no class weight because of stiffness screening. Early-type galaxies with dynamics are NOT TESTED. The dwarf mass/gas convention differs from the SFH-based CFG827 sample used by CFG920.

## What CFG919 does and does not imply for the source

The displayed CFG638 kinetic system has baryonic density as an input through Φ, the phantom target and related clock/region definitions. It has no direct baryonic velocity or stress-tensor argument. This supports the narrow structural statement: **with the same complete baryonic density field and the same other dynamical inputs/state, changing only the label “rotation” to “pressure support” cannot change this closure's instantaneous equations.** In the declared spherical, deficit-closed settled branch, the target profile is fixed by M_b(<r).

That statement should not be expanded into a theorem at fixed *one-number* g_bar: matching g_bar does not match the full three-dimensional density, geometry, assembly history or boundary state. Nor is arbitrary stationarity equivalent to v_s=0 without further assumptions; the relevant branch here is the specifically settled deficit-closed state. Time-dependent density history or non-spherical geometry can correlate with support without a direct stress coupling. Those possibilities were not solved by CFG919.

To insert a direct kinematic retention/source rule into the present model would add a constitutive input; the data ordering does not derive it. No stress term, source variation, reciprocal work, microscopic latch, population stock or bath is supplied by the new selector fit. CFG919 therefore leaves the existing capture package's O1/O4 source/transition obligations open. It particularly prevents replacing the missing binding physics with a claimed validated universal f_P gate.

## CFG920: sample underdetermination with conditional object-level failures

Criteria `a229bb78c` test a **condition of D-i**, inherited by CFG916: cold mass bound at formation, retained while baryons are subsequently lost. The input amount relation is L_req=exp(4E_σ), with E_σ=ln(σ_obs/σ_law), deep-regime and retained-component dominated. The graded chemical model is a one-zone homogeneous leaky box, primordial start, no inflow, instantaneous recycling/mixing, a constant wind at ISM metallicity, Fe yields log y=−0.5/−0.2/+0.1, and W1 wind versus W2 wind plus terminal removal. Unmixed unseen loss can raise the amount but cannot lower its chemical minimum. These are hypotheses, not measured formation masses or a derived cold-formation history.

The raw main JSON reports **UNDERDETERMINED on both footings and overall**. There are 20 metallicity-tested objects and eight NOT TESTED. The tested-set median required loss is 3.81485 canonical / 3.18485 alt; the familiar 4.32471 is the earlier all-28 canonical median and must not replace the tested-set denominator.

| sample-median corner | median chemical minimum | ratio canonical, 16–84% | ratio alt, 16–84% |
|---|---:|---:|---:|
| −0.5 yield, W2 | 3.34360 | 1.14094 [0.83059, 3.14407] | 0.95252 [0.69220, 2.62485] |
| +0.1 yield, W2 | 12.51566 | 0.30481 [0.21813, 0.66004] | 0.25447 [0.18170, 0.55176] |
| +0.1 yield, W1 | 17.40698 | 0.21916 [0.15589, 0.64708] | 0.18296 [0.13035, 0.53935] |

The favorable yield corner spans compatibility with the required loss; it is not itself a formal sample COMPATIBLE result. Both high-yield corners exclude the amount by the declared bootstrap criterion. Because exclusion does not hold across the entire frozen bracket, the overall median is UNDERDETERMINED. The nominal-yield median intervals also cross the permitted boundary. Do not promote the high-yield result into a bracket-independent D-i falsification.

The individual failures remain consequential under the same assumptions. At the frozen 1σ grading, canonical has 1 COMPATIBLE / 15 UNDERDETERMINED / 4 CONTRADICTED; alt has 0/15/5. The four shared contradicted objects are Hercules, Andromeda II, Cetus and IC 1613; alt also has Leo IV. At the reported 2σ variant only Hercules remains CONTRADICTED on each footing. These are conditional object-level contradictions, not a claim that a universal all-object model has passed merely because its aggregate median is underdetermined.

**Direction matters:** metal-poor gas-free dwarfs often require *more* chemical baryon loss than D-i can retain without overpredicting their observed excess. Adding unseen loss cannot fix that mismatch; it raises the loss further. The reported post hoc gas-free/gas-bearing summary finds E_pred>E_obs for all 11 gas-free dwarfs at the nominal yield, and 8/11 canonical or 9/11 alt in the favorable low-yield W2 corner. This split summary was added after the full run from already stored values and has no new class weight.

The timing map is reported, not graded. Under its SF-onset binding convention, seven canonical objects at yield −0.5 fit the amount only after 51–99.9% of their star formation; late-tail dates are resolution-limited. Such delayed binding changes D-i's “bound at formation” premise. It is not a physical derivation of a delayed latch. Metal-enhanced winds (ζ≈3–19 for several canonical cases, larger for others) and pristine inflow are outside the graded bracket; they are possible modeling escapes with a stated price, not detected processes or demonstrated rescues. Hercules remains especially difficult inside that restricted chemical model.

For gas-bearing dwarfs, stars-only L_req often needs extra loss that the metallicity does not observe. Counting all HI in the law's baryons lowers L_req below one for six of nine. The amount problem is therefore sensitive to the inherited gas bookkeeping, and the all-gas variant itself remains a bracket on the actual baryons within the kinematic aperture. No gas-rich object should be used as an unqualified proof of a retained cold stock.

K1–K4 pass in the stored result, including recovery of the earlier dynamical and leaky-box estimators. MUTATE changes the canonical median from CONTRADICTED at L=1 to UNDERDETERMINED at L=20 and changes 17/20 per-dwarf classes. This shows the existing classifier responds to loading; it does not validate the leaky-box assumptions. The small-u implementation repair preceded any number, and the reporting fix/post hoc split are disclosed without a new gate. No scientific rerun was performed for this receipt.

## Reconciliation with the capture package

1. **The missing physical transition remains missing.** Neither arrival identifies the internal state that stores binding/ownership, its energy, receiver, reciprocal force, phase-space reaction kernel or finite release rate. The non-injectivity and finite-temperature qualifications on literal exact LR-c remain unchanged.
2. **D-i's historical stock remains conditional.** CFG920 constrains how much and when baryons could be lost in a declared chemical model. It does not show that cold material remains bound during that loss or solve the falling-capacity problem C−t<0 in the minimal site model. A delayed latch or a different chemical history would require an explicitly changed physical history.
3. **No new force law or selector is licensed.** CFG919's ordering gives a descriptive target for a future physical mechanism; its common forms do not pass at the primary floor and are systematic-sensitive. Replacing a density/history label with f_P would add a new posit, not close source variation or conservative bookkeeping.
4. **The merger/escape/release obligations are unaffected.** Chemistry and class ordering do not convert a spherical Jacobi cut into a phase-space escape theorem, give a retained fraction, or supply the second release clock. The analytic counterexample and conditional sequential-clock bounds in RESULT.md stand within their original scope.

**Convention warning:** CFG919 defines E_g=ln(g_obs/g_pred), equal to 2ln(σ_obs/σ_law) for its dwarfs; CFG920 uses E_σ=ln(σ_obs/σ_law). Even with identical baryonic conventions, D-i would be L=exp(2E_g), not exp(4E_g). Here the samples and stellar/gas masses also differ, so the numerical E values must not be interchanged or pooled.

The next substantive capture/source step is still one physical binding/history state with its energy, receiver, material stock and derived finite transition, tested through baryon loss and subsequent escape/transport. For D-i specifically, independent yield/SN-Ia, MDF or formation-time information would reduce the current chemical underdetermination. This receipt introduces no replacement gate or additional fit. κ=1/2 remains fitted; cold mass remains required; theory closure is not established.

## Receipt and exact version

`OWNER_ARRIVAL_919_920_RECEIPT.json` records the exact byte counts and SHA-256 of all 17 owner-lane files, observed HEAD/time, owner/freeze/A1/ledger commit identifiers, and hashes of the existing capture/source context. Every observed owner file matches its stated result commit byte for byte. These are source-identity checks, not a scientific rerun.

Raw result hashes:

- CFG919 `cfg919_results.json`: `c4d0e6dfa9733070edd1cf80b19972669aefc9de9de6e0cd219d417ba4a18549`.
- CFG920 `cfg920_results.json`: `d9b6ae90f7fb864ac4c8173ea3bb22fbc8f94976107560ac40d9d19b1119ff3b`.

Only this report and its receipt were written for this arrival. Completed observational and normalization evidence, capture results, owner sources, frozen criteria and prior packet inventories were not modified.
