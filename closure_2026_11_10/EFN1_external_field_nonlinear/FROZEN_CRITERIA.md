# EFN1 (the nonlinear outcome of SCS3's external-field instability): FROZEN CRITERIA, committed alone before any EFN1 script or number

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings canonical (a0 9.3603e-11 m/s^2) and
alt (1.1312e-10 m/s^2), never pooled. The component is cold dark energy; no particle is added anywhere. No download. This
lane does not edit SCS1 / SCS2 / SCS3 files, any PAPER72 file, the register or the decision files; code it needs from SCS2 /
SCS3 is copied into this folder unedited and named.

Id check: `ls closure_2026_11_10 | grep -i efn` and `git log --all --oneline | grep -i efn1` found nothing.

## 0. The question

SCS3 (fable52_push/SCS3_external_field_stability, result origin e6a6dc2cf2) found the static clock of form B unstable around a
disc in a uniform external field g_e, in a shell r >~ 0.74 r_e (r_e = sqrt(G M a0)/g_e) where the law's phantom density D.P is
negative; e-folding 0.73-2.0 Gyr at g_e = 0.1 a0. Its line: whether the growth "saturates, reshapes the outer halo or leaves
the static branch is not computed." EFN1 computes that nonlinear outcome.

## 1. The equations (from action (A), same reduction as SCS1-SCS3)

Action (A) (QX17 section 0) at mu_K = 0, gamma_L = 0, with no dust of the clock's own (n_d = 0). Approximations, all as in
SCS1/SCS2/SCS3: Newtonian order (Phi, d_t pi and |grad pi|^2 of order eps, d_t ~ eps^1/2 d_x); quasi-static metric with
psi = phi; shift, momentum constraint, sqrt(-g) and projector corrections dropped as 1PN; P eliminated by its Legendre
maximum (gamma_L = 0); the multiplier's leafwise flux lambda P/Q dropped (it is eps times the advective flux; stated, and
shown by order counting in the sympy file). Units: kpc, km/s, Msun, K = 4 pi G.

Clock tau = t + pi. To this order the leaf lapse is ln N_tau = S, with

    S = Phi - d_t pi + |grad pi|^2 / 2          (to be verified by sympy from -g^{mn} d_m tau d_n tau),

the leaf acceleration is A = grad S, and the reduced Lagrangian is

    L = -|grad Phi|^2/(2K) - rho_b Phi + J(|grad S|),   K J'(A) = a0 A/(a0 + A),   K J = a0 A - a0^2 ln(1 + A/a0).

Its Euler-Lagrange equations (to be verified by sympy), with P = J'(|A|) A/|A| and N = div P (the law's phantom density):

    (E-Phi)  lap Phi = K (rho_b + N)
    (E-pi)   d_t N + div(N v) = 0,   v = -grad pi          (the conserved clock current; QX17 E3 at this order)
    (def)    d_t pi = Phi - S + |grad pi|^2/2,   with S fixed by div P(grad S) = N.

Static state (SCS3's background): pi = 0, S = Phi_0, N_0 = D.P. Evolved form, perturbation variables (exact, not
linearised): Phi = Phi_0 + phi, S = Phi_0 + s, N = N_0 + n,

    d_t pi = phi - s + |grad pi|^2/2,   lap phi = K n,   div[P(grad Phi_0 + grad s)] - div[P(grad Phi_0)] = n,
    d_t n = div[(N_0 + n) grad pi].

**Known answer KA-a (sympy, graded):** (i) the lapse expansion gives S above with residual 0 at order eps; (ii) the
linearisation of (E-Phi, E-pi) about the static state equals the Euler-Lagrange equations of SCS1's quadratic Lagrangian
L2 = -|grad phi|^2/(2K) + (1/2) grad chi . J'' . grad chi + Pbar . grad(|grad pi|^2)/2, chi = phi - pi_t (mu_K = n_d = 0),
residual 0; (iii) the constant-coefficient high-k symbol of the linearised system is omega^2 = G (1 - K m)/m with G = D.P,
m = khat.J''.khat (SCS3's route L operator), residual 0. Any non-zero residual: every label NO VERDICT.

## 2. Setting (cheapest decisive case first, by name)

- **Graded set:** the axial family (g_e along the disc axis, 2-D axisymmetric, full theta) at g_e = 0.1 a0, on exactly the
  backgrounds SCS3's A4 reading lists as converged (UNSTABLE by rule) at 0.1 a0:
  - canonical: expo 9.4, expo 10.45, expo 10.7, kuzmin 9.4, kuzmin 10.7, kuzmin 10.9;
  - alt: expo 9.4, expo 10.45, expo 10.7, expo 10.9, kuzmin 9.4, kuzmin 10.9.
  Backgrounds are built by SCS2's solver (scs2_aqual.py, copied unedited from SCS3's folder) on SCS3's AX grids R_k
  (AX_BASE, r from 1e-4 R_d to max(1e3 R_d, 10 r_e)), Picard tolerance 1e-8 as frozen there.
