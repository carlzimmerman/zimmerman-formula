# AKD1 RESULT: dust stiffness keyed on the clock's acceleration (2026-11-10)

**Label, canonical and alt: BREAKS AT A1** (NOT WELL-POSED AROUND FRW). **Part B (the collapse): NOT GRADED.**

The id AK1 was taken (the 11-07 fold-release lane), so this lane is AKD1.

The key does what it was built for in the background: there the acceleration is zero, so the dust is exactly MK1's
constant-mu dust (cold by z 3400, Jeans line met). It breaks one order up.
- At quadratic order the key enters as a term in |A|^2 with a **negative** coefficient, M_2'(0) (Q-1)^2 / (2K). That is
  a negative copy of the law's own term: eliminating P gives +|A|^2/(2K) near A = 0.
- Its weight against the law is R = p (mu_0 q0 / g_c)^2, with q0 = Q - 1 in the background.
- R is 3.9e14 / 4.2e14 at z 3400 and 4.5e11 / 4.9e11 at z 1100. Even with the law on, the clock's inertia is then
  **negative on every sub-horizon scale: a ghost** (A_z < 0 over the whole band from the horizon to 1 pc).
- The ghost lasts until z 11.6 / 11.4, where R falls through 1.
- Just above that epoch the zero of A_z is inside the horizon, at 15 to 60 pc. There the growth rate is unbounded
  (106 H at 1.0001 times the threshold wavenumber), and it is 1.0 to 1.7 H on all smaller scales.

The closure chat's hand algebra had the sign the other way ("a healthy-sign gradient term"). It treated delta(Q-1) as a
coordinate. It is a velocity: in unitary gauge the momentum constraint ties the lapse to the curvature's velocity, so a
negative |grad delta-ln Q|^2 term is negative inertia.

The failure is not special to this shape of M_2.
- **Cosmology.** Any M_2 with M_2'(0) < 0 has R growing as (1+z)^6. The law beats it at z 3400 only if
  g_c >= sqrt(p) mu_0 q0(3400) c^2 = 1.1e-7 m/s^2, about 1.2e3 a0. Galaxies would then stay stiff, and MK1's gap
  returns.
- **Static wells.** A shape that is flat at Y = 0 escapes the cosmological ghost but fails there. Any M_2 that falls from
  the Jeans line (mu_J^2) at Y = 0 to KiDS's line (mu_KiDS^2) by the lowest acceleration KiDS sees has a negative
  transverse inertia somewhere: by the mean value theorem, the weight W = |M_2'| q^2 (1+u) reaches at least
  8.5e7 / 7.1e7 where the standing clock's acceleration passes through the drop.
