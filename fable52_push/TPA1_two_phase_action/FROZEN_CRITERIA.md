# TPA1 (two-phase action): FROZEN CRITERIA, committed alone before any TPA1 script, Lean file or graded number

TEST lane, quarantined. Adopts nothing and relabels nothing. Not registered. kappa = 1/2 FITTED; not theory closed. Footings
canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2) wherever a0 enters a number, never pooled. No LCDM input, no download.
This lane does not edit fable52_push/README.md, any PAPER file, the closure register or the memory index.

Id check before this file: `ls -d fable52_push/TPA1*` found nothing; `git log --all --oneline | grep TPA1` found nothing.

## 0. The question

The owner asked for the full two-phase theory written as one action with its equations. This lane writes the action, derives
its complete field equations, certifies them against direct variation, and states what they reduce to in every regime and what
they do not deliver. It grades no mechanism and no data gate.

## 1. The action (frozen)

Units c = 1, K = 4 pi G. PAPER70 Eq. (A) (QX17 conventions, PAPER70 'Definitions' paragraph) with one change:

    L/sqrt(-g) = [R - 2 Lambda]/(4K) + L_K(Q) + S(n_d) Lam_law + lambda n^m P_m + L_m ,

    L_K(Q)  = mu_K^2 (Q - 1)^2 / (2K)                          (= 2 mu_K^2 (Q-1)^2/(4K), PAPER70's dust term)
    Lam_law = P^m A_m - W(K|P|) - gamma_L F(Pi)                 (the law's whole Lagrangian: Legendre pair plus stiffness)
    W(p)    = (a0^2/K)[-p/a0 - ln(1 - p/a0)],  F = PAPER70's adopted stiffness (blend, b = rho_DE), Pi = D_m P^m.

Q, n_m, h_mn, l = ln Q, A_m = -h_m^n d_n l, D_m are PAPER70's. As in QX17's checker, P^m A_m is written -P^m d_m l and
Pi = nabla.P + P^m d_m l; the two forms differ by terms proportional to n.P, which the multiplier absorbs.

**The density the switch reads (two definitions, both carried).**
- **D1 (primary, certified in full).** n_d = mu_K^2 (Q - 1)/K = L_K'(Q). This is the charge density of the clock current
  n^m L_K'(Q) when the law sector is absent (QX17 E3 at P = 0), i.e. the "rho" of the record's charge N = rho + Pi
  (response_evolution_2026_11_09/DERIVATION.txt section 3). It is a function of Q alone, so S(n_d) = S(Q) adds no derivative
  and no new field.
- **D2 (reported, derived, not in the overall label).** n_d = N_2 = mu_K^2 (Q - 1)/K + Pi, the record's leading full charge
  N = rho + Pi with the law's own polarization. The exact charge of the switched action contains S itself, so a non-circular
  definition must use this S-independent leading form. For D2 the lane derives the P equation and the static reduction and
  states what differs from D1.

**The switch class.** S: [0, inf) -> [0, 1], C^2, non-increasing, S = 1 on [0, n_1] and S = 0 on [n_2, inf) (flat ends,
0 < n_1 < n_2), the threshold n_* between them. The exact phase statements (items 2, 5) use the flat ends. The identity checks
(item 1) use generic smooth test functions with non-zero S' and S'' at the test points, so they hold for every S.

**Reading choice R1 (frozen).** S multiplies the law's whole Lagrangian Lam_law (Legendre pair and stiffness); the constraint
lambda n.P does not carry S. Reasons, to be shown by the equations (item 1): (i) S on both P.A and W is what keeps the
unscreened Legendre map K|P| = a0|A|/(a0 + |A|) for every S > 0; S on one of them alone distorts it; (ii) with the stiffness
inside, the screened map (E2) is QX17's exactly wherever S is locally constant, 0 < S < 1, whereas with the stiffness outside
gamma_L becomes gamma_L/S; (iii) at S = 0 the stiffness, whose scale b = rho_DE is the law's own, vanishes with the rest of the
law; (iv) whether the constraint carries S is on-shell equivalent wherever S > 0 (lambda -> S lambda) and is kept bare so that
n.P = 0 holds in both phases. The literal form in the brief (stiffness bare, "V0") is certified alongside, because the closed
forms are written with two independent switches S_L (Legendre pair) and S_F (stiffness); R1 is S_F = S_L, V0 is S_F = 1.

## 2. Items, checks and labels

Every equation is derived by hand (route 1, closed form) and checked against a direct sympy variation of the action (route 2).
An item is **CERTIFIED** if both routes agree, every known answer passes and every MUTATE arm assigned to it fails; otherwise
**NOT CERTIFIED**, naming the check that failed.

### Item 1. Complete covariant Euler-Lagrange set (script tpa1_cov.py)

Route 2 exactly as QX17: sympy builds the Lagrangian density (non-GR part) on jet symbols in 2+1 dimensions (g_ab, d_c g_ab,
d tau, dd tau, P_a, d_b P_a, lambda), with S_L(Q), S_F(Q) independent explicit test functions of n_d, a generic polynomial W
and a generic polynomial F. Partial derivatives in the jet symbols are taken symbolically. Change from QX17: total derivatives
are evaluated exactly by truncated multivariate Taylor arithmetic (order 5, float64) on QX17-style random polynomial
configurations instead of mpmath finite differences, so the run takes minutes. Seeds 11, 22, 33; n.P = 0 imposed by P = h.V.

Checks (relative residual |a - b| / max(|a|, |b|), line 1e-8 on every component and seed):
- C1-P: the P equation (3 components) against EL in P_a.
- C1-tau: the clock equation against EL in tau.
- C1-g: the full non-GR stress tensor T^{ab} = (2/sqrt(-g)) dS/dg_ab (6 components).
- C1-B: the off-shell Noether identity of the closed forms, nabla^m T_mn = E_tau d_n tau + E_P^m (d_n P_m - d_m P_n)
  - P_n nabla_m E_P^m + E_lambda d_n lambda (3 components), with T, E_tau, E_P from route 1 only. On shell it is
  nabla^m T^X_mn = 0, i.e. matter conservation through the Bianchi identity. Line 1e-8 relative to the largest single term.

Known answers:
- KA1-1: closed forms at S_L = S_F = 1 equal QX17's closed forms (QX17D general-F stress) re-coded from PAPER70 (line 1e-10).
- KA1-2: closed forms at S_L = S_F = 0 equal GR with PAPER70's dust: T = T^Q + T^lambda, E_P = lambda n^m, clock charge n_d.
- KA1-3: C1-B passes with QX17's forms at S = 1.

MUTATE (each run writes its own tpa1_cov_MUTATE_<arm>.json/.out; each must exceed 1e-3 relative on at least one checked
component on every seed):
- M1 clock sign: the new term (S' terms) in the clock charge with the opposite sign. C1-tau must fail.
- M2a S on the constraint: route 2 varies S_L(Q) lambda n.P against R1's closed forms. Must fail (disclosed beforehand: this
  arm is on-shell equivalent where S > 0, so it bites the identity, not the physics).
- M2b literal form V0 (stiffness bare): route 2 with S_F = 1 against R1's closed forms (S_F = S_L). Must fail.
- M3 drop one stress component: the Q dS/dQ Lam_law n_m n_n term removed. C1-g and C1-B must fail.

### Item 2. FRW (script tpa1_reduce.py, sympy exact)

With dust at the cosmic density: show P = 0 is forced by isotropy, give the background equations for symbolic S, and the
leading change at S = epsilon on the background. Known answer: Qbar = 1 + I0/(2 mu_K^2 a^3), rho = I0(1 + w0/a^3)/(8 pi G a^3),
w = w0/(w0 + a^3) (QX17 K4 / C4 K7), exactly, for every S.

### Item 3. Linear perturbations about FRW (tpa1_reduce.py, sympy)

Unitary gauge (clock = time), scalar sector, symbolic S(Q) with Sbar, Sbar', Sbar''. Show: (a) the law sector's quadratic
Lagrangian is Sbar times the quadratic part of Lam_law, with no S' or S'' (they enter at cubic order); (b) at Sbar = 0 it
vanishes, so the linear theory is GR + baryons + the cold component; (c) at Sbar = epsilon, after eliminating P, the only change
is the replacement mu_K^2 Qbar^2 -> mu_K^2 Qbar^2 + epsilon k^2/a^2 in the coefficient of the lapse perturbation squared
(adopted blend: F''(0) = 0); (d) the quasi-static growth source of the cold component, route 1 by hand and route 2 from the
quadratic action's dispersion relation.
Known answers: epsilon = 1 gives the record's clock self-growth eigenvalue R f, f = 1/(1 + q^2/mu_K^2) (RK04 DERIVATION
section 4 at sigma = 0, alpha = 0); epsilon = 0 gives the isolated-fluid Jeans form R (1 - q^2/mu_K^2) that RK04 contrasts.
GAL1 bound (reported with the number, not graded as a gate): GAL1's 2 sigma allowance f <= 0.01968 (z_on 3) read as a source
boost q = 1.5 f/(1 - f); the bound on epsilon from the first correction at mu_K = mu_K* (KD1: 8.890e6 / 8.889e6 Mpc^-1) and
proper k up to 1 Mpc^-1. If the bound is vacuous it is reported as vacuous, with the mu_K below which it would bite.

### Item 4. Static weak field and the wall pressure (tpa1_reduce.py, sympy and numbers)

- 4a. Route 1: the P equation's leaf part at gamma_L = 0 plus (E4)_00 with the switched stress at Newtonian order. Route 2: EL of
  the static Lagrangian built from the action. Both for D1 with a static clock (n_d slaved to Phi) and with S's argument held.
  Known answer: with the argument held, exactly SWT1's class div[(1 - S/(1 + u)) grad Phi] + mu_K^2 Phi = 4 pi G rho_b; at
  S = 1 PAPER70's static equation. Any extra term the static clock produces is reported, not hidden.
- 4b. Wall pressure from the covariant equations, two routes: (A) the Noether identity of the switched law sector with S's
  argument held, nabla^m T^L_mn = Lam_law d_n S on the P shell, so the force density on whatever carries S is -Lam_law D_n S;
  (B) the S' term of the clock charge read as the law's partial pressure on the dust. Integrated across a planar wall at fixed
  displacement (sources fixed). Known answer: (a0^2/K) W(u), W = u - ln(1 + u) - u^2/(2(1 + u)^2), outward, equal to swt1.json
  KA_W1 'closed' at every y and KA_W3 'closed' at every radius to 1e-9 relative (canonical, as SWT1 ran it), and to the
  transcribed closed form on the alt footing.
- 4c. Compensation from the covariant energy density (Gauss with div(S P)): KA-CP3's tanh profile; exterior
  |M_eff/M_b - 1| <= 1e-6 beyond 1.2 R and the interior ratio at 0.5 R equal to swt1.json's 39.374089574428226 to 1e-9.
- MUTATE M1 (shared with item 1): with the clock term's sign flipped, route (B) must give an inward force at every y.

### Item 5. The two phases as exact solutions (tpa1_reduce.py; Lean)

- S = 1 phase (n_d <= n_1): every equation is QX17's (from KA1-1 with S' = S'' = 0); spherical static with mu_K = 0 gives
  g^2 = g_N (g + a0) (Lean). The condition for a static clock to stay in this phase is stated.
