# E3_dwarf_excess — CRISP FINDING (Part A: the excess survives clean choices; Part B: UNDECIDABLE on a ΛCDM-processed input, and no binding mechanism in the record)

**Verdict.**
1. **Part A — A-SURVIVES, both footings.** The sub-threshold satellites' "+2.15 dex above Newton" is +2.01 ± 0.12 dex with
   statistical binary corrections. In the worst clean combination (Υ_V = 4, binary fraction 0.7, lower of LVD/DEIMOS σ)
   it is +1.64 ± 0.12 dex. That is 76% of the raw value; W − 2σ = +1.40 (alt +1.39) ≥ 1.0.
2. **The +2.15 dex is the wrong yardstick for the screened theory.** At L* = 24 pc, the CFG820/CFG691 screening still gives
   the 45 systems a median boost B_scr = 10^1.23 ≈ 17× over Newton. The reason is that S multiplies ν − 1 ≈ 10–100. The data
   sit **+0.89 ± 0.13 dex** above the screened prediction (alt +0.85). The cold mass to be supplied is set by that +0.89, not
   by +2.15. At L* = 90 pc the gap is +1.52 dex. Compact UFDs are near Newton (Segue 1, Willman 1, Carina III: B ≈ 2.7);
   extended ones are not (Tucana II 62×, Crater II 90×).
3. **Part B — UNDECIDABLE (the catchment baryon mass / f_ret is not native), both footings, and NO MECHANISM IN THE RECORD.**
   - Extra bound cold needed inside r12 (record Class-A accounting): median 4.9e5 M☉.
   - At the census f_ret = 0.10, the median system must hold **q = 0.81** of its whole catchment's cold energy inside r12
     (16%: 0.61; alt 0.77). 6/45 exceed the whole supply at 2σ: Segue 1, Tucana II, Tucana IV, Eridanus IV, UMa I, UMa II.
   - Census-free (f_ret = 1, present baryons only): q = **8.0**, a shortfall of **+0.90 dex** (alt 7.7).
   - The supply suffices only through the ΛCDM-processed census. It also needs a binding mechanism, and the record has none.
   - Worst-clean data: q = 0.29 (census) and 2.9 (census-free).

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold energy, no particle. Not "theory closed". Nothing here
says the data favour the framework.

## Files
- `FROZEN_CRITERIA.md`: committed alone first (5686635887).
- Script `e3_dwarf_excess.py` → `e3_dwarf_excess.out`, `e3_dwarf_excess_results.json`, `e3_per_system.csv`,
  `e3_inputs_ledger.csv`.
- `--mutate` → `*_MUTATE.*`.
- **6/6 checks PASS.** The run takes about 2 s on one thread.

## Part A — what the +2.15 dex is made of (input ledger: `e3_inputs_ledger.csv`)
| ingredient | source | class | effect on the median (canonical) |
|---|---|---|---|
| σ_los | LVD compilation | RAW (mostly single-epoch) | — |
| binaries, statistical | Arroyo-Polonio 2026 (8 of the 45 matched; the rest get the median ratio) | SURVEY-CALIBRATION (population model) | free-f −0.15; f = 0.7 −0.22 dex |
| binaries, multi-epoch | Geha 2026 II DEIMOS (15 matched), CFG51 Walker | RAW | DEIMOS σ +0.02 vs clean |
| R_e (circularised) | LVD | RAW × distance | in the MC |
| distance | LVD distance modulus | SURVEY-CALIBRATION | ratio ∝ 1/D; in the MC |
| M* (Υ_V = 2) | LVD | SURVEY-CALIBRATION (SPS M/L) | Υ 1 / 4: +0.30 / −0.30 dex |
| Wolf 3σ²r12/G | A26 eq. 3 | MODEL ASSUMPTION (equilibrium, sphericity; anisotropy-insensitive at r12) | factor 1 instead of 3: −0.47 (not clean) |
| equilibrium / tides | none measured per UFD; CFG838: no present-day tidal signal | MODEL ASSUMPTION | bounded below |
| EFE (+1.25 dex reading) | D2 `efe_delta`: 1-D QUMOND ν(y_i + y_e) with K term | **STANDARD-MOND-MACHINERY** + external host masses | not used in the +2.15 or in Part B |
| M_crit sample cut | a0 L*²/G, L* = 24 pc (CFG820) | FRAMEWORK-NATIVE (L* a fitted bound; a0 via κ = ½ FITTED) | alt cut gives 46 systems, same class |
| 5.364, f_ret = 0.10 | Planck Ω_c/Ω_b (CFG886); CFG416/556 census | **ΛCDM-PROCESSED** | Part B only: q ∝ 1/5.364, q ∝ f_ret |

**Clean recompute** (bootstrap × per-system MC, 4000 draws; `results.json` → `A`):

