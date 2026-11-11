# FRZ1 FROZEN CRITERIA: the forest row with form B's redistribution computed at the forest's own redshifts

Committed alone, before any FRZ1 script exists and before any FRZ1 number is computed. TEST lane, quarantined. Relabels
nothing, registers nothing. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), graded separately, never pooled.
Cold dark energy is a gravitating field component; no particle is added anywhere. A HOLDS outcome is not a pass for the
theory and is reported as needing an independent re-grade; nothing here says the data favour the framework.

## 0. The question, and what was seen before this freeze

HLF1 (`closure_2026_11_10/HLF1_own_halo_list_forest/`, criteria 123947b9dc, A1 657e245086, result 7d34a142f4) computed the
forest row of form B with the record's gate and found it NO VERDICT / NO VERDICT: reading H (CO1's z = 0 R_cold held at
every z) gives Delta chi^2 160.74 / 1025.57 (FAIL), reading F (the record's fade, zero above z = 1) gives 0 (PASS). The
missing number is the redistribution at z 2.2 to 4.4. This lane computes it.

Seen before this freeze: everything in HLF1 (its criteria, amendment, RESULT, every output, including readings H and F,
the per-z split of reading H, the own-list reading 99.88 / 852.69 and R_cold(k) at z = 0 to k = 10, which falls from 1.090
at k 5 to 0.987 at k 10 on canonical and from 1.159 to 1.060 on alt); CO1's criteria, result and `co1_hm.py`; CFG556's
library (lines 1 to 215); PD1's median shares per redshift (canonical 59.486 / 58.572 / 55.716 and alt 59.503 / 58.588 /
55.731 at z 0 / 0.3 / 1.0; PD1 has no table above z 1). No R_cold at any z > 0 has been computed by anyone.

## 1. The layout at redshift z (comoving Mpc/h, Msun/h; every z-dependence below is identity at z = 0)

The machinery is CO1's `co1_hm.py` layout (its galaxy rule, cluster rule and comparison layout Rb, unchanged in form) on
CFG556's halo model, with these ingredients evaluated at z:

| ingredient | at z | source | status |
|---|---|---|---|
| linear spectrum | P_lin(k, z) = P_lin(k, 0) D(z)^2, D the linear growth of flat LCDM at CFG556's cosmology (h 0.6736, Om 0.3138), normalised D(0) = 1 | standard growth integral | form B's linear content is the cold reference (rule 3); computed |
| sigma(M, z) | sigma(M, 0) D(z) | same | computed |
| mass function | Tinker 2008 with its z-scaling at Delta 200m: A(z) = 0.186 (1+z)^-0.14, a(z) = 1.47 (1+z)^-0.06, b(z) = 2.57 (1+z)^-alpha, alpha = 10^-[0.75 / ln(200/75)]^1.2, c = 1.19 | Tinker et al. 2008 eqs 5 to 8 (from memory: PROVISIONAL); calibrated to z 2.5, extrapolated to 4.4 | inherited |
| bias | Tinker 2010 at nu = 1.686 / sigma(M, z) (its z-universal form) | Tinker et al. 2010 | inherited |
| concentration | c(M, z) = 10.14 (M / 2e12)^-0.081 (1 + z)^-1.01 | Duffy et al. 2008, full sample, Delta 200m (from memory: PROVISIONAL); calibrated to z 2 | inherited |
| r200m | 200 times the mean matter density at z: in comoving units the z = 0 formula | definition | — |
| r200c, M200c | mean enclosed density 200 rho_crit(z), i.e. 200 / Om(z) times the comoving mean | definition | — |
| turnaround | Delta_ta(z) = 5.55 + (11.81 - 5.55) Omega_L(z) / Omega_L(0) (mean-density units): CFG556's PM value 11.81 at z = 0, the matter-era spherical-collapse value (3 pi / 4)^2 = 5.55 when Lambda is negligible | form choice (an interpolation), named | bracketed |
| the law's scale | a0 constant in physical units (the framework: a0 does not track z in form B's rules, CO1 section 3 "a0 is constant"). In comoving units this is a0 / (1 + z)^2 in every a0 term (r_M, the phantom) | rule 4 | — |
| v_vir | sqrt(G M200c / R200c,phys) = sqrt((1 + z) G M200c / R200c,comoving) | definition | — |
| v_stiff, core prefactor 1/2, W(v) with 15 km/s | constant in z | PD1 A1 / CO1 | form choices, as at z = 0 |
| PD1's share X | PD1's z = 1.0 median (55.716 / 55.731) for every z >= 1 (the latest table PD1 has) | PD1 | bracketed (z 0 value) |
| baryon fraction FB, baryon shapes (Moster 2013 stars at z = 0, beta-model gas, core 0.1 R200c) | as at z = 0 | CFG556 | inherited |

