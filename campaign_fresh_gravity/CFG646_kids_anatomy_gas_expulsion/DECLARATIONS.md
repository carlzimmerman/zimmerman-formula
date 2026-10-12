# CFG646 declarations (committed alone, before any CFG646 code or number)

Lane: (i) the anatomy of CFG596's raw-KiDS exclusion; (ii) the framework's OWN gas expulsion, which the PM omits.
Date 2026-10-12. kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy MASS still required; no
particle species; not "theory closed". Nothing here changes CFG596's verdict (canonical KiDS EXCLUDED, DES NOT DIAGNOSTIC,
alt PENDING). Parts (i) and (ii) are POST-HOC DIAGNOSTICS and ESTIMATES. They carry no verdict.

## (i) Anatomy (post hoc, no verdict change)

- Inputs: CFG596's committed runs and scripts only (cfg596_native.py, CFG592 library exec'd unchanged, the P0/P1 run JSONs).
  No new statistic, data cut, nuisance or prior.
- Reproduction gate A0: the script must reproduce CFG596's canonical dchi2 (KiDS +68.73, DES +22.37) to |d| <= 0.05,
  else the anatomy is not reported.
- Decompositions (all reported):
  1. per-point split of each best-fit chi2_data, c_i = r_i (C^-1 r)_i (sums exactly to chi2_data); dchi2 per point =
     c_i(F) - c_i(S0); prior difference reported separately. Grouped by xi+ / xi-, angular bin, tomographic pair.
  2. fixed-nuisance version (F evaluated at S0's best-fit nuisances), same grouping.
  3. k sampling of each kept point: fractions of its absolute integrand (S0 spectrum, nominal nuisances, no IA; the
     support-mask construction) in k bins [<0.3, 0.3-1, 1-2, >2] h/Mpc and its median k; dchi2 grouped by median k.
  4. k-swap refits (same fit routine): framework spectrum below k_c and S0 above, and the reverse, k_c = 0.3, 0.5, 1, 2.
- Headline: the share of +68.7 carried by k > 1 vs k < 1 (from 4, with 1 and 3 as cross-checks), stated with the
  non-uniqueness of any split of a correlated chi2 disclosed.

## (ii) Framework-native gas expulsion (estimate only)

- The framework's census (CFG416/515 fret_of, verbatim) retains M_b = f_ret f_b M_ta per catchment. The non-retained
  baryons (1 - f_ret) f_b M_ta are, in the framework, NOT in the halo.
- PRIMARY placement (declared from the record): CFG632's PRIMARY DIFF, the census gas the raw FRB DMs accepted:
  non-retained baryons are diffuse, present only in the two-halo term, with the large-scale bias that conserves mass
  (CFG632 overlap rule b_d; total bias 1 on large scales).
- Brackets: SHELL (CFG632 bracket, rho ~ r^-2 between r_edge and r_ta); DIFF-U (uniform, bias 0: the maximal-removal
  extreme); and, for the "from" side, the omitted baryons following NFW (primary) or the framework's own total profile.
- Estimate 1 (halo model, CFG556 machinery, both footings): Delta P / P at k 0.3 / 0.5 / 1 / 2 h/Mpc at z = 0.
  Tinker08 / Tinker10 / NFW-Duffy08 are CONTEXT-ONLY ingredients, used only inside a ratio, never as a yardstick.
- Estimate 2 (PM-native post-process): on CFG596 P1's own 256^3 block means (z = 0, 0.5, 1), the engine's own catchment
  routines (cover_peaks / cover_balls, RMIN 0.78125, census f_ret code) rebuilt at 256^3; the gravitating field
  delta_grav' = delta_grav - f_b (1 - f_ret(x)) (1 + delta_part) + (re-placed mass per variant). Resolution-limited
  (catchments rebuilt on a 4x coarser mesh) and disclosed as such. Alt footing: the same post-process on CFG530's
  L100 N512 LRalt / LRcan fields (no 1024^3 alt run exists).
- Propagation: the ratio P'/P (per node z where available, else held from z = 0) multiplies the framework's measured
  P_grav in cfg596_native.py's own projection and fit; dchi2' = chi2(F') - chi2(S0) and chi2(F') with its p on the raw
  data are reported as an ESTIMATE, not a verdict.
- Plain statement required: whether expulsion could plausibly remove the 19-25% excess at k 0.3-1, or only a few %.
  If it is negligible, that is said.

## (iii) A FROZEN CRITERIA + PM spec for a native run with expulsion is written after (ii), committed alone, and not run
at >= 256^3 in this lane.
