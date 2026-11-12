# NOVERDICT.md — CLOSE-4: the repairs actually executed on gates that produced NO VERDICT

Ledger of work done, written after the runs. Criteria were committed alone before any script ran
(`FROZEN_CRITERIA.md`). Every number below is real output; the JSON and `.out` files are in `parts/`.

TEST lane. Relabels nothing, adopts nothing, is not registered. **kappa = 1/2 FITTED; not theory closed.**
Footings canonical (a0 = 9.3603e-11) and alt (1.1312e-10 m/s^2) are reported separately and **never pooled**.
Cold dark energy is a gravitating field component of the sector's own stress-energy — never a particle; dark mass IS
that sector's stress-energy. Stated as the claim, no LCDM hedging.

| # | gate | repair | executed? | does the frozen label move? |
|---|---|---|---|---|
| 1 | KL1 / KL1R MUTATE MA2 on DES Y3 (inherited by BX1) | R1: freeze KA2's selection sets | **YES — bites on both surveys, both footings** | KL1/KL1R: yes, and **not** to the A1 label. BX1: no (KA3, MB2) |
| 2 | DCN1 M3 numerical half (2.1 % against a 5 % line) | R2: detection test + the line on a u >= 1 testbed | **YES — bites on both footings, both clauses** | **No.** KA3/KA4/KA5 carry DCN1's NO VERDICT |
| 3 | SCS2 / SCS3 / EFN1 external-field family | R3: ONE rule, RULE-GC, on the ladders in the record | **YES — it decides, against convergence** | **No**, and it names the blocking quantity and backgrounds |

---

## 1. The DES Y3 covariance guard (KL1, KL1R; inherited by BX1) — REPAIRED

### The exact guard

- **KL1 `FROZEN_CRITERIA.md` (99a42c78ef) §3, KA2.** With `nfrac = diag(N)/diag(G)` (N the shape-noise term, G my
  Gaussian covariance at the fitted area): test (i) runs on points with `nfrac >= 0.8`, test (ii) on points with
  `nfrac < 0.5`. The escape: *"If (i) or (ii) has fewer than 5 points it reads NOT EVALUABLE."*
- **§5, MA2:** *"KA2 rerun with every n_i halved must FAIL (ii)."*
- **The bite, `kl1.py:202`:** `bites = bool(k["ii_pass"] is False)`, and `ka2()` sets `ii_pass = None` when
  `n_signal < 5` (`kl1.py:65`). `None is False` is false, so **NOT EVALUABLE is scored as "does not bite."**

### Why it cannot bite

`n_i` is the only thing MA2 changes and `nfrac` is the only thing that defines the (ii) point set. Halving every `n_i`
doubles `N^ij = s_i^2 / n_i`, so `nfrac` rises on every point and points migrate **out of** the (ii) set. The mutation
destroys the population it is meant to be measured on.

| | (ii) points, unmutated | (ii) points, n_i halved | `ii_pass` | bites |
|---|---|---|---|---|
| KiDS-1000 canonical / alt | 38 / 38 | 15 / 15 | False | yes |
| **DES Y3 canonical / alt** | **39 / 39** | **3 / 4** | **None (NOT EVALUABLE)** | **no** |

This is a selection artefact of the mutation. It is not a statement about the covariance.

### R1: what was done, and what it returned

`close4_ma2_fixed.py` → `parts/ma2_fixed.json` / `.out`. The (i) and (ii) index sets are computed **once** at KA2's own
configuration (`ng_scale = 1.0`) and then **held fixed**; the mutation changes the covariance only. The area is refitted
by the frozen rule on the fixed (i) set. The control is the same machinery at `ng_scale = 1.0` on the same fixed sets.

| footing | survey | control (ng x 1, fixed sets) | MUTATED (n_i halved, fixed sets) | bites |
|---|---|---|---|---|
| canonical | KiDS-1000 | (i) 0.883-1.135 → T; (ii) med 1.144, min 1.034 → T | (ii) med **2.070**, min 1.473 → F | **YES** |
| canonical | **DES Y3** | (i) 0.973-1.026 → T; (ii) med 1.230, min 1.084 → T | (ii) med **1.953**, min 1.482 → F | **YES** |
| alt | KiDS-1000 | (i) 0.883-1.136 → T; (ii) med 1.151, min 1.037 → T | (ii) med **2.075**, min 1.475 → F | **YES** |
| alt | **DES Y3** | (i) 0.973-1.026 → T; (ii) med 1.228, min 1.083 → T | (ii) med **1.952**, min 1.481 → F | **YES** |