- For the primary shape, W > 1 already inside ONE1's middle KiDS window at three of the four masses.

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled. The cold component is
cold dark energy (clock dust plus the law's halo), never a particle. Per the frozen stop rule, A3 (turnaround), A5
(MK1's rows) and Part B were not graded. A2, the A4 weight W, A6 and the brackets are reported.

Commits (local / origin): criteria d88d310eb1 / 512e4e1f7f (alone, before any script or number); result
4b63dfc169 / 622bd80344.

## Table (canonical / alt where they differ; primary values unless a bracket is named)

| item | verdict | numbers |
|---|---|---|
| g_c rule (frozen) | met | g_min = law g at ONE1's middle-window edge = 9.568e-13 / 1.051e-12 m/s^2 (1.02e-2 / 9.29e-3 a0); g_c = 5.524e-15 / 5.309e-15 m/s^2 = **5.90e-5 / 4.69e-5 a0**; sqrt(M_2(g_min^2)) = 1.000 / 0.765 per Mpc (the KiDS line, with equality) |
| A1 K1: covariant current (sympy jets, 1+1) | **PASS** | J^m = [F_Q + (2/Q) nabla_k(F_Y A^k)] n^m + (2/Q) F_Y (n.d ln Q) A^m; EL = -d_m(sqrt(-g) J^m). Residual <= 1.3e-40 (6 random jets, 40 digits); opposite-sign control 2.00. Charge along n = M_2 (Q-1)/K + (2/Q) nabla.(F_Y A): dust plus a polarization-like P_K = 2 F_Y A = M_2'(Y)(Q-1)^2 A/K, **antiparallel to the law's P** when M_2' < 0 |
| A1 K2: unitary-gauge content | **PASS** | Y = (d_x ln N)^2 / gamma_xx exactly (with shift; residual 0); no dependence on N-dot, gamma-dot, shift or shift-dot; Q^2 N^2 = 1. L_K is a function of N, d_i N, gamma_ij only (Horava's healthy-extension class): metric and matter stay second order in time; the lapse obeys a leaf constraint |
| A1 K3: order and principal part | reported | 4th order in tau; principal symbol = 2 sqrt(-g) (n.xi)^2 [F_Y h(xi,xi) + 2 F_YY (A.xi)^2] / Q^2 (ratio 1.0 at 5 of 6 jets, 30-digit evaluation; the 6th has a zero symbol). Two derivatives along n acting on a leaf operator: no new characteristic cone. The sign of the inertia it multiplies is K4's question |
| A1 K4: quadratic action on flat FRW | closed form | **A_z = a^3 (F_QQ a^2 + 2 k^2 F_Y N0^2) / (4 N0 a-dot^2)**; alpha = a Z-dot / a-dot (momentum constraint); the gradient term is F_Y-free (the k-essence dust's). So A_z < 0 iff F_Y < 0 and k_phys^2 > F_QQ Q0^2 / (2 \|F_Y\|). With F_Y,tot = [c_law - R]/(2K): K (F_QQ Q0^2 + 2 F_Y k^2) = M_2(0) Q0^2 + k^2 (c_law - R) |
| **A1 on FRW, R1 (law on, unscreened; label-setting)** | **NOT WELL-POSED** | **ghost on 100 % of k_phys in [H/c, 1/pc] at z 3400 and 1100** (zero of A_z below H/c: super-horizon); healthy at z 10, 2, 0. R(z) = 3.90e14 / 4.22e14 (z 3400), 4.48e11 / 4.85e11 (1100), 0.446 / 0.483 (10), 1.8e-4 / 2.0e-4 (2), 2.5e-7 / 2.7e-7 (0). R = 1 at **z_x = 11.59 / 11.42**; 140-point grid: ghost for every z >= 12.1 |
| A1, R0 (law held at P = 0, TK1's convention) | ghost | 100 % of the band at z 3400, 1100; at z 10 above 4.5e4 / 4.3e4 per Mpc (22 / 23 pc, 16 % of the band); at z 2 and 0 only above 1/pc (0.02 pc today) |
| A1, R2 (law on, screened, Lstar 21.7 / 22.9 pc) | ghost | 100 % at z 3400, 1100; at z 10 above 9.1e4 / 8.4e4 per Mpc (11 / 12 pc); at z 2 and 0 only above 1/pc |
| c_s^2 and growth (K4 closed forms, K4's own background) | reported | where A_z < 0 the gradient stays > 0, so omega^2 < 0: growth. High-k growth / H = 5.2e-8 / 5.0e-8 (z 3400), 1.5e-6 (z 1100). Above z_x (z 12-27): the zero of A_z is at 27 to 450 pc; growth / H at k/k_th = 1.0001, 1.01, 1.1, 2, 10 is 106, 10.6, 3.6, 1.7, 1.5 at z 11.96 and 6.4, 0.65, 0.22, 0.10, 0.09 at z 27.3: **unbounded at the zero** (rate^2 = grad/\|A_z\|, grad > 0) |
| G_cosmo / G_N | 1 at linear order | FRW: A = 0, so rho_K at fixed charge is MK1's (no H dependence). Around Q = 1 the Y-term's coefficient M_2'(Y)(Q-1)^2 vanishes at linear order. The Horava-like coefficient eta_eff = 4K F_Y,tot = 2 (c_law - R): **-7.8e14 / -8.4e14 at z 3400** on R1 (healthy needs 0 < eta < 2) |
| A2 FRW limit (reported) | PASS | w(z 3400) = 4.41e-7 (line 0.01); mu_eff = sqrt(M_2(0)) = 3.000e4 per Mpc vs mu_J 2.512e4 (ratio 1.194) |
| A3 turnaround | NOT GRADED | (homogeneous patch has A = 0: it would be MK1's constant-mu patch; not run, per the stop rule) |
| A4 static-well weight W (reported) | **W > 1 inside the middle KiDS window at 3 of 4 masses** | max W inside the window: 0.36 / 3.1 / 5.5 / 12.1 (canonical), 0.31 / 2.7 / 4.7 / 10.3 (alt) at log M_b 9.4 / 10.45 / 10.7 / 10.9; W > 1 from 204 (just past the 190 kpc edge) / 562 / 700 / 848 kpc (canonical); out to 30 x the edge W reaches 1.8e9 to 5.9e10. Frozen label 4 would also fire. Saturn: mu_eff = 1.0e-3 per Mpc vs 6.22e3, PASS |
| Class bound (reported) | any decreasing M_2 | falling from mu_J^2 at Y = 0 to mu_KiDS^2 at g_min^2 forces W >= 8.5e7 / 7.1e7 somewhere the standing clock's g passes below g_min (log M_b 10.7, Newtonian outskirts) |
| A5 MK1's rows | NOT GRADED | clusters would fail (no cluster state in a single-clock action), as expected |
| A6 (i) standing branch | unstable where W > 1 | transverse inertia = law 1/(1+u) + candidate M_2'(g^2) q^2: negative iff W > 1 (Lean `transverse_ghost`); flat static reading (SCS1's form with K m = 1 - R): omega^2 -> -K Q n R/(R-1) at high k for R > 1 |
| A6 (ii) leaving the stiff branch | reported | A = K \|grad n\| / M_2(0) > g_c needs an overdensity of **2.5e5 / 2.4e5** times today's mean clock charge over 3 kpc: only at a fold |
| Brackets (reported) | all NOT WELL-POSED | p 1: g_c 3.4e-7 / 2.4e-7 a0, ghost on R1 at z 3400, 1100, 10 and 2 (z_x 1.53 / 1.39); p 4: g_c 7.8e-4 / 6.6e-4 a0, ghost at z 3400, 1100 (z_x 25.5 / 25.7); floor off: as the primary (z_x 11.59 / 11.42) |
| Part B (collapse in COL1's solver) | NOT GRADED | Part A structurally dead |
| Known answers KA1-KA6 | 6 of 6 PASS | below |
| MUTATE MU1, MU2, MU3, Lean twin | all bite | below |
| Lean | compiles | `AKD1.lean` exit 0, 9 theorems, standard axioms only (`compile.txt`); `AKD1_MUTATE.lean` fails on all 9 false statements (`compile_MUTATE.txt`) |

## What happened, in plain words

1. **The background is fine.** In FRW every clock falls freely, so A = 0 and M_2 = mu_0^2 + M_f^2 exactly. The dust is
   MK1's at mu = 3e4 per Mpc: cold by z 3400 and stiff enough for the CMB-lensing Jeans line.
2. **The key is invisible in the background but not in its perturbations.**
   - A perturbation tilts the clock, so it has an acceleration delta-A = -grad(delta ln Q).
   - The term M_2(Y)(Q-1)^2/(2K) then contributes M_2'(0) q0^2 |delta-A|^2/(2K). It is quadratic in the perturbation
     and does not vanish, because the background offset q0 is not zero.
   - The key must make the stiffness fall with A, so M_2'(0) < 0.
   - In unitary gauge delta ln Q is minus the lapse perturbation, and the momentum constraint fixes the lapse as
     zeta-dot / H. So |grad delta ln Q|^2 is a kinetic term, and with a negative coefficient it is negative inertia.
   - K4 gives the inertia exactly: proportional to F_QQ Q0^2 + 2 F_Y k_phys^2. An independent Minkowski decoupling
     computation gives the same ratio (KA4).
3. **The law's own term is the same operator with the healthy sign.**
   - Eliminating P gives +J(|A|) = +|A|^2/(2K) near A = 0. That is the law's positive inertia: SCS1's K m = 1, which
     the flat-limit known answer reproduces.
   - So the candidate is an anti-law term, and the contest is one number, R = p (mu_0 q0 / g_c)^2 = p [K n / (mu_0 g_c)]^2.
4. **R is huge early.**
   - g_c has to be tiny: about 6e-5 a0, for the dust to be soft (mu <= 1 per Mpc) where KiDS sees the law
     (about 0.01 a0).
   - K n / mu_0 is large early: 1.96e-18 (1+z)^3 m/s^2.
   - So R is about 4e14 at z 3400 and 4e11 at z 1100.
   - The anti-law term beats the law (and the dust's own inertia) on every scale above about 23 Mpc physical at z 1100
     and 1 Gpc at z 3400, which is every sub-horizon scale. That is a ghost.
5. **Is it only a quantum objection? No.**
   - Early on the classical growth is slow: 5e-8 H at z 3400, 1.5e-6 H at z 1100.
   - But the zero of the inertia sweeps through every comoving wavenumber as R falls (R goes as a^-6). Near the zero
     the growth rate is unbounded.
   - It enters the horizon at z of about 12 to 27, at 30 to 450 pc. There the computed growth reaches 106 H at
     1.0001 times the threshold, and modes 2 to 10 times shorter grow at 1 to 1.7 H.
   - The Cauchy problem is ill-posed there. This is the same kind of failure as TK1's, one stage earlier: TK1 died at
     turnaround, AKD1 dies in the linear background.
6. **Moving g_c does not help.** A larger g_c (MU2: x 100) only moves z_x up, to 57. Galaxies need g_c far below a0;
   the law needs it above 1e3 a0.

## Hand estimate against the outcome

| hand (criteria section 2, before any script) | outcome |
|---|---|
| new term = negative copy of the law's +Y/(2K); the chat's "healthy sign" is wrong | confirmed (K4 closed form, KA4, KA5) |
| g_c about g_min / 173 = 5.5e-15 m/s^2, 6e-5 a0 | 5.524e-15 m/s^2, 5.90e-5 a0 |
| R(3400) about 4e14, R(1100) about 5e11, R(10) about 0.5, R(2) about 2e-4, R(0) about 3e-7 | 3.9e14, 4.5e11, 0.45, 1.8e-4, 2.5e-7 |
| R = 1 near z 11-12; ghost at z 3400 and 1100 on every reading, all sub-horizon k | z_x 11.59; confirmed |
| P = 0 and screened readings: ghost below about 1e-2 pc at all z | at z 2 and 0 only above 1/pc (0.02 pc today); at z 10 above 11-23 pc |
| rate at z 1100 about 1e-6 H; > H only near z 11-15, unbounded at the zero | 1.5e-6 H; 1-1.7 H at z 12-14 for k >= 2 k_th, 106 H at 1.0001 k_th |
| W > 1 where g < about 5e-3 a0 (KiDS outskirts) | W > 1 from 562-848 kpc at three masses (inside the middle window) |
| class bound W of order 1e9 | 8.5e7 / 7.1e7 (the hand estimate dropped the factor 1/2 and the q^2-propto-sqrt(Y) weighting) |
| A6(ii) overdensity of order 1e5 over 3 kpc | 2.5e5 |

## Known answers (all pass; `akd1_grade.out`)

| | what | value |
|---|---|---|
| KA1 | covariant current vs direct Euler-Lagrange (1+1 jets) | max rel 1.3e-40 (line 1e-30) |
| KA2 | F_Y = 0: A_z = F_QQ a^5/(4 N0 a-dot^2) (TK1's closed form with the theta terms off) | residual 0 |
| KA3 | M_2 constant: mu_B1a 198.2542 / 198.2449 vs KD1 | rel -6.9e-17 / -6.3e-17 |
| KA4 | K4's A_z(k)/A_z(0) = Minkowski decoupling inertia ratio 1 + 2 F_Y k^2/(F_QQ Q0^2); decoupling B = F_Q Q0 / 2 | residuals 0, 0, 0 |
| KA5 | flat Newtonian dispersion with the law (K m = 2K F_Y) = SCS1's closed form; at K m = 1 = TPA1 4.4 | rel 0 at k 0.3, 30, 3e4; residual 0 |
| KA6 | law g closed form vs root solve | max rel 2.3e-41 |

## MUTATE (separate outputs)

- **MU1** (sign of p flipped, p = -2, M_2 increasing in Y): A1 flips to WELL-POSED on both footings (R < 0: the term then
  adds inertia). It bites. The g_c rule cannot be met for an increasing M_2 (the primary's g_c was kept, disclosed), and
  such a key makes static wells stiffer, the opposite of what MK1 needs.
- **MU2** (g_c x 100): the z 3400 threshold wavenumber moves x 100 / x 100; z_x moves from 11.59 / 11.42 to 57.4 / 56.7. It bites.
  The label is unchanged (ghost at z 3400 and 1100).
- **MU3** (F_Y dropped from K4 and from the decoupling code): KA4 fails on both sides. It bites.
- **Lean twin**: all 9 false statements fail.

## What this does not settle

- **Quadratic order only.** The verdict is the sign of the scalar's kinetic term around flat FRW (and, reported, a local
  WKB sign in static wells). Nonlinear completion is not computed.
- **The law sector at quadratic order** was read three ways because F(Pi) = max(Pi, 0)^2/2 has a kink at Pi = 0. A real
  perturbation samples both branches, so the physical inertia is no larger than R1's (the most favourable). R1 still
  fails at z 3400 and 1100. The v3s Pi^6 blend was not used (the brief names action (A)).
- **K4's content** is gravity + clock + Lambda (+ the law's quadratic piece). Baryons and radiation enter the background
  only. The sign of A_z needs only F_QQ, F_Y, Q0 and k, so this does not touch the label. The rates use K4's own
  background, with all matter in the clock (disclosed).
- **A3, A5 and Part B were not run** (frozen stop rule). The g_c rule used the law's uncapped g at the window edge (as
  frozen).
- **Post-freeze reported readings** (`akd1_extra.*`, disclosed, label-setting nothing):
  - (a) the growth rates above z_x on K4's own background;
  - (b) the same rule with the PD1-capped g at the edge (5.86e-13 m/s^2). It gives g_c 3.6e-5 / 2.6e-5 a0 and a ghost at
    z 3400, 1100 and 10 (z_x 9.7 / 9.2). W > 1 inside the window at log M_b 10.7 and 10.9 (canonical), and at 10.9 (alt).
  - A first extra run sampled the zero of A_z with the real background's q0 while the rates used K4's background. That
    hid the divergence, so it was replaced (the main outputs were re-run and are unchanged, checked by diff).

## Files

- `FROZEN_CRITERIA.md` (alone, before any script).
- `akd1_a1.py` -> `.out` / `.json`: K1, K2, K3, about 6 min. K2's first run printed "K2 pass: False" only because sympy
  did not reduce sqrt(N^-2) to 1/N without N > 0; the check was made positivity-safe (Q^2 N^2 = 1) and the script re-run.
- `akd1_k4.py` -> `.out` / `.json` (MU3: `akd1_k4_MUTATE_MU3.*`).
- `akd1_dec.py` -> `.out` / `.json` (MU3: `akd1_dec_MUTATE_MU3.*`): KA4 decoupling side, KA5.
- `akd1_eval.py` -> `.out` / `.json`: g_c, KA3, KA6, A1 evaluation, rates, brackets, G-ratio, A2, A4 W, A6(ii). MU1 and MU2:
  `akd1_eval_MUTATE_MU1.*`, `akd1_eval_MUTATE_MU2.*`. `AKD1_EXTRA=1` gives `akd1_extra.*`.
- `akd1_grade.py` -> `.out` / `.json`.
- `AKD1.lean`, `AKD1_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
