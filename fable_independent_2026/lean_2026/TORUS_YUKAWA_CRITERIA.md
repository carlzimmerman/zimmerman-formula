# MAGNETIZED-TORUS YUKAWA DOOR — FROZEN CRITERIA (committed before any script)

Setup: T² with periods 1, τ. Left and right fermions with flux M_L = M_R = 3 (3 generations each), Higgs with
flux M_H = 6 (6 zero modes). Zero modes ψ^{j,M}(z) = N e^{iπ M z Im z / Im τ} ϑ[j/M, 0](M z, M τ), normalised
numerically. Yukawa Y_ijk = ∫ ψ_i^{(3)} ψ_j^{(3)} conj(ψ_k^{(6)}) d²z on a grid (no recalled closed formula).
Mass matrix m_ij = Σ_k Y_ijk h_k; lepton masses = singular values; Q = Σm / (Σ√m)².
Sanity gates (must pass first): orthonormality of zero modes to 1e-6; |ψ| periodic under z→z+1, z→z+τ.

PRE-DECLARED natural points (no Wilson lines): τ ∈ {i, e^{2πi/3}} × Higgs h = single mode k ∈ {0..5} or uniform
(1,...,1) → 14 configurations. Report all 14.
 PASS (a real lead): some configuration gives |Q - 0.666661| < 3e-5 with three NON-degenerate masses.
 Also report: m_μ/m_e and m_τ/m_μ at that point (a lead must also be in the right ballpark, within 2×).
 KILL otherwise. Secondary (reported, not a pass): where on τ = i t (t ∈ [0.5, 5]) Q crosses 2/3 for each Higgs
 choice — a crossing at a non-special t is tuning, not derivation.
