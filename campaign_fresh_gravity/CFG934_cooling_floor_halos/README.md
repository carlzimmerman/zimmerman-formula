# CFG934: cooling-floor primordial halos (H-CF). Reading (S): PARTIAL on both footings, FRAGILE. Reading (M): PARTIAL (corner-selectable)

**Bottom line.** A parameter-free floor (every star-forming dwarf sits in a primordial cold-matter halo at least as massive as
the atomic-cooling threshold T_vir = 1e4 K at its formation epoch) does part of the job and not all of it.

- **What it does.** Under the primary sum reading (S), it closes the MW ultra-faints at the ionised (μ 0.59) τ50 corners:
  +0.325 / +0.304 dex goes to −0.066 … +0.055 dex. It leaves the MW classicals, the M31 dSphs and all 110 gas-rich SPARC dwarfs
  exactly where the bare law puts them. CFG42's classical over-prediction disappears, because the floor masses (1e8–2e9 M☉)
  are 10–100× below the Moster masses CFG42 used.
- **What it does not do.** The LVD-83 class stays CONTRADICTED at 11 of 12 corners on both footings, and TENSION at the 12th:
  +0.518 / +0.472 ln goes to +0.110 … +0.403 ln. The isolated LG dwarfs stay at their bare-law TENSION.
- **Why.** The sum reading's leftover fraction f_ex is zero whenever the law's own phantom inside CFG35's edge exceeds the
  floor's cold mass. That happens from M_b ≈ 9e4 M☉ (μ 0.59) or 2–4e4 M☉ (μ 1.22) upward, except for late-forming dwarfs whose
  own SFH gives a larger floor. It covers the intermediate dSphs (−10 < M_V ≤ −7.7: Draco, And IX, And V, …), which carry
  +0.24 to +0.36 ln of residual. The floor reaches the faint dwarfs and closes them; it does not reach the intermediate ones.
- **Not FAILS only narrowly.** The frozen FAILS rule needs one class CONTRADICTED at all 12 corners. LVD-83 reaches TENSION
  (z +2.38 / +2.20) at the single most generous corner (μ 0.59, τ50, C 6000).
- **FRAGILE.** With Υ_V = 1 for the I and L classes the verdict becomes FAILS. With Υ_V = 4, or CFG930's uniform Υ-floor recipe,
  it becomes corner-selectable.

κ = ½ is FITTED. The footings 9.3603e-11 / 1.1312e-10 m/s² are scored separately and never pooled. Verdicts use raw data and
framework-native inputs only: CFG42's Moster / Dutton–Macciò inputs appear only in K1. The extra mass is cold energy, not a
particle. Not "theory closed". Nothing here says the data favour the framework.

| | |
|---|---|
| Kind | HYPOTHESIS TEST: one new supply rule, zero fitted constants (μ, τ, C are declared brackets) |
| Block | CFG930–939 (this lane = CFG934) |
| Criteria | `FROZEN_CRITERIA.md`, **9782c3df7**, committed alone before any script or number |
| Results | **e8bb2ae70**: `cfg934.py`, all outputs (K, MUTATE_T100, MUTATE_T001, main) and the post-hoc diagnostic part 1. Part 2 of `cfg934_posthoc.py` (where f_ex switches off; POST-HOC, 2026-10-20, no class weight) was committed with this README. `cfg934.py` did not change after e8bb2ae70. |
| Run | `CFG934_MODE=K|MUTATE_T100|MUTATE_T001|main OMP_NUM_THREADS=1 nice -n 10 python3 cfg934.py` (each mode about 5 s, peak 142 MB) |
| Not blind | H-CF was formed after CFG42, CFG45, CFG65, CFG827, CFG877, CFG878, CFG880, CFG921, CFG930, CFG932 and CFG933. Criteria §0 discloses expectations E1–E3. **E2 was confirmed**, with the switch lower than E2 guessed (M_b ~1e5 rather than ~1e6): f_ex = 0 for the brighter dwarfs, so (S) cannot close LVD-83. |

## Hypothesis and posits

**H-CF.** Before any bound system exists, cold energy is ordinary cold collisionless matter (CFG649/CFG654), so it collapses into
primordial halos. A system forms stars only if its halo reached T_vir ≈ 1e4 K at its formation epoch z_f. H-CF assigns each dwarf
exactly that floor halo, the minimal parameter-free assignment, as its collapse debris. It is combined with the law by CFG45's
readings: (S) sum, the primary, and (M) max, the alternative.

