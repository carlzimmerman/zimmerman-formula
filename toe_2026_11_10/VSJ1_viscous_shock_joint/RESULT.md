# VSJ1 RESULT: is VSH1's settled state the joint? (2026-11-12)

**Label, canonical and alt: NO VERDICT / NO VERDICT as frozen. Under AMENDMENT A1 (post hoc): STANDS BUT MISCOUNTED /
STANDS BUT MISCOUNTED. VSH1's settled state is not the joint.** The clock does come to rest behind the shock (G1,
reproduced with independent time stepping at every mass and footing). But in action (A) kept whole the standing region
then gravitates as the baryons, plus the real hot charge, plus the law's phantom of both (G2). That misses the law for
the baryons alone under both supplies (G3), it ends in a wall with a jump of 8.3 to 54 in the field (G4), and it stops
short of the cap and the KiDS windows (G5).

- **As frozen** the lane has no verdict: the frozen statistic for the edge of the standing region does not measure
  standing (it stays under its line beyond the turnaround radius in every run), and S-cosmo's host rule was not tuned
  under it. A1 replaces it with a local rule. A1 was written after the first runs were seen and before any gate was
  graded. The frozen-edge readings are reported below; none of them passes a gate that A1 fails.
- **Under A1** every known answer passes and every MUTATE twin bites.

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled. Cold dark energy is
a field, never a particle. Not a LCDM lane. Criteria `FROZEN_CRITERIA.md`, committed alone before any script or number;
`AMENDMENT_A1.md`, post hoc, committed alone. Because the label rests on a post hoc amendment it needs an independent
regrade before any paper quotes it as a verdict. Step R found no independent regrade of VSH1.

## The answer in plain words

1. **It stands.** VSH1's result holds under a different integrator: a viscous clock with the heat kept is at rest and in
   pressure balance inside CFG461's edge at log M_b 9 / 10.5 / 11.5 on both footings.
2. **What gravitates there is not what VSH1's force law assumed.** In (A), the polarization P is tied to the clock's
   total acceleration, and a clock at rest has acceleration grad Phi whatever holds it up. So a standing clock carries
   the full law for every real source inside it, and the pressure belongs to the clock's dust part. VSH1's force law
   lets pressure hold the clock while the polarization stays equal to the charge that arrived; the two agree only at
   zero pressure (sympy, residual 0).
