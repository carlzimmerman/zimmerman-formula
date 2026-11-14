# AGB1 — the supernova progenitor-age bias, tested on DESI DR2 BAO and the DES-SN5YR Dovekie supernovae (FROZEN, before any number)

2026-11-13. Owner: "swing a lane on the progenitor age bias". A test of a published claim on public data.
It adopts nothing and edits no ledger. No script of this lane exists when this file is committed.

## Why
Son et al. (arXiv:2510.13121, MNRAS 544, 975; "S25" below) say that standardised supernova brightness depends on
progenitor age, that progenitors were younger in the past, and that once this is corrected the supernovae plus BAO
plus CMB give a universe that is **not accelerating today** (q0 > 0), with dark energy that changes in time.
Wiseman et al. (arXiv:2601.13785) and Murakami et al. (arXiv:2604.16597) say the effect is several times smaller and
changes nothing; Chung et al. (arXiv:2605.21586) reply that about 85 % of it survives. The repository has cited the
dispute (`real_research/a0z_snia_systematics_forks.py`, 2026-07-20) but no lane has put it to data.
This lane asks three questions of the distances on disk:
1. **Amplitude.** Do the data want a redshift drift of supernova magnitudes with the S25 shape, and how much of it?
2. **Today.** With the correction off, on at its published size, and free: is the expansion speeding up today?
3. **Ever.** In each of those cases: is a universe that never accelerated allowed? This is the question the 1998
   supernova result answered, so it is the one that decides whether that result is overturned.

## Data
1. **DESI DR2 BAO**, arXiv:2503.14738 Table `tab:alphas`, the vector hard-coded and checked against the TeX in
   `closure_2026_11_13/NUF1_neutrino_floor_geometry/nuf1_run.py`: BGS D_V/r_d at z 0.295; D_M/r_d, D_H/r_d and their
   correlation for LRG1 (0.510), LRG2 (0.706), LRG3+ELG1 (0.934), ELG2 (1.321), QSO (1.484), Lyα (2.330). Bins independent.
2. **DES-SN5YR Dovekie** Hubble diagram and STAT+SYS inverse covariance, `_external_data/cfg684_inputs/des5/`, loaded
   as CFG684 and as the DES likelihood file beside it: zHD for the distance, (1 + zHEL) in the luminosity factor, the
   offset ℳ marginalised analytically, a dropped supernova removed by inverting, taking the sub-block and inverting.
   Counts checked before the freeze (redshifts and survey codes only, no magnitudes): 1,820 supernovae; 1,623 DES
   (IDSURVEY 10, z 0.0733–1.1442, median 0.519); 197 legacy (z 0.0251–0.0870).
3. **Compressed CMB prior** (Part C only), arXiv:2503.14738 Appendix A, mean and covariance of (θ*, ω_b, ω_bc) as
   hard-coded in `nuf1_run.py` (verbatim from the TeX).

