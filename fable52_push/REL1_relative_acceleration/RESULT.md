# REL1 RESULT: the law on the clock's acceleration relative to the baryon flow (2026-11-10)

**Label, canonical and alt: NOT WELL-DEFINED.** The action can be written and its limits are right, but it makes every
piece of ordinary matter run away. The law's Legendre pair now contains the time derivative of the baryons' velocity,
inside a strictly convex function. That turns the baryons' equation of motion from second order into fourth order
(Ostrogradsky). Free-falling rock e-folds in 10 minutes and blows up (infinite acceleration) in about 5 hours; a mass
resting on a lab bench e-folds in about 2 ms. The stiffness (gamma_L) does not remove it. Not varying u_b instead breaks
the Bianchi identity. Steps 2-7 were not graded (the criteria stop at the first structural failure).

TEST lane, quarantined. Criteria e495153acf (committed alone; origin 76f0cdddf1); AMENDMENT A1 96c0968d9e (post hoc,
committed alone, the energy-check normalization only; origin a900f9f5bd); result a4e86fc8b0 (origin 6db345c60e). Adopts nothing. kappa = 1/2 FITTED; not theory closed. Not registered.

## Table

| item | verdict | numbers (both footings unless split) |
|---|---|---|
| Step 1, K1: covariant definition and limits | **PASS** | D: A_rel = h.n.nabla(u_b/gamma). Exact in 2+1: (i) u_b = n gives A; (ii) static clock and ANY steady baryon flow gives A; (iii) free-falling clock past baryons at rest gives grad Phi to O(e^2); (d) flat space: A_rel = d_t v_b exactly |
| Step 1, K2: matter's kinetic structure (S1) | **FAILS: Ostrogradsky** | Hessian of J in xi'': 1/(K(1+u)^2) along A_rel, 1/(K(1+u)) across, never 0. EL: xi''''/K - rho xi'' - k xi = 0; runaway s^2 = [K rho + sqrt(K^2 rho^2 + 4Kk)]/2 > 0 for any restoring k. Ostrogradsky H linear in p1 |
| e-fold, free-falling body (u = 0), both footings | runaway | water 1092 s, rock 630 s, Earth 465 s, Pt 236 s, Ti 514 s; ISM 1 cm^-3 2.7e7 yr; halo gas 1e-4 cm^-3 2.7e9 yr; mean baryon density 5.3e10 yr (only this one is slower than the age) |
| e-fold, body at rest on Earth (u = 9.81/a0) | runaway | across A_rel: rock 1.9 / 2.1 ms, Pt 0.73 / 0.80 ms (canonical / alt); along A_rel 6e-9 s |
| Step 1, K3: stiffness gamma_L > 0 | does not help | b.(M + gamma k k^T)^-1.b = b.M^-1.b for displacement patterns with b . k = 0: gamma drops out exactly |
| Step 1, K4: nonlinear 1D, Noether energy | blow-up in finite time | From eps = 1e-12 a0: T = 27.22 / sqrt(4 pi G rho): rock 4.8 h, Earth-density 3.5 h, Pt 1.8 h, Ti 3.9 h. KA4 rate 1.000000; energy drift 2.3e-14 (A1) |
| Step 1, K5: the other exit, u_b not varied | inconsistent | the P sector exchanges J'(y) != 0 with a flow that feels nothing back: non-GR stress not conserved, Bianchi violated |
| Step 1, K6: WEP | D: no first-order force on a compact free-falling body (A_rel = 0 inside it); the runaway rate itself depends on density (Pt 236 s, Ti 514 s). D': eta = 2.8e-12 / 3.3e-12, 2.8e3 / 3.3e3 x MICROSCOPE (argued, unscreened) |
| Step 2, statics | NOT GRADED | (K1 shows D gives A exactly for a static clock and any steady flow, so the law would be recovered there) |
| Step 3, double counting | NOT GRADED | |
| Step 4, one mu_K (MK1 rows 1, 2, 5, 6, 7) | NOT GRADED | |
| Step 5, Solar System, moving sources, Cassini | NOT GRADED | |
| Step 6, SCS1 coupled dispersion | NOT GRADED | |
| Step 7, clusters and the Bullet | NOT GRADED | |
| Known answers KA1-KA4 | PASS | KA1 Legendre residual 0; KA2 law residual 0; KA3 dust-only limit is GR + dust + baryons; KA4 growth rate 1.000000 |
| MUTATE M1 (Christoffel sign) | bites | K1 (iii) fails for D and D' |
| MUTATE M2 (u_b coupling removed) | bites | Hessian 0, roots s^2 = -k/rho, no runaway, no blow-up |
| MUTATE M3 (J concave) | bites | roots oscillatory, no blow-up; H_O still linear in p1 (a negative-energy ghost instead of a runaway) |
| Lean | compiles | `REL1.lean` exit 0 (`compile.txt`); twin `REL1_MUTATE.lean` fails on all 5 statements (`compile_MUTATE.txt`) |

## What happened, in plain words

The candidate needed a quantity that is non-zero for a free-falling clock and equals grad Phi there. By the equivalence
principle, gravity (the Christoffel symbol) can enter a vector built from n and u_b only through a covariant derivative
of a velocity field. For a free-falling clock that derivative has to be of the baryons' velocity. And the Christoffel
symbol comes with the time derivative of that velocity: n.nabla u_b = d_t v_b + grad Phi + ... (K1 (d), exact). So A_rel
holds the baryons' acceleration. The law's Lagrangian is J(|A_rel|), strictly convex (J'' = 1/(K(1+u)^2) > 0). A
Lagrangian that is non-degenerate in a second time derivative has a Hamiltonian that is unbounded below (Ostrogradsky).
Here the result is concrete: about any background, a displacement grows as e^{s t} with s at least sqrt(4 pi G rho_b),
the free-fall rate of the matter's own density. For anything solid that is minutes. The nonlinear version blows up in
hours: the force J' saturates at a0/K while the acceleration needed to keep up goes to infinity.

The proposal's own example, D' = A - h.a_b (the difference of the two proper accelerations), has the same flaw. It also
gives A_rel = 0 for baryons held at rest beside a static clock (K1), so it switches the law off inside any
pressure-supported medium. D does not have that problem.

## What the change buys and what it costs

- **Buys (on paper only):** D is exactly A for a static clock and any steady baryon flow, and is grad Phi past a
  free-falling clock. So the law would no longer need a static clock where baryons flow steadily. That was the point,
  and the definition delivers it.
- **Costs:** the theory is not well-defined. Matter runs away. No choice of the stiffness, sign convention or fluid
  model removes it: an elastic or pressure restoring force keeps a positive root (Lean `runaway_root_pos`), and a
  concave J only trades the runaway for a negative-energy ghost (M3). Leaving u_b unvaried breaks the Bianchi identity.
  Removing the u_b derivative (M2) removes the runaway, but also removes the law for a free-falling clock.

## The variant without the baryon derivative (V0, argued, not graded)

V0: A_rel = A + h.(w.nabla n) (the clock's shear seen by the moving baryons) has no derivative of u_b, so no
Ostrogradsky runaway. It is not a way out.
1. It gives grad Phi only for a steady infall (it is -(v_c.grad) v_c = grad Phi + d_t v_c).
2. It is built from grad n, and n does not exist behind the fold. COL1 has the clock fold within 0.06-0.15 Gyr, and
   FLD1's folded region covers every SPARC and RC100 radius. So V0 cannot carry the law where rotation curves are
   measured.
3. It couples P to the baryon velocity with a coefficient that does not depend on rho_b. That gives dilute gas an extra
   acceleration up to about a0/(4 pi G rho_b r) times g: 0.22 / 0.26 for 1 cm^-3 gas at 10 kpc and 216 / 261 for
   1e-4 cm^-3 halo gas at 100 kpc (my arithmetic, upper estimate with K|P| <= a0). That is a density-dependent force on
   gas, far larger than gravity in halos.

## What this does not settle

- Steps 2-7 were not run: double counting, one mu_K, the Solar System and moving sources, SCS1's dispersion, clusters
  and the Bullet. Nothing here says how D or V0 would read on them.
- The full covariant variation in 2+1 (as QX17 and TPA1 did) was not done. The failure is in the matter's kinetic
  structure, which the reduced checks settle exactly: P carries no time derivative in (A) (QX17 section 1), so at
  gamma_L = 0 it is eliminated exactly; K3 covers gamma_L > 0 for divergence-free patterns. The coupling to the clock
  and the metric was not included in K2. It enters without second time derivatives of the baryons, so it cannot make the
  Hessian degenerate, but that is argued, not computed.
- A theory that keeps only the order-reduced (non-runaway) solutions, as is done for the Abraham-Lorentz equation, was
  not considered. It would make matter's motion acausal over the e-fold times above (minutes for rock), and it is not
  an action principle.
- WEP for D' and V0 is argued with unscreened P. Screening was not modelled.
- u_b is undefined where there are no baryons. In practice the IGM fills space; the lane did not test what a vacuum
  region would mean.
- Whether some other relative quantity, built with a non-convex or degenerate law function, escapes: not studied. The
  argument above says it would need J to be degenerate in the baryon acceleration, which the a0 law's J is not.

## Files

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`; `rel1.py` (2.3 s, sympy + scipy, one thread, ~140 MB) -> `rel1.out`, `rel1.json`;
MUTATE `REL1_MUTATE=M1|M2|M3` -> `rel1_MUTATE_M*.out/json`; `REL1.lean`, `REL1_MUTATE.lean`, `compile.txt`,
`compile_MUTATE.txt` (`cd fable_independent_2026/lean_2026 && lake env lean <absolute path>`).

The first full run read the K4 energy check as FAIL (drift divided by |H_O| ~ 1e-12) and the label as NO VERDICT; A1
(post hoc) set the normalization to the largest term; the rerun is the one kept. Before A1, an earlier attempt was
stopped by hand while a weak-field series for D' was still running (no number came from it). The D' limit check was
then rewritten to take the series of h.a_b alone, which is the same statement because D' = A - h.a_b by definition.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
