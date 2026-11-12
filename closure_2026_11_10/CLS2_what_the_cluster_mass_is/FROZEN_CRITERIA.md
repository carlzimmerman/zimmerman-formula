# CLS2 FROZEN CRITERIA: what IS the cluster's non-baryonic mass under form B? (2026-11-11)

Committed alone, before any script or any number of this lane. TEST lane, quarantined: adopts nothing, relabels nothing
(RB1's, XCV1's, CLS1's, DD1's and AKS1's labels stand), registers nothing. Footings never pooled. Cold dark energy is a
gravitating field component, never a particle. kappa = 1/2 FITTED; not theory closed.

## 0. The situation this lane inherits (quoted, not re-graded)

- **CLS1** (`closure_2026_11_10/CLS1_cluster_state_in_action/`): under form B's action (A), **no static clock state exists
  in any of the seven X-COP clusters at form B's own mu_K**. At mu_K = 198.25/Mpc the required potential span beats the
  allowed enthalpy span by **396 to 2,192**; at the CMB-lensing line mu_J = 2.512e4/Mpc by 6.3e6 to 3.5e7. Over all mu_K
  the necessary conditions leave one window common to all seven, **2.97-4.43/Mpc**, and inside it a dense scan builds
  **0 of 7** states (best miss 2.6 half-widths). S2a: the clock's stress is a perfect fluid (sympy, residual 0) - one
  velocity per point, isotropic p = n x / 2, zero momentum density - so there is no collisionless or velocity-dispersion
  pressure in (A). S2b: a stationary tilted clock that is regular at the centre carries zero radial khronon current.
- **DD1** (`fable52_push/DD1_deduce_from_data/`): the statistic X = g_obs/g_bar - 1 = M_nonbaryonic/M_baryons, scored as
  Y = log10(1 + X). **X-COP sits +0.57 / +0.48 / +0.50 dex and CLASH +0.55 / +0.55 / +0.55 dex ABOVE the law (L0), at
  15-24 standard errors. Groups sit at +0.16 / +0.17 / +0.16.** DD1's L2 (the law's curve with a0 per class) puts X-COP
  at a0 = **14.4 (13.3-17.5) x canonical** and CLASH at 20.4 (18.9-21.8).
- **XCV1** (`closure_2026_11_10/XCV1_xcop_nonhydrostatic_mass/`): frozen label NO VERDICT (KA-3 failed); under the post
  hoc A1, AT THE CEILING, median f_ret 1.369 [0.735, 2.619]. Its hydrostatic-bias row is Q = M_caus/M_FORW = **0.768
  [0.521, 0.819] at the same radius** - the non-hydrostatic (caustic) masses are BELOW the hydrostatic ones.
- **AKS1 Part T** (`toe_2026_11_10/AKS1_acceleration_keyed_sink/`, T5(o)): the static dust of (A) at the CMB mu_K gives
  **3.6 to 8.4 times the law's halo at SPARC radii**, scaling as mu_K^2, so **x 1.61e4 at mu_J**. Branch rule: D-V(o)
  closes on over-capture (line >= 2).

**The question.** CLS1 proves the cluster's non-baryonic mass is not a static-clock state. DD1 measures it at +0.5 dex
above the law with 15-24 se. So something in the cluster carries ~3 times the mass the law gives it. What is it?

## 1. Data (frozen, read-only)

- X-COP, the same seven clusters and the same loader as DT2 / DT3 / CLS1:
  `real_research/data/xcop/<NAME>/<NAME>_{hydro_mass,fgas_profile,mstar}.fits`, read through
  `research_closure_2026_11_10/DT2_response_audit/cluster/check_shape.py` (G, A0, NAMES, RHO_BG, `load()`).
  Nothing is downloaded, nothing is written to `real_research/`.
