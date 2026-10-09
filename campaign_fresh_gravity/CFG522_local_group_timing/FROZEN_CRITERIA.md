# CFG522 FROZEN CRITERIA: the Local Group timing miss (CFG515 (d)): mechanism, data error, or genuine tension?

Frozen 2026-10-09, committed alone before any CFG522 script exists.
κ = ½ is FITTED. Footings 9.36e-11 / 1.13e-10 m/s² are never pooled; every number is reported per footing. a0 is flat (w = −1).
Kernel ν_mono(y) = 1/(1 − exp(−√y)). Candidate B: law switched off outside bound halos; cold energy (Ω_c/Ω_b = 5.364) settles
into the phantom profile up to the census edge r_edge = r_M / ln(1 + f_ret f_b/(1 − f_b)). The cold energy's mass is still
required. Nothing here closes the theory. No downloads: every external number below is a published value recalled from the
literature and is marked PROVISIONAL (not re-verified against the paper in this lane).

## 0. The miss being explained (CFG515 committed outputs)
CFG515 (d), census f_ret (MW 0.100, M31 0.136, CFG416 `fret_of` solved per object): totals 3.28e12 / 4.86e12 Msun, predicted
LG radial velocity −168.7 km/s vs −109.3 ± 4.4 (van der Marel+12), z = +13.5 on both footings (measurement error only).
f_ret = 1 gives z = −22.8. Post hoc common f_ret needed 0.206.

Pre-freeze disclosure (dated 2026-10-09): before freezing I made hand estimates that (i) the census turnaround spheres of the MW
and of M31 (CFG416 Δ_ta = 11.806, Ω_m 0.315, h 0.674) have radii ~1.2–1.4 Mpc, i.e. larger than the 780 kpc separation, and
(ii) `fret_census` on the combined MW+M31 baryons lands near 0.17 (close to the 0.18 bracket that gave z +3.1 in CFG515).
I also estimated that the LMC barycentre correction makes the observed approach slower (worse for heavy masses). The rules
below were written knowing these rough numbers; none of the pass thresholds were tuned to them (they are CFG515's |z| ≤ 3 and
CFG433 D ≤ 3, unchanged).

## 1. Inputs (frozen)
- Baryons as CFG515: MW 6.0e10 (L172 shapes; variant 7.3e10), M31 1.2e11 point mass. Profiles from CFG513's `Prof` class read-only.
- Timing integrator: CFG513/515's `coll_time` (radial, with Λ term Ω_Λ H0² d), t0 = 13.80 Gyr, D = 780 kpc.
- Observed: v_r = −109.3 ± 4.4 km/s, v_tan = 17.0 km/s (vdM12, 1σ upper 34.3); distance 770 ± 40 kpc (vdM12).
- PROVISIONAL literature values for the data re-check:
  - M31 heliocentric v = −301 ± 1 km/s, (l, b) = (121.17°, −21.57°) (vdM12);
  - vdM12 solar motion: R0 8.29 kpc, V0 239 km/s, (U, V, W)_⊙ = (11.1, 12.24, 7.25) km/s;
  - modern solar motion: R0 8.178 kpc (GRAVITY 2019) or 8.277 (GRAVITY 2022), Sgr A* proper motion 6.411 mas/yr (Reid &
    Brunthaler 2020) giving V_φ,⊙ = 4.74047 R0 μ, with the same U, W;
  - M31 distance alternatives: 785 ± 25 (McConnachie 2012), 761 ± 11 (Li+21 Cepheids), 752 ± 27 (Riess+12);
  - M31 transverse velocity: 17 (vdM12), 57 (+35/−31) (vdM19, Gaia DR2), 82.4 ± 31.2 km/s (Salomon+21, Gaia EDR3);
  - LMC: Galactocentric position (−1, −41, −28) kpc, velocity (−57, −226, 221) km/s (Kallivayalil+13), mass 1.38e11 (Erkal+19);
  - M33: (l, b) = (133.61°, −31.33°), heliocentric v = −180 km/s, baryons ~ 8e9 (stars + gas, Corbelli+14 class).

## 2. Data re-check items (each with its rule)
- D1 v_r re-derivation: recompute the Galactocentric radial velocity of M31 along the GC→M31 line from −301 km/s with (a) the
  vdM12 solar motion and (b) the modern solar motion (both R0). Control K5: (a) must reproduce −109.3 within 1.5 km/s.
  DATA ISSUE in v_r iff (b) differs from −109.3 by more than 4.4 km/s in the direction that reduces the census miss.
- D2 distance: census-individual timing at 752, 761, 770, 785, 730 (vdM12 −1σ) and 810 kpc. DATA ISSUE iff any value within its
  own quoted 1σ gives census |z| ≤ 3 (measurement-only error).
- D3 tangential motion: non-radial two-body timing (2-D orbit, Λ, first pericentre in the past at t = t0 ago; the radial
  integrator is the v_tan = 0 limit, control K4 within 0.5 km/s). Census-individual v_r prediction at v_tan = 17, 34.3, 57, 82.4,
  113.6. DATA ISSUE iff the census |z| ≤ 3 at Salomon+21's central 82.4 km/s.
- D4 LMC barycentre: v_r of M31 relative to the MW+LMC barycentre = −109.3 − f (v_LMC · n̂), f = M_LMC/M_MW,tot, M_LMC = 1.38e11
  counted as part of the MW's present total (no extra mass added under the census). Reported per model; it enters the
  robustness rule in section 5.
