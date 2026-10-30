# MF1_h2_cooling_floor_mass — FROZEN CRITERIA (committed alone, before any script or graded number)

**Question.** PC1's post-hoc scan found M200 = max(EM1 relation, M_f) reproduces all five X49 dwarf classes at lg M_f = 6.25–7.00, with
M_f fitted. Can M_f be derived? Hypothesis: a galaxy exists only if its halo's core is deep enough for primordial gas to cool, so
M_f is the mass of the smallest floor halo whose gas cools by molecular hydrogen. No parameter is tuned to the window.

Standing rules: kappa = 1/2 FITTED. Footings never pooled (9.3603e-11 / 1.1312e-10 m/s^2). Route E, Newtonian. Cold dark energy, not
matter; no particle species. Native background only (F3 A_c2b_refit, as X49); no LCDM halo mass function or merger tree. Not "theory
closed". Nothing may say the data favour the framework.

## 0. Seen before freezing (disclosed: this lane is NOT blind)

- The target window is known, as are all PC1 Z values.
- A rough chat estimate: T = 1000–2000 K through a floor halo's peak speed gives lg M_f ~ 6.3–6.9, inside the window; T = 1e4 K gives
  ~8.2. The idea was chosen after seeing this. **A landing here is therefore a consistency, not a blind prediction.** The chat estimate
  assumed T; this lane computes T from chemistry instead, and that step is what can fail.
- CFG934 / CFG937 tested atomic-cooling floors under the law with standard virial speeds: PARTIAL, FRAGILE. DF1 listed "cooling floor"
  as closed under its brief. This lane differs in three ways: route E (no law), the depth is the floor core's own peak speed, and the
  coolant is H2. Atomic cooling is carried as the tooth below.
- Formula provenance, read from TeX on 2026-10-30: Tegmark+1997 (astro-ph/9603007) k_rec = 1.88e-10 T^-0.64, k_m = 1.83e-18 T^0.88 cm^3/s;
  Galli & Palla 1998 (astro-ph/9803315) low-density H2 cooling polynomial. Residual ionisation is Peebles' x0 = 1.2e-5 sqrt(Om)/(Ob h),
  from memory, checked by K2.

## 1. Derivation (primary)

1. Gas at redshift z: hydrogen density n = 0.76 x 178 x rho_b(z) / m_p, from the native omega_b. Age budget t = 1/H(z), native flat background.
2. H2 fraction, Tegmark's closed form: x_H2 = (k_m / k_rec) ln(1 + x0 n k_rec t).
3. Cooling time t_cool = 1.5 k T / (x_H2 n Lambda_GP(T)).
4. **T_crit(z)** = lowest T in [100, 1e4] K with t_cool <= t. No collisional dissociation or Lyman-Werner background (limits, §5).
5. Depth: V^2 = 2 k T_crit / (mu m_p), mu = 1.22 (neutral primordial). Floor halo: V_peak^2 = 0.254484 a0 x 0.9634 r0 (X47 / PC1), which gives r0.
6. **M_f** = the z = 0 M200 of a floor Burkert halo with that r0, via X49's convention (200 rho_c(0), compact branch).

**z is not derived.** Primary z = 15; band z = 10, 15, 25. Reasons: UFD stars are ancient and the first cooling is before reionization; 15 is
a mid value chosen a priori, not by scanning. Later growth raises M200, so M_f is a lower bound on present M200.

## 2. Tests

- **Regrade:** X49's rows exactly, with M200 = max(EM1 relation, M_f(z=15)) per footing. Same bootstrap (10000 resamples, seed 20261026), per
  class median E and Z, |Z| < 2 = reproduced.
- **Tooth:** same regrade with T = 1e4 K (atomic) in place of T_crit. Reported; if atomic also reproduces all five, the test has no power and
  the verdict becomes NOT DIAGNOSTIC.

## 3. Verdict (per footing; footings separate)

- **CONSISTENT, BAND-STABLE:** all five classes reproduced at z = 15, and lg M_f within [6.25, 7.00] at z = 10, 15, 25.
- **CONSISTENT, z-DEPENDENT:** all five reproduced at z = 15, but the band leaves the window.
- **MISS:** any class not reproduced at z = 15. Reported then with the T that would have been needed.
- NOT DIAGNOSTIC per §2's tooth.

## 4. Reported only (no verdict)

- Standard virial speed V200(z) at the same M_f: what T does it imply? This shows how much the result depends on using the core's depth.
- Variant density: n from the core itself, 0.76 (Ob/Om) rho0 / m_p, solved self-consistently with r0.
- a0 lower by 7% (CFG689), and T thresholds 1000 and 2000 K fixed by hand.
- Spearman(E, lg M*) after the regrade (X49: -0.64).
- Systems individually above the prediction by > 2 s; Draco.
- Requested forecast: starless floor lumps below M_f, and the minimum V_peak of any luminous system.

## 5. Checks

K1: Lambda_GP(1000 K) = 10^-24.24 (polynomial evaluated by hand). K2: x0 within 1.5e-4–3e-4. K3: Tegmark's rates reproduce x_H2 by direct ODE
integration to 5% at one (T, n, t). K4: reproduces PC1 post-hoc Z(MW ultra-faint) at lg M_f = 6.50 to 0.15 (+0.51 / +0.02; different resample count).
K5: the r0 -> M200 round trip to 1e-3. MUTATE (`--mutate`): Lambda / 1000 must raise T_crit and shift lg M_f by > 0.25; exit 1 if not. Own outputs `_MUTATE`.

## 6. Limits named now

- **The floor core must already exist when the gas cools.** Floor cores are denser than collapse density at these masses, and the floor has no
  mechanism; X81 found native 1e12 halos are cusps; X80 is queued. If not in place, step 5's depth is wrong.
- Lyman-Werner feedback, streaming velocity, HD cooling and metals are not modelled. Lyman-Werner would raise the threshold.
- Baryons are assumed to reach the cold sector's fair density. The gas pressure and Jeans filter are not treated.
- A selection floor says which halos host stars, not why their kinematics match; X49's data stay as they are.
- M_f does not explain DF1's shape result (n ~ 0.78); the Spearman report is the only touch on that.
