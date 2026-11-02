# BK2_dimensional_law_search: FROZEN CRITERIA, committed alone before any script or number of this lane

Owner's go, 2026-11-02. **Not blind.** Read before this freeze: BF1 (README, A1, bf1.py, bf1_read.py, L3 hits), AF1 README, UX3 README and scripts, UX6 README, criteria and bullet code, LW1 README, criteria and scripts, FG1 criteria, M3A1 and UL1 and LF1 headlines, SL1's grader code and cache layout, CFG770's bound constants, the record's alpha = 1 ephemeris note, ENGINE_REVERSE_ENGINEERING. I know the law's rows on every line, that BF1's L3 near-miss family pi^2 g_gas/a0 is DEAD on the Bullet as present gas, and that N2 (gas carried with galaxies) was closest there.

kappa = 1/2 FITTED. The cold sector stays retired; nothing here reinstates it. No dark matter particle. No Planck or LCDM input. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2: searched separately, reported separately, never pooled. Not theory closed. Nothing here says the data favour the framework. A SURVIVOR is a candidate only: no action, no CMB.

## Question
Is there one dimensionally valid closed form g = F(leaves) that reduces to Newton at high g, keeps discs, and passes every line on data it never saw?

## Difference from BF1
BF1 used three dimensionless leaves and fixed wrappers around the law's interpolation. BK2 carries dimensions, adds local leaves BF1 did not have, separates g_star and g_gas, varies the interpolation, and has additive and raw forms. Overlap with BF1 is limited to low-complexity law x H(y, ell, f) rows and is not removed; I report how many.

