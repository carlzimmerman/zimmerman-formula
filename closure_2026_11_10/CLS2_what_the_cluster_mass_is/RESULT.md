# CLS2 RESULT: what IS the cluster's non-baryonic mass under form B? (2026-11-11)

**Label, canonical and alt: NO CANDIDATE / NO CANDIDATE.**
All four candidates are killed or fail on both footings. (a) and (b) and (d) are KILLED BY PROOF; (c) FAILS on a
budget. Nothing in this lane supplies the cluster's missing mass.

Criteria 7630e48454, committed alone before any script or number. TEST lane, quarantined: adopts nothing, relabels
nothing (RB1's, XCV1's, CLS1's, DD1's and AKS1's labels stand), registers nothing. Footings never pooled. Cold dark
energy is a gravitating field component, never a particle. kappa = 1/2 FITTED; not theory closed.

## What was being explained

On the seven X-COP clusters, with their real gas and stellar profiles and DT2's frozen five nodes (0.1, 0.2, 0.3, 0.5,
0.7 R500):

| footing | bare-law residual, mean over the 35 nodes | median over the seven clusters | range | KA1 |
|---|---|---|---|---|
| canonical | **0.46749895** | 0.457 | 0.422 (A2142) .. 0.550 (A644) | PASS (DT2/CLS1 0.46749899) |
| alt | **0.43452306** | 0.423 | 0.389 (A2142) .. 0.517 (A644) | PASS (DT2/CLS1 0.43452310) |

Per cluster (canonical || alt): A1795 0.451 || 0.418, A2029 0.467 || 0.435, A2142 0.422 || 0.389, A2319 0.493 ||
0.460, A644 0.550 || 0.517, A85 0.433 || 0.399, ZW1215 0.457 || 0.423. Statistical errors from EM_FORW alone are
0.004-0.011 dex; the excess is 40-100 se, consistent with DD1's "15-24 se" on its own statistic.

Cross-checks against DD1's frozen table (read-only): X-COP 129 points, +0.466 || +0.434 dex; **CLASH 84 points, 20
clusters, +0.527 || +0.498 dex** (KA6, KA7 PASS).

The measured dynamical mass is **2.93x (canonical) / 2.72x (alt)** what the law gives from the same baryons. That is
the number every candidate has to reproduce.

## The four candidates

### (a) Non-hydrostatic support — KILLED BY PROOF (all three kills fire)

- **Wrong sign, and it is the wrong sign on every cluster.** Recomputed from the HeCS-omnibus table on disk, the
  caustic (non-hydrostatic) mass divided by the hydrostatic mass at each cluster's own R200: A85 0.819, A1795 0.776,
  A2029 0.768, ZW1215 0.736, A2142 0.521 — **median 0.768, five of five below 1** (A2319 and A644 have no row in the
  HeCS-omnibus table at all — the same coverage gap XCV1 reports, 6 of 12 X-COP clusters). Removing the hydrostatic
  assumption *lowers* the mass. So (a) does not supply the missing mass, it takes mass away: the residual moves
  **+0.115 dex** the wrong way, 0.457 -> 0.572 (canonical) and 0.423 -> 0.538 (alt).
- **Not an artifact of hydrostatic equilibrium at all.** The CLASH residual, computed from 84 points in 20 clusters
  whose masses are *lensing* masses, is +0.527 || +0.498 dex. The excess is present where no HSE assumption is made.
- **Unavailable to form B.** CLS1 S2a: the clock's stress in action (A) is a perfect fluid (sympy, residual 0) — one
  velocity per point, isotropic p = n x / 2, zero momentum density. There is no collisionless or velocity-dispersion
  pressure for the cold component to supply.
- **What XCV1 actually establishes, stated plainly.** XCV1's post hoc A1 reading does *not* show that non-hydrostatic
  support relieves the ceiling. It shows the opposite: the caustic masses are ~23 % *below* the hydrostatic masses at
  the same radius, so f_ret rises from the hydrostatic 1.03 to 1.37. XCV1's own verdict is that item 6 "gets worse, not
  better" and stays open. Its frozen label is NO VERDICT (a KA failure), and its A1 label AT THE CEILING carries the
  caustic method's 40 % scatter, so it cannot even call the direction at 95 %. Read here, against the sign of the
  effect rather than its significance, XCV1 is a *kill* for (a), not a rescue.

### (b) The dust term pooled in the well — KILLED BY PROOF (all three kills fire)

