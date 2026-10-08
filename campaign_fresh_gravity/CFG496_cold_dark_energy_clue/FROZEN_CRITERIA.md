# CFG496 FROZEN CRITERIA: a clue linking COLD ENERGY and DARK ENERGY? (hunt with anti-numerology controls)

Committed alone, before any script was written or any match computed.

## Terms (owner, 2026-10-08)
- **COLD ENERGY**: the framework's cold, clumping component (formerly "cold fluid"). Pressureless (w ~ 0). Cosmic amount
  R = Omega_c/Omega_b = 5.364 is an INPUT. Its mass is still required. No particle.
- **DARK ENERGY**: the vacuum component, rho_Lambda. The framework ties it to galaxies through a0 = kappa c sqrt(G rho_Lambda),
  kappa = 1/2 FITTED. Both footings (a0 = 9.3603e-11 and 1.1312e-10 m/s^2) are scored separately, never pooled.

Inputs: Planck 2018 (h 0.6736, Omega_b h^2 0.02237, Omega_c h^2 0.1200), so R = 5.364, f_b = 1/(1+R) = 0.1571,
Omega_m = 0.3147, Omega_Lambda = 1 - Omega_m (flat). Kernel: the record's nu_mono (FP1) for the law; its exponential closed
form nu = 1/(1 - exp(-sqrt y)) for the edge (they agree to 3e-9 at y = 0.03). Edge: s = ln(1 + 1/R), y_e = s^2,
r_edge = r_M/s, r_M = sqrt(G M_b/a0) (CFG423/461).

Already on record, NOT re-chased (read first): SCAN_cosmic_supply_coincidence_2026-10-07 (y_H = s, today-only),
the 32 pi lanes and CFG380, L258 (the Omega_Lambda-from-a0 rung is circular), CFG461 R0 (temperature = edge restatement),
CFG487 (SPARC/KiDS beyond-edge test: the edge FAILS KiDS by +60 chi^2), CFG488/490 (supply needs a label).

## Candidate list (declared now; all scored, none dropped)

| ID | class | statement tested |
|---|---|---|
| C01 | structural | inside r_edge the total-to-baryon mass equals the cosmic mix 1 + R |
| C02 | structural | the settled SIS temperature sigma^4 = G M_b a0/4 follows from the share inside the edge |
| C03 | structural | the total field at the edge, g_e/a0 = (1+R) ln^2(1+1/R) = 0.186, equals a simple dark-energy-set number |
| C04 | structural | edge density (local, and mean inside r_edge) is a fixed multiple of rho_Lambda across galaxies, groups, clusters |
| C05 | structural | edge dynamical time is a fixed multiple of the vacuum time 1/sqrt(G rho_Lambda) across masses |
| C06 | structural | r_edge is a fixed multiple of the Lambda zero-velocity radius (3 G M_tot/(Lambda c^2))^(1/3) across masses |
| C07 | structural | any mass-independent galaxy-level relation between edge quantities and rho_Lambda exists that is NOT set by a0 (Buckingham) |
| C08 | simulation | zero-knob PM: the largest fraction of a turnaround catchment that is settled, q_max = 0.302, equals Omega_m |
| C09 | simulation | zero-knob PM: the settled cold energy shows a regularity with a0 that is not put in by the code |
| C10 | epoch | the framework predicts WHY NOW (Omega_c ~ Omega_Lambda today), rather than taking it as input |
| C11 | epoch | today's cold-to-dark ratio rho_c/rho_Lambda = Omega_c/Omega_Lambda equals a simple framework number |
| C12 | epoch/amount | the amount R = 5.364 equals a simple dark-energy-set number |
| C13 | data (X-COP) | clusters reach the cosmic mix M_HSE/M_b = 1 + R at the same field y_mix = g_N,b/a0 as the galaxy edge y_e |
| C14 | data (SPARC) | the observed boost shows the edge feature at y_e (points with y < y_e fall below the law toward the cap 1 + R) |
| C15 | data (SPARC) | per-galaxy RAR residuals correlate with dark-energy-scaled quantities: log(R_last/r_edge), log(Sigma_eff/Sigma_M), Sigma_M = a0/(2 pi G) |

Not included (reason stated in advance): MeerKAT (on-disk product is a width-based a0, no per-radius curves except one disc);
satellites (no dependence on R); KiDS (edge already scored and FAILED in CFG487/413; not re-scored).

## Classification rules (frozen)

Labels: **BUILT-IN**, **CLUE**, **COINCIDENCE**, **NO MATCH**. Only CLUE counts as a clue.

1. **BUILT-IN**: the relation follows from the law plus the edge definition (or from how the inputs are defined). Test: a
   sympy identity that holds for SYMBOLIC R and kappa (C01, C02, C10), a Buckingham-Pi proof (C07), or code inspection
   showing the quantity is computed from a0 by the script itself (C09). A BUILT-IN relation is not a clue whatever its
   numerical quality.
2. **Scale-free test** (C04-C06): compute d ln(ratio)/d ln M_b over M_b = 1e7 ... 1e15 Msun. Scale-free requires
   |slope| <= 0.02. If not scale-free: NO MATCH (it is not a relation, only a mass-specific crossing; the crossing mass is
   reported).
