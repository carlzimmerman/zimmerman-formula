# CFG363 FROZEN CRITERIA: the lensing kill test of the two-level retention picture

Committed alone, before any script. kappa = 1/2 FITTED and fixed. nu_mono. No dark-matter particle species: the cold MASS is
still required and is kept. No knob scans (the brackets below are declared physical ranges, each reported, never tuned).
Owner (2026-10-06, in the chat "Nobel Prize and neutrinos"): "run the lensing kill test here". The orchestrator was told
that this chat is running option (a).

**Question (cm10's named kill test).** cold_mass cm08-cm10 measured two retention levels for the cold fluid: r = 0.13 of
the cosmic share in galaxies and 0.60 in group/cluster hosts, with a step at host M200m 1e12-1e13 Msun and late sorting
(z <~ 2). So 75-81% of the cold mass must sit outside halo apertures today. Is that compatible with (i) the CMB-lensing
amplitude and (ii) cosmic-shear S8?

## Scaffold (declared; the same one cm10 used)
- colossus planck18: linear P(k, z), Tinker+08 mass function and Tinker+10 bias (M200m), diemer19 concentrations, NFW.
  This is a LCDM scaffold for halo abundance, NOT the framework's own growth (L341: the chassis fails sigma8). This lane
  therefore tests the REDISTRIBUTION plus the PHANTOM on a fixed halo population, nothing more.
- Halo model for the LENSING density contrast, with mass grid 1e8-1e16 Msun/h:
  P = P_1h + P_2h, where P_2h = [I_b(k)]^2 P_lin and I_b = sum over halos of b n M_lens u(k)/rho_m, plus a consistency
  remainder (1 - integral of b n M/rho_m), identical in both models.
- **LCDM reference:** halo lensing profile = M u_NFW.
- **Two-level model, z < z_sort:** each halo's profile is
  (f_b + r(M) f_c) M u_NFW  (baryons + retained cold)
  + (1 - r(M)) f_c M u_G(k; R_s)  (the moved cold, a Gaussian envelope of comoving width R_s around its host; mass conserved)
  + PHANTOM M_ph u_ph(k).
  r(M) = 0.13 below M_step, 0.60 above.
- **z >= z_sort:** r = 1 (not yet sorted); the phantom is still on.
- **Phantom (the framework's own, baryon-sourced):** for baryons M_b = f_b M treated as a point mass,
  M_ph(<r) = (nu_mono(y) - 1) M_b with y = G M_b/(r^2 a0), truncated at r_sw (the switch-ON region). The mean is absorbed
  into the background (the CFG359 convention). a0 is flat, canonical footing.
- **Brackets (each reported, never pooled, never tuned):** M_step in {1e12, 1e13} Msun; R_s in {1, 3, 10} comoving Mpc;
  z_sort in {1, 2}; r_sw in {1, 3} x R200m; phantom {ON (framework), OFF (pure redistribution, cm10's literal question)}.

## Observables
- **CMB lensing:** Limber C_L^kk to z* = 1100. Statistic: mean ratio (model/LCDM) over L = 40-763 (the ACT DR6 baseline
  range). Anchor: the measured lensing amplitude agrees with Planck LCDM to ~2-3%.
- **Cosmic shear:** Limber C_l for n(z) proportional to z^2 exp(-(z/0.5)^1.5) (median ~0.8). Statistic: mean ratio over
  l = 150-1500, mapped to S8_eff = S8_ref x ratio^(1/2.5), with S8_ref from the scaffold. Exponent 2.0 and 3.0 reported.
  Anchor: DES Y3 0.776 +- 0.017 and KiDS-Legacy 0.815 +- 0.02.

## Tests
**T0 (controls).**
- T0a: the LCDM halo model's 2-halo term reproduces P_lin at k = 0.01 h/Mpc to 3%.
- T0b: the two-level model with r = 1 and the phantom OFF equals LCDM to 1e-6.
- T0c: per-halo real mass is conserved: the profile masses (phantom excluded) sum to M, to 1e-6.
- T0d: LCDM C_L^kk at L = 100 lies within 1e-7 to 3e-7 (order-of-magnitude sanity check, stated as such).

**T1 (CMB lensing).** PASS if the mean ratio is within +-5%. KILL-CMB if it is off by more than 10%.

**T2 (shear).** PASS if S8_eff lies in [0.74, 0.85]. KILL-SHEAR if it lies outside [0.70, 0.89].

## Verdict classes (declared)
- **KILLED:** with the phantom ON, EVERY bracket hits KILL-CMB or KILL-SHEAR.
- **SURVIVES (scaffold):** at least one phantom-ON bracket passes both T1 and T2. Name the brackets.
- **TENSION:** neither of the above.
- The phantom-OFF rows are reported as cm10's literal question; they do not set the verdict, because the framework always
  has the phantom.
- A KILLED or a SURVIVES here is a scaffold result. The framework-native test is CFG359/CFG361's PM machinery. Say so.

**MUTATE.** Drop the moved cold mass instead of placing it in the envelope: T0c must FAIL, rc = 1.

Local compute only. No downloads.
