# D7c_q2_rar_gate — FROZEN CRITERIA (2026-10-22, committed alone before any script or number)

## Question
Does ANY law form already in the record's family pass BOTH the Cassini quadrupole Q₂ and SPARC's RAR shape, on both
footings? Scope: **UNSCREENED law forms only** (point-mass Sun + uniform external field, no L★ stiffness screening;
the screened case belongs to lane D7d_screened_q2). No conclusion here is phrased as "the framework fails Cassini";
the wording is "the unscreened law family passes/fails Cassini".

## Candidates (no new law invented)
Named record laws (ν(y) = g/g_N, y = g_N/a₀, w = ν − 1):
- **L** n=1 canonical, g_N = g²/(g+a₀): ν = (1+√(1+4/y))/2 (BRIEF §1, PAPER49, AG4).
- **Q** n=2, g² − g_N² = a₀g_N: ν = √(1+1/y). This is the same function as the "quadrature" P2 (CFG4 `nu_p2`, A25 "Q")
  and the retired "α=1" de Sitter–Unruh kernel (DESITTER_GAUGE_MOND_SCALE.md §2). One law, four names; a check verifies
  the identity numerically.
- **M** ν_mono, CFG4_common `nu_mono` (FP1's committed splice, exec'd read-only).
- **S** standard μ = x/√(1+x²) (the "α=2" kernel the DESITTER paper adopted on 2026-07-30, phenomenological).
- **R** ν_RAR = 1/(1−e^{−√y}): a reference shape only (A25's reference, CFG4 "reference only"), not a framework law.
  It is scored like the others and is the "best kernel" comparator if it fits best.

Families with a continuous parameter defined in the record (scanned; the sub-range passing both is reported, never a best fit):
- **capacity family** (AG4 G3, Lean T7 with n ∈ ℝ): u² + n g_N u = a₀ g_N, w_n(y) = (√(n²+4/y) − n)/2 (n=1 → L, n=2 → Q).
  Grid n ∈ {0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8}.
- **β family** (CFG4_common `nu_beta`, "effective description of transition sharpness"): ν_β = (1+y^{−β})^{1/(2β)} (β=1 → Q).
  Grid β ∈ {0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6}.

## Q₂ (D7b's validated solver, Route M, imported read-only from `D7b_cassini_Q2/d7b_cassini_q2.py`)
- No P5 turn-off (D7b: it moves Q₂ by ≤ 0.7 %). a₀ = 9.36e-11 (canonical), 1.13e-10 (alt), as in D7b.
- External field: E0 = Newtonian g_N,e = 6.913e-11 (A60, law-independent); E1/E2/E3 = kinematic totals 1.9/2.2/2.6 × 9.36e-11,
  converted to g_N,e with each law's own ν (D7b's `gNe_from_total`).
- **Q₂ PASS (Hees 2014, primary):** −3.0e-27 ≤ Q₂ ≤ 9.0e-27 s⁻² at all four E; **FAIL** if outside at all four; else
  **E-DEPENDENT**. Park 2026 (2σ upper 5.2e-27, lower −2.0e-27) reported with the same rule, not graded.
- Tension in Hees σ: (Q₂ − 3e-27)/3e-27.

## SPARC (AG4b's pipeline, reproduced verbatim; per-galaxy Υ profiled)
- CFG4_common.load_sparc, a₀ = CFG4 A0 (9.3603e-11 / 1.1312e-10); per-galaxy MAP Υ_disk under log-normal prior
  N(log 0.5, 0.10 dex), bulge 1.4Υ, s₀ = 0.05 dex, ≥ 5 points (AG4b FROZEN_CRITERIA).
- Primary: AG4b's paired statistic between law X and comparator Y: d_g = rms_g(X) − rms_g(Y), D = median, σ_D from
  10,000 bootstrap resamples (seed 20261020), z_XY = −D/σ_D (z > 0: X fits better).
- Comparators: the five named laws L, Q, M, S, R ("best kernel" = whichever beats X most).
- **SPARC PASS** on a footing iff min over comparators Y of z_XY > −2 (AG4b's "FLIPS" line: X is not disfavoured at ≥ 2σ
  by any record law). **FAIL** iff some comparator gives z_XY ≤ −2.
