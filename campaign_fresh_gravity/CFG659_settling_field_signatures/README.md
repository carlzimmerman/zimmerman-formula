# CFG659: does the settling field P leave a signature in ordinary matter or light?

**Label: NO VISIBLE SIGNATURE FROM P.** Every matter channel is BELOW THRESHOLD at the worst corner of the window. Light needs
a new coupling (none added). The one channel that comes close is the double pulsar, at 4.2e-2 of the room it allows. It
constrains the unfixed wave speed: c_P > 1.7e-3 c at L* = 5.75 pc.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (75e95fe06), 2026-10-13.
- **Script:** `cfg659.py`, one process, about 20 s, exit 0 → `cfg659.out`, `cfg659_results.json`.
  - `CFG659_MUTATE=1` sets the P–Φ coupling λ to 0. Every channel comes out exactly 0 (exit 0 = control PASS) →
    `cfg659_MUTATE.out`, `cfg659_results_MUTATE.json`.
  - It reads CFG630's JSON. CFG690–699 are read only; nothing there is imported or edited. Nothing is downloaded.
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory
  closed"; no ΛCDM or standard-MOND yardstick in any verdict.
- **Window:** L* ∈ {5.75, 100, 1000} pc; c_P ∈ {5e-3, 1.5e-2, 0.1, 1} c. The worst corner decides each verdict.

## Coupling (D1–D3, D5)
Action: L = −|∇Φ − 4πG P|²/8πG − ρ_bΦ − W(P) − (γ/2)|∇P|² + (I/2)|Ṗ|², with γ = 2πG L*² and c_P = √(γ/I).

1. **How matter feels P.**
   - Varying Φ gives ∇·(∇Φ − 4πG P) = 4πGρ_b, so **g = g_N − 4πG P_L**. This is checked spectrally in 3-D to machine
     precision.
   - Matter feels P only through Φ: the coupling is universal and gravitational.
   - A passing longitudinal wave gives every body δa = −4πG δP_L.
   - Transverse P never enters Φ.
2. **Light.** The action has **no term with A_μ or F_μν**. A direct P–light coupling would be a new term (a knob), so none is
   added. Light can see P only through the metric potentials, and Ψ = Φ (the relativistic completion) is open.
3. **Waves.**
   - **Longitudinal waves** satisfy Iω² = γ(k² + m²), with m² = 2w″(u₀)/L*². The coupling term is independent of P_L, so it
     gives them no mass; the gap comes from W″ about the local background u₀.
   - The gap is m² = 4u₀/(a₀L*²) where u₀ ≪ a₀. In saturated regions (g ≫ a₀) it is m ≈ √2 g/(a₀L*). Inside a star's
     screened core it is about 0.
   - **Transverse modes** are massive (4πG/I) and do not couple to matter.
   - **These are not GR gravitational waves:** they are longitudinal, travel at c_P, and are gapped wherever u₀ ≠ 0.
4. **Flux and absorption.**
   - A travelling wave has flux F = c_P I Ṗ² and amplitude δu₀ = √(16πG c_P F)/(ωL*).
   - With baryons that respond, Iω² gains −(4πG)²ρ_b/ω². The absorbed fraction per radian is therefore ≤ ω_J²Ω_I²/ω⁴, and the
     heating per unit mass is ≤ 4πG Ω_I² F/(ω³c_P), independent of the gas density.

## Settling energy and luminosity
- **K1 PASS.** E_code(200) = 3.0033 against CFG696's 2.99995 for the zero start. E grows as (0.665 ≈ ⅔) ln S, the deep-MOND
  logarithm.
- **Per halo** (saturating W): E = ε M_b V_f², with ε = 1.6–2.3.

| halo | E (canonical / alt) | no-trap ceiling L, relaxed / merging (canonical) |
|---|---|---|
| galaxy, 6e10 M☉ | 6.8e51 / 7.7e51 J | 2.1e34 / 3.6e35 W |
| group, 1e12 M☉ | 4.9e53 / 5.5e53 J | 1.5e36 / 1.1e37 W |
| cluster, 1e14 M☉ | 3.6e56 / 4.1e56 J | 1.1e39 / 6.2e39 W |

- **Cosmic ceiling** (CFG630 K4): u_P ≤ 3.1e-15 J/m³, if every bit of settling energy ever went into P waves.
- **Trapping (S2): the main result of this lane.**
  - Baryons drive the settling at ω ~ 2π/t_dyn, which lies far below the local W″ gap, so the response is evanescent.
  - The radiated fraction is ≤ **10^-195 (group), 10^-223 (galaxy) and 10^-1790 (cluster)** at the most favourable corner
    (merging, L* = 1000 pc, c_P = 5e-3 c).
  - **CFG696 PDE ramp (S3).** Ramping the source by +10% over a time T cuts the radiated energy from 1 (a sudden step) to
    9.9e-2 (T = 30), 2.7e-3 (T = 100) and 6.1e-4 (T = 300), a slope of −2.2. Real settling corresponds to T ≥ 1e9 in code units.
  - **Reading.** CFG696's "relaxes by radiating" holds for a sudden start. Real, slowly assembling halos instead follow
    adiabatically: the settling energy is exchanged reversibly with the baryons, not radiated.

