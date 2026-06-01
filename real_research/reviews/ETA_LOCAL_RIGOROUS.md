# Does η_local(R³/Z₂) = 4π/3? A Rigorous Brüning–Seeley Treatment

**Date:** 2026-05-31
**Question (Carl's):** Start from Brüning–Seeley spectral theory for the Dirac operator
on cones, compute the regularized spectral sum at the R³/Z₂ singularity, and show whether
it equals 4π/3 **without inserting the answer.**

**Answer: it does not. The rigorous local contribution is 0.** The value 4π/3 is the
volume of the unit 3-ball, and it appears only after the Dirac operator D is silently
replaced by |D| — i.e. after the spectral *asymmetry* (what η measures) is replaced by a
mode *count* (what a ball volume measures). Companion script: `reviews/eta_local_bruning_seeley.py`.

---

## Step 1 — Brüning–Seeley cone setup (the framework's own setup, kept)

R³/Z₂ under x ↦ −x is the metric cone C(N) over the link N = S²/antipodal = **RP²**, round.
The Dirac operator on the cone separates radially (Cheeger; Brüning–Seeley 1988):

$$D_C \;=\; \gamma^r\!\left(\partial_r + \frac{n-1}{2r} + \frac{1}{r}\,D_N\right),\qquad n=\dim C=3.$$

The **apex contribution to η is controlled entirely by the spectrum of the link operator
D_N** on RP². This much in `research/OP1_LOCAL_ETA_DERIVATION.md` §2–3 is correct.

## Step 2 — The regularized spectral sum at the singularity

The Brüning–Seeley apex term is a *signed* zeta-regularized sum over the link eigenvalues
{λ} of D_N, schematically

$$\eta_{\text{apex}} \;=\; \tfrac{1}{2}\,\operatorname{FP}_{s\to 0}\sum_{\lambda}\operatorname{sign}(\lambda)\,|\lambda|^{-s}\,(\text{radial Bessel weight}),$$

with genuine contributions only from link modes inside the critical window |λ| < 1 (outside
it the radial operator is limit-point / essentially self-adjoint — no defect, no extension
freedom). The key word is **sign(λ)**: the apex term is a spectral *asymmetry* of the link.

**The link spectrum is ± symmetric.** On round S² the Dirac eigenvalues are ±(k+1),
k ≥ 0, multiplicity 2(k+1). The antipodal map is an isometry that commutes with D, so it
preserves each eigenspace; the Z₂-projection to RP² (Pin⁻) inherits a ± symmetric spectrum.
A signed sum over a ± symmetric spectrum is **0**. Hence

$$\boxed{\;\eta_{\text{apex}}(R^3/\mathbb Z_2) = 0\;}$$

(Numerically confirmed, part C of the script: signed count = 0 over 4,006,002 modes.)

## Step 3 — Does it equal 4π/3? No — and here is exactly where 4π/3 enters

The framework reaches 4π/3 at one identifiable step,
`research/OP1_LOCAL_ETA_DERIVATION.md:165`:

> "But wait — sign(|p|) = +1 for all p ≠ 0!"

and `research/computational_math/eta_invariant_T3Z2.py:199–235`. Setting sign(|p|) = +1
**replaces the Dirac operator D (eigenvalues ±|p|, both signs at every momentum) by |D|
(all +).** The object that results,

$$\tfrac12\!\int \!d^3p\,|p|^{-s}\quad\text{(regularized)},$$

is the zeta-function **mode count**, not the eta function. A regularized mode count over a
ball is, by Weyl's law, proportional to the **volume of the ball**:

$$\underbrace{\int d\Omega}_{4\pi}\;\times\;\underbrace{\int_0^1 r^2\,dr}_{1/3}\;=\;\frac{4\pi}{3}\;=\;\operatorname{vol}(B^3).$$

That is the entire origin of 4π/3. The four "verification methods" in
`eta_invariant_T3Z2.py:245–275` — direct volume, solid-angle×radial, the Γ-function ball
formula π^{3/2}/Γ(5/2), and a Monte-Carlo ball volume — all compute **the volume of the
unit ball four ways.** True, but never in dispute, and not an eta invariant.

The framework's own honest spectral line (`eta_invariant_T3Z2.py:206`) already flags the
mismatch: the actual regularized spectral sum gives **1/(12π²) ≈ 0.0084**, then the script
says *"Wait — this gives 1/(12π²), not 4π/3!"* and substitutes the volume. Note 1/(12π²)
isn't an eta invariant either — it's the same all-positive mode count carried with the
(2π)³ measure (`OP1` §7.4: ζ_D^{<Λ}(0) = Λ³/12π², a pure Weyl volume term). Both numbers
are mode counts; neither is a spectral asymmetry. The asymmetry is 0 (Step 2).

## Two kill shots that need no rationality assumption

Carl correctly noted the "η must be rational" claim is not airtight for cone extensions.
Neither of the following uses it:

1. **Scale invariance.** η is invariant under g → c²g (eigenvalues scale, signs don't), so
   it is a pure scale-free number. "4π/3 = volume of the **unit** ball" is a radius-1
   volume, scaling as c³. A scale-free spectral invariant cannot equal a scale-set volume.
   (The only escape — "treat 4π/3 as the bare number 4.19" — is closed by #2.)
2. **Global consistency.** η(T³/Z₂) = 0, robustly: the flat-torus Dirac spectrum is exactly
   ±2π|n| (± symmetric), and the Z₂ block-swap preserves the pairing (computed in
   `reviews/unfinished_math.py`; the repo's own `SIGNATURE_OPERATOR_DERIVATION.md:18` also
   sets η = 0). In the APS/Cheeger split η = ∫(flat bulk = 0) + Σ₈ η_local, this forces
   **Σ₈ η_local = 0.** Eight identical apex terms summing to 0 ⇒ each is 0. They cannot each
   be +4π/3 (that would give η = 32π/3 ≠ 0, contradicting the direct computation). The
   framework cannot hold both "η_local = 4π/3" and a consistent global η.

## What is genuinely subtle (Carl is right here)

The *exact* value of an isolated RP² cone η, under a non-Friedrichs self-adjoint extension,
is a real research-level question, and a nonzero scale-free trigonometric value is
conceivable in principle. But:
- it would still be a **trig/Dedekind-type number**, never a ball volume, and never tunable
  to land on 4π/3 with that coefficient;
- the **global** constraint (Σ₈ = 0) holds for *any* admissible extension, so it can never
  deliver 32π/3.

## Verdict

The rigorous Brüning–Seeley local contribution for R³/Z₂ is **0**. 4π/3 is vol(B³),
produced by swapping D for |D| (turning η into a mode-count). Therefore
η(T³/Z₂) ≠ 32π/3, and **Z² = 32π/3 is a definition** — the Friedmann factor 8×(4π/3), which
is exactly what the repo's honest documents (`SIGNATURE_OPERATOR_DERIVATION.md:187`,
`T3_INDEX_CALCULATION.md:394`, and the OP-1 confidence table at
`OP1_LOCAL_ETA_DERIVATION.md:297` marking η_local "MEDIUM (heuristic)") already say.

This closes the one derivation the framework most needed to be real. It does not touch the
*forward* predictions (r = 0.0149, the JUNO Δm² ratio, a₀(z)), which remain the only path
that could revive the program — none of which require Z² to be a spectral invariant.
