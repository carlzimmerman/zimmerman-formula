# XF1: the action's own hosted state (a body moving through its host's khronon): FAIL / FAIL

Criteria: FROZEN_CRITERIA.md (8b99d12c42, frozen before any script; no amendment). Both footings graded separately on the
record's hosted-path values a0 = 9.3603e-11 (canonical) / 1.1312e-10 m s^-2 (alt), L* at the floor 21.68 / 22.85 pc; never
pooled. TEST lane, quarantined as HY1/BG1/PJ1: it re-grades hosted rows and adopts nothing. kappa = 1/2 FITTED; not theory
closed. No dark-matter particle. Scripts: xf1_cells.py, xf1_stageA.py, xf1_field.py, xf1_hydro.py (diff from MS3's
hydro_ms3.py in xf1_hydro.diff), xf1_runlist.py / xf1_run_all.py (128 runs), xf1_grade.py. Outputs: xf1_stageA.out/.json,
xf1_cells.json, xf1.out / xf1.json, xf1_MUTATE.out, parts/<run>/{snap_04.npz, static.npz, done.json}, logs/.

**Label: FAIL (canonical) / FAIL (alt), by C3 and C1.** The sign check C3 fires first: on every Coma UDG row of both footings
D = log10(g_dyn/g_static) is negative (canonical -0.401 to -0.229, median -0.274; alt -0.453 to -0.266, median -0.315), so the
moving body is not mis-graded in the theory's favour; the sweep removes the body's own hosted phantom and leaves it Newtonian.
C1's F is then negative on every row (canonical -0.646 to -0.287; alt -0.748 to -0.333), under the FAIL line 0.3. C5 holds
(the Sun stays under every AC15/MS3 line, worst 0.215 of the Mars line). The hosted rows stand as graded, and the static
external-field state is, if anything, generous to the theory.

## The question and the answer in one paragraph