The pooled dust is the leading-order response rho = (mu^2 / 4 pi G)(Psi - Psi(R_out)); the first iteration uses the
observed well only and is a strict lower bound, because the dust's own gravity only deepens the well.

| row | canonical | alt |
|---|---|---|
| R_b = M_dust(198.25/Mpc) / M_nonbaryonic,obs, median over seven | **3.78e3** (log10 **+3.58 dex**) | same (a0-free) |
| per cluster R_b | 2.63e3 (A1795) .. 4.29e3 (A2142) | — |
| R_b at the CMB-lensing line mu_J = 2.512e4/Mpc | 6.07e7 | — |
| **M_dust / the law's phantom** (AKS1 T5's own ratio) | **1.71e4** | 1.52e4 |
| mu_fit: the mu_K that would pool exactly the observed mass | **3.22/Mpc** (3.03-3.87) | same |
| self-consistent pooling iteration | **diverges on all seven** (growth 4.5e3-6.8e3 per iteration) | — |

- **"Is the +0.5 dex exactly that factor?" No — and it is not close.** The cluster needs a factor 2.93. The dust at
  the CMB mu_K gives 3.78e3 against the observed non-baryonic mass, and 1.71e4 against the law's phantom. AKS1 T5's
  quoted **3.6-8.4** is a *SPARC-radius* number; in a cluster the same term is **2 000 to 4 700 times larger**. The
  reason is in the exact point-mass form (sympy, KA5): M_dust / M_ph = (mu R)^2 / 6 x sqrt(g_N / a0). At fixed mu_K the
  factor grows as R^2, and the aperture grows from ~10 kpc to 600-1400 kpc. So the over-capture and the needed
  shortfall are not the same number anywhere: (b) overshoots by **3.11 dex**, not by 0.
- **The mu_K that would fit is 61x below the CMB line.** mu_fit = 3.22/Mpc against form B's required 198.25/Mpc.
- **And it lands exactly in the region CLS1 already emptied.** 3.22/Mpc is *inside* CLS1's common cluster window
  2.97-4.43/Mpc — the only window the necessary conditions leave — which is where CLS1's dense scan built **0 of 7**
  states (best miss 2.6 half-widths at A2319). So the "fit" value of mu_K is not merely below the CMB line; it sits in
  the one place CLS1 proved by construction that no cluster state exists.
- **There is no profile to pool.** At mu_K = 198.25/Mpc the self-consistent iteration has no fixed point: the dust's
  own gravity amplifies the response by 4.5e3 to 6.8e3 per pass on every cluster. That is the same fact CLS1's S2c
  expresses as a 396-to-2,192 violation of the enthalpy-span inequality.

*Correction to the frozen hand-estimate:* the criteria's section 8 wrote the point-mass coefficient as 1/2; the exact
value with the outer-boundary subtraction is **1/6** (KA5, sympy residual 0). This lowers (b)'s over-capture by a
factor 3 and does not change any verdict.

### (c) The gas is under-counted — FAILS (both kills fire, both footings)

The baryons the law needs are the exact inverse image M_b,req = F_src(M_FORW, r, a0).

| footing | median R_gas = M_b,req / M_b | per cluster | median f_b,req = M_b,req / M_FORW | cosmic share | all seven over the share |
|---|---|---|---|---|---|
| canonical | **5.01** | 4.39 (A2142) .. 6.90 (A644) | **0.602** (0.544-0.636) | 0.156 | **yes** |
| alt | **4.66** | 4.06 (A2142) .. 6.43 (A644) | **0.557** (0.497-0.593) | 0.156 | **yes** |

The gas would have to be under-counted by ~5x (and since the gas is ~80 % of the cluster's baryons, the X-ray gas mass
itself by ~6x), and the cluster would then hold 56-60 % of its mass in baryons where the universe has 15.6 %. That is
not a census error, it is a different baryon budget. HY4-1 (GAS1) is grading the census bin by bin; this lane only
reports the size of the required revision, which is 3.5-4.1x the entire cosmic share.

### (d) Superposition of galaxy halos, one per member — KILLED BY PROOF (K-D1 and K-D3 fire; K-D2 does not)

Two readings, and the gap between them is the result.

**d-TRUNC — the EFE reading, no free parameters.** Each member's halo is truncated where its internal field falls to
the cluster's field; the phantom per unit member mass is m f(g_ext), f(g) = (sqrt(1 + 4 a0/g) - 1)/2 (KA4, sympy
residual 0).

