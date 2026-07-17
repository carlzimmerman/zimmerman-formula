# The Kernel-Argument Derivation — is the dS–Unruh MI kernel argument BARE or HORIZON-FLOORED, and is it consistent across cosmology and galaxies?

**Date:** 2026-07-17. **Script (exit 0, both a₀ footings, no hard-coded booleans):**
`kernel_argument.py`. **Sources read (frozen read-only repo + local prep, cited inline):**
`mi_field_theory/BASELINE_ACTION.md`, `mi_field_theory/MATTER_COUPLING.md`,
`mi_field_theory/rederive_identity.py`, `mi_closure_pin/PULLBACK.md`,
`mi_fingerprint/KERNEL_THEORY.md`, `mi_linear_cosmology/RESULT.md`.

Framework: Zimmerman **modified-inertia** action
`S_matter = −½∫√−g ρ_m [s uᵘ K(□_u/a₀²) u_μ]`, `K(z)=(√(1+4z)−1)/(2√z)`,
`□_u f = uᵃ∇ₐ(uᵇ∇_b f)`, `s=−1` (postulate). Matter feels the kernel through **its own
4-acceleration** `aᵘ = uᵇ∇_b uᵘ` via `X = |a|²/a₀²` (MATTER_COUPLING.md:24–27). Own
interpolation `ν(y)=√(1+1/y)` (never McGaugh's). `a₀ = cH_Λ/Z = 9.36×10⁻¹¹` (canonical,
ρ_DE) / `1.13×10⁻¹⁰` (alt, ρ_tot/cH₀); `Z=√(32π/3)=5.78881`, so **cH_Λ = Z·a₀ = 5.789 a₀**
(footing-independent — Z is geometric). Both footings carried.

---

## 0. One-line answer

**The same covariant □_u does NOT, by itself, deliver (A) horizon-floored and (B) un-floored.**
Reduced by the **same** closure it gives the **same** answer for both cases:

- **first-moment closure** (the reduction that *produces* the RAR, ring-exact) → argument is
  **BARE** `|a|²/a₀²` for **both** → cosmology **overshoots** (banked σ₈ = 8.5–9.9× Planck),
  galaxies fine;
- **pole / dS–Unruh closure** (the pullback memory pole) → argument is **FLOORED**
  `Z² + (|a|/a₀)²` for **both** → galaxies **die** (deep-MOND boost ν≈10 collapses to ν≈1.09).

The split that the cosmology fork needs (floor A, bare B) is **consistent only if the closure is
frequency-selected**: fast bound orbits (ω/H_Λ ≳ 22) take the first moment → bare; the slow
secular growing mode (ω/H_Λ ~ 1) couples to the dS bath → pole → floored. A genuine frequency
**gap exists** to support this, and the equivalence principle **cleanly** removes H locally in
galaxies (dS tidal / orbital ~ 10⁻⁴). **But the frequency selection is exactly the FREE gap-A
closure that the pullback provably does NOT pin.** So the floor is **physically motivated and not
a blunt manufactured save** — real physics separates the two cases — **yet it is not derived or
forced either.** The cosmological verdict (overshoot vs σ₈=1.02) hangs on this undetermined
closure, plus a second fork (constant H_Λ floor vs rising H(z) floor).

---

## 1. The two closures differ by an additive **Z² = 33.5** floor (§0 of the script)

- BARE argument: `X_bare = (|a|/a₀)²`.
- FLOORED argument (pole): `X_floor = (cκ_eff/a₀)² = Z² + (|a|/a₀)² = 33.50 + (|a|/a₀)²`,
  because `cH_Λ = Z a₀`. Verified symbolically both footings.

`K(33.50 + small) ≈ 1 ⇒ ν ≈ 1` (Newtonian): the floor **switches MI off**. This single fact
governs everything below — the entire question is whether that additive Z² is present.

## 2. (A) Cosmological element — the first moment is BARE, the floor lives only in the POLE

**The covariant first moment does NOT contain the cH_Λ floor.** Computed directly on FLRW
(`ds²=−dt²+a²dx²`, script §1):

- an **exactly comoving** element is geodesic: `|a|² = 0` (not Z², not anything floored). If the
  horizon floor were a first-moment effect this would be Z²·a₀². It is **zero**.
