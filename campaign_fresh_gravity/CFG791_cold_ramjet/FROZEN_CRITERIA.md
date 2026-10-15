# CFG791 FROZEN CRITERIA: the hypothetical cold-energy photon ramjet. Relativistic acceleration and mission times

Committed alone, before any script. 2026-10-15. Block CFG790–799. Owner: "yeah this is best". HYPOTHETICAL: it assumes a
portal that converts intercepted cold energy to light with efficiency η. No such portal is derived (CFG789/790).

## Model (exact relativistic momentum bookkeeping)
- The craft has fixed rest mass M (all converted mass leaves as light) and intake area A ⊥ motion.
- Cold energy is at rest in the Galaxy with density ρ = 0.01 M☉ pc⁻³. The craft starts at v₀ = 230 km/s relative to it.
- Unconverted cold energy passes through untouched (collisionless), so it adds no drag.
- In the craft frame, converted rest mass arrives at dm′/dτ = η ρ A γ v, carrying momentum −γv per unit rest mass. Its full
  energy γc² is re-emitted backward as light, carrying momentum +γc.
- Proper force F′ = η ρ A γ² v (c − v). Proper acceleration α = F′/M = (η ρ A c²/M) β/(1 + β).
- Rapidity: dφ/dτ = α/c, with β = tanh φ. Galaxy time: dt = γ dτ.
- Limits:
  - low β: exponential, e-fold time τ₀ = M/(η ρ A c);
  - high β: α → η ρ A c²/(2M), constant.
- Intake power (craft frame): P = η ρ A γ² v c².

## Designs (declared)
- D1: M 100 kg, A 100 km² (areal density 1 g m⁻², sail-like).
- D2: M 1 t, A 1 km².
- D3: M 10 t, A 10⁴ km².
- Each at η = 1, 0.1, 0.01.

## Outputs per design and η
- τ₀ (days).
- Proper and Galaxy time to β = 0.1, 0.5, 0.9.
- Asymptotic proper acceleration.
- Galaxy time and proper time to cover 4.37 ly (α Cen) from rest-relative start.
- Intake power at β = 0.1.

## Controls
- K1: low-β numerical τ₀ matches M/(η ρ A c) to 1e-3.
- K2: the high-β numerical proper acceleration matches η ρ A c²/(2M) to 1e-3 at β = 0.999.
- K3: energy check. Craft-frame intake power equals emitted light power (rest mass constant), within 1e-12.
- MUTATE (CFG791_MUTATE=1): treat drag as if the unconverted cold energy were absorbed too, with η = 0.1. Acceleration
  must fall (drag present). This demonstrates that the collisionless pass-through matters.

## Hand estimate
- D1 η = 1: τ₀ ≈ 57 days; β = 0.1 in about 1 yr; asymptotic α ≈ 3 g; α Cen in a few years of proper time.
- Lower η scales the times by 1/η.

κ fitted; not theory closed. A hypothetical design study, not a claim that the drive exists.
