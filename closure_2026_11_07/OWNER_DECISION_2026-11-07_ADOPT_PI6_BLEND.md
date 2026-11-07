# Owner decision, 2026-11-07: the Pi^6 blend is adopted as the stiffness of the action

Recorded at the owner's instruction. The question put in chat was whether to adopt the Pi^6 blend as the action's
stiffness, with the cases for and against on the record (PI6_BLEND_ADOPTION_CASE_2026_11_07.md, c526a4818b). The
owner answered **"Adopt the blend"**. This file is committed alone and is never edited; any change goes in a new dated
file. It changes no frozen file and no graded number. Kappa = 1/2 FITTED. Not theory closed. Nothing here says the
data favour the framework.

## What is decided

- **v3s's stiffness is the blend.** The raw kink -(gamma/2) [max(D.P, 0)]^2 is replaced by AC21 iter_6's blend,
  F = gamma b^2 f(Sigma/b), with b = rho_DE. Near 0, f is a pure Pi^6 (m = 6 > d + 2 = 5). It is C4 and convex, and it
  is exactly Sigma^2/2 for Sigma >= b. b is the a0 law's own scale, so there is no new constant.
- **AC2q.** AC2q is still the candidate successor and is not adopted here. If it is adopted later, it carries the same
  blend with b = X, which is QX19's one action.
- **v3s's scope is unchanged:** isolated galaxies, the Solar System, galaxy lensing and gravitational waves
  (OWNER_DECISION_2026-11-04_ADOPT_V3S_SCOPED.md). Clusters, growth / CMB lensing, AGC 114905, Malin 1 and the canonical
  FG1 tilt keep their labels, because the blend moves no failing gate (largest effect <= 1.4e-4 dex, QX19 C8).
- **a0 is still put in by hand.** a0 = kappa c sqrt(G rho_DE), kappa = 1/2 FITTED.

## What the adoption rests on

| item | result | lane |
|---|---|---|
| raw switch | no C1 solution across a transverse switch; in 3D the max form collapses (sigma -0.50, D diverges) | AC16, BL3 control |
| 3D condition | symmetric hyperbolic theory across the switch iff F is a pure power Pi^m near 0 with m > d + 2 | AC21 iter_1 (theorem) |
| curved 2D | PASS, C1 and C2, all five form rows | AC22 |
| curved 3D, spherical switch | PASS, C1 C2 C3; m5 fails, m6 passes | BL3 |
| every graded gate | C1-C9 carry: c_T, tensor mass, lensing slip, PPN / Cassini, FRW (exact), PN sign, slow roots, SPARC, galaxy linear health | QX19 |
| equality off the layer | equals the raw form with both first derivatives on {Sigma > b} union {Sigma < 0} | TC1 S1 (shown for AC2q, b = X) |

## Limits adopted with it, stated wherever the action is stated

- Well-posedness is **local in time**. Smooth solutions form ordinary gas shocks after about sqrt(a/Pi) of a crossing
  time (AC20), and weak or shock solutions are not graded.
- It is tested in **spherical 3D only**. Non-radial (l >= 1) modes are untested (BL3).
- **Folds are unchanged.** The blend can neither cause nor cure the soft-side caustic folds (TC1 J3; PI6 case file).
- **Power 6 is not forced.** It is the smallest integer with m > d + 2, and the record shows the blend is admissible,
  not unique. The form came after four failed families (AC21 iters 1, 3, 4, 5).
- **Narrow and post-data points** stay disclosed as in the case file:
  - AC21's iter_7 C1 FAIL as frozen;
  - AC22's crossing statistic was chosen after iter_7;
  - BL3's tight C2 margin (0.114 vs 0.117);
  - every check is on the PN charge-velocity system, not the full covariant system.
- The AC16 row remains the label **of the raw switch**.

## What follows (each item for its owning session; nothing is edited here)

- CLOSURE_FINAL.md: the "Repair on the table, NOT adopted" paragraph becomes the adopted stiffness statement, and the
  waiting-list line "Adoption: the Pi^6-blend stiffness repair" is closed by this file.
- EQUATIONS_IN_ORDER.md: the stiffness takes F = gamma b^2 f. Row 8.3 is read with AC16 and TC1's local-in-time
  scope.
- PAPER70 (SE3, Field equations session): state the action once in the operative Legendre form P.A - W(K|P|), with the
  blended stiffness. This carries the PAPER68 erratum and the blend together.
- PAPER68 v1.0 (DOI 10.5281/zenodo.23990944) prints the raw max form. A new version or PAPER70 supersedes that text.
  The owner holds every deposit.
- STANDING.md gets one dated addendum (with this file).

Kappa = 1/2 FITTED; not theory closed.
