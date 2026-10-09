# CFG564 FROZEN CRITERIA: SAGA DR3 satellite kinematics, interloper-aware (the PRIMARY rerun of CFG562)

Committed alone, before any script is written and before any number from SAGA Table C2 is computed. What has been seen before
freezing: everything in CFG562 (its README, criteria, script, outputs: the data dispersions sit 10-60 km/s above every model;
a fitted uniform interloper fraction 0.21-0.38 makes all models agree within Delta(-2lnL) <= 4.2), the byte-by-byte header of
SAGA DR3 Table C2 and its first ~25 rows (to read the format), and the C1 header (columns HRV, Dist, DistMod, nz-total).
No sideband count, no interloper density and no likelihood with a fixed interloper fraction has been computed.

kappa = 1/2 is FITTED. Both a0 footings are run and never pooled: canonical 9.3603e-11, alt 1.1312e-10 m/s^2. Kernel nu_mono
(CFG4_common). No dark-matter particle: the framework's cold mass is required and its amount is free. The verdict concerns this
one observable; nothing here can say "theory closed" or "the data favour the framework over LCDM".

## Data
- C1 (101 hosts) and C3 (378 satellites): CFG562's copies (CFG562_saga_satellite_dispersion/data/), sha256 checked.
- C2 (SAGA DR3 redshift catalogue, 10.8 MB, owner approved for this lane): https://sagasurvey.org/data/saga-dr3-tableC2.txt,
  stored in campaign_fresh_gravity/_external_data/cfg564/ (git-ignored), sha256 in FETCH_LOG.md and checked by the script.
