# SET1 FROZEN CRITERIA: irreversible settling of cold dark energy toward the law's halo (2026-11-10)

TEST lane, quarantined. Relabels nothing, adopts nothing, not registered. kappa = 1/2 FITTED; not theory closed.
Footings graded separately, never pooled: canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2.
Cold dark energy is a gravitating field component, never a particle. The phase-space density f(x, v, t) used here is a
description of the field's state; it adds no particle species. No LCDM-calibrated machinery enters any verdict.
Lane id: `ls closure_2026_11_10/` and `git log --all --grep=SET1` returned nothing before this file was written.

This file is committed alone, before any script exists or any number is computed.

## 0. The candidate (the closure chat's, 2026-11-10; tested here, not adopted)

    df/dt + v . grad f - grad Phi . df/dv = -(f - f_law)/tau,    del^2 Phi = 4 pi G (rho_b + rho_c),   rho_c = Int f d^3v.

- f_law: same local density as f, zero mean velocity, and "the velocity spread that makes the law's halo an equilibrium";
  in spherical symmetry the brief writes it isotropic (Maxwellian) with rho_c sigma^2 = J(g),
  J(g) = (a0^2 / 4 pi G)[u - ln(1 + u)], u = g/a0, g the local total field.
- tau: infinite in single-stream flow; eta x local orbital time (2 pi r / v_c) after streams cross. eta = 1 primary;
  0.3 and 3 reported.
- Right side off: cold dust. Gravity is Newtonian on rho_b + rho_c; the law is not put into gravity.

**What is put in by hand (stated once, binding on every reading below).** The law's function enters through the target
state f_law (through J), and tau's rule is a postulate. A pass anywhere in this lane is therefore an existence statement
about an irreversible, charge-conserving joint, not a derivation of the law.

**Readings of the target spread.** The candidate as written is LOCAL: f_law is built from the local density of f and the
local field g. That is reading **L** (rho sigma^2 = J(g)), and it sets the label. If the brief's identity "the spread that
makes the law's halo an equilibrium = J(g)" fails for some profile, the spread that does hold the law's halo there is
computed and REPORTED as reading **D**, with its locality stated. Reading D does not set the label (it is a different,
non-local candidate the brief did not write).

## 1. Hand estimate (written before any script; to be compared with the outcome in RESULT.md)

**Mine.**
- A1, point mass: P = J(g) with Poisson gives the law exactly at the Jeans level. Outside the baryons Jeans + Poisson
  with P = J(g) reads g'(2 + u)/(1 + u) + 2g/r = 4 pi G rho_b, and the law reads mu(u) x [the same left side] =
  4 pi G rho_b, so they coincide where rho_b = 0; the integration constant r^2 mu g is fixed to G M_b by a regular centre
  (no cold point mass). Deep field: sigma^2 = (1/2) sqrt(G M_b a0), rho = sigma^2/(2 pi G r^2).
- A1, extended spherical baryons: **fails.** Put the law's state into Jeans with P = J(g): the residual should be exactly
  dJ/dr + rho_ph g = a0 rho_b (the divergence of the anisotropic part of M5's field stress, whose radial-minus-tangential
  part in spherical symmetry is -a0 g_N / 4 pi G). The self-consistent P = J(g) state is then the law of an effective mass
  M_eff(r) = Int_0^r mu dM_b < M_b. In a cored profile the centre is always deep (g -> 0) and the state there has
  g ~ (pi G rho_b0) r rising outward, so rho_c = -g'/(4 pi G (1 + u)) < 0: no f >= 0 static state with this target. A
  cusped (Hernquist) profile keeps rho_c >= 0 but the field sits low by ~0.5 log10(M_eff/M_b): about -0.05 dex at
  log M_b 10.9 and -0.13 to -0.17 dex at 9.4 (u ~ 1 at R_50 there), above the SPARC line at the low mass.
- A1, reading D: the isotropic pressure that does hold the law's halo of a sphere is P_eq = J(g) + a0 Int_r^inf rho_b dr'
  (a radial column of baryons): positive, but not local.
