# Item D — the DBI wall in cluster cores: not a fix, a cross-constraint (2026-09-02)

**Question.** Item C and the 09-02 addendum used the quadratic K(Q). v9's action has the DBI form, whose sound speed vanishes at the wall
x = μ_D u/M² = 1 and whose charge n = K′ diverges there. Does saturation concentrate the dust into the 420-kpc core?

**Exact relations (sympy, A1–A3).** c_s² = [u/(Q₀+u)](1 − x²); n = μ_D²u/√(1−x²) (the polytrope's charge times F = 1/√(1−ν²));
in a static well the lapse relation is exact for any K, u = u₀ + Q₀(C−Ψ), so ν = ν₀[1 + (C−Ψ)/h̄] with h̄ = u₀/Q₀ = 4πGρ̄_d/μ_H² =
(43 km s⁻¹)² = 2.0×10⁻⁸ c² at μ_H⁻¹ = 1 Mpc. Galaxy wells: ν ≤ 0.005. Cluster wells: ν ≤ 0.09. The pinned core level C−Ψ ≈ 1.1×10⁻⁴ c²:
ν = 0.12 (window bottom, ν₀ = 2.1×10⁻⁵) to 0.98 (window top, ν₀ = 1.8×10⁻⁴).

**Cluster solve (item C's free-surface solver with the dust term × F(ν)), captured mass normalised to the observed η(R500):**

| ν₀ | window | core yield, raw η = 2.33 | ν_max | core yield, WL η = 1.7 | wall hit |
|---|---|---|---|---|---|
| 0 (quadratic) | — | 20.2% | 0 | 13.8% | no |
| 2.1×10⁻⁵ | in | 20.2% | 0.06 | 13.8% | no |
| 1.0×10⁻⁴ | in | 20.6% | 0.27 | 13.9% | no |
| 1.8×10⁻⁴ | in (top) | 21.6% | 0.49 | 14.3% | no |
| 3.0×10⁻⁴ | out | 25.4% | 0.82 | 15.2% | no |
| 5.0×10⁻⁴ | out | 468% | > 1 | 222% | **yes** |

**Verdict.** Inside the stage-17 window the DBI enhancement adds at most two percentage points and the wall is never reached. Reaching
the residual requires ν₀ ≳ 5×10⁻⁴, above the window's RAR-via-drain edge, and it does so by driving the core into the wall, where c_s → 0
and the density diverges: the EFT exit / core collapse of nbody stage 3, not a closure. The cluster core stays ≥ 65% open. New: the two
fronts are cross-linked — cluster cores independently bound ν₀ ≲ 3–5×10⁻⁴ (no core collapse), consistent with the window. Script
`itemD_dbi_wall_core_2026.py` (6 checks, rc=0; control: the ν₀ = 0 row reproduces item C).