- **Dynamic region:** pi and n evolve only on cells with r >= r_in = 0.4 r_e (the negative region starts at 0.74-0.85 r_e;
  by SCS3's RESULT that start is 10-35 R_d at 0.1 a0, so R_d <~ 0.08 r_e and r_in >~ 5 R_d on every graded background). Inside r_in, pi = n = 0 for all time (the inner halo and the disc
  are held static: stated approximation); faces at r_in and at r_max carry no clock flux. phi and s are solved on the whole
  grid (Dirichlet 0 at r_max, as SCS3's linearised far field; no condition needed at the inner sphere beyond SCS2's mirror
  ghost).
- **Grids:** R2, R3, R4 of SCS3 (refinement 1.5). R3 and R4 are graded; R2 is reported.
- **Extensions, stated in advance:** if every graded run has finished within 3 hours of compute in all, one converged
  0.01 a0 axial background per footing (expo 9.4, both footings converged in SCS3 A4) is run at R3 and R4 to 14 e-folds and
  labelled by the same rule (reported beside, not in the lane label; 14 e-folds at 0.01 a0 is 310-360 Gyr, far beyond t_H, and
  RESULT.md says so). **Not attempted in this lane:** the in-plane family (3-D, its linear rates were not converged by SCS3),
  the thick-disc twin and the disc-centre null (DCN1's question), extended or non-uniform external fields, gamma_L > 0,
  mu_K > 0. RESULT.md lists them as not computed.

## 3. Two routes

### Route D (direct, decides)

Time-stepping of the perturbation equations of section 1 from the static state plus a seed:
- **Discretisation:** SCS2's finite-volume faces and cell gradients. phi: the face Laplacian (coefficient 1), sparse LU once.
  s: the nonlinear face flux of SCS2's phantom(): K P_f . n_f = (Phi_k' - Phi_k)/d_f / (1 + u_f), u_f from the normal
  difference and the averaged tangential cell gradients (face_mu), solved for s by a quasi-Newton iteration on the
  background's normal-derivative Jacobian (LU once; refactorised at the current state if 30 iterations do not reach a
  relative residual of 1e-10). pi_t: phi - s + |grad pi|^2/2 with SCS2's cell gradient. n_t: the face flux
  N_f (pi_k' - pi_k) A_f/d_f with N_f = the face average of N_0 (the symmetric operator SCS3's L_G uses) plus the upwind n
  (upwind with respect to v = -grad pi).
- **Integrator:** classical RK4. dt = min(0.02/Gamma_ref, 0.25/omega_max, 0.25 min_cells h/|v|), Gamma_ref = 1/(SCS3's A4
  converged e-folding time), omega_max = the largest local rate sqrt(4 pi G |D.P| u (2 + u)) over the dynamic region.
- **Seed:** a smooth Lagrangian displacement xi = eps r_e exp(-(r - r*)^2/(2 (0.2 r_e)^2) - (theta - theta*)^2/(2 (0.2)^2)) rhat,
  with (r*, theta*) the route-L maximum cell of the same grid; initial n = -div(N_0 xi) (face form), pi = 0. Primary
  eps = 1e-4, positive sign.
- **Amplitude:** a(t) = max over dynamic cells |n| / |min over dynamic cells of N_0|. Also recorded: max|v|, and the relative
  change of the radial acceleration, dg(r) = max over theta of |d_r phi| / |grad Phi_0|, and its theta mean, at
  r/r_e = 0.5, 0.75, 1, 1.5, 2, 4.
- **Run length:** t_end = 14 / Gamma_ref, or a stop line.
- **Stop lines (breakdown):** F1 density fold: a(t) >= 10; F2 inverse map breakdown: the s iteration does not reach 1e-10
  after one refactorisation and 60 more iterations; F3 time-step collapse: dt < 1e-3 of the initial dt; F4 non-finite value.
  The time t_F and the stop line are recorded with the cell where a(t) is largest.

