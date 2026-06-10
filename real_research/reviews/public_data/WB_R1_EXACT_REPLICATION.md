# WB-R1 — faithful published-selection replication (Chae 2023 / Banik 2024) + D1/D2/D4

*C. Zimmerman, 2026-06-09. `data/widebinaries/wb_exact_replication.py` (+`.out`). Cuts transcribed in
`wb_published_cuts.md`. El-Badry+2021 eDR3 catalog, Zenodo record 4435257 (DOI 10.5281/zenodo.4435257).
Inline execution, no swarms. This is the **Outcome-A relay** Fable was waiting on before the WB-3 Monte-Carlo.*

## The four-column table (framework a₀ = 9.36×10⁻¹¹; deep bins g_N/a₀ < 0.3)

| Selection | N | gate (±10% of pub) | D1 median σ/v_N | D2 super-escape f(ṽ>√2) | D4 mass-sensitivity |
|---|---|---|---|---|---|
| **Chae-exact** (cuts) | **24,111** | [23954, 29277] ✅ **PASS** | 0.117 | **0.097** | 1.40× (robust) |
| **Banik-exact** (RUWE<1.4) | 10,751 | [7750, 9472] +25% | 0.148 | **0.098** | 1.34× (robust) |
| **Banik-exact** (RUWE<1.2 proxy) | 9,508 | [7750, 9472] +0.4% over ceiling | 0.154 | **0.098** | 1.32× (robust) |

All thresholds: D1 stop-trigger >0.3, D2 stop-trigger >0.15, D4 stop-trigger >1.5. **Every cell is below its trigger.**

## Verdict: pre-registered **Outcome A** (clean below both thresholds → halt before MC, relay first)
With the **faithful Banik-cubic mass pipeline**, all three selections agree: **D2 super-escape ≈ 0.10, D1 ≈ 0.12–0.15**,
both below their stop-triggers, for **both teams' cuts**, and **stable across the entire RUWE 1.2–1.4 bracket** (N moves
9,508→10,751; the diagnostics do not move). The deep-MOND bins are **not** noise/contamination-dominated under faithful
selection. This is the clean-below-thresholds outcome → per the standing block, **halt before the Monte-Carlo and relay.**

## ⚠️ Mass-pipeline CORRECTION (supersedes the WB-2 headline number)
The earlier passes inverted the Banik mass cubic (M_G = 4.887 − 5.693x + 0.4164x² + 0.9611x³, x≡ln M) **outside its
valid range** (M_G∈[0.6,11.1], M∈[0.23,2.7] M☉). Extrapolated to M=0.08 M☉ the cubic returns a non-physical M_G≈6.4
(true ≈14), and being non-monotonic it corrupts the whole lookup → **systematically too-low masses → too-low v_N → INFLATED
ṽ = v_sky/v_N → spurious super-escape.** That bug produced the earlier **~0.48** Chae-cut super-escape and inflated the
WB-2 looser-sample **0.27**. With the inversion restricted to the cubic's valid, monotonic window and observed M_G clipped
to [0.6,11.1] (median M_tot = 1.26 M☉, 99.9% of the core inside Banik's [0.464,4.31] window), the **faithful super-escape
is ≈0.10**. **The earlier 0.48 / 0.27 are RETRACTED as mass-estimator artifacts** — do not cite them as the faithful number.
This correction runs *toward* a cleaner sample (less contamination than WB-2 implied); it is reported with the same rigor as
a deficit would be, and it explicitly does **not** license a boost claim (see below).

## What is firm, what is not (both directions)
**Firm (gate- and convention-independent):**
- **D4 robust, 1.3–1.4× for all selections** → the super-escape is **not** a mass-estimator artifact. *Fable's single
  biggest worry — that a separation-dependent mass bias masquerades as the velocity trend — is resolved.*
- The super-escape floor is **~10%** under faithful cuts, not ~25–50%. The deep bins are usable.

**Not adjudicated (the honest fence):**
- This is the **sky-projected** observable ṽ = v_sky/v_N for **both** selections. Chae's published ~5σ boost comes from a
  **3D deprojection Monte-Carlo** (inclination/eccentricity/phase, Hwang+2022) — **fork F3, NOT implemented here.** So
  "Chae-exact" replicates Chae's *cuts*, not his *estimator*; **this pass does not settle Chae-vs-Banik.**
- The median sky-projected ṽ rises **modestly** into deep-MOND (≈0.57→0.66). Whether that rise is a genuine boost or
  projection+noise **cannot be decided from the sky-projected statistic** — it needs the deprojection MC against a matched
  Newtonian forward model (WB-3). **Neither a manufactured boost nor a reflexive dismissal:** the data are clean enough to
  adjudicate; this pass does not adjudicate.

## Gate status & the genuine catalog-version differences (Fable Step-2 escape hatch)
- **Chae-exact lands IN the gate (24,111)** → faithful selection-replication achieved.
- **Banik-exact is at/just-above the gate ceiling.** With RUWE<1.4 it is +25% (10,751); with the **defensible RUWE<1.2 proxy**
  for his stricter astrometric χ²/ν cut (eq.4) it is **9,508, +0.4% over the +10% boundary** — and the diagnostics are flat
  across that whole bracket, so the edge-miss is immaterial. The residual gap to 8,611 is **three cuts not implementable from
  the El-Badry eDR3 catalog**, all of which would *remove* pairs (so this sample is *looser/more contaminated* than Banik's →
  its 0.10 super-escape is an **upper bound**; the true Banik is cleaner):
  1. **astrometric χ²/ν ≤ 1.2·max(1, e^{−0.2(m_G−19.5)})** (eq.4) — needs `astrometric_chi2_al`, absent → RUWE substitute;
  2. **faint-companion / triple search to m_G<20** — needs deeper imaging not in the catalog;
  3. **DR3-RV triple screen** (reject Δ(RV)>3σ or 3v_c) — El-Badry carries **DR2** RVs (mostly fill values), not DR3.
  Per Fable's WB-R1 Step 2, these are identified as **genuine catalog/data-availability differences**, not implementation drift.

## Next step (held, per Outcome A)
**WB-3 deprojection Monte-Carlo** is the real crux: a matched Newtonian (and framework-MOND) forward model that (a) reproduces
this σ/v_N(bin) and the ~10% super-escape floor from a *bound* population, then (b) deprojects to 3D to test whether the median
rise exceeds Newton. Held until this table is relayed and the forward model is pre-registered (`wb_mc_preregistration.md`).
**C1/C2 only — this says nothing about a₀(z) (C3 fence). Positions for Gaia DR4 (late 2026).**