- Graded nodes: **x = 0.1, 0.2, 0.3, 0.5, 0.7 R500** (DT2's frozen five). At each node: r (kpc), M_FORW and EM_FORW
  (hydrostatic mass and its statistical error), M_b = M_gas + M_star from the real gas and stellar profiles by log-log
  interpolation (DT2's `interp`), which requires the node to lie inside both profiles.
- Integrals for (b) and (d) use a **fine grid of 60 nodes, log-spaced, from 0.05 to 0.90 R500**, the same interpolations.
- HeCS-omnibus table 2 (`_external_data/hecs_omnibus_2026_11_10/table2.tsv`) for the non-hydrostatic row of (a), read
  exactly as XCV1/CLS1 do it.
- DD1's frozen table `fable52_push/DD1_deduce_from_data/dd1_table.csv` for the known-answer cross-check (KA6) and for
  the CLASH lensing row of (a). Read-only.
- Footings: **canonical a0 = 9.360324825027975e-11 m/s^2**, **alt a0 = 1.1312035414413022e-10 m/s^2**. Never pooled;
  a per-footing number is printed for every graded quantity.

## 2. Statistic (frozen)

The law is the action-exact spherical pair

    M_law(M_b, r, a0) = ( M_b + sqrt(M_b^2 + 4 M_b a0 r^2 / G) ) / 2          (dynamical mass from baryons)
    F_src(M,   r, a0) = M^2 / ( M + a0 r^2 / G )                              (baryons from dynamical mass)

which are exact inverses (KA2), and which reproduce `law(g_N)` because g_bar = g_obs^2/(g_obs + a0).

**Residual of a candidate, in dex, at a node:**

    res(r) = log10( M_FORW(r) / M_cand(r) )

Positive = the candidate still falls SHORT of the measured mass; negative = it overshoots. For the bare law this is
exactly DD1's Y-offset, since Y = log10(1 + X) = log10(M/M_b) and Y_obs - Y_law = log10(M_obs/M_law) (KA6).

Per cluster: the **mean over the five graded nodes** (CLS1's KA1 convention). Per class: the **median over the seven
clusters**, with the mean and the full range reported.

Errors: EM_FORW is propagated to dex as EM_FORW/(M_FORW ln 10) at each node; the cluster mean carries the node errors
added in quadrature over the five nodes, divided by 5 (statistical only - the X-COP systematic envelope is DT3's and
XCV1's business, not re-graded here).

## 3. The four candidates (definitions frozen here, before any run)

### (a) Non-hydrostatic support

The measured M_FORW assumes hydrostatic equilibrium. If the gas carries non-thermal pressure (turbulence, bulk
motions, cosmic rays, magnetic fields), M_FORW over-estimates the true mass and the "+0.5 dex" is an artifact.

Three rows, all frozen:
- **a1 SIGN**: Q = M_caus/M_FORW at each cluster's HeCS R200, recomputed from the HeCS table on disk. (a) helps only if
  Q > 1. If Q < 1 the non-hydrostatic mass is *below* the hydrostatic mass and (a) moves the residual the WRONG WAY, by
  log10(1/Q).
- **a2 PROOF (quoted, CLS1 S2a)**: within action (A) the clock's stress is a perfect fluid, so the cold component cannot
  supply velocity-dispersion or collisionless pressure at all. (a) is not merely unsupported by the data; it is
  unavailable to form B.
- **a3 LENSING**: the CLASH residual recomputed from DD1's table (20 clusters, 84 points). CLASH masses are lensing
  masses; they make no hydrostatic assumption. If the CLASH residual is >= 0.3 dex the excess is not an HSE artifact.

### (b) The cluster's mass is the dust term pooled in the well

AKS1 T5(o): in a static region n_d = dF/dh (c_0 - Phi) is one function of the well depth, so the dust pools where the
well is deep. AKS1 quotes the over-capture at the CMB mu_K as 3.6-8.4 x the law's halo at SPARC radii, x 1.61e4 at
mu_J. This lane computes what the same term does **in a cluster**, with the real profiles.

Definition. Tolman balance gives ln(1 + x(r)) = (Psi(r) - Psi(R_out))/c^2 with the dust vanishing at the outer boundary;
x = ALPHA n / mu_K^2 with ALPHA = 4 pi G / c^2; the active density is m = n(1 + 2x) >= n. So the leading-order pooled
dust mass is the **linear response**

    M_dust(<R)  =  (mu_K^2 / G) * integral_0^R  ( Psi(r) - Psi(R_out) ) r^2 dr                       (mu_K in 1/kpc)

with Psi the potential depth generated by the mass that is actually there. **Psi from the OBSERVED profile alone gives a
strict LOWER BOUND**, because the dust's own gravity only deepens the well. The self-consistent value is reached by
iteration; if the iteration does not converge, that is reported as the result (no static pooling exists at that mu_K).

Rows:
- **b1 OVER-CAPTURE**: R_b = M_dust(mu_K = 198.25/Mpc) / M_nonbaryonic,obs, where M_nonbaryonic,obs = M_FORW - M_b.
  Reported per cluster per node, and at mu_J = 2.512e4/Mpc.
- **b2 FIT mu_K**: mu_fit = 198.25 * sqrt( M_nb,obs / M_dust(198.25) ) per Mpc - the mu_K that would pool exactly the
  observed non-baryonic mass. Compared with the CMB line 198.25/Mpc, the lensing line 2.512e4/Mpc, and CLS1's cluster
  window 2.97-4.43/Mpc.
- **b3 SCALING (sympy)**: for a point mass, M_dust/M_ph = (mu_K R)^2/2 * sqrt(g_N/a0) with M_ph the law's phantom and
  g_N = G M_b/R^2. The factor therefore grows as R^2 at fixed mu_K. This is the row that says whether "+0.5 dex is
  exactly that factor": AKS1's 3.6-8.4 is measured at SPARC radii (R ~ 10 kpc); a cluster is graded at R ~ 600-1400 kpc.
- **b4 PROOF (quoted, CLS1 S2c)**: no static state exists at mu_K >= 198.25/Mpc (396 to 2,192), so there is no static
  dust profile in a cluster to pool. Whatever (b) computes is a response, not a state.

### (c) The cluster's gas is under-counted (the HY4-1 census issue)

If the true baryons were M_b' > M_b, the law would predict more mass. The baryons the law needs to reproduce M_FORW are
exactly the inverse image

    M_b,req(r) = F_src( M_FORW(r), r, a0 ),        R_gas = M_b,req / M_b

Rows:
- **c1 BUDGET**: f_b,req = M_b,req / M_FORW against the cosmic share **Omega_b/Omega_m = 0.156** (XCV1's number: at the
  edge f_ret <= 1 is the same statement as f_b <= 1/(1 + R) = 0.156). If f_b,req > 0.156 the cluster would hold more
  baryons than the universe has to give, which is not a census error but new physics.
- **c2 FACTOR**: R_gas per cluster per node. The X-COP gas masses come from X-ray surface-brightness deprojection with
  a few per cent statistical error; the size of the required revision is the number this lane reports, and the census
  grade itself is HY4-1's (GAS1), which is running it bin by bin. This lane does not grade the census.

### (d) The cluster is a superposition of galaxy halos, one per member

The "counted once" rule applied per galaxy rather than per cluster: each member carries the law's share, and the
cluster's non-baryonic mass is the sum of the members' shares.

Two readings, both frozen, because the two disagree and the disagreement is the result:

- **d-TRUNC (the EFE reading, no free parameters).** A member of mass m sitting in the cluster's field g_ext has its
  halo truncated where its internal field falls to the external field, r_t = sqrt(G m / g_ext). Its phantom mass is then
  M_law(m, r_t) - m = m f(g_ext) with **f(g) = ( sqrt(1 + 4 a0/g) - 1 ) / 2** (KA4). With the real profiles,

      M_dTRUNC(R) = M_b(R) + integral_0^R  f( g_N(r) ) dM_b(r),      g_N(r) = G M_b(<r) / r^2

  and the variant **d-TRUNC-s** in which only the *stars* sit in members and the gas keeps the cluster-level share:
  `M_b(R) + integral f(g_N(r)) dM_star(r) - M_star(R) f(g_N(R)) + M_gas(R) f(g_N(R))`, i.e. the gas gets 1 + f(g_N(R))
  and the stars get 1 + f(g_N(r)) shell by shell.
  Note the identity that makes this reading decisive: at fixed external field the phantom ratio f(g_ext) depends on the
  field only, not on how the baryons are split. So a truncated superposition returns the cluster-level law.

- **d-FREE (the untruncated superposition; the boost reading).** Every member's halo is extended to the cluster
  aperture. For N_eff equal members the sum is **exactly the law with a0 replaced by N_eff a0** (KA3):

      sum_i M_law(m_i, R)  =  M_law( M_star(R), R ; a0 -> N_eff a0 )

  so (d-FREE) is nothing but an a0 boost of N_eff on the member (stellar) mass, and the number to report is
  **N_eff,req**: the N_eff that makes M_law(M_star, R; N_eff a0) + [the gas's share] equal M_FORW(R), per cluster per
  node. The gas's share is taken at cluster level (1 + f(g_N(R))) in the graded row; the variants with the gas bare and
  with the gas also fragmented are reported. N_eff,req is to be compared with (i) DD1's L2 a0 for X-COP, 14.4
  (13.3-17.5) - which is the same number read from the other end - (ii) the effective member count of a cluster galaxy
  mass function, and (iii) the truncation, which forces N_eff -> 1.

## 4. Kills (pre-registered; a kill fires or it does not, on the printed number)

| id | candidate | kill fires if |
|---|---|---|
| K-A1 | (a) | median Q = M_caus/M_FORW < 1 (wrong sign). Non-hydrostatic support then REMOVES mass. |
| K-A2 | (a) | CLS1 S2a stands: perfect fluid, no dispersion pressure. (Quoted proof; fires independent of data.) |
| K-A3 | (a) | the CLASH lensing residual >= 0.3 dex on both footings. |
| K-B1 | (b) | median log10 R_b > +0.30 dex at mu_K = 198.25/Mpc (over-capture by more than a factor 2). |
| K-B2 | (b) | mu_fit < 198.25/Mpc, or mu_fit outside CLS1's 2.97-4.43/Mpc window. |
| K-B3 | (b) | CLS1 S2c stands: no static state at mu_K >= 198.25 (396 to 2,192). (Quoted proof.) |
| K-C1 | (c) | f_b,req > 0.156 on all seven clusters, both footings. |
| K-C2 | (c) | median R_gas > 3 (a factor-3 error in an X-ray gas mass). |
| K-D1 | (d) | median res(d-TRUNC) >= median res(law) - 0.10 dex, i.e. the per-galaxy rule reproduces the cluster law and explains nothing. |
| K-D2 | (d) | N_eff,req > 100 on all seven, or the truncation bound N_eff <= 1 is what the theory gives. |
| K-D3 | (d) | the action-exact spherical law depends on enclosed baryons only (KA2/KA3): splitting the baryons into members is not a degree of freedom of the theory. |

## 5. Labels (per footing)

Per candidate:
- **SUPPLIES THE MASS** - |median residual| <= 0.10 dex and no kill fires.
- **PARTIAL** - 0.10 < |median residual| <= 0.30 dex, or the right sign but >= 0.10 dex on >= 5 of 7 clusters.
- **FAILS** - |median residual| > 0.30 dex, or a numeric kill fires.
- **KILLED BY PROOF** - a quoted proof (K-A2, K-B3, K-D3) excludes it regardless of the number.

Lane label, per footing:
- if at least one candidate is SUPPLIES THE MASS: **<that candidate> SUPPLIES THE MASS**.
- if the best is PARTIAL: **BEST IS <candidate>, RESIDUAL <x> dex**.
- if every candidate is FAILS or KILLED BY PROOF: **NO CANDIDATE / NO CANDIDATE**, with the best candidate and its
  residual dex named in the result.

## 6. Known answers (all must pass)

| id | check | expected |
|---|---|---|
| KA1 | bare-law residual, mean over the 35 graded nodes | 0.46749899 / 0.43452310 dex to 1e-6 (DT2/CLS1 KA1) |
| KA2 | F_src and M_law are exact inverses; M_law(M_b,r)/M_b = 1 + f(g_N) with g_N = G M_b/r^2 | sympy residual 0; floating point < 1e-12 relative |
| KA3 | N equal members: sum_i M_law(M/N, R) = M_law(M, R; a0 -> N a0) | sympy residual 0 |
| KA4 | EFE truncation: M_law(m, sqrt(G m/g_ext)) - m = m f(g_ext) | sympy residual 0 |
| KA5 | point-mass linear dust response: M_dust/M_ph = (mu R)^2/2 * sqrt(g_N/a0) | sympy residual 0 |
| KA6 | DD1's per-cluster X-COP Y-offset recomputed from `dd1_table.csv`, canonical | 0.42-0.55 dex per cluster, mean ~0.467 |
| KA7 | CLASH lensing residual from `dd1_table.csv` (84 points, 20 clusters) | >= 0.3 dex on both footings (DD1 quotes +0.55) |

## 7. Mutation arm (every twin must bite)

Each twin must move at least one graded number by >= 0.10 dex or flip a verdict; a twin that does not bite is reported
as a failure of this lane's design, not as a result.

| twin | change | what it must move |
|---|---|---|
| M1 | (d-TRUNC) no EFE truncation: f(g_N(r)) -> f(g_N(R)) everywhere | d-TRUNC collapses onto the cluster law exactly |
| M2 | a0 -> 0 (Newtonian law) in the baseline | the law residual becomes log10(M_FORW/M_b) |
| M3 | (b) at mu_K = 2.97/Mpc (CLS1's window edge) instead of 198.25 | R_b x (2.97/198.25)^2 = 2.25e-4 |
| M4 | (c) gas x 3 | R_gas falls by ~3 |
| M5 | (d-FREE) N_eff = 1 | d-FREE collapses onto the cluster law |
| M6 | pool the footings (forbidden) | must NOT be done; the check is that canonical != alt on every a0-carrying row |

## 8. Hand expectation (before the script; check, do not trust)

- (a): Q ~ 0.77, wrong sign. CLASH lensing ~ +0.4 dex. (a) FAILS / KILLED BY PROOF.
- (b): my point-mass estimate gives M_dust/M_ph ~ (mu R)^2/2 sqrt(g_N/a0) ~ 2.4e3 at R = 1 Mpc, mu = 198.25/Mpc,
  g_N/a0 ~ 0.015 - three orders of magnitude ABOVE the ~2.9 needed. mu_fit ~ 7/Mpc: 28x below the CMB line, above
  CLS1's window. (b) FAILS / KILLED BY PROOF.
- (c): needing ~2.9x more dynamical mass at M_law/M_b ~ 6 means M_b,req ~ 5-8 x M_b, so f_b,req ~ 0.2-0.3 > 0.156.
  (c) FAILS on the budget.
- (d): d-TRUNC returns the cluster law (residual ~ +0.47, unchanged). d-FREE needs N_eff,req of order DD1's L2 value,
  10-20 - but the truncation forces N_eff -> 1, and the spherical law has no room for a member split at all. (d) FAILS.
- Expected lane label: **NO CANDIDATE / NO CANDIDATE**, best candidate (d-FREE) with a residual that is real but bought
  by double-counting, ~0.0 dex if N_eff is tuned and ~+0.47 dex if the truncation the cluster's own field imposes is
  honoured.

## 9. What this lane does not settle

- It does not build any state. Everything here is a bookkeeping identity plus a residual; CLS1 owns the existence
  question and it has answered it (NO STATE).
- It does not grade the gas census. That is HY4-1 (GAS1).
- It does not use member catalogues. No per-cluster galaxy mass function for these seven X-COP clusters was found on
  disk; (d-FREE) is therefore reported as the N_eff it would need, with the Cauchy-Schwarz bound N_eff <= N_members
  stated, and not as a fit to a measured mass function.
- Hydrostatic masses, their EM_FORW errors, and the gas and stellar profiles are taken as given, as in DT2, DT3, CLS1
  and XCV1.
- Moving, non-spherical or shell-crossed configurations are outside this lane, as in CLS1 and DT3.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
