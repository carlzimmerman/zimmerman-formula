# FA2 frozen criteria: grading the top three local-action candidates (C1, C2, C3 of IDEAS.md)

Frozen before any FA2 script or number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle.
Footings graded separately, never pooled:
- canonical: a0 = 9.360324825027975e-11 m/s^2, Lstar = 21.7 pc;
- alt: a0 = 1.1312035414413022e-10 m/s^2, Lstar = 22.9 pc.

Compute: one script fa2.py, one thread, nice 15, under 1 GB, preemptible (exit on SIGTERM, nothing long-lived).
Outputs fa2.json / fa2.out; fa2.py --mutate writes fa2_MUTATE.json / fa2_MUTATE.out. No downloads; every input is on
disk in the record and read read-only.

## 0. Read-only reuse

- GB1 battery (criteria e9464bc8ce): gb1.py's source executed up to its main block, exactly as WL1 does, for every
  loader and for gates G1-G8 with GB1's lines unchanged.
- KiDS K-G6: QX5's lensing() loader (59 Brouwer+2021 Fig. 9 isolated-lens points, 4 mass bins, each lens a point
  mass, R = sqrt(G M_b / g_bar)). Line |mean log10(g_cand / g_base)| <= 0.05 dex (QX7 iter_4/5 G6 line, as WL1).
  Graded in the pointwise reading (g at R from the enclosed effective mass), the reading in which each candidate's
  multiplier is defined; the projected 4 G DeltaSigma reading is not computed (disclosed).
- SV5 iter_1 web: sv5_web.py's functions (seed 5, 128^3, 2000 Mpc, its z grid, its projection). Line r <= 1.072.
- WL1 stage 2 (d306609bfb): the hosts' retained phantom inside the law-on turnaround radius gives r_pop 3.75 / 4.32
  at z 1 (q_pop 0.936 / 1.079 vs 0.0354). Read from wl1.out exactly. Used as a lower bound on the web row of any
  candidate whose phantom multiplier is >= 1 everywhere inside R_ms (WL1: "holds for any arm-(i) key that keeps KiDS").

## 1. Known answers (KA FAIL: stop, nothing graded)

- KA-GB1: rebuilt L0 class means equal gb1.json KA1 to 1e-9, and L0's G1-G8 statuses equal gb1.json's, both footings.
- KA-K: the 59-point KiDS base mean log10(g_obs / g_law) equals QX7 iter_4 BASE L (0.141707 / 0.101597) to 1e-9.
- KA-SV5: sv5_iter1.json r = 74.7424 (canonical) and alt to the quoted rounding 89.4; and C2's own web code at
  L2 = infinity reproduces those JSON r values to 1e-6 relative.
- KA-WL1: wl1.out stage 2 z 1 lines read r_pop 3.75 / 4.32.
- KA-ell: for a point mass the code's ell equals r/2 (Newtonian limit, y = 1e4) and r (deep limit, y = 1e-4) to 1e-3.

## 2. Shared definitions

- **Local field length** ell = |g| / |dg/dr| = r / |s|, s = d ln g_law / d ln r, from each system's own profile:
  SPARC per galaxy (np.gradient of ln g_law in ln r over its points); X-COP per cluster over its points; groups the
  two-point slope between R2500 and R500; ellipticals from M_b(r) at r(1 +- 1e-3); KiDS lenses and the Solar System
  from the point-mass law. Coma UDGs and dSphs with an external field: |A| = a0 sqrt(x_e^2 + x_i^2) with
  x_i = x nu(x_e) (quasi-Newtonian EFE), |grad A| = 2 a0 x_i / r_h (internal-dominated), so
  ell = r_h sqrt(x_e^2 + x_i^2) / (2 x_i); without x_e, the point-mass law. Approximations, frozen as stated.
