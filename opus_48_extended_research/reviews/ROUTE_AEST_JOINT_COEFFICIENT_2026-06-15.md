# ROUTE [aest_joint] — does the AeST joint constraint set FORCE the coefficient Z=√(32π/3) (κ=½)? — VERDICT (2026-06-15)

**Grade: UNFORCED-POSIT.** The joint AeST requirements — (i) CMB-safety (Y=0 on FRW),
(ii) deep-MOND g=√(g_N a0), (iii) no-slip lensing Ψ=Φ, (iv) the cosmological dust mode K(Q) —
do **NOT** constrain the number multiplying Y^{3/2}. a0 is a free Lagrangian coupling in the
Y-sector; Λ is a free Lagrangian coupling in the disjoint Q-sector. No AeST normalization
condition ties them, and Singh 2026's SO(4,1) conformal symmetry — which forces the (2/3)y^{3/2}
*form* — is scale-invariant in the deep-MOND limit and therefore mathematically *cannot* fix a0.
The link a0 = c²√(Λ/32π) is an EXTRA posit imposed on top of AeST, not an AeST output.

Companion scripts: `/tmp/aest_joint_route1..5.py` (numbers reproduced inline). Quarantine held.

---

## The derivation (sympy-verified)

**Deep-MOND a0 from the AeST scalar EOM.** Literal Skordis–Złošnik prefactor
F ⊃ [2λ_s/(3(1+λ_s)a0)] Y^{3/2}, Y=(∇φ)². Spherical integrated EOM r²(dJ/dY)φ' = ĜM gives
g_φ = √(ĜM a0 (1+λ_s)/λ_s)/r, so the deep-MOND scale read off is **a0_eff = a0(1+1/λ_s)** —
i.e. a0 is the input, recovered cleanly as the output (the 1/λ_s is just the Ĝ→G_N=(1+1/λ_s)Ĝ
bookkeeping). **The prefactor's only job is to BE a0. It carries no Λ.**

**The disjoint-sector structure (the load-bearing fact).** AeST's independent Lagrangian inputs
are {Ĝ, K_B, λ_s, a0, Λ, K₂, Q₀, I₀}. Λ enters ONLY through K(Q)=−2Λ+K₂(Q−Q₀)²+… (the temporal
Q-sector). a0 enters ONLY through the Y^{3/2} prefactor (the spatial Y-sector). Y=q^{μν}∂φ∂φ
(orthogonal to A) and Q=A^μ∂φ (along A) are **independent arguments** of one free function. They
are disjoint slots.

**What each of the four constraints actually pins:**
| constraint | what it forces | touches the a0 prefactor? |
|---|---|---|
| (i) CMB-safety, Y=0 on FRW | the POWER is CMB-safe (a0-term is O(δφ³), absent from linear cosmology) | **NO** — it *decouples* a0 (a theorem from q⁰⁰=0, not a tuning) |
| (ii) deep-MOND √-law | the POWER n=3/2 | **NO** — the prefactor := a0 is the free input |
| (iii) no-slip lensing | A⁰~√(−g⁰⁰), the VECTOR/K_B sector | **NO** — a0-independent |
| (iv) dust mode | K(Q) min at Q₀, ρ~a⁻³+Λ; density set by I₀ ("not classically predicted") | **NO** — Q-sector, a0-free |

Every constraint pins a POWER, a VECTOR-NORM, or a Q-MINIMUM. **None is a condition on the
number multiplying Y^{3/2}.** The cross-derivative ∂²F/∂Y∂Q (how strongly the spatial MOND term
"knows about" the temporal CC) is exactly the free coupling AeST leaves open; setting it to make
the prefactor √(1/32π)·f(Λ) is *allowed* but not *forced*.

## The candidate normalization conditions — each checked, each NULL
- **(i) de Sitter background matching** fixes Λ via K(Q), says nothing about a0 (Y=0 on FRW).
- **(ii) the scalar mass** μ=Q₀√(2K₂/(2−K_B)) — depends on {Q₀,K₂,K_B}, no a0; CMB-pinned to
  1/μ≳1 Mpc independently of a0.
