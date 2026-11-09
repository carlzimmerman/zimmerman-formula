# SS1 variants B-G RESULT: every variant FAIL / FAIL (A2 2b866ef57a, A3 694668618a; criteria b5adc7a90b)

These are the outside source's repairs of A (rounds 4-10), each frozen once as given in AMENDMENT_A2, which was committed
alone before any B-G number. A3 corrected E's central share (also committed alone, before any E number). Variant A's
result stands as recorded (RESULT.md, b8569ef94a). TEST lane, quarantined; adopts nothing; no particle adopted.
kappa = 1/2 FITTED; not theory closed. Footings graded separately, never pooled.

**Correction (with variant H, A4 8bcceec033):** the fsigma8 derivative is now computed by fine-grid central differences. The
earlier coarse cubic spline rang across the onset kink; before-onset rows (LRG2, LRG3) now read exactly 1.000. Every variant
cosmology was rerun, and ss1v.json / ss1v.out carry the corrected numbers. **No label changes.**
- G: Rf BGS 0.090 / 0.008, LRG1 0.644 / 0.582 (was 0.133 / 0.050, 0.651 / 0.599), still FAIL.
- D: gate 8 flips FAIL -> PASS (BGS 0.53, LRG1 0.97), but D's first failing gate is still KiDS.
- B: Rf BGS 0.50, LRG1 0.09, still FAIL.
- E: BGS 0.004, still FAIL.
- F: BGS 0.081, still FAIL.
- C: unchanged, PASS.
See RESULT_H.md.

## Labels (frozen rule: first failing gate in the order 1, 2, 3, 5, 5b, 6, 7b, 8, 9, 10)

| variant | canonical | alt | constants (as recorded beside the label) |
|---|---|---|---|
| **G (primary)** | **FAIL at 2 groups** | **FAIL at 2 groups** | 0 fitted; form choices: 4 pi, kick factor 4, factor 3, cube-root combination |
| B | FAIL at 1 KiDS (subhalo bracket) | FAIL at 1 KiDS | 0.035, 250 kpc, 0.012, Hill 4, 0.72 profile, alpha 3.80 |
| C | FAIL at 1 KiDS (own shelf; subhalo bracket) | FAIL at 1 KiDS | B's constants + exponent 3/2, kick 220 km/s |
| D | FAIL at 1 KiDS (subhalo bracket) | FAIL at 1 KiDS | as C, kick 1150 km/s |
| E | FAIL at 2 groups | FAIL at 2 groups | six added: 260, 410, 95 km/s, 0.120, 0.008, 3/2 |
| F | FAIL at 2 groups | FAIL at 2 groups | 2 fitted (3.40, 0.75) + the baryon key f_cen |

Beyond the first failure, every variant also fails X-COP (3) and the Bullet (9) on both footings, and every variant except
C fails growth (8).

## G, the primary variant (canonical / alt)

