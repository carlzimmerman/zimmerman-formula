# CFG940 finalized arrival: the primary acceleration window is empty

New checkpoint, 2026-10-20. This appends finalized evidence to the earlier criteria-only observation in `CLAUDE_937_ARRIVAL.md`; that historical audit is unchanged. No Claude case, control shuffle or physical experiment was rerun. Source bytes and independent arithmetic checks are pinned in `sources_claude_940.json`.

**Primary result: NOT DIAGNOSTIC (DATA).** None of the25 gas-rich rotators occupies the predeclared `g_bar < 1e-12 m/s^2` window at its measured radius. The secondary all25 result is estimator-dependent. The useful selector clue is a matched-acceleration pressure-supported/rotating contrast at somewhat higher acceleration, rather than validation of a dwarf formation mechanism or a generic dark-matter conclusion.

## Revision identity and scope

| Evidence | Exact commit |
|---|---|
| Criteria alone | `798e98d78e8019c983bc01e0f94b8cee81478318` |
| Post-hoc amendment A1 and failed pre-A1 K outputs | `bda93d8dbf001285907cbfabdafd42cc701d58a5` |
| Script, raw results/stdout and controls | `7c7fc125e745daab8ca042023e6bdd824dce7a5f` |
| Final README | `ba794bf4f47ce1bfeb3b78aedc6e601b5ab9976f` |
| Ledger arrival | `cad364953f1f655df89f269f9caa46f7ed816a33` |

All14 current lane files match their corresponding committed blobs exactly. Main-result SHA-256 is `d8e8c97eeed952f20f765db738c58ee2b1e0b6a4fdb49481953157c07dfa397c`; script is `8910ca27bcee4504e481fd101806dc01c1d070a33aaf7464ea9347f6161aa4ac`; final README is `03567a2cd39144276bc18568f6000eb205c6cafd7302703e37258ae9b2413dc6`.

The lane tests an empirical gravity law/kernel against on-disk McQuinn+2022 kinematics, using two separately retained a0 footings. Its collisionless-halo/framework interpretation is distinct from this packet's alternative Psi/X/chi field action. No scalar mass/time normalization, capture, torque or microscopic radiation law is measured here. The residual is **dex in acceleration**, `E=log10(g_obs/g_law)`, not CFG937's `ln sigma` or the field solver's energy.

## Primary gate versus the secondary estimator bracket

`g_obs=V_cor^2/R_max`; primary A uses **total** tabulated baryonic mass in `g_bar=GM_bary/R_max^2`, an upper bound for a spherical enclosed-mass interpretation. Bracket B uses modeled enclosed exponential-disc masses. It is a separate mass estimator; changing A to B raises the mean residual by about0.22 dex.

Independent MRT parsing reproduces all25 radii and A accelerations, and B's enclosed fractions using the recorded scale lengths. All100 per-object A/B/footing residuals agree within1e-13. Every saved W1 entry has N0; its data gate requires at least5. Base-estimator minima are log10(g_bar) **-11.714899 for A (AGC229053)** and **-11.961940 for B (DDO154)**. These are nominal measurements under the frozen estimator/gate, not a proof that uncertain true accelerations cannot cross the threshold.

The secondary all25 means are:

| Estimator | Canonical E +/- se, dex | Alternate E +/- se, dex | Secondary class |
|---|---:|---:|---|
| A, total baryons | -0.304123 +/-0.067517 | -0.340186 +/-0.067392 | S-BELOW |
| B, enclosed discs | -0.083328 +/-0.063744 | -0.121319 +/-0.063731 | S-ON |

B2 gives S-BELOW, B3/B4 S-ON, and B5/B6 split by footing. The combined upward systematic corner reaches S-ON (+0.117258/+0.079246 dex). Thus the primary empty-window class must not be replaced by the secondary S-BELOW or S-ON label, and A's deficit is not established as a failure of the underlying law. The overlap check is INFO only: seven shared SPARC galaxies show median McQuinn/SPARC speed ratio0.873 and residual offsets -0.177 dex under A versus +0.002 under B. These are limitations of a single-radius comparison, rather than a new cold-matter normalization.

## Matched contrast and the four-dwarf selector

The only eligible dSph cell is `1e-12 <= g_bar < 10^-11.5`, with six dSphs. Their mean residual is +0.239537 canonical/+0.201039 alternate dex. For A, five rotators match that cell and `D=E_dSph-E_rot=+0.438297 +/-0.122278` canonical (+0.437835 +/-0.122184 alternate). For B,18 rotators match and D is +0.317797 +/-0.107884 (+0.317551 +/-0.107821 alternate). Independently selecting the rotators from the per-object table reproduces their matched means and all four contrasts. Matching uses a0-independent baryonic acceleration bins; footings are not pooled.

This retains a population/kinematic clue: at the available matched acceleration, the pressure-supported objects show more excess than gas-rich rotators. It does **not** sample the lower-acceleration interval containing the strongest dSph excess, nor isolate the Draco/Sextans versus Fornax/Leo I retention rule. Sextans A/B in this gas-rich sample are different galaxies from the target Sextans dSph. A universal mass-filling or cooling prescription cannot be declared successful by adding the same excess to every small galaxy; it needs a physical dependence on assembly, geometry, gas/stellar dynamics and the relevant enclosed radius, tested without tuned per-galaxy efficiencies. CFG940 supplies no such dependence, transport history or survival calculation.

## Controls and precise qualifications

The frozen K3 radius check first failed; its exit2/no-class record remains preserved. A1 changes only the tolerance for comparing rounded diameters/radii; primary recomputed radii are unchanged. Post-A1 K checks pass. All148 saved main classifications independently follow the frozen thresholds. Four secondary means, the canonical aggregation errors and matched contrasts have been independently checked. The plant controls have12 required secondary successes; all four primary-window plants are unavailable because N0. Shuffle arithmetic passes all four secondary S1 checks and the one required S2 check. The primary shuffle checks are skipped, so neither control establishes power in the missing W1 population. Some NumPy boolean fields were serialized as literal strings `"True"`/`"False"`; this audit recomputed the numeric requirements instead of treating nonempty strings as booleans.

Three source/report qualifications do not change the lane classification:

- The README/ledger attributes both minima to DDO154. The A minimum is actually AGC229053; B's minimum is DDO154.
- The ledger's "All25 above Newton" overstates an ensemble result. Five objects have negative individual `log10(g_obs/g_bar)` under A (AGC110482, DDO125, UGC04483, UGCA292, DDO53). All25 are individually above Newton under B; the ensemble means are above Newton under both estimators. Neither statement uniquely identifies cold energy or a microscopic matter model.
- A1's conversion of diameter rounding is conservative by a factor2: because `R=DPV*distance/2`, a diameter rounding of +/-0.5 arcsec contributes +/-0.25 arcsec times distance to R. The written A1 tolerance adds0.5 arcsec times distance. Independently using the half-diameter contribution still passes all25 comparisons (maximum error/tolerance0.929552); the original0.051 kpc check fails. No frozen tolerance or result was changed here.

The finalized evidence narrows the observational selector problem and preserves an explicit data gap. It does not complete the cold-energy mechanisms or settle the four dwarf mass/overboost budgets.
