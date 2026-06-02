# The Surviving Theory — the puzzle assembled, piece by piece

**Date:** 2026-06-02 · *every piece is backed by a runnable check in this repo; the dead
pieces are named explicitly so the boundary is part of the structure.*

This is the whole edifice that survives review, in logical order. Each piece answers the
question the previous one raises. Nothing here depends on the α/mass-ratio numerology or the
Z² = 32π/3 topology — those are **dead** (`reviews/OPUS_PHYSICS_REVIEW.md`), and the puzzle is
built without them. The honest status of every piece is tagged:
**[KNOWN]** established physics, not ours · **[POSIT]** a chosen O(1) input · **[DERIVED]**
follows from the premise · **[DATA]** confronted with measurement · **[OPEN]** a real
calculation not yet done (and not faked).

---

## The spine on one page

```
  (foundation: only the MOND-scaling survives; numerology + Z²-topology are dead)
        │
  1. PREMISE      a0 = cH/Z          MOND scale = cosmic-acceleration scale     [KNOWN+POSIT]
        │  ── if a0 tracks the density literally, then it must evolve ──
  2. EVOLUTION    a0(z) = a0(0)E(z)  coefficient-free (Z cancels)               [DERIVED]
        │  ── confront the only distinctive claim with data ──
  3. DATA         p = 0.80 ± 0.17    ~2σ hint (5σ naive; systematics cut it)    [DATA: weak]
        │  ── does it have a covariant home? ──
  4. ACTION       AeST + a0 = cθ/3Z  θ = ∇·A; evolution becomes a field eqn     [KNOWN+POSIT]
        │  ── does the action deliver a0=cH/Z where the galaxies are? ──
  5. LOCAL        galaxy sees θ≈3H(z) anti-screening, to 1e-6                   [DERIVED]
        │  ── which density does a0 track — Λ or ρ_total? ──
  6. FORK         data lean θ=3H      √ρ_total > √Λ & √ρ_m (~2σ, see Piece 3)   [DATA: weak]
        │  ── does running a0 break the microwave background? ──
  7. CMB          a0 absent at linear order; 2nd-order ~0.01–0.1%              [DERIVED+OPEN]
        │  ── what does the premise force for formed galaxies? ──
  8. CASCADE      one E(z) drives all — but DEEP-MOND targets only             [DERIVED, qualified]
        │  ── the same θ that evolves a0 also sets it locally → ──
  9. EFE          environmental EFE + cosmic evolution = one mechanism          [DERIVED+OPEN]
        │  ── what is left to close? ──
 10. FRONTIER     the open checks collapse to TWO                               [OPEN]
```

---

## 1. The premise — a₀ = cH/Z  **[KNOWN coincidence + POSIT]**

The MOND acceleration scale equals the cosmic acceleration scale:
$$a_0=\tfrac{c}{2}\sqrt{G\rho_c}=\frac{cH}{Z},\qquad Z=2\sqrt{8\pi/3}=5.789.$$
√(8π/3) is exact Friedmann physics; the factor of 2 (hence Z) is a chosen O(1) number.
**Status:** that a₀ ~ cH₀ is a 40-year-old coincidence (Milgrom: a₀≈cH₀/2π; Verlinde). The
*framing* a₀=cH/Z is ours; the coincidence is not. The factor of 2 is **not derived** — Bridge 2
showed thermodynamics fixes the *evolution*, not the coefficient.
*Check:* `schwarzschild_friedmann_core.py`, `bridge2_coefficient_thermodynamics.py`.

**→ raises:** if a₀ is literally set by the density ρ_c, and ρ_c falls as the universe expands,
a₀ cannot be constant. What does it do?

## 2. The evolution — a₀(z) = a₀(0)·E(z)  **[DERIVED, coefficient-free]**

With ρ_c(z) ∝ E(z)², the premise forces
$$a_0(z)=a_0(0)\,E(z),\qquad E(z)=\sqrt{\Omega_m(1+z)^3+\Omega_\Lambda}.$$
**Z cancels in the ratio** a₀(z)/a₀(0) — so this prediction carries *no* free coefficient and
cannot be tuned. **This is the single distinctive, falsifiable claim of the whole framework.**
Everything downstream is its consequence.

**→ raises:** is it true? It is already testable.

## 3. The data — p = 0.80 ± 0.17, but only a ~2σ hint  **[DATA: weak, single-point-driven]**

Fitting a₀(z)=a₀(0)E(z)^p to the local SPARC scale, Vărăşteanu (z≈0.05) and MUSE-DARK (z≈0.9):
**p = 0.80 ± 0.17**, and *naively* constant a₀ (p=0) is rejected at 5.0σ. **A direct attempt to
kill it (`reviews/stresstest_piece3_evolution.py`) cuts that down — honestly:**

- **Jackknife:** drop the single z≈0.9 point and the rejection collapses to **1.2σ**. The only
  measurement carrying a redshift lever arm is MUSE-DARK; the whole "evolution" rides on it.
