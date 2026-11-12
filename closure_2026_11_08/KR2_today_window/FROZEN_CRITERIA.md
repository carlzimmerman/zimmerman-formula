# KR2 frozen criteria: the present-day mu_K window for the action's K(Q) dust at the CMB's amount

Frozen before any KR2 script or KR2 number exists. Brief: `closure_2026_11_08/KR1_KR2_BRIEF_2026_11_08.md` (KR2 section),
tightened, never loosened. TEST lane under the owner's 11-04 rule, opened 2026-11-08 ("launch lanes, solve clusters and CMB
based on this framework or something compatible with the action equations"). The component is the action's own K(Q) sector,
cold dark energy; never dark matter; no particle. Adopts nothing. Kappa = 1/2 FITTED; not theory closed. Both footings
(canonical a0 1.2e-10 line, alt 1.1e-10 line; each column uses the a0 its record machinery uses, stated in RESULT), graded
separately, never pooled. Raw data or framework-native only: the dust distribution comes from the record's own n = 1
host-hydrostatic K(Q) dynamics; no NFW, no LambdaCDM simulation profile, no LambdaCDM parameter value. One thread, RSS < 1 GB,
SIGTERM checkpoint, each column in its own process. No downloads. Read-only use of every other lane's code and JSON.

## 0. Question

mu_K(0) (physical Mpc^-1) is the one quantity the action leaves free today; KR1 derives mu_K(z). KR2 maps where mu_K(0) must
land: for mu_K(0) in [0.1, 79.43] Mpc^-1, with the CMB's amount of K-dust (F1A R = 5.409583 canonical / 5.412268 alt times
the system's baryons) distributed by the action's own dynamics, is there ONE mu_K(0) that passes every column, per footing?
This is not a knob scan: the grid maps a window for KR1 to read against; nothing is fitted.

## 1. What the record already says (stated before any number; the lane re-grades, it does not cite these as results)

- KQ1 (criteria 07534f282b) did NOT use mu_K = 8.9e6 for its scan: it scanned mu_K 0.1-1e4 Mpc^-1 (28 grid + 4 refined) with
  QX7 iter_5's host-hydrostatic n = 1 solver at amount F_X = 4.1786 / 3.7833 (KD1's X-COP need), and found CANNOT FORM CORE
  (closest mu_K 19.05, per-bin rms 0.784 / 0.758; best rms anywhere 0.226 at mu_K 2.5). KQ1 used 8.89e6 only as its M1
  (KD1's cusp). KR2 re-grades at the CMB amount R and with the brief's U1 cap rule (reading B below).
- QX7 iter_5 / QX10 iter_2: host-held n = 1 dust at f_cap R; galaxy gates pass only at lambda_0 = 2 pi/mu_K >= 10 Mpc
  (mu_K <= 0.63); X-COP rms never below 0.225.
- GL1 (corrected kernel, GL2 CONFIRMED): constant-mu CMB-lensing Jeans line mu_J = 631; Delta chi^2 667.5 / 309.0 (canonical)
  and 667.3 / 309.0 (alt) at mu 0.1 / 79.43.
- HY1: KD1's point-mass dust (mu* 8.89e6) at f_cap R fails SPARC and X-COP at every kappa.

## 2. The dust (frozen)

- Dynamics: the record's n = 1 host-hydrostatic equation (QX7 iter_5 `profile`, executed read-only through KQ1's prefix,
  which goes through NA2's): d rho/dr = -(mu_K^2 / 4 pi G) g_law(G (M_b(<r) + M_d(<r)) / r^2), rho_c shot to the total
  M_d,tot. mu_K physical, today (a = 1). Retention: iter_5's rule, the system keeps M_d,tot if r_s < r_ta0(M_b,tot), else
  nothing.
- Amount (label): M_d,tot = R x M_b,sys with F1A's R per footing (the brief's f 5.41). Reported bracket (never the label):
  f_cap R = 0.76 R (KD1/X22 capture, 4.111 / 4.113).
- **Reading B (the label; the brief's rule, U1):** held dust inside r_J = 1/mu_K is at most the phantom, which the a0 law
  already counts, so the EXTRA mass inside r_J is zero; the dust is self-bound only beyond r_J. Operationally:
  M_B(<r) = 0 for r < r_J and M_B(<r) = M_A(<r) for r >= r_J (the solver's inner mass placed as a shell at r_J; mass and
  the field outside r_J unchanged).
- **Reading A (reported, every column):** the solver's M_A(<r) uncapped (KQ1 / iter_5's reading).
- C5 (KiDS) uses KX1's own sector machinery (QX10 iter_2 `solve_static`, the same n = 1 equation and K = G lambda^2/(2 pi),
  closed boundary at r_ta: retains what fits) with its lam set to 2 pi/mu_K and the amount set to R x M* (KX1/HY1 lens
  convention); reading B applied the same way. The two solvers are cross-checked (KA6).
