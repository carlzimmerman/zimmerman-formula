# SS2 RESULT: FAIL / FAIL (criteria 390a1dc5ff)

This lane grades variant G alone, the outside source's virial-gated late conversion. TEST lane, quarantined; adopts nothing;
no particle adopted. kappa = 1/2 FITTED; not theory closed. Footings canonical and alt, graded separately, never pooled.

**Not blind.** SS1 had already graded G (SS1 A2, result f3186ce8e7), and these criteria were frozen with that known. Every
SS2 number that repeats SS1's G reproduces it exactly: groups 3/20 and 0/20, X-COP -0.214, sigma8 0.654.

What is new here:
- the CMB-lensing validation (it failed, so 7(b) is NO VERDICT);
- the source-constant bracket;
- the per-group amount and TR1 readings;
- M5 (onset at z 2);
- the Lean separation bounds at alpha 4.39.

**Correction (after the result, with SS1 A4):** fsigma8 is now computed by fine-grid central differences. The earlier coarse
spline rang across the onset kink; before-onset rows now read exactly 1.000. ss2.json / ss2.out were rerun and regraded.
**Label unchanged:**
- G: Rf BGS 0.090 / 0.008, LRG1 0.644 / 0.582 (table below shows the pre-correction 0.133 / 0.651);
- M_min 1e10 bracket: BGS 0.396 / 0.339;
- G-source: BGS 0.016.

**Label (frozen rule): FAIL on canonical, FAIL on alt. First failing gate: 2, groups.**
- Also failing on both footings: 3 X-COP, 8 growth (fsigma8) and 9 Bullet.
- Passing: 1 KiDS, 5 SPARC, 5b Ursa Major, 6 background (BAO + SN), 10 Cassini.
- 7(b) CMB lensing: NO VERDICT.
- Under the source's own constants (z_dec 0.642, alpha 4.39, v_stiff 286, bracket G-source) the label is the same: FAIL at
  groups.
- Count beside the label: 0 fitted constants. Form choices: the cube root (a0 c L*)^(1/3), the kick factor 4, the 4 pi in
  Gamma0, the factor 3 in x0.

## Constants on the record's footings

| | canonical | alt | source |
|---|---|---|---|
| z_dec (q = 0) | 0.6313 | 0.6310 | 0.642 |
| alpha = 4 pi H0 sqrt(Omega_DE) t_dec | 4.367 | 4.366 | 4.39 |
| x_crit = ((64/15)(alpha - ln 2))^(1/4) | 1.9898 | 1.9896 | 1.9929 |
| v_stiff = (a0 c L*)^(1/3) | 265.8 km/s | 288.1 km/s | 286 |
| kick 4 v_stiff | 1063 km/s | 1152 km/s | 1144 |

## Gate table, primary (KD1 P3 SIS halos at z_dec)

| gate | canonical | alt |
|---|---|---|
| 1 KiDS | PASS max 0.012 (galaxy-scale halos sit below threshold and convert) | PASS 0.012 |
| **2 groups** | **FAIL** 3/20 (f* 0), 0/20 (f* 1); median residual -0.07 / -0.28 | **FAIL** 2/20, 0/20; -0.08 / -0.31 |
| 3 X-COP | FAIL mean -0.214, rms 0.241; bins -0.30, -0.15, -0.16 | FAIL -0.233; -0.32, -0.17, -0.18 |
| 4 Coma UDGs (reported) | +1.126 (+4.30 sigma_U) | +1.097 |
| 5 SPARC + F2 | PASS rms 0.0559 (line 0.0660); F2 0.012 | PASS 0.0559 (0.0658) |
| 5b Ursa Major | PASS: Delta_pred -0.001 vs EV1 -0.024 +- 0.064 (UMa is far below Delta 500) | PASS |
| 6 background | PASS: mass kept, so the background equals the reference and SS1's BAO failure is gone | PASS |
| 7(b) CMB lensing | NO VERDICT (validation failed); reading 8.48 (baseline 8.56) | NO VERDICT; 8.48 |
| 8 forest + fsigma8 | FAIL: 63 % of the component converts; sigma8 0.654 (ref 0.808), S8 0.670; Rf BGS 0.133, LRG1 0.651, LRG2 1.019, LRG3 0.997; forest 0.000 | FAIL: sigma8 0.639, S8 0.656; Rf 0.050, 0.599 |
| 9 Bullet | FAIL (DB1 cls FAIL): M300 4.32, 1.99 e14 (Z +1.56, -0.90); the subcluster's convergence peak sits 95 kpc from its galaxies and 63 kpc from the gas | FAIL (Z +1.95, -0.56) |
| 10 Cassini | PASS | PASS |

