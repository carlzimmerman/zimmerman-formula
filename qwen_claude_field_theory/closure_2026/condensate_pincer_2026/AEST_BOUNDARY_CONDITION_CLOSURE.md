# AeST's boundary constant is not free, and the fixed value is excluded by KiDS-1000 (2026-09-02)

**Script:** `aest_boundary_condition_closure_2026.py` (8 checks, 0 FAIL, both a₀ footings, mutation control, both ways). Output: `.out`.

## What was already known (priority)

- **Skordis & Złośnik 2021** (PRL 127, 161302), verbatim: the quasistatic scalar equation carries a mass term μ² = 2K₂Q₀²/(2−K_B); "We require μ⁻¹ ≳ 1 Mpc so that MOND behavior … may still be attained in galaxies"; and, for the cosmological dust, w₀ = 8πG̃ρ̄₀/(4Q₀²K₂) with c²_ad = 2w₀/a³, "Observations give w ≲ 0.02 at a ∼ 10⁻⁴, hence w₀ ≲ 2×10⁻¹⁴." For a quadratic K these two sentences are the μ-pincer this programme found on the DBI chassis: w₀ = 4πGρ̄₀/(μ²(2−K_B)) ≲ 2e-14 ⇒ μ⁻¹ ≲ 1–1.4 kpc, against μ⁻¹ ≳ Mpc. Their escape is a non-quadratic K: of their three CMB-fitting parameter sets, only the "Exp" function (K₂ = 9.5e3, Q₀ = 1e-4, Z₀ = 1e-17; static μ⁻¹ ≈ 100 Mpc) satisfies the galactic bound, because its exponential wall keeps the dust cold away from the minimum. **Consequence for the published theorem paper:** the "18–300× above its own P(k) ceiling" pin is a pin of the DBI chassis (pinned R = Λ_D/Q₀), correctly scoped there; it does not extend to all K. The matching theorem itself (well = background at (1+z)³ = δ, same sound speed, any K) is unaffected.
- **Mistele, McGaugh & Hossenfelder 2023** (A&A 676, A100; arXiv:2301.03499) confronted AeST with the same Brouwer+ 2021 lensing relation: ρ_c = (m²/4πG f_G)(φ̇/Q₀ − Φ̂ − φ), the constant φ̇/Q₀ a per-galaxy "chemical potential" they left free; deviations from MOND set in inside the KiDS range unless m²/f_G ≲ 1 Mpc⁻² (rail ≥ 1e-13) or ≲ 1e-3 Mpc⁻² (to 1e-15); "we do not know of any mechanism that would result in these particular boundary conditions."

## What this script adds

The matching theorem supplies the mechanism: ρ_c is the conserved shift charge (n ∝ a⁻³), and a well holds the charge that fell into it. The charge delivered by the framework-native accretion (spherical collapse in the same gravity, external field e_N, the repo's `dark_charge_kids_lensing_gate`) fixes C. With the AeST spherical system solved outward (Φ̂, φ, ρ_c; total g = ν(g_N/a₀)g_N, Route A kernel), template lens M_b = 5e10 M☉, Brouwer+ 2021 isolated lenses (15 points, full covariance; rail g_bar ≥ 1e-13 = 7 points at 39–228 kpc), coherent amplitude ±0.3 dex profiled:

| | result |
|---|---|
| M0 mutation | m² → 0 reproduces the MOND-only χ² (28.0 / 27.2 on the rail) to 1% for any C. Note: C = Φ(0) is *not* zero charge; D = C − Φ turns negative outward (the VSB24 oscillatory regime / DS24 negative density). |
| H1a (MMH23, small m²) | m² ≤ 1e-3 Mpc⁻²: a C exists with Δχ²_rail = −0.5 to −4.9 (AeST ≥ MOND). |
| H1b (MMH23, large m²) | m² ≥ 10 Mpc⁻²: no C within Δχ² < +10 of MOND, rail (+14 to +36) or all 15 (+221 to +638). |
| H1c (a WORKS, both ways) | m² = 1e-2–1 Mpc⁻² with C free **improves** the rail by Δχ² ≈ −18 with 1.5–1.8 M_b of charge inside 250 kpc, but the same C wrecks the outer 8 points by +200 to +9e4. The rail's appetite for extra mass at 100–250 kpc cannot be fed by a Helmholtz charge. |
| H2a (charge fixed, the closure) | e_N = 0.03–0.1: Δχ²_rail ≥ **+106** for every m² in 1e-4…100 Mpc⁻², both footings (28 cases; +322 to +5680 at e_N = 0.03, +106 to +4095 at e_N = 0.1), amplitude pinned at its −0.30 dex edge every time. |
| H2b | m² ≤ 0.1 Mpc⁻² needs C − Φ(0) ≥ 45 MOND well depths (5–10 at m² = 1): the accreted charge cannot sit in quasistatic equilibrium in MMH23's allowed range; it is a pile-up, and the mass count is what lensing sees. |
| H2c | the arrangement-independent mass count: Δχ² = +689/+135 (canonical, e_N 0.03/0.1), +962/+235 (alt). |
| H2d (both ways) | e_N = 0.3 (unphysical for isolated lenses: needs a 1e11 M☉ neighbour within ~40 kpc) throttles the accretion to 6 M_b inside 100 kpc and the profile is absorbed by the amplitude budget (Δχ² = −6.6 canonical, +21 alt). |

**Verdict.** AeST at galaxy-lensing scales is closed for every m² once its boundary constant is set by charge conservation, at the external fields isolated galaxies actually sit in. Horn 1 (free C, m² ≥ 10) is MMH23's; horn 2 (fixed C, all m²) is this programme's. It rests on (a) the accretion estimate (spherical collapse with the EFE; no N-body of AeST exists, VSB24 say as much) and (b) the ±0.3 dex amplitude budget; the MOND-only baseline's own χ²/dof ≈ 4 on this rail is the older, separate question. Both ways stated.

**Footing.** Canonical a₀ = 9.36e-11 and alt 1.13e-10 give the same verdict at every line. **What this is not:** a discovery. It is a closure of the leading relativistic MOND theory's dark sector at the scales where its own authors said the theory should be tested, using the framework's one novel identity (the matching theorem) to remove the free constant that the previous confrontation had to leave open.
