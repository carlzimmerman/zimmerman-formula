# CFG598 FROZEN CRITERIA -- an anisotropic, self-consistent velocity-relaxation target (FIX-2 successor test)

Committed alone, before any script of this lane exists and before any number of this lane is computed. Date 2026-10-10.
Lane folder: `campaign_fresh_gravity/CFG598_anisotropic_velocity_target/`. Inputs are read only (CFG541, CFG544, CFG550,
CFG554, CFG559 folders; `sol61_push/` is read only and never edited). No PM runs. No downloads. Compute: `nice -n 10`,
<= 4 processes of 1 thread, <= 8 GB.

## Lead and what is being tested

REVIEW_openai_astra_2026-10-10.md (items KINETIC_GATE and streaming_edge). FIX-2's velocity target (CFG544/554/558: OU toward the
ISOTROPIC Jeans dispersion of the current density) is POSITED (CFG554 b; CFG558 ISOTROPY CHOSEN). KINETIC_GATE: an isotropic
f(E) >= 0 has drho/dPhi <= 0, but the exponential-kernel halo around compact baryons RISES outward for r < r_M/q*,
q* coth(q*/2) = 4, so the isotropic target cannot be a stationary kinetic state there. streaming_edge: a tangential
Osipkov-Merritt f(E,L) >= 0 reproduces the truncated law halo exactly for Hernquist b >= r_M (proof) with a SHARP edge
(sigma_r -> 0), but fails for b <= 0.1 r_M (its scout). That contradicts the generality of CFG544's "kinetic support softens
the edge outward by 25-55%". This lane asks whether a DERIVED anisotropic target exists that is self-consistent at all radii in
compact AND extended systems, whether it keeps the edge sharp, and whether it survives the CFG544 bench.

## Settings

kappa = 1/2 FITTED; footings 9.3603e-11 (can) and 1.1312e-10 (alt), judged separately, never pooled. Kernel: the EXPONENTIAL
RAR form nu(y) = 1/(1 - exp(-sqrt y)) (THEORY_v1 A1 naming note: this is the form CFG541/544/556/597 use, NOT the repaired
nu_mono of the PM lineage; the obstruction of KINETIC_GATE is specific to it). Candidate B; G9 (the cold energy feels real mass
only: baryons + settled cold energy); no EFE; round per-region phantom. The cold energy's MASS is still required. No
dark-matter particle species. Not "theory closed". Energy sink: only the dynamical, non-clustering dark energy (phi partner).
No knobs: alpha (O(1) FREE, CFG541) and tau = (4 pi G rho_m)^(-1/2) as in CFG544; nothing else may be inserted.

## Cells (3 systems x 2 footings = 6)

- MW-like: M_b = 6.0e10 Msun, Hernquist a = 2.5 kpc (b/r_M = 0.26 / 0.29); CFG541 JSON inputs, as CFG544.
- Cluster-like: point mass 1.5e14 Msun; CFG541 JSON inputs, as CFG544.
- Compact-elliptical-like (new): M_b = 1.0e11 Msun, Hernquist a = 1.0 kpc, so b/r_M = 0.082 (can) / 0.090 (alt) <= 0.1.
  f_ret = CFG515 `fret_census(1e11)`, r_ta, M_cat and r_* = `Model.analytic_rstar()` from CFG541's own code (imported read only,
  same definitions as the CFG541 JSON entries), dt = 1e-3 r_*/V_f (the MW value). Its whole-history energy uses CFG541's
  `Model.run(alpha=1)` drift-only release, computed the same way as CFG541's dW_per_mass.