The control reproduces KA2 on both surveys and both footings, so R1 is not a silent change of the test.
**MA2 now bites on DES Y3 on both footings.** The frozen re-selecting version is reported beside it in the same file.

### What the repaired guard does to the labels

Recomputed from KL1's own stored numbers with KL1's own label rule (`kl1_grade.py` lines 33-38), with `MA2_DES` set by
R1 and every other gate exactly as KL1 landed it:

**Part A (KiDS-1000 + DES Y3), both footings:**

| | KiDS-1000 | DES Y3 | overall |
|---|---|---|---|
| as landed (frozen) | TENSION | NO VERDICT (MA2) | NO VERDICT |
| **with R1** | **TENSION** (p 0.0381 / 0.0365, gap 3.95 / 4.06 w) | **CONSISTENT** (p 0.1593 / 0.1575, gap 2.83 / 3.02 w) | **TENSION** |

**Part B (KiDS-Legacy + DES Y3), both footings:**

| | KiDS-Legacy | DES Y3 | overall |
|---|---|---|---|
| as landed (frozen) | CONSISTENT (p 0.111 / 0.101, BALL) | NO VERDICT (MA2) | NO VERDICT |
| **with R1** | **CONSISTENT** | **CONSISTENT** (p 0.159 / 0.157) | **AMPLITUDE CONSISTENT WITH RAW LENSING** |

**Read this carefully — it is the substantive result of R1.** The repaired frozen gate does **not** reproduce KL1's
post hoc A1 headline in general. It reproduces it for Part B (Legacy + DES), and it **contradicts** it for Part A:
on KiDS-1000 the same repaired gate reads **TENSION**, not CONSISTENT. A1's headline
("AMPLITUDE CONSISTENT WITH RAW LENSING") was carried by the Legacy release; the older KiDS-1000 data still sit at
3.95 / 4.06 widths and p 0.038. Nothing in R1 changes that, and the ledger should not let the Part B label stand in
for the Part A one.

Caveats carried unchanged from the lanes: **MB2 does not bite** on Part B (0.46 / 0.47 widths against 0.5). KL1 reads
it as guarding no graded row; KL1R's strict reading would make the Part B label NO VERDICT. That disagreement is not
repaired here and is not touched by R1.

**BX1.** BX1's DES Y3 gate runs on KL1's covariance at the model, so R1 removes the inherited unguardedness there.
But **BX1's frozen label does not move**: its own rule (`FROZEN_CRITERIA.md` §9) reads NO VERDICT if any of KA1-KA5
fails or a MUTATE arm does not bite, and **KA3 fails (chi^2 44.8 / 70.9 / 177.9 on 15 bins at z 1 / 0.5 / 0; (b) x9 /
x6 / x4 against the line x5) and MB2 does not bite (ratios 1.8 / 1.5 / 1.2 against the line 1.5 at z 0)**. Both are
256^3 simulation gates, not the DES covariance. Repairing BX1's frozen label is a different job and is **not done
here** — recorded, not hidden.

**Status of R1: COMPLETE.** It is a post hoc amendment to KL1 and KL1R (the outcome was seen). It repairs a
bookkeeping defect in the mutation's point set, not the physics.

---

## 2. DCN1's M3 numerical half — REPAIRED

**The clause** (`FROZEN_CRITERIA.md` d603f1703c §5): *"drop the 1/(1+u) in A1: the sympy check must fail, and
Gamma_id^2 must disagree with route L on the KA4 sphere by more than 5 %."*
**Landed:** sympy BITES (cubics 1.6 relative); numerical half 2.13 % against the 5 % line → DOES NOT BITE.

**Why the line is unattainable.** The mutation replaces `u Phi_nn/(1+u)` by `u Phi_nn`. The change it can produce is
capped by `u_max/(1 + u_max)` over the analysis region. On the KA4 sphere the annulus has `u_max = 0.1006`
(canonical; 0.0912 alt), so the cap is 0.0914 of the `u Phi_nn` share of `Gamma_id^2`. The realised value, 2.13 %, is
that cap being attained. **The 5 % line demands more than the testbed's own `u` allows.** It is a mis-scaled line, not
a failing pipeline: the same run shows the *unmutated* identity agrees with route L to 0.036 %, so the mutation is
detected at 59x the pipeline's own error.

