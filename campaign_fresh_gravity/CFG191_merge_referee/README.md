# CFG191 -- independent referee of CFG179 (door 11: merging rivers), merge half only

Frozen criteria: `CFG191_FROZEN_CRITERIA.md` (sha256 0cf1ae38..., committed as "CFG191: frozen criteria"), written before any script and before any CFG179 script, `.out` or `.json` was opened. Scope: items (a)-(e) of the peer's list. The swirl half of CFG179 (W1-W5, S-F..S-a0, G5 swirl, GP-B numbers) and CFG179's Chae statistic (M5) are NOT refereed. kappa = 1/2 is FITTED. Nothing here says the theory is closed, and nothing here says the data favour the framework. README numbers of CFG179 were targets, not blind predictions; my hand estimates were made after reading them.

Re-run (from any directory; the repo root is `ZF_REPO` or found by walking up from the scripts): `ZF_REPO=<repo> bash CFG191_run_all.sh`. Expected: every main run exits 0, every `MUTATE=1` run exits 1, then the verdict table and the CFG179 comparison are rewritten. Total about 20 minutes (tier 2: about 4 min main, 2 min MUTATE; Picard check about 3 min per mode).

## Verdict per frozen pass line

| item | pass line | verdict | one-line reason |
|---|---|---|---|
| (a) | A1 six declared points negative, sympy = root-finding, F = cz exact | REPRODUCES | residuals -0.0827, -0.0899, -0.1734, -0.2260, -0.2260, -0.3789 |
| (a) | A2 strict sub-additivity on a 200 x 200 grid | REPRODUCES | P2 and nu_simple: max r < 0 (-0.0185); nu_RAR z is not concave at large z (informational, still negative) |
| (a) | A3 vector form forces linearity | REPRODUCES | 188,876 random 3-D pairs, min ratio 1.6e-4; aligned pairs equal the 1-D residual |
| (a) | A4 "only B escapes" | PARTIAL | true for laws that keep a sqrt regime at the scale; other laws also have zero residual (below) |
| (a) | A5 survival ratios (README line T) | REPRODUCES | within 0.01 of all five 1-D and all five E7 values |
| (b) | B4 E7 + P2 offset +1.309 / +1.275 dex, 5.6 / 5.4 sigma | REPRODUCES | mine +1.308 / +1.274 dex, 5.55 / 5.41 sigma |
| (b) | framing "fails at 5.6 / 5.4 sigma" | PARTIAL | offset over a declared 0.235-dex budget; 2.96-3.24 sigma at the first-infall field; ownership 1.75 sigma |
| (c) | C2 sign: strict-law Q2 above the ceiling for every P2 entry | REPRODUCES | P2 3.63-4.81 x, nu_RAR 4.74-6.29 x |
| (c) | C2 range "4.0-5.7 x" | PARTIAL | a kernel x footing x g_ext-convention range; P2 alone spans 3.63-4.81; no single kernel spans 4.0-5.7 |
| (d) | D1 9/14 vs 6/14 (8 vs 6 on 13) | REPRODUCES | both footings |
| (d) | D4 order kept in every frozen recount variant | REPRODUCES | a tie appears in one variant I added after the freeze |
| (d) | framing "9/14 vs 6/14" as evidence | PARTIAL | 7 of 14 rows differ, sign test p = 0.227; G1 is a convention; two README items are also scorecard rows |
| (e) | E1 arithmetic 5.8-6.5 / 6.8-8.1 / 2.9 sigma_tot | REPRODUCES | 5.76, 6.48, 6.85, 8.10, 2.85 |
| (e) | "Arm A (merge, P2 as modified gravity, full solve)" | DISAGREES | Arm A is the nu_RAR solve; my P2 merge through the frozen estimator is 1.089-1.102 (canonical) and 1.111-1.127 (alt) |
| (e) | "1.08 in the MI form" | PARTIAL | the retired alpha = 1 value; in force 1.0310 |
| (e) | "DR4 decides merge vs ownership" | PARTIAL | true against the unscreened strict law only |

MUTATE outcomes: all seven scripts exit 1 (the controls bite). Two frozen MUTATE expectations were wrong and are kept (see "Failed controls and wrong expectations").