- Satellites exactly as CFG562: every C3 entry with 30 <= Rhost < 300 kpc, all three samples; Gold+Silver reported.
- Models, baryons, Jeans solver, tracer profile (power law fitted to the stacked radii, CFG562's gamma_t), r_t = 1 Mpc,
  eps = 20 km/s velocity error, the |dv| < 275 km/s hard truncation: all copied unchanged from CFG562.

## Interloper estimate (PRIMARY: flat velocity sideband)
- For every C2 object with a measured redshift (z > 0): its host from HOSTID; projected R = Dist x angular separation (small
  angle, kpc); dv = c (z - z_h) / (1 + z_h), z_h = HRV / c. Fallback, used only if control K1 fails for this formula:
  dv = c z - HRV. (The first that passes K1 is used for everything.)
- Magnitude matching: an object counts only if its absolute magnitude at the host distance, rmag - DistMod_host, lies inside
  the range [min, max] of the same quantity over the primary satellite sample (C3 rmag - host DistMod).
- Sideband: 30 <= R < 300 kpc and 275 <= |dv| < 1000 km/s (total width 1450 km/s). Interlopers are assumed flat in velocity
  across the window and the sideband, and uniform in projected area (their counts in each radial bin are taken directly).
- Expected interlopers in CFG562's radial bin k (30-60, 60-110, 110-190, 190-300 kpc), stacked over all 101 hosts:
  n_int,k = N_side,k x 550 / 1450. Observed window members n_obs,k = primary satellites in bin k.
  f_int,k = min(n_int,k / n_obs,k, 0.9). f_int(R) is piecewise constant on the four bins.
- Interloper velocity pdf inside the window: uniform, 1/550 per km/s.

## Likelihood (unbinned)
Per satellite j (host h, bin k): L_j = (1 - f_int,k) TG(v_j; s_h(R_j)) + f_int,k / 550, where TG is the Gaussian truncated to
|v| < 275 km/s with s^2 = sigma_los,model,h(R_j)^2 + eps^2. -2lnL = -2 sum_j ln L_j. Zero free parameters per model.
Models per footing: (a) law; (b) supply edge f_ret 0.18 and 0.10; (c) NFW Moster+13 + Dutton-Maccio; (c') NFW at Lim+17
halo masses (reported). Isotropic primary; beta = 0.3 reported.

## Verdict (per footing, fixed f_int, primary)
Comparison set S = {law, edge f_ret 0.18, NFW Moster}. Delta = -2lnL(model) - min over S.
- LAW-FLAT: the law has the minimum over S and both others have Delta > 9.
- SUPPLY EDGE (f_ret 0.18): the edge has the minimum and both others have Delta > 9.
- NFW-PREFERRED: NFW has the minimum and both others have Delta > 9.
- NON-DISCRIMINATING otherwise.
Edge 0.10 is NOT in S: inside r_edge it is identical to the law and CFG562 showed SAGA cannot separate it (Delta ~ 1.5-2.4 in
chi2); it and NFW-Lim are reported with their Delta. Edge 0.18 and NFW are known to be nearly degenerate (CFG562 MUTATE); a
SUPPLY EDGE or NFW-PREFERRED outcome is read together with the injection confusion matrix.

## Power (stated BEFORE scoring; stage 1 committed before stage 2 runs)
Stage 1 (`--stage power`) uses only satellite positions, hosts and f_int,k (no satellite velocities). Per footing, 300 mock
catalogues for each generator in {law, edge 0.18, edge 0.10, NFW}: model velocity draws (truncated, eps), then each satellite
replaced with probability f_int,k by a uniform draw in |v| < 275. Each mock is scored with the primary likelihood and verdict
rule. Reported: median Delta for every pair, and the verdict confusion matrix (fraction of each verdict per generator).
Stage 1 output is committed before stage 2 (`--stage score`) is run. Rule: if a generator's mocks return its own verdict in
< 50% of cases, a data verdict naming that model (or excluding it) is labelled LOW-POWER in the README.

## Reported (not verdict inputs)
- Free interloper fraction: (i) constant f fitted per model on [0, 0.6] step 0.001 (CFG562's procedure); (ii) the primary shape
  scaled, A x f_int,k, A on [0, 1/max f_int,k], with its Delta table and fitted A per model.
- Sideband 275-2000 km/s; sloped sideband: an exponential n(|v|) proportional to exp(-|v|/v_s) fitted by unbinned MLE to the
  stacked sideband objects with 275 <= |dv| < 3000 km/s (v_s grid 100-20000 km/s), extrapolated into the window for both the
  count and the in-window pdf (if v_s hits the grid top it equals the flat case).
- beta = 0.3; Gold+Silver; NFW-Lim; mock goodness of fit (fraction of the best model's mocks with -2lnL above the data).
- Poisson uncertainty of N_side,k.

## Controls
- K0: sha256 of C1, C2, C3.
- K1 geometry: C2 entries with sample > 0 matched to C3 by OBJID; >= 99% of C3 satellites found; recomputed R and dv agree with
  C3 Rhost and DVhost to median |dR| < 1 kpc and median |d dv| < 2 km/s.
- K2 reproduce CFG562: the constant free-f fit reproduces CFG562's committed -2lnL_mix (within 0.05) and f_int (within 0.002)
  for every model it reported.
- K3 injection-recovery (canonical, from stage 1 mocks): for each generator in {law, edge 0.18, NFW} its own model has the
  lowest median -2lnL over S; the shape scale A fitted on 50 law mocks has median in [0.8, 1.2].
- MUTATE (`--mutate`, separate outputs): data velocities replaced by NFW-Moster draws, then each satellite replaced with
  probability f_int,k by a uniform interloper; full primary pipeline. It must NOT return LAW-FLAT (canonical); the script exits 1
  when it does not (detected), 0 when it returns LAW-FLAT (failed control, kept and reported).
- A failed control is kept and reported; a failed K1 for both dv formulas stops the lane (verdict not issued).

## Departures already declared
- Interlopers are taken flat in velocity across +-1000 km/s and uniform within a radial bin; correlated (2-halo) structure would
  make the true in-window density higher than the flat sideband estimate (the sloped variant reports the size of this).
- f_int is stacked over hosts (no host-mass dependence) and the tracer profile is not corrected for interlopers.
- The magnitude matching uses the host distance for sideband objects (they lie within ~14 Mpc of the host).
