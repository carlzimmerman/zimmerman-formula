# The cold-energy formula as of 2026-10-13 (both chats consolidated)

For the owner. Every term carries its status: DERIVED (from an action or theorem on the record), FORCED (by data with a committed
lane), FITTED (a constant set from data), INPUT (an axiom), or OPEN. κ = ½ is fitted; footings are never pooled; the cold energy's
mass is required; no particle species; not "theory closed"; nothing here says the data favour the framework.

## 0. Inputs

| symbol | value | status |
|---|---|---|
| a₀ | κ c √(G ρ_DE), κ = ½; tracks ρ_DE(z) | FITTED (κ); INPUT (the tie to ρ_DE) |
| Ω_c/Ω_b | 5.364 (cosmic amount of cold energy) | INPUT |
| k | ≈ 2.9–3.6 (retention per unit hot-gas mass) | FITTED on X-COP (CFG745) |
| L* | ≥ 5.75 pc (stiffness length) | FITTED / bounded (CFG691) |

## 1. The full mass budget of a bound system

**M_total(<r) = M_b(<r) + M_settled(<r) + C(<r)**

**(a) Settled cold energy, the galaxy law.** Static form (all systems):

M_settled(<r) = [ν(g_N/a₀) − 1] · M_b(<r),  g_N = G M_b(<r)/r², each system's **own** baryons (no external-field effect).

- Kernel: ν_s(y) = ½ + √(¼ + 1/y), the static law of the one-action construction (CFG695; raw SPARC rms 0.1009 / 0.0994). The
  record's ν_mono = 1/(1 − e^(−√y)) fits the same (0.1003). Either is FORCED by SPARC at that level; neither is derived from first
  principles of known physics.
- **As an action (the other chat's C\*, CFG692–695):** cold energy is the bound charge ∇·P of a vacuum polarization field,
  L = −|∇Φ|²/8πG − (ρ_b + ∇·P)Φ − W(P) − (γ/2)|∇P|² + (I/2)|Ṗ|²,  W(u) = −(a₀/4πG)[u + a₀ ln(1 − u/a₀)].
  Critical quadratic (no mass term of its own), saturation at a₀, stiffness γ screens the Solar System (L* ≥ 5.75 pc). Passes EFE gates,
  SPARC, cluster shear (CFG658). Its consistency with the forced properties below is **DERIVED** inside the construction; the
  construction itself is a postulated action (R0-shaped).
- Supply edge: the settled mass stops where the system's share of cold energy runs out (R2).

**(b) Retained collisionless cold energy, the state-dependent term (CFG745):**

C = k · M_hot  (hot, X-ray-phase gas), collisionless, retained at formation, so it moves with the galaxies (Bullet-safe).

- Galaxies (f_hot ≈ 0): C ≈ 0. Groups (f_hot ≈ 0.08): small (TENSION at one end). Clusters (f_hot ≈ 0.9): ≈ 3 M_b (X-COP by construction).
- Supplies the massive early types' shortfall if they hold M_hot ≈ 0.17–0.25 M* inside 100 kpc: **SEALED prediction CFG746**
  (hash 79140240…), decided by SZ / X-ray mass profiles.
- Status: **FITTED (k), no mechanism.** It is consistent with this chat's raw-lensing results: the early-type excess is real at matched
  near-IR mass (CFG669, ×1.9), not an age effect (CFG667), survives isolation (CFG96), and rises continuously with colour (CFG721).

**(c) Outside bound systems:** cold energy is ordinary cold matter with Ω_c/Ω_b = 5.364 (CMB, growth).

## 2. Dynamics

- **Settling toward (a)** (class A + FIX-2 + gate, CFG541/544/639; fluid form CFG638): drift v_s = −α 𝔊 τ∇ψ, ∇²ψ = 4πG(ρ_target − ρ_c),
  τ = (4πGρ)^(−1/2), gate 𝔊 = 1 only where cold energy is missing; Jeans relaxation at rate α/τ; released energy to dark energy
  (Q = αρ_cτ𝔊∇ψ·∇Φ, a 10⁻⁶ trickle). As a fluid: Israel–Stewart, Re ≈ 4α.
- **Or, in C\*:** the field responds with an inertia-set time t_resp. **CFG720 (queued)** measures the t_resp window that the Bullet + Harvey
  data allow; instant response is the excluded α = ∞ class.
- α / t_resp: **OPEN** (galaxies want settling; mergers want little or none; with the gate α = 0.1 is unscored, not excluded).

## 3. What is forced, what is not

| property | status | lane |
|---|---|---|
| the extra pull is real gravitating mass that lenses like dynamics | FORCED | CFG663 |
| no external-field effect (each system's own baryons) | FORCED | PAPER44 |
| the profile is not a local equilibrium of the cold energy's own stress | DERIVED (no-go) | CFG660, CFG661 |
| the profile is the static response of a stiff, saturating polarization (C\*) | CONSTRUCTION, passes galaxies / EFE / cluster shear | CFG658, CFG692–695 |
| the hot-gas-proportional retained term C = k M_hot | FITTED, consistent, prediction sealed | CFG745, CFG746 |
| why ν has its shape, why a₀ = κ c √(Gρ_DE), why k ≈ 3 | **OPEN** (no known physics passes the selector spec) | MECHANISM_JOINT §6–7 |
| merger response of C\* | **PENDING** | CFG720 |

## 4. The formula in one line

**M_total(<r) = ν(g_N/a₀)·M_b(<r) + k·M_hot(<r)**, with ν from a saturating vacuum polarization (C\*), a₀ = ½ c √(Gρ_DE), k ≈ 3, each system
reading only its own baryons; cold matter with Ω_c/Ω_b = 5.364 everywhere else.

Two constants are fitted (κ, k), one is bounded (L*), and the selector's physics is open. The decisive near-term tests are CFG720
(mergers) and CFG746's sealed hot-gas prediction (SZ / X-ray stacks of log M* ≈ 10.8 quiescent galaxies).
