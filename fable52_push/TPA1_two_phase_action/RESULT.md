# TPA1 RESULT (criteria b81c28d00c)

**TPA1: EQUATIONS COMPLETE. Health: UNHEALTHY** — a gradient instability, with no ghost, in the law-on phase.

**Health first, as the criteria require.** A static clock in the S = 1 phase is gradient-unstable wherever its own dust
density is below n_crit = -dp/dx, the outward fall-off rate of the law's polarization p = |P|. For a point mass this is
0.08 to 0.9 of the law's phantom density: 2.2e3 to 1.1e5 x today's mean cold density on the canonical footing, 3.0e3 to
1.5e5 on the alt footing. On the frozen grid the e-folding time is 5.0 Myr to 0.62 Gyr. This is the phase the two-phase
theory needs to be cleared of dust. The wall itself is stable: in 720 WKB rows there is no ghost and no instability,
because the switch's own term -S_Q W enters the gradient coefficient with a stabilising sign. The S = 0 phase is healthy.
S adds no propagating mode. Every analysis was done in the decoupling limit (metric frozen).

TEST lane, quarantined. Adopts nothing and relabels nothing. Not registered. kappa = 1/2 FITTED; not theory closed.
Footings are never pooled (canonical / alt below).

## The action (frozen in the criteria; written out in full in EQUATIONS.md)

    L/sqrt(-g) = [R - 2 Lambda]/(4K) + mu_K^2 (Q-1)^2/(2K) + S(n_d) [P.A - W(K|P|) - gamma_L F(Pi)] + lambda n.P + L_m ,
    n_d = mu_K^2 (Q - 1)/K .

- The reading choice R1 puts S on the law's whole Lagrangian (the Legendre pair and the stiffness). The constraint does
  not carry S.
- The literal form with the stiffness outside S (V0) is certified alongside. The closed forms carry two independent
  switches, S_L on the pair and S_F on the stiffness.
- Which choice keeps the Legendre map:
  - S on both P.A and W keeps K|P| = a0|A|/(a0 + |A|) for every S > 0. S on P.A alone gives a0 S|A|/(a0 + S|A|) (Lean).
  - With the stiffness inside S (R1), QX17's screened map is unchanged wherever S is locally constant.
  - V0 rescales gamma_L to gamma_L/S.
  - S on the constraint is equivalent on shell wherever S > 0.
- The density the switch reads has two readings:
  - D1, n_d = L_K'(Q), is certified.
  - D2, the full leading charge N = n_d + Pi, is derived and reported. It breaks the Legendre map wherever S' is non-zero
    and makes the switch read the law's own phantom as dust.

## Item table

