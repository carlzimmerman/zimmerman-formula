# NV1_nonlocal_variable: no single non-local variable on record resolves the residual rows. The basin mass E2 moves A12, A13 and A30 partway, but it breaks gate 3 (SPARC) and gate 5 (A1 rms) to get there

Criteria `FROZEN_CRITERIA.md` (ab1ec3ab46), committed alone. Amendments, each committed alone:
- `AMENDMENT_A1.md` (cf9242edf7): after step 1, before any control. It discloses two departures in step 1 that enter no label.
- `AMENDMENT_A2.md`: post-control, before any real fit. The control flag is recomputed as frozen; one extra reverse check was mine, failed by construction, and is reported but not gated.

Scripts:
- `nv1_env.py`: E1-E4 per system.
- `nv1_core.py`: L3+E arm on NP2's machinery (imported read-only), gates on rows with E, sign test.
- `nv1_cand.py`: RQ3 loader with E lookup.
- `nv1_stage3.py`: RQ3 unedited (U card) and the declared SUBSET card (S).
- `nv1.py`: modes `coverage`, `controls`, `real`.

Outputs are `nv1_<mode>.{json,out}`, `rules/`, `candidates/` and `results/` (RQ3 cards). Run with `PYTHONHASHSEED=0 nice -n 10 python3 -I nv1.py <mode>`, one thread. Physical footprint peaked at 0.62 GB; max RSS read 1.45 GB, which counts freed pages (NP2 A3).

**Not blind** (see the criteria). κ = ½ FITTED. The cold sector stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. A pass is a description of data, not a theory.

## Candidates and coverage (`nv1_coverage.out`)

| E | Definition (record source) | Train X-COP | Train SPARC rows | LT (RQ3) | Dwarfs | Lensing | IC 1613 | Fit-able |
|---|---|---|---|---|---|---|---|---|
| E1 | 2M++ + MCXC external field, gext_vectors_2026 | 0/4 | 1531/1531 | 8/20 | 0/89 | NOT COMPUTABLE | no | **no** |
| E2 | BS1 basin mass, CX1's E leaf formula | 4/4 | 1501/1531 | 11/20 | 89/89 | EM1 of total baryons | LG basin 12.39 | **yes** |
| E3 | host potential depth, X1 d_host, RQ3 host masses | 0/4 | 0 | 4/20 | 89/89 | NOT COMPUTABLE | yes | **no** |
| E4 | UNGC tidal index Θ1 | 0/4 | 548/1531 (28 galaxies) | 17/20 | 62/89 | NOT COMPUTABLE | 0.7 | **no** |

- E2 matches CX1's own E leaf on all 240 systems compared, with no mismatch.
- **On RQ3's unedited card,** E2 leaves the whole SPARC block (A1-A10) NOT COMPUTABLE, because two SPARC galaxies (DDO064 and UGC03546, BS1 `no_dist`) have no basin. A10 and A5-A7 are therefore graded only on the S card. The S card drops those 2 galaxies and 9 of the 20 LITTLE THINGS galaxies.
- Every NV1 card carries RQ3's [LABEL] tag, because E is looked up by name, sample and r500. This is inherent to a non-local leaf.
- **NEEDS DATA** (none downloaded):
  - E1 for KiDS lenses needs the lens positions (the KiDS-1000 bright isolated-lens catalogue of Brouwer+21) and a neighbour catalogue deeper than 2M++'s 200 Mpc (for example KiDS-bright). The sizes can't be checked from disk; an estimate is 0.1-1 GB each.
  - E1 for X-COP needs the same deeper catalogue (the clusters lie at 190-420 Mpc).
  - E1 inside the Local Group is not a download problem. It would need a new estimator built on UNGC sources plus the Milky Way, which was not built here.
  - E3 and E4 have no X-COP or lensing analogue on disk.

## Sign test at fixed local leaves (step 1; NP2 L3 F residuals; 50 nearest train rows in NP2's kernel metric)

| E | Train trend (ρ, p), canonical / alt | IC 1613 wants less: ΔE | UFDs want more: ΔE | Dw want more: ΔE | Lensing | Label |
|---|---|---|---|---|---|---|
| E1 | −0.25 (0.034) / −0.30 (0.011) | NOT COMPUTABLE | NOT COMPUTABLE | NOT COMPUTABLE | NOT COMPUTABLE | **NOT COMPUTABLE** |
| E2 | +0.01 (0.91) / −0.01 (0.92) | +1.96 | +1.64 | +1.64 | want 0 (+0.116 ± 0.063) | **DOES NOT SEPARATE** |
| E3 | no train system | | | | | **NOT COMPUTABLE** |
| E4 | +0.16 (0.40) / +0.14 (0.48) | +0.8 | +2.2 | +1.1 | NOT COMPUTABLE | **DOES NOT SEPARATE** |

- IC 1613 and the dwarfs sit on the **same side** of their local-leaf neighbours in E2 (the whole Local Group shares the basin 12.39) and in E4 (both are more tidally disturbed than their SPARC neighbours). Their wants are opposite, so no rule monotone in E can separate them.
- Neither E2 nor E4 has a train trend for a fit to learn from.
- Shuffles (1000): SEPARATES 0.4-0.6 %, PARTIAL or better 3-4 %.

## Controls, all frozen ones pass on both footings (`nv1_controls.out`; AMENDMENT_A2)