| | canonical | alt |
|---|---|---|
| raw A26 (MC) | +2.16 ± 0.12 | +2.15 ± 0.11 |
| clean primary (Arroyo free-f) | +2.01 ± 0.12 | +2.00 ± 0.11 |
| Υ_V 4 | +1.72 | +1.70 |
| f = 0.7 binaries | +1.95 | +1.93 |
| worst-clean W | **+1.64 ± 0.12** | **+1.63 ± 0.12** |
| clean, above the unscreened isolated law | +0.56 ± 0.10 | +0.51 ± 0.10 |
| clean, above the screened prediction (L* = 24 / 90 pc) | **+0.89 ± 0.13 / +1.52 ± 0.14** | +0.85 / +1.49 |

**Non-equilibrium (not correctable from disk).**
- To reach the screened prediction at L* = 24 pc, each system's σ would need a median inflation of 2.97× (range 0.5–16).
- The largest dataset-to-dataset σ change on disk is 3.12×: Boötes III, LVD 1.69 vs DEIMOS 5.27 km/s, a disrupting system.
  24/45 systems need no more than that.
- So non-equilibrium cannot be excluded system by system. It would have to act in most of the sample at once.
- Informational: 14% of the satellites have r12 beyond their baryon-only Newtonian Jacobi radius.

## Part B — the framework's native capacity
- **Required:** M_c,req = M_dyn − (M*/2)·B_scr. The B_scr term holds the tethered, screened phantom. Extra cold energy gets
  Newtonian self-gravity (CFG888 Class A).
- **Ceiling:** C = 5.364 M_b / f_ret, the whole catchment's cold supply, with no placement assumed. This is CFG823's form, and
  K5 reproduces CFG823's Draco q = 0.496.
- **Per-system L_req** = M_c,req / (5.364 M*) is the catchment-to-present baryon ratio needed for q = 1. Its median is
  8.3 (canonical), against the census's 10.

| case (canonical) | median q | 16% | q > 1 at 2σ | read |
|---|---|---|---|---|
| L* 24, f_ret 0.10 (primary) | 0.81 | 0.61 | 6/45 | 81% of the whole catchment inside r12 |
| L* 24, f_ret 1 (census-free) | 7.97 | 6.05 | 21/45 | shortfall +0.90 dex |
| L* 90, f_ret 0.10 | 0.93 | 0.73 | 6/45 | |
| Newton, f_ret 0.10 | 0.96 | 0.76 | 8/45 | |
| self-boost variant (H-LINK, not in record) | 0.06 | 0.04 | 0 | needs CFG722's rejected coupling |
| worst-clean, f_ret 0.10 / 1 | 0.29 / 2.87 | 0.20 / 2.00 | 0 / 14 | |

Alt footing: 0.77 / 7.69 / 0.88 / 0.93 / — / 0.27 / 2.70, the same class.

**Mechanism inventory (restated from the record, not re-tested):**
- CFG822: free cold energy from expelled gas lands too far out.
- CFG842: host capture supplies 1e-8 to 1e-5 of the need.
- CFG888: extra cold energy gets no law self-boost, and has no self-gravity at all in the S3 action.
- CFG889: the gate does not retain a clump once orbits are included.
- CFG959: native debris sits below the law on dSphs.

There is no "mechanism X". The outcome is therefore not "bound cold mass can supply it". The ceiling allows the median system
only if (a) the census f_ret holds and (b) some unmodelled mechanism packs about 80% of a catchment's cold energy inside r12.

## Record errors / wording found
- `campaign_fresh_gravity/CFG820_stiffness_from_globulars/README.md:18-19` says UFDs at L* = 24 pc are "largely screened and
  nearly Newtonian". S = 0.06–0.30 multiplies ν − 1 ≈ 10–100, so the screened boost is 2.7–100× (median 17×), not ≈ 1.
  The cold mass the screened theory needs is set by +0.89 dex, not +2.15.
- The brief's and D2 README Q3's "+2.15 dex above Newton" is the medium-first / L* → ∞ yardstick. It is not the screened
  theory's prediction.

## Checks and mutation
- K1: A26 reproduced (45, +2.147).
- K2: Wolf identity vs LVD, 0.009 dex.
- K3: screening limits.
- K4: Arroyo-Polonio ratios −0.068 / −0.104.
- K5: CFG823 Draco q.
- K6: the excess is seen.
- `--mutate` sets σ to the screened prediction: K1 FAILS (E_N 1.26), and Part B flips to CEILING ALLOWS.
- **Disclosed:** the criteria expected K6 to fail under mutate too. It does not, because the screened prediction itself sits
  1.26 dex above Newton. That threshold was built on the "nearly Newtonian" premise this lane corrects.

## What this does not show
- No per-UFD M/L. No multi-epoch σ beyond DEIMOS/Walker. Non-equilibrium is bounded, not measured.
- Leo T's gas is counted in its supply but not in g_bar (one system).
- The B_scr screening radius uses baryons only.
- f_ret has no native value. A framework rule for a satellite's catchment baryon mass would decide Part B, and none exists
  (CFG920: UNDERDETERMINED).
- Nothing was downloaded. Deciding Part B needs either a native catchment rule or isolated UFDs (Rubin/LSST).
