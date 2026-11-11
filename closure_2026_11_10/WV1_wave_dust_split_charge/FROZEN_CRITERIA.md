# WV1 FROZEN CRITERIA: wave dust with a split charge (2026-11-10)

TEST lane, quarantined. Committed ALONE, before any script or number of this lane. Adopts nothing, relabels nothing,
registers nothing. Footings canonical (a0 = 9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2), graded separately, never
pooled. The cold component is cold dark energy, a field (Psi), never a particle or dark matter. Amendments, if any, are
post hoc, each committed alone and disclosed in RESULT.md.

## 0. Question

Is there a parent action that works everywhere and reduces to action (A)'s static law in galaxies, built by splitting
what (A) conflates: the law's frame and phantom density on one side, the cold dark energy's conserved charge on the
other, with the cold dark energy carried by a complex wave field Psi that can multi-stream by interference?

Record read first (not re-graded here): QX17 (action (A)), LFS1 (the clock's polarization flux is carried with the
clock's flow), CLS1 (no cluster state in (A)), COL1 / FLD1 (the infalling clock folds; fold reach), EW2 (AeST's one
length), X14 (C5, complex-scalar completion, rejected for v3s's sign-indefinite charge), QX28 (diffuse cored component
outside the law passes SPARC and KiDS), HY1 (cuspy dust in galaxies wrecks discs), QG1 (health of (A); clock charge
G = n_d + D.P sets the clock's gradient energy), ROOT note (alpha(0) = 2 is forced by any deep-MOND regime).

## 1. The parent action (two variants), units c = 1, K = 4 pi G, nu = hbar/m

Common part (QX17's (A) with the dust term K(Q) REMOVED, the Pi^6 blend as adopted, and Psi added):

    S = Int sqrt(-g) { (R - 2 Lambda)/(4K) + P^m A_m[n] - W(K|P|) - gamma_L F(Pi) + lambda n^m P_m
                       - (hbar^2/2m) [ g^{mn} d_m Psi* d_n Psi + (m/hbar)^2 |Psi|^2 ] } + S_m[g]

    W(p) = (a0^2/K)[-p/a0 - ln(1 - p/a0)],  Pi = D_m P^m,  F = the adopted Pi^6 blend (QX17D: Pi_+ -> F'(Pi)),
    A_m = n^r nabla_r n_m (the frame's acceleration),  n_m = -d_m tau / Q,  Q = sqrt(-g^{mn} d_m tau d_n tau).

Matter and Psi couple to g only. Non-relativistic limit: Psi = e^{-i m t/hbar} psi, m|psi|^2 = Psi's mass density,
psi = sqrt(n) e^{i theta}, flow velocity v = nu grad theta.

- **V1 (frame = phase of Psi).** tau = -(hbar/m) arg Psi (so tau -> t in the NR limit). No other clock field.
- **V2 (separate frame).** tau is an independent khronon, with no K(Q) term (no dust in the frame). Psi does not couple to
  tau and falls through it. (V2 is graded with beta = lambda = 0 as in (A); adding khronometric beta, lambda is
  REPORTED via the BPS speed, not graded.)

NR Lagrangian used for the symbolic checks (Newtonian gauge, weak field):

    L = -hbar n theta_t - hbar^2 n |grad theta|^2/(2m) - hbar^2 |grad sqrt n|^2/(2m) - m n Phi
        - |grad Phi|^2/(8 pi G) - rho_b Phi + P.A - W(K|P|) - gamma_L F(div P)
    V1: A = grad( Phi + (hbar/m) theta_t + (hbar/m)^2 |grad theta|^2/2 )
    V2: A = grad( Phi - chi_t + |grad chi|^2/2 ),  tau = t - chi (chi independent of theta)

## 2. Parts, items and gates (per variant, per footing)

### S0 static reduction (gate)
In a static weak-field galaxy with Psi stationary (V1: psi = f(x) e^{-i eps t/hbar}, f real; V2: any static f) and the
frame static, the field equations must reduce EXACTLY (sympy residual 0) to (A)'s static equations at mu_K = 0 with
rho_b -> rho_b + m f^2: the P equation (QX17 E2 with Pi_+ -> F'(Pi)), Poisson with the phantom density div P, hence
div[mu(|grad Phi|/a0) grad Phi] = 4 pi G (rho_b + m f^2), mu = x/(1+x), wherever the screening terms vanish; and in V1
the phase equation must be identically satisfied and the f equation must be the stationary Schrodinger equation in the
total Phi. **S0 PASS iff every residual is 0.** The lane also states, as a reading (no gate), whether rho includes the
Psi dust and what "counted once" then means.

### S1 structure and linear health (gate)
- S1a DOF count (reported): graviton 2 + Psi 2 real (+ V2's khronon 1).
- S1b the frame's Noether charge (exact, sympy, NR Lagrangian): the shift-symmetry current of the frame field (V1:
  theta; V2: chi). Reported as an exact identity; it decides S3(b) for V2 and S3(c) for V1.
- S1c **FRW (gate).** The frame scalar's dispersion on QG1's FRW backgrounds (z = 1100 and z = 1, sub-horizon, QG1's
  closed form omega^2 = G k^2 (b - a)/(a b), G = the frame's charge on the background):
  - V2: G = 0 (no frame dust, P_bar = 0 by isotropy). Graded with QG1's own code (`mode`, `lambda_s`) at G = 0.
  - V1: G = rho_bar_Psi; the K(Q) stiffness mu^2/K of QG1's a is replaced by Psi's (exact NR reduction, to be derived in
    S1b's script: mu_eff^2 = k_J^4/k^2 with k_J^4 = 16 pi G rho_bar/nu^2).
  - **S1c FAILS** on a background if omega^2 = 0 at every k (QG1: then Lambda_s = 0, Lambda_s L < 10), or if any mode has
    negative kinetic coefficient (ghost), or if the growth rate sqrt(-omega^2) exceeds sqrt(4 pi G rho_bar) (1 + 1e-9) at
    any k or increases with k at large k (gradient instability). Otherwise PASS (linear health only; for V1 the
    strong-coupling scale is not computed and is not graded).
- S1d static galaxy (gate): QG1's point-mass rows (x_N = 1e-2, 1, 1e2) with Psi absent; V1 adds m f^2 >= 0 to G.
  PASS iff QG1's graded PM rows pass when re-run here (they are (A)'s rows at mu_K = 0).
- S1e c_T = c (statement; QG1 KA1: neither the P sector nor Psi couples to h_TT beyond R).

**S1 PASS iff S1c and S1d pass on both FRW rows and all PM rows.**

### S2 FRW: the dust at the CMB (window)
Psi's comoving Jeans wavenumber k_J(a) = (16 pi G rho_Psi0 a / nu^2)^(1/4), rho_Psi0 = omega_d rho_crit,100 (KD1's
setting per footing; the 5.41 share). The record's line (QX28 G6a / G6c, QX3 iter3 G4'): comoving Jeans length
2 pi / k_J <= 0.42/h Mpc at z = 3, 10, 100 and 1089. **nu_max = the largest nu meeting all four.** The same k_J is graded
for V1 and V2: for plain Psi (V2) omega^2 = 0 at k_J; for V1 the P sector modifies the dispersion (S1b) and the growth
rate there is reported (expected: half the pressureless rate). The acoustic-peak scale (k <= 0.3/Mpc at z = 1089) is
reported. The law's linear growth: V1 = the exact P-sector term of S1b; V2 = none (frame degenerate, S1c).

### S3 spherical collapse (gate)
Solver: radial Schrodinger-Poisson for Psi in comoving coordinates (u = x psi, split-step with a discrete sine
transform), COL1's setup otherwise: Psi uniform in Hubble flow at z = 10, KD1's cosmology per footing, a baryon point
mass softened over 1 kpc and ramped on over 1 Gyr (smoothstep), uniform baryon background. Primary run: law OFF (this is
V2's actual evolution and V1's diagnostic). Bracket (reported, and used where stated): the law on the baryons' field,
g -> law_g(g_N,b, a0) - g_N,b added. Masses log M_b = 10.7 (graded; KiDS windows 362 / 849 kpc, SPARC largest R_last
71 kpc, R_ta 325 kpc, FLD1) and 9.4 (graded; 81 / 190, 23, 120). nu scan: nu_max x {1, 4, 16, 64, 256, 1024, 4096}
(canonical nu_max; alt uses its own). Preemptible (checkpoint on SIGTERM), under 3 GB, outputs small (profiles
down-sampled). Outputs at z = 2, 1, 0.5 and 9 times spaced evenly over the last 1 Gyr (the "last-Gyr set").

Items:
- **S3(a) fold-free.** Psi's density stays finite and resolved: at no output does any local density maximum have a
  full width at half maximum narrower than 4 grid cells, and at nu_max (log M_b 10.7, law off, to z = 2) a run at half
  the grid spacing gives the peak central density and the z = 2 central density within 20 %. V2 also needs its FRAME
  fold-free: V2's frame is the zero-charge clock (mimetic: test shells), so its central focusing time is COL1's
  (`col1_focus_check.py`; KA4). **V1 S3(a) PASS iff Psi fold-free. V2 S3(a) FAILS if its frame focuses (it is not Psi).**
- **S3(b) the law where it is seen.**
  - V1: the frame is static at radius r iff, at every output in the last-Gyr set and at every r' in [2 dx, r]:
    |v_r(r')| <= 0.1 v_c(r') (physical radial Madelung velocity) and |A(r') - dPhi/dr(r')| <= 0.1 |dPhi/dr(r')|, with
    A = -d(Q_qu)/dr the frame's proper acceleration (Q_qu Psi's quantum potential, physical) and dPhi/dr the total
    physical gravity of the run. R_s = the largest such r (0 if r = 2 dx fails). Graded value: max(R_s law-off, R_s
    bracket). **V1 S3(b) PASS iff, at some nu <= nu_max, R_s(z = 0) >= the KiDS inner window edge AND >= SPARC's largest
    R_last at both masses.** nu_min = the smallest scanned nu at which both hold at both masses (none if none).
  - V2: the frame's polarization charge is advected with the frame (S1b), it is zero on FRW, so the law's reach is
    computed from that identity: **V2 S3(b) PASS iff the identity allows a nonzero D.P to appear on a regular frame that
    starts with P = 0** (expected: it does not; reach 0).
- **S3(c) V1 only: can the wave multi-stream in V1?** In V1 Psi's U(1) mass charge is C = m n + D.P (S1b), carried with v,
  so n = (C - D.P)/m. Along the law-off solution (C = m n_SP to leading order), evaluate D.P from the frame acceleration:
  K|P| = a0 x/(1+x), x = |A|/a0, P radial with the sign of A, D.P = r^-2 d(r^2 P)/dr (unscreened local law; Lstar is
  reported against the fringe scale). **S3(c) FAILS** if, at any output in the last-Gyr set, more than 1 % of Psi's mass
  inside r_ta(z = 0) sits in cells with D.P > m n (there V1 would need n < 0). Graded at every scanned nu <= nu_max of
  the footing (law-off runs, both masses); reported at every nu.
- S3(d) reported: r_c (half central density, last-Gyr mean), r_ta (outermost zero of the shell-mass-weighted radial
  velocity), r_c / r_ta against QX28's 0.15-0.26.

**S3 PASS (V1) iff S3(a), S3(b), S3(c) pass. S3 PASS (V2) iff S3(a) and S3(b) pass.**

### S4 static rows (only if S0-S3 pass for a variant; otherwise NOT GRADED)
SPARC (QX28's method and line: rms <= 0.110 dex with the Psi share cored, law from baryons + cored Psi share as the
action gives), KiDS host-free (ONE1's frozen gate), X-COP and groups (QX10's lines as RB1 used), Cassini (v3s screening,
C6P's margin). Rows frozen now as these record gates; numbers only if S0-S3 pass.

## 3. Labels (per variant, per footing)

- **WORKS EVERYWHERE GRADED**: S0, S1, S3 pass, S2 x S3(b) gives a nu window, and every S4 row passes.
- **STRUCTURE HOLDS, DATA FAIL (gate)**: S0-S3 pass, an S4 row fails (name it).
- **STRUCTURE FAILS (part)**: any of S0, S1, S3 fails, or the window [nu_min, nu_max] is empty. Every failing part is
  named; S4 is then NOT GRADED.
- **NO VERDICT**: a known answer the deciding item rests on fails, a MUTATE arm the deciding item rests on does not
  bite, or a deciding run does not finish.

## 4. Known answers (must pass)

- KA1 X14's C5 dispersion: plain Psi (P sector off) gives omega^2 = (nu^2/4) k^4 - 4 pi G rho_bar (n = 4, nu^2/4), sympy.
- KA2 QX17's static row: (A)'s static weak-field P equation and Poisson at mu_K = 0 give the law (sympy, residual 0).
- KA3 QG1's machinery: re-run QG1's graded FRW and PM rows through its own functions; Lambda_s L must equal QG1's
  printed values (FRW1100 334 / 316, FRW1 1.84e5 / 1.74e5) to 1 % and the PM rows must PASS; QG1's "other reading"
  FRW (mu_K = 0) must give Lambda_s = 0.
- KA4 COL1's fold time with Psi off: (i) COL1's test-shell focus time at log M_b 10.7 and 9.4 (0.0712 and 0.1533 Gyr)
  reproduced to 1e-3 relative; (ii) this lane's SP solver at small nu (nu = 0.2 kpc km/s on a central domain of 100
  comoving kpc, run to 0.12 Gyr after z = 10) puts its central density maximum within 5 % of COL1's focus time at
  log M_b 10.7.
- KA5 the SP ground state: imaginary-time relaxation on this lane's grid gives G M r_1/2 / nu^2 = 3.925 within 2 %.
- KA6 LFS1's spherical identity: in the NR V2 Lagrangian the frame charge D.P is advected with the frame (residual 0);
  with a dust term added it reproduces LFS1's dust-to-polarization exchange.
- KA7 (only if S4 is graded) QX28's SPARC rms 0.0591 / 0.0621 reproduced to 0.002.

## 5. MUTATE twins (must bite)

- M1 (sym): V1 with the frame decoupled from Psi's phase: the U(1) charge becomes m n alone; the S1b identity
  C = m n + D.P must fail.
- M2 (S1c): give V2's frame QG1's dust charge (G = rho_c, mu_K*): S1c V2 must flip to PASS on the FRW rows.
- M3 (window logic): force the static test true at every radius (R_s = the run's outer physical radius at z = 0):
  S3(b) V1 must flip to PASS at nu_max (shows the comparison can pass).
- M4 (S3(c)): replace A by dPhi/dr (frame static everywhere): S3(c) must flip to PASS.
- M5 (solver): KA4(ii)'s run with nu x 10 must show a peak central density at least 30 x smaller than at nu (so the
  focusing sharpens toward the classical fold as nu falls).
- Lean twin: false versions of every Lean theorem must fail to compile.

## 6. Lean (structural claims)

WV1.lean: (i) G = 0 makes QG1's closed-form omega^2 vanish at every k; (ii) V1's dispersion at screening factor cY = 1 is
negative for every q (no Jeans scale on the off branch) and reduces to C5's at cY = 0; (iii) C = m n + D with D > C and
m > 0 forces n < 0; (iv) a quantity constant along every flow line that is zero at the start is zero (advection); (v)
the window is empty when nu_min > nu_max. Standard axioms only. Compiled with the repository's Lean build.

## 7. Hand result, stated before any script (expected, not a result)

- V2: STRUCTURE FAILS. S1c: the frame carries no charge on FRW, so omega^2 = 0 at every k (QG1's Minkowski failure on
  FRW). S3: the frame's polarization charge is carried with the frame's own flow; it starts at zero, so the law never
  appears; the uncharged frame is mimetic dust and focuses at COL1's time.
- V1: STRUCTURE FAILS. S1b: the law's phantom density is part of Psi's U(1) charge (premise (1) of the brief fails in
  V1: D.P IS a conserved charge there), so X14's C5 objection returns. S2: nu_max of order 25 kpc km/s. S3(b): the
  frame is static only where Psi is held by quantum pressure (soliton or Debye cloud), of size ~ nu / v_c, far below
  KiDS's windows at nu_max; S3(c): in interference fringes |A| >> a0 and the phantom charge exceeds Psi's density.
- S4 NOT GRADED for either.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