| Control | Result |
|---|---|
| Known answer | X-COP +0.4675, LT −0.0252 |
| Zero-weight E2 rule | U: 8 computed rows match RQ3's law card. S: 18 rows match the plain law on S. 0 mismatches |
| Checker | flags the bump (2677 violations); zero rule clean |
| Admissible plant | converged, clean, G3 SPARC 0.123 / 0.196, G4 −0.001 |
| Planted boost 0.15 z_E | true E recovers dm/dE 0.168 (planted 0.176) and passes gates 3-4. Shuffled E fails gates 1 and 3 (X-COP +0.30); SPARC-even rms 0.145 against 0.121 |

## Real fit, E2, L3+E, mode F (`nv1_real.out`)

| | Canonical | Alt |
|---|---|---|
| λ | **32, grid edge** | **32, grid edge** |
| ML length of E (standardised) | **0.02** | **0.02** |
| Checker | 0 violations | 0 violations |
| G1 X-COP train | −0.000 / 0.039 P | −0.000 / 0.037 P |
| G2 SPARC train | 0.133 / 0.176 P | 0.133 / 0.178 P |
| **G3 SPARC even** | **0.244 / 0.196 F** | **0.243 / 0.197 F** |
| G3 X-COP unseen | −0.016 / 0.093 P | −0.019 / 0.098 P |
| G4 LT (11 galaxies with E) | −0.087 P | −0.086 P |
| **G5 A1 rms (S card)** | **0.117 F** (NP2 0.054) | **0.115 F** (NP2 0.052) |
| E-shuffle MUTATE | G1 +0.189 F, G3 S 0.227 F, G3 X-COP +0.265 F, G4 +0.161 F | G3 S 0.228 F, G3 X-COP +0.082 F, G4 +0.241 F |

**Why the gates break.** E2 is nearly unique per system: for isolated galaxies it is EM1 of the galaxy's own baryon mass. With an ML length of 0.02 standardised units, the rule uses E as a galaxy label. It fits train galaxy by galaxy, then fails unseen SPARC galaxies. That is gate 3, gate 5's A1, and the grid-edge λ.

## Target rows, before (NP2 L3 F) → after (NV1 E2), Z; MUTATE in brackets

| Row | Card | Canonical | Alt |
|---|---|---|---|
| A10 IC 1613 | S | −4.30 → −3.76 [−3.70] FAIL | −4.23 → −3.73 [−3.21] FAIL |
| A12 dwarfs | U = S | **+6.38 → +4.45** [+8.29] FAIL | **+8.25 → +4.57** [+7.40] FAIL |
| A13 dwarfs (field) | U = S | +13.69 → +7.15 [+10.00] FAIL | +8.54 → +7.20 [+7.51] FAIL |
| A30 lensing | U = S | **+11.35 → +7.08** [+14.70] FAIL | **+10.21 → +8.16** [+69.8] FAIL |
| A5 | S | +3.58 → +4.53 (worse) FAIL | +3.82 → +4.50 (worse) FAIL |
| A6 | S | +5.16 → +6.52 (worse) FAIL | +5.44 → +6.48 (worse) FAIL |
| A7 | S | −2.17 → −2.00 FAIL | **−2.11 → −1.99 PASS** (marginal) |

- **Moves that pass the frozen PARTIAL rule** (|Z| falls by at least 1 and MUTATE doesn't reproduce half of it): A12 and A30 on both footings, and A7 on alt S.
- **A13's fall is reproduced by MUTATE,** so it doesn't count.
- A10 moves by 0.5 and still fails.
- **A5 and A6 get worse.**
- No target row passes except A7 on alt S, by 0.01.

## Verdict (frozen labels, per footing)
- **E2: PARTIAL** on both footings. A12 and A30 move partway, but the fit **breaks gate 3 (SPARC holdout) and gate 5 (A1 rms on S)**, so it is not a resolution. Its moves come with a rule that memorises galaxies.
- **E1, E3: NOT COMPUTABLE** (no X-COP train coverage; no target row, or no train system).
- **E4: NOT COMPUTABLE** for the fit. Its sign test reads DOES NOT SEPARATE.
- **Lane: NO SINGLE NON-LOCAL VARIABLE ON RECORD RESOLVES** on either footing. The PARTIAL movers are E2's A12 and A30, plus A7 on alt.
- The look-elsewhere control (E-shuffle MUTATE) bites: it fails gates 1/3/4 and worsens A12, A30, A7 on most cells.

## Departures, all disclosed
1. **AMENDMENT_A1:**
   - the look-elsewhere shuffles use 500 inner permutations;
   - E1 uses one σ;
   - the neighbour set is the union over a group's rows.
2. **AMENDMENT_A2:** an unfrozen reverse S-card check is reported, not gated. The as-run flag is stored as `ok_as_run`.
3. **The PARTIAL label in the code** checks moves and MUTATE, not gates, as frozen. The gate-3 and gate-5 failures are stated beside it above.
4. **Gate 4 runs on 11 of 20 LITTLE THINGS galaxies,** and gate 3 SPARC on 1621 of 1635 rows (the rows with E).
5. **Only E2 was fitted, in mode F, arm L3+E,** as frozen.
6. **RQ3 support files** (`old_gates.py`, `tolerances.json`, `row_marks.json`) are byte-identical copies. Caches and logs are gitignored.

κ = ½ FITTED. Not theory closed.