| reading | canonical | alt | against the bare law |
|---|---|---|---|
| d-TRUNC (every baryon in a member) | **+0.507** dex | +0.475 | **worse** than +0.457 / +0.423 |
| d-TRUNC-s (only the stars in members, gas at cluster level) | **+0.462** | +0.429 | **equal to within 0.005 / 0.006 dex** |

Per cluster, d-TRUNC: A1795 0.507 || 0.475, A2029 0.521 || 0.491, A2142 0.453 || 0.422, A2319 0.517 || 0.485,
A644 0.595 || 0.563, A85 0.465 || 0.432, ZW1215 0.479 || 0.445.

So the honest answer to "what does the per-galaxy rule give in a cluster" is: **the cluster law, or less.** d-TRUNC-s
reproduces the cluster-level law to 0.005 dex on the same seven clusters with the same profiles — a numerical
demonstration, not an assumption, of K-D3. The identity behind it is that the truncation factor f(g_ext) depends on
the field only, not on how the baryons are split, so a truncated superposition is the cluster-level law. d-TRUNC is
*worse* than the law by 0.05 dex because the inner baryons sit in a stronger field and are truncated harder. Applying
"counted once" per galaxy therefore explains nothing; it removes a little mass.

**d-FREE — the untruncated superposition.** Every member's halo is extended to the cluster aperture. For N_eff equal
members the sum is *exactly* the law with a0 -> N_eff a0 (KA3, sympy residual 0), so the whole reading collapses onto
one number: the N_eff it needs.

| footing | N_eff required (median, and per cluster) | radial spread max/min within a cluster | residual at DD1's L2 N_eff = 14.4 | residual at a Schechter N_eff (log M* 10.6, alpha -1.1) |
|---|---|---|---|---|
| canonical | **58** (A1795 42.8, A2029 58.3, A2142 42.1, A2319 61.8, A644 96.6, A85 62.3, ZW1215 52.3) | 2.00-3.64, median 2.59 | **+0.166** dex | **-0.233** dex (overshoots) |
| alt | **44** (33.8, 44.2, 32.2, 46.3, 76.2, 48.6, 40.0) | 1.98-3.78, median 2.84 | **+0.129** dex | **-0.273** dex |

- Even granted the double counting, **no single N_eff fits**: the required value runs by a factor 2.0-3.6 across the
  five radii of one cluster (A644: 41.6 at 0.1 R500, 151.3 at 0.3 R500, 42.5 at 0.7 R500). The boost has the wrong
  radial shape.
- At DD1's own L2 a0 for X-COP (14.4 x canonical, which is the same number read from the other end) the residual is
  still **+0.166 || +0.129 dex** — it does not close.
- At the N_eff a real cluster galaxy mass function gives (140-363 for log M* 10.6, alpha -1.1), it **overshoots** by
  0.23-0.27 dex. So the superposition brackets the answer from both sides with the truncation switched off, and
  collapses to N_eff = 1 — the cluster law, +0.51 || +0.48 dex — with it switched on.
- **K-D2 did not fire** (the pre-registered line was N_eff > 100; the median is 58 || 44). It is reported as not
  firing. The verdict comes from K-D1 and K-D3, and the radial-spread row above is an additional failure not
  pre-registered.

## Rows of the lane

| item | verdict | numbers |
|---|---|---|
| KA1 bare-law shortfall, 35 nodes | PASS | 0.46749895 / 0.43452306, to 1e-6 of DT2/CLS1 |
| KA2 F_src and M_law exact inverses; M_law/M_b = 1 + f(g_N) | PASS | sympy residual 0 |
| KA3 N equal members: sum M_law(M/N, R) = M_law(M, R; N a0) | PASS | sympy residual 0 |
| KA4 EFE truncation: M_law(m, sqrt(Gm/g)) - m = m f(g) | PASS | sympy residual 0 |
| KA5 point-mass dust: M_dust = mu^2 M_b R^2/6, ratio = (mu R)^2/6 sqrt(g_N/a0) | PASS | sympy residual 0 |
| KA6 DD1 X-COP from `dd1_table.csv`, 129 points | PASS | +0.466 / +0.434 |
| KA7 DD1 CLASH lensing, 84 points, 20 clusters | PASS | +0.527 / +0.498 |
| (a) K-A1 sign, K-A2 proof, K-A3 lensing | all fire | Q median 0.768, 5/5 below 1; CLASH +0.527 / +0.498 |
| (b) K-B1, K-B2, K-B3 | all fire | +3.58 dex; mu_fit 3.22/Mpc; CLS1 S2c |
| (c) K-C1, K-C2 | fire on both footings | f_b,req 0.602 / 0.557 > 0.156; R_gas 5.01 / 4.66 > 3 |
| (d) K-D1, K-D2, K-D3 | K-D1 and K-D3 fire, **K-D2 does not** | see above |
| MUTATE M1-M5, each run alone | **all five bite** | below |

