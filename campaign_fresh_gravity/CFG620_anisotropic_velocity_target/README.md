# CFG620: an anisotropic, self-consistent velocity-relaxation target (FIX-2 successor test)

**Lane ID note (dated 2026-10-11).** The frozen criteria were committed as 93abcbeb6 under the name **CFG598**. A parallel lane
(settling front, criteria dd49c4124) had claimed CFG598 two minutes earlier. This lane was therefore renamed **CFG620** by a
forward move; history was not rewritten. The criteria text in `FROZEN_CRITERIA.md` is unchanged, and it still says "CFG598"
throughout. The folder rename itself was swept into a parallel session's commit 3dcb3a075 (staged rename,
`FROZEN_CRITERIA.md`, 0 lines changed).

**Result.**
- A maximum-entropy, exactly stationary, anisotropic target exists. It is computed with no constant, and it holds the law's
  profile at all radii, including the rising inner "hollow" of compact systems.
- On the CFG544 bench it keeps the hollow filled exactly as the law requires, where isotropic FIX-2 overfills it by a factor of
  2.3 to 2.8. Its end state keeps a sharp edge.
- **As frozen it still fails:**
  - G550 steadiness at the frozen reading times (alpha = 1; 10 Gyr for IC-B, 5 Gyr for IC-C) in 5 of 6 cells;
  - the edge criterion at those times in the cluster cells;
  - overfill;
  - alpha x 0.5.

**Labels:**

| item | label |
|---|---|
| target | INCONSISTENT (as frozen) |
| edge | SOFTENED (as frozen; sharp at 13.8 Gyr for alpha >= 1) |
| works in compact systems | NO (as frozen) |
| overfill | NOT HANDLED |
| alpha | NOT alpha-ROBUST |
| full-system Lyapunov | NOT ESTABLISHED |

The labels are computed with CS read outside the library's inner boundary layer and with C4 read at the toy's resolution (the
CFG544 C4 precedent; see the disclosures). **As frozen: NO LABEL** (CS and C4 fail).

kappa = 1/2 is FITTED. The footings (9.3603e-11 can / 1.1312e-10 alt) are never pooled. The kernel is the **exponential** RAR
form nu(y) = 1/(1 - exp(-sqrt y)) (THEORY_v1 A1 naming), not the repaired nu_mono. The cold energy's mass is still required. No
dark-matter particle. This is not a closed theory. Every number below is read from `cfg620_results.json`,
`cfg620_results_MUTATE.json` or `cfg620_post.json`.

## Files and how to run

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (93abcbeb6, as CFG598).
- **Scripts** (all `OMP_NUM_THREADS=1 nice -n 10`, at most 4 processes):
  - `cfg620.py` is the main run, about 1 h of bench on a shared machine. It writes `cfg620.out` and `cfg620_results.json`.
    `CFG620_MUTATE=1` writes `_MUTATE` outputs and exits 1 only if every tooth bites; it exits 0 here (MI does not bite).
  - `cfg620_lib.py` holds the orbit library, the max-entropy solver, the LP tests and the target sampler.
  - `cfg620_sympy.py` holds K1–K6.
  - `cfg620_post.py` holds the post-run diagnostics D1 and D2. No label depends on them.
- **Inputs (read only):**
  - CFG541 JSON and CFG541's own `Model` (compact cell);
  - CFG544, CFG554 and CFG559 JSON;
  - the CFG544 toy, imported unchanged through CFG554.
- No downloads. No PM.

## Q1: the target

**Definition.** Maximise S = -int F ln F over F(E, L) >= 0 in the law's real-mass field (G9), subject to reproducing rho_ph
(truncated at r_*). The constraints are only the law's density and exact Vlasov stationarity (Jeans theorem). There is no
isotropy constraint and no energy constraint: by K2 the energy is fixed anyway by the virial theorem.
- The maximiser is F = exp(-1 - <lambda>_orbit), positive by construction.
- beta(r) is an output, not an input.
- This is the exact-kinetic version of CFG554 route (a).

