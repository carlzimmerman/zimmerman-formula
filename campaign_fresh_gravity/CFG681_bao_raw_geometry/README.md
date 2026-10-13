# CFG681 — BAO from raw distances only (criteria fe91fd3bc; block CFG680–689)

DESI DR2 BAO (arXiv 2503.14738 table) + Pantheon+ STAT+SYS shape (sha256 abf806d9…, outside the repo at
`_external_data/pantheonplus_dr/`). No CMB, no CPL, no ΛCDM model: X(z) = ρ_DE(z)/ρ_DE(0) piecewise-linear, 5 free nodes.

| test | result | frozen verdict |
|---|---|---|
| T1 BAO only: X ≡ 1 vs free X | Δχ² = 7.41 / 5 dof, p = 0.19 (1.3σ) | CONSISTENT WITH CONSTANT |
| T2 BAO + SN shape | Δχ² = 12.08 / 5 dof, p = 0.034 (2.1σ) | HINT |
| T3 D_M/D_H at six tracers, X ≡ 1 | χ² = 5.98 / 5, p = 0.31; largest pull LRG1 +1.85 | X≡1 SHAPE ALLOWED |
| T4 distance duality η ∝ (1+z)^ε | ε = +0.17 ± 0.11 (1.6σ; LRG1, LRG2, LRG3+ELG1, ELG2) | CONSERVED |

**The dark degeneracy decides the a0 question.** With X free, Ω_m runs to the 0.15 floor (X rising to ~7 by z = 2.33 imitates matter).
At fixed Ω_m the data fit equally well (Δχ² ≤ 0.3 between grid points) but the dark energy, and so the owner's tracking a0, differs completely:
| Ω_m (fixed) | T1 χ² free | √X(2.33) = a0(2.33)/a0(0), BAO only | BAO + SN |
|---|---|---|---|
| 0.25 | 3.25 | 1.93 | 1.97 |
| 0.30 | 3.32 | 1.14 | 1.24 |
| 0.35 | 3.41 | 0.00 | 0.00 |
So raw BAO (+SN) cannot say what a0 does at high z without an independent Ω_m. The earlier "a0 declines" results took Ω_m from the CMB
and the shape from CPL; that is where the decline came from, not from BAO.

Disclosed: RUN1 profile grid did not span X = 1 (kept as `cfg681_RUN1_gridbug.*`); RUN2's penalised profile fits still fail at some
grid points (Δχ² ~1e9, band edges on the grid floor), so the √X profile bands printed in `cfg681.out` are NOT used. The fixed-Ω_m grid
above (part of the frozen report) carries the a0 statement. T4 shifts each SN to the tracer z using the T2 best-fit shape (small).
MUTATE: M1 (DESI → its own X≡1 fit) Δχ² = 0.00, T3 χ² = 0.00 ✓; M2 (inject ε = +0.10) recovers ε = +0.272 vs +0.170 + 0.10 ✓.
κ fitted; cold energy mass required; not theory closed.