- a **peculiar-velocity** element (constant proper speed V) has `|a|² = γ²V²H²` — the **Hubble-drag**
  acceleration. Numerically `H₀·V ≈ 6.8×10⁻¹³ = 0.007 a₀` (V=300 km/s) — the **same tiny deep-MOND
  order** as the peculiar gravity `a_pec ~ 0.011 a₀`, and **~800× below** the cH_Λ=5.79 a₀ floor.

So the covariant first moment for a growing-mode element is `|a_pec + Hubble-drag|² ~ (0.01 a₀)²` —
**BARE, no Z² floor.** This is why the banked `mi_linear_cosmology` (using the first-moment/peculiar-
acceleration argument) **overshoots**: on the RAR-producing closure the cosmological element is
deep in MOND (ν≈10), driving σ₈ = 8.5–9.9× Planck and bulk flows 8–15× Qin 2021.

**The floor is a separate, nonlocal (spectral) object — the pole (script §2).** From
`PULLBACK.md`, the pulled-back de Sitter Wightman correlator has its memory pole at
`κ_eff = √(H² + (a/c)²) ≥ H_Λ`; in argument units `X_pole = Z² + (|a|/a₀)²`. At `|a|=a₀` the
pole sits 1.48% above H_Λ (`√(1+1/Z²)=1.01481`, both footings — matches PULLBACK PB-D2). The pole
floors because the **de Sitter background curvature is physically present** for a mode referred to
the cosmic frame over horizon scales/timescales (memory time `2c/a₀ ≈ 200 Gyr`). The floored
variant is what lands σ₈ = 1.02 in the banked cosmology — but by making the cosmological element
**nearly Newtonian** (ν_floored ≈ 1.09), i.e. it nearly switches MI off in cosmology by construction.

## 3. (B) Galactic orbit — the equivalence principle removes H locally; BARE survives; a floor would KILL deep-MOND

The galaxy's centre of mass is a **geodesic** of the cosmic frame. In Fermi normal coordinates the
metric is `η + O(R·x²)` with cosmological Riemann `R ~ H_Λ²`, so the only residual cosmological
effect on a star is the **de Sitter tide** `a_tidal ~ H_Λ² r`. Numerically (script §3, r=10 kpc):
`a_tidal ≈ 1.0×10⁻¹⁵ = 1.1×10⁻⁵ a₀`, i.e. `a_tidal/a_orbit ~ 10⁻⁴` (both footings). A galaxy
(10 kpc ≪ curvature radius `c/H_Λ ≈ 4 Gpc`) fits inside **one** local inertial frame; H is gauged
away to 1 part in 10⁴. **Local □_u = flat first moment = BARE |a_orbit|²** → deep-MOND RAR preserved.

**The manufactured-save test (script §3b).** If the cH_Λ floor were applied to galaxies, the
argument `Z² + y²` gives ν_floored ≈ 1.09 at **every** y:

| y = g_bar/a₀ | ν_bare (correct) | ν_floored | boost destroyed |
|---|---|---|---|
| 0.01 | 10.05 | 1.090 | ×9.2 |
| 0.10 | 3.32 | 1.090 | ×3.0 |
| 1.00 | 1.41 | 1.089 | ×1.3 |

The floor **destroys the RAR** (kills the deep-MOND boost). So a floor that fixes σ₈ **is** a
manufactured save **iff it also floors galaxies**. The whole resolution rests on the cosmological
element **not** getting the same local (bare) treatment the galaxy gets.

## 4. The frequency hierarchy — the one variable that can separate (A) from (B) (script §4)

Both first-moment closures floor neither; the pole floors both. What decides *which* reduction
governs is whether the acceleration is **fast** (ω ≫ H_Λ → the 200-Gyr memory kernel averages it,
the AC content passes as pure phase, the **first moment** survives → BARE — this is the exact
mechanism KERNEL_THEORY §2 / PULLBACK §2 use to derive the RAR) or **slow/secular** (ω ~ H_Λ →
couples to the dS bath → **pole** → FLOORED).

| system | ω/H_Λ |
|---|---|
| MW disk (230 Myr) | 479 |
| Fornax dSph (0.5 Gyr) | 220 |
| outer dSph / UDG (2 Gyr) | 55 |
| cluster-galaxy orbit (5 Gyr) | 22 |
| **cosmological growing mode, z≈0** | **~1** (ω ~ H(z), → H_Λ) |

