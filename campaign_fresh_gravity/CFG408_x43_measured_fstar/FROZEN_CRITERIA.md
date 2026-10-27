# CFG408 FROZEN CRITERIA: X43 re-scored with measured stellar fractions instead of f★ = 0.20 (KiDS cluster keys and X-COP)

Committed alone, with its LEDGER row, before any script exists. κ = ½ FITTED; footings never pooled; cold dark energy, never a particle; not theory closed. Nothing here says the data favour the framework. Owner (2026-10-27): "Yes, write frozen criteria for re-scoring X43 (KiDS keys and X-COP) with measured stellar fractions instead of f* = 0.20. Check the CFG ID blocks first." The owner chose ID CFG408, a spare in the 10-06 block 400–409. It is unused in the LEDGER, directories and committed .md files.

## Why
- X43 (00bc1a7950), X30, X2 and CFG687 all set the stars to **0.20 × gas** at every radius. In X30's `prep(i, …)`, the line is `Mb = Mg*(1 + 0.20)`. Because X43 ties the cold mass to the baryons (M_fair = 5.364 M_bt), f★ scales the whole prediction.
- **CFG407** (2803cc10a0, post hoc, labelled): X-COP's measured M★/M_gas(<R500) is 0.035–0.074. With measured baryons, X-COP sat +0.05 to +0.08 dex above X43 (MIXED), the same sign as KiDS G-OUT-M3.
- **CFG922** (a9d0669c5): the KiDS census of measured stars is below f★ = 0.20 (A1 central S/M_gas,cyl median 0.034; 84th percentile of the upper estimate 0.217).
- **This lane replaces the assumed 0.20 with measured values** and asks whether X43's cluster grades survive.

## Measured stellar fractions (inputs; all on disk)
- **KiDS / eRASS1:** CFG922's census, **A1 version** (`CFG922_cluster_core_baryon_recheck/cfg922_census_A1.json`, 318 clusters in CFG687 order).
  - Per cluster: f★ = S / gas_cyl, with S the stellar mass and gas_cyl the gas mass, both inside the projected R ≤ 0.5 Mpc cylinder.
  - A1 is primary because it corrects the frozen census's documented low bias (aperture → total flux, masked galaxies kept, coverage gaps filled with medians). The frozen census is a reported low bracket.
- **X-COP:** `*_mstar.fits` (HDU2) for the 7 clusters that have it (A85, A644, A1795, A2029, A2142, A2319, ZW1215).
  - f★ = M★(<R500)/M_gas(<R500), after the BAO-raw q conversion (M★ × q², M_gas × q^2.5).
  - **The 5 clusters without stars** (A1644, A2255, A3158, A3266, RXC1825) get the **median of the 7** (declared fallback).

