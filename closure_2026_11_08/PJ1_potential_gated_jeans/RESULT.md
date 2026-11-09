# PJ1 RESULT: FAIL / FAIL (criteria e3c9bc7d3c)

Potential-gated biharmonic Jeans scale for the K(Q) component (outside proposal, graded as a quarantined TEST lane under the
record's gates; owner decision OWNER_DECISION_2026-11-08_PJ1_LAUNCH.md). Adopts nothing. kappa = 1/2 FITTED; not theory
closed. Footings canonical (a0 9.3603e-11) and alt (a0 1.1312e-10) graded separately, never pooled.

Label rule (frozen): PASS iff one grid point or the as-written point passes G1-G10; FAIL iff none; NO VERDICT only for a
NOT EVALUABLE gate. **No cell passes on either footing: 0 of 756 (252 grid points x 3 ell_theta) on canonical, 0 of 756 on
alt, and the as-written point passes only G10 on both footings and both R_J forms. No gate is NOT EVALUABLE.** Label FAIL
on both footings.

## What was built (pj1.py, pj1_web.py, pj1_cmb.py, pj1_bullet.py, pj1_grade.py)
- Two-field tridiagonal (banded) solve of [1 + R_J^4 grad^4] rho_K = rho_b S(Phi) in spherical symmetry on a log-radial
  grid: R_J^2 grad^2 rho_K = u, R_J^2 grad^2 u = rho_b S - rho_K; zero flux at the origin, decay at the outer edge.
  With a position-dependent R_J the literal operator ordering (R_J^2 lap)(R_J^2 lap) does not conserve the source mass
  (it creates 2.6x / 1.9x the source at the as-written point, forms T / C); the lane uses the divergence form
  div(R_J^2 grad f), which conserves mass exactly and coincides with the literal form at constant R_J. The literal form
  is kept as an option and reported, not graded (disclosed).
- Self-consistent depth Phi including M_K: the law's potential integrated outward to r_EFE (QX5 key-a convention, cut at
  g_law = 0.03 a0), damped fixed point (tol 1e-5). Both R_J forms, T (text) and C (code). Law on g_source = G(M_b + M_K)/r^2;
  disc correction g_eff = g_source [1 - ell_theta^2 grad^2 ln(1 + g_source/a0)] with the in-plane Laplacian (the spherical
  Laplacian reported); a negative g_eff is floored, giving a large residual rather than a nan.
- G7: scale-dependent weight w(k) = S(Phi_rms(k))/R_cmb at z 1100 with Phi_rms(k) = sqrt(k^3 P_Weyl/2 pi^2)/k^2 from the
  linear Weyl spectrum at recombination; CAMB source transfers Delta_ell(k) on a grid of 11 constant weights on the same
  background (clustering omega_c = w omega_d; the smooth remainder carried as a c_s^2 = 1, w(a)-tabulated fluid with Lambda),
  assembled per k at w(k), lensed with the w = 1 potential; own binned CamSpec NPIPE 12.6 likelihood to ell 2500 (TT 143x143
  30-2000, 217x217 and 143x217 500-2500, TE and EE 30-2000; 9915 multipoles in 996 bins; F1A's foreground model and
  nuisance priors); Delta chi^2 vs the constant-weight fit, then a 40-evaluation Nelder-Mead refit of the 5 cosmological
  parameters at the as-written gate (verify the fail as hard as a win).
- G8: QX3 iter2 growth ODE with a per-k non-clustering fraction 1 - W(k, a), W = S(Phi_lin(k, a))/R / (1 + (k R_J/a)^4),
  Phi_lin per mode from the linear web by Poisson; GL1 corrected Limber kernel on raw PR4 lensing; CE2/BG1 fsigma8 rule on
  DESI DR1. G9: NC2 G3 forest machinery (DESI DR1 P1D, md5 checked, 755 bins). G6: DB1/UX6 Bullet machinery with the
  component sourced on gas + stars at S(Phi) of the Bullet depth. G5: Coma UDGs through GB1's rows at the S1 host depths.
  G10: MW Hernquist depth at R0, component density as a Cassini-use term, c_T = 1 stated (spatial-only term).