## The requested table: the P2 merge value in the DR4 Arm A geometry (my own code)

Kernel P2 = sqrt(1 + a0/g_N) (nu_RAR beside it for the kernel dependence). Estimator: the frozen pipeline's `bin_medians`, `model_medians`, `fit_gamma`, imported read-only; population, boost solver (one-field AQUAL by Picard), composition grades and debias control are my code (`CFG191_s5b_pipeline_tier2.py`). "floor" = total-mass composition grade, "top" = benchmark-corrected grade (my own exact two-body QUMOND benchmark, f_tm(P2) = 1.46 flat over y = 3-32, f_tm(nu_RAR) = 1.4-1.7). Mean and rms over the 6-seed battery (seeds 4242, 1111, 2222, 3333, 5555, 7777), 30,000 pairs per seed. "point" is sqrt(nu(y_extN)). a0 footings are the pipeline's: canonical 9.36e-11, alt 1.13e-10 m/s^2.

| kernel | a0 footing | g_ext [m/s^2] | floor (rms) | top (rms) | point sqrt(nu0) | floor / top below Arm A floor, in sigma_fit = 0.019 |
|---|---|---|---|---|---|---|
| **P2** | canonical | **1.778e-10 (primary)** | **1.0890** (0.0071) | **1.1023** (0.0102) | 1.1390 | 3.8 / 3.1 |
| nu_RAR | canonical | 1.778e-10 | 1.1596 (0.0117) | 1.1842 (0.0122) | 1.2138 | 0.1 / -1.2 |
| **P2** | alt | **1.778e-10 (primary)** | **1.1113** (0.0040) | **1.1267** (0.0084) | 1.1692 | 4.2 / 3.4 |
| nu_RAR | alt | 1.778e-10 | 1.2046 (0.0120) | 1.2262 (0.0094) | 1.2592 | -0.7 / -1.8 |
| P2 | canonical | 2.146e-10 (variant) | 1.0630 (0.0082) | 1.0772 (0.0066) | 1.1143 | 5.2 / 4.4 |
| nu_RAR | canonical | 2.146e-10 (variant) | 1.1212 (0.0088) | 1.1424 (0.0081) | 1.1749 | 2.1 / 1.0 |
| P2 | alt | 2.146e-10 (variant) | 1.0794 (0.0062) | 1.0990 (0.0100) | 1.1390 | 5.9 / 4.9 |
| nu_RAR | alt | 2.146e-10 (variant) | 1.1468 (0.0064) | 1.1722 (0.0034) | 1.2139 | 2.4 / 1.0 |

