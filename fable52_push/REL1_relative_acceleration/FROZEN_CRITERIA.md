# REL1 (the law on the clock's acceleration relative to the baryon flow): FROZEN CRITERIA, committed alone before any script, Lean file or graded number

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Both footings (canonical a0 9.3603e-11,
alt 1.1312e-10 m/s^2), never pooled. The cold component is cold dark energy (the clock's dust), never a particle. Not a
LCDM lane. No download. This lane does not edit fable52_push/README.md, fable52_push/CLOSURE.md, any PAPER file, the
register, the owner's decision files, the memory index, or MK2's folder.

Id check: `ls -d fable52_push/REL1*` found nothing; `git log --all --oneline | grep REL1` found nothing. The lane was
asked for by the fable52 lead after the owner's "you can do it" in the lead chat (2026-11-10), with the warning that it
is a hand idea and may fail like the others.

## 0. The question

Action (A) (`closure_2026_11_06/QX17_covariant_field_equations/RESULT.md`) holds the law only where the clock is static,
because its Legendre pair P.A - W(K|P|) sees the clock's own acceleration A = n.grad n, which is zero for a free-falling
clock (FB1 note; COL1; FLD1). The candidate replaces A by an acceleration of the clock congruence relative to the baryon
flow u_b. Is there a covariant, well-defined action of this kind, and which of the record's failures does it remove or
create?

## 1. The candidate (frozen)

Notation as QX17 section 1. Baryons: a perfect fluid with four-velocity u_b, rest density rho_b, written as a
Lagrangian-coordinate (pull-back) fluid so that u_b is varied with the matter. gamma = -n.u_b >= 1. The baryons' velocity
relative to the clock, on the leaves: w^m = h^m_n u_b^n / gamma.

**Primary definition D (frozen):**

    A_rel^m := h^m_n n^r nabla_r ( u_b^n / gamma )           ( = A^m + h^m_n n^r nabla_r w^n )

that is, the clock's acceleration plus the rate at which the baryons' relative velocity changes along the clock. The
action is (A) with P^m A_m replaced by P^m A_rel_m and nothing else changed:

    S = Int sqrt(-g) { [R - 2 Lambda + 2 mu_K^2 (Q-1)^2]/(4K) + P^m A_rel_m - W(K|P|) - gamma_L F(Pi) + lambda n^m P_m }
        + S_b[g, baryon fluid] .

The required limits, each checked by item K1 below (exact symbolic, not by hand):
- (i) baryons comoving with the clock (u_b = n): A_rel = A exactly, so action (A) and QX17's equations come back;
- (ii) static clock, steady baryon flow (orbiting or held): A_rel = A;
- (iii) free-falling clock, baryons held at rest in a static potential: A_rel = grad Phi to Newtonian order.

**Disclosed alternatives (reported beside D, never substituted for it):**
- D' : A_rel = A - h.a_b (difference of the two proper accelerations, a_b = u_b.nabla u_b). Same steps 1 and 2 items.
- V0 : A_rel = A + h.(w.nabla n) (the clock's acceleration plus its shear seen by the moving baryons; no derivative of
  u_b). It meets (iii) only for a steady infall. Reported in step 1 only, argued, with its own line in RESULT.md.

## 2. Items, in order; the lane stops at the first structural failure and reports it as the result

**Step 1. Definition and consistency.**
- K1 (definition): sympy exact checks of limits (i)-(iii) for D and D' in 2+1 (static metric with lapse N(x, y) for (i)
  and (ii); weak static metric with a moving clock for (iii)). A limit that fails = D (or D') does not meet the brief.
- K2 (matter's kinetic structure): u_b enters A_rel through its derivative along n. P carries no time derivative in (A)
  (QX17 section 1), so at gamma_L = 0 P is eliminated exactly by the Legendre maximum, giving the matter Lagrangian
  term J(|A_rel|), J(y) = (a0^2/K)[y/a0 - ln(1 + y/a0)] (QX17 K0). sympy computes the Hessian of J(|A_rel|) in the
  baryons' second time derivative (Lagrangian displacement xi, about a static background).
  **Structural test S1 (Ostrogradsky):** if that Hessian is non-degenerate, the baryon sector is a non-degenerate
  higher-derivative system: its Ostrogradsky Hamiltonian is linear in one momentum, unbounded below. Then sympy derives
  the linearized Euler-Lagrange equation for xi and its characteristic roots; a real positive s (growth e^{s t}) is a
  runaway of matter. S1 fails if the Hessian is non-degenerate on an open set of backgrounds that includes ordinary
  matter, and the runaway rate there is faster than 1 / (age of the universe). Rates are reported for water/rock,
  Earth, platinum and titanium (MICROSCOPE's masses), interstellar gas (1 cm^-3), halo gas (1e-4 cm^-3) and the mean
  baryon density, both footings, at u = |A_rel|/a0 = 0 and at the background u of a test mass in Earth orbit (r = 7081 km).
- K3 (gamma_L > 0): whether the stiffness removes the degeneracy found in K2. Done by the linear algebra of the screened
  constitutive law (QX17 E2) for a displacement pattern with no divergence; argued, stated as such.
- K4 (nonlinear check): the 1D reduced system L = rho xdot^2/2 - rho Phi(x) + J(|xddot + Phi'|) in a uniform field,
  integrated numerically from a perturbation eps = 1e-12 a0 of the acceleration; report the time to blow-up and the
  conservation of its Ostrogradsky energy (Noether for time translation; drift line 1e-8 relative).
- K5 (the other exit): if u_b is NOT varied (a background flow), state the Noether/Bianchi consequence: the divergence
  of the non-GR stress on shell. Shown in the reduced system as non-conservation of energy (explicit time dependence).
- K6 (WEP): the composition dependence implied by K2/K4 (runaway rate depends on rho_b), and the order-reduced static
  force on a compact free-falling body, against MICROSCOPE (|eta| ~ 1e-15). Argued, with numbers.

**Steps 2-7** (statics; double counting; one mu_K; Solar System and moving sources; SCS1's coupled dispersion; clusters
and the Bullet) as the lead's brief lists them, run only if step 1 passes. If step 1 fails they are listed as NOT GRADED.

## 3. Labels, per footing (frozen)

- **NOT WELL-DEFINED (why)**: S1 fails (Ostrogradsky runaway of ordinary matter), or the action cannot be written with
  u_b varied without breaking the Bianchi identity, or a required limit of K1 fails for D.
- **FAILS (first failing item and by how much)**: step 1 well-defined, a later graded row fails.
- **WELL-DEFINED AND PASSES THE GRADED ROWS (list rows not graded)**.
- **NO VERDICT**: a known answer fails, or a MUTATE twin does not bite where it must.

If D is NOT WELL-DEFINED, D' and V0 are reported with what step 1 says about them; they do not change D's label.

## 4. Known answers (must pass or NO VERDICT)

- KA1: QX17 K0: max_P [P y - W(K P)] = (a0^2/K)[u - ln(1 + u)], sympy exact.
- KA2: with the u_b coupling switched off (A_rel -> A), the static spherical balance is the law g^2 = g_N (g + a0)
  (sympy; Lean QX1.balance_iff_lawS is the record's certificate).
- KA3: dust-only limit (P = 0): every new term vanishes, the action is GR with the clock's dust and baryons.
- KA4: K4's integrator reproduces the linear growth rate sqrt(K rho) at small amplitude to 1e-3 relative.
- MK1's and QX8's numbers: reproduced only if steps 3-4 are reached and reuse them.

## 5. MUTATE (separate outputs, each must bite; any that does not is disclosed)

- M1: sign of the Christoffel (gravity) term flipped in K1's limit (iii) -> limit (iii) must fail.
- M2: the u_b coupling removed from A_rel (A_rel = A) -> the Hessian in xi'' must become degenerate (zero) and the
  runaway root must disappear.
- M3: J replaced by a concave function (sign of J'' flipped) -> the runaway root must become oscillatory (s^2 < 0); the
  Ostrogradsky Hamiltonian must stay linear in one momentum (shows the ghost does not depend on that sign).

## 6. Lean (with a MUTATE twin that must not compile)

Closed forms: the runaway root s^2 = (rho + sqrt(rho^2 + 4 Jpp k)) / (2 Jpp) > 0 of Jpp s^4 - rho s^2 - k = 0 for
Jpp > 0, rho > 0, k >= 0 (elastic or pressure restoring force does not remove it); the Ostrogradsky Hamiltonian
H = p1 q2 + p2^2/(2 Jpp) - rho q2^2/2 + k q1^2/2 takes values below any bound; the Hessian eigenvalues of J at u:
1/(K (1+u)^2) along A_rel and 1/(K (1+u)) across it, both > 0. Compile:
`cd fable_independent_2026/lean_2026 && lake env lean <absolute path>`.

## 7. Before any script (disclosed)

Hand reasoning before this file: I expect S1 to fail for D and D', because any vector that gives grad Phi for a
free-falling clock past baryons at rest must contain the Christoffel symbol, which appears only next to the time
derivative of u_b (equivalence principle), and J is strictly convex. That expectation is not a result; K1-K4 decide.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
