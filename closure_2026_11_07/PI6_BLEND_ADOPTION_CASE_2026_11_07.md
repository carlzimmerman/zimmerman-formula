# The case for and against adopting the Pi^6-blend stiffness repair (11-07)

Item 2 of DIRECTION_2026_11_07.md (c1f7a6299e). Written for the owner, who alone adopts. It adopts nothing, changes no
label and adds no number; every figure below is quoted from the lane named beside it.

## What changes in the action

Only the stiffness term. The kink F(Pi) = (1/2)[max(Pi, 0)]^2 (v3s: Pi = D.P; AC2q: Sigma = D.P + 2X) is replaced by
AC21 iter_6's blend F = gamma b^2 f(Pi/b). It is a pure power Pi^6 below b/2 (f = (122363904/44610575) q^6 exactly,
QX19 C6), a C^4, structurally convex blend on the layer (A = 734183424/8922115, B = 3165142806/44610575, exact
rationals fixed by f(1) = 1/2 and f'(1) = 1), and exactly (gamma/2) Pi^2 for Pi >= b (AC21 63242d3e1e). The scale is
b = rho_DE for v3s and b = X for AC2q, both taken from the a0 law, so there is no new constant. The knot choices
(tau 1/2, x1 1/4, x0 4/5, n 5) are pure numbers, the first qualifying member of a search order declared in advance (AC21).

## FOR

- **It fixes the one classical failure of the raw switch.** AC16 (6d5faba9bd) proved that no C1 solution exists across
  a transverse D.P = 0 interface for generic data: the force jumps by -gamma grad Pi. With the blend, AC21's theorem
  (symmetric hyperbolic in w, Kato H^s across the switch iff F ~ Pi^m with m > d + 2) is met, with m = 6 > 5.
- **The numerics agree on curved interfaces.** AC22 (23b4be92bf): curved 2D, C1 and C2 PASS on all five form rows to
  N 51200, while the raw form collapses (sigma -0.50). BL3 (30cfe4a1cf): curved 3D spherical switch, C1/C2/C3 PASS on
  all five rows; the boundary case m5 holds a finite D3 (-12.68, analytic -12.75) and fails, m6 passes; KA reproduces
  AC22 bit for bit; MUTATE bites.
- **It keeps everything graded.** QX19 (e2f938cdfc), all ten carries proved: statics change <= 2.0e-5 on the Cassini
  margin 4.8e7, so PPN gamma = beta = 1 carries; FRW exact (the background sits at q = 2, F = Sigma^2/2, dF/db = 0);
  PN sign B >= s for any convex F (AC21 T7); c_T = c for generic F; slip <= 5.9e-15; SPARC phantom change 1.4e-4 dex.
- **It costs nothing elsewhere.** TC1 (746f8b6fb4): the blend equals AC2q exactly on Sigma > X and Sigma < 0; no static
  SPARC or X-COP radius sits in the layer, and FRW and linear states never enter it. No QX19 PASS row is lost.

## AGAINST, and what stays open

- **It cures nothing physical that the record grades.** TC1: physical states sit at Sigma/X ~ 1e2-1e5 or Sigma < 0, so
  the blend "can neither cause nor cure the fold". The clock-stream folds still fire at 9.0-9.6 Myr and 183-200 Myr,
  identical to AC2q, both footings. Well-posedness is therefore local-in-time only: classical solutions of the
  blended action still break down in finite time on physical data. FS2 (fd29a9fc84) finds no pair where AC2q
  regularizes a fold; AC22 argues (not runs) that soft-side folds are unchanged by construction.
- **Non-radial modes are untested.** BL3 is spherical (l = 0) only; the 3D count m > d + 2 is AC21's analytic map, not
  something any ladder derives.
- **J = 0 drift.** The J = 0 events drift slowly downward after the J <= 1/2 event (AC22 sigma_0 -0.05 to -0.12; BL3 -0.08
  to -0.14, inside the -0.35 line). This sits in the window where stiff-side gas shocks form (AC20); a slow post-shock
  approach to zero is not excluded. Shocks and weak solutions are out of scope in every lane.
- **Power 6 is not forced.** AC21's condition is m > d + 2, a strict inequality on a real exponent; 6 is the smallest
  integer that meets it, and the blend shape is one construction among others. The record shows admissibility, not
  uniqueness.
- **Narrow and post-data points on the record.** AC21's overall 3D label is NOT PASSED as frozen (iter_7 C1 FAIL, crossing
  ratio 1.1045 vs 1.1). AC22's crossing statistic was chosen after iter_7's numbers (disclosed); iter_7's legacy line
  would fail one AC22 row (1.164) and three BL3 rows. The winning form came after four NO-GO families (AC21 iters 1,
  3, 4, 5). BL3's C2 margin is tight (0.114 vs 0.117, converging at second order), and its D3 leak check is post-run.
  AC20's 1D contact form (3384fe50b6) is not a 3D repair. Every check is on the PN charge-velocity system with a
  transverse switch, not the full covariant system. QX19's float evaluation carries about 1e-4 cancellation (TC1 note).

## What adopting it would change

- CLOSURE_FINAL.md: the "Repair on the table, NOT adopted" paragraph and the BL3/QX19 rows become the action's stiffness
  statement; "Adoption: the Pi^6-blend stiffness repair" leaves the waiting list; the AC16 row stays as the label of
  the raw switch.
- EQUATIONS_IN_ORDER.md: the stiffness in section 1 and the AC2q L_stiff line take F = gamma b^2 f; row 8.3 ("well posed",
  X3 pointwise WKB) is read with AC16 and the local-in-time scope from TC1.
- PAPER68 v1.0 (DOI 10.5281/zenodo.23990944) prints max(D.P, 0)^2 and the J(Y) + independent-P form that decouples P if
  read literally (QX17 70bbb84f45). A new version, or PAPER70 (SE3, draft, not deposited), would state the action once
  in the operative Legendre form P.A - W(K|P|) with the blended stiffness, carrying both changes together.

## What not adopting leaves

The action keeps the raw max switch. AC16's FAIL across the switch stands as its label: no classical solution for
generic data crossing D.P = 0, well-posed on each branch only. The blend stays on the record as a proved,
cost-free option (QX19, BL3), and PAPER68 still needs its Legendre-form erratum either way.

## The decision

Do you adopt AC21's Pi^6 blend (b = rho_DE for v3s, b = X for AC2q) as the stiffness of the action, accepting that
well-posedness is then local-in-time, spherical-3D tested and not unique in its power, or keep the raw max switch with
AC16's FAIL as its label?

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
