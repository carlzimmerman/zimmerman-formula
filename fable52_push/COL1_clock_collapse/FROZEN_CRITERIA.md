# COL1 FROZEN CRITERIA: does a free-falling clock end in the static-clock state? (2026-11-10)

Committed alone, before any script or graded number. TEST lane, quarantined: adopts nothing, relabels nothing, registers
nothing. Two footings, never pooled: canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2 (kappa = 1/2 FITTED).
Say "the cold component" or "cold dark energy"; no particle claims; not a LCDM lane.

## 0. Question

In action (A) (PAPER70; QX17's certified (E1)-(E5)), does a clock that starts as free-falling cold dust around a baryon mass
end in the static-clock state (the law's halo, with only the static dust -mu_K^2 Phi / K left), or does it pile up, oscillate
without settling, or break down (the single-stream description ends)?

## 1. What the record already settles (read before design; quoted in RESULT.md with scope)

- **QX17** (CERTIFIED): the covariant (E1)-(E5). The clock charge is conserved: nabla_m[n^m rho_Q - lambda P^m/Q] = 0, with
  rho_Q -> n_d + D.P at leading order. Static weak limit only; no time-dependent reduction is written there.
- **TPA1 EQUATIONS.md** sections 4.1, 4.4: the S = 1 phase is action (A). Linear FRW perturbations: omega^2 = -K nbar /
  (1 + k^2/mu_K^2) with the law on (the clock's self-growth is suppressed at k > mu_K); -K nbar (1 - k^2/mu_K^2) with it off.
- **SCS1**: omega^2 = K G [(1 - K m) k^2 - mu_K^2 Qbar^2] / (mu_K^2 Qbar^2 + K m k^2), G = Qbar n_d + D.P. The static
  state around a point mass is STABLE at mu_K = 0 and 0.1 per Mpc, JEANS-ONLY at mu_K*. "Stability of the end state is not
  a path to it" (its own words). At mu_K = 0 the frequency does not depend on k: clock disturbances do not propagate.
- **SCS2**: isolated discs STABLE; external-field brackets NO VERDICT.
- **X14** (analytic, v3s PN, mu_K up to the S4 allowance): the exact shell equation r'' = -G(M_b + m)/r^2 + U(G m/r^2),
  U(y) = a0 y/(a0 - |y|), flux cap |K P| < a0; caustics generic; held shells oscillate at omega^2 = 2 a0 x^2 / r and phase-mix
  to shell crossing; K(Q) inert at the fold scale for S4-allowed mu_K. **This already answers the question at mu_K = 0 and
  0.1 per Mpc in spherical symmetry up to first crossing.** COL1 adds: the dust term live at mu_K up to the CMB-side values,
  a cosmological start, time to the first event, and the charge that has arrived by then.
- **AC15, MS1-MS3, XF1** (axisymmetric hydro, mu_K = 0, PN, moving source): a source moving through its clock loses its
  hosted law ("the wind sweeps the static hedgehog away"; XF1 FAIL / FAIL). Scope: moving sources, not infall onto a source
  at rest. **QX17C**: a static solver. **EW2, AN1 v3**: AeST, not action (A); AN1 v3's spherical dust collapse: "none
  settles". **AK1**: planar folds. None evolves the clock of action (A) onto a mass in spherical symmetry. No certified
  time-dependent solver for this system exists; COL1 writes one (section 4).
- **CMB constant.** FB1's arithmetic (w0 about 1e-8/mu_K^2, "to be below 1e-9") and the brief's 3.71 per Mpc are rechecked
  in Part 0 against KD1 (`closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json`): mu_B1a = 198.25 / 198.24 per Mpc (w <= 0.01 at
  z 3400), mu_B1b = 8.890e6 / 8.889e6 per Mpc (BBN). RESULT.md says plainly if 3.71 is not a CMB value.

## 2. Settings (frozen)

- Units kpc, km/s, Msun; G = 4.30091e-6; K = 4 pi G; a0 = 2888.3 / 3490.6 (km/s)^2/kpc (canonical / alt; 1 kpc = 3.0857e19 m).
- Cosmology per footing from KD1's setting: h, omega_d, omega_b as in kd1.json; flat, Omega_L = 1 - Omega_m; radiation
  neglected after z = 10. The clock's mean charge is the FRW cold component, Kbar n = mu_K^2 hbar (hbar = c^2 (Qbar - 1)).
- gamma_L = 0 (the stiffness; argued in RESULT.md: its galaxy-scale weight is (Lstar/r)^2 ~ 1e-8). S = 1 (action (A)).
- mu_K (per Mpc). Part 0: 0, 0.1, 1.78 / 1.74 (QX2 iter 5, per footing), 3.71 (brief), 198.25 / 198.24 (KD1 mu_B1a),
  8.890e6 / 8.889e6 (KD1 mu_B1b). Part 2: **primary 3.71**; brackets 1.78 / 1.74 and 0.1; reported bracket 198.25 / 198.24.
  mu_K = 8.89e6 is not run in Part 2: on resolved scales it is the law-off dust (argued from Pi/N <= (mu_K L)^-2).
- Baryons: point mass, log M_b = 9.4, 10.45, 10.7, 10.9 (KiDS masses). Part 2 softens it (Plummer, eps = 1 kpc).
- Radii for reads: 10, 30, 100, 300 kpc.

## 3. Part 0 (no time evolution)

For every mu_K, mass, footing:
- Static dust M_d(<r) = (mu_K^2/G) Int_0^r (C - Phi) r'^2 dr' on the **law's point-mass potential** (test field, no
  back-reaction; QX2 iter 5's generous form), C = Phi(R_ref), R_ref = 1 Mpc primary, 0.3 and 3 Mpc reported. Also the
  Newtonian closed form (Phi(inf) = 0): M_d/M_b = (mu_K r)^2/2. Also the self-consistent static ODE (law applied to
  baryons + dust, back-reaction on): M_d and the first radius where n_d < 0, if inside R_ref.
- Each as a fraction of M_b and of the law's halo M_ph(<r) = r^2 [g_law - g_N]/G (g_N = G M_b/r^2).
- Sound speed of the dust c_s^2 = K n_d/mu_K^2 at today's mean and at the static n_d inside 10 and 100 kpc; Jeans length
  2 pi/mu_K against 30 kpc (galaxy) and 2 Mpc (cluster). w(z) at z 1090 and 3400.
- SPARC: the ledger's f (RM2: M = M0 + f (M_c - M0), M0 an uncontracted cold halo; LC1: f_Q = (Q_live - 1)/(Q_Blum - 1))
  is defined relative to an uncontracted cold halo. RESULT.md states whether it can be evaluated for a static clock; the
  number reported in its place is M_d/M_ph and M_d/M_b at r/R_d = 2, 3, 4 (R_d from log R_d = -3.31 + 0.35 log M_b, kpc,
  stated as an assumption), beside KD1's diagnostic line (uniform extra baryon fraction f <= 0.33 / 0.19). Reported, not graded.

Part 0 carries no label. RESULT.md says in words what "collapse onto a galaxy" can mean at each mu_K.

## 4. Part 1, the system

**Reduction (to be derived and checked).** Newtonian order, spherical, gamma_L = 0, P eliminated by its Legendre maximum
(QX17 K0). With h = c^2 (Q - 1), velocity potential phi (v = grad phi), the claim is the reduced Lagrangian density

    L = mu_K^2 h^2/(2K) + J(|grad h|) - |grad Phi|^2/(2K) - rho_b Phi,    h = -(phi_t + |grad phi|^2/2 + Phi),
    J(s) = (a0^2/K)[s/a0 - ln(1 + s/a0)],

whose Euler-Lagrange equations are: the clock charge N = mu_K^2 h/K + div P, K P = a0 A/(a0 + |A|), A = -grad h, conserved:
d_t N + div(N v) = 0; Poisson grad^2 Phi = K (rho_b + N); and (identically) d_t v + v.grad v = -grad Phi + A.
Gauge: unitary-type split tau = t - phi/c^2 with phi = O(v^2) and Phi = O(v^2); the multiplier flux lambda P/Q and W are
dropped as O(v^2/c^2) (argued, with orders, in RESULT.md). Constraint: n.P = 0 (P spatial at this order).

**Checks of the reduction (sympy, exact):**
- R1: EL of L in spherical symmetry against the stated system, residual 0.
- R2: the leading-order expansion of action (A)'s clock Lagrangian sqrt(-g)[L_K(Q) + P.A - W] in the weak-field metric gives
  mu_K^2 h^2/(2K) + P.(-grad h) - W, residual 0 at leading order.
- R3: WKB linearisation of the reduced system about a static background equals SCS1's closed form with Qbar = 1, residual 0.
- R4: a sign flip of P.A is a field redefinition (max_P[-P.A - W] = J): disclosed before any run as a MUTATE that cannot bite.

**Solver.** Lagrangian thin shells (charges on nodes, conserved), h on the nodes as piecewise-linear hat functions, the h field
obtained each step as the unique maximiser of the discrete Legendre functional
U = max_h [sum_j m_j h_j - sum_gaps Int (mu_K^2 h^2/(2K) + J(|h'|)) dV] (Dirichlet h = hbar at the outer node; tridiagonal
Newton), forces from the envelope theorem (-dU/dr_j at fixed h), thin-shell gravity, KDK leapfrog, adaptive step.
mu_K = 0: no background charge exists (Kbar n = mu_K^2 hbar); not run in Part 2.

**Known answers (all must pass before any graded run; any fail makes the affected rows NO VERDICT):**
- KA1 R1-R3 above.
- KA2 law off, cold limit: (a) a uniform cold ball's top-hat collapse time pi sqrt(R^3/(8 G M)) to 1e-3; (b) a shell around the
  point mass (eps -> 0 limit, eps = 1e-3 kpc) reaches the centre at (pi/2) sqrt(q^3/(2 G M_b)) to 1e-3.
- KA3 law off, static K(Q) profile: a static n = 1 polytrope (no point mass, n_d proportional to sin(mu_K r)/(mu_K r)) held
  10 sound-crossing times with max |v| <= 1e-3 c_s(0) at the coarse grid and falling by >= 3x at the fine grid.
- KA4 static fixed point with the law on (point mass, mu_K = 0.1 and 3.71, non-expanding, h at the outer node from the static
  solution): the discretised static state's residual acceleration <= 1e-3 g at the coarse grid and >= 3x smaller at the fine
  grid; evolved 2 Gyr, max |v| <= 0.01 v_c.
- KA5 linear oscillation: a small radial displacement of one shell of the static law state (mu_K = 0) oscillates at the local
  shell frequency omega^2 = -d/dr[-g_b - y + U(y)] at fixed enclosed charge (= X14's 2 a0 x^2/[r (1 - x)^2]), to 2 %; and that
  frequency equals SCS1's high-k limit G (1 - K m)/m on the same background (sympy/numeric, 1e-6).
- KA6 energy: non-expanding isolated cloud (static state kicked by 10 % in velocity), fixed step: the discrete energy
  E = KE + U + W_grav conserved to 1e-4 relative over 2 Gyr, error falling by >= 3x when dt halves, at both resolutions;
  charge conserved exactly (by construction; reported).
- KA7 background: with M_b = 0 the Hubble-flow run keeps every shell on a(t) X to 1e-3 to z = 0 (mu_K 3.71 and 0.1).

## 5. Part 2, the evolution

- **Primary initial state: Hubble flow.** Clock uniform at its FRW mean, every shell on v = H r, at z_i = 10; background
  baryons uniform in Hubble flow; Lambda included; the point mass ramps on as a smoothstep over 1 Gyr from z_i. Outer node:
  prescribed r = a(t) X_out, h = hbar(t). X_out = 8 Mpc comoving; innermost node X_in = 20 kpc comoving; nodes log-spaced.
  Run to z = 0 (13.3 Gyr after z_i; the brief's 10 Gyr is inside it; the state at 10 Gyr is printed) or to breakdown.
- **Bracket: at rest.** Clock uniform at today's mean density, at rest, gravity of the mean subtracted (Jeans swindle), no
  Lambda, no background baryons; point mass ramped over 1 Gyr; outer node fixed at 8 Mpc; 10 Gyr.
- **Bracket: damped.** The primary with von Neumann-Richtmyer artificial viscosity (q = 2 rho (dv)^2 on compressing gaps).
  Labelled bracket only; it never sets a label.
- **Resolutions:** coarse 1200 nodes, fine 2400 nodes. Check: one primary row (mu_K 3.71, 10.45, canonical) with X_out = 16 Mpc.
- **Grid:** primary: 3 mu_K x 4 masses x 2 footings x 2 resolutions. At-rest and damped brackets and mu_K = 198: log M_b 10.45,
  both footings, both resolutions. MUTATE: section 7.
- **Reads** (every 0.25 Gyr and at the first event): n_d against its static value mu_K^2 (C - Phi)/K with C from the current
  h + Phi at 300 kpc; the static residuals |dv/dt| / g and |v| / v_c; the enclosed charge M_N(<r) against the law's halo
  M_ph(<r) of M_b; the split M_N = M_d + M_Pi; the mass inside 10/30/100/300 kpc.

**Events (any one ends the run and its time and radius are reported):**
- E1 caustic: a gap between neighbouring shells (or between the centre and the first shell) reaches <= 1e-6 of its Hubble-flow
  value a(t) dX, or shells cross. The single-stream clock has no answer beyond it.
- E2 no h solution (the flux cap |K P| < a0 exceeded; possible only at mu_K = 0) or Newton failure.
- E3 non-convergence: at the coarse-grid Lagrangian labels X >= 4 X_in, max |r_fine - r_coarse| / r_coarse > 0.1 at a read
  (graded once both resolutions exist; a shock or fold that the inviscid equations do not resolve).

## 6. Labels (per mu_K, footing, mass; the per-(mu_K, footing) headline is the common label of the four masses, else the
   10.45 label with "(masses differ)")

- **BREAKS DOWN**: E1 or E2 at both resolutions before the end, or E3. Time and radius at both resolutions; "converged" if they
  agree to 10 % in time and a factor 2 in radius, else "(time grid-limited)". Says the equations give no answer beyond it.
- **REACHES THE STATIC STATE**: no event; over the final 2 Gyr every node inside R_s has |v| <= 0.05 v_c and
  |dv/dt| <= 0.05 g; R_s >= 30 kpc at both resolutions. Report R_s, when first reached, and M_N(<r)/M_ph(<r).
- **OSCILLATES ABOUT IT**: no event; not REACHES; inside 100 kpc the time-mean of (dv/dt)/g over the final 4 Gyr is within
  0.1 of 0 for every node, but the instantaneous amplitude exceeds 0.05; "no decay" if the amplitude in the final 2 Gyr is
  >= 0.5 of that in the 2 Gyr before. Report amplitude and period.
- **DOES NOT**: no event, neither of the above. Report how much charge stays where (M_N/M_ph at the four radii).
- **NO VERDICT**: a known answer fails, or the two resolutions give different labels (E3 aside).

Whatever the label, RESULT.md reports M_N(<r)/M_ph(<r) at the four radii at the last read before the end.

## 7. MUTATE (separate outputs; each must change the primary row's charge inside 100 kpc at the end/event, or its event time,
   by >= 10 %, or flip a known answer; any that does not bite is disclosed)

- M1 law off (S = 0: J removed; the clock is the K(Q) polytrope). Must reproduce KA2/KA3; must differ from the primary.
  Disclosed before any run: at small mu_K the law-off fluid is a hot polytrope (c_s^2 = K nbar/mu_K^2), so "plain dust
  infall" holds only where c_s is far below the infall speed.
- M2 J -> -J (the polarization charge enters N with the opposite sign). Must bite.
- M2a P.A -> -P.A: a field redefinition (R4); predicted not to bite; run and disclosed.
- M3 U(y) -> y (no flux cap, linear Legendre map; X14's m1). Must break KA5 or bite.

## 8. Lean

`COL1.lean` (Mathlib): the closed forms used: Newtonian static dust M_d = mu^2 M r^2/2 (derivative), the n = 1 polytrope's
Jeans wavenumber (c_s^2 k^2 = K n at k = mu), the law-on response dh = K dN/(mu^2 + k^2) and the cancellation of the clock's
self-gravity at mu = 0, the shell equilibrium (y^2 = g_b (a0 - y)) and frequency identity, the reduced WKB form = SCS1's form,
the shell energy identity, the FRW w0 arithmetic. `COL1_MUTATE.lean`: the same with signs flipped, must fail to compile.

## 9. Resources

One thread per job, under 1.5 GB, checkpointed (npz per read) and resumable; up to 4 jobs at once; nothing downloaded.
Snapshots stay outside the repo; JSON summaries and logs are committed.

## 10. Done

Criteria (this file, alone), scripts with outputs and MUTATE outputs, Lean with compile outputs, RESULT.md (label first, in
plain words, with what it means for form B and the spiral wall; earlier lanes and whether this agrees; what it does not settle:
non-spherical infall, mergers, the cosmological setting beyond a point mass, baryon physics; anything in FB1, SCS1, SCS2 or the
brief found wrong), committed with explicit paths and pushed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