- **Control (load-bearing, passed):** my nu_RAR rows at the primary g_ext reproduce the four registered Arm A anchors (1.1614 / 1.1814 canonical, 1.1917 / 1.2267 alt) with deviations -0.0018 / +0.0028 / +0.0129 / -0.0005 (pass line 0.020; the largest is the alt floor). With P2 substituted for nu_RAR the control fails (MUTATE, exit 1).
- **Reading:** a P2 merge through the frozen estimator lands 3.1-4.2 sigma_fit (2.1-2.9 sigma_tot) below Arm A's floor at the primary field. In distance from Newton it is (1.0890 - 1)/0.028 = 3.2 sigma_tot (canonical floor) to 4.5 sigma_tot (alt top), inside the frozen "1.083-1.145, framework-band, arm NOT decided" row. The 5.8-6.5 sigma_tot of the README belongs to the nu_RAR band, not to a P2 merge.
- **Labels:** the estimator's transition-shape parameter is the pipeline's own `y_extN(a0)` (P2 inversion at 1.778e-10) in every row, as frozen; only the injected physics changes. The 2.146e-10 rows are a labelled variant (the preregistration's own alt g_ext is 2.078e-10); the pipeline is not re-tuned for it.
- **Not done:** the real DR4 catalogue and frozen N (mock only); AQUAL for the isolated two-body benchmark (QUMOND, as in the preregistration's own benchmark); the tangential force and the real-sky field geometry (isotropic field direction per system, as the preregistration's own solve does). The AQUAL Picard iteration does not reach its 2e-4 residual in 140 iterations; the boost is stable to 0.2% against 600 iterations (`CFG191_s5c_picard_check.py`).

## (a) The theorem, its premises and its escapes

Script `CFG191_s1_theorem.py`. Reproduced: all checks A1-A5 (17/17).

**Premises (P1-P6, stated by me before deriving):** P1 local single-argument law g = F(z_tot) on the total Newtonian field; P2 difference rule g_int = F(z + z_e) - F(z_e) (universal free fall); P3 "no EFE" means g_int = F(z) for all z, z_e >= 0; P4 F monotone (or measurable, or bounded on an interval), differentiability not needed; P5 aligned 1-D fields suffice for the scalar statement, the vector statement needs P3 for every direction pair; P6 F(0) = 0.

**Derivation:** z = z_e = 0 gives F(0) = 0; P3 is Cauchy additivity on the half-line, so F(qx) = qF(x) for rational q, and P4 gives F(x) = F(1) x. If F is C1, differentiating P3 in z_e gives F'(z + z_e) = F'(z_e), F' constant. Strict concavity with F(0) = 0 gives strict sub-additivity: one sign of the residual (suppression) for every strictly concave F. P2 has F'' = -1/(4 (z^2 + z)^(3/2)) and F'(0+) = infinity (sympy). Without P4, non-measurable (Hamel-basis) solutions exist (from memory, unverified).

**Vector form:** a continuous additive G: R^3 -> R^3 is linear, and rotational covariance then forces G = c*Id. So the vector form also forces linearity; without the isotropy premise every linear map A survives (anisotropic linear laws, V^2 ~ M, not sqrt-like). Numerically: P2 fails additivity on all 188,876 sampled pairs (min |R|/|G(a)| = 1.6e-4).

**Exactly which laws escape (residual test and small-z slope, from A4):**

| law | residual max abs(r)/F | small-z slope | note |
|---|---|---|---|
| ownership composition g_int = F(z), F = P2 | 0 | 0.500 | nonlocal; keeps a sqrt regime: the only escape that does |
| anisotropic linear G = Ax | 0 | 1.0 | local; V^2 ~ M; no BTFR |
| linear-in-source, any kernel (F = cz) | 4e-14 | 1.0 | local; V^2 ~ M |
| screened F = z + (P2 - z) s(r/xi), r/xi = 0.01 | 9e-4 | 0.955 | r-dependent; the Arm B / chain class; residual -> P2's (0.90) as r/xi -> infinity |
| E7 (MI worldline composition) | not zero | 0.5 | outside P2's difference rule; still has an EFE (survival 0.12-0.99) |
| explicit EFE term in the composition | by construction | | not covered |
| Hamel-basis Cauchy solutions | | | excluded by P4 |

**"Only B escapes":** it holds within CFG179's own scope (a law that keeps a sqrt regime at the scale in question, local total-field argument, difference rule): only an ownership-type nonlocal composition has zero residual and a sqrt regime together. As worded in the README and LEDGER it FAILS as a complete statement: (i) it omits P2 (difference rule), P4 and the vector case, none of which CFG179's M3 states (its M3a uses differentiability only); (ii) screened / r-dependent laws (the preregistration's Arm B and derivation chain) and linear-in-source laws also have zero or vanishing residual, by not having the sqrt pull at that scale. CFG179's own S1 verdict text says "unless the boost is keyed to something other than the local total flow", which is broader than "only B". Class: framing / omission, not a numerical difference. The theorem is textbook-level (MOND-type laws violate the strong equivalence principle; from memory, unverified as a citation).

## (b) Coma UDGs

Script `CFG191_s2_coma_udg.py` (12/12). Controls: reconstruction of g_bar, g_obs within 0.02 dex; isolated nu_RAR offset +0.3962 (tsv) / +0.3965 (reconstruction) against L23's +0.3965; E7 cubic re-derived by sympy; L23's budget entries recomputed to 0.2355.

Reproduced: E7 + P2 at 0.845 a0: **+1.308 / +1.274 dex = 5.55 / 5.41 sigma** (CFG179 +1.309 / +1.275, 5.6 / 5.4). The 0.001-dex difference is numerical (constants: Msun, G, kpc; 0.2355 vs 0.235). Field sweep (canonical): 0.427 a0 4.94 sigma, 0.653 5.35, 0.845 5.55, 1.059 5.70; alt 4.71-5.58. Isolated P2 (ownership, no infall gas): +0.413 / +0.372 dex = 1.75 / 1.58 sigma.

Which inputs are measured and which are model-dependent (frozen classification): measured are sigma_obs, R_e, L and the projected distance. Model-dependent are M/L (SSP), the sigma-to-g estimator, the 3-D position, the Coma mass profile and hence g_ext (beta model + closure inversion, L23, taken as an input), E7's theta_0 = sqrt(2) (postulated), the kernel and the 0.235-dex budget.

Qualifications (framing): the "sigma" is offset over a declared systematic budget (M/L 0.148, aperture 0.120 dominate). Over the statistic alone the same offset is 21 sigma; over the EFE-term budget 0.128 it is 7.0 sigma. At L23's first-infall field (0.112 a0) the E7 offset is +0.763 / +0.698 dex = 3.24 / 2.96 sigma. Per-galaxy fields (each galaxy at its Einasto distance) give 5.37 / 5.20 sigma. Jackknife 5.24-5.65 sigma; dropping DF44 raises it. The offset closes at an M_* multiplier of 21.5 (SSP range 0.37-1.48). CFG179's README explanation of the gap to L23's nu_RAR row (about 0.13 dex: P2's missing tail plus one field value) is reproduced as an identity: 1.308 (E7, one field) - 1.155 (nu_RAR, per-galaxy sphere coupling, my reproduction of L23's +1.159) = 0.042 (one field vs per-galaxy) + 0.025 (E7 vs sphere coupling) + 0.085 (kernel).

## (c) Solar-System quadrupole

Script `CFG191_s3_solar_q2.py` (8/8). Which quantity: the external-field quadrupole Q2 of a point Sun in the Galactic field, QUMOND, against Q2 <= 5.2e-27 s^-2 (Park+2026 as quoted in the repo).

My own derivation: QUMOND phantom density, interior quadrupole coefficient, two routes (direct divergence by sympy; integration by parts). With the Q2 normalisation of eq (10) and no fitted constant they reproduce the published nu_RAR anchors q(1) = 0.094, q(1.5) = 0.159, q(2) = 0.221 to 0.76%, 0.31%, 0.00% and the in-repo reference row 5.772 / 6.286 (g_ext 2.146e-10) to 1.5%; the two routes agree to 3%.

| Q2 / ceiling | canonical, 1.778e-10 | canonical, 2.146e-10 | alt, 1.778e-10 | alt, 2.146e-10 |
|---|---|---|---|---|
| P2 | 3.63 | 4.22 | 4.09 | 4.81 |
| nu_RAR | 4.74 | 5.77 | 5.08 | 6.29 |

Reproduced: the FAIL of the strict law, for every kernel, footing and g_ext convention tested (the rescue field is 0.25-0.26 of V^2/R0). The natural scale a0/r_M = 7.86e-26 s^-2 = 15.1 x (canonical), 20.1 x (alt) is reproduced. Partial: "4.0-5.7 x" is a kernel-mixed range (P2 alone 3.63-4.81, nu_RAR 4.74-6.29); its origin is the nu_RAR QUMOND computation (5.77 / 6.29 at 2.146e-10), and CFG172 (C5) records that an earlier description of the same number as the Milky Way host tide was wrong. Class: framing (a cited range, not recomputed by CFG179) plus numerical. Not covered: AQUAL, E7's Q2 (no field equation), the 3-D geometry, Jupiter (0.05%, quoted). The monopole (a0/2, 1279 x the Earth bound) and the host tide are different quantities.

## (d) The scorecard

Script `CFG191_s4_scorecard.py` (6/6); sigma values parsed from the committed `CFG7_hierarchy_fg001.out`, not recomputed.

- Reproduced: 9/14 vs 6/14 on both footings, 8 vs 6 on the 13 physical rows.
- Row classes: tie-pass G2, G3, G10, G12; tie-fail G5, G6, G7; discriminating G1, G4, G8, G9, G11 (ownership) and G13, G14 (rival). Only 7 of 14 rows differ; one-sided sign test on them p = 0.227 (0.344 without G1).
- Flags: G1 is a declared convention (the rival's "inf FAIL"; ownership passes because the Sun owns no phantom). Data-sharing pairs: (G5, G6), (G9, G10), (G11, G12), (G13, G14). Rival scored at its best variant on G8-G11. Post-hoc: only H8 (fossil gas, outside the 14) is stated post hoc; whether the class-A rule was formed after h43 / f13 could not be checked from the documents I read (not scored).

| recount (ownership vs rival) | canonical | alt |
|---|---|---|
| all 14 rows, 2.0 sigma (CFG7) | 9 vs 6 | 9 vs 6 |
| without G1 (13) | 8 vs 6 | 8 vs 6 |
| discriminating rows only (7; 6 without G1) | 5 vs 2 (4 vs 2) | 5 vs 2 (4 vs 2) |
| dedup (drop G6, G10, G12, G14; 10 rows; 9 without G1) | 7 vs 3 (6 vs 3) | 7 vs 3 (6 vs 3) |
| threshold 2.5 sigma | 9 vs 7 | 11 vs 7 |
| threshold 3.0 sigma (13 rows) | 11 vs 8 (10 vs 8) | 11 vs 7 (10 vs 7) |
| **with all flagged rows out** (G1, G6, G8-G12, G14; a variant I added after the freeze) | **3 vs 3** | **3 vs 3** |
| column swap (control) | 6 vs 9 | 6 vs 9 |

The order is never reversed in a frozen variant; leave-one-row-out margin +2 to +4. With every flagged row removed it is a tie, which is not a reversal but is the only variant that does not favour ownership. Framing: the count is threshold- and row-dependent; two of the README's "against committed tests" items are rows inside it (Chae = G13 + G14, Solar System = G1); Coma UDGs and DR4 are not rows; the rival is the record's 1-D QUMOND recipe (h43 / Famaey-McGaugh 2012 eq 60), not E7 and not exactly F(z + z_e) - F(z_e).

## (e) The DR4 mapping against the preregistration

Scripts `CFG191_s5_dr4_mapping.py` (10/10), `CFG191_s5b_pipeline_tier2.py` (8/8), `CFG191_s5c_picard_check.py`. The preregistration was read-only; every quoted number was string-matched in the frozen file.

- **What Arm A is:** "the full nonlinear AQUAL-EFE solve of the frozen kernel taken as modified gravity with no coherence length" (Amendment 11(a)); the solve script names the kernel: Route A, nu_RAR = 1/(1 - exp(-sqrt y)), y_extN = 1.28903 / 0.99240 (`aqual_efe_full_solve_2026.py`). P2 has y_extN 1.4647 / 1.1513 and sqrt(nu) = 1.139. CFG179's control C3 reproduces the section-1.1 P2 numbers, not the Arm A solve. Kernel label: DISAGREES. Result above: a P2 merge is 1.089-1.102 (canonical), 1.111-1.127 (alt). Class: definition (kernel label).
- **What gamma-hat means:** the deep-regime velocity-boost asymptote gamma_inf of the frozen estimator (median vtilde in 8 log-y bins, single-parameter profile fit with the frozen transition shape); frozen sigma_fit 0.019, sigma_sys 0.02, sigma_tot 0.028; "consistent" |z| < 2, "disfavored" |z| > 3.
- **Arithmetic (E1):** (1.1614 - 1)/0.028 = 5.76, 6.48, 6.85, 8.10 and 2.85 for 1.0799: reproduced. Class: none.
- **MI form:** 1.0799 is the alpha = 1 orientation-average (Amendment 2), retired by Amendment 3 (alpha = 2), corrected by Amendment 4 to 1.0310 (range 1.0218-1.0472); MI-as-fundamental was closed by Amendment 9. CFG179 labels its value "Amendment 2, alpha = 1", so the label is accurate; it is a retired number used as a live comparison. Class: framing.
- **Screened merge-type readings (omitted by the mapping):** Arm B (screened, carrier, xi >= 4 pc): 1.0000 +- 0.0025 (Amendment 12); the derivation chain's law (two-field AQUAL with the P2-based kernel J_P2 and a heat filter): ceiling 1.0725 / 1.0900, falling onto Newton at larger xi (Amendment 14). CFG179's M7 states "every merging-river composition predicts a boost (gamma > 1); only the no-merge rule (Arm C) predicts 1.000". That is false as a universal claim. The same unscreened law is used twice: as the G5 FAIL and as the DR4 prediction; the screened variant that passes G5 predicts at most 1.0725 / 1.0900 (chain) or 1.000 (Arm B). Class: framing.
- **Orientation of the axes:** CFG179's quoted P2 "perpendicular 1.139 / parallel 1.017" are the algebraic (MI-type) eigenvalues. The Poisson-solved MG tensor (QUMOND or AQUAL) has B_par = nu0 and B_perp = nu0 (1 + L/2) (QUMOND) or nu0 / sqrt(1 + L0) (AQUAL): for P2 canonical B_par = 1.2973, B_perp = 1.1657 / 1.1582. The sphere averages agree: 1.0975 (AQUAL, sqrt of the average of B) against CFG179's 1.0998. Class: definition; no effect on the estimator-level number.
- **What DR4 can decide under the mapping:** the mapping adds no decision row (every CFG179 DR4 number equals a value already registered). Arm A vs Arm C is 5.8 sigma_tot apart; Arm B and Arm C are the same number (0 sigma_tot) and equal Newton on this estimator; the chain's ceiling is 2.6 sigma_tot above 1.000 and a P2 merge (mine) 3.2-3.7 sigma_tot above it (canonical, primary field, floor / top; 4.0-4.5 alt). A Newtonian result kills Arm A only and does not favour ownership over Newton, Arm B or a screened merge (Amendment 13(e) says so itself). A high result (>= 1.084 with the frozen stability conditions) kills Arm C and Arm B (not the chain below 1.157). So "DR4 decides" holds for {unscreened strict merge} against {ownership, screened merges, Newton}, and a P2 merge lies in the "arm not decided" band, where it cannot be told from MI-form or chain readings by the frozen statistic.

## CFG179 numbers beside mine (`CFG191_compare_cfg179.out`, opened only after my runs were saved)

CFG179's `s1` and `s2` text outputs were read. Residuals agree to the printed digits; Coma offsets differ by 0.0014-0.0017 dex (constants); the natural scale and the scorecard are identical. Differences by class: numerical: Coma offsets, sigma rounding (5.6 vs 5.55); definition: the Arm A kernel, the orientation of the point-field axes; framing: "only B escapes", "5.6 / 5.4 sigma fails", "4.0-5.7 x", "9/14 vs 6/14", "every merge predicts gamma > 1", "DR4 decides"; scoring convention: G1's "inf" and the 2.0-sigma line; README typo: none found. CFG179's remark that the quadrupole coefficient is "about 0.3-0.4 of a0/r_M" is a rounding of 4.0/15.1 = 0.26 and 5.7/15.1 = 0.38; mine is 0.24-0.32 for P2 at the canonical scale.

## Failed controls and wrong expectations (kept, not repaired)

- s1 first run (`CFG191_s1_theorem_firstrun.out`): check A4c (screened residual -> 0) failed on a threshold I set inconsistently (9.04e-4 against 9.0e-4); loosened to 10 % of the large-r/xi value after the freeze; the physics is unchanged.
- s2 first run: the L23 string check failed on whitespace; normalised. Frozen M4 ("g_obs x 10^1.3") has the sign wrong (raising g_obs widens the offset): as frozen it does NOT bite (offset +2.61 dex, 11 sigma); the corrected sign (x 10^-1.3, offset +0.008) bites and is labelled a deviation. M3 bites as frozen.
- s4 first run: my added "all flagged rows out" variant produced a tie 3 vs 3 and made the original strict-order check fail; the check was split (frozen variants LB; the added variant reported as a finding). Frozen M6 (G1 rival pass, rival threshold 2.5 on G9) gives 9 vs 8, not the 8 vs 8 I wrote: as frozen it does NOT bite; M6' (G1 forced, rival at 3.0 sigma against ownership at 2.0) gives 9 vs 9 and bites.
- s5 first run: two check-design defects (the preregistration's "> " quote markers broke a whitespace match; the README's rounded 8.1 vs 8.11). Fixed; first run kept.
- Frozen E2 grouped "QUMOND/MI tensor (perp = nu, par = d(y nu)/dy)". My derivation shows the Poisson-solved QUMOND tensor is parallel-dominant (B_par = nu0); only the local algebraic (MI-type) tensor is perpendicular-dominant. Frozen text wrong; kept.
- Hand estimates: H-a1..a3, H-b1, H-b2, H-b4, H-c1, H-c2, H-d1, H-e1, H-e2 held. H-b3 (first infall 3.0-3.5 sigma): canonical 3.24 held, alt 2.96 is just outside. H-e2 (P2 near 1.09-1.11, below the floor): crude transfers gave 1.090-1.124 (canonical); the pipeline-grade value is 1.089-1.102.
- In (c) the frozen plan expected a fitted normalisation constant; none was needed (eq 10 reproduces the anchors directly).
- The tier-2 estimator uses the pipeline's a0 footings (9.36e-11 / 1.13e-10); scripts s1-s3 use CFG179's charter footings (9.3603e-11 / 1.1312e-10). Both are stated.

## Where independence stops, and what was NOT tested

Independence stops at: the Q2 definition and the published q anchors and ceiling (in-repo, second-hand); L23's external-field table and 0.235 budget (inputs); the CFG7 sigma inputs (parsed); the preregistration's numbers and its frozen estimator, error model and master population (imported or quoted read-only); constants; and facts from memory, unverified (SEP violation of MOND-type laws; existence of non-measurable Cauchy solutions).

NOT tested: Amendments 5-8, 15-17 and preregistration section 2 were not read; the swirl half of CFG179 (all of W1-W5, S-F, S-u, S-j, S-Lambda, S-a0, the swirl G5, the GP-B numbers); CFG179's Chae statistic (M5) and its post hoc variants; the CFG7 data themselves; AQUAL and E7 Solar-System quadrupoles; the real DR4 catalogue; whether the class-A ownership rule was formed after the data; CFG179's scripts, `_MUTATE` and `_firstrun` files (only the s1 and s2 main `.out` text was read, for the comparison).

## Files (all in this directory, all named CFG191_*)

`CFG191_FROZEN_CRITERIA.md`, `README.md`, `CFG191_common.py`, `CFG191_s1_theorem.py`, `CFG191_s2_coma_udg.py`, `CFG191_s3_solar_q2.py`, `CFG191_s4_scorecard.py`, `CFG191_s5_dr4_mapping.py`, `CFG191_s5b_pipeline_tier2.py`, `CFG191_s5c_picard_check.py`, `CFG191_verdict.py`, `CFG191_compare_cfg179.py`, `CFG191_run_all.sh`; for each script `<name>.out`, `<name>_results.json`, `<name>_MUTATE.out`, `<name>_MUTATE_results.json`; first runs kept as `<name>_firstrun.out` and `_firstrun_results.json` for s1, s2, s4, s5; `CFG191_verdict.out`, `CFG191_compare_cfg179.out`, `CFG191_run_all.out`.

## In-place re-run (orchestrator)

`bash CFG191_run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`): every main run (s1-s5, s5b, s5c) exits 0 and every `MUTATE=1` run exits 1; the verdict script and `CFG191_compare_cfg179.py` (opened after all of the above were saved) exit 0. Every `_results.json` is identical to the referee's; every `.out` differs only in timing lines (elapsed seconds). The referee's `.err` files for s5c were not in its directory; the ones here are this re-run's. The frozen criteria are `../CFG191_FROZEN_CRITERIA.md` (157894552). This lane refereed the merge half of CFG179 only; the swirl half and its Chae statistic, Amendments 5-8 and 15-17 and preregistration section 2 were not read or refereed.
