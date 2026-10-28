# A field equation for the basin rule: the candidate, its requirements, and how to kill it (2026-10-28)

**Status:** a CANDIDATE, not derived and not graded. It is written so that a frozen lane can test it. κ = ½ FITTED. Not
"theory closed". Nothing here says the data favour the framework.

## 1. What any field equation must reproduce

These requirements come from graded lanes.

| # | requirement | source |
|---|---|---|
| R1 | A system carries a cold dark energy halo iff the **gravitational basin** it belongs to passes η(L) Σ_coll(M_basin) > a₀/2πG | BS1 979363d820, CL3 variant (passes every canonical line and the MW) |
| R2 | Satellites carry halos (they sit inside their host's basin) | X51 / X62 / BS1 |
| R3 | KiDS isolated lenses of the MW's mass do **not** (alone in their basin) | CF2 / CL2 / BS1 |
| R4 | The switch must **not** be keyed on potential depth: satellites sit in shallower potentials (\|Φ\|/c² ≈ 4e-8) than the Sun (2.6e-7) | J1 (FAILS); X19 |
| R5 | The cold component is collisionless on cluster scales; a pressure fluid with c_s ≈ 450–500 km/s shocks in the Bullet Cluster | X19 record |
| R6 | It must leave the Solar System and binary pulsars alone | PAPER58 / X15–X16 |

**R4 is the key constraint.** Potential depth, σ and acceleration have all been tried as selectors and failed (J1, X19,
X60). The one quantity that separates "MW in the Local Group" from "isolated KiDS lens" and also includes satellites is
**membership in a collapsed, turned-around region**.

## 2. The observation that points to the field

BS1 did not define the LG basin by mass or by potential. It used the **zero crossing of the radial velocity field**:
R0_data = 795 ± 152 kpc, the radius where peculiar infall cancels the Hubble flow. In fluid language that is the
surface where the coarse-grained **expansion scalar of the matter flow** changes sign:

    θ_R(x) ≡ ∇·v (smoothed on scale R)  =  3H  (Hubble flow)   →   θ_R < 0 inside a turned-around region

**A basin is a connected region with θ_R < 0.** Satellites are inside their host's (R2). An isolated galaxy's
turned-around region holds only its own mass (R3). θ is not the potential, so R4 is respected automatically.

**θ is native to the record's covariant frameworks.** In Einstein-aether, Khronon (v3) and AeST (v4), the vector u^μ
carries the kinetic term c₂(∇_μ u^μ)² = c₂ θ_u². The expansion of the preferred-frame congruence is already a field
of the action. It is not an add-on.

## 3. The candidate action

Let χ be the cold dark energy order parameter. Its condensed phase (χ ≠ 0) is the route-E halo; its uncondensed phase
is the smooth w ≈ 0 component paired with dark energy. Add to the record's AeST/Khronon action:

    S_χ = ∫ d⁴x √−g [ −½ (∇χ)²  −  ½ m²(θ_u, Σ) χ²  −  ¼ λ χ⁴ ]

    m²(θ_u, Σ) = m₀² [ Θ(θ_u) − 1 + s(Σ) ],     Θ(θ) = 1 if θ > 0 (expanding), 0 if θ ≤ 0 (turned around)
    s(Σ)       = (a₀ / 2πG) / (η(L) Σ_coll)                     (the max() rule's ratio)

- **Outside every basin** (θ_u > 0): m² ≥ 0, so χ = 0. Cold dark energy stays smooth and the law (2) is the whole
  story.
- **Inside a turned-around region:** m² = m₀² (s − 1). That is negative, so the field condenses (a symmetry-breaking
  transition), exactly when η Σ_coll > a₀/2πG, i.e. when the second term of the max() wins. The threshold mass T is
  that condition's root, so it is **not a new constant**.
- **Collisionless after condensation:** for m₀ ≫ H and small λ, the condensate behaves as cold, pressureless matter
  (the standard oscillating-scalar result). That satisfies R5, unlike a pressure fluid.
- **Solar System:** the term multiplies χ². With χ = 0 outside basins, and a χ condensate inside the LG basin that
  behaves as Newtonian cold matter, there is no fifth force at O(1). R6 needs the condensate's local density, which is
  route E's halo density, and that is already in the graded mass budget.

**Honest limits of this candidate.**
- The step function Θ(θ_u) and the smoothing scale R are **posited**. A smooth version, e.g. tanh(θ_u/θ_w), adds one
  width.
- s(Σ) is the graded max() rule written as a mass term. It is **not** derived from anything deeper.
- The cold matter-like behaviour is standard for an oscillating scalar. The *timing* of condensation, after turnaround,
  must be checked against structure growth. That is the record's growth-correction lane: particles versus a
  gravitating field.

## 4. What it predicts beyond BS1 (and how to kill it)

| test | candidate's prediction | data |
|---|---|---|
| **K-θ1: basins are flow-defined.** Galaxies inside a measured zero-velocity surface carry halos; just outside, they do not | A sharp change in dynamics across the zero-velocity surface of nearby groups | Cosmicflows-4 / UNGC local flows (UNGC on disk; CF4 needs approval) |
| **K-θ2: timing.** Halos exist only after turnaround, so galaxies falling in for the first time switch late | Backsplash and first-infall dwarfs at the same M★ differ | LG field dwarfs with orbits (Gaia), e.g. Leo T and Phoenix inside R0 |
| **K-θ3: SP2's step.** At fixed M★, basin members lens like route E and isolated ones like the law | Sealed: S_env = 0.48 at 0.3 Mpc | KiDS-Legacy / Euclid environment splits (SP2 568aa930c6) |
| **K-θ4: no potential dependence.** At fixed basin membership, potential depth does not matter | Satellites at 300 kpc and 50 kpc are equally switched | MW/M31 satellites (graded classes) |

**How it dies:**
- (i) the SP2 step fails;
- (ii) the dynamics do not change across zero-velocity surfaces;
- (iii) condensation after turnaround is too late to build the observed cluster halos (a growth check).

## 5. Next lane (proposed, not yet frozen)

**TH1_turnaround_basins.** Recompute every BS1 basin from a measured flow criterion (θ < 0, the zero crossing of the
radial velocity) instead of group-catalogue membership, using UNGC for the Local Volume, and regrade BS1's lines.
- **Pass:** the flow-defined basins reproduce BS1's flags and pass.
- **Fail:** any graded system changes branch in a way the data reject.
- This tests R1 with the field's own variable, not with a catalogue.
