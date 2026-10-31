# SI3_nested_isolation: FROZEN CRITERIA (committed alone, before any script output or model number on these samples)

**Question.** Route E (Newtonian halos of cold dark energy, no a₀ force) loses to the a₀ law on KiDS photometric "isolated" lensing by Δχ² +434 (X53 harness at FC1's rule, B21's released bins). Is that lead environmental? Grade route E and the law on the nested photo-z isolation samples, and see how Δχ² = χ²(route E) − χ²(law) moves as isolation tightens.

**What is already known to me.** F2's law amplitudes on the raw stacks of these samples (F2 README), X53's and FC1's numbers on B21's bins, SI1 and SI2 on spectroscopic lenses, and Argon's predictions below. Route E has never been run on these samples. No I stack exists for them. A timing probe ran before this file: P2's record-path source loop on 900 positions shifted off the lenses, printing times only (0.54 ms of CPU per centre) and no shear number. That probe is why the hole term is in the plan.

## Data
**Lens stacks.** F2 Track B's per-lens arrays `WG_L`, `WW_L` (`cfg110_perlens.npz`), `PATCH`, `LBIN`, unchanged. 4 stellar-mass bins, 15 g_bar bins, 50 patches.

**Samples, F2's definitions executed from F2's text, nested:**
- S10 (181,477): no pool galaxy with lg M★ > lg M★,lens − 1 within 3/χ radians and |Δχ| < 10 Mpc.
- S20: the same at |Δχ| < 20. S30: the same at |Δχ| < 30.
- S_strict (40,576): S30, and no pool galaxy with lg M★ ≥ lg M★,lens within 1 Mpc physical and |Δχ| < 100 Mpc.
- S_x300 (21,571): S30, and the same host veto at |Δχ| < 300 Mpc.

**Hole term.** I is the stack around isolated random points, built for each sample separately:
- **Clones.** Each point takes a lens drawn with replacement from that sample (lenses in mass bins 1 to 4): its z, χ, lg M★, M_gal and mass bin.
- **Footprint.** CFG903's rule: uniform on the sphere in the two KiDS field boxes (split at Dec −15), kept if the nearest of all 1,239,422 KiDS-bright rows lies within 4′ and has `masked` = 0.
- **Veto.** The sample's own veto with the clone's z, χ and lg M★, against the same pool, with no self-exclusion.
- **Counts.** I: 4 N_S accepted points. R (plain randoms, same clones and footprint, no veto, reported only): 2 N_S points. Master seed 20261031, one spawned stream per catalogue.
- **Estimator.** P2's `measure` in its record path, executed from P2's text, on F1's source cache, plus the record's rule that a centre with fewer than 5 background sources contributes nothing. Same g_bar bins per clone from its M_gal, same 1+K, same data factor as Track B.
- **Patches.** The agentK scheme with its quantile edges from the June lenses, applied to the points' positions, paired with the lenses in the jackknife.

**Data vectors.** Primary: Δ = L − I, per mass bin and g_bar bin, in Track B's native units. Reported: raw L, L − R, I − R.

## Models (both per lens, stacked with Track B's WW weights; nothing fitted)
- **Law:** F2's `table_RM`, `perlens_model` at CENTRAL with y_e = 0 (F2 L4).
- **Route E:** X53's `mass_H`, `halo_setup` at FC1's rule, by executing X79's and FC1's text with asserted replacements: smooth core, S = max(a₀/2πG, f_c η Σ_coll) on X53's path, EM1's M200 at lg(M★ + M_cold), sharp cut at R200. Same projector, same `LMG`, `LRT` tables.
- **No neighbour term in either graded model.** A photo-z catalogue cannot place neighbours along the line of sight, and SI1's T_nbr needs spectroscopic positions. This is a limit, listed below.

