# TS1 (tidal-signature web-off switch, the outside source's variant M): FROZEN CRITERIA, committed alone before any TS1 script or number

TEST lane, quarantined; registered RUNNING at 6286c8a18c (owner "Yes, round 17"). Adopts nothing. kappa = 1/2 FITTED; not theory
closed. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10), never pooled. A FAIL is verified as hard as a PASS. Read-only
machinery: WM1 (wm1_local / wm1_cosmo / wm1_cmb / wm1_hc1 / wm1_seed, exec'd with in-process patches), SS1 / GB1 / QX8 loaders,
SS5 D1 (via WM1's solver, KA-W2-verified), HC1 G9, QX15, WL1 (numbers read). No file of another lane is edited.

## 1. The switch, frozen once

- **Field:** nu_eff(y, I) = 1 + (nu(y) - 1) s, with s = max(0, I/2), nu(y) = 1/2 + sqrt(1/4 + 1/y), y = |g_N| / a0.
- **Tidal signature:** I = -det(H) / ((1/6) Tr(H^2))^(3/2), with H_ij = d_i d_j Phi_N, the Newtonian potential of all matter
  (baryons + component).
- **s is not capped.** For a traceless H, |I| <= 2. With matter present, I reaches +2 sqrt 2, so s reaches sqrt 2 (see section 2).
- **Form choices beside the label:** the normalisation of I, the max(0, I/2) map, and (M-split) the 50/50 split and the factor-10
  mass ratio. Fitted: 0.

**Sub-variants**
- **M-W:** the switch plus WM1's relic, unchanged (188.7 eV, M_hm 4.97e12; each system holds S(M200) x SS1's primary halo).
- **M-split:** the switch plus 50 % at 188.7 eV and 50 % at 18.87 eV, each half with WM1's rule using its own M_hm (Viel half-mode
  at its own m).
  - CLASS: two ncdm species, each omega = omega_chi / 2.
  - Locally: M_chi(<r) = sum over halves of 0.5 S_i(M200) M_chi0 min(r, R200) / R200.
  - The source's asserted phase-space core is not modelled.
- **M-law:** the switch with the law alone, no component (control).

## 2. Closed forms used (known answers KA-T)

- **KA-T1:** point mass, I = +2 exactly. Eigenvalues GM/r^3 (-2, 1, 1).
- **KA-T2:** plane sheet, I = 0.
- **KA-T3:** line mass, I = 0.
- **KA-T4:** isotropic linear overdensity H = c 1 (c > 0), I = -2 sqrt 2 = -2.83. Switch off.
  - The orchestrator's stated -2/sqrt 3 is not what the definition gives; this lane records -2 sqrt 2 and discloses the difference.
  - Void centre (c < 0): I = +2 sqrt 2, s = sqrt 2.
- **KA-T5:** spherical systems. With u = g_N / r and x = rho / rho_bar(<r) = (1/3) dlnM_N / dlnr, H has eigenvalues
  ((3x - 2) u, u, u). So I(x) = -(3x - 2) / (((3x - 2)^2 + 2) / 6)^(3/2).
  - Vacuum, x = 0: I = 2, s = 1.
  - Isothermal, x = 1/3: I = 2 sqrt 2, s = sqrt 2 (the maximum).
  - Uniform core, x = 1: I = -2 sqrt 2, s = 0.
  - The switch turns off for x > 2/3.
- **KA-T6:** with s set to 1 everywhere, every local gate reproduces the law-only (L0) numbers of SS1 KA3 / WM1 to 1e-9.
- **KA-T7:** the Monte Carlo of the Gaussian Hessian (section 4, T6) reproduces <H11^2> / <H12^2> = 3 and <H11 H22> / <H12^2> = 1
  within 2 %.
- Every analytic value is checked numerically, from finite differences of the potential.

## 3. Gates (per sub-variant, per footing) and the label order

Order: **0, T1, 1, T3, 2, 3, T4, 6, 7a, 7b-N, 7b-L, 8, CS, 10.**

