# VCC1 (can the clock sector's charge be SOURCED?): FROZEN CRITERIA, committed alone before any script or number

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings canonical (a0 = 9.3603e-11 m/s^2)
and alt (1.1312e-10), graded separately, never pooled. The halo's charge is cold dark energy (the clock's charge), never
a particle. kappa = 1/2 FITTED; not theory closed. This lane edits nothing outside its own folder.

Id check: `git log --all --oneline | grep -ci vcc1` = 0; `ls closure_2026_11_11` has no VCC1.

## 0. The question

The amount problem is capped by two exact results. **T4** (SMF1 S0b, exact): the net polarization charge inside any ball
whose boundary free-falls is 0 at all times, for any momentum equation. **LFS1** (exact): for a static clock the
polarization is frozen, the halo's charge changes only by O(|Phi|/c^2) ~ 1e-6. Together they say the halo's charge equals
the dust charge carried in, which VSH1/COL1 measure at 0.9 to 1.4 M_b, while KiDS needs 59.5 M_b and the cosmic budget is
5.41 M_b (AMT1). The only way past a conservation cap is to break the conservation.

In action (A) (QX17 section 0, c = 1, K = 4 pi G; restore c: K -> 4 pi G/c^2)

    S = Int sqrt(-g) { [R - 2 Lambda + 2 mu_K^2 (Q-1)^2]/(4K) + P^m A_m - W(K|P|) - gamma_L F(Pi) + lambda n^m P_m } + S_m  (A)

the clock's equation (E3) is the conservation law

    nabla_m [ n^m rho_Q - lambda P^m / Q ] = 0 ,    rho_Q = J_P/Q + mu_K^2 (Q-1)/K ,  J_P = nabla_m[(1+gamma_L Pi_+) P^m].

This lane asks six questions about breaking it, and grades them.

