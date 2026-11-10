# AKD1 (dust stiffness keyed on the clock's acceleration): FROZEN CRITERIA, committed alone before any script, Lean file or graded number

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Both footings (canonical a0 9.3603e-11,
alt 1.1312e-10 m/s^2), graded separately, never pooled. The cold component is cold dark energy (the clock's dust and the
law's halo), a gravitating field component, never a particle. No LCDM-calibrated machinery enters a verdict. No download.
This lane writes only inside `closure_2026_11_10/AKD1_acceleration_keyed_dust/`; it reads TK1, MK1, KD1, QX17, SCS1,
FLD1, COL1 and never edits them. Lean files live here and compile with the in-repo build
(`cd fable_independent_2026/lean_2026 && lake env lean <absolute path>`).

**Id check.** The brief asked for AK1. AK1 is taken: `closure_2026_11_07/AK1_fold_release_layer/` and commits 5c882ed13e,
a6c9137af9 (the 11-07 fold-release lane). `find . -maxdepth 3 -name 'AKD1_*'` found nothing and
`git log --all --oneline --grep=AKD1` gave nothing. This lane is **AKD1**.

## 0. The question

MK1: no dust term in the clock offset Q - 1 alone is stiff in the expanding background (mu >= 2.512e4 per Mpc, the
CMB-lensing Jeans line) and nearly inert in a static galaxy well (mu <= 1.00 / 0.765 per Mpc, KiDS host-free capped).
TK1: keying the stiffness on the expansion theta fails at turnaround (theta = 0 while the clock still falls). The
candidate keys it on the clock's acceleration A_m = n^k nabla_k n_m = -D_m ln Q, which is zero for a freely falling clock
anywhere (background and turnaround) and equals the local field for a standing clock. Is the action well posed, and does
it keep MK1's rows?

## 1. The candidate (frozen, in this lane's words)

Notation as QX17 section 1 (c = 1 unless shown, K = 4 pi G, mostly-plus signature). Y := A_m A^m >= 0 (A is spacelike);
in unitary gauge (tau = t, Q = 1/N) A_i = d_i ln N and Y = gamma^{ij} d_i ln N d_j ln N. Action (A) with its dust term
mu_K^2 (Q-1)^2/(2K) replaced by

    L_K = M_2(Y) (Q-1)^2 / (2K),     M_2(Y) = mu_0^2 / (1 + Y/g_c^2)^p + M_f^2,

and nothing else changed (law sector P^m A_m - W(K|P|) - gamma_L F(Pi) + lambda n^m P_m, gravity, Lambda, minimally
coupled matter, all as in (A)).

- **Primary:** mu_0 = 3e4 per Mpc (physical; TK1's), p = 2, M_f = 1e-3 per Mpc. Then M_2(0) = mu_0^2 + M_f^2 and
  M_2'(0) = -p mu_0^2 / g_c^2.
- **The rule that fixes g_c (frozen here, before any number is graded).**
  - g_min := the action's law g (mu(x) = x/(1+x): g = g_N/2 + sqrt(g_N^2/4 + g_N a0), g_N = G M_b / r^2) at the edge of
    ONE1's middle KiDS window, the outermost window in the record's table (FLD1 RESULT, canonical table: 190 / 637 / 849 /
    1069 kpc at log M_b 9.4 / 10.45 / 10.7 / 10.9), minimised over the four masses. Per footing (its own a0; the window
    radii are the canonical table's on both footings, disclosed).
  - g_c := the largest value with sqrt(M_2(g_min^2)) <= mu_KiDS, mu_KiDS = MK1 row 6 = 1.00 / 0.765 per Mpc (canonical /
    alt). Closed form: g_c = g_min / sqrt( [mu_0^2 / (mu_KiDS^2 - M_f^2)]^(1/p) - 1 ).
  - Because M_2 decreases in Y and every SPARC and inner-KiDS acceleration exceeds g_min while their lines are higher
    (SPARC 7.08 / 5.62), this g_c also meets MK1's SPARC row and Saturn's line (6.2e3) in a static well. Groups and X-COP
    are not used to fix g_c.
  - The closure chat's hand value (about 3e-5 a0 at p = 2) is NOT used.
- **Brackets (reported, never label-setting):** p = 1; p = 4; floor off (M_f = 0). Each changed alone, with g_c re-fixed
  by the same rule.
- Background inputs as TK1 (`tk1_lib.py`, read not edited): H0 = 67.4 km/s/Mpc, I0 from KD1 (`kd1.json`) per footing,
  Omega_b = Omega_d / 5.41 equivalent via KD1's omega_b, Omega_r from KD1, Lambda the rest (flat).
- Lstar (law screening length, gamma_L = K Lstar^2/2): 21.7 / 22.9 pc (QX17, SCS1).

## 2. Hand estimate (written before any script; to be checked, not relied on)

1. **What the new term is at quadratic order around FRW.** A = 0 on FRW, so M_2 = M_2(0) there and the background is
   MK1's constant-mu background exactly. At quadratic order Y = (d delta-ln N)^2/a^2 and the new piece is
   F_Y Y with F_Y = M_2'(0) q0^2 / (2K) = -p mu_0^2 q0^2 / (2K g_c^2) < 0 (q0 = Qbar - 1 = I0 / (2 M_2(0) a^3)).
2. **Its sign.** delta-ln N is not a coordinate: in unitary gauge the lapse is auxiliary and the momentum constraint ties
   it to the curvature's velocity (alpha ~ zeta-dot / H); in the decoupling limit (tau = Q0 (t + pi)) delta ln Q =
   pi-dot, so Y = |grad pi-dot|^2. A negative F_Y is therefore a NEGATIVE contribution to the scalar's inertia, growing
   as k^2. The closure chat called it a healthy gradient term; on this reading that sign is wrong.
   Decoupling-limit inertia: I(k) = (1/2) F_QQ Q0^2 + F_Y,tot k_phys^2, F_QQ = M_2(0)/K.
3. **The law sector is the same kind of term with the healthy sign.** Eliminating P at gamma_L = 0 gives
   +J(|A|) = (a0^2/K)[u - ln(1+u)] = +Y/(2K) + O(Y^(3/2)) near A = 0 (QX17 K0). So the law contributes
   F_Y,law = +1/(2K) (unscreened; the screened branch Pi > 0 gives 1/(2K (1 + Lstar^2 k_phys^2/2))). The candidate's
   term is a negative copy of it with relative weight
       R(z) = p mu_0^2 q0(z)^2 / g_c^2  ( = p [K n / (mu_0 g_c)]^2 for M_f << mu_0 ).
   Total F_Y,tot = (1 - R)/(2K) unscreened. Ghost (I < 0) for k_phys^2 > M_2(0) Q0^2 / (R - 1) whenever R > 1.
   With the law held at P = 0 (TK1's convention), ghost for k_phys > 1/ell, ell = sqrt(2 p) q0 / (Q0 g_c) (M_f << mu_0), at every z.
4. **Numbers by hand** (g_c from the rule: g_min about 1e-12 m/s^2 = 1e-2 a0, g_c about g_min / 173 = 5.5e-15 m/s^2 =
   6e-5 a0 canonical; mu_0 q0 c^2 = 1.96e-18 (1+z)^3 m/s^2): R(0) about 3e-7, R(2) about 2e-4, R(10) about 0.5,
   R(1100) about 5e11, R(3400) about 4e14. R = 1 near z 11 to 12. So the hand estimate is **a ghost at z 3400 and
   1100 on every reading, covering every sub-horizon wavenumber** (threshold k_phys about mu_0 / sqrt(R): 23 Mpc
   physical at z 1100, far outside the horizon); healthy at z 10, 2, 0 on the unscreened law reading; ghost below about
   1e-2 pc at all z on the screened and P = 0 readings. **A1 fails.**
5. **Classical rates.** Where I < 0 and the gradient B = (1/2) F_Q Q0 > 0: rate^2 = B k^2 / |I| -> M_2(0) q0 Q0 / (R - 1)
   at high k (finite), and unbounded as k approaches the zero of I from above. At z 1100 the high-k rate is about 1e-6 H;
   it exceeds H only for 1 < R < about 2 (z about 11 to 15, scales <= 1/mu_0 = 33 pc), where the rate is unbounded near
   the threshold. So the ghost is classically slow early, but the zero of I sweeps every comoving mode and the rate is
   unbounded there: ill-posed, not only a quantum objection.
6. **Static wells (A4, A6 i) by hand.** Around a standing clock (Y = g^2, q about |Phi|/c^2) the same comparison holds for
   transverse perturbations: law's coefficient 1/(2K (1+u)) against the candidate's M_2'(g^2) q^2 / (2K). Weight
   W = |M_2'(g^2)| q^2 (1+u). For the primary W > 1 where g < about 5e-3 a0, i.e. in the KiDS outskirts, so the standing
   branch would be a ghost where the key turns. The candidate's polarization-like term dL_K/dA = 2 F_Y A = M_2' q^2 A / K
   points against the law's P (K P = A/(1+u)) with the same weight W, so where W > 1 the net phantom charge changes sign.
   Since g_c is pinned near g_min, any decreasing M_2 that falls from >= mu_J^2 to <= mu_KiDS^2 by g_min has
   |M_2'| >= (mu_J^2 - mu_KiDS^2)/g_min^2 somewhere, and with q about 2e-7 there W is about 1e9: the class, not just
   this shape, fails in the outskirts.
7. **Switching branches (A6 ii) by hand.** In dust Q - 1 = K n / M_2, so A = K |grad n| / mu_0^2 on the stiff branch;
   A > g_c needs |grad n| > mu_0^2 g_c / K: about 1e5 times today's mean clock charge over 3 kpc. Only at a fold.

## 3. Items, in order. Stop at the first structural failure (A1 or A3) and report it as the result

### A1 well-posedness (structural)

- **K1 covariant current (sympy, jets, 1+1).** Hand result to be checked: with F = L_K as a function of (Q, Y),
  delta S = Int sqrt(-g) J^m d_m delta-tau, EL: d_m(sqrt(-g) J^m) = 0 up to sign, with
      J^m = [F_Q + (2/Q) nabla_k(F_Y A^k)] n^m + (2/Q) F_Y (n^k d_k ln Q) A^m.
  So the charge along n is F_Q + (2/Q) nabla.(F_Y A) = M_2 (Q-1)/K + (2/Q) nabla.(F_Y A): the dust plus a
  polarization-like term P_K = 2 F_Y A. Checked against a direct Euler-Lagrange variation in 1+1 with metric
  -e^{2A(t,x)} dt^2 + e^{2B(t,x)} dx^2, F = (Q-1)^2 (m0 + m1 Y + m2 Y^2), 6 random jets, 40 digits: residual <= 1e-30.
- **K2 unitary-gauge content.** (a) L_K has no matter field. (b) In unitary gauge L_K is a function of N, d_i N and
  gamma_ij only: list every velocity it depends on (expected: none; no N-dot, no gamma-dot, no shift). Then matter and
  metric stay second order in time and the lapse obeys a constraint (Horava's healthy-extension class), checked
  symbolically, not assumed.
- **K3 order and principal part of the khronon equation.** Highest derivative of tau in the EL expression and its
  principal symbol, against the hand form sigma_4 = -(2/Q^2) (n.xi)^2 [F_Y h(xi,xi) + 2 F_YY (A.xi)^2] (ratio printed at
  random jets). Read: second order along n acting on a leaf-elliptic operator; no new characteristic cone; the inertia
  operator's sign is K4's question.
- **K4 scalar quadratic action around flat FRW (sympy, unitary gauge),** TK1's construction with F(Q, Y):
  gamma_ij = a^2 e^{2 zeta} delta_ij, N = N0 (1 + alpha), N_i = d_i psi, one Fourier mode; gravity + clock + Lambda;
  the law sector's quadratic piece enters as an extra F_Y,law Y (P eliminated at quadratic order around P = 0, where
  P^t = 0 and Pi is leafwise). alpha, psi eliminated; L2 = A_z zeta-dot^2 - grad(k) zeta^2. Three readings of the law:
  - R0: law held at P = 0 (TK1's convention): F_Y,law = 0;
  - R1: law on, unscreened branch (Pi < 0): F_Y,law = 1/(2K);
  - R2: law on, screened branch (Pi > 0): F_Y,law = 1/(2K (1 + Lstar^2 k_phys^2 / 2)).
  A real perturbation samples both branches, so the physical inertia is no larger than R1's: **R1 is the reading most
  favourable to the candidate and sets the label** (the monotonicity of A_z in F_Y is printed, not assumed).
- **Evaluation.** Primary background at z = 3400, 1100, 10, 2, 0 (the printed set), both footings, k_phys on a log grid
  from H(z)/c to 1 pc^-1 (galaxy scales and up; ghosts only above 1 pc^-1 are reported, never label-setting). Printed per
  z and reading: R(z), sign of A_z over the band, the threshold k where A_z = 0, c_s^2 = grad/A_z at high k, the
  classical rate sqrt(grad/|A_z|)/H at three k in the ghost band. Also a 140-point log grid in z for z_x (R = 1).
- **G-ratio (reported).** G_cosmo from the Friedmann equation at fixed charge (A = 0: rho_K is MK1's, no H dependence);
  G_N from the static weak field around Q = 1 (F_Y is proportional to q^2, so zero at linear order); and the Horava-like
  coefficient eta_eff(z) = 4 K F_Y,tot printed per reading.
- **Growth of delta (reported).** The K4 mode's growth rate / H at three k per z (above); baryon growth is not computed
  (disclosed).
- **A1 label:** WELL-POSED AROUND FRW iff K1 residual <= 1e-30, K2 shows no velocity in L_K, and on R1 at every printed z
  A_z > 0 and c_s^2 >= 0 for every k_phys in [H/c, 1 pc^-1]. Otherwise **NOT WELL-POSED AROUND FRW**, naming z and band.

### A2 FRW limit (closed form; reported if A1 fails)

w(z 3400) <= 0.01 (KD1 B1a) and mu_eff = sqrt(M_2(0)) >= mu_J = 2.512e4 per Mpc. Known answer: with p = 0 the
background is MK1's (mu_B1a 198.25 / 198.24 to 1e-4; w = w0/(w0 + a^3) residual 0).

### A3 turnaround (structural; graded only if A1 passes)

Homogeneous closed patch has A = 0, so it is A2's constant-M_2 patch: REGULAR iff the TK1 MU2 machinery reaches a_ta/2
at z_ta 5, 2, 1 (z_ta 0.5 reads as GR does). Patch edge: bound A at the edge by K |grad n| / mu_0^2 against g_c.

### A4 static wells (graded only if A1 and A3 pass; the closed-form weight W is computed and reported regardless)

W(r) := |M_2'(g^2)| q^2 (1 + u) with q = |Phi|/c^2 of the law's halo (Phi zero at infinity in the PD1-capped form,
i.e. the halo ends at PD1's cap and is point-mass outside; disclosed) at MK1's four masses from 10 kpc to the middle
KiDS window, per footing. Printed: the radius where W first exceeds 1 (if any) against the window edges. Saturn line:
mu_eff(g_Saturn) <= 6.2e3 per Mpc. The full modified static solve is run only if A1 and A3 pass.

### A5 MK1's rows re-read (graded only if A1 and A3 pass)

MK1's table at mu_eff = sqrt(M_2(g^2)) per row's acceleration; clusters expected to fail.

### A6 the two branches

(i) Standing-branch stability: the hand closed form of item 6 above, sign of the transverse inertia
law + candidate, reported with A4's W. (ii) Leaving the stiff branch: |grad n| needed for A = g_c, as an overdensity
over 3 kpc against today's mean clock charge, printed. Both closed form, reported regardless.

## 4. Labels (frozen)

Part A, per footing, first that applies:
1. **NO VERDICT** if any known answer below fails.
2. **BREAKS AT A1** if A1 reads NOT WELL-POSED AROUND FRW.
3. **BREAKS AT A3** if A3 reads SINGULAR or STALLS.
4. **BREAKS AT A4** if the static solve has no solution or W > 1 inside the middle KiDS window at any of the four masses
   (the standing branch is then a ghost where the law is observed).
5. Otherwise **WELL-POSED AND CONSISTENT WITH MK1'S ROWS EXCEPT CLUSTERS** if every A5 row except X-COP passes; else
   **ROWS FAIL**, naming them.

Part B (the collapse with M_2(Y) in COL1's solver): REACHES THE STANDING STATE / BREAKS DOWN / NO VERDICT, graded only if
Part A's label is 5. If Part A stops at 2-4, RESULT.md says Part B was not graded.

Counts against the candidate (listed whatever the label): a ghost on R1 at any printed z; c_s^2 < 0; any growth rate
above H on galaxy scales; W > 1 anywhere inside the KiDS windows; a bracket that fails where the primary does not;
a g_c rule that cannot be met.

## 5. Known answers (all must pass, else NO VERDICT)

- KA1: K1 residual <= 1e-30 (covariant current vs direct variation).
- KA2: p = 0 (F_Y = 0): K4's A_z equals TK1's closed form at F_th = F_Qth = F_thth = 0, A_z = F_QQ a^5 / (4 N0 a-dot^2)
  (residual 0), and c_s^2 = (Q-1)/Q at high k (TK1 KA5), relative 1e-6.
- KA3: background at M_2 constant: w = w0/(w0 + a^3) and mu_B1a = 198.25 / 198.24 (relative 1e-4).
- KA4: decoupling limit (Minkowski, tau = Q0 (t + pi), independent sympy code) gives inertia
  (1/2) F_QQ Q0^2 + F_Y k^2 and gradient (1/2) F_Q Q0; K4's A_z must be proportional to the decoupling inertia at fixed
  background, i.e. A_z(k)/A_z(0) = 1 + 2 F_Y k_phys^2 / (F_QQ Q0^2) exactly (residual 0).
- KA5: law-on flat limit: with F_Y,K = 0 and F_Y,law = m/2 (SCS1's K m), the decoupling dispersion with gravity's
  Jeans term reproduces SCS1's closed form omega^2 = K G [(1 - K m) k^2 - mu^2 Q^2] / (mu^2 Q^2 + K m k^2) at
  G = Q n (FRW, D.P = 0), hence TPA1 4.4 at K m = 1 (relative 1e-12 at three k).
- KA6: the law's g at FLD1's window edges from two routes (the closed form and a root solve of g_N = g^2/(g + a0)):
  relative 1e-12.

## 6. MUTATE (separate outputs; each must bite)

- MU1 (physics arm, sign of p flipped: p = -2, M_2 increasing): F_Y > 0, so the A1 verdict must change: A_z > 0 on R1 at
  every printed z (and on R0). Bites if the A1 reading flips.
- MU2 (physics arm, g_c x 100): R falls by 1e4; bites if the z 3400 threshold k moves by a factor >= 10 and z_x moves.
- MU3 (code): drop the F_Y term from K4's expansion: KA4's ratio must fail (A_z loses its k dependence).
- Lean: `AKD1.lean` (inertia closed form negative beyond the threshold when F_Y < 0; M_2'(0) for the primary; the R > 1
  ghost condition with the law; the g_c closed form meets the KiDS line with equality) compiles; `AKD1_MUTATE.lean`
  states one false version per theorem and must fail on every one.

## 7. Rules

Commits with explicit paths only; every message ends "Adopts nothing. kappa = 1/2 FITTED; not theory closed." Later
changes go in AMENDMENT_An.md, committed alone, marked post hoc if any graded number was seen. Compute light (sympy and
closed forms, one thread, nice 10). Push by cherry-picking onto a sparse temporary worktree of origin/main.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