### Route W (weakly nonlinear; supporting)

On the same discrete operator (dynamic region, grids R2 and R3; R4 if the block LU stays under 4 GB): the leading eigenpair of
the linear system y_t = L y, y = (pi, n), L = [[0, M], [-L_G, 0]], M n = phi(n) - s_lin(n), by shift-invert on SCS3's 3n block
system; the left eigenvector by the transposed solves. Unstable-manifold expansion y = a e + a^2 h2 + a^3 h3, normal form
da/dt = Gamma a + c2 a^2 + c3 a^3, with c2 = <e+, N2(e,e)>, (2 Gamma - L) h2 = N2(e,e) - c2 e, c3 = <e+, 2 N2(e,h2) + N3(e,e,e)>,
where N2, N3 are the quadratic and cubic parts of the discrete right-hand side (the s-map's second and third directional
derivatives by a 4-point stencil in the amplitude, step 1e-3 and 5e-4, Richardson-combined). The eigenvector is normalised
so that a = 1 means max|n| = |min N_0| (the same scale as route D's a).
- **Converged** iff Gamma, c2 and c3 each change by <= 20 % from the coarser to the finer of the two finest grids run.
- **Reading (only if converged):** SATURATES-W if for both signs of a the normal form has a stable fixed point with
  |a*| <= 0.3; RUNAWAY-W (counts as LEAVES) if for at least one sign it has no fixed point with |a| <= 1; otherwise
  INCONCLUSIVE-W. Not converged: route W reads NO VERDICT.
- **Which route decides:** route D. Route W is reported beside it; a disagreement between a converged route W and route D is
  reported, and the background's label is then route D's with the note "routes disagree". If route D cannot be made to work
  on a background (a known answer of route D fails), that background is graded by route W alone and labelled no stronger than
  route W's reading, with NO VERDICT where route W is not converged.

## 4. Outcome labels (per background and footing; route D on R3 and R4)

- **LEAVES THE STATIC BRANCH:** on both R3 and R4 a stop line F1-F4 is met before t_end, with the same stop line and
  t_F(R3), t_F(R4) differing by <= 0.5 / Gamma_ref; or (unbounded growth) a(t_end) >= 1 on both grids with the fitted growth
  rate of a over the last 3 e-folds >= 0.3 Gamma_ref.
- **SATURATES:** on both grids no stop line, a(t) over the last 3 e-folds of the run has max/min <= 1.5 and a fitted rate
  <= 0.1 Gamma_ref, and dg(r) <= 10 % at every listed radius >= 0.75 r_e (theta max) at t_end. Reported: a(t_end) as the
  fraction of |min N_0|, and dg at the listed radii.
- **RESHAPES:** as SATURATES, but dg(r) > 10 % (theta max) at some listed radius >= 0.75 r_e at t_end.
- **NO VERDICT:** a known answer of section 5 fails for that background, or R3 and R4 give different labels, or the label's
  numbers fail the refinement lines above, or none of the above is met (for example a still growing but below 1 at t_end).

**Lane label, per footing:** the common label of the six graded backgrounds if they all agree; if they differ and none is
NO VERDICT, MIXED with the counts; if any is NO VERDICT, NO VERDICT with the others reported. Written canonical / alt. The 0.01
a0 extension is reported beside, never folded in.

## 5. Known answers (a fail makes the affected label NO VERDICT)

- **KA-a** the sympy checks of section 1 (all labels).
- **KA-b** linear growth, per background on R3 and R4: (b1) route W's leading discrete Gamma (R3; R4 where run) equals SCS3's A4
  converged route-L rate for that background to 10 % (Gamma, not Gamma^2); (b2) route D with the nonlinear terms switched off,
  seeded with the leading eigenvector at 1e-8, grows at route W's Gamma to 2 % over 5 e-folds (run on R3 on the four
  mutation backgrounds below); (b3) route D's primary run, over its first e-folds where a < 1e-2, grows at a fitted rate
  within [0.5, 1.10] Gamma_ref (the smooth seed's rate approaches the continuum edge from below, so only an upper excess is a
  failure of the reduction; below 0.5 is also a failure).