| posit | status | value / source |
|---|---|---|
| **cooling-floor supply rule: collapse mass = M_cool(z_f)** | **NEW (the only new rule)** | this lane |
| T_vir = 1e4 K; T_vir = μ m_p V_c²/(2k), V_c² = GM/r_vir | input (atomic physics; BL01 eq. 26 convention) | fixed |
| μ | input, bracket | 0.59 ionised / 1.22 neutral |
| z_f | input (data), bracket | Weisz+14 τ50 / τ90 (CFG824's rule). Missing SFH: Weisz median of the same host group × luminosity class |
| Δ_vir(z_f) | framework-native | 8 Δ_ta(z_ta) [(1+z_ta)/(1+z_f)]³ from CFG654's N0 table (Δ_vir 303.9 at z = 0, 177.5 at z = 9) |
| profile: NFW, ρ_s = C ρ̄_m(z_f), truncated at r_vir | declared generic collapse physics (as CFG930), bracket | C 1500 / 3000 / 6000, giving c ≈ 2.3 / 3.3 / 4.5 at z ≥ 2 |
| background h, Ω_m, Ω_r, f_b | framework-native | CFG654 A1 CMB set: 0.6777, 0.3104, 9.1e-5, 0.1568 |
| f_ex, CFG35 edge, readings (S) / (M), estimators | inherited, unchanged | CFG35 / CFG42 / CFG45 / CFG874 / CFG880 |

### The floor masses used (`cfg934.out`; V_vir = 16.73 / 11.63 km/s for μ 0.59 / 1.22 at every epoch)

| z_f | 0 | 1 | 2 | 3 | 5 | 7 | 9 |
|---|---|---|---|---|---|---|---|
| M_cool, μ 0.59 [M☉] | 2.34e9 | 1.03e9 | 5.79e8 | 3.80e8 | 2.08e8 | 1.35e8 | 9.67e7 |
| M_cool, μ 1.22 [M☉] | 7.86e8 | 3.46e8 | 1.95e8 | 1.28e8 | 6.99e7 | 4.54e7 | 3.25e7 |
| r_vir, μ 0.59 [kpc] | 35.9 | 15.8 | 8.9 | 5.8 | 3.2 | 2.1 | 1.5 |

Formation epochs by class (median z; τ50 / τ90):
- U: 4.59 / 1.61 (only 3 of 31 have their own SFH);
- C: 1.70 / 0.34;
- M31 LVD: 1.70 / 0.34;
- I: 2.03 / 0.26;
- L: 3.42 / 1.09 (29 of 83 have their own SFH).

The Weisz grid caps τ at 12.59 Gyr, so z_f ≤ 4.96. The satellite-faint default is τ50 12.47 / τ90 9.76 Gyr (N 6).

Two results on the UFD floor:
- For μ 0.59 at z_f ≈ 4.6, the floor mass is about 2.3e8 M☉. That is close to the ~3e8 where CFG42's Moster + Dutton–Macciò
  offset crossed zero. This is a coincidence of scale, not evidence.
- **SPARC uses z_f = 0**, the largest floor (2.3e9 M☉). Even there f_ex = 0 in all 110 galaxies.

## Results (`cfg934.out`, `cfg934_results.json`)

Statistics, as in each source lane:
- U, C, M: dex in σ, with CFG42's error (bootstrap or 1.2533 rms/√n, ⊕ the Υ_V 1–4 floor; no collapse-mass floor, since H-CF has
  no free collapse mass);
