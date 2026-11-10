# TK1 (dust stiffness keyed on the clock's expansion): FROZEN CRITERIA, committed alone before any script, Lean file or number

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Both footings (canonical a0 9.3603e-11,
alt 1.1312e-10 m/s^2), never pooled. The cold component is cold dark energy (the clock's dust), never a particle. Not a
LCDM lane. No download. This lane edits nothing outside `closure_2026_11_10/TK1_expansion_keyed_dust/` (Lean files for
this lane live in this folder and are compiled with the in-repo build:
`cd fable_independent_2026/lean_2026 && lake env lean <absolute path>`).

Id check: `ls closure_2026_11_10/TK1*` found nothing; `git log --all --oneline | grep -c TK1` gave 0. The owner said
"Lane it now" for this construction on 2026-11-10. The construction came from an outside model's reply to the owner's
handoff (`CARBON_HANDOFF_2026-11-10.md`); it is restated here in this lane's own words and notation.

## 0. The question

MK1 found that no dust term depending on the clock offset Q - 1 alone can be stiff in the expanding background
(mu_K >= 2.51e4 per Mpc, the CMB-lensing Jeans line) and nearly inert in a static galaxy well (mu_K <= 1). The candidate
lets the stiffness depend on the clock congruence's expansion theta, which is 3H in the background and 0 in a static
well. Is the resulting action well posed, does a forming structure survive turnaround, and which of MK1's rows does it
move?

## 1. The candidate (frozen)

Notation as QX17 section 1 (c = 1 where not stated, K = 4 pi G, mostly-plus signature). theta := nabla_m n^m
(n_m = -d_m tau / Q); in unitary gauge theta is the trace of the leaves' extrinsic curvature, theta = 3H in FRW.
Action (A) with the dust term L_K = mu_K^2 (Q-1)^2 / (2K) replaced by

    L_K = M_2(theta) (Q-1)^2 / (2K),   M_2(theta) = mu_0^2 s^p + M_f^2,   s = theta^2 / (theta^2 + theta_0^2),

and nothing else changed (law sector, P stiffness gamma_L, multiplier, matter all as in (A)).

- **Primary (the proposal's values):** mu_0 = 3e4 per Mpc (physical), theta_0 = 0.1 H0/c, p = 2, floor M_f = 1e-3 per Mpc
  (the proposal's "residual floor"; read here as added to M_2; near theta = 0 this equals any max-type floor).
- **Brackets (reported, never label-setting):** theta_0 = 9 H0/c; p = 4; floor off (M_f = 0); each changed alone.
- H0 = 67.4 km/s/Mpc (KD1/QX15's h 0.674), so H0/c = 2.2482e-4 per Mpc. Background: Omega_d from KD1's I0 = 4.037e-8
  Mpc^-2 (Omega_d = I0 / (3 (H0/c)^2)), Omega_b = Omega_d / 5.41 (form B), radiation Omega_r h^2 = 4.15e-5, Lambda the
  rest (flat).
- The Part B barrier (proposal's term -M_f^2 (Q-1)^2 / (1 - theta^2/theta_c^2), theta_c = 1e-14 per s) is graded only if
  Part A is not structurally dead (section 4).

## 2. Part A items, in order. The lane stops at the first structural failure (A1 or A3) and reports it as the result

A4 and A5 are closed-form re-reads; they are computed and reported whatever A1-A3 give, but they set the label only if
A1 and A3 pass.

### A1 well-posedness (structural)

- **K1 khronon equation and current (sympy, jet variables).** Hand result to be checked: delta S = Int sqrt(-g) J^k d_k
  delta tau with J^k = F_Q n^k + h^{km} d_m F_theta / Q (F = L_K as a function of Q and theta), so the khronon equation is
  nabla_k J^k = 0 (plus (A)'s unchanged law-sector current), the charge along n is F_Q = M_2(theta)(Q-1)/K, and the
  new leafwise flux is h.grad(F_theta)/Q. Checked by a direct Euler-Lagrange variation in 1+1 with metric
  -e^{2A(t,x)} dt^2 + e^{2B(t,x)} dx^2, tau(t,x) free, F = (Q-1)^2 (m0 + m2 theta^2 + m4 theta^4): residual 0.
- **K2 matter and unitary-gauge kinetic structure (sympy).** (a) L_K contains no matter field (matter couples to g only),
  so matter's equations are those of (A). (b) In unitary gauge (tau = t, Q = 1/N) list every velocity L_K depends on:
  must be gamma-dot_ij only (no N-dot, no shift-dot); then matter and metric stay second order in time. (c) The velocity
  Hessian of EH + L_K: traceless part (1/4K) N sqrt(gamma); trace part h_tr = N sqrt(gamma) [-1/(6K) + F_thth / 2].
  Degenerate iff F_thth = 1/(3K), i.e. lambda_eff := -2K F_thth = -M_2''(theta)(Q-1)^2 = -2/3 (Horava's lambda = 1/3).
  Checked symbolically (residual 0).
- **K3 order of the khronon equation.** Highest derivative of tau in nabla.J, and its principal part (expected:
  4th order, coefficient F_thth (h^{ab} xi_a xi_b)^2 / Q^2: leaf-elliptic, i.e. an instantaneous mode, no new
  propagating characteristic). Reported with where the coefficient vanishes (type change).
- **K4 scalar quadratic action around flat FRW (sympy, unitary gauge).** gamma_ij = a^2 e^{2 zeta} delta_ij,
  N = N0 (1 + alpha), N_i = d_i psi, one Fourier mode; gravity + clock + Lambda (the law sector held at its FRW value
  P = 0, as the record's linear cosmology does; disclosed). Eliminate alpha and psi (auxiliary), giving
  L2 = A_z zeta-dot^2 - (B_z k^2/a^2 + C_z) zeta^2 after integrating the zeta zeta-dot term by parts. No-ghost: A_z > 0;
  gradient: c_s^2 = B_z / A_z at high k. Evaluated on the primary's FRW background at z = 3400, 1100, 10, 2, 0 (and on
  each bracket).
- **G-ratio.** G_cosmo / G_N - 1, with G_cosmo from the Friedmann equation's H^2 dependence of rho_K at fixed charge
  (G_cosmo = G / (1 - (8 pi G/3) d rho_K / d(H^2))), G_N from the static weak field (theta = 0); printed at z = 3400,
  1100, 0. Also lambda_eff(z).
- **A1 label:** WELL-POSED AROUND FRW if K1 and K2 residuals are 0, matter stays second order (K2 a, b), h_tr != 0 and
  A_z > 0 and c_s^2 >= 0 at every printed z in [0, 3400] on the primary. NOT WELL-DEFINED otherwise, naming the item and
  the z. (Behaviour away from FRW, at turnaround, is A3's item s2/s3.)

### A2 FRW limit (row, closed form)

- The component's w at z 3400 <= 0.01 (KD1 B1a) and mu_eff(z) := sqrt(M_2(3H(z))) >= mu_J = 2.512e4 per Mpc for every z
  in [0, 3400] (dominance: then the pressure-supported comoving band is no wider at any epoch than for the record's
  constant mu_J, so the record's CMB-lensing line is met). If mu_eff dips below mu_J at some z, the row reads NOT
  EVALUABLE (closed form cannot settle it) and min over z of mu_eff(z)/(1+z) is printed against mu_J/3401 = 7.39 per Mpc.
- Known answer: with M_2 constant the w(a) reduces exactly to MK1's w0/(w0 + a^3) (residual 0) and reproduces KD1's
  mu_B1a = 198.25 / 198.24 (relative 1e-4).
- Both footings (identical inputs here; printed twice).

### A3 turnaround (structural; the expected first kill)

- **Model.** A spherical top-hat as a closed FRW patch (homogeneous inside; edge effects not modelled, disclosed), with
  baryons and clock charge in form B's cosmic ratio, adiabatic, starting in the growing mode at z_i = 200. Inside a
  homogeneous patch A = 0, so P = 0 (no law, no phantom). Unitary gauge minisuperspace with N, a: the N-equation is the
  Friedmann constraint H^2 + k/a^2 = (8 pi G/3)(rho_b + rho_Lambda + rho_K), rho_K = Q F_Q + theta F_theta - F, with the
  charge n a^3 = a^3 F_Q conserved (K-identity: E + N dL/dN = -a^3 F_Q, sympy residual 0). Q - 1 = K n / M_2(theta)
  exactly. H (proper) is the root of the constraint at each a. Initial delta chosen so that pure dust (rho_K = n) turns
  around at z_ta = 5, 2, 1, 0.5 (the GR top-hat). Integration in proper time to t0 (the age) or to collapse.
- **Lines, read along the patch from z_i until it reaches a_ta / 2 on collapse (GR's virial radius) or t0:**
  - s1: Q - 1, rho_K or F_theta diverges at finite proper time;
  - s2: the velocity Hessian degenerates (h_tr = 0, lambda_eff = -2/3; K2 c) or the N-equation degenerates (F_QQ = 0);
  - s3: the K4 kinetic coefficient A_z (evaluated with the patch's local H, N0 and F derivatives; spatial curvature
    dropped at high k, disclosed) changes sign (ghost) or c_s^2 < 0 with growth rate > the patch's 1/t.
- **A3 label (per z_ta, primary):** SINGULAR if s1, s2 or s3 occurs (time, a/a_ta, theta/H0, Q - 1 and lambda_eff printed
  at the event). STALLS if none occurs but the patch does not reach a_ta / 2 by t0 (printed: a(t0)/a_ta, H(t0)).
  REGULAR otherwise, with the collapse time against GR's and max(Q - 1); flagged STRONG FIELD if max(Q - 1) > 0.1 (the
  weak-field readings of A4/A5 then do not hold inside forming structures). The lane's A3 label is the worst over the
  four z_ta. Footing-independent (a0 does not enter); printed for both.

### A4 static-well bookkeeping (reported; label-setting only if A1 and A3 pass)

With theta = 0 the dust part of the charge is M_2(0)(Q-1)/K = M_f^2 (Q-1)/K, negligible at Q - 1 ~ Phi/c^2, so the
static halo's charge must be the phantom D.P. Needed charge inside r: C_need(r) = M_b [nu(y) - 1] with the action's law
(mu(x) = x/(1+x), so g = g_N/2 + sqrt(g_N^2/4 + g_N a0)), and its deep form sqrt(M_b a0 / G) r (constant checked:
25,914 Msun/kpc canonical, brief's value, relative 1e-3, KA7). At log M_b 9.4, 10.45, 10.7, 10.9 and r = 100, 300 kpc,
per footing: C_need / M_b against (i) 5.41 (form B's cosmic share), (ii) PD1's cap 59.486 / 59.503 (ONE1), (iii) FLD1's
corrected arrival (1.6 to 5.1 % of the halo's charge inside 10-300 kpc at z 0; read as C_arrive <= 0.051 C_need).
HOLDS at (r, share) iff C_need <= share. Also printed: the dust charge the static well would need to hold if the
collapsed clock charge stayed as dust, Q - 1 = K n / M_f^2 at n = 200 and 5.41 x 200 times the mean baryon density.

### A5 rows (reported; label-setting only if A1 and A3 pass)

MK1's rows re-read at the environment's mu_eff (no re-run of MK1's machinery): static wells (X-COP, groups, SPARC, KiDS,
Saturn) have theta = 0, so mu_eff = M_f; the background rows use A2. A row passes iff mu_eff lies in MK1's allowed set
for that row and footing (MK1 RESULT table). X-COP's set is empty in MK1, so X-COP fails at any mu_eff. Linear growth:
delta M_2 / M_2 = (d ln M_2 / d ln theta) delta theta / theta printed at z = 3400, 1100, 2, 0, and f sigma8 / CMB lensing
read at closed-form level as "same as MK1's quadratic at mu_eff(z)" when |d ln M_2/d ln theta| < 1e-2.

## 3. Lane label (frozen)

Per footing, first that applies:
1. **NOT WELL-DEFINED** if A1 fails around FRW at the primary values.
2. **BREAKS AT TURNAROUND** if A3 is SINGULAR on the primary.
3. **STALLS AT TURNAROUND** if A3 is STALLS on the primary.
4. Otherwise from A2, A4, A5: **CLOSES MK1's GAP** if A2 passes, A4 HOLDS at both radii for share (ii) at all four
   masses, and every A5 row passes; **ROWS FAIL** otherwise, naming them.
5. **NO VERDICT** if any known answer fails.

Counts against the candidate (listed in RESULT.md whatever the label): any A5 row failing; A4 short at share (i);
STRONG FIELD in A3; G_cosmo / G_N - 1 above 1e-2 anywhere in [0, 3400]; mu_eff below mu_J at any z; a bracket that is
SINGULAR or STALLS when the primary is not (fragility).

## 4. Part B (only if Part A's label is 4)

The theta_c barrier: (B1) does a single-valued tau form the claimed shock, and where (claimed 0.642 R_ta), by the
minisuperspace patch with the barrier term added; (B2) does the static region reach KiDS's windows (FLD1: inner / middle
edge 362 / 849 kpc at log M_b 10.7; and at 9.4, 10.45, 10.9). B passes iff B1 gives a shock and R_static(z 0) >= the inner
window edge at all four masses. Not graded if Part A is structurally dead (labels 1-3); then RESULT.md says so.

## 5. Known answers (all must pass, else NO VERDICT)

- KA1: K1 residual 0 (covariant current vs direct variation).
- KA2: minisuperspace identity E + N L_N = -a^3 F_Q for generic F(Q, theta): residual 0; Friedmann form of the N-equation
  with rho_K = Q F_Q + theta F_theta - F: residual 0.
- KA3: M_2 constant: rho_K = n + K n^2 / (2 M^2), w = w0/(w0 + a^3) (MK1): residual 0; mu_B1a = 198.25 / 198.24 to 1e-4.
- KA4: F = -lambda theta^2 / (4K) (khronometric lambda-term): G_cosmo = G / (1 + 3 lambda / 2) from the same G-ratio
  code: residual 0.
- KA5: K4 with M_2 constant: A_z > 0 and c_s^2 = (Q-1)/Q (the k-essence dust's sound speed, c_s^2 = P_X/(P_X + 2 X P_XX)),
  relative 1e-6 at high k.
- KA6: A3 machinery with rho_K = n, Lambda = 0, Omega = 1 (EdS): linear delta at collapse (a_ta/2 in the closed patch is
  replaced here by the standard crunch-time reading t_coll = 2 t_ta) 1.686 to 1e-3; t_coll / t_ta = 2 to 1e-4.
- KA7: sqrt(Msun a0 / G) per kpc = 25,914 Msun/kpc (canonical) to 1e-3.

## 6. MUTATE (separate outputs; each must bite)

- MU1 (code): drop theta F_theta from rho_K. KA2's identity must fail (residual != 0), and A3's patch energy check
  (conserved n a^3 recomputed from the integrated trajectory) must drift by more than 1e-3.
- MU2 (physics arm, key off): M_2 = mu_0^2 constant. A3 must read REGULAR with collapse within 1e-3 of GR's time at every
  z_ta (if the primary is REGULAR too, MU2 must still move max(Q - 1) by a factor > 10).
- MU3 (code): drop F_thth from K4's quadratic action. KA4's analogue in K4 (lambda-term shifting A_z) must fail.
- Lean: `TK1.lean` (closed forms: charge identity in the homogeneous case, Hessian trace coefficient and its zero,
  rho_K's form, the A4 constant bound, the stall inequality if A3 needs it) compiles; `TK1_MUTATE.lean` states false
  versions, one per theorem, and must fail on every one.

## 7. Rules

Commits with explicit paths only; every message ends "Adopts nothing. kappa = 1/2 FITTED; not theory closed." Post hoc
changes go in AMENDMENT files committed alone before the affected number is computed (or marked post hoc if after).
Compute light (sympy and ODEs, one thread, no heavy runs). Push by replaying this lane's commits onto origin's tip
(merge-tree + commit-tree), no worktree, no rebase.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