- **KA-c** external field off: the isolated twin (SCS2's isolated disc of the same kind and mass, built on the same full-theta
  R3 grid and the same r range and dynamic region as its 0.1 a0 twin): route W's leading eigenvalue has Gamma^2 <= 1e-3
  Gamma_ref^2 (no growth), and route D seeded the same way keeps a(t) <= 2 a(0) to t_end. Run on the four mutation backgrounds.
- **KA-d** no seed: route D in the full (not perturbative) form, phi from the full Poisson solve of K (rho_b + N_0 + n) minus
  Phi_0 and s from the full nonlinear solve of N_0 + n minus Phi_0 (so the background's Picard residual is the only seed): its
  a(t) stays <= 0.1 times the primary run's a(t) at every recorded time up to the primary run's t_F or t_end. Run on R3 on the
  four mutation backgrounds; the perturbative form with no seed must stay exactly zero (checked on every background).
- **KA-e** refinement: the label is the same on R3 and R4 (section 4); and on R3, halving all three dt factors changes t_F by
  <= 0.1 / Gamma_ref (or, without a stop line, a(t_end) by <= 5 %). Run on every graded background.

## 6. MUTATE twins (separate `_MUTATE` outputs; on R3; on four backgrounds: canonical expo 9.4 and kuzmin 10.9, alt expo 9.4 and kuzmin 10.9)

- **M1 seed x 10 (eps = 1e-3):** bites if it reproduces the label and, for LEAVES, t_F moves earlier by ln(10)/Gamma_ref to
  within +-0.5 / Gamma_ref; for SATURATES / RESHAPES, a(t_end) within 20 % of the primary. Otherwise the label rests on the
  seed: disclosed, and the background's label is reported as seed-dependent.
- **M2 sign of every nonlinear term flipped** (|grad pi|^2/2, the upwind n flux and the s-map's nonlinear part): must change
  the trajectory: a different stop line, or t_F or a(t_end) different by more than 0.5 e-folds / 20 %, or the location of the
  maximum moved by > 0.2 r_e. Disclosed now: flipping only the quadratic part is the same as flipping the seed's sign at
  quadratic order, so M2 tests whether the outcome depends on the sign of the perturbation.
- **M3 nonlinear terms removed** (linear run): must reach t_end without F1-F3 and with a(t_end) = a(0) times its linear growth;
  if the primary is LEAVES, this bites by changing the label (the fold is then due to the nonlinear terms, not the integrator).
- **M4 route W with the s-map's second derivative sign flipped:** c2 must change sign (relative change >= 1.5) on R3.

## 7. Hand estimates, written before any number

- The perturbation system is a pressureless fluid (the phantom density N carried by the clock's tilt v = -grad pi) moving in
  the force -grad(phi - s). Linearly, the force on a density excess is gravity-like (both phi and s go as n/k^2) with
  effective constant (1/m - K) > 0, and where N_0 < 0 it pulls the flow into regions of more negative N: cold collapse of a
  negative-density fluid. The linear rate is the same at every k (SCS3: route 2 is the high-k limit), so there is no isolated
  slow mode; the edge of the spectrum is at the grid scale.
- I therefore expect **route D: LEAVES THE STATIC BRANCH by a density fold (F1)**, a caustic of the clock flow in the
  negative shell near the route-L maximum (0.85-0.95 r_e, about 40 degrees off the axis), at roughly
  t_F ~ [ln(1/eps) - 2 to 0] / Gamma, i.e. about 7-10 e-folds for eps = 1e-4: 6-20 Gyr at 0.1 a0. Same on both footings.
  Pressureless folds converge in time under refinement, so I expect KA-e to pass for t_F.
- **Route W:** NO VERDICT (not converged). The leading discrete mode is the continuum edge, localised at the grid scale near
  the route-L maximum, so c2 and c3 depend on the cell size. If it does converge, I expect c2 != 0 (no symmetry pi -> -pi),
  hence RUNAWAY-W for one sign.
- **M1** bites (t_F earlier by about ln 10); **M2** changes the fold's location or time; **M3** grows linearly to t_end.
- These are expectations, not results; the rules above decide.

## 8. Compute and repository rules

At most 4 threads, nice 19, one heavy job at a time, resident memory under 4 GB, at least 5 GB disk free; runs checkpoint to a
partial json per run and stop cleanly on SIGTERM; no field dumps beyond small arrays; background caches go to the system temp
directory and are removed. While the BX1 queue is live on the machine, only light work is done here. Commits with explicit
paths only; no push from this lane. A change after this freeze goes into a dated amendment file committed alone, and both
readings are reported.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
