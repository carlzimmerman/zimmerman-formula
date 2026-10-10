# CFG548: weighing the Local Group from its fringe. Verdict NOT DIAGNOSTIC as frozen, leaning TOO MASSIVE (Z +2.78 on both footings). The flow mass, about 1.1–1.7e12, is 3–5× below the framework's 5.85e12. ΛCDM's timing mass is just as heavy, so this measures the known timing-versus-flow tension, not the framework against ΛCDM

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (9eeab46c4). It includes a dated disclosure of what was read and hand-estimated before freezing.
- **Script:** `cfg548_lg_zvs.py`. It writes `cfg548_lg_zvs.out` and `cfg548_results.json`, and with `CFG548_MUTATE=1` it writes the `*_MUTATE.*` files. It takes about 5 min at nice 10 with 2 threads.
- **Settings:** κ = ½ is FITTED. The two footings are never pooled. The cold energy's mass is still required. This is not "theory closed", and nothing here says the data favour the framework.
- **Data:** the committed UNGC (Karachentsev+13, `real_research/data/ungc_karachentsev2013.tsv`). Nothing was downloaded, and no download is needed for this test.
- **Literature values:** published numbers were recalled, not re-fetched, and are marked PROVISIONAL:
  - Karachentsev+09: R0 0.96 ± 0.03 Mpc;
  - Peñarrubia+14: 2.3 ± 0.7e12;
  - Peñarrubia+16, including the LMC: 2.64 (+0.42/−0.38)e12.
- **Not used:** Teyssier/Johnston, Benisty, Hartl/del Pino, Wempe, Anand/Tully and Cosmicflows-4. There is no table on disk and no precise recall.

## The model
- Radial Lynden-Bell–Sandage shells are started on the Hubble flow at the Big Bang and integrated to t0 = 13.80 Gyr. The equation of motion is r'' = −GM/r² + Λ push, taking the first infall/outflow branch.
- Under candidate B the law is switched off outside bound systems. The cold-energy edges (302/427 kpc canonical, 275/389 alt) lie well inside the fringe, so a fringe galaxy feels Newtonian gravity from the LG's total mass (baryons plus settled cold energy).
- In the point-mass primary the two footings give identical R0. That is stated here, not hidden. They differ only through the edges, which sit inside every shell that matters.

## Controls
| control | result |
|---|---|
| K1 | Λ = 0 matches the Lynden-Bell closed form: 1595.4 vs 1595.2 kpc |
| K2 | the ΛCDM radial timing mass is 4.731e12 (D 770 kpc, v_r −109.3) and re-integrates to −109.300 km/s. With v_tan 82.4 the mass is 5.815e12. Reported: F-M1 as a point mass gives −129.1 km/s at 780 kpc, vs −128.5 for CFG522's extended profile |
| K3 | injection–recovery of F-M1: recovered R0 is 0.4% low, mean Z +0.02, so the pipeline can pass a true mass |
| K4 (reported) | linear fit of the f31 = 0.63 flow (0.7–3 Mpc): R0 1093 kpc on all accurate distances, 1036 kpc with the group rule. FP11's committed values are 1050 / 1048 |

## The weighing (frozen sample: 27 galaxies, f31 = 2/3, 0.6–2.5 Mpc)
- M_flow = **1.12e12**, R0_meas = **830 kpc**, σ_int 47 km/s.
- Errors:
  - σ_boot is 80 kpc;
  - σ_sys is 205 kpc, from 9 frame/window variants with R0 between 621 and 1030;
  - σ_tot is 219 kpc, **26% of R0**. That is above the 11.6% diagnostic line, so the frozen verdict is **NOT DIAGNOSTIC**.
- The DESI w0wa backgrounds leave both the fit and the predictions unchanged to within 1 kpc (R0_meas 831).

| model mass | M [Msun] | R0_pred [kpc] | Z (frozen σ) | Z vs K09 0.96 ± 0.03 (+σ_sys) | M_flow/M |
|---|---|---|---|---|---|
| **F-M1 shared catchment** (both footings) | 5.845e12 | 1440 | **+2.78** | +2.32 | 0.192 |
| F-CI census-individual | 8.142e12 | 1608 | +3.54 | +3.14 | 0.138 |
| F-M1, M_b,MW 7.3e10 | 6.048e12 | 1457 | +2.85 | +2.40 | 0.185 |
| F-M1, +M33/LMC baryons | 6.017e12 | 1454 | +2.84 | +2.39 | 0.186 |
| ΛCDM timing, radial | 4.731e12 | 1342 | +2.33 | +1.85 | 0.237 |
| ΛCDM timing, v_tan 82.4 | 5.815e12 | 1438 | +2.77 | +2.31 | 0.193 |

**Variants**
- DESI w0wa (both): F-M1 Z +2.77.
- Growth bracket, reported only (cold mass ∝ t): R0 1244, Z +1.88.
- Reference, NOT candidate B (law on outside, baryons only): R0 2158 / 2261, Z +6.05 / +6.52. This repeats k02/XR4: the plain law overshoots R0 about 2×.
- Rigid-profile variant as frozen: **not computable**. The shells start on the point-mass-total family at r_i ≈ 0.6 kpc, feel only about 1e11 there, and all escape, so there is no zero crossing. See the post-hoc note.

