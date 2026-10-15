# ARGON08 — HOW IT FUNCTIONS: the mechanism of the framework, end to end

**Date:** 2026-10-15. **Home:** `argon_push/ARGON08_how_it_functions_2026-10-15/`.
Synthesis of the mechanism from the record (canonical S2, CFG694/696, GF1/GF2, CFG723, CFG793,
ARGON01–07). κ = ½ FITTED; the three constants (κ, supply 5.364, L*) are postulates; everything else
follows. Not theory closed.

## The one-paragraph mechanism

Cold energy is a **stiff, massive, self-gravitating elastic medium** — an aether — whose polarization
field P is *tethered* to the gravitational potential: in equilibrium ∇Φ = KP, so the medium is the
potential's shadow, and its divergence ∇·P = ρ_c is itself mass that gravitates. Baryonic mass polarizes
the medium; the polarization piles up around the mass (the phantom halo); the pile-up deepens the well it
responds to — a feedback loop that **saturates at a₀** (the medium cannot polarize beyond a₀). The
saturation is the MOND law: weak fields get a floor acceleration a₀, strong fields get a tiny correction.
The medium is stiff — it cannot bend on scales below L* ≥ 5.75 pc — so the effect switches on only at
galactic scales (the Solar System is Newtonian). Its ground state is the vacuum energy (ρ_DE = 4a₀²/Gc²);
its quantum is m_native = 2.24 meV; its rest density is 5.364× the baryon density (measured, not derived).
One field, four phenomena: phantom (response), vacuum (ground state), quantum (2.24 meV), stiffness (L*).

## The action and what each term does

    L = −|∇Φ − KP|²/(2K) − ρΦ − W_rem(u) − (γ/2)|∇P|² + (I/2)|∂ₜP|²
        K = 4πG,  W_rem′(u)·K = u²/(a₀−u),  γ = K L*²/2,  c_P² = γ/I,  u = K|P|

| term | role |
|---|---|
| −|∇Φ − KP|²/2K | **the tether.** Vanishes when ∇Φ = KP: the medium's equilibrium is to mirror the potential. Its variation gives ∇²Φ = K∇·P + 4πGρ_b — the cold mass ∇·P sources gravity exactly like baryons. No new force: same Poisson equation, extra source. |
| −ρΦ | ordinary coupling of all energy to the potential (EM energy gravitates — the only photon–P link, CFG793). |
| −W_rem(u) | **the constitutive response.** W_rem′(u) = u²/(K(a₀−u)): a pole at u = a₀ — the medium *cannot* polarize beyond a₀. This saturation IS the MOND interpolation: in the settled state u = g − g_N and the law g_N = g²/(g+a₀) follows. |
| −(γ/2)|∇P|² | **the stiffness.** γ = KL*²/2: the medium resists bending on scales < L*. Screens the phantom at short scales (Newtonian Solar System), kills the portal (E6), kills the lab sphere (ARGON07). |
| +(I/2)|∂ₜP|² | **the inertia.** Waves at c_P = √(γ/I); the W_rem curvature gives a mass gap ω_gap = √(W_rem″/I) ≈ 7.4e-9 rad/s at the local field → 4.3 yr response time; subluminal devices are below the gap → evanescent (ARGON05). |

## The feedback loop (why it saturates)

1. Baryonic mass M_b creates a Newtonian well g_N.
2. The medium responds: u = g − g_N (polarization = the field the baryons are missing).
3. The polarization is mass: ρ_c = ∇·P — the phantom halo M_c(r) = M_b(√(1+4r²/r_M²)−1)/2, r_M = √(GM_b/a₀).
4. The halo deepens the well → more response → more pile-up — **but** W_rem′ → ∞ at u = a₀: the response
   saturates. The settled state is the self-consistent solution of the loop, and it is the law
   g_N = g²/(g+a₀) with the phantom amplitude LOCKED: g_ph = √(GM_b a₀)/r (deep), σ² = √(GM_b a₀)/2 (GF2).
5. The supply rule caps the total: M_c ≤ 5.364 M_b within r_e = 5.84 r_M (measured input).

## The two regimes

- **g ≫ a₀ (strong):** u → a₀ — a constant floor. Newtonian gravity plus a tiny a₀ correction —
  screened anyway by L* at short scales.
- **g ≪ a₀ (deep):** u ≈ √(g_N a₀) — the phantom dominates: g ≈ √(g_N a₀) — flat rotation curves,
  BTFR v⁴ = GM_b a₀, the ESD ΔΣ = √(GM_b a₀)/(4GR) (ARGON02).

## The four phenomena of one field

| phenomenon | what it is | status |
|---|---|---|
| phantom (dark mass) | the medium's saturated response to baryons; T^φ_μν is the dark mass (no particle) | derived from the law |
| vacuum (dark energy) | the medium's ground state: ρ_DE = 4a₀²/Gc² (C₀ = 64πa₀²/α, GF2/ARGON01) | derived, κ fitted |
| quantum | m_native = (ρ_DE ħ³/c³)^{1/4} = 2.24 meV → 542 GHz line (ARGON03) | derived from a₀ |
| stiffness | L* ∈ [5.75 pc, ~1 kpc] — screening length, portal killer, sphere killer | measured, not derived |

## What is postulate and what follows

**Postulates (fitted/measured):** κ = ½ (a₀ = κc√(Gρ_Λ)); the constitutive pole at a₀ (the interpolation
function's form); the supply ratio 5.364 (Ω_c/Ω_b); L* ∈ [5.75 pc, ~1 kpc]; the minimal metric coupling.

**Follows (derived, machine-checked):** the phantom profile and its locked amplitude; the BTFR; the ESD
curve and its break at 5.84 r_M; ρ_DE from the static closure; the native quantum mass and the 542 GHz
line; the evanescence below the gap; the E6 consistency (portal invisible iff L* ≳ 2.3 km); the
rest-mass conservation theorem (no term of the action converts cold mass).

## The honest gaps (the three numbers that would complete "how it functions")

1. **Why a₀?** The pole position is input. κ = ½ is FITTED — every local derivation route is closed
   (ARGON01); only global/sequestering structure remains.
2. **Why 5.364?** The medium's rest density is measured, not derived (16/3 near-miss = non-claim).
3. **Why L*?** Bounded [5.75 pc, ~1 kpc], not derived — but it is now doing real work: one constant
   closes the portal (14 orders) and the sphere (1e-34 screening).

**Verdict: the framework functions — the mechanism is coherent, self-consistent, and every derived
consequence is on the record with a kill condition. What remains is the origin of its three constants,
not the machinery.**