**What "rule 5 applies" means for a halo at z 3 (graded reading, L):** each halo at z carries the charge rule 5 assigns to
its present state at z: below v_stiff the cold dust of its Lagrangian turnaround sphere at z laid out as the law's phantom
around its condensed baryons; above v_stiff the share inside R200c with the core rule. The fold that makes a standing clock
takes 0.06 to 0.15 Gyr (COL1), short against the age at z 3 (about 2 Gyr), so the layout is taken as instantaneous.
**Alternative reading (V, reported, never graded):** a halo still assembling has only the charge inside its virial radius
laid out (CO1's "galaxy rule in the virial scope" at z).

## 2. The computation

For each footing and each DESI DR1 P1D redshift bin z_i (2.2, 2.4, ..., 4.4): R_cold(k, z_i) = R_tot / R_bar at z_i on CO1's k
grid (1e-3 to 10 h/Mpc). The forest gate is HLF1 Part B's, unchanged: the record's `ss1_cosmo.forest_eval` executed
read-only with its reference replaced by form B's own CLASS spectrum (F1A B2 cold fit) and background; the model amplitude
ratio on the pipeline's (KG, ZG) grid is sqrt(R_cold(k / h_B, z_i)) in the ZG column that `forest_eval` uses for bin z_i
(its nearest node), flat at its end values outside CO1's k grid. DESI DR1 P1D, 755 points, md5 33d7fc21bfd3d745ed71a0bbe80ca433,
gate **Delta chi^2 <= 4**. Per-bin Delta chi^2 (own covariance block) reported.

## 3. Labels (per footing)

- **FOREST ROW HOLDS:** Delta chi^2 <= 4 in reading L. **FOREST ROW FAILS:** > 4. **NO VERDICT:** a known answer fails or a
  mutation arm does not bite.
- **Brackets** (reported beside the label): c(M, z) x 0.7 and x 1.3; c without its z-scaling; Tinker 2008 without its
  z-scaling; Press-Schechter mass function with the Mo-White bias; Delta_ta 5.55 and 11.81; X at its z = 0 value; minimum halo
  mass 1e10 Msun/h (halos below it keep the reference layout); R = 1 above 10 h/Mpc; reading V. **Rule:** if any bracket
  lands on the other side of the gate from reading L, the label is written with the qualifier "FRAGILE" and the crossing
  brackets named; the label itself does not change.
- **Lane label:** the pair of footing labels; in one word HOLDS (both hold), FAILS (both fail), SPLIT (one each), NO VERDICT
  (either is NO VERDICT).

## 4. Known answers (any failure stops grading: NO VERDICT)

- **KA1:** at z = 0 the z-code reproduces CO1's stored primary R_cold (`co1_hm.json`) on both footings to 1e-10 relative.
- **KA2:** R = 1 gives Delta chi^2 = 0 exactly (and the DESI md5 matches).
- **KA3:** CO1's z = 0 R_cold held at every bin reproduces HLF1's reading H, 160.74 / 1025.57, to 0.01.
- **KA4:** D(z) from my growth integral against CLASS's sigma8(z) / sigma8(0) at CFG556's cosmology (massless neutrinos) at
  z 2.2, 3.0, 4.4: within 0.5 %.
- **KA5:** every layout at z conserves M_ta inside r_ta to 1e-9 and is non-decreasing (CO1's KA3 at z = 3).

## 5. MUTATE (separate `_MUTATE` outputs; each must bite)

- **MZ1:** the 3 keV thermal-relic cutoff (HLF1's MB1) on form B's own spectrum: Delta chi^2 > 4.
- **MZ2 (the z-layout responds to the scope):** at z = 3 the cluster rule in the Lagrangian scope, R_tot over the primary
  R_bar at k = 1, must exceed the primary R_cold by at least 0.10 (CO1 A1's restated M4, at z = 3), canonical.
- **MZ3 (a0 enters at z):** a0 left in comoving units unscaled (no (1 + z)^-2) must change R_cold at k = 3, z = 3 by at least
  0.005, canonical.

## 6. Hand estimates (before any number)

At z 3 the nonlinear mass is near 1e10 to 1e11 Msun/h and haloes above the v_stiff boundary (about 1e12 at z 3, since
v_vir grows as (1+z)^1/2 at fixed mass) are rare. The law's comoving scale r_M is (1 + z) times larger relative to the halo
than at z = 0, so the phantom spreads the cold dark energy wider: I expect R_cold(k, z 3) - 1 of order -0.03 to +0.03 at
k 1 to 5 h/Mpc, sign uncertain, smaller in magnitude than CO1's z = 0 values. The 1D ratio then moves by 0.5 to 2 % and
Delta chi^2 is of order 10 to 300: expected label FOREST ROW FAILS on alt and probably on canonical, with brackets
possibly crossing (FRAGILE). I have no better than even confidence in the sign.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
