# SCS1 (static clock, coupled stability): FROZEN CRITERIA, committed alone before any SCS1 script, Lean file or number

TEST lane, quarantined. Adopts nothing and relabels nothing. Not registered. kappa = 1/2 FITTED; not theory closed. Footings
canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), never pooled. No LCDM input, no download. This lane does not edit
fable52_push/README.md, any PAPER file, the closure register, the owner's decision files or the memory index.

Id check: `ls -d fable52_push/SCS1*` found nothing; `git log --all --oneline | grep SCS1` found nothing. The lane was asked
for by the fable52 lead on the owner's instruction ("Yes, run it", lead chat, 2026-11-09), after the owner chose form B
(closure_2026_11_09/OWNER_DECISION_2026-11-09_FINAL_FORM_B.md) and after TPA1 (origin 347967f64f) reported the law-on
static clock gradient-unstable in the decoupling limit.

## 0. The question

Is the static clock of action (A) (PAPER70 / QX17 = TPA1's S = 1 phase), carrying little or no dust of its own, linearly
stable when the metric is not frozen? This is form B's static state: the law's halo is the sector's own gravitating
density D.P on the one conserved clock current (fable52_push/FB1_form_b_from_the_action/NOTE.md).

## 1. The system (frozen)

Action (A) at S = 1, units c = 1, K = 4 pi G:
L/sqrt(-g) = [R - 2 Lambda]/(4K) + mu_K^2 (Q-1)^2/(2K) + P.A - W(K|P|) - gamma_L F(Pi) + lambda n.P + L_m.

- **Background.** Static weak field of a point baryon mass M_b on the law: N = exp(Phi), Phi' = g(r),
  g^2 = g_N (g + a0); static clock tau = Q_inf t (Q = Q_inf/N), so n_d = mu_K^2 (Q_inf/N - 1)/K; P from the Legendre map.
  The background's own dust gravity is neglected (stated; it is a bracket quantity only).
- **Perturbations.** Clock tau = Q_inf t + pi; P perturbed and, at gamma_L = 0, eliminated exactly by the Legendre maximum
  (it carries no time derivative); metric in **Newtonian gauge** (zero shift, no E): g_tt = -(N (1 + phi))^2,
  g_ij = (1 - 2 psi) delta_ij. The metric perturbations are quasi-static (no phi_t, psi_t: their terms are 1PN for motions
  on free-fall times). The shift and the momentum constraint are 1PN for such motions and are dropped by order counting
  (stated, not computed). GR's part is its Newtonian quadratic Lagrangian (|grad psi|^2 - 2 grad phi . grad psi)/(2K),
  the same as TPA1 item 3 used.
- **Primary configuration:** gamma_L = 0, mu_K = 0 (so n_d = 0), the spherical point-mass background, coupled.
- **Brackets (reported, each with its own label):** mu_K = 0.1 Mpc^-1 (the record's galaxy bound) with
  n_d in {0, 1, 1e3 x mean, n_crit}; mu_K = mu_K* (KD1: 8.890e6 / 8.889e6 Mpc^-1) with the same n_d; the stiffness on
  (gamma_L = K Lstar^2/2, Lstar 21.7 / 22.9 pc, maximal branch F'' = 1), from the hand closed form only. Here
  mean = I0/(2K) with KD1's I0 = 4.037e-8 Mpc^-2, and n_crit is TPA1's planar threshold -dp/dr at the same radius.

## 2. Two routes

- **Route 1 (WKB, full covariant).** As TPA1 item 6 but in 3+1 with phi and psi: sympy builds the non-GR Lagrangian
  sqrt(-g)[L_K(Q) + J(|A|)] on jets of pi (first and second order), phi and psi (value and first order); its Hessian in
  the jets gives the coefficient functions; the symbol of the Euler-Lagrange operator on a plane wave keeps every
  coefficient's spatial derivatives (60-digit mp.diff). The background is a local Taylor model of N in (x, y, z) about
  (r, 0, 0): **spherical** (N = N(|x|), transverse curvature included) for every graded row, **planar** (N = N(x), TPA1's
  model) for the known answer and MUTATE M3 only. det of the 3x3 symbol (pi, phi, psi) = 0 gives omega; growth
  Gamma = max |Im omega|.
- **Route 2 (radial eigenvalue solve).** The Newtonian-order quadratic Lagrangian written by hand,

      L2 = -|grad phi|^2/(2K) + (1/2) grad chi . J'' . grad chi + (mu_K^2/2K) chi^2 - (n_d/2)|grad pi|^2
           + Pbar . grad(|grad pi|^2)/2 ,      chi = phi - pi_t ,  psi = phi ,

  is checked against route 1 at kr >= 1e3 (line: relative 1e-3, both footings) and then solved globally for l = 0, 1, 2
  about the point mass on log-uniform radial grids of N = 200, 400, 800 nodes on [3 kpc, 1 Mpc], Dirichlet ends, as a
  generalized eigenproblem in lambda = omega^2 (pi eliminated through pi_t = phi - chi). The tilt term is discretized as
  written (not integrated by parts by hand). Unstable: lambda < 0 or complex.

## 3. Grid (frozen)

- Masses log M_b 9.4, 10.45, 10.7, 10.9 at radii 10, 30, 100, 300 kpc; plus TPA1's item-6 points (log M_b 10.45 at
  y = 0.01, 0.1, 1, 10).
- Wavenumbers kr in {10, 1e2, 1e3, 1e4, 1e5}; directions radial, tangential, 45 degrees.
- Both footings.

## 4. Labels (per footing, primary configuration; the same rule labels each bracket)

- **STABLE:** route 1 finds no growing root (Gamma below 1e-6 of the local free-fall rate) at every grid point, and route 2
  finds no lambda < 0 and no complex lambda for l = 0, 1, 2 at every resolution.
- **JEANS-ONLY:** growing modes exist; the growth is bounded in k (Gamma(kr = 1e5)/Gamma(kr = 1e3) <= 1.1 at every growing
  point; route 2's most negative lambda changes by <= 10 % from N = 400 to 800); and Gamma <= 10 x the local free-fall rate
  sqrt(4 pi G rho_loc), rho_loc = n_d + D.Pbar.
- **GRADIENT-UNSTABLE:** at some grid point Gamma(kr = 1e5)/Gamma(kr = 1e3) >= 10, or route 2's most negative lambda grows by
  a factor >= 3 from N = 400 to 800. The range of e-folding times is quoted.
- **NO VERDICT:** any known answer fails, the two routes disagree on the label, or the growth is bounded but faster than
  10 x free fall.
- Reported beside each growing mode: e-folding time, the local free-fall time 1/sqrt(4 pi G rho_loc) and r/v_c, and the
  mode's composition (delta n_d against delta(D.P): whether it moves dust, halo, or both with the same sign).

## 5. Known answers (all must pass, or the label is NO VERDICT)

- **KA1** Decoupling limit (phi, psi dropped), planar background, mu_K*: route 1 reproduces TPA1 item 6's S = 1 rows
  (K, c0, omega^2 to relative 1e-6) and its e-folding range 5.03e6 to 6.25e8 yr (three significant digits).
- **KA2** S = 0 (dust) phase, flat background, mu_K*: omega^2 equals (K n_d/mu_K^2)(k^2 - mu_K^2) to 1e-6; the growth rate
  at k << mu_K is sqrt(4 pi G n_d) to 1 %; no growth for k >= 10 mu_K.
- **KA3** The TPA1 hand claim "mixing rescales the kinetic coefficient by 1/(1 - S K J'') and leaves the gradient
  coefficient unchanged" is tested on the constraint surface (route 1 coefficients, phi and psi eliminated) at mu_K = 0
  and at mu_K*, to 1e-6. RESULT.md says plainly where it is wrong.
- **KA4** The point mass with the law switched off (S = 0, n_d = 0) has no growing mode in either route.

## 6. MUTATE (separate output files; each must bite, or the failure to bite is disclosed)

- **M1 (as asked):** flip the sign of every clock-metric mixing entry (pi-phi and pi-psi Hessian entries). Disclosed before
  any run: this equals the field redefinition (phi, psi) -> (-phi, -psi), so it cannot change any eigenvalue; it is
  expected NOT to bite. **M1b** flips the mixing inside the law's term only (keeping the dust term's), which is not a
  redefinition where mu_K > 0; it must change omega^2 at the mu_K* rows (relative >= 1e-3).
- **M2:** drop the mixing (pi-phi and pi-psi entries set to zero): must return the decoupled result (relative 1e-12).
- **M3 (my choice):** the planar background (TPA1's model, no transverse curvature) on the primary configuration: must
  change the primary label.

## 7. Lean (TPA1-style, in fable_independent_2026/lean_2026 inside the repo)

Closed forms of the dispersion relation: the constraint elimination of phi; omega^2 = K G [(1 - K m) k^2 - mu_K^2] /
(mu_K^2 + K m k^2) with G = n_d + D.Pbar and m = khat.J''.khat; the bounded high-k decomposition; stability at mu_K = 0 for
G > 0 and 0 < K m < 1; K m < 1 for u > 0; the mixing factor 1/(1 - K m - mu_K^2/k^2); the dust Jeans limit; the stiffness
form; the spherical divergence p' + 2p/r. A twin with false versions must not compile.

## 8. Disclosure: hand expectations before any number

- The lead's and TPA1's expectation: the gradient instability survives coupling.
- **Mine, worked out while writing these criteria, contradicts it.** At Newtonian order the tilt term
  Pbar . grad(|grad pi|^2)/2 integrates to -(1/2)(div Pbar)|grad pi|^2 in three dimensions, so the clock's gradient
  coefficient is G = n_d + D.Pbar, the clock's own charge density (N = rho + Pi). TPA1's 2+1 planar background has
  div Pbar = p', which is negative for a field falling outward; around a real point mass D.Pbar = p' + 2p/r is the phantom
  density, which is positive. I therefore expect form B's static state to be **STABLE** in the primary configuration,
  TPA1's S = 1 instability to be an artefact of its planar background (M3 should reproduce it), and the growth to be
  bounded in k without the stiffness in every configuration (omega^2 -> G (1 - K m)/m). With mu_K* I expect Jeans growth at
  sqrt(4 pi G (n_d + D.Pbar)). With the stiffness on and G < 0 the growth would rise with k above 1/Lstar. I expect the
  hand claim KA3 to hold only at mu_K = 0 (the full factor carrying -mu_K^2/k^2). These are expectations; the frozen rules
  above decide.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
