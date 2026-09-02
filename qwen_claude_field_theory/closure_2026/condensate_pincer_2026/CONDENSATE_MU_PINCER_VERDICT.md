# The condensate μ-pincer: one relation closes the Ω-allocation fork (2026-09-02)

Script: `condensate_mu_pincer_2026.py` (18 checks, 0 FAIL; output in `.out`; ~4 s).

## The relation

The cluster-phase polytrope (`cluster_phase_2026/itemC`, p_d = (2πG/μ²)ρ_d², c_s² = 4πGρ_d/μ²) holds for any
shift-symmetric condensate at a quadratic minimum, on the cosmic background as well as in a static well (A1, A2).
For a condensate that carries the dark matter:

    c_s²(z) = 4πG ρ_dm(z) / (μ² c²) = 2.0×10⁻⁸ (μ⁻¹ / 1 Mpc)² (1+z)³        until saturation

with the same μ that governs the static Helmholtz equation. The dust's galaxy-scale behaviour and its cosmological
behaviour are therefore one number. The repo priced the two horns of the Ω-allocation fork separately
(`lyman_alpha_dust_ic_2026.py` Part F: "flips the verdict"); this script confronts them.

## Horn 1: the v9 DBI khronon's dust is Ω_dm

At β = 1 the DBI energy density decomposes exactly as ρ = Q₀n + M⁴√(1+ν²) (A3), the dust being the charge term.
With M⁴ = ρ_Λ this pins the DBI amplitude (A4):

    R = Λ_D/Q₀ = ν₀ Ω_Λ/Ω_dm = 2.6 ν₀

The repo bounded R as a free parameter (stage 69: R ≤ 1.5–3.1×10⁻⁶ at 3% on P(k=0.2); forest: ≤ 2.3×10⁻⁹).

| ν₀ | R pinned | R / stage-69 ceiling | c_s²(0) | μ⁻¹ equivalent | peak c_s² | z_peak | P(k=0.2, z=0) suppression |
|---|---|---|---|---|---|---|---|
| 2.14e-5 (floor) | 5.6e-5 | 18 | 1.2e-9 | 0.24 Mpc | 2.1e-5 | 31 | 44% |
| 1.0e-4 | 2.6e-4 | 169 | 2.6e-8 | 1.14 Mpc | 1.0e-4 | 18 | 100% |
| 1.77e-4 (ceiling) | 4.6e-4 | 299 | 8.1e-8 | 2.0 Mpc | 1.8e-4 | 15 | 100% |