"Hollow cells" = cells whose law profile rho_ph (unsoftened, as the bench's own rho_ph) has drho_ph/dr > 0 somewhere in
(RMIN, r_*); r_pk = the radius of the density maximum; the hollow region is r < r_pk. Determined by the script, reported.

## Q1 -- the target

**Definition (route "ME", declared now).** The target is the maximum-entropy STATIONARY distribution of the law's settled
halo: maximise S[F] = -int F ln F dtau over F(E, L) >= 0 (functions of the isolating integrals of the spherical real-mass
potential Phi_eq = baryons + rho_ph truncated at r_*, i.e. exact Vlasov stationarity by the Jeans theorem), subject to
int F d^3v = rho_ph(r) for r < r_* and = 0 beyond (so only orbits with apocentre <= r_* are populated). No energy constraint
(it is implied by the virial theorem for any exact stationary F reproducing rho_ph; sympy K2) and no isotropy or anisotropy
constraint. The maximiser is F = exp(-1 - <lambda>_orbit) (orbit time-average of a multiplier field), positive everywhere.
This is the exact-kinetic version of CFG554 route (a) (which used only the second-moment tensor constraint and whose maximiser
is not an exact Vlasov steady state, CFG554 S4). Its anisotropy beta(r) is an OUTPUT.

**Numerics.** Orbit library in (r_peri, r_apo), log grid, 2x finer than the constraint bins; phase volume
8 pi^2 L T_r dE dL (cell areas from the (E, L) images of the cell corners); time fractions by theta-quadrature
(r = rbar - Delta cos theta). Constraint bins: 120 log bins. Convex dual solved by damped Newton.
- Part S (exact law, unsoftened, units r_M): r from 0.05 r_M to r_*; all 6 cells.
- Part N (bench field): the toy's softened equilibrium field (EPS = 0.01 r_*), r from RMIN to r_*; all 6 cells.

**Self-consistency (per cell, Parts S and N):** max over bins |M_k,model / M_k - 1| <= 1e-3 (F >= 0 is automatic).
Reported: beta(r), sigma_r^2/sigma_t^2 at the edge, beta in the hollow vs the cusp-slope-anisotropy line gamma/2
(report only), and a fine-grid density reconstruction (report only).

**LP tests (Part S, scipy HiGHS; variables = cell masses >= 0, bin masses exact):**
- ISO: minimise over F the maximum over hollow bins of d_k = |Pi_t,k - 2 Pi_r,k| / (Pi_t,k + 2 Pi_r,k) (bisection);
  "locally isotropic support EXISTS in the hollow" iff d_min <= 0.02. Also reported for the bins r_pk < r < 0.9 r_*.
- MIRROR: the radially biased mirror of the ME target, x' = 1/x with x = sigma_t^2/(2 sigma_r^2) per bin (beta' = 1 - 1/x;
  admissible, beta' < 1), imposed on every bin with |beta_ME| >= 0.05; d'_min defined as above with 2(1 - beta') in place of 2.

**Sympy items (all must pass for DERIVED):**
- K1: stationarity of the discrete Lagrangian gives F_c = exp(-1 - sum_k lambda_k P_ck); dual Hessian is a Gram matrix (PSD);
  S strictly concave (unique maximiser).
- K2: integrating r^3 x the anisotropic radial Jeans equation with P_r(r_*) = 0 gives 2K = int rho r g dV for every beta(r)
  (energy constraint redundant).
- K3: for orbits with r_apo <= R, v_r^2 <= 2[Phi_eff(R) - Phi_eff(r)] -> 0 linearly as r -> R, so sigma_r -> 0 at the edge
  while sigma_t stays finite (the target's edge is sharp by construction).
- K4: re-verification of KINETIC_GATE: d ln rho/d ln r = -4 + q coth(q/2) for the point-mass exponential-kernel phantom;
  q* in (3, 4); isotropic drho/dPhi = -2 pi sqrt2 int f/sqrt(E - Phi) dE <= 0.
- K5: relaxation operator structure (below): local mass exact; d KL(f || n F_hat)/dt <= 0; log-mean factorisation
  C = -Lambda ln(f/(n F_hat)), Lambda >= 0; the energy exchanged equals int (v^2/2) C and is closed only with the phi partner
  (without it, M.dE != 0).
- K6 (numeric): a bin-wise momentum-shifted variant of the resampling conserves total J on a rotating-shell test to <= 1e-12
  (relative); the plain resampling is reported for contrast. The spherical bench has J = 0 and runs the plain operator.

## Bench (CFG544 toy imported unchanged, through CFG554's module)

N = 30000, EPS = 0.01 r_*, RMIN = 1e-3 r_*, 100 bins, seed 544, dt per system, Vlasov integrator, two-sided drift (FIX-1),
energy accounting; only the velocity step changes.

**FIX-A (primary operator).** BGK relaxation at rate gamma = alpha/tau (tau as CFG544's local value) toward n_c F_hat(v | r)
inside r_*: each particle inside r_* is resampled with probability 1 - exp(-gamma dt). The new velocity is drawn from the
ME target's conditional at its radius: an orbit cell is drawn with weight = its target mass in the particle's constraint bin;
(r_peri, r_apo) is jittered inside the cell and clamped to bracket r; (v_r, v_t) follow from the turning-point relations in
the CURRENT real-mass field (G9). At the fixed point (rho_c = rho_ph) this is exactly F_hat; off it, it keeps the target's
orbit-shape distribution (declared continuation; no constant). Particles at r >= r_* get no velocity relaxation.
**FIX-AG (secondary, reported, no label):** anisotropic Gaussian OU with the ME target's sigma_r^2(r), sigma_t^2(r) (Part N),
inside r_*. It separates "anisotropy" from "the target's bounded orbit support".
**FIX-2 (comparator = forced isotropy):** CFG544's operator unchanged (CFG554 route b).

**Runs:** FIX-A at alpha = 0.5, 1, 2: IC-B and IC-C, 13.8 Gyr each, all 6 cells (the alpha = 1 gate is read at 10 Gyr (IC-B)
and 5 Gyr (IC-C) from the same runs; identical RNG sequence). FIX-AG and FIX-2: alpha = 1, IC-B 10 Gyr, IC-C 5 Gyr, 6 cells.
Overfill pair (FIX-A, 5 Gyr): IC-F (positions from rho_ph, velocities from the target conditional) and IC-F + 0.3 M_ph(<0.3 r_*)
(rho_ph-shaped, target velocities). Control C2': IC-F under pure Vlasov, 2 Gyr.

**Diagnostics:** CFG554's G550 (|D| <= 0.1, |log10 X_J| <= 0.1 at the end, both changed <= 0.05 dex over the last 2 Gyr);
CFG544's gate alongside; edge ln(r_99/r_99,analytic); beta in the shell; energy (CFG554 definitions); blow-up (CFG554
definition); hollow ratio H = log10[<M_c(RMIN < r < r_pk)> / M_ph(RMIN < r < r_pk)], time-averaged over the last 2 Gyr
(sampled every 10 steps), with its Poisson error sigma_H from the mean count (hollow cells only).
**HOLLOW HELD** iff |H| <= 0.15 + 2 sigma_H.

## Labels

- **Target ANISOTROPIC TARGET DERIVED** iff: the ME maximiser is self-consistent in all 6 cells (Parts S and N); K1-K5 pass;
  FIX-A passes G550 at alpha = 1 on IC-B and IC-C in all 6 cells; no blow-up; energy COMPATIBLE (CFG554 definition: IC-B net in
  [0, 1.0], IC-C whole-history net in [0, 1.0] V_f^2 per M_cat); HOLLOW HELD in every hollow cell (IC-B and IC-C). Each other
  failed item (edge, overfill, alpha, Lyapunov, angular momentum) is listed as OPEN with the label.
  Stated with it: the selection principle (maximum entropy over exact Vlasov steady states at the law's density) is of the same
  class as CFG554 route (a), accepted there as "from a principle"; the orbit-shape continuation only acts off the fixed point.
- **POSITED** iff the bench passes but the target needed an inserted assumption beyond the principle above.
- **INCONSISTENT** iff the maximiser fails self-consistency in any cell, or FIX-A fails G550 (alpha = 1) in any cell, or blows
  up, or energy is not COMPATIBLE, or the hollow is not held in a hollow cell.
- **Edge SHARP** iff |ln(r_99/r_99,analytic)| <= 0.1 for FIX-A at alpha = 1 on IC-B (10 Gyr) and IC-C (5 Gyr) in all 6 cells;
  else **SOFTENED** (amounts reported against FIX-2's on the same bench).
- **Works in compact systems YES** iff in the compact-elliptical AND cluster cells (both footings) FIX-A passes G550 (alpha = 1,
  IC-B and IC-C), the hollow is held and nothing blows up; else **NO**.
- **Overfill HANDLED** iff P (CFG544 definition, 5 Gyr, FIX-A) <= 0.2 in all 6 cells; else NOT HANDLED.
- **alpha-ROBUST** iff for alpha in {0.5, 1, 2}, IC-B and IC-C, all 6 cells, at the snapshot nearest 13.8 Gyr:
  |log10 X_J| <= 0.05, |D| <= 0.05, both changed <= 0.05 dex over the preceding 2 Gyr, and |ln(r_99/r_99,analytic)| <= 0.1;
  else NOT alpha-ROBUST (the CFG558 edge allowance C2_cell + 0.1 is reported alongside for the MW and cluster cells).
- **Full-system Lyapunov:** NOT ESTABLISHED unless proven (not attempted beyond CFG554's argument); the largest rise of the
  drift functional F along the runs is reported.

## Q2 -- edge and KiDS (context only; no new KiDS fit)

If the edge is SHARP, the settled profile is the law's sharp profile, i.e. CFG559's MK0 (kinetic support off). The KiDS
consequence is then read from `CFG559_kinetic_settled_profile/cfg559_kids_results.json` (sharp chi^2 A/B, inner-9 and outer-6,
both footings) and CFG559's kinetic gain is withdrawn under this target. If SOFTENED, the measured softening is reported
against CFG559's and its KiDS direction stated qualitatively. CFG529 construction A/B enters only through those numbers. The
inner-bin shortfall is reported from the same JSON; the bench's inner profile (D in the shell, H in the hollow) says whether
the anisotropic target changes it.

## Controls (all must pass, else no label)

- CS (solver): harmonic field g = r, rho = exp(-r^2/2), edge R = 5 (isothermal, for which the ME maximiser is exactly
  F ~ exp(-E), isotropic): sigma_r^2 and sigma_t^2/2 within 2% of 1 for r <= 3, bin masses <= 1e-3.
- C2': IC-F under pure Vlasov for 2 Gyr passes the end gate (|D| <= 0.1, |log10 X_J| <= 0.1) in all 6 cells (edge reported).
- C4: M_ph(<r_*) of the toy equals M_cat to 1e-4 (reported per cell; the CFG544 precedent applies if it misses at 1e-4 level).
- C5: FIX-2 IC-C 5 Gyr end state (log X, D) reproduces CFG544's JSON to 1e-6 in the 4 inherited cells.
- Mass exact in every run.

## MUTATE (`CFG598_MUTATE=1`, writes `_MUTATE` outputs; exit 1 iff all teeth bite)

- **MI (forcing isotropy reproduces the compact-system failure):** bites iff (a) the LP ISO test gives d_min >= 0.1 in every
  hollow cell (Part S), AND (b) FIX-2 (forced isotropy, alpha = 1, read from the main run) has edge ln(r_99/r_99,an) > 0.1 in all
  6 cells (CFG544/554's softening) AND H >= +0.3 in every hollow cell (IC-B or IC-C).
- **MF (flip beta to radial bias):** bites iff the LP MIRROR test gives d'_min >= 0.05 in every hollow cell, AND the bench arm
  "FIX-AG with the mirrored ratio, total dispersion kept" (IC-C, 5 Gyr) fails G550, or edge SHARP, or HOLLOW HELD, in every cell.
- **MT (target hot):** FIX-A with resampled velocities x sqrt2 (sigma^2 x 2), IC-C 5 Gyr: must fail G550 in all 6 cells.

## Reporting

Scripts, `.out` / `_MUTATE.out`, results JSON, README (numbers read from the JSON). Dated disclosures for anything changed
after this freeze; this text is never edited. Commit results with message "CFG598 results: ...", lane folder only, specific
paths; no push.