**Derived constants.** On the record's footings the source's derivations give:
- z_dec (q = 0): 0.631, not 0.642.
- alpha: 4.367 / 4.366 (4 pi H0 sqrt(Omega_DE) times 6.0 Gyr).
- x_crit: 1.990.
- v_stiff = (a0 c L*)^(1/3): 265.8 km/s canonical, 288.1 alt (the source's 286 assumes a0 1.2e-10, L* 22 pc).
- Kick: 1063 / 1152 km/s.

| gate | canonical | alt |
|---|---|---|
| 1 KiDS | PASS max 0.012 (isolated lenses sit below threshold and convert) | PASS 0.012 |
| **2 groups** | **FAIL** 3/20 (f* 0), 0/20 (f* 1); median residual -0.07 / -0.28 | **FAIL** 2/20, 0/20; -0.08 / -0.31 |
| 3 X-COP | FAIL mean -0.214, rms 0.241; bins -0.30, -0.15, -0.16 (over-filled) | FAIL -0.233; -0.32, -0.17, -0.18 |
| 4 Coma UDGs (reported) | +1.126 (+4.30 sigma_U) | +1.097 |
| 5 SPARC | PASS rms 0.0559 (line 0.0660); F2 0.012 | PASS 0.0559 (0.0658) |
| 5b Ursa Major | PASS: Delta_pred -0.001 (the UMa host is far below Delta 500, so x_host = 0) vs EV1 -0.024 +- 0.064 | PASS -0.001 |
| 6 background | PASS (mass kept) | PASS |
| 7b CMB lensing | NO VERDICT; reading 8.48 (baseline 8.56) | NO VERDICT; 8.48 |
| 8 forest + growth | FAIL. About 63 % of the component converts; sigma8 0.654 (ref 0.808), S8 0.670; Rf BGS 0.133, LRG1 0.651 (pre-correction; corrected 0.090, 0.644, see Correction above); forest 0.000 | FAIL. sigma8 0.639, S8 0.656; Rf 0.050, 0.599 (pre-correction; corrected 0.008, 0.582) |
| 9 Bullet | FAIL (cls FAIL): M300 4.32, 1.99 e14 (Z +1.56, -0.90); the subcluster's peak sits 95 kpc from its galaxies and 63 kpc from the gas | FAIL (Z +1.95, -0.56) |
| 10 Cassini | PASS | PASS |

**Why G fails.**
- The threshold works, as the orchestrator said: every group and cluster on the record retains (Lovisari groups f >= 0.9919
  on their table M500 / R500), and the galaxies drain.
- But full retention gives each group its whole pre-conversion share, 4.1 M_b. The record needs 3.46 (f* 0) and 1.23 (f* 1).
  Group residuals go negative (-0.07 / -0.28): the AMOUNT is too large.
- X-COP is over-filled in every bin, inner bin -0.30.
- Growth: two-body conversion in every collapsed sub-threshold halo converts 63 % of the component (41 % if only halos
  above 1e10 Msun convert). Daughters streaming over about 6.7 Mpc stop clustering at k > 0.15 / Mpc, so sigma8 drops to
  0.65-0.71 and the low-z fsigma8 rows fall below CE2's 2 sigma. The source's 22 % converted, sigma8 0.748 and fsigma8
  0.450 are not reproduced; the M_min 1e10 bracket gives sigma8 0.706 / 0.695, S8 0.723 / 0.713, and gate 8 still FAILS.

**G brackets (reported, none grades):**
- G-obs (v_vir from the Lovisari / X-COP M500): groups 3/0, X-COP -0.214. Same FAIL.
- G-local: the local v profile plus the 18 % expansion, added assumptions; a local dispersion gate sits close to the dead
  keys HX1 / SK1. Groups 8/3 (canonical) and 3/4 (alt), median +0.09 / -0.18; X-COP -0.165, inner bin -0.25. Still FAIL:
  the local gate halves the group excess but not enough, and clusters stay over-filled.
- Duffy NFW and Moster AM (local gates): groups and X-COP FAIL in every case. KiDS and SPARC FAIL under Moster: the
  abundance-matched top KiDS bin passes threshold and keeps its halo, +0.16 dex.

**G MUTATE (ss1v_MUTATE.out):**
- MG3 (alpha -> 0): KiDS 0.378, SPARC FAIL. **BITES.**
- MG4 (x0 = 0 everywhere): groups +0.35 / +0.19 and X-COP +0.44, FAIL. **BITES.**
- MG1 / MG2 (v_stiff x 1.25 and / 1.25): numbers move (groups 3/2 and median +0.13 / -0.22 at x 1.25) but no status flips.
  **NO BITE** by the status-vector rule; the FAIL is robust to v_stiff within 25 %.

**Frozen predictions (no lens-redshift split is on disk, so not graded).** Only the KiDS-bright catalogue is on disk:
redshifts, no shear profiles. Recorded:
- G: isolated M* 1e11 lens Delta Sigma excess over the bare law +0.245 / +0.205 / +0.078 / +0.020 dex at 0.3 Mpc for
  z_lens 0.8 / 0.6 / 0.4 / 0.2.
- F: +0.21..+0.27 at z 0.4-0.8 and about +0.03 at z 0.2.

The record's KiDS loader has no 10^11.3 or 10^11.5 bin (top bin log M* 10.9), so the source's 5.0 % / 9.8 % stack claims
are not graded.

## B-F in one line each

- **B:** with the subhalo bracket (f_sub 0.318 field, 0.220 isolated), every halo larger than about 50 kpc in R500 sits above
  threshold. KiDS FAILS (0.148), and so do SPARC, groups (over-filled), X-COP and growth (warm sea 54 % converted, Rf BGS
  0.43). UMa PASSES even bathed (+0.084, inside the 2 sigma band).
- **C:** its own shelf FAILS KiDS (max 0.355 dex). Growth PASSES (220 km/s stays within 1.3 Mpc). Groups, X-COP and Bullet
  FAIL.
- **D:** KiDS FAILS (0.30) on the subhalo bracket; growth FAILS (1150 km/s).
- **E:** KiDS and SPARC PASS (W_mach zeroes galaxy halos). Groups FAIL (3/0 and 2/2; median +0.16 / -0.17: the f* 1 reading is
  over-filled). X-COP, growth and Bullet FAIL.
- **F:** same pattern as G at both f_cen values (0.6 graded, 0.3 bracket): groups, X-COP, growth and Bullet FAIL.

## Known answers (parts/v_ka.json, parts/v_KC_replay.json)

- **K0, closed form vs ODE:** PASS (max dev 4.5e-13).
- **K-B reproduction:** the source's x0 1.95 / 2.10 / 2.40 -> 25.0 / 66.7 / 85.2 % does not solve its own closed form, which
  gives 56.9 / 73.0 / 86.5 % (the hand estimate frozen in A2). KiDS x0 0.18-0.64 -> 2.24-2.33 % reproduces.
- **K-D:** x_crit 1.908 (alpha 3.80) and 1.993 (4.39). Reproduced.
- **K-F:** x0 1.27 -> 0.0429 / 0.0238 (ref 0.043 / 0.024). Reproduced.
- **K-G:** v_vir reproduced to 0.3 % at every M500. f reproduced to 0.005 except at M500 1e13, which sits on the threshold
  (0.148 vs 0.161: f is that steep there). Lovisari min f 0.9919 (claim >= 0.992). Printed as FAIL by the frozen tolerance;
  disclosed, and it has no bearing on any gate.
- **K-C:** the source's shelf numbers for M* 10^11.3 (+0.28 at 1 Mpc, +0.31 at 1.5 Mpc) are NOT replayed, because the lane's
  brackets put that lens in a different regime:
  - Moster 2013 at z 0.55 gives M200 1.2e14.
  - The subhalo bracket gives x0 13.4, so the lens keeps its whole halo.
  - The pointwise shift is +1.4 dex.
  The source's numbers assume its own small f_sub and a 1e13 halo.
- **A's KAs, rerun in every pass:** law-only replay and the Bullet K1 both PASS.

## Lean (ss1_lean/SS1_variants.lean)

Compiles with exit 0 and standard axioms only. The MUTATE (wrong half-retention constant 64/16) fails, as it must.
- **Closed form:** `hasDerivAt_F` and `closed_form_solves` prove that a differentiable y with F(x0, y(t)) = t solves
  dy/dt = -y/(1 + (x0 y)^4).
- **Half retention:** `half_retention` proves F(x, 1/2) = alpha iff x^4 = (64/15)(alpha - ln 2).
- **Monotone:** `retention_mono` proves the retention is monotone in x0.
- **Bounds:** `bound_195` (x0 >= 1.95 gives f > 0.249) and `bound_32` (x0 >= 3.2 gives f > 0.958), at alpha 3.80.
- **Not formalised:** the third relayed bound (f < 0.0235 for x0 <= 0.65) needs exp(3.7554) > 42.55. Checked numerically
  (0.0233 at x0 0.65), not proved in Lean.
- **Theorem 3's dropped minus sign:** not visible to the lane (outside text not in the lane).

These certify the switch, not the physics.

## Disclosures

1. **Streaming-length bug, fixed before grading.** The first C-G cosmology runs had a unit bug (1 km/s x 1 Gyr taken as
   1.02 Mpc instead of kpc). All C-G and MG cosmology runs were redone after the fix (run_v_cosmo_rerun.sh); every number
   above is post-fix.
2. **Subhalo bracket.** The f_sub bracket is the unevolved Jiang & van den Bosch 2016 function. It over-counts bound,
   stripped subhalos, which is generous to the sloshing and multiplicity gates. The record has no subhalo masses for its
   groups, X-COP or KiDS lenses; record-native values are used only for the Bullet, UMa and MW.
3. **Growth model.** The record's linear two-fluid ODE with a k-dependent non-clustering fraction, F_conv(a) (1 - 1/(1 +
   (k lambda)^2)). lambda is for a daughter produced at onset (the largest), with v proportional to 1/a. Galaxy-scale
   sub-threshold halos convert (two-body inside Delta > 200); M_min 1e10 is the bracket. The fsigma8 failure rests on this
   linear treatment of streaming daughters.
4. **Daughters leave their systems (D-G).** Where a cluster's escape speed exceeds the kick, daughters would be re-accreted;
   this is irrelevant here because every cluster retains about 100 %.
5. **UMa geometry.** The host is the members' summed primary halos inside the source's R_sys 1.5 Mpc (Delta about 1). The
   bound-group reading is reported beside it.
6. **Compute and inputs.** Local passes 1-10 s and under 0.15 GB; cosmology 8-30 s and under 0.6 GB (CLASS); Bullet child
   about 1.36 GB (DB1). PJ1 loaders come from a read-only copy of origin's lane dir.

**Reading.** G's single velocity threshold sorts galaxies from groups correctly. But a system above it keeps its entire
pre-conversion share, which over-fills groups and clusters, and converting every sub-threshold collapsed halo turns about
40-60 % of the component into fast streaming daughters, which suppresses low-z growth below the record's fsigma8 rows.

**What a repair would have to change:**
- groups must keep a mass-dependent fraction of order 30-85 %, not about 100 %;
- clusters must keep a falling fraction (TR1), not their whole SIS share;
- the converted mass must not leave the small-scale matter field at that scale and speed: either far less converts (only
  above about 1e12 Msun), or the daughter stays bound.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
