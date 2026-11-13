# EUC13 (POPULATION SOURCE GATE): RESULT

2026-11-12. Criteria 486c59d12a (alone, before any script, fetch or number). Scripts and outputs 871b86be61.
Amendment A1 9dd8ef58a2 (post hoc, alone), its reading 525d4752f4.

## Verdict: EUC13-P NO VERDICT / NO VERDICT (canonical / alt). f25 statistic: CEILING BROKEN / CEILING BROKEN.

This is a **population** gate: it grades Euclid's lenses against modelled and borrowed source-redshift distributions,
not against measured sources. It is weaker evidence than EUC1-F, which stays open and untouched until row-level
source redshifts exist. Nothing here is a pass of the theory.

With source redshifts drawn from AGEL DR2 (M1), from DESI Strong Lens Foundry IV (M2), or from a validated forward model
(M3, μ = 10), the median Euclid lens needs **+0.20 to +0.30 dex** (1.6 to 2.0 × Salpeter) for law S. No member's
interval reaches the HOLDS line (every lower bound is above 0.15), and only M2 on canonical clears the FAILS line, so
the word is NO VERDICT on both footings. In every member 43 to 58 % of P needs more than 1.78 × Salpeter; every lower
bound on f25 is above EUC1's 0.25 break line. All known answers pass; the mutation twin exits 1.

κ = ½ FITTED; not theory closed. Footings never pooled.

## 1. Members on sample P (N = 3,192; law S; 95 % intervals, recentred, 400 replicates)

| Member | median z_s | b_med canonical | b_med alt | f25 canonical | f25 alt |
|---|---|---|---|---|---|
| M1 AGEL DR2 (N 90) | 2.05 | +0.238 [+0.213, +0.265] | +0.220 [+0.195, +0.247] | 0.479 [0.443, 0.519] | 0.451 [0.415, 0.491] |
| M2 SLF IV, MUSE (N 49) | 1.60 | +0.298 [+0.253, +0.346] | +0.281 [+0.235, +0.330] | 0.576 [0.512, 0.645] | 0.549 [0.480, 0.615] |
| M3 μ 10, law's own cross-section | 2.17 | +0.233 [+0.219, +0.244] | +0.215 [+0.202, +0.227] | 0.474 [0.453, 0.489] | 0.445 [0.427, 0.462] |
| M3 μ 10, saturated (SIS) limit | 2.27 | +0.222 [+0.208, +0.233] | +0.204 [+0.191, +0.217] | 0.456 [0.437, 0.472] | 0.427 [0.408, 0.443] |
| **M3 envelope** | | **[+0.208, +0.244]** | **[+0.191, +0.227]** | [0.437, 0.489] | [0.408, 0.462] |

Replicates resample P, resample the published sample (M1, M2), redraw sources and redraw P's catalogued errors (EUC1
run 6). Intervals are recentred on the catalogued-value point because the error draw adds measured noise a second time;
raw percentiles are in `euc13.out` (they sit 0.01 to 0.02 dex higher). M1 and M2 points equal EUC10 Part B exactly; the
new part is the honest width: ± 0.026 (M1) and ± 0.047 (M2) instead of EUC10's ± 0.005 draw spread.

## 2. Validation of M3 (a gate on the member, sis weight)

| Setting | V1: SLF IV median, model vs observed (47 systems) | V1 KS p | V2: PIT KS p (8 ECLIPSE lenses), extremes | Kept |
|---|---|---|---|---|
| μ 3 | 0.962 vs 1.434 | 9e-9 | 0.0006, 1 | dropped |
| μ 10 | 1.266 vs 1.434 | 0.10 | 0.105, 1 | **survives** |
| μ marginal (bias on, p(μ) ∝ μ⁻³, 2-30) | 1.074 vs 1.434 | 2e-4 | 0.016, 1 | dropped |

Arcs on P: VIS 22.69 median (16-84 %: 21.54-23.55); 3,021 of 3,192 from the catalogue's flux ratio × the lens's MER
flux, 171 from neighbours. V2 could evaluate only 8 of the 17 known-source ECLIPSE lenses (L000613, L004966, L008608,
L013325, L014483, L015763, L015871, L016382); the rest lack an arc magnitude or a lens redshift.

**Two warnings from validation, in opposite directions.** On SLF IV the surviving model puts sources 0.17 lower than
observed (inside the 0.25 tolerance). On the 8 known ECLIPSE sources it puts them *higher* than observed: 7 of 8 PIT
values exceed 0.5 (0.66, 0.82, 0.76, 0.89, 0.04, 0.999, 0.28, 0.86); L015763 (z_s 1.366) sits at PIT 0.999. Those 8
are bright, wide, followed-up systems, so this is not a measurement of P; but if Euclid's sources lie lower than M3
puts them, the true b_med is higher than M3's +0.23 / +0.22, towards M2.

