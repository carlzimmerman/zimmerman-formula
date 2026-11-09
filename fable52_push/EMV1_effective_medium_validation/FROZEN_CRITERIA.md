# EMV1 (effective-medium validation): FROZEN CRITERIA, committed alone before any EMV1 script, Lean file or graded number

TEST lane, quarantined. Not registered. Relabels nothing in the record (SWT1, WL1, PAPER70, the closure register and
fable52_push/README.md are not edited). Footings canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), never pooled. No LCDM
input, no download, no new data. A FAIL is verified as hard as a PASS.

## 0. Question

SWT1's T2 (fable52_push/SWT1_switch_theorems, criteria 4d86f4d107, result 69a553a2a7) treats every law-on bubble as a LINEAR
inclusion: around the galaxy's own radial field it carries the law's incremental permittivity (radial u (2 + u) / (1 + u)^2,
tangential u / (1 + u)), `alpha_law` integrates the l = 1 Riccati equation to get its polarizability (-0.43 to -0.50), and
`compensated` turns the population into q_C by Maxwell-Garnett. The allowance on the filling, f <= LINE / (3/2 + LINE) = 0.0231
(LINE = 0.0354, WL1's lensing line), and SWT1's q_C rest on that linearisation.

The law's own field at a bubble wall is small (about 1e-12 m/s^2 at 1 Mpc from 5e10 Msun), the same order as large-scale fields.
**Does T2 survive a direct nonlinear solve of one bubble in a uniform external field g_ext?**

## 1. The problem solved (one bubble)

- Inside r < R_w: div[mu(|grad Phi| / a0) grad Phi] = 4 pi G M_b delta^3(x), mu(u) = u / (1 + u), point baryons at the centre.
- Outside: Laplace (S = 0, Newton).
- At R_w: Phi continuous and the normal flux continuous, mu dPhi/dr (inside) = dPhi/dr (outside).
- Far away: Phi -> -g_ext z (plus the monopole and induced multipoles).
- Dimensionless form: lengths in R_w, fields in a0. The problem depends only on y_w = G M_b / (R_w^2 a0) and e = g_ext / a0.
  g_wall = a0 u_in(y_w) is the law's own field just inside the wall.

**Numerics (frozen in kind; the grid is fixed by the known answers below before any graded number is seen).**
- Phi = Phi_ref(r) + psi, Phi_ref the spherical law solution (exact background flux G M_b at every radius).
- Axisymmetric finite volume in s = ln r (vertex-centred, nodes on both boundaries) and mu = cos theta (cells centred on
  Gauss-Legendre nodes, widths = Gauss weights, so the Legendre projection on the boundary is exact for l < N_mu).
- Outer boundary: the exact exterior Dirichlet-to-Neumann map. With psi_l the Legendre coefficients of psi at R_w, the exterior
  normal field is y_w - 3 e mu - sum_{l >= 1} (l + 1) psi_l P_l(mu); flux continuity sets the boundary cell's outer flux to it.
  No truncated exterior domain.
- Inner boundary at r_0 with y(r_0) = 1e6 (Newtonian core, mu = 1 - 1e-6): regular modes, d psi_l / d ln r = l psi_l.
- Gauge: the constant in psi is pinned by a grounding term on the exterior l = 0 mode (changes no gradient).
- Newton's method with a sparse finite-difference Jacobian (central differences, column grouping), continuation in e.
  A regulariser |grad Phi| -> sqrt(|grad Phi|^2 + eps^2), eps = 1e-6 x min(g_wall, g_ext) in a0 units, is used where the
  galaxy's field and the external field cancel (a null point exists inside the bubble once g_ext >~ 0.7 g_wall). KA7 bounds it.
- **Dipole.** Exterior l = 1: psi_out = (-e r + alpha_tot e / r^2) P_1, so alpha_tot = p / (R_w^3 g_ext) = 1 + psi_1(R_w) / e.
- **Incremental.** alpha_inc = (dp / dg_ext) / R_w^3 = 1 + d psi_1 / d e, from the tangent problem J d psi = -dF/de at the
  converged state (one linear solve), checked against central differences of p (KA6).
- Because the bubble plus centred baryons is isotropic, p(g_vec) = alpha_tot(|g|) R_w^3 g_vec exactly. So the response to a
  perturbation PERPENDICULAR to g_ext is alpha_tot, and along it alpha_inc. Orientation average: alpha_iso = (alpha_inc + 2 alpha_tot) / 3.

## 2. Inputs

- Masses and radii exactly as SWT1 T2 (its functions are loaded read-only from swt1.py, as swt1_extra.py does): the Driver+2022
  GSMF, log M* 9-12 on SWT1's 13-node grid LG, M_b = M*, WL1's shell solver for the radii, **z = 1 (WL1's graded epoch)**,
  readings **L** (law-on turnaround, baryons only) and **NC** (self-consistent, Newtonian collapse outside).
- The four KiDS masses log M_b 9.4, 10.45, 10.7, 10.9 at the L and NC radii (z = 1), for the table.
- The allowance's bubble: wall at SWT1's allowed reach, g_bar = 7.4625e-15 m/s^2 (swt1.json `gbar_floor_allowed`), so
  y_A = 7.4625e-15 / a0 on each footing. alpha there depends on y_A and e only, the same for every mass.
- Form-factor term q_ff: SWT1's, unchanged (it is the transform of the retained phantom and does not involve alpha).

## 3. The external-field bracket (from the record; SI, the same on both footings, Newtonian fields)

Levels the record has used or measured for KiDS lenses:

| source | level | g_ext (m/s^2) |
|---|---|---|
| P2 (rebuild_2026_10_22/P2_spec_isolated_lensing, JSON `ye_S3`, canonical units x 9.3603e-11): GAMA spectroscopically isolated KiDS lenses, catalogue baryons | c10 p16 1.7288e-5 | 1.6182e-15 |
| " | lo10 median (no completeness) 2.5613e-5 | 2.3975e-15 |
| " | **c10 median (P2's catalogue field) 6.5629e-5** | 6.1430e-15 |
| " | c20 median (to 20 Mpc) 1.0614e-4 | 9.9354e-15 |
| " | c10 p84 2.0404e-4 | 1.9098e-14 |
| " | bary median (all cosmic baryons trace galaxies) 1.3785e-3 | 1.2903e-13 |
| " | matter median (component traces them too; P2 flags it) 8.7728e-3 | 8.2116e-13 |
| " | matter p84 2.7274e-2 | 2.5529e-12 |
| S2 (rebuild_2026_10_22/S2_v3_lowg_lensing, Chae+21 medians used for KiDS lenses) | noclu 10^-3.215 x 1.2e-10 | 7.3145e-14 |
| " | maxclu 10^-2.30 x 1.2e-10 | 6.0142e-13 |
| QX7 iter_6 (closure_2026_11_06/QX7_unified_cold_switch/iter_6_efe_capped_wells; e_N x 1.2e-10, applied to KiDS isolated lenses) | noclu median 0.0004 | 4.8e-14 |
| " | **PRIMARY maxclu median 0.0033** | 3.96e-13 |
| " | maxclu p84 0.0052 | 6.24e-13 |
| " | ceiling x8 (missing baryons) 0.026 | 3.12e-12 |

**Graded bracket: all 14 nodes, 1.6182e-15 to 3.12e-12 m/s^2.** The script reads P2's values from its JSON and asserts them.
Note for the reading: in the two-phase picture the field outside the bubbles includes the cold component, about (1 + R) = 6.56
times a baryon-only field; P2's "matter" levels and QX7's x8 ceiling are the record's numbers of that size, and both are inside the
bracket. The bracket's levels are low-z values applied at z = 1 as they stand (stated approximation; reported below is the field at
which each move reaches 20 %, so a reader can place any other level).

## 4. Gates and labels (per footing)

- Allowance at node g: A(g) = LINE / (-alpha_inc(y_A, e) (3 + 2 LINE)) (the filling at which Maxwell-Garnett's q_C equals LINE).
  move_A = A(g) / 0.0230559 - 1 (SWT1's allowance, swt1.json `filling_allowed_insulating`).
- Readings X = L, NC at z = 1: q_tot,X(g) = q_C(alpha_inc on the LG masses, interpolated as SWT1 does) + |q_ff|.
  move_X = q_tot,X(g) / q_tot,X(SWT1) - 1, SWT1's values 0.302859 / 0.361214 (L) and 0.0180437 / 0.0181768 (NC).
- **T2 HOLDS**: max over the 14 nodes of |move_A|, |move_L|, |move_NC| < 0.20, AND at every node L stays above 0.0354 and NC
  stays at or below it.
- **T2 MOVES**: otherwise. Give the new allowance at the top node and which readings change side.
- **NO VERDICT**: if any known answer (Section 5) fails on that footing.
- Reported, no label: alpha_tot, alpha_iso and the q's with alpha_iso; the field g_20 at which each move reaches 20 % (scanned
  past the bracket to g_ext = a0); the self-consistent reach (allowance -> reach -> y_A -> alpha, iterated); the table of
  alpha_tot and alpha_inc against g_ext / g_wall = 10^(-2 + k/4), k = 0..12 (0.01 to 10), for the four KiDS masses at the L and NC
  radii, both footings; the null-point radius when one exists.

## 5. Known answers (all must pass, per footing where applicable)

- **KA0.** SWT1's functions reproduce its printed z = 1 q_tot for L and NC and the allowance 0.0230559 (relative 1e-6); the bracket
  values equal the record files (P2 JSON) to 1e-4 relative.
- **KA1** (task). As g_ext -> 0, alpha_inc -> `alpha_law`: at g_ext / g_wall = 0.01, |alpha_inc / alpha_law - 1| < 0.01 for the
  four KiDS masses at both readings' radii and at y_A, both footings.
- **KA2.** Linear homogeneous sphere (mu constant, no galaxy): alpha = (mu - 1) / (mu + 2) for mu = 0.1, 0.5, 2, to 2e-3 absolute;
  SWT1's coated-sphere closed form (swt1_extra.py E1, its three cases), to 2e-3.
- **KA3.** No galaxy (M_b = 0), nonlinear, e = 1e-3, 1e-2, 0.1, 1: the interior field is uniform (max relative deviation of
  |grad Phi| from its mean over interior nodes < 1 %) and solves g_in (mu(g_in / a0) + 2) = 3 g_ext; closed forms derived by hand
  before freezing (x = g_in / a0): alpha_tot = -1 / (2 + 3 x), alpha_inc = -1 / (2 + 6 x + 3 x^2). Both to 2e-3.
- **KA4.** No external field, with the reference switched to Newton's point field (so the solver must build the law itself):
  r^2 g / (G M_b) = nu(y) at r = 0.01, 0.1, 0.5, 0.9 R_w to 1e-3, and exactly M_b outside (exterior l = 0 flux; every l >= 1
  coefficient below 1e-10 of y_w).
- **KA5.** Resolution: doubling both grid sizes changes alpha_inc by < 2e-3 at g_ext / g_wall = 0.01, 1, 10 for log M_b 10.45
  at the L and NC radii, canonical, and at the top bracket node at y_A, both footings.
- **KA6.** The tangent-solve alpha_inc equals the central difference of p (step 1 % in g_ext) to 1e-3 at three points.
- **KA7.** eps x 10 changes alpha_inc by < 1e-4 at g_ext / g_wall = 10 (log M_b 10.45, L, canonical).

## 6. MUTATE (separate outputs; each must bite)

- **M-MU1** (emv1_MUTATE_mu1.*): mu = 1 inside the bubble. alpha must vanish (|alpha_tot|, |alpha_inc| < 2e-3 at every node) and
  KA1 must FAIL, so the mutate run's label is NO VERDICT.
- **M-FLUX** (emv1_MUTATE_flux.*): the flux condition dropped (dPhi/dr continuous at the wall instead of mu dPhi/dr). KA1 and
  KA2 must FAIL.
- Lean twin (EMV1_MUTATE.lean): false versions must fail to compile.

## 7. Lean (if closed forms are worth certifying; in the style of SWT1.lean, `lake env lean`, standard axioms only)

Planned: the homogeneous sphere, -1/2 <= (m - 1) / (m + 2) <= 0 for 0 <= m <= 1; the uniform nonlinear solution parametrised by
its interior field x > 0, e(x) = x (3 x + 2) / (3 (1 + x)) solves x (mu(x) + 2) = 3 e and is strictly increasing (so the solution
is unique); alpha_tot = 1 - x / e = -1 / (2 + 3 x); de/dx = (3 x^2 + 6 x + 2) / (3 (1 + x)^2) (HasDerivAt); alpha_inc =
1 - 1 / (de/dx) = -1 / (3 x^2 + 6 x + 2); -1/2 < alpha_tot < alpha_inc < 0; and the allowance: for -1/2 <= alpha < 0 the
Maxwell-Garnett line q_C <= q holds iff f <= q / (-alpha (3 + 2 q)), which is >= q / (3/2 + q). A statement that cannot be proved
is listed NOT CERTIFIED with its numerical known answer beside it; no label rests on Lean.

## 8. Disclosure: what I looked at and estimated before freezing

Read: SWT1's RESULT, FROZEN_CRITERIA, swt1.py, swt1_extra.py (head), swt1.out and swt1.json (SWT1's own graded numbers, used as the
baselines above); P2's README and JSON; QX7 iter_6's criteria and README; S2's criteria and README; CZ1's README. No EMV1 script
existed and no EMV1 number had been computed.

Hand estimates (expectations, not results):
- No galaxy, the closed forms above (derived by hand): at the bracket top on canonical (e = 0.0333) the interior field is
  x = 0.049, alpha_tot = -0.466, alpha_inc = -0.435.
- With the galaxy: the bubble's response is set by its outer shell; there the interior field is about sqrt(x^2 + u_wall^2) and
  alpha_inc ~ -1 / (2 + 6 u_eff). For L (u_wall ~ 0.008) I expect alpha_inc ~ -0.43 at the bracket top, so q_C(L) falls about
  11-13 %; for NC (u_wall ~ 0.02) about 8 %; the allowance rises about 15-17 % (0.0231 -> about 0.027). Alt moves less (larger
  a0, smaller e). At P2's measured catalogue field and QX7's primary the moves are under 3 %.
- So I expect **T2 HOLDS / HOLDS, narrowly at the top of the bracket**, with the 20 % line crossed near g_ext ~ 4-5e-12 m/s^2 on
  canonical. The proposer's expectation (alpha between -0.5 and -0.4 in both regimes, HOLDS) is the same.
- No reading can change side: |alpha| <= 1/2 caps NC's rise at a few per cent, and L would need alpha ~ -0.06 to reach the line.

## 9. Operational

One thread (OMP / OpenBLAS 1), under 1 GB, minutes. Files: emv1.py -> emv1.json / emv1.out; emv1_MUTATE_mu1.*; emv1_MUTATE_flux.*;
EMV1.lean, EMV1_MUTATE.lean, compile.txt, compile_MUTATE.txt; RESULT.md (label first, table of alpha against g_ext / g_wall).
Commits with explicit paths only. Amendments, if any, committed alone with the reason.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
