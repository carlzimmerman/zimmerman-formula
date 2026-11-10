# TK1 RESULT: dust stiffness keyed on the clock's expansion theta (2026-11-10)

**Label, canonical and alt: BREAKS AT TURNAROUND.** The same under AMENDMENT A1.

The key does what it was built for in the expanding background: the action stays well posed around FRW, and the dust is
stiff there (Jeans line met with a margin of 1.19). It fails where every forming structure goes: through turnaround.
- As a collapsing region slows down, its expansion rate falls through theta_0. There the stiffness function bends the
  other way (M_2'' changes sign), and the new term's k^4 piece makes short waves grow without bound.
- This happens 2 to 140 Myr before the GR turnaround on the primary values, at every turnaround redshift tried (z 5, 2,
  1, 0.5). By then waves of 0.5 to 4 kpc already grow faster than 1/t.
- Then the region does not turn around at all. The clock's energy density at fixed charge goes as 1/M_2(theta), and that
  diverges as the expansion goes to zero. So the region hangs at its turnaround radius: today it sits at 1.00004 to
  1.00016 of that radius, still expanding at about 1e-4 H0. Nothing collapses within the age of the universe.

So the key removes MK1's contradiction in the background and replaces it with a worse one: no bound structure forms.

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled (a0 enters only A4
and A5; A1-A3 use the same inputs on both footings and are printed twice). Part B (the theta_c barrier) was **not
graded**: the criteria grade it only if Part A is not structurally dead.

Commits (local / origin): criteria 98f2ab2b6e / a1ea8af5d1 (alone, before any script or number); AMENDMENT A1
813946cec9 / 175bea03be (post hoc, alone, before the graded A3 runs); result 6279d7f0c2 / 87fd33a27b.

## Table (canonical / alt where they differ; primary values unless a bracket is named)

| item | verdict | numbers |
|---|---|---|
| A1 K1: khronon equation and current (sympy, jets, 1+1) | **PASS** | J^k = F_Q n^k + h^{km} d_m F_theta / Q; residual vs direct Euler-Lagrange <= 6.2e-40 (6 random jets, 40 digits). Charge along n = F_Q = M_2(theta)(Q-1)/K; new leafwise flux h.grad(F_theta)/Q |
| A1 K2: matter and unitary-gauge kinetic structure | **PASS** | L_K has no matter field; in unitary gauge theta = K_ADM exactly (for N > 0) and depends on gamma-dot only (not N-dot, not shift-dot), so matter and metric stay second order in time. Velocity Hessian: traceless 1/(8 K N a), trace (3 K F_thth - 1)/(4 K N a): degenerate iff lambda_eff = -2 K F_thth = -2/3 (residual 0) |
| A1 K3: order of the khronon equation | reported | 4th order in tau; principal symbol = sqrt(-g) F_thth (h^{ab} xi_a xi_b)^2 / Q^2 (ratio 1.000000000000000 at 5 of 6 random jets; one jet had h xi xi = 0, 0/0). Zero only for xi along n: a leaf-elliptic, instantaneous mode, no new propagating cone. Its coefficient changes sign where M_2'' = 0 |
| A1 K4: scalar quadratic action around flat FRW | closed form | A_z = (3K F_QQ F_thth - 3K F_Qth^2 - F_QQ) a^5 / (4 N0 Den), Den = K^2 (F_QQ F_thth - F_Qth^2) a^2 + 2K F_Qth a a-dot + (3K F_thth - 1) a-dot^2; no k dependence. Gradient g4 k^4 + g2 k^2 + g0 with g4 = F_thth N0^3 a / (4 Den) |
| A1 on FRW, z 0 to 3400 | **WELL-POSED** | A_z > 0 and g4/A_z > 0 on a 140-point log grid; dust c_s^2 = (Q-1)/Q (8.8e-7 at z 3400, 2.2e-17 today) |
| G_cosmo / G_N - 1 | negligible | at most 2.0e-19 in size (-5.0e-20 at z 3400, -2.0e-20 today); lambda_eff 1.3e-20 to 1.3e-19. G_N: at theta = 0, F_thth = 0 (p = 2), so the static weak field is action (A)'s with mu_K = M_f |
| A2 FRW limit | **PASS** | w(z 3400) = 4.4e-7 (line 0.01); mu_eff = sqrt(M_2(3H)) >= 2.997e4 per Mpc for all z in [0, 3400] (minimum today), against mu_J 2.512e4: ratio 1.193. d ln M_2 / d ln theta = 4.4e-3 today, smaller earlier |
| **A3 turnaround** | **SINGULAR** at all four z_ta | see the A3 table: the gradient line s3 fires first (lambda_eff < 0, k^4 term unstable), 2.4 / 19.5 / 64.9 / 141 Myr before GR's turnaround (z_ta 5 / 2 / 1 / 0.5). The frozen s2 (Hessian degenerate) follows 0.02 / 0.14 / 0.45 / 0.85 Myr before it. No collapse by t0 on any track |
| A4 static-well charge (reported) | short of form B's share | the law's halo needs 8.7 to 155 M_b (canonical; 9.6 to 170 alt) inside 100 / 300 kpc: short of 5.41 M_b at 8 of 8 points (x1.6 to x29 canonical, x1.8 to x31 alt); within PD1's 59.5 cap at 7 of 8 (not log M_b 9.4 at 300 kpc). FLD1's corrected arrival is <= 5.1 % of the need |
| A5 MK1's rows re-read (reported) | X-COP and groups fail | in a static well theta = 0, so mu_eff = M_f = 1e-3 per Mpc: SPARC (<= 7.08 / 5.62), KiDS capped (<= 1.00 / 0.765), Saturn (<= 6.2e3) pass; groups need 0.912-1.514 / 0.759-1.380: FAIL; X-COP has no value in MK1: FAIL. CMB rows pass (mu_eff 3.0e4) |
| Part B (theta_c barrier, 0.642 R_ta, KiDS windows) | NOT GRADED | Part A is structurally dead |
| Known answers KA1-KA7, KA-K4 | 10 of 10 PASS | below |
| MUTATE MU1, MU2, MU3 | all bite | below |
| Lean | compiles | `TK1.lean` exit 0, 9 theorems, standard axioms only (`compile.txt`); `TK1_MUTATE.lean` fails on all 7 false statements (`compile_MUTATE.txt`) |