| # | gate | how | line |
|---|---|---|---|
| 0 | seeding | WM1 A2 (c830b470e0) with nu -> nu_eff_web (section 4); M-split transfers = the mean of the two species. M-law: reported (baryon-only seeds; the record's baryons-only controls) | sharp-k n(>1e10, 1e11) at z 2, 0 >= 0.5 x cold reference |
| T1 | SPARC, I inside the disc (first expected kill) | per point, per Upsilon node, in the mid-plane. Phi_R = g_N(R), Phi_RR = d g_N / dR (finite difference), Phi_phiphi = g_N / R, Phi_zz = 4 pi G rho_0 - Phi_RR - g_N / R (Poisson). rho_0 = Upsilon SBdisk / (2 h_z), h_z = 0.196 R_d^0.633 kpc (Bershady 2010). **Bulge and gas density are left out of rho_0:** this lowers rho_0 and pushes I toward the vacuum value, so it is generous to the switch. Through QX8's fit (Upsilon per galaxy, exact-field term Tf kept as is, disclosed) | record G5 line: rms <= L0 rms + 0.010, \|mean\| <= 0.05, same for the massive tail (Vflat >= 250) |
| T1-z | SPARC above the disc | at z = 2 h_z with rho = rho_0 sech^2(2) and the in-plane terms held | reported |
| 1 | KiDS, single lens | spherical s(x) from the lens's own M_N(r) (point baryons + component) | \|shift\| <= 0.05 at all 59 points |
| T3 | KiDS to the saddle | lens plus an equal-mass neighbour at D = 3.5 Mpc (saddle 1.75 Mpc); s averaged over directions at each r; the lens's own radial g_N | \|shift\| <= 0.05 at all 59 points |
| 2 | groups (Lovisari 20) | SS1 gate 2 with g = nu_eff(y, I(x)) g_N, x from np.gradient of ln M_N vs ln r over each group's points | >= 16 of 20 at f* = 0 and 1 |
| 3 | X-COP | SS1 gate 3 likewise; retained / M_dyn vs TR1 reported | SS1 lines |
| T4 | WL1 population phantom | outside the baryon body of an isolated host, s = 1 exactly (KA-T1, KA-T5 at x = 0), so the phantom WL1 counted inside R_ms is untouched except inside the body. Bound: q_pop(TS1) >= (1 - r_b / R_ms,low) x q_pop(WL1), using deep-MOND M_ph(<r) proportional to r, with r_b = 30 kpc and R_ms lower 0.92 / 0.96 Mpc (WL1). The source's "cosmic mean phantom vanishes" is graded by this | q_pop <= 0.0354 |
| 6 | BAO+SN | M-W: WM1's +0.058 carried (the switch does not touch the background). M-split: wm1_cosmo with two species | Delta chi^2 <= 4 |
| 7a | CMB primary | M-W: WM1's carried. M-split: wm1_cmb with two species. M-law: QX15's MB control (+172,848 / +166,612), carried | <= 4 PASS, > 4 blocks |
| 7b-N (T5) | CMB lensing at the cutoff | HC1 G9, 8 corners. M-split: two species, omega 2.705 omega_b each | worst <= 18.48 |
| 7b-L, 8, CS (T6) | web: lensing law-on, forest + fsigma8, S8 | wm1_cosmo with nu -> nu_eff_web = 1 + (nu - 1) <s>_w | WM1 lines |
| 10 | Cassini | outside the Sun, I = 2 and s = 1: the record's PASS carried; inside the Sun not used | record |
| T2 | voids | s at an isotropic void centre (sqrt 2); <s> over the delta < 0 half of the Gaussian ensemble | reported (the record has no void line) |
| T7 | covariance | statement (section 5) | reported |
| NOT RUN | Bullet (the DB1 child has the law built in), Ursa Major, Coma UDGs | reasons stated | |

**Label:** PASS iff every graded gate passes; otherwise FAIL, naming the first failing gate in the order above. Per sub-variant,
per footing.

## 4. T6: the linear web's effective switch

- **Ensemble:** Gaussian isotropic Hessians, 2e6 samples, covariance <H_ij H_kl> proportional to (d_ij d_kl + d_ik d_jl + d_il d_jk).
  I is scale-free, so the ensemble needs no amplitude.
- **Graded linear-response weight:** <s>_w = <s (Tr H)^2> / <(Tr H)^2>. Tr H is proportional to delta, so this is the
  coefficient a delta-mode sees in the linearised equation; gradients of s are neglected (disclosed).
- **Reported beside:** the volume mean <s>, the fraction with s > 0, <s> over delta > 0 and over delta < 0.
- nu_eff_web(k, z) = 1 + (nu(k, z) - 1) <s>_w enters WM1's D1 (A1's nu) for 7b-L, 8, CS and gate 0.
- **"Newtonian by construction"** is tested by <s>_w: it is Newtonian only if <s>_w = 0.

