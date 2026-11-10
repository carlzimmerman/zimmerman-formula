# MK1 RESULT: one dust constant mu_K? NO VALUE / NO VALUE (canonical / alt). The answer does not turn on the cap.

Criteria b1fbded1e2 (committed alone before any script or number). AMENDMENT A1 916f4e0e22 (which capped state to use;
committed alone before any graded number). TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing.
Footings never pooled. kappa = 1/2 FITTED; not theory closed.

Commit ids: in the shared checkout, criteria b1fbded1e2, A1 916f4e0e22, result 0ca085a0af. On origin, criteria
11f43f9490, A1 b076803437, result 204ef24ac1.

## Label

**NO VALUE / NO VALUE.** With the quadratic K(Q) of action (A), read as form B, no single mu_K is allowed by the CMB,
clusters and galaxies together, on either footing. All 16 known answers pass.

- **The rows that do not meet.** The CMB needs mu_K >= 2.51e4 per Mpc for its lensing shape (KD1's Jeans line on
  QX3's machinery). It needs >= 198 just for the component to be cold by z 3400 (KD1's B1a). Every galaxy, group and
  Solar-System row ends far below that. KiDS ends at 1.00 / 0.77, groups at 1.51 / 1.38, SPARC at 7.1 / 5.6 and Saturn
  at 6.2e3. The binding pair is the Jeans line against KiDS, a factor of **2.5e4 / 3.3e4**. The CMB's background line
  against KiDS is a factor of 198 / 259. The Jeans line is 4.0 times above even the Saturn line.
- **X-COP has no value at all.** On the action's own static equation, no mu_K from 1e-3 to 1e4 per Mpc passes G-X on
  either footing. The closest miss is rms 0.263 / 0.255 at mu_K 1.35 / 1.26, against the 0.10 line.
- **The cap does not change the answer.** Without it, KiDS allows no mu_K at all (even mu_K = 0 fails ONE1's gate on the
  own halo). With it, KiDS allows up to 1.00 / 0.77 per Mpc. The CMB rows sit two to four orders of magnitude above
  every galaxy row either way.
