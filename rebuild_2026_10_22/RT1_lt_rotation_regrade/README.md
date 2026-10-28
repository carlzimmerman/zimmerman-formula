# RT1_lt_rotation_regrade: an independent tracer confirms it; the law over-predicts IC 1613 on its HI rotation too

Criteria: `FROZEN_CRITERIA.md` (ac267e8bf1, committed alone, before any Table 2 number was read); no amendment.

**Data.**
- Source: Oh et al. 2015, AJ 149, 180 (LITTLE THINGS), Table 2, parsed directly from the arXiv LaTeX source
  (1502.01281).
- Location: downloaded with the owner's approval to `_external_data/little_things_oh2015/src/` (untracked).
- Tarball sha256: `71af1655…a9d6`.
- VizieR/CDS timed out from this machine.

κ = ½ FITTED. Footings never pooled. Cold dark energy is not matter and not a particle. Not "theory closed". Nothing here
says the data favour the framework.

## Verdict (frozen): **IC 1613 OVER-PREDICTED ON ROTATION** (canonical and alt)

Recipe: g_obs = V_rot(R_max)²/R_max; g_N = G(M★,SED + M_gas)/R_max²; E_rot = log g_obs − log[ν(g_N/a₀) g_N].

| galaxy (LG field) | R_max (kpc) | V_rot (km/s) | log M_b (SED) | E_rot canonical (Z) | E_rot alt (Z) | record (stellar σ, HO3 canonical) |
|---|---|---|---|---|---|---|
| **IC 1613** | 2.71 | 16.9 | 7.94 | **−0.593 (−7.90)** | −0.631 (−8.42) | −0.535 (−6.75) |
| WLM | 3.04 | 37.3 | 7.98 | +0.079 (+1.05) | +0.040 (+0.53) | |
| DDO 210 = Aquarius | 0.31 | 12.0 | 6.30 | −0.077 (−1.03) | −0.115 (−1.53) | |
| DDO 216 = Pegasus dIrr | 1.12 | 18.9 | 7.30 | −0.178 (−2.38) | −0.216 (−2.88) | |

- The kinematic-M★ variant moves IC 1613 by only 0.03 dex (−0.567, Z −7.56).
- **Context (not graded).** The same recipe over all 20 LITTLE THINGS galaxies with an SED mass gives a median E_rot of
  −0.025 (16–84 %: −0.18, +0.32). The recipe carries no large offset, so IC 1613 is an outlier within its own survey.

## Reading

**Two independent tracers agree.** The stellar dispersion at r₁₂ (HO3, −0.54) and the HI rotation at R_max (here,
−0.59) both say IC 1613 pulls about 3.5–4× less than the law predicts from its baryons. LITTLE THINGS' own SED stellar
mass (2.9e7 M☉) is even lower than UNGC's K-band value. So FD1's "data issue" lever (the stellar mass) is now used up:
**IC 1613 is a real law over-prediction, not a stellar-mass artefact.**

**The one remaining data lever is the inclination.**
- Oh+15 fixed i = 48° for IC 1613 (Table 1, error 0.0).
- V_rot scales as 1/sin i. Reaching the law's deep-limit speed (≈ 32 km/s for log M_b 7.94, canonical) would need
  i ≈ 23°.
- IC 1613 is known as a kinematically disturbed, nearly face-on HI system, so a low inclination is possible. But the
  stellar-σ tracer, which needs no inclination, gives the same over-prediction.

**Status.** IC 1613 is a genuine, two-tracer failure of the law (and of route E under BS1). WLM and Aquarius are
consistent; Pegasus dIrr is a mild over-prediction (Z −2.4).

## Checks: 4/4

- **K0:** all 26 Table 2 row names parsed. Each LG dwarf's numbers are echoed with their LaTeX line numbers (IC 1613:
  line 503).
- **K1:** the source sha256 is recorded.
- **K2:** peak RSS 0.05 GB.
- **K3:** V_rot ≤ 3 V_ISO, with R_max read from its own column.
- **Rerun:** the results JSON is byte-identical (`05078851…56a3`).
- **MUTATE twin** (`RT1_MUTATE=1`, R_max read from the R_0.3 column): K3 fails, checks 3/4, exit 1.

**Disclosed:**
- Table 2 gives no error on V_rot(R_max), so σ_E is the frozen 0.15 dex baryonic-mass term alone (0.075 dex). With a
  realistic 10–20 % velocity error, IC 1613's |Z| would fall to about 4–5, still well past 2.
- All baryons are taken inside R_max. That raises g_N, and so the prediction, by an amount that depends on how
  extended the HI is.