## 5. T7, covariance (stated, not computed)

The lane states whether I can be the argument of a healthy covariant action:
- I is a non-polynomial function of the second-derivative invariants e2, e3 of an auxiliary field (Phi_N);
- the Horndeski / DHOST classes and Galileon determinant structures carry only specific polynomial (antisymmetrised) combinations;
- max(0, .) is non-smooth.
The expected statement: no known healthy class carries it, so it is a phenomenological switch. The lane says so plainly or says
what would change that.

## 6. Hand estimates and expected kills (before any number)

- **T1 SPARC: expected FAIL.**
  - In a Milky-Way-like mid-plane, 4 pi G rho_0 is about 6.5 x v^2 / R^2. So the eigenvalues are about (6.5, -1, 1) v^2 / R^2,
    I about 0.3 and s about 0.16.
  - The law's boost is cut about 6x where rotation curves are measured, in HSB discs. LSB / gas-rich outer discs sit nearer s = 1.
- **Spherical gates.** Isothermal-like total profiles (x near 1/3) give s near sqrt 2, so the law is boosted by 1.4 in group and
  cluster outskirts, and cores (x > 2/3) switch off.
  - M-W X-COP, already over-filled in WM1, gets worse at large radii.
  - M-split's halved component may help X-COP's amount but not the core's switch-off.
- **KiDS:** single lens s = 1 (vacuum outside the body). With the neighbour, the off-axis tides change s modestly. Expected PASS
  (single), PASS or near (T3).
- **T4: expected FAIL x25-30.** The switch is exactly on around every isolated host.
- **T6:** for a Gaussian field, det(H) < 0 in about half of space (the trace-negative half preferentially). So <s>_w is about
  0.3-0.6, not 0. The web is not Newtonian, so 7b-L, 8 and CS stay FAIL at a reduced boost.
- **T5 M-split:** the 18.87 eV half is hot (k_hm about 0.02 h/Mpc). CMB lensing at 50 % hot is likely to FAIL (HC1 at 100 %:
  166-194).
- **Gate 0:** WM1's Newton reading already fails (0.010-0.07), and nu_eff_web lies between Newton and the law. Expected FAIL for
  M-W and M-split.
- **M-law:** the CMB primary fails (record MB).
- **Expected labels:** M-W FAIL at 0; M-split FAIL at 0; M-law FAIL at T1.

## 7. MUTATE

- **MT1, s = 0 everywhere (Newton):** SPARC must FAIL (power on T1).
- **MT2, h_z x 3** (thicker discs, lower rho_0): the T1 statistic must move (reported whether the label moves).
- **MT3, D = 7 Mpc for T3:** the T3 shift must move toward the single-lens value.
- **KA-T6** (s = 1) is the null.

## 8. Operational

- One thread, nice 10; RSS < 1 GB except CLASS (disclosed); small json / out.
- Explicit-path commits via a sparse temporary worktree, removed after. SS1's battery needs SS1_PJ1_DIR (a read-only extract of
  origin's PJ1 dir in scratch).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