- Secondary (reported, same −2 line, not graded): AG4b's S1 Σ_g Δχ²_min with its z. If S1 and the primary disagree for a
  law that would decide the outcome, the outcome is reported as **undecided** for that law.
- Power is inherited from AG4b (the n=1 vs n=2 contrast is DIAGNOSTIC at 80 %/90 %); not re-measured here (disclosed).

## Outcome (one of)
- **A law passes both:** some named law or family member passes Q₂ (Hees) AND SPARC on BOTH footings → name it, numbers.
- **No law passes both:** no candidate passes both on both footings → "the unscreened law family and Cassini are in
  tension", quantified per family by (i) the Hees σ of the SPARC-passing members (at their most favourable E) and
  (ii) the worst SPARC z of the Q₂-passing members; the stated N is the smaller of the two over the family.
- **Undecided:** if the passing sets touch a grid edge in a way that leaves the overlap open, or S1 contradicts the
  primary for a deciding member; the reason is stated exactly.

## External-field dependence (reported)
For L (canonical law) on both footings: Q₂ vs total g_e on a log grid g_e/9.36e-11 ∈ [0.05, 30] (121 points); report the
g_e intervals where Q₂ ≤ 9.0e-27 and ≤ 5.2e-27 (bisected edges).

## Checks (script `d7c_q2_rar_gate.py`, `K# PASS value threshold`, exit 0 iff all pass)
- K1: D7b's Q₂ for the canonical law, no turn-off, both footings × E0–E3, reproduced to 1e-6 relative.
- K2: AG4b's primary D and z (n=2 − n=1) reproduced on both footings (|ΔD| ≤ 1e-4 dex, |Δz| ≤ 0.02) and S1 Σ Δχ² to 0.5.
- K3: identities to 1e-12: capacity n=1 ≡ L, n=2 ≡ Q, β=1 ≡ Q, Q ≡ inverse of the α=1 μ = (√(1+4x²)−1)/(2x).
- K4: CFG4 `nu_mono` equals A25's explicit ν_mono splice to 1e-10 on y ∈ [1e-4, 1e4].
- K5: Q₂ convergence: Route-M split 1 vs 2 agree to 5e-3 for M, S, R, n=8, β=6 at E2 canonical.
- K6: analytic limit q = −(16/49)√e_N for ν−1 = 1/y at e_N = 2 to 1e-3.
- MUTATE (`--mutate`): the record's /√D Q₂ transcription bug (as in D7b) → K1 and K6 must FAIL; outputs `*_MUTATE.*`.

## Settings
κ = ½ FITTED; footings never pooled; no dark-matter particle; not theory closed; single thread, nice 10, no downloads.

## AMENDMENT A1 (POST-RESULT, 2026-10-22; the frozen lines above are unchanged)
- K3 first run FAILED (6.0e-11 > 1e-12): the check computed μ_α1 = (√(1+4x²)−1)/(2x), which cancels at small x. The check
  implementation now uses the algebraically identical stable form 2x/(√(1+4x²)+1); tolerance unchanged; it passes at 6.7e-16.
  First-run output kept: `d7c_q2_rar_gate_firstrun.out`, `d7c_q2_rar_gate_results_firstrun.json`.
- K4 FAILS as frozen (3.27e-9 > 1e-10): CFG4's `nu_mono` is a tabulated trapezoid integral (FP1), A25's is the closed-form
  splice; they differ at 3e-9. Kept failed; the script exits 1 for this reason only. It moves no Q₂ or SPARC number visibly.
- The frozen tension metric "Hees σ at the most favourable E" is ill-defined for E-DEPENDENT members (their best cell is
  inside the band). Added: the member's WORST-cell Hees σ (a PASS needs every cell); the family N now uses it. Both are printed.
- Added (reported, not graded): a footing-split reading (members passing Q₂ and the SPARC primary on one footing), and the
  β family's alt-footing E0 cell at β = 4, 6, 10, 20, 40 (beyond the frozen grid) to show the cell's floor.
- The E-field "peak" label is renamed "max on grid" (Q₂ rises monotonically to the grid top).