**Hubble slope just outside, reported.** Fitted over R0_meas to 2.5 Mpc: the data give 105 km/s/Mpc (N 17), F-M1 gives 147, ΛCDM radial timing 141, and the best-fit flow mass 110. The F-M1 outflow is too steep in the same direction as the R0 lean.

**Published masses, PROVISIONAL.** F-M1 is 3.1× K09, 2.5× P14 and 2.2× P16 (including the LMC). Taken at face value with the quoted errors, those are Z_mass +20 / +5 / +8. The declared LMC systematic (P16) therefore does not rescue the framework mass.

**Timing agreement (frozen rule).** The R0 weighing **DISAGREES** with the CFG522 timing mass, M_flow/M = 0.192 against a 2σ band of ×0.20–4.88. This is marginal, right at the band edge. The ΛCDM radial timing mass formally AGREES (0.237), and the ΛCDM v_tan 82.4 mass DISAGREES (0.193).

**Post-hoc common f_ret** implied by the flow mass: 1.03. This is essentially CFG522's f_ret = 1 total (1.15e12), which the LG timing rejects at z −22.8. The flow and the timing pull f_ret in opposite directions.

## MUTATE
- **T1 PASS:** at fixed M, Λ moves R0 inward by a factor of 0.903 (1595 → 1440 kpc), and Λ = 0 equals the closed form.
- **T2 FAIL (frozen tooth):** F-M1 × 0.3 = 1.75e12 gives Z +0.61, not ≤ −2. I checked why rather than accept it.
  - The tooth assumed the framework mass would sit near the measured one.
  - The measured flow mass (1.12e12) is below even 0.3 × F-M1. With σ_tot at 26% of R0, the frozen statistic cannot call 1.75e12 too light.
  - So this failure is the same weakness as NOT DIAGNOSTIC. It is not a bug, and it is recorded as a failed control.
- **T3 PASS:** shuffling distances kills the v–R relation. |r| falls from 0.80 to a median of 0.14, and ΔlnL ≥ 10 in 100% of 200 permutations (median 21).

## Verdict: **NOT DIAGNOSTIC** (frozen rule; σ_tot/R0 = 0.26)
1. **Lean.** It leans **TOO MASSIVE** on both footings: F-M1 Z +2.78 (frozen σ), +2.32 against the published R0 0.96 ± 0.03, and F-CI +3.54.
2. **What drives the large σ_sys.** The frozen window starts at 0.6 Mpc from the barycentre. With f31 = 2/3 the MW sits at 518 kpc from it, so bound MW satellites (Leo I/II, Leo IV/V, CVn I, Phoenix, Cetus at 0.6–0.7 Mpc) enter the fit and drag the 0.5–2.0 Mpc variant down to R0 621.
3. **POST HOC (dated 2026-10-09, not the verdict).**
   - Removing galaxies within 300 or 400 kpc of the MW or M31 gives N 22, M_flow 1.73e12 and **R0 960 kpc**, the same as Karachentsev+09. σ_tot/R0 is then 0.109, which would be diagnostic.
   - Z is then **+4.6 for F-M1**, +6.2 for F-CI, +3.7 for ΛCDM radial timing and +4.6 for ΛCDM v_tan 82.4.
   - A rigid-profile run with a self-consistent start gives R0 1455 (Z +2.84 at the frozen σ), the same as the point mass.
4. **Read this honestly.**
   - The framework's shared-catchment mass is too heavy for the local Hubble flow by a factor of about 3–5. Its outflow slope is also too steep.
   - **ΛCDM's own timing mass misses in the same way.** F-M1 (5.85e12) is almost exactly the ΛCDM timing mass with Gaia v_tan (5.82e12).
   - So R0 does not separate the framework from ΛCDM here. It exposes the timing-versus-flow mass tension that both share.
   - That tension is a known literature issue, recalled PROVISIONALLY; candidate causes are non-sphericity, the LMC, and the local mass history.
   - **For the framework specifically,** the flow wants f_ret ≈ 1, while the timing wants f_ret around 0.12–0.30. A single cold-energy supply cannot satisfy both with this point-mass model.

## Scope (declared)
- Spherical point mass (no MW–M31 quadrupole) and first branch only.
- No intervening background matter (the Lemaître–Tolman version is not modelled).
- Cold energy settled at all times. The growth bracket only shows the direction: a later-settled mass lowers R0, to Z +1.9.
- Vlg frame from the catalogue. The barycentre's own motion from M31's tangential velocity is not propagated into the flow frame.

## Dated notes (2026-10-09)
- **Development run.** The first full run (before the post-hoc block was added) gave identical frozen numbers. The post-hoc block (satellite cut and self-consistent profile start) was added after the frozen results were read, and it is labelled post hoc in the script and the `.out`.
- **Spurious floating-point warnings.** Accelerate matmul flagged warnings on UNGC rows without coordinates. They are suppressed with `np.errstate`; the values were unaffected.