- D5 M33 barycentre (reported only, radial projection only): v_r → −109.3 + f33 (v_GSR,M33 − v_GSR,M31), f33 from the census
  masses (M33 baryons 8e9 with its own census f_ret).
- D6 inputs to the census: report M_ta, f_ret and the census turnaround radius R_ta for MW, M31 and the MW+M31 pair; state
  whether M31's 0.136 is a ramp value of `fret_of` (it is reported, not judged).

## 3. Mechanisms (each derived, no new knob; each with a pass rule)
- M1 SHARED CATCHMENT. Precondition (computed): the census turnaround radius of each object,
  R_ta = [3 M_ta / (4π Δ_ta ρ̄_m)]^(1/3) with CFG416's constants, exceeds D_LG = 780 kpc for at least one of MW, M31. If so, the
  two census catchments are the same Lagrangian region and the census must be applied once to the pair: f_LG =
  `fret_census`(M_b,MW + M_b,M31), with each object's cold energy 5.364 M_b,i / f_LG and its own edge at f_LG. If the
  precondition fails, M1 is NOT APPLICABLE. PASS iff |z| ≤ 3 (measurement-only, radial, as CFG515) AND CFG433 D ≤ 3 on BOTH
  footings at primary baryons. Satellite unbound count is reported (CFG515 reported it too). The 7.3e10 variant and the
  +M33/+LMC-baryons variant (M_b,LG + 8e9 + 3e9) are reported.
- M2 EXTENDED-BODY MUTUAL FORCE. The CFG513 integrator uses a_rel = G[M_MW(<d) + M31(<d)]/d². For overlapping extended bodies
  the exact rigid-body relative acceleration is a_rel = F(d)(1/M_1 + 1/M_2), F(d) = ∫ρ_1(x) g_2(x − d) dV (2-D quadrature,
  control K3: two well-separated profiles reproduce G M1 M2/d² within 1e-3). Applied to census-individual masses and to M1.
  PASS (as a mechanism on its own) iff census-individual |z| ≤ 3 on both footings.
- M3 LAW BETWEEN THE PAIR. (a) Reported reference, not candidate B: baryons-only two-body timing with the law on between the
  pair, EFE-free, a0 flat: a_rel = ν_mono(g_N/a0) g_N, g_N = G M_b,LG/d² (test-mass form), and the deep-MOND two-body form
  a_rel = (2/3)√(G a0)[M^{3/2} − m1^{3/2} − m2^{3/2}] M/(m1 m2 d) (reported). (b) Under candidate B, a bound pair's phantom IS
  the settled cold energy, so law-on-plus-cold-energy is double counting: it is used as MUTATE T2 below, not as a mechanism.
- M4 TIME DEPENDENCE. a0(z) is flat for w = −1, so the a0 term in the timing is time-independent (identity, stated). The
  settling history of cold energy is not in the record, so a growing mass M(t) cannot be derived: SCOPE statement only. One
  reported-only bracket (no verdict weight, not a knob fitted to anything): M_cold(t) ∝ t/t0 for the census-individual case,
  to give the sign and size.

## 4. MUTATE controls (CFG522_MUTATE=1, separate outputs; each must FAIL the timing, |z| > 3 on both footings)
- T1 M31 total mass × 0.3 (baryons and cold energy) at the M1 f_LG.
- T2 law-on between the halos added to M1's Newtonian total-mass force (a_rel = ν_mono(g/a0) g with g the M1 total-mass force).
- T3 double-counted supply: each object assigned the full LG supply 5.364 M_b,LG / f_LG.

## 5. Statistics and verdict (frozen)
- z_meas = (|v_pred| − 109.3)/4.4 at v_tan = 0 (CFG515's strict statistic).
- z_full = (v_pred(v_tan = 82.4) − v_obs)/σ_full, σ_full² = 4.4² + σ_D² + σ_vt², with σ_D and σ_vt the half-differences of
  v_pred at D = 770 ± 40 and v_tan = 82.4 ± 31.2 (finite differences through the same timing model). v_obs = −109.3.
  z_full,LMC: same with v_obs corrected by D4 for that model's MW total.
- Verdict, first rule that applies:
  1. DATA-ISSUE: census-individual |z_full| ≤ 3 AND |z_full,LMC| ≤ 3 on both footings, or D1/D2 trigger.
  2. MECHANISM FOUND: M1 (or M2) passes its strict rule (section 3) AND its |z_full,LMC| ≤ 3 on both footings AND every MUTATE
     T1–T3 fails.
  3. MECHANISM FOUND, CONDITIONAL ON THE MEASURED TANGENTIAL MOTION: M1 fails strict but |z_full| ≤ 3 AND |z_full,LMC| ≤ 3 on both
     footings, MUTATEs fail.
  4. NOT DIAGNOSTIC: census-individual AND f_ret = 1 both have |z_full| ≤ 3 (the timing cannot separate them).
  5. GENUINE TENSION: none of the above; quote z_meas, z_full and z_full,LMC for census-individual and for M1.
- Controls (load-bearing): K1 CFG515 census v −168.7 and f_ret = 1 z −22.8 reproduced within 0.5 km/s / 0.3;
  K2 point-mass Λ = 0 radial timing reproduces the Kepler (Kahn–Woltjer) mass from the analytic cycloid within 0.5%;
  K3, K4, K5 as above.
- Compute: nice -n 10, ≤ 2 threads. Numbers in the README come from the results JSON.