- **Without the CMB rows there would still be no value.** Groups, KiDS, SPARC and Saturn do share a narrow window
  (0.91-1.00 / 0.76-0.77 per Mpc), but X-COP has none. In that window the groups' dust is also 2.1 to 3.2 times the
  share form B allows a group (RB1's conservation reading, reported).

**What a dust term would have to do differently (a requirement only).** The clock offset Q - 1 is about 1e-6 both in
the expanding background at z 3400 and in a galaxy well today. At that offset the term must be stiff in the expanding
background (a Jeans length below 0.25 kpc, mu_K >= 2.5e4) yet nearly inert in a static well (mu_K <= 1, so about 6e8
times softer in mu_K^2). So it cannot depend on the clock offset alone.

## The table (per Mpc, physical; canonical / alt)

| row | allowed mu_K | gate, and the lane it comes from | quality |
|---|---|---|---|
| 1 CMB and background | >= 198.25 / 198.24 | w(z 3400) <= 0.01: KD1 B1a on QX17's FRW w(a) | background line, not a likelihood (row notes) |
| 2 clustering scale | >= 2.512e4 / 2.512e4 | CMB-lensing Jeans line: KD1 G9a on QX3 iter2 (CLASS, PR4, Delta chi^2 <= 4) | record value, not recomputed |
| 3 X-COP | **none** (0 of 701 grid values) | G-X (\|mean\| <= 0.05, rms <= 0.10): QX2 builder, QX6 back-reaction, action-exact dust | computed |
| 4 groups | 0.912-1.514 / 0.759-1.380 | QX5's group gate (stars 0..gas bracket meets +-0.05) | computed; power-law HSE potential, zero at 3 R200 |
| 5 SPARC | <= 7.08 / 5.62 | QX8's grader and line (rms <= 0.110, median U 0.50-0.80) | computed; dust spherical, plus QX8's exact-field T |
| 6 KiDS host-free, capped | <= 1.00 / 0.765 | ONE1's frozen gate at the 1.6 R_h veto, neighbours, k fitted | computed |
| 7 Solar System | <= 6.22e3 / 6.22e3 | Saturn 7.0e-15 m/s^2 and Q2 9e-27 s^-2: EW2 iter4 | closed form |
| **all rows** | **empty / empty** | binding: row 2 against row 6, factor 2.5e4 / 3.3e4; row 3 empty | |

Row 8 (reported, not graded) is in the row notes.

## What the cap changes

- **KiDS (row 6).** This is where the cap matters.
  - Without the cap: the law with no end plus the dust, with S4's zero point, own halo only, run through ONE1's
    statistic. It fails at every grid value, including mu_K = 0. At mu_K = 0 the late types sit at -2.14 / -2.16 sigma.
    At 0.1 per Mpc the dust's outer mass gives R_s 1.36 / 1.33 against the data's 0.81 (z -4.1 / -3.8). The old bound
    was S4's guard, |v3/law - 1| <= 0.14 on Brouwer+21's bins, which held at 0.03 and failed at 0.1.
  - With the cap: total charge (halo plus dust) ends at PD1's 59.5 M_b. Then the dust cannot add mass. It only moves
    the share inward, so the end radius shrinks: x_c = 57.5 / 31.5 / 9.8 r_M at m = mu_K r_M = 1e-3 / 1e-2 / 0.1.
  - KiDS accepts that up to 1.00 / 0.77 per Mpc. Beyond, the outer windows empty: R_s falls from 1.00 to 0.57 at 1.13
    (canonical) and the early types fail first (+2.05 sigma).
  - Reported: the capped model's z for all lenses crosses zero near mu_K 0.4-0.7. Pulling the share inward mimics a
    smaller share; ONE1's X = 53.6 bracket read the same way. This is a degeneracy between share and mu_K, not a
    measurement of mu_K. M-2X shows it from the other side: with the share doubled, mu_K = 0 fails and only mu_K near 1
    passes.
- **SPARC (row 5).** Here the cap tightens the bound a little. Capped: <= 7.08 / 5.62. Uncapped with S4's zero point:
  passes at 10 and fails at 30 (coarse grid). At these mu_K the uncapped potential has already turned over near
  (r_M/mu_K^2)^(1/3), so it is shallower inside the disc than the capped halo's, which runs out to about 60 r_M.
- **Groups and X-COP (rows 3, 4)** use QX2's zero point (3 R200), as frozen. The cap enters only through RB1's
  conservation reading of the groups (above). The X-COP row is empty on both zero points tried (3 R200 and 10 R200).
- **The CMB rows (1, 2)** have no cap in them. That is why the cap cannot close the gap.

## What this lane does not settle

- **The collapse.** Only static states are graded. Whether a falling clock ever reaches the static capped state is
  COL1's question (`fable52_push/COL1_clock_collapse/`, not touched).
- **A non-quadratic K(Q).** Only mu_K^2 (Q - 1)^2 is graded. The requirement sentence above says what another K would
  need. Nothing is designed here.
- **Rows graded with a stand-in.**
  - Row 1 uses KD1's background line, not the CMB likelihood (row notes say why).
  - Row 2 is the record's CLASS number, not recomputed.
  - Row 5 treats the dust as spherical, in the algebraic law, added to QX8's exact-field correction.
  - Rows 3 and 4 put Phi's zero point at 3 R200 (QX2's choice); the groups' potential comes from a two-point power law.
  - Row 6's uncapped reading has no neighbours (the law with no end has no finite neighbour halo). Its zero point is
    S4's.
  - M-2X on row 6 is the own halo only (below).
- **Spherical symmetry and statics throughout**, except the KiDS projection.

## What this lane finds wrong in FB1, QX2 and the brief

1. **FB1 section 2 item 1:** "dust by recombination needs mu_K of at least a few per Mpc (w0 ... below 1e-9)".
   - The w0 arithmetic is right: 1.0631e-8 / mu_K^2 at H0 70 and Omega_c 0.26 (KA4, and Lean `fb1_arith`).
   - The line is wrong. At z 1100, a^3 = 7.5e-10, so w0 = 1e-9 gives w = 0.57: not dust.
   - Cold by z 1100 (w <= 0.01) needs mu_K of about 37. The record's own line, cold by z 3400 (KD1 B1a), needs 198.
   - Neither is the binding CMB number. The CMB-lensing Jeans line needs 2.5e4 (KD1, QX3), and BBN needs 8.9e6 (KD1).