- **Inter-method systematic:** the two *local* points (1.20 vs 1.69 at essentially the same z)
  disagree at 1.7σ — which a₀ evolution *cannot* explain, so there is a ~0.28 inter-method
  systematic the quoted errors miss. Folding it in drops the constant-a₀ rejection to **~2σ**.
- **ΛCDM-degenerate:** denser high-z halos *and* dispersion-vs-rotation sample selection both push
  apparent a₀ up with z; three heterogeneous points cannot separate that from fundamental a₀(z).

**Status:** the *direction* is real (a₀ at z≈0.9 sits above the local value), but this is a **~2σ
hint, not a detection — the premise is not yet empirically established.** That is the honest leg
the whole chain currently stands on. *Check:* `a0_powerlaw_confrontation.py`,
`reviews/stresstest_piece3_evolution.py`.

**→ raises:** can an evolving a₀ live inside a real relativistic theory, or is it just a fit?

## 4. The action — AeST with a₀ → cθ/(3Z)  **[KNOWN host + POSIT coupling]**

Take AeST (Skordis–Złošnik 2021 — the relativistic MOND that fits the CMB and keeps c_GW=c).
Its MOND scale a₀ is the coefficient of the spatial 𝒴^{3/2} term. The aether already carries a
local scalar, its expansion θ=∇·A. **Promote** a₀ → a₀(θ)=cθ/(3Z). One covariant change, no new
field; on FRW θ=3H, so a₀(z)=cH(z)/Z becomes a **field-equation output**, not a fitted relation.
**Status:** the host theory is established; the θ-coupling and Z are ours and chosen.
*Check:* `reviews/GEOMETRIC_ACTION_theta_coupling.md`, `bridge1_aest_equations.md`.

**→ raises:** the action gives a₀=cH/Z on the cosmic background — but galaxies are *bound*. Do
they actually see 3H, or does local collapse screen θ to zero (which would kill a₀ locally)?

## 5. Local realization — the galaxy sees 3H(z)  **[DERIVED, anti-screening]**

To first order in the weak field, θ = 3H − 3HΨ − 3Φ̇ + ∇·B. In a quasi-static galaxy all three
corrections are negligible (Ψ~10⁻⁶, Φ̇≈0, ∇·B≈0), so the galaxy at epoch z sees **θ ≈ 3H(z) to
~1 part in 10⁶**. The cosmic expansion threads through the bound system; it is **not screened**.
So the coupling delivers a₀=cH(z)/Z exactly where the rotation curves are measured.
*Check:* `reviews/theta_3H_coupling.py` [A,B] (sympy).

**→ raises:** a₀ could track √Λ (de Sitter, constant) or √ρ_total (=H, evolving). Which?

## 6. The fork — the data lean to √ρ_total  **[DATA: weak discriminant]**

| a₀ couples to | p | distance from fit |
|---|:--:|:--:|
| √Λ (de Sitter / Verlinde) — constant | 0 | 4.7σ rejected |
| **θ = 3H ∝ √ρ_total (this coupling)** | 1 | **1.2σ favored** |
| √ρ_matter | 1.5 | 4.1σ rejected |

The evolution **favors the aether-expansion coupling** and disfavors the purely-geometric
de-Sitter origin that emergent-gravity stories most naturally give. (Distances here use the
naive p=0.80±0.17; per Piece 3's stress-test the *effective* significance is ~2σ, not 4–5σ — so
read this as a **weak preference** for p≈1, not a rejection of the alternatives.) *Check:*
`reviews/theta_3H_coupling.py` [D], `reviews/stresstest_piece3_evolution.py`.

**→ raises:** running a₀ to ~20,000× its value at recombination — does that wreck the CMB?

## 7. CMB consistency — linear-safe, second-order scoped  **[DERIVED + OPEN]**

