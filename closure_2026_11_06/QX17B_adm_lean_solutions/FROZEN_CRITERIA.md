# QX17B_adm_lean_solutions: FROZEN CRITERIA (committed alone, before any script or number)

Owner 11-06: "go deeper on the derivation" and "and solve them", after QX17 (v3s covariant equations, CERTIFIED,
70bbb84f45). Adopts nothing. kappa = 1/2 FITTED. Not theory closed. Footings canonical a0 = 9.3603e-11, alt 1.1312e-10 m/s^2,
never pooled. Lstar = 21.7 / 22.9 pc (canonical / alt), mu_K = 0 in galaxies and the Solar System (record).
Lane id checked free (`ls closure_2026_11_06 | grep QX17B`, `git log --all | grep QX17B`: empty).

## B1. ADM (3+1) form, c restored
Unitary gauge tau = t: lapse N, shift N^i, gamma_ij. Derive the Hamiltonian constraint, the momentum constraint, the
lapse/P equations and the spatial stress S_ij in SI units (K = 4 pi G, A = c^2 n.grad n).
**Check B1-N:** on 3 random 3+1 configurations (QX17's generator, D = 4), the ADM expressions equal the covariant
QX17 closed forms projected (n n, n h, h h), relative residual <= 1e-10. The on-shell identities (momentum density of the
P sector = 0 once lambda is used; S_ij on shell = gamma_ij[K W'|P| - W + gamma F] - K W' P_i P_j/|P|) are checked on the same configs.

## B2. Lean certificate (fable_independent_2026/lean_2026/QX17B_field_equations.lean + _MUTATE twin)
Algebraic kernels only: Legendre stationarity and value (K0), mu = x/(1+x) from the gamma = 0 P equation, the lambda
solve and the vanishing of the P-sector momentum density, the on-shell spatial stress contraction, the K(Q) lapse
derivative, and AC2q's FRW cancellation, on-region nn identity and continuity at the switch. PASS = 0 sorry, standard
axioms only (propext, Classical.choice, Quot.sound); MUTATE twin must fail on each declared false claim.

## B3. Solutions
- **S-FRW:** closed form (QX17 K4), restated.
- **S-tensor:** from B1, the principal (kinetic) part of h_ij is GR's (argued from the ADM structure; no numeric line).
- **S-sph (static spherical, exact).** Areal gauge ds^2 = -N^2 c^2 dt^2 + B^2 dr^2 + r^2 dOmega^2, P = p(r) dr. Reduce the action
  (symmetric criticality) to 1D, derive the exact ODEs for N, B, p by sympy, and check them against QX17's covariant E2/E4
  on the ansatz (residual <= 1e-10 at random points). Solve as a BVP in vacuum outside a point mass M
  (inner regularity: no 1/r^2 mode in the extra field; outer: no growing mode).
  - **Sun** (M = 1 Msun): PASS iff the extra field y = g - g_N equals GM/Lstar^2 to <= 1 % for 10 AU <= r <= 1e-3 Lstar,
    both footings (record C6 hedgehog). Report y/(GM/Lstar^2) at 1, 10, 100 AU and the approach to law S beyond Lstar (no line).
  - **Galaxy** (M = 1e10 Msun point mass): PASS iff |g/g_S - 1| <= 1e-2 for 1 <= r <= 30 kpc, both footings.
  - **GR remainder:** the full nonlinear solve differs from the weak-field solve (same BVP with N = e^Phi, B = 1 to first order)
    by <= 10 U_max (U = GM/(c^2 r)) at every grid point. Reported; FAIL if larger.
  - **Known answer:** Lstar -> 1e-3 pc gives law S to <= 1e-3 for r >= 1 kpc (galaxy).
  - **MUTATE:** gamma_L = 0 (no stiffness): the Sun's y at 10 AU must be the unscreened law-S value (>= 1e3 x GM/Lstar^2), i.e.
    the hedgehog check FAILS.
- **Full 3+1 jet variation** (QX17's method, D = 4, one seed): attempted in the background; if it does not finish within
  3 h it is reported as NOT RUN, and B1-N carries the 3+1 statement.

Labels: B1/B2/S-sph each PASS / FAIL; lane CERTIFIED iff all pass.