1. Is that identity forced by the action's symmetries, or is it an accident of the term list?
2. What is the SMALLEST change to the action that gives the current a source, and what sources it (the vacuum / Lambda, a
   second field, the clock's own dust)?
3. Does the change preserve the Bianchi identity and total stress-energy conservation (the source must be paid for by the
   vacuum)?
4. The background: must still give 5.41 times the baryons, w about 0 for the cold part, and the MK1/CO1 CMB rows.
5. A galaxy: can it produce 59.5 M_b of charge by today, without over-producing at z > 2 (the FRZ1/FZS1 forest gates) and
   without over-producing in the Solar System?
6. The Bullet: the component must pass through.

## 1. Hand results to be checked (written before any script; the lane's job is to confirm or refute)

**(H1) The identity is Noether's first theorem for an accidental global symmetry.** For any L(tau, d_m tau, ...) the
Euler-Lagrange expression is E_tau = dL/dtau - nabla_m (dL/d(d_m tau)), so on shell

    nabla_m J^m = dL/dtau ,     J^m := dL/d(d_m tau) .

(A) contains tau only through d_m tau (Q = sqrt(-g^{mn} d_m tau d_n tau), n_m = -d_m tau/Q, A_m = -h^n_m d_n ln Q,
l = ln Q), so dL/dtau = 0 identically and the current is conserved. The symmetry is the *rigid* shift tau -> tau + c. It
is not a gauge symmetry (tau -> tau + c(x) is not a symmetry) and it is not forced by diffeomorphism invariance: V(tau)
is a scalar, so a bare tau is allowed. So: **forced by an accidental global symmetry of the term list, one term away from
being broken.** The lane's job is to check J^m = n^m rho_Q - lambda P^m/Q and dL/dtau = 0 exactly.

**(H2) The smallest change is to let the existing vacuum constant depend on tau: -2 Lambda -> -2 Lambda(tau).** No new
term, no new field, no new sector; one existing constant becomes a function. The source is

    nabla_m J^m = -Lambda'(tau)/(2K)   (per unit volume;  rho_Lambda := Lambda/(2K) = Lambda/(8 pi G) ),

i.e. the vacuum pays, homogeneously (in unitary gauge tau = t, so the source is a function of t only). The alternatives
are all larger: a new -sqrt(-g) V(tau) term (same physics, one more term), a tau-dependent coefficient on an existing
sector (gamma_L(tau), (1+eps(tau)) on P.A - W, mu_K(tau)), a second field, or a coupling to a non-conserved matter
current (R541D/R541E).

**(H3) The source's spatial profile is the source's, and the charge it makes is its volume integral.** With the P equation
untouched by a V(tau)-type term, lambda N^2 is still (d_t - N^j d_j) X, X = N(1+gamma_L Pi_+), and LFS1's identity
sqrt(gamma) rho_Q = d_i(X Y^i) + sqrt(gamma) d still holds, so in a static clock (zero shift), mu_K = 0:

    d_i [ X d_t Y^i ] = sqrt(gamma) S      ->   spherical, regular centre:   d_t C(R) = Integral_{V(R)} S dV .

So a homogeneous source makes a **uniform** charge density: C_cre(R) = rho_cre (4 pi/3) R^3, i.e. C_cre grows as R^3.
The law's halo grows as C_law(R) = M_b X(R/r_M) ~ M_b R/r_M, i.e. as R. **A vacuum-paid source cannot make the law's
profile.** Expected: the mismatch between 10 kpc and the KiDS middle edge is of order 1e5 to 1e6.

**(H4) The vacuum cannot pay it.** The created charge carries rest mass; the vacuum's energy density inside the halo is
rho_Lambda = 86.2 Msun/kpc^3 (canonical). Supplying the law's halo at radius R needs a created density
rho_cre(R) = [C_law(R) - C_dust(R)]/V(R), which the hand estimate puts at 22 to 2.3e4 times rho_Lambda over the graded
radii. Expected: FAIL by 2.2e1 to 2.3e4 against the line rho_cre <= 0.1 rho_Lambda.

If the scripts refute any of H1 to H4, the label follows the scripts.

## 2. Inputs (frozen)

- Constants: G 6.674e-11 SI, M_sun 1.98847e30 kg, kpc 3.085677581e19 m, c 2.99792458e8 m/s, Gyr 3.15576e16 s.
- Background: flat, H0 67.4 km/s/Mpc, Omega_b 0.0493, Omega_c = 5.41 Omega_b = 0.266713, Omega_r h^2 4.15e-5,
  Omega_Lambda = 1 - Omega_b - Omega_c - Omega_r = 0.683244 (TK1's background, CO1's fit).
  rho_crit = 3 H0^2/(8 pi G); rho_c0 = Omega_c rho_crit; rho_Lambda = Omega_Lambda rho_crit.
- Footings: a0 = 9.3603e-11 (canonical), 1.1312e-10 (alt) m/s^2.
- The law's halo: C_law(R) = M_b X(x), X(x) = (sqrt(1 + 4 x^2) - 1)/2, x = R/r_M, r_M = sqrt(G M_b/a0) (AMT1 step 0).
- Dust already delivered (not created): **C_dust = 1.40 M_b** primary (VSH1 settled, under its post hoc A1);
  bracket C_dust = 1.06 M_b (COL1 A4 / FLD1 corrected). Reported, never label-setting on its own.
- Masses: log M_b = 9.4, 10.45, 10.7, 10.9. r_M from AMT1: 1.934 / 6.479 / 8.640 / 10.877 kpc canonical.
- Graded radii per mass: {10, 30, 100} kpc (SPARC / COL1 Part 0), FLD1's KiDS inner and middle window edges
  (81 / 272 / 362 / 456 and 190 / 637 / 849 / 1069 kpc for log M_b 9.4 / 10.45 / 10.7 / 10.9), and ONE1's end radius
  (R where X = 59.5: 116.0 / 388.7 / 518.4 / 652.6 kpc canonical, FLD1's R_cap; alt 0.9100 x those).
- Deep-regime law field (used for the profiles): g = a0 r_M/r, K|P| = a0 x/(1+x) with x = g/a0,
  Pi = D.P = (a0 r_M/K)(r + 2 r_M)/[r (r + r_M)^2], J(g) = P.A - W = (a0^2/K)[u - ln(1+u)], u = g/a0.
- Bullet (frozen for gate V6, PROVISIONAL): main and subcluster R_200 = 1.70 and 1.10 Mpc; M(<R_200) read as
  200 rho_crit V(R_200). The created mass inside R must be <= 0.10 of the mass measured there.
- Solar System (frozen for V5d, PROVISIONAL): dark mass inside Saturn's orbit (9.5 AU = 1.4212e12 m) <= 1e-10 M_sun
  (Pitjev & Pitjeva 2013).

## 3. Items

### V1 Is the conservation law forced? (sympy, exact)

- **V1a.** For action (A), dL/dtau = 0 identically: sympy in 1+1 with a generic metric g_tt(t,x), g_tx, g_xx, a generic
  tau(t,x), generic P_m, lambda, and a generic W. Residual 0.
- **V1b.** The Noether current: J^m := (1/sqrt(-g)) d(sqrt(-g) L)/d(d_m tau) equals -(n^m rho_Q - lambda P^m/Q) (sign
  fixed by the first run and printed). Residual 0.
- **V1c.** The identity nabla_m J^m - dL/dtau = -E_tau (E_tau the Euler-Lagrange expression): residual 0 for a generic
  L(tau, d tau) in 1+1.
- **V1d.** The symmetry: (A) is invariant under tau -> tau + c (rigid) and not under tau -> tau + c(x). Stated and
  checked by substituting tau + c and tau + c(t,x) into Q, n_m, A_m and l.
- **Answer to question (1), reported:** forced by the accidental rigid shift symmetry of (A)'s term list; not forced by
  diffeomorphism invariance, which permits a bare tau.

### V2 The smallest change, and what sources it

Each candidate is written as a change to (A), with its new ingredient, its source S = dL/dtau per unit volume, and that
source's value in FRW and its radial profile in a static galaxy's deep regime (sympy where the profile is claimed exact):

| id | change | new ingredient | source S | in FRW | profile in a halo (deep) |
|---|---|---|---|---|---|
| C-I | -2 Lambda -> -2 Lambda(tau) | one constant -> one function | -Lambda'(tau)/(2K) | = S(t), homogeneous | uniform |
| C-II | gamma_L -> gamma_L(tau) | one constant -> one function | -gamma_L'(tau) F(Pi) | 0 (Pi = 0) | F = Pi^2/2, Pi ~ (a0 r_M/K)/r^2 -> S ~ r^-4 |
| C-III | (P.A - W) -> (1+eps(tau))(P.A - W) | one function | eps'(tau) J(g) | 0 (P = 0, A = 0) | J ~ g^2/(2K) ~ r^-2 |
| C-IV | mu_K -> mu_K(tau) | one constant -> one function | (mu_K mu_K'/K)(Q-1)^2 | ~ (mu_K mu_K'/K)(Q-1)^2 | Q-1 = |Phi|/c^2 ~ 1e-6 -> S ~ 1e-12 |
| C-V | add -sqrt(-g) V(tau) | a new term | -V'(tau) | = S(t), homogeneous | uniform (same physics as C-I) |
| C-VI | eps is a dynamical field chi | a new field + its kinetic/potential | paid by T^chi | set by chi's own equation | set by chi's profile |
| C-VII | coupling to a non-conserved matter current | a new coupling | proportional to nabla.J_matter | 0 at z < 2 (B, L conserved; sphalerons inactive below 131.7 GeV) | 0 |

- **V2a.** The constitutive law under C-III: varying P_m gives (1+eps)[A_m - K W' P-hat_m] + gamma_L curlyD_m = 0, so the
  law's *form* is unchanged (the Legendre pair scales together); what changes is the P sector's weight in the metric
  equation, by the factor (1+eps). Exact, residual 0.
- **V2b.** The charge C-III makes: with rho_cre = eps(t) J(g)/c^2 and J ~ g^2/(2K), C_cre(R) = Integral eps J/c^2 dV.
  Deep regime, sympy: C_cre(R) = eps * 4 pi a0^2 r_M^2 R/(2 K c^2) — linear in R, i.e. **the law's own profile**.
  Matching C_cre = C_law = M_b R/r_M in the deep regime gives **eps = 2 c^2/(a0 r_M) = 2 c^2/v_flat^2**, printed per mass
  and footing. The lane reports the spread of that required eps across the four masses (eps(tau) is ONE function of
  cosmic time, so a spread is a failure).
- **V2 PASSES** iff at least one candidate is a change to (A) with no new field, and its source's profile in a halo
  equals the law's (C_cre proportional to C_law at every graded radius) up to a single constant.

### V3 Bianchi identity, total stress-energy, and who pays

- **V3a (exact).** For C-I: G_mn + Lambda(tau) g_mn = 2K T^(m+c)_mn. With T^Lambda_mn = -(Lambda(tau)/(2K)) g_mn,
  nabla^m (T^(m+c) + T^Lambda)_mn = 0. sympy, residual 0, using nabla^m G_mn = 0.
- **V3b (exact).** The ledger: d(rho_cre a^3) + d(rho_Lambda a^3) = 0, i.e. the created charge's energy equals the vacuum
  energy lost. Residual 0 against the FRW component of V3a.
- **V3c (numbers).** The payment bound: rho_cre(R) <= 0.10 rho_Lambda at every graded R (the vacuum must pay, and
  Omega_Lambda is measured to about 2 % with w = -1 to about 5 % over 0 <= z <= 2). Printed per mass, per R, per footing.
- **V3d (numbers).** For C-II, C-III, C-IV the payer is the sector carrying the tau-dependent coefficient. Its available
  mass-equivalent energy density in the halo, against rho_cre c^2:
  - C-III: the P sector carries J/c^2 = rho_ph v_flat^2/(2 c^2) (FB1 KA1: p/rho = (1/2) sqrt(G M_b a0)); with the factor
    (1+eps) it carries (1+eps) times that. Required eps is V2b's. Reported: the ratio (P sector's energy with that eps) /
    (created rest mass), and the factor by which the law's sector's stress tensor is multiplied in the metric equation.
  - C-II: gamma_L F / (created rest mass), at r = 100 kpc, L* = 21.7 pc canonical / 22.9 pc alt.
  - C-IV: (mu_K^2/2K)(Q^2-1)/(created rest mass), with Q-1 = |Phi|/c^2 at r = 100 kpc.
  - C-VII: reported as 0 at z < 2 (R541D/R541E graded the early case and EXCLUDED it).
- **V3 PASSES** iff V3a and V3b hold and V3c holds at every graded R, or (for an inhomogeneous candidate) the paying
  sector's own energy density is at least the created rest-mass energy density at every graded R.

### V4 The background

- **V4a.** rho_cre(t0)/rho_c0 <= 0.05 (the cold-to-baryon ratio must stay 5.41 within 5 %; CO1's C1 fit is 5.410 / 5.412).
- **V4b.** |w_Lambda + 1| <= 0.05 over 0 <= z <= 2, where w_Lambda = -1 + (drain rate)/(3 H rho_Lambda), computed for the
  drain history that the galaxy's halo demands.
- **V4c.** Reported against CO1's C1-C5 and MK1's rows (read, not recomputed): the shift in Omega_c h^2, Omega_Lambda and
  in the cold component's w at z 3400 (MK1's B1a / KD1's Jeans line).
- **V4 PASSES** iff V4a and V4b hold at the rho_cre the galaxy needs.

### V5 A galaxy

- **V5a (profile).** For a single rho_cre (a homogeneous source has one), C_cre(R)/C_law(R) must lie in [0.9, 1.1] at
  every graded R in {10, 30, 100 kpc, KiDS inner, ONE1 end, KiDS middle}. Reported: the required rho_cre at each R,
  C_cre/C_law for the rho_cre that matches at (i) 10 kpc, (ii) the ONE1 end radius, (iii) the KiDS middle edge, and the
  ratio (max over R of the requirement)/(min over R of the requirement).
- **V5b (payment).** rho_cre(R)/rho_Lambda at every graded R (line 0.10).
- **V5c (forest / z > 2).** The created fraction at z = 2.2, 2.8, 3.4 and 4.4 and at z = 0.5, for the histories
  (i) uniform in cosmic time from z = 6 to 0, (ii) all of it after z = 2, (iii) all of it after z = 1. Against
  FRZ1's gate (Delta chi^2 <= 4 over 755 points; FRZ1 FAILS at 9916 / 9009 with the share already in place at z 2.2-4.4)
  and FZS1's (38.7 / 36.7, FRAGILE). Rule: any history that leaves more than 10 % of today's created charge in place at
  z >= 2.2 inherits FRZ1's fail (9916 / 9009) and is EXCLUDED; a history that leaves <= 10 % there must still deliver
  >= 0.9 of today's halo by z = 0.5, where KiDS measures it.
- **V5d (Solar System).** Created mass inside Saturn's orbit against 1e-10 M_sun.
- **V5e (universality).** The spread of V2b's required eps across the four masses (eps is one function of cosmic time).

### V6 The Bullet

- The created mass inside each component's R_200 against 0.10 of the mass measured there (200 rho_crit V), for the
  rho_cre that V5a demands at the inner radii and at the ONE1 radius. Reported as a range.
- Stated, not computed: for C-I the created charge is made in place, at a rate set by tau alone; it is not a component
  that passes through. It is polarization charge D.P inside any static region, so it tracks the potential, not the
  galaxies.

## 4. Lane label (frozen), per footing, first that applies

1. **NO VERDICT** if any known answer (section 5) fails, or any MUTATE twin fails to bite.
2. **SOURCED** if some candidate change passes V2, V3, V4, V5a-V5e and V6 on that footing.
3. **TRADES** if it passes V3, V5 and V6 but the amount is carried by a new constant or a new field, with the count of
   new ingredients and of fitted numbers named.
4. **EXCLUDED** otherwise. RESULT.md names every gate that fails and the factor.

The mutation arm (section 6) must fail.

## 5. Known answers (all must pass, else NO VERDICT)

- **KA1.** With the source off, V1a/b/c/d residuals 0, and the current reduces to QX17's E3 (residual 0).
- **KA2.** R541B's charge equation with -sqrt(-g) V(tau): dC/dt = -N a^3 V'(tau) (residual 0 against the FRW reduction).
- **KA3.** LFS1's S1(a): sqrt(gamma) rho_Q = d_i(X Y^i) + sqrt(gamma) d, generic 3D functions, residual 0; and S1(b)
  lambda N^2 = (d_t - N^j d_j) X, residual 0.
- **KA4.** LFS1's frozen flux with no source: d_t Y^r = 0 (zero shift, spherical, regular centre). Reproduced.
- **KA5.** FB1's KA1: rho_ph = sqrt(G M_b a0)/(4 pi G r^2) with p = J(g) = g^2/(2K) gives sigma^2 = p/rho_ph =
  (1/2) sqrt(G M_b a0) (residual 0).
- **KA6.** AMT1's pipeline: r_M for the four masses (1.934 / 6.479 / 8.640 / 10.877 kpc canonical; alt 0.9100 x), the
  budget radius 5.889 r_M, and X_s/5.41 = 10.998, each to 3e-3.
- **KA7.** Gauss on law S: 4 pi R^2 P^r(R) = M_b (nu - 1) = R^2 g a0/(G (g + a0)) with K P = (1 - mu) g (residual 0).
- **KA8.** The vacuum ledger: d(rho_Lambda a^3)/dt + p_Lambda d(a^3)/dt with p_Lambda = -rho_Lambda c^2 equals minus the
  created charge's energy rate (residual 0).

## 6. MUTATE twins (each must bite; the arm must fail)

- **MU1.** Add -sqrt(-g) V(tau) to (A). V1a must fail (residual = -V'(tau), nonzero).
- **MU2.** Replace the homogeneous source by hand with the law's own required source
  S_law(r) = (1/(4 pi r^2)) d_R[d_t C_law(R)] (i.e. inject the profile the law demands, ignoring where it comes from).
  V5a must PASS (ratio 1 to 1e-9 at every graded R) — proving the grader moves when the profile is right.
- **MU3.** Halve the drain: Lambda' -> Lambda'/2. Every V5b ratio must halve (to 1e-6).
- **MU4.** Set C_dust = 0 (no dust arrival). Every required rho_cre must rise, and the worst V5b ratio must rise.
- **MU5.** Drop the polarization charge from the profile identity (treat the created charge as dust, C_cre = rho_cre V
  with the created dust free to cluster by 200 x). The V6 Bullet ratio must rise by 200.

## 7. How this lane differs from the closed doors (checked before freezing)

| record | what it asked | why VCC1 is not it |
|---|---|---|
| R541A | a clock-matter coupling -alpha rho_b f(Q) | keeps the shift symmetry (f depends on Q, not tau); asks the cosmic 5.41, not a halo's 59.5. EXCLUDED |
| R541B | an early potential V(tau) on the clock | asks the cosmic share R = 5.41 by fitting V0, tau_s; homogeneous, background only. TRADES |
| R541C | a Gauss-Bonnet source gamma tau G_GB | a topological source in FRW; asks the cosmic share. EXCLUDED |
| R541D / R541E | eps d tau . J_B / J_{B-L} | sources the current through a *matter* current's non-conservation, early (sphalerons); asks eta_B. EXCLUDED. VCC1's C-VII is the z < 2 remnant, where B and L are conserved, so it is 0 |
| W4-24 | the vacuum constant inside the two-phase action's switch | asks whether a_0 and Lambda are tied in a *switched* class; never asks whether the charge is sourced. CLOSURE: kappa free |
| AMT1 | the arithmetic of the budget | assumes the conservation cap. VCC1 asks whether the cap itself can be broken |
| LFS1 / T4 | the cap itself | VCC1 grants them and asks what breaks them |

**What is new here:** the identity nabla_m J^m = dL/dtau (so the whole question is "does L contain a bare tau"), the
profile theorem d_t C(R) = Integral_{V(R)} S dV (which turns "what sources it" into "what shape is the source"), the
payment bound rho_cre <= rho_Lambda, the required eps = 2 c^2/v_flat^2 for the one inhomogeneous candidate that has the
law's profile, and the fact that its value must be one function of cosmic time while four masses disagree by 5.6 x.

## 8. Resources

Sympy plus small numpy grids; under 4 GB and a few minutes. Script `vcc1.py`, output `vcc1.out`, MUTATE via
`VCC1_MUTATE=MU1..MU5` to separate files.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