- A vectorised copy of `profile` (same algorithm over many hosts at once) may be used for speed only after KA7 shows it equals
  `profile` to <= 1e-5 relative in M_d at the graded radii on >= 5 SPARC galaxies, 2 X-COP clusters and 2 groups, per footing.

## 3. Grid

mu_K(0) in G = {0.1 x 10^(k/5), k = 0..14} U {79.43282347242821} (16 values, 0.1 to 79.43). Per footing. Edge refinement
(reported only, never the label): 12 log-halvings between grid neighbours where a column's status changes, for C2, C3, C5,
C6. No other scan. MUTATE values in section 6.

## 4. Columns (each per footing, per grid mu, reading B at amount R is the label; A and f_cap R reported)

- **C1 SPARC clean.** QX8's per-galaxy rule as HY1 C1 ran it (kappa 1/2; per-galaxy U refit; pooled rms <= the QX8 line and
  median U in its band; T carried, and T = 0 must give the same PASS/FAIL or the cell is NOT EVALUABLE), with g_N at each point
  raised by G M_d(<R)/R^2. Host baryons for the dust: the galaxy's M_b(<r) at U_disc 0.5, U_bulge 0.7, constant beyond the
  last point at max(M_b(r_last), 0.5 L36 + 1.33 M_HI) (HY1's M_tot at U 0.5). AND per galaxy: M_d(<r_last) / M_b(<r_last)
  <= SPARC's cap 0.3257 / 0.1937 (KD1 uniform-f diag) for EVERY galaxy. Both parts must pass.
- **C2 X-COP core.** KQ1's lines on the 7 X-COP clusters (iter_5 XPROF hosts, M_d,tot = R x M_last): L3 concentration
  M_d(<0.25 R500)/M_d(<0.7 R500) in [0.2475, 0.2665] every cluster; L4 NA2's per-bin rule (rms <= 0.10 and every bin with
  n >= 3 |mean| <= 0.10, inner bin included); L5 the need amount present: M_d(<r_ta0) >= F_X M_last (retained). Core line:
  reading B: L1B r_J <= 100.5 kpc (the extra cannot start outside the 50-100 kpc core); reading A: KQ1's L1 (r_1/2 in
  [49.5, 100.5] kpc) and L2 (max |dln rho/dln r| <= 0.5 inside 20 kpc). C2 passes if all its lines pass.
- **C3 groups.** UA1's budget as HY1 C3a ran it: the law-relative step (mean over all GB1 group points of
  log10 glaw(g_N + G M_d(<r)/r^2) / glaw(g_N)) inside UA1's 95 % interval (canonical [0.0524, 0.4595], alt [0.0093, 0.4151])
  for BOTH stellar brackets f* 0 and f* 1. Host: point mass M_sys = g5 (1 + f*) (GB1's group total), M_d,tot = R M_sys.
  GB1's strict per-group rule reported only.
- **C4 Bullet.** DB1's arms. The only Bullet machinery on disk (DB1/UX6 through NA2's child) measured 1.19-1.48 GB (NA2, CE2).
  It is NOT run; C4 is NOT EVALUABLE under the RSS line, and the window is stated without it (it could only shrink it).
- **C5 KiDS G6 with kSZ gas.** KX1's budget (P1 gas central, two-halo at b_cap/2, full sigma_tot, 100-300 kpc window, four
  mass bins) with the dust added to g_N; HY1's two-sided rule: FAIL if |z| > 2 in >= 2 of the 4 bins, z = (W - E)/sigma_win.
  Dust beyond r_J adds to the stack through M_d(<r).
- **C6 hosts inside R500.** NC4's census: host baryons inside R500 = 0.0133 of rho_b. Held share H = 0.0133 x
  median_X-COP[M_d(<R500)/M_b(<R500)] / R must be <= NC4's most generous capacity 0.0248 / 0.0222, AND every X-COP cluster
  M_d(<R500)/M_b(<R500) <= F_X (4.1786 / 3.7833; hosts cannot hold more than they need). Both must pass.
- **C7 CMB lensing shape, corrected kernel.** KD1's footing background (QX15 theta), QX3 iter2's Jeans growth ODE with
  suppression (k/(a mu))^2 and GL1's Limber with the k^-4 restored (n = 4), PR4 L <= 400, A_s refit; Delta chi^2 vs mu -> inf
  <= 4. **C7-static (graded):** mu(z) = mu_K(0) at every z. **C7-run (hand-off to KR1, reported, never the label):**
  mu(z) = mu_K(0) for z < z_run, no suppression above; z_run in {0.25, 0.5, 1, 1.5, 2, 3, 5, 10, 20}; z_run,max(mu_K(0)) = the
  largest grid z_run with Delta chi^2 <= 4 at it and every smaller z_run.