Known answers, all PASS on both footings: KA1 QX8 law pooled rms reproduced to 1e-6; KA2 GB1 L0 X-COP and UDG means
reproduced to 1e-6; KA3 biharmonic solver vs the Fourier-exact Gaussian response (ratios 1.0000 +- 4e-4, total 1.0001;
point-source closed form 3e-3 beyond 0.3 Mpc, reported); KA4 depth tail vs QX5 tail_phi (3e-5); KA5 web identities at R = 1
(fs8 ratios 1.000, lensing and forest Delta chi^2 0.0); CMB KA_C1/C2 assembly vs CAMB (TT 1.6e-3, EE 7e-3 reported),
KA_C3 F1A's PA chi^2 at the B2 best fit (+2.0, within 3), KA_C4 fluid route at w 0.999 vs Lambda (1.8e-3), KA_C5 assembled
vs direct Planck-2500 chi^2 (+2.1 of 996 bins); Bullet KA5 law-alone masses reproduced (M300 1.112e14 / 7.337e13).

## Gate table, AS-WRITTEN point (R_J0 1.4 Mpc, Phi_*/c^2 1.5e-6, p 2, ell_theta 1.5 kpc, R_cmb 5.41)

| gate | canonical, form T | canonical, form C | alt, form T | alt, form C |
|---|---|---|---|---|
| G1 SPARC (rms vs line 0.066 / 0.0658, |mean| <= 0.05) | FAIL 0.789, mean +0.057, 3.0 % negative g_eff | FAIL 0.791, +0.046 | FAIL 0.720, +0.044 | FAIL 0.726, +0.024 |
| G1 at ell_theta 0 (component alone) | PASS 0.0562 (law alone 0.0560), f_K 5e-7 | PASS 0.0562 | PASS 0.056 | PASS 0.056 |
| G1b massive tail (10 galaxies, line 0.0475 / 0.0426) | FAIL 0.697 | FAIL 0.699 | FAIL 0.694 | FAIL 0.698 |
| G2 KiDS 59 points, every bin |shift| <= 0.05 | FAIL max 0.417 (outer bins), mean +0.080, 19 points over | FAIL 0.431, +0.111, 23 over | FAIL 0.423, +0.087, 21 over | FAIL 0.435, +0.130, 27 over |
| G3 X-COP (|mean| <= 0.05, rms <= 0.10) | FAIL -0.067 / 0.105 | FAIL -0.067 / 0.105 | FAIL -0.090 / 0.121 | FAIL -0.090 / 0.121 |
| G3 shape, M(<0.25)/M(<0.7 R500): component / gas / need | 0.209 / 0.202 / 0.267 (component no more concentrated than gas) | same | same | same |
| G4 groups >= 16/20 (two footings of the need band) | FAIL 2 / 0 | FAIL 2 / 0 | FAIL 1 / 0 | FAIL 1 / 0 |
| G5 Coma UDGs within 2 sigma_U | FAIL +1.119 dex (+4.27 sigma), b 1.00 | FAIL +0.687 (+2.62), b 6.45 | FAIL +1.076 (+4.11) | FAIL +0.645 (+2.46), b 6.49 |
| G6 Bullet (component centroid on the galaxies' side) | FAIL, S/R 1.000 at the Bullet depth; dkappa -0.23 / -0.47 | FAIL | FAIL, -0.25 / -0.48 | FAIL |
| G7 primary CMB Delta chi^2 <= 10 | FAIL +619.5 no refit, +171.7 after the 40-eval refit | same (S-only statistic) | FAIL +613.5 / +170.9 | same |
| G8 PR4 lensing Delta chi^2 <= 4 and fsigma8 | FAIL 1162, fs8 ratios 0.056-0.058 | FAIL 575, ratios 0.152-0.156 | FAIL 1162 | FAIL 575 |
| G9 forest (NC2 gate, Asimov Delta chi^2 <= 4) | FAIL 2.3e5 | FAIL 2.3e5 | FAIL 2.3e5 | FAIL 2.3e5 |
| G10 Cassini + c_T = 1 | PASS (use 2.8e-8; rho_K 1.2e-7 Msun/pc^3) | PASS (9.7e-7) | PASS (2.0e-8) | PASS |
| gates passed | 1 of 11 | 1 of 11 | 1 of 11 | 1 of 11 |

Reported alternative R_cmb 4.4 (the proposal's misreading, not the primary): G3 PASSES (-0.013 / 0.082 canonical,
-0.037 / 0.090 alt) but G2 (max 0.378-0.394), G4 (3/1, 3/0, 2/0), G5 (+1.12 / +0.73; +1.08 / +0.69) and G7 (+3667 / +3684 at
constant weight x 4.4/R) still fail. Total-potential web reading (G8/G9 keyed on the total linear-web potential instead
of the per-mode potential, reported): form C passes G8 (Delta chi^2 0.13, fs8 within 2 sigma) but G9 stays at 1.8e5; form T
fails both (485; 2.3e5). k^4-cutoff variants of G7 (R_J a proper length, k comoving): form T +287,177, form C +106,417;
with a comoving R_J0 cutoff +622 (both footings alike). G1c (informational): AGC 114905 law chi^2 843.6 / 995.8 -> 847.9 /
999.9 with the component and ell 1.5 kpc (860.9 / 1012 at 3 kpc); Malin 1 law 69.0 / 132.5 -> 76.1 / 146.0 (form T),
2222 / 4148 (form C, where f_K reaches 3.7-4.6 inside the giant disc).

## Best grid point (most gates passed, then smallest summed miss), both footings
T | R_J0 2.5 Mpc | Phi_* 3e-7 | p 2 | ell_theta 0: 4 of 11 gates (G1 rms 0.0617 / 0.0652, G1b 0.0386 / 0.0378, G7 +3.5,
G10). Failing: G2 max 0.439 / 0.441 dex (outer bins), G3 -0.067 / 0.105 and -0.090 / 0.121, G4 2/0 and 1/0, G5 +1.096 /
+1.056 (+4.2 / +4.0 sigma_U), G6 FAIL, G8 lensing 823 with fs8 ratios far below 1, G9 2.3e5. **Killing gate G9 (forest),
miss 5.7e4 in units of its bound; G8 next (miss 206); G2 next (7.8).** Per-gate windows over the 756 cells: G1 183 / 179,
G1b 186 / 181, G2 207 / 204, G7 84 / 84, G10 756 / 756; G3, G4, G5, G6, G8, G9: 0 / 0 on both footings. G7 passes only at
Phi_* 3e-7 with p 2 or 3 (+3.5; +0.4), where the weight stays above 0.93 out to k 0.2 (0.80 / 0.89 at k 0.3), i.e. where
the gate barely acts on the acoustic range; every cell with Phi_* >= 1e-6 fails G7 (>= +65; p 1 at 3e-7 fails too, +66).

## Expected kills (brief): all three fire on both footings and both forms
1. G7 damping tail: the linear potential at recombination falls from 2.6e-5 at k 0.01 to 2.9e-6 at k 0.1, 1.1e-6 at k 0.2
   and 5.9e-7 at k 0.3 (Phi_rms per ln k), straight through the gate's range, so at the as-written Phi_* 1.5e-6, p 2 the
   weight is 0.997 at k 0.01, 0.79 at 0.1, 0.59 at 0.14, 0.35 at 0.2 and 0.135 at 0.3 (the brief's hand estimate, 0.99 at
   peak 1 to about 0.6 at ell 2000, is confirmed in sign and size): Delta chi^2 +614 to +620, +171 after refit. FIRES.
2. G2 outer bins: the component fills the isolated lenses' outskirts (0.3-1.5 Mpc) at S/R near 1: shift 0.42-0.44 dex
   there. FIRES.
3. G3 / G6 gas-traced shape: the component sourced by the hot gas is no more concentrated than the gas (0.209 vs 0.202,
   need 0.267) and over-fills X-COP at the CMB amount (-0.067 / -0.090); on the Bullet it tracks the gas, centroid on the
   gas side, dkappa -0.23 / -0.47. FIRES (both G3 and G6).

## MUTATE (pj1_MUTATE.json / .out)
- M1 gate inverted (S large where |Phi| is small), as-written: G1 at ell 1.5 FAIL, G2 FAIL (max 0.16-0.18), G3 +0.47 / +0.43
  -> BITES (both footings, both forms).
- M2 S -> 0 (law alone): X-COP +0.4675 / 0.4763 and +0.4345 / 0.4442 -> BITES.
- M3 R_J0 -> 10 R_J0 at the best point (2.5 -> 25 Mpc): G2 stays FAIL (0.439 -> 0.274; 0.441 -> 0.303), G8 stays FAIL
  (823 -> 1418) -> **does NOT bite as frozen**: both gates fail on both sides of the mutation; the numbers move by 0.14-0.17
  dex and Delta chi^2 +595, so the mutation acts but flips no status. The label does not rest on M3 (no cell is near a
  pass on G2 or G8). Disclosed.
- KA replay Phi_* x10 at the best point: flips G7 (+3.5 -> FAIL) -> BITES; criteria hash e3c9bc7d3c in every output.

## Disclosures
- Divergence-form operator used for variable R_J (mass-conserving); literal ordering reported only (creates 2.6x / 1.9x
  the source mass at the as-written point). At constant R_J both coincide and the solver is verified against the exact
  Fourier response (KA3).
- G6 is graded under the record's instantaneous Bullet relation (DB1/UX6: the component follows S(Phi) x the present gas +
  stellar fields); no dynamical merger model exists in the record, so the gate is EVALUABLE only in that sense and would
  be NOT EVALUABLE for a component with memory. The label does not rest on G6 (G2, G3, G7, G8, G9 fail everywhere).