- A1, kinetic (reported): a local Maxwellian is a stationary solution of the collisionless operator only where sigma^2 is
  uniform. Around a point mass sigma^2 = J/rho_ph runs from G M_b/(2 r) inside r_M to (1/2) sqrt(G M_b a0) outside, so
  f = f_law is not static for r below a few r_M even at the Jeans level's exact point; and with tau = eta t_orb the
  Knudsen number sigma tau / r is ~ 4 eta, so the BGK steady state is not close to f_law there.
- Expected label: **STRUCTURE FAILS AT A1** on both footings (extended profiles, reading L). A2 onward not reached.
- If A1 were to hold: A2 would fail as the closure chat says (in a disc |g| is not constant on equipotentials, so no
  P(|g|) balances anything, and the phantom's force density has a curl); A3's momentum and energy sink has nowhere to
  go that SMF1 / PAR1 allow; Part B start (i) short as COL1.

**The closure chat's (quoted from the brief).** A1 holds; A2 is where it most likely breaks (the law's exact stress is a
field stress, not a pressure); with start (i) the amount is short, as COL1 found; with start (ii) it settles in the middle
masses and misses at the ends, because the share's own collapse radius goes as the cube root of the mass and the law's
cap as the square root.

## 2. Fixed inputs

- Units kpc, km/s, Msun; G = 4.30091e-6; a0 in (km/s)^2/kpc = a0[SI] x 3.0857e19 / 1e6. K = 4 pi G.
- Masses log M_b = 9.4, 10.45, 10.7, 10.9 (the record's four). r_M = sqrt(G M_b / a0).
- Sizes: R_50 from SCS2's relation (Shen et al. 2003 late types, as SCS2 quoted it from memory; read, not re-sourced):
  R_50 = 0.10 kpc M^0.14 (1 + M / 3.98e10)^0.25.
- Extended spherical profiles, both set to that R_50: Plummer (cored; b = R_50 / 1.3048) and Hernquist (cusped;
  a = R_50 / (1 + sqrt 2)).
- SPARC line (dex in g, the RAR-style residual the record grades): 0.0660 canonical / 0.0658 alt (SS1 G5 = L0 + 0.010;
  PD1 P2 rms 0.0563 / 0.0558).
- Graded window for extended profiles: r in [0.3, 6] R_50, 60 log-spaced points (SPARC's last radii sit near 10 R_d =
  6 R_50 at log M_b 10.45).
- The law (spherical, exact): mu(u) g = g_N, mu(x) = x/(1 + x); g_law = (g_N + sqrt(g_N^2 + 4 a0 g_N))/2;
  rho_ph = (1 / K r^2) d[r^2 (g_law - g_N)]/dr. Point mass: M_ph(<r) = M_b (sqrt(1 + 4 x^2) - 1)/2, x = r / r_M.

## 3. Part A items, in order; stop at the first structural failure

### A1. The fixed point, spherical

- **A1a (sympy, exact).** (i) Jeans with isotropic P = J(g) plus Poisson is equivalent to F(g) = K rho_b with
  F(g) = g'(2 + u)/(1 + u) + 2 g / r; the law is mu(u) F(g) = K rho_b. (ii) The residual of Jeans with P = J(g) on the
  law's state (g_law, rho_c = rho_ph), dJ/dr + rho_ph g, simplified exactly. (iii) Point mass: residual 0 for r > 0;
  deep-field known answer sigma^2 = (1/2) sqrt(G M_b a0) and rho = sigma^2 / (2 pi G r^2). (iv) Uniqueness: outside the
  baryons F(g) = 0 is d(r^2 mu g)/dr = 0, a one-parameter family r^2 mu(u) g = C; state which C a regular centre forces
  and what the rest of the family is.
- **A1b (numbers).** For both profiles at the four masses and both footings, solve the P = J(g) state exactly as
  Y(r) = r^2 mu(u) g / G = Int_0^r mu(u) dM_b (from A1a(i)), with g from a0 u^2/(1 + u) = G Y / r^2. Report: min rho_c
  and where it is negative (radius range, mass of the negative region over M_b); rms and max |log10(g / g_law)| over the
  window; the asymptotic offset 0.5 log10(M_eff / M_b); for reading D, P_eq = J + a0 Int_r^inf rho_b dr' (P_eq >= 0
  check) and the ratio of its non-local piece to J at R_50.
