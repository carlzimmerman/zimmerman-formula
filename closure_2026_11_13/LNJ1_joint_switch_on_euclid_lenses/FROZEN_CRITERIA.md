# LNJ1 FROZEN CRITERIA: is the ceiling break in Euclid's lenses the crossing-speed joint's switch?

TEST lane. Adopts nothing, relabels nothing, registers nothing. Written and committed alone, before any script of this
lane exists and before any number of this lane is computed. Footings never pooled (canonical a0 = 9.3603e-11, alt
1.1312e-10 m/s^2). Cold dark energy is a gravitating field component; no particle. kappa = 1/2 and the share 5.41 are
FITTED. No downloads, no web. One thread, under 2 GB. Nothing outside this folder is edited; owners' code is imported
read-only (bytecode writing off).

**POST HOC, twice.** The wide-lens ceiling break (EUC1 map, EUC4, EUC4R, EUC8, EUC13 / EUC13R by class) was seen before
this lane, and the crossing-speed joint (JNT2) was built after other rows failed. The boundary v*(z) was not tuned to
lenses (it comes from route D's lemma, a0 / (10 (1 + 5.41) H)); that is the only reason this test has any value. Any
favourable word is a HIT awaiting an independent re-grade, never a pass of the theory.

## 0. The question

The law acting on a lens galaxy's stars alone ("law S") has a ceiling on the projected mass it can give inside the
Einstein radius. Euclid lenses with theta_E below about 1.3" sit inside the law's band; those at and above 1.3" sit above
it. JNT2's joint says: systems slower than v*(z) = v*(0) / E(z) (v*(0) = 668.53 / 807.93 km/s) keep the law's layout;
FASTER systems carry their share of cold dark energy as cold dust in the reference layout (FRZ1's halo, as evaluated on
single galaxies in SRJ3), with Newtonian gravity at every radius. Is the ceiling break that switch?

## 1. Sample and files

- Catalogue (the EUC lanes', on disk, hash-checked by EUC1's frozen sha256):
  `_external_data/euclid_dr1_eclipse/eclipse_dr1_catalogue_key_v20261103.csv` and `ECLIPSE_object_catalogue.csv`
  (path set relative to the script).
- Selection: EUC1's cuts exactly (lens_model_success, final_sample, no large-system warning; theta_E > 0, theta_e > 0,
  0.6 <= n <= 10, z > 0, log M* > 0), grades A and B (EUC1's sample S). Primary = S. P (grade A) and grade B alone are
  reported, not graded.
- Lens redshift: the catalogue's median photometric redshift (`eclipse_median_phz`), as EUC1 / EUC4 / EUC13.
- Einstein radius: `eclipse_effective_einstein_radius`; R_E = theta_E D_A(z_l) in the catalogue's cosmology (H0 67.74,
  Om 0.3089), EUC1's `Cosmo`.
