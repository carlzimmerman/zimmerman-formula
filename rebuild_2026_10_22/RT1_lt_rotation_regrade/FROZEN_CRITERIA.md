# RT1_lt_rotation_regrade: FROZEN CRITERIA (committed alone, before any Table 2 number was read)

Written 2026-10-28, after the owner approved: "download the LITTLE THINGS (Oh et al. 2015) rotation curves and stellar
masses for the LG field dwarfs into a fresh _external_data folder, then freeze a regrade before looking at the numbers."

## 0. Data actually obtained

- **The download.** VizieR/CDS (J/AJ/149/180) timed out from this machine. The paper's arXiv source (1502.01281,
  "High-resolution mass models of dwarf galaxies from LITTLE THINGS") was downloaded instead, into
  `_external_data/little_things_oh2015/src/` (untracked). It is a gzip tarball of `ms.tex` and figures.
- **The rotation curves** are given only as figures. Machine-readable curves are not in the source.
- **Table 2** ("Mass modelling results", `\label{MD_results_LT}`) gives per galaxy, among other columns:
  - R_max, the radius of the outermost rotation-curve point;
  - V_rot(R_max), asymmetric-drift corrected, with its error;
  - M_gas;
  - M★ from kinematics;
  - M★ from SED (Zhang+12).
- **The LG field dwarfs in the sample:** IC 1613, WLM, DDO 210 (= Aquarius) and DDO 216 (= Pegasus dIrr).
- **Seen before freezing (disclosed):** the Table 2 column notes, the row names, and, by a filtering mistake, the
  numbers of Table 1 (positions, distances, V_sys, PA, inclination, M_V, SFRs). No graded quantity is in Table 1.
  Table 2's numbers had not been read when this file was committed.

## 1. The test (the owner's question: is IC 1613's law over-prediction a data artefact?)

The record grades IC 1613 with the stellar σ at r₁₂ (HO3: E −0.535, Z −6.75; FD1: −0.305 with UNGC inputs). RT1 regrades
the four LG LITTLE THINGS dwarfs with an **independent tracer**, the HI rotation at R_max.

    g_obs  = V_rot(R_max)² / R_max
    g_N    = G M_b / R_max²,   M_b = M★ + M_gas      (Table 2 totals; all baryons taken inside R_max — disclosed)
    g_pred = ν(g_N/a₀) g_N,    ν(y) = ½ + √(¼ + 1/y)
    E_rot  = log g_obs − log g_pred

- **PRIMARY:** M★ is the SED value. The kinematic M★ is a reported variant.
- **M_gas** is used as published. If Table 2's M_gas excludes helium, the helium factor is applied as Oh+15 define it.
  The script reads the paper's own definition in Section `GAS_DISTRIBUTION` and states it.
- **Distances** are Oh+15's own. The masses and R_max are self-consistent at that distance.
- **Error:**
  - σ_E = √[(2 σ_V/V / ln10)² + (½ · 0.15)²].
  - The second term is a 0.15 dex baryonic-mass uncertainty, propagated at the deep-limit slope ½. It is frozen here
    because Table 2 may not give M★ errors.
  - Z = E_rot / σ_E.
- **The all-baryons-inside-R_max convention** biases g_N **high**. That makes the law's prediction an upper bound in the
  deep regime, which is conservative for an over-prediction verdict.

## 2. Verdict (frozen, canonical primary; alt reported with its own)

| verdict | condition (for IC 1613) |
|---|---|
| **IC 1613 CONSISTENT ON ROTATION** | \|Z\| < 2 |
| **IC 1613 OVER-PREDICTED ON ROTATION** | Z ≤ −2 |
| **IC 1613 UNDER-PREDICTED ON ROTATION** | Z ≥ 2 |

**Reported:**
- the same quantities for WLM, Aquarius and Pegasus, as context;
- the SED and kinematic M★ for all four, against X1's log M★ and UNGC's 0.6 L_K;
- the median E_rot over all 26 LITTLE THINGS galaxies with the same recipe, as context for the recipe's own offset. It
  is not graded.

## 3. Checks and twin

- **K0.** The parser recovers exactly the 26 Table 2 row names in the record listing (CVnIdwA … Haro 36). For each LG
  dwarf, every parsed number is echoed with its LaTeX source line number, so the transcription can be audited.
- **K1.** The source tarball's sha256 is recorded in the results.
- **K2.** Peak RSS < 1 GB.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`RT1_MUTATE=1`, separate outputs).** R_max is read from the wrong column, the next one. A K3 consistency
  check must then fail and the run must exit 1. K3 requires V_rot(R_max) ≤ 3 × V_ISO(R_max), where V_ISO is the
  adjacent column (4).

**Run:** `PYTHONHASHSEED=0 python3 -I rt1_lt_rotation_regrade.py`