There **is a clean gap**: every bound system sits at ω/H_Λ ≳ 22; the growing mode near z=0 sits at
~1. The frequency hierarchy **can** physically separate the two cases. **Caveat/fork:** at high z
the growing mode has ω ~ H(z) ≫ H_Λ too (z=1 → 2.2, z=3 → 8.0), so a **constant H_Λ** floor only
bites near z=0, whereas a floor **tracking H(z)** (rising into the past) bites at all epochs. This
is the memory's declining-ρ_DE (→cH_Λ) vs rising-cH·E(z) footing fork — the two give materially
different growth histories and both must be carried.

## 5. Consistency verdict — honest, both ways (script §5)

**Does the same covariant □_u realize the local-vs-cosmological split?** Answer: **not on its own.**

- **first-moment closure** (RAR-producing, ring-exact, worldline-general `u·□_u u = −|a|²`) →
  **BARE for both** → cosmology overshoots 8.5×, galaxies OK. Applied consistently, **no floor** —
  and this is the closure that is actually *derived* (D4/D5 in BASELINE_ACTION).
- **pole / dS–Unruh closure** (PULLBACK memory pole) → **FLOORED for both** → galaxies die.

The desired split is **achievable but not forced**: it requires the closure to be
**frequency-selected** (fast bound orbits → first moment/bare; slow secular growing mode →
pole/floored). Three things are true and reported straight:

1. A **real frequency gap exists** (22 vs 1) and the **equivalence principle cleanly removes H
   locally** for galaxies (tidal ~10⁻⁴) — so the floor is **physically motivated**, not a blunt
   number inserted to fix σ₈. The two cases *are* genuinely different physics.
2. The frequency selection **is the FREE gap-A closure** — `PULLBACK.md` PB-D4/PB-P1 proved the
   pullback pole sits ≥ H_Λ for **every** moment weighting and therefore **selects none** (η(β)
   free). The covariant □_u as currently derived does **not** force the growing mode onto the pole
   rather than the first moment. That step is a **physically-reasonable modeling choice inside the
   undetermined closure**, not a theorem.
3. Consequently the cosmological verdict is **bracketed, not settled**:

   | | ν (cosmo element, y≈0.01) | consequence |
   |---|---|---|
   | first-moment / BARE (galactic-consistent) | ν_bare ≈ 9.6–10.6 | σ₈ 8.5–9.9× — **OVERSHOOT** |
   | pole / FLOORED (cH_Λ) | ν_floored ≈ 1.09 | σ₈ ≈ 1.02 — **cured, MI ~off in cosmology** |

   Both footings agree (spread ~15%). Plus the H_Λ-vs-H(z) floor-tracking fork on top.

**Bottom line.** The horizon floor is **not derivable from the same first-moment prescription that
gives the galactic RAR** — that prescription floors neither and overshoots cosmologically. The
floor lives in the **pole** reduction, which is physically available cosmologically (slow secular
mode + real dS curvature) and physically *excluded* galactically (fast orbits + EP-flat local
frame), so the two-sided outcome (cosmology floored, galaxies bare) **is self-consistent** — but
**only** through a frequency-selected closure that sits in the theory's genuinely FREE gap-A. It is
therefore an **honest, physically-grounded resolution that is consistent but not forced**: it does
**not** floor both (galaxies survive), it does **not** manufacture the save by breaking the RAR, and
it does **not** rise to a derivation. The σ₈ question stays **open**, bracketed between the
galactic-consistent BARE overshoot and the dS-bath FLOORED cure, awaiting the unbuilt **covariant MI
perturbation theory** on FLRW (which must compute, not posit, whether the growing mode's secular
acceleration couples to the pole or the first moment) and a resolution of the H_Λ-vs-H(z) fork.

---

*Reproduce:* `cd /Users/carlzimmerman/new_physics/prep_2026/mi_kernel_argument && python3 kernel_argument.py`
(exit 0). Both a₀ footings throughout; `s=−1` and a₀'s value postulated; no "proves"/closed/TOE
claim. The RAR (deep-MOND preserved) is the hard constraint the resolution satisfies; the floor is
reported as physically-motivated-but-free, and the BARE overshoot is reported with equal weight.*