- Observed Einstein mass: M_obs = pi R_E^2 Sigma_cr(z_l, z_s).
- **Unknown source redshift (EUC1 / EUC13's treatment).** Primary: source at infinity (z_s = 1100, the lenient case: the
  least mass lensing allows). Bracket: EUC13's member M1 (AGEL DR2 population, `../../closure_2026_11_12/
  EUC10_published_source_redshifts/euc10_partB_samples.csv`, sample AGEL): per lens, z_s drawn from the 10 AGEL systems
  nearest in z_l, redrawn until z_s > z_l + 0.2 (EUC13's recipe, guard 0.2); 50 draws, seed 20261113. The bracket word
  is the word reached in the majority of draws. An UNDER-prediction found at z_s = infinity is robust to real sources
  (they only raise M_obs); an OVER-prediction at z_s = infinity is not.

## 2. Stellar mass and the baryons counted

- **Primary: EUC12's common scale.** EUC12 put ECLIPSE's Salpeter masses and Auger's (SLACS) Salpeter masses on one
  CIGALE scale: delta_E = +0.222 (all P), delta_S = +0.258. The common-scale mass expressed in the Salpeter
  normalisation the record grades SLACS on is log M* = log M*_cat - delta_E + delta_S = log M*_cat + 0.036 (one constant
  for every lens; per-lens deltas exist for 33 lenses only).
- **Bracket: the catalogue's own Salpeter mass** (`eclipse_log_survived_mass_med`, shift 0). Reported only, not a
  bracket: the Chabrier-like CIGALE scale (shift -0.222).
- Baryons counted: the lens galaxy's stars only (catalogue Sersic profile: theta_e, n; Prugniel-Simien deprojection,
  EUC1's functions). **Not counted:** cold or hot gas of the lens, other group members, intragroup light, the group's
  hot gas, line-of-sight structure. Every one of them would raise M_b and the lens speed on the model rule; this is
  stated, not corrected.

## 3. Membership (which side of v*(z_l))

v*(z) from JNT2's `jnt2_common.py` (imported read-only): v*(z) = a0 / (10 (1 + 5.41) H0 E(z)), H0 = 67.4, OL = 0.6847.
s = (lens speed) / v*(z_l). Above the boundary: s >= 1.

- **Primary (JNT2's model rule, from the baryons):** v_L = (10 G (1 + 5.41) M_b H(z_l))^(1/3), M_b = the stars on the
  common scale (section 2). JNT2's `vL_kms`.
- **Bracket (measured-speed rule, from the Einstein radius):** the SIS circular speed that gives the observed Einstein
  mass, v_meas = sqrt(2 G M_obs / (pi R_E)) (SIS: M_2D(<R) = pi sigma^2 R / G, v_c = sqrt(2) sigma). Depends on z_s
  (infinity primary). Note: v_meas and the boost b share theta_E; the shuffle twin (section 7) is what tells a break in
  speed from a break in theta_E.

## 4. Predicted Einstein mass on each side

- **Below (s < 1): the law on the stars, as the EUC lanes compute it.** M_law = (R_E^2 / G) int_R_E^rmax g_S(g_N(r))
  dr / sqrt(r^2 - R_E^2), g_S = (g_N / 2)(1 + sqrt(1 + 4 a0 / g_N)), g_N from the deprojected Sersic stars, rmax 1e6
  kpc, 400-node Gauss-Legendre in u (r = R_E cosh u): EUC1's Engine formula, re-coded here.
- **Above (s >= 1): stars plus the reference layout at the cosmic share, Newtonian, projected in a cylinder inside R_E.**
  M_joint = M* F_2D(R_E) + C_cyl(R_E), where C(r) = X M_b m(min(r, r_ta) / r_s) / m(c_ta), m(x) = ln(1 + x) - x / (1 + x),
  and the halo is FRZ1's (copied from `closure_2026_11_10/FRZ1_forest_redistribution_at_z/frz1_hm.py`, as SRJ3 / DSC1
  evaluate it on single galaxies): M_ta = X M_b h / (1 - f_b) in Msun/h with CFG556's h = 0.6736, f_b = 0.02237 /
  0.14237, Om = 0.14237 / h^2; NFW at 200 x mean density; **concentration c(M) = 10.14 (M / 2e12 Msun/h)^-0.081
  (1 + z)^-1.01** (FRZ1's default, cfac 1); turnaround at mean overdensity Delta_ta(z) = 5.55 + 6.26 (1 - Om(z)) /
  (1 - Om); comoving Mpc/h converted to physical by 1 / (h (1 + z)). C_cyl by the same Abel quadrature as M_law, with
  g = G C(r) / r^2 (mass constant beyond r_ta).
  - **X primary = 5.41 (the cosmic share, the lemma's).** Bracket: X = PD1's per-galaxy share used by SRJ3 / DSC1
    (median `share_over_Mb`: 59.49 / 59.50 for z < 1, 55.72 / 55.73 for z >= 1; canonical / alt).
  - Concentration brackets: c x 0.7 and c x 1.4.
- The law's band (per lens, the EUC lanes' line): **a lens is above the law's band if M_obs > M_law(10^0.25 M*)**, i.e.
  it needs more than 1.78 x its stars for law S (EUC1's b > 0.25).

## 5. Statistics (per footing, per configuration)

(a) **Boost against speed.** b = log10(M_obs / M_law(M*)) (a mass ratio) against s, in bins of s: [0, 0.3), [0.3, 0.4),
[0.4, 0.5), [0.5, 0.6), [0.6, 0.8), [0.8, 1.0), [1.0, 1.25), [1.25, inf): N, median b, fraction above the band. The
fraction above the band on each side of s = 1 with 95 % bootstrap intervals.

(b) **Residual against the joint's own prediction.** r = log10(M_obs / M_pred), M_pred = M_law for s < 1 and M_joint for
s >= 1: median r and 95 % bootstrap interval on each side. Above-side lines: FITS if the interval of median r overlaps
[-0.10, +0.10]; UNDER-PREDICTS if its lower bound > +0.10; OVER-PREDICTS if its upper bound < -0.10. Below-side line:
the law holds below if the fraction above the band among s < 1 lenses is <= 0.20 (point).

(c) **Free break location.** A step in the fraction above the band, f(s) = f_lo for s < s_b and f_hi for s >= s_b, fitted
by binomial maximum likelihood over log10 s_b in [-1.0, +0.6] step 0.01, at least 20 lenses on each side, f_hi > f_lo
required. 400 bootstrap resamples of lenses (seed 20261113), refitted each time: s_b interval = 2.5 / 97.5 percentiles;
Delta f = f_hi - f_lo at each replicate's own s_b. **The break is REAL if the bootstrap 2.5 % point of Delta f >= 0.20.**
The joint says s_b = 1. Reported beside: the same fit in theta_E (arcsec), and the s at which a running fraction above the
band crosses 0.25 and 0.5.

## 6. Labels (per footing; primary = model rule, common scale, z_s infinity, X 5.41, FRZ1 c)

Raw word, in order:
1. Break REAL and 1 inside the s_b interval:
   - N(s >= 1) < 20: NO POWER;
   - joint FITS above and the law holds below: **SWITCH AT THE JOINT'S SPEED** (a HIT, not a pass; post hoc; awaits an
     independent re-grade);
   - joint UNDER- / OVER-PREDICTS above: **JOINT UNDER- / OVER-PREDICTS ABOVE THE BOUNDARY [median r]**;
   - joint FITS above but the law fails below: **LAW FAILS BELOW [fraction]**.
2. Break REAL and 1 outside the interval: **SWITCH AT ANOTHER SPEED [s_b and interval]**. If N(s >= 1) >= 20 and the
   joint is out of its line above, that is stated beside the word (not the word).
3. Break not REAL:
   - N(s < 1) >= 20, N(s >= 1) >= 20 and the bootstrap 97.5 % point of f(s >= 1) - f(s < 1) < 0.10: **NO SWITCH**;
   - N(s >= 1) >= 20 and the joint out of its line above: JOINT UNDER- / OVER-PREDICTS ABOVE THE BOUNDARY;
   - otherwise **NO POWER**.

Power gates (a failed gate turns the word into NO POWER; the raw word is reported beside):
- **Boundary twins.** TW-H (v*/2) and TW-D (2 v*) are re-run through the whole decision. A twin BITES if its raw word
  differs from the main raw word, or N(s >= 1) changes by at least max(5, 25 %), or the fraction above the band among
  s >= 1 lenses moves by >= 0.10 (both with N >= 20). Both must bite, except: for SWITCH AT ANOTHER SPEED with the
  whole interval below 1 only TW-H must bite (TW-D has nothing to move), and with the whole interval above 1 only TW-D.
- **Shuffle twin TW-SH** (stellar masses permuted among lenses, seed 20261113; M_law, membership, halo all recomputed):
  when the main break is REAL, the shuffle must destroy it (bootstrap 2.5 % point of Delta f < 0.20, or Delta f point at
  most half the main one). If it does not, the break is set by the Einstein radius, not by the lens's baryons: NO POWER.

**FRAGILE** if any frozen bracket gives a different final word: catalogue mass scale; c x 0.7; c x 1.4; X = PD1 share;
measured-speed membership (with its own twins); AGEL source draws (majority word over 50 draws; twins run on draw 0).

## 7. Known answers (all must pass, else NOT EVALUABLE)

- KA-1 EUC4's headline fractions with this lane's loader and its own route (M_obs > M_law(10^0.25 M*), no bisection),
  EUC1's footings (alt 1.132e-10, as those lanes ran): W_B (grade B, theta_E >= 1.7") f25 = 0.758 / 0.702 (N 124), to
  0.001; P f25 = 0.156 / 0.139 (N 3,192), to 0.001.
- KA-2 one number of EUC13: M1 AGEL b_med on P = +0.238 / +0.220 (EUC13 KA3, 200 draws, seed 20261112, EUC1 footings),
  to 0.003, with this lane's b-table.
- KA-3 v*(0) = 668.53 / 807.93 km/s to 0.01.
- KA-4 the halo copy against SRJ3 K5 (zC 400569, z 2.24, X 55.72, log M_b 10.95, R_e 4.31 kpc, canonical):
  r_200c 121.62 kpc, r_s 39.53 kpc, g_mod 4.4290e-10 m/s^2, to 0.1 %; and the interpolated halo table against direct
  solves on 20 lenses to 1e-3.
- KA-5 projection: a truncated-free NFW cylinder mass against the analytic projected NFW, and a point mass, to 1e-3.
- KA-6 SI hand check of one lens (Sigma_cr, M_obs, v_meas, v_L) by a second route in plain SI.

## 8. Expectation and hand estimate (written before any number)

- **Model rule.** A median wide lens (log M* 11.66, z 0.43): v_L = (10 G 6.41 x 4.6e11 Msun x H(0.43))^(1/3) ~ 220
  km/s against v*(0.43) ~ 527 / 637 km/s, s ~ 0.42 / 0.35. Even log M* 12.3 at z 1 gives s ~ 0.9. I expect at most a
  handful of lenses at s >= 1, TW-D unable to bite, and **NO POWER on both footings** (P ~ 0.8). On the model rule the
  wide lenses carry only ~0.24 dex more stars than the rest (s higher by ~8 %), so I expect any break in s_mod to be weak.
- **Measured rule.** v_meas(theta_E 2", z 0.43, z_s infinity) ~ 400 km/s, s ~ 0.75 / 0.62; theta_E 1.3" gives s ~ 0.6
  / 0.5. I expect the break at **s_b ~ 0.55-0.65 canonical, ~0.45-0.55 alt, interval excluding 1** (raw SWITCH AT
  ANOTHER SPEED), and the shuffle twin NOT to destroy it (the break lives in theta_E), so the bracket word NO POWER.
- **Amplitude above the boundary.** Median wide lens: stars inside R_E ~ 2.4e11 Msun; the cosmic-share halo (M_ta ~
  2e12 Msun/h, c ~ 7, r_s ~ 38 kpc) puts ~3 % of its cold mass, ~0.8e11, in the 12.6 kpc cylinder; joint ~ 3.2e11
  against M_obs ~ 7e11 (far source): **under-predicts by ~0.3 dex** (~0.6 dex at z_s ~ 2), and is below the law itself
  (the law adds ~2e11 of phantom). The per-galaxy share (X ~ 56) builds a halo 10 x heavier but far more extended
  (r_s ~ 160 kpc), so only ~0.5 % lands inside R_E: ~1.3e11, still under-predicting by ~0.25 dex.
- Probabilities (primary word): NO POWER 0.75; SWITCH AT ANOTHER SPEED 0.12; JOINT UNDER-PREDICTS 0.08; SWITCH AT THE
  JOINT'S SPEED 0.03; NO SWITCH 0.02.

## 9. Outputs

`lnj1.py`; `lnj1.json`, `lnj1.out`, `lnj1_per_lens.csv`; twins `lnj1_MUTATE_TWH`, `_TWD`, `_TWSH` (.json / .out);
`RESULT.md`. No home paths in any file; warnings suppressed; one thread.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