**Sympy items (pass).**
- K1: stationarity; the dual Hessian is a Gram matrix; the maximiser is unique.
- K2: 2K = int rho r g dV for any beta.
- K3: sigma_r -> 0 linearly at the edge while sigma_t stays finite.
- K4: the KINETIC_GATE re-verification, with q* = 3.8300.
- K5: BGK mass is exact; the KL divergence decreases; the log-mean factorisation holds; the energy balance closes only with the
  phi partner.
- K6: bin-wise momentum-shifted resampling conserves J to 2.9e-16, against 1.00 lost by the plain operator.

**Part S (exact law, unsoftened, r >= 0.05 r_M).** The maximiser is self-consistent in all 6 cells (bin error <= 6.3e-6).

| cell | hollow (r_pk/r_M) | beta in the hollow (median) | beta in the bulk (median) | sigma_r^2/sigma_t^2 at the edge | LP ISO d_min in the hollow | LP MIRROR d'_min in the hollow |
|---|---|---|---|---|---|---|
| MW can / alt | none (monotone) | — | -0.012 / -0.011 | 0.029 | — | — |
| cluster can / alt | 0.264 | -5.82 | -0.260 | 0.015 | 0.82 | 0.99 |
| compact can | 0.170 | -0.73 | -0.041 | 0.029 | 0.024 | 0.29 |
| compact alt | 0.157 | -0.58 | -0.040 | 0.029 | 0.000 (artefact, D2) | 0.16 |

- **The target is tangential where it has to be.** It is strongly tangential in the point-mass hollow, mildly tangential in the
  compact hollow, nearly isotropic in the bulk, and tangential at the edge (radial pressure goes to 0).
- **The cusp-slope–anisotropy line holds.** No hollow bin violates beta <= gamma/2.
- **Isotropic support of the hollow.** LP ISO (locally isotropic second moments, F >= 0, exact bin masses) is infeasible in
  the cluster hollows at 120 and 240 bins (D2).
  - compact_can is infeasible at 120 and 240 bins, but its bisection d_min is only 0.024 (a beta of about -0.1 suffices).
  - compact_alt reports feasible. D2 shows that the LP solution empties 13 of 61 (120 bins) and 27 of 123 (240 bins) fine
    sub-bins in the hollow, down to -296 dex. It is a binning artefact, not a smooth density.
  - The ME target reproduces the fine grid to within ±0.10 dex.
  - An isotropic f(E) is excluded analytically (KINETIC_GATE, K4).
