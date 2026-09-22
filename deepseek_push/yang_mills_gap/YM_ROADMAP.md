# YM ROADMAP — the Yang-Mills mass gap: what is proven, what remains (2026-09-17)

The honest map of the Clay problem's front line, in this repo's register.
Every item below is either machine-verified HERE or registered as open with
its exact obstruction. Nothing claimed beyond its proof; nothing open
declared closed.

**2026-09-22 correction to R4:** the original Lean certificates prove scalar
inequalities. The operator comparison is now supplied separately in
[I15 operator proof](../../real_research/reviews/spectral_spine_closure_2026_09_22/i15/PROOF.md).
It proves the original lower bound on a single plaquette and, by applying
Yarotsky's established theorem, a gap uniform in N and open lattice volume
at a finite but numerically unspecified strong-coupling threshold. The
external operator theorem is not Lean-formalized. The original x>=2 bound
is not promoted to arbitrary volume, and no novelty or continuum claim is
made. This correction supersedes the broader R4 wording below in earlier
revisions.

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
| R4 | **Fixed-spacing SU(N), all N>=2: single plaquette and sufficiently strong-coupling open lattice** | **Operator proof; external-theorem application; scalar constants Lean-certified** | Single plaquette: min-max gives Δ>=2x C_F-b_N/x>=gapN(N,x)>=1 for x>=2 and 0<=b_N<=2N. The values 1 and 7/3 are lower bounds, not exact gaps. Full lattice: Yarotsky math-ph/0411042v1, Theorems 1-3, after explicit local normalization, gives Δ>=3x/16 for x>=X_d, with X_d independent of N and volume but not numerically evaluated; canonical infinite-volume physical GNS gap also follows. Proof and boundary/gauge qualifications in the correction link above. |
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

R1–R3 retain their separately recorded scope; this correction does not
re-audit them. R4 now has a specified operator comparison and a checked
application of established strong-coupling mathematics. Neither proves an
identification with the framework's scalar sector. R5/R6 remain open: a
fixed-spacing strong-coupling gap does not establish a continuum theory or
a gap along its weak-coupling scaling trajectory. R7 retains its separately
recorded scope. The exact I15 conclusions and unresolved thresholds are
listed in the linked proof rather than inferred from certificate counts.