**M3's interval understates its uncertainty.** It carries resampling and catalogue noise only; the model systematics
(VIS ≈ HSC i, μ fixed at 10, COSMOS field variance and incompleteness beyond i ≈ 27) are not in it. The only systematic
bracket that survived validation is the cross-section form (full vs SIS: 0.011 dex).

## 3. Cross-section approximation (self-consistency and A1)

Self-consistent lens boost b*: median +0.205 / +0.184; largest per-lens change in the third iteration 0.017; no
predictive mass at a capped Einstein radius. A1 (post hoc, μ 10, boost fixed): b = 0 gives +0.232 / +0.213, b = 0.5
gives +0.237 / +0.218, against +0.233 / +0.215 self-consistent. The weight's dependence on the lens mass moves b_med by
at most 0.004 dex.

## 4. Readings by Einstein radius against EUC5's sealed bands (NOT EUC5-F; bands not moved)

| Class (N) | M1 | M2 | M3 full / sis | Band canonical / alt | Place |
|---|---|---|---|---|---|
| θ_E < 1.0″ (1,948) | +0.167 / +0.149 | +0.231 / +0.215 | +0.157 / +0.145 (can.) | −0.19..+0.22 / −0.19..+0.21 | inside, all |
| 1.0-1.3″ (691) | +0.280 / +0.262 | +0.333 / +0.316 | +0.276 / +0.266 (can.) | −0.05..+0.30 / −0.06..+0.34 | inside, all |
| θ_E ≥ 1.3″ (553) | +0.449 / +0.431 | +0.496 / +0.477 | +0.454 / +0.445 (can.) | +0.03..+0.32 / +0.03..+0.31 | **above**, all |

M1, M2 columns are canonical / alt. Every member, both footings, puts the wide class above its dynamical band (lower
bounds +0.40 to +0.45) and the two smaller classes inside. This is EUC1's wide-lens excess again, now at modelled
source redshifts. It is a reading on sample P, not EUC5-F (sample S, row-level redshifts).

## 5. Checks (all pass)

KA1 SLACS +0.0815 / +0.0696. KA2 EUC1 source-free −0.0185 / −0.0439 (N 3,192). KA3 EUC10 Part B by its own recipe
+0.2381 / +0.2201 (AGEL), +0.2983 / +0.2816 (SLF IV); KA4 the same draws through EUC13's b table within 0.0001. KA5 b
table vs 300 direct solves per footing: max 1.5e-4. KA6 COSMOS2020 median photo-z at 23.5 < i < 24.5: 0.994. MUTATE
newton: b_med rises in every member and footing (M1 +0.238 → +0.347, M2 +0.298 → +0.399, M3 +0.233 → +0.349 canonical;
alt likewise), so the word would move to FAILS; exit 1.

## 6. Deviations and limits (disclosed)

1. CfA TAPVizieR did not answer; COSMOS2020 Classic (713,374 galaxies, FlagCOMBINED 0, i < 28) came from the CfA ASU
   service in 12 magnitude slices. Seven slices first returned server error pages ("database not reachable"); these were
   set aside and refetched, all logged in `_external_data/euc13_population_gate/MANIFEST.txt` (14 MB, untracked). Only
   the aggregate counts are committed. No IRSA, ESA or SPARCL query.
2. After the first full run one printed label was corrected ("μ marginal" → the setting actually used, μ 10, for the
   self-consistent boost). The re-run reproduced every number; only that line changed.
3. The criteria's bounding readings named the μ-marginal setting, which validation dropped; A1 ran them at μ 10.
4. Nothing is PROVISIONAL: every input is machine-readable (ECLIPSE, EUC3's cached MER table, COSMOS2020 via VizieR,
   the publications' own LaTeX). COSMOS2020 redshifts are photometric.
5. The lens MER flux may include some arc light (arc magnitude slightly too bright, source z slightly too low).

## 7. The lead's hand estimate

Partly wrong. M3's typical source sits near z 2.2, not 1.5-2, and reads +0.23 / +0.22, not +0.25 to +0.30. AGEL just
under 0.25 on canonical: right (+0.238). NO VERDICT both footings: right. f25 well above 0.25 in every member: right.

## 8. What this says

If Euclid's lensed sources are distributed like any population this lane could build or borrow, the law needs about
1.6-2.0 × Salpeter for the median Euclid lens, against 1.17 × for SLACS at measured redshifts; no member allows the
HOLDS line (1.41 ×). The excess sits in the wide lenses. The word stays NO VERDICT because the members straddle 0.25,
and a population model cannot replace measured redshifts. EUC1-F remains the gate.

Files: `euc13_fetch_cosmos.py`, `euc13.py`, `euc13_posthoc.py`; `euc13_cosmos2020_counts.csv`, `euc13.out`,
`euc13_results.json`, `euc13_per_lens.csv`, `euc13_MUTATE_newton.*`, `euc13_posthoc.*`.

    python3 -I euc13.py --data-dir <ECLIPSE dir> --lit <EUC10 lit dir>

Adopts nothing. κ = ½ FITTED; not theory closed.