## Mutation arm (each twin run alone against the main pass; all must move >= 0.10 dex)

| twin | change | effect on a graded number |
|---|---|---|
| M1 | drop the EFE truncation in (d) | d-TRUNC median **-0.170 dex** (0.507 -> 0.337): removing the truncation does buy mass, which is exactly the double counting K-D3 forbids |
| M2 | a0 -> 0 (Newtonian law) | baseline **+0.470 dex**; R_gas **+3.41**; f_b,req **+0.398**; N_eff -> no finite solution |
| M3 | mu_K = 2.97/Mpc (CLS1's window edge) instead of 198.25 | log10 R_b **-3.6489 dex** = 2 log10(2.97/198.25), exactly as pre-registered. mu_fit is invariant by construction (a check, not a target) |
| M4 | gas x 3 | R_gas **-3.138** |
| M5 | N_eff = 1 in (d-FREE) | N_eff required **-57.3** (58 -> 1); the superposition collapses onto the cluster law |

Footings were never pooled; every a0-carrying row is printed twice and the two differ (0.4675 against 0.4345 at the
top, and everywhere below).

## What this lane says, in one paragraph

Under form B the cluster's non-baryonic mass is not a state, not pressure, not missing gas and not the sum of its
members' halos. CLS1 closed the state. The dust term that AKS1's T5 flags as over-capturing by 3.6-8.4 in galaxies
over-captures by 1.7e4 in a cluster, because the factor carries R^2; the mu_K that would give the right amount is
3.2/Mpc, 61x below the CMB line and sitting inside the very window where CLS1 built no state. Non-hydrostatic support
runs backwards: the non-hydrostatic masses are 23 % below the hydrostatic ones, so it deepens the problem by 0.115 dex,
and the excess is anyway present in lensing. The gas would have to be under-counted 5x, which would give the cluster
60 % of its mass in baryons against a cosmic share of 15.6 %. And the per-galaxy "counted once" rule, applied with the
truncation the cluster's own field imposes, returns the cluster-level law to 0.005 dex — it is not an alternative to
the cluster law, it is the same calculation. With the truncation switched off it needs N_eff ~ 58 || 44 and still
misses the radial shape by a factor 2.0-3.6. The measured +0.47 || +0.42 dex is unexplained by every candidate this
lane was asked to grade.

## What was not settled

- No state is built here, and none is offered. CLS1 owns existence and has answered NO STATE.
- No member catalogue. No per-cluster galaxy mass function for these seven X-COP clusters was found on disk, so (d)'s
  N_eff is reported as the value it would need (plus a Schechter band, log M* 10.6 +/- 0.3, alpha -1.1 +/- 0.2, and
  the Cauchy-Schwarz bound N_eff <= N_members), not as a fit to measured members.
- The gas census itself is HY4-1's (GAS1). This lane reports only the size of the revision (c) needs.
- Hydrostatic masses, their EM_FORW errors and the gas and stellar profiles are taken as given, as in DT2, DT3, CLS1
  and XCV1. Inside 0.05 R500 nothing is graded; the fine grid for the integrals runs 0.05-0.90 R500.
- (b)'s response is computed at leading order in Psi/c^2; the exact relation x = exp(Delta Psi/c^2) - 1 >= Delta Psi/c^2
  makes the leading order a strict lower bound, so the over-capture numbers are floors, not ceilings.
- Moving, non-spherical or shell-crossed configurations are outside this lane, as in CLS1 and DT3.

## Files

`FROZEN_CRITERIA.md` (criteria 7630e48454, committed alone), `cls2.py` -> `cls2.json` / `cls2.out` (0.2 s, one
thread), and the five mutation passes `cls2_MUTATE_M{1..5}.json` / `.out`. Re-run with
`python3 -I cls2.py cls2.json` and `python3 -I cls2.py --mutate=M3` from this folder. Data are read only:
`real_research/data/xcop/`, `_external_data/hecs_omnibus_2026_11_10/table2.tsv`, and DD1's `dd1_table.csv`.
Nothing was downloaded.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.