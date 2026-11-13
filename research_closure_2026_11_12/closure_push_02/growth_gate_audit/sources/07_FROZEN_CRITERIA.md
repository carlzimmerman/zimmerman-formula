# PIK1 frozen criteria: the two-variable dust term L_K(Q, Pi) = (mu_K^2 / 2K) (Q - 1)^2 S(Pi / Pi_c)

Committed alone, before any script or graded number of this lane. TEST lane, quarantined. Adopts nothing, relabels
nothing, registers nothing. Both footings (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2), never pooled. The cold
component is cold dark energy (the khronon's dust), never a particle. Not a LCDM lane. kappa = 1/2 FITTED.

## 0. The question

MK1 (`../MK1_one_dust_constant/RESULT.md`) concluded, of the quadratic K(Q) = mu_K^2 (Q - 1)^2: NO VALUE / NO VALUE,
and closed with a requirement only — "it cannot depend on the clock offset alone". DT1
(`../DT1_dust_term_design/DESIGN.md` section 2) then produced a trade-off that kills every **one-variable** dust term
n(x), x = Q - 1: cold-and-clustering at late times implies pooling in galaxy wells. DT1's proof assumes n = n(x).

This lane grades the two-variable term

    L_K(Q, Pi) = (mu_K^2 / (2K)) (Q - 1)^2 S(Pi / Pi_c),      Pi = D_m P^m,     S(0) = 1,

in action (A) as QX17 prints it (`closure_2026_11_06/QX17_covariant_field_equations/RESULT.md` §0), everything else
unchanged. Pi is already in the action (it carries the stiffness gamma_L F(Pi)); the new step is that the clock's dust
term reads it too. In the static weak field Pi = c^2 rho_halo, the **law's own halo (phantom) density** (§1 below), so
the term gates the dust on the local halo density: no halo, dust on; halo present, dust off.

The question: **does this "key" lift MK1's galaxy bound on mu_K while keeping mu_K at the CMB's 198 per Mpc or
2.51e4 per Mpc, and does it turn the dust ON in X-COP clusters, which MK1 found empty at every mu_K?**

## 1. Physics fixed before any number

- **Units and symbols as QX17**: c = 1 unless restored, K = 4 pi G, Q the clock rate, n_m = -d_m tau / Q,
  h_mn = g_mn + n_m n_n, l = ln Q, A_m = -h_m^n d_n l, D_m = h_m^n d_n, Pi = D_m P^m = (Q sqrt(-g))^{-1} d_m(Q sqrt(-g) P^m).
  The term's Q-derivative and Pi-derivative are written L_Q = dL_K/dQ (Pi fixed) and **G = dL_K/dPi** (Q fixed);
  for this term G = (mu_K^2 / 2K) (Q - 1)^2 S'(Pi/Pi_c) / Pi_c.
- **Static weak field, gamma_L = 0** (QX17 §3 row 2, MK1 §1): with S the 00 equation reads
  `div[mu(|grad Phi|/a0) grad Phi] + mu_K^2 S(Pi/Pi_c) Phi = 4 pi G rho_b`, Phi zero far away, so the dust is
  `delta rho_K = -mu_K^2 S(Pi/Pi_c) Phi / (4 pi G)` and it is a **source** of the law:
  `r^2 mu(g/a0) g = G [M_b(r) + M_K(r)]`, `M_K(r) = -(mu_K^2/G) Int_0^r S(Pi(r')/Pi_c) Phi(r') r'^2 dr'`.
  This is MK1's ACTION-EXACT form with S inserted. (Certified in row 0: the n.n energy density of the new term is
  exactly the quadratic's times S, and every extra stress it produces is proportional to h_mn, i.e. leafwise, so it
  does not touch the 00/Poisson equation. The QX2 ADDITIVE form `M_model = law(M_b) + M_K` is reported beside, never
  graded.)
- **What Pi is, physically.** In the static weak field QX17 §3 gives K P = (1 - mu) grad Phi, so
  `Pi = D_m P^m = div[(1 - mu) grad Phi] / K = c^2 rho_halo`, with rho_halo the law's phantom halo mass density
  (4 pi G rho_halo = div[(1 - mu) grad Phi]). Deep law: rho_halo = sqrt(M_b a0 / G) / (4 pi r^2) for a point M_b.
  **So the key gates on sqrt(M_b)/r^2, not on the potential.** For clusters and groups rho_halo is taken from the
  data: rho_halo(r) = (1/(4 pi r^2)) d(M_HSE - M_b)/dr.
- **Form B's cap** (ONE1's construction, PD1's share X = 59.486 / 59.503 M_b from
  `../ONE1_counted_once/one1.json`): the total charge C(r) = M_L(r) - M_b ends at r_c where C(r_c) = X M_b.
  The key does not change the cap; it changes what fills it.