2. **FB1 item 3 and QX2 iteration 5:** "the K(Q) dust needs mu_K 1.78 / 1.74 per Mpc to close it".
   - That is only where the mean Delta is zero. At no mu_K does the shape pass (rms >= 0.263 / 0.255; QX6 already
     said so for QX2's form). So the dust does not close X-COP at any mu_K.
   - QX2 also added the dust unboosted: M_model = law(M_b) + M_K. In the action's static equation the dust is a source
     of the law: r^2 mu(g/a0) g = G (M_b + M_K). Done that way, the mean-zero value is 1.53 / 1.46.
   - QX2 called its form generous. It is not, in this respect. QX2's FAIL stands, because no value passes either way.
3. **QX2 iteration 5, FB1 and the brief:** "the record's galaxy-lensing bound is mu_K <= 0.1 per Mpc (S4)".
   - 0.1 is S4's first failing grid value: S4's guard held at 0.03 and failed at 0.1 (max \|v3/law - 1\| 0.29 against
     0.14). The bound lies between 0.03 and 0.1.
   - S4's guard is a model-against-model line (the dust model against the law) on Brouwer+21's four mass bins. It was
     not graded against KiDS's pooled outer points.
   - "17-18 times the galaxy bound" should read "18 to 60 times".
4. **The brief's hope that this lane could close two open items at once.** The cap does raise the galaxy-lensing bound
   on mu_K, from S4's 0.03-0.1 to ONE1-statistic values of 1.00 / 0.77. But the CMB needs 2.5e4, and X-COP has no
   value. So the two items stay open.

## Row notes

**Row 1 (CMB and background).** w(a) = w0/(w0 + a^3), w0 = I0/(4 mu_K^2), I0 = 4.037e-8 Mpc^-2 per footing (kd1.json, from
QX15's omega_d at h 0.674). Cold by z 3400 (w <= 0.01, KD1's B1a) needs mu_K >= 198.25 / 198.24; it reproduces KD1's
value to 1e-6 (KA7). For comparison, w <= 0.01 at z 1100 needs about 37. The component turns dust-like (w = 1/2) at
1 + z = (4 mu_K^2 / I0)^(1/3): 463 at mu_K 1, 1.57e4 at 198, 3.97e5 at 2.51e4. Reported beside, not graded: BBN (KD1's
B1b) needs 8.89e6.
Why not the CMB likelihood: the record's primary-CMB machinery (F1A + PJ1's CamSpec-2500 reader, as WD1 G7 ran it)
carries a smooth c_s^2 = 1 component through CAMB's tabulated-w fluid. The stiff partner rho_d0 w0 a^-6 could be written
that way, but it exceeds radiation for a below a_x = sqrt(Omega_d w0 / Omega_r): a_x = 2.7e-5 at mu_K 198, 2.2e-7 at
2.51e4, 6e-10 at 8.9e6. That is inside the radiation era where CAMB sets its adiabatic initial conditions on a
radiation-dominated background. The machinery cannot take this w(a) without changing its early-time set-up, so row 1 is
graded on KD1's background line. Quality: a background line, not a likelihood. It does not bind: row 2 is 127 times
higher.

**Row 2 (clustering scale).** The quadratic K(Q) is an n = 1 polytrope with a fixed physical Jeans wavenumber mu_K (QX3,
Lean). The record's CMB-lensing Jeans line is mu_J = 2.512e4 per Mpc on both footings (KD1 G9a on QX3 iter2's CLASS
machinery; QX3's bracket corners give 2.51e4 to 3.98e4). There lambda_J = 2 pi/mu_J = 0.25 kpc physical. The comoving
Jeans wavenumber mu_K/(1 + z) is 7.4 per Mpc at z 3400 and 22.8 at z 1100. The sound speed at the mean density is
336 km/s at z 3400 and 1.7e-3 km/s today. Closed-form stand-ins (reported): growth on k <= 0.2 h/Mpc from z 3400 needs
mu_K >= 458; the forest's k <= 3 h/Mpc from z 3400 needs >= 6.9e3. The CLASS value binds. Quality: the record's value,
not recomputed here.