**R2 as run** (`close4_m3.py` → `parts/m3_repaired.json` / `.out`), on DCN1's own KA4 sphere, N_R = 108, canonical 9.4
thick disc's `rho_0` and `L`, DCN1's annulus `L/8 <= s <= L/2`, DCN1's finite-difference Hessians:

| footing | `sup_ann u` | `d0` identity vs route L | `d1` mutated vs route L | `dp` predicted | `d1/d0` (line 10) | `d1/dp` (band 0.5-2) | R2-a | frozen 5 % |
|---|---|---|---|---|---|---|---|---|
| canonical | 0.1006 | 0.00036 | 0.02130 | 0.02130 | **59.5** | 1.000 | **BITES** | not met |
| alt | 0.0912 | 0.00036 | 0.01920 | 0.01920 | **53.9** | 1.000 | **BITES** | not met |

**R2-b** (the frozen 5 % line, relocated to a testbed where it is attainable). `rho_0` scaled by the first factor in
the pre-registered ladder {1, 3, 10, 30, 100, 300} whose annulus reaches `sup u >= 1`:

| footing | factor | `sup_ann u` | `d0` | `d1` | frozen 5 % line |
|---|---|---|---|---|---|
| canonical | **x100** (x3 → 0.181, x10 → 0.353, x30 → 0.681) | 1.5241 | 0.00051 | **0.47806** | **MET — BITES** |
| alt | **x100** (x3 → 0.163, x10 → 0.317, x30 → 0.606) | 1.3329 | 0.00049 | **0.40567** | **MET — BITES** |

**M3 now bites on both footings, under both the replacement line and the frozen line.** `d1 = dp` to three digits: the
mutation produces exactly the change the algebra predicts, which is the strongest form the arm could take.

**DCN1's lane label does not move.** M3 guards the A1 identity's numerical use. The frozen NO VERDICT is carried by the
known answers — **KA3 fails** on the frozen test grid (9 of 12 converge, p = 0.75 cases' E > 20 %; it passes only on
A6's `h = 1/N_R`) and **KA4 fails** as frozen (null-cell value 0.78 of exact; it passes only under A3/A6). A6, the one
reading in which every known answer passes, is post hoc. Nothing in R2 touches KA3, KA4 or KA5. Recorded, not hidden.

**Status of R2: COMPLETE.**

---

## 3. SCS2 / SCS3 / EFN1 — ONE rule applied; it decides against convergence

**RULE-GC** is adopted verbatim from **SCS3's A4 rule** (b34295ebcd §3, flat clause removed) and **DCN1's §2**
(d603f1703c), which adopted the same rule and validated it in DCN1's KA3 (12 of 12 to 2.4e-15 on `h = 1/N_R`; `h^-1`
and `h^-0.5` Diverging; `1 + h^0.3` not Converged). CLOSE-4 adds **no clause to the arithmetic** — only the `n < 3`
case (NOT EVALUABLE) and the lane-level combination (SCS3's A4 requirement: every background in a family must
converge). `close4_gc.py` runs no solver; it reads stored JSON.

**SCS2's ladder.** As landed, SCS2's axial external-field family has two resolutions (R0 = 48x24, R1 = 72x36), and
RULE-GC returns **NOT EVALUABLE on all 32 backgrounds for both graded quantities** — that is the honest statement of
SCS2's situation, and it is why its two-grid 20 % clause could not decide anything.

**SCS3's AX backgrounds are SCS2's exactly** (SCS3 §1: same `scs2_aqual.py`, same solver, same inner treatment, same
Dirichlet rule). Before using SCS3's ladders for SCS2, CLOSE-4 checked all 32 twins against SCS2's stored
`scs2_resolution.json` fine/coarse values:

| SCS2's stored value | matches `scs3_maps_AX.json` (pre-A4) | matches `scs3_maps_AX_A4.json` (A4 rerun) |
|---|---|---|
| `min_dp_fine` / `min_dp_coarse` | **32 / 32** | **32 / 32** |
| `frac_fine` / `frac_coarse` | **32 / 32** | **0 / 32** |

SCS3's A4 rerun changed the negative **region**, not the background: on `alt_AX_expo_10.45_0.01` R1 the off-plane
negative cells go 70 → 110 and `Q_neg_offplane` -1.683e11 → -2.345e11, while `min_dp_offplane` is bit-identical. So
**SCS2's charge fraction is the pre-A4 number**, and SCS2 is graded on the pre-A4 ladder (R0-R3, four resolutions).
The minimum G is graded on both ladders; they agree in kind.

