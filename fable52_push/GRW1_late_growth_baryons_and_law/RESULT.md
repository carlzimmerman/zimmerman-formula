# GRW1 RESULT: baryons under the a0 law do not build late structure when the cold component is warm late. T-A FALLS SHORT / FALLS SHORT; T-S FALLS SHORT AND OVERSHOOTS / FALLS SHORT AND OVERSHOOTS. As frozen: NO VERDICT / NO VERDICT

Criteria 11c19a2c5f (committed alone before any script or number). Amendment A1 4dfa022e34 (POST HOC: two known-answer checks,
committed alone before any graded number). TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing.
Footings never pooled (canonical / alt). kappa = 1/2 FITTED; not theory closed.

## Label

**No treatment of the law builds it, on either footing, at any sound speed tried (350 to 4481 km/s).** The direction of
the miss depends on how the nonlinear law is treated:

- **T-A, the action's own linear theory (primary): FALLS SHORT / FALLS SHORT.** The law reads the clock's acceleration.
  The law's halo is part of the clock's conserved charge, so it has to flow in, and the clock falls toward the baryons at
  best like a cold fluid with no self-gravity. Growth on small scales runs at about a^0.61 (EdS), against a^1 for the cold
  reference and a^0.30 for baryons alone. Every graded line misses (L1, L3, L4, L5 short; L2 fails) at every c_s in MK2's band (1000 to
  4481 km/s). In DT1's bracket (350 to 707 km/s) S8 and the forest are short at every c_s; at 350 km/s T-A meets L1 to L3.
- **T-A-max, the bound on T-A: FALLS SHORT / FALLS SHORT.** It takes c = 1 on every mode and the cold reference's state at z
  700, so it bounds T-A for any external-field treatment and any law history before z 700 (Lean `ta_coeff_mono`,
  `cfac_unit`). It is still short on every line at every c_s.