## The AMOUNT question (groups, X-COP)

**The threshold works.**
- Every Lovisari group retains (min f 0.9919 on its table M500 / R500).
- 12 of 20 groups (canonical) also keep the full 4.1 M_b on the primary halos.
- Isolated lenses and discs drain to about 1.2 %.

**The failure is the amount.**
- **Groups.** At f* 0 the record needs about 3.46 M_b and G gives 4.1 to most groups. Median residual -0.07, but only 3/20
  sit within 2 sigma at every point. At f* 1 the need is 1.23 and G over-fills by 0.28 dex.
- **X-COP.** The retained component over the dynamical mass is 1.57 / 0.90 / 0.75 in TR1's first three bins, against TR1's
  0.71 / 0.66 / 0.58.
- **New: the shape follows.** TR1's per-bin SHAPE statistic for the retained component, with one amplitude per cluster,
  reads -0.09, +0.09, +0.04 (RMS 0.075 / 0.071, max 0.089 / 0.093). That is inside TR1's FOLLOWS line (RMS <= 0.10,
  max <= 0.15). G's pre-conversion SIS has the right shape for X-COP; its amount is about 1.3-2x too large.

**Brackets (none grades):**
- G-obs (observed M500): groups 3/0. Same FAIL.
- G-local (local v profile + 18 % expansion, named added assumptions, close to HX1 / SK1): groups 8/3 and 3/4, X-COP -0.165.
  Still FAIL.
- Duffy NFW and Moster AM: groups and X-COP FAIL in every case. Under Moster the top KiDS bin passes the threshold and keeps
  its halo, so KiDS FAILS (+0.16) and so does SPARC.

## Growth (gate 8)

- **Where the conversion happens.** Two-body conversion in every collapsed halo below the threshold converts 63 % of the
  component by today (PS above 1e6 Msun). That is 53 % of all matter, against the source's 22 %.
- **Effect on structure.** The daughters stream about 6.7-7.3 Mpc comoving and stop clustering at k > about 0.15 / Mpc.
  sigma8 drops to 0.65 and the low-z fsigma8 rows fall far below CE2's 2 sigma.
- **Bracket M_min 1e10** (only halos above 1e10 Msun convert): 41 % converts, sigma8 0.706 / 0.695, S8 0.723 / 0.713,
  Rf BGS 0.43 / 0.37. Still FAIL.
- **Not reproduced:** the source's sigma8 0.748, S8 0.762 and fsigma8 0.450 / 0.466.
- **KiDS 2-halo:** NOT EVALUABLE on the record's machinery (as frozen).

## CMB lensing validation (section 4): FAIL, so 7(b) is NO VERDICT

| | canonical | alt |
|---|---|---|
| CLASS, 20 % of the cold component as a smooth matter fluid from the start | chi^2 44.59 | 44.58 |
| the lane's ratio method at fc = 0.20 | 11.15 | 11.16 |
| tolerance 0.15 \|CLASS - baseline 8.56\| | 5.40 | 5.40 |

Diagnosis:
- The two agree on the small-scale amplitude: S(L 400) is 0.184 in both.
- They disagree on the low-L shape: S(L 40) is 0.278 in CLASS against 0.167 in the method.
- A component that is smooth from the start also changes the early transfer function (matter-radiation equality and the
  turnover), which the method, a late-time growth ratio, does not model.

So the test as frozen could not validate the method for a late-onset conversion. A valid test needs a time-switched species
inside CLASS (a code change). The reading of 8.48 for G (S(L 100) about 0.99) is reported, not graded.

## MUTATE (ss2_MUTATE.out)

- **M1 / M2 (v_stiff x 1.25 and / 1.25): NO BITE.** Numbers move (groups 3/2, median +0.13 / -0.22 at x 1.25) but no status
  changes. As in SS1, the FAIL is robust to v_stiff within 25 %.
- **M3 (alpha -> 0): BITES.** KiDS 0.378 and SPARC FAIL.
- **M4 (x0 = 0): BITES.** Groups +0.35 / +0.19 and X-COP +0.44, FAIL.
- **M5 (onset z 2): BITES.** The lensing reading rises 8.48 -> 8.66 / 8.68, and sigma8 drops to 0.56 / 0.55.

