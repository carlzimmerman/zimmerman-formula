# CFG337 FROZEN CRITERIA: is there a stable action for candidate B's bound-only switch?

**Lane:** orchestrator-dispatched research lane. The owner asked for "a deep dive to find solutions" to the
structure-growth failure (bare chassis L340 lets all matter feel nu_mono; growth ~7x too fast, excluded by CMB
lensing, L341 / AUDIT_SIGMA8_2026-10-03). Candidate B's bound-only switch restores LCDM growth (CFG324), but B has
no stable action. Written before any lane script.

**Fixed throughout:** c_T = 1; the beta = 0 chassis; the nu_mono kernel; the switch reads baryons only (MS1-MS5:
never the carrier, never curvature); kappa = 1/2 fixed (fitted); no dark-matter particle (the cold mass is still
required). Both footings where a number depends on a0.

## Part 1: diagnosis table (from the record only, no new computation)
For each prior gated action (DE7 curvature gate, DE12 MOND-sector gate, DE13 gradient repair, MS5 kappa cap,
XR36 theta gate, CFG48 local/nonlocal gates, CFG49 dynamical gate scalar, CFG172D theta-flow gate, CFG242 latch and
BIMOND, CFG243-245 ownership classes, V0 region gate): which failure (ghost / gradient / Hadamard / strong coupling /
non-instability), in which regime, with the commit or file it comes from.

## Part 2: screen (decided by argument plus a cheap sympy check each)
- S1 k-mouflage / kinetic (field-strength) switch with a baryonic threshold;
- S2 symmetron / dilaton with a baryonic coupling (standard sign and inverted, density-triggered sign);
- S3 cubic Galileon / Vainshtein-like derivative switch (both signs);
- S4 "virial" switch from a local scalar of the baryonic stress tensor (trace, P/rho);
- S5 switch on the khronon's leaf-averaged quantities (CFG329: diffeomorphism-safe);
- S6 (record reference) the nonlocal enclosed-mass gate (CFG48), not a legal local term.
Each is scored on: OFF on linear FRW (delta << 1, unbound); ON in virialised baryonic systems; ghost-free;
gradient-free; well-posed linearisation on both sides; respects the fixed constraints above.

## Part 3: at most 2 promising candidates, quadratic actions in sympy
Backgrounds: (a) FRW with linear perturbations; (b) a static virialised baryonic background (WKB, k >> background
gradient scale); (c) the switch's transition region, on the record's own transition profiles (DE12's transition()
function, loaded read-only: z = 0.25, 1, 2.5, 4; M_b = 1e10, 1e11, 1e12; both footings; gate widths w = 0.25 and 1).

**Health criteria on each background (all must hold):**
- H1 kinetic matrix positive definite (no ghost);
- H2 all high-k sound speeds squared > 0 and <= 1 (luminal allowed);
- H3 Hadamard well-posed: the growth rate is bounded uniformly in k (omega^2 bounded below as k -> infinity);
- H4 (transition only, physical) any bounded long-wavelength growth of the transition gas is no faster than the
  local gravitational rate Gamma_g = sqrt(4 pi G rho_m) (rho_m = rho_b / f_b + rho_ph at the worst point), AT a
  switch length ell no longer than the record's localisation tolerance ell_loc = 100 kpc (XR15: the flagship holds
  to 100 kpc smoothing). Reported alongside: 500 kpc and the transition radius r_edge.
- On FRW additionally: the growth equation of the matter perturbation is the LCDM one at linear order (switch OFF).

## Decision (frozen)
- **CANDIDATE FOUND:** one action passes H1-H3 on FRW, H1-H3 on the bound background, and H1-H4 in the
  transition region, with linear FRW growth OFF.
- **PARTIAL:** it passes on two of the three (FRW, bound, transition).
- **NO-GO:** fewer than two; state the obstruction exactly.

## Controls
- R1 (known failure returns): the record's prescribed gate (DE12's MOND-sector gate, w = 0.25, M*) treated as the
  slaved (no own kinetic / gradient term) limit of the candidate: must give c_gate > c_s and Hadamard growth
  Gamma ~ k sqrt(c_gate^2 - c_s^2) with min c_gate within 1% of DE12's committed 1526 km/s and min Gamma/H at
  k = 1/kpc within 1% of 2.0e4 at z = 0.25; and DE7-T1's sign fact (a smooth gate flat at both ends has W'' > 0
  somewhere) checked on DE12's W.
- R2 GR limit: switch coupling and MOND sector off -> the quadratic form reduces to a canonical scalar plus
  pressure-supported Newtonian fluid: healthy, standard Jeans growth.
- MUTATE (env CFG337_MUTATE=1, separate outputs *_MUTATE*): flip the sign of the switch field's kinetic term; H1
  must be flagged (ghost) and the run must exit 1.

## Lean
Certify the decisive sign / positivity inequalities of the best candidate (2x2 positivity, bounded-below dispersion
vs the unbounded slaved limit, the transition-length inequality on the committed numbers, the ghost under the sign
flip). Mathlib, no sorry; compiled with `lake env lean` from fable_independent_2026/lean_2026.

## Scope
Quadratic (linear) level only; quasi-static Newtonian limit on the khronon leaves for the matter / switch sector;
the chassis' tensor and khronon sectors are untouched by a minimally coupled switch. No nonlinear evolution. No
downloads. A clean no-go is a valid result.