## A3 in detail (primary; canonical, alt within a few % in the times)

| z_ta (GR) | lambda_eff turns negative (s3 gradient) | unstable band then reaches | frozen s2 (lambda_eff = -2/3) | fold of the homogeneous branch | the patch at t0 |
|---|---|---|---|---|---|
| 5 | -2.4 Myr, theta 0.098 H0 | 4.1 kpc | -0.019 Myr, band 7.7 Mpc | after 9.4e5 Gyr | a/a_ta 1.00016, H 1.4e-4 H0, Q-1 7.5e-5 |
| 2 | -19.5 / -19.3 Myr, theta 0.099 H0 | 2.2 / 1.2 kpc | -0.14 / -0.15 Myr, band 25 Mpc | after 5.9e5 Gyr | 1.00009, 1.0e-4 H0, 4.4e-5 |
| 1 | -64.9 Myr, theta 0.100 H0 | 0.49 / 0.52 kpc | -0.45 Myr, band 49 Mpc | after 4.1e5 Gyr | 1.00006, 8.6e-5 H0, 2.6e-5 |
| 0.5 | -141 Myr, theta 0.098 H0 | 1.7 kpc | -0.85 / -0.83 Myr, band 75 Mpc | after 3.1e5 Gyr | 1.00004, 8.3e-5 H0, 1.5e-5 |

Times are relative to the GR patch's own turnaround (1.17, 3.26, 5.84, 8.58 Gyr after the big bang; GR's collapse to a_ta/2 at 2.12, 5.94, 10.64, 15.66 Gyr). "Band" is the longest
wavelength that grows faster than 1/t. The first band value is at the first grid point after the sign change (grid-limited:
the band is at least that wide by then).

Labels:
- **As frozen:** SINGULAR (s3) at every z_ta, and every bracket too. If s3 were set aside, the frozen s2 would still
  make every track SINGULAR.
- **Under A1** (the Cauchy problem's real principal matrix: the lapse is eliminated, so the minisuperspace determinant
  D stays negative through lambda_eff = -2/3 and vanishes only at the fold): SINGULAR (s3) at every z_ta. With s3 set
  aside, every track STALLS. The fold comes after 3e5 to 9e5 Gyr.
- **So under every reading the top-hat does not collapse.** The two A3 outcomes the criteria allow, SINGULAR and
  STALLS, are both structural. The label is set by the first.

Brackets (reported):
- theta_0 = 9 H0: the band opens 0.2 to 6 Gyr before turnaround. It is not well-posed around FRW either: A_z <= 0 (a
  ghost) at z 0.19-1.8, and the k^4 term is unstable at z < 1.8. mu_eff falls to 3.0e3 per Mpc today, below the Jeans
  line (ratio 0.12), so the dominance line fails.
- p = 4: the band opens 3.8 to 218 Myr before turnaround; the fold comes after 7e3 to 2e4 Gyr.
- Floor off: the same as the primary up to turnaround. There is no fold: the stiff part diverges as theta goes to 0, and
  the patch stalls for ever.

