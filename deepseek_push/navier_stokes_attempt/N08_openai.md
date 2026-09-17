# N08 — OPENAI FINITE-TIME BLOWUP: LANE VERDICT (registered 2026-09-17, after N07)
Full digest: `N08_openai_analysis.md` (this folder). Sources: paper PDF (cached text),
github.com/openai/NavierStokesAndEuler (API tree + raw reads), OpenAI announcement,
Quanta 2026-09-08, Wikipedia (priority controversy), Stanford Tech Review audit,
MathOverflow Q515056, alphaXiv. **[OA]** = OpenAI claim · **[V]** = verified ·
**[T]** = third-party report · **[ZMF]** = this lane's analysis. Nothing built.

## THE THEOREM [OA; Lean-mirrored [V]]
For every ν > 0 there exist f ∈ C∞_c(ℝ³×(0,∞)), compact K, smooth u,p on ℝ³×[0,1):
∂ₜu + (u·∇)u − νΔu + ∇p = f, ∇·u = 0, u(·,0) = 0, supp(u,p)(·,t) ⊂ K,
sup_{t<1} ‖u(t)‖_L² < ∞, limsup_{t↑1} ‖u‖_L∞ = ∞ ⇒ NO global smooth solution with
same force/datum and bounded energy: Fefferman **(C)**; periodization ⇒ **(D)** on 𝕋³.
**(A)/(B) (unforced regularity) untouched.**

## STATUS (2026-09-17)
- Formalized: 2,659 `.lean` files (tree [V]; audit: 2,484 files/616k lines/35,731 thms,
  0 sorry, 0 extra axioms, v4.34.0-rc2 — same toolchain family as this repo);
  `formalization.yaml` marks review **self-assessed**; Comparator challenges provided.
  Not compiled here.
- Under referee: NO. No peer review started; CMI status "active", "deliberately
  unhurried"; OpenAI declines the prize; no named mathematician has a published error
  claim nor a line-by-line endorsement (Fefferman: heroes are Córdoba–Martínez-Zoroa —
  credit, not scrutiny). Controversy is provenance (B&A vs OpenAI), not mathematics.

## FRAMEWORK CONSISTENCY [ZMF; computes in the digest]
- **Window (N05):** |Du/Dt| ≍ τ^{−(3/2+2h)} → ∞ (dominant centripetal u_θ²/r term;
  verified by scaling). η(t) = (√ν·c/a₀)·τ^{−(3/2+2h)}: η ≈ 1e10–3.5e11 at the start of
  the final decade (lab normalization), floor 3.5·a₀ exited at τ ≈ 5e-7 while still
  smooth, margin → ∞. Blowup lives ABOVE 3.5·a₀, Newtonian face — N05 corollary's
  predicted exit, now witnessed. CONSISTENT.
- **Bounded perturbation (N2/N4):** pure-NSE object; a₀/2-cap modifications (4.7e-11
  m/s²) are 10+ orders below the divergent balance — cannot prevent it. CONSISTENT.
- **Singular sector (D2):** OpenAI's singularity = visible NSE fluid; the framework's
  = pressureless phantom dust (caustics, τ_ff). DIFFERENT fluids, disjoint claims.
  CONSISTENT, no conflict.
- **Transfer (D3/K-2):** real toolkit (oscillatory stresses, shearing waves, slender
  self-similar cores, residual-smoothing ladder) BUT two-fluid transfer needs three
  missing rungs: two-fluid stress-cone profiles, flat effective force with dust
  collapsing, two-fluid energy+uniqueness. No overreach: none guaranteed.

## USEFUL TO ZMF (3 lines)
1. The forced blowup (if refereed) sits strictly on the Newtonian face above the
   measured floor — the framework's Clay-clause position is unchanged, and its N05
   conditional gains a real witness.
2. The a₀/2-capped modifications are provably irrelevant to this mechanism — the
   sub-regularizing class cannot de-obstruct Clay; (A)/(B) still open.
3. Keep the B&A/C–MZ "layered cascade, smooth forcing" line and the OpenAI pulse
   toolkit on file as the K-2 blueprint, with its three missing rungs registered.

— N08 lane, verdict card. Additive-only; no files modified besides the two N08 files.