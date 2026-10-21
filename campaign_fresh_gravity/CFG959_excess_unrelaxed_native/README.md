# CFG959: the excess family as UNRELAXED native cold energy (H-UNR). PARTIAL under the frozen rule (clusters and red lenses only), FRAGILE; it FAILS on the dSphs and the Coma UDGs

**Plain summary.**
1. The idea: the law is the settled end state of a system's cold energy, only a rotating disc can settle it, and a
   dispersion-supported system keeps its native collapse debris, which would be the excess.
2. Tested with zero new constants, the idea reproduces the eRASS1 cluster cores and outskirts, keeps SPARC discs on the law and
   is consistent with the red lenses. The retained fraction is taken from each system's own kinematics, and the cluster result
   is CFG949's untethered result reused unchanged.
3. It fails on the defining members of the excess family. At dSph apertures the record's native debris is only 0.09–0.56 of the
   law's phantom, and at Coma-UDG apertures 0.55–0.75. Unrelaxed dSphs and UDGs therefore come out BELOW the law, not above it.
   For the dSphs the prediction is −0.57 dex against +0.37 observed: residual +0.90 dex, z +17. For the UDGs the residual is
   +0.51 dex, z +4.5.
4. The per-dwarf pattern runs the wrong way: the dwarfs with the least debris relative to the law carry the largest excess (slope
   of observed on predicted −1.8 ± 0.3).
   The sharp prediction for dSphs against faint rotators at the same g_bar also fails at z +7.5: dSphs are observed 0.25 dex
   above the rotators and predicted 0.50 dex below.
5. The frozen class is PARTIAL on both footings, but FRAGILE (10 of 12 profile/supply corners FAIL). No form, reading or corner
   brings the dSphs within 5σ: the best is +0.25 dex, z +5.5, in the non-conserving additive bracket, and +0.60 dex, z +11, in the
   governing reading. This route does not explain the excess family.

κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻² are scored separately and never pooled. Raw data and framework-native
inputs only. "Cold energy" is the framework's own cold component; no particle species. Not "theory closed". Nothing here says the
data favour the framework.

| | |
|---|---|
| Kind | HYPOTHESIS TEST, zero fitted constants (primary form); a NEW RULE (kinematics-dependent retention, CFG919 family 2) |
| Block | CFG950–959 (LEDGER row "CFG950–959") |
| Criteria | `FROZEN_CRITERIA.md`, **3b52ca39f**, committed alone before any script or number; no amendments |
| Not blind | written after the excess record was read; pre-freeze expectations E1–E7 in criteria §9 (E1 dSphs below the law, E2 R-A overshoots clusters: both confirmed; E3 red-lens overshoot: wrong under the primary form, confirmed only for R-A; E4 UDGs: unknown beforehand, came out below the law) |

## The hypothesis and the derived criterion

- **Rule.** Cold energy relaxes to the law only by handing energy and angular momentum to a coherent baryonic flow. CFG919 proved
  that the record's equation (CFG638) cannot make any kinematic selector, so this is a posit outside the record. It brings no
  new constant.
- **Derived retained fraction (P-LIN).** Random motions exert no secular torque. The debris is shared between the ordered and the
  random channel in proportion to their shares of the baryons' kinetic energy (virial support). The ordered channel relaxes its
  share and the random channel keeps its share. Hence

      u = K_rand/K = f_P = 3σ²/(v² + 3σ²)

  This is CFG919's own measure, taken per system from data. It has no threshold and no constant; items 2–3 of the argument are
  the posit.
- **Reported alternative forms:**
  - V-EQ: u = Θ(f_P > ½), no constant.
  - V-OP: u = Θ(f_P > 0.72), from the Ostriker–Peebles T_rot/|W| = 0.14. This constant is imported, not derived.
- **Model, primary reading R-C (mass-conserving):**

      g = g_N + G[min(M_ph, (1−u)M_c) + u·M_cNFW]/r²

  At u = 1 this is CFG949's B0.
- **Secondary reading R-A (additive):** g = g_law + u·G·M_cNFW/r². It double-counts the cold energy and is reported as a bracket
  only.
- **Native supply.** M_c = 5.364 × catchment baryons (census f_ret, CFG804 fixed point), in the CFG930 R930 NFW: C 3000, r_ta,
  native EPS z_c, z_i = 0 for galaxies and each cluster's own z.

## Result: primary form P-LIN, reading R-C, primary corner

| item | f_P → u | canonical | alt | label (can / alt) |
|---|---|---|---|---|
| (a) SPARC, CFG695 S2 (rms ≤ 0.110, Υ 0.50–0.80) | 3σ²/(V_flat²+3σ²), σ 10; median 0.029, max 0.49 | 0.1013 @ 0.59 (Δ +0.0004) | 0.1002 @ 0.55 (Δ +0.0008) | PASS / PASS |
| (a2) B21 n < 2 lenses (rotation-supported) | 0.20 | resid −0.159 ± 0.091 ln (z −1.7) | −0.236 ± 0.091 (z −2.6) | CONSISTENT / TENSION |
| **(b) dSphs, 83 LVD** (record +0.372 / +0.332 dex) | 1 | predicted −0.566 dex; **resid +0.900 dex (z +17.3)** | predicted −0.605; **resid +0.900 (z +17.3)** | **CONTRADICTED** |
| **(b2) per-dwarf scatter** | — | s 1.32 [1.12–1.58] vs constant 0.955; Δ(−2lnL) −45.9; slope E_obs on E_pred **−1.82 ± 0.27** | 1.32 vs 0.950; −46.3; −1.79 ± 0.27 | **FAIL** |
| **(c) Coma UDGs, 9** (+0.760 / +0.669 ln) | 1 | predicted −0.424 ln; **resid +1.184 ± 0.262 ln (+0.51 dex, z +4.5)** | −0.515; +1.184 ± 0.262 (z +4.5) | **CONTRADICTED** |
| (d) eRASS1 clusters (318) | 1 | MID 1.011 ± 0.063, OUTER 1.047 ± 0.089, s 0.661 (−1.12 s_err) | identical (no a0 at u = 1) | EXPLAINS (= CFG949 B0) |
| (e) red lenses n > 2 (+0.293 / +0.203 ln) | 0.80 | resid +0.089 ± 0.067 (z +1.3); IMF +0.006 ± 0.066 | +0.073 (z +1.1); IMF −0.009 | CONSISTENT (both versions) |
| (f) TDGs; DF2/DF4 (no capture → Newton) | — | +0.055 ± 0.114 dex; +0.028 ± 0.539 ln | same | CONSISTENT (inherited) |
| (g) McQuinn faint rotators, bracket B (25) | 3σ²/(V_rot²+3σ²), σ 10 | resid −0.150 ± 0.066 dex (z −2.3); A −0.345 ± 0.069 | −0.183 ± 0.066 (z −2.8) | TENSION / TENSION |
| (g2, reported) dSph − rotator, cell [10⁻¹², 10⁻¹¹·⁵) | — | D_obs +0.253, D_pred **−0.495** ± 0.100 (z +7.5; 10 dSphs, 18 rotators) | +0.253 vs −0.529 (z +7.8) | sharp prediction FAILS |
| (g) rotating UDGs | — | none in the record | — | NOT TESTABLE |

**Frozen class: PARTIAL on both footings.**
- Explained: (d) clusters and (e) red lenses.
- Not explained: (b) dSphs and (c) Coma UDGs; (b2) fails.
- The anchor holds: (a) PASS, (a2) and (g) are not CONTRADICTED.

**Robustness: FRAGILE.** Over the 12 corners (C 1500/3000/6000 × r_ta/r_vir × census/×2 supply) the class is PARTIAL at 2 and
FAILS at 10, on each footing.

### Why: the native debris sits below the phantom at small apertures

- **Q = native debris / settled phantom at the observed aperture** (canonical):
  - dSphs: median **0.239** (0.093–0.555), Q > 1 in **0 of 83**;
  - Coma UDGs: median **0.595** (0.551–0.746);
  - L* lenses at 20–110 kpc: ≈ 1 (M_deb/M_b 2.53–10.07 against a phantom of 2.59–9.18 M_b, `cfg959.out` diagnostics);
  - cluster cores: > 1 (CFG949).