Every hosted row of the record was graded with a STATIC external-field state. The adopted action's moving-Sun solve (AC15,
MS3) found that a hypersonic body sweeps its static hedgehog away. XF1 asks whether the same sweep acts on the phantom of
a hosted galaxy, and in which direction it moves the hosted rows. Stage A derives the stationary-pattern system of the full
screened action (W live, not AC15's PN reduction): the khronon charge q = div P is advected by the frame and conserved; the
frame moves under the body's gravity, the charge's gravity, the Legendre force grad chi (where chi is fixed by the elliptic
constraint div[grad chi/(1+|grad chi|/a0)] = K q) and the stiffness pressure; no Bernoulli integral survives while W is live.
For a hosted galaxy the body's gravity deflects the host wind by gpar = GM/(aV^2) ~ 1e-4 (Coma UDGs) to 1e-3 (dSphs), and the
restoring force of the charge is 1e-5 of the inertia at the readout radius, so the frame streams through ballistically and the
static EFE phantom, which is what makes g_static exceed Newton by 1.7-2.8x (UDGs) and 3.8-8.6x (dSphs), is carried downstream
at the wind speed: the HEDGEHOG start loses 99.86-100.01 % of its phantom inside the readout sphere by t_end in every row,
both footings, both V readings, both grids. What remains is the Newtonian field plus an anomalous charge whose gravity is at
most 1.9e-3 of g_N (the UNIFORM-start compression and the swept remnant are of the order of the scheme's truncation noise,
1e-2 of rho_h). So g_dyn = g_N to 2e-3 dex, D = log10(g_N/g_static) < 0, F < 0: the hosted rows get worse, not better.

## Stage A (xf1_stageA.out, all PASS)

- A1a/A1b (sympy): the P equation grad(Xi + gamma_L F'(q)) = K W'(K|P|) P^ and the khronon equation d_t q + div(q v) = 0
  from the Legendre-form Lagrangian with W and F general. A1c: W is the Legendre dual of PAPER70's J (residual 0).
  A1d: the P equation inverts to div[grad chi/(1 + |grad chi|/a0)] = K q, chi = Xi + gamma_L F'(q). A1e: chi is constant
  iff W' = 0, so there is NO first integral while W is live (HE-a HIT). A1f: in the body frame Xi = phi + (w^2 - V^2)/2 and
  div(q w) = 0 (AC15 S1b/KA2 re-verified). A1g: dP/dA about the host state is 1/(K(1+x_e)^2) along e^ and 1/(K(1+x_e))
  across (D10 Route F's kernel; K^2 W'' = K M_theta, AC15's screening coefficient). A1h: the static linear EFE response
  div[(I - D) grad phi_t] = K rho_b, anisotropic Coulomb solution verified.
- A2 PASS: at V = 0 the system is D10's (L) + (P_L), the solver X1 and SE2 graded with. A3 PASS: the uniform wind is exact
  (rho_h = 0 trivially; rho_h != 0 as the Galilean boost of the static host, Xi and continuity invariant). A4 PASS: with W
  dropped and F raw, gamma q = c_gal^2 + Phi_N + (V^2 - w^2)/2, AC15 S1b term by term.
- Perpendicular g_ext: equations written (e^ = x^), not axisymmetric: Stage B NOT RUN for it (declared).

## Stage B (xf1_hydro.py; 128 runs, every known answer PASS)

The AC15/MS3 axisymmetric (ln r, theta) architecture, code units L0 (the body's Plummer scale a for B1-B4, R_A for the point
Sun), V, rho_h; AC15's stiffness fluid; plus the two Stage A forces AC15 did not carry, computed with one finite-volume
anisotropic Poisson operator family on the grid (prefactorised), so the linear static EFE start is an exact discrete fixed
point (residual 1.6e-7). A signed tracer carries the HEDGEHOG phantom of the galaxy cells: the record's own nonlinear static
EFE solution (D10's Solver2D on X1/SE2's call, interpolated; its monopole boost agrees with D10's to 0.5 %). Bodies: Plummer
a = R_e (SE2) for the UDGs, a = r_h (X1) for the dSphs, a = 3 / 5 kpc (assumption) for the group / X-COP member proxies,
the point Sun for B5. V brackets: 1000 / 1732 km/s (Coma 1D and 3D), X1's V_c(d) and sqrt 2 V_c (dSphs), 300 / 520 (group),
1000 / 1732 (X-COP), 220 / 369 (Sun). Coarse for every row (9 UDGs, 8 dSphs), medium for the representative rows (DFX1,
Sextans), both starts, both V; B3/B4 UNIFORM only (coarse both V, medium V1); B5 as AC15 (TRANSMIT uniform coarse + medium,
HEDGEHOG coarse, both M per footing; REFLECT coarse at the higher M).

- KB1a PASS: AC15's REFLECT M490 coarse run with the reduced equations is reproduced bitwise (max |diff| 0.0 on q, u, v);
  regraded over AC15's 12 cells, q_B reading: Earth 0.03629 (AC15 0.03628), Saturn 0.10752 (AC15 0.10749).
  KB1b PASS: under the full A1 system (Legendre force and charge gravity on), the canonical floor cell at 1 AU reads
  G1 Earth 5.705e-5 against AC15's 5.705e-5 (rel diff 1.2e-5; line 27 %): at 1 AU the extra terms are 1e-21 of the inertia.
- KB2 PASS: the HEDGEHOG start at V = 0 holds its static solution to 2.1e-10 (B1 coarse), 1.2e-10 (B1 medium), 7.0e-11
  (B2 Sextans), 8.7e-4 (the Sun, AC15 KA4 style), line 1e-2. Reported: the record's nonlinear D10 phantom under the
  linearised kernel drifts 1.7e-1 over t 20 (it is not the kernel's fixed point; the HEDGEHOG wind runs start from it).
- KB3 PASS: gravity off, the uniform wind holds to 5.1e-3 (B1 grid) and 4.6e-3 (Sun grid) on medium (coarse 1.27e-2 /
  1.20e-2, AC15's KA3 numbers).
- Steadiness: the graded ratio changes by <= 1.9e-3 over the last 20 % of every galaxy run (<= 7e-6 for the UNIFORM starts).
  Convergence: coarse -> medium changes the graded ratio by 6.8e-5 (B1) and 4.0e-4 (B2); both V readings give the same
  label on every row. Forces: the Stage A extra forces are <= 5e-3 of the body's gravity in every UNIFORM run (0.3-0.5 in
  the HEDGEHOG runs, where they balance gravity at t = 0 by construction). Peak RSS 597 MB.

## Stage C (xf1.out), per footing

Static references from D10's solver on X1/SE2's own call (KA_SE2: SE2's per-galaxy E_v3_dmean reproduced to 6e-15 with S1's
constants; KA_X1: X1's per-row Delta[v3 L*floor] - Delta[Newton] reproduced to 0.007 dex; Newton residual <= 9e-11).

| footing | cell | g_static/g_N at the readout | D = log10(g_dyn/g_static), per row | F per row | swept fraction |
|---|---|---|---|---|---|
| canonical | B1 Coma UDGs (9) | 1.70-2.52 | -0.401 ... -0.229 (median -0.274), ALL NEGATIVE | -0.646 ... -0.287 (median -0.383) | 0.9997-1.0001 |
| canonical | B2 MW classical (8) | 3.79-8.06 | -0.906 ... -0.577 (median -0.792), ALL NEGATIVE | -94 ... -1.57 | 0.9986-0.9998 |
| canonical | B3 group member proxy | 2.00 | -0.300 (C4: D only) | (not graded) | HEDGEHOG NOT RUN |
| canonical | B4 X-COP member proxy | 1.58 | -0.198 (C4: D only) | (not graded) | HEDGEHOG NOT RUN |
| alt | B1 Coma UDGs (9) | 1.85-2.84 | -0.453 ... -0.266 (median -0.315), ALL NEGATIVE | -0.748 ... -0.333 (median -0.443) | 0.9997-1.0000 |
| alt | B2 MW classical (8) | 4.09-8.65 | -0.936 ... -0.610 (median -0.822), ALL NEGATIVE | -80 ... -1.62 | 0.9986-0.9998 |
| alt | B3 group member proxy | 2.13 | -0.328 (C4: D only) | | HEDGEHOG NOT RUN |
| alt | B4 X-COP member proxy | 1.66 | -0.221 (C4: D only) | | HEDGEHOG NOT RUN |

g_dyn/g_N = 1 + eps with eps the anomalous charge's gravity at the readout, worst over starts, V and grids: |eps| <= 5.1e-4
(B1), <= 1.9e-3 (B2), <= 1.6e-3 (B3), <= 2.3e-4 (B4); so D equals log10(g_N/g_static) to 2e-3 dex and the rows are graded
at the readout radii of the criteria (R_e for the UDGs, a for the dSphs, 10 kpc for the proxies).

- **C3 (first):** D < 0 on every B1 row, both footings. The body's own hosted phantom is swept with the host's; the moving
  body is MORE Newtonian than the static EFE state, not less. FAIL of the reading "hosted rows are mis-graded in the
  theory's favour".
- **C1:** F < 0 everywhere (the dynamic reading lies on the far side of the static one from the isolated law): FAIL (hosted
  rows stand as graded). Coarse/medium spread of the graded ratio 6.8e-5 (B1), 4.0e-4 (B2).
- **C2:** on SE2's data path (post_udg, widths_half_post_freeze) the Coma UDG shortfall moves from +1.121 [0.773, 1.478]
  (record) to +1.412 [1.064, 1.768] dex canonical, and from +1.076 [0.722, 1.431] to +1.409 [1.055, 1.765] alt: NOT
  EXPLAINED, by 0.29-0.33 dex more. X1's rows (bootstrap median over systems with the per-row MC sd): MW classical
  +0.356 [0.000, 0.935] -> +1.208 [0.700, 1.757] canonical and +0.321 [-0.033, 0.904] -> +1.203 [0.699, 1.758] alt; bright
  M31 +0.633 [0.350, 0.887] -> +1.555 [1.287, 1.794] canonical and +0.600 [0.315, 0.846] -> +1.555 [1.287, 1.793] alt:
  all NOT EXPLAINED. (The criteria's "+0.32 / +0.48 QUMOND EFE medians" are not X1's v3 L*floor numbers; X1's are the ones
  above, recomputed from x1_per_system.csv.)
- **C4:** B3 and B4 are proxies: D only, -0.300 / -0.198 canonical and -0.328 / -0.221 alt. Those rows are host rows, not
  member rows; the member sweep cannot by itself change the host's own hydrostatic/lensing need of x4.2/3.8.
- **C5 PASS:** under the full A1 system the Sun stays under every AC15/MS3 line on both footings, every bracket (TRANSMIT
  uniform coarse/medium and HEDGEHOG coarse at both M, REFLECT coarse; q and q_B readings, envelopes where NOT STEADY):
  worst ratio to line canonical G1 Earth 0.032, Mars 0.215, Saturn 0.111, G2 0.018 / 0.132 / 0.095, G3 Cassini 0.071;
  alt 0.028, 0.194, 0.100, 0.016 / 0.120 / 0.085, 0.064. The q readings are 4e-4 to 1e-3 of the lines; the q_B shock proxy
  sets the worst, as in AC15/MS3.

## MUTATE (xf1_MUTATE.out)

- MUTATE-1 (V -> 0): the held state read against the lane's own static reference gives F = 1.6e-11 (B1) and 5.2e-12 (B2):
  reads 0. Against the record's nonlinear static (D10) it reads +0.001 / +0.021 canonical and -0.086 / -0.042 alt: the
  linear-versus-nonlinear offset of the static boost (2.522 vs 2.517 / 2.842 for DFX1; 8.183 vs 7.963 / 8.648 for Sextans),
  reported, not a pipeline fault.
- MUTATE-2 (g_ext -> 0, the body keeps its own khronon, g_dyn = g_iso): F = 1.0000 on both cells and footings.
- MUTATE-3 (+0.5 dex planted on g_dyn in B1): the C2 half-width median moves from +1.412 to +0.912 [0.564, 1.268] canonical
  and +1.409 to +0.909 [0.555, 1.265] alt: the plant is detected to 0.001 dex, but C2 does not flip to EXPLAINED, so C2 is
  reported NO POWER at a 0.5 dex plant (the shortfall after the sweep is 1.4 dex; the label does not rest on C2).

## Hand estimates (frozen)

- HE-a HIT: the screened system is a coupled PDE; Bernoulli survives only with W dropped (AC15's PN regime).
- HE-b MISS: F is not between 0.3 and 0.7; it is negative on every row (-0.75 to -0.29).
- HE-c MISS: C5 passes, but with margin 4.6x (Mars q_B, 0.215), not > 10x; the q readings alone have margin > 1000x.
- HE-d MISS on the sign (D is negative: the host's suppression does not weaken, the body's own phantom is removed); the
  second half holds (C2 stays NOT EXPLAINED, now by 1.4 dex).

## Limits and disclosures

- The sweep is the ballistic advection of a conserved charge; its amplitude does not depend on the force kernel. The force
  kernel (Legendre force + charge gravity) is the linear response about the host state (A1g), valid where the body's
  Newtonian field is well below the host's: true at the readout for every Coma UDG (gN/gext 0.007-0.020) and for four dSphs
  (Sextans 0.011, Ursa Minor 0.038, Draco 0.072, Carina 0.098); extrapolated for Fornax, Leo I, Leo II, Sculptor (0.32-2.5)
  and for the B3/B4 proxies (2.1-2.6). Where the forces are 1e-5 to 5e-3 of the inertia this changes nothing graded.
- B3/B4 HEDGEHOG starts NOT RUN: the linear phantom carries a negative total charge (to -12.6 rho_h) and its hold runs away;
  B3/B4 are graded on the UNIFORM start only (C4 asks D only). For 7 of 8 dSphs the record's own nonlinear static phantom
  added to the host's uniform charge is also negative in the equatorial lobes (to -61 rho_h for Leo II); the tracer is
  signed and advected regardless, flagged "kernel extrapolated" in parts/*/static.npz.
- The static references are the record's (D10, nonlinear, screening at the floor); the HEDGEHOG wind runs start from them;
  the holds (KB2) test the code's own linear fixed point, which is the A2 solution of the linearised system (the nonlinear
  start drifts 17 % under the linear kernel over t 20, reported).
- The outer boundary of the FV operators is chi = Phi = 0 at r_out = 50 a (100 a for B3/B4); the readout error is
  O((a/r_out)^3). The inner face carries the body's enclosed-mass flux; the first cell's gradient is one-sided (49 % off there,
  1.4e-3 at r >= 0.1 a on coarse, 3.5e-4 on medium).
- B5's core cap is AC15's Bernoulli cap inside 2 R_A; for the extended galaxy bodies no core is excised (r_in = 0.05 a, inside
  the smooth Plummer core), and the printed cap(2R_A)/M_b of xf1_cells.json is not applicable to them.
- The hosted charge density rho_h is the host law field's phantom-inclusive dynamical density at the body (S1's Coma beta
  model; X1's Hernquist host; the QX10 X-COP and group profiles; AC12's Galactic Pi for the Sun); the B3 member mass
  (10^10.5 Msun stars + 20 % gas) and the B3/B4 Plummer scales are proxy assumptions; B3/B4 D is read at 10 kpc.
- The stiffness pressure acts on the fluid charge q, not on the tracer s (p(q + s) - p(q) <= 1e-9 of the inertia in every
  galaxy cell); for the Sun the HEDGEHOG start is AC15's fluid hedgehog, unchanged.
- Perpendicular g_ext NOT RUN (not axisymmetric), declared.
- One run (the Sun's no-wind hold) failed on a ghost-cell shape bug in the first launch and was rerun after the fix (the fix
  touches only the no-wind point-mass path; the diff is committed). The run list was regenerated once before the graded
  launch (B3/B4 HEDGEHOG removed, the dSph representative row set to Sextans, a reported D10 hold added); no graded number
  existed before the final launch.
- Beyond this lane: the same sweep would act on an ISOLATED galaxy moving through the cosmic khronon at its peculiar speed,
  where the record grades discs with a static khronon; the deceleration of the inflowing frame by the galaxy's own charge is
  marginal at MW mass (needs ln(r2/r1) ~ 3.6 of deep-MOND field) and impossible for dwarfs. Not graded here; a limit on the
  record's disc rows to be stated, not a result.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