**Row 3 (X-COP).** QX2's builder (7 clusters, 35 points), G-X unchanged. The graded model is the action's own static
equation, r^2 mu(g/a0) g = G (M_b + M_K): the dust is a source of the law, so the law boosts it. Phi is the potential of
the measured M_HSE with its zero at 3 R200 (QX2's psi_profile, QX6's back-reaction). On the 701-point grid from 1e-3 to
1e4 per Mpc, no value passes on either footing. The closest miss is rms 0.263 / 0.255 at mu_K 1.35 / 1.26 (line 0.10). The
mean is zero at 1.53 / 1.46, where the rms is 0.270 / 0.262. The zero at 10 R200 does worse (min rms 0.307 / 0.296).
QX2's additive form reproduces QX2 exactly (KA1: +0.4644 / +0.4317 at 0.1, mean zero at 1.778 / 1.736). It also has no
pass (min rms 0.271 / 0.262, as QX6 found).

**Row 4 (groups).** 20 Lovisari groups at R2500 and R500, stars bracketed from 0 to the gas mass. Phi is the potential of
a power-law M_HSE through the two measured points, with its zero at 3 R200. At mu_K = 0 the lane reproduces QX5's
bracket, [+0.196, +0.359] / [+0.158, +0.320] (KA9). The bracket meets [-0.05, +0.05] for mu_K in 0.912-1.514 / 0.759-1.380.
**RB1's conservation reading (beside, not graded):** at those values the charge (M_model - M_b) at R500 is 2.1 to 3.2
times the groups' share 5.41 M_b. So the dust that rescues the groups' amount is two to three times more than form B
lets a group hold.

**Row 5 (SPARC).** QX8's grader, mask, weights, U grid and line, with QX8's exact-field T plus the dust's T_K. At
mu_K = 0 it equals QX8: 0.0560 @ 0.58 / 0.0558 @ 0.52 (KA3). It passes up to 7.08 / 5.62 per Mpc (0.05-dex grid) and
first fails at 7.94 / 6.31. There the dust inside the last point is 17 / 10 times the baryons in the worst galaxy. The
canonical line breaks on rms (0.119); the alt line breaks on U (median 0.49 < 0.50, rms 0.1025). QX6's stricter recheck
line (rms rise <= 0.01, mean shift <= 0.02) holds up to 3.55 / 3.16.

**Row 6 (KiDS host-free, capped).** ONE1's machinery unchanged except the profile: each lens and each neighbour carries the
capped, dust-included profile at its own m = mu_K r_M(k M_b) (own halo by a 2-D table in log u and log m; neighbours by
46 kernel tables in log m). At mu_K = 0 it reproduces ONE1's graded numbers exactly (KA2; tables match ONE1's to 2.4e-6 /
4.8e-7, KA6).
  - Canonical: passes at 0, 0.03, 0.1, 0.3 and 1.0; fails at 1.13, 1.28, 1.44, 2.08, 3 and 10. Upper bound 1.00.
  - Alt: passes up to 0.765; fails at 0.875, 1, 3 and 10. Upper bound 0.765.
  - The first line to break is always the early types. Canonical at 1.13: z +2.05, model R_s 0.567 against data 0.811,
    k 1.40. Alt at 0.875: z +2.01, R_s 0.564 against 0.809.
  - Up to 0.1 per Mpc nothing moves (R_s 1.003 to 1.005 canonical). The dust is boosted by the law, but the cap absorbs
    it: the share ends sooner, and the total stays 59.5 M_b.
  - The fitted mass factor k falls as mu_K grows (2.50, then 1.55 at 1.0, then 0.32 at 10), because the share collects
    at small radii and fills the inner window. On the capped branch mu_K r_c tends to about 1.55 (A1). So at large mu_K
    the whole share sits in a dust core of radius about 1.55/mu_K.
  - Peak memory 1.57 GiB (1.68 GB by /usr/bin/time), slightly above the brief's 1.5 GB. Neighbour pairs are streamed
    per lens chunk. One KiDS point takes about 160 s.

**Row 7 (Solar System).** EW2 iter4's closed form: the dust at the Sun gives dg = mu^2 (G M_sun / 2 + Phi0 R_Saturn / 3)
with Phi0 = (600 km/s)^2. The Saturn line (7.0e-15 m/s^2) allows mu_K <= 6223; the Q2 line allows <= 8451. The lane
reproduces EW2's 7.5e-14 at 2.04e4 (KA8). With a capped Milky Way potential at the Sun ((401 / 415 km/s)^2, reported) the
bound is 9.3e3 / 9.0e3.

