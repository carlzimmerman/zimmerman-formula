# CFG562 FROZEN CRITERIA: SAGA DR3 stacked satellite velocity dispersion vs the isolated law, the supply-limited law (CFG398 edge) and LCDM NFW

Committed alone, before any script or dispersion is computed. What has been seen before freezing: the SAGA DR3 data page, the
byte-by-byte headers of Tables C1 (hosts) and C3 (satellites), and the first ~25 printed rows of C3 (to read the format).
No dispersion, no radial count and no host-mass distribution was computed or looked at.

kappa = 1/2 is FITTED. Both a0 footings are run and never pooled: canonical 9.3603e-11, alt 1.1312e-10 m/s^2.
Kernel nu_mono (CFG4_common). No dark-matter particle: the framework's cold mass is required and its amount is free.
Verdicts are about this one observable; nothing here can say "theory closed" or "data favour the framework over LCDM".

## Data (owner approved the SAGA fetch for this lane)
- SAGA DR3 (Mao et al. 2024, ApJ 976, 117; Geha et al. 2024), sagasurvey.org/data: Table C1 (101 hosts), Table C3 (378
  satellites), Table C4 (candidates without redshifts; fetched, not used). Logged in FETCH_LOG.md (URL, UTC date, bytes, sha256).
- Host: HOSTID, Dist, log(M*), log(MHI) (may be blank), log(Mhalo) (Lim+17). Satellite: HOSTID, Rhost (projected kpc),
  DVhost (km/s, relative to the host), sample (1 Gold, 2 Silver, 3 Participation).
- Membership = SAGA's own: a satellite is any C3 entry (SAGA's definition: R_proj < 300 kpc, |dv| < 275 km/s). No further
  interloper clipping. The |dv| < 275 km/s window is treated as a hard truncation in every estimator and every mock.
- Primary sample: all three samples (kinematics do not need completeness). Gold+Silver only is REPORTED.
- Radial range 30 <= R < 300 kpc (R < 30 dropped).

## Baryonic mass (declared)
M_b = M* + 1.33 M_HI when log(MHI) is given, else M_b = 1.2 M*. Point-mass baryons (as CFG398). No M_b scatter propagated.

## Models (zero free parameters each, per footing)
Radial acceleration g(r) of an isolated host; external field ignored (declared).
- (a) LAW: g = g_N nu_mono(g_N / a0), g_N = G M_b / r^2. At 30-300 kpc this is the deep regime: flat V_f^4 = G M_b a0 to < few %.
- (b) SUPPLY-LIMITED (CFG398): r_edge solves M_b (nu_mono(y) - 1) = (Omega_c/Omega_b) M_b / f_ret, Omega_c/Omega_b =
  0.1200/0.02237 = 5.364; g = law for r <= r_edge; for r > r_edge g = G M_b [1 + 5.364/f_ret] / r^2 (Keplerian on the full
  supply). f_ret = 0.10 and 0.18 (verdict uses 0.18). Inside r_edge (b) and (a) are IDENTICAL by construction.