3. **Under S-seed (VSH1's own infall)** the real hot charge is 0.69 to 0.86 M_b inside the standing region, 1 to 7 % of
   the baryons' law halo there. The law's halo is polarization. It is neutralised by a layer of -16 to -89 M_b at the
   shock, where the field drops by 9.8 to 54 to 0.02 to 0.14 of the law. That is HE1's wall, and SMF1 S0e says nothing
   holds the layer. Inside, the hot charge within 10 r_M (0.13 to 0.71 M_b) lifts the cold-to-baryon ratio X above the
   law's by 0.03 / 0.09 to 0.10 / 0.13 dex: over SHP1's 0.10 line at log M_b 11.5 only, by 0.03 dex.
4. **Under S-cosmo (the dust clustering as dust, as form B's cosmology needs)** the shock holds a real hot halo of the
   host mass, 5.4 M_b or 23 to 82 M_b, and (A) puts the law's phantom on top of it. The cold-to-baryon ratio X at 10 r_M is 1.7 to 4.8
   times the law's (0.23 to 0.68 dex over, line 0.10). That is HY1's failure. It already fails with no primordial
   perturbation at all (0.11 to 0.22 dex).
5. **The temperature is virial, not the law's**: under S-seed and the cosmic-share bracket sigma^4 falls 0.6 to 2.7 dex
   below G M_b a0/4, scales as M_b^1.33 to M_b^1.53, and does not change with a0 between the footings (d ln sigma^4 / d ln a0 = 0.000 to 0.008 against 1).
6. **The Bullet (estimate):** at nu_F the hot charge has a Knudsen number of 0.004 on a cluster core. It is a fluid; it
   shocks with the gas, which is RB1's failing arm M4.

**The lead's hand expectation, checked.** The label is the one expected. Three details differ:
- Under S-seed the miscount is marginal and at one mass only (0.135 / 0.127 dex against 0.10 at log M_b 11.5; 9 and 10.5
  pass at 0.036 / 0.032 and 0.099 / 0.091). With that mass inside the line the label would read STANDS WITH A WALL. Both
  failures are present; the wall is the robust one under S-seed.
- The real charge is 1.0 to 6.9 % of the baryons' law halo at the edge (expected 1 to 3 %).
- Under S-cosmo the hot halo is 5.4 M_b on the cosmic-share bracket and 82 / 23 / 537 M_b on the abundance-matching
  bracket (expected 30 to 100); both brackets fail.
My own pre-freeze expectation (S-seed passes G3) was wrong at 11.5.

## G1 standing (graded at 10.5; `vsj1_grade.out`)

| footing | log M_b | N | R_sh (kpc) | r_e* | S inside r_e* (line 0.10) | SETTLED | shock past r_e* at z | VSH1's R_sh, S |
|---|---|---|---|---|---|---|---|---|
| canonical | 9 | 600 | 154.0 | 7.2 | 4.0e-5 | yes | 4.98 | 153.9, 4.0e-5 |
| canonical | 10.5 | 600 | 410.5 | 40.5 | 2.1e-5 | **yes** | 3.45 | 410.3, 2.2e-5 |
| canonical | 11.5 | 300 | 839.2 | 127.9 | 2.8e-4 | yes | 1.51 | 836.6, 1.7e-4 (N 600) |
| alt | 9 | 600 | 154.0 | 6.5 | 3.2e-5 | yes | 4.98 | 153.9, 3.2e-5 |
| alt | 10.5 | 600 | 410.5 | 36.8 | 1.6e-5 | **yes** | 3.65 | 410.3, 1.6e-5 |
| alt | 11.5 | 300 | 839.2 | 116.4 | 1.7e-4 | yes | 1.70 | 836.5, 1.3e-4 (N 600) |

This lane's stepping is a two-stage predictor-corrector with nodes and velocities at the same time level; VSH1's is a
staggered single stage. The spatial scheme, the viscous operator and the shock-capture coefficients are the model's
and are the same. **G1 PASS / PASS.** VSH1 is reproduced.

## G2 what gravitates (`vsj1_g2.out`, sympy; every residual 0)

| step | statement |
|---|---|
| a | A static clock (tau = t) has A_r = d_r ln N and no other component. No other field enters: this is kinematics |
| b | E2 on the leaves, K W'(K\|P\|) = \|A\|, gives K P = (1 - mu) A with mu(x) = x/(1 + x) |
| c | E3's charge rho_Q = div P + n_hot in E4's Poisson equation gives div[mu grad Phi] = 4 pi G (rho_b + n_hot); a hot static dust n_d(depth, s) (AKS1 T5h) is in hydrostatic balance in that total field |
| d | The polarization charge inside R is R^2 (g - g_N)/G. Where the clock goes from rest to free fall P drops to zero, and a layer of minus that charge sits there (SMF1 S0b, AKS1 T4) |
| e | VSH1's force law at rest, U(y) - y = g_Nb - f with f the pressure acceleration, equals (A)'s U(y_A) - y_A = g_N(real sources) only at f = 0. With pressure support VSH1's polarization is below (A)'s |

**G2 PASS.** So inside the standing region mu(g/a0) g = G [M_b + M_hot(<r)]/r^2: the gravitating density is the baryons,
the real hot charge, and the law's phantom of both. Outside it the field is Newton's of what is inside. G3 and G4 use
this. The collapse itself was run in VSH1's force law (S-seed) or as self-gravitating dust (S-cosmo), not in (A) with
P tied to the total acceleration; see Limits.

## G3 amount and no second halo (max |log10(X_tot / X_L)| over 1 to 10 r_M; line 0.10; canonical / alt)

| supply | log M_b 9 | 10.5 | 11.5 | gate |
|---|---|---|---|---|
| **S-seed** | 0.036 / 0.032 | 0.099 / 0.091 | **0.135 / 0.127** | **FAIL / FAIL** (at 11.5) |
| hot charge inside 10 r_M (M_b) | 0.152 / 0.134 | 0.482 / 0.437 | 0.713 / 0.660 | |
| **S-cosmo H1** (5.41 M_b; achieved 5.36) | **0.243 / 0.227** | **0.329 / 0.315** | **0.384 / 0.371** | **FAIL / FAIL** |
| hot charge inside 10 r_M (M_b) | 1.64 / 1.49 | 2.73 / 2.54 | 3.65 / 3.42 | |
| **S-cosmo H2** (PD1's table: 83.9 / 23.7 / 537 M_b; achieved 82.0, alt 79.7 / 22.8 / 289) | **0.678 / 0.661** | **0.546 / 0.532** | not tuned (289 M_b: 1.37 / 1.33, reported) | **FAIL / FAIL** (decided at 9 and 10.5) |
| hot charge inside 10 r_M (M_b) | 13.7 / 12.8 | 7.83 / 7.37 | | |

- The worst point is x = 10 in every tuned row: the hot charge inside r grows with r.
- X_tot at 10 r_M against the law's 9.51: S-seed 10.3 / 11.9 / 13.0; H1 16.6 / 20.3 / 23.0; H2 45.4 / 33.5 (canonical).
- **H2 at log M_b 11.5 is not graded.** The host target is 537 M_b. The nearest run (A = 46) holds 289 M_b, outside the
  10 % rule, and a run at about twice that amplitude would take over two hours. It is not needed: H2's G3 is decided by
  the other two masses. Reported at 289 M_b: 1.37 / 1.33 dex.
- Reported, S-seed with all the settled charge moved to the centre (upper bound; the hot charge was not re-settled in
  (A)'s deeper field): 0.35 / 0.41 / 0.40 dex. FAIL at every mass. So S-seed's passes at 9 and 10.5 are not robust.
- Reported, VSH1's own force law read literally (no polarization beyond the charge): X at 10 r_M is 0.15 / 0.48 / 0.71
  against 9.51, 1.2 to 2.3 dex below the law. In that reading the settled state carries no law at all.
- Reported, S-cosmo with no primordial perturbation (A = 0; host 1.78 M_b), canonical: 0.110 / 0.174 / 0.217. FAIL.
- Real charge inside the standing region against the baryons' law halo there: S-seed 0.011 / 0.042 / 0.069 (alt 0.010 /
  0.038 / 0.063); H1 0.106 / 0.190 / 0.281; H2 0.69 / 0.55.

## G4 wall (at the edge of the standing region; PASS iff the jump is at most 0.10 dex; canonical, alt in brackets)

| supply | log M_b | R_st (kpc; in r_M) | jump J = g_in / g_out | polarization layer (M_b) | g_out / the baryons' law | HE1's reason applies |
|---|---|---|---|---|---|---|
| S-seed | 9 | 76.5 (62.7) | 48.7 (53.5) | -80.6 (-88.7) | 0.027 (0.024) | yes |
| S-seed | 10.5 | 144.2 (21.0) | 15.9 (17.5) | -27.7 (-30.6) | 0.086 (0.079) | yes |
| S-seed | 11.5 | 275.1 (12.7) | 9.85 (10.8) | -16.3 (-18.0) | 0.140 (0.128) | yes |
| S-cosmo H1 | 9 | 62.4 (51.1) | 20.8 (22.8) | -126 (-139) | 0.123 (0.112) | yes |
| S-cosmo H1 | 10.5 | 197.2 (28.7) | 11.9 (13.0) | -69.4 (-76.6) | 0.218 (0.198) | yes |
| S-cosmo H1 | 11.5 | 424.9 (19.6) | 8.28 (9.05) | -46.3 (-51.2) | 0.317 (0.289) | yes |
| S-cosmo H2 | 9 | 145.9 (119.6) [alt 126.2] | 13.6 (13.2) | -1049 (-982) | 0.69 (0.71) | no: the edge is beyond the middle window |
| S-cosmo H2 | 10.5 | 287.5 (41.9) | 9.10 (9.95) | -193 (-213) | 0.56 (0.51) | yes |
| S-cosmo H2, 289 M_b (not graded) | 11.5 | 1151 (53.0) | 3.65 (3.96) | -770 (-859) | 5.4 (4.9) | no: g_out is above the law |

**G4 FAIL / FAIL under every supply.** The smallest graded jump is 8.3 (0.92 dex) against a line of 0.10 dex. Under
S-seed and H1 the field outside the wall is 0.02 to 0.32 of the law for the baryons, inside the KiDS middle window,
where HE1's late-type stacks sit near 1.5 of it.

## G5 reach (the edge against AKS1's cap and FLD1's KiDS window edges; factor = radius / R_st, PASS iff all three <= 1)

| supply | log M_b | cap | KiDS inner | KiDS middle | |
|---|---|---|---|---|---|
| S-seed | 9 / 10.5 / 11.5 | x0.96 / 2.85 / 4.73 (alt 0.87 / 2.60 / 4.31) | x0.67 / 2.00 / 3.31 | x1.57 / 4.68 / 7.75 | **FAIL** |
| S-cosmo H1 | 9 / 10.5 / 11.5 | x1.17 / 2.09 / 3.06 (alt 1.07 / 1.90 / 2.79) | x0.82 / 1.46 / 2.14 | x1.92 / 3.42 / 5.02 | **FAIL** |
| S-cosmo H2 | 9 / 10.5 | x0.50 / 1.43 (alt 0.53 / 1.30) | x0.35 / 1.00 (alt 0.41 / 1.00) | x0.82 / 2.35 (alt 0.95 / 2.35) | **FAIL** (9 passes; 10.5 fails) |

The standing region ends at 1.32 / 0.56 / 0.47 of the run's turnaround radius under S-seed (at log M_b 9 the viscous
flow is slow out to beyond turnaround) and at 0.34 to 0.47 R_ta under S-cosmo, where FLD1 put the fold (0.52). The shock
does not extend the reach.

## G6 temperature (reported; inside R_st; canonical, alt in brackets)

| supply | log M_b | sigma (km/s) | log10 sigma^4 / (G M_b a0/4) | sigma^2 / virial |
|---|---|---|---|---|
| S-seed | 9 / 10.5 / 11.5 | 9.3 / 36.3 / 83.8 | -2.63 / -1.75 / -1.30 (-2.71 / -1.83 / -1.38) | 0.71 / 0.76 / 0.78 |
| S-seed, inside r_e* | 9 / 10.5 / 11.5 | 20.5 / 57.1 / 110.6 | -1.25 / -0.97 / -0.82 (-1.27 / -0.97 / -0.82) | 0.89 / 0.91 / 0.87 |
| S-cosmo H1 | 9 / 10.5 / 11.5 | 18.4 / 58.3 / 125.7 | -1.43 / -0.93 / -0.59 (-1.51 / -1.01 / -0.68) | 0.93 |

d ln sigma^4 / d ln M_b: 1.53 (S-seed), 1.33 (H1; exact, by the run's scaling). The law needs 1 +- 0.1 and CFG461's
virial classes give 4/3. d ln sigma^4 / d ln a0 between the footings: +0.0002 / +0.0039 / +0.0085 (S-seed), +0.0006 (H1),
against 1. **Not tied to the law.** This is CFG461's c-test again: a shock sets the virial temperature of what fell in.

## G7 Bullet (ESTIMATE)

Kn = 3 nu_F / (sigma L) = 0.0043 with nu_F 141.9 / 142.0 kpc km/s, sigma 1000 km/s, L 100 kpc (round numbers,
PROVISIONAL; the conversion nu = lambda sigma / 3 is kinetic theory's). At nu = 0 the state is an ideal fluid. Either way
the hot charge is collisional on cluster scales, more so than the cluster's own gas. It shocks and lags with the gas.
RB1 gate 4 needs the cold component on the galaxies; its arm M4 (cold on the gas) is class FAIL. **Fails, as an
estimate.** No collision was computed.

## The frozen edge (reported; `S-seed, frozen R_st` rows of `vsj1_grade.out`)

With the criteria's cumulative statistic the S-seed edge is 109 / 403 / 872 kpc, beyond the turnaround radius (58 / 260 /
588 kpc). G3 is unchanged (0.036 / 0.099 / 0.135: FAIL). G4 fails harder (J 64.7 / 38.7 / 26.5; alt 71.1 / 42.5 / 29.1).
G5 fails (cap x0.67 / 1.02 / 1.49, inner x0.47 / 0.71 / 1.04, middle x1.10 / 1.67 / 2.45). The A1-tuned S-cosmo runs hold
8.11 (H1) and 112.7 / 33.2 M_b (H2) inside the frozen edge, outside the 10 % rule, so S-cosmo is not decided as frozen.
The A = 0 run holds 2.94 M_b inside the frozen edge and already fails G3, so an amplitude tuned to 5.41 M_b under the
frozen edge lies between two failing runs.

## Known answers and MUTATE (`vsj1_grade.out`, `vsj1_MUTATE.out`)

| item | result |
|---|---|
| KA1 Noh, this lane's stepping | PASS: shock 0.2055 (0.2000), post-shock density 59.9 (64), energy 1.0e-7 |
| KA2 fluid terms off against FLD1's R_ta | PASS: 87.7 (88) and 597.0 (600) |
| KA3 SIS identities, the law's closed form (sympy) | PASS: residual 0 |
| KA4 EdS self-similar collisional infall | PASS: shock at 0.382 R_ta (0.339, +12.6 %, line 15 %); density slope -2.35 (-2.25, line 0.25) |
| KA5 resolution, 10.5 canonical, N 300 against 600 | PASS: both SETTLED; R_st 141.4 / 144.2; M_hot(<10 r_M) 0.4815 / 0.4818 M_b |
| KA6 zero hot charge | PASS: 1.4e-16 |
| M1 heat removed (10.5 canonical, N 300) | BITES: zones tangle at step 425 (z 7.2); not SETTLED |
| M2 hot charge set to zero in G3 | BITES: S-cosmo's G3 passes on both brackets |
| M3 law off for the standing clock | BITES: G4 passes (J = 1); S-seed's G3 fails at every mass (2.31 / 1.47 / 1.22 dex; alt 2.39 / 1.53 / 1.28), where 9 and 10.5 passed |

M3's G3 half is read per mass: the S-seed gate already fails in the primary at 11.5, so the gate-level outcome could not
flip. KA4's reference value is from memory (PROVISIONAL) and the pass is inside the line by 2.4 points.

## What it means for the joint

VSH1 found the first route in which the fold ends in a standing clock. Graded against the record's conditions
(`THEORY_ASSEMBLED_2026-11-10.md` section 4), that state meets conditions 1 and 2 and the first half of 3 (it acts where the
flow folds, the clock stands, the infall energy is kept as heat) and fails the rest:
- **Condition 3, second half (the law's dispersion).** The heat kept is the virial heat of what fell in (G6).
- **Condition 4 (the charge).** With the charge FLD1's infall supplies, the law's halo is polarization with no charge
  behind it, closed by a negative layer (Gauss). With the charge cosmology supplies, the charge is real, hot, and
  additional to the law's phantom, not instead of it. In neither case is the halo "the charge itself, counted once".
  The two supplies fail in opposite directions, and the abundance-matching bracket shows the second failure grows with
  the host mass.
- **Condition 5 (reach).** The shock sits at about half the turnaround radius, where FLD1 put the fold.
- The Bullet adds a miss that does not depend on the supply (estimate).

Named, not run: a state in which the hot charge is exactly the law's phantom needs sigma^4 = G M_b a0/4 at every mass,
which a shock does not give (G6), and a supply of 12 to 62 M_b inside 13 to 63 r_M, which neither infall model gives.

## Hypotheses and limits

- **The collapse was not run in (A) kept whole.** S-seed uses VSH1's force law (FLD1's shell equation plus fluid terms);
  S-cosmo uses Newtonian dust with the law term off. G2 is a statement about the static end state. With P tied to the
  total acceleration during the collapse, and with the phantom's gravity acting on the hot charge, the hot charge would
  sit deeper; the "all charge at the centre" row bounds that for S-seed and fails. A dynamical (A) run with a pressured
  dust part is not on the record.
- **S-cosmo's perturbation** is a point-seed tail capped at overdensity 0.3 at z 30, one amplitude per host mass. Real
  peaks, mergers and non-spherical infall are absent. The host ratio is read at a zone edge: A 7.1 gives 82.0 M_b inside 0.47 R_ta and
  A 7.7 gives 79.7 M_b inside 0.34 R_ta, so the edge radius is uncertain by tens of per cent while the charge inside it
  moves by 3 %. S-cosmo uses nu = 0 so that one run serves every
  mass; VSH1 found the settling independent of the viscosity.
- **Abundance matching** equates PD1's table share (Moster halo mass times the cold fraction, with M_* = M_b) with the
  charge inside the standing region. It is a bracket. At log M_b 11.5 it asks for a cluster-size host and was not tuned.
- Spherical symmetry; a regular centre; no cooling; baryons a softened point mass switched on over 1 Gyr.
- The log M_b 11.5 S-seed runs are N 300 (frozen). KA5 shows the graded quantity does not move with N at 10.5.
- nu_F, r_e* and R_cap are AKS1's (`aks1_t.json`); the KiDS edges are FLD1's rule on `cfg110_perlens.npz`.
- G7 is an estimate. No Lean file: G2 is sympy only.
- Not re-run by anyone else.

## Files

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`; `vsj1_hydro.py` (solver; modes ka1, ka2, ka4, seed, cosmo) -> `runs/*.json`
(summaries and z = 0 profiles); `vsj1_g2.py` -> `vsj1_g2.json` / `.out`; `vsj1_cosmo.py` (grid, select) ->
`vsj1_cosmo_tune.json`, `vsj1_cosmo_select.out`; `vsj1_grade.py` -> `vsj1_grade.json` / `.out` and, with `mutate`, `vsj1_MUTATE.json` / `.out`.
Re-run: `python3 vsj1_hydro.py ka1`, `ka2`, `ka4`; `seed <footing> <logMb> <N>` for the six runs (N 600, 600, 300),
`seed canonical 10.5 300` and `seed canonical 10.5 300 _M1 0`; `cosmo canonical <A>` for A 0, 0.31, 1, 1.9, 7.1, 46 and
`cosmo alt <A>` for 0.31, 1.9, 7.7, 46; then `python3 vsj1_g2.py`, `python3 vsj1_cosmo.py select`,
`python3 vsj1_grade.py`, `python3 vsj1_grade.py mutate`. One thread per run, nice 10, under 0.2 GB each; 4 to 30 minutes
per S-seed run, 25 to 100 minutes per S-cosmo run. Nothing downloaded.

Commits (local / origin; pushed by replay onto origin/main, 9866eebdff..c7a234b426):

| commit | local | origin |
|---|---|---|
| criteria, alone | 5a13c296ea | 6dd438834d |
| AMENDMENT A1, alone (post hoc) | 5f0b3f379e | 1be4f0e291 |
| scripts, runs, outputs, RESULT.md | 42ad7ef2c9 | c7a234b426 |
| this table | the commit that adds it | its replay, the last VSJ1 commit on origin |

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
