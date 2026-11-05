# AC6 frozen criteria: is AC2's dark-energy clock healthy inside galaxies?

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED;
not theory closed. Adopts nothing. No dark-matter particle.

## Hypothesis

AC2 (../AC2_single_clock/ACTION.md) replaces v3s's khronon dust sector K(Q) by a
canonical dark-energy clock X - V and keeps the stiffness -(gamma/2)(D.P)^2
smooth and UNSWITCHED. H4 (rebuild_2026_10_22/H4_v3_saddle_stability) proved that
with an unswitched stiffness the khronon pair is Hadamard ill-posed wherever its
charge rho_tau < 0, and found such regions in every two-body saddle and every
external-field lobe. In AC2 the clock's inertia is (rho + p)_phi = phidot^2,
at most 2 rho_DE for V >= 0. If the effective charge is rho_eff = D.P + phidot^2,
AC2 is ill-posed wherever D.P < -phidot^2. The switched form (AC2s) would then
be the repair.

## Part A: derivation (sympy, all residuals must be identically 0)

PN Lagrangian: H4's A1 Lagrangian with the dust term mu_K^2 Xi^2/(2K) replaced by
the clock term C = (s^2/2) [ (1 + sigma_t)^2/(1 + phi)^2 - |grad sigma|^2 ],
s = phidot (the clock's background rate); V' dropped (it is O(H phidot)).

- A1: derive the sigma and phi Euler-Lagrange equations; record rho_eff exactly
  as it appears (continuity form), and the clock's gravitating density.
- A2: WKB dispersion on a frozen background (H4 A4's system: Poisson, the
  anisotropic W Hessian with M_L, M_T, the gamma term, continuity, Bernoulli),
  with the clock's linearised terms in place of the dust's.
- Known answers: (i) H4's own dust system, rebuilt in this script, reproduces
  H4's A4 dispersion rho_tau (k^2/chi - K) exactly; (ii) s -> 0 gives H4's
  mu_K = 0 form K rho_tau (M_theta - 1 + gamma k^2/K) exactly.
- Graded symbolic statement: the sign of lim_{k->inf} omega^2/k^2. ILL-POSED
  branch exists if that limit is negative whenever rho_eff < 0 (Gamma ~ k).
- Switched form AC2s (gamma -> 0 where D.P < 0): the same limit must be finite
  and k-independent there (bounded rate).

## Part B: where rho_eff < 0 (H4's own solver, imported unchanged)

Systems: H4's declared set S1-S6 (pairs, single in field, MW-like and dwarf
discs, with and without g_e = 0.01 a0), both footings, base and fine levels.
Offset: rho_eff = D.P + s^2 with s^2 = (1+w) rho_DE, rho_DE framework-native:
rho_DE = a0^2 / (kappa^2 c^2 G), kappa = 1/2, per footing. Three offsets:
(1+w) = 0.1, 1, 2 (2 is the maximum for V >= 0). No LCDM background number.

- Known answer: with H4's own offset (f = 3 x 0.26 rho_crit as in H4) this run
  reproduces H4's fine-level near-zone medians for S2_LMC-MW (both footings)
  to 1 %.
- Convergence: H4's line, base -> fine change in negative volume and median
  |rho| <= 10 % for every map used in a verdict; a map missing it cannot
  support a verdict.

## Lines (stated before running)

- AC2 (unswitched) ILL-POSED if Part A gives Gamma ~ k for rho_eff < 0 AND
  Part B finds rho_eff < 0 regions at (1+w) = 2 in at least one system on both
  footings with converged maps.
- AC2 HEALTHY at this order if Part B finds no rho_eff < 0 region at
  (1+w) = 0.1 in any system.
- Otherwise UNDECIDED, reported per offset.
- AC2s: BOUNDED if Part A's switched limit is k-independent; e-folds over
  the region lifetime computed with H4's rates() at its bounded branch and
  reported, not graded.

## Negative control

MUTATE flips the sign of the first-order term (H4's convention, separate
outputs). It must turn the Solar-System / isolated-disc rows ILL-POSED
(H4's A4/B2 behaviour). If it does not bite, no verdict above stands.

## Compute

H4's solver, one thread per process, parallel over systems (spawned process
pool, <= 12 workers), each child < 1 GB RSS as in H4. No downloads.