- **A1c (reported, not label-setting).** Point mass: sigma^2(r) = J / rho_ph, d ln sigma^2 / d ln r and the Knudsen
  number sigma tau / r (tau = eta 2 pi r / v_c; eta 0.3, 1, 3) at r = 0.3, 1, 3, 10 r_M.

**A1 rule (per footing).** STRUCTURE FAILS AT A1 if any of:
1. A1a(iii) fails (the point mass is not a static P = J(g) state with the law's field);
2. for either profile at any of the four masses, rho_c < 0 on a resolved region (min rho_c below -1e-6 of the window's
   peak rho_ph, over a radial range wider than 1 % of R_50): no f >= 0 static state exists with the target;
3. for either profile at any of the four masses, the rms of log10(g / g_law) over the window exceeds the SPARC line.
Otherwise A1 HOLDS and A2 is run.

**A1 known answers (must pass before any A1 row is graded).**
- KA1: point-mass M_ph closed form against the numeric rho_ph integral at x = 0.1, 0.3, 1, 3, 10 (relative 1e-6).
- KA2: Newtonian limit (a0 x 1e-6): the P = J(g) Plummer state equals g_N to 1e-4 relative over the window.
- KA3: deep limit (a0 x 1e8), Plummer: g = (G M / 2 r b)[1 - (1 + r^2/b^2)^(-3/2)] (closed form; my derivation) to 1e-4
  relative. Hernquist: g = G M (r + 2a) / (2 a (r + a)^2) to 1e-4.
- KA4: a compact Plummer (b = 1e-4 r_M): the P = J(g) state equals the law at r >= 0.1 r_M to 1e-3 dex.
**A1 MUTATE arms (outputs `*_MUTATE_<arm>.*`; each must bite):**
- M1 target spread doubled (P = 2J): the point-mass state misses the law by more than the line somewhere in
  [0.3, 30] r_M.
- M2 the A1a(ii) identity checked against 2 a0 rho_b: residual nonzero.
- M3 no target pressure (J = 0): the state is Newtonian and misses the law by more than the line in the window.

### A2. Positivity and geometry (only if A1 holds)

Razor-thin exponential and Kuzmin discs at the four masses (SCS2's AQUAL backgrounds, imported read-only). Compute:
the mass-weighted sine of the angle between grad rho_ph and grad Phi (zero iff an isotropic pressure can hold the
phantom); the anisotropic positive-definite Jeans construction (S_zz = Int_z^inf rho_ph |g_z| dz', S_RR = S_zz,
S_phiphi from the radial equation; report where S_phiphi < 0); the best isotropic-pressure equilibrium rho_c = F(Phi_tot)
with Newtonian Poisson on rho_b + rho_c, F >= 0 chosen (6-knot log spline, least squares) to fit the law's midplane
rotation curve over [0.5, 10] R_d. **Rule:** STRUCTURE FAILS AT A2 if the best isotropic gap (rms dex in g over that
range) exceeds the SPARC line at any mass on either disc. KA: SCS2's KA2 (Kuzmin closed form) re-run; a spherical
background gives sine 0 to 1e-3. MUTATE: a phantom shifted to Phi + const x z^2 must give sine > 0.05.

### A3. Conservation and irreversibility (only if A2 holds)

Charge: Int (f - f_law) d^3v = 0 identically. H-theorem: find a functional that only decreases (candidate: the free
energy for an isothermal target; the relative entropy to the steady state otherwise), or show none exists. Momentum and
energy removed per unit mass at the four masses for a halo settling from the infall state (from Part B if run; else the
energy difference between cold infall at turnaround and the law's isothermal halo). State the second equation a closed
system would need, which M5 hypothesis is dropped (momentum conservation), and whether SMF1's S0b (Gauss) and S0c
(starvation) apply when the halo is the medium's own mass (quote SMF1). **Rule:** STRUCTURE FAILS AT A3 if the removed
energy and momentum can only go to a channel the record already excludes (SMF1, PAR1 C16-C20, MEDIUM_DESIGN section 3),
and the lane cannot name one it does not.

### A4. The expanding universe (only if A3 holds)

Background and linear modes with tau infinite are exactly dust (state). Check that no tau-on region exists before first
crossing in a linear mode, and that a homogeneous region at turnaround (single stream, zero expansion) stays
collisionless (TK1's edge). **Rule:** STRUCTURE FAILS AT A4 if the stream-crossing switch can fire on a single-stream flow.

### A5. Hot systems (reported, not graded unless forced)

The weakest local rule for tau that leaves a system hotter than the law's spread unsettled (e.g. tau growing with
sigma_local / sigma_target), and its cost: one more postulate. A rule that cannot be stated locally counts against.

**Part A label:** STRUCTURE HOLDS (spherical) / STRUCTURE FAILS AT <item> / NO VERDICT (a known answer of the item that
would set the label fails), with A2's disc reading stated beside it.

## 4. Part B, the collapse (only if A1 to A4 are not structurally dead)

Spherical shell code: collisionless shells that pass through each other, Newtonian gravity of a softened (1 kpc) baryon
point mass ramped over 1 Gyr (COL1's set-up) plus the shells, Hubble-flow start at z = 10 on the KD1 footing cosmology,
as COL1 / FLD1 used. Relaxation: a BGK step on crossed shells (each crossed shell redraws its radial velocity from the
target at rate 1/tau; charge per shell conserved). Starts frozen: (i) COL1's uniform medium; (ii) total cold mass
59.5 M_b as its own top-hat overdensity turning around at z 2 and at z 5. Measurements at z = 0 at the four masses:
enclosed cold mass against M_b (sqrt(1 + 4x^2) - 1)/2 from 0.2 r_M outward; residual of g against the line; steadiness
over the last 2 Gyr (change < 0.02 dex); reach against FLD1's lines (SPARC last radii, KiDS windows, cap at 59.5 r_M);
total mass against 59.5 M_b; energy removed.
**Rule per start and footing:** SETTLES TO THE LAW'S HALO if, at all four masses, the g residual over [0.2 r_M, R_cap]
is within the line, the state is steady, and the reach meets the cap; DOES NOT SETTLE if any of these fails; NO VERDICT
if a known answer fails. Known answers: energy conservation with the right side off (1e-4 over 2 Gyr); a Kepler shell
(1e-3); FLD1's law-off R_fold at log M_b 10.45 (160.9 kpc, 5 %) and COL1's first-crossing times where the set-ups
coincide (2 %). MUTATE: relaxation off (must not settle), target spread doubled (must miss the law), eta x 10 (reported).

## 5. What counts AGAINST the candidate (frozen)

- No f >= 0 static state with the target for an extended baryon profile, or a static state off the law by more than
  the SPARC line (A1).
- No positive spread tensor for discs within the SPARC line (A2).
- The settled state not steady; the amount or the reach short, as in COL1 and FLD1 (Part B).
- A hot rule that cannot be stated locally (A5).
- The removed energy having nowhere to go that SMF1 or PAR1 do not exclude (A3).
- A target that is only definable non-locally (reported against reading D; it is not the candidate as written).

## 6. Output and process

Scripts write `set1_*.out` / `.json`; MUTATE runs write `*_MUTATE_<arm>.*`. One thread per job, `nice -n 10`.
Later changes go in `AMENDMENT_An.md`, each committed alone, marked post hoc if any number has been seen. RESULT.md leads
with the label for both footings.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