- An unrelaxed system can sit above the law only where Q > 1. H-UNR therefore makes the cluster-core excess, but puts dSphs and
  UDGs below the law, with the wrong sign.
- Across the 83 dwarfs, the observed offset falls as H-UNR's predicted offset rises (slope −1.82 ± 0.27): the dwarfs with the
  smallest Q carry the largest excess, so H-UNR's per-dwarf predictions anti-correlate with the data.
- This confirms CFG930 D4 and CFG955 T-EX for a kinematic selector. It also gives the UDG Q values that T-EX had not computed:
  0.55–0.75 rather than the dwarf 0.14–0.32, still below 1.
- **u < 1 and u = 1 behave very differently in R-C.**
  - For u < 1 with (1−u)·M_c ≥ M_ph the model is the law plus u·debris, i.e. above the law. That is why the red lenses
    (u = 0.8) come out CONSISTENT: +0.46 ln at 35–109 kpc. At 346 kpc the supply cap binds and the prediction drops to
    −0.195 ln.
  - At u = 1 it is debris only, i.e. below the law.
  - So the two explained items come from different regimes of the same model. The red-lens pass vanishes when u = 1 for
    f_P = 0.8 (V-EQ, V-OP).

## Forms, readings and brackets (primary corner; reported, they do not change the governing class)

| setting | (b) dSph resid | (c) Coma | (d) clusters | (e) red lenses | (a2) / (g) | class (can / alt) |
|---|---|---|---|---|---|---|
| **P-LIN, R-C (governing)** | +0.900 dex, z +17 | CONTRADICTED | EXPLAINS | CONSISTENT | (a2) CONSISTENT / TENSION; (g) TENSION / TENSION | PARTIAL / PARTIAL |
| P-LIN, R-A (additive) | +0.282 / +0.249 dex, z +6.2 / +5.5 | **CONSISTENT** (+0.31 / +0.25 ln, z +1.2 / +0.95) | FAILS (MID 0.707, OUTER 0.554; 0.684 / 0.527) | CONTRADICTED (overshoot, −0.20 / −0.26 ln) | — | PARTIAL (Coma only) |
| V-EQ, R-C | +0.900 dex | CONTRADICTED | EXPLAINS | CONTRADICTED (+0.42 ln, z +6.3: u = 1 removes the law) | CONSISTENT / CONSISTENT | PARTIAL (clusters only) |
| V-OP, R-C (imported 0.14) | +0.900 dex | CONTRADICTED | EXPLAINS | CONTRADICTED | CONSISTENT / CONSISTENT | PARTIAL (clusters only) |
| V-EQ / V-OP, R-A | +0.28 / +0.25 dex | CONSISTENT | FAILS | CONTRADICTED | CONSISTENT (V-EQ alt rotators TENSION, z −2.3) | PARTIAL (Coma only) |
| dSph f_P bracket (HI v/σ 1, others 0.5) | +0.461 / +0.450 dex, z +9.8 / +9.6 | CONTRADICTED | EXPLAINS | CONSISTENT | as primary | PARTIAL |
| σ 6 km/s / σ 20 km/s (SPARC, rotators) | +0.900 | CONTRADICTED | EXPLAINS | CONSISTENT | σ 20 alt: rotators CONTRADICTED (−0.225, z −3.4) | PARTIAL; σ 20 alt FAILS |
| lens f_P (0.43, 0.57) / (0.10, 0.97) | +0.900 | CONTRADICTED | EXPLAINS | CONSISTENT / CONTRADICTED | (0.43, 0.57): n < 2 CONTRADICTED (−0.31 / −0.37 ln) | FAILS / PARTIAL (clusters only) |
| clusters at z_i = 0 | +0.900 | CONTRADICTED | EXPLAINS (1.091, 1.107) | CONSISTENT | as primary | PARTIAL |

- No setting explains the dSphs. The smallest dSph residual anywhere is +0.249 dex (R-A, alt, z +5.5); in R-C it is +0.595 dex
  at the most generous corner (C 6000, r_vir, ×2; z +11.2).
- R-A rescues the Coma UDGs. But it double-counts the cold energy, overshoots the cluster core ×1.4 (A_MID 0.71) and overshoots
  the red lenses.
