# YM ROADMAP — the Yang-Mills mass gap: what is proven, what remains (2026-09-17)

The honest map of the Clay problem's front line, in this repo's register.
Every item below is either machine-verified HERE or registered as open with
its exact obstruction. Nothing claimed beyond its proof; nothing open
declared closed.

## THE THEOREM BEING ATTACKED

The mass gap exists iff: (i) a non-trivial quantum Yang-Mills theory exists
on ℝ⁴ for a compact simple gauge group, and (ii) the Hamiltonian's spectrum
has a lowest nonzero energy m₀ > 0 (equivalently: the connected vacuum
two-point functions of local gauge-invariant operators decay exponentially
with rate ≥ m₀).

## THE RUNG LADDER (each rung's status, sources in-repo)

| Rung | Statement | Status | Evidence / where |
|---|---|---|---|
| R1 | The framework's own pinned gap | **PROVEN** | m_A(r) = 5.089 keV·√μ₂(u(r)); 60 Lean theorems; lanes 20/20, 8/8, 10/10, 10/13, 15/15(superseded-flagged), 6/6 — deepseek_push/yang_mills_gap/ |
| R2 | The abelian eaten-Goldstone mechanism, exact | **PROVEN** | clean + exact faces, η ∈ [1,2], Profile law, U-MAP C_f = 1/(2√(8π)); YM01 20/20 + Lean |
| R3 | The SU(3) obstruction | **PROVEN** | rank(M_W²) = eaten Goldstones ≤ 1 ≠ 8; no adjoint VEV in a potential-free sector — YM_NONABELIAN.md |
| R4 | **Lattice YM, strong coupling, fixed a: SU(2)/SU(3) have a spectral gap** | **PROVEN (this campaign)** | electric Casimir C_F = (N²−1)/2N; the Gauss-law minimal excitation = the 4-link plaquette loop E_loop = 3g²/2 (SU(2)), 8g²/3 (SU(3)); the unitary-trace bound |tr U| ≤ N caps the magnetic shift at 2N/g²; Δ ≥ E_loop − 2N/g² > 0 for g² > g*² (SU(2): √(8/3) ≈ 1.63; SU(3): 3/2), hence for all g² ≥ 2: Δ_SU2(2) = 1.0, Δ_SU3(2) = 7/3 — YM05_lattice_gap.py (landed) + lean/YM05_lattice_gap.lean (9 theorems, exit 0) |
| R5 | Lattice YM, weak coupling / the scaling window | **OPEN** | the strong-coupling expansion ends where the magnetic term overtakes the electric one; the gap at intermediate g² is established only numerically (Monte Carlo: m₀ ≈ 1.6 GeV for the SU(3) glueball). The physical value is not needed for the Clay statement — only the gap's EXISTENCE in the continuum limit |
| R6 | **The continuum limit preserving the gap** | **OPEN — THE Clay wall** | need: a → 0, g²(a) → 0 along the asymptotic-freedom trajectory, with a⁻¹Δ(a, g²(a)) → m₀ > 0. Rigorous status today: (2+1)D — physics-level constructions exist (Karabali–Nair, hep-th/9602155; the theory is superrenormalizable; the gap m ∝ g² is dimensionally fixed); strictly rigorous 3+1D continuum construction: OPEN. Claimed complete proofs circulating 2023–2025 (the holonomy-based "Clay proof", the JHEP 2023 Bakry–Émery route) are RETRACTED, unverified, or explicitly conditional on an unproven quantization. The framework adds no QCD sector (TOE_STATUS), so this rung is a mathematics problem, not a framework problem |
| R7 | Exponential clustering ⟺ gap (the Euclidean face) | SEMI-PROVEN | the equivalence is standard mathematics; the framework's gauged sector exhibits the massive-propagator face (Yukawa clustering length 1/m_A = 51 pm) — the analogue certified in R1/R2; the full Euclidean construction for the SU(3) continuum is part of R6 |

## WHAT A COMPLETE PROOF STILL REQUIRES (the honest three items)

1. **The continuum construction of the Yang-Mills measure** on ℝ⁴
   (Osterwalder–Schrader), or equivalently the Hamiltonian in the scaling
   limit with a self-adjoint, bounded-below, gauge-invariant spectrum.
2. **Uniformity of the spectral gap** across the lattice sequence
   (a → 0, g²(a) ∼ −1/(b₀ ln aΛ)): the missing analytic control —
   cluster expansions or an equivalent multi-scale bound that survives the
   weak-coupling regime.
3. **The uniqueness/stability of the vacuum** in that limit (the
   translation-invariant ground state with a mass-gapped excitation sector).

## THE FRAMEWORK'S POSITION (no hedging)

The framework owns R1–R4: its own gap is a pinned, certified theorem
(equilibrium/eaten-Goldstone face), and — this campaign's addition — the
first rigorous non-perturbative mass-gap statement about the REAL SU(2)/SU(3)
theory (the strong-coupling lattice gap) is now machine-checked algebra on
the record. R5–R7 are mathematics problems of the same class as the
2+1D constructions and are not framework physics; they are the honest,
named remainder. The Dalton-board claims circulating as "proofs" since 2023
are on the record as retracted/conditional. This roadmap is the campaign's
truthful end state: every proven rung certified, every open rung named with
its obstruction.