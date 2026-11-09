# SNP1 (snowplow clearing): FROZEN CRITERIA, committed alone before any SNP1 script, Lean file or graded number

TEST lane, quarantined. Adopts nothing. Relabels nothing in the record. Not registered. Footings canonical (a0 9.3603e-11) and
alt (1.1312e-10 m/s^2), never pooled. No LCDM input, no download, no new data. Does not edit fable52_push/README.md, PAPER70,
the closure register or any other lane's files.

## 0. Question

SWT1 (fable52_push/SWT1_switch_theorems) proved that any action-based switch on the law pushes its carrier out of law-on regions
with p_wall = (a0^2 / 4 pi G) W(u), W(u) = u - ln(1 + u) - u^2 / (2 (1 + u)^2), u the law's field just inside the wall, and that
this beats the static pressure of the record's cosmic share around galaxies (T3, NOT A NO-GO AS FROZEN). It did not show that the
share is actually removed: the swept-up component must be carried, and its weight held, over cosmic time (README item 3).

SNP1 asks: **can the law's own wall pressure clear the cold component from around galaxies, dynamically, and so deliver the
two-phase reading?** Spherical, one galaxy, a thin swept-up shell, in the record's expanding background.

## 1. Record checked before freezing

- Id free: `ls -d fable52_push/SNP1*` finds nothing; `git log --all --oneline | grep SNP1` finds nothing.
- Read: SWT1 FROZEN_CRITERIA, AMENDMENT_A1, RESULT, swt1.py, swt1_extra.py, SWT1.lean; fable52_push/README.md; the GAL1
  hand-over note in the shared session notes (tighter filling allowance 0.0197 at switch-on z 3; reported here only, the frozen
  line below is SWT1's 0.0354 statistic).
- SWT1 E2 (reported there): the same share confined to R_h / 4 leaves 0.7-2.0 M_b inside 200 kpc. SQ1 graded one local density
  screen, not a wall force at the wall.

## 2. Disclosure: hand estimates made before freezing (expectations, not results)

Units: r_M = sqrt(G M_b / a0) (canonical 1.93 / 6.48 / 8.64 / 10.9 kpc for log M_b 9.4 / 10.45 / 10.7 / 10.9; alt x 0.910);
v_f^4 = G M_b a0; F_w = 4 pi R^2 p_wall = a0 M_b W(u) / y.

- **A.1.** F_w <= a0 M_b and F_w <= (2/3) a0 M_b sqrt(y) follow at once from SWT1's W <= y and W <= (2/3) y^(3/2). By hand I
  also find u^3 / (2 (1 + u)^2) < W(u) < u^3 / (1 + u)^2 for u > 0 (derivatives u^2 / (2 (1 + u)^2) and u^2 / (1 + u)^3), i.e.
  (1/2) a0 M_b mu(u) < F_w < a0 M_b mu(u), mu = u / (1 + u).
- **A.2.** For a shell of fixed mass m M_b, equilibrium is W / y^2 = k, k = m (1 + m / 2). The lower bound on W makes
  Psi(u) = W (1 + u)^2 / u^4 strictly decreasing, so the equilibrium is unique and **unstable** (the proposer's hand algebra
  agrees): inside R_eq the shell falls, outside it is expelled. Deep limit R_eq = (3/2) k r_M; in general
  sqrt(k (k + 1)) < R_eq / r_M < sqrt(2k (2k + 1)). For the record's share (m = R = 5.5619, k = 21.03): R_eq ~ 31.5 r_M =
  61 / 204 / 272 / 343 kpc canonical. For X = 3 (k = 156): ~234 r_M, 0.45-2.5 Mpc.
- **A.3.** Swept mean background: F_w is strictly decreasing in R (upper bound on W) and the weight strictly increasing, so the
  balance is unique and **stable**. Static balance at today's mean density (no IGM baryons, deep form):
  0.73 / 1.5 / ~1.8 / 2.0 Mpc for the four masses, i.e. 1.46 / 0.89 / ~0.80 / 0.72 of R_K = sqrt(G M_b / 1.38e-15).
  Scaling R ~ (M_b v_f^2 / G rho^2)^(1/5) ~ M_b^0.3, which reproduces the proposer's 2.3 Mpc (M_b / 1e11)^0.3. I therefore
  expect G-K to **fail** for the two heaviest bins (the proposer expected a narrow pass), unless the dynamics carry the wall
  1.1-1.4x past the static balance.
- **Sweeping the bound share (deep, static, no expansion).** Resistance / F_w = (3/2) (r_M / R_h) s (3/2 + s x) with
  s = X R, x = R / R_h: the quasi-static stall is at x_s = [(2/3) (R_h / r_M) / s - 3/2] / s, and with momentum carried the shell
  stops at ~2 x_s. Break-out of the share needs R_h,n / r_M >~ (3/2) s (3/2 + s / 2): ~36 for X = 1, ~250 for X = 3. Interpolating
  SWT1's printed NC radii (z 1 and 2; z 3 and 6 extrapolated, unverified) gives R_h,n / r_M ~ 45 / 26 / 14 at z_n 1.5 / 3 / 6 for
  log M 10.45. So: X = 1 breaks out only for z_n = 1.5; X = 3 never.
- **Elastic front, no gravity:** comoving front x^(5/2) = (5/2) v_f sqrt(M_b / (12 pi rho_d0)) Delta eta, ~1.0-1.2 Mpc today for
  log M 10.45; same M_b^0.3 scaling.
- **Expected outcome.** X = 1, z_n 6 and 3: the wall stalls inside the share, G-F2 FAIL (~5 M_b inside 200 kpc), G-K FAIL,
  G-L PASS. X = 1, z_n 1.5: break-out, G-F2 PASS, G-L at z 1 small (the wall is young) and may PASS, G-K decides (expected FAIL
  for the heavy bins). X = 0: G-F2 PASS, G-K FAIL heavy bins, G-L FAIL or marginal. X = 3: G-F2 FAIL. **Expected label FAILS /
  FAILS**, failing gate G-K at every z_n, G-F2 at z_n 6 and 3. Energy-conserving bracket: same label.
- Structural note (from SWT1's numbers, not a gate): G-K at z 0 forces a z 0 filling >= 0.29; G-L at z 1 then needs the bubbles'
  comoving radius to grow ~2.3x between z 1 and z 0. A swept bubble grows ~a^0.2 comoving; only a wall that nucleates late can
  meet both.

## 3. Model (frozen; changed only by a committed amendment)

### 3.1 Inputs taken from swt1.py (imported by executing its library part, as swt1_extra.py does)

Constants and background (G, MS, MPC, KPC, OB 0.0215, OD 0.11958..., H0 65, radiation 4.15e-5 h^-2, flat, Lambda; Hs(a),
RHO_M0, RHO_D0, R = OD / OB = 5.5619), the shell solver `shell` / `r_ta` and the reading `Rms`, the law `u_in`, `Wfun`,
`p_wall`, the GSMF grid LG (log M 9.0-12.0, step 0.25), `compensated`, and LINE = 0.0354. rho_b(a) = OB h^-2 rho_crit / a^3,
rho_d(a) = RHO_D0 / a^3, rho_Lambda and rho_r from the same background.

### 3.2 Galaxy, wall, carrier

- Point baryons M_b. Masses: KiDS's four bins log M_b 9.4, 10.45, 10.7, 10.9 (G-F2, G-K) and the GSMF grid LG (G-L).
- **Wall.** The law is on inside the wall radius R_w and there is no cold component there. R_w is the inner edge of the cold
  component. The outward force on the carrier at the wall is F_w(R) = 4 pi R^2 p_wall(y), y = G M_b / (R^2 a0).
- **Nucleation.** At a_n = 1 / (1 + z_n), z_n in {6, 3, 1.5}, the wall appears at R_0 = r_M (per footing).
- **Bound region** r < R_h,n := Rms("NC", M_b, 0, a_n), the record's self-consistent radius at the nucleation epoch, the same for
  every X (as SWT1's share-multiple bracket kept R_h fixed). Cold density rho_B(r) = X R M_b / (4 pi R_h,n r^2) + rho_d(a_n):
  the share as SWT1 placed it (singular isothermal) plus the cosmic mean at nucleation, static (mean radial velocity zero, fixed
  physical radii) until swept, with A1's local isothermal pressure p_B(r) = rho_B(r) G (M_b + M_B(<r)) / (2 r), M_B(<r) the
  bound cold mass inside r. X in {0, 1, 3}; **X = 1 is graded**; 0 and 3 are brackets. (Including the mean adds about 1 M_b to
  what SWT1's carrier held: conservative. For X = 0 the bound region holds the mean at nucleation only.)
- **Unbound background** r > R_h,n: cold component at the cosmic mean rho_d(a) (the record's uniform-background convention),
  pressureless, radial velocity v_bg(r, a) of the record's shell equation (Newtonian, excess dM_X = M_b (1 + X R)):
  Lagrangian elements started in Hubble flow at z 1000 exactly as `shell` starts them, 160 comoving labels log-spaced over a range
  that covers every radius the runs reach, followed through turnaround until r < 1 kpc or a = 1; v_bg(r, a) by interpolation
  across the elements still above 1 kpc at that a (below the innermost one: its velocity; beyond the outermost: Hubble flow
  H(a) r). The unbound medium is never swept back into the bound region (infall onto the bound region outside the wall is not
  tracked: generous to G-F2, disclosed).
- **IGM baryons** stay uniform at rho_b(a) everywhere, are not swept and gravitate.
- **Gravity** on a body at r (absolute form): g = -G [M_b + (4 pi / 3) rho_b(a) r^3 + M_c(<r)] / r^2 + (8 pi G / 3) (rho_L -
  rho_r(a)) r, M_c(<r) the cold mass inside r, a thin layer's own mass counted half. With M_c the uniform mean plus dM_X - M_b
  this is the record's shell equation.

### 3.3 Graded dynamics: sticky (momentum-conserving) snowplow

Thin shell (R, V, M_s); initial R_0 = r_M, V_0 = 0, M_s,0 = M_B(<R_0).

    d(M_s V)/dt = F_w(R) + M_s g_s(R) - 4 pi R^2 p_ext + Mdot_s v_ext,   Mdot_s = 4 pi R^2 rho_ext max(V - v_ext, 0),
    g_s = -G [M_b + (4 pi / 3) rho_b R^3 + M_s / 2] / R^2 + (8 pi G / 3) (rho_L - rho_r) R.

The medium just outside the shell: the bound region while the shell is at its swept front (R = R_max,B < R_h,n): rho_B, v = 0,
p_B; the unbound background for R >= R_h,n: rho_d(a), v_bg, p = 0; nothing while the shell is inside a region it has swept
(R < R_max,B). Stall: at the bound front with V = 0 and 0 <= F_w + M_s g_s <= 4 pi R^2 p_B the shell is held (it can neither
advance nor detach); it resumes when F_w + M_s g_s exceeds 4 pi R^2 p_B and detaches inward when F_w + M_s g_s < 0. Collapse:
R < 0.1 r_M ends the wall (R_w = 0 from then on; its mass is cold inside every radius). Integrated in ln a with LSODA segments
and events at every switch of medium or state.

### 3.4 Reported bracket: energy-conserving ("each layer receives the impulse and then moves freely")

Same medium, gravity, F_w and nucleation. No mass sticks to the wall.
- **Front** R_f = inner edge of the unswept medium. While it is the innermost cold it advances as an elastic piston:
  bound: dR_f/dt = sqrt(max(p_wall - p_B, 0) / (2 rho_B)) (the bound edge holds where p_wall <= p_B and never flows inward:
  generous, disclosed); unbound: dR_f/dt = v_bg + sqrt(p_wall / (2 rho_d)). Material it crosses is ejected at
  2 dR_f/dt - v_ext (elastic reflection in the front's frame), which is the work p_wall dV turned into kinetic energy.
- **Free layers.** Ejected material is binned into layers of mass max(0.02 M_b, 0.03 x the mass ejected so far), collisionless
  (they pass through each other and through unswept material), each under g with its own mass counted half.
- **Innermost rule.** When a free layer is inside R_f and is the innermost cold, it, and only it, receives F_w (on top of g); the
  front then does not advance (bound edge holds; unbound edge moves with v_bg without ejecting).
- A free layer below 0.1 r_M joins a central point mass (cold inside every radius; it does not define the wall: generous,
  disclosed). The initial bound mass inside R_0 is one free layer at rest at R_0.
- R_w = innermost cold radius; R_w and the cold mass inside 200 kpc are averaged over the last Delta ln a = 0.05 before each
  output epoch (bounces). KDK leapfrog with adaptive steps.
- Grid: the four KiDS masses for every (X, z_n) and footing, and the GSMF grid for every (X, z_n) and footing. Pre-registered
  contingency: if the E-bracket's projected runtime exceeds 30 minutes, its G-L uses every other GSMF mass with log R_w
  interpolated linearly in log M, decided before any E-bracket G-L number is printed.

## 4. Gates (per footing, per (X, z_n), per bracket)

- **G-F2.** Cold mass inside 200 kpc (physical) at z 0 <= 0.9 M_b for all four KiDS masses (the record's F2 figure, as SWT1 T3
  used it). Counted: the shell (or free layers / central mass) inside 200 kpc, unswept bound material inside 200 kpc, unbound
  mean inside 200 kpc beyond the cleared region.
- **G-K.** R_w(z 0) >= R_K = sqrt(G M_b / 1.38e-15 m/s^2) for all four masses. Reported: R_w / R_K per bin and how many of the
  59 points of real_research/data/lensing_rar/brouwer2021_rar/Fig-9_RAR-KiDS-isolated_Massbin-[1-4].txt (loaded as swt1_extra.py
  loads them; radius sqrt(G M_b,bin / g_bar)) lie outside the wall.
- **G-L.** The GSMF population with bubble radii R_w(M, z) (physical; a mass with no wall at that epoch, not yet nucleated or
  collapsed, gets a 1 kpc placeholder) through swt1's `compensated`: q_C + |q_ff| <= 0.0354 at **z 1 (graded)**; z 0, 0.5 and 2
  reported. SWT1's NOT DILUTE rule is inherited. GAL1's tighter 0.0197 filling allowance is quoted beside it, never graded.

## 5. Labels (per footing)

- **SNP1 (graded: sticky snowplow, X = 1):**
  - **DELIVERS** if for at least one z_n in {6, 3, 1.5} G-F2, G-K and G-L all pass (the z_n named).
  - **FAILS** otherwise, with the failing gates named for each z_n.
  - **NO VERDICT** if any known answer KA-1 to KA-6 fails.
- **Robustness suffix:** the E-bracket at X = 1 is graded the same way. If its DELIVERS / FAILS verdict differs from the sticky
  one, the label carries "HINGES ON THE STICKY IDEALISATION"; if it agrees, "SAME UNDER THE ENERGY-CONSERVING BRACKET", with any
  gate whose verdict differs listed.
- **Brackets X = 0 and X = 3:** same form, reported beside the label, never the lane label. A DELIVERS at X = 0 only would read
  "delivers only if the share was never bound".

## 6. Part A, exact statements (Lean, in the style of SWT1.lean; standard axioms only)

W, mu, nu as in SWT1; F_w / (a0 M_b) = W(u) (1 + u) / u^2 at y = u^2 / (1 + u); R / r_M = sqrt(1 + u) / u.
- A1a  F_w <= a0 M_b. A1b  F_w <= (2/3) a0 M_b sqrt(y) (stated in t = sqrt(1 + u)). A1c  (1/2) mu < F_w / (a0 M_b) < mu, from
  u^3 / (2 (1 + u)^2) < W < u^3 / (1 + u)^2 (u > 0). A1d  a shell whose weight exceeds a0 M_b has a net inward force.
- A2a  Psi(u) = W (1 + u)^2 / u^4 is strictly decreasing on u > 0 (derivative given). A2b  Psi(u) = k > 0 implies
  1 / (2k) < u < 1 / k, hence k (k + 1) < (R_eq / r_M)^2 < 2k (2k + 1). A2c  instability: net outward force y (Psi(u) - k) is
  positive outside R_eq and negative inside. A2d  deep closed form: with W = (2/3) y^(3/2), R_eq = (3/2) k r_M.
- A3a  Phi(u) = W (1 + u) / u^2 strictly increasing on u > 0, so F_w strictly decreases with R (u_in increasing in y is also
  stated). A3b  the swept weight G (4 pi / 3) rho R (M_b + (2 pi / 3) rho R^3) strictly increases with R; a strictly decreasing
  force meeting a strictly increasing weight has a unique, stable balance. A3c  deep limits of the swept balance:
  R = v_f / sqrt(2 pi G rho) (M_s << M_b) and R^5 = 3 M_b v_f^2 / (4 pi^2 G rho^2) (M_s >> M_b), as algebra from
  F = (2/3) M_b v_f^2 / R.
- B1  a sticky merge conserves momentum and loses (1/2) M m (V - v)^2 / (M + m) >= 0 of kinetic energy; B2  reflection off a
  wall moving at V (v' = 2V - v) keeps the speed in the wall's frame.
- Numbers reported with Part A: R_eq for X = 1 and 3 (closed form and exact root) at the four masses, both footings; swept
  balance at today's mean density with and without IGM baryons, and as a fraction of R_K.
- Any statement that cannot be proved is listed NOT CERTIFIED beside its numerical check; Part A labels nothing in Part B.

## 7. Known answers (all must pass; otherwise NO VERDICT)

- **KA-1** F_w = a0 M_b W(u) / y against 4 pi R^2 swt1.p_wall(y) at 20 radii (relative 1e-12), and against
  a0 M_b (1 / y) integral_0^y (nu(t) - 1) t dt by quadrature (relative 1e-8).
- **KA-2** My integrator (ln a stepping, the absolute gravity of 3.2 with the uniform mean plus dM, wall off) bisected over
  labels reproduces swt1.r_ta(dM, 0, a) for dM = M_b (1 + R) at a = 1 and 0.5, log M_b 9.4, 10.45, 10.9, relative 1e-4.
- **KA-3** Statics: the exact root of Psi(u) = k lies inside A2b's bracket for k in {0.01, 0.1, 1, 10, 21.03, 155.9, 1e3}; at
  k = 1e4 it matches (3/2) k r_M to 1e-3; the shell equation (M_b and M_s gravity only, no background, no sweeping) started at
  rest at 0.99 R_eq falls inward and at 1.01 R_eq moves outward.
- **KA-4** Snowplow step against the analytic case (static uniform medium, no gravity, no wall, M_0, V_0):
  t(R) = [M_0 (R - R_0) + (4 pi / 3) rho ((R^4 - R_0^4) / 4 - R_0^3 (R - R_0))] / (M_0 V_0), relative 1e-6 at five times, and
  M_s V conserved to 1e-8.
- **KA-5** Energy-conserving bracket against the elastic piston (no gravity, no expansion, constant p on a static uniform
  medium): front speed sqrt(p / (2 rho)) and ejecta speed twice it to 1e-3; ejecta kinetic energy equals the work
  integral p 4 pi R^2 dR to 1e-3.
- **KA-6** Transcription: `compensated` on the NC table at z 1 returns SWT1's 0.0180 / 0.0182 within 1e-3 absolute; the KiDS
  loader returns 59 points.

## 8. MUTATE (separate outputs snp1_MUTATE.json / .out; sticky model, X = 1, every z_n, both footings)

- **M-OFF** F_w = 0: G-F2 must FAIL for all four masses.
- **M-SIGN** F_w -> -F_w: the wall must collapse (R_w(z 0) = 0) for all four masses.
- **M-x100** F_w x 100: R_w(z 0) must rise at least 2x for each of the four masses (a graded collapse counts as R_w = 0, so any
  wall then counts as a rise).
- **Lean twin** SNP1_MUTATE.lean with false versions (reversed lower bound on W, F_w <= a0 M_b / 2, Psi increasing, the
  equilibrium below 1 / (2k), energy gained in a sticky merge) must fail to compile.

## 9. Reported, never graded

R_0 = 0.3 and 3 r_M (sticky, X = 1, four masses); a pressureless bound share (p_B = 0; sticky, X = 1, four masses); shell mass,
velocity, stall / collapse / break-out flags and epochs; filling against GAL1's 0.0197.

## 10. Operational

One thread, under 1 GB, minutes. Files: snp1.py -> snp1.json / .out; snp1_MUTATE.json / .out; SNP1.lean, SNP1_MUTATE.lean,
compile.txt, compile_MUTATE.txt (no home paths); RESULT.md with the label first and a table per gate. Commits with explicit paths
only; pushed via a temporary sparse worktree. Not registered.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