## 5. Labels (per footing; footings never pooled)

- Column window W_k = the grid mu where column k passes (reading B, amount R).
- **PASS (window W)** if W = W1 n W2 n W3 n W5 n W6 n W7 (C7-static) is non-empty (C4 NOT EVALUABLE, disclosed).
- **FAIL (empty at Ck)** if W is empty; Ck = the first column, in the order C1, C2, C3, C5, C6, C7, at which the running
  intersection becomes empty. Also stated: which column windows are empty on their own and which pairs are disjoint.
- **Today window (hand-off, not the label):** W_today = W1 n W2 n W3 n W5 n W6, sent to KR1 with z_run,max on it (or the
  statement that it is empty and the first column that empties it).
- **NO VERDICT** if any KA fails, a MUTATE twin fails to bite, or a graded cell errors.
- Reading A's windows and the f_cap R bracket are reported per column; they do not change the label.

## 6. Known answers (all before any graded number; a KA FAIL means stop) and MUTATE

- KA1 F1A R read exactly (5.4095831638392 / 5.41226812314077); KD1 f-table read (F_X, capture, SPARC cap).
- KA2 SPARC law only (f 0) through my C1 evaluator = QX8 exact (HY1 KA2: rms 0.05604651 @ U 0.58 / 0.05582588 @ 0.52), |d| <= 1e-6.
- KA3 X-COP law only through my C2 evaluator = 0.467499 / 0.434523 (GB1 KA20) to 1e-6; KQ1's own KA1-KA5 replay inside its
  prefix (all PASS).
- KA4 KiDS law (f 0) through my C5 wrapper = KX1's E_b and sigma_tot per bin, |d| <= 1e-9, W = 0.
- KA5 groups law only: step 0 for both f* (HY1 KA5).
- KA6 cross-solver: KQ1's recorded closest row (mu 19.05, amount F_X) reproduced through my C2 path with `profile`: per-bin rms
  and inner bin to 1e-3; KX1's recorded C2 cell W per bin reproduced through my C5 wrapper with the cell's own lam and amount
  to 1e-9; and the two solvers' M_d(200 kpc) for a lens host of 10^10.7 at one bound mu agree to 2 %.
- KA7 vectorised solver (only if used): section 2.
- KA8 C7: GL1's corrected KD1 converse Delta chi^2 at mu 0.1 and 79.43 per footing reproduced to 1e-3; C7-run with
  z_run -> infinity (> 3400) equals C7-static to 1e-9.
- **M1 mu_K -> 8.89e6 (KD1's mu_B per footing, 8.890e6 / 8.889e6) must reproduce KD1 / KQ1 failures:** at KD1's capture amount
  my C2 path gives KD1's G2 cusp mean / rms (-0.702864 / 0.802677; -0.714392 / 0.809485) to 1e-5 and L1 fails (r_1/2 < 1 kpc);
  at amount R: C1, C2 and C5 FAIL on both footings. If any of these does not happen: NO VERDICT.
- **M2 f -> 0 must reproduce the law's record numbers to 0:** KA2-KA5 (SPARC QX8, X-COP 0.467499 / 0.434523, KX1 baseline E_b,
  UA1 step 0). C2 must FAIL at f 0 (the law alone fails X-COP), so C2 has power.
- **M3 planted core (power):** NC4's cored isothermal r_c 100 kpc at the need amount (KQ1's M3 install) must pass C2's L3 and
  L4 through my evaluator (KQ1 M3: rms 0.0908 / 0.0907). If it fails, C2 is mis-built: NO VERDICT.

## 7. Expected outcome (honest, before any number)

FAIL on both footings, emptied at C2. Under reading B the X-COP extra starts at r_J = 1/mu_K: for mu_K < 10 the core line L1B
fails (hollow beyond 100 kpc); for mu_K >= 10 KQ1's equilibrium puts the whole amount inside 0.25 R500 (c ~ 1), and R = 5.41 is
above X-COP's need, so the inner bins over-fill. I expect C1 to pass at most mu_K (under B the extra sits beyond r_J, outside
most discs, until mu_K ~ 10-40), C5 to pass only at low mu_K (<= ~0.6, iter_5/QX10) where lenses do not retain, C6 to need the
dust beyond R500 (low mu_K), and C7-static to fail at every mu_K <= 79.43 (GL1's line 631). If a window appears anywhere, I
expect it at mu_K <= 0.6, without C2.

## 8. Outputs

`kr2.py` (subcommands, each its own process) -> `parts/*.json`; `kr2_grade.py` -> `kr2.json` / `kr2.out`; MUTATE ->
`kr2_MUTATE.json` / `kr2_MUTATE.out`; `RESULT.md`. Untracked symlink to the gitignored KiDS data (as HY1), not committed.
Post-freeze changes are committed as amendments before any rerun and disclosed.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