- **Required multiplier** at a point: F_req = (10^D g_law - g_N) / (g_law - g_N) (GB1's interface, b = 1).
- Bins in log10: width 0.2 dex, edges at integer multiples of 0.2.

## 3. C1, profile-length key (any F of the local ell)

Graded as a key class (IDEAS C1: the action's static observable is a multiplier set by ell / L2).
- **Oracle (most generous member that passes X-COP's mean).** In every ell bin holding at least one X-COP point,
  F_bin = median of F_req over those X-COP points; F = 1 in every other bin. Then the generous scaling
  F_gen = 1 + t (F_bin - 1), with t in (0, 1] the smallest value that brings X-COP's mean residual to <= +0.05
  (t = 1 if not reachable). F_gen is the graded member: it is the smallest boost that still passes X-COP's mean.
- **Rows:** GB1 G1-G8 with (b = 1, F = F_gen(ell), T = 0); K-G6 with g_cand = g_N + F_gen(ell) (g_law - g_N) at
  each KiDS point; web: F = 1 on web scales by construction, so W = L0's r (74.7 / 89.4), and any non-monotone variant
  that turns the web off still keeps F >= 1 inside R_ms, so W >= WL1's r_pop.
- **Reported:** per bin, the KiDS points and group points sharing X-COP's bins (the same-ell conflict), and the
  F_bin table.
- **MUTATE:** M1, X-COP D set to 0 (no cluster need): F == 1, every row must equal L0 and K-G6 shift = 0 (PASS);
  bites iff main K-G6 FAILs. M2, Newton (F = 0): G1 must FAIL.

## 4. C2, Yukawa-screened phantom (range L2)

- **Sympy (derivation, graded as a statement):** (a) QUMOND's action L = -rho Phi - (1/8 pi G)[2 grad Phi . grad psi
  - a0^2 Q(|grad psi|^2 / a0^2) - m^2 (Phi - psi)^2] gives grad^2 psi = 4 pi G rho - m^2 (Phi - psi) and
  grad^2 Phi = 4 pi G rho + div[(nu - 1) grad psi] identically (verified by EL residual 0): no screening of Phi's
  source. Label line: "NATURAL FORM DOES NOT SCREEN" if the identity holds. (b) The target observable is then graded
  as a necessary condition.
- **Target observable:** Phi_k = psi_N,k + chi_k, chi_k = (k^2 / (k^2 + m^2)) x (unscreened phantom potential)_k,
  m = 1/L2. On the web: SV5's fields with V_k = N_k + [k^2/(k^2 + m^2)] W_k (N = g_N, W = (nu - 1) g_N), same B,
  same projection.
- **Ladder (locates the bound, not a fit):** L2 in {infinity (KA), 30, 10, 3, 1, 0.3, 0.1, 0.03 Mpc, 0 (MUTATE)}.
  L_max = the largest listed L2 with r <= 1.072 on both footings. r(L2) is monotone in L2 (checked and printed).
- **Galaxy side at L_max (most generous admissible: largest range keeps most phantom):**
  - K-G6: each KiDS lens a point mass with the law's phantom density dM_ph/dr (WL1's dMph); chi's force at R summed
    over Yukawa shells (exact shell potential -(G dm L2 / (2 r s)) [e^{-|r-s|/L2} - e^{-(r+s)/L2}], force by
    differentiation), shells from 1e-3 R to R + 30 L2; g_cand = G M_b / R^2 + g_chi(R).
  - G1 SPARC: each galaxy spherical with M_b(<r) = vb2 r / G at its points (point mass beyond the last point), same
    shell sum; F = g_chi / g_ph at each point; graded with GB1's g_sparc.
  - G2-G7: screening can only lower the phantom force (F <= 1, checked on every SPARC and KiDS point); L0's
    residuals there are positive, so each L0 FAIL stays FAIL (lemma, printed with the max F). G8: F_SS = 1 to
    O((AU / L2)^2), equals L0 (PASS).
- **MUTATE:** L2 = 0 gives r = 1 exactly (web passes) and K-G6 at L2 = 0 must FAIL (Newtonian lenses); L2 = infinity
  gives K-G6 shift 0. Bites iff main K-G6 at L_max FAILs and the web ladder is not flat.

## 5. C3, two-branch balance (S-shaped h(x) = mu(x) x)

- **Sympy (statement):** for g = g(r) r_hat the linearised AQUAL flux d(mu(|g|/a0) g_i)/d g_j has eigenvalues h'(x)
  (radial) and h(x)/x (transverse). Any C^1 h with two stable branches over a common y window has an interval with
  h' < 0, where the static operator is not elliptic (radial only). Well-posedness row WP: FAIL on an open set of
  field values, the record's AC16 standard. Reported, not graded: Maxwell plateau, upper branch metastable.
- **Oracle (two values per y, most generous):** Delta_low(y) = 0 (the law); Delta_up(y) per y bin (y = g_N / a0),
  chosen on a grid 0.00-1.50 step 0.01 to minimise, over the hot-class points in the bin (X-COP sigma 0.10; groups
  their sigma_log, f* = 0 and 1 both counted; ellipticals 0.15; Coma UDGs sigma_U), the sum of
  min(res_low^2, res_up^2) / sigma^2. Every point of every class (and every KiDS point) then takes whichever branch
  gives the smaller |residual| (per point: the most favourable history).
- **Rows:** GB1 G1-G8 with that per-point Delta, K-G6, WP, web (lower branch = law: W = 74.7 / 89.4, and
  W >= r_pop since the phantom is never below the law's).
- **MUTATE:** M1, groups' D replaced by Delta_up at their y bin (0 where no bin value): G3 must then PASS on both
  f*; bites iff main G3 FAILs. M2, Newton: G1 FAIL.

## 6. Labels (per candidate, both footings)

- **SURVIVES (gates named):** every graded row PASS on both footings, including web and K-G6. It still owes field
  equations and well-posedness; never "passes all gates" (CMB shape PR4 chi^2 not run here).
- **FAIL (rows named):** any graded row FAIL on either footing.
- **NO VERDICT (bracket):** no FAIL but a row not computable; the bracket is stated.
- The lane label lists all three. A FAIL in C1 / C2 / C3 is a label on that key class or observable, not only on one
  member, where the oracle / bound construction above makes it so; the README says which.

Kappa = 1/2 FITTED; not theory closed.
