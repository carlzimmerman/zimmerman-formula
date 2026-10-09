# CFG522: the Local Group timing miss. Verdict DATA-ISSUE (assumption): most of CFG515's +13.5σ came from a radial orbit and a measurement-only error. Shared catchment (M1) is a derived mechanism that closes the remainder, but it still fails the strict radial statistic (z +4.4)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (d38a869bc). It includes a dated disclosure of hand estimates made before freezing.
- **Script:** `cfg522_lg_timing.py`. It writes `cfg522_lg_timing.out` and `cfg522_results.json`, and with `CFG522_MUTATE=1` it writes the `*_MUTATE.*` files. Run the MUTATE pass first, because the verdict needs its teeth. It takes about 1 minute at nice 10 with 2 threads.
- **Settings:** κ = ½ is FITTED. The two footings are never pooled; the cold-energy timing numbers agree across footings to within 0.03σ (the baryons-only M3 numbers differ). a0 is flat. The cold energy's mass is still required. This is not "theory closed", and nothing here says the data favour the framework.
- **Literature values:** recalled, not re-fetched. They are marked PROVISIONAL, and nothing was downloaded.

## Controls (5/5 pass)
- **K1:** the fast integrator reproduces CFG515: census −168.68 / −168.82 km/s, and f_ret = 1 gives z −22.82.
- **K2:** with Λ = 0 the radial integrator matches the Kepler cycloid exactly (mass error +0.000%).
- **K3:** the mutual-force quadrature gives G M1 M2/d² to 7e-6 at 20 Mpc.
- **K4:** the 2-D integrator at v_tan = 0.5 km/s equals the radial one (−168.68).
- **K5:** the vdM12 solar motion gives −110.2 km/s, against the published −109.3.

## Data re-check
| item | result | data issue? |
|---|---|---|
| D1: v_r re-derived from −301 km/s | vdM12 solar motion −110.2; modern (R0 8.178 / 8.277, Sgr A* 6.411 mas/yr) −112.3 / −110.0. The −109.3 value is sound | no |
| D2: distance 730–810 kpc | census z_meas runs from +17.0 at 730 to +11.5 at 810 | no |
| D3: transverse velocity | census v_r prediction is −167.9 / −160.5 / −151.4 / −134.7 at v_tan = 17 / 57 / 82.4 / 113.6. At Salomon+21's 82.4 alone, z_meas is +9.6 | no, alone |
| D4: LMC barycentre | v_LMC·n̂ = −231.8 km/s, so the MW+LMC barycentre approaches M31 more slowly: v_obs is −99.5 (census MW mass) or −92.9 (M1). This makes heavy masses worse | enters robustness |
| D5: M33 barycentre (reported, radial projection only) | adds +74.3 km/s × f33. With LMC and M33, census v_obs is −93.4 | reported |
| D6: census inputs | MW 0.100 (floor), M31 0.136 (a ramp value; log M_ta 12.58). Census turnaround radii are **1249 / 1421 kpc, larger than the 780 kpc separation** | see M1 |

**The full statistic (frozen).**
- z_full is taken at v_tan = 82.4. Its error σ_full adds 4.4 km/s, the distance error (±40) and the v_tan error (±31.2), each propagated through the same timing model.
- For the census-individual model: σ_full = 19.2 km/s, z_full = **+2.19 / +2.20**, and z_full,LMC = **+2.70 / +2.70**. These are below 3, so the frozen rule 1 returns **DATA-ISSUE**.
- Adding M33 (reported only) gives **+3.01 / +3.02**, right on the threshold. So this verdict is fragile.
- f_ret = 1 has no solution: the pair cannot have turned around at the measured v_tan. So the full statistic still discriminates.

## Mechanisms
- **M1, shared catchment (derived, no knob).**
  - Each galaxy's census turnaround sphere contains the other, so the census must be applied once to the pair.
  - f_LG = `fret_census`(1.8e11) = **0.1704**, which puts 1.95e12 in the MW and 3.90e12 in M31.
  - Strict CFG515 statistic: v −128.5 / −128.6, **z_meas +4.37 / +4.39, which FAILS**. D +2.89 / +2.52 passes, and 4/39 satellites are unbound.
  - Full statistic: z_full −0.11 / −0.10, z_full,LMC +0.64, +M33 +0.98.
  - Variants: M_b,MW = 7.3e10 gives z_meas +5.25. Adding M33 and LMC baryons to the catchment gives +3.61.
- **M2, exact extended-body mutual force.** The acceleration at 780 kpc is 0.977 / 0.992 of the shortcut. Census z_meas goes to +13.13 / +13.29, which is negligible. Not a mechanism.
- **M3, law on between the pair (reference, not candidate B).** Baryons only, with ν_mono and no EFE:
  - test-mass form: −222.6 / −241.5 km/s (z +25.7 / +30.0);
  - deep-MOND two-body form: −178.0 / −194.4 (z +15.6 / +19.3).
  - Plain MOND timing is also too fast.
- **M4, time dependence.** a0 is flat for w = −1, so there is no effect. The settling history of cold energy is not in the record, which is a SCOPE limit. A reported-only bracket with cold mass ∝ t gives z +5.4, the same sign as M1.

## MUTATE (all three teeth fail, as required)
- **T1:** M31 × 0.3 gives z_meas −9.08 / −9.07.
- **T2:** turning the law on between the halos on top of the cold energy gives +168 / +181.
- **T3:** a double-counted supply gives +24.6 / +24.9.

## Verdict: **DATA-ISSUE** (frozen rule 1)
1. **What drove the "+13.5σ".** CFG515's statistic assumed a purely radial orbit and used only the 4.4 km/s error.
   - The Gaia EDR3 transverse velocity of 82 ± 31 km/s lowers the census prediction to −151 km/s.
   - The distance and v_tan errors raise σ to about 19 km/s.
   - Together they leave the census-individual model at +2.2σ (+2.7σ with the LMC barycentre, and about +3.0σ adding M33, which is reported only).
2. **The census itself was being misapplied.** The MW and M31 sit inside each other's census turnaround spheres, so their supplies were counted twice. Applying the census once (M1, f_LG 0.170) cuts the pair's mass from 8.1e12 to 5.9e12 (−28%), with no knob. That removes about 70% of the excess over the ~4.9e12 the radial timing needs (CFG515's post hoc common f_ret of 0.206). It lands at z_full −0.1 (+0.6 with LMC, +1.0 adding M33).
3. **What still fails.** On the strict radial statistic, M1 still misses: z +4.4. M1 is a mechanism *conditional on the measured transverse motion*.
4. **Read this honestly.**
   - Post hoc, the full statistic allows a common f_ret of roughly 0.12–0.30 (canonical, |z_full,LMC| ≤ 3).
   - So the LG timing is a weak discriminator once v_tan is included. It does reject f_ret = 1 and a common f_ret of 0.10.
   - It does not single out the census.

## Dated notes (2026-10-09)
- **Bugs fixed during development, before any result was read for the verdict.** The pericentre event had the wrong sign, so it stopped at the apocentre. K4 caught it: −204 vs −169. Also, mass inside 0.01 kpc was dropped in the shell sum. Both runs were redone.
- **Non-numeric z_full.** When v_pred has no solution at v_tan + 1σ, σ_full and z_full are NaN or ∞. The verdict treats that as a fail, as for f_ret = 1 and T1.
- **K5 approximation.** K5 neglects the transverse-motion term in projecting onto the GC→M31 line. That term is about 1 km/s.
- **Settled masses at all times.** Cold-energy masses are taken as settled at all times, with rigid spherical profiles and point-mass M31 baryons, as in CFG513 and CFG515.