The growth integrator (two-fluid, sub-horizon, DOP853; C0 reproduces the ΛCDM growth integral to 0.2%; C2
reproduces stage 69's calibration, 3.0% at k = 0.2 at R = 3.06×10⁻⁶) confirms the kill (C3). A "works" inside the
kill (B2): the pinned window maps to μ⁻¹ = 0.24–2.0 Mpc, exactly AeST/DS24's phenomenological 1 Mpc, and the wall does
keep the dust cold at recombination (c_s²(z_rec) ≤ 10⁻¹³, B3). The excess is entirely post-recombination.

Mutation: identifying the dust with the internal-energy branch M⁴(√(1+ν²)−1) instead of Q₀n forces ν₀ = 0.88 and
leaves R free. The pin exists only because the dust is the charge (repo filter F1).

## Horn 2: Ω_dm is a separate quadratic condensate χ with Helmholtz mass μ_χ

| μ_χ⁻¹ | c_s²(z_rec) | T²(k=1, z=3) | T²(k=10, z=3) | T²(k=0.2, z=0) | polytrope M_χ(<30 kpc)/M_b (canonical / alt) |
|---|---|---|---|---|---|
| 0.3 kpc | 2.3e-6 | 0.985 | 0.16 | 0.999 | no pressure support inside 30 kpc |
| 1 kpc | 2.6e-5 | 0.84 | 0.06 | 0.993 | no pressure support inside 30 kpc |
| 3 kpc | 2.3e-4 | 0.16 | 0.004 | 0.94 | no pressure support inside 30 kpc |
| 10 kpc | 2.6e-3 | 0.06 | 0.002 | 0.48 | 10.7 / 11.6 |
| 100 kpc | 0.15 | 0.000 | 0.000 | 0.02 | 0.33 / 0.36 |
| 200 kpc | 0.25 | 0.000 | 0.000 | 0.00 | 0.098 / 0.108 |
| 1 Mpc | 0.33 | 0.000 | 0.000 | 0.00 | 0.005 / 0.006 |

CMB coldness at the loose end of the GDM range (c_s²(z_rec) ≤ 10⁻⁵) needs μ_χ⁻¹ ≤ 0.6 kpc. Shielding an L* galaxy
(polytrope dust inside 30 kpc ≤ 30% of the baryons, both a₀ footings) needs μ_χ⁻¹ ≥ 200 kpc; ≤ 10% needs 1 Mpc.
Gap ≥ 300× (D1, D2). The loose forest yardstick (T² ≥ 0.5 at k = 10 h/Mpc, z = 3, the ~3 keV WDM half-mode class)
already fails at 3 kpc (C4).

Escape: a χ with its own DBI wall (own M_χ⁴, no pin). At the loose shield floor, every R passes at most one of the two
yardsticks (D3): R = 1.5e-6 gives T²(0.2, 0) = 0.96 but T²(10, 3) = 0.005; larger R fails P(k=0.2).

Mutation (C5): a constant c_s² equal to today's value at μ⁻¹ = 100 kpc leaves T²(10, 3) = 0.93. The kill is the
(1+z)³ history, not today's sound speed.

## The K-independent statement (Part F)

c_s² = K′/(QK″) depends on the excitation u alone. A static well imposes u_well = −Q₀Ψ (lapse relation, any K); the
background carries n(z) = K′(u(z)) = n₀(1+z)³. The well's dust overdensity is δ_well = n_well/n₀, so the background
passes through the well's state at (1+z_match)³ = δ_well with identical sound speed. For every K-shape tried
(u², u³, u⁴, u⁸) and every shield-compatible overdensity (δ_well ≤ 5000, z_match ≤ 16), the dust's sound speed at z = 3
is ≥ 20 km/s (F1), an order of magnitude above what the forest tolerates (the constant-c_s² control at 4 km/s already
loses 7% at k = 10). The dust at z = 3 is the dust in a galaxy well today. Pressure cannot keep Ω_dm out of galaxies.

## What this closes and what survives

- **Closed:** Horn 1, the v9 single-field dark sector (THE_COMPLETION §1.2 "dust job"), by P(k) at k ≥ 0.2 h/Mpc.
  The cluster phase-pinning paper's dark sector (ρ̄_d = Ω_dm ρ_c at μ⁻¹ = 1 Mpc, DOI 10.5281/zenodo.22242701 / 22254075)
  is this pinned Horn 1 at ν₀ = 8.8×10⁻⁵ and is therefore excluded as a cosmology; the static polytrope algebra stands.
- **Closed:** the pressure route to "no dark matter in galaxies" (the open 2d/virialisation front), for any K.
- **Survives:** the a₀(z) law of stage 17 (it needs only the trace khronon dust of D4, Ω_kd ≤ 4.4×10⁻⁷, where the pin
  gives Λ_D/Q₀ ≥ 33 and the sector is cosmologically invisible); MOND phenomenology; a cold, CDM-like Ω_dm, which
  double-counts with MOND in galaxies by the repo's own ξ = 1 numbers (2.7–4.4× overshoot).

Yardsticks were taken at their loose ends throughout (30% shield, 10⁻⁵ CMB, 0.5 forest, stage 69's own 3%).

## Footing check (2026-09-02, after the objection "stop playing high priest of ΛCDM")

The growth yardsticks above assume the dark fluid carries structure by Newtonian linear growth. Whether that is the
framework's own footing or ΛCDM's was tested in `mond_growth_framework_footing_2026.py` (7 checks, 0 FAIL):

- **The framework's own derived cosmological kernel argument** (`prep_2026/mi_covariant_pt`, 17/17) carries a dS-Unruh
  Hubble floor, X = Z²(H/H_Λ)² + (a_pec/a₀)². With it, MOND changes linear growth by at most 6% at every k, z and both
  a₀ footings (1a). The Newtonian yardsticks are therefore the framework's footing, and the pinned Horn 1 underproduces
  the measured clustering by 40–600× at k ≥ 0.2 h/Mpc (1c).
- **Without the floor** (a Nusser/Sanders MOND cosmology, which the framework's derivation rejects): the linear per-mode
  boost model put the pinned warm dust plus MOND-grown baryons within 2× of the measured z = 3 power at k = 1–10 h/Mpc (1b).
  **WITHDRAWN 2026-09-02 (same day):** the per-mode model ignores the external-field effect of the large-scale modes; the exact
  1-D sheet N-body (`mond_sheet_nbody_forest_gate_2026.py`) finds a 1000–5000× shortfall instead. It overproduces the k ≤ 0.2 h/Mpc power 5–13× at z = 3 and makes 100-Mpc
  scales nonlinear by z = 0 (1b′). No μ⁻¹ in 0.1–5 Mpc fixes the shape: the large-scale overproduction is μ-independent (1d).
- **No dark field at all** (Ω_m = Ω_b, MOND from z = 20): with the floor, nothing grows (2a); without it, the z = 3
  spectrum is tilted 30–200× in power between k = 0.05 and 10 h/Mpc relative to the measured shape, for every IC
  normalisation (2b).

Nothing in the framework boosts k ≳ 1 h/Mpc without also boosting k ≈ 0.05 h/Mpc. Structure needs an Ω_dm-worth of
something that clusters on 100-Mpc scales without a MOND boost, and the pincer says that something is cold above ~1 kpc.