- G8/G9 primary reading keys the gate on the per-mode linear potential (the proposal's Phi(k)); the total-web-potential
  reading is reported above (form C passes G8 there, G9 fails under both).
- Compute: local grid 1075 s at 0.19 GB RSS (resumed once from its own checkpoint after the disk filled; every point graded
  by the same code), M1 twin 777 s at 0.20 GB, web 425 s at 0.37 GB, CMB 828 / 839 s per footing at a peak RSS of 1.004 GB
  (canonical) / 0.998 GB (alt) in units of 1e9 bytes (0.935 / 0.929 GiB), after holding the transfers in float32 and freeing
  F1A's likelihood objects after KA_C3; Bullet 38 s with DB1's child process at 1.39 GB (the record's machinery, run as
  is). The 1 GB touch is disclosed, not hidden.
- Both CMB footings and the local grid were run as separate processes; the grader merges parts/cmb_canonical.json and
  parts/cmb_alt.json.

## Reading
The potential gate does the galaxy side no harm only where it does nothing (Phi_* 3e-7: S near 1 at every depth that
matters, so the component is just the CMB amount of dust in every well, and G2-G6, G8, G9 fail as for plain dust), while
any Phi_* large enough to shape the weight (>= 1e-6) cuts it across the acoustic range, because the recombination potential
runs from 2.6e-5 at k 0.01 down to 6e-7 at k 0.3, straight through the gate: Delta chi^2 >= +65 at Phi_* 1e-6, +600 at the
proposal's value. No value keeps the component out of the KiDS outskirts, the Coma UDGs or the forest. The biharmonic scale R_J adds nothing that survives: the forest (G9) and growth (G8)
reject every R_J0 in 0.3-10 Mpc on both footings, and X-COP, groups, UDGs and the Bullet fail at every grid point. The
K(Q) sector stays closed (KR1, KR2, BG1, HY1); PJ1 adds that a potential-gated Jeans scale is not an open door either.
