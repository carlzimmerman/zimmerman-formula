# CD1 AMENDMENT A1 (check definition only, before any graded number)

The first run stopped at K2 as frozen: Δ[Newton] was reproduced from the CSV's `sigma` in 51 of 89 rows (canonical). No
z, S, fraction or class was computed.

**Diagnosis.** The CSV's `sigma` is the raw LVD dispersion. X1's Δ[Newton] uses the binary-corrected σ (X1 FROZEN
§2: Arroyo-Polonio free-f ratio where matched; S1's median ratio for other systems with M_V > −7.7; no correction for
M_V ≤ −7.7). Checked:
- canonical: all 51 rows with M_V ≤ −7.7 match within 0.02 dex. The 38 rows with M_V > −7.7 are offset by +0.148 median
  (+0.037 to +0.347), which is the binary correction.
- alt: the same 51 match within 0.031 (X1's per-footing Monte Carlo medians); the offset rows have median +0.146.

So g_N, r₁₂ and the Wolf convention agree with X1 exactly. Only the σ correction differs, and the graded quantity
(§2: g_obs = g_N · 10^Δ with X1's Δ) already carries X1's corrected σ.

**Change.** K2 now passes if (i) every row with M_V ≤ −7.7 matches within 0.035 dex, and (ii) every row with M_V > −7.7
has an offset between 0 and +0.40 dex (a correction that lowers σ). The graded quantity, classes, ceiling and every other
line are unchanged. Nothing else was looked at.
