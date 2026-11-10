# LFS1 (can the khronon's leafwise flux supply the law's halo?): FROZEN CRITERIA, committed alone before any script, Lean file or number

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Both footings (canonical a0 9.3603e-11,
alt 1.1312e-10 m/s^2), never pooled. The halo's charge is cold dark energy (the clock's charge), never a particle. Not
a LCDM lane. No download. This lane edits nothing outside `closure_2026_11_10/LFS1_leafwise_flux_supply/` (its Lean files
live here and are compiled with the in-repo build: `cd fable_independent_2026/lean_2026 && lake env lean <absolute path>`).

Id check: `ls closure_2026_11_10/` has no LFS1; `git log --all --oneline | grep -c LFS1` gave 0.

## 0. The question

`fable52_push/CLOSURE.md` ("The amount"): every failed completion (COL1, FLD1, MK1, MK2, TK1, DT3) treats the law's halo
as advected clock charge that has to fall in, and the charge that arrives is far short. "One in which the halo is the
polarization of a static clock needs no advected dust; whether the action's leafwise flux can supply it has not been
computed." In action (A) (QX17 eq. E3, unitary gauge, lapse N, shift N^i, leaves gamma_ij)

    d_t(sqrt(gamma) rho_Q) - d_i[ sqrt(gamma) ( N^i rho_Q + lambda N^2 P^i ) ] = 0,
    rho_Q = N { D_i[(1 + gamma_L Pi_+) P^i] + (1 + gamma_L Pi_+) P^i A_i } + mu_K^2 (1/N - 1)/K,  A_i = d_i ln N,

and the normal part of the P equation (QX17 E2) fixes the multiplier:

    lambda = (1 + gamma_L Pi_+) n^m d_m ln N + gamma_L n^m d_m Pi_+,   n^m d_m = (1/N)(d_t - N^i d_i).

Can the term lambda N^2 P^i build the law's halo around a growing baryon mass while the clock stays static?

QX17's equations are taken as certified (its K1-K3 are direct variations of (A)); this lane re-derives nothing from the
Lagrangian, but re-checks the pieces it uses (KA3).

## 1. Hand result to be checked (written before any script; the lane's job is to confirm or refute it)

Write X = N (1 + gamma_L Pi_+), Y^i = sqrt(gamma) P^i. Then (identity) sqrt(gamma) rho_Q = d_i(X Y^i) + sqrt(gamma) d with
d = mu_K^2 (1/N - 1)/K, and by the normal equation lambda N^2 = (d_t - N^j d_j) X. With mu_K = 0 (the record's galaxy
setting) the khronon equation becomes

    d_i [ X d_t Y^i  +  (N^j d_j X) Y^i  -  N^i d_j (X Y^j) ] = 0 .

- Zero shift (a static clock): d_i(X d_t Y^i) = 0. In spherical symmetry, regular at the centre: d_t Y^r = 0 at every r.
  So the polarization flux through every sphere, hence the halo charge C(R) = X Y^r(R) (x 4 pi), is frozen up to the
  factor X = N (1 + gamma_L Pi_+) = 1 + O(Phi/c^2) + O(gamma_L Pi). The halo cannot grow.
- With a shift, spherical: d_t Y^r = N^r d_r Y^r: the polarization flux is carried with the clock's flow (an advected
  invariant). In a sphere that moves with the clock the enclosed charge changes only by Y dX.
- So the leafwise flux is not an independent supply: the normal equation sets lambda so that the flux exactly carries the
  change of the factor X in rho_Q and nothing more. The halo's charge inside a sphere is the charge the clock carried in.

Expected label from the hand result: ILL-POSED on both footings (A1 fails by a factor of order c^2/|Phi|). If the scripts
refute the hand result, the label follows the scripts, not this section.

## 2. Inputs (frozen)

