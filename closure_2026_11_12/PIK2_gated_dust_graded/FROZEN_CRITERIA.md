# PIK2 frozen criteria: the gated dust term L_K(Q, Pi) = (mu_K^2 / 2K) (Q - 1)^2 S(Pi / Pi_c), computed and graded blind

Committed alone, before any script of this lane exists and before any number of this lane is computed. TEST lane:
adopts nothing, relabels nothing (PIK1's committed label is not touched), registers nothing. Both footings
(canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2), every graded row on both, never pooled. The component is cold
dark energy (the clock's dust), never a particle. kappa = 1/2 FITTED; nothing here derives it.

## READING (what was read before this file was written, and what was not)

Read: the six memory notes named in the brief (cold-fluid name, path-limited commits, verify in SI, shape not one
amplitude, pgrep self-match, preemptible compute). PIK1's `FROZEN_CRITERIA.md` (committed version). MK1's committed
`FROZEN_CRITERIA.md`, `RESULT.md`, `mk1_rows.py`, the first 150 lines of `mk1_lib.py`, and `mk1_grade.json`. KD1's
committed `RESULT.md` and the setting / B1 block of `kd1.json`. QX17's committed `RESULT.md` (action (A), (E1)-(E4),
reductions). QX2's `qx2.py` (builder, `law_M`, `gate`, `psi_profile`, iteration 5). QX5's `groups()`. The share X from
ONE1's `one1.json`. Not yet opened: ONE1, DT1 and SWT1 texts (DT1's one-variable trade-off and SWT1's closed switch class
are known to me only through PIK1's criteria and the brief).

Pinned commit: on the coordinator's instruction every committed file is read at 7172d3dd4f. Six files were first read
at HEAD 1ba6f9a900 (PIK1 criteria, MK1 criteria, MK1 result, mk1_rows.py, KD1 result, QX17 result); their blob ids at
1ba6f9a900 and at 7172d3dd4f are identical (checked with `git rev-parse`, no diff shown), so nothing read differs from
the pinned version.

Not opened (blindness): PIK1's `RESULT.md`, its scripts, any `CORRECTION_2026_11_12.md`, `research_closure_2026_11_12/`,
`reviews/codex_corrections_audit_2026_11_12/`, the PIK1 passages of `fable52_push/CLOSURE.md` and `README.md`, the
PAPER72 files, and any `git log -p` / `git diff` of them.

Seen by accident or through the brief (disclosed): (1) the brief itself states three claims of another session: an
early-history requirement mu_K >= 8.89e6 per Mpc for a gated construction, a galaxy pressure ceiling mu_K <= about 450
per Mpc, and "an instability of the flat-gate family", and says PIK1's linear-invisibility argument is disputed.
(2) Commit subject lines only (no bodies, no diffs): the session context and one `git log --oneline -5` showed the
subjects of 1ba6f9a900 (Codex corrections audit README: lists slice C2 as "PIK1 and FRM1" and "nine things that should
change"), 7e7709fa62 (audit C3, kappa lanes; not PIK1), and a0faab06a9 (PAPER72 v1.2 draft revision 2: "replaces the
six pending markers ... (MK1's 2.51e4 per Mpc line, PIK1, ...) with sentences quoting the committed audit"). None states
a PIK1 number, label or argument. (3) The `git status` snapshot lists, as file names only, modified files under
`fable52_push/PIK1_pi_gated_dust/` (RESULT.md, pik1.py, pik1_var.py) and the MK1 / KD1 result files. No content seen.

## 0. The question

Does the gate S on the law's own halo density let one dust constant mu_K at the CMB's value (2.512e4 per Mpc, KD1 G9a
on QX3) survive the galaxy rows (SPARC, KiDS, Solar System), and does it put the right amount of dust, with the right
radial shape, into X-COP clusters and groups? And: is the gate invisible about FRW at linear order, as PIK1 asserted?

## 1. Physics fixed before any number

- **Action.** Action (A) of QX17 with mu_K^2 (Q - 1)^2 / (2K) replaced by L_K = F(Q) S(Pi / Pi_c), F(Q) =
  mu_K^2 (Q - 1)^2 / (2K), S(0) = 1; everything else unchanged. Pi = D_m P^m = (Q sqrt(-g))^-1 d_m (Q sqrt(-g) P^m).
- **Unitary gauge** (tau = t): Q = 1/N, Q sqrt(-g) = sqrt(gamma), P^0 = 0 (from n.P = 0), so
  sqrt(-g) L_K = sqrt(gamma) (F(Q)/Q) S(Pi/Pi_c) with Pi = gamma^(-1/2) d_i (sqrt(gamma) P^i). The gate term depends on
  the lapse only through Q, on the spatial metric only through sqrt(gamma), not on the shift, and has no time derivative.
- **Threshold.** xi = Pi_c / (c^2 rho_d0), rho_d0 = I0 c^2 / (8 pi G) from kd1.json per footing. u = Pi / Pi_c.
- **Static weak field (hand derivation, certified in row 0b).** Lapse N = 1 + Phi/c^2, gamma_L = 0 in rows 3-7.
  - Lapse equation: the gate term's energy density is exactly S x the quadratic's, (mu_K^2/2K)(Q^2 - 1) S, so
    div[mu(|grad Phi_eff|/a0) grad Phi_eff] + mu_K^2 S(u) Phi = 4 pi G rho_b (leading order), the dust being
    rho_K = -mu_K^2 S(u) Phi / (4 pi G), a source of the law: r^2 mu(g/a0) g = G (M_b + M_K),
    M_K(r) = (mu_K^2 / G) Int_0^r S(u) |Phi| r'^2 dr' (Phi < 0).
  - P equation: the law acts on Phi_eff = Phi - c^2 Gm, Gm = dL_K/dPi = F(Q) S'(u) / Pi_c. In SI,
    c^2 Gm = mu_K^2 Phi^2 S'(u) / (8 pi G rho_c), rho_c = xi rho_d0.
  - u = rho_halo / rho_c, rho_halo = the law's phantom density = div[(1 - mu) grad Phi] / (4 pi G).
- **Graded static reading ("dust on the law's own halo").** In rows 3-7 the dust is computed on a fixed potential
  (the row's own, below) with u taken from the **dust-free law phantom of the baryons**, rho_halo = (4 pi r^2)^-1
  d[law(M_b)(r) - M_b(r)]/dr, and Phi_eff = Phi (the law not modified by Gm). Both simplifications are checked in
  row 8(a) and, for any passing (S, xi), by a self-consistent re-run (phantom recomputed from law(M_b + M_K) - M_b - M_K,
  five iterations), which must also pass (check K-SC). Where the phantom density is negative, S is evaluated at u = 0
  (gate fully on); the count of such points is reported.
- **What is out of scope (stated plainly).** The full covariant stress tensor of the gated term, the covariant khronon
  equation, and the collapse. Row 0 certifies the gate term in the two settings the rows use, not the full field
  equations. No Lean in this lane (departure from PIK1 section 6: time; the certification is sympy, exact).

## 2. Gate family (frozen)

Decreasing, not flat at the origin: E1 = exp(-u); P1 = (1+u)^-1; P2 = (1+u)^-2; P4 = (1+u)^-4.
Flat at the origin: F2 = exp(-u^2); F3 = exp(-u^3); R3 = 1/(1+u^3).
Sharp step: ST = 1 for u < 1, 0 for u >= 1.
Reported, not graded for the label (a designed switch; the record's switch class is closed, SWT1): BAND = 1 (u < 1),
0 (1 <= u < 3), 10^-b (3 <= u < 30), 0 (u >= 30), b = 0..12 in steps of 1.
For Taylor use at u = 0: (s1, s2) = S'(0), S''(0): E1 (-1, 1), P1 (-1, 2), P2 (-2, 6), P4 (-4, 20), F2 (0, -2), F3 (0, 0),
R3 (0, 0), ST (0, 0 away from the step). Negative u (FRW perturbations) uses the analytic formula (rows 2 only need s1, s2).

Threshold grid: log10 xi = -2.00 to 12.00 in steps of 0.05 (281 values). mu_K values: **2.512e4 per Mpc (primary, KD1 G9a
Jeans line as recorded)**, 198.25 / 198.24 (secondary, KD1 B1a), 8.89e6 (reported: KD1's BBN line, a background line
the gate cannot touch because Pi = 0 on FRW).

## 3. Rows, gates and lines

| row | quantity | line | source / note |
|---|---|---|---|
| 0a | second-order gate action about FRW, unitary gauge, 3 space dims, general S | **C0a: sympy expansion of sqrt(gamma)(F/Q)[S(Pi/Pi_c) - 1] to O(eps^2), integrated exactly over a 3-torus on trigonometric lapse, metric and P^i perturbations with S = 1 + s1 u + s2 u^2/2 + s3 u^3/6 symbolic, equals my hand form** `Int a^3 [ -(s1/Pi_c) (F/Q)'(Qbar) P^i d_i dQ + (s2 / 2 Pi_c^2) (Fbar/Qbar) (d_i P^i)^2 ]` **(difference identically 0), and s3 drops out.** C0a' (KA3): Int sqrt(-g) F Pi = -Int sqrt(gamma) P^i d_i(F/Q) on the torus, difference 0 | new |
| 0b | static weak-field equations with the gate | **C0b: sympy `euler_equations` of the static Lagrangian (lapse N = 1 + Phi, generic F, S, W, P in 3D) give, for the gate's part, the lapse equation d[N F(1/N)]/dN S and the P equation -grad[N F(1/N) S'/Pi_c] exactly as my hand derivation (residual 0); C2: energy density -d[N F(1/N)]/dN = (mu^2/2K)(Q^2 - 1) (exact); C3: Pi does not depend on N at fixed P^i (exact)** | QX17 method |
| 1 | FRW background | Pi = 0 and S(0) = 1, so w(a) and every background line are MK1's / KD1's. KA2 below | KD1 B1a, B1b |
| 2 | linear visibility and health about FRW | (i) **VISIBLE** iff (s1, s2) != (0, 0), from C0a. (ii) **Sub-horizon Newtonian reduction** (hand, certified by a sympy elimination): with W ~ K P^2/2 (valid while \|A\| << a0, checked), integrating out P and Phi gives a charge equation `ddot delta + 2H dot delta = K rhobar_m delta - K rhobar_d k^2 delta / M(k)`, `M = mu^2 + beta k^2`, `beta = (1 + e1)^2 / (1 - e2 k^2 / K)`, `e1 = s1 rhobar_d/(Qbar^2 rho_c)`, `e2 = s2 Fbar/(Qbar Pi_c^2) - gamma_L theta(Pi)`, k physical, gamma_L = K Lstar^2/2 (Lstar 21.7 / 22.9 pc), theta = 1 on the Pi > 0 branch, 0 on Pi < 0. **Health H2: K_P(k) = 1 - e2 k^2/K > 0 and M(k) > 0 for every physical k in [1e-4, 1e6] per Mpc and every z in [0, 3400], on both Pi branches.** (iii) **Growth-factor criterion (in place of a CMB-lensing likelihood, which this lane cannot run): G2: \|D_gate/D_ungated - 1\| <= 0.01 at comoving k = 0.01, 0.05, 0.2 h/Mpc, integrated from z 3400 to 0** in the same reduction (ungated = S = 1 with P, i.e. beta = 1). Row 2 PASSES for a (S, xi, mu) iff H2 and G2 pass. Reported: the z and k ranges where H2 fails; KA4 | new; QX3, KD1 |
| 3 | X-COP | QX2's builder (7 clusters, 35 points, 0.1-0.7 R500); **G-X: \|mean Delta\| <= 0.05 and rms <= 0.10**, Delta = log10(M_HSE / law(M_b + M_K)), Phi = QX2's psi_profile (zero at 3 R200); M_b(r) log-log interpolated through each cluster's 5 points, power-law extended inside 0.1 R500 with the first two points' slope; integrals from 1 kpc. Reported: min rms over xi per gate and its xi; the ADDITIVE form | QX2, MK1 row 3 |
| 4 | groups | Lovisari 20 groups at R2500 and R500 (QX5's `groups()`); M_b = Mgas(1 + s), s in {0, 1}, power law through the two radii; Phi = potential of the M_HSE power law, zero at 3 x 1.5 R500 (MK1's construction); **PASS iff the bracket of mean Delta over s overlaps [-0.05, 0.05]** | QX5, MK1 row 4 |
| 5 | SPARC (proxy) | point baryon masses M_b = 1e9, 1e10, 1e11 Msun on the dust-free **capped** law potential (MK1 lib, m = 0, X = PD1's share): **R5: M_K^gate(<r; mu) <= M_K^{S=1}(<r; mu_SPARC) at every r in [1, 30] kpc and every M_b**, mu_SPARC = 7.08 / 5.62 (MK1). Quality: a proxy; it holds as a sufficient condition only if MK1's SPARC grade is monotone in the enclosed dust at every radius | MK1 row 5 |
| 6 | KiDS (proxy) | as row 5 for M_b = 1e10, 1e11, 1e12 Msun, r in [1, min(1000 kpc, r_c)], capped potential, **R6: same inequality with mu_KiDS = 1.00 / 0.765** (MK1). Reported: the uncapped reading (law with no end, S4's zero point, to 1000 kpc) | MK1 row 6, ONE1 |
| 7 | Solar System | **mu^2 S(u_Sun) <= mu_7^2**, mu_7 from EW2 iter4's cassini (Saturn 7.0e-15 m/s^2, Q2 9e-27 s^-2, Phi0 = (600 km/s)^2); u_Sun from the law phantom of a 5e10 Msun point at 8 kpc | MK1 row 7 |
| 8a | law back-reaction | **\|c^2 Gm / Phi\| <= 0.02 and \|d(c^2 Gm)/dr\| / \|dPhi/dr\| <= 0.02** at every graded radius of rows 3, 5, 6 (X-COP points; 1-30 kpc; 1 kpc-r_c). Departure from PIK1's 1e-3: 0.02 is below every graded line (0.05 dex = 12 %) yet keeps the row's law the record's law to 2 % | PIK1 row 8a |
| 8b | health on static backgrounds (fixed metric, gravity not coupled, local high-k) | **K_P > 0 at every k: gamma_L - F(Q_bg) S''(u_bg)/Pi_c^2 >= 0, i.e. S''(u) (rho_K1/rho_c)^2 <= (mu Lstar)^2** with rho_K1 = mu^2 \|Phi\|/(4 pi G), at every graded radius of rows 3, 5, 6 (galaxy and cluster backgrounds; Pi > 0 there). Where it fails the khronon's kinetic coefficient F'' S + (F' S'/Pi_c)^2 k^2 / K_P(k) passes through a pole and turns negative above k_* = (K / (F S''/Pi_c^2 - gamma_L))^(1/2); k_* r reported. The step's S'' is a delta function: 8b is evaluated away from u = 1 and the surface is reported | new |

## 4. Labels (per footing, frozen)

At mu_K = 2.512e4 (primary), and separately reported at 198.25 and 8.89e6:
- **KEY OPENS A WINDOW [mu_K, xi, S] (hit; awaits an independent re-grade)** if some graded S (not BAND) and xi on the
  grid pass rows 2, 3, 4, 5, 6, 7, 8a, 8b and K-SC on that footing. The label line says "awaits an independent re-grade".
- **CMB-ONLY** if some (S, xi) passes rows 2, 5, 6, 7 and 8 at the galaxy radii, but none also passes rows 3 and 4.
- **NO VALUE** otherwise. The label names, per gate, the rows that never pass together and the closest miss.
  Departure from PIK1: row 8 (health and back-reaction) and row 2 (health and growth) enter the label; a (S, xi) that
  passes rows 3-7 but fails row 8 is NO VALUE, and the reason is stated.
- **NO VERDICT** if a known answer fails, or C0a / C0b / C2 / C3 fail.
Row 2's VISIBLE / INVISIBLE word is reported per gate whatever the label. If row 2 says VISIBLE, the 2.512e4 line is the
record's ungated line and is not certified for that gate; the label line says so.

## 5. Known answers (all must pass, else NO VERDICT)

- KA1 (S = 1 reduces to MK1, X-COP): ADDITIVE mean at mu 0.1 = +0.4644 / +0.4317 (\|d\| <= 1e-3), mean-zero mu
  1.778 / 1.736 (\|d\| <= 0.01); ACTION-EXACT mean-zero mu 1.53 / 1.46 (\|d\| <= 0.01).
- KA2 (FRW): mu_B1a = 198.254 / 198.245 from w(z 3400) = 0.01 (rel <= 1e-6).
- KA3: the identity of C0a' (exact).
- KA4: the Newtonian reduction with the P sector removed returns the n = 1 polytrope: omega^2 = K rhobar (k^2/mu^2 - 1)
  (exact, sympy); with P and S = 1, beta = 1 (exact).
- KA5 (phantom): the lane's finite-difference phantom density of a point mass equals the closed form
  M_b x / sqrt(1/4 + x^2) / (4 pi r_M^3 x^2) (rel <= 1e-4 on 1-300 kpc at 1e11 Msun), and tends to the deep form
  sqrt(M_b a0 / G)/(4 pi r^2) at x = 1e3 (rel <= 1e-6).
- KA6 (S = 1 dust): the lane's X-COP M_K(<r) at S = 1 equals MK1's MKc construction at mu 1 (rel <= 1e-8).
- KA7 (groups at mu 0): [+0.196, +0.359] / [+0.158, +0.320] (\|d\| <= 2e-3).
- KA8 (EW2): dg(Saturn) at 2.04e4 = 7.5e-14 (rel 2 %); mu_7 = 6223 (MK1).
- KA9 (units, SI): rho_d0 and c^2 Gm recomputed independently in SI from G, c, H0, Omega_d agree with the scripts'
  values (rel <= 1e-6).

## 6. MUTATE (separate `*_MUTATE*` outputs; each must move a row or a check; one that does not is disclosed)

- M-S1: S = 1 everywhere (key off): rows 5, 6, 7 must FAIL at 2.512e4 for every xi.
- M-SIGN: S = exp(+u): rows 5, 6, 7 must FAIL at every xi.
- M-PIB: u read as the baryon density rho_b / rho_c instead of the phantom: must change row 3's or row 6's pass set or
  closest miss.
- M-NOCAP: rows 5 and 6 on the uncapped potential: must change a pass set or the worst ratio.
- M-ID: C0a with sqrt(gamma) dropped from Pi: C0a must FAIL.
- M-S2: the sign of the s2 term flipped in row 2: H2 must change for E1 and F2.

## 7. Expectations (stated before any number)

- Row 2: VISIBLE for E1, P1, P2, P4, F2; INVISIBLE at linear order for F3, R3 and ST. I expect e1 and e2 to be huge at
  the CMB epoch for any xi the static rows can use (rhobar_d / rho_c = (1+z)^3 / xi), and the s2 > 0 gates (E1, P1-P4)
  to fail H2 (M < 0 above a wavenumber that is tiny at z ~ 1000); F2 to pass H2; growth on CMB scales to move little where
  H2 holds, because k << mu there.
- Rows 3-7: at mu 2.512e4 the ungated dust in a cluster is of order 1e-16 kg/m^3 against the 1e-24 needed, so the gate
  must sit near 1e-8 to 1e-9 in clusters while varying smoothly across 0.1-0.7 R500. I expect every graded gate to fail
  X-COP's shape (rms) or, where it passes rows 3-4, to fail row 8b by many orders of magnitude, because S'' (rho_K1/rho_c)^2
  is about (S''/S) u (rho_K1 / rho_c) ~ 1e10 there. Expected label NO VALUE / NO VALUE.

## 8. Rules

Light compute (nice 19, one thread, each job under ten minutes); no downloads; data read in place; paths relative to the
script; no home paths. Inputs copied in content (MK1 lib, QX2 builder, QX5 groups) and cited. Commits path-limited.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