- (c) NFW: M200 from inverse Moster+13 (as CFG476: M1 = 10^11.590, N = 0.0351, beta 1.376, gamma 0.608) applied to M*;
  c200 = Dutton-Maccio 2014 (10^(0.905 - 0.101 log10(M200 h / 1e12)), h = 0.7, rho_crit at H0 = 70); NFW extended beyond
  R200 (no truncation); plus the baryon point mass. Reported variant (c'): M200 = SAGA's Lim+17 log(Mhalo).

## Jeans prediction (declared)
- Tracer: 3D nu(r) proportional to r^-gamma_t, with gamma_t fitted ONCE by maximum likelihood to the stacked projected radii of
  the primary sample in [30, 300) kpc, using p(R) proportional to R^(2 - gamma_t) (untruncated power-law projection; declared
  approximation). Tracer extends to r_t = 1 Mpc (sensitivity 0.6 and 3 Mpc REPORTED).
- Spherical Jeans with constant anisotropy: nu sigma_r^2 (r) = r^(-2 beta) int_r^r_t r'^(2 beta) nu g dr'.
  sigma_los^2(R) Sigma(R) = 2 int_R^r_t (1 - beta R^2/r^2) nu sigma_r^2 r dr / sqrt(r^2 - R^2).
  Primary beta = 0 (isotropic); beta = 0.3 REPORTED. Computed per host, numerically.
- Per-object velocity error eps = 20 km/s added in quadrature (SAGA does not tabulate per-object velocity errors; declared).
  Sensitivity eps = 0 and 40 km/s REPORTED.

## Estimator, binning, stacking
- Radial bins (kpc): [30, 60), [60, 110), [110, 190), [190, 300).
- Host-mass bins: two, split at the median host log M_b (of hosts with >= 1 primary satellite in range). 2 x 4 = 8 data points.
  The all-host stack (4 points) is REPORTED.
- Bin estimator: maximum-likelihood sigma of a zero-mean Gaussian of variance s^2 + eps^2 truncated to |v| < 275 km/s
  (bounded scalar search, s in [5, 600] km/s).
- Errors: bootstrap over hosts (resample hosts with replacement, carry their satellites), 1000 draws, seed 562; error = std.
  Primary chi^2 uses diagonal bootstrap errors; full bootstrap covariance chi^2 REPORTED.
- Model bin value: the SAME estimator applied to mock velocities drawn from each model at the actual satellites' hosts and
  projected radii (sigma_los,model(R_i)^2 + eps^2, truncated at 275 km/s), averaged over 200 mock realisations (seed 5620).
  This carries truncation and host-mass mixing exactly.
- Reported (not verdict): unbinned log-likelihood of every satellite velocity per model (zero free parameters), and the same
  with a uniform-in-[-275, 275] interloper component whose global fraction is fitted per model.

## Verdicts (per footing; primary = 8 points, diagonal errors, beta = 0, eps = 20, r_t = 1 Mpc, all samples)
chi^2_X over the 8 bins, dof = 8 (no fitted parameters). Order of evaluation:
1. SUPPLY EDGE SEEN if chi^2_a - chi^2_(b,0.18) > 9.
2. NFW-PREFERRED if chi^2_a - chi^2_c > 9 AND chi^2_(b,0.18) - chi^2_c > 9.
3. LAW-FLAT if p(chi^2_a, 8) > 0.01 AND chi^2_(b,0.18) - chi^2_a > 9 (b disfavoured).
4. else NON-DISCRIMINATING. Then state the power: the forecast Delta chi^2 = sum over bins of (model_b(f) - model_a)^2 / err^2
   on a grid f_ret in [0.05, 1.0]; the smallest f_ret at which the forecast reaches 9 is the "detectable f_ret"
   (larger f_ret = smaller supply = edge further in): SAGA can see the edge only if f_ret >= that value.
Also reported: p-value of every model, chi^2_(b,0.10).
If 1 and 2 both hold, both are stated (no tie-breaking).

## Controls
- K1 reproduce CFG398: our r_edge reproduces CFG398's committed x values (cfg398_supply_edge_results.json) at log M_b
  10/10.5/11/11.5, f_ret 0.07/0.10/0.18, both footings, to relative 1e-6. Also print r_edge at log M_b 10.6 and 11.0 for
  f_ret 0.10 / 0.18 (expected ~370-660 / ~210-370 kpc).
- K2 Jeans solver: for a pure power-law tracer in a log potential (g = V^2/r) with beta = 0 and r_t = 100 Mpc, sigma_los
  at R = 100 kpc must equal V / sqrt(gamma_t) to 1%.
- K3 estimator: on 2000 synthetic draws from a truncated Gaussian sigma 120, eps 20, the estimator returns 120 within 3%.
- K-INJ injection: 20 mock data sets with velocities drawn from (b) at f_ret = 0.18 (canonical footing) at the real positions,
  run through the full binned pipeline (bootstrap errors recomputed per mock, 200 boots to save compute; model bin values reused).
  PASS if the median of chi^2_a - chi^2_(b,0.18) is > 0 AND the fraction of mocks reaching SUPPLY EDGE SEEN agrees with the
  forecast (expected Delta chi^2 >= 9 -> fraction >= 0.5; < 9 -> fraction <= 0.5). Plus a strong injection at f_ret = 1.0
  (edge ~ 75 kpc): PASS if chi^2_(b,1.0) is the smallest of {a, b0.10, b0.18, b1.0, c} in >= 15 of 20 mocks.
- Failed controls are kept and disclosed, never re-tuned silently.

## MUTATE (`--mutate`, separate outputs *_MUTATE*)
Replace every satellite velocity by a draw from model (c) (truncated at 275, eps 20; seed 56299). Run the primary pipeline.
Detected (exit 1) if the canonical-footing verdict is NFW-PREFERRED, or the law is rejected (p(chi^2_a, 8) <= 0.01). If the NFW mock is NOT distinguished
from the law (law and NFW predict similar sigma), MUTATE exits 0 and that is reported as a power statement, not hidden.

## Honesty clauses
- Inside r_edge, settling and the bare law coincide exactly; the test only has leverage where r_edge < ~300 kpc in 3D
  (projected satellites at R sample r >= R).
- No result here measures a0, and none measures f_ret except as a bound if the edge is excluded.
- SAGA hosts are MW analogues in group environments; external fields and host-to-host M_b errors are not modelled.