- **The threshold is one number, Pi_c**, reported as `xi = Pi_c / (c^2 rho_d0)` with
  rho_d0 = I0 c^2 / (8 pi G) the cosmic mean dust mass density today (I0 from `KD1_unpinned_kq_dust/kd1.json`).
  Only **ratios** of Pi can matter (xi is a common scale), so the graded object is the ordering of u = Pi/Pi_c
  between rows, which is xi-independent.

## 2. Rows, gates and lines

| row | quantity | gate and line | source |
|---|---|---|---|
| 0 certified variation | the field equations of the new term; the current; the stress | sympy, exact, Euler-Lagrange against g^{mn}, tau (2nd order) and P_m, on random configurations. **C0: every derived equation matches the direct variation (max rel <= 1e-30). C1: the tau equation is still a total divergence, i.e. the charge is conserved. C2: the energy density n^m n^n T_mn = (mu_K^2/2K)(Q^2-1) S. C3: the new stress is proportional to h_mn only.** | QX17 K1-K3 method |
| 1 CMB and background (FRW) | MK1's row 1 | Pi = 0 in FRW (P = 0 by isotropy) and S(0) = 1, so L_K is exactly the quadratic there. **R1: this lane's w(a), w0 and mu_B1a equal MK1's / KD1's (rel <= 1e-6).** Line: KD1's B1a, w(z = 3400) <= 0.01 -> mu_K >= 198.25 / 198.24 | MK1 row 1, KD1, QX17 |
| 2 linear order about FRW | is the key visible? | **R2: the S'(0) Pi piece of the action at linear order about FRW.** Certified two ways: (i) the exact identity Int sqrt(-g) F(Q) Pi = -Int sqrt(-g) Q P^m d_m(F/Q) + boundary, with P^0 = 0 (the constraint n.P = 0 in unitary gauge) and F/Q spatially constant on the background; (ii) an explicit linearized FRW configuration evaluated in sympy. **R2 reports VISIBLE or INVISIBLE and, if invisible, the growth consequence.** Line: MK1's row 2 Jeans line mu_K >= 2.512e4 stands or falls with R2 | MK1 row 2, KD1 G9a, QX3 |
| 3 X-COP | interval passing G-X | QX2's builder (7 clusters, 35 points, 0.1-0.7 R500) copied in content; **G-X: \|mean Delta\| <= 0.05 and rms <= 0.10**, Delta = log10(M_HSE / M_model). Graded model ACTION-EXACT with S, Phi = the potential of the measured M_HSE, zero at 3 R200 (QX2's psi_profile). mu_K fixed at the CMB's 2.512e4; the scan is over xi and the S shape. **Reported: MK1's ADDITIVE form and the zero at 10 R200; the rms and mean at every (xi, S)** | QX2 iter 5, QX6, MK1 row 3 |
| 4 groups | interval passing the group gate | Lovisari 2015, 20 groups, R2500 and R500 (QX5's `groups()`); M_b = Mgas (1 + s), s in [0, 1]; **PASS iff the bracket of mean Delta overlaps [-0.05, 0.05]**. Phi = potential of a power-law M_HSE through the two points, zero at 3 R200 (QX2's fallback). mu_K at 2.512e4; scan over xi and S. Same reported forms as row 3 | QX5, MK1 row 4 |
| 5 SPARC | upper bound in the effective-dust reading | **R5: mu_K^2 f_S(r) <= mu_K,SPARC^2 for every r in [1, 30] kpc of a 1e9 - 1e11 M_sun galaxy**, f_S(r) = M_K(<r)/M_K^{S=1}(<r) on the dust-free law potential. mu_K,SPARC = 7.08 / 5.62 per Mpc (MK1's capped bound). Quality: a certified sufficient condition (the dust is a monotone source), not a re-run of QX8's exact-field grader | MK1 row 5, QX8 |
| 6 KiDS host-free, capped | upper bound in the effective-dust reading | **R6: mu_K^2 f_S(r) <= mu_K,KiDS^2 for every r in [1, 1000] kpc of a 1e10 - 1e12 M_sun galaxy**, on the dust-free **capped** potential integrated to r_c, plus the self-consistent capped solve at the reported points. mu_K,KiDS = 1.00 / 0.765 per Mpc (MK1's capped bound). Also reported: the old S4 bound (0.03-0.1 per Mpc) and the uncapped reading. Quality: as row 5; ONE1's statistic is not re-run | MK1 row 6, ONE1, S4 |
| 7 Solar System | upper bound | EW2 iter4's `cassini` closed form with the key: **mu_K^2 S(u_Sun) <= (6223)^2**, u_Sun from the Milky Way's halo density at 8 kpc (M_b 5e10 M_sun). dg <= 7.0e-15 m/s^2, Q2 <= 9.0e-27 s^-2 | MK1 row 7, EW2 iter4 |
| 8 consistency | reported, not graded | (a) **the constitutive-law correction**: the leaf part of (E2) with the key reads (1 + gamma_L Pi_+ - G) A_m + gamma_L D_m Pi_+ - D_m G = K W' Phat_m, so the law is rescaled by (1 - G) and shifted by D_m G. **Line: \|G\| <= 1e-3 and \|D_m G\| <= 1e-3 \|A_m\| wherever the law is measured (SPARC, X-COP, KiDS), else the row's law is no longer the record's law.** (b) the u = Pi/Pi_c range each row probes, and the ordering between rows | new; MK1 row 8 |

## 3. Label (per footing, frozen before any number)

- Rows 1 and 2 are lower bounds on mu_K (from FRW and from the linear order, where the key cannot act if R2 says
  INVISIBLE). Rows 3-7 are constraints on (mu_K, xi, S). The label is stated at the CMB value mu_K = 2.512e4 per Mpc
  (row 2's line) and, secondarily, at 198.25 per Mpc (row 1's line).
- **KEY OPENS A WINDOW [mu_K, xi, S]** if, at mu_K = 2.512e4, some (xi, S) with S(0) = 1 passes rows 3, 4, 5, 6, 7 and
  row 8(a) on that footing.
- **NO VALUE** if no (xi, S) does. The label names the rows that do not meet and the ordering that blocks them, and
  states the factor by which the binding pair misses.
- **CMB-ONLY** if rows 5, 6, 7 pass at 2.512e4 but rows 3 and 4 (clusters and groups) do not: the key lifts the galaxy
  bound and leaves the cluster gap open.
- **NO VERDICT** if any known answer in §4 fails, or if row 0's C0-C3 fail.

## 4. Known answers (all must pass, else NO VERDICT)

- KA1 (S = 1 reduces to MK1): with S set to the constant 1, this lane's X-COP mean at mu_K = 0.1 equals MK1's additive
  value +0.4644 / +0.4317 (|d| <= 1e-3) and its mean-zero mu_K equals 1.778 / 1.736 (|d| <= 0.01) on the ADDITIVE
  form; on the ACTION-EXACT form the mean-zero mu_K is 1.53 / 1.46 (|d| <= 0.01, MK1 row 3).
- KA2 (FRW = MK1): w(a) = w0/(w0 + a^3), w0 = I0/(4 mu_K^2); mu_B1a = 198.254 / 198.245 (rel <= 1e-6, KD1's KA).
- KA3 (the identity): Int sqrt(-g) F(Q) Pi = -Int sqrt(-g) Q P^m d_m(F/Q) checked numerically on a random configuration
  to the boundary term's own accuracy (rel <= 1e-30).
- KA4 (QX17's quadratic is recovered at S = 1 and at Pi = 0): this lane's (E2), (E3), (E4) with S -> 1 equal QX17 §2's
  term by term.
- KA5 (the halo density): for a point M_b in the deep law this lane's rho_halo(r) equals sqrt(M_b a0/G)/(4 pi r^2)
  (rel <= 1e-6 on 30-300 kpc at M_b = 1e11).
- KA6 (MK1's dust): with S = 1 this lane's M_K(<r) equals MK1's -mu_K^2 Int Phi r^2 dr / G (rel <= 1e-8).

## 5. MUTATE (separate output `pik1_MUTATE.out`; each must move a row or a check; any that does not is disclosed)

- **M-S1**: S set to the constant 1 (the key off). Rows 3-7 must return MK1's numbers.
- **M-SIGN**: S(u) = exp(+u) (increasing; the other sign). Must break rows 5, 6, 7 outright.
- **M-FLUX**: the sign of the new flux term in the conserved current flipped. Row 0's C0 must fail.
- **M-PIB**: Pi read as the **baryon** density c^2 rho_b instead of the halo density c^2 rho_halo. Must move rows 3 and 6.
- **M-NOCAP**: row 6 without form B's cap.

## 6. Lean

`fable_independent_2026/lean_2026/PIK1.lean` + `PIK1_MUTATE.lean`: the exact identity
Int sqrt(-g) F(Q) Pi = -Int sqrt(-g) Q P^m d_m(F/Q) + boundary (as the divergence identity for D_m P^m); P^0 = 0 from
n.P = 0 in unitary gauge; the energy density n.n T^Q = (mu_K^2/2K)(Q^2 - 1) S; rho_halo = sqrt(M_b a0/G)/(4 pi r^2) in
the deep law and its M_b^{1/2} / r^2 scaling; and the ordering lemma: at their own dust-dominant radii a cluster's
u exceeds a 1e11 galaxy's, so a monotone S gives the cluster a smaller f_S than the galaxy. The twin states the false
versions (F(Q) Pi is not a divergence, P^0 free, the energy density without S, rho_halo independent of M_b, the
cluster's u below the galaxy's) and must fail to compile.

## 7. Scope and rules

Statics and the FRW background; spherical symmetry except the KiDS projection. One new function S and one new
constant Pi_c; no other change to action (A). The collapse is not touched; the route from linear growth to the static
state is not computed (COL1's lane). Compute: one thread, under about 1.5 GB, preemptible; no downloads; data read in
place. Every file ends "kappa = 1/2 FITTED; not theory closed. Adopts nothing."

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
