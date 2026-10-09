# CFG560: no friction signal. Bar rotation rates do not track the law's dark fraction at corotation (MaNGA TW, 210 bars)

Criteria 90477f2ca (committed before the script). Script `cfg560_bars.py` (< 1 min, niced). κ = ½ fitted; both footings (they move f_dark, not the ranks, so the correlations are identical).

| subset | N | median f_dark (can / alt) | S1 ρ(R, f_dark) | S2 partial ρ given R_CR | S3 ρ(R, g/a₀) |
|---|---|---|---|---|---|
| all with bounds | 210 | 0.35 / 0.40 | +0.104 (p 0.13) | +0.075 (p 0.28) | −0.104 |
| σ_R/R ≤ 0.35 (primary) | 104 | 0.36 / 0.40 | −0.044 (p 0.66) | **−0.091 (p 0.35)** | +0.044 |
| σ_R/R ≤ 0.20 | 37 | 0.32 / 0.37 | +0.080 (p 0.64) | −0.109 (p 0.52) | −0.080 |

**Verdict: NO FRICTION SIGNAL.**

**Reading.** In none of the subsets do bars rotate measurably slower where the law's dark fraction near corotation is higher. Three readings fit this, and the lane cannot separate them:
- weak inner friction, consistent with settling's low inner cold density (the retained cold mass sits mostly at large radius);
- weak friction in ΛCDM halos at these radii;
- h29's finding that MaNGA TW R values are dominated by measurement systematics (R correlates with its own error).

It does **not** support a strong friction signature of a responsive dark component at corotation. It does not separate settling from ΛCDM, as declared.

**Controls.**
- K1 PASS (210 rows, median R 1.663, as h29).
- K2 PASS after a tolerance fix.
- MUTATE (R shuffled) gives a null: the run exits as designed, but the check is uninformative because the real correlation is already null.

**Departures (disclosed; fixed after the first run, before any verdict was read).**
- (1) The table's e_R/E_R columns are the published lower/upper BOUNDS, so the half-width is (E − e)/2. The first run averaged the bounds, which emptied the quality subsets.
- (2) brentq's default absolute tolerance was too coarse for accelerations near 1e-10; K2 failed on it.

One-line summary: CFG560 bars × law dark fraction at corotation: NO FRICTION SIGNAL (partial ρ −0.09, p 0.35, N 104); cannot separate settling from ΛCDM; TW systematics (h29) dominate.
