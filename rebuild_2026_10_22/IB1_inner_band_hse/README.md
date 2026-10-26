# IB1_inner_band_hse: RESULT HG TRADES (both footings). The gas's hydrostatic mass fixes INNER and every MID cell; OUTER fails in 3 cells, mostly where σ is a tercile fill

Graded under frozen criteria `FROZEN_CRITERIA.md` (0669ca3fc9). Amendment A1 (902e279dfa) is post-result and touches the K1
check window only; a fix-forward (167d264879) followed it. The graded lines are byte-identical to run 1. Checks pass: K0
(OS1 reproduced exactly, both footings), K1 (≤ 6.9e-6), K2 (0.56 GB). MUTATE (2 kT on K1's analytic side) fails K1 and
exits 1. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework.

## Result: HG, cluster total mass = 3β σ² r³ / G(r² + r_c²) from each cluster's own gas (no q, c_f or M_fair)

Canonical; alt gives the same Z, because HG's mass does not depend on a₀ and the footing only rescales the C\* units.

| cell | Z h 0.672 / 0.686 | OS1 Z | |
|---|---|---|---|
| **G-IN-Mall** | **−0.33 / −0.35** | −2.41 FAIL | **fixed** |
| G-IN-all | −0.59 / −0.68 | −1.82 | |
| G-MID-T1 / T2 / T3 / b | −0.07, +0.80, −0.27, +0.19 | −1.72, −1.01, −1.29, +0.85 | all closer to the data |
| G-OUT-T1 / T2 / T3 / b | −0.99, −1.09, −1.34, +0.44 | −1.11, −1.07, −0.33, +1.09 | pass |
| G-OUT-Mall / M2 | +0.32, −0.37 | +0.08, −0.78 | pass |
| **G-OUT-all** (106 KT) | **−2.02 / −2.27** | −1.47 | FAIL (over, marginal) |
| **G-OUT-M1** | **−2.02 / −2.10** | −0.38 | FAIL (over, marginal) |
| **G-OUT-M3** | **+5.02 / +4.36** | +1.81 | **FAIL (under)** |

**Class: TRADES on both footings, so the verdict is TRADES.** The inner miss is gone with no fitted constant, and all four
MID cells move toward the data. Three outer cells that OS1 passed now fail.

Reported (not graded):
- The truncation choice does not rescue it: at r_ta the same 3 cells fail; at 2.2 R500, G-OUT-all and M3 fail.
- σ² × 1.15 (non-thermal pressure, context) adds G-OUT-T3.
- Implied core surface density Σ_HG / Σ_OS1 = 0.37 (0.31–0.47) canonical, 0.41 alt. The core law's cluster cores are
  about 2.5× too dense by the gas's own measure.
- Per-bin pred/meas, innermost to outermost: 1.68, 1.21, 0.99, 0.88, 0.86, 0.91, 1.09, 0.90. Under OS1 the same bins ran
  3.51 down to 0.85. Bin 0 is the null-test-failing bin.

**Not a test (quoted, criteria §1):**
- Groups keep the core law (GR1 PASS, both footings).
- SPARC keeps OS1's core law; it was re-run only as K0.
- What selects HG over the core law is not derived.

## Post-result diagnostic (labelled, not graded; `ib1_post_outer.py` / `.out`, canonical h 0.672)

OUTER pred/meas by MGAS500 tercile, split by where σ comes from:

| tercile | KT clusters (σ from kT) | σ-filled clusters |
|---|---|---|
| M1 | 7.96 (n 29; meas A 0.14, noisy) | 1.59 (n 80) |
| M2 | 1.71 (n 39) | 0.80 (n 69) |
| M3 | 0.81 (n 38) | **0.52 (n 71)** |

The 220 clusters without kT get OS1/X30's **tercile fill**: one σ per tercile (449 / 507 / 631 km/s). HG's mass scales
as σ², so a per-tercile constant erases the mass trend inside each tercile. The core law did not feel this, because
M_fair ∝ M_b followed each cluster's own gas mass. The M3 under-prediction is carried mainly by the filled clusters (0.52 vs
0.81 for KT).

So the MGAS OUTER fails mostly test the inherited fill, not HG. A next lane would replace the fill with σ predicted from each
cluster's own Mgas500, using the KT clusters' own σ–Mgas500 relation (raw data, no ΛCDM). That needs its own frozen
criteria. Two things stand regardless:
- G-OUT-all (KT only, Z −2.02 / −2.27) is a marginal over-prediction on measured temperatures, with no fill involved;
- G-OUT-M1's KT subset (n 29) is very noisy.

