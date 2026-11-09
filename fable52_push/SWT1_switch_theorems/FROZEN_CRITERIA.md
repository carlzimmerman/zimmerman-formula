# SWT1 (switch theorems): FROZEN CRITERIA, committed alone before any SWT1 script, Lean file or graded number

TEST lane, quarantined. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings canonical (a0 9.3603e-11) and alt
(1.1312e-10 m/s^2), never pooled. A FAIL is verified as hard as a PASS. No LCDM input, no download, no new data. The closure
register and PAPER70 are not edited by this lane; labels of other lanes are not changed by it, only reported on.

## 0. What this lane is, and what it is not

It is not a new mechanism. It asks two class-level questions about **any switch on the law that comes from an action**, the class
the 2026-11-07 to 11-09 lanes keep grading one member at a time (WL1's multi-stream key, SQ1's component-density screen, BI1's
switched coupling, TS1's tidal switch).

The class. In the weak-field limit the law's sector is PAPER70 Eq. (A) at gamma_L = 0 after maximising over P:

    L = -|grad Phi|^2 / (8 pi G) + S J(|grad Phi|) - rho Phi,
    J(g) = (a0^2 / 4 pi G) [u - ln(1 + u)],  u = g / a0,  0 <= S <= 1.

S = 1 is the law (mu = u / (1 + u), nu(y) = 1/2 + sqrt(1/4 + 1/y)); S = 0 is Newton. A "variational switch" is any rule that makes
S a function or functional of other fields (a carrier's density, a stream count, a tidal invariant) inside this Lagrangian. The
field equation is div[(1 - S / (1 + u)) grad Phi] = 4 pi G rho, for every such rule.

**Q-CP (compensation).** WL1 stage 2 (criteria c371c8ce59, A1 bcaa90c6dc, result b8f52359c1) sums the phantom each host retains
inside R_ms and counts it as a lensing source at bias 1 ("q_pop", 0.936 / 1.079 at z 1 against a line of 0.0354), and states that
the kill "holds for any arm-(i) key". Is that statistic the large-scale lensing source of a variational switch?

**Q-WP (wall pressure).** SQ1 (criteria 7e8fa69c63, result e8880bf3c8) found, for one screening function and by shell integration,
that the switch's reaction on the component changes its density inside 3 Mpc by under 0.1 %. Is there a bound that holds for every
S and every key, and does it forbid a switch from keeping a settled component out of the radii where the galaxy gates forbid it?

## 1. Record checked before freezing

- "compensat", "negative shell", "surface layer", "Gauss": no hit in WL1, PD1, PD2. BI1 (2026-11-09) grades the reaction force of
  one switched coupling at a 1e-3-of-g line; it does not state a bound in closed form or the exterior monopole.
- SQ1's sign: the lane graded the source's stated Lagrangian (the component is attracted) and reported the opposite sign as a
  bracket; both changed the density by under 0.1 %.
- The crossover value 1 / (R (R + 1)) = 0.0288 is in CMB3's RESULT, in the z 1100 context. It is used here only as a lemma.
- L61 (2026-09-09) is the "excess spent once" theorem; KR1 closes barotropic clock fluids. Neither is re-derived here.

## 2. Disclosure: what I looked at and estimated before freezing

Made in this session, by hand, before this file. They are expectations, not results.

- Compensation: a spherical switched law gives r^2 g / G = M_b outside the switch radius, so the exterior phantom monopole is zero.
- Filling: with WL1's GSMF and radii I expect a volume filling of 0.2-0.3 at z 1 for WL1's graded reading L (statistic 0.4-0.6,
  FAIL by about 10-17x) and about 0.5 % for its self-consistent reading NC (statistic about 0.007, PASS).
- Wall pressure: I expect the closed form W(u) = u - ln(1 + u) - u^2 / (2 (1 + u)^2) in units of a0^2 / (4 pi G), with u the
  law's field just inside the wall; ratios to a settled component's pressure of about 0.03 at R200, 0.13 at 100 kpc and 0.4 at
  30 kpc for an L* lens; a clearing radius of 1-2 MOND radii (10-25 kpc); uncleared mass inside 200 kpc of about 1.2 M_b for the
  heaviest KiDS bin (line 0.9, a thin margin) and about 5 M_b for the lightest.
- Data look, no model compared: the 59 KiDS points (Brouwer+2021 Fig. 9 files on disk) have per-point errors of 0.04-0.16 dex.
  This is reported in the README only and enters no label.

## 3. Statements, checks and lines

### T1. Compensation (exact)

Spherical baryons M_b, S = 1 for r < R and 0 for r > R. Then the effective enclosed mass M_eff(r) = r^2 g / G is
M_b nu(y(r)) for r < R and exactly M_b for r > R, with y = G M_b / (r^2 a0). The switch surface carries a layer of
-M_b (nu(y(R)) - 1). Check: Lean (Section 6), plus KA-CP3.

### T2. The compensated large-scale statistic

For long-wavelength sources outside the law-on regions, each region responds as an inclusion with the law's incremental
permittivity around its own radial field: radial mu_r = u (2 + u) / (1 + u)^2, tangential mu_t = u / (1 + u), with
u(r) = nu(y) y for a point M_b.

- Polarizability: alpha = (Lambda - 1) / (Lambda + 2), Lambda = mu_r(R) R f'(R) / f(R), where f solves
  (r^2 mu_r f')' - 2 mu_t f = 0, regular at the centre. The insulating limit alpha = -1/2 is the bracket.
- Maxwell-Garnett: beta = sum n V alpha, mu_M = (1 + 2 beta) / (1 - beta), **q_C = 1 / mu_M - 1**. Used only for a filling
  f_V = sum n V <= 0.30; above that the reading is recorded NOT DILUTE and its q_C is taken as at least the value at 0.30
  (q_C rises with f_V; Lean states the bound q_C <= (3/2) f_V / (1 - f_V)).
- Form factor (reported, added in absolute value): q_ff(k) = sum n M_ph(<R) u~(k R) / rho_d at comoving k = 0.1 / Mpc, u~ the
  transform of the retained phantom minus its surface layer.
- Inputs exactly as WL1 stage 2: background OB 0.0215, OD 0.11958060485606123, H0 65, radiation 4.15e-5; Driver+2022 GSMF from
  closure_program_2026_10_27/population/inputs.json, log M* 9-12, M_b = M*, the z = 0 GSMF at every z; WL1's shell solver,
  transcribed. Proper number density n (1 + z)^3 with physical radii.
- Readings: **L** (law-on turnaround, baryons only; WL1's graded stage-2 reading), C (ceiling), NC and NL (self-consistent:
  Newtonian collapse outside the switch). z = 1 graded, z = 0.5 and 2 reported.
- **Line:** q_C + |q_ff| <= 0.0354, WL1's own line, per reading and footing.
- Reported beside it: the filling needed to keep the law on out to 0.43, 1.0 and 2.8 Mpc for every lens with log M* >= 9.4.

### T3. Wall pressure (exact) and the self-clearing gate

- **Identity.** At fixed displacement y (the Newtonian field of the sources at the wall, in units of a0), the outward force per
  unit area on whatever carries the switch, across a wall where S falls from 1 to 0, is
  p_wall = integral_0^1 J(u(S, y)) dS = (a0^2 / 4 pi G) W(u_1), W(u) = u - ln(1 + u) - u^2 / (2 (1 + u)^2), u_1 = nu(y) y.
  Equivalently p_wall = (a0^2 / 8 pi G) F(y) with F' = 2 y (nu - 1). The sign is fixed by the law being attractive: a carrier that
  lowers S is pushed out of high-field regions. For S falling only part of the way the force is smaller.
- **Bounds.** 0 <= W <= y and W <= (2/3) y^(3/2).
- **Gate (self-clearing).** The carrier is the cosmic share R M_b (R = OD / OB) placed as generously to clearing as the record
  allows: a singular isothermal sphere out to WL1's self-consistent radius R_h = R_ms^NC(M_b) (0.13-0.83 Mpc), isotropic, at rest
  in the filled Newtonian state g = G (M_b + M_d(<r)) / r^2, pressure from the Jeans equation with p(R_h) = 0.
  - Clearing radius r_c: the largest r <= R_h with p_wall(y(r)) >= p_d(r), 0 if none.
  - Uncleared mass inside 200 kpc: M_unc = M_d(< min(200 kpc, R_h)) - M_d(< min(r_c, 200 kpc, R_h)).
  - **Line:** M_unc <= 0.9 M_b, the record's F2 figure for isolated lenses inside 200 kpc (PAPER70 closing statement, item 3).
  - Masses: KiDS's four bins, log M_b 9.4, 10.45, 10.7, 10.9, point baryons.
- Reported, not graded: r_c in MOND radii; the ram-pressure bracket rho_d v_ff^2; the ratio p_wall / p_d at 0.1, 0.3 and 1 R_h
  for a group (M_b 3e12, R_h 0.45 Mpc) and a cluster (M_b 1.4e14, R_h 1.4 Mpc) with baryons enclosed in proportion to r; the
  share fraction at which M_unc meets the line.

### T4. Crossover lemma (Lean only, no label)

nu(y) = 1 + R exactly when y = 1 / (R (R + 1)); mu(g / a0) = 1 / (1 + R) exactly when g = a0 / R.

## 4. Labels

- **SWT1-CP**
  - KEY-DEPENDENT: reading L fails the compensated line and NC or NL passes it, on both footings. Then WL1's FAIL stands on its
    graded reading, and its scope sentence ("any arm-(i) key") does not hold for variational switches.
  - KEY-INDEPENDENT: every reading fails the compensated line on both footings. WL1's scope sentence stands.
  - WL1 LABEL MOVES: reading L passes the compensated line on a footing. Reported to the owner; this lane relabels nothing.
  - MIXED: anything else, stated per footing.
- **SWT1-WP**
  - SELF-CLEARING NO-GO: M_unc > 0.9 M_b for all four masses on both footings.
  - NOT A NO-GO AS FROZEN: otherwise, with the masses that clear named.
- **NO VERDICT** on a label if a known answer it rests on fails, or if T1 (for CP) or T3's identity (for WP) is not certified.

## 5. Known answers

- KA-CP1: the transcribed solver reproduces WL1's q_pop at z 1 on its own statistic: L 0.936 / 1.079 and NC 0.384 / 0.423,
  within 1 %.
- KA-CP2: the polarizability solver returns (mu - 1) / (mu + 2) for a uniform inclusion with mu = 0.1, 0.5, 2, to 1e-6.
- KA-CP3: a smooth spherical switch (tanh, width 0.02 R) solved numerically gives r^2 g / G = M_b beyond 1.2 R to 1e-6.
- KA-W1: W equals the quadrature of integral_0^y (nu(t) - 1) t dt at y = 1e-6, 1e-3, 0.1, 1, 10, 1e4, relative 1e-8.
- KA-W2: W / ((2/3) y^(3/2)) is within 2e-3 of 1 at y = 1e-6; W / y is within 2e-3 of 1 at y = 1e4.
- KA-W3 (independent derivation): for a Plummer sphere of baryons, the full Lagrangian (field term, S J term and source term
  -rho Phi, all by quadrature) differenced in the switch radius R equals 4 pi R^2 p_wall(y(R)), relative 1e-5, with the
  outward sign.

## 6. Lean (compiled from the copy that still has its Mathlib build; `lake env lean`, standard axioms only)

Statements to certify: T1 (interior, exterior and layer); the law solves mu(u) u = y at u = nu(y) y; T3's identity (the Legendre
combination equals W); W's derivative u^2 (2 + u) / (1 + u)^3 and dW = (u - y) dy; W >= 0; W <= y; W <= (2/3) y^(3/2) (stated in
t = sqrt(1 + u)); alpha >= -1/2 for Lambda >= 0; q_C <= (3/2) f / (1 - f) and the filling line; T4.
A statement that cannot be proved is listed NOT CERTIFIED, with its numerical known answer beside it; the labels need T1 and
T3's identity certified. A MUTATE twin with false versions must fail to compile.

## 7. MUTATE

- M-CP: drop the compensation (count the retained phantom as exterior mass): must reproduce WL1's stage-2 FAIL on every reading.
- M-W: flip the sign of the S J term: KA-W3's force must change sign.
- M-WP: divide the carrier's pressure by 100: the no-go must fail for at least one mass.
- Lean twin, as above.

## 8. Operational

One thread, under 1 GB, minutes. Files: swt1.py, swt1.json / .out, swt1_MUTATE.json / .out, SWT1.lean, SWT1_MUTATE.lean,
compile.txt, compile_MUTATE.txt, RESULT.md. Commits with explicit paths only. The orchestrator registers; this lane does not.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