| item | label | what was checked | result |
|---|---|---|---|
| 1. Covariant Euler-Lagrange set | **CERTIFIED** | closed forms against direct sympy variation in 2+1 dimensions (3 seeds; exact Taylor total derivatives); off-shell Noether/Bianchi identity of the closed forms | P equation 2.4e-15, clock 7.4e-15, stress (6 components) 3.8e-15, Noether 4.1e-16 (max relative; line 1e-8). Known answers: S = 1 equals QX17 1.2e-15; S = 0 equals GR plus dust 1.0e-13; Noether with QX17's forms 7.4e-16. MUTATE worst per seed: M1 (clock sign) 1.03 / 1.61 / 1.15; M2a (S on constraint) 0.75 / 0.71 / 0.56; M2b (literal V0 against R1) 1.59 / 0.72 / 0.59; M3 (stress term dropped; Noether fails) 2.05 / 1.37 / 0.48. All bite (line 1e-3). 28 s. |
| 2. FRW | **CERTIFIED** | sympy exact | Isotropy forces P = 0 (W'(p) = 0 only at p = 0). The law's Lagrangian is 0 at P = 0, so the background contains no S. Qbar, rho and w equal QX17 K4 / C4 K7 exactly. S = epsilon changes the background by exactly zero. |
| 3. Linear theory about FRW | **CERTIFIED** | unitary-gauge quadratic action (sympy, symbolic S); Jeans dispersion by hand and from the expanded covariant Lagrangian | The law's quadratic Lagrangian is Sbar [P.d alpha - K P^2/2] a; S' and S'' enter only at cubic order. At Sbar = 0 the law drops out. At Sbar = epsilon: mu_K^2 Qbar^2 -> mu_K^2 Qbar^2 + epsilon k^2/a^2. omega^2 = -K nbar [1 - k^2/(mu_K^2 + epsilon k^2)]. Route 2 matches route 1 at epsilon 0, 0.3 and 1 and k/mu_K 0.14, 1.4, 14, with a residual of order nbar (5.8e-7 at nbar 1e-8; it halves exactly when nbar halves). Known answers: epsilon 1 gives RK04's R f; epsilon 0 gives the isolated-fluid Jeans form. |
| 3'. GAL1 bound on epsilon | reported | GAL1's 2 sigma f 0.01968 gives q = 0.0301 | First correction epsilon (k/mu_K)^4 = 1.6e-28 at k 1/Mpc, mu_K* 8.890e6 / 8.889e6 Mpc^-1. Bound epsilon <= 1.9e26: **vacuous** on both footings. It would bite at epsilon 1 only for mu_K < 2.4 Mpc^-1, which the CMB and BBN exclude (KD1). |
| 4. Static weak field and wall pressure | **CERTIFIED** | static reduction by two routes (covariant energy density with Poisson; EL of the static Lagrangian), Newtonian order, general switch; wall pressure from the covariant stress, two routes, against swt1.json; compensation | With S's argument held: exactly div[(1 - S/(1+u)) grad Phi] + mu_K^2 Phi = 4 pi G rho_b. With a static clock (n_d = -mu_K^2 Phi/K) one more source term appears, mu_K^2 S'(n_d) J. It is a layer where S varies and zero in each phase. On-shell leaf stress T^L_xx = -S W(K|P|). The momentum-flux jump at fixed displacement is (a0^2/4 pi G) W_wall(u) exactly (symbolic and Lean), with dPi/dS = J. Noether force with S held: nabla^m T^L_mx = Lam dS/dx exactly (residual 0); with the clock carrying S, 0 exactly. Against swt1 KA_W1: 1.5e-10 (route A: force integral; route B: the clock charge's S' term over an explicit profile in Q). KA_W3 forces: 9.6e-14 on both footings. All outward. M1 turns the force inward at all six y. Compensation: exterior 2.06e-9 / 2.06e-9; interior 39.374089574424 against 39.374089574428 (1.1e-13). |
| 5. The two phases as exact solutions | **CERTIFIED** | from item 1's reductions; sympy; Lean | S = 1 is QX17 exactly; spherical, mu_K = 0 gives g^2 = g_N (g + a0) (Lean). S = 0 is GR plus PAPER70's dust: P is free and stress-free, and a0 is absent from the S = 0 Lagrangian. Static clock: S(n_d(N)) rises with N for any non-increasing S (Lean), so the law-on phase lies at the shallow potential. |
| 6. Health | **UNHEALTHY** | decoupling limit, WKB with coefficient gradients kept; 720 wall rows and 288 phase rows on the frozen grid; hand gradient formula as a second route | Wall: 0 ghost, 0 unstable. S = 0: healthy (k-essence clock; numeric KA6 exact). S = 1 with n_d at 1 or 1e3 x mean: 96 of 96 rows unstable; at 1e6 x mean: stable. No ghost anywhere. No pi_tt^2 term and a symbol quadratic in omega: no new mode. Gradient coefficient, hand against numeric: 72 rows agree to 1.6e-42. |
| D2 | reported | P equation by hand and by EL (sympy) | S(N_2)(A - K W') = d/dx[S'(N_2)(P.A - W)]: the Legendre map is lost where S' is non-zero. |
| Lean | PASS | TPA1.lean: 14 theorems, exit 0, axioms propext, Classical.choice, Quot.sound only. TPA1_MUTATE.lean: 5 false statements, 6 errors, exit 1 | |

**Overall: EQUATIONS COMPLETE** (items 1 to 5 CERTIFIED). **Health: UNHEALTHY.**

## The five results that carry the label

1. The complete covariant set (E1) to (E5) agrees with direct variation to about 1e-15 for an arbitrary switch. It obeys
   the off-shell Noether identity, so matter is conserved. The clock equation's new term is (mu_K^2/K) S'(n_d) [P.A - W - gamma_L F].
2. The cosmic background contains no S at all, and linear theory sees only Sbar. Its effect is to replace mu_K^2 by
   mu_K^2 + epsilon k^2. At the record's mu_K that is unobservable, so GAL1 cannot bound epsilon.
3. SWT1's wall pressure follows from the covariant equations without the static Lagrangian, by two routes: the
   momentum-flux jump of the law's covariant stress, and the clock charge's S' term. It matches swt1.json to 1.5e-10.
   Reversing the sign of the clock term reverses the force.
4. In a static clock the switch's own energy layer balances the wall force for any profile, and the law-on phase sits where
   the potential is shallow (Lean). A static clock cannot hold a cleared region inside a dust envelope.
5. The cleared, law-on phase with a static clock is gradient-unstable (e-folding 5 Myr to 0.6 Gyr) unless it carries dust
   at a sizeable fraction of the law's phantom density. The switch's wall is stable.

## 7. What the equations do not deliver (plain words)

The only force the law exerts on the dust is f = -[P.A - W] grad S. It acts only where S changes, at a wall. Inside either
phase it is exactly zero.

Dust that is already bound in a galaxy's well is dense, so S = 0 around it. The law is switched off there, and no force
reaches that dust from inside the galaxy. The only push is at the edge of a law-on region, and it is bounded. Per unit
area it is at most (a0^2/4 pi G) W(u), which is at most a0 g_N/(4 pi G). Over a sphere it is less than a0 M_b (SNP1 A.1).
A shell heavier than that falls inward, whatever the baryons do.

For a static clock the push is exactly cancelled by the weight of the switch's own energy layer. A static configuration
then has the dust in the deep potential and the law outside: the reverse of a cleared disc. With the record's mu_K
(8.9e6 Mpc^-1) a static clock can stay in the law-on phase only across a potential difference of K n_1/mu_K^2. That is
2.6e-22 c^2 at n_1 equal to the mean cold density, and 2.6e-16 c^2 at 1e6 times it. A disc galaxy spans about 1e-6 c^2.

Run as a moving wall in the expanding background, the same pressure FAILS SNP1 on both footings. It clears the inner
200 kpc only if the wall forms late (z 1.5), and it never reaches KiDS's range.

**The action as written does not by itself clear a disc of a collapsed share.** It gives the force only at a wall, it bounds
that force, a static clock balances it, and a static clock puts the dust inside. Clearing needs a clock that moves outward
and formation history (initial data). The action supplies neither. If the law-on phase were cleared, it would be
gradient-unstable (item 6).

## Disclosures

- **Item 4a, first run.** The slaved-switch comparison failed on a script bug. Route 1 used the unscaled a0 symbol inside
  W, while the Newtonian bookkeeping needed ev alpha0. The outputs are kept as tpa1_reduce_run1_scriptbug.json / .out.
  The fix touched only that line, plus expand_log in the comparisons and a general symbolic cubic for the switch. A local
  identity sees only S, S' and S'', so the cubic loses nothing. No other number changed.
- **Item 6, implementation.** Two runs were stopped for speed before giving any number. The evaluation was then rebuilt:
  a Hessian in the jets, with coefficient x-derivatives taken by 60-digit mp.diff. The first complete run (kept as
  tpa1_health_run1.out) had phase rows only at n_* = mean. Its symbolic KA6 failed only because N0 was not declared
  positive; the numeric KA6 (exact) passes.
- **Added after seeing the first item-6 numbers.** The phase rows were extended to the full frozen grid. The S = 1
  stability threshold scan, the hand gradient formula (route 1) and the decomposition were added; they are reported. The
  label rests on the frozen rule alone.
- **My pre-freeze expectation for item 6 was wrong in its mechanism.** I expected the switch's S' term to destabilise the
  wall. It stabilises it: the term enters as -S_Q W, through the Legendre identity J - P.A = -W. The instability is in the
  S = 1 phase instead. I expected UNHEALTHY, and that is the label, for a different reason.
- **Item 3, dispersion.** It is checked at exact rational parameter points, because the fully symbolic expansion was too
  slow. The numeric line (relative 1e-5, and the residual halving with nbar) was set after the first look at the residuals.
  The exact halving (ratio 2.000) is what shows the two routes agree at first order.
- **Item 6, caveat.**
  - Decoupling limit. At WKB order, mixing with the Newtonian potential rescales the kinetic coefficient by
    1/(1 - S K J''). That factor is positive, and the mixing does not enter the gradient coefficient (argued by hand, not
    computed).
  - The growth rate is of order sqrt(K x phantom density), so a fully coupled analysis is the next check. It has not been
    done.
  - The S = 1 instability is a property of PAPER70's own clock sector when the clock's dust density is low. It is reported
    here and relabels nothing in the record.

## Files

- Criteria and statements: FROZEN_CRITERIA.md (b81c28d00c); EQUATIONS.md (the paper-ready statement).
- tpa1_cov.py -> tpa1_cov.json / .out, and tpa1_cov_MUTATE_{M1, M2a, M2b, M3}.json / .out.
- tpa1_reduce.py -> tpa1_reduce.json / .out, tpa1_reduce_MUTATE_M1.json / .out, tpa1_reduce_run1_scriptbug.json / .out.
- tpa1_health.py -> tpa1_health.json / .out, tpa1_health_run1.out.
- TPA1.lean, TPA1_MUTATE.lean, compile.txt, compile_MUTATE.txt.
- Resources: one thread each. Runs took 28 s (item 1, each MUTATE about the same), 20 s (reductions) and 46 s (health),
  all under 0.15 GB. Lean was compiled with `lake env lean` from the copy of fable_independent_2026/lean_2026 that has its
  Mathlib build (about 30 s per file). Nothing was downloaded.

Not registered. Does not edit fable52_push/README.md, any PAPER file or the closure register.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