## Known answers

- **K0, closed form vs ODE:** PASS (4.5e-13).
- **K-G:** v_vir reproduced to 0.3 %. f reproduced except at M500 1e13, which sits on the threshold (0.148 vs 0.161).
  Printed as FAIL by the frozen tolerance; it touches no gate.
- **Lovisari:** min f 0.9919 (claim >= 0.992).
- **x_crit:** 1.9929 at alpha 4.39.
- **Replays:** law-only replay and the Bullet K1 both PASS; the background with Gamma0 -> 0 returns the reference (SS1
  machinery).
- **Consistency:** SS2 equals SS1's G to the last printed digit.

## Frozen prediction (no lens-redshift split on disk, so recorded, not graded)

Isolated M* 10^11 lens excess over the bare law at 0.3 Mpc, for z_lens 0.8 / 0.6 / 0.4 / 0.2:

| reading | excess (dex) |
|---|---|
| source | +0.245 / +0.205 / +0.078 / +0.020 |
| lane, primary halos | +0.365 / +0.340 / +0.180 / +0.061 (canonical; alt the same to 0.001) |
| lane, Moster halos | +0.99 / +0.99 / +0.97 / +0.94 (canonical) and +0.98 / +0.97 / +0.84 / +0.55 (alt): the halo sits above threshold and keeps its share |

## Lean (ss2_lean/SS2.lean)

Compiles with exit 0 and standard axioms only (propext, Classical.choice, Quot.sound). The MUTATE (claiming f > 0.85 at
x0 >= 2.4, where the true root is 0.8375) fails, as it must. Proved:
- the closed form solves dy/dtau = -y/(1 + (x0 y)^4);
- F(x, 1/2) = alpha iff x^4 = (64/15)(alpha - ln 2);
- monotonicity in x0;
- the separation bounds at alpha 4.39: x0 <= 0.65 gives f < 0.0137; x0 >= 2.4 gives f > 0.83; x0 >= 3 gives f > 0.94.

These certify the switch, not the physics.

## Disclosures

1. **CLASS validation setting changed after the freeze.** CLASS refuses a dark fluid with w = 0 at early times
   (`w_fld_ini >= 0`). The run crashed before producing any number, so it uses w0 = -0.001 (matter-like to 0.1 %). The
   validation failed for the transfer-function reason above, not because of this.
2. **The growth model** is SS1's: the record's linear two-fluid ODE with a k-dependent non-clustering fraction, lambda for a
   daughter produced at onset, and conversion in every collapsed sub-threshold halo above M_min. The fsigma8 failure rests on
   this linear treatment.
3. **Machinery reused read-only.** SS1's machinery (ss1v.py, ss1.py, ss1_cosmo.py, ss1_bullet.py) runs read-only with
   outputs redirected here. PJ1 loaders come from a read-only copy of origin's lane dir.
4. **Compute.** Every run under 0.6 GB except the DB1 Bullet child (about 1.36 GB, the record's machinery).

## Reading

G's velocity gate separates galaxies from groups the way the record needs. KiDS, SPARC, Ursa Major and Cassini pass, and the
mass-kept daughter removes A's BAO failure. Its pre-conversion halo even has the right per-bin shape for X-COP. But it keeps
the whole pre-conversion share wherever it keeps anything: groups and clusters get 1.3-2x too much. It converts every
smaller collapsed halo into fast daughters, which removes 40-63 % of the component from the small-scale matter field after
z 0.63 and cuts low-z growth far below the fsigma8 rows. The Bullet also fails on DB1's offset rule.

**What a repair would need:**
- **Groups and clusters:** they must keep about 0.45-0.85 of their share, not all of it.
- **Small halos:** most of them must not convert, or their daughters must stay in the small-scale field: about 10 % of the
  component or less may stream out.
- **The test:** the lensing gate needs a time-switched species in CLASS.

## Files

- Criteria: `FROZEN_CRITERIA.md`.
- Scripts: `ss2.py`, `ss2_grade.py`, `run_chain.sh`.
- Outputs: `ss2.json` / `ss2.out`, `ss2_MUTATE.json` / `.out`, `parts/`, the run logs `run_*.txt`.
- Lean: `ss2_lean/`.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
