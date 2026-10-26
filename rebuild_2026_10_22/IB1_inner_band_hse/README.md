# IB1_inner_band_hse: why the core law over-predicts the INNER cluster band. DIAGNOSTICS ONLY (not graded, no criteria frozen)

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

Run: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ib1_diagnostics.py` (about 1 min, one thread).