- **The radial mirror is infeasible in every hollow** (d'_min 0.16–0.99).

**Part N (bench field).** Self-consistent in 5 of 6 cells as frozen. cluster_alt stopped at the frozen 400-step Newton cap with
bin error 1.9e-3 > 1e-3. D1 re-solves it with a higher cap (same code) and reaches 7.6e-8. The moments change by <= 1.9e-3, so
the bench target was effectively the converged one. Disclosed; the label's self-consistency item uses the as-run value.

## Bench (FIX-A = two-sided drift + BGK toward the target at rate alpha/tau)

**Controls.**
- **C2' pure Vlasov from the target:** stationary, as the target should be. ln(r_99/r_99,an) is -0.005 to -0.007 in all 6
  cells, against +0.26 to +0.54 for CFG544's isotropic equilibrium. H is +0.02 to +0.11.
- **C5:** reproduces CFG544 exactly (difference 0).
- **Mass:** exact in every run.

**alpha = 1, read at the frozen times (IC-B 10 Gyr / IC-C 5 Gyr).**

| cell | G550 B / C | failing item | edge B / C (FIX-A) | edge B / C (FIX-2) | H B / C (FIX-A) | H (FIX-2) |
|---|---|---|---|---|---|---|
| MW can | F / F | steady (0.06–0.07 dex) | +0.042 / +0.053 | +0.218 / +0.222 | — | — |
| MW alt | F / F | steady | +0.075 / +0.077 | +0.243 / +0.257 | — | — |
| cluster can | pass / F | steady (C) | **+0.120 / +0.125** | +0.433 / +0.376 | +0.006 / -0.004 (σ 0.04) | +0.44 / +0.41 |
| cluster alt | pass / pass | — | +0.079 / **+0.129** | +0.447 / +0.408 | +0.001 / -0.002 | +0.43 / +0.42 |
| compact can | F / F | steady | +0.069 / +0.078 | +0.237 / +0.238 | +0.03 / -0.02 (σ 0.17–0.18) | +0.37 / +0.37 |
| compact alt | pass / F | steady (C) | +0.086 / +0.086 | +0.244 / +0.246 | -0.01 / +0.02 | +0.38 / +0.38 |

- **End values are close; steadiness is the problem.** |D| <= 0.019 and |log X_J| <= 0.030 everywhere. The failures are only
  that both quantities still change by 0.05–0.07 dex over the preceding 2 Gyr.
- **The edge breathes out and back.** For example, MW can IC-C has r_99 = 0.99 at the start, 1.10 r_* at about 7 Gyr, and
  0.98 from 11 Gyr on.
- **Hollow held in every hollow cell** (|H| <= 0.03). Forced isotropy (FIX-2) overfills the hollow by 10^0.37–10^0.44.
- **No blow-up.**
- **Energy COMPATIBLE:**
  - IC-B net +0.250 to +0.388 V_f^2 per M_cat;
  - IC-C whole history +0.256 to +0.389.

**FIX-AG (Gaussian OU with the target's anisotropic moments; reported, no label).**
- Edges +0.20 to +0.61; hollow H +0.27 / +0.28 (cluster) and +0.005 to +0.047 (compact).
- So anisotropy alone does not give the sharp edge or hold the point-mass hollow. The target's bounded orbit support
  (apocentres <= r_*) does.

**alpha to 13.8 Gyr (gate |log X_J|, |D| <= 0.05, steady, edge |ln| <= 0.1).** 30 of 36 pass.
- alpha = 1 and alpha = 2 pass in every cell and IC. Edges are -0.013 to +0.066; for example, MW can IC-B is +0.066 and every
  cluster cell is <= -0.007.
- alpha = 0.5: IC-C passes, but IC-B fails the edge in all 6 cells (+0.49 to +0.60). MW can IC-B also fails the gate (D -0.051).
- So the end state at alpha >= 1 is a sharp-edged, steady, kinetically supported law halo. The frozen alpha = 1 reading at
  5 and 10 Gyr catches it still breathing.

**Overfill (FIX-A, 5 Gyr):** P = 0.36 / 0.37 (MW), 0.42 / 0.50 (cluster), 0.31 / 0.32 (compact). This is above 0.2: **NOT
HANDLED**. Resampling keeps injected mass on orbits bound inside r_*, so it is the position-sector item CFG554/558 already named.

**Lyapunov:** the largest rise of F along FIX-A runs is 0.013 F_0. NOT ESTABLISHED.

## Q2: edge and KiDS (context; read from CFG559's JSON, no new fit)

- **FIX-A's end state is the law's sharp profile.** That is CFG559's MK0, not its kinetically softened profile. The KiDS
  consequence is CFG559's sharp row:
  - canonical: chi^2 A/B 59.13 / 66.04; inner-9 20.01 / 20.29; outer-6 33.63 / 32.56;
  - alt: 50.44 / 55.50; inner-9 14.22 / 14.43; outer-6 33.88 / 32.75.
  - Against CFG559's isotropic kinetic profile (canonical 57.77 / 63.97, inner-9 19.03 / 19.29), the small kinetic gain is
    withdrawn: chi^2 +1.4 to +2.1, inner-9 +1.0 / +1.4.
  - The median effective edge returns from x_99 0.256 / 0.224 to the sharp values of about 0.196 / 0.169 (CFG559 README). KiDS
    prefers 0.45–0.50, so edge placement (CFG529 construction A/B) moves further from the data, not closer.
- **The inner-bin shortfall is unchanged.** Inside 0.1–0.9 r_*, FIX-A matches the law profile (|D| <= 0.019). In the hollow it
  matches it exactly (H about 0), while FIX-2 overfills it. Anisotropic support therefore keeps compact-system inner profiles
  at the law's value. It neither creates nor fixes inner-bin mass.
- **CFG544's "kinetic support softens the edge by 25–55%" is specific to isotropic (or unbounded-Gaussian) support.** It is not
  a property of kinetic support as such.

## MUTATE (exit 0: not every tooth bites)

- **MI (forcing isotropy reproduces the compact-system failure): does NOT bite as frozen.**
  - (b) bites: FIX-2's edges are +0.22 to +0.45 in all cells, and its hollow H is +0.37 to +0.44 in every hollow cell.
  - (a) fails: the compact LP ISO d_min is 0.024 (can) and 0.000 (alt), both below 0.1. compact_alt's "feasible" isotropic
    moments are a binning artefact (D2). The cluster hollows give 0.82.
  - Read plainly: forced isotropy fails the compact hollow dynamically (factor 2.3 overfill on the bench) and analytically
    (f(E), K4). Locally isotropic *second moments* are only marginally excluded in the shallow compact hollow (b about 0.08 to
    0.09 r_M).
- **MF (radial mirror): bites.** LP d'_min is 0.16 to 0.99 in every hollow. On the bench, every cell fails (edge +0.25 to +0.79;
  cluster hollow overfilled, H +0.37 / +0.38).
- **MT (target hot, sigma^2 x 2): bites.** G550 fails in all 6 cells (log X_J +0.13 to +0.16, D -0.14 to -0.18).

## Disclosures (dated 2026-10-10/11; the frozen text is not edited)

1. **CS fails as frozen.** It deviates by up to 0.99 in the bins next to the library's inner boundary (r < 0.1 = 10 r_lo), where no
   orbit can pass inside r_lo. For 0.1 <= r <= 3 the maximum deviation is 0.0071, within the 2% tolerance. Labels are given
   with CS read outside that layer, following the CFG544 C4 / CFG554 C6 precedent.
2. **C4 misses 1e-4 at the 1e-4 level** (1.0–2.2e-4). This is CFG544's definitional offset, about 100x below toy noise.
3. **Library lower limit (numerical rule set before the bench):**
   - The library starts at max(0.005 r_M, the radius where rho_ph = 1e-9 of its maximum) in Part S, and at max(RMIN, the same)
     in Part N. The convex dual cannot resolve density ratios of about 1e-75 in double precision.
   - The reporting range r >= 0.05 r_M is as frozen.
   - Particles inside the Part N floor (point mass only, mass about 1e-12 M_cat in equilibrium) draw from the first bin.
4. **The frozen text said "Part S: r from 0.05 r_M"**; the library extends lower, as in item 3, to keep its boundary layer out
   of the reported range.
5. **LP numerics.** Unscaled HiGHS with a 60 s time limit per feasibility LP. Six or seven cluster LPs timed out and were counted
   as infeasible, so the cluster d_min of 0.82 is an upper estimate. D2's direct t = 0 LPs are infeasible at 120 and 240 bins.
   The first attempt (without the floor of item 3) stalled and was killed. No number from it is used.
6. **The bench target is fixed,** solved once from rho_ph in the toy's equilibrium field. Off the fixed point, the resampled
   orbit shapes (r_peri, r_apo) are turned into velocities in the *current* field. This continuation is declared in the
   criteria.
7. **The run was restarted after the ID rename.** No number was taken from the earlier partial run.
8. **Toy limits** are as CFG544: spherical; static baryons; 0.05 V_f seed; alpha O(1) FREE; EPS = 0.01 r_*, which puts the
   compact baryons inside the softening. The compact hollow holds only 5 to 6 particles, hence sigma_H of about 0.18.

## Plain reading

- A derived anisotropic target exists and is not posited. It is the maximum-entropy *exact* steady state of the law's halo,
  and it is everything the isotropic FIX-2 target is not:
  - it is a true kinetic equilibrium, even around compact baryons, where the halo rises outward;
  - it is tangentially biased exactly where that is required;
  - it has a sharp edge.
- On the bench it holds the law's inner profile, and it holds the edge once settled.
- As frozen, the label is INCONSISTENT. The halo is still breathing at the frozen 5 and 10 Gyr checkpoints, and it settles only
  by 13.8 Gyr at alpha >= 1. Overfill and alpha x 0.5 also remain open.
- For KiDS this points the wrong way. A sharp edge removes CFG559's small kinetic gain, so the edge-placement tension with KiDS
  is a property of the law's profile and supply, not of the velocity part.

Commits:
- criteria 93abcbeb6 (as CFG598);
- rename swept into 3dcb3a075;
- results in the commit that adds this README.
