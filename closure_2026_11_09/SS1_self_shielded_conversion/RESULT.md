# SS1 RESULT: FAIL / FAIL (criteria b5adc7a90b, amendment A1 9aeeb48503)

This file covers variant A, the round-3 construction. Variants B-G (AMENDMENT_A2 / A3) are graded in RESULT_B_G.md, variant H (AMENDMENT_A4) in RESULT_H.md and variant I (AMENDMENT_A5) in RESULT_I.md: every one is FAIL / FAIL.

Self-shielded late conversion, graded under ONE gate rule (self-consistent radial peeling of the component's own column).
TEST lane, quarantined (owner decision `../OWNER_DECISION_2026-11-09_SS1_LAUNCH.md`). Adopts nothing; no particle adopted (the
component is the record's test object). kappa = 1/2 FITTED; not theory closed. Footings canonical (a0 9.3603e-11) and alt
(1.1312e-10), graded separately, never pooled.

**Label (frozen rule): FAIL on canonical, FAIL on alt. First failing gate: 2, groups.** Gates 3 (X-COP), 6 (BAO with a bare
Lambda) and 9 (Bullet) also fail on both footings. Gate 7(b) (CMB lensing) is NO VERDICT: its ratio method failed the frozen
validation against CLASS (KA4b). Gates 1 (KiDS), 5 (SPARC), 8 (forest + growth) and 10 (Cassini) pass on the primary halos.

## The construction as graded (frozen once)

- Before z_dec = 0.55: cold dust, omega_chi = R omega_b, with R = 5.4092 (QX15 main theta; F1A R_B2 5.4096 / 5.4123).
- After z_dec: bare rate Gamma0 0.820 / Gyr and time budget tau 4.49, frozen as given. Gamma0 times the footing lookback to
  z 0.55 is 4.60, reported beside it.
- P_esc = 1/(1 + x^2), with x = Sigma / Sigma_gate, Sigma_gate = 0.042 g/cm^2 = 2.01e8 Msun/kpc^2, and
  Sigma(r) = sqrt((R500^2 - r^2) rhobar_chi(<0.25 R500) rho_chi(r)).
- **One rule for every system:** each of 300 shells drains at Gamma0 P_esc(x(r, tau)). The column is recomputed from the
  current densities at every RK4 step.
- **Members** (the Coma UDGs) add the host's draining column at their radius to their own.
- **Pre-conversion halos (primary):** the KD1 P3 capture amount, f_cap R M_b with f_cap 0.76. Each halo is a singular
  isothermal sphere truncated at R200, where the mean density is 200 rho_crit(z_dec). No LCDM fitting formula is used.
- **Brackets, disclosed, never graded:** B1 NFW with the Duffy et al. 2008 c-M relation; B2 Moster, Naab & White 2013
  abundance matching for the galaxy-scale systems.
- **Cosmic mean:** Press-Schechter collapsed fraction at z_dec on the footing's CLASS linear power (Sheth-Tormen as a
  bracket), 40 mass nodes, each a primary halo that peels. The converted energy goes into dark radiation.

## Gate table, primary halos (canonical / alt)

| gate | canonical | alt | line |
|---|---|---|---|
| 1 KiDS, 59 points | **PASS** max \|shift\| 0.020, 0 over | **PASS** 0.020 | every point \|shift\| <= 0.05 |
| 2 groups (Lovisari 20) | **FAIL** 0/20 (f* 0), 8/20 (f* 1); median residual +0.24 / +0.04 | **FAIL** 2/20, 9/20; +0.20 / +0.01 | >= 16/20 at both f* |
| 3 X-COP, amount + per-bin shape | **FAIL** mean -0.108, rms 0.198; bins -0.27, -0.07, +0.04 | **FAIL** -0.129, 0.206; -0.29, -0.09, +0.01 | \|mean\| <= 0.05, rms <= 0.10, each bin within 0.10 |
| 4 Coma UDGs (reported, UA1) | +1.211 (+4.62 sigma_U); +1.107 without the host term | +1.174 (+4.48); +1.066 | (2 sigma_U, not graded) |
| 5 SPARC + F2 allowance | **PASS** rms 0.0593 (line 0.0660), mean +0.001; tail 0.0455 (0.0475); retained inside the last point 0.027 M_b (allowance 0.326) | **PASS** 0.0580 (0.0658); tail 0.0392 (0.0426); 0.027 (0.194) | as frozen |
| 6 BAO + SN, bare Lambda, theta_s held | **FAIL** Delta chi^2 +8.21 (BAO +8.18, SN +0.03); h 0.6741 -> 0.6602; Omega_dr0 0.194 | **FAIL** +8.23 (BAO +8.19); h 0.6740 -> 0.6601 | Delta chi^2 <= 4 |
| 7(a) primary peaks | verified: omega's above z_dec identical (max \|S - 1\| 1e-13), D_M(z*) held to 1e-8; late ISW NOT EVALUATED | same | verification |
| 7(b) CMB lensing | **NO VERDICT** (KA4b failed); ratio-method reading 13.37 | **NO VERDICT**; 13.38 | chi^2 <= 18.48 |
| 8 forest + fsigma8 | **PASS** forest Delta chi^2 0.010; Rf 0.907 / 0.975 / 0.991 / 0.992 (all inside CE2's 2 sigma) | **PASS** same | as frozen |
| 9 Bullet (on the galaxies) | **FAIL** cls FAIL; M300 2.07, 0.99 e14 (Z -2.71, -3.81) | **FAIL** M300 2.21, 1.06 e14 (Z -2.46, -3.59) | DB1 label PASS |
| 10 Cassini | **PASS** use 2.8e-8, worst planet 0.21 | **PASS** 2.0e-8, 0.19 | GB1 G8 |

## Brackets on the local gates (gates 1, 2, 3, 5, 10)

| setting | canonical | alt |
|---|---|---|
| primary SIS | G1 P, G2 F, G3 F, G5 P, G10 P | same |
| B1 NFW (Duffy 08) | G1 P (0.011), G2 F (0/3), G3 F (+0.044 / 0.109; bins -0.04, +0.06, +0.12), G5 P, G10 P | G1 P, G2 F (0/3), **G3 P** (+0.019 / 0.098; bins -0.06, +0.03, +0.09), G5 P, G10 P |
| B2 abundance matching (Moster 13) | **G1 F** (0.282; 59/59 over), G2 F, G3 F, **G5 F** (rms 0.446; 0.91 M_b inside the last point), G10 P | same pattern |
| B1 + B2 | G1 F (0.151), G2 F, G3 F, G5 F (0.197), G10 P | G1 F, G2 F, G3 P, G5 F, G10 P |

Groups fail in every bracket. KiDS and SPARC pass only on the record's own capture convention. With abundance-matched halos,
the top KiDS bin (log M* 10.9) sits at M200 5.0e12 at z 0.55 and carries 2.4 M_b of the component inside 200 kpc: the
orchestrator's K1 kill, at +0.28 dex. The groups row does not move into its line under any bracket. The label is FAIL under
every bracket.

## Why it fails (from the run)

1. **Groups (first gate).**
   - Pre-conversion columns: x0 1.55-3.17.
   - Under peeling, a group keeps only 7-16 % of its component inside R500, or 0.21-0.45 M_b in all (0.27-0.56 at f* 1).
   - KD1's uniform need is 3.46 M_b (f* 0) and 1.23 M_b (f* 1).
   - The column of a self-similar halo scales as R500^1 (x0 ~ R500 / 135 kpc at z 0.55). One Sigma_gate cannot keep groups
     while the field and the galaxies drain.
2. **X-COP.**
   - Clusters reach x0 6.5-8.8. Inside 0.25 R500 they keep 0.89-0.94 of their component, inside R500 only 0.33-0.42: the
     outer shells have small geometric factors and densities, so they drain.
   - The whole-halo retention is 0.87-1.10 M_b, against KD1's 4.18.
   - The retained profile is too concentrated. The inner bin is over-filled (-0.27); the 0.5-0.75 R500 bin sits near zero.
   - Retained over dynamical mass, by bin: 1.45, 0.65, 0.32. TR1 has 0.71, 0.66, 0.58.
   - TR1's SHAPE statistic with the retained component as the tracer: -0.22, +0.03, +0.20 (RMS 0.18). It does not follow.
3. **Background.**
   - Today 96.9 % of the component has become dark radiation (cosmic S0 0.031; halo part 92 % of it). Omega_dr0 is 0.194.
   - Holding theta_s pulls h to 0.660.
   - D_M changes by +0.87 % at z 0.51, falling to +0.03 % at z 2.33; D_H by -0.79 % to -0.12 %.
   - BAO with r_d fixed by the CMB: Delta chi^2 +8.2.
   - With r_d profiled: +3.7, reported.
   - The w = -0.85 product, a separate sector graded as a bracket only: +183 (h 0.753). The outside text's compensation
     makes the background worse.
4. **Bullet.** The retained component (1.06 M_b main, 0.59 M_b sub) rides on the galaxies but is too little: M300 sits at
   Z -2.7 / -3.8. Mediator drag: Gamma0/Gamma_psi = 1.95e-4, negligible.
5. **Coma UDGs (reported).** Coma's pre-conversion R500 is 1.28 Mpc, but its outer shells drain, so the column at the
   UDGs' radii falls and the bath gives them almost nothing (median retention 0.02, b = 1.04). Coma's own retained
   component deepens the external field, so the shortfall grows from +1.11 to +1.21 dex.

## Known answers

| KA | result |
|---|---|
| KA1 peeling (orchestrator's numbers) | **PASS** 1.35 -> 0.02789, 1.80 -> 0.05641, 3.20 -> 0.50604; frozen-Da 1.80 -> 0.34682 |
| KA2 (A1) geometric factor held, top-hat: central shell = reduced ODE | **PASS** max dev 3e-14; true top-hat central shell 0.0276 / 0.0552 / 0.5002 (reported) |
| convergence (half step) | **PASS** 1e-14 |
| KA3 component -> 0 replays law-only numbers | **PASS** both (QX8 SPARC, KiDS 0, X-COP +0.467500 / 0.476307 and +0.434524 / 0.444158, groups 0/0, UDGs +1.120753 / +1.077576) |
| KA4a LD1 replay | **PASS** 46.322 / 53.039 exactly |
| KA4b ratio method vs CLASS dcdm at LD1's uniform decay, QX15 h | **FAIL** 77.46 vs 59.69 (tolerance 7.67); 92.81 vs 70.40 (9.28) -> gate 7(b) NO VERDICT, as frozen |
| KA5 baseline lensing 8.5599 / 8.5604; forest at R = 1 | **PASS** |
| KA6 Bullet law alone = DB1 K1 | **PASS** |
| KA7 Gamma0 -> 0 background | **PASS** (h to 1e-7, chi^2 to 1e-5 relative) |

**KA4b diagnosis** (`ss1_ka4_diag.py`, `parts/ka4_diag.txt`, post-run, reported):
- The lane's background matches CLASS's dcdm background to 1e-6 in H and D_M.
- The sub-horizon growth matches at k 0.1 (P ratio 0.603 vs 0.598 at z 0).
- The miss: the method drops the freshly converted dark radiation, which still clusters on scales larger than its
  free-streaming length, and it drops horizon-scale terms. So it over-suppresses lensing: S(L) 0.355 vs 0.380 at L 100,
  0.147 vs 0.235 at L 8.
- In the validation case the method over-states chi^2 by 30 %.
- So SS1's reading of 13.4 is probably above the true value, but the frozen rule gives NO VERDICT, and that stands.
- Grading it would need a time-gated decay inside CLASS, which the record's machinery does not have.

## Hand estimates (frozen) as they fired

| estimate | result | |
|---|---|---|
| cluster retention ~0.9 | 0.89-0.94 inside 0.25 R500 (the reduced reading 0.89-0.94) | HIT (core) |
| cluster ~3.7 M_b retained | 0.87-1.10 M_b (outer shells drain) | MISS |
| groups x0 ~3.4, retention ~0.55, ~2.3 M_b | x0 1.55-3.17, 0.07-0.16 inside R500, 0.21-0.45 M_b | MISS |
| KiDS top bin retention ~0.02 | 0.023 | HIT |
| SPARC retention 0.01-0.02 << 0.33 | 0.014-0.023; 0.027 M_b inside the last point | HIT |
| B2: KiDS fails by > 0.5 dex | fails, by 0.28 dex | HIT (fail), MISS (size) |
| cosmic S0 0.06-0.08 | 0.031 | MISS |
| Omega_dr0 0.15-0.2 | 0.194 | HIT |
| BAO FAILS by >> 4 | +8.2 | HIT (fail) |
| lensing between 8.56 and 46 | 13.4 (reading; NO VERDICT) | HIT (reading) |
| UDG shortfall ~+0.9 to +1.1 | +1.21 / +1.17 | MISS (worse) |
| forest PASS; fsigma8 down several %, inside 2 sigma | Delta chi^2 0.01; BGS -9.3 %, passes | HIT |
| HE-a (KiDS primary PASS, B2 FAIL) | yes | HIT |
| HE-b (BAO FAIL) | yes | HIT |
| HE-c (X-COP amount within 0.1 dex) | -0.108 / -0.129 | MISS |
| HE-d (lensing below LD1's 46) | 13.4 (reading) | HIT |

## MUTATE (`ss1_MUTATE.json` / `.out`)

- **M1 (Sigma_gate x 3) and M2 (/ 3): NO BITE by the frozen status-vector rule.**
  - No gate changes status and the label stays FAIL at gate 2.
  - The numbers move a lot. Groups go 0/20 -> 0/20 (M1) and 7/20 (M2) at f* 0. X-COP goes +0.075 (M1) and -0.182 (M2).
    Cosmic S0 goes 0.016 and 0.077. Bullet M300 Z goes -3.8 and -1.4.
  - What it means: the FAIL does not hinge on Sigma_gate within a factor 3 either way.
  - At M2 the groups only reach 7-8 / 20 while the X-COP inner bin over-fills to -0.29. The group amount and the cluster
    shape pull against each other inside one Sigma_gate.
- **M3 (z_dec = 2): BITES.** CMB-lensing reading 69.7 (FAIL). BAO + SN +90. fsigma8 and the F2 allowance also flip to FAIL.
- **M4 (gate off, the LD1 class): BITES.** X-COP +0.441 / +0.409 (FAIL), groups 0/0 and 0/1, Bullet Z -4.5.

## Sigma_gate derivation check

0.042 g/cm^2 is **NOT REPRODUCED** from the stated constants. The search covered products of powers -1 .. +1 in half steps
of sigma/m, v_med, Gamma_psi, R_abs, Gamma0 and c. Only two column-dimension combinations land within 10 %:
- (sigma/m)^-1 (v_med/c) = 0.0451 (+7.5 %)
- (sigma/m)^-1 (Gamma0 c / (v_med Gamma_psi))^1/2 = 0.0397 (-5.5 %)

Neither is within the frozen 2 %. 0.042 is used as given.

## The outside text's four "theorems" (Lean, `ss1_lean/`)

- **Theorem 2** (retention >= 0.615 at x0 3.2): **false as written.**
  - The reduced solution is 0.506.
  - `thm2_corrected` proves 1/2 < f < 0.615.
  - The MUTATE file `SS1_MUTATE.lean` (the bound as written) fails to compile, as it must.
- **Theorem 4** (Gamma0/Gamma_psi = 0.032): **false as written.** `thm4_corrected` proves it is 1.952e-4.
- **Theorems 1 and 3:** their text was not in the lane's inputs (the outside text stays untracked with the orchestrator).
  NOT EVALUATED, disclosed.
- In their place the lane proves the two properties any correct statement about the reduced peeling needs:
  - `peel_ge_bare`: retention >= exp(-tau).
  - `peel_le_frozen`: retention <= exp(-tau/(1 + x0^2)). Self-consistent peeling never keeps more than the frozen-Da
    formula, which is why the outside groups row (frozen) and lens row (peeling) cannot both hold.
- Compiled with `lake env lean` from the record's Lean tree (fable_independent_2026/lean_2026, the working copy):
  exit 0, standard axioms only (propext, Classical.choice, Quot.sound); `compile.txt`, `compile_MUTATE.txt`.

## The outside text's printed claims beside the lane's numbers (numbers only)

| claim | printed by the outside text | the lane |
|---|---|---|
| KiDS shift at 0.3 Mpc | +0.011 / +0.026 / +0.046 | +0.012 to +0.020 (primary); +0.15 to +0.28 (B2) |
| Coma UDG bath retention | 0.85 | 0.02 |
| fsigma8 at z 0.3 | -3.4 % | -9.3 % |
| CMB-lensing Delta C_L at L 100 | -3.1 % | -6.5 % (ratio method) |
| BAO with a bare Lambda | 4.8 sigma, +4-6 % in D_M | Delta chi^2 +8.2; +0.87 % in D_M at z 0.51 |

## Reading

Under one consistent gate rule, the component's own column cannot sort the systems the way the record needs. A self-similar
halo's column grows only as R500, so groups (x0 1.6-3.2) drain to 0.2-0.45 M_b while they need 1.2-3.5. Clusters keep their
cores but lose their outer halos, which gives a retained profile more concentrated than TR1's falling fraction. Turning about
97 % of the component into dark radiation after z 0.55 shifts the BAO distances by about 0.9 % (Delta chi^2 +8 with a bare
Lambda), and the outside text's w = -0.85 fix makes the background worse.

**What a repair would have to change:**
- The gate needs a key that rises much faster than R500 between galaxy and group scale (the pre-read's ~R500^2.4), not the
  self-similar column.
- The retention must stay high out to R500 in clusters (a falling fraction, not a core).
- The converted energy must leave the expansion history intact. Radiation with a bare Lambda fails, and so does a w = -0.85
  product.

KiDS, SPARC, Cassini, the forest and fsigma8 all pass on the record's own capture convention, but KiDS and SPARC lose that
pass under abundance-matched halos.

## Disclosures

1. **Primary halo convention.** KD1 P3 (f_cap 0.76 x R x M_b) assigns galaxy-scale systems small pre-conversion halos. That
   is the record's own convention and the reason KiDS and SPARC pass. Abundance matching (B2) reverses both.
2. **No adiabatic re-expansion.** The retained profile is not re-expanded for the mass that drains; with it the retained
   component would be less concentrated. The KiDS halos are truncated at R200 at z 0.55 (100-200 kpc), so the component
   shift is flat beyond that radius.
3. **Time budget.** Local peeling uses the frozen tau 4.49; the footing lookback gives 4.60, reported.
4. **No accretion after z_dec.** Today's systems are taken as already assembled at z_dec. That is generous to clusters
   (accreted field matter has drained).
5. **Coma UDGs.** Their own halos at z_dec use M* only (KD1 convention), with no tidal truncation; the bath is the host's
   draining column at d_mean.
6. **CMB lensing.** The kernel is the record's linear Limber kernel with the k^-4 factor (GL1 / BG1 limber4), on the SS1
   background's distances. The source ratio comes from the record's two-fluid growth ODE with the cosmic S(tau). Dark
   radiation perturbations are omitted, which caused KA4b's miss; see the diagnosis above.
7. **fsigma8.** Graded on the clustering-matter contrast. The velocity-tracer reading (d delta_b / d ln a) is reported in
   `parts/cosmo_*.json`; it is within 2 % of the graded reading (BGS 0.923 vs 0.907).
8. **Background.** Ingredients:
   - DESI DR2 BAO table and Pantheon+ cuts transcribed from CFG681 (Pantheon+ files read from the shared
     `_external_data`);
   - r_d (146.87 Mpc) and z* from the footing's CLASS reference;
   - the lane's own background integrator, checked against CLASS (KA4 diagnosis, KA7).
9. **Compute.**
   - Local gates 20 s, peak RSS 0.22 GB.
   - Cosmology children 8-16 s each, 0.37-0.56 GB (CLASS).
   - Bullet child 1.36 GB peak (DB1, the record's machinery).
   - PJ1's loaders were imported from a read-only copy of origin/main's lane dir (`SS1_PJ1_DIR`), because the shared
     checkout is behind origin.

## Files

- Criteria and amendment: `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`.
- Scripts: `ss1_core.py`, `ss1.py`, `ss1_cosmo.py`, `ss1_bullet.py`, `ss1_grade.py`, `ss1_ka4_diag.py`, `run_chain.sh`.
- Outputs: `ss1.json` / `ss1.out`, `ss1_MUTATE.json` / `ss1_MUTATE.out`, `parts/`, and the run logs `run_*.txt`.
- Lean: `ss1_lean/`.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