## Channels (worst corner)

| channel | signal at the worst corner | threshold | verdict |
|---|---|---|---|
| C1 gas heating, cluster ICM | 0 with trapping; no-trap ceiling 3.9e-9 W/kg | 0.1 × free-free cooling 7.2e-8 W/kg | **BELOW** (ceiling alone 5e-2) |
| C1 hot galactic halo | 2.5e-233 W/kg; ceiling 4.5e-10 | 1.4e-9 W/kg | **BELOW** (ceiling alone 0.31) |
| C2 disc heating, R0 | 1.4e-233 W/kg; full-dissipation ceiling 2.6e-10 | 0.1 σ_z²/10 Gyr = 1.3e-10 W/kg | **BELOW** (ceiling alone 2.0, see disclosures) |
| C3 double-pulsar decay | 3.8e-6 of the GR rate (L* 5.75 pc, c_P 5e-3 c) | room 9e-5 | **BELOW, 4.2e-2**; excludes c_P < 1.7e-3 c (L* 5.75), < 2.6e-4 c (100), < 5.6e-5 c (1000) |
| C4 PTA (SMBH binaries; settling) | escaped 0 (τ ≥ 1.9e4); free ratio up to 1.9e3 × GW | 0.1 of GW power | **BELOW** (trapped in the saturated nucleus) |
| C5 merging-cluster lensing | profile change 6.1e-6; centroid offset 0 | 5%; 10 kpc | **BELOW** (1.2e-4; fully damped ceiling 1.2 kpc = 0.12) |
| C6 light | no term | — | **REQUIRES NEW COUPLING**; via gravity δΦ/c² ≤ 1.3e-9 (1.3e-4 of 1e-5) |

- **C3 formula.** Pow/Pow_GR = (1/12)(c/c_P)³(c/ω_orb L*)². The binary has σ = 2r_M²/L*² = 2.3e-4, so it is screened and
  linear. The radiated frequency 2ω lies far above the Galactic gap.
- **C4 timing signature.** Settling sits about 7 decades below the nHz band, and SMBH-binary P waves cannot leave the nucleus.
  The waves would be longitudinal, so they could not mimic Hellings–Downs; in this window they do not reach Earth.

## Verdict
**No visible signature from P.**
- **Matter.** P acts on matter only as static gravity (the phantom, already scored elsewhere).
- **Light.** It would need a new coupling; none is added.
- **What the lane yields instead of a signature.**
  - A lower bound on the unfixed constant: c_P > 1.7e-3 c (double pulsar, L* = 5.75 pc).
  - A consistency floor: c_P must exceed the fastest bulk motions, about 1.5e-2 c for Bullet-like mergers. Below that the field
    cannot follow its sources statically.
  - c_P = c (CFG696's "free" option) makes every channel smaller still.

## Disclosures
- **C2 and hot-halo C1 rest on trapping.** Without trapping, the full-dissipation ceilings at L* = 1000 pc and c_P = 5e-3 c are
  2.0× (disc) and 0.31× (hot halo) of the thresholds. The BELOW verdicts therefore rest on S2's trapping. C2 also rests on
  adiabatic invariance: collisionless stars forced at ω ≫ Ω gain no secular heat at linear order.
- **C5 at the 5e-3 c floor.** The Bullet's 4500 km/s exceeds c_P there, and the in-phase analysis assumes v < c_P. The honest
  C5 floor is c_P ≳ 1.5e-2 c.
- **C4 gap.** The SMBH-binary gap uses the law background with stiffness folded in as a (1 − 2/σ) source shift. It is an
  approximation, not a solved profile.
- **Double-pulsar room.** The figure (0.999963 ± 0.000063) is quoted from the literature record (Kramer et al. 2021) and was
  not re-fetched. Eccentricity is neglected.
- **Approximations.**
  - Settling energies use an unscreened point mass.
  - K1 uses the cubic W, as CFG696 does.
  - The ramp test runs in a box that ends at s = 200; trapping beyond the box is the analytic S2.
- **The Newtonian action is incomplete.** Φ is instantaneous, and P-wave energy does not gravitate. The relativistic completion
  is open.
- **CFG630's budget** is class-A settling energy. It is used only as a ceiling.
- **Flag for the CFG69x lane, not acted on here.** In real halos the settling energy is not radiated (S2/S3). CFG696's ledger
  (energy lost = energy radiated) describes the sudden-start problem. For slow assembly the exchange is reversible work on the
  baryons. This bears on any reading of settling energy as feeding dark energy (CFG630).