| quantity | CONVERGED | NOT CONVERGED | DIVERGING | family reading |
|---|---|---|---|---|
| SCS2 as landed, R0-R1: charge fraction | 0 | 0 | 0 (32 NOT EVALUABLE) | NOT EVALUABLE |
| SCS2 as landed, R0-R1: minimum G | 0 | 0 | 0 (32 NOT EVALUABLE) | NOT EVALUABLE |
| **SCS2 charge fraction, pre-A4 ladder R0-R3** | **21** | 11 | 0 | **NO VERDICT** |
| **SCS2 minimum G, pre-A4 ladder R0-R3** | **6** | 19 | **7** | **DIVERGING** |
| **SCS2 minimum G, A4 ladder R0-R6** | **5** | 20 | **7** | **DIVERGING** |
| SCS3 (A4 ladder): route L `Gamma_L^2` | 26 | 6 | 0 | NO VERDICT |
| SCS3 (A4 ladder): charge fraction | 28 | 4 | 0 | NO VERDICT |
| **SCS3 (A4 ladder): minimum D.P** | **5** | 20 | **7** | **DIVERGING** |
| **SCS3 (A4 ladder): inner radius in r_e** | **24** | 7 | **1** | **DIVERGING** |
| SCS3: route 2 `Gamma_2^2 = -lambda_min` (16 bgs, R0-R4) | 14 | 2 | 0 | NO VERDICT |
| **EFN1 route D: stop time `tF_efolds`** (12 bgs, R2-R4) | 0 | 10 | **2** | **DIVERGING** |
| EFN1 route W: c2 | 0 | 0 | 0 (12 NOT EVALUABLE) | NOT EVALUABLE (2 grids) |
| EFN1 route W: c3 | 0 | 0 | 0 (12 NOT EVALUABLE) | NOT EVALUABLE (2 grids) |

**Minimum-D.P DIVERGING backgrounds.** Pre-A4 ladder (7): `canonical_AX_expo_9.4_0.01`,
`canonical_AX_kuzmin_10.7_0.1`, `canonical_AX_kuzmin_9.4_0.01`, `canonical_AX_kuzmin_9.4_0.1`,
`alt_AX_expo_9.4_0.1`, `alt_AX_kuzmin_9.4_0.01`, `alt_AX_kuzmin_10.9_0.1`. A4 ladder (7):
`canonical_AX_expo_9.4_0.1`, `canonical_AX_kuzmin_10.7_0.1`, `alt_AX_expo_9.4_0.01`, `alt_AX_expo_9.4_0.1`,
`alt_AX_expo_10.45_0.01`, `alt_AX_kuzmin_10.7_0.1`, `alt_AX_kuzmin_10.9_0.1`. **Seven diverging backgrounds on both
ladders, overlapping but not identical sets.** The divergence is robust in kind; which background carries it depends
on the inner-boundary treatment.

**The 11 NOT CONVERGED charge-fraction backgrounds (SCS2, pre-A4 ladder):**
`canonical_AX_expo_10.45_0.01`, `canonical_AX_expo_10.45_0.1`, `canonical_AX_expo_10.7_0.01`,
`canonical_AX_expo_10.9_0.01`, `canonical_AX_expo_10.9_0.1`, `canonical_AX_expo_9.4_0.1`,
`alt_AX_expo_10.45_0.01`, `alt_AX_expo_10.7_0.01`, `alt_AX_expo_10.9_0.01`, `alt_AX_expo_9.4_0.01`,
`alt_AX_expo_9.4_0.1`.

**The 6 NOT CONVERGED route-L `Gamma_L^2` backgrounds:** `canonical_AX_expo_10.7_0.01`,
`canonical_AX_kuzmin_9.4_0.01`, `canonical_AX_kuzmin_10.45_0.1`, `canonical_AX_kuzmin_10.7_0.01`,
`alt_AX_expo_10.9_0.01`, `alt_AX_kuzmin_10.9_0.01`.