**Row 8 (consistency; reported).**
  - **(a) Where the static dust alone would exceed the share.** This uses the dust-free capped potential, integrated to
    r_c. Canonical, at log M_b 8 / 9 / 10 / 11 / 12: 64 / 20 / 6.4 / 2.0 / 0.64 per Mpc (alt 71 / 22 / 7.1 / 2.2 /
    0.71). With the 5.41 share, at log M_b 13 / 14: 1.9 / 0.60 (alt 2.1 / 0.66). So at the groups' window (about
    1 per Mpc) the dust alone would already exceed the share of a 1e12 galaxy and of a 1e14 cluster. M-2X halves these.
  - **(b) The capped branch at each row's value** (log M_b 9-11, canonical; `mk1_row8.out`).
    - The dust's own mass is 0.2-5 % of the share at 1 per Mpc and 3-34 % at SPARC's 7.08.
    - It is 68-99 % at the background line (198). There r_c is 6-8 kpc, against a dust-free 73-732 kpc.
    - At 6.2e3 and at 2.5e4 it is all of the share, in a core of 0.25 kpc and 62 pc.
    - mu_K r_c never exceeds 1.554, so a Jeans wavelength 2 pi/mu_K never fits inside the capped state.
  - **SCS1's reading.** SCS1's growing band, k < mu_K / sqrt(1 - K m), therefore never resolves inside the capped
    state (its WKB route needs k r >> 1). SCS1's own labels stand: STABLE at mu_K 0 and 0.1, JEANS-ONLY at 8.9e6.
  - So at the CMB's mu_K the static capped state is not a halo. It is the whole share in a dust core of radius about
    1.55/mu_K, and SPARC's row excludes that by orders of magnitude.

## Known answers (16 of 16 PASS)

| | what | value |
|---|---|---|
| KA1 | QX2 iter 5 (additive form) at 0.1; mean-zero mu_K | +0.4644 / +0.4317; 1.778 / 1.736 (= QX2) |
| KA2 | ONE1's graded KiDS numbers at mu_K = 0 through this lane's tables and kernel | z -1.141 / -1.459 / -0.651 and -0.232 / -1.231 / +0.214; chi^2 1.915 / 0.868 (exact) |
| KA3 | QX8's exact-field SPARC grade at mu_K = 0 | 0.0560 @ 0.58 / 0.0558 @ 0.52 (exact) |
| KA4 | FB1's arithmetic I0/4 | 1.0631e-8 Mpc^-2 |
| KA5 | static dust enclosed mass: direct quadrature vs solver; deep-law closed form | 3e-7 / 4e-7 / 4e-7 (line 1e-5); 1.1e-9 (line 1e-4) |
| KA6 | the capped tables at m = 0 vs ONE1's projection and kernel (x2 footings) | 2.4e-6 and 4.8e-7 (line 1e-3) |
| KA7 | KD1's mu_B1a (x2 footings) | 198.254 / 198.245 (rel 1e-6) |
| KA8 | EW2's Saturn anomaly at 2.04e4 | 7.52e-14 (EW2 7.5e-14) |
| KA9 | QX5's group bracket at mu_K = 0 (x2 footings) | [+0.196, +0.359] / [+0.158, +0.320] (exact to 1e-3) |
| KA10 | S4's zero point (lambda_max, law potential to 3 Mpc) | rel 1.7e-10 |

KA1, KA2, KA3, KA6, KA7 and KA9 count once per footing: 16 in all, as `mk1_grade.out` lists them.

## MUTATE (separate outputs; each must move an interval)

All arms but one move an interval (`mk1_grade.out`).

- **M-NOCAP** (no cap).
  - Row 6: the bound 1.00 / 0.765 becomes none. The uncapped reading fails at every grid value, including 0.
  - Row 5: 7.08 / 5.62 becomes 10 / 10 (coarse grid). **Moves.**
- **M-2X** (share doubled).
  - Row 5: 7.08 / 5.62 becomes 5.62 / 4.47.
  - Row 8: the dust-alone threshold halves (log M_b 10: 6.42 becomes 3.24).
  - Row 6 was run on the lens's own halo only, both for the arm and for the primary it is compared with (as ONE1's M2).
    The doubled halos' neighbour search is about four times longer, about 3.5 hours. The primary's own-halo reading
    passes at 0-0.87 / 0-0.67. With the share doubled, mu_K = 0 fails (late types -2.26 / -2.14), and only mu_K = 1.0
    passes on the grid. **Moves.**