3. **Number-family test** (C03, C08, C11, C12): family F1 = {p pi^a kappa^b Omega_Lambda^c Omega_m^d},
   p in {1, 2, 3, 4, 8, 1/2, 1/3, 1/4, 1/8, 2/3, 3/2, 3/4, 4/3}, a, b, c, d in {-1, 0, 1} (1,053 forms), used for C03, C08,
   C12. For C11 (made of Omega's) the family is F2 = {p pi^a kappa^b}, a, b in {-2..2} (325 forms). delta = min |ln(v/X)|.
   **Match** if delta <= 0.01. **Look-elsewhere p**: v' = v x 10^U(-1,1), 20,000 draws, seed 496; p = P(delta(v') <= delta(v)).
   Control passes if p < 0.01.
4. **Second check** (epoch or scale). For a family match: if the best form contains Omega_Lambda or Omega_m, re-evaluate both
   sides at z = 1 (Omega's evolve; R, f_b, y_e, g_e/a0 do not; rho_c/rho_Lambda scales as (1+z)^3); pass if still within
   3 delta_max = 3%. If the best form is a pure number (no Omega), no second epoch or scale exists: second check NOT AVAILABLE,
   which counts as a FAIL. C08's second check: the same rule at 512^3 (CFG439/460 q_max) within 10%.
5. **C13 (X-COP)**: per cluster, y_mix = G M_b(r)/(r^2 a0) at the radius where M_HSE/(1-b)/M_b first falls to 1 + R, searched
   on 0.05 R500 ... the outermost measured gas radius (no extrapolation; a cluster that never crosses is censored and counted).
   M_b = gas + stars (CFG432 convention). Cells: b = 0, 0.3 x both footings. Match: |median log10(y_mix/y_e)| <= 0.15 dex
   and within 2 sigma (cluster bootstrap) in all four cells. Look-elsewhere: p = P(|U| <= |Delta|), U uniform on a 3-dex prior
   for log y, i.e. p = 2|Delta|/3. Second check: no mass trend, |d log y_mix/d log M500| within 2 sigma of 0, in every cell.
6. **C14 (SPARC)**: Upsilon_disk 0.5, Upsilon_bul 0.7 (the record's 1.4 ratio), Q < 3, Inc >= 30 deg. Point residual
   r = log g_obs - log(nu_mono(y) g_N). Statistic Delta = mean r(y < y_e) - mean r(y_e <= y < 3 y_e), galaxy bootstrap.
   Edge prediction Delta_pred = mean over the same points of log((1+R)/nu(y)) for y < y_e (cap) minus 0. Match: |Delta| >= 3 sigma
   AND |Delta - Delta_pred| <= 2 sigma, both footings. Look-elsewhere: replace y_e by y_t = ln^2(1 + 1/R') for 200 R' log-uniform
   in [1.5, 20]; p = fraction of thresholds that also match. Second check: C13 (cluster scale) must also match.
7. **C15 (SPARC correlations)**: Spearman rho of per-galaxy mean residual vs each of the two quantities; look-elsewhere p
   from 2,000 shuffles on max|rho| over both (seed 496). Before computing: R enters log(R_last/r_edge) only as the constant
   log s and does not enter Sigma_M at all, so these correlations are INVARIANT under any change of R. Rule: an R-invariant
   statistic cannot link the amount of cold energy to dark energy; if p < 0.01 it is reported as a LAW RESIDUAL and labelled
   BUILT-IN (not R-specific); otherwise NO MATCH.
8. **CLUE** = not BUILT-IN AND match AND look-elsewhere p < 0.01 AND second check passes. A match failing the control or
   the second check is **COINCIDENCE**. No match at all is **NO MATCH**.
9. Any classification issued here is provisional on the record's kernel, data and footings; a CLUE would be a lead, not a
   derivation, and kappa stays FITTED.

## MUTATE (frozen): scrambled cosmology

`CFG496_MUTATE=1`: 200 draws (seed 4960) of R' uniform in [3, 8], with Omega_b fixed, Omega_c' = R' Omega_b,
Omega_m' = Omega_b + Omega_c', Omega_Lambda' = 1 - Omega_m'; a0 unchanged (it is set by rho_Lambda and kappa; the footing a0
values are held, as the record measures them on SPARC). Every R-dependent candidate (C01-C03, C08 via the share scaling q ->
q R'/R, C11-C14) is re-scored with the same rules; R-invariant ones (C04-C07, C09, C10, C15) keep their labels. Reported: the
mean number of CLUE labels per draw and the fraction of draws with >= 1 CLUE (the hunt's false-positive rate), and, for C13/C14,
the fraction of draws that match (specificity of the real R).

Expected (stated in advance): most candidates BUILT-IN or COINCIDENCE/NO MATCH; the framework does not predict "why now".

## Controls
- K1 sympy: C01/C02/C10 identities hold for symbolic R, kappa; a deliberately wrong identity (1 + R replaced by R) fails.
- K2 family test can fire: a planted value v = 3 pi kappa Omega_m (exact) gives delta = 0 and p < 0.01.
- K3 X-COP loader reproduces CFG432's C2 data identity (all profiles positive/finite on 0.1-1 R500).
- K4 SPARC: nu_mono residual median within 0.1 dex of 0 on both footings (sanity).
Exit code 0 when K1-K4 pass; MUTATE run exits 0 when it completes (it is a rate measurement, not a pass/fail).

kappa = 1/2 is FITTED. No dark-matter particle; the cold energy's mass is still required. Never "theory closed".
