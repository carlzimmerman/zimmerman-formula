# CFG936: systems below the law (Lelli+15 tidal dwarfs, NGC 1052-DF2/DF4)

The lane has two parts:
- Part A scores CFG930's sealed S1.
- Part B asks whether the framework can put a system below its own law without an EFE.

## Bottom line

**S1 (CFG930's seal, "tidal dwarfs show zero excess"): NOT DIAGNOSTIC (BELOW THE LAW), ROBUST, on both footings.**
- The six Lelli+15 TDGs sit at mean Δ = **−0.690 ± 0.078 dex** (canonical) and **−0.728 ± 0.079** (alt). These are 8.8σ and
  9.2σ below the law.
- The seal's kill clause (mean excess > +2 se) is **not met**: there is no excess at all.
- The seal's premise, that the sample sits on the law, is not met either. H-ELS and the bare law both predict 0, so they
  share the deficit.
- The test had the power to see a uniform dwarf excess (+0.37 / +0.33 dex). The TDGs sit 13.5 se below that, so they reject
  the "uniform dwarf excess" reading that S1 was written to separate from H-ELS.

**The deficit question.** The framework can put these systems below its law without an EFE in only one way: give them **no
cold energy**.

| route | class T: 6 TDGs (canonical / alt) | class U: DF2 + DF4 (canonical / alt) | route overall |
|---|---|---|---|
| **(i) supply**: zero supply (S4 / FG001; CFG657 capture at α_P = 0) | **EXPLAINS** / **EXPLAINS** [FRAGILE] | **EXPLAINS** / **EXPLAINS** [FRAGILE] | **EXPLAINS**, both footings |
| **(ii) settling clock** (CFG763, EFE-free, τ = 3.47 Gyr) | **EXPLAINS** / **EXPLAINS** [FRAGILE: only at the slow end] | **FAILS** / **FAILS** [ROBUST] | **PARTIAL**, both footings |
| (iii) EFE: **declared contrast, not a framework route** | FAILS / FAILS [FRAGILE] | PARTIAL / FAILS [FRAGILE] | PARTIAL (canonical) / FAILS (alt) |

**Plain statement.**
- **The data fit the supply route.** The TDGs and DF2/DF4 do not contradict the "real assembled mass, no EFE" picture:
  - TDGs: +0.055 ± 0.114 dex against Newton, χ² 1.17/6.
  - DF2/DF4: +0.021 ± 0.539 ln, χ² 0.26/2.
- **The fit rests on a zero-supply label, not a derivation.** The prediction is binary: a system labelled debris gets
  exactly Newton, and one labelled primordial gets the full law. The label is not derived from anything the system shows.
- **The rule saw these objects first.** It was formed with them in view (CFG7/FG001, CFG441, CFG655/657), so this is a
  consistency check, not an out-of-sample confirmation.
- **No partial-filling route covers both classes.**
  - The clock reaches the young TDGs only at its slow end, and only if they are at the young end of their ages.
  - The clock fails for the old debris, which it fills to 91–95%.
- **An EFE does worse than zero supply.**
  - The TDGs would need host fields about 30× Lelli's estimates.
  - DF2 would need about 18×.
  - DF4 sits below even the Newtonian floor (E_obs −2.17 against −1.93 for Newton, a −0.3σ gap), so no EFE reaches it.

κ = ½ is FITTED. The footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled. Verdicts are framework-native; the framework's
own numbers are EFE-free. The extra mass is cold energy, not a particle. Not "theory closed". Nothing here says the data
favour the framework.

## Record of this lane

- **Kind:** score of a sealed statement (CFG930 S1, seal commit cbb3b9888, sha256 57b1141e…, verified in K0), plus a route
  test. Block 930–939. No new constant, nothing fitted.
- **Criteria:** `FROZEN_CRITERIA.md`, **71d010099**, committed alone before any script or number.
- **Amendment A1:** **f59ef9b22**, post hoc. It was written after the K-only run and before any test number, and committed
  alone.
  - K3's code carried an extra clause that was not in the frozen text: CFG4_common.A0 == the rounded footings.
  - CFG4_common holds FP0's unrounded a0, which sits a relative +2.7e-6 / +3.1e-6 above. CFG763 used those values, and K3
    reproduces them exactly (max diff 0).
  - The clause was dropped and the difference is reported. Nothing else changed.
- **Not blind** (criteria §1):
  - Seen before freezing: CFG931's TDG INFO (−0.690 / −0.728), CFG933's DF2/DF4 numbers, CFG763's bracket, CFG768's f_cap
    and Z, and CFG7's Newtonian χ².
  - Expectations X1–X5 were written down first. X1, X2, X4 and X5 came out as expected.
  - X3 (the clock for the TDGs, "borderline") came out as EXPLAINS at τ = 3.47, with a −1.6 / −1.8 σ under-prediction.

## Part A: S1

The estimator is the seal's own: CFG931's INFO path, one point at R_out, M_bar = 1.37 M_HI + M_mol + M_* (gas counted),
Δ = log10(g_obs/g_law), kernel ν_e. The error is se = sd/√6 combined in quadrature with a Υ floor (CFG930's uniform recipe:
M_* × 2 against × ½).

| footing | mean Δ (dex) | se (sd/√6 ⊕ Υ floor) | z | kill clause (> +2 se) | class |
|---|---|---|---|---|---|
| canonical | **−0.690** | 0.078 (0.075 ⊕ 0.023) | −8.8 | not met | **NOT DIAGNOSTIC (BELOW THE LAW)**, ROBUST |
| alt | **−0.728** | 0.079 (0.075 ⊕ 0.023) | −9.2 | not met | **NOT DIAGNOSTIC (BELOW THE LAW)**, ROBUST |

- **Per object (canonical):** NGC 5291N −0.40 ± 0.18, NGC 5291S −0.61 ± 0.15, NGC 5291SW −0.62 ± 0.22, NGC 7252E −0.87 ± 0.24,
  NGC 7252NW −0.89 ± 0.25, VCC 2062 −0.75 ± 0.38. The σ include the V, M_bar and R_out errors.
- **None of the declared alternatives or variants changes the class:**
  - the measurement-term se (0.104);
  - the median form (−0.687 ± 0.089);
  - the velocity-only σ;
  - ν_simple (the law as written, g_N = g²/(g + a0));
  - M_mol × 0 and × 2.
- **Reading.** S1's operational kill clause is not met, so the seal does not fail. Its premise (TDGs on the law) is
  violated, in the direction no excess-based reading predicts. That is a failure of the equilibrium, isolated law for these
  objects. H-ELS (already CONTRADICTED by CFG930) and the bare law share it, and S1 was not built to score it.

## Part B: can the framework put them below its law without an EFE?

**Classes and notation.**
- **Class T:** the six TDGs, residuals in dex of g.
- **Class U:** DF2 and DF4, with CFG933's sealed estimator (E in ln σ²).
- **r̄** is the mean residual against the route's prediction. Its se is the larger of the scatter and measurement terms.
- **χ²** is over n objects, with no parameter fitted.

**Class rule.**
- **EXPLAINS:** |r̄| < 2 se and p ≥ 0.05.
- **PARTIAL:** the route removes at least half of the law's deficit, or it EXPLAINS at a declared corner.
- **FAILS:** otherwise.

The law's own deficit is r̄_law = −0.690 / −0.728 dex for T and −1.940 / −2.028 ln for U.

### Route (i): supply (framework-native)

**Rule.** The cold mass inside the aperture is the smaller of the law's target and the captured free supply:
f = min(1, M_sup/((ν − 1) M_b)).

**Primary inputs.**
- **T:** THEORY_CANONICAL S4, "debris born moving through resting cold energy captures none". v2 did not remove it, and
  v2's catchment for a TDG lies inside its host's settled region, which is tethered to the host. So f = 0.
- **U:** CFG657's derived capture rule with α_P = 0 (CFG768 Part A), at CFG657's primary inputs. This gives
  f = 5.9e-4 (DF2) and 1.6e-3 (DF4) on canonical, and 4e-4 / 1.1e-3 on alt.

| | canonical | alt |
|---|---|---|
| T against zero supply (= Newton) | r̄ **+0.055 ± 0.114** dex, χ² 1.17/6 (p 0.98): **EXPLAINS** | the same (Newton is a0-free): **EXPLAINS** |
| T predicted Δ (Newton) / observed | −0.57 / −0.40, −0.72 / −0.61, −0.71 / −0.62, −0.81 / −0.87, −0.87 / −0.89, −0.79 / −0.75 | −0.60 / −0.44 … −0.83 / −0.79 |
| U against CFG657 at α_P = 0 | r̄ **+0.021 ± 0.539** ln, χ² 0.26/2 (p 0.88): **EXPLAINS**. DF2 E_pred −2.001 vs −1.709 ± 0.729 (z +0.40); DF4 −1.921 vs −2.170 ± 0.794 (z −0.31) | +0.023 ± 0.539, p 0.88: **EXPLAINS** |

**FRAGILE.**
- **T:** the recent-catchment upper bound (CFG657 channel F with every ambient element captured: host settled halo at D_p,
  Jacobi or exhaustion radius) gives f = 0.01 to 0.69 across 12 corners (0.015–0.687 canonical, 0.012–0.667 alt). Under the generous corners (R = D_p/2 with an
  unsettled reservoir k = 3) a TDG fills enough to fail:
  - 4 of 12 corners differ on canonical: 3 FAILS and 1 PARTIAL;
  - 3 of 12 differ on alt: 2 FAILS and 1 PARTIAL.
- **U:** 2 of 17 corners differ, on both footings:
  - V_coll 250 km/s → PARTIAL (DF4 falls back to full supply);
  - progenitor M_b,p 1e10 → FAILS (both galaxies fall back).

  These are the same fallback ends CFG768 flagged.

**Contrasts (no class weight).**
- (a) The own cosmic share kept (5.364 M_b; the 10-14 rule that v2 removed) fills f = 0.75–1.0. This gives
  r̄ −0.678 / −0.698 dex (T) and −1.823 / −1.823 ln (U), canonical / alt: it fails like the law.
- (b) The v2 catchment taken as if the system were a primordial, isolated galaxy (N = 1/f_ret = 10) gives f = 1, which is the
  law itself.

**What this means.** Only "captures none" works. Any rule that lets the debris keep or collect its cosmic share puts it back
on the law.

### Route (ii): settling clock (framework-native, EFE-free)

**Model.** f(t) = 1 − e^{−t/τ}, run at τ = 3.47 Gyr: the slowest clock old SPARC discs allow. CFG763's lower end was fitted to
these same TDGs with the 1-D EFE, so it is not an independent prediction for them.
- TDG ages: t_merg = 0.35–0.75 Gyr (Lelli).
- DF2/DF4 ages: vD+22, 8.28 / 10.68 Gyr.

**Results.**

| | canonical | alt |
|---|---|---|
| T at τ 3.47, nominal ages (f 0.10–0.19) | r̄ **−0.170 ± 0.106** dex (z −1.61), χ² 4.49/6 (p 0.61): **EXPLAINS**. Removes 75% of the law's deficit; under-predicts NGC 7252E/NW (z −1.45 / −1.27) | r̄ −0.189 ± 0.106 (z −1.79), p 0.52: **EXPLAINS** |
| T corners | ages −1σ: EXPLAINS (−0.093). Ages +1σ: **PARTIAL** (−0.228, z −2.18). τ_min 0.724: **FAILS** (−0.472, z −4.6) | the same pattern: −0.106, −0.250 (PARTIAL), −0.475 (FAILS) |
| U at τ 3.47 (f 0.91 / 0.95) | r̄ **−1.878 ± 0.480** ln (z −3.91), χ² 16.2/2 (p 3e-4): **FAILS**. DF2 z −3.00, DF4 z −2.68; removes 3% | −1.965 ± 0.480 (z −4.09): **FAILS** |
| U corners | ages −1σ, CFG768's 6 Gyr cap, τ_min: all FAILS (ROBUST) | all FAILS |

**D-ii: CFG763's own lower bound re-run EFE-free** (same 7 objects, recipe and grid). This is the key new number of this
route.
- The EFE-free law χ² rises to 146 / 169 (it was 34 / 40 with the 1-D EFE). Newton stays at 1.10.
- τ_min,95 moves from 0.72 / 0.83 Gyr to:
  - **2.04 / 2.29 Gyr** at −1σ ages, which is CFG763's rule. The window [τ_min, 3.47] is still **OPEN**;
  - **3.80 / 4.27 Gyr** at nominal ages. That lies above SPARC's 3.47 Gyr, so the window closes at nominal ages.
- ν_mono gives the same numbers. Note that CFG763's a0 is a relative 3e-6 off the rounded footings used here (A1).

**What this means.**
- **The clock is squeezed.** EFE-free it survives for the young TDGs only in a narrow band, τ ≈ 2.0–3.5 Gyr, and only if the
  TDG ages sit at their young ends.
- **It cannot be the common explanation.** For the ≥ 6 Gyr-old debris every allowed τ fills them to ≥ 82%, as CFG768 B
  already found.

### Route (iii): EFE (declared contrast, NOT a framework route)

**Setup.** FM12 eq. 60 (= Lelli+15 eq. 4) with ν_e, at the framework footings.
- TDG hosts: 0.6 L_K at D_p.
- DF2/DF4: the scalar sum of the NGC 1052 (1e11) and NGC 1035 (5e9) fields at projected distances. This is the most generous
  field, since projected distance ≤ 3D distance and the scalar sum ≥ the vector sum.

**Results.**

| | canonical | alt |
|---|---|---|
| T | r̄ −0.381 ± 0.110 dex (z −3.48), χ² 14.9/6 (p 0.02); removes 45% → **FAILS** (M_host × 2: PARTIAL) | −0.414 ± 0.109 (z −3.79); removes 43% → **FAILS** |
| U | r̄ −1.153 ± 0.480 ln (z −2.40), p 0.053; removes 41%; EXPLAINS only at NGC 1052 = 3e11 → **PARTIAL** | −1.232 ± 0.480 (z −2.57); best corner PARTIAL → **FAILS** |

**What an EFE explanation would need.**
- **TDGs:** a common host-mass factor of **29× / 36×** Lelli's 0.6 L_K. The estimated g_Ne/a0 is 0.018–0.061.
- **DF2:** g_Ne/a0 = **0.42**, against an estimate of 0.024 (×18). Its projected distance from NGC 1052 is 79 kpc.
- **DF4:** **unreachable.** Its E_obs (−2.17) lies below Newton (−1.93), and an EFE can only lower a system to Newton. Its
  projected distance from NGC 1035 is 21 kpc.

**What this means.** Even taken as a non-framework hypothesis, the EFE explains less than zero supply does. Within the
framework the EFE is excluded anyway (CL-AR; CFG925 R3).

## Plain statement (criteria §7)

1. **Can the framework put a system below its own law without an EFE?** Yes, in exactly one way. A system that has captured
   no cold energy obeys Newton. The record's rules give that for debris:
   - S4: "debris born moving through resting cold energy captures none";
   - FG001: "formed embedded → Newtonian";
   - CFG657's capture with α_P = 0, which yields f ~ 1e-3.

   That is where both classes sit: the TDGs at Newton + 0.055 ± 0.114 dex, and DF2/DF4 within 0.4σ of Newton.
2. **So the TDG and DF2/DF4 data do not contradict "real assembled mass, no EFE".** They fit it through the supply route.
3. **The fit has three conditions, stated so that it is not over-read.**
   - **Label-driven.** The prediction is law-or-Newton, decided by a formation label (debris or primordial), not by anything
     measured on the system. The fallback corners of CFG657 (V_coll 250, M_b,p 1e10) put the same galaxies back on the law.
   - **Not out-of-sample.** S4/FG001 and CFG655/657 were written with these TDGs and DF2/DF4 in view.
   - **In tension with "deficits fill in" (CFG747/748).** Old debris that stay Newtonian for 8–10 Gyr need capture to be
     shut off, not merely slow. CFG768's α_P = 0 provides that, conditional on one c_P. A clock that fills primordial and
     debris systems alike (route ii) is excluded by DF2/DF4.
4. **No partial-filling route covers both classes.** The clock explains the young TDGs only at its slow end, and fails for
   the old debris.
5. **What would decide it:** the sealed tests already on record.
   - An old TDG, NGC 5557-E1 (~4 Gyr). Sealed prediction: Newtonian, 16–24 km/s. The clock instead predicts ≥ 68% of the law.
   - CFG769's sealed trail galaxies (C-A6: σ_N for E-labelled debris).

   A clean ~10 km/s dispersion in an E-labelled trail dwarf, or law-level kinematics in an old TDG, would break the
   zero-supply reading.

## Controls

| control | result |
|---|---|
| K0 | CFG930's seal intact (sha256 57b1141e… = the committed file); S1 text found; CFG657 / CFG804 slices exec'd read-only without error |
| K1 | **CFG931's TDG INFO reproduced** to 1.1e-16 (means −0.6904 / −0.7276). The two Lelli CSVs agree on 42/42 shared values |
| K2 | **CFG933's DF2/DF4 reproduced** to 7e-15: E_obs −1.709 / −2.170; z vs P2 −3.22 / −2.79 canonical, −3.37 / −2.88 alt. The z vs the bare law, now stored, is −3.16 / −2.73 and −3.32 / −2.84 |
| K3 | **CFG763's clock bracket reproduced** exactly (max diff 0): τ_min,95 0.7244 / 1.2023 (canonical), 0.8318 / 1.3804 (alt); χ²(τ → 0) 34.018 / 40.290; χ²(τ → ∞) 1.105; upper bound 3.4744 → 3.47 (A1 above) |
| K4 | CFG768 reproduced (max diff 0): f_cap(α 0) primary/min/max; Part B f 0.8226 and Z −3.97 / −3.93 etc. |
| K5 | CFG7 C2 (Lelli Table 9 from eq. 4 at 1.25e-10) reproduced to 1e-10: max \|dV_ISO\| 1.0292, \|dV_EFE\| 1.4161 km/s |
| K6 | CFG804 census N(10.5) = 10 |
| K7 | limits exact to 1.1e-16 (f = 1 → law; f = 0 → −log10 ν; EFE with no host → law) |
| MUTATE onlaw (required) | TDGs planted on the law → mean −0.0000 ± 0.023 → **S1 HOLDS**, both footings: BEHAVES |
| MUTATE plus04 (tooth) | planted +0.4 dex → **S1 FAILS**, both: BEHAVES |
| MUTATE fullsupply (required) | route (i) with the full cosmic catchment (N = 10) → f = 1, \|Δ_pred\| = \|E_pred\| = 0: **no deficit**, BEHAVES |
| MUTATE oldclock (tooth) | all ages 13 Gyr → \|Δ_pred\| ≤ 0.009 dex, \|E_pred\| ≤ 0.021: BITES (an old system sits on the law) |

## Limitations

- **Non-equilibrium.** The TDG HI discs have turned less than one orbit (Lelli's caveat). Every route assumes equilibrium.
- **Small samples.** There are 6 TDGs and 2 DFs. The DF2/DF4 se is large (0.48–0.54 ln). With CFG933's R4 dispersions
  (DF2 10.8, DF4 8.0 km/s; reported, no class weight):
  - route (i): r̄ +0.50 ± 0.44 (p 0.52);
  - clock: −1.40 (p 0.002);
  - EFE: −0.67 ± 0.41 (p 0.21).
- **Simple estimators.** The TDG estimator is one point at R_out, with all baryons treated as a sphere, as CFG931 does. Host
  masses are Lelli's 0.6 L_K.
- **Channel F for the TDGs** is CFG657's form applied to TDG inputs. It is this lane's adaptation, used only as an upper
  bound with P_F = 1.
- **The primary supply rule is a postulate** (S4), not a derivation. f_ret and κ are inputs.
- **ν_simple** is a declared S1 variant (class unchanged). In Part B it is reported with no class weight, and no route's mean
  moves by more than 0.001 dex.

## Reproduce

All runs: one core, about 0.1 GB, under a second, nothing downloaded. Run order: K, the four MUTATE, then main.
- `CFG936_MODE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg936.py` → `cfg936_K.out`, `cfg936_results_K.json` (exit 0)
- `CFG936_MODE=MUTATE_onlaw …`, `MUTATE_plus04`, `MUTATE_fullsupply`, `MUTATE_oldclock` → `cfg936_MUTATE_<tag>.out`,
  `cfg936_results_MUTATE_<tag>.json` (exit 0 each)
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg936.py` → `cfg936.out`, `cfg936_results.json` (exit 0)

**Other lanes' files** were only read:
- CFG930, CFG931, CFG933, CFG763, CFG768, CFG7 and CFG804 JSON or text;
- CFG441's Arp 72c;
- CFG4_common, imported for ν_mono / A0;
- cfg657_capture.py and cfg804.py, exec'd read-only from their text with writes refused.

No other lane's file was edited.