## Earlier: diagnostics run before the criteria (b963ce381c)


Question (owner, 10-26): what makes the core law over-predict the INNER cells ~2× without breaking groups and MGAS T3 OUTER?

Read-only on IC1's loader (`ic1b_lib` → SC1 → X38 → X30/X2/X7), at OS1's q_f (0.892 / 0.748), h 0.672. κ = ½ FITTED.
Not theory closed. Nothing here says the data favour the framework. **Nothing below is a verdict.** A graded lane needs
frozen criteria first.

## Findings (`ib1_diagnostics.out`; canonical, alt in brackets)

**D1. The excess grows steadily inward.** Pred/meas by bin, from the outermost (bin 7) to the innermost (bin 0), over all
326 clusters: 0.85, 1.25, 1.18, 1.27, 1.42, 1.72, 2.19, **3.51** [alt 0.84 … 3.11].
- Bin 0 (~0.15 Mpc) carries a cross shear of −4.4 A units (−4.0). It fails its own null test. That is where INNER's large
  s_IN comes from.
- Bins 1–2 are still over by 2.2× and 1.7×, so dropping bin 0 would not remove the miss.
- The OS1 halo core is compact: median r₀ is 0.12 Mpc (16–84% 0.07–0.16).

**D2. X-ray data, independent of lensing, show the same excess.** The record's gas profile (β = 2/3, r_c = 0.15 R500)
with the measured isothermal kT fixes a hydrostatic mass. For the 106 KT clusters, the ratio (OS1 halo + baryons) / M_HSE
has these medians:

| r (Mpc) | 0.15 | 0.30 | 0.46 | 1.0 | 2.0 |
|---|---|---|---|---|---|
| canonical | 1.98 | 1.80 | 1.62 | 1.28 | 0.95 |
| alt | 1.81 | 1.70 | 1.57 | 1.25 | 0.94 |

At r ≥ 0.3 Mpc (r ≫ r_c), M_HSE ≈ 2σ²r/G does not depend on the assumed r_c. So the ~1.7× excess at 0.3–0.46 Mpc does not
rest on the gas-core convention. The radial pattern tracks D1's lensing pattern.

**D3. The hydrostatic mass alone lenses correctly in all three bands** (KT_all, 106 clusters; route E: total mass = M_HSE,
Newtonian, truncated at 3 Mpc like the gas):

| band | measured A | OS1 pred | M_HSE pred |
|---|---|---|---|
| INNER | 1.94 ± 1.67 | 4.98 | 2.92 |
| MID | 1.67 ± 0.34 | 2.09 | 1.63 |
| OUTER | 0.72 ± 0.17 | 0.92 | 1.00 |

(alt: INNER 1.78 ± 1.53 / 4.23 / 2.68; MID 1.53 ± 0.31 / 1.86 / 1.49; OUTER 0.66 ± 0.15 / 0.84 / 0.92)

## Reading (diagnostic)

The ~2× INNER miss is not a lensing artefact. The core-law halo puts about twice the mass inside 0.5 Mpc that the cluster
gas can be holding up at its measured temperature. The gas's own hydrostatic mass matches the measured lensing in INNER and
MID, and is 1.7σ high in OUTER.

The core law sets the cluster core from two ingredients:
- Σ ∝ σ^q, extrapolated from SPARC;
- M(r_ta) = M_fair, where M_fair = 5.364 M_b, the Planck ΛCDM ratio. The owner banned it on 10-25.

In clusters, these two together overfill the core.

A candidate fix, derived rather than fitted (NOT tested here): cold dark energy and gas in the same potential with equal σ
(both isothermal) share one density shape, ρ_c ∝ ρ_g. Hydrostatic equilibrium then fixes the total. This removes M_fair
(and with it 5.364), q and c_f from clusters. It is a structural change to the flagship's cluster sector, so it is the
owner's call. Before grading it needs:
- frozen criteria;
- the 220 clusters without KT (σ fill);
- the groups and MGAS T3 OUTER keys;
- a statement of the inherited conventions: β = 2/3 and r_c = 0.15 R500 (fixed, not fitted), and the ΛCDM-processed
  R500 in r_c.

Run: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ib1_diagnostics.py | ib1_hse_halo.py [--mutate] | ib1_post_outer.py` (each under a minute, one thread).