## How f★ enters (one injection; everything else is X43 as committed)
- **Profile:** f★ is held **constant with radius** (stars ∝ gas), exactly X43's structure, with 0.20 replaced. The core ratio is an *upper* estimate of the outer stellar share, since stars are more concentrated than gas. This choice can only *under*-state any deficit that lower stars create.
- **KiDS keys:** X43 is run in subprocesses exactly as CFG406 did (cfg406_rescore.py's child pattern). The one replacement in X30's code is `Mb = Mg*(1 + 0.20)` → `Mb = Mg*(1 + __FS__[i])`, asserted once. Every prediction, every in-run baseline (DC) and every in-run measured statistic is recomputed. M_fair = 5.364 M_bt follows the new baryons. Terciles (T3M, TID) are unchanged.
- **Stored X7 values** (G-OUT-Mall, G-OUT-M1..3) are rescaled by the baseline ratio R, as in CFG406. **K5** checks exactness. If it fails, those keys are marked APPROXIMATE but still graded, as in CFG406.
- **Matching the 326 X7/X30 clusters to the 318 census rows:** nearest RA/Dec within 30″ (the census is in `cfg687_percluster.npz`'s ra/dec order).
- **KiDS f★ variants:**
  - **F-TERC (PRIMARY):** each cluster gets the **median A1 central f★ of its observed-Mgas500 tercile** (X30's T3M, using matched clusters only). Clusters without a census match also get their tercile median. Tercile medians keep the mass dependence and suppress per-cluster noise (net = aperture − background, floored at the BCG).
  - **F-UP (bracket):** the same, using the A1 *upper* estimate S_up / gas_cyl.
  - **F-CLUSTER (reported):** per-cluster A1 central f★ where matched, tercile median otherwise.
  - **F-FROZEN (reported, low bracket):** tercile medians of the frozen census.
  - **F-XCOP (reported):** a constant f★ = the X-COP-7 median, for every cluster (a heavy-cluster calibration).
- **X-COP part:** CFG407's machinery, with X43's recipe (X30 gas "P" from X-COP's Mgas500, BAO-raw distances, 4 footing × h cells), M_b = Mg_P × (1 + f★,i) with X-COP's own f★,i, and the statistic and classes exactly as CFG407 (Δ = log10[M_HSE/(1−b)/M_X43] over 5 radii in [R500, R200]; b = 0 and 0.3).
  - **X-PRIMARY:** all 12 (7 measured + 5 fallback).
  - **X-7 (reported):** the 7 only.
  - **X-PROF (reported):** the 7 with their measured stellar *profile* (MSTAR(r), continued ∝ gas beyond its last point) instead of a constant ratio.
  - **X-NAT (reported):** X-PRIMARY on the native background (5.2715; CFG407's V-NAT code).

## Readings (frozen)
- **KiDS part (PRIMARY F-TERC; per footing; X43's |Z| ≤ 2 in both h cells):**
  - **X43 GAINS:** the failing cluster-key set is a strict subset of X43's {G-OUT-M3}.
  - **X43 HOLDS:** the same set.
  - **X43 LOSES:** any new failure. The README names each, with its sign.

  The groups key is unchanged (Tian+ masses; no f★) and is reported at Z +2.05.
- **X-COP part (X-PRIMARY):** CFG407's classes verbatim: EXCESS CONFIRMED / X43 OVERPREDICTS / CONSISTENT / MIXED.
- **Combined label (frozen):**
  - **BOTH CONFIRM UNDER-SUPPLY:** KiDS G-OUT-M3 fails as UNDER on both footings, AND X-COP is EXCESS CONFIRMED.
  - **KIDS ONLY:** G-OUT-M3 fails UNDER, and X-COP is CONSISTENT or MIXED.
  - **X-COP ONLY:** G-OUT-M3 passes, and X-COP is EXCESS CONFIRMED.
  - **NEITHER:** G-OUT-M3 passes, and X-COP is not EXCESS CONFIRMED.
  - **CONTRADICTORY:** any OVERPREDICTS together with a KiDS UNDER failure.

  "Under-supply" refers to X43's heavy-cluster outskirts only.

## Controls (each must pass, or that part is INVALID; K5 only marks keys APPROXIMATE)
- **K1 (KiDS identity):** with f★ ≡ 0.20 through the injection, every committed X43 cluster cell (meas, s, pred, Z; both footings and h cells) is reproduced to ≤ 1e-9.
- **K2 (census read):** the A1 census reproduces CFG922's printed summary (ratio_cen_median 0.0340, ratio_up_84 0.2165, n_not_measured 33) to the printed precision. At least 300 of the 326 X7 clusters match within 30″. The count is printed and unmatched clusters are listed.
- **K3 (X-COP identity):** with f★ ≡ 0.20 for all 12, CFG407's PRIMARY Δ̄ (b = 0) is reproduced in all four cells to ≤ 1e-9.
- **K4 (X-COP f★ read):** the 7 measured f★,i equal CFG407's post-hoc printout (0.035 / 0.071 / 0.062 / 0.074 / 0.065 / 0.048 / 0.053 for A85, A644, A1795, A2029, A2142, A2319, ZW1215) to 3 decimals at q = 1. This is a re-read, not a re-derivation.
- **K5 (stored-X7 rescale exactness):** as CFG406. Failure marks G-OUT-Mall / M1..3 APPROXIMATE.
- **MUTATE (rc 1):** f★ = 0.60 for every cluster (×3 the assumed value, in the opposite direction from the measured one). KiDS G-OUT-M3's predicted A must **rise** and X-COP's Δ̄ must **fall**, on both footings. This proves the injection reaches the cold mass.

## Not blind (disclosed)
- **Seen:**
  - CFG922's README, including the A1 summary numbers above.
  - CFG407's per-cluster X-COP f★ and its V-MEAS results.
  - CFG406's X43 behaviour when the baryons drop: G-OUT-M3 worsened while the other keys moved toward or past zero.
- **Not computed:** the per-tercile census medians, and any X43 or X-COP number under a changed f★.
- **Expectation:**
  - **X-COP:** f★ ≈ 0.06 instead of 0.20 lowers M_b by about 12 %, and so the prediction by about 0.05 dex. Δ̄ is then about +0.04 ± 0.03: CONSISTENT, possibly EXCESS on some cells.
  - **KiDS:** if the tercile medians are well below 0.20, G-OUT-M3 worsens, and G-OUT-Mall may cross +2 (a new UNDER failure).
  - If the light tercile's f★ is near or above 0.20, the light keys barely move.

## Disclosed inherited inputs
X43 as committed: the Planck ratio 5.364 and X30's OB946 / H0 67.4 in M_fair and r_ta (owner's 10-25 rule; flagged); c_f = 4 external; "A_c2b_refit" EPS background. The native background is reported for X-COP only (X-NAT). On the KiDS side it would need a second injection and is out of scope here. CFG922's census uses LePhare stellar masses (GAaP → total-flux rebuild with H0 70 / Ω_m 0.3 bookkeeping, as CFG922 disclosed).

## Statement-change rule
- Only X43's failing-key list and the heavy-cluster status line may change, in LEDGER (and STANDING, if one exists), per the frozen readings.
- If KiDS LOSES: the record says X43's 14/15 cluster pass rests on f★ = 0.20, and gives the count under measured stars.
- No a0 value, no "favours", no change to X43's frozen verdict text.

## Compute and files
Single thread (nice), CPU only. KiDS: X43 child runs for identity, F-TERC, F-UP, F-CLUSTER, F-FROZEN, F-XCOP and MUTATE, about 85 s each (~10 min). X-COP: about 1 min. RSS < 1 GB, no downloads. Allowed under the small-job rule while the X48 runs are live. Script `cfg408_measured_fstar.py` (`MUTATE=1`; the internal `--x43 <variant>` child mode, as CFG406). Outputs `cfg408.out`, `cfg408_results.json`, `_MUTATE` siblings, the child outputs, README. Nothing is written outside this directory.