- The governing reading cannot have both: R-C has the clusters without the UDGs, and R-A has the UDGs without the clusters.
- Supply and boundary trade the classes against each other:
  - more debris (×2, r_vir, C 6000) moves the Coma UDGs toward the data (CONSISTENT only at C 6000 r_vir ×2);
  - but it breaks the clusters (A_MID 0.39–0.79), the red lenses, the n < 2 lenses and the rotators;
  - the dSphs stay CONTRADICTED at every corner (+0.60 to +0.99 dex, z +11 to +19).

## Controls

- **K 9/9 PASS** (`cfg959_K.out`):

  | test | what it checks | max difference |
  |---|---|---|
  | K1 | CFG919 class means DW / LS / LD | 0 |
  | K2 | CFG687 A through CFG949's machinery | 1.6e-15 rel |
  | K3 | CFG949 B0 primary corner A_MID 1.0109 ± 0.0632, A_OUTER 1.0469 ± 0.0888, s 0.6615 = H-UNR R-C at u = 1, and this lane's cold builder = CFG949's | 0 |
  | K4 | CFG930's SPARC native-halo medians (147 galaxies) | 1.1e-16 |
  | K5 | CFG695 S2 0.10091 @ 0.60 / 0.09943 @ 0.55 | 6.9e-17 |
  | K6 | CFG933 Coma +0.76036 ± 0.26180 ln | 0 |
  | K7 | CFG936 route (i), and Newton-exact DF2/DF4 = its 'S4 strict f=0' corner | 1.4e-17 |
  | K8 | CFG940 WS means A −0.3041 ± 0.0675, B −0.0833 ± 0.0637 dex, its per-galaxy E from its logs, and the Table 2 V_rot/V_cor parse | 2e-15 |
  | K9 | CFG880's 83 σ_law | 0 |

- **MUTATE: 3/3 arms bite** (`cfg959_MUTATE.out`):

  | arm | what it does | result |
  |---|---|---|
  | **M-DISC** | u = 1 for discs too | SPARC 0.1109 @ Υ 0.67 on both footings, FAILS the 0.110 line, **but only by 0.0009 dex** |
  | **M-ZERO** | no retained debris | every record offset returns to 2.2e-16 (dSph +0.856 / +0.765 ln, Coma, red lenses, cluster A, SPARC), so the excesses reappear as model deficits. With the supply cap kept at u = 0 the dSph mean moves by +2.5e-4 / +1.6e-3 ln, and no SPARC point is capped |
  | **M-PLANT** | observed values replaced by the H-UNR prediction plus noise | every planted item comes back CONSISTENT / EXPLAINS (dSph +0.040 ± 0.084, Coma +0.171 ± 0.262, rotators +0.022 ± 0.057, lenses 0, clusters MID 1.037 OUTER 0.962) |

  In M-DISC the native debris nearly passes SPARC on the CFG4 statistic. With u = 1, the n < 2 lenses give +0.023 ± 0.091 and
  the rotators +0.138 ± 0.064 dex.

## Side findings (no class weight)

- **The native debris rule mimics the law in massive galaxies.**
  - At u = 1, SPARC gives 0.1109 and the n < 2 lenses give +0.02 ln, because Q ≈ 1 at 20–100 kpc for L* systems.
  - So the galaxy-scale separation between "law" and "native debris" rests on dwarf-sized systems, where the debris falls short.
  - This is a statement about the CFG930 collapse convention (C 3000, NFW97-style), not a ΛCDM input.
- **DF2/DF4.** If they had kept native debris (u = 1) they would sit at −0.398 / −0.460 ln, against −1.709 / −2.170 observed
  (z −2.4 / −2.2). The derived no-capture label does all the work for (f), as CFG936 said.
- **The matched-cell test in the governing form makes (g2) a clean kill of the kinematic picture with native debris.**
  - Rotators get a little debris on top of the law (u = f_P 0.085–0.75, median 0.43; 0.75 at V_rot 10 km/s, 0.43 at 20 km/s).
  - dSphs get debris instead of the law.
  - So H-UNR predicts dSphs below the rotators, while the data put them 0.25 dex above.

## What is established

