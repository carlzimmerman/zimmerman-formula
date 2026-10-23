# DRAFT: canonical correction note on CFG938 (not applied)

**Scope.** This file lives only in this lane. It is for whoever maintains THEORY_CANONICAL. These files are not edited:
- THEORY_CANONICAL_2026-10-18.md: its 2026-10-20 note, lines 173–174, says "well-posed".
- THEORY_CANONICAL_2026-10-21_DRAFT.md: §3.6 line 131 and obligation 9, line 302.

---

**Proposed note (2026-10-2x, CFG961 + WT-02; corrects the 2026-10-20 CFG938 note).**

CFG938's covariant parent of S2 is linearly stable only on static media. That is the case it computed, and it stands: the
dispersion relation, the inertia condition, slip ≤ 1.54e-5 and the law to 2.2e-16.

**On FRW** (WT-02 9b3d77382; independently CFG961, gravity off and full GR):
- The constraint operator h^{μν}∇_μ∇_νχ = ³Δχ − θ u·∂χ turns (χ, λ) into a forward/backward heat pair, and λ becomes χ's
  conjugate momentum.
- The linear Cauchy problem has growing modes, Re σ = c²k²/(3|H|), in both expanding and contracting media.
- **This is physical, not a multiplier artefact:**
  - λ's gradient forces the medium;
  - the Bardeen potential responds;
  - in full GR, when χ̄̇ ≠ 0, the λ equation is implied by the Hamiltonian constraint plus the trace-ij equation.
- **The parent is therefore not a well-posed covariant theory on cosmological backgrounds.**
- The intrinsic-Laplacian repair needs an explicit mean-density subtraction. It is under test in WT-08 (criteria 1bf29e407; no
  committed result).

**c_T is not structurally c.**
- δ(c_T²/c²) = (3/2)L*²[u_⊥² + (u_∥ + ∂₀χ)²]/c⁴.
- The FRW clock ∂₀χ̄ = cΩ_cH/2 (= 0.92 a₀ canonical, 0.77 a₀ alt; independent of the footing) dominates GW170817's path average:
  c_T/c − 1 = 3.9e-19 (L* = 24 pc) to 6.8e-16 (1 kpc).
  - This passes, but caps L* ≲ 1.0 kpc.
  - With the measured source distance instead of the conservative 26 Mpc, the cap is 0.76 kpc.
- If the medium exists early, the tensor kinetic coefficient turns negative before 1 + z ≈ 2.7e5 (1 kpc) to 1.1e7 (24 pc). This is
  the sol61 audit's finding, at a67f9ed9c.

**Hidden clock.** χ̄(t) is a preferred-frame time. A medium moving at v sees u_v = (Ω_cH₀/2)v = 1.1e-3 a₀ at 370 km/s:
- not visible in SPARC, wide binaries or the Solar System;
- undecided against the KiDS tail ends;
- it already enters the medium's inertia (CFG941's a^0.694).

**Effect on the canonical text.**
- §3.6's slip bound stays "conditional on a well-posed parent". It is not upgraded by CFG938.
- Obligation 9 ("the relativistic parent") should list CFG938 as ILL-POSED off static backgrounds, alongside the v3/v4 forms'
  own well-posedness failures (THEORY_V3_DRAFT: H4 for v3 where ρ_τ < 0; I1 for v4 where the aether twists). These are different
  defects in different actions.
- κ = ½ FITTED; not theory closed.