## The correction template (built before the freeze; no supernova magnitude was read to build it)
S25 give the correction as Δm(z) = 0.030 mag/Gyr × Δage(z), with Δage(z) the fall of the median progenitor age since
z = 0, and say it is applied as μ → μ − Δm(z). They print no table of Δage(z); it is a plotted curve. The web reading of
S25 (PROVISIONAL, summariser) gives: slope 0.030 ± 0.004 mag/Gyr; "a 5.3 Gyr variation" over 0 < z < 1, so about
0.16 mag; the method of Childress et al. (2014): cosmic star-formation history folded with a delay-time distribution.
Wiseman et al. state S25's delay-time distribution as a power law of slope −1 with a prompt time of 0.3 Gyr.
**Template T_S (primary), rebuilt here from that recipe:** star-formation history of Behroozi et al. (2013),
ψ(z) ∝ 1/(10^{−0.997(z−1.243)} + 10^{0.241(z−1.243)}); delay-time distribution of Childress et al. (2014),
Φ(t) ∝ (t/t_p)^α / ((t/t_p)^{α−s} + 1) with t_p = 0.3 Gyr, α = 20, s = −1; progenitor ages τ at redshift z weighted by
ψ(z_form(t(z) − τ)) Φ(τ); the **median** age; age–redshift relation of a flat w0–wa background with H0 = 63.6 km/s/Mpc,
Ω_m = 0.353, w0 = −0.42, wa = −1.75 (the DESI DR2 BAO + CMB fit S25 say they used; my recollection of those four
values, not re-read, and they matter little: a flat Ω_m = 0.3, H0 = 70 background changes Δage(1) from 5.44 to 5.29 Gyr).
T_S(z) = 0.030 × [age(0) − age(z)] mag. Values computed before the freeze: median age 6.70 Gyr at z = 0;
Δage = 0.64, 1.21, 2.17, 2.94, 4.07, 4.81, 5.44, 5.68 Gyr at z = 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.2;
so T_S = 0.019, 0.036, 0.065, 0.088, 0.122, 0.144, 0.163, 0.170 mag.
**Template T_W (control shape):** star-formation history of Madau & Dickinson (2014); power-law delay-time distribution
of slope −1.13 from 40 Myr (the values Wiseman et al. prefer); median age; same background; the same 0.030 mag/Gyr.
Computed: median age 2.30 Gyr at z = 0; Δage = 1.57, 1.92, 1.99 Gyr at z = 0.5, 1.0, 1.2.
**Amplitude.** The fitted model is μ_model(z) + ℳ + A × T(z_HD). A = 0 is the published Dovekie moduli; A = 1 is the
S25 correction at its published size. A is a pure number; negative values are allowed.
For T_W, A_W = 1 means "the S25 slope with the short-delay age history"; Wiseman et al.'s own slope
(−0.007 mag/Gyr) corresponds to A_W = 0.23.

