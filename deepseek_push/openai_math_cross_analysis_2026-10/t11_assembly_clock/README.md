# T11 — the assembly clock: the historical face of the settling law

**The first PURELY-historical quantitative prediction of the campaign** —
no λ, no a₀, no κ, no cosmology beyond the R500 density-locking. The
settling law (T10 S1) assigns completeness f = 1 − e^{−Γt}; since R500 is
DENSITY-defined (ρ̄(<R500) = 500ρ_crit, identical for clusters and groups
at the same z), the rate Γ is COMMON, and the measured completeness pair
(0.43 clusters X-COP, 0.60 groups) forces the assembly-time ratio with Γ
cancelling exactly:

    t_c / t_g = ln(1 − f_c) / ln(1 − f_g) = ln(57/100)/ln(2/5) = 0.6135

## Results (5/5 checks PASS, rc 0; MUTATE flips C1+C2+C3, rc 1)

| check | content | value |
|---|---|---|
| C1 | exact-ln ratio | **0.6135** (declared 0.6135) |
| C2 | curvature signature: exact 0.6135 < linear-branch 0.7167 | PASS — the exponential-curvature correction is real and testable |
| C3 | second-mode window (Neumann amplitudes, c₂/c₁ = 1/9) | **[0.5577, 0.5926]** ⊂ declared [0.55, 0.66] |
| C4 | density-locking: ρ̄(R500) = 500ρ_crit(z = 0.1) = 4.77e-24 kg/m³; R500 = 0.47 Mpc (1e13) / 2.17 Mpc (1e15) — Planck/X-COP M^{1/3}-consistent | PASS |
| C5 | z-face: t(0.75) = 7.10 Gyr, t(0.15) = 11.92 Gyr, ratio 0.595 | PASS |
| C6 | literature grounding (fetched): 1409.4820 (BCG late-time assembly 2–14%), 2603.19521 (cluster formation z₁₄ ≈ 0.8, BCG identity z ≈ 0.5), 0902.3392 (EDisCS) | **grounded — see verdict** |

## The measured side (verdict registered, one-sided)

The law's window is t_c/t_g ∈ [0.55, 0.66]. The literature's cluster
formation redshift — z₁₄ ≈ 0.8 for present-day massive clusters
(2603.19521, main-branch halo ≥ 1.5e14 M⊙) — gives t(z = 0.8) ≈ 6.6 Gyr;
groups assembled to z ≲ 0.3 give t_g ≈ 11–12 Gyr. Ratio ≈ 0.55–0.62:
**INSIDE the window, near the exact 0.6135**. Current data do not kill
the law's historical face; they land on its prediction.

**Pre-registered kill condition:** a direct assembly-epoch measurement
(BCG/red-sequence archaeology, halo-formation catalogs) with
t_c/t_g < 0.55 or > 0.66 kills the historical face of the settling law.

## The sharp corollary (A4)

Completeness at fixed overdensity is MASS-INDEPENDENT up to assembly
history: a 10¹³ M_b group and a 10¹⁵ M_b cluster at their respective R500
sit on the SAME f(Γt) curve with the SAME Γ. Testable: a completeness
sample split by mass at fixed Δ should show NO mass trend beyond the
epoch trend.

## Corrections to the freeze (dated, on top)

- 2026-10-07: MUTATE C3 declared pair-agnostic was WRONG — the second-mode
  window is pair-dependent (swapped pair → [1.619, 1.619], off-window).
  Corrected declaration: C3 flips with the pair; verified.
- 2026-10-07: KM_MPC unit bug (e19 → e22) fixed — H was 1000× too big;
  C4 now carries physical R500 sanity bounds.
- 2026-10-07: C6's original grounding URLs were junk picks (irrelevant
  arXiv categories); replaced with the three genuine assembly-epoch
  sources listed above.

## Lean certificate (`../lean_certs/cert_assembly_clock.lean`)

`assembly_ratio_from_law`: given the settling law at both epochs with a
common rate Γ (and Γ, t_g ≠ 0), t_c/t_g = ln(1−f_c)/ln(1−f_g) — Γ divides
out exactly. rc 0, zero sorry, axioms = {propext, Classical.choice,
Quot.sound}. Numeric evaluation (0.6135) and the inequality 0.6135 <
0.7167 ride in the lane (house pattern).

## Bottom line

The 0.43-vs-0.60 completeness gap the campaign previously filed as
"needs history, not local product" is now a DERIVED clock reading:
the settling law says the gap IS the assembly-time ratio 0.6135 — and
the current epoch measurements sit on it. The historical face is live
and killable.