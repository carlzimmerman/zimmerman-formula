# ONE1 FROZEN CRITERIA: the cold component counted once, graded on every gate for one share rule

Committed alone, before any ONE1 script exists and before any ONE1 number is computed.
TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings canonical (a0 9.3603e-11) and alt
(1.1312e-10 m/s^2), never pooled. A fail is reported as a fail, first, in plain words.

## 1. The reading

The a0 law is not a second force. It is the gravity of the cold component itself, counted once. Gravity is Newton (GR)
with the total mass everywhere; no nu acts on anything.

- **Galaxies** (KiDS lenses, their catalogued neighbours, SPARC galaxies). Each galaxy holds one share X M_b. Inside the
  galaxy the share is laid out as the law's own phantom halo of its baryons, until the share runs out. With
  x = r / r_M, r_M = sqrt(G M_b / a0), the enclosed mass is M(<r) / M_b = m(x) = nu(1 / x^2) = 1/2 + sqrt(1/4 + x^2) for
  x <= x_t, and 1 + X beyond. The halo ends where nu = 1 + X, so x_t^2 = X (X + 1). The baryons sit at the centre (the
  law's own spherical convention). There is no turnaround cap and no core for galaxies.
- **Groups and clusters** (X-COP, the record's 20 groups, the Bullet's subclusters). PD1's last stated rule for groups
  and clusters (PD1 AMENDMENT_A2 item 2): the measured M_b,sys already is the basin's baryons, so share = 5.41 M_b,sys
  (the cosmic ratio omega_d / omega_b as PD1 uses it). Of that share, f_core = (1/2)[1 - (v_stiff / v_vir)^2] sits in a
  Duffy NFW core when v_vir > v_stiff; the phantom W_vir M_b(<r)(nu - 1) is capped at (1 - f_core) share; the remainder is
  isothermal out to R_ms (PD1 A1's system()). All of it is Newtonian mass.
- **The Bullet.** The cold component is collisionless, so each subcluster's phantom (capped), core and remainder inside
  R200 sit with its galaxies; gravity is Newtonian (PD1 A2's frozen Bullet reading, DB1's child with a0 -> 1e-30).
- **Coma's diffuse galaxies and dwarf spheroidals.** A member's halo is real mass, laid out as its own isolated phantom
  halo. There is no external-field effect.
- **Solar System and wide binaries.** No star holds a share; the galaxy's halo is smooth at these scales. Newtonian.

## 2. The share rule (fixed here; no tuning afterwards)

- **Primary, galaxies:** PD1's own Lagrangian share: the dust inside the Lagrangian sphere of the shell that turns around
  at z 0, share = rho_bar_d (4 pi / 3) x_ta^3 + R M_b with seed M_b (1 + R). It is computed by PD1's `share_table`
  (pd1.py, executed read-only) on each footing's background; PD1 prints 59.5 M_b. X is that number, per footing.
- **Primary, groups and clusters:** 5.41 M_b,sys with the core prefactor 1/2, as in section 1.
- **Brackets (reported, never graded):** X = 53.64 (the census cap, CFG804 / KO1's X_CAP); X = 80; the cluster core
  prefactor 1 against 1/2; PD1's Lagrangian share at cluster scale under A1's rule (pd1_a1.json) and PD1's original
  leftover rule (pd1.json), both as published.
- **Disclosure on the cluster choice.** PD1's published rows for groups, X-COP and the Bullet are known to me under
  every PD1 rule: groups and the Bullet fail under all of them; X-COP passes only with prefactor 1 at the cosmic share.
  The primary here is PD1's last stated rule. The choice cannot turn a groups or Bullet fail into a pass.
- **Groups' baryons.** The record holds no independent baryon census for groups. M_b,sys is GB1's g5 (1 + f*) at
  f* = 0 and 1, as PD1 used it. The groups row is graded as it stands.

## 3. Rows, statistics and lines (one table, canonical / alt; PASS / FAIL / NOT EVALUABLE with the number and the line)

**Row 0. Conservation.** q = [GSMF-summed X M_b] / rho_bar_d at z 0 (PD1's GSMF and grid, PD1's convention M_b = 10^m).
Line q <= 1 (PD1 P1's line: the halos cannot hold more than the cosmic dust).

**Row 1. SPARC.** PD1's P2 SPARC machinery (QX8 fit, Upsilon marginalised as QX8) with the galaxy halo of section 1:
glaw inside R_t = x_t r_M, frozen phantom (R_t / R)^2 beyond, no leftover. Line: SS1 G5 as PD1 graded it (rms <= L0 +
0.010, |mean| <= 0.05, the same for the massive tail Vflat >= 250). Reported: the fraction of galaxies with R_t inside
their last measured radius.

**Row 2. KiDS, host-free lenses (KO1).**
- *Lens sets.* KO1's host-free cut (Delta 0.3 dex, W 230 Mpc), veto radius F R_h with F = 1.0, 1.3, 1.6. **Tie rule:**
  KO1's plain float comparison (a decimal tie is not a host), so KO1's published numbers are the known answer. KO1R's rule
  (a tie within 1e-9 dex counts as a host) is a bracket at every F. Samples: all, late (typ 0), early (typ 1).
- *Data statistic.* KO1's estimator, unchanged: per bin D_k = 4 G ESD_k, M_k the law stack at catalogued Mgal, s_k the
  delete-one-patch jackknife error of D_k for that set; A(S) = sum D_k M_k / s_k^2 / sum M_k^2 / s_k^2. Shape ratio
  R_s = A(outer bins 0-3) / A(inner bins 7-12). Per-bin outer profile p_k = (D_k / M_k) / A(inner), k = 0..3.
  Errors: delete-one-patch jackknife over KO1's 50 patches, s_k held fixed.
- *Model.* Every cell (lens l, bin b) = lens's own halo + neighbours' halos.
  - Lens's own halo, KO1's cell convention: the area average over the cell of g_law(k g_bar) x rho(u), with
    rho(u) = DeltaSigma_t(u; X) / DeltaSigma_inf(u) the exact projected ratio of the truncated to the untruncated halo at
    u = R / r_M(k), r_M(k) = sqrt(G k Mgal / a0). Written in my own code; checked against the lead's `dsig`.
  - **Mass factor k (calibration).** The shape ratio cancels a mass calibration only for a scale-free model. This model has
    a scale (x_t r_M grows as sqrt(k M_b)). So, as KO1's PH3 did for its exterior, k is the factor that makes the model's
    inner amplitude equal the measured one, fitted per sample, footing and veto (and refitted in every jackknife sample).
    The share is X times the fitted mass, for the lens and its neighbours alike. **Bracket: k = 1** (catalogued masses;
    the lead's pre-freeze convention).
  - Neighbours (KO1 E8's pool and window, extended): every pool object other than the lens (r < 20, 0.02 <= z <= 0.8,
    finite log M* > 7) with |chi_j - chi_l| < 230 Mpc and projected separation d < R_h,l + r_t,j, carrying the same share:
    its own truncated halo of total k (1 + X) M_b,j (record's recipe), r_t,j = x_t sqrt(G k M_b,j / a0). The exact
    annulus average of its tangential shear about the lens is used (section 5), with the same sum around shuffled lens
    positions subtracted (5 shuffles, seed 52, positions permuted among the host-free lenses at F = 1.0).
- *Gate (graded at F = 1.6 R_h; F = 1.0 and 1.3 reported: their outer bins carry the veto's tapered edge, KO1 A2/E7).*
  - G-K1: for each of all, late, early: |R_s,data - R_s,model| <= 2 sigma, sigma the jackknife error of the difference.
  - G-K2: all: per-bin profile chi^2 (4 bins; jackknife covariance of p_k^data - p_k^model, Hartlap factor 44 / 49)
    <= 9.49 (p >= 0.05).
  - G-K3, one share for both types: |(R_s,early - R_s,late)_data - (same)_model| <= 2 sigma (jackknife).
  - KiDS PASS iff G-K1 (all three samples), G-K2 and G-K3 hold. Otherwise FAIL, naming the failing line. Every sigma is
    printed, so a pass that comes from a large error is visible.
- Reported beside it: the neighbours' term in R_s (extended against point masses; the lead's "about 0.1" checked), the
  k values, all three vetoes, both tie rules, k = 1, and the brackets X = 53.64, 80.
- KO2 (`closure_2026_11_09/KO2_kids_own_field_by_type/`, another session): if its RESULT.md exists when I grade, its
  late-type label is quoted against the lead's blind prediction, and I say so. I do not open KO2's outputs before ONE1's
  KiDS numbers are written. I do not edit that folder.

**Row 3. X-COP, Row 4. groups.** PD1 A1's system() and gate code (executed read-only from pd1_a1.py's prefix; the gate
loops transcribed) with the primary group/cluster rule. Lines as PD1: X-COP |mean| <= 0.05, rms <= 0.10 and every graded
bin within 0.10 dex; groups >= 16 of 20 at f* 0 and at f* 1.

**Row 5. The Bullet.** PD1 A2's child (pd1_a2.py `nchild ... newton`, DB1's bullet_row), galaxy-traced dark mass from the
primary rule at z 0.3. Line: DB1's row label (offset class and the subcluster's M300 Z). Offset and M300 Z reported.

**Row 6. Coma's diffuse galaxies and dSphs.** Reused graders, not new code:
- Coma UDGs: S1's Coma chain with x_e = 0 (row "S2 AQUAL isolated L*0 E-W" of `rebuild_2026_10_22/S1_v3_hosted_small`)
  carried; my own algebraic recomputation of S1's "S1 kernel nu1" row from S1's per-galaxy inputs as a check. Line:
  GB1 G5, |mean residual| <= 2 sigma_U with GB1's sigma_U as stored in gb1.json.
- dSphs: GB1 G6 for the plain law L0 (LW1 "plain" = isolated nu(g_N), no external field), carried from gb1.json. Line:
  GB1 G6 (each graded class's bootstrap CI of median minus the SPARC anchor contains 0).
- Truncation check for both: x_t r_M against the readout radius per system. A halo that ends inside the readout radius
  lowers the prediction; that can only raise a positive residual. Reported per system.

**Row 7. CMB, growth, CMB lensing.** Carried from the record's cold reference (PD1 P4: QX15 L1, CMB lensing 8.56 against
18.48, growth f sigma8 ratio 1, S8 change 0) if and only if the reading adds nothing on top of the cold component. Checked,
not asserted: (a) no field equation carries nu (section 1); (b) the halos are carved out of the cold component (row 0);
(c) SWT1 T2's filling line: a ONE1 halo is a fixed function of its own M_b, so its response to a long-wavelength field
(the incremental permittivity T2 uses) is 1 and q_C = 0; the script evaluates T2's permittivity for this halo and prints
it. The 1-halo redistribution of the component is NOT EVALUATED (no halo-model lensing machinery in the record; PD1).

**Row 8. Solar System and wide binaries.** Newtonian. Stated: what the record's Cassini / planetary gate (GB1 G8) reads for
a Newtonian field plus the smooth galactic halo (anomalous acceleration at Saturn from the local halo density, against
the gate's bound), and which row of the Gaia DR4 pre-registration (`prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`, read
only) the reading predicts. The wide-binary row is NOT EVALUABLE until DR4 (the record's gamma_v is ungated).

**Row 9 (not a gate; its own RESULT section): what the reading does not derive.** The halo's profile needs the assumed
relation of PD1 P7 / A2 item 5 (dispersion locked to sigma^2 = (1/2) sqrt(G M_b a0)). I search the record's actions for one
that produces it and say what I find, and whether a0 = (1/2) c sqrt(G rho_DE) enters anywhere except through that relation.

## 4. Label (per footing, primary share)

- **NO VERDICT** if a known answer that feeds a row fails (that row is then NO VERDICT and the label cannot be PASSES ALL).
- **FAILS** if any graded row fails; every failing row is named.
- **PASSES ALL** only if every graded row passes; rows NOT EVALUABLE are named beside the label and do not count as passes.
Then one sentence per bracket.

## 5. Known answers (all must pass)

- KA1. PD1's published rows reproduced with PD1's own shares and prefactors, to 1e-6 relative: SPARC rms (pd1.json),
  X-COP and groups (pd1_a1_share5.41.json, pd1_a1.json, pd1_a1_share5.41_fcpre1.0.json), Bullet M300 Z (pd1_a2.json).
- KA2. The lead's pre-freeze table: with k = 1 and no neighbours, my code returns the lead's model R_s (and the late /
  early "model outer x inner level") for X = 53.64, 59.5, 80 and no end, every veto and footing, to 0.01.
- KA3. The untruncated halo returns KO1's law amplitudes: rho(u) at X = 1e8 equals 1 within 1e-3 on u in [0.3, 2000].
- KA4. The far field equals the point mass: DeltaSigma_t(u) pi u^2 / (1 + X) = 1 within 1e-4 for u >= x_t; the ratio to
  the untruncated form equals 4 (1 + X) / (pi u) within 1e-3 at u = 2000 (X = 53.64).
- KA5. X to infinity returns the law: the model R_s at X = 1e6 equals the law's R_s at the same k within 1e-3.
- KA6. Data side: KO1 E7 (ko1_shape.json) host-free counts 40,667 / 25,708 / 17,335 and the per-bin amplitudes, inner
  amplitude and R_s of "all" at every veto, to 1e-6 relative.
- KA7. Neighbour kernel: (i) where the neighbour's halo lies wholly inside or outside a cell's circles, the extended kernel
  equals E8's point-mass kernel to 1e-4; (ii) centred (d = 0) it equals the lens-own projection to 1e-3; (iii) halos
  scattered uniformly give zero net annulus shear, |.| < 0.02 of the inner part; (iv) with point masses, X = 5.562, k = 1
  and E8's own pairs and shuffles, E8's net a_nb at F = 1.0 (0.00181 / 0.00165 per unit (1 + X)) is reproduced to 2 %.
- KA8. Coma: my algebraic isolated-law mean equals S1's "S1 kernel nu1" row (+0.330 / +0.291 dex) to 1e-3.

## 6. MUTATE (separate outputs; each must bite, and any that does not is disclosed)

- M1. Share x 0.1: must FAIL KiDS (gate as frozen).
- M2. Share x 10: must FAIL row 0 (conservation: the halos would hold more than the cosmic dust). Its KiDS reading is
  reported.
- M3. Neighbours' positions shuffled (a shuffled set used as the real one): the net neighbour term must change by more
  than 3 sigma of its jackknife error.

## 7. Lean (`ONE1.lean`, twin `ONE1_MUTATE.lean` of false statements that must fail; compile outputs with no home paths)

Certified: x_t^2 = X (X + 1) from nu = 1 + X; continuity of the enclosed mass at x_t; the far-field ratio
4 (1 + X) / (pi u) against the isothermal form; the truncated mass never exceeds the law's and is monotone in X; inner radii
(x <= x_t) are unaffected by X; a thin shell outside R lowers DeltaSigma at R; and the shape-ratio monotonicity lemma (an
outer amplitude non-decreasing and a positive inner amplitude non-increasing in X give a ratio non-decreasing in X). That
the projected stack meets the lemma's premises is checked numerically on the X grid, not in Lean.

## 8. Hand estimate (before any number; to be checked, not trusted)

- With k fitted (about 2.8 / 2.4 at 1.6 R_h), the halo ends 1.6 to 1.7 times further out than with k = 1, which acts like
  X near 100 at k = 1: R_s about 0.85, plus a neighbours' term of 0.1 to 0.2. Against 0.81 +- 0.13 at 1.6 R_h that passes;
  at 1.0 R_h (0.61 +- 0.09) it would fail by about 3 sigma (reported only). Late types: model near 0.9 against data near
  0.1 with an error near 0.45, about 1.8 sigma: a near miss either way.
- Groups and the Bullet fail as in PD1. X-COP fails at prefactor 1/2 (under-filled) and passes at 1 (bracket).
- SPARC passes (halos end beyond the last points). Coma UDGs pass with no external field (+0.33 dex against 0.52).
  dSphs fail (bright M31). Solar System passes. CMB carried.
- Expected label: FAILS / FAILS (groups, X-COP, Bullet, dSphs).

## 9. Operational

One thread, small jobs (under about 1.5 GB). Scripts: `one1.py` (rows 0-5, 7, 8 and KAs), `one1_kids.py` (row 2, KAs
2-7), `one1_coma.py` (row 6, KA8). Outputs: `.json` / `.out` per script, `one1_MUTATE.json` / `.out`, `ONE1.lean`,
`ONE1_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`, `RESULT.md`. The three pre-freeze files are not edited. Commits
with explicit paths; pushed by a sparse temporary worktree.

## What I have seen before freezing (disclosure)

The lead's PREFREEZE_NOTE.md, one1_prefreeze_look.py and its .out (k = 1, no neighbours: R_s 0.510 / 0.515 / 0.525 at
X = 59.5); KO1's RESULT, criteria, amendments, ko1_shape.py / ko1_neighbours.py and their .out (E7, PH3 with k 2.83 / 2.39 at
1.6 R_h, E8); PD1's criteria, amendments, RESULT and every PD1 .out; GB1's RESULT table (L0: G5 FAIL +1.121, G6 FAIL bright
M31 +0.199 [+0.079, +0.393], G8 PASS); S1's Coma chain (isolated rows +0.325 / +0.285 dex); SWT1's T1 / T2 summary; the
Gaia DR4 pre-registration's Newtonian row and Amendment 1. Not seen: any KO2 output, any by-type shape ratio at 1.3 or 1.6
R_h, any extended-neighbour term.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