- S = 0 phase (n_d >= n_2): every equation is GR with PAPER70's dust; check that a0 is not a free symbol of the S = 0 equation
  set built with the physical W (sympy), and that P carries no stress there.
- Static existence: for a static clock n_d = mu_K^2 (Q_inf/N - 1)/K. Lean: S(n_d(N)) is monotone in N for any non-increasing S,
  so in a static configuration the law-on phase is a superlevel set of the potential.

### Item 6. Health (script tpa1_health.py; reported HEALTHY / UNHEALTHY / NOT DECIDED)

Decoupling limit (metric frozen at a static weak background, gamma_L = 0, P eliminated exactly by the Legendre maximum),
1+1 and 2+1 frozen-coefficient (WKB) quadratic action for the clock perturbation tau = t + pi in (i) the S = 0 phase, (ii) the
S = 1 phase, (iii) inside a smooth wall with the law's field on. Report the kinetic coefficient K(k) and gradient coefficient
G(k), symbolically in S, S', S''. Any new propagating mode S introduces is reported (counting time derivatives). Numbers at the
record's values: mu_K = mu_K* (both footings), n_* = {1, 1e3, 1e6} x today's mean cold density (KD1's I0), switch width
Delta n_d = n_*, field at the wall y in {0.01, 0.1, 1, 10}, and only WKB modes with k l_w >= 10 (l_w the wall thickness).
- UNHEALTHY if, at any grid point, a WKB mode has K < 0 (ghost) or G/K < 0 (gradient instability).
- HEALTHY if no grid point shows either and the symbolic coefficients show no sign change for any switch in the class.
- NOT DECIDED otherwise. The switch width that would be needed for health is reported either way.

### Item 7. What the equations do not deliver (required section of RESULT.md)

From the equations alone: the force available to move dust that is already bound around a galaxy (force density -Lam_law D S,
zero wherever S is uniform), its bound per wall (SNP1 A.1: F_w <= a0 M_b), and SNP1's verdict cited. RESULT.md says plainly
that the action as written does not by itself clear a disc of a collapsed share.

### D2 (reported)

tpa1_reduce.py derives the D2 P equation in the static weak field by both routes and states what differs from D1.

### Lean (TPA1.lean, compiled in the copy of fable_independent_2026/lean_2026 that has its Mathlib build)

Theorems: the Legendre map with S (S on both terms leaves u = x/(1 - x); S on P.A alone gives x = S u/(1 + S u)); the Legendre
value; the static S = 1 law; the stationarity of the leaf stress along fixed displacement and the stress jump equal to W(u)
(the wall identity from the covariant stress); the flipped clock term giving -W; the static-clock monotonicity. Standard axioms
only. TPA1_MUTATE.lean: false versions that must not compile. compile.txt and compile_MUTATE.txt without home paths.

## 3. Overall label

**EQUATIONS COMPLETE** if items 1 to 5 are CERTIFIED; otherwise the label names what is missing. Item 6 is reported as
HEALTHY / UNHEALTHY / NOT DECIDED. RESULT.md gives the labels first, then the item table, then section 7 in plain words.

## 4. Disclosure: what I worked out by hand before freezing (expectations, not results)

- FRW: P = 0 by isotropy and Lam_law(P = 0) = 0, so I expect the background to be PAPER70's for every S, with no change at
  S = epsilon at any order.
- Linear theory: Lam_law is quadratic in perturbations about P = 0, so I expect only Sbar to enter, as
  mu_K^2 -> mu_K^2 + epsilon k^2 (proper k). With mu_K near 8.9e6 Mpc^-1 I expect the correction to be of order
  epsilon (k/mu_K)^4 < 1e-27 and GAL1's bound on epsilon to be vacuous. I expect the growth source at epsilon = 1 to be RK04's.
- Static: with a static clock, n_d = -mu_K^2 Phi/K is slaved to the potential, so I expect the static equation to carry one term
  beyond SWT1's, mu_K^2 S'(n_d) J, a layer at the wall, which vanishes in each phase and when S's argument is held. I expect
  the wall pressure from the covariant stress to come out as the integral of J dS across the wall at fixed displacement,
  which equals W(u).
- Static existence: a static clock's dust is densest where the potential is deepest, so I expect the law-on phase to sit
  outside an equipotential, the opposite of a cleared disc.
- Health: from a leading-order gradient expansion I expect the clock's kinetic coefficient in the wall to pick up terms of
  order S'' W and S' Pi, and its gradient coefficient a term S' J, each multiplied by mu_K^2/K, which at the record's mu_K
  dwarf n_d and mu_K^2/K. I expect a sign change inside any wall narrower than an enormous width, i.e. UNHEALTHY. This
  expectation is not a result; the frozen rule above decides.
- Item 7: I expect the force to act only where S varies, to be balanced for a static clock by the weight of the switch's own
  energy layer, and therefore not to clear a share already bound in the well.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