## Part A — BAO + supernovae, no CMB (primary)
**Model.** Flat, w(a) = w0 + wa(1 − a): E²(z) = Ω_m(1+z)³ + (1 − Ω_m)(1+z)^{3(1+w0+wa)} exp(−3 wa z/(1+z)).
No radiation (it changes D_H at z 2.33 by 0.04 %, against a 1.2 % error). Fitted: Ω_m in (0.05, 0.7), w0 in [−3, 1],
wa in [−3, 2], w0 + wa < 0 (DESI's bounds on w0 and wa). Profiled analytically: the BAO scale c/(H0 r_d), the supernova
offset ℳ, and A when it is free (all three enter linearly). Distances by quadrature of 1/E.
Deceleration: q(z) = ½ + (3/2) w(z) Ω_DE(z); q0 = ½ + (3/2) w0 (1 − Ω_m).
**Samples.** `full` (1,820; primary, the selection S25 used); `des_only` (1,623, legacy dropped; the bracket this
repository requires of every Dovekie lane); `rand197` (legacy kept, 197 DES supernovae dropped, numpy default_rng seed
20261113 over the DES rows in file order, the draw of LGS1; a size control).
**Fits, per sample.**
- *A profile:* χ² minimised over (Ω_m, w0, wa) at each A on the grid −1.0 … 3.0 in steps of 0.1, and once with A free.
  Reported: best A, the Δχ² = 1 and Δχ² = 4 intervals, Δχ²(A = 0) and Δχ²(A = 1), both measured from the A-free minimum.
- *Three forks:* A = 0, A = 1, A free. For each: the best fit (Ω_m, w0, wa, q0); the best fit with q0 = 0 imposed
  (w0 = −1/(3(1 − Ω_m))), giving Δχ²_today; and the best fit with q(z) ≥ 0 at every z in [0, 2.33] imposed, giving Δχ²_never.
Minimiser: Nelder–Mead from four fixed starts (Ω_m, w0, wa) = (0.31, −1, 0), (0.32, −0.8, −0.7), (0.35, −0.45, −1.7),
(0.37, −0.3, −2.2) plus the neighbouring grid point, each polished by a restart; the lowest χ² is kept. The inequality
is imposed by a quadratic penalty and the reported χ² is the unpenalised one at a point that satisfies it to 10⁻³.
A best fit on a prior edge is flagged AT PRIOR EDGE.

**Frozen words (judged on `full`).**
- **W1, amplitude:**
  AGE BIAS EXCLUDED AT 3 SIGMA if Δχ²(A=1) ≥ 9 and Δχ²(A=0) < 4;
  AGE BIAS DISFAVOURED if 4 ≤ Δχ²(A=1) < 9 and Δχ²(A=0) < 4;
  AGE BIAS REQUIRED AT 3 SIGMA if Δχ²(A=0) ≥ 9 and Δχ²(A=1) < 4;
  AGE BIAS FAVOURED if 4 ≤ Δχ²(A=0) < 9 and Δχ²(A=1) < 4;
  UNDECIDED if both are < 4; NEITHER if both are ≥ 4.
  Second word: ROBUST if `des_only` and `bao_overlap` (below) give the same first word, else FRAGILE, naming which.
- **W2, today, per fork:** ACCELERATING TODAY if the best-fit q0 < 0 and Δχ²_today ≥ 4; DECELERATING TODAY if the
  best-fit q0 > 0 and Δχ²_today ≥ 4; else SIGN NOT SETTLED.
- **W3, ever, per fork:** NEVER-ACCELERATED EXCLUDED AT 3 SIGMA if Δχ²_never ≥ 9; NEVER-ACCELERATED DISFAVOURED if
  4 ≤ Δχ²_never < 9; NEVER-ACCELERATED ALLOWED if < 4.
W2 and W3 are also printed for `des_only`; they carry the same words there and no second word.

**Controls.**
- `des_only`: every fit above.
- `rand197`: the A profile only. If `des_only` changes W1 and `rand197` does not, the change comes from the legacy set
  and not from the loss of 197 objects.
- `bao_overlap`: `full` supernovae with only the BAO bins inside the supernova range (BGS, LRG1, LRG2, LRG3+ELG1;
  z_eff < 1.2). The A profile and the three forks.

**Known-answer checks (judged before the words are read).**
- **KT, template.** Δage_S(1.0) in [5.0, 5.6] Gyr and T_S(1.0) in [0.15, 0.17] mag (S25: 5.3 Gyr, about 0.16 mag);
  Δage_W(1.2) in [1.7, 2.1] Gyr (Wiseman et al.: 1.9 Gyr between z 0 and 1.2). Already computed above: 5.44, 0.163, 1.99.
- **K1, BAO only, flat ΛCDM.** Target arXiv:2503.14738: Ω_m = 0.2975 ± 0.0086, h r_d = 101.54 ± 0.73 Mpc.
  Pass: |ΔΩ_m| ≤ 0.003 and |Δ(h r_d)| ≤ 0.3 Mpc (NUF1's K1 tolerances and reasons; a wrong D_V or D_H definition
  moves Ω_m by ≥ 0.01).
- **K2, supernovae only, flat ΛCDM, `full`.** Target arXiv:2511.07517 abstract (web reading, PROVISIONAL):
  Ω_m = 0.330 ± 0.015. Pass: |ΔΩ_m| ≤ 0.0075 (half a sigma: best fit against a posterior mean of a one-parameter,
  nearly Gaussian likelihood; the older DES-SN5YR calibration sits at 0.352, three tolerances away).
- **K4, the w0–wa integrator.** D_M and D_H at z = 0.5, 1.0, 2.33 for (Ω_m, w0, wa) = (0.32, −0.8, −0.7) against
  CAMB 1.6.6 (PPF, h = 0.68, massless neutrinos). Pass: every relative difference ≤ 1 × 10⁻³ (CAMB carries radiation,
  worth up to 0.05 %; a wrong exponent in the dark-energy density is worth several per cent).
- **K3, mutation twins (exit 3 on pass, 4 on fail).** Supernova and BAO vectors replaced by the model's own
  prediction at (Ω_m, w0, wa) = (0.31, −0.8, −0.6), h r_d = 101.6 Mpc, plus A_true × T_S, covariances unchanged, no noise;
  twins with A_true = 1 and A_true = 0. Pass each: |A_free − A_true| ≤ 0.01, |w0 + 0.8| ≤ 0.01, |wa + 0.6| ≤ 0.05,
  χ²_min ≤ 10⁻³, and Δχ² at the wrong amplitude (A = 0 for the first twin, A = 1 for the second) > 0.
- **KA, the A profile against the analytic fit.** |spline minimum of the grid − A_free| ≤ 0.03 and the two χ²_min
  within 0.05, on `full`.
If KT, K1, K2, K3, K4 or KA fails, the Part A words are **NOT EVALUABLE**; the numbers are still reported as a reading.

## Part C — the same with DESI's compressed CMB prior (inherited early-universe physics; its own words)
Fitted: h, ω_b, ω_bc, w0, wa (bounds as Part A); Σm_ν = 0.06 eV in one massive state, N_eff = 3.044; CAMB 1.6.6
background (PPF) for D_M(z), H(z), r_d and θ*; χ² = BAO + prior + supernovae, with ℳ and A profiled analytically.
q(z) from the flat formula of Part A with Ω_m = (ω_bc + 0.06/93.14)/h² (radiation left out: 10⁻⁴ in q0).
Samples `full` and `des_only`. A grid −1.0 … 3.0 in steps of 0.25 plus A free; the three forks with Δχ²_today and
Δχ²_never as in Part A. Words **W1c, W2c, W3c** by the same rules, judged on `full`; W1c's second word from `des_only` alone.
These words rest on standard physics before recombination and are reported beside Part A, never in place of it.
- **K5.** BAO + prior, no supernovae: χ²(w0–wa) − χ²(ΛCDM) within ±1.0 of −8.0 (arXiv:2503.14738 Table `tab:dchisq`;
  NUF1's K2A).
- **K6.** BAO + prior + `full` supernovae, A = 0: w0 within ±0.040 of −0.803 and wa within ±0.16 of −0.72
  (arXiv:2511.07517 abstract, PROVISIONAL: −0.803 ± 0.054, −0.72 ± 0.21 with the full CMB likelihoods; three quarters
  of a sigma for the compressed prior, best fit against posterior mean, and the minimiser; the older calibration sits at
  −0.752, −0.86).
If K5 or K6 fails, the Part C words are NOT EVALUABLE. Part A does not depend on them.

## Part B — this repository's Dovekie lanes re-read with the S25 correction at A = 1
`agb1_reread.py` executes the committed sources of CFG684 and CFG689 as LGS1's harness does, with one more exact
substitution: the moduli become μ − A × T_S(zHD) before the selection. Rules are LGS1's, with the age correction in
the place of the legacy cut; each A = 1 run is compared with the A = 0 run **of the same sample**, taken from LGS1's
committed outputs (`lgs1_cfg684_<sample>.json`, `lgs1_cfg689_<mode>_<sample>.json`).
- **Harness checks.** `cfg684 full A=0` must reproduce `cfg684_results.json` (Δχ²_max, flat-a0 Ω_m mean and sd, tracking
  and rival bands at z* 1.0, 1.5, 2.33) to 10⁻⁶ in both combinations. `cfg689 TD5F des_only A=0` must reproduce LGS1's
  committed tracking √X quantiles at z* 1.0, 1.2, 1.5, 2.33 to 0.005. A failed check makes that script's rows NOT EVALUABLE.
- **CFG684 (BAO+DES5 and BAO+DES5+CC), samples `full` and `des_only`:**
  A1 DEGENERACY BROKEN if Δχ²_max ≥ 4, else NOT BROKEN;
  A2 ROBUST if the flat-a0 Ω_m at A = 1 agrees with A = 0 within the two sd added in quadrature, else AGE-DEPENDENT;
  A3 FLOOR HOLDS if the lower edge of the tracking band √X(2.33) is above 0, else FLOOR LOST.
- **CFG689 modes D5 and TD5F (60,000 steps, same seeds), samples `full` and `des_only`:**
  B1 per z* (1.0, 1.2, 1.5, 2.33): STABLE if the A = 1 median of tracking √X lies inside the A = 0 68 % band and the
  A = 0 median inside the A = 1 68 % band, else SHIFTED;
  B2 CLASS UNCHANGED if the script's P1 and P0 classes are the same, else CLASS CHANGED.
  The script's chain check (K4 of CFG689) must be ok or the mode is NOT EVALUABLE. A mode that exits on its busy-machine
  guard (exit 75) is NOT RUN. P2 (free nodes against constant dark energy), e_3σ and the script's native H0 are
  reported, no label.

## Reported only (no frozen word)
- `tmpl_W`: Part A's A profile on `full` and `des_only` with template T_W: best A_W, intervals, Δχ² at A_W = 0, 0.23, 1.
- `legacy_offset`: on `full`, Part A with a constant offset δ between the 197 legacy supernovae and the DES ones in the
  place of the age template (δ free: best δ and Δχ² at δ = 0), and with δ and A both free (best A, its interval, and
  Δχ² at A = 0 and A = 1 with δ free). It asks whether a wanted "age drift" is a step between surveys.
- For every fork: the redshift and value of the smallest q(z), and the χ² split (BAO, supernovae, prior).
- S25's printed fits beside ours (PROVISIONAL web reading; S25 used the older DES-SN5YR calibration and the full CMB
  likelihoods, so these are comparisons, not checks): BAO + DES5Y corrected, no CMB: Ω_m 0.374 ± 0.011, w0 −0.320 ± 0.072,
  wa −2.136 ± 0.386, q0 +0.199 ± 0.070; BAO + CMB + DES5Y corrected: 0.363 ± 0.006, −0.337 ± 0.062, −1.902 ± 0.246,
  +0.178 ± 0.061; uncorrected: 0.319 ± 0.006, −0.754 ± 0.056, −0.848 ± 0.217, −0.271 ± 0.061; BAO + CMB without supernovae:
  w0 −0.430 ± 0.207, wa −1.704 ± 0.580, q0 +0.075 ± 0.215.

## What the result may and may not say
- A is the size of a redshift drift with the S25 shape. A fit cannot tell progenitor age from anything else with that
  shape: a calibration step between surveys, selection, dust, or an expansion history outside the flat w0–wa family.
  A non-zero A is therefore "the distances want a drift of this shape", not "progenitor age is the cause"; whether age
  causes it is settled by host-galaxy data this lane does not read.
- All three words live inside the flat w0–wa family. "Never accelerated" means no member of that family with q ≥ 0
  throughout fits. Δχ² thresholds are read as one degree of freedom (4 = 2σ, 9 = 3σ).
- The Dovekie moduli carry the DES team's own bias corrections and host-mass step, computed with a reference cosmology.
  That is inherited and not re-derived here.
- Part A and Part C do not grade this repository's framework and use no a0. Part B is a re-read: ROBUST / STABLE means
  the committed numbers do not lean on the age question; AGE-DEPENDENT / SHIFTED means they do, and those lanes then
  carry that as a stated dependence. It does not say which amplitude is right.

## Files and order
`agb1_run.py MODE` (Parts A and C, one mode per process, `agb1_<MODE>.json` and `.out`), `agb1_reread.py` (Part B),
`agb1_collect.py` (applies the checks and the words; `agb1_results.json`, `agb1_collect.out`).
This file is committed alone, before any script. The scripts are committed next, before any real-data number; until
then only the K3 twins, KT and K4 (none reads a measured magnitude) are run, in a scratch copy, to debug plumbing.
Any change after this commit is a dated amendment committed alone before the re-run, and both readings are reported.

kappa = 1/2 FITTED; not theory closed.