**EFN1 route D, per background** (stop time in e-folds, R2 → R3 → R4): ten are monotone with `|d2| < |d1|` but the
GCI error swamps the extrapolated limit. Example, `primary_canonical_expo_9.4_0.1`: values 15.877 → 13.356 → 11.628,
`d1` -2.522, `d2` -1.728, p 0.932 (in window), `Q_inf` 7.87, `E` 4.70 against the line `0.20 |Q_inf|` = 1.57
→ NOT CONVERGED; two are monotone non-shrinking
(`primary_alt_kuzmin_9.4_0.1`, `primary_canonical_expo_10.45_0.1`) → DIVERGING. The `dthalf` sub-batch in the same
file is a single-resolution integrator control (n = 1, NOT EVALUABLE) and is not part of the graded family.

### What RULE-GC decides

1. **The minimum D.P in the external-field family is not a convergent quantity.** It diverges on 7 of 32 backgrounds
   and is not converged on 20 more. This is the quantity SCS2's KA4 clause tried to compare between two grids. SCS2's
   "the coarse grid is 20 to 35 % shallower" was not a near miss to a limit — there is no limit to agree with. **That
   is a verdict, and it is the first time this family's magnitude question has been decided rather than left open.**
2. **The negative-cell charge fraction is largely convergent, and so is route L's `Gamma_L^2` and route 2's
   `Gamma_2^2`.** On SCS2's pre-A4 ladder the charge fraction converges on 21 of 32 backgrounds; on SCS3's A4 ladder
   on 28 of 32; route L's `Gamma_L^2` on 26 of 32; route 2's `Gamma_2^2` on 14 of 16. They do not converge on *every*
   background, so by SCS3's A4 combination rule the families still read NO VERDICT — but the blockers are now named
   backgrounds, not a global "magnitudes never converge".
3. **EFN1's route D stop time diverges with refinement.** This confirms, at the level of a pre-registered rule rather
   than an impression, EFN1's own diagnosis that the graded "LEAVES" is a boundary artefact at
   r = 0.41-0.43 r_e, theta = 90 deg: the quantity it measures has no grid-independent value.
4. **EFN1's route W cannot be decided at all.** `Gamma`, `c3` and `c2` exist at two resolutions (R2, R3). RULE-GC
   returns NOT EVALUABLE for all 12 backgrounds. **This is a blocker, and it is named: a third route-W resolution is
   required before any convergence rule can say anything about it.**

**No lane's frozen label moves under R3.** SCS2's external-field family still fails a known answer (KA4 — now for a
stronger reason: the quantity diverges). SCS3's A4 requirement that every background converge is still not met.
EFN1's route D is still blocked by its boundary. What moved is the *record*: three lanes that said "the magnitudes
never converge" now say which quantity diverges, on which backgrounds, and which quantities do converge.

**Status of R3: COMPLETE.**

---

## 4. What is still blocked, and by what

| item | blocker | what it would take |
|---|---|---|
| BX1's frozen label | its own KA3 (fails) and MB2 (does not bite), both 256^3 simulation gates | a KA3(a')-style re-freeze and an MB2' line, committed alone, then a rerun. Not attempted here. |
| EFN1 route W | only two resolutions exist for `Gamma`, `c3`, `c2` | one more route-W resolution. Not attempted here (no solver was run by CLOSE-4). |
| SCS3's in-plane (PL) family | three grids, R3 does not fit in memory (SCS3 §1) | a larger-memory run. Outside CLOSE-4's remit. |
| DCN1's lane label | KA3 and KA4 fail as frozen; the only all-pass reading (A6) is post hoc | a fresh criteria commit with A6's grid promoted before any number. Not attempted here. |
| KL1 / KL1R Part B | MB2 does not bite (0.46 / 0.47 widths against 0.5) | a re-frozen MB2 line. Not attempted here. |

## 5. Files

- `FROZEN_CRITERIA.md` — the pre-registration, committed alone before any run
- `close4_ma2_fixed.py` → `parts/ma2_fixed.json`, `parts/ma2_fixed.out` (R1)
- `close4_m3.py` → `parts/m3_repaired.json`, `parts/m3_repaired.out` (R2)
- `close4_gc.py` → `parts/gc_SCS2.*`, `parts/gc_SCS3.*`, `parts/gc_EFN1.*` (R3)
- `NOVERDICT.md` — this file

No lane outside `hy4_preview_push/CLOSE-4_noverdict_repairs/` was modified. KL1's, KL1R's, DCN1's, SCS2's, SCS3's and
EFN1's scripts were imported read-only; no source line of any of them was edited.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.