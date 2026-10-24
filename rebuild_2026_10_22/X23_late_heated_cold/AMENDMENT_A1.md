# X23_late_heated_cold: AMENDMENT A1 (coordinator request; committed before the script was ever run, before any number)

**Why.** X22's c_s,need (190.0 / 201.3 km/s) is a LOWER bound set by SPARC. The frozen test grades LHC only at that bound.
A1 adds an overdetermination test: can ONE c_s ≥ c_s,need satisfy, together, at least five constraints? One parameter
against ≥ 5 constraints is a consistency test, not a knob fit; no c_s is adopted.

**Scan.** c_s = c_s,need × {1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 13, 16} per footing, all 4 cells (footings never pooled).

**Normalisation for the scan (stated so that "hot" can escape):** ρ_c(r) = ρ_n exp[∫_r^{r_ta} g dr′/c_s²] with ρ_n set by
the smaller of (i) X22's convention ρ_c(r_ta) = Ω_c ρ_crit,0 (1+z)³ (cosmic mean at turnaround) and (ii) the mass-conserving
fair share M_c(<r_ta) = 5.364 M_b. Where (ii) is smaller this equals the frozen §2 rule; the count of clusters where the cap
binds at c_s,need is printed. If it binds in every cluster at c_s,need, the frozen §3 grading is unchanged by A1. No background
subtraction (as X22 and the peer lane).

**Constraints (allowed set of grid c_s per footing; a constraint holds on a footing only if it holds in both h cells):**
- C-SPARC: c_s ≥ c_s,need (X22's d2 line, by X22's bisection; not recomputed).
- C-GRP: groups, the peer lane's own predictor (`e_pred`, X22's flat-well profile at X19's median group row), copied
  verbatim: |E_obs − E_pred(c_s)| < 2 s.
- C-T1, C-T2, C-T3: X7's MGAS500 terciles (X7 `bins.terciles|<cell>` MID A_CAL, s_CAL), my C\* + LHC model:
  |A_CAL − A_pred(c_s)| ≤ 2 s_CAL. (T1 ≈ none and T2/T3 ≈ +0.27 dex are these rows.) K0 is extended: X7's tercile A_CAL is
  reproduced from n/d to ≤ 1e-9.
- C-KT3: X21's KT terciles, all three |Z_t| ≤ 2.
- C-KTb: X21's KT slope, |Z_slope| ≤ 2.

**Output:** per footing, the allowed grid set of each constraint, their intersection, and the line
**INTERSECTION EMPTY** / **INTERSECTION NON-EMPTY (list)**. Hosted dwarfs remain a reported conflict (both X20 lanes).
The frozen lane verdict (§3) is unchanged; A1's line is reported beside it.