## Leaves and dimensions (L, T, M)
G, c, a0, rho_DE, g_star, g_gas, g_b = g_star + g_gas (a convenience leaf, same information), r, Sigma_b, rho_b, Phi_b.
- rho_DE is fixed per footing by a0 = (1/2) c sqrt(G rho_DE), so it carries no independent number and no background input. Value deduplication removes c sqrt(G rho_DE) against 2 a0.
- With M_b(<r) = g_b r^2 / G: **Sigma_b = (dM_b/dr)/(2 pi r), rho_b = (dM_b/dr)/(4 pi r^2)**, local on the measured profile, negative slopes clipped at 0. **Phi_b = r g_b + integral of g_b from r to the last point + G M_last / r_last.**
- One-point samples (LITTLE THINGS, groups as rows, dwarfs, IC 1613) have no slope: dlnM/dlnr = 1 and Phi_b = 2 r g_b, tagged [ONE-POINT]. Solar System: g_gas 0, Phi_b = GM/r, rho_b from the solar wind, 8e-21 kg/m^3 at 1 AU falling as r^-2, PROVISIONAL, recalled, disclosed; Sigma_b from the same definition.
- **T and sigma:** the owner allows them where measured. X-COP's disk files carry mass and gas profiles, no T. SPARC carries no dispersion. So neither is measured on any train row: a formula using them can't be graded at the train gates. **They are not in the grammar, and that is a limit reported, not a result.** Files that would lift it get named in the report.
- Non-local: **one history leaf, only at the Bullet gate:** g_gas^mem, gas restored on its galaxies (UX6's N2), with carrier equation stated: d rho_mem/dt + div(rho_mem v_gal) = 0, source-free, rho_mem = rho_gas before the merger. Identical to g_gas on relaxed rows, so it adds no search. It is a named kinematic rule, not a physical mechanism. Each formula holding g_gas is graded on the Bullet on both the present and the carried reading, reported apart.

Constants: 1/2, 1, 2, 3, 4, pi, 2 pi, 4 pi, pi^2, 1/pi, 4/3, 8 pi/3. Geometry only. **At most one fitted constant, in its own tier T5, on a stated grid, counted and labelled FITTED.**

## Grammar, exhaustive within this
By Buckingham, any valid expression is an acceleration monomial times a function of dimensionless groups, and a sum of like dimensions X + Y is X (1 + Y/X). So:
- **Monomials:** products of at most 4 distinct leaves, exponents in +-1/2, +-1, +-2, in dimension acceleration (M_A) or dimensionless (M_D). Dimension is structural: anything else is never scored. Value-deduplicated on the evaluation points; cost = leaves + non-unit exponents.
- **D (dimensionless):** D0 = constants and M_D. D1 = unary of D0 (sqrt, square, inverse, log1p, 1/(1+x), exp(-x)). D2 = binary of D0 and D1 (+, -, *, /), and unary of those. Capped at CAP_D by cost then lexical order.
- **A (acceleration):** A0 = constant x M_A. A1 = A0 x D2. A2 = I_k(A0, A0). Capped at CAP_A by cost then lexical order.
- **Interpolations I_k(X, Y)**, fixed macros, no numbers fitted: I1 law X/2 + sqrt(X^2/4 + X Y); I2 X sqrt(1/2 + sqrt(1/4 + (Y/X)^2)); I3 X (1/2 + sqrt(1/4 + (Y/X)^3))^(1/3); I4 X (1/2 + sqrt(1/4 + (Y/X)^4))^(1/4); I5 X/(1 - exp(-sqrt(X/Y))); I6 X (1 + (Y/X)^2)^(1/4).
- **Top forms:** T1 I_k(A, B); T2 A + B, A - B; T3 I_k(g_b, a0) x H, H = D op D; T4 A x H, A in A0, H in D2; T5 FITTED: I_k(g_b, a0)(1 + k H), I_k(g_b, a0) + k E, H in D2, E in A1, k on 81 log-spaced values 1e-3 to 1e3.
- **Levels:** L1 CAP_D 3e4, CAP_A 3e4. L2 CAP_D 1e5, CAP_A 3e5. L1 runs real then control on both footings, then L2. Caps are real limits and are reported, with the closure size before capping. L2 is ordered so a partial run is the low-cost part.

Forms where two terms of size g_b cancel to Newton are covered in T1, T2 because every pair is tested on the Solar System point, not pruned by assumption.

## Gates, all required, cheap to dear
Each gate has **two readings, both reported with Z: LINE,** the record's frozen line, unchanged; and **ERR,** from that line's measured error budget. A formula is **SURVIVOR** only if it passes every gate on the LINE reading. If it passes on ERR everywhere and misses a LINE, it is **WITHIN ERRORS, OUTSIDE A LINE**, named and listed, not a survivor. Tolerances are stated here and never widened after a result.

| Gate | Data | LINE | ERR: Z, passes if |
|---|---|---|---|
| G0 dimension | none | acceleration | structural |
| G1a Newton | Earth, Mars, Saturn | abs(g/g_N - 1) <= 1e-3 | same |
| G1b Cassini | 1 AU, Saturn, each footing | anomaly <= 3.66e-14 m/s^2 at 1 AU; <= G (6.7e-11 Msun)/(9.54 AU)^2 at Saturn (the record's 2 sigma ephemeris bounds, CFG770) | Z = anomaly/(bound/2), <= 2: the same line, already an error |
| G2 SPARC train | odd sorted names, BF1's cuts | rms <= 1.05 x law's rms, abs(median) <= 0.03, at Upsilon 0.5, 0.7 | Z_rms = (rms^2 - rms_law^2)/se, galaxy-block paired bootstrap, <= 2, one-sided. Z_U: median at disc Upsilon 0.50, 0.65, 0.80 (bulge x 1.4), the SPS range FG1 uses; 0 if the median crosses zero inside it, else nearest abs(median)/se, <= 2 |
| G3 X-COP train | sorted positions 0, 2, 4, 6, x <= 0.75 | abs(mean) <= 0.05, rms <= 0.10 | Z_mean = mean/sqrt(se_cl^2 + 0.12^2), se_cl cluster-block, 0.12 LF1's measured HSE-lensing offset in quadrature with no shift, <= 2. Z_shape from chi^2 of residual about the mean with sigma_i^2 = EM_FORW^2 + spread of the four mass models on disk: (chi^2 - n)/sqrt(2 n), <= 2. Diagonal: no covariance on disk, said so |
| G4 SPARC holdout | even names | as G2; plus FG1's S on per-galaxy Upsilon, median U 0.50-0.80, with the harness's rms line (value read from the harness in a commit before any formula is graded), and tilt <= 0.15 | as G2, Z_U = distance outside 0.50-0.80 over the bootstrap se of U |
| G5 X-COP holdout | other three clusters | as G3 | as G3 |
| G6 LITTLE THINGS | 19-20 rows | abs(median E) <= 0.10 | median/sqrt(se_boot^2 + 0.075^2), <= 2, 0.075 the record's sE |
| G7 groups | 63 | CONSISTENT, SL1's path | its Z, already stat plus M/L slope in quadrature |
| G8 keys | 15, LW1's path, gas +0.005 and +0, both f*, both h | 15 of 15, per footing | per-key stat Z; G-OUT-M3 Z_tot with M3A1's terms (gas 0.021, slope 0.007, seed 0 since no zoom, m 0.031, n(z) 0.011, leakage 0.079) in quadrature, no shift; joint chi^2 with BA1's R, cut as BA1, ERR passes if p >= 0.05 and M3 Z_tot < 2 and other keys < 2. Other keys have no systematic budget: said so |
| G9 Local Group | X51's classes | every class abs(Z) < 2, on the plain reading and on the algebraic external-field reading g = F(g_N + g_Ne) - F(g_Ne), both reported; both required | same: Z already carries the MC errors |
| G10 IC 1613 | X1 row | abs(Z) < 2 | same |
| G11 Milky Way | X5's 175 cells, form R on F | FEASIBLE IN PRIORS, GD3's classify, UR3's gate | D (scaled so 1 is the 2 sigma edge), <= 1; K_z scale length reported |
| G12 DiskMass | CFG576's data, UR3's estimator, form R on F | r 0.90-1.10, n >= 27, at 1.5 h_R | Z = (r - 1)/sqrt(se_r^2 + sigma_c^2), sigma_c = OD1's c range 1.2-1.9 taken as half-range on r via r proportional to 1/c, <= 2 |
| G13 Bullet | UX6's path, static Plummer map | PASS class at both footings: O1, O2, O3 by UX6's cell grade, position, sign, mass | its Z's, as frozen there |

Form R and the magnitude reading on maps are readings of F, as in LW1 and UX6: F is a scalar rule with no field equation. Vector form: g = ghat_b F. On the Bullet a leaf r is the distance to the nearer BCG, [READING]; that goes in the row. A formula with a leaf not defined on a line's data is **NOT EVALUABLE** there, which is never a pass. **No action or Poisson solve is made for F.**

**Cassini Q2 isn't evaluated:** it needs a field equation F doesn't have. Monopole only, stated. **The law itself fails G1b, about 2500 x at 1 AU, and I expect that to remove every form with a constant a0 tail. That is the owner's gate and it stands. The counts report "fails only G1b" so those rows stay visible,** as a screened tail is a separate question.

## Order of evaluation
Inside the train stage: Saturn point (one number), other Solar System points, X-COP train (20 rows), SPARC subsample (240 rows, BF1's kind), then full train. X-COP precedes SPARC only for cost. Gates are conjunctive, so survivors don't depend on it; cumulative counts are stated in the order run. The prefilter is looser than both readings: X-COP abs(mean) <= 0.30, rms <= 0.40; SPARC subsample rms <= 1.3 x law, abs(median) <= 0.10. All counts past that are upper bounds until the full train gates.

Dear gates G8 (LW1's real path), G11, G13 run only on formulas passing everything before them on either reading, plus the top 5 near misses by Z_max per footing. G8 has a fast tier on SL1's cached linear response, if and only if it reproduces LW1's law row within 0.1 in every Z in a check committed first; else only the real path. Harness code for these gates gets committed before any formula is read on them, with the law's known-answer row first.

## Near misses
Top 200 per footing and tier by Z_max, the largest ERR Z over train gates; top 25 taken through every cheap gate regardless of failing, with margins on both readings. Hits with an infinite or negative value on any row in a gate fail that gate.

## Controls, at the same tolerances
- **Scrambled control:** same search, same caps, same gates and both readings, with g_star/g_gas split, r, Sigma_b, rho_b, Phi_b permuted across rows within X-COP train and within SPARC train; g_b and target kept. Per-gate counts beside the real ones. A real count not clearly above control's goes in the title.
- **Look-elsewhere:** counts reported: expressions enumerated, passing G1a, distinct by value on the evaluation points (N_eff). For any formula passing ERR, p_local from its joint train Z and Sidak p_global = 1 - (1 - p_local)^N_eff, both shown. Real over control reported as the empirical correction. N_eff is an upper bound on independent trials, so this errs conservative.
- **Planted test,** before real: mock target from g = I5(g_b, a0) + pi^2 g_gas^2 / a0 on every train and holdout row. Must be recovered, residual rms < 1e-6, and pass G2-G5 LINE in the search's own output.
- **Known answers:** F = I1(g_b, a0) gives BF1's X-COP +0.4675, 0.4763 within 0.01; SPARC train rms 0.166; LT, groups, dwarfs, IC 1613 match LW1's rows within 0.01 in value and 0.05 in Z (one-point leaves are not used by it); Cassini ratio about 2500 at 1 AU; UX3's row law x (1 + pi^2 g_gas/a0) reproduces UX3's X-COP train and SPARC train numbers within 0.005.
- **MUTATE twin, must fail:** a dimension-check disabled run must be caught by a unit test; X-COP tolerance 1e-6 returns zero; a0 x 1.5 in the known answer must fail its check. Separate outputs.
- **Rerun byte-identical** on a limited chunk set.
- **Independent recheck:** a SURVIVOR gets rechecked by a separately written implementation sharing no code with the search, reading raw files, on every gate it can reach, before any label is published. If it disagrees, the label stands withdrawn.

## Labels, per footing
- **SURVIVOR:** every gate, LINE. Candidate only.
- **WITHIN ERRORS, OUTSIDE A LINE:** every evaluated gate on ERR, misses a LINE.
- **TRAIN ONLY:** G1-G3 pass, later gate fails.
- **FAILS ONLY CASSINI:** all else evaluated passes, G1b doesn't.
- **NO HIT:** nothing passes G1-G3 on either reading.
Unfinished levels are named. A cap or a grammar limit means this is no impossibility statement.

## Expectation, mine, on record
Passing G1 and G2 LINE: exists, 90 %, since SPARC doesn't pin the tail. Passing G1-G3 on ERR: 60 %, since the 0.12 dex budget is wide. On LINE: 25 %. Past G5 on LINE: 8 %. Past G8: 3 %. SURVIVOR: under 1 %. The Bullet is the likeliest last wall, and T, sigma absent is the likeliest honest limit.

## Compute
Lowest priority: at most 2 processes, nice 19, one per footing, one thread each, under 4 GB each. Chunks checkpointed, SIGTERM saves and exits, rerun resumes. Disk is at 20 GB free, so hits are capped at 200 MB per run and logs stay small; a binding cap is reported. BF1, AR1 and the rest keep their cores and aren't touched. Local commits of this lane only. No pushes, no downloads, no deposits.