On FRW the spatial 𝒴̄=0 (q⁰⁰=−1+1=0), so the a₀-term is O(δφ³): **absent from every linear
equation.** Peaks do not move (r_s, ℓ_A unchanged), the transfer function is a₀-invariant — and
the θ-dressing doesn't lower the order (θ̄=3H̄≠0). The first a₀-dependent effect is **second
order**, where a₀ is ~2×10⁴ larger; the estimated C_ℓ correction is **~0.01–0.1%** (likely below
Planck's ~0.3–1%, but soft because of the 𝒴^{3/2} non-analyticity). *Check:*
`bridge1_linear_boltzmann.py` (verified vs BBKS/Planck), `reviews/nonlinear_cmb_scoping.py`.

**→ raises:** granting the premise, what is *forced* for the galaxies JWST will measure?

## 8. The consequence cascade — one E(z), but deep-MOND targets only  **[DERIVED, qualified]**

Because v⁴=GM·a₀(z): M_dyn/M⋆ ∝ √E, v & σ ∝ E¼, BTFR/Faber–Jackson zero-point ∝ −log E, sizes ∝
1/√E, Σ ∝ E. **Every channel keys off the *same* E(z)**, and that simultaneous coherence is the
fingerprint no ΛCDM+systematics conspiracy (or sample selection) forges coherently. With Piece 3
weak, **this is now *the* decisive test.** But the red-team (`reviews/redteam_the_puzzle.py`)
adds two hard caveats that *sharpen* it:

- **These are DEEP-MOND scalings** (they need g_bar < a₀(z)). High-z galaxies are compact, and at
  fixed mass g/a₀ ∝ (1+z)^{0.5} — so the compact, massive targets trend **Newtonian**, where the
  boosts vanish. The test must target **extended / low-surface-brightness** high-z galaxies, *not*
  the compact "impossible" ones.
- **de Graaff's M_dyn/M⋆ ≈ 40 is NOT support.** The evolving-a₀ boost for a realistic compact
  JADES galaxy is only ~1.5–3 (an order of magnitude short); reaching 40 needs a ~14 kpc diffuse
  system. If those ratios are real they cut **against** the MOND explanation — earlier drafts that
  cited de Graaff as a hint had the sign backwards.

*Check:* `jwst_full_predictions.py`, `reviews/redteam_the_puzzle.py`.

**→ raises:** the same θ that evolves a₀ also sets it locally — is there a second phenomenology?

## 9. The EFE bonus — evolution and environment, one mechanism  **[DERIVED + OPEN]**

a₀ is set by the local aether expansion θ. Its cosmic part (3H) gives the **redshift evolution**;
its inhomogeneous part (∇·B) is exactly where the **External Field Effect** enters. So a₀ depends
on both epoch *and* environment through one quantity — a structural prediction, not two knobs.
The precise EFE map needs the aether back-reaction solved. *Check:* `reviews/theta_3H_coupling.py`
[B], `mond_first_principles.py` (EFE).

**→ raises:** what is actually left to close the theory?

## 10. The frontier — the open checks collapse to two  **[OPEN]**

At linear order the θ-coupled theory *is* constant-a₀ AeST, inheriting its ghost-freedom, c_GW=c,
and CMB fit. So the second-order CMB, the dressed-term stability, and the non-analyticity are
**one** problem — the 𝒴^{3/2} term at second order around 𝒴=0. The only separate piece is the
**EFE/∇·B** back-reaction. **The frontier is: one nonlinear cosmological calculation, plus the
EFE.** *Check:* `reviews/GEOMETRIC_ACTION_theta_coupling.md`, `reviews/nonlinear_cmb_scoping.py`.

---

## What is NOT in the puzzle (the boundary is part of the structure)

- **α⁻¹ = 4Z²+3 and all the constants** (mass ratios, sin²θ_W=3/13, Ω_Λ=13/19, Koide, CKM/PMNS):
  ~0 bits of evidence — a 34,073-formula search hits an arbitrary O(100) target this well ~20% of
  the time; in real units they miss by 10⁵–10⁶σ. **Dead.** (`reviews/false_discovery_rate.py`.)
- **Z² = 32π/3 from orbifold topology / the η-invariant**: a category/term error (a Euclidean
  ball volume relabeled as a Dirac η-invariant), with an openly-abandoned generation count. **Dead
  as a derivation.** (`reviews/OPUS_PHYSICS_REVIEW.md` §4.)
- **The Standard Model, masses, reionization, the UV luminosity function**: this framework is
  **silent** — they are gas/stellar/linear physics, a₀-independent.

## The puzzle in one sentence

> The acceleration scale that governs galaxies is the cosmic density's own acceleration —
> so it must evolve as E(z); that evolution is a field-equation output of an aether-expansion
> coupling, it survives the linear CMB, it is the coupling the current data *weakly* favor
> (~2σ, single-point-driven), and JWST kinematics will confirm or kill it within a few years.

Everything above is either **[KNOWN]** (inherited), **[POSIT]** (Z, chosen), **[DERIVED]**
(forced by the premise), **[DATA]** (a ~2σ hint, not yet a detection — Piece 3), or **[OPEN]**
(one nonlinear calc + the EFE). There is no numerology load-bearing anywhere in the chain.

But a full red-team (`reviews/redteam_the_puzzle.py`) leaves the **empirical case weak on every
leg**: Piece 3 is ~2σ and single-point-driven; Piece 8's boosts are deep-MOND-only (suppressed
for the compact high-z targets, and de Graaff's M_dyn/M⋆≈40 actually cuts *against* the framework,
not for it); Pieces 1/2/4 rest on a re-dressed coincidence, a chosen density, and a hand-inserted
coupling. What *survives* the attack is the **structure**: the action, and the exact linear
CMB-safety (Piece 7 — δq⁰⁰=0, verified under the harder test). **Honest standing: a coherent,
falsifiable model with no current positive evidence above ~2σ.** JWST can still decide it — but
only on *extended* high-z galaxies, via the cross-channel coherence (Piece 8), not the compact
ones and not the current three-point fit.