- With the record's native-debris rule and a kinematic retention rule that has no constant, unrelaxed native cold energy cannot
  produce the dSph excess:
  - CONTRADICTED at every corner, form, reading and bracket tested;
  - mean, per-dwarf scatter and the matched-cell discriminator all fail;
  - both footings.
- It cannot produce the Coma-UDG excess in the mass-conserving reading.
- It reproduces the cluster core and outskirts only because at u = 1 it is CFG949's B0. That result keeps CFG949's fragility
  (supply ×2 or r_vir → FAILS) and its extrapolated-gas caveat.
- H-UNR does supply the selector CFG949 lacked (clusters are dispersion-supported). But the same selector applied to dSphs and
  UDGs gives the wrong sign.

## What is NOT established

- **No other supply rule is excluded.** Every number uses the census catchment (5.364/f_ret, f_ret 0.10 for galaxies) and
  CFG930's collapse convention. CFG930 D3 showed that a supply ~6000× larger would be needed for the ultra-faints.
- **The derivation of u = f_P is a posit-level argument, not a theorem.**
  - The bang-bang relaxation and the virial share are assumptions.
  - The record's equations contain no torque channel at all (CFG919).
- **Inputs are declared, not measured.** Lens kinematics are CFG919's Sérsic proxy, and the dSph/UDG f_P is a class value (no
  rotation data on disk). The lens point-mass radius and the 4GΔΣ-vs-3D comparison are the record's conventions; the NFW-vs-SIS
  difference is not corrected.
- **Groups and rotating UDGs are untested.**
- **The excess family is still unexplained.**

## Disclosures

1. **First K attempt (2026-10-21, no output files written, before any H-UNR number).** It stopped for two reasons:
   - K1 failed at 1.5e-6. The dwarf estimator was built with CFG4's unrounded FP0 a0, which differs from the rounded footing by
     2.6e-6 relative. The dwarf, lens, UDG and rotator estimators were switched to the rounded footings their record lanes use.
     SPARC and the clusters keep FP0, as CFG695 and CFG687 do.
   - A JSON key path for K3 was wrong (`main.B0_primary`).
   - K1 diagnostics were added to the check line. Nothing else changed.
2. **The dSph cell for (g2)** uses the 83 CFG880 dwarfs (declared in the criteria). CFG940 used CFG828's 29 (6 in the cell,
   +0.318 ± 0.108). Here 10 dwarfs are in the cell (D_obs +0.253).
3. **Runs.** Peak RSS 0.35 GB, one core, nice 10, one process at a time. MAIN takes 16 s. The K and MUTATE stages each take a few
   seconds.
4. **Final reruns.** A reported-only diagnostic block (lens debris vs phantom; rotator u range) was added to MAIN after the first
   full run, so that every README number comes from a committed output. K, MUTATE and MAIN were then rerun from the final
   `cfg959.py`. Every graded number and label is identical to the first full run.

## Files and re-run (from this directory, one at a time, `OMP_NUM_THREADS=1 nice -n 10`)

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (3b52ca39f) |
| `cfg959.py` | K, MUTATE, MAIN |
| `cfg959_K.out`, `cfg959_results_K.json` | `CFG959_MODE=K python3 cfg959.py` (exit 0) |
| `cfg959_MUTATE.out`, `cfg959_results_MUTATE.json` | `CFG959_MODE=MUTATE python3 cfg959.py` (exit 0 = all arms bite) |
| `cfg959.out`, `cfg959_results.json` | `python3 cfg959.py` (main; re-checks K first; exit 0) |

- **Read-only inputs:**
  - CFG949's script slice, exec'd with every write outside this directory refused; through it, CFG686, CFG687, CFG922 and
    CFG932 slices and the CFG654 native tables;
  - CFG880's input slice;
  - CFG919's lens and cell functions, copied verbatim;
  - CFG4_common;
  - committed JSON of CFG919, 930, 933, 936, 940, 949, 695, 880 and 687;
  - McQuinn+22 Table 2, on disk, parsed by byte positions.
- Nothing was downloaded. No other lane, no LEDGER row and no THEORY_CANONICAL file was edited.

κ = ½ FITTED; footings never pooled; cold energy, not a particle; not theory closed.