The key-off arm (MU2) collapses on GR's schedule.

## What happened, in plain words

1. **The background is fine.**
   - In FRW the expansion is 3H, at least 30 times theta_0 even today. So M_2 is mu_0^2 to 0.2 %, the term is MK1's
     quadratic at mu_K = 3e4, and the dust is cold and Jeans-stable.
   - The extra kinetic piece the term brings (a khronometric lambda-term, lambda_eff ~ 1e-20) is harmless. G changes
     by 2e-19.
2. **A forming structure must pass through theta = 0.** Every overdensity stops expanding before it collapses. On the
   way, theta passes theta_0, and two things happen.
   - **(a) The stiffness function changes curvature.** M_2 = mu_0^2 s^2 has an inflection near theta_0. Below it,
     F_thth = M_2''(Q-1)^2/(2K) is positive. K4 shows the k^4 coefficient of the scalar's gradient energy is
     F_thth N0^3 a / (4 Den), with Den < 0. So it turns negative while the kinetic coefficient stays positive: short
     waves grow, at a rate proportional to k^2, so without bound.
     - This is the leaf-elliptic (instantaneous) mode of K3 getting the wrong sign.
     - Within tens of Myr of turnaround the unstable band covers all galaxy scales.
   - **(b) The clock's energy at fixed charge diverges.** It is n + K n^2/(2 M_2) (1 + theta M_2'/M_2) (Lean
     `rhoK_form`).
     - Without the floor, M_2 goes to 0 as theta^4, and this diverges.
     - With the floor, it peaks near theta ~ theta_0 sqrt(M_f/mu_0) ~ 2e-5 H0.
     - Either way the Friedmann constraint has no solution at H = 0 while the region is still near its turnaround
       radius. The region keeps expanding ever more slowly and never turns around within a Hubble time.
3. **The proposal's premise, Q - 1 = K n / M_2(theta), is the problem.** With the charge conserved and the stiffness
   going to zero, the clock offset must grow, or the charge must leave the dust. In a homogeneous patch it cannot leave.
   - So the term that was meant to be inert at theta = 0 dominates exactly there.
   - At the stall Q - 1 is still small (1e-5 to 1e-4), but the stiff part is enough to hold the region open, because
     H^2 is itself tiny there.

## What the key buys and what it costs

- **Buys:**
  - The CMB rows (w by z 3400 and the Jeans line, both footings) are met with one constant set.
  - Static wells see mu_eff = 1e-3, below the SPARC, KiDS and Saturn bounds.
  - MK1's background-against-galaxy factor of 2.5e4 is gone.
- **Costs (graded):**
  - Collapse through turnaround is either ill-posed (k^4 gradient instability, s3; also the frozen Hessian line s2) or,
    with those lines set aside, never completes (STALLS).
  - So no halo, group or cluster forms in the theory as written.
- **Costs (reported):**
  - Inert dust in static wells means groups get no dust (they needed mu_K ~ 1) and X-COP stays without a value.
  - The static halo's charge must then all be the phantom D.P. That is 8.7 to 170 M_b inside 100-300 kpc, beyond form
    B's 5.41 at every point.
  - Had the collapsed charge stayed as dust at theta = 0, the floor would give Q - 1 = K n / M_f^2 = 0.75 (at 200 times
    the mean baryon density) to 4.0 (at 200 times the mean clock charge): strong field.

## Known answers (all pass; `tk1_grade.out`)

| | what | value |
|---|---|---|
| KA1 | covariant current vs direct variation | max rel 6.2e-40 |
| KA2 | E + N L_N = -a^3 F_Q; N-equation = Friedmann with rho_K = Q F_Q + theta F_theta - F | 0; 0 |
| KA3 | rho_K at M_2 const = n + K n^2/(2M) (symbolic); mu_B1a -> w(3400) = 0.01 | 0; rel -2.2e-16 / -2.2e-16 |
| KA4 | lambda-term: G_cosmo = G/(1 + 3 lambda/2) | 0 |
| KA5 | K4 with the key off: c_s^2 = (Q-1)/Q on a background with K4's own content | max rel 2.5e-16 |
| KA6 | EdS top-hat: linear delta at collapse | 1.686483 (1.68647; rel 7.5e-6) |
| KA7 | sqrt(M_sun a0/G) per kpc | 25,914.3 canonical (28,488.2 alt) |
| KA-K4 | A_z's numerator at F_Qth = 0 is a^5 x 3K F_QQ (F_thth - 1/(3K)) (K2c's trace, independent code) | ratio a^5 |

## MUTATE (separate outputs)