- **T-S, the static law with the total field as external field (the lead's suggestion): FALLS SHORT AND OVERSHOOTS on both
  footings.** Large scales overshoot by about 300 times in CMB-lensing amplitude. The boosted large-scale field (0.3 to 0.5
  a0) then acts as the external field of small scales. That keeps the small-scale boost near 3, which cannot make up for
  the lost cold clustering, so the forest falls short by 10^4 or more. The record's WG2 and WG6 found this pattern with
  QUMOND in a box: 14 times too much power at L 28, 0.08 times at L 377. T-S also breaks counted once: its halo needs 4 to
  27 times the cold mean density at z 0.
- **As frozen: NO VERDICT / NO VERDICT.** Two known answers failed as written, KA2(b) and KA5(a). Both failed for reasons in
  my own criteria, not in the engine (A1, below). The labels above are under A1.

## The table (c_s = 1000 km/s, the band's most favourable value; canonical / alt)

| line | required | T-A obtained | T-A factor | T-A-max obtained | T-S obtained | T-S factor |
|---|---|---|---|---|---|---|
| L1 CMB-lensing amplitude r_eff (GAL1: PR4 amplitude of X0) | 0.952 to 1.048 | 0.859 / 0.860 | 0.90 short | 0.861 | 289 / 401 | 276 / 383 over |
| L2 CMB-lensing shape Delta chi^2 (KD1 G9a) | <= 4 | 16.2 / 16.2 | 4.1 x the line | 15.8 | 350 / 354 | 87 x the line |
| L3 f sigma8 ratio Rf, DESI DR1, 4 bins x 2 panels (GAL1) | data ratio +- 2 err (LRG1 lower edge 0.83 / 0.90) | 0.665 to 0.706 / 0.665 to 0.707 | 0.76 short (worst bin) | 0.670 to 0.712 | 8.5 to 10.7 / 10.0 to 12.6 | 8.9 / 10.5 over |
| L4 S8 ratio s (KiDS-1000 change, GAL1) | 0.941 to 1.059 | 0.556 / 0.556 | 0.59 short | 0.560 | 19.3 / 23.0 | 18 / 22 over |
| L5 forest gas power ratio, 1.10 to 3.56 h/Mpc, z 2 and 3 (L346) | 0.8 to 1.2 | 7.7e-5 to 0.094 / 7.8e-5 to 0.097 | 1e-4 short (worst bin) | 0.056 to 0.165 (0.07 short) | 2.6e-5 to 0.050 / 2.8e-5 to 0.059 | 3e-5 short |

Higher c_s is worse on every line for T-A. At 4481 km/s: r_eff 0.51, Delta chi^2 180, Rf 0.27 to 0.30, s 0.20, forest at most
4e-4. For T-S, higher c_s means less overshoot on L1 to L4 and a worse forest. Even DT1's 350 km/s does not build it. There
T-A meets L1 (0.966), L2 (1.6) and L3 (0.89 to 0.92), but s is 0.83 and the forest 0.06 to 0.45. On L1 to L4 the footings differ by
under 0.1 % in T-A (the forest's top bin by 2 %). a0 enters T-A only through c, which is already within 1 % of 1 at late times (x = 0.003 to 0.011 at z 0
to 3).

## 1. What was computed

**The universe.** Baryons, photons, neutrinos, a cosmological-constant dark energy (so a0 is constant on each footing),
and the cold component as MK2's exponential term: an isothermal fluid with one sound speed c_s, w = c_s^2. Its comoving
Jeans wavenumber falls as (1 + z)^(1/2), so it is cold early and warm late. At 1000 km/s, k_J is 1.4 per Mpc at z 1100 and
0.043 per Mpc today. The background is GAL1's record reference (QX3 iter2 corner). CLASS carries everything, law off, to
z 700 (the cold component in CLASS's fluid slot). From there a two-fluid Newtonian engine runs to z 0 on 64 k from 1e-3 to
10 per Mpc, 6 angle nodes, with Compton drag and a 1.5e4 K IGM after reionization. Every graded quantity is a ratio to the
cold reference run through the same engine.

**What gravitates.** In action (A) read as form B (the law on everywhere), the cold component's energy density at linear
order is n_d + Pi. Here n_d is the dust part, which carries the pressure, and Pi is the law's halo. Their sum is the
conserved clock charge N (TPA1 E3, E4). Both parts gravitate, and lensing sees Phi = Psi.

**How the law enters.** The law is nonlinear, so linear growth needs a stated treatment.
- **T-A.** The law reads the clock's acceleration A = -c_s^2 grad delta_d (exact for the exponential term). Linearised about
  an external |A| = x a0, the halo is delta_Pi = c q^2 delta_d, with q = k/k_J and c = (1/(1+x))(1 - x mu^2/(1+x)). So the
  pressure acts only on delta_d = delta_N / (1 + c q^2). The clock's force coefficient is 1 - q^2/(1 + c q^2). That is TPA1
  4.4's dispersion with epsilon = c (KA5b). Where (1 - c) q^2 > 1 its static equilibrium is the AQUAL response of the simple
  law, total source = baryons x 1/(mu_e (1 + L_e mu^2)) (Lean `equilibrium_total`, `aqual_response`). x is the
  self-consistent rms clock acceleration over all modes.
- **T-S.** The static law's boost B = 1/(mu_e (1 + L_e mu^2)) acts at once on the Newtonian source of baryons plus the
  dust's clumped part, on every scale. Its x is the self-consistent rms total peculiar field: the large-scale field acting
  as the external field of small scales. This is the record's WG2 R1 rule in linear mean-field form.

**The density lensing sees, relative to the cold reference** (T-A canonical, c_s 1000; `grw1.json` has every run):

| z \ k (per Mpc) | 0.01 | 0.03 | 0.1 | 0.3 | 1 | 3 | 10 |
|---|---|---|---|---|---|---|---|
| 0 | 0.972 | 0.799 | 0.282 | 0.045 | 2.9e-3 | 4.4e-5 | 5e-9 |
| 1 | 0.984 | 0.870 | 0.391 | 0.069 | 4.4e-3 | 7.5e-5 | 8e-9 |
| 2 | 0.989 | 0.907 | 0.479 | 0.095 | 6.0e-3 | 1.1e-4 | 2e-8 |
| 4 | 0.993 | 0.941 | 0.598 | 0.143 | 9.0e-3 | 1.7e-4 | 4e-8 |

T-S canonical at c_s 1000, same grid at z 0: 1700, 1460, 224, 0.30, 1.0e-3, 4e-8, 5e-13. The PR4 per-bin ratio (L 8 to 400)
falls from 0.956 to 0.694 for T-A, and from 492 to 95 for T-S. The z 0 sigma8 is 0.442 (T-A) against the reference's 0.796.

## 2. What it means for every completion with a warm cold component

- **The exponential term (MK2's candidate) cannot carry CMB lensing, growth or the forest, law on or off, at any sound
  speed MK2's other rows allow.** Its last open route, baryons plus the law's halos, is now computed and short. With the
  clusters and groups row already empty (MK2), it fails on two independent fronts.
- **The law does not rescue a warm cold component in the action's own dynamics.** Once the law is on, the warm clock's
  pressure is nearly cancelled on scales below its Jeans length (c near 1). So the clock's charge does clump there, mostly
  as halo (at z 0, rms over k <= 1: delta_N 0.53, of which delta_Pi 0.42 and delta_d 0.18). But it clumps only by falling
  toward the baryons. A non-self-gravitating cold fluid plus baryons grows as a^0.61 in the matter era (Lean
  `exponent_order`: a^0.30 < a^0.61 < a^1). The boost the static law promises, 1/(1 - c) of about 50 to 300 at x 0.003 to 0.011, never arrives in
  linear growth, because the halo it needs is the clock's own charge and has to be carried in.
- **If the halo were simply in place (T-S), structure overshoots on large scales and still falls short on small ones.**
  That is the WG2/WG6 shape failure again, now with the cold component present. It also needs more cold charge than
  exists (counted once broken by 4 to 27 times at z 0). So the static-law reading is not a way out either.
- **What survives: a completion that stays cold until late.** Reported only, not graded (step family W: cold until z_w,
  then 1000 km/s, T-A):

  | z_w | L1 r_eff | L2 | L3 Rf | L4 s | L5 forest | T-A label |
  |---|---|---|---|---|---|---|
  | 3 (frozen) | 0.956 | 0.23 | 0.93 to 0.97 | 0.790 | 1.00 | FALLS SHORT (S8) |
  | 2 (added after the run) | 0.975 | -0.06 | 0.96 to 0.99 | 0.847 | 1.00 | FALLS SHORT (S8) |
  | 1 (frozen) | 0.995 | 0.00 | 0.99 to 1.00 | 0.928 | 1.00 | FALLS SHORT (S8, factor 0.987) |
  | 0.5 (added after the run) | 0.999 | 0.00 | 1.00 | 0.974 | 1.00 | BUILDS IT |

  With the law off the same histories fail S8 badly (0.48, 0.52, 0.64, 0.79). So T-A does real work for a late warm-up, and
  the line is crossed between z_w 1 and 0.5. Such a completion is not excluded by this lane. It faces a different problem,
  not computed here. Galaxies that formed while it was cold would have captured cold dust (QX3 G3: about 4 M_b inside the
  optical radius). And dust at galaxy densities sits where the term is steep, which is the cold part, so it would not
  obviously leave when the mean warms. Whether a late warm-up keeps galaxies clean is now the open question for this
  family.

## 3. What it does not settle

- **It is not an N-body run.** Linear theory only, on the gravitating field (CFG555's rule). The forest band and k >= 1
  per Mpc are mildly nonlinear in the reference. The ratios are where linear theory is most reliable, but the forest
  numbers are linear-proxy numbers, as L346's are.
- **The nonlinear law is a mean field.** Each mode is linearised about the rms field, angle-averaged over 6 nodes. T-A-max
  removes T-A's dependence on that choice, and it is still short. T-S's numbers depend on it. A real web has a
  distribution of fields: the record's WG1 measured 0.003 to 0.22 a0, against T-S's 0.3 to 0.5 a0.
- **Before z 700** the law is off (CLASS). T-A-max bounds that too, from the cold side. T-A started at z 900 gives the same
  label (r_eff 0.832, forest at most 0.095 at 1000 km/s).
- **Baryonic physics.** The IGM model is one temperature (1.5e4 K, gamma 1.5). With zero heating T-A-max's forest is 0.065 to 0.167, with 3e4 K
  0.048 to 0.164, against the line's 0.8 (`grw1_extra.out`; 0.056 to 0.165 at the frozen 1.5e4 K). No feedback, no reionization patchiness, no gas-dust
  coupling beyond gravity.
- **Other completions.** Only the exponential term (constant c_s) is graded, plus the step family as a report. A dust
  term with another n(x) is covered only to the extent the step family brackets it.
- **The primary CMB** is not re-graded (MK2 row a2 holds it at the reference's lensing).

## 4. What it finds wrong

1. **MK2 section b's "would demand" values for CMB lensing are too strict by about ten.** MK2 wrote that the
   CMB-lensing line, if the dust had to supply it, needs c_s <= 43 km/s (k_J >= 1 per Mpc at z 0). It was a closed-form
   stand-in, reported only. Graded on the record's own PR4 lines here, the warm component meets L1 and L2 with the law off
   at 350 km/s (r_eff 0.961, Delta chi^2 2.2) and misses at 500 (0.933). The growth stand-in (316 km/s) is about right: at
   350 km/s, f sigma8 is just short (0.87 to 0.90, factor 0.98). The forest stand-in (36 km/s) cannot be checked here; the
   forest fails at 350 km/s by about 170.
2. **DT1 section 4 item 1 and MK2 ("the dust does not clump below 25 to 70 Mpc", "nothing on the record computes what the
   baryons and the law build instead") treat the warm component as a law-off fluid.** In form B the law is on, and it
   cancels most of the clock's pressure below the Jeans length. So the clock's charge does clump there, as halo. The
   Jeans length is the clustering scale of the dust part n_d only, not of the clock's gravitating charge. This does not
   change MK2's or DT1's conclusion (the structure is still too low), but it changes the reason. It is not "nothing clumps
   below L_J"; it is "what clumps below L_J only falls".
3. **CLOSURE.md's "the law's halo is real, gravitating and conserved" carries a consequence CLOSURE.md does not draw.**
   Because the halo is part of the conserved clock charge, a halo cannot appear faster than the clock can carry charge in.
   In linear cosmology that caps growth at the non-self-gravitating rate (T-A-max). COL1 found the same limit in the
   nonlinear regime from the other side (the clock falls like test particles). So the static law's large boost is not
   available to structure growth in this action at linear order either.
4. **DT1's "everything small and late has to be built by baryons and the law's halos"** is right only if "the law's halos"
   means the cold component's own charge. They are not extra mass (counted once). T-S, which treats them as extra, needs 4
   to 27 times the cold mean.

**What in the brief was wrong.**
- "Take z_w and L_J from MK2's passing band": MK2's term has no z_w. It is warm on small scales from before recombination,
  and its warmth spreads to larger scales as (1 + z)^(-1/2). The step family supplies the z_w reading, and there the answer
  turns on z_w (above).
- The suggested treatment (the law's boost on the total field, with the large-scale field as the external field) is not
  how the action's law enters. The action's law reads the clock's acceleration, so a field the clock falls with carries no
  law: the equivalence-principle argument REL1 made. Graded, that treatment repeats the record's WG2 failure in both
  directions at once.
- The lead's hand expectation said the result "could land on either side". T-S lands on both sides at once; T-A lands
  short. "Baryons alone start a factor of several behind" undersells it: on forest scales with the law off the shortfall is
  10^2 to 10^8 in power across MK2's band.

## Known answers (as frozen 4 of 6 pass; under A1 6 of 6)

| | what | value |
|---|---|---|
| KA1 | GAL1's PR4 row: A_X0, sigma_A,rel, chi^2(X0) | 1.0210287, 0.0240616, 8.5708 (record 8.5709): exact |
| KA2 | cold reference, law off, my engine from z 700 against CLASS | (a) D, f, f sigma8 at GAL1's 8 z: 1.7e-3 (line 2e-3). (b) P within 1 % at k 0.04 to 10: **as frozen 0.369, FAIL** (my engine has IGM photoheating, CLASS has none); A1a with the heating zeroed: 1.8e-3, PASS |
| KA3 | EdS late slopes | baryons alone (f 0.157 / 0.05 / 0.5): 0.29589 / 0.12081 / 0.65139 = (-1 + sqrt(1 + 24 f))/4; T-A at c = 1: 0.60937 / 0.40503 / 0.87961 = the eigen-exponent; T-A at c = 0, q -> infinity: equals baryons alone; max error 5e-7 |
| KA4 | warm law-off engine against CLASS's fluid, c_s 1000 and 4481, z 0, 1, 3 | max \|delta_mine - delta_CLASS\| / \|delta_ref\| = 1.6e-3 (line 1e-2) |
| KA5 | the law's linear response | (a) **as frozen 1.03e-12 against 1e-12, FAIL** (float roundoff of 1 - c at x 1e-4); A1b exact rationals: 0 of 100 mismatches. (b) T-A = TPA1 4.4: 1.8e-15. (c) 1-D nonlinear AQUAL along and across x 0.03 / 0.3 / 3: within 4e-8 of B(1), B(0) |
| KA6 | Limber | constant ratio 8e-15; absolute X_L against CLASS within 4e-4 at L 100 to 400; z-only against k-code 8e-15 |

Numerical convergence (reported, not frozen): rtol 1e-7 to 1e-9 changes r_eff, s and the forest by under 1e-7 relative,
for both T-A and T-S.

## MUTATE (separate outputs `grw1_MUTATE_*.json/.out`; c_s 1000 and 4481, both footings)

| arm | stated direction | T-A | T-S |
|---|---|---|---|
| M-OFF (law off) | every graded quantity down | **bites** 4 of 4 (down 3 % to 99.97 %) | **bites** 4 of 4 (down 54 % to 99.9 %) |
| M-COLD (cold throughout, law on) | T-A: back to the reference exactly; T-S: up | **bites** 4 of 4 (every ratio 1 within 1e-6) | **does not bite as frozen**, 0 of 4: 17 of 18 quantities rise (s to 35, the forest by up to 1e9), but r_eff falls 11 to 30 % (289 to 257) |
| M-2A0 (a0 doubled) | up | **bites** 3 of 4; **does not bite as frozen** on alt at 1000 km/s: the top forest bin (3.56 h/Mpc) at z 3 falls 1.6 % (9.5e-5 to 9.3e-5, at 1e-4 of the reference); the other 17 quantities rise | **bites** 4 of 4 (up 13 % to 250 %) |

**Disclosed.**
- M-COLD under T-S: the PR4 amplitude fit weights the low-L bins. The warm T-S runs have a larger low-L excess than the
  cold one (k 0.01: 1700 to 2900 times against a flatter boost), so r_eff is not monotone in "more structure" once the
  shape is this far off.
- M-2A0 under T-A on alt: at the top forest bin, T-A's early pressure history (x near 0.6 at z 700) is not monotone in a0.
- No label rests on either arm.

## Lean

`fable_independent_2026/lean_2026/GRW1.lean`: 13 theorems, standard axioms only (`compile.txt`, exit 0).
- `ta_coeff_mono`, `ta_coeff_le_cold`, `ta_coeff_one`, `cfac_unit`: the T-A-max bound.
- `aqual_response`, `equilibrium_total`: the static limit is the AQUAL law.
- `exp_baryons`, `lam_root`, `pA_root`, `g_one`, `g_strictMono`, `baryons_is_g`, `exponent_order`: the growth exponents,
  ordered.

The twin `GRW1_MUTATE.lean` (`compile_MUTATE.txt`, exit 1) has 7 errors, one per false statement: the coefficient
falling with c, 2/(1 + q^2) at c = 1, the AQUAL angle term's sign flipped, the equilibrium with +1 in the denominator, the
baryon quadratic without its 1/2, the eigenvalue with +f lambda, and c > 1.

## Files and commits

- `FROZEN_CRITERIA.md` (11c19a2c5f) and `AMENDMENT_A1.md` (4dfa022e34), each committed alone.
- Engine and known answers (60678cadaa): `grw1_lib.py`, `grw1_obs.py`, `grw1_ka.py` -> `grw1_ka.json` / `.out` (`run_ka.txt`).
- `grw1_run.py` -> `grw1.json` / `.out` (`run_main.txt`): every model, treatment and footing, the step family, z_start 900,
  and the tolerance check. Per-run JSON in `parts/*.json`. The state files `parts/*.npz` are regenerated and not committed.
- `grw1_run.py --mutate off|cold|2a0` -> `grw1_MUTATE_<arm>.json` / `.out` (`run_mutate_*.txt`).
- `grw1_extra.py` -> `grw1_extra.json` / `.out` (`run_extra.txt`). Reported only: W at z_w 2 and 0.5, and the IGM
  temperature.
- Lean `GRW1.lean`, `GRW1_MUTATE.lean`; `compile.txt`, `compile_MUTATE.txt`.
- One thread. The main run takes 16 s, all runs about 2 minutes. Peak 0.60 GB (the M-COLD run). Nothing downloaded.
- Inputs read only, never edited: QX3 iter2 (`iter2.py`, `iter2.json`) with the PR4 files via cfg917_lib; SV5
  `sv5_t0.json`; GAL1's DESI and S8 rows; L346's forest band; TPA1's EQUATIONS.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