**Stellar-mass rungs, the same for both models (SI2's conventions).** R0: catalogue M★. R2: lenses with `typ` = 1 (u − r > 2.0) +0.295 dex in M★; blue unchanged; cold gas and hot CGM stay at catalogue M★; route E's M200 moves with M★ through EM1's relation; the g_bar bins do not move. The data vector does not change between rungs.

## Graded statistic
Δχ² = χ²(route E) − χ²(law), no fitted parameter, canonical primary, alt reported and never pooled.

**Bins.** Range "all": every (mass bin, g_bar bin) with 0.03 < R_med ≤ 3 Mpc, F2's R_med on S10, which is 59 of 60 cells. Ranges in (≤ 0.31), O1 (0.4 to 1.1), O2 (1.1 to 3), out (O1 + O2) are F2's `RANGE`.

**Covariance.** The 50-patch jackknife cannot invert 59 bins, since its rank is at most 49. I use it block-diagonal: one jackknife covariance per mass bin, over that block's p used bins (14 or 15), paired across L and I, inverted with SI1's Hartlap factor (50 − p − 2)/49. Covariance between mass bins is dropped. χ²(M) = Σ_b H_b rᵀ C_b⁻¹ r. Sub-ranges take the sub-block and its own Hartlap factor. B21's released matrix belongs to B21's sample and bins, so it cannot serve here.

**What that choice does is reported, not assumed:** on B21's bins, Δχ² with the released matrix against its own block-diagonal part; on these samples, the diagonal-only Δχ².

**Power.** D² = Σ_b H_b (m_H − m_L)ᵀ C_b⁻¹ (m_H − m_L). Δχ² has mean +D² if the law is true, −D² if route E is true, σ = 2D. Reported on every line: Q = Δχ²/D², which is +1 if the law is true and −1 if route E is true, σ = 2/D. Q is the number to compare between samples, because raw Δχ² falls with N whether or not anything environmental happens.

**Classes, SI1's, per line:**
- **NOT POWERED:** D < 3.
- **LAW PREFERRED:** D ≥ 3, Δχ² ≥ 0, |Δχ² − D²| ≤ 4D.
- **ROUTE E PREFERRED:** D ≥ 3, Δχ² ≤ 0, |Δχ² + D²| ≤ 4D.
- **NEITHER:** otherwise. Goodness of fit, χ²/n and p from χ²(n), is reported for each model.

## Frozen verdict (canonical, R2, Δ = L − I, S_strict; S_x300's label printed beside it)
- **LEAD SURVIVES STRICT ISOLATION:** D ≥ 5, Δχ² ≥ D² − 4D, and route E's p < 0.01. This is the brief's line: then KiDS's preference is not environmental at this isolation.
- **LEAD GONE AT STRICT ISOLATION:** D ≥ 3 and Δχ² < D² − 4D. The law's expected lead is rejected at 2σ on the low side. This is what an environmental lead would do. It does not show the lead was environmental.
- **NOT POWERED:** D < 3.
- **MIXED:** anything else.

If S_x300's label differs from S_strict's, the lane verdict says so in the same line. Any failed check makes the verdict NO VERDICT. If the hole term cannot be built or fails its checks, the Δ lines read NOT DONE or NO VERDICT, the raw L results are delivered as raw L, and nothing stands in for I.

## Argon's frozen lines (`ARGON_REPLY_2026-10-31/PREDICTIONS_ON_RECORD.md`, 01c405354a), scored after the run
At R2 with Δ = L − I, Δχ² = route E − law:

| Sample | Argon's Δχ² |
|---|---|
| S10 | +280 to +350 |
| S30 | +80 to +140 |
| S_strict | −5 to +15 |

S_strict amplitudes: A_O1 data/route E 1.35 ± 0.25, A_O2 data/law at or below 0.35.
- **Argon's pass line:** Δχ² at or below +15 on S_strict, with A_O2 consistent with 1 within 2σ. Its text doesn't name the model for that A_O2. I read it as route E's, because its own line puts the law's at or below 0.35. Both are printed.
- **Argon's fail line:** D at or above 5 with Δχ² at or above +25.
- **Argon's falsifier:** above +30 on S_strict, it says environment is falsified as the excuse for KiDS's +434.

Argon's text doesn't state the covariance or whether a two-halo term is in the model. Those choices are mine and are frozen here. Each band is scored HIT or MISS on the graded statistic, canonical, and also printed on X53's two-halo line. A band's score on either line is conditional on these choices.

## Reported, not graded
- **X53's two-halo line, the statistic of the +434.** Each model plus b T₂ with b ≥ 0 fitted per mass bin (4 per model), T₂ being CFG805's template evaluated per lens at R70 with X53's exclusion radii, on the same block covariance. It is not a grade because X53's ledger (A12) records its initial conditions as ΛCDM-inherited, and its 4 amplitudes are knobs (F2's audit). Its expected separations are the fit of b T₂ to the other model's best fit, as in X53's forecast lines. Printed for every sample beside the graded Δχ².
- **Halo continued to r_ta,** SI1's profile E with one z_ta, S_strict's lens-weighted median z. Graded statistic, every sample, R0 and R2, both footings.
- **A_in, A_O1, A_O2** for both models, by F2's estimator, on every line.
- **Raw L and L − R** at R0 and R2, same statistic and classes. **I − R** in O1 and O2, the hole's own size, against its jackknife error.
- **Inner and outer Δχ²,** per-mass-bin Δχ², Q ladder, and paired-jackknife errors on Q(S10) − Q(S_strict) and Q(S10) − Q(S_x300) with each sample's covariance held fixed.
- **Lens/I source-weight ratio** per range.

## Checks (any failure makes the verdict NO VERDICT; a K_H failure touches only the Δ lines)
- **K0:** F2's `trackB_stats` executed from F2's text, and my own stack function, both reproduce F2's committed law A_in, A_O1, A_O2 and their errors at y_e = 0 on S10, S20, S30, S_strict and S_x300, both footings, |d| ≤ 1e-9.
- **K1:** at R0 on B21's bins, my execution of X53's text at FC1's rule reproduces the committed `FC1_cold_share_native_eta/x79_rule/x79_kids_results_native.json`: χ² of L, H, L2H, H2H and the b values on primary and all radii, both footings, |d| ≤ 1e-9.
- **K2:** on 300 seeded lenses, stacked route E and law models from the tables agree with direct projection within 1 % in every used bin. M_h(R200) = M200 within 1e-8.
- **K_H1:** P2's record path on 3,000 seeded real lenses across the footprint reproduces `cfg110_perlens.npz`: summed WW within 1e-6, stacked ΔΣ within 1e-3 σ per bin, and CFG116's WX in the same way, sign checked.
- **K_H2:** my veto function on all 181,477 real lenses with self-exclusion returns S10, S20, S30, `host` and `host300` exactly.
- **K_H3:** the patch edges reproduce the June labels exactly. The lens/I source-weight ratio per centre, averaged over O2, lies within 0.10 of 1 on every sample.
- **K_H4:** cross-shear null of Δ, block statistic, p ≥ 0.001 on every sample.
- **K_H5:** I from two random halves of its points: their difference, block statistic, p ≥ 0.001 on every sample.
- **MUTATE (`--mutate`, separate outputs):** route E's halo × 0.5, lens WG × 1.10, I built from cross shear. K0 and K1 must fail, m_H must fall in every used bin, every sample's χ²(route E) and Δ must change, and the run must print NO VERDICT and exit 1.

## What this cannot show
- **Neighbours.** The graded models have no neighbour term, which leans toward the law, because route E's mass sits in halos and neighbours that survive the veto add signal. SI1 measured that term at +3.7 in Δχ² on N = 10,620. X53's two-halo line is the only proxy here.
- **Leakage.** F2's AMENDMENT A1 estimates S_strict still leaks about 38 % of hosts. Δ removes the hole, not leaked hosts. S_x300's window captures about 99 %, and it was defined after F2's result.
- **R2 is an open choice,** taken from the record, and a reading at R2 is conditional on it.
- **Route E's rule is taken as given.** EM1's M200 relation was calibrated with NFW halos and Bullock c(M), which the record's own audit flags. FC1's rule on X53's path is what this lane tests, nothing else.
- **Sample.** S10 is the record's reconstruction of B21's sample (181k against 259k), and its re-measurement runs 1.15 × B21 (F2 K4b). Absolute Δχ² here is not directly comparable with +434. Q and the ladder are the comparison.
- **Covariance.** Dropping cross-mass terms and using a noisy jackknife inverse both affect χ². Hartlap corrects only the mean.
- A preference here compares two members of this record only.

## Resources
One thread, `nice -n 15`, under about 2 GB, at most two processes at once. No downloads. Nothing outside this lane is written except scratch work files.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. The theory stays open. Nothing here says the data favour the framework.