- **MU1** (theta F_theta dropped from rho_K) bites twice.
  - KA2's Friedmann-form residual becomes nonzero (`tk1_a1_MUTATE_MU1.out`).
  - On A3 tracks the a-equation residual rises to 0.08-0.48, against at most 1.1e-24 on the primary
    (`tk1_a3_MUTATE_MU1.out`).
  - The charge identity itself does not involve rho_K and holds under MU1. Disclosed: the frozen text named "KA2's
    identity".
- **MU2** (key off, M_2 = mu_0^2) bites: REGULAR at z_ta 5, 2 and 1 on both footings.
  - Collapse is within 1.1e-4 to 4.6e-4 of GR's time.
  - At z_ta 0.5 even GR's patch reaches a_ta/2 only after t0 (15.7 Gyr), so the frozen line reads STALLS there for GR
    too. MU2 matches GR's time there to 1.6e-4 / 1.2e-4. Disclosed: the frozen line is ill-posed at that z_ta.
- **MU3** (F_thth dropped from K4) bites: the KA-K4 ratio becomes a^5/(3K F_thth - 1), and g4 = 0.

## What this does not settle

- **The law sector in K4.** K4 holds the law sector at its FRW value (P = 0), as the record's linear cosmology does and as
  the criteria froze.
  - Its linear response (an alpha-like term) would add a k^2 gradient energy and could tame the k^4 instability that
    sets the label.
  - That was not computed.
  - It would not rescue the region: with s3 set aside the frozen s2 still reads SINGULAR, and under A1 every track
    STALLS.
- **Homogeneous top-hat only.**
  - The edge of the overdensity, shell crossing and non-spherical collapse were not modelled.
  - The stall comes from the local Friedmann constraint, which every shell obeys as its own theta passes zero. That is
    argued, not computed for shells.
- **K4 on the patch.** The flat-FRW closed forms were evaluated with the patch's local H, N0 and F derivatives; the
  patch's spatial curvature was dropped (high k).
  - A_z and g4 contain no time derivatives and no Lambda, so they do not depend on the background equations.
  - The k^2 coefficient used for the band edge is the KA5-checked dust form.
- **Unstable-band widths are grid-limited** at the sign change.
- **Not graded:**
  - Part B (the theta_c barrier: the claimed shock at 0.642 R_ta and the KiDS windows).
  - The proposal's other numbers.
- **The floor is read as additive** (M_2 = mu_0^2 s^p + M_f^2). Near theta = 0 this equals a max-type floor.

## Disclosures

- **AMENDMENT A1 (post hoc).**
  - It came after one toy evaluation of the Friedmann function (not a graded row). That evaluation showed the
    non-monotone G(H) and the lambda_eff = -2/3 crossing.
  - A1 adds the Schur-complement reading s2' (the fold) and extends s1 to dH/dt diverging.
  - Labels are printed both ways. They agree.
- **An early full A3 run was stopped and redone.** Its calibration used the target time instead of the GR patch's
  actual turnaround time. That is up to 1.3 % off on alt (44 Myr), which would have shifted every "Myr before
  turnaround" number. Only the corrected run is kept.
- **Development runs whose outputs were discarded:**
  - Two earlier tk1_a1 attempts, stopped by hand: sympy's euler_equations, then substitution of concrete functions.
    Both were too slow.
  - Test tracks.
  - A K4 evaluation with numerical derivatives through the root solver. It gave ä = 0 and was replaced by implicit
    differentiation.
  - The KA5 check, first run interactively, then saved as `tk1_ka5.py`.

## Files

- `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`.
- `tk1_a1.py` -> `tk1_a1.out` / `.json`: K1, K2, K3, KA2-KA4, about 2.5 min. MU1: `tk1_a1_MUTATE_MU1.*`.
- `tk1_k4.py` -> `tk1_k4.out` / `.json`: K4 closed forms, 18 s. MU3: `tk1_k4_MUTATE_MU3.*`.
- `tk1_k4eval.py`, `tk1_ka5.py` -> `tk1_ka5.out` / `.json`.
- `tk1_lib.py`.
- `tk1_frw.py` -> `tk1_frw.out` / `.json`: A1 on FRW.
- `tk1_a3.py` -> `tk1_a3.out` / `.json`: A2 and A3, 8 min, one thread; `run_a3_time.txt`. MU1 / MU2: `tk1_a3_MUTATE_MU*.*`.
- `tk1_ka3.py` -> `tk1_ka3.json`.
- `tk1_a45.py` -> `tk1_a45.out` / `.json`.
- `tk1_grade.py` -> `tk1_grade.out` / `.json`.
- `TK1.lean`, `TK1_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`
  (`cd fable_independent_2026/lean_2026 && lake env lean <absolute path>`).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
