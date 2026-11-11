# FRZ1R READING (blind re-grade of FRZ1; committed alone, before any FRZ1R script or number)

Re-grades FRZ1's FROZEN_CRITERIA (graded reading L; reading V reported). Opened: FRZ1's criteria, CO1's criteria / A1 / RESULT,
PD1 A1 / A2, CFG556's library (lines 24-215), HLF1's `hlf1_forest.py`. Not opened: FRZ1's RESULT or any frz1_* file, FRZ2.
Own code for R_cold(k, z); the forest gate (`ss1_cosmo.forest_eval`, form B's CLASS reference) is shared machinery, copied from HLF1.

## Ingredients as read
- Cosmology, linear spectrum shape (Eisenstein-Hu no-wiggle, sigma8 0.811), Tinker 2008 / Tinker 2010 settings, mass grid
  1e8-1e16, Moster 2013 stars + beta-model gas (`baryon_cum`), turnaround from the NFW extension at Delta_ta, the spectrum
  formulas (P_std on r200m-truncated NFW; turnaround-scope P with the 2-halo integral normalised by sum W b M_ta / rho_m):
  TAKEN FROM CFG556's CODE (its README does not define them). Re-implemented, not imported.
- At z: P_lin D(z)^2 with D from the flat-LCDM growth integral (Om 0.3138); sigma(M) D; Tinker 2008 z-scaling of A, a, b
  (c fixed); Tinker 2010 bias at nu = 1.686/sigma(M,z); c = Duffy x (1+z)^-1.01; r200m comoving as at z 0; R200c at
  200/Om(z) x comoving mean; Delta_ta(z) = 5.55 + 6.26 Omega_L(z)/Omega_L(0); a0 -> a0/(1+z)^2 in comoving units in r_M
  and the phantom; v_vir^2 = (1+z) G M200c / R200c(comoving); X = 55.716 / 55.731 for z >= 1; FB, baryon shapes as z 0.
- Galaxy regime (v_vir <= v_stiff 265.8 / 288.1): M_b = (1-FB) M_ta / X as a point mass at the centre; cold M_b[m(x)-1] to
  x_t, X M_b beyond; uncondensed baryons (FB M_ta - M_b) in the reference shape M_L/M_ta. Rb: M_b + (M_ta - M_b) M_L/M_ta.
- Cluster regime: CO1 section 3 as written (baryon_cum to M_b,sys = FB M200c at R200c; f_core = 1/2[1-(v_s/v)^2] of
  (1-FB) M200c in NFW truncated at R200c; phantom W M_b(<r)[nu-1], source frozen beyond R200c, capped at E; remainder
  E - M_ph(r_ta) as M proportional to r on [0, r_ta]; reference M_L(r) - M200c added beyond R200c). Rb: baryons +
  (1-FB) M_L inside R200c, reference outside.
- R_tot = 1 + (P_B - P_Lta)/P_std, R_bar = 1 + (P_Rb - P_Lta)/P_std, R_cold = R_tot/R_bar, each at its own z.

## Ambiguities (reading chosen / alternative)
1. **Galaxy phantom past r_ta (new at z: r_M comoving grows as 1+z, so r_t can exceed r_ta).** Chosen: phantom
   M_b[m(x)-1] up to min(r_t, r_ta); the cold mass it leaves unplaced inside r_ta is spread in the reference shape
   (rem x M_L/M_ta, CFG556's own capped-halo rule), so M_ta is held. Alternative (reported): the remainder as a shell at r_ta.
2. Condensed baryons: point mass (CO1's "at the centre") / alt: baryon_cum shape. Point mass used; it cancels mostly in R_cold.
3. Cluster isothermal remainder: M proportional to r from 0 to r_ta (chosen) / from R200c to r_ta (alternative, not run).
4. ZG mapping: R_cold computed at each DESI bin z_i and put in every ZG column (0.02 to ZPK) whose nearest DESI bin is z_i;
   columns below 2.1 get the z 2.2 values (the gate only reads columns at the bins).
5. k outside 1e-3 to 10 h/Mpc: flat at end values (frozen).

## Validation (stops grading if it fails)
- z = 0: R_cold at k 1 / 3 / 5 within 0.02 of CO1's 1.006 / 1.051 / 1.090 (canonical) and 1.010 / 1.088 / 1.159 (alt).
- Gate: R = 1 -> Delta chi^2 0 exactly; CO1's stored z = 0 R_cold held at every bin -> 160.74 / 1025.57 to 0.5.
- M_ta held inside r_ta and layouts non-decreasing (1e-9); D(z) against the EdS-limit sanity D(4.4)(1+4.4) ~ 1.3.

## Mutation (must bite)
- a0 left unscaled in comoving units (no (1+z)^-2) must change R_cold at k 3, z 3 (canonical) by >= 0.005.

## Labels (FRZ1 section 3)
FOREST ROW HOLDS (Delta chi^2 <= 4) / FAILS (> 4) / NO VERDICT (validation or mutation fails), per footing, never pooled.

## Hand estimate (before any number)
At z 3 the galaxy-regime phantom is an isothermal-like profile from a small core (r_M comoving 4x its z 0 value) out to
near r_ta, against a low-concentration NFW (c ~ 2.5-3): more mass at small r and a drained edge, so R_cold - 1 > 0 at
k 3-5, of order +0.02 to +0.10, smaller on canonical than alt. Clusters are absent at z 3. Expected Delta chi^2 tens to
hundreds: FOREST ROW FAILS on both footings likely. Confidence in the sign about 60 %.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