- **M-SIGN** (dust sign flipped).
  - Row 6: 1.00 / 0.765 becomes 0.010 / 0.0144. The flipped branch folds near m = 1.3e-3 (A1). From 0.1 up, the model
    cannot even reach the data's inner amplitude.
    Disclosed: the fold count runs over every k on ONE1's fit grid (0.25-60), not only the fitted k. That is stricter
    than needed. The arm moves either way.
  - Row 5: becomes 0.040 / 0.045. Row 4: [0.91, 1.51] / [0.76, 1.38] becomes none. **Moves.**
  - Row 3: **does not move as frozen.** X-COP is empty both ways. Only its closest miss moves, from rms 0.263 / 0.255 to
    0.476 / 0.444. Disclosed.

## Lean

`fable_independent_2026/lean_2026/MK1.lean`: 14 theorems, standard axioms only (`compile.txt`, exit 0).
- `w_turnover` and `w_strictAnti_mu`: w = 1/2 at a^3 = w0; w falls as mu_K rises.
- `fb1_arith`: FB1's I0/4 lies in (1.0630e-8, 1.0632e-8).
- `deep_dust_hasDeriv`: the deep-law static dust's enclosed mass, a derivative identity. KA5 checks it numerically.
- `dust_mono_mu`.
- `cap_law_relation`: on the law at the cap, m_s = (1 + X)^2 / (x^2 + 1 + X). The solver uses it.
- `cap_radius_anti`: dust pulls the cap radius in.
- `saturn_mono`.
- `no_window`, with five numeric instances: Jeans vs Saturn, background vs SPARC, background vs groups, background vs
  KiDS, Jeans vs KiDS.

`MK1_MUTATE.lean` states seven false versions (`compile_MUTATE.txt`, exit 1, 7 errors, one per false theorem): w rising
in mu_K, FB1's constant ten times larger, dust pushing the cap out, a window between 25118 and 7, the dust identity
without its r^3/9 term, the Saturn anomaly falling, and the cap relation with (1 + X) for (1 + X)^2.

## Files

- `FROZEN_CRITERIA.md` (b1fbded1e2) and `AMENDMENT_A1.md` (916f4e0e22).
- Library: `mk1_lib.py`. It holds the capped and uncapped dust solvers, the projection, and ONE1's kernel generalised
  to any profile.
- Rows 1-4, 7, 8: `mk1_rows.py` -> `mk1_rows.json` / `.out`, plus `mk1_rows_MUTATE.json` / `.out`. Run log
  `run_rows.txt`. 8 s.
- Row 5: `mk1_sparc.py` -> `mk1_sparc.json` / `.out`, plus `mk1_sparc_MUTATE.json` / `.out`. Run log `run_sparc.txt`.
  5 min.
- Row 6: `mk1_kids.py` -> `mk1_kids.json` / `.out`, plus `mk1_kids_MUTATE.json` / `.out`.
  - Part files: `parts/kids/pt_*.json`, one per (reading, footing, mu_K).
  - Run logs: `run_kids.txt` (primary and uncapped), then `run_kids_resume.txt` (the MUTATE arms).
  - The resume was a restart that reused every finished part file. It came after M-2X was moved to the own halo only.
  - About 2.5 h on one thread; peak 1.57 GiB. That is slightly above the brief's 1.5 GB, disclosed.
  - The kernel and profile tables (`parts/kids/*.npz`, 232 MB) are regenerated by the script and not committed.
- Row 8 reading: `mk1_row8.py` -> `mk1_row8.json` / `.out`.
- Label: `mk1_grade.py` -> `mk1_grade.json` / `.out`.
- Lean: `fable_independent_2026/lean_2026/MK1.lean` and `MK1_MUTATE.lean`; outputs `compile.txt` and
  `compile_MUTATE.txt`.
- Inputs read only, never edited: KD1 `kd1.json`; QX3 iter2 `iter2.json`; QX2 `qx2.py`; QX5 `qx5.py`; QX8 `qx8.py`
  with its `parts/`; S4 `s4_v3_muk_clusters.py`; ONE1 `one1_kids.py` and `one1.json`, with the KiDS files under
  `real_research/data/lensing_rar/`; EW2 iter4's constants.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