- Constants: G 6.674e-11 SI, M_sun 1.98847e30 kg, kpc 3.085677581e19 m, c 2.99792458e8 m/s, Gyr 3.15576e16 s.
- Background for t(z) and the mean dust density: flat, H0 67.4 km/s/Mpc, Omega_d = I0 / (3 (H0/c)^2) with KD1's
  I0 4.037e-8 Mpc^-2, Omega_b = Omega_d / 5.41, Omega_r h^2 4.15e-5, Lambda the rest (TK1's background).
- The law: law S, g^2 = g_N (g + a0), g_N = G M_b(t) / r^2 (point mass; graded radii r >= 10 kpc, disclosed); the static
  constitutive law K P = (1 - mu) g with mu = x/(1+x), x = g/a0 (QX17 limits table, gamma_L = 0); C(R,t) = M_b (nu - 1)
  = R^2 (g - g_N) / G.
- Masses: log M_b(z = 0) = 9.4, 10.45, 10.7, 10.9.
- Accretion history (primary): M_b(z) = M_b0 exp(-alpha z), alpha = 0.8. Brackets alpha = 0.4 and 1.5 (reported, never
  label-setting).
- Lapse: N = 1 + Phi/c^2, Phi(r,t) = -Int_r^inf g dr' with the law out to R_cap(t) and a point mass M_b (1 + X_cap)
  beyond (primary). Bracket: the law out to 10 Mpc, point mass beyond (reported).
- gamma_L Pi_+ = 2 pi G rho_ph L*^2 / c^2 with rho_ph the law's phantom density, L* = 21.7 pc canonical / 22.9 pc alt.
- Cap: R_cap = x_t r_M, x_t^2 = X (X + 1), r_M = sqrt(G M_b / a0), X = 59.486 canonical / 59.503 alt (PD1 / ONE1).
- Turnaround radius at z 0 and the KiDS window edges: FLD1's table (quoted, not recomputed): R_ta = 120 / 268 / 325 / 378
  kpc; inner edge 81 / 272 / 362 / 456 kpc; middle edge 190 / 637 / 849 / 1069 kpc (log M_b 9.4 / 10.45 / 10.7 / 10.9).
- FLD1's corrected arrival: the charge that arrives as dust is <= 5.1 % of the halo's need (quoted).
- mu_K = 0 primary (the record's galaxy setting). Bracket mu_K = 1 per Mpc (host-free KiDS's bound; reported): its dust
  part d is computed and the hand result's mu_K term is checked symbolically.

## 3. Part A items (all computed and reported; the label rule is section 4)

### A1 lambda: finite, single-signed, and the one the normal equation fixes?

- **S1 (sympy, exact).** (a) sqrt(gamma) rho_Q = d_i(X Y^i) + sqrt(gamma) d, generic 3D functions, residual 0.
  (b) lambda N^2 = (d_t - N^j d_j) X from the normal equation, residual 0. (c) The khronon equation reduces to section 1's
  divergence form, residual 0, generic 3D with shift. (d) Spherical: with zero shift, d_t Y^r = 0; with shift,
  d_t Y^r = N^r d_r Y^r (regularity at r = 0 stated as the assumption). (e) With mu_K != 0: the enclosed total charge
  X Y^r + Int sqrt(gamma) d in a sphere moving with the clock changes only by Y^r dX (residual 0).
- **S2 (numeric, independent route).** A spherical finite-difference integration of the khronon equation with lambda from
  the normal equation, for an arbitrary (non-law) N(r,t), Pi(r,t) and initial P, zero shift: max |Y^r(t)/Y^r(0) - 1| over
  the grid must be below 1e-6 (discretisation), while the same run with lambda set to the supply value of the next bullet
  must move Y^r by order 1. Confirms or refutes S1(d) numerically.
- **Demanded lambda.** For a static clock (zero shift) at fixed R the halo must follow the law, so the khronon equation
  demands (exactly, from the integrated khronon equation) lambda_s N^2 Y^r = d_t (X Y^r)_law, i.e.
  lambda_s N^2 = X d_t ln C_law(R,t). The allowed one is lambda_n N^2 = d_t X. Ratio
  rho_lambda := lambda_n / lambda_s = (d_t ln X) / (d_t ln C_law), on the grid R = 10, 30, 100, 300 kpc and
  R_cap(z) (if > 300 kpc), z = 0, 0.5, 1, 2, four masses, per footing. Also the integrated ratio from z 2 to 0:
  ln[X(t0)/X(t2)] / ln[C(t0)/C(t2)].
- **A1 PASSES** iff lambda_s is finite and of one sign on the grid AND |rho_lambda - 1| <= 0.5 at every grid point. Else
  A1 FAILS, naming the worst point and the size of rho_lambda.
- Reported: the frozen-halo deficit (a clock static since z_s = 2, 1, 0.5 keeps its charge up to X: C(R, z 0) / C_law(R,
  z 0)); the shift (creep) speed v = d_t Y^r / d_r Y^r the law would need (km/s) at each grid point; and the radius R'(z)
  at z = 1, 2 that held, in the clock's flow, the charge now inside R (C(R', t) = C(R, t0)), against FLD1's turnaround
  scale (R_ta(z) read as R_fold(z) / (R_fold/R_ta)(z) from FLD1's text: 0.46 at z 1, 0.435 at z 2).

### A2 where the charge comes from; does the supply leave negative or unphysical rho_Q?

- **Net charge theorem (sympy + Lean, structural).** For any region whose boundary lies where P = 0 (a free-falling clock:
  A = 0, so P = 0; FB1, FLD1), Int sqrt(gamma) (rho_Q - d) = closed surface integral of X Y = 0. A static halo that ends
  where the clock stops being static therefore carries, at and just outside its edge R_s, a negative polarization charge
  equal to -C(R_s) (a layer of D.P < 0), whatever the width of the transition.
- Numbers per mass and footing at R_s = R_ta(z 0) (FLD1) and R_s = R_cap(z 0): C(R_s)/M_b; the edge's mean rho_Q for a
  transition width w = 0.1 R_s against the mean cold-dark-energy density today (Omega_d rho_crit); the positive dust
  charge needed to make the edge non-negative, against 5.41 M_b (form B's cosmic share) and against FLD1's arrival
  (<= 0.051 C_need).
- Reservoir: whether the leafwise flux can reach the background dust at all (it cannot cross a surface where P = 0; S1
  shows any flux through such a surface is the advective N^i rho_Q term).
- **A2 PASSES** iff the static region including its edge has rho_Q >= 0 everywhere with mu_K = 0 primary (i.e. the edge
  charge is >= 0). Else A2 FAILS (negative gravitating clock density at the edge).

### A3 reach by z 0 (reported; label-setting only through rule 3)

R_s(z 0) := the largest radius at which a static interior can meet the exterior without a velocity jump, bounded by
FLD1's R_ta(z 0). Compared with R_cap and the KiDS inner and middle edges, per mass. Also the projected lensing effect of
the edge layer (a thin shell of mass -C(R_s) at R_s) on Delta Sigma at R = 0.5 R_s and 0.9 R_s, as a fraction of the law
halo's own Delta Sigma there (reported).

### A4 matching the static interior to the expanding clock outside

Inside: theta = 0, A = g(R_s) (static), P = (1 - mu) g / K. Outside: the free-falling clock, A = 0, P = 0, theta = the
local expansion (3H far out). Classification, per R_s in {R_ta, R_cap}:
- **SMOOTH** iff A and n are both continuous (needs g(R_s) = 0 and the exterior clock at rest in the static frame).
- **WALL** iff A jumps (g(R_s) > 0): the jump carries the polarization layer of A2 (surface charge -C/(4 pi R_s^2) as a
  sheet; Delta g = -G C(R_s)/R_s^2 across it). This is the switch class's wall (law-on region inside, free-falling clock
  outside; SWT1 T1 / HE1: it cannot be held).
- **FOLD** iff n jumps (exterior clock moving in the static frame: R_s != R_ta), reported in addition.
Printed: g(R_s)/a0, sigma_edge (M_sun/pc^2), Delta g / g.

## 4. Lane label (frozen), per footing, first that applies

1. **NO VERDICT** if any known answer (section 5) fails.
2. **ILL-POSED** if A1 fails, or A2 fails, or A4 is WALL or FOLD at the R_s that A3 uses (R_ta). RESULT.md names every
   item that fails.
3. **SUPPLIES-SHORT** if A1 and A2 pass, A4 is SMOOTH, and R_s(z 0) < R_cap at any of the four masses.
4. **SUPPLIES** otherwise.

Part B (linear stability of the supply flow, SPARC rows) is graded only for labels 3-4; under labels 1-2 RESULT.md says it
was not graded.

Counts against the candidate (listed whatever the label): the frozen-halo deficit; the creep speed; R_s < KiDS inner or
middle edge; any bracket that changes an A1 or A2 verdict.

## 5. Known answers (all must pass, else NO VERDICT)

- **KA1** Deep-law hydrostatics: the phantom density rho_ph = sqrt(G M_b a0)/(4 pi G r^2) held by the isotropic pressure
  p = J(g) = g^2/(2K) (FB1) gives sigma^2 = p/rho_ph = (1/2) sqrt(G M_b a0) (sympy residual 0); printed sigma at log M_b
  10.7 per footing.
- **KA2** Gauss on law S: 4 pi R^2 P_r(R) = M_b (nu - 1) = R^2 g a0 / (G (g + a0)) with K P = (1 - mu) g (sympy residual 0).
- **KA3** QX17's printed equations, re-checked: (a) unitary-gauge form of E3 from the covariant current
  n^m rho_Q - lambda P^m / Q (sqrt(-g) = N sqrt(gamma), P^0 = 0): residual 0; (b) lambda from projecting the full E2 on n:
  residual 0; (c) the Noether cross-check: QX17's T^P_{0i} with lambda from (b), zero shift, gamma_L = 0, equals 0 (the
  static clock's sector carries no momentum), consistent with (d) of S1 via the 0i metric equation: residual 0.
- **KA4** sqrt(M_sun a0 / G) = 25,914 M_sun per kpc canonical to 1e-3 (TK1 KA7).
- **KA5** R_cap(z 0) = 116 / 389 / 518 / 653 kpc canonical (FLD1's table) within 0.5 %.
- **KA6** S2's zero-shift run conserves Y^r to 1e-6 (this is also the numeric check of S1(d)); if S1 and S2 disagree the
  label is NO VERDICT.

## 6. MUTATE twins (must bite)

- **MU1** Flip the sign of lambda in the khronon equation (QX17's own mutation): S1(c)/(d) and KA3(c) must fail
  (non-zero residual) and S2's zero-shift run must move Y^r by order 1.
- **MU2** Inject lambda := lambda_s by hand (ignore the normal equation): A1 must PASS (rho_lambda = 1) in the grader.
- **MU3** Continue P past the edge (no P = 0 exterior): A2's edge charge must vanish and A2 PASS in the grader.
Each twin writes separate outputs (`*_MUTATE_MU*.json/.out`).

## 7. Lean

A short file for the structural claims: (i) telescoping: the polarization charge of a region whose boundary flux is zero
sums to zero, so a positive interior forces an equal negative edge; (ii) the discrete form of the frozen-flux statement:
if each step's charge ratio equals the ratio of X, then C/X is constant, and with X in [1 - eps, 1 + eps] the charge can
grow at most by (1 + eps)/(1 - eps); (iii) KA2's algebra. A MUTATE twin of false statements must fail to compile.

## 8. Resources

Sympy plus small numpy grids; under 4 GB and minutes. Nothing heavy, nothing preempted.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
