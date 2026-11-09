# TR1 RESULT: NO TRACER FOLLOWS (canonical) / NO TRACER FOLLOWS (alt), on both readings

Criteria 45ee5f7d8b (frozen, committed alone before any script or number). tr1.py, tr1.out/.json, tr1_MUTATE.out/.json
and this file are in the result commit. A grading lane of the adopted law; it adopts nothing. Both footings separately
(canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2, the loaders' values). kappa = 1/2 FITTED; not theory closed. No particle
is named: the component is "the missing mass".

## The question and the answer

Per cluster and per r/R500 bin (0, 0.25, 0.5, 0.75, 1, 2), does the cluster missing mass follow the hot gas, the stars,
gas + stars, or the hydrostatic total, with ONE amplitude per cluster? **On X-COP (the primary leg, 7 clusters with
measured stars) no single tracer follows, on either reading of the missing mass, on either footing, and in every
bracket but one.** The missing mass is MORE concentrated than the gas, than gas + stars and than the hydrostatic total
(inner bins high, outer bins low for all three), and LESS concentrated than the stars (inner bins low). It sits between
the stars and everything else, as QX33 found on CLASH, now per cluster and per bin. The closest tracer is the
hydrostatic total, and its amplitude is the same in every cluster to 0.05 dex.

Two readings were graded (frozen):
- **D (the brief's):** M_miss(<r) = M_dyn(<r) - M_law(<r), M_law = r^2 g_law(g_bar)/G.
- **S (source):** M_src(<r) = r^2 g_N(g_dyn)/G - M_bar(<r), the extra mass that, added to the baryons inside the law,
  gives g_dyn (the reading of QX29 B1, NA2's F and QX33's M_need).
Both name the same closest tracer (tot) and the same pattern. They differ only in how far each misses.

## Labels (frozen rule: FOLLOWS iff RMS <= 0.10 dex and max |SHAPE_b| <= 0.15 dex; UNIVERSAL iff SD(log A) <= 0.10)

| leg | reading | canonical | alt |
|---|---|---|---|
| **X-COP (decides)** | D | **NO TRACER FOLLOWS** (closest tot, inner HIGH); bracket-sensitive: inside R500 tot FOLLOWS | **NO TRACER FOLLOWS** (closest tot, inner HIGH); bracket-sensitive: inside R500 tot FOLLOWS |
| **X-COP (decides)** | S | **NO TRACER FOLLOWS** (closest tot, inner HIGH) | **NO TRACER FOLLOWS** (closest tot, inner HIGH) |
| CLASH (second leg) | D | tot (bar also follows) | tot (bar also follows) |
| CLASH (second leg) | S | TIE (tot, bar) | TIE (tot, bar) |

**The specification for the closing statement** (frozen meaning: a tracer that FOLLOWS with a UNIVERSAL amplitude on
both footings) **is NOT a single-amplitude baryon tracer.** On the closest tracer, the shape the missing mass needs is
the table below: a fraction of the hydrostatic total that falls outward, with the same amplitude in every cluster.

## Per-bin SHAPE, X-COP primary

Cluster median of the per-cluster residual, dex; 95 % bootstrap intervals over clusters shown for tot in bins 0 and 4 (all
bins and tracers in tr1.json); 7 clusters per bin, 6 in 1-2 R500.

| reading, footing | tracer | 0-0.25 | 0.25-0.5 | 0.5-0.75 | 0.75-1 | 1-2 | RMS | A median | SD(log A) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| D canonical | gas | +0.328 | +0.126 | +0.003 | -0.142 | -0.321 | 0.336 | 4.17 | 0.104 | no |
| D canonical | stars | -0.396 | +0.182 | +0.216 | +0.103 | -0.068 | 0.326 | 37.4 | 0.135 | no |
| D canonical | bar | +0.207 | +0.145 | +0.030 | -0.098 | -0.286 | 0.297 | 3.67 | 0.097 | no |
| D canonical | **tot** | **+0.145** [+0.095, +0.155] | +0.098 | +0.026 | -0.064 | **-0.216** [-0.439, -0.128] | 0.165 | 0.506 | **0.047** | no (closest) |
| D alt | gas | +0.357 | +0.146 | +0.012 | -0.152 | -0.377 | 0.368 | 3.74 | 0.114 | no |
| D alt | stars | -0.363 | +0.209 | +0.215 | +0.101 | -0.124 | 0.483 | 33.5 | 0.212 | no |
| D alt | bar | +0.221 | +0.166 | +0.039 | -0.107 | -0.341 | 0.326 | 3.34 | 0.105 | no |
| D alt | **tot** | **+0.173** [+0.110, +0.187] | +0.119 | +0.035 | -0.072 | **-0.267** [-0.460, -0.156] | 0.179 | 0.461 | **0.049** | no (closest) |
| S canonical | gas | +0.443 | +0.178 | +0.002 | -0.189 | -0.444 | 0.389 | 2.61 | 0.105 | no |
| S canonical | stars | -0.273 | +0.252 | +0.198 | +0.061 | -0.222 | 0.336 | 24.4 | 0.134 | no |
| S canonical | bar | +0.317 | +0.200 | +0.032 | -0.155 | -0.412 | 0.342 | 2.28 | 0.094 | no |
| S canonical | **tot** | **+0.251** [+0.162, +0.264] | +0.153 | +0.030 | -0.116 | **-0.346** [-0.456, -0.234] | 0.211 | 0.335 | **0.052** | no (closest) |
| S alt | gas | +0.483 | +0.203 | +0.009 | -0.204 | -0.507 | 0.406 | 2.22 | 0.110 | no |
| S alt | stars | -0.236 | +0.282 | +0.193 | +0.052 | -0.288 | 0.452 | 20.8 | 0.185 | no |
| S alt | bar | +0.355 | +0.226 | +0.040 | -0.173 | -0.476 | 0.358 | 1.93 | 0.097 | no |
| S alt | **tot** | **+0.285** [+0.186, +0.304] | +0.179 | +0.038 | -0.137 | **-0.409** [-0.473, -0.272] | 0.235 | 0.299 | **0.061** | no (closest) |

Every one of the 7 clusters shows the same pattern on tot (positive inside 0.5 R500, negative beyond 0.75; per-cluster
rows in tr1.out); the 95 % intervals on bins 0 and 4 exclude zero for gas, bar and tot on every reading and footing. A644's 1-2 R500 bin is the frozen
-1.0 marker (M_X <= 0 there: M_dyn meets M_law beyond R500 in that cluster; 2-3 such points in the sample); it does not
move any cluster median.

**What the missing mass is, as a fraction of the hydrostatic total** (cluster medians of M_X / M_dyn per bin):

| reading, footing | 0-0.25 | 0.25-0.5 | 0.5-0.75 | 0.75-1 | 1-2 R500 |
|---|---|---|---|---|---|
| D canonical | 0.71 | 0.66 | 0.58 | 0.46 | 0.32 |
| D alt | 0.68 | 0.63 | 0.54 | 0.41 | 0.26 |
| S canonical | 0.60 | 0.48 | 0.37 | 0.27 | 0.16 |
| S alt | 0.56 | 0.43 | 0.32 | 0.22 | 0.12 |

Same table in units of the baryons, M_X / (M_gas + M_star): D canonical 6.1, 5.5, 4.2, 2.9, 1.9; S canonical 4.8, 4.2,
2.8, 1.7, 0.9 (alt in tr1.out). The record's "stars + gas at 3-4x" is a bin-averaged value of a ratio that falls by a
factor 3-5 from the core to 1-2 R500.

## Brackets (verify the FAIL as hard as a PASS)

| bracket | D canonical / alt | S canonical / alt |
|---|---|---|
| b1 without A2319 (6) | every tracer DOES NOT FOLLOW; tot RMS 0.173 / 0.187 | every tracer DOES NOT FOLLOW; tot 0.219 / 0.243 |
| b2 all 12, 5 with imputed stars | every tracer DOES NOT FOLLOW; tot 0.151 / 0.170 | every tracer DOES NOT FOLLOW; tot 0.206 / 0.233 |
| b3 inside R500 only (4 bins) | **tot FOLLOWS: RMS 0.077, max 0.116 / RMS 0.090, max 0.138**; bar 0.129 / 0.142 (no); gas, stars no | every tracer DOES NOT FOLLOW; tot 0.137 / 0.157, bar 0.186 / 0.205 |

The X-COP FAIL survives every bracket on reading S. On reading D it survives b1 and b2 and turns on the 1-2 R500 bin: inside
R500 the missing mass follows the hydrostatic total at a universal ~0.5 M_dyn (A 0.51 / 0.46, SD 0.05). Beyond R500 the
hydrostatic mass is the forward-model fit resting on SZ pressure (HL3 limit 9); that bin is graded as frozen, and the
label carries "bracket-sensitive". Gas, stars and gas + stars fail every bracket on both readings.

## Core read inside 0.25 R500 (r1, reported, not graded)

Cluster-median residual against each tracer's five-bin fit, sub-bins 0-0.05 / 0.05-0.10 / 0.10-0.25 R500 (D canonical):
gas +0.62 / +0.34 / +0.21; **stars -0.77 / -0.49 / -0.07**; bar +0.17 / +0.20 / +0.21; tot +0.14 / +0.15 / +0.13.
The missing mass does not follow the BCG cusp (stars fall 0.8 dex short in the inner 5 % of R500), and inside the core it
is flat against gas + stars and against the total (no extra cusp): the excess over those tracers is a single step of
+0.15 to +0.2 dex across the whole inner quarter of R500, not a central spike. Reading S is the same at +0.1 dex higher.

## Two-component mix (r2, reported, never a label)

M_X = a M_gas + b M_star per cluster (NNLS on relative residuals): reading D canonical a = 0-6, b = 4-12 (median a 3.0,
b 6.2); per-cluster bin rms 0.07-0.19 (A644 0.88, its 1-2 bin). A free stars/gas mix with two amplitudes per cluster
does better than any one tracer but scatters by x3 in b between clusters; a universal mix does not exist in these 7.

## Reconciliation with KA2 (r4, added after the first run, reported only; disclosed)

QX29 B1 (baryon-traced source at one amplitude f_cap R = 4.227) passed X-COP G4 (rms 0.082) while TR1 grades bar as
DOES NOT FOLLOW on reading S. r4 runs B1's exact model on TR1's points: on the TOTAL mass at r/R500 0.1-0.7 it gives
mean +0.014, rms 0.071 (alt -0.010, 0.071), reproducing the pass; on the COMPONENT the same model is off by +0.05, -0.01,
-0.17, -0.39, -0.68 dex by bin (alt to -0.81), and the total mass itself goes -0.19 and -0.28 dex low beyond 0.75 R500.
The pass was a total-mass read over 0.1-0.7 R500, where the missing component's shape error is diluted by the baryons
and the law's boost (about x0.5) and the outer bins are absent. TR1 grades the component itself over 0-2 R500.
Nothing in QX29 changes.

## CLASH second leg (per cluster, 16 X-ray selected; bracket all 20)

The Tian+2020 table carries cluster identity, so CLASH is graded per cluster; only gas + BCG ("bar") and the lensing total
("tot") exist on this leg. 12 of 16 clusters have points in two bins (0-0.25 and 0.25-0.5; two clusters reach 0.5-0.75,
not graded). Both tracers FOLLOW on both readings and footings (D tot RMS 0.022 / 0.026, max bin 0.013 / 0.015; bar
0.056 / 0.057 with SD(log A) 0.16 = CLUSTER-DEPENDENT; S TIE tot / bar). This has little power: across the two shared
bins X-COP's tot SHAPE moves by only 0.05 dex (+0.145 to +0.098, D canonical), well under the lines, so CLASH and X-COP
AGREE where they overlap (the inner half of R500) and CLASH cannot test the outer bins where the X-COP FAIL lives. The
CLASH tot amplitude is UNIVERSAL (SD 0.044 / 0.049; median A 0.71 / 0.69 on D, i.e. 71 % of the lensing mass missing
inside 0.5 R500, beside X-COP's 0.71 / 0.66 in its two inner bins). HE6 HIT.

## HFF member light (r3, reported, not graded)

Projected cumulative F160W member light around the brightest F160W member, slope d log L(<R)/d log R over 50-300 kpc:
A2744 1.45 (a merger with two BCGs; the brightest member is off-centre), AS1063 0.67, M0416 1.09, M1149 0.50; X-COP 3D
beside them: stars 0.57, gas 2.22, missing mass 1.73 (D) / 1.67 (S). Projection steepens a cumulative slope, member light
is magnitude-limited and excludes intracluster light, and the HFF fields reach 460-940 kpc. Read only as: member light
is shallower than the missing mass in every HFF cluster, consistent with the X-COP stars result. Redshifts: Umetsu+2016
table 1 (AS1063 = RXJ2248, M0416, M1149) and Groener+2016 (A2744), both on disk.

## Known answers (all PASS; tr1.out prints them first)

| KA | reference | TR1 |
|---|---|---|
| KA1 HL3 hydrostatic medians on the 7 | +0.530 / +0.463 / +0.372 / +0.264 / +0.161 (alt +0.500 / +0.429 / +0.339 / +0.229 / +0.126) | +0.5304 / +0.4629 / +0.3722 / +0.2642 / +0.1612 (alt +0.5001 / +0.4288 / +0.3388 / +0.2295 / +0.1257) |
| KA2 QX29 B1 X-COP, f_cap R | -0.003 / 0.082 (alt -0.027 / 0.087) | -0.0026 / 0.0819 (alt -0.0266 / 0.0872) |
| KA3 CLASH parse + HL3 lensing medians | 84 / 20; +0.578 / +0.516 (alt +0.549 / +0.485) | 84 / 20; +0.5784 / +0.5159 (alt +0.5489 / +0.4849) |
| KA4 law inversion; D = S = 0 at M_dyn = M_law | 1e-12; 1e-9 | 4.4e-16; 2.9e-16 |

## MUTATE (tr1_MUTATE.out): all bite, both footings, both readings (target: tot, the closest)

| check | D canonical | D alt | S canonical | S alt |
|---|---|---|---|---|
| M1 swap A1795 <-> ZW1215 tot profiles (pair RMS) | 0.107 -> 0.185 BITES | 0.131 -> 0.205 BITES | 0.191 -> 0.254 BITES | 0.222 -> 0.284 BITES |
| M2 plant +0.3 dex inside 0.25 R500 (SHAPE_0) | +0.145 -> +0.385 BITES | +0.173 -> +0.413 | +0.251 -> +0.491 | +0.285 -> +0.525 |
| M3a A x2, no refit (RMS) | 0.165 -> 0.343 BITES | 0.179 -> 0.350 | 0.211 -> 0.367 | 0.235 -> 0.382 |
| M3b M_X x2 in A1795, A2029, A2142, refit (SD log A) | 0.047 -> 0.157, UNIVERSAL -> CLUSTER-DEPENDENT | 0.049 -> 0.150 | 0.052 -> 0.147 | 0.061 -> 0.140 |

Disclosure: the criteria wrote that M3a moves every residual "+0.301"; doubling A moves it by -0.301 (the magnitude is
what the check uses). Because no tracer FOLLOWS on the primary, M2 and M3a were judged by their frozen "already does not
follow" branches (SHAPE_0 rise >= 0.20; RMS rise >= 0.10); the flip branch was not exercised.

## Hand estimates (frozen)

| HE | claim | result | |
|---|---|---|---|
| HE1 | gas DOES NOT FOLLOW both readings, inner HIGH, SHAPE_0 ~ +0.3 (D) | +0.328 / +0.357 (D), +0.443 / +0.483 (S) | HIT |
| HE2 | stars DOES NOT FOLLOW, inner LOW | -0.396 / -0.363 (D), -0.273 / -0.236 (S) | HIT |
| HE3 | D: bar no (SHAPE_0 ~ +0.25), tot closest (RMS ~0.13, failing at 1-2), tot FOLLOWS inside R500 (RMS ~0.07); label NO TRACER FOLLOWS | bar +0.207; tot RMS 0.165 / 0.179; b3 tot 0.077 / 0.090 FOLLOWS; label as estimated | HIT |
| HE4 | S: bar FOLLOWS (from QX29 B1); tot does not | bar RMS 0.342 / 0.358, DOES NOT FOLLOW; tot does not | **MISS** (bar): the estimate took QX29's total-mass pass as a component pass (r4) |
| HE5 | best tracer's SD(log A) 0.10-0.15; S/bar A ~3-4 | tot SD 0.047-0.061 (tighter, UNIVERSAL); S/bar A 2.28 / 1.93 (D/bar 3.67 / 3.34) | MISS (both parts) |
| HE6 | CLASH: both tracers follow, low power | both follow, both readings; 2 shared bins | HIT |

## Amplitudes per cluster (X-COP primary; gas / stars / bar / tot)

| cluster | D canonical | D alt | S canonical | S alt |
|---|---|---|---|---|
| A1795 | 4.17 / 37.4 / 3.60 / 0.49 | 3.74 / 33.5 / 3.23 / 0.44 | 2.55 / 22.8 / 2.20 / 0.30 | 2.13 / 19.1 / 1.84 / 0.25 |
| A2029 | 4.33 / 36.3 / 3.71 / 0.53 | 3.98 / 33.3 / 3.41 / 0.48 | 2.86 / 23.8 / 2.47 / 0.35 | 2.46 / 20.4 / 2.13 / 0.30 |
| A2142 | 3.94 / 36.9 / 3.43 / 0.51 | 3.59 / 33.5 / 3.12 / 0.46 | 2.61 / 24.4 / 2.27 / 0.33 | 2.22 / 20.8 / 1.93 / 0.28 |
| A2319 | 5.99 / 44.4 / 4.80 / 0.60 | 5.66 / 41.9 / 4.54 / 0.57 | 4.30 / 32.0 / 3.45 / 0.43 | 3.83 / 28.5 / 3.07 / 0.39 |
| A644 | 3.49 / 27.2 / 2.89 / 0.44 | 3.08 / 13.8 / 2.58 / 0.42 | 2.41 / 17.0 / 2.02 / 0.33 | 2.20 / 9.9 / 1.85 / 0.30 |
| A85 | 4.08 / 62.8 / 3.67 / 0.50 | 3.72 / 57.0 / 3.34 / 0.46 | 2.55 / 39.1 / 2.28 / 0.32 | 2.16 / 33.0 / 1.92 / 0.27 |
| ZW1215 | 6.76 / 64.1 / 5.63 / 0.59 | 6.36 / 60.3 / 5.29 / 0.56 | 4.11 / 39.1 / 3.42 / 0.36 | 3.58 / 34.1 / 2.97 / 0.32 |
| SD(log A) | 0.104 / 0.135 / 0.097 / **0.047** | 0.114 / 0.212 / 0.105 / **0.049** | 0.105 / 0.134 / 0.094 / **0.052** | 0.110 / 0.185 / 0.097 / **0.061** |

A is the bin-averaged ratio (log-mean over bins of the per-bin median of M_X / M_T); with the shape not flat, A is a
convention and the per-bin table above is the specification. CLASH amplitudes per cluster are in tr1.out.

## Downloads

The owner approved downloads of public per-cluster lensing mass profiles (HFF clusters; CLASH per-cluster profiles where
published as tables), relayed by the orchestrator on 2026-11-09 after the criteria were frozen. **None was made, and no
amendment was filed,** because a lensing profile alone cannot enter TR1's statistic: M_X needs the baryon mass
M_bar(<r) at the same radii (gas and stars), and
- for CLASH beyond 600 kpc no per-radius gas profile is on disk (Tian+2020's g_bar stops at 600 kpc; Donahue+2014 has no
  per-radius gas table, HL3 FETCH_LOG), so a lensing profile to R500 adds only the tot tracer's denominator with no
  missing mass to divide;
- for the HFF clusters no gas profile of any kind is on disk, and AS1063 (RXJ2248), M0416 and M1149 are already in
  Tian's per-cluster table to 600 kpc;
- HL3 already found Umetsu+2016's surface-density profiles published as figures only (not digitised, by rule).
What a download would add, in order of value:
1. **Per-cluster gas mass profiles to >= R500 for the CLASH / HFF clusters** (Chandra / XMM deprojected density
   profiles published as tables, e.g. the ACCEPT archive, Cavagnolo et al. 2009) TOGETHER WITH per-cluster lensing
   profiles to R500 (tabulated CLASH weak + strong lensing profiles if a table release exists). That is the one
   combination that grades the outer bins on a lensing leg, where the X-COP FAIL lives. It needs the owner's separate yes
   for the gas profiles (outside the 11-09 scope) and its own criteria.
2. HFF lens-model convergence maps (MAST) with the on-disk member photometry: a projected stars-versus-total comparison
   inside ~500 kpc. It cannot form M_X without gas and is not worth a lane by itself.

## Reading

1. The cluster missing mass has no single-amplitude baryon tracer. Against gas, gas + stars and the hydrostatic total it
   is too concentrated (inner bins +0.15 to +0.48 dex), and against the stars it is too extended (-0.24 to -0.40 dex in
   the inner bin, -0.8 dex in the inner 5 % of R500). It lies between the stellar cusp and the total, as QX33 found on
   CLASH.
2. The tightest description is a falling fraction of the hydrostatic total: M_X / M_dyn = 0.71, 0.66, 0.58, 0.46, 0.32
   by bin (D canonical; S canonical 0.60 to 0.16). The fraction is the same in every X-COP cluster to 0.05 dex, and the
   same as CLASH's lensing value (0.71) where the two legs overlap. On reading D, inside R500, this is a FOLLOWS at ~0.5
   M_dyn.
3. For the closing statement: the component the law is missing in clusters must have a profile that is a radius-
   dependent fraction of the total (about 70 % inside 0.25 R500 falling to about 45 % at R500 on reading D). Its
   amplitude is cluster-universal, but no baryon component predicts it at one amplitude. "Traces stars + gas at 3-4x"
   holds only as a bin average. The per-bin ratio to gas + stars falls from 6 to 2 (D) or from 5 to 1 (S) between the
   core and 1-2 R500.

## Limits

1. Seven X-COP clusters (measured stars); all-12 bracket with imputed stars agrees.
2. The 1-2 R500 bin is the forward-model hydrostatic mass (SZ pressure); reading D's FAIL rests on it (b3).
3. CLASH reaches 0.59 R500 at most; only two shared bins, low power; gas and BCG are not split there.
4. The amplitude is defined as a log-mean over bins (frozen); a different averaging changes A, not the shape or the
   label.
5. A Newtonian hydrostatic mass is used as M_dyn (as every cluster lane on this path does); HL3 showed the lensing leg has
   the same per-bin residual inside 0.5 R500.
6. r4 was added after the first run to reconcile KA2. It is reported only, no label rests on it, and it is disclosed
   here.

## Compute and process

tr1.py about 5 s, peak RSS 315-373 MB (main), 197 MB (mutate); one thread, nice 10; SIGTERM exits before writing.
HL3's builder executed from source up to its KA4 block (nothing written in HL3's folder); QX29 / QX27 imported read-only
with argv cleared. One code fix before the first complete run (np.trapz for an older numpy), no number touched. No
download.

kappa = 1/2 FITTED; not theory closed. Adopts nothing; the owner adopts.