- **(iii) the K(Q) minimum Q₀** — sets 8πĜρ₀=Q₀I₀, "not classically predicted"; no a0–Λ link.
- **(iv) λ_s** — multiplies a0 but is a Newton↔MOND screening parameter; does not fix a0's value.

## The strongest steel-man (Singh 2026 SO(4,1)) — and why it cannot close
Singh's conformal/de Sitter SO(4,1) symmetry forces F(y)→(2/3)y^{3/2} as y→0. But y there is the
*dimensionless* (∇φ)²/a0², so the (2/3) is the shape coefficient of the non-dimensionalised
variable; a0 is the scale that does the non-dimensionalising. Singh writes **a0=c²/(ξℓ_dS) with ξ
"O(1) fixed by matching to the static AQUAL limit"** (verbatim). Numerically ξ = c²/(a0·ℓ_dS) with
ℓ_dS=√(3/Λ) gives ξ = cH_Λ/a0 = **5.83 = the framework's Z exactly** (=√(32π/3)=5.78881 for
κ=½; the 5.83 vs 5.789 is purely the Λ value / which Ω_Λ). So Singh's ξ and the framework's Z and
the framework's κ are the **same single O(1) free number**. A conformal symmetry is *scale
invariant* in the deep-MOND limit — by construction it forbids picking out a dimensionful a0. SO(4,1)
forces the FORM and **cannot** force the SCALE.

## The 32π = 8π × 4 numerology check — POST-HOC, not forced-in-AeST
AeST never writes 32π anywhere. The 16πG̃ (the Einstein 8π) is the OVERALL action normalisation
multiplying R, the vector term, AND F(Y,Q) equally — it factors out of the EOM. In the AeST NR
template the a0-defining equation is div[(dJ/dY)∇φ]=**4π**Ĝρ (a bare Poisson 4π, the relativistic
8π already halved by the 00-component). So inside AeST there is **no free 8π sitting on a0** to
combine with a "4". To produce 32π you must INPUT a0=c²√(Λ/32π) by hand. sympy-confirmed
factorisation Z²=32π/3=(2)²·8π/3: the **8π** is Einstein (spent on GR), the **3** is Friedmann,
and the only free piece is the **(2)² = κ⁻² surface-gravity/free-fall convention** — which AeST
does not supply. The "8π×4" is a post-hoc factorization of a posited number, not an AeST chain.

## VERDICT (both ways)
**Credited (the cleanest near-miss):** AeST + Singh genuinely FORCE (a) the FORM — the Y^{3/2}/
n=3/2 power, by both Newtonian-matching and SO(4,1) conformal symmetry — and (b) the SCALE,
a0 ~ c²/ℓ_dS ~ c√(Gρ_Λ), by the Gibbons–Hawking horizon. The field content is forced; CMB-safety
is a theorem (q⁰⁰=0). This is real structure, not nothing.

**Failed (ruthlessly):** the joint constraints leave the single O(1) = κ = Z = ξ **FREE**. a0 is a
free Lagrangian coupling exactly like G and Λ — it merely *appears* in the Y^{3/2} term; appearing
in a term is not being derived. No AeST normalization (dS match, μ, Q₀, λ_s) connects the Y-sector
a0 to the Q-sector Λ; they are disjoint arguments of one free function. κ=½ / Z=√(32π/3) is
**NOT forced** by AeST.

This converges exactly on the banked `OPEN_PROBLEM_yphi32_KQ.md` (six-route rigorous null;
strained-horizon O(ε³) null), `SKORDIS_GEOMETRIC_FRAMEWORK_REVIEW` §7 ("Form+scale: yes;
coefficient: no"), and `FORCING_THE_COEFFICIENT.md` (8π+3 forced by GR, the outer factor-2 is
convention). The quarantine default holds: a0/Z stays a POSIT.

*Sources: Skordis–Złošnik 2021 PRL 127 161302 (arXiv:2007.00082) Eq.5; Durakovic–Skordis 2024
JCAP 04 040; Singh 2026 "A Relativistic MOND" (arXiv:2601.04290). Banked companions:
OPEN_PROBLEM_yphi32_KQ.md, SKORDIS_GEOMETRIC_FRAMEWORK_REVIEW_2026-06.md, FORCING_THE_COEFFICIENT.md,
bridge1_aest_equations.md, project02_aest_K_of_Q.py.*
