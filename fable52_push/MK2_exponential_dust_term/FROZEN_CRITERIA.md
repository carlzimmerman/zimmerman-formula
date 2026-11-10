# MK2 frozen criteria: the exponential dust term L_K(Q) = (n_* x_T / K) exp((Q - 1)/x_T) against MK1's rows (2026-11-10)

Committed alone, before any script or graded number of this lane. TEST lane, quarantined. Adopts nothing, relabels
nothing, registers nothing. Both footings (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2), never pooled. The cold
component is cold dark energy (the khronon's dust), never a particle. Not a LCDM lane. The candidate comes from DT1's
design note (`fable52_push/DT1_dust_term_design/DESIGN.md`, origin 136f7cc8c2, read only after MK1 was pushed); every
number in that note is treated as a claim to test. The DT1 folder is not touched.

## 0. The question

With L_K(Q) = (n_* x_T / K) exp((Q - 1)/x_T) in place of mu_K^2 (Q - 1)^2/(2K) in action (A), so that
n(x) = K L_K'(1 + x) = n_* exp(x / x_T), x = Q - 1, with one constant c_s = c sqrt(x_T): is there a value of c_s that
MK1's rows allow, and which rows can no longer be carried at all?

## 1. What a general L_K(Q) changes (derived from QX17's equations before any number)

Replace mu_K^2 (Q-1)^2/(2K) in (A) by a general L_K(Q). Then, by the same variations as QX17:
- **Clock charge (E3):** rho_Q = J_P/Q + L_K'(Q). The dust part is n_d = L_K'(Q); n(x) = K n_d. The record's N = n_d + D.P
  keeps its form.
- **Stress (E4):** T^Q_mn = g_mn L_K + Q L_K'(Q) n_m n_n. So rho_K = Q L_K' - L_K and p_K = L_K
  (quadratic: rho_K = mu_K^2 (Q^2 - 1)/(2K), QX17 K5).
- **FRW row:** a^3 L_K'(Qbar) = const, i.e. n(xbar(a)) = n0 / a^3; w = L_K / (Q L_K' - L_K).
  - Exponential: w = x_T / (1 + xbar - x_T), so w = x_T to O(x). No stiff a^-6 partner.
  - Quadratic: w = w0/(w0 + a^3), KD1's stiff phase.
- **Sound speed and Jeans scale:** c_s^2 = L_K'/(Q L_K'') = n/(Q n'). The Jeans wavenumber is k_J^2 = Q n'(xbar), which
  is n' to O(x), physical.
  - Exponential: k_J^2 = n/x_T, proportional to the density.
  - Quadratic: k_J = mu_K at every density.
- **Static row:** a static clock has Q = Q_inf/N, so x = xbar_inf + phi, phi = |Phi|/c^2 (to first order in Phi). The
  static equation becomes div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho_b + c^2 [n(xbar_inf + phi) - n(xbar_inf)].
  - Exponential: the dust is isothermal, rho_d = rho_bar_d exp(|Phi|/c_s^2) with c_s^2 = x_T c^2, a source of the law
    (the law boosts it, as in MK1's action-exact form).
  - Quadratic: -mu_K^2 Phi.
- **SCS1's dispersion relation:** in its second-order Lagrangian, mu_K^2 enters only as K L_K''(Qbar). So locally (WKB)
  omega^2 = K G [(1 - K m) k^2 - n'(x)] / (n'(x) + K m k^2), with G = n(x)/K + D.P. The dust adds a growing band
  k < sqrt(n'(x)) / sqrt(1 - K m), the local Jeans band.
- **Record results that assumed the quadratic and do not carry:**
  - w0 = I0/(4 mu_K^2) and the stiff phase (QX17's FRW row, FB1, KD1 B1b).
  - k_J = mu_K at every density: QX3's n = 1 polytrope, KD1 G9a's line written as mu_K >= 2.5e4, and QX3 G3's capture
    bound mu_K <= 79.
  - The static dust linear in Phi, with S4's Helmholtz oscillation and negative dust: S4, QX2 iteration 5, QX6, KQ1 and
    MK1 rows 3-8.
  - KD1's P1 ("the static term does not depend on the amplitude"): the exponential's static dust is proportional to
    today's mean cold density.
  - MK1's A1 branch, with its asymptote mu_K r_c -> 1.55.
  - SCS1's mu* bracket.

## 2. The trade-off (DT1 section 2), stated and to be certified

Let n be absolutely continuous and non-decreasing. Let the background pass from n_a = n(x_a) to n_b = n(x_b) with
n_a < n_b. Suppose n' >= k^2 on [x_a, x_b] ("cold on physical scale k" during that stretch). Then:

    x_b - x_a <= (n_b - n_a)/k^2 ;

and any static well of depth phi with xbar_0 + phi >= x_b holds n >= n_b. In particular every well with
phi >= (x_a - xbar_0) + (n_b - n_a)/k^2 does. Here xbar_0 is today's background offset, and the static clock is
matched to it.

Conditions, stated before checking:
- n non-decreasing (health: c_s^2 = n/(Q n') >= 0).
- Weak field (phi << 1).
- The static clock matched to today's background.

Lean (`MK2.lean`) certifies the two steps:
- `width_le`: k^2 (x_b - x_a) <= n_b - n_a, from k^2 <= n' (Mathlib's mean-value bound).
- `well_floods`: monotonicity.

A numeric check on the exponential and the quadratic compares both sides. Reported: DT1's derived claim ("slope at
most 0.14 per Mpc^2, a Jeans length of at least 17 Mpc for z < 2"), stated as what the theorem actually implies. The
theorem gives an average-slope bound over [xbar_0, x_a], so it guarantees a Jeans length at least that long at SOME
epoch of the stretch, not at every one.

## 3. Rows, gates and lines (each from the lane named; c_s in km/s; both footings)

Common grid: c_s from 10 to 1e4 km/s, step 0.025 dex (121 values), unless a row says otherwise. Today's mean cold
density is rho_bar_d = 3 H0^2 Omega_d/(8 pi G) from kd1.json's I0 per footing (KD1, from QX15's omega_d, h 0.674).

| row | quantity | gate and line | source |
|---|---|---|---|
| a CMB and background | interval | (a1) **KD1 B1a**: w(z 3400) <= 0.01 with w = x_T/(1 + xbar - x_T). (a2) If its two known answers pass, **the record's primary-CMB likelihood** as F1A graded it (CAMB 1.6.6, lmax 7000, F1A's own P-ACT likelihood `PA`, nuisances profiled), taken at F1A's B2 cold best fit per footing. The cold component is replaced by a constant (w, c_s^2) = (x_T, x_T) fluid, carried with Lambda in CAMB's tabulated-w dark-energy fluid (the PJ1 / WD1 construction; the combined fluid's perturbation equations equal the cold fluid's because Lambda has no perturbations). Its unlensed spectra are lensed by the cold reference's lensing potential (camb.correlations, PJ1's construction). Late-time lensing is item 4 and is not graded. Line: **Delta chi^2_PA <= 10** against the cold reference (WD1 G7's line). It is graded before refit. At the first failing grid value a 5-parameter refit (ob, od, lnA, ns, tau; F1A's footing_h) is run; if the refit passes, the scan continues upward with refits. Grid for (a2): 30, 100, 300, 1000, 3000, 1e4, 3e4 km/s, then two log-midpoints between the last pass and the first fail. Reported beside: KD1 B1b (BBN; no stiff phase). | KD1; F1A; PJ1; WD1 |
| b clustering scale | per line: interval or NOT CARRIED | Each line MK1's row 2 used (KD1 G9a / QX3 G2, the CMB-lensing Jeans line; the growth stand-in; the forest stand-in): state what it presupposes. A line that presupposes the dust builds late-time structure (so that galaxies need clumped dust of their own) is NOT CARRIED and moves to item 4. Reported: the comoving Jeans wavenumber sqrt(n0 (1+z)/x_T) at z 0, 2, 5, 30, 1100, 3400, and what each line would demand if it were carried. | KD1, QX3 |
| c X-COP | interval | QX2's builder (7 clusters, 35 points), **G-X** (\|mean\| <= 0.05, rms <= 0.10). Graded model: the static isothermal dust **with its self-gravity and the share cap**. Spherical, static equation of section 1, baryons M_b(r) = gas + stars from X-COP's own profiles (log-log interpolation; beyond the data the last slope out to 3 R200, then constant). Total charge C(r) = M_L(r) - M_b(r) ends at r_c, where C(r_c) = X_cl M_b(r_c) with X_cl = 5.41 (RB1's R). Beyond r_c, M_L = M_b(r) + C(r_c) (Newtonian). Phi -> 0 at infinity (the cosmic background). Solved by shooting on r_c (inward, dust zero at the centre) along the branch continuous from no dust (continuation in decreasing c_s, steps <= 0.025 dex). Where the branch folds there is no static capped state and that c_s FAILS. Reported: amount (dust / baryons at R500) and radial shape (median Delta per x = 0.1 ... 0.7); MK1's reading (QX2's HSE potential, zero at 3 R200, no self-gravity, no cap). | QX2, QX6, RB1 |
| d groups | interval | Lovisari 2015, 20 groups, R2500 and R500 (QX5's `groups()`). **QX5's gate**: the bracket of mean Delta over stars 0..gas meets [-0.05, 0.05]. Same solver as row c: baryons a power law through the two gas points times (1 + s), s in {0, 1}; X_cl = 5.41. Reported: RB1's charge / (5.41 M_b) at R500. | QX5, RB1 |
| e SPARC | interval | **QX8's grader and line** (rms <= 0.110, median U 0.50-0.80), with QX8's exact-field T plus the dust's T_K = log10[g_law(g_bar + G M_d(<r)/r^2) / g_law(g_bar)]. Phi per galaxy and U: the data law field inside the last point, three iterations of the dust's own feedback; outside, the capped point-mass profile with the exponential dust (this lane's solver; X = PD1's share). The set is the c_s values at which the line passes. Reported: QX6's recheck line. | QX8, MK1 |
| f KiDS host-free, capped | interval | **ONE1's frozen statistic and gate** (1.6 R_h veto, KO1 tie rule, k fitted, neighbours carrying the same profile, five shuffles subtracted; G-K1 all / late / early within 2 sigma, G-K2 chi^2 <= 9.49, G-K3 within 2 sigma), with MK1's machinery and the exponential source. Own and neighbour tables per c_s on a grid of log(k M_b). Grid: 1000, 500, 300, 200, 150, 120, 100, 80, 60, 40 km/s, descending, then two log-midpoints between the last pass and the first fail. Lower bound = the smallest grid value such that it and every larger grid value pass. | ONE1, MK1 |
| g Solar System | interval | EW2 iter4's lines with this dust. Dust density at the Sun rho_bar_d exp((Phi0 + G M_sun/r)/c_s^2), Phi0 = (600 km/s)^2. **dg(Saturn) = G M_dust(< R_Saturn)/R_Saturn^2 <= 7.0e-15 m/s^2** and **Q2 = (4 pi/3) G rho_dust(1 AU) <= 9.0e-27 s^-2**. | EW2 |
| h SCS1 stability | interval | In the static states of rows c, d (both brackets) and of point masses at log M_b 9, 10, 11 (k 2.5, PD1's share): mu_eff(r) = sqrt(4 pi G rho_d(r)) / c_s, the local Jeans wavenumber. **PASS iff max_r mu_eff(r) r <= 2 pi in every state** (no local Jeans wavelength fits inside its radius, so SCS1's growing band is not resolved). Reported: the values, and SCS1's own labels. | SCS1 |

## 4. Rows that cannot be graded here (named, not graded)

The forest, linear growth and CMB-lensing rows. Form B carried them from the cold reference. With a Jeans length of
tens of Mpc at late times (row b's table), the dust no longer supplies that structure. To grade them one would compute
the late-time structure built by the baryons and the law's halos, with this dust as a smooth component: the record's
WG / GAL1 linear web with the law on, plus the nonlinear collapse (COL1's first step). This lane gives what those
computations would need and grades nothing there with a stand-in.

## 5. Label (per footing, frozen before any number)

- Graded rows: a, c, d, e, f, g, h. Not carried: the three lines of row b and the rows of section 4.
- **A VALUE EXISTS ON THE GRADED ROWS [L, U]** if every graded row is non-empty and their intersection is non-empty.
  The rows not carried are listed with it.
- **NO VALUE** otherwise. The label names the rows whose sets do not meet and the factor between the binding pair (for
  an empty row: its closest miss).
- **NO VERDICT** if any known answer of section 6 fails. KA-C1 and KA-C2 are the exception: they only decide whether
  (a2) is evaluable. If either fails, (a2) is NOT EVALUABLE with the reason, and row a rests on (a1).

## 6. Known answers

- **KA1, the quadratic through this lane's code reproduces MK1:**
  - Row c in MK1's reading: empty, min rms 0.263 / 0.255 at mu_K 1.35 / 1.26 (|d| <= 0.002).
  - Row d in MK1's reading: interval 0.912-1.514 / 0.759-1.380 (endpoints to one grid step).
  - Row e: capped upper bound 7.08 / 5.62 on MK1's grid.
  - Row g: 6223 (rel 1e-3).
  - KD1's mu_B1a: 198.254 (rel 1e-6).
- **KA2, isothermal closed forms:**
  - The Newtonian, baryon-free isothermal sphere integrated by this lane's ODE (Emden's equation) gives Bonnor-Ebert's
    critical xi 6.451 with centre-to-edge contrast 14.04 (rel 2e-3).
  - Its large-xi solution tends to the singular sphere, rho = c_s^2/(2 pi G r^2): Emden's e^-psi xi^2 / 2 stays within
    3 % of 1 over xi 3e3-1e4. The tolerance was set after a pure-math check of Emden's equation, before any lane
    number.
- **KA3:** the static dust of the capped point mass on the law against a direct quadrature of its density on the
  solver's own Phi (rel 1e-5).
- **KA4, no dust (c_s -> 1e7 km/s) reproduces the record:**
  - X-COP plain-law mean +0.4675 / +0.4345 (|d| <= 2e-3).
  - QX5's group bracket [+0.196, +0.359] / [+0.158, +0.320] (|d| <= 2e-3).
  - QX8's exact-field SPARC 0.0560 @ 0.58 / 0.0558 @ 0.52.
  - ONE1's graded KiDS z values (|d| <= 0.02).
- **KA-C1:** F1A's PA chi^2 at the B2 best fit, 3740.16 / 3740.30 (|d| <= 3).
- **KA-C2:** the fluid at c_s = 0.3 km/s (x_T = 1e-12) reproduces the cold reference's PA chi^2 (|d| <= 3).

## 7. MUTATE (separate outputs; each must move an interval, shown; any that does not is disclosed)

- **M-NOCAP:** rows c and d without the cap (uncapped isothermal dust, Phi -> 0 at infinity).
- **M-NOSELF:** rows c and d without the dust's self-gravity (the dust sits in the baryons' law field only).
- **M-2X:** the cluster and group share doubled (X_cl = 10.82), and PD1's galaxy share doubled in row e.

## 8. Lean

`fable_independent_2026/lean_2026/MK2.lean`:
- the trade-off (`width_le`, `well_floods`, `flood_threshold`);
- the exponential's w, c_s^2 and k_J^2 identities;
- the singular isothermal sphere satisfying hydrostatic balance with Poisson;
- monotonicity of the static dust in phi and in 1/x_T.

The twin `MK2_MUTATE.lean` states false versions (the width bound reversed, flooding without monotonicity, a wrong SIS
normalisation, w independent of x_T) and must fail to compile.

## 9. Scope and rules

- Statics and spherical symmetry, except the KiDS projection.
- Form B's share cap as stated.
- One thread, about 1.5 GB, preemptible; no downloads.
- Files end "kappa = 1/2 FITTED; not theory closed. Adopts nothing."

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