- I: dex in g (CFG874's mean D, bootstrap replay);
- L: ln σ (CFG880's estimator, CFG919's se);
- S: the fraction of 110 SPARC dwarfs raised by less than 0.03 dex.

Classes: |z| < 2 CONSISTENT; 2–3 TENSION; ≥ 3 CONTRADICTED.

### Reading (S), primary: range over the 12 corners (μ × τ × C)

| class | canonical: bare → H-CF (z range) | labels C/T/X of 12 | alt: bare → H-CF (z range) | labels C/T/X |
|---|---|---|---|---|
| **U** MW ultra-faints (31 + 9 limits) | +0.325 (+3.77) → −0.066 … +0.239 (−1.38 … +5.09) | 5 / 2 / 5 | +0.304 (+3.55) → −0.052 … +0.227 (−1.01 … +6.20) | 4 / 3 / 5 |
| **C** MW classicals (14) | +0.027 → +0.027 (+0.32 … +0.34) | 12 / 0 / 0 | +0.007 → +0.007 | 12 / 0 / 0 |
| **M** M31 dSphs (Collins+13 / LVD, the worse) | +0.064 → +0.064 (+0.78 … +0.83) | 12 / 0 / 0 | +0.045 → +0.045 | 12 / 0 / 0 |
| **I** isolated LG dwarfs (11) | +0.194 (+2.53) → +0.142 … +0.194 (+2.22 … +2.53) | 0 / 12 / 0 | +0.155 (+2.03) → +0.112 … +0.155 (+1.73 … +2.03) | 3 / 9 / 0 |
| **S** SPARC gas-rich dwarfs (110) | 1.00 → 1.00 (f_ex = 0 in all 110) | 12 / 0 / 0 | 1.00 → 1.00 | 12 / 0 / 0 |
| **L** LVD-83 | +0.518 (+8.86) → +0.121 … +0.403 (+2.38 … +7.93) | 0 / 1 / 11 | +0.472 (+8.10) → +0.110 … +0.369 (+2.20 … +7.22) | 0 / 1 / 11 |

**Verdict (S): PARTIAL on both footings, not corner-selectable.**
- No corner has all six classes CONSISTENT on either footing.
- U on the canonical footing is CONSISTENT at μ 0.59 / τ50 (all three C values), at μ 0.59 / τ90 / C 6000 and at
  μ 1.22 / τ50 / C 6000. The alt footing is the same except that μ 1.22 / τ50 / C 6000 is TENSION (+2.17). U is CONTRADICTED
  at every μ 1.22 / τ90 corner on both footings.
- The best corner is μ 0.59, τ50, C 6000:
  - canonical: U −0.066 (−1.38), C +0.027, M +0.064, I +0.194 (+2.53, TENSION), S 1.00, L +0.121 (+2.38, TENSION);
  - alt: U −0.052, I +0.155 (+2.03, TENSION), L +0.110 (+2.20, TENSION).
- f_ex > 0:
  - in 25–31 of the 31 ultra-faints (median 0.43–0.94);
  - in 0 of 11 isolated dwarfs at τ50 (5 at μ 0.59 τ90);
  - in 0–3 of 14 MW classicals;
  - in 25–55 of the LVD-83.

### Why LVD-83 stays high under (S) (POST-HOC diagnostic, `cfg934_posthoc.out`, added after the main run; no class weight)

Bare-law LVD-83 excess by luminosity, canonical:
- M_V ≤ −10: +0.01 ln (N 17);
- −10 < M_V ≤ −7.7: +0.36 (N 28);
- M_V > −7.7: +0.86 (N 38).

At the best corner (μ 0.59, τ50, C 6000), canonical:
- **M_V > −7.7:** the floor acts in 34 of 38 and brings them to **+0.02**.
- **−10 < M_V ≤ −7.7:** it acts in only 6 of 28, and the residual stays **+0.33**. The largest intermediate residuals are
  And IX (+0.93), And V (+0.73) and Draco (+0.73), all with f_ex = 0. And XXVII (+1.17) and Cas II (+1.01) sit at the bin edge
  with small f_ex (0.27, 0.34).
- **M_V ≤ −10:** untouched, and already on the law.

The alt footing is the same: faint +0.03; intermediate +0.30 with 3 of 28 acted on.

**Where f_ex switches off** (part 2 of the same post-hoc diagnostic). Edge phantom vs cold floor (1 − f_b) M_cool at μ 0.59,
τ50, C 6000, canonical:

| dwarf | edge phantom | cold floor | f_ex |
|---|---|---|---|
| Segue 1 | 4.4e6 | 1.95e8 | 0.98 |
| Boötes I | 1.1e8 | 1.95e8 | 0.41 |
| Eridanus II (M_V −7.1, already off) | 2.4e8 | 1.95e8 | 0 |
| And IX | 6.9e8 | 5.7e8 | 0 |
| Draco | 8.2e8 | 3.4e8 | 0 |
| And V | 1.1e9 | 4.4e8 | 0 |

Across the 83, f_ex = 0 from M_b 8.7e4 (μ 0.59) or 2.0–3.6e4 M☉ (μ 1.22). The only exceptions are late-forming dwarfs with a
larger floor: f_ex > 0 up to M_b 1e6.

The floor closes the faint end. The intermediate dSphs carry an excess of about ×1.4 in σ that the sum reading cannot reach,
because their law phantom inside the edge exceeds the floor's cold mass.

### Reading (M), alternative: PARTIAL (corner-selectable)

At μ 0.59, τ50, C 6000 all six classes are CONSISTENT on both footings:
- canonical: U −0.081 (−1.55), C −0.058, M +0.050, I +0.097 (+1.54), S 1.00, L −0.008 (−0.16);
- alt: U −0.081, C −0.066, M +0.040, I +0.079 (+1.27), S 1.00, L −0.019 (−0.36).

This is the only such corner. At C 3000 the canonical I is TENSION (+2.33). Every τ90 and every μ 1.22 / C ≤ 3000 corner leaves
U or L CONTRADICTED.

Under (M) the floor halo acts on the intermediate dSphs, because the max needs no leftover. But it acts enough only at the
heaviest, earliest and densest corner of the declared bracket. Picking that corner is a discrete fit, not a survival.

### Variants (reading S; criteria §4)

| variant | verdict | note |
|---|---|---|
| V1 Δ_vir = 18π² | PARTIAL | identical label counts |
| V2 onset z_coll (13.3 Gyr) | PARTIAL | denser halos: L CONSISTENT at 5 / 6 corners, but U is over-predicted, CONTRADICTED at 7 / 6 corners (L too at μ 0.59 τ90) |
| **V3 Υ_V 1 (I, L)** | **FAILS** | I CONTRADICTED 12/12, L 11/12 + TENSION 1 |
| **V3 Υ_V 4 (I, L)** | **PARTIAL (corner-selectable)** | I CONSISTENT 12/12; L CONSISTENT 1 / 3 corners |
| **V4 CFG930 uniform recipe (Υ ×½–×2 floor on I, L)** | **PARTIAL (corner-selectable)** | the Υ floor dilutes the L test (L TENSION 8/12) |
| V5 Υ_SFH (CFG827) for I, L | PARTIAL | |
| V6 luminosity-class τ default | PARTIAL | |

**FRAGILE: yes.** The verdict moves between FAILS and corner-selectable with the stellar M/L of the I and L classes. It does not
move with Δ_vir, z_coll or the τ default.

## Controls

| control | result |
|---|---|
| K1 | CFG42 H1/H2/H4 reproduced **through this lane's generic estimator** with CFG42's own inputs: 60 UF/CL numbers, max \|d\| 0; H4 n 110, nfex 0, frac 1.000 |
| K1b | CFG45's (M) reading: 16 numbers, max \|d\| 1.8e-15; SPARC dwarf\|M frac 0.9182, max 0.0596 (exact) |
| K2 | M_cool vs BL01 eq. 26 (z 9, 18π², μ 0.6, 1.98e4 K): 2.627e8 vs 2.649e8 M☉ (0.8%; BL01's coefficient is rounded). V_c identity 1.6e-15; NFW vs quadrature 1.2e-14; c solve 2e-15 |
| K3 | CFG827: 36 E_SFH rows exact; OOS weighted flat mean +0.324643 exact; OOS unweighted mean **+0.3747 (25/28 above the law)**, i.e. the record's dwarf excess; τ50/τ90 = CFG824's (36/36, exact) |
| K4 | CFG874 isolated E +0.1944 ± 0.0767 / +0.1553 ± 0.0765, exact replay |
| K5 | CFG880 sample N 83, host counts as declared; σ_law² equals CFG880's law2 (4e-16) |
| K6 | Δ_ta nodes exact; Δ_vir(30)/18π² − 1 = −0.0055; t0 13.7723 Gyr (table = quadrature) |
| MUTATE T001 (T_vir × 0.01) | **PASS:** every class equals the bare law exactly (max \|d\| 0; reading M 1e-16) |
| MUTATE T100 (T_vir × 100) | **FAILED as frozen in 7 cells.** Every statistic is negative (over-predicted) at every corner, but Collins+13 at six τ90 C ≤ 3000 corners (z −1.0 … −1.6) and the MW classicals at one (−1.91) do not reach z ≤ −2. Their errors (Υ floor ⊕ rms) are large. U, I and L bite at −2.6 … −19σ. Kept as a FAIL. **Flag:** at those corners the M class has limited power to detect over-prediction. This does not bear on the (S) verdict, which is set by L, U and I. |

**Fixes before any H-CF number** (disclosed): two crashes stopped the first two K launches.
- The CFG654 table key is lower-case `z`: a KeyError at load, before any number.
- scipy's brentq refused rtol 4e-16 (minimum 8.9e-16), so rtol became 1e-15. This happened after K1/K1b had printed their
  reproduction numbers and before any H-CF number.

No criterion changed.

## Ungraded reports (criteria §6)

- **Clusters.** f_ex = 0 (edge phantom 2e14–1e15 vs cold floor 7e8–2e9 M☉). Under (M) the floor inside 0.5 Mpc (≤ 2e9) is
  far below the phantom (4–9e13). H-CF does nothing for clusters: a separate problem, as expected.
- **Tidal dwarfs and NGC 1052-DF2/DF4** (formed without a primordial halo). H-CF gives them no debris, so σ_pred = σ_law exactly.
  - Observed: DF2/DF4 at E −1.71 / −2.17 ln canonical (CFG933); Lelli+15 TDGs 0.69 dex below the bare law (CFG931 INFO).
  - H-CF's qualitative expectation, **no excess**, matches the sign. The deficits are not explained, and they belong to the law
    side (environment / EFE).
  - Even with a floor halo at any z_f 0–5 they would get E_pred = 0 under both readings: f_ex = 0, and the floor sits below
    their phantom at r12.
- **Coma UDGs** (CFG933's 9). H-CF predicts **zero excess** under both readings at every z_f 0–5, both μ, C 3000: f_ex = 0 in 9/9,
  and the floor sits below the phantom. The observed values are ⟨E⟩ +0.760 / +0.669 ln. **The UDG excess is not a cooling-floor
  effect** under H-CF as frozen.
- **CFG880's scatter.** LVD-83 intrinsic scatter of ln(σ_obs/σ_pred), by ML with the same estimator:
  - bare law 0.462 (95% 0.388–0.557);
  - H-CF (S) 0.33–0.38, (M) 0.34–0.45;
  - CFG877's universal clump 0.271.

  The floor puts its mass in the right dwarfs: Spearman ρ(predicted boost, observed excess) is +0.56 … +0.63 under (S). But it
  removes less of the scatter than one universal clump. The variation of M_cool with z_f does not reproduce CFG880's s_int: a
  large part of the scatter is the intermediate dSphs that the floor does not reach.
- **The common scale.** By construction every floor halo has the same V_vir (16.7 / 11.6 km/s) and V_max ≈ 1.0–1.05 V_vir, at
  every epoch. Its cold mass inside 300 pc over the 83 is:
  - median 4.4e6 (16–84%: 2.3–5.9e6) at μ 0.59 / τ50 / C 1500;
  - median 1.1e6 (0.6–1.5e6) at μ 1.22 / τ90 / C 1500.

  That is a luminosity-independent inner scale with about 0.1–0.2 dex half-width. The literature's "common mass" value was not
  compared: it is not on disk.
- The floor velocity (11.6 km/s neutral, σ ≈ 8.2 km/s) is the CFG878 H-cooling number; under H-CF it is a V_vir, not a clump σ.

## What is and is not established

**Established (conditional on the declared brackets and the inherited estimators):**
1. A framework-native, parameter-free floor halo can carry the MW ultra-faints onto the law under the sum reading, at the ionised
   τ50 corners. It does so without touching the classicals, the M31 dSphs or SPARC. The classical over-prediction that CFG42's
   Moster masses produced does not occur, because the floor masses are 10–100× smaller.
2. Under (S) the floor cannot supply the intermediate-luminosity dSph excess (−10 < M_V ≤ −7.7, about +0.3 ln): f_ex = 0 there.
   The LVD-83 class is therefore CONTRADICTED at 11/12 corners on both footings.
3. H-CF predicts zero excess for Coma UDGs, DF2/DF4, TDGs and clusters.

**Not established:**
- That H-CF survives. (S) is PARTIAL and FRAGILE; (M) needs one corner choice.
- That the floor is the dwarfs' actual halo mass. It is a lower bound: a heavier halo would need an assembly history, i.e. a
  parameter.
- That the corner where (M) works (μ 0.59, τ50, C 6000) is physically preferred. Neutral gas at the 1e4 K threshold argues for
  μ 1.22, and at μ 1.22 neither reading works.
- Anything about the UFD z_f beyond the Weisz group default: 28 of 31 ultra-faints have no own SFH, and the grid caps τ.
- Tides, the external field and binaries (not modelled, as in CFG42). The inherited CFG35 edge uses CFG7's flat-Λ turnaround
  convention. The NFW shape and the ρ_s = C ρ̄_m(z_coll) convention come from collisionless-collapse simulations (declared as
  generic collapse physics, as in CFG930).

**For the record.** The floor is a natural, zero-constant answer for the faintest dwarfs. It is not the answer for the
intermediate dSphs or for UDGs, which carry similar excesses. Something other than a primordial cooling floor, or a reading
other than CFG35's leftover sum, is needed there.

κ = ½ FITTED; footings never pooled; cold energy, not a particle; not theory closed.
