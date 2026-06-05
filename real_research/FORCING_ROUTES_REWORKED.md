# Trying All the Forcing/Construction Routes Again — A Fresh Honest Pass

**C. Zimmerman, June 2026.** *After the anharmonic framing (`ANHARMONIC_AND_32PI.md`), I re-attempted every open
route to **force** the coefficient Z = 2√(8π/3) (equivalently 32π) or **construct** the framework from a deeper
theory — not cataloging them, actually working them. Four routes, four scripts, all verified. The honest result:
no route forces the coefficient, one route surfaced a genuine **correction** to the just-written 32π decomposition,
and there is now a clear **structural reason** the coefficient cannot be forced by symmetry. Each verdict was
independently re-checked by hand before being recorded (the surface-gravity correction below was caught exactly this
way).*

---

## The four re-attempts

| # | Route (the unworked thing) | Script | Verdict |
|---|---|---|---|
| 1 | **AeST cross-coupling** — build a non-separable ℱ(𝒴,𝒬) that *forces* a₀ = c²√(Λ/32π) instead of inserting it | `reviews/project_aest_crosscoupling.py` | 🟡 **INSERTED, not forced** |
| 2 | **Entanglement volume coefficient** — extract a₀ *and its number* from the dS volume-law in Jacobson's equilibrium | `reviews/project_entanglement_volume_coefficient.py` | 🟡 **Lands at 6, not 32π/3** |
| 3 | **Anharmonic normalization** — is the 8π→32π factor-4 *forced* by a normalization principle? | `reviews/project_anharmonic_normalization_force.py` | 🔴 **CONVENTION — and a correction (below)** |
| 4 | **Heat-kernel longshot** — does the floor/Einstein ratio for the conformal (SO(4,1)) scalar on dS₄ force 32π/3? | `reviews/project_heatkernel_longshot.py` | 🔴 **NO — degenerate / regulator-dependent** |

### 1. AeST cross-coupling → INSERTED
A non-separable ℱ(𝒴,𝒬) = 𝒦(𝒬) + C·(−𝒦(𝒬))^p·𝒴^{3/2} *can* reproduce a₀ = c²√(Λ/32π) — but the welding is a free
choice, not a consequence. The only Λ-free ("forced-looking") exponent p = −½ requires (−𝒦)^{−1/2}, which goes
**imaginary/singular where 𝒦(𝒬) crosses zero on the cosmological background** (a ghost/hyperbolicity violation,
verified). The ghost-*safe* branch carries a bare 1/Λ in its coupling — manifest hand-tuning. None of shift symmetry,
scale invariance, or c_GW = c selects the welding. So AeST hosts the relation perfectly (CMB-safe, GW170817-safe) but
**does not force it** — exactly the zoo's universal verdict (every covariant MOND theory inserts a₀), now confirmed
for the specific welding construction.

### 2. Entanglement volume coefficient → 6, not 32π/3
Rebuilding Jacobson's causal-diamond variation from the metric (not asserting Verlinde's answer) and inserting the de
Sitter volume-law term: the volume entropy overtakes the area entropy at **δS_V/δS_A = ℓ/L exactly** → crossover at
the de Sitter radius → the **scale** a₀ ~ cH is genuinely forced. But the bare crossover carries coefficient **1**, and
the number multiplying it is the d=3 strain/volume factor d(d−1)|₃ = **6** (Verlinde's value; the thermal route gives
the neighboring 2π). **It is not 32π/3 = 33.51.** Decisively: 32π/3 appears *only* as a tautology of the definition
a₀ = c²√(Λ/32π) with Λ = 3H²/c² fed in — it is **never an output** of the variation. And extracting any a₀ requires
**relaxing Jacobson's fixed-volume constraint** (Verlinde's dynamical-volume move) — a real modification. So the route
derives the scale and lands the coefficient in the geometric O(1)~6 cluster, but **does not force 32π/3.**

### 3. Anharmonic normalization → CONVENTION (and a correction to my own just-written decomposition)
The question: is the factor-4 separating Blanchet's 8π floor from the framework's 32π *forced*? Worked with every
factor carried explicitly, the answer is **no — it is a convention** — and the analysis exposed a **mis-attribution in
the 32π decomposition I had just committed.** The honest picture:

- a₀ = (prefactor) × c√(Gρ_Λ) with ρ_Λ = Λc²/8πG. **Prefactor 1 → Λc⁴/a₀² = 8π** (Blanchet's floor); **prefactor ½ →
  Λc⁴/a₀² = 32π** (the framework). The "4" is (1/½)² — that single unforced prefactor, squared.
- The **8π is genuinely forced** (the Einstein coupling, entering via ρ_Λ) — Blanchet and the framework share it.
- **The correction:** I had written "the 4 = (surface-gravity 2)², from κ = c²/2R." **That is wrong.** Using the
  actual de Sitter surface gravity κ = c²/2R as the acceleration gives **Λc⁴/κ² = 12**, not 32π (verified by hand and
  in-script). The ½ that really produces 32π is the **free-fall/kinematic prefactor** in a₀ = (c/2)√(Gρ_Λ) — a
  *different* ½ from the surface-gravity one, and a convention (the forcing analysis already classified the outer
  factor-2 as convention). `ANHARMONIC_AND_32PI.md` and `reviews/project_anharmonic_32pi.py` are corrected accordingly.

So 32π = 4 × 8π is **8π (forced Einstein coupling) × 4 (free-fall-prefactor convention)** — *not* an upgrade from
route-forced to forced, and the clean "surface-gravity 2²" story does not survive a direct check.

### 4. Heat-kernel longshot → NO (the one route the completeness sweep flagged)
The completeness critic surfaced exactly one unworked route with any forcing chance: the spectral-action /
induced-gravity ratio of the floor (induced Λ) term to the Einstein (induced 1/G) term, for the **conformally-coupled
scalar** (whose SO(4,1) symmetry *is* deep-MOND), on dS₄ — because that ratio is the same *kind* of object as
32π = Λc⁴/a₀². Worked with the standard Gilkey–Seeley–DeWitt coefficients (no imported volume — guarding against a
prior retracted attempt that got 32π/3 only by hard-coding a unit-ball 4π/3):
- a₀ density (floor) = tr(1); a₂ density (Einstein) = (1/6 − ξ)R.
- **For the conformal coupling ξ = 1/6, a₂ ≡ 0** — the symmetric field induces *no* Einstein term at this order, so the
  floor/Einstein ratio is **degenerate (∞)**, not 32π/3.
- For ξ ≠ 1/6 the ratio ∝ 1/(1/6 − ξ) × (regulator cutoff-moment ratio f₀/f₂) — it **rides on a free parameter and the
  regulator**, so it is not a forced pure number either.

This is the **sharp form of the obstruction**: a₀ (hence 32π) is the *scale at which deep-MOND conformal symmetry
breaks*, and **symmetry fixes the cubic *form* but provably never the breaking *scale*.** No unworked forcing route
remains.

---

## The meta-verdict — as closed as honesty allows

The coefficient-forcing question now rests on **four independent worked negatives**, not one:

1. **DSSYK** (the make-or-break): computed to fail — forces Z → ∞ in the physical limit.
2. **AeST construction**: the welding can only be inserted (ghost-freedom kills the forced-looking form).
3. **Entanglement variation**: outputs 6, never 32π/3 (which is definitional, not derived).
4. **Heat-kernel / spectral**: degenerate for the symmetric field, regulator-dependent otherwise.

…and behind all four, a **structural reason**: the coefficient is a *symmetry-breaking scale*, and no symmetry fixes
the scale that breaks it. So the standing verdict is now **robustly** established, not provisional:

> **Z = 2√(8π/3) is GR-traceable — the 8π (Einstein coupling) and the 3 (Friedmann) are forced — and *route-forced*
> in its remaining factor (the free-fall-prefactor 4, a convention, *not* surface gravity). It is NOT uniquely forced,
> and four worked routes plus one structural argument now say it cannot be, short of a new principle no one has.**

What this pass did *not* do (the honest residue, unchanged): it did not force the coefficient, and it did not touch
the *value* of Λ (the cosmological-constant problem). What it did do: it converted "reproduced, not forced" from a
single-route statement into a four-route-plus-structural conclusion, it confirmed the two buildable homes (AeST,
entanglement) **host/reproduce but do not force**, it closed the one remaining longshot (heat-kernel) as a clean
negative, and it **caught and corrected a real mis-attribution** in the freshly-written 32π decomposition (surface
gravity → free-fall prefactor; κ gives 12). No route manufactured a win; the one tempting "upgrade" (the factor-4
forcing) was tested and honestly returned to convention.

---

## The mechanism-class closure — even bound-saturation doesn't force it

The structural reason ("symmetry fixes the cubic *form* but never the breaking *scale*") closes the *symmetry*
routes — but symmetry is only **one of the three ways physics fixes a scale or a dimensionless coefficient**. A
*bound* and a *dynamically generated scale* are not symmetries, so they could in principle evade the obstruction.
Both are now checked (`reviews/project_maxforce_minaccel.py`):

| mechanism class | how it fixes a scale | does it force 32π? |
|---|---|---|
| **(1) Symmetry** | a symmetry forces the *form* of the term | 🔴 No — fixes |∇φ|³, never the breaking scale (structural) |
| **(2) Bound saturation** | max force F=c⁴/4G, min accel, horizon surface gravity | 🔴 No — gives cH/a₀ = **1–2** (the kinematic cluster), Λc⁴/a₀² = 3 or 12; never 5.79/32π |
| **(3) Dimensional transmutation** | a dimensionless coupling + RG running → a scale | 🔴 No — would give exp(−1/bg), a *tuned transcendental*; and there is no a₀ running coupling anyway |

The bound-saturation result is the sharpest new datum: every bound (naive horizon c²/L, de Sitter surface gravity
c²/2L, maximum force over the Hubble mass, Unruh = de Sitter temperature) lands a₀ at **cH/a₀ ≈ 1–2** — a *different,
lower* O(1) cluster than the density/thermal routes (~6). So the coefficient spread across mechanisms is wider than
the 5.79–6.28 previously emphasized: it runs **1 → 12** (Λc⁴/a₀²: kinematic 3–12, density/thermal ~100), and the
framework's specific 5.789 comes **only** from the density factor √(3/8π) of the Friedmann route. No bound, and no
symmetry, and no transmutation selects it.

**So the closure is now complete across all three mechanism classes.** The *scale* a₀ ~ cH is **over-determined** —
every mechanism reproduces it, which is real physics and explains why the Milgrom coincidence is so robust. The
*coefficient* is fixed by **none** of them. That is the final, honest shape of the question: **Z is GR-traceable and
route-forced, not uniquely forced — and there is now no remaining class of scale-fixing mechanism that could force
it, short of a genuinely new principle.** The action therefore moves off the coefficient (closed) and onto the two
things that can still decide the framework: the *empirical* test of a₀(z) ∝ H(z) (its one distinctive falsifiable
signature), and the *value* of Λ (the cosmological-constant problem, owed by everyone).